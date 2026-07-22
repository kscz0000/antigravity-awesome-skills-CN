---
platform: runpod
kind: ssh-rental
meter_stop_verb: terminate       # stop 释放 GPU 但仍以2倍费率收取卷磁盘费；只有 terminate 停止计费
meter_stop_irreversible: true    # terminate 删除容器 + 卷磁盘；只有 Network Volume 存活
detach_primitive: tmux           # 需先 apt-install；在 SSH 断开后存活，不在 Pod stop/restart 后存活
spot_available: true
spot_grace: ~5s                  # Spot/interruptible 抢占时 SIGTERM → SIGKILL 窗口
shared_fs: false                 # 全局网络 = 仅私有 IP；Network Volume 在单个数据中心内共享，不是全局 FS
inode_cap: none                  # 按 GB 配额，无文档化的 inode 上限
free_egress: true                # 无出口费；下载/上传到开放互联网免费
china_mirror_needed: false       # 无中国大陆机房，无 GFW — 使用 HF_HUB_ENABLE_HF_TRANSFER=1，非镜像
host_driver_cuda_max: image-dependent   # 主机驱动因机器而异；通过 CUDA-Version 过滤器选择（RP9）
local_nvme: true
---

# RunPod — 平台 Profile

一句话目的：RunPod Pods 的平台底层——**Docker 镜像就是环境契约**，三层存储模型中持久挂载与停放挂载不同，且拆除动词（`terminate`）会删除卷磁盘。在 Phase 0 之前阅读；它拥有 SKILL.md 各阶段委托的每个路径、端口、计费动词和 spot 规则。通用陷阱不在此重复——参见 `references/gotchas_universal.md`。

> **预先告知用户（原则 #10）：** 便利——RunPod 的 HTTP 代理自动 HTTPS 暴露 TB/Jupyter（无需隧道）。⚠️ 危险时钟——**已停止的 Pod 仍以2倍费率收取卷磁盘费**且可能以**零 GPU**重启（RP1/RP4），所以 stop 不是安全停放；**低账户余额自动删除** Pod；**~5 GB 容器磁盘**静默填满（重定向缓存，§8）。将持久状态解耦到 Network Volume + **terminate** 以真正停止计费。

快速跳转：`grep -in <keyword> profiles/runpod.md`（例如 `terminate`、`network volume`、`scp`、`zero-gpu`、`CUDA`、`interruptible`）。

目录：1 LAUNCH · 2 STORAGE MODEL · 3 NETWORK · 4 SPOT / INTERRUPTION + RESUME · 5 TEARDOWN / BILLING · 6 DAEMON TOOL · 7 TOP GOTCHAS (+ 平台专属调试) · 8 SCRIPT OVERRIDES

**与 AutoDL 的心智模型转变（打破可移植性的一个事实）：** AutoDL 在关机后保留 `/root`，所以"关机省钱，稍后重启"是安全的。在 RunPod 上，已停止的 Pod 被**固定到一台物理机器且其 GPU 可被租走**（重启零 GPU，RP1），并且它仍以2倍费率收取卷磁盘费（RP4）。Stop 不是安全停放。将持久状态解耦到 **Network Volume** 并 **terminate** 以真正停止计费。

---

## 1. LAUNCH

一个 Pod = GPU 主机上的一个 Docker 容器。五个等价入口：

- **Web 控制台** — 选择 GPU + 模板（Docker 镜像），Secure 或 Community Cloud，On-Demand 或 Spot/interruptible。模板（镜像 + 端口 + 环境变量 + 卷挂载）是可复现性的单元。
- **`runpodctl` CLI** — `runpodctl create pod --imageName=<img> --gpuType=<id>`，然后 `start|stop|remove pod <id>`、`get pod`。每个官方模板 Pod 预装 `runpodctl` 及 pod 范围密钥（已验证 docs.runpod.io/runpodctl 2026-06）。
- **REST API** — 当前一流的自动化接口：`POST /v2/pods`（以及 `/pods/{id}/start|stop`、`DELETE`）。创建 body 接受 `cloudType: SECURE|COMMUNITY` 和 **`interruptible: true|false`** 用于 Spot（已验证 docs.runpod.io/api-reference/pods/POST/pods 2026-06）。**(新 — 当前事实)** 较新的 REST 创建 Pod 输入**没有 `bidPerGpu` 字段**；interruptible 是普通布尔值。旧版 **GraphQL** `podRentInterruptable`/`bidPerGpu` 竞价变更仍存在于旧 API 接口——如果脚本设置了竞价，走的是 GraphQL 路径，非 REST。
- **Python SDK** — `runpod` pip 包，封装 API + serverless-worker SDK。
- **自定义 Docker 镜像** — 任何镜像都可用；官方 RunPod 模板预配置 SSH 守护进程 + `/start.sh`，但**自定义镜像必须自行启动 `sshd`** 且必须使用 **`CMD`，而非 `ENTRYPOINT`**（RP10）。

