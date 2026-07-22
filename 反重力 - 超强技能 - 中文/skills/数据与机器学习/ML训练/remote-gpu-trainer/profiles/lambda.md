---
platform: lambda
kind: cloud-api               # REST API / web 控制台 / SSH 到标准 Ubuntu VM
meter_stop_verb: terminate    # 唯一停止计费的动作；sudo shutdown 不停止计费
meter_stop_irreversible: true # terminate 抹除本地 NVMe — 没有 stop/suspend 状态
detach_primitive: tmux        # 标准 Ubuntu；tmux/screen/nohup，如缺失则安装
spot_available: false         # 无 spot/抢占层级；中断来自启动时的容量问题
spot_grace: n/a               # 无运行中驱逐 → 无宽限窗口
shared_fs: true               # 区域锁定的 NFS 文件系统，仅在启动时挂载
inode_cap: none               # 无文档化 inode 上限；仅有 GiB 配额
free_egress: true             # 实例和文件系统均无入站/出站费用
china_mirror_needed: false    # 美国/全球云，直连出站；无平台代理
host_driver_cuda_max: lambda-stack-dependent  # Lambda Stack 捆绑 driver+CUDA+PyTorch；版本随发布变化 — 在机器上读 nvidia-smi，不要假定一个数字
local_nvme: true              # 临时的 root/本地 NVMe，terminate 后消失
---

# Lambda Cloud — 平台 Profile

Lambda Cloud 是一个 **cattle-not-pets**（牛非宠物）模型 GPU 云：按需 + 预留实例，预构建的 **Lambda Stack** 镜像，且 **没有 stop/suspend 状态** — 实例只能被 **启动、重启或终止**，terminate 会销毁本地 NVMe。机器上没有任何东西能在拆除后存活，除非是被推送出去的或写入已挂载的 **区域锁定 NFS 文件系统** 的内容。这颠覆了 AutoDL 的"关机保留数据"直觉：在这里，持久化设计（checkpoint-to-NFS + 幂等恢复）是 **强制性的，而非可选的**。

> **前置告知用户（原则 #10）：** ⚠️ 危险时钟 — **没有 stop/suspend**：实例只能被启动 / 重启 / **终止，而终止会抹除本地 NVMe** — 只有已挂载的 **NFS 文件系统** 能存活，且 **它在被手动删除前会持续计费**（LAM6）。便利设施 — 每个实例一键 **JupyterLab**，双向免费出站流量。terminate→relaunch 会产生一个 **新 IP**。

> 文档/控制台域名已从 `lambdalabs.com` 迁移至 `lambda.ai`（文档在 `docs.lambda.ai`，控制台在 `cloud.lambda.ai`）；**REST API 基地址仍然是 `cloud.lambdalabs.com/api/v1`**，`cloud.lambda.ai` 也可解析（已验证 docs.lambda.ai + cloud-api 2026-06）。两个主机均视为存活。

快速跳转：`grep -in <keyword> profiles/lambda.md`。

**目录** — 1. 启动 · 2. 存储模型（生存矩阵） · 3. 网络 ·
4. SPOT/中断 + 恢复 · 5. 拆除/计费 · 6. 守护工具 · 7. 主要陷阱（LAM1–LAM13）+
平台专属调试 · 8. 脚本覆盖。

通用陷阱（CRLF、inode/`df -i`、静默同步、cgroup OOM、spot 宽限）在此不重复 —
参见 `references/gotchas_universal.md`。通用不变量 → `references/principles.md`。

---

## 1. 启动

入口：
- **Web 控制台** 在 `cloud.lambda.ai` → Instances → Launch（选择 GPU 类型 + 区域，如需要则在此挂载文件系统 — 见 §2；同时在此挂载每实例防火墙规则集 — 见 §3/LAM4）。
- **REST API** — `https://cloud.lambdalabs.com/api/v1`，认证 `curl -u $LAMBDA_API_KEY:`（basic-auth，密码为空）。规范自动化入口（已验证 docs.lambda.ai/api/cloud 2026-06）：
  - `GET  /instance-types` — 列出每种 GPU 类型**及** `regions_with_capacity_available[]` 字段。
    该字段就是容量信号 — 轮询它以了解某种类型当前可以在哪里启动（驱动 LAM5
    的 retry-until-available 策略）。
  - `POST /instance-operations/launch` · `.../terminate` · `.../restart` — 创建 / 停止计费 / 重启。
