# Profile: AutoDL

最深、经实战验证的 Profile——一个中国 cgroup 隔离的 SSH 租赁平台，拥有3层存储模型，且是*唯一*一个计费停止动作非破坏性的租赁平台。完整覆盖8个 schema 章节（`profiles/_schema.md`）。在 Phase 0 之前阅读本文；它拥有 SKILL.md 各阶段委托的每个路径、代理、计费动词和 TB 固定配置。通用陷阱不在本文重复——参见 `references/gotchas_universal.md`。

> **预先告知用户（原则 #10）：** 大多数用户忽略的便利功能——控制台有**一键"设置SSH免密登录"**（注册你的密钥以便智能体非交互连接）、**GPU可用性通知**（"订阅GPU通知"）和内置 **AutoPanel / JupyterLab / TensorBoard** 面板。⚠️ 危险时钟——**关机后15天自动释放实例 → 数据盘被删除**（AD-DANGER，§5）；只有 `/root/autodl-fs` 在释放后存活；低余额/欠费会强制停机。TB 面板**固定指向 `/root/tf-logs`**——将 logger 写入该路径（或符号链接），否则面板显示空白（AD7 / U39）。

快速跳转：`grep -in '<keyword>' profiles/autodl.md`（例如 `grep -in inode profiles/autodl.md`）。

## 目录

1. LAUNCH — 入口 + 环境契约（base miniconda 就是环境）
2. STORAGE MODEL — 3层 + 生存矩阵 + inode 上限
3. NETWORK — 学术代理 + 中国镜像 + 固定 TB
4. SPOT / INTERRUPTION + RESUME — 实际为按需实例
5. TEARDOWN / BILLING — 关机停止计费且保留磁盘（AutoDL 的例外）
6. DAEMON TOOL — tmux / nohup
7. TOP GOTCHAS — AD1..AD9，平台专属
8. SCRIPT OVERRIDES — 参数化 `scripts/` 的值

---

```yaml
---
platform: autodl
kind: ssh-rental
meter_stop_verb: 关机           # 关机停止计费且保留 /root + 磁盘
meter_stop_irreversible: false  # AutoDL 例外 — 关机可逆；只有释放/释放会删除
detach_primitive: tmux          # 当 tmux 未安装时回退到 nohup（新镜像中经常没有）
spot_available: false           # 仅按需；无 spot/竞价/抢占模型
spot_grace: n/a
shared_fs: true                 # /root/autodl-fs — 地域锁定，同区域内跨实例共享
inode_cap: ~200K                # 共享 FS 的硬上限，与字节容量无关
free_egress: true               # 无按 GB 出口费，但跨 GFW 拉取需要学术代理（见 china_mirror_needed）
china_mirror_needed: true       # 在 GFW 之后 — hf-mirror / ModelScope + /etc/network_turbo
host_driver_cuda_max: image-dependent   # 预构建镜像固定 torch+CUDA；不要降级（AD9）
local_nvme: true                # /root/autodl-tmp 数据盘为快速本地 NVMe，按实例分配
---
```

---

## 1. LAUNCH

**首次使用？（租赁 → 连接到机器）。** 在 AutoDL 控制台：选择有库存的 GPU + 地域 → **创建实例**（选择 PyTorch 镜像——基础环境预构建）→ 通过**设置SSH免密登录**一次性注册密钥（以便智能体非交互连接）→ 从控制台复制实例的 **SSH 连接字符串** + 密码 → 测试 `ssh -p <PORT> root@connect.<region>.seetacloud.com 'nvidia-smi'`。该字符串是你进入以下所有阶段的入口。（仅限控制台步骤；AutoDL 的 UI 可能变动——若标签位置变了请重新查阅文档。）

**入口。** Web 控制台（创建实例）用于创建/释放/开关机；从控制台获取每个实例的 SSH 连接字符串（`ssh -p <PORT> root@connect.<region>.seetacloud.com`）。无一流的平台 CLI/REST 用于作业控制——SSH 是编排通道。在 `~/.ssh/config` 中为每个实例设置稳定别名（`Host autodl-<proj>-<N>`，`HostName connect.<region>.seetacloud.com`，`Port <PORT>`），使后续每个命令都简短；端口在创建时分配且**重新创建时会变化**（更新别名）。SSH/keepalive 配置 → `references/ssh_transport.md`。

