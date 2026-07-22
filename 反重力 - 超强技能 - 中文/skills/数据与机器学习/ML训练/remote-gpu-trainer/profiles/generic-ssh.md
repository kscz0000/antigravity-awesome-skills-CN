---
platform: generic-ssh        # 通用 SSH + Slurm / K8s / Colab-Kaggle 默认 profile
kind: ssh-rental + batch     # 标准计算集群或 notebook 服务；非商业 GPU 租赁平台
meter_stop_verb: per-subprofile   # scancel / kubectl delete / N/A（notebook 计时器）— 无平台计费
meter_stop_irreversible: false    # 作业可取消并重启；集群配额恢复
detach_primitive: tmux      # tmux/screen/nohub 在 SSH 主机上；Slurm 作业由调度器守护；notebook 原生分离
spot_available: per-subprofile    # Slurm: 是（分区可能为 preemptible）；K8s: 是（spot 节点池）；notebook: 否
spot_grace: per-subprofile       # Slurm: SIGTERM→SIGKILL（可配置）；K8s: 30s 优雅终止；notebook: N/A
shared_fs: per-subprofile        # Slurm: $HOME + 共享文件系统；K8s: PersistentVolume；notebook: Google Drive / /kaggle/working
inode_cap: per-subprofile        # 取决于共享文件系统配额；HPC 上常见陷阱（U7）
free_egress: per-subprofile      # 通常直连出站；Colab/Kaggle 在空闲配额内免费
china_mirror_needed: false  # 通用 profile 不假设 GFW — 需要时应用 references/china-network.md
host_driver_cuda_max: host-dependent   # 驱动/CUDA 版本随集群/主机变化 — 从机器上读取
local_nvme: per-subprofile        # Slurm: 通常是 $TMPDIR / node-local NVMe；K8s: emptyDir；notebook: N/A
---

# 通用 SSH / Slurm / K8s / Colab-Kaggle — 默认 Profile

一句话定位：在**非商业 GPU 租赁平台**上运行分离 GPU 作业的基底 — 大学/公司 HPC 集群
(Slurm)、Kubernetes GPU 节点池、以及 Google Colab/Kaggle notebook — 差异在于什么停止"计费"（配额/信用而非金钱）、什么在作业取消后存活、以及如何守护一个长运行的训练。本 profile 定义一个**基线**行为 + 三个 **thin diff**（Slurm / K8s / Notebook），每个仅覆盖与基线的差异。通用陷阱在此不重复 — 参见 `references/gotchas_universal.md`。

> **前置告知用户（原则 #10）：** ⚠️ 提醒 — 这里没有商业计费，但有 **配额/信用时钟**（Colab 计算单元、Kaggle GPU 配额、Slurm fairshare 衰减）和 **静默会话超时**（Colab 12h / Kaggle 9h / 断开的 SSH）。守护进程设计与商业平台一样关键。

快速跳转：`grep -in '<keyword>' profiles/generic-ssh.md`。

## 目录
1. 启动 — 基线 + 三个子 profile
2. 存储模型 — 生存矩阵
3. 网络
4. SPOT / 中断 + 恢复
5. 拆除 / 计费（配额）
6. 守护工具
7. 主要陷阱（GEN1–GEN8 基线 + SLURM1–SLURM5 + K8S1–K8S6 + NB1–NB5）+ 平台专属调试
8. 脚本覆盖

---

## 1. 启动

### 基线（通用 SSH 主机）

SSH 到一台 Linux 机器（大学服务器、公司 DGX、裸金属租赁机），其上有 NVIDIA GPU 和
足够新的 driver。没有平台提供的控制台或 API — 直接 `ssh` + `tmux` + 运行。环境由
管理员或您的 dotfiles 管理。

**环境契约：** 驱动/CUDA/PyTorch 版本**随主机变化** — 从机器上读取（`nvidia-smi`、
`python -c "import torch; ..."`），而非假定一个数字。"预构建基础即环境"原则（原则 #2）在此含义不同：如果您对机器有持久的 root 访问权限，构建自定义环境是可接受的（不同于租赁机），但**仍建议**一个可复现的 `requirements.txt`/lock 文件 + venv 或 conda `--prefix`，这样如果管理员升级了系统 CUDA，您的环境不会静默损坏。

