---
platform: vastai
kind: ssh-rental
meter_stop_verb: destroy        # 停止计费的动作；stop 永远收取磁盘费（计算关闭，存储开启）
meter_stop_irreversible: true   # destroy 永久删除容器磁盘
detach_primitive: tmux          # 登录时自动附着；容器重启时消亡 → onstart.sh 是持久钩子
spot_available: true            # interruptible（竞价）拍卖 — 平台核心
spot_grace: ~0s                 # 抢占是突然暂停，无文档化通知 / 无 SIGTERM
shared_fs: false               # 无平台范围 FS；Volume 是机器锁定（重启时绑定到特定 GPU）
inode_cap: host-dependent       # 无文档；取决于主机的 Docker 存储驱动
free_egress: host-dependent     # 已修正：主机设定带宽价格；按字节双向计费，通常 $0 但不保证
china_mirror_needed: false      # 无中国机房且无平台代理；在工作负载层面修复 HF
host_driver_cuda_max: image-dependent  # CUDA 在所选 Docker 镜像中；必须 ≤ 主机驱动
local_nvme: host-dependent
---

# vast.ai — 平台 Profile

一句话目的：以 **Docker 镜像在第三方主机上**租赁市场 GPU，运行 spot 可恢复作业，并在 `destroy` 之前**将结果复制出去**——唯一停止全部计费的动词。

> **预先告知用户（原则 #10）：** ⚠️ 危险时钟——**`stop` 的实例永远收取磁盘费**（只有 `destroy` 停止全部计费，而 `destroy` 删除一切）；**带宽/出口持续计费**，由主机定价。风险——仅租赁**已验证、高可靠性**且带直连端口的主机（未验证主机可能运行中途消失）；云同步即使在 stop 状态也有效（§5），最干净的持久目标。

**目录**（`grep -in '^## ' profiles/vastai.md` 跳转）：
- §1 LAUNCH — offer 驱动，Docker-镜像即环境
- §2 STORAGE MODEL — 按机器本地磁盘；生存矩阵；云同步逃生舱
- §3 NETWORK — 代理 vs direct SSH；随机端口；主机设定带宽；无中国代理
- §4 SPOT / INTERRUPTION + RESUME — 竞价拍卖，约0 s 暂停，GPU 绑定恢复，状态轮询循环
- §5 TEARDOWN / BILLING — `destroy` 是计费停止；`stop` 永远收取磁盘费；带宽始终计费
- §6 DAEMON TOOL — tmux 在重启时消亡；`onstart.sh` 是持久重新启动
- §7 TOP GOTCHAS — VAST1–VAST13，平台专属 + 平台专属调试
- §8 SCRIPT OVERRIDES — 参数化 `scripts/` 的值

通用陷阱不在本文重复——参见 `references/gotchas_universal.md`。Spot 节奏数学和原子恢复在 `references/spot-resilience.md`。

**重塑一切的一个事实：** vast.ai 是第三方主机的**去中心化市场**，不是统一的一线云。与 AutoDL 的分歧后果：**无平台范围共享 FS**、**无中国镜像代理**、**无单一预构建 conda 环境**（Docker 镜像就是环境）、**存储锁定到一台物理主机甚至一个 GPU ID**、**带宽由主机定价（非平台免费指定）**、**interruptible（竞价）抢占是真实的核心且突然的模型**。

---

## 1. LAUNCH

**入口**（全部等价）：web 控制台（`cloud.vast.ai`）、`vastai` CLI / Python SDK、REST API（`https://console.vast.ai/api/v1/...`，Bearer token）和 SSH 进入运行中的容器。CLI 是编排界面：`pip install vastai`，然后 `vastai set api-key $VAST_API_KEY`（仅环境变量名——绝不内联密钥）。

**环境契约 — Docker 镜像就是环境。** 默认不提供裸 VM；创建调用必须指定 `--image`（例如 `pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime`）。**CUDA 版本是镜像附带的**——与主机驱动不匹配是真实失败模式（VAST5）。镜像的默认 Python 环境是低摩擦运行地点——不要在租赁机上 `conda create`（remote-base 例外仍然成立）。注意：**不支持 Docker-in-Docker**"出于安全约束"（已验证 docs.vast.ai/.../faq/instances 2026-06）——容器化的内部运行时不是选项。