**环境契约 — 镜像就是环境。** RunPod 交付调用者指定的容器，而非预构建的 base conda 环境（AutoDL 模型）。通过 `@sha256:` 摘要固定镜像，而非 `:latest`，以确保可复现性。"在 `base` 中运行没问题"仍然成立（容器是临时的）——但任何位于**卷挂载（`/workspace`）之外**的环境、conda/pip 安装或代码在 stop 时消失（§2）。将长期环境安装在 `/workspace` 下，或烘焙进镜像。

---

## 2. STORAGE MODEL  *(生存矩阵 — 原则 #4)*

三层，各有不同的存活语义。这是 RunPod 上最容易出错的领域。

| 层级 | 路径 | 速度 | 容量 | 价格（已验证 docs.runpod.io/pods/pricing + storage/types 2026-06） |
|---|---|---|---|---|
| 容器磁盘 | `/`（overlay fs，系统管理） | 本地 NVMe | GB 配额；**默认约5 GB（如未提高）** | $0.10/GB/月运行中，**停止时不收费** |
| 卷磁盘（按 Pod） | `/workspace`（默认） | 本地 NVMe | GB 配额，**仅增不减** | $0.10/GB/月运行中，**$0.20 停止时（2倍）** |
| Network Volume | `/workspace`（Pod）· `/runpod-volume`（Serverless）· `/workspace` 每节点（Instant Clusters） | 网络 | 4 TB 软上限（**>4 TB 需支持**） | 标准 $0.07/GB/月（→1 TB 以上 $0.05）；**高性能 $0.14/GB/月（约3倍吞吐量）** |

**生存矩阵：**

| 层级 | STOP 后存活？ | TERMINATE 后存活？ | 跨 Pod 可移植？ |
|---|---|---|---|
| 容器磁盘 | **否**（stop 时擦除） | 否 | 否 |
| 卷磁盘 | **是**（保留直到 Pod 被删除） | **否**（terminate 时删除） | 否（固定到该 Pod） |
| Network Volume | 是 | **是** | **是**（在单个数据中心内可共享） |

**如果 `terminate` 是预期的拆除动词（§5），检查点必须写入 Network Volume**——按 Pod 的卷磁盘在 terminate 时被删除，所以仅在 stop 下安全但非 terminate 安全的持久状态在计费真正停止的那一刻就丢失了。

关键属性：
- **容器磁盘默认很小（约5 GB）**— pip wheel、HF 缓存、apt 和 conda 都默认落到 `/` 并静默填满它；创建时提高容器磁盘大小或重定向每个缓存到 `/workspace`（RP11，§7-调试）。
- **卷磁盘只增不减**——保守地超额预配置；缩容需要新 Pod（已验证 docs.runpod.io/pods/storage/types: "Increase only" 2026-06）。
- **Network Volume 是机房锁定的** — 挂载一个会将所有未来 GPU 部署约束到该机房，"可能限制 GPU 可用性并减少故障转移选项"（已验证 docs.runpod.io/pods/storage/create-network-volumes 2026-06）；在 Pod 上它必须在**创建时挂载且之后无法分离**（RP7）。跨机房迁移是手动的：在两个桥接 Pod 之间 rsync/`runpodctl`，或使用 **S3 兼容 API**（无需启动计算即可管理文件）。
- **并发写入损坏** — "多个 worker 同时写入同一卷可能导致数据损坏"（已验证同页 2026-06）。序列化写入者；对于并行消融扇出，为每个 cell 分配**隔离写入路径**（见 `references/parallel_ablation.md`）。
- **无文档化的 inode 上限** — RunPod 规范是 GB 配额，非 inode 计数。用 `du` 在实际挂载上审计 GB 用量；`references/gotchas_universal.md` 中的 `df -i` 纪律仍然适用于任何小文件多的评估树，但没有 AutoDL 式的 ~200K 硬上限。
- **Network Volume 无法加密**且对每个挂载的 Pod 可见——绝不在那里写入密钥（§8）。
- **全局网络 ≠ 共享 FS** — RunPod 全局网络给 Pod 提供私有 IP（`<POD_ID>.runpod.internal`）用于 Pod 间流量，不是共享文件系统（已验证 docs.runpod.io/pods/networking 2026-06）。共享*存储*仍是 Network Volume，单机房。