**环境契约 — 预构建的 base miniconda 就是环境（AD6）。** 镜像将完整 DL 栈安装到 **base**（`/root/miniconda3/bin/python`）；不存在 `/root/miniconda3/envs/<name>/`。Base 是刻意设计的单租户项目环境。**绝不在租赁机上 `conda create` / `conda clone base`**——克隆浪费约16 GB 的 base 包 + 刚释放的磁盘空间，毫无收益。使用显式解释器 `/root/miniconda3/bin/python` 训练；在远程轮询中使用该路径或纯 shell，绝不用裸 `python3`（可能不存在 → exit 127）。安装项目依赖时，**过滤框架版本锁定**，使 `requirements.txt` 不会降级镜像的 torch 构建（AD9）。

> "不在 conda base 中做 DL"的纪律仅适用于*持久本地*机器——在临时租赁机上，base 就是预期运行的地方。本地环境守卫钩子必须豁免 remote-ssh + 实例 base。

---

## 2. STORAGE MODEL  *(生存矩阵 — 原则 #4)*

三层，各有不同的速度/容量/inode 特征和**不同的存活行为**：

| 层级 | 路径 | 速度 | 容量 | Inode 上限 | 范围 |
|---|---|---|---|---|---|
| 系统盘 | `/` | 中等 | ~30 GB | 无 | 按实例 |
| 数据盘 | `/root/autodl-tmp` | **快速 NVMe** | 按计划（例如 ~50 GB） | 无 | 按实例 |
| 共享 FS | `/root/autodl-fs` | NFS（慢，~30 s/同步） | ~200 GB | **~200K（硬上限）** | **地域锁定**，同区域所有实例 |

**生存矩阵** — 大多数平台出错的部分，而 AutoDL 是**例外**：

| 层级 | 关机后存活？ | 释放后存活？ | 备注 |
|---|---|---|---|
| `/` 系统 | **是** | 否 | AutoDL 在关机后保留 `/root` — 不同于 RunPod/vast/K8s/Colab |
| `/root/autodl-tmp` 数据 | **是** | 否 | 快速层；运行中检查点写在此处 |
| `/root/autodl-fs` 共享 | **是** | **是** | 唯一在释放后存活的层级；地域锁定 |

**§5 拆除动词下检查点必须写入的位置：** 将实时检查点写到快速数据盘（`/root/autodl-tmp/checkpoints/<name>`，绝不在30 GB 系统盘上），然后**校验同步 `best.pth` 到 `/root/autodl-fs`**——唯一在释放后存活的层级。如果只使用关机，数据盘也存活，但将持久副本同步到 FS 是安全默认（后续释放会丢失数据盘）。

**地域/机房锁定（AD3）。** FS 配额是地域范围的；每个地域有自己的物理挂载。从 `<region-a>` 实例写入的文件对 `<region-b>` 实例不可见，即使路径同为 `/root/autodl-fs/`。在与实例**同一地域**创建 FS 配额；跨地域桥接需选择一个地域为主，通过 scp 传输（慢）。在依赖之前用"一端写/另一端读"探测确认共享。

**Inode 纪律（AD4）。** ~200K 上限**与字节数无关**：`df -h` 可能显示34%而 `cp` 因 `df -i` 达100%而失败"No space left"。Inode 炸弹来自**逐样本评估可视化**（`files_per_sample × N_samples × N_conditions` → 数万小文件）；检查点（少数大文件）对 inode 消耗极小。监控 `df -i`，不只是 `df -h`（Phase 0 + 每次空间检查）。评估产物大小策略由 **REQUIRED:** verifying-dl-experiments 负责。

**数据盘占满（AD5）。** 当 `/root/autodl-tmp` 达到100%但 `runs/` 看起来很小时，真正的占空间者是**符号链接到数据盘的 HF 缓存**（`~/.cache/huggingface` → 数十 GB 的模型 blob）。在删除检查点之前审计 `du -sh ~/.cache/huggingface/hub/models--* | sort -rh`；显式将 `HF_HOME` 重定向到数据盘（见 §8）。磁盘可扩容——优先扩容而非静默缩减实验（原则 #9）。获取用户显式确认并指明 `rm -rf` 目标（harness 分类器阻止智能体推断的不可逆删除）。