- **SSH** — 标准连接到 Ubuntu VM；**默认用户是 `ubuntu`**（不是 `root`）；使用
  `sudo` 获取 root 权限。每个实例提供一键 **JupyterLab**。
- **SkyPilot** — 事实上的编排层：`pip install "skypilot[lambda]"`，密钥文件在
  `~/.lambda_cloud/lambda_keys`，包含一行 `api_key = <KEY>`（已验证 docs.skypilot.co 2026-06）。
  用它实现 retry-until-capacity + autostop（§4, §6）。

**环境契约 — 镜像/基础即环境。** 实例预装 **Lambda Stack**（NVIDIA driver + CUDA +
cuDNN + PyTorch/TensorFlow，作为一个 apt 元包统一升级）。直接在临时机器上运行它 — **不要**在租赁机上 `conda create`（`references/principles.md` §2），也不要在上面 `pip
install torch`（LAM7/LAM8）。Lambda Stack 的精确 CUDA/driver/PyTorch 版本**随发布变化**；
从机器上读取（`nvidia-smi`、`python -c "import torch;print(torch.__version__,torch.version.cuda)"`）
而非假定一个数字。环境的**持久化**形式是 Docker 镜像（Lambda 推荐在实例内运行 Docker）或每次启动时重放的 setup 脚本 — 因为 terminate 会销毁机器。
预留 / 1-Click Clusters 提供固定费率多节点（独立计费模型 — LAM12）。

> **验证：** `ssh ubuntu@<IP> 'python -c "import torch;print(torch.cuda.is_available())"'` → `True`。

---

## 2. 存储模型  *(生存矩阵 — 原则 #4)*

两个层级，陷阱在于默认工作位置是 **易失的** 那个。

- **本地 / root NVMe** — 快速、每实例独占、**临时**。文档：*"Data not stored in the mount location
  is erased once you terminate your instance and cannot be recovered"*（已验证 docs.lambda.ai
  creating-managing-instances 2026-06）。这是工作默认落地的地方。
- **NFS 文件系统** — 区域网络文件系统，挂载在 `/lambda/nfs/<name>`（文档示例挂载点：
  `/lambda/nfs/persistent-storage`）。**唯一的持久化归宿。** 三个硬约束（已验证
  docs.lambda.ai/public-cloud/filesystems 2026-06）：
  - **区域锁定** — *"The filesystem must reside in the same region as the instance or cluster"* 且
    *"Filesystems cannot currently be transferred between regions."* 创建时谨慎选择区域。
  - **仅在启动时挂载** — *"You must attach the filesystem … at the time that the instance … is
    launched"* 且 *"You can't attach a filesystem after you've created an instance."*
  - 计费 **$0.20/GiB/月，按 1 小时增量**，**免费入站/出站流量**；**每账户最多 24 个文件系统**；大多数区域允许每文件系统最多 8 EB，但 **us-south-1 (Texas) 上限为 10 TB**。
- **无文档化 inode 上限** — 仅有 GiB 配额；没有暴露的 `df -i` 上限（仍需按通用存储陷阱审计 `df -i`）。

| 层级 | 路径 | RESTART 后存活？ | TERMINATE 后存活？ | 容量 |
|---|---|---|---|---|
| 本地 / root NVMe | `/`, `/home/ubuntu` | 是（数据保留；**但冷重启会清除 RAM** — LAM9） | **否**（被擦除，不可恢复） | 实例 root 卷 |
| NFS 文件系统 | `/lambda/nfs/<name>` | 是 | **是**（独立生命周期；持续计费 — LAM6） | GiB 配额；us-south-1 约 10 TB，其他区域 8 EB |