→ **验证：** `ssh <host> 'python -c "import torch;print(torch.cuda.is_available())"'` 返回 `True`。

### Thin Diff: Slurm

HPC 集群调度器。不直接 `ssh` 到 GPU 节点 — 通过 Slurm 提交作业：

```bash
sbatch --gpus=1 --time=24:00:00 --output=slurm-%j.out my_train.sh
# 或交互式：
srun --gpus=1 --time=2:00:00 --pty bash
```

- **登录节点 → 计算节点。** 您 SSH 到一个*登录节点*（无 GPU），通过 `sbatch`/`srun` 请求 GPU。代码和数据驻留在**共享文件系统**（`$HOME`，`$SCRATCH`）上，两个节点都可见。
- **调度器守护进程。** `sbatch` 提交的作业由 Slurm 守护 — 没有 tmux 需求，SSH
  可以断开。交互式 `srun --pty` 会话在 SSH 断开时**确实会消亡** — 对于长作业使用 `sbatch`。
- **分区/队列。** GPU 以*分区*（如 `gpu-a100`、`gpu-interactive`）提供；一些分区可能是
  **preemptible**（类 spot）— 被更高优先级作业抢占。检查 `sinfo -p <partition>` 和 `squeue -u $USER`。

**环境契约：** 通常是 **Lmod 模块** — `module load cuda/12.1 python/3.11 pytorch/2.3` —
在 `.bashrc` 或作业脚本中加载。模块版本变化 ⇒ 作业脚本中的固定版本，而非
`module load python`（浮动的）。一些集群提供 **Spack** 或 **conda** — 相同原则：可复现锁定文件，而非浮动的 `latest`。

### Thin Diff: Kubernetes (K8s)

GPU 节点池由集群管理员提供。通过 **Pod 清单**请求 GPU：

```yaml
apiVersion: v1
kind: Pod
metadata: { name: train-job }
spec:
  containers:
  - name: train
    image: pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime
    resources: { limits: { nvidia.com/gpu: 1 } }
    volumeMounts: [{ name: data, mountPath: /data }]
  volumes: [{ name: data, persistentVolumeClaim: { claimName: my-pvc } }]
```

- **Pod 即实例。** Pod 是调度单位；**Pod 删除 = 实例删除**（数据在
  PersistentVolume 上存活 — 见 §2）。
- **kubectl exec** 进入运行中的 pod，或使用 **Kubeflow / Jupyter on K8s** 获取 notebook 风格访问。
- **Spot 节点池。** 集群可能有按需和 spot 节点池 — spot pod 可以**以 30 秒优雅终止**被驱逐。与 `SpotInterrupt` 相同的恢复脊柱（原则 #8）适用于此处。

**环境契约：** 容器镜像即环境 — 使用官方 PyTorch 镜像或自定义构建。**不要**在
运行中的 pod 内 `pip install`（重启后丢失）— 通过 `requirements.txt` 构建新镜像层，或挂载一个持久卷并安装到那里。

### Thin Diff: Colab / Kaggle Notebook

托管 Jupyter notebook，带免费/付费 GPU 时间。

- **Colab** — Google 账号，12 小时免费 GPU 上限（T4），**Compute Units** 用于付费
  A100/L4。输出写入 `/content`（临时）或 Google Drive（通过挂载持久）。无 SSH daemon — notebook 内终端是受限的。
- **Kaggle** — 每**周 30 小时 GPU** 配额（T4 x 2 / P100）；输出写入 `/kaggle/working`（持久，可下载）；数据集来自 `/kaggle/input/`。会话超时因不活动而变 — **约 9 小时**最大运行时间（已验证 kaggle.com/docs 2026-06）。无 SSH。

**环境契约：** notebook 镜像即环境 — `pip install` 在运行时持久于会话中，但**重启后丢失**
（除非写入持久存储）。对于可复现性，将 `pip freeze > requirements.txt` 保存到 Drive/Kaggle working。