---

## 3. NETWORK

**出口代理 — `source /etc/network_turbo` 是必须的（AD1）。** 实例启动时无代理；直连到 `api.wandb.ai` / `huggingface.co` / `github.com` / `pypi.org` 不可靠（0.5 s … 300 s … 被阻断）。每个调用 wandb / HF / pip / git 的 shell 都必须先 `source /etc/network_turbo`（在每个 wrapper 顶部加 `source /etc/network_turbo 2>/dev/null || true`）。它导出 `http_proxy` / `https_proxy` 指向机房内学术代理（`http://<proxy-ip>:<port>`）、`no_proxy` 国内端点白名单和 CA bundle。性能差异：wandb 推送使用 turbo 约0.8 s vs 无 turbo 超过120 s 超时——无例外，即使很小的 `wandb.summary` 写入也可能卡住数分钟。

**中国镜像（AD2）。** HF 在 GFW 之后 → `HF_ENDPOINT=https://hf-mirror.com` 或从 **ModelScope** 拉取。两个叠加陷阱：(a) HF 的 **Xet CAS 后端**不被镜像代理（镜像覆盖 API 但大型 `.safetensors` 分片仍然命中不稳定的国际端点）→ `export HF_HUB_DISABLE_XET=1`（或 `pip uninstall -y hf_xet`）强制走镜像确实代理的经典 LFS 路径；(b) network_turbo 中的 `no_proxy` 列出了 `modelscope.com` 但**不含** `modelscope.cn`——将国内源路由通过国际加速代理反而更慢。每个下载包裹在 `timeout <s> … && break` 重试循环中（恢复部分文件；卡顿 ≠ 永久失败）。完整镜像表 + `no_proxy` 阶梯 → `references/china-network.md`。

**端口暴露。** AutoDL 映射一个自定义端口（6006）用于用户服务；平台还暴露 JupyterLab。SSH 端口是按实例的 `<PORT>`，重新创建时会变化。

**平台 TensorBoard 固定指向 `/root/tf-logs`（AD7）。** 镜像开机时自动启动 `tensorboard --logdir /root/tf-logs --port 6007`，AutoPanel TB 面板直接代理到该进程——`--logdir` 是硬固定的，无法从容器内重新配置。写入其他位置的事件在 Web 面板中不可见，无论 `SummaryWriter` 设置多么正确。修复：写入 `SummaryWriter(log_dir="/root/tf-logs/<run>")`，或 `ln -sfn <your-tb> /root/tf-logs/<run>`（固定 TB 的 `--reload=5` 会在约5 s 内识别到运行——无需重启）。用 `curl -s http://127.0.0.1:6007/data/runs` 验证（期望包含运行的 JSON 数组），而**不是** `ss`（容器内可能显示为空但 curl 返回200）。本地日志随实例消失——持久曲线使用托管追踪器（**REQUIRED:** huggingface-skills:huggingface-trackio）。

**SSH 风格。** 按实例 host:port 的 direct-TCP SSH——`scp`/`rsync` 正常工作（无代理 SSH 限制）。大传输使用按目录可恢复循环（单连接 `scp -r` 在传输中途重置）；优先使用 `rsync -avz --partial`。传输模式 → `references/ssh_transport.md`。

---

## 4. SPOT / INTERRUPTION + RESUME  *(原则 #7/#8)*

**无 spot/竞价/抢占模型——AutoDL 是按需的。** 没有运行中驱逐，没有需要处理的 SIGTERM 宽限期（`spot_grace: n/a`）。真正的损失向量是：(a) **忘记释放/关机** → 闲置计费（原则 #1）；(b) 实例**重启**导致未脱离的进程消失（进程消失不总是 OOM——在得出结论前枚举重启 / OOM / SSH-HUP / 手动kill，见 `references/gotchas_universal.md`）；(c) 可用性——创建时 GPU 方案售罄（构建重试直到可用，而非存活驱逐）。

**恢复钩子。** 通用主干仍然适用（原则 #8）：原子写入检查点到数据盘 + 同步 `best.pth` 到 FS，重新启动时无条件 resume-from-latest。脱离原语（§6）使*相同的启动命令*在 SSH 断开后存活；checkpoint+resume 使其在重启后存活。节奏公式 → `references/spot-resilience.md`（公式即使没有 spot 也通用——它限定重启损失的重计算量）。