**检查点必须写入** `/lambda/nfs/<name>`（持久层）以应对 §5 的 `terminate` 操作。
留在本地 NVMe 上的检查点随机器一起消亡。如果启动时没有挂载文件系统，唯一的持久化路径是在终止前将结果 `pull` 到机外（免费出站）。

---

## 3. 网络

- **直连、无代理出站。** 美国/全球云 — 到 HF / GitHub / PyPI 的出站是直连的；**不存在 `network_turbo` 风格的加速器**，也不需要。中国镜像相关性**不作为平台功能适用**（仅当从中国境内操作时相关；此时 `references/china-network.md` 适用于用户自身的设置，与平台无关）。
- **双向免费出站** — *"Transparent pricing with no egress fees"*（已验证 lambda.ai
  pricing 2026-06）。重新拉取大模型或将结果推送到机外不花一分钱，使得"terminate 前 pull"成为未挂载 NFS 时的廉价安全默认操作。
- **防火墙** — 默认仅允许*"incoming ICMP traffic or TCP traffic on port 22 (SSH)"*。通过**全局规则**（工作区范围应用）或**每实例规则集**（区域范围）开放更多端口。每实例规则集：*"You must attach rulesets during the instance launch process. You can't attach them after the instance has been launched"* 且 *"You can't remove rulesets from an instance after the instance has been launched"*（已验证 docs.lambda.ai/public-cloud/firewalls 2026-06）→ 启动前规划端口暴露（陷阱 LAM4）。全局规则仍可在事后编辑。
- **暴露 TensorBoard / Jupyter** — 实例获得公网 IP；通过 SSH 隧道而非开放端口：
  `ssh -L 8888:localhost:8888 -L 6006:localhost:6006 ubuntu@<IP>`。无平台绑定的 TensorBoard 目录 — 在 NFS 挂载点下的 logdir 上运行 TB `:6006`。
- **SSH 风格** — 直接 TCP 连接到标准 VM（`ubuntu@<IP>`）；完整 `scp`/`rsync` 可用，无代理跳板怪癖。
  **无静态 IP 功能** — *"On-Demand Cloud doesn't support static IP addresses"*（已验证 DeepTalk
  staff 2026-06）。IP 在实例生命周期内固定，但 **terminate→relaunch 产生新 IP**
  （LAM10）— 每次启动从控制台/API 重新读取；永远不要在自动化中硬编码。

---

## 4. SPOT / 中断 + 恢复  *(原则 #7/#8)*

**没有 spot / 抢占层级 — 也没有运行中驱逐。** 这是与 vast.ai/RunPod 的关键分歧：
**没有 SIGTERM→SIGKILL 宽限窗口需要应对**，因为运行中的实例从不在 epoch 中间被驱逐。中断模型在性质上不同：

- **启动时的容量问题是真正的失败。** 期望的 GPU 类型可能在启动尝试时**不可用** — Lambda **没有可回退的 spot 层级**，且实际按需填充率波动较大（一份公开的 6 个月日志：约 64% 的同日 A100 成功 — 即约 1/3 的尝试被阻塞；一次从 2 扩展到 4 H100 的 26 小时"暂时不可用"停滞；已验证 medium.com/@velinxs 2026-06）。H100/B200 容量最为紧张。恢复模式是 **retry-until-available**，而非 survive-eviction：
  轮询 `GET /instance-types` 的 `regions_with_capacity_available`，某区域出现时立即 `POST .../launch`（或让 SkyPilot 的 provisioner 跨区域/类型重试）。
- **仅自我造成的终止。** 一旦运行，仅有的破坏性事件是操作员的
  `terminate`，或一个**不当的 `sudo shutdown`** 将机器推入 **Alert** 状态却仍在计费
  （LAM3 / §5），或一个**冷重启**清除 RAM（LAM9）。