**启动是 offer 驱动且两步**（搜索市场 offer → 在其上创建）：

```bash
#!/usr/bin/env bash
set -u
# 1) 查找已验证、可租赁的 offer，至少一个直连端口，按 $/dlperf 最便宜排序
vastai search offers 'gpu_name=RTX_4090 num_gpus=1 verified=true rentable=true direct_port_count>=1' -o 'dlperf_usd-'
# 2) 在选定的 OFFER_ID 上创建；--direct 启用 direct-TCP SSH（见 §3）
vastai create instance OFFER_ID --image pytorch/pytorch:2.4.0-cuda12.4-cudnn9-runtime \
  --disk 50 --ssh --direct --onstart-cmd 'nvidia-smi && bash /workspace/onstart.sh'
```

`--onstart-cmd`（**最大16 KB**；更长脚本需 gzip+base64 编码）被写入 `/root/onstart.sh` 且**每次容器启动时重新运行**——这是平台原生启动钩子和持久重新启动路径（§6）（已验证 docs.vast.ai/cli/commands 2026-06）。严格过滤 offer：未验证、低可靠性的主机可能直接变为 `Offline`（VAST7）。启动不是即时的：主机必须**拉取 Docker 镜像并启动——通常1-5分钟取决于镜像大小**（已验证 docs.vast.ai CLI Hello World 2026-06）；大镜像卡在 `Loading` 是慢下载症状（VAST13）。

→ **验证：** `vastai show instance OFFER_ID` 列出新实例 `running`，且容器内 `nvidia-smi`（通过 `--onstart-cmd` 或首次 SSH）显示与镜像匹配的预期 GPU 和 CUDA。

---

## 2. STORAGE MODEL  *(生存矩阵 — 原则 #4)*

三层；持久性 + 地域故事是与 AutoDL 最大分歧——**没有地域范围的共享 FS**。（已验证 docs.vast.ai/.../storage/types 2026-06）

| 层级 | 路径 | 速度 | STOP 后存活？ | DESTROY 后存活？ | 容量 |
|---|---|---|---|---|---|
| 容器/实例磁盘（`--disk N`） | `/` + `/workspace` | 本地 | **是**（计费） | **否 — 消失** | 创建时固定，**不可调整**，最少 **10 GB**（默认） |
| Volume（本地） | 挂载路径 | 本地 | 是 | **是，直到 volume 被删除**（存在期间按 GB 计费） | 固定；**机器锁定**，不可调整 |
| 云同步（S3 / GDrive / Backblaze / Dropbox） | 机外桶 | 网络 | 是 | **是 — 完全机外** | 供应商的；**实例停止时也有效** |
| Network Volume（跨机器） | — | — | — | — | **不在当前存储文档中 — 视为不可用** |

**机器锁定——以及 GPU 绑定——是陷阱。** Volume "绑定到创建它的物理机器"且"无法在不同物理机器间迁移"。更糟，已停止的实例**绑定到特定 GPU ID**，不只是机器："实例创建时绑定到特定 GPU ID。如果实例停止，它仍然绑定到同一 GPU ID 并等待该 GPU 再次可用"（已验证 vast-ai.crisp.help scheduling article 2026-06）。所以一台机器可能显示**可供租赁**（其他 GPU 空闲）而已停止的实例卡在 `Scheduling` 等待*其* GPU（VAST3）。

**§5 动词下检查点必须写入的位置：** 容器磁盘上**没有在 `destroy` 后存活的持久挂载**——所以持久目标是**机外**。两条真正的机外路径：(a) 在 `destroy` 之前 `vastai copy` 结果到本地/另一实例/Volume；(b) **云同步**（`vastai cloud copy`）到 S3/GDrive/Backblaze/Dropbox——值得注意的是**实例停止时也有效**（已验证 docs.vast.ai/.../data-movement 2026-06），这使它成为 spot 作业最干净的持久目标。始终假设实例在其生命周期过期后丢失。Inode 上限和 FS 类型**无文档且取决于主机**（取决于主机的 Docker 存储驱动）— 每台主机 `df -i`，不要假设 AutoDL 式平台常数。