---

## 5. TEARDOWN / BILLING  *(原则 #9 + 铁律)*

**关机停止计费且保留 `/root` + 两个磁盘——这是租赁平台中 AutoDL 的例外。** 其他所有平台（RunPod 在 stop 时擦除容器磁盘，vast 永远收取磁盘费，K8s 擦除 pod FS，Colab 丢失 `/content`）"stop"是有损的或仍在计费。在 AutoDL，关机是**安全停放**：计费关闭，三层完整，稍后重启。还有一个**无GPU / 无卡模式**用于低成本重启来复制文件或修复环境，无需为 GPU 付费。

| 操作 | 停止计费？ | 保留 `/` + 数据盘？ | 保留 FS？ | 可逆？ |
|---|---|---|---|---|
| 关机 | **是** | **是** | 是 | **是** — 随时重启（AutoDL 例外） |
| 无卡模式 | 大部分（便宜） | 是 | 是 | 是 |
| 释放 | 是 | **否** | 是 | **否 — 不可逆地删除 `/` + 数据盘** |

**费用陷阱。** 关机时 GPU 计费关闭但仍以小费率收取数据盘*存储*费——远低于运行费用，但不是免费的。只有释放完全结束存储计费，代价是数据盘。**⚠️ 自动释放时钟（AD-DANGER）：** 关机（已停止）的实例**15天后自动释放**（控制台显示"关机15天后释放"）→ 该释放删除 `/` **和数据盘**，所以关机仅在窗口内是安全停放；较长时间暂停，将 `best` 同步到 `/root/autodl-fs`（在释放后存活）或预期重新下载。低余额/欠费也会强制停机。**预先告知用户（原则 #10）**——大多数用户假设关机能无限期停放。
**拆除铁律（SKILL.md Phase 5）：** 在 `best.pth` 被**拉取到本地并通过加载验证**（`scripts/verify_local.py`）且用户显式批准之前，不得 释放/文件删除——"日志里看着完成了"不是证据（原则 #3）。因为此处关机是非破坏性的，不确定时便宜的安全做法是**关机并询问**，绝不猜测性地释放。**REQUIRED:** superpowers:verification-before-completion 是此门控的通用形式。

---

## 6. DAEMON TOOL

**tmux** 是可用时的脱离原语，但 **tmux 通常未安装在全新 AutoDL 镜像上**，且出口不通时 `apt-get install tmux` 会失败。零依赖回退：
`nohup bash run_queue.sh queue.txt </dev/null >master.log 2>&1 &` — 在 SSH 断开（SIGHUP）后存活，无需安装包。用 `pgrep -af <script>` 验证。脱离在 SSH 断开后存活；它**不**在关机/重启后存活——那是 checkpoint+resume（§4）的职责。

**原生队列：无。** AutoDL 无内置调度器 → 使用附带的 `scripts/run_queue.sh.template`（可恢复的队列迭代器，`start_index` 用于恢复）驱动每个 cell 的 `scripts/run_one.sh.template`。**绝不覆盖正在被 bash 执行中的脚本**（bash 按字节偏移读取 → 会重执行代码块；对文件名做版本化）——通用物理规律，见 `references/gotchas_universal.md`。

**监控。** 会话绑定的监控器随会话消亡；多小时运行部署四层持久架构（`references/monitoring_patterns.md`）。通过**日志标记**检测"完成"（`grep -q 'QUEUE DONE' master.log`），绝不用 `pgrep`（等待器自己的命令行匹配模式会无限循环）。云调度器无法触达租赁机（云沙箱中无 SSH 密钥——密钥泄露）；诚实的定期检查是远程自监控 + 使用本地密钥的会话循环。

---

## 7. TOP GOTCHAS  (AutoDL 专属；通用陷阱 → `references/gotchas_universal.md`)

**AD1 — 外部网络调用卡死 / wandb 显示0次运行。** *症状：* `wandb.init` 在 90/120/180 s 超时，仪表盘显示0次运行而本地 `wandb/run-*` 存在；HF 下载卡住；pip/git 极慢。*根因：* 实例启动时**无代理**；直连到 wandb/HF/PyPI/GitHub 不可靠或被阻断，且 wandb-core 在不稳定链路下的重试逻辑可能回滚已上传的运行。*修复：* 在**每个** shell/wrapper 中任何外部调用之前 `source /etc/network_turbo`；恢复空白的云项目：`for d in wandb/run-*; do timeout 120 wandb sync "$d"; done`。