- **恢复钩子** — 在周期性定时器上将完整状态检查点到 NFS 文件系统，启动时无条件加载最新状态，使容量恢复后的新启动是恢复而非重启。因为机器是 cattle，恢复路径在*每次*重新启动时都会执行，而非仅在罕见的抢占之后。

间隔公式（Young/Daly）+ 原子写入恢复 → `references/spot-resilience.md`。这里公式的 μ 实际上是"自愿重启之间的时间"，而非抢占率。

---

## 5. 拆除 / 计费  *(原则 #9 + 铁律)*

**TERMINATE 是停止计费的动词 — 且不可逆。** *"Billing begins the moment you launch an
instance and the instance passes health checks, and ends the moment you terminate the instance"*，按**一分钟增量**计费，*"regardless if they're actively being used"*（已验证
docs.lambda.ai/public-cloud/billing 2026-06）。

> **shutdown 陷阱（本平台最容易出错的事实）：** *"Do not use commands such as `sudo
> shutdown -h now` or `sudo systemctl poweroff` … These commands will not work as expected and will cause
> your instances to go into Alert status, and billing will continue"*（已验证 docs.lambda.ai 2026-06）。
> 同样 `halt` / `shutdown -P 0` 只停止 OS，不停止计费（DeepTalk staff）。停止计费**仅能**通过控制台的 `terminate` 或 `POST /instance-operations/terminate` — 甚至可以在实例内部执行。

各操作保留什么：
- **terminate** — 停止实例计费；**擦除本地 NVMe**（不可恢复）。NFS 文件系统有**独立生命周期**并存活 — 但它**持续以 $0.20/GiB/月计费直到显式删除**
  （*"Billing continues as long as a filesystem exists, even if it's not mounted to an instance"*），
  所以一个已终止但被遗忘的文件系统是静默的持续费用（LAM6）。
- **没有 stop/suspend 状态** — *"It currently isn't possible to pause (suspend) your instance …
  Your only options are to launch, restart, or terminate"*（已验证 docs.lambda.ai 2026-06）。廉价空闲暂停是不可能的；停止为计算付费的唯一方式是销毁机器并后续重建。
- **restart / 冷重启** — **不**停止计费，**不**擦除磁盘，但**冷重启清除 RAM 并跳过安全关机** — 仅在机器冻结时使用（LAM9）。

**铁律（SKILL.md Phase 5）：** 在检查点**已 pull 到本地或在 NFS 上经加载测试确认**且用户批准了影响成本的操作之前，不得执行 `terminate`。因为 terminate 是破坏性且不可逆的，一次未验证的 `cp`/`rsync` 到 NFS 意味着**永久丢失** — 在终止前验证同步（checksum /
`ls -l` / 一次加载），而非之后。出站免费，所以双重保险的 `pull` 到本地也是廉价的。交叉引用：`superpowers:verification-before-completion`（必需），用于通用门控。

---

## 6. 守护工具

- **分离原语：`tmux`**（或 `screen` / `nohup`）在标准 Ubuntu VM 上 — 与 AutoDL tmux 模式相同的操作手册。如缺失则安装（`sudo apt install -y tmux`）；回退到
  `nohup … </dev/null >log 2>&1 &`。
- **在 SSH 断开后存活，不在 terminate 后存活。** tmux 在连接断开时保持作业存活，但在没有 stop 状态的情况下，分离原语无法在拆除后存活 — 只有 **checkpoint-to-NFS +
  幂等恢复** 脊柱能做到（原则 #8）。tmux 是 SSH 弹性层；检查点是实例弹性层。（tmux 也不在冷重启后存活 — LAM9。）
- **原生编排：SkyPilot**（托管作业、autostop、retry-until-capacity）+ **1-Click
  Clusters** 用于多节点；否则无平台作业队列。SkyPilot 在容量丢失时迁移机器，但**从头重启进程 — 检查点加载恢复进度**（不要假设框架恢复了训练状态）。

---

## 7. 主要陷阱  (Lambda 专属 — 通用陷阱见 `references/gotchas_universal.md`)

- **LAM1 — Terminate 擦除本地 NVMe；没有 stop/suspend。**
  症状：重启的实例是空白的，昨天的运行消失了。→ 根因：本地存储是临时的（*"Data not stored in the mount location is erased … and cannot be recovered"*）且没有 stop 状态保留它；AutoDL 的"关机保留数据"假设是错误的。→ 修复：围绕销毁/重建设计每个工作流 — 检查点到 `/lambda/nfs/<name>` 或在任意 terminate 前 `pull` 到机外；永远不要在本地 NVMe 上保留唯一副本。（docs.lambda.ai 2026-06）

- **LAM2 — 文件系统仅支持启动时挂载且区域锁定。**
  症状：运行中的实例没有持久存储且无法添加；或 us-east 文件系统无法挂载到 us-west 实例。→ 根因：文件系统仅在创建时挂载，不能跨区域移动。→ 修复：在**启动时**决定区域并挂载文件系统；将实例 + 文件系统置于同一区域。（filesystems doc 2026-06）

- **LAM3 — `sudo shutdown` / `poweroff` 使计费继续运行（Alert 状态）。**
  症状：实例"已关机"但账单持续攀升。→ 根因：OS 内关机将实例送入 **Alert** 而不停止计费；`halt`/`shutdown -P 0` 仅停止 OS，不停止计费。
  → 修复：仅通过 **terminate** 停止计费（控制台或 `POST /instance-operations/terminate`）；永远不要依赖机内关机。（billing doc + DeepTalk staff 2026-06）

- **LAM4 — 每实例防火墙规则集启动后不可变。**
  症状：需要的入站端口无法开放（或错误端口无法移除）。→ 根因：每实例规则集*"must [be attached] during the instance launch process"*且*"can't [be removed]
  after the instance has been launched."* → 修复：启动前规划端口暴露，使用可编辑的**全局**规则，或通过 SSH 隧道（`-L`，§3）代替开放端口。（firewalls doc 2026-06）

- **LAM5 — 容量而非驱逐是瓶颈（无 spot 回退）。**
  症状：启动失败 / 控制台显示期望的 GPU 类型不可用；扩展时长时间停滞。→ 根因：特定 GPU/区域的按需供应耗尽（H100/B200 最差），且没有可回退的 spot 层级。→ 修复：轮询 `GET /instance-types` 的 `regions_with_capacity_available`，区域出现时立即启动（或使用 SkyPilot 的跨区域/类型 provisioner）；获得容量后从 NFS 检查点恢复（§4）。（cloud-api doc + medium.com/@velinxs 2026-06）

- **LAM6 — NFS 文件系统在实例终止后继续计费。**
  症状：所有实例已终止，但存储费用继续。→ 根因：*"Billing continues as
  long as a filesystem exists, even if it's not mounted to an instance"* — $0.20/GiB/月直到删除。
  → 修复：在最终 `pull` + 验证后，**删除文件系统**（控制台 Storage → Delete；需要先终止挂载的实例）— 一个独立的拆除步骤。（billing + filesystems docs 2026-06）

- **LAM7 — 在 Lambda Stack 上 `pip install torch` 静默遮蔽或冲突。**
  症状：`base` 中的 `pip install` 报告*"Defaulting to user installation because normal site-packages
  is not writeable"*并安装到 `~/.local`，或 `torch==X` 硬锁定拉入一个与系统构建冲突的 CUDA/torchvision 组合 → import/CUDA 错误。→ 根因：Lambda Stack PyTorch 位于系统 `/usr/lib/python3/dist-packages`（作为 `ubuntu` 无法用 pip 写入）；pip 的用户安装或硬版本锁定与之分歧。→ 修复：原样使用 Stack 的 PyTorch（不要重装），放宽锁定（`torch>=2.x` 而非 `==`），或在全新的 venv/conda env 中完全隔离并干净地安装 torch — 不要半混 pip-over-system。（DeepTalk threads 2026-06）

- **LAM8 — conda/venv 通过 system-site-packages "借用" Stack PyTorch 后在 pip 上崩溃。**
  症状：创建了 conda env 使用 Stack 的 torch，后续 `pip install` 拉入第二个冲突的 torch 或无法写入 site-packages。→ 根因：将 `--system-site-packages`（查看系统 torch）与 pip 安装到同一 env 混合会产生两份 torch。→ 修复：选择**一种**模式 — 要么在裸 Stack base 中运行（租赁机上的首选），要么构建完全自包含的 env 并 `conda install pytorch torchvision`（不借用 system-site-packages）。（DeepTalk
  bypassing-lambda-stack thread 2026-06）

- **LAM9 — 冷重启清除 RAM 和 tmux；热重启仍然计费。**
  症状：重启后分离的训练作业消失，机器恢复干净状态。→ 根因：**冷重启** *"erases all data currently in the instance's memory and bypasses the operating
  system's safe-shutdown mechanisms"* — 杀死 tmux 会话和所有 RAM 中状态；两种重启都不停止计费。→ 修复：仅对冻结的机器执行冷重启；依赖 checkpoint-to-NFS，而非进程跨重启存活；预期需要重新 `ssh` 和 `tmux attach`（会话可能已消失）。（console doc 2026-06）

- **LAM10 — 无静态 IP；公网 IP 在 terminate→relaunch 后变化。**
  症状：自动化/SSH 配置硬编码了昨天的 IP，重新启动后失败。→ 根因：*"On-Demand Cloud doesn't support static IP addresses"* — 新启动获得新 IP。→ 修复：每次启动从控制台 / `GET /instances` 读取 IP；动态模板化 SSH 配置；永远不要硬编码。（DeepTalk staff 2026-06）

- **LAM11 — 在 Lambda Stack 镜像上 `apt full-upgrade` 可能破坏 cuDNN/DOCA。**
  症状：执行推荐的 `apt-get update && upgrade`（或 24.04 镜像上的 `full-upgrade`）后，PyTorch/TF 找不到 cuDNN，或 full-upgrade 本身在 DOCA 包上失败。→ 根因：系统 cuDNN 升级或 DOCA 仓库状态与 Stack 捆绑的库分歧。→ 修复：在租赁机上避免全面 `full-upgrade`；如果 cuDNN 缺失，符号链接 Stack 副本 —
  `for so in /usr/lib/python3/dist-packages/tensorflow/libcudnn*; do sudo ln -s "$so" /usr/lib/x86_64-linux-gnu/; done`
  （注意：Stack cuDNN 仅能被 Stack 安装的 PyTorch/TF 使用）。（troubleshooting doc 2026-06）

- **LAM12 — 1-Click Clusters / 预留实例计费方式与按需不同（承诺陷阱）。**
  症状：预期按分钟计费，却得到 2 周最低期限 / 周账单 / 过期预留。→ 根因：**1-Click Clusters** 携带**最低 2 周承诺且按周计费**（非按分钟）；**预留**容量需要 Lambda 批准，且**发票必须在约 10 天内支付否则预留被没收**，条款不可取消。→ 修复：使用普通按需单实例进行按分钟实验；仅在确认持续需求和预算批准后才进入集群/预留。（1-click-clusters docs + nOps/CheckThat 2026-06）

- **LAM13 — GH200 (ARM/aarch64) 上 `pip install torch` 失败 — 需要 ARM 构建。**
  症状：在 1× GH200 机器上，`pip install torch` 安装了**仅 CPU** 的 wheel（无 CUDA），或硬锁定的 `torch==2.2.0` 无法解析。→ 根因：GH200 是 aarch64；PyPI 上 aarch64 的默认 torch wheel 是仅 CPU 的。→ 修复：原样使用 Lambda Stack 预编译的 ARM PyTorch（如 2.4.1），或从 CUDA index 安装 `pip install torch --index-url https://download.pytorch.org/whl/cu128`（aarch64 GPU
  wheels 在那里），或从源码编译更新版本；放宽精确锁定。（DeepTalk GH200 thread
  + pytorch.org 2026-06）