→ **验证：** 在任何拆除前，`vastai copy <id>:/path/to/ckpt local:/path/to/local` exit 0（或 `vastai cloud copy` 完成）且本地产物可加载（`scripts/verify_local.py`）。

---

## 3. NETWORK

**共享公网 IP + 随机外部端口。** 每个实例共享主机（通常共享的）公网 IP；"每个开放内部端口（如22或8080等）映射到*随机*外部端口"从 **"IP Port Info"弹出窗口**（实例上的按钮）或 `vastai show instance` 读取——格式 `PUBLIC_IP:33526 -> 8081/tcp`（已验证 docs.vast.ai/.../connect/networking 2026-06）。端口按实例变化——运行时发现，绝不硬编码。**硬上限每实例64个开放端口。**

**两种 SSH 风格——及 scp 大小陷阱：**
- **代理 SSH**（默认，通过 Vast 代理）："适用于所有机器，数据传输较慢。"它支持 `scp` 但被限速——vast 自己的指导是**代理 scp 仅用于约1 GB以下的传输**；超过时"建议使用直连 SSH 连接"（已验证 docs.vast.ai/.../data-movement 2026-06）。
- **直连 SSH**（direct-TCP 到主机）："需要开放端口的机器，更快更可靠，首选方法。"这是承载大型 `scp`/`rsync`/`vastai copy` 而不卡顿的方式。它**需要 offer 暴露开放端口** → 过滤 `direct_port_count>=1` 并以 `--direct` 创建。

**规则：** 如果批量传输必须工作，在创建时要求 **direct-TCP**。`vastai copy` "使用 rsync，通常快速高效，受单链路上传/下载约束"——对于多 GB 结果，使用 direct + 可恢复循环（`references/gotchas_universal.md` U12）。对于大型*入站*数据集，优先从云桶 `wget`/`curl` 而非代理 SSH（高得多的吞吐量）。自定义服务使用 Docker `-p`（例如 `-p 8081:8081`）；Jupyter 默认内部8080，由 `JUPYTER_TOKEN` 门控（通过 `JUPYTER_PORT` 覆盖端口）。

**带宽是计量的且由主机定价——非平台免费指定（已修正）。** "对发送到或从实例接收的每个字节收取带宽价格，无论处于什么状态"，且"定价由主机设定且特定于每个 offer"（已验证 docs.vast.ai/.../reference/billing + .../instances/pricing 2026-06）。实际上许多主机将出口定价为约 $0（vast 通常是低/零出口选项），但特定 offer **可能**双向按 GB 收费——在传输密集型作业前读取每个 offer 的带宽费率（悬停实例卡/搜索页面上的价格）。这就是为什么 frontmatter 是 `free_egress: host-dependent` 而非 `true`。

**中国相关性：平台层面无。** 无中国数据中心，无 `/etc/network_turbo` 等价物，无内置 HF 镜像。HF 不可达的问题在*工作负载*层面仍然存在（某些主机），但修复是作业**自己的** `HF_ENDPOINT=https://hf-mirror.com` / `hf_transfer`，不是平台脚本——见 `references/gotchas_universal.md`（HF 下载）的可恢复下载阶梯。

→ **验证：** 通过**direct**端点 `ssh <alias> 'echo ok'`，然后1文件 `vastai copy` 往返 exit 0。

---

## 4. SPOT / INTERRUPTION + RESUME  *(原则 #7/#8)*

vast.ai 的 **interruptible** 租赁是**实时连续竞价拍卖**——平台的便宜 GPU 核心（"可降低成本百分之五十甚至更多"），远比 AutoDL 上任何东西都更一线。（已验证 vast.ai/article/Rental-Types 2026-06）