---

## 2. 存储模型  *(生存矩阵 — 原则 #4)*

### 基线

标准 Linux 机器 — **所有存储通常跨重启持久**（不像 AutoDL 的关机擦除 `/root`），但**管理员维护/硬件故障**可能擦除本地磁盘。安全默认：检查点到独立存储
（NFS、S3、本地工作站）。

| 层级 | 路径 | 重启后存活？ | 硬件故障/维护后存活？ | 备注 |
|---|---|---|---|---|
| 本地磁盘 | `/home`, `/data` | 是 | **否** | 管理员维护可能擦除；检查点到机外 |
| NFS/共享 | 挂载点 | 是 | 取决于 NFS 服务器 | 通常冗余；但配额/inode 有限 |

### Slurm Thin Diff

- **$HOME** — 共享文件系统，跨登录和计算节点可见，跨作业**持久**。
- **$SCRATCH / $TMPDIR** — **每作业临时存储**，作业结束后擦除。将大型数据集暂存到
  `$TMPDIR`（通常是节点本地 NVMe）以提升 IO，但**在作业结束时将结果写回 $HOME 或共享存储**。
- **配额** — `$HOME` 通常有严格配额（50 GB–500 GB）；`$SCRATCH` 更宽松但定期清理。`df -i` 对共享文件系统至关重要（U7）。

| 层级 | 路径 | 作业结束后存活？ | 备注 |
|---|---|---|---|
| $HOME（共享 FS） | `/home/<user>` | 是 | 配额受限；inode 陷阱（U7） |
| $SCRATCH（共享 FS） | `/scratch/<user>` | 是（但定期清理） | 大型数据集存放处；非永久 |
| $TMPDIR（节点本地） | `/tmp` 或 NVMe | **否 — 作业后擦除** | 快速暂存；作业结束时写回 |

### K8s Thin Diff

- **PersistentVolume (PV) / PersistentVolumeClaim (PVC)** — 持久存储，**跨 Pod 删除存活**。绑定到
  PVC 的数据在 pod 重建后存活。存储类（`standard`、`premium-rwo` 等）决定性能和冗余。
- **emptyDir** — **每 Pod 临时**，pod 删除时擦除。适合暂存，不适合检查点。
- **ConfigMap / Secret** — 小型只读配置注入 — 不用于数据。

| 层级 | 路径 | Pod 删除后存活？ | 备注 |
|---|---|---|---|
| PVC 挂载 | `/data`（自定义） | **是** | 唯一安全的检查点目标 |
| emptyDir | `/tmp`（自定义） | **否** | 仅暂存 |
| 容器层 | 容器内 | **否** | 重启后擦除 |

### Notebook Thin Diff

- **Colab** — `/content` 是临时的；**Google Drive**（`drive.mount('/content/drive')`）持久。Drive 有
  15 GB 免费配额；Google One 扩展。
- **Kaggle** — `/kaggle/working` 持久（可下载）；`/kaggle/input/` 只读数据集。**输出大小限制约 20 GB**（已验证 kaggle.com/docs 2026-06）。

| 层级 | 路径 | 会话超时后存活？ | 备注 |
|---|---|---|---|---|
| Colab 临时 | `/content` | **否** | 默认工作区 — 永远不是检查点目标 |
| Colab Drive | `/content/drive/MyDrive` | 是 | 15 GB 免费；IO 慢于本地 |
| Kaggle working | `/kaggle/working` | 是（可下载） | 约 20 GB 上限 |
| Kaggle input | `/kaggle/input` | 是（只读） | 数据集；不可写 |

---

## 3. 网络

### 基线

直连出站到 HF/GitHub/PyPI — 无代理需求（除非在 GFW 之后，此时
`references/china-network.md` 适用）。防火墙规则由管理员管理 — 通过 SSH 隧道暴露服务。

### Slurm Thin Diff

登录节点通常有**完整出站**；计算节点可能有**限制性出站**（无互联网） — 通过登录节点代理
或预暂存数据到共享文件系统。**不要**假设计算节点能 `pip install`。