---

## 3. NETWORK

- **出口 / 代理 / 中国镜像：不适用。** 免费出口，区域覆盖北美 + 欧洲 + 大洋洲 + 亚太（例如 `AP-IN-1` 印度于2026-04新增），**无中国大陆数据中心**（已验证 runpod.io/blog/new-runpod-datacenter-now-live-ap-in-1 2026-06）。无 `/etc/network_turbo` 等价物且不需要中国镜像；`pip`/`hf`/`apt` 直接访问开放互联网。对于 HF 大分片卡顿，修复方法**不是**镜像——`pip install huggingface_hub[hf_transfer]` + `export HF_HUB_ENABLE_HF_TRANSFER=1`，并将 `HF_HOME` 指向 Network Volume 以便重下载在 Pod 轮换后存活（RP-G4 / RP11 下文；传输动词 → huggingface-skills:hf-cli **REQUIRED**）。
- **暴露服务的两种方式**（已验证 docs.runpod.io/pods/configuration/expose-ports 2026-06）：
  1. **HTTP 代理** — `https://<POD_ID>-<INTERNAL_PORT>.proxy.runpod.net`，自动 HTTPS。**硬100 s Cloudflare 超时** — 不在100 s 内响应的服务关闭并返回 **524**；长/流式/大载荷请求会死。适合 TensorBoard（6006）/ Jupyter（8888）UI；影响 WebSockets 和长轮询。
  2. **Direct TCP** — 公网 IP + **随机外部端口**，每次 Pod 重置时变化。SSH-scp、DB、WebSockets、长轮询需要此方式。在 TCP 配置中请求**70000以上**的端口号以获得**对称（外部 == 内部）映射**（"不是有效端口号，但信号 RunPod 分配匹配的内外部端口"）。
- 一个端口不能同时以 HTTP 和 TCP 暴露。
- **公网 IP 稳定性因云而异（新 — 当前事实）：** Community Cloud 公网 IP **可能在迁移/重启时变化**；Secure Cloud IP "应保持稳定"（已验证 expose-ports 2026-06）。固定 SSH 目标在 Secure Cloud 上更安全。
- **SSH 风格 — 代理 SSH 无法传输文件。** *Basic SSH* 通过 `ssh.runpod.io` 代理（到处可用但**不支持 `scp`/`sftp`/`rsync`**）。*Full SSH* 是直接 TCP 到 Pod 的公网 IP 暴露端口22（支持 `scp`/`rsync`，需要公网 IP Pod + TCP 22 暴露 + 运行中的 SSH 守护进程 + 账户上的密钥）。批量代码/数据传输必须使用 full SSH（RP6）。无公网 IP 时，使用 **`runpodctl send` / `receive`**（一次性代码，无需 API 密钥，预安装）移动文件——但它定位为**仅限中小文件**；大型数据集使用 full-SSH rsync（RP12）。SSH 配置 + 可恢复 rsync 模式 → `references/ssh_transport.md`。

---

## 4. SPOT / INTERRUPTION + RESUME  *(原则 #7/#8)*

两种购买模式，两种不同的中断向量：