- **竞价：** 客户设定出价；"当前最高出价是运行的实例，其他被暂停。" **On-demand 始终击败 interruptible**，无论出价金额（"on-demand 实例始终优先"）。
- **出价在创建时固定。** "竞价方法在实例租赁后无法更改"（已验证 Rental-Types 2026-06）——所以恢复杠杆**不是**"提高此实例的出价"。要恢复被出价超过的运行，要么等待更高出价完成，要么**在新的 offer 上重新启动相同作业**（更便宜/on-demand）——这就是为什么机外检查点（§2）很重要。
- **抢占 = 暂停，非销毁。** 被抢占的实例被暂停（磁盘存活）直到其出价重新获得最高优先级或更高出价完成。因为存储是机器/GPU 锁定的，它只能在**原始主机的原始 GPU**上恢复——可恢复性悬崖（VAST3）。
- **检测信号 + 宽限期：** **几乎无提前通知——将宽限期视为约0 s，突然暂停。** 无文档化的终止信号；SIGTERM 刷新处理器**不是**安全网。通过 API 检测：`show_instance` 返回 `actual_status`（当前容器状态）、`intended_status`（期望状态）、`cur_state`（合约/硬件分配）和 `status_msg`（人类可读字符串，例如 "success, running ..."）（已验证 docs.vast.ai/api-reference/instances/show-instances 2026-06）。被抢占的实例停止 `running`；UI 显示 **Inactive**（停止，数据保留）/ **Scheduling**（等待 GPU 释放）/ **Offline**（主机消失）。
- **恢复钩子：** 等待更高出价完成或重启实例；它仅在同一 GPU 仍然空闲时返回 `Scheduling → running`（否则卡住——VAST3），然后 **`/root/onstart.sh` 重新运行**并重新启动训练（§6）。作业本身必须是 checkpoint-resumable 的（`--resume`，无条件 load-latest），以便相同命令幂等恢复。

**编排模式：** 在定时器上轮询 `actual_status` / `status_msg`；抢占时重启（或在新 offer 上重新启动）并让 `onstart.sh` + checkpoint-resume 恢复。节奏公式（Young/Daly）和原子 temp→fsync→rename 恢复 → `references/spot-resilience.md`。

→ **验证：** kill-and-resume 演练 — `vastai stop instance <id>` 然后 `start`；作业从最后检查点步骤恢复，而非 epoch 0。

---

## 5. TEARDOWN / BILLING  *(原则 #9 + 铁律)*

这是最容易出错的章节——必须精确。（已验证 docs.vast.ai/.../reference/billing + .../manage-instances 2026-06）

- **`destroy` 是唯一停止全部计费的动作**（计算**和**磁盘）。它是**不可逆的** — 所有容器磁盘数据被永久删除。（`vastai destroy instance <id>`）
- **`stop` 是陷阱：** 它分离 GPU 并停止计算计费，但**磁盘在停止状态下继续无限计费**——"停止实例不避免存储成本"，"即使余额为负也将继续收取磁盘存储费"。vast.ai 上第一大意外账单。"已停止" ≠ "计费关闭"。
- **带宽在任何状态下都计费。** "对发送或接收的每个字节收费……无论处于什么状态"——所以即使是与*已停止*实例的传输（云同步）也累积主机设定的带宽成本（§3）。
- **Volume 在实例销毁后继续计费**，直到卷本身被删除（"卷存在期间按 GB 收费"，独立于实例）。
- **On-demand 实例在主机设定的生命周期到期时自动停止** — "当租赁结束日期到达时，租赁合约过期，实例被停止。"数据保留直到被销毁。无人值守的作业可能静默结束，所以像随时可能消失一样做检查点。
- **零/负余额 → 删除。** 在 $0.00 时"你的实例、存储卷和数据将被安排删除，除非你添加信用"；无已保存卡片时"你的实例和存储数据将被销毁"。有"短暂的宽限期，余额可能变负后才发生删除"——不要依赖它。
- **轮询循环成本陷阱：** 无 timeout/错误检查的状态轮询循环将在实例继续累积磁盘 + 带宽费用时永远循环。每个轮询循环用 `timeout` + 退出检查限定。