### K8s Thin Diff

Pod 出站由 **NetworkPolicy** 和集群配置控制。大多数集群允许完整出站；受限集群可能需要
**NAT 网关**或 **HTTP 代理**。为 `pip install` / `huggingface-cli download` 测试出站。

### Notebook Thin Diff

**无 SSH daemon** — 通过 notebook UI 访问。Colab 有 **Google Drive API** 访问；Kaggle 有
**Kaggle API** 访问。两个平台出站均直连 HF/PyPI（美国/全球）。在中国使用时
（`references/china-network.md`），Colab 需要 VPN；Kaggle 可能不稳定。

---

## 4. SPOT / 中断 + 恢复  *(原则 #7/#8)*

### 基线

**无 spot 层级** — 标准硬件，无运行中驱逐。中断来自硬件故障或管理员维护。
checkpoint-to-durable + load-latest 仍然是正确的脊柱，但间隔通常由您自己的重启计划驱动
而非外部抢占。

### Slurm Thin Diff

- **Preemptible 分区** — 一些 GPU 分区标记为 preemptible（低优先级）。Slurm 发送
  **SIGTERM**，然后可配置宽限期后发送 **SIGKILL**。默认宽限期因集群而异 — 检查
  `scontrol show partition <name>` 或询问管理员。
- **检查点 + 重新提交** — 被抢占的作业应将检查点写入 `$HOME` 并以 `sbatch` 重新提交自身
  （或使用脚本封装器）。`references/spot-resilience.md` 中的间隔公式适用
  — μ 是被抢占之间的预期时间（检查集群历史或询问管理员）。
- **Fairshare 衰减** — Slurm fairshare 随时间衰减 — 使用后立即重新提交的作业可能等待更长时间。
  对于关键路径作业，在低使用率窗口（夜间/周末）提交。

### K8s Thin Diff

- **Spot 节点池** — 运行在 spot/抢占式实例上的节点可以在 **30 秒优雅终止** 内被回收。
  Pod 收到 SIGTERM，有 30 秒完成并退出。**检查点必须在 <30 秒内完成**（通常意味着增量/快速检查点）。
- **Pod 干扰预算 (PDB)** — 可以限制同时被驱逐的 pod 数量 — 但这仅帮助批处理部署，非单个训练 pod。
- **恢复：** 重建 pod 从 PVC 加载检查点 — 与原则 #8 相同的 load-latest-on-startup 脊柱。

### Notebook Thin Diff

- **会话超时** — Colab：12 小时（免费 T4），Compute Units 可延长；Kaggle：~9 小时。
  这些是确定性的硬上限，不是随机驱逐 — 在窗口前规划检查点。
- **空闲断开** — Colab 可能在空闲时断开（浏览器标签页不活跃）— 使用 **防空闲技巧**
  或保持标签页活跃。
- **恢复：** 重新连接 notebook 并从 Drive/working 加载最新检查点。因为超时是已知时间，
  检查点间隔可以被规划（例如每 30 分钟在 12 小时窗口内）。

---

## 5. 拆除 / 计费（配额） *(原则 #9 + 铁律)*

**没有商业计费 — 但有配额/信用消耗，同样需要铁律门控。** "浪费 GPU 小时"和"浪费美元"
在效用上等价。

| 子 Profile | "停止计费"动词 | 配额/信用影响 |
|---|---|---|
| 基线 SSH | `Ctrl+C` / 关闭 tmux | 无 — 硬件独占 |
| Slurm | `scancel <jobid>` | 释放 fairshare 配额；作业重新排队 |
| K8s | `kubectl delete pod <name>` | 释放 GPU 资源；PVC 数据存活 |
| Colab | 断开会话 | 消耗计算单元（付费）或免费 GPU 时间 |
| Kaggle | 结束会话 | 消耗每周 GPU 配额（30h/周） |

**铁律仍然适用：** 在检查点**已 pull 到本地并通过加载验证**，且用户已批准操作之前，不得
`scancel`、`kubectl delete`、或结束 notebook 会话。配额和美元一样宝贵。

---