**AD2 — 即使使用 hf-mirror + turbo，HF 下载仍卡住。** *症状：* `from_pretrained` / `snapshot_download` 卡住或大型 `.safetensors` 分片出现 `ConnectTimeout`。*根因：* (a) HF 的 Xet CAS 后端不被镜像代理；(b) `no_proxy` 列出 `modelscope.com` 而非 `modelscope.cn`（国内源被强制走国际代理 = 更慢）；(c) 在无 turbo 的情况下运行的 curl 测试测量了错误路径。*修复：* `export HF_HUB_DISABLE_XET=1`（或 `pip uninstall -y hf_xet`）配合 `HF_ENDPOINT=https://hf-mirror.com`，或从 ModelScope 拉取到普通目录 + 通过本地路径覆盖加载；包裹在 `timeout … && break` 恢复循环中。详情 → `references/china-network.md`。

**AD3 — 跨地域实例无法共享 FS。** *症状：* 不同地域的两个实例看到相同的 `/root/autodl-fs/` 路径但一端写入的文件对另一端不可见。*根因：* FS 配额是地域范围的；每个地域有自己的物理挂载。*修复：* 在与实例同一地域创建 FS 配额；通过从选定的主地域 scp 桥接地域；用"一端写/另一端读"探测验证。

**AD4 — FS 写入失败"No space left"但 `df -h` 看起来正常。** *症状：* `cp`/`mkdir` 到 `/root/autodl-fs` 失败但 `df -h` 显示约34%；`df -i` 显示 `… 0 100%`。*根因：* 共享 FS 强制执行**与字节无关的 ~200K 硬 inode 上限**；逐样本评估可视化（大量小文件）耗尽它。*修复：* 监控 `df -i`；在大测试集上限制逐样本评估可视化（大小规划 → verifying-dl-experiments）；一旦结果目录在本地验证，从 FS 中修剪其逐样本图片子目录；通过 `find /root/autodl-fs -type d -name '<vis-dir>' -exec rm -rf {} +` 快速释放 inode。

**AD5 — 数据盘满；HF 缓存是隐藏的占空间者；智能体 `rm` 被自动拒绝。** *症状：* `/root/autodl-tmp` 达100%但 `runs/` 看起来很小；智能体对"明显垃圾"的 `rm -rf` 被自动拒绝。*根因：* `~/.cache/huggingface` 被符号链接到数据盘，因此 **HF 模型缓存**（数十 GB）才是真正的占空间者；harness 阻止目标是智能体推断的不可逆 `rm -rf`。*修复：* 审计 `du -sh ~/.cache/huggingface/hub/models--* | sort -rh`；将 `HF_HOME` 设为选定的数据盘目录 + 保留指标/评估 JSON（微小证据）；展示确切删除目标 + 大小供用户显式确认；提供"清理 vs 扩容磁盘"。

**AD6 — base 就是环境；"永不使用 base"规则阻止每个远程命令。** *症状：* 本地"不在 conda base 中运行 DL"守卫在 `ssh autodl 'python train.py'` 时触发，但 `conda env list` 显示空且 `/root/miniconda3/envs/` 为空；调用 `python3` 的轮询脚本 exit 127。*根因：* 镜像将整个 DL 栈安装到 **base** — base 就是单租户项目环境（无 `/envs/`），且镜像通常只附带 `python`（无 `python3`）。*修复：* 使用 `/root/miniconda3/bin/python` 训练；豁免 remote-ssh + 实例 base 免受本地守卫约束（绝不 `conda create --clone base`）；在远程脚本中使用显式解释器或纯 shell，绝不用裸 `python3`。