**拆除铁律（vast.ai 实例）：** 在检查点被**复制到机外并通过加载验证**之前不得 `destroy`——要么通过 `vastai copy` 到本地（`scripts/verify_local.py` 报告100% OK）要么通过 `vastai cloud copy` 确认——复制退出状态已检查（VAST2），且用户已**显式批准**影响成本的操作。"日志里看着完成了"不是证据（原则 #3）。因为 `destroy` 删除磁盘且**无共享 FS 可回退**，确认门控在这里更重要，而非更不重要。

---

## 6. DAEMON TOOL

- **SSH 登录时自动 tmux**（与 AutoDL 相同）：登录时附着 tmux 会话"以在断开连接时保持会话活跃。"用 `touch ~/.no_auto_tmux` 禁用然后重新连接（已验证 docs.vast.ai jupyter-ssh FAQ 2026-06）。
- **tmux 在 SSH 断开后存活但不在容器重启/重启/spot-resume 后存活** — 重启或 spot-resume 擦除 tmux 会话。**持久重新启动钩子是 `/root/onstart.sh`**（`--onstart-cmd`），它在每次容器启动时重新运行。将训练重新启动放在那里，**不是** tmux 中，以便 spot-resume 真正重启作业。
- **SSH 密钥仅适用于添加密钥后创建的实例** — 现有实例不会自动获取新密钥。在创建前设置账户密钥，或通过 `onstart` 注入。粘贴的密钥缺少 `ssh-rsa`/`ssh-ed25519` 前缀或 `user@host` 后缀会认证为密码提示——复制整行（已验证 docs.vast.ai jupyter-ssh FAQ 2026-06）。
- **原生队列：** vast.ai 有 **Serverless / autoscaler** 用于队列式工作负载，但单实例训练无托管调度器——编排器 + `onstart.sh` + checkpoint-resume **就是**队列。

---

## 7. TOP GOTCHAS  (平台专属；症状 → 根因 → 修复)

通用陷阱（CRLF、cgroup OOM、静默同步、HF 卡顿、僵尸 VRAM、GPU-0%-利用率、scp 重置、出口附加费）在 `references/gotchas_universal.md` 中——不在本文重复。