## 6. 守护工具

### 基线

`tmux` / `screen` / `nohup` — 标准工具。SSH 断开后 tmux 存活；在管理重启后不存活（检查点到持久存储仍然是脊柱）。

### Slurm Thin Diff

**`sbatch` 作业由调度器守护** — 不需要 tmux。交互式 `srun` 会话在 SSH 断开后消亡 — 对于长作业始终使用 `sbatch`。如果需要交互式 + 持久：`srun ... --pty tmux` 给出调度器守护 + tmux 可重连。

### K8s Thin Diff

**Pod 是调度单位** — `kubectl exec -it <pod> -- tmux` 给出 tmux 在 pod 内。Pod 删除杀死 tmux
+ 所有进程。长作业应作为 **Kubernetes Job**（`backoffLimit: 0`，`restartPolicy: Never`）提交
而非手动 pod — Job 控制器在 pod 失败时重新创建 pod（但**不**恢复训练状态 — 检查点加载是您的责任）。

### Notebook Thin Diff

**Jupyter kernel 是"守护进程"** — 只要 notebook 会话活跃，内核就运行。
防空闲技巧保持会话活跃：Colab 中 `while True: pass` 或 JavaScript 计时器。Kaggle notebook
在 `Commit` 运行模式下自动执行，有 9 小时上限。

---

## 7. 主要陷阱  *(基线 + thin diff; 通用陷阱 → `references/gotchas_universal.md`)*

### 基线陷阱 (GEN1–GEN8)

- **GEN1 — 驱动/CUDA 不匹配静默降级到 CPU。**
  症状：`torch.cuda.is_available()` 返回 `False` 或 `RuntimeError: CUDA out of memory` 即使物理 GPU 存在。→ 根因：宿主 driver 太旧，或 PyTorch wheel 的 CUDA 版本与 driver 不匹配。→ 修复：`nvidia-smi` 读取 driver CUDA 版本（右上角）；安装匹配的 torch
  构建（`pip install torch --index-url https://download.pytorch.org/whl/cu121`）。CUDA 三角
  → U28 in `references/gotchas_universal.md`。

- **GEN2 — `nohup` 输出静默截断或丢失。**
  症状：`nohup.out` 为空或截断；Python 输出未刷新。→ 根因：Python stdout 缓冲在与 nohup 重定向时 — 输出保留在缓冲区中，进程被杀死时丢失。→ 修复：
  `python -u train.py`（无缓冲）或 `PYTHONUNBUFFERED=1`；或 `nohup python -u train.py >log 2>&1 &`。

- **GEN3 — 共享机器上的 GPU 内存争用。**
  症状：OOM 错误，即使您是唯一的用户；或 `nvidia-smi` 显示其他人的进程在消耗 GPU 显存。→ 根因：多用户共享 GPU — 您的作业被其他人的进程饿死。→ 修复：独占请求 GPU
  （Slurm：`--gpus=1`；K8s：`nvidia.com/gpu: 1` limit）；在启动前检查 `nvidia-smi` 是否
  GPU 干净；如果是共享且无独占访问，使用 `CUDA_VISIBLE_DEVICES` 选择空闲 GPU。

- **GEN4 — 大文件同步在慢速 NFS 上静默失败或损坏。**
  症状：`rsync`/`scp` 完成但文件损坏或比预期小。→ 根因：NFS 在大文件传输时断开或
  超时；部分写入被缓存。→ 修复：`rsync -avz --checksum`（传输后验证）；`md5sum`
  源和目标；将大传输拆分为较小批次。

- **GEN5 — 磁盘配额在训练期间耗尽（共享 FS inode 陷阱）。**
  症状：`OSError: [Errno 28] No space left on device` 但 `df -h` 显示空闲空间。→ 根因：
  inode 配额耗尽（太多小文件 — HF 缓存、检查点碎片）。→ 修复：`df -i <mount>` 检查
  inode 使用；清理 HF 缓存（`huggingface-cli delete-cache`）；检查点修剪策略。通用
  U7 → `references/gotchas_universal.md`。