- **Spot / interruptible** — 设置 `interruptible: true`（REST）或通过旧版 GraphQL 竞价。比 On-Demand 便宜约**50%**（已验证 runpod.io/blog/spot-vs-on-demand-instances-runpod：例如 A6000 spot $0.232 vs on-demand $0.491/gpu/hr 2026-06；其他营销材料引用"高达60%"）。中断是"无通知"的——另一个用户的 On-Demand 请求可以回收 GPU。检测信号：**`SIGTERM`，然后约5 s 后 `SIGKILL`** — 仅够刷新标志或触发已频繁的检查点，不够写入全新大型检查点。
- **On-Demand** — 运行中不可中断，但携带更隐蔽的**重启零 GPU**陷阱（RP1）：已停止的 Pod 固定到其主机，如果该 GPU 被租走，Pod 只能以**零 GPU**重启（"你 Pod 运行的机器上没有可用的 GPU" — 已验证 docs.runpod.io/references/faq 2026-06）。将其作为数据恢复启动，而非计算启动。

**两种向量要求相同设计：** 将完整状态**持续按定时器检查点到 Network Volume**（原子 temp→fsync→rename），启动时**无条件** load-latest，并在**新主机**上重新启动——绝不假设 stop 后同一机器/GPU 可用。约5 s 宽限期仅是机会性的最后刷新，绝非主要持久性机制。节奏公式（Young/Daly）和原子恢复模式 → `references/spot-resilience.md`。

---

## 5. TEARDOWN / BILLING  *(原则 #9 + 铁律)*

| 操作 | 停止计算计费？ | 停止存储计费？ | 删除数据？ |
|---|---|---|---|
| **Stop** | 是（释放 GPU） | **否 — 以2倍费率收取卷磁盘费（$0.20/GB/月）** | 否，但 GPU 可能在重启时丢失（零 GPU，RP1） |
| **Terminate** | 是 | 是（对于该 Pod） | **是 — 删除容器 + 卷磁盘，不可逆。** 只有 Network Volume 存活 |

- **Stop 是陷阱，不是安全停放。** 它不停止计费（卷磁盘继续以*双倍*费率收取），且有零 GPU 锁定风险。长期停止的 Pod 静默流血——`terminate` + Network Volume 对任何超过短暂暂停的闲置期都更便宜。
- **Terminate 是计费停止动词且它是破坏性的。** "Terminating 永久删除所有未存储在 network volume 中的数据。请先导出重要数据。"（已验证 docs.runpod.io/pods/manage-pods 2026-06）。在 terminating 之前将每个需要的产物移到 Network Volume（然后以 $0.07/GB/月计费）或下平台。如果拆除时检查点仍只在按 Pod 的**卷磁盘**上，将它们 rsync 到 Network Volume **或先拉取到本地**——Network Volume 无法在创建后挂载到现有 Pod（§2 / RP7），所以此救援必须在 Pod 仍然存活时进行。
- **低余额自动停止 → 静默删除（新 — 计费陷阱）。** 当账户余额无法覆盖剩余运行时间时，RunPod **自动停止所有 Pod**；存储然后在已停止的卷磁盘上继续累积，且**耗尽的余额可能导致 Pod + 存储被删除且无备份**（"Runpod 一旦因余额不足终止资源则无法恢复数据…不维护备份" — 已验证 contact.runpod.io Data-Loss-on-Low-Balance 2026-06）。此外，**陈旧已停止的 Pod 在约30天**不使用后被移除。磁盘费用**不可退款**。总结：被遗忘的 Pod 先耗尽信用，然后丢失数据——启用 Auto-Pay 或在离开前 terminate-with-Network-Volume。
- **计费粒度：** 计算 + 容器/卷磁盘按**秒**计费；Network Volume 按**小时**计费（已验证 docs.runpod.io/references/billing-information 2026-06）。
- Savings Plans 是预付的3或6个月不可退款承诺——独立的计费旋钮，与 stop/terminate 正交。

> **拆除铁律（SKILL.md Phase 5）：** 在检查点被**拉取到本地或在 Network Volume 上确认存在，并通过加载验证**，且用户已显式批准影响成本的操作之前，不得 `terminate`。在 RunPod 上计费停止动词按设计不可逆，且**无备份安全网**（上述低余额删除）——"日志里看着完成了"不是证据（原则 #3）。交叉链接：superpowers:verification-before-completion **REQUIRED**。

---

## 6. DAEMON TOOL