- **VAST1 — "已停止"实例的意外账单。** 症状：已停止的闲置实例持续数天收费，甚至超过负余额。→ 根因：`stop` 仅停止计算；**磁盘在停止状态下永远计费**，且带宽在任何状态下都计费。→ 修复：要停止计费，**`destroy`**（在按 §5 复制出去之后）；绝不仅用 stop 来"省钱"。
- **VAST2 — 拆除后结果丢失。** 症状：执行 `destroy`，检查点不可恢复。→ 根因：`destroy` 永久销毁容器磁盘且**无平台范围 FS 可回退**。→ 修复：在 `destroy` 之前 `vastai copy` 出去（或 `vastai cloud copy` 到桶）并**检查其退出状态**；将成功行门控在复制结果上，而非日志声明。
- **VAST3 — 暂停/停止的实例卡在 `Scheduling` 但机器显示"可用"。** 症状：被抢占或停止的运行永不恢复；门户仍列出同一台机器可供租赁。→ 根因：实例**绑定到特定 GPU ID**（非机器）；如果该 GPU 被重新租赁，它会无限等待而主机上*其他* GPU 保持空闲。"如果卡住超过30 s，GPU 可能已被其他用户租赁。"→ 修复：停止调度尝试，**在同一主机上创建新实例并重新挂载同一 Volume**（可行因为其他 GPU 空闲），或从机外检查点重新在另一个 offer 上启动；不要等待同一 GPU 回来（已验证 vast-ai.crisp.help + manage-instances 2026-06）。
- **VAST4 — 作业在步中途无警告消亡。** 症状：interruptible 运行突然消失。→ 根因：竞价抢占**约0 s 通知且无 SIGTERM**；刷新处理器从不触发。→ 修复：按 Young/Daly 定时器周期性检查点到磁盘 + load-latest-on-resume；轮询 `actual_status`/`status_msg` 并重启（§4，`references/spot-resilience.md`）。出价无法在运行实例上提高——如果 GPU 已不在则重新在其他地方启动。
- **VAST5 — 新机器上 CUDA 驱动不匹配。** 症状：`torch.cuda.is_available()` 为 False / 驱动不匹配错误。→ 根因：**CUDA 在 Docker 镜像中，非主机**；镜像的 CUDA 可能比主机驱动支持的新（镜像 CUDA 必须 ≤ 主机驱动）。→ 修复：选择 CUDA ≤ 主机驱动的镜像；在 `onstart` 中训练前验证 `nvidia-smi`/`nvcc`（通用三角：`gotchas_universal.md` U28）。
- **VAST6 — 服务在其"自有"端口上不可达。** 症状：TB/Jupyter/API 在内部端口上不可达。→ 根因：内部端口映射到**随机外部端口**且每实例有**64端口上限**。→ 修复：创建时用 `-p` 开放端口，**运行时发现外部映射**（`vastai show instance` / IP Port Info 弹窗），绝不硬编码端口。
- **VAST7 — 主机运行中途消失。** 症状：实例翻转为 `Offline`，工作丢失。→ 根因：这是**市场** — 未验证/低可靠性的主机可能断线。→ 修复：过滤 offer 为 `verified=true`、高 `reliability` 和 `direct_port_count>=1`；将任何单台主机视为一次性的并相应地将检查点存到机外。
- **VAST8 — 默认 SSH 上批量 `scp` 卡住/爬行。** 症状：多 GB 结果在默认端点上复制挂起或以滴流速度运行。→ 根因：**默认是代理 SSH**，被限速且仅推荐 <1 GB；大传输需要 direct-TCP。→ 修复：以 `--direct` 创建（offer 必须有 `direct_port_count>=1`）并使用该端点进行 `scp`/`vastai copy`；大型*入站*数据优先从桶 `wget`/`curl`（已验证 data-movement docs 2026-06）。
- **VAST9 — 带宽出现在账单上。** 症状：传输密集型作业成本超过 GPU 小时费。→ 根因：带宽**由主机定价且双向按字节计量，在任何状态下** — 有些 offer 不是 $0 出口。→ 修复：在承诺前读取每个 offer 的带宽费率；将数据集拉取**一次**到持久本地/Volume，而非每 epoch 从远程桶拉取（通用形式：`gotchas_universal.md` U14/U15）。
- **VAST10 — 磁盘满，且无法扩容。** 症状：运行中途 `No space left on device`；`--disk` 无法提高。→ 根因：容器磁盘**创建时固定（最少10 GB）且不可调整**；Docker 层 + HF 缓存 + 检查点超出它。→ 修复：创建时超额预配置 `--disk`；将 `HF_HOME` 重定向到数据盘；修剪 `latest`/periodic 检查点，仅保留 `best`（inode/byte 审计：`gotchas_universal.md` U6/U7）。
- **VAST11 — 烘焙进镜像或 onstart-cmd 的密钥可被恢复。** 症状：构建时嵌入的密钥或在 `--onstart-cmd` 中的密钥被平台存储。→ 根因：镜像层和16 KB onstart 字符串在服务器端持久保存。→ 修复：在创建时通过**环境变量**注入 `WANDB_API_KEY`/`HF_TOKEN`，绝不烘焙进镜像层或 `--onstart-cmd`；运行时通过 stdin 流式传输凭证（`gotchas_universal.md` U34）。
- **VAST12 — 假设存在跨机器 Network Volume。** 症状：计划依赖 Volume 随作业迁移到不同主机。→ 根因：Volume 是**机器锁定**的；跨机器 Network Volume **不在当前存储文档中**。→ 修复：设计为机外持久（`vastai cloud copy` 到桶），非可移植卷；仅同机器重新挂载可靠。
- **VAST13 — 实例卡在 `Loading`，永远不到达 `running`。** 症状：新实例在 `Loading`/`Connecting` 状态停留多分钟。→ 根因：主机在**拉取大型 Docker 镜像**（启动需1-5分钟，大镜像更长）或主机链路慢。→ 修复：等待文档化窗口，然后读取 `vastai show logs <id>`（下文）查看拉取进度；如果仍卡住，`destroy` 并在更快的 offer 上以更小的镜像重新创建。