### 平台专属调试
- **确认计费确实停止了：** 拆除后，通过控制台或 `curl -u $LAMBDA_API_KEY: https://cloud.lambdalabs.com/api/v1/instances` 检查实例确实**消失**（不在 *Alert* 状态）— Alert 状态的机器（来自 OS 内关机）仍在计费（LAM3）。
- **启动前容量探测：** `curl -u $LAMBDA_API_KEY: .../instance-types | jq '.data | to_entries[]
  | {type:.key, regions:.value.regions_with_capacity_available}'` — 空 `regions` ⇒ 该 GPU 类型当前无法在任何地方启动（LAM5）；这是 retry-until-available 的循环条件。
- **机器上 GPU 健康检查：** `nvidia-smi`（driver/CUDA + 利用率）和 `python -c "import torch;
  print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"` — `torch.version.cuda` 与
  `nvidia-smi` CUDA 不匹配通常意味着 pip 遮蔽了 torch（LAM7/8/13），而非 Stack 问题。
- **读取真实 Stack 版本，永远不要假定：** `apt list --installed 2>/dev/null | grep -i lambda-stack`
  和 `dpkg -l | grep -i cudnn` — 在调试"版本不匹配"前先确认。
- **临时 root 上的磁盘压力：** `df -h /` 和 `df -h /lambda/nfs/<name>`；记住 `/home/ubuntu`
  是易失的 — 填满 root 卷的大数据集/检查点在 terminate 时也会*丢失*，所以将它们移到 NFS，不仅是为了腾空间。