- **tmux** — 可用但**默认未安装**：`apt-get update && apt-get install -y tmux`。在 SSH 断开后存活；**不在 Pod restart/stop 后存活**（会话是容器范围的进程）。`screen`/`nohup` 同样是进程范围的——如果 tmux 不可用则使用 `nohup <cmd> </dev/null >log 2>&1 &`。
- **原生队列：Serverless** — RunPod 的 request→worker→result→scale-to-zero 系统。`executionTimeout` 和 `ttl` 各上限为**7天**（TTL 即使在作业中途也是硬 kill）。它是 request/response 形状的，为推理/批处理设计——**不适合交互式长训练**。
- **多日训练：Pod + tmux + 频繁检查点到 Network Volume**，通过 `runpodctl`/REST 编排。脱离原语（tmux）是可替换的插件；checkpoint-to-durable + resume-from-latest 主干（原则 #8）才是真正在 tmux 无法存活的重启后存活的。

---

## 7. TOP GOTCHAS  (平台专属；通用陷阱 → `references/gotchas_universal.md`)

- **RP1 — 重启零 GPU。** 症状：已停止的 Pod 重启时无 GPU 附着且拒绝计算工作（"Zero GPU Pods"）。根因：已停止的 Pod 绑定到其物理主机；另一个用户在停止期间租走了该 GPU。修复：将所有持久状态保留在 **Network Volume** 上，terminate 而非 stop，在新主机上重新启动。（已验证 docs.runpod.io/references/faq 2026-06）
- **RP2 — Stop 时容器磁盘被擦除。** 症状：stop 后代码、conda/pip 环境或检查点消失。根因：只有 `/workspace`（卷磁盘）或 Network Volume 在 stop 后存活；容器磁盘（`/`）被清除。修复：在 `/workspace`（或 Network Volume）下安装环境和写入所有状态。
- **RP3 — Terminate 不可逆地删除卷磁盘。** 症状：一个 `remove pod` 丢失所有检查点。根因：terminate 永久删除容器 + 卷磁盘；只有 Network Volume 存活。修复：在 terminating 之前将产物移到 Network Volume（或本地）并 verify-by-load（铁律，§5）。
- **RP4 — 已停止存储费用翻倍。** 症状："为省钱停止的"Pod 持续收费，比预期更快。根因：已停止的卷磁盘以 $0.20/GB/月（2倍运行费率）计费且永不到零。修复：对于闲置期，使用 terminate-with-Network-Volume 而非 stop。
- **RP5 — HTTP 代理100 s Cloudflare 超时。** 症状：通过 `*.proxy.runpod.net` 的长/流式/大载荷请求返回524。根因：固定的100 s Cloudflare 代理超时。修复：对 WebSockets、长轮询和大载荷使用 direct TCP（70000以上端口）；将 HTTP 代理保留给短 UI 请求。
- **RP6 — Basic（代理）SSH 无法 scp/rsync；外部 TCP 端口在每次重置时变化。** 症状：通过 `ssh.runpod.io` 的批量上传/下载失败，或硬编码的外部 SSH/服务端口在重启后停止工作。根因：代理 basic SSH 不支持 `scp`/`sftp`/`rsync`，且外部端口映射（及 Community Cloud 公网 IP）在每次重置时重新分配。修复：使用 full direct-TCP SSH（公网 IP + TCP 22 + 账户上的密钥），且绝不硬编码外部端口——每次（重新）启动后从 Connect → TCP 重新读取（Secure Cloud IP 比 Community 更稳定）。
- **RP7 — Network Volume 是机房锁定的且无法分离。** 症状：GPU 可用性意外受限，或 Network Volume 无法从 Pod 移除。根因：Network Volume 将所有未来部署固定到其数据中心，且必须在 Pod 创建时挂载，永远无法分离。修复：预先慎重选择机房；跨机房迁移通过桥接 Pod rsync 或 S3 API。
- **RP8 — 低余额自动停止后静默删除。** 症状：账户余额低后 Pod 消失且数据不可恢复；或 Pod 什么都不做却持续"每天"收费。根因：耗尽的余额自动停止 Pod（存储仍在计费），且余额耗尽/30天陈旧的 Pod 被删除且**无备份保留**。修复：启用 Auto-Pay 或在 Pod 闲置前 terminate-with-Network-Volume；将 Network Volume / 本地拉取视为唯一安全网（§5）。（已验证 contact.runpod.io 2026-06）
- **RP9 — CUDA 前向兼容错误（主机驱动太旧）。** 症状：容器在本地运行但在 RunPod 上抛出 `CUDA failure 804: forward compatibility was attempted on non supported HW`，或 `cuda>=12.x, please update your driver`，或 `OCI runtime create failed`。根因：分配机器的 NVIDIA 主机驱动比镜像的 CUDA 需求更旧（例如驱动525.x 在 CUDA 12.1 镜像下）。修复：在部署对话框中使用 **Additional filters → CUDA Version** 来要求驱动满足镜像最低需求的机器；或选择与可用驱动匹配的镜像。（已验证 github.com/runpod/containers/issues/67 2026-06）
- **RP10 — 自定义镜像中的 `ENTRYPOINT` 使模板启动命令静默。** 症状：自定义镜像部署但从不启动 `sshd` / handler / `/start.sh`；容器运行错误进程且 SSH 永不起来。根因：镜像 `ENTRYPOINT` 无法被 RunPod 模板的"容器启动命令"覆盖（它只覆盖 `CMD`）。修复：在 Dockerfile 中使用 `CMD ["/start.sh"]`（不是 `ENTRYPOINT`）以使模板覆盖生效。（已验证 github.com/runpod/runpodctl/issues/170 2026-06）
- **RP11 — 容器磁盘（约5 GB）填满，而非卷磁盘。** 症状：`pip install` / 下载中途出现"No space left on device"，尽管 `/workspace` 有空闲 GB。根因：pip wheel、HF 缓存、apt 和 conda 默认到 `/`（小的约5 GB overlay），而非 `/workspace`。修复：创建时提高容器磁盘大小，并将缓存重定向到卷上——`export HF_HOME=/workspace/hf PIP_CACHE_DIR=/workspace/.cache/pip`，在 `/workspace` 下安装 conda 环境。用 §7-调试命令诊断。（已验证 docs.runpod.io/pods/troubleshooting/storage-full 2026-06）
- **RP12 — Pod 上设置的环境变量在 full-SSH（over-TCP）会话中缺失。** 症状：通过 full SSH 访问时 `WANDB_API_KEY` / `HF_TOKEN` / 模板环境变量为空，尽管它们在 web 终端 / basic SSH 中存在。根因：SSH 守护进程的登录 shell 不继承启动时在 PID 1 上设置的容器环境。修复：显式传递少量所需的非密钥值，或在容器磁盘上以 `umask 077` 创建一个 root 所有/session-only 的文件并仅包含命名导出。绝不全量 dump `env`，绝不在 `/workspace` 或 Network Volume 下写入密钥快照。（已验证 leimao.github.io Setting-Up-Environment-Variables-SSH-Over-TCP-Runpod 2026-06）
- **RP13 — `runpodctl send/receive` 仅适用于小/中文件。** 症状：通过 `runpodctl send` 的大型数据集传输缓慢或不可靠。根因：一次性代码传输定位为"快速、偶尔、中小"交换，非批量数据。修复：对大型数据集使用 full-SSH `rsync`（RP6）或 Network-Volume S3 API；将 `send/receive` 保留给无公网 IP Pod 的无密钥一次性拉取。（已验证 docs.runpod.io/runpodctl/transfer-files 2026-06）