- **GEN6 — 环境漂移在重启后静默破坏训练。**
  症状：相同代码 + 相同数据产生不同结果；import 错误在"未更改任何东西"后出现。→ 根因：
  管理员升级了系统 CUDA/driver/Python，或浮动 `module load` 解析到新版本。→ 修复：
  在 `requirements.txt`/lock 文件中锁定依赖版本；在作业脚本中固定模块版本
  （`module load cuda/12.1` 而非 `module load cuda`）；在训练前 `pip freeze > freeze.txt`。

- **GEN7 — SSH 超时杀死交互式作业（非 tmux）。**
  症状：在 SSH 终端中运行的训练在断开连接后消失。→ 根因：SSH 会话终止时，其子进程收到
  SIGHUP。→ 修复：始终在 `tmux`/`screen` 中运行，或使用 `nohup`；永远不要在裸 SSH shell 中运行长作业。

- **GEN8 — Node-local NVMe 未在 Slurm 作业结束时清理。**
  症状：后续作业发现前一个作业的 `$TMPDIR` 数据；或磁盘在多次作业后填满。→ 根因：
  `$TMPDIR`（node-local NVMe）不被 Slurm 自动清理 — 依赖 `epilog` 脚本（可能未配置）。→ 修复：
  在作业脚本中手动清理（`rm -rf $TMPDIR/*` 在开头和结尾）；不要假设 `$TMPDIR` 是空的。

### Slurm Thin Diff 陷阱 (SLURM1–SLURM5)

- **SLURM1 — 在登录节点上运行 GPU 训练（禁令）。**
  症状：登录节点管理员警告/封禁；训练极慢（无 GPU）。→ 根因：登录节点是共享的，无 GPU — 仅用于
  轻量任务（编辑、`sbatch`、编译）。→ 修复：始终通过 `sbatch`/`srun` 提交 GPU 作业到计算节点。

- **SLURM2 — 长作业超过 `--time` 限制被杀。**
  症状：作业在恰好请求的时间限制处被 SIGTERM + SIGKILL。→ 根因：Slurm 强制执行时间限制 — 没有宽限。
  → 修复：设置 `--time` 为预期运行时间的 1.5x–2x；实现周期性检查点以便 SIGTERM 处理器可以保存状态
  （如果集群启用 `--signal=B:USR1@300` — 在 SIGKILL 前 5 分钟发送 SIGUSR1）。

- **SLURM3 — 交互式 `srun` 会话在 SSH 断开时消亡。**
  症状：`srun --pty bash` 会话在 SSH 断开后丢失。→ 根因：`srun` 绑定到 SSH 会话 — 断开时
  Slurm 取消作业。→ 修复：对于长作业使用 `sbatch`；对于需要交互+持久：`srun ... --pty tmux`。

- **SLURM4 — Preemptible 作业静默被杀，无宽限。**
  症状：低优先级作业在无 SIGTERM 的情况下消失。→ 栨因：某些集群配置中 preemption 使用
  `SIGKILL` 而非 `SIGTERM`（检查 `scontrol show partition`）。→ 修复：持续检查点到
  `$HOME`（而非 `$TMPDIR`）；实现快速增量检查点；使用 `--requeue` 标志让 Slurm 自动重新排队
  被抢占的作业。

- **SLURM5 — `$SCRATCH` 定期清理删除旧数据。**
  症状：`$SCRATCH` 中的数据集/检查点突然消失。→ 根因：HPC 中心通常每周/每月清理 `$SCRATCH`
  中超过 N 天的文件。→ 修复：仅将 `$SCRATCH` 用于活跃作业数据；将重要结果移到 `$HOME` 或
  外部存储；阅读集群的 scratch 清理策略。

### K8s Thin Diff 陷阱 (K8S1–K8S6)

- **K8S1 — Pod 内 `pip install` 在重启后丢失。**
  症状：容器重启后安装的包消失。→ 根因：容器层是临时的 — 重启恢复到镜像状态。→ 修复：
  安装到持久卷（`pip install --target /data/venv`）或在 CI 中构建新镜像。