- **检测停滞的下载：** 后台拉取（`nohup … &`）并观察增长 —
  `watch -n5 'du -sh <target>; ls -l <target>'`（大小连续几分钟不变 ⇒ 停滞；重新拉取，出站免费）。
- **重启后卡住/不可达：** 如果重启后 SSH 失联，机器可能处于 *Alert* 或网络未能启动 — 检查控制台状态，优先执行全新的 **terminate→relaunch**（从 NFS 恢复）而非对抗一个已经清除了 RAM 的冷重启（LAM9）。

---

## 8. 脚本覆盖

为 Lambda 参数化 `scripts/` 模板的值：

```
DATA_DIR=       /home/ubuntu (临时 NVMe — terminate 后丢失)
DURABLE_DIR=    /lambda/nfs/<name>
PROXY_HOOK=     (无 — 直连出站；无 network_turbo)
CRED_FILE=      ""  (Lambda 密钥是 $LAMBDA_API_KEY 环境变量，不是磁盘文件 — run_one 的 [ -n "$CRED_FILE" ] 守卫跳过文件读取，环境变量直接传递；SkyPilot 密钥文件在 ~/.lambda_cloud/lambda_keys，格式 `api_key = <KEY>`)
SCRATCH=        在本地 NVMe 上周期性修剪检查点；仅保留 `best` 在 /lambda/nfs/<name>
HF_HOME=        /lambda/nfs/<name>/.cache/huggingface   (持久；在 terminate 后存活，重新拉取免费出站)
DETACH=         tmux  (如缺失则 apt install；nohup 回退)
SSH_USER=       ubuntu   (不是 root)
```

封装器注意事项：
- 默认检查点目录 → NFS 挂载点，不是 `/home/ubuntu` — 后者在 terminate 时被擦除。
- 如果没有挂载 NFS 文件系统，将封装器设置为在周期性定时器上将检查点 `pull` 到本地（免费出站）而非依赖机器上的持久存储。
- 每次启动从控制台/API 重新读取实例 IP（LAM10）— 永远不要在 SSH 配置中持久化它。
- 不要在租赁机上 `pip install torch` / 全面 `apt full-upgrade` — 原样使用 Stack（LAM7/8/11）；
  在 GH200 上使用 ARM 构建（LAM13）。
- 拆除步骤是**通过 API terminate**，由铁律门控；验证计费已停止（无 *Alert* 状态）并添加显式提醒在项目完成时**删除 NFS 文件系统**（LAM6）。