### 平台专属调试

RunPod Pod 异常时的快速检查（在 Pod 内运行，除非特别说明）：

- **哪个磁盘满了？** `df -h` — 分别读取 **`overlay`** 行（= 容器磁盘 `/`，通常仅约5 GB）和 **`/workspace`** 行（卷 / Network Volume）。`overlay` 满而 `/workspace` 几乎空是 RP11，不是真正的空间不足。最大占空间者：`find /workspace -type f -exec du -h {} + | sort -rh | head -n 10`（将 `/workspace` 换为 `/` 来追查容器磁盘膨胀）。如果 JupyterLab 中删除的文件没有释放空间，清空 `~/.local/share/Trash/` 和 `/workspace/.Trash*`。（已验证 docs.runpod.io/pods/troubleshooting/storage-full 2026-06）
- **GPU 确实附着？** `nvidia-smi` — 如果报错或显示无设备，怀疑重启零 GPU（RP1）或驱动/CUDA 不匹配（RP9）。交叉检查镜像 CUDA vs 主机驱动：`nvcc --version`（镜像）对 `nvidia-smi` 中的驱动行（主机）。
- **初始化卡住 / 镜像拉取？** 循环"initializing"的 Pod 通常是慢/失败的镜像拉取或被限速的机器。查看**容器日志**（web 控制台 → Pod 的 *Logs* 标签，或 `runpodctl get pod <id>`）；将模板克隆到不同机器/云通常能解决。
- **自定义镜像上 SSH 连不上？** 确认 `sshd` 确实在运行（`ps aux | grep sshd`），TCP 22 已暴露，Dockerfile 使用了 `CMD` 而非 `ENTRYPOINT`（RP10）；确认公钥在账户上且与本地私钥匹配。
- **SSH 上环境变量缺失？** 在 SSH shell vs web 终端中 `env | grep <VAR>` — 分歧是 RP12。
- **检测卡住的/僵尸下载：** 监视目标增长 — `watch -n5 'du -sh /workspace/hf 2>/dev/null; ls -la <partial-file>'`；`.incomplete`/`.part` 文件大小冻结意味着 HF 拉取卡住 → 用 `HF_HUB_ENABLE_HF_TRANSFER=1` 重跑（§3）。对于稳健的远程 ssh-poll 循环，见 `references/gotchas_universal.md` U17。
- **计费现实检查：** 运行计费器和剩余余额运行时间在 web 控制台计费页面；不要信任"应该很便宜因为已停止"——已停止的 Pod 仍以2倍费率收取卷磁盘费（RP4）且低余额会静默删除（RP8）。