- **K8S2 — GPU 资源请求格式错误导致 CPU-only 调度。**
  症状：Pod 运行在 CPU 节点上；`nvidia-smi` 不可用。→ 根因：资源键 `nvidia.com/gpu` 必须在
  `limits` 中（不是 `requests` — 尽管通常设置两者相等），且节点必须有安装的 GPU device plugin。→ 修复：
  在 `limits` 和 `requests` 中都设置 `nvidia.com/gpu: 1`；验证节点有
  `nvidia.com/gpu` allocatable（`kubectl describe node <name>`）。

- **K8S3 — ImagePullBackOff 阻止 Pod 启动。**
  症状：Pod 停在 `ImagePullBackOff` 或 `ErrImagePull`。→ 根因：私有镜像需要
  `imagePullSecrets`；或镜像标签不存在；或节点没有磁盘空间拉取。→ 修复：
  添加 `imagePullSecrets` 到 pod spec；验证镜像存在（`docker pull` 本地）；检查节点磁盘。

- **K8S4 — OOMKilled — 容器内存限制太低。**
  症状：Pod 以 `OOMKilled` 退出；训练在内存密集操作（数据加载、大 batch）时崩溃。→ 根因：
  容器内存 `limit` 太低 — PyTorch 数据加载器和工作进程可能使用比预期更多的 RAM。→ 修复：
  增加 `resources.limits.memory`；减少 `num_workers`；使用 `__pycache__` 内存映射；
  监控 `kubectl top pod`。

- **K8S5 — Spot pod 在 30 秒优雅终止内被回收 — 检查点太慢。**
  症状：Spot pod 被驱逐但检查点未完成（30 秒内）。→ 根因：完整检查点需要 >30 秒（大模型、慢 PVC）。→ 修复：实现快速增量检查点（仅保存 diff）；在 SIGTERM 处理器中
  触发检查点；使用 `terminationGracePeriodSeconds` 延长窗口（如果集群允许 — 最大 600 秒）。

- **K8S6 — PVC 在所有 Pod 释放前无法删除（Terminating 卡住）。**
  症状：`kubectl delete pvc <name>` 卡在 `Terminating`。→ 栄因：PVC 有活跃的挂载 pod — 必须先删除 pod。→ 修复：先 `kubectl delete pod <name>`；等待 pod 终止；然后 PVC 删除完成。
  Reclaim policy `Retain` 在 PVC 删除后保留数据；`Delete` 擦除它 — 检查 storage class。

### Notebook Thin Diff 陷阱 (NB1–NB5)

- **NB1 — Colab 12 小时 / Kaggle 9 小时会话超时无报错杀死训练。**
  症状：训练在恰好 12 小时 / 9 小时消亡；无 traceback。→ 根因：硬性会话超时 — 无法延长
  （Colab 免费）或需要 Compute Units（Colab 付费）。→ 修复：在超时前每 30 分钟检查点到
  Drive/Kaggle working；Colab 付费 A100 有更长限制（~24 小时，Compute Units 允许）。

- **NB2 — Colab Google Drive IO 极慢，瓶颈训练。**
  症状：检查点到 Drive 花费分钟而非秒；epoch 间出现巨大 IO 停顿。→ 栨因：Drive FUSE 挂载是
  网络文件系统，延迟远高于本地。→ 修复：检查点到 `/content`（本地临时），然后定期
  `cp` 到 Drive；将检查点频率与 Drive IO 速度匹配（非每个 step）。

- **NB3 — Kaggle `/kaggle/working` 20 GB 上限截断输出。**
  症状：大型输出文件写入失败或被截断。→ 根因：Kaggle 输出有约 20 GB 上限。→ 修复：
  修剪检查点（仅保留 best + latest）；将中间结果流式传输到外部存储（S3/GCS）；
  使用 `kaggle datasets create` 保存大型输出。

- **NB4 — Colab 空闲断开（浏览器标签页不活跃）。**
  症状：Colab 会话在标签页最小化约 90 分钟后断开。→ 根因：Google 检测空闲会话并回收资源。→ 修复：保持标签页活跃（防空闲 JS 计时器：`setInterval(() => { document.querySelector('#connect').click() }, 60000)`）；或使用 **Colab Pro** 延长空闲超时。