### 平台专属调试（命令 + 检查什么）

- **从机外读取启动/容器/系统日志：**
  `vastai show logs <id> --tail 200 [--filter <grep>] [--daemon-logs]` — 将容器日志（以及带 `--daemon-logs` 的主机/系统日志）上传到生成的 URL。这是无法连接的机器、卡住的 `Loading` 或静默 `onstart` 失败的第一站（已验证 docs.vast.ai/api-reference/instances/show-logs 2026-06）。GUI 等价是实例卡上的**"Logs"按钮**。
- **无 SSH 检查实时状态机：** `vastai show instance <id>`（或 API）— 比较 `actual_status`（容器*在哪里*）、`intended_status`（*应该*在哪里）、`cur_state`（合约/硬件分配）和 `status_msg`。`intended=running` 但 `actual≠running` + `Scheduling` ⇒ VAST3（GPU 绑定等待）；`Offline` ⇒ VAST7（主机消失）。
- **确认 GPU 确实附着：** 在 `onstart` / 首次 SSH 中运行 `nvidia-smi` 和 `python -c "import torch; print(torch.cuda.is_available(), torch.version.cuda)"` — `False`/CPU-only ⇒ VAST5（镜像 CUDA > 主机驱动）或无 GPU 容器（`gotchas_universal.md` U31）。
- **检测机箱内卡住的下载：** `du -sh ~/.cache/huggingface/hub` 随时间变化（无增长 = HF 拉取卡住）、`df -h /`（在填充 = 活跃下载）和 `df -i /`（inode），然后是 `gotchas_universal.md` 中的可恢复下载阶梯。SSH 前的大镜像卡顿仅通过 `vastai show logs` 可见。
- **找到真实外部端口 / SSH 目标：** `vastai show instance <id>` 列出端口映射，`vastai ssh-url <id>` 打印连接字符串 — 绝不假设端口22可达（VAST6）。

---

## 8. SCRIPT OVERRIDES

为 vast.ai 参数化 `scripts/` 模板的值：

```bash
# DATA_DIR — 数据 +（仅）检查点挂载；无任何内容在 destroy 后存活，所以持久 = 机外复制/云同步
DATA_DIR=/workspace              # 容器磁盘；stop 后存活，永远计费，destroy 后消失
DURABLE_DIR=off-box              # 无 destroy 后存活的挂载：在 destroy 前 vastai copy / vastai cloud copy（§5）
# PROXY_HOOK — 平台层面无（无 /etc/network_turbo）。HF 镜像是作业自己的环境（如需）：
PROXY_HOOK=''                    # 仅在主机无法访问 HF 时在作业环境中设置 HF_ENDPOINT=https://hf-mirror.com
# CRED_FILE — 空：vast 的密钥是 VAST_API_KEY 环境变量，非文件。WANDB_API_KEY/HF_TOKEN 也通过环境到达。
CRED_FILE=""                     # 磁盘上无凭证文件 → run_one 的 [ -n "$CRED_FILE" ] 守卫跳过 cat；VAST_API_KEY + WANDB_API_KEY/HF_TOKEN 在创建时通过环境注入，非镜像或 onstart-cmd
# SCRATCH — 要清理的内容（磁盘固定大小，不可调整 → 积极修剪）
SCRATCH='latest.pth periodic-*.pth *.tmp ~/.cache/huggingface/hub/blobs'  # 仅保留 best + 微小评估 JSON
# HF_HOME — 将缓存重定向离开小根分区到数据盘
HF_HOME=/workspace/.cache/huggingface
# DETACH — 持久重新启动是 onstart.sh，非 tmux（tmux 在容器重启/spot-resume 时消亡）
DETACH='/root/onstart.sh'        # 每次容器启动时重新运行；tmux 仅用于附着的 SSH 会话
```

**密钥说明：** 在创建时通过**环境变量**注入 `WANDB_API_KEY` / `HF_TOKEN`，绝不烘焙进 Docker 镜像层或16 KB `--onstart-cmd`（两者都被平台存储 — VAST11）。