---

## 8. SCRIPT OVERRIDES

为 RunPod 参数化 `scripts/` 模板的值：

- `DATA_DIR=` `/workspace`（按 Pod 的卷磁盘）— stop 安全的工作状态（代码、conda/pip 环境、进行中输出在 stop 后存活，不在 terminate 后存活）。
- `DURABLE_DIR=` 一个 **Network Volume** 挂载（Pod 上 `/workspace`，Serverless 上 `/runpod-volume`）— terminate 安全的持久检查点。当 `terminate` 是拆除动词时将 `DURABLE_DIR` 指向 Network Volume，以便 `best` 检查点在 Pod 删除和低余额自动删除后存活（RP8）。
- `PROXY_HOOK=` 无。无中国镜像。改为 `export HF_HUB_ENABLE_HF_TRANSFER=1`（在 `pip install huggingface_hub[hf_transfer]` 之后）。
- `CRED_FILE=""` — 磁盘上无凭证文件；密钥是 RunPod secret / 在 Pod 创建时注入的环境变量，所以 `WANDB_API_KEY` / `HF_TOKEN` 通过平台环境到达，`run_one` 的 `[ -n "$CRED_FILE" ]` 守卫跳过文件读取。**注意事项（RP12）：** full-SSH-over-TCP 登录 shell 可能看不到这些环境变量。优先使用平台 secret 或将命名值直接传递给需要它们的命令。如果临时桥接文件不可避免，以 `umask 077` 在容器磁盘上创建，仅写入命名需要的导出，使用后删除，绝不放在 `/workspace` 或 Network Volume 下。
- `SCRATCH=` Network Volume 下的 periodic/`latest` 检查点；仅保留 `best`（`save_top_k` 小）。修剪在这里更重要——卷磁盘只增不减且已停止存储双倍计价（RP4）。
- `HF_HOME=` Network Volume 上的路径（例如 Network-Volume 支持的 Pod 上 `/workspace/hf`），以便模型缓存在 Pod 轮换后存活而非重新下载——并且将缓存移出小的约5 GB 容器磁盘（RP11）。同样 `PIP_CACHE_DIR=/workspace/.cache/pip`。
- `DETACH=` `tmux`（在 `apt-get install -y tmux` 之后）；回退到 `nohup … </dev/null >log 2>&1 &`。两者都不在 Pod 重启后存活——checkpoint-to-Network-Volume 是弹性层。