- **NB5 — `pip install` 在 notebook 重启后丢失。**
  症状：重启后包消失；`import` 失败。→ 根因：安装写入临时容器层 — 重启恢复到镜像状态。→ 修复：
  Colab：将 `!pip install <pkg>` 放在 notebook 第一个单元格中（每次重启重新运行）；
  Kaggle：同样方法。将 `requirements.txt` 保存在 Drive/working 中以复现。

### 平台专属调试

- **GEN/SSH：** `nvidia-smi` → driver + GPU 健康；`nvtop` 实时监控；`htop` CPU/RAM；
  `df -h` 和 `df -i` 磁盘/inode；`iostat -x 1` IO 瓶颈。
- **Slurm：** `squeue -u $USER` 作业状态；`scontrol show job <id>` 详细信息；`sacct -j <id>`
  历史资源使用；`seff <id>` 效率摘要。被抢占的作业检查 `sacct -j <id> -n -X | grep PREEMPTED`。
- **K8s：** `kubectl get pods` 状态；`kubectl describe pod <name>` 事件和资源；`kubectl logs <name>`
  容器输出；`kubectl top pod` 实时资源使用。`Events` 部分显示调度失败、OOMKills 等。
- **Notebook：** Colab：`!nvidia-smi` 在单元格中；`!df -h` 磁盘；运行时 → 查看系统日志。Kaggle：
  单元格中的 `!nvidia-smi`；设置 → 查看会话信息。

---

## 8. 脚本覆盖

按子 profile 参数化 `scripts/` 模板：

```sh
# --- 基线 SSH ---
DATA_DIR=/home/<user>/data          # 占位符
DURABLE_DIR=/home/<user>/checkpoints # 占位符 — 持久存储
SCRATCH=/tmp
HF_HOME=/home/<user>/.cache/huggingface
PROXY_HOOK=                          # 无 — 直连出站
CRED_FILE=""                         # 环境变量，非文件
DETACH=tmux

# --- Slurm ---
DATA_DIR=$SCRATCH                    # 作业暂存；$SCRATCH 自动设置
DURABLE_DIR=$HOME/checkpoints        # $HOME 跨作业持久
SCRATCH=$TMPDIR                      # 节点本地 NVMe（快，作业后擦除）
HF_HOME=$HOME/.cache/huggingface     # HF 缓存在共享 FS 上
PROXY_HOOK=                          # 可能需要通过登录节点代理
CRED_FILE=""                         # 环境变量
DETACH=sbatch                        # 调度器守护 — 无 tmux 需求

# --- K8s ---
DATA_DIR=/data                       # PVC 挂载点
DURABLE_DIR=/data/checkpoints        # PVC — 跨 pod 删除持久
SCRATCH=/tmp                         # emptyDir — pod 删除时擦除
HF_HOME=/data/.cache/huggingface     # PVC 上
PROXY_HOOK=                          # 集群依赖 — 可能需要 NAT 网关
CRED_FILE=""                         # Secret 挂载为环境变量
DETACH=Job                           # Kubernetes Job 控制器守护

# --- Notebook (Colab/Kaggle) ---
DATA_DIR=/content                    # Colab 临时；Kaggle: /kaggle/input
DURABLE_DIR=/content/drive/MyDrive/checkpoints   # Colab Drive；Kaggle: /kaggle/working
SCRATCH=/tmp
HF_HOME=/content/.cache/huggingface  # Colab 临时；考虑重定向到 Drive
PROXY_HOOK=                          # 直连出站
CRED_FILE=""                         # 用户/secrets 管理
DETACH=kernel                        # Jupyter kernel 是守护进程
```

所有子 profile 通用：凭据仅通过环境变量名引用 — 永远不要内联密钥。在 K8s 上，使用
**Secret** 对象注入环境变量。在 Slurm 上，使用 `~/.netrc` 或环境模块。在 Notebook 上，使用
平台 secrets（Colab 用户数据 / Kaggle 秘密值）。