**AD7 — 平台 TensorBoard 固定指向 `/root/tf-logs`；其他位置的事件不可见。** *症状：* 事件文件非空且 `curl http://127.0.0.1:6007/` 返回200，但 AutoPanel TB 面板显示0次运行；`/data/runs` 返回 `[]`。*根因：* 镜像自动启动 `tensorboard --logdir /root/tf-logs` 且面板代理该进程；`--logdir` 是硬固定的，容器内不可重新配置。*修复：* 写入 `SummaryWriter(log_dir="/root/tf-logs/<run>")`，或 `ln -sfn <your-tb> /root/tf-logs/<run>`（固定 TB 的 `--reload=5` 在约5 s 内识别）；用 `curl … /data/runs` 验证，而非 `ss`。（另外：在删除/重命名运行后重启 TB 服务器以清除陈旧缓存标签。）跨平台"实时面板静默空白"类别（任何平台上的路径/端口/进程不匹配）是通用形式 → `references/gotchas_universal.md` U39。

**AD8 — wandb 验证阶段在 epoch 1 结束时 CPU 内存飙升至30+ GB。** *症状：* 在 epoch 1 结束（验证）时，cgroup 内存从约8 GB 跳到30+ GB，有时卡住实例。*根因：* 项目训练器在 `step==1` 时记录逐样本分布（例如 LPIPS/VGG 在约2000个样本上 = 约30 GB 激活值）。*修复：* 限制验证时样本累加器 — `-o training.val_metric_sample_cap=256`（项目专属旋钮；检查训练器的等效配置）。与 DataLoader-worker cgroup OOM（通用陷阱）不同。

**AD9 — 项目 torch 版本锁定会降级镜像的工作构建。** *症状：* 镜像附带了支持新架构的 torch（sm_120）；项目锁定 `torch<2.9`；朴素 `pip install -r requirements.txt` 将其替换为缺少该架构内核的 wheel → 首次前向时 `no kernel image is available`。*根因：* 镜像的 torch/CUDA 构建与租赁的 GPU 架构匹配；项目锁定已过时。*修复：* 从远程安装中过滤框架锁定——`grep -ivE '^(torch|torchvision|torchaudio)' requirements.txt > /root/req_remote.txt && pip install -r /root/req_remote.txt` — 保留镜像构建；启动前用 `torch.cuda.get_device_capability()` + 重载导入做冒烟测试；随结果披露非标准 torch 版本。

---

## 8. SCRIPT OVERRIDES

为 AutoDL 参数化 `scripts/` 模板（`scripts/run_one.sh.template`，`scripts/run_queue.sh.template`）所需的确切值：

```sh
DATA_DIR=/root/autodl-tmp             # 快速 NVMe 数据盘 — 实时检查点、日志、HF 缓存
DURABLE_DIR=/root/autodl-fs           # 地域锁定共享 FS — 唯一在释放后存活的层级
PROXY_HOOK='source /etc/network_turbo 2>/dev/null || true'   # 任何外部调用前必须执行（AD1）
CRED_FILE=/root/.wandb_key            # 仅按实例 — FS 安全分类器阻止 wandb 密钥
SCRATCH='latest.pth'                  # 成功时清理；保留 best.pth（可保留产物）
HF_HOME=/root/autodl-tmp/huggingface_cache   # 重定向离开符号链接的 ~/.cache（AD5）
HF_ENDPOINT=https://hf-mirror.com     # + HF_HUB_DISABLE_XET=1（AD2）
DETACH=tmux                           # tmux 缺失时回退到 nohup（§6）
PY=/root/miniconda3/bin/python        # base 就是环境 — 显式解释器，绝不用裸 python3（AD6）
TB_LOGDIR=/root/tf-logs               # 平台 TB 固定在此处（AD7）
```

**凭证推送（AutoDL 专属）。** FS 安全分类器阻止匹配 wandb 密钥模式的文件——将密钥放在**按实例**的 `/root/.wandb_key`，绝不在 `/root/autodl-fs` 上。通过 stdin 精确流式传输一个凭证块，使密钥永不出现在命令中；wrapper 在启动前将其读入 `WANDB_API_KEY`。密钥-via-stdin 模式 → `references/ssh_transport.md`。

**校验同步（门控成功行）。** `run_one.sh` 将实时检查点写入 `$DATA_DIR/checkpoints/<name>`，成功时修剪 `latest.pth`，然后同步 `best.pth` 到 `$DURABLE_DIR/final_ckpts/<name>` **将成功 echo 门控在实际复制结果上** — 无条件的"synced"在 FS inode 上限（AD4）静默使 `mkdir`/`cp` 失败时撒谎（通用静默同步陷阱）。在本地验证下载完成之前，**数据盘**副本是事实来源。
