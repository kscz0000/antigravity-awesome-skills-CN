---
platform: paperspace        # Paperspace（现属 DigitalOcean）：Gradient Notebooks + Core/Machines
kind: cloud-api             # web 控制台 + pspace/gradient CLI/SDK + REST；Core 机器也可通过 SSH 访问
meter_stop_verb: shut-down  # shut-down/power-off 停止计算；仅 destroy/delete 停止存储 + IP
meter_stop_irreversible: false   # stop 可逆；destroy/delete 不可逆（丢失块存储）
detach_primitive: tmux      # 在 Core VM 上；Notebooks 没有干净的 SSH-daemon 方案（Jupyter kernel + 硬性 auto-shutdown 上限）
spot_available: false       # 无 AWS 式 spot/抢占带 2 分钟警告
spot_grace: n/a             # 中断来自启动时容量 + 确定性 auto-shutdown 时钟，而非驱逐
shared_fs: true             # Gradient /storage 按存储区域/集群在团队间共享
inode_cap: none             # /storage 和 Core 块存储均无文档化 inode 上限
free_egress: true           # 无文档化入站/出站费用
china_mirror_needed: false  # 美国/全球云，直连出站；无平台提供的代理
host_driver_cuda_max: "host-dependent"   # ML-in-a-Box / 模板预装 CUDA+driver 栈（通常滞后）
local_nvme: host-dependent  # Notebooks 上的临时工作区；Core 上的块存储
---

# Paperspace (DigitalOcean) — 平台 Profile

一句话定位：在 Paperspace Gradient（托管 Jupyter notebook/部署）和 Paperspace Core（原生 Linux VM，"Machines"）上运行分离 GPU 作业的基底 — 什么停止计费、什么在 stop 与 destroy 之间存活、以及终止每次长运行的 auto-shutdown 时钟。通用陷阱在此不重复 — 参见 `references/gotchas_universal.md`。

> **前置告知用户（原则 #10）：** ⚠️ 危险时钟 — **auto-shutdown 定时器终止每次 Notebook/Core 运行**（需有意识地设置；Gradient 免费 notebook 硬性上限 6 小时）；**快照 / 块存储在机器销毁后仍继续计费**（孤立泄漏）。提醒 — **Gradient CLI/API 已于 2024 年 7 月 15 日弃用**（锁定 `gradient<3.0`；三 CLI 混乱，§1）。

快速跳转：`grep -in '<keyword>' profiles/paperspace.md`。

## 目录
1. 启动 — Gradient vs Core，环境契约，三 CLI 混乱
2. 存储模型 — 生存矩阵，stop-保留-磁盘 规则，pip 不持久
3. 网络 — 公网 IP（静态 vs 动态），端口，SSH 风格
4. SPOT / 中断 + 恢复 — auto-shutdown 时钟，不是 spot
5. 拆除 / 计费 — 什么真正停止计费（陷阱）
6. 守护工具 — Core 上的 tmux；为什么 Notebook 抵抗守护进程
7. 主要陷阱 — `PS1`–`PS13`，平台专属 + 平台专属调试
8. 脚本覆盖 — `scripts/` 模板的值

---

## 1. 启动

两个产品系列，运营模式截然相反：

- **Gradient** — 托管层。**Notebooks** 是共享持久存储上的 web Jupyter IDE；
  **Deployments** 在 REST 端点后服务容器（自带 Docker 镜像 `<user>/img:tag`）；
  **Workflows** 运行 GPU 支持的 DAG 自动化。入口：web 控制台、CLI/SDK 或 REST。
- **Core / Machines** — 带持久块磁盘的原生 Linux/Windows VM，完整 root/SSH。OS 模板
  包括 **ML-in-a-Box**（预装 CUDA + PyTorch/TensorFlow/RAPIDS/Jupyter；**仅终端/SSH**，
  主目录 `/home/paperspace`，shell `/bin/bash`）。**H100 需要 Ubuntu 22.04，A100 推荐 22.04；其他机器类型推荐 Ubuntu 20.04**（已验证 github.com/Paperspace/ml-in-a-box
  README + DO machines docs 2026-06）。这是与 AutoDL tmux-弹性-训练模式最匹配的产品系列。

**环境契约。** 所选镜像/模板即 Python 环境 — **不要**在租赁机上 `conda create`
（原则：预构建基础即环境）。在 Core 上，直接在 **ML-in-a-Box** 内运行；在 Gradient
Deployments 上，环境是创建时指定的 Docker 镜像。因为 *destroy* 会擦除机器，环境的持久化等价物是一个 Docker 镜像加上保存在机外的 `requirements.txt`/lock 文件，使重建可复现。**在 Notebooks 上，普通的 `pip install` 在重启后不存活**（写入
`/usr/local/lib`，临时）— 见 §2 / `PS3`。

**三 CLI 混乱（影响所有自动化）。** 工具链在 DigitalOcean 收购后碎片化；
草稿中的"迁移到当前 API/CLI"低估了这个陷阱（已验证 github.com/Paperspace 2026-06）：
- **旧版 Gradient REST API 端点已于 2024 年 7 月 15 日弃用** — 过时调用返回 404 或无操作。
- **`gradient-cli` v2 已弃用**；仅锁定 `pip install "gradient<3.0"` 来保持*旧*脚本存活。
- **`gradient-python`**（github.com/digitalocean/gradient-python）**不是编排 CLI** — 它是新的 DigitalOcean *Gradient AI / GenAI 推理* SDK。**名称冲突** — 不要安装它来控制 notebook/machine。
- **新工作的推荐工具是简化的 `pspace` CLI**（github.com/Paperspace/cli，
  2026 年持续发布；如 `pspace public-ip release <ip>`）。在任何自动化中锁定并验证 CLI 二进制 +
  版本；不要假设 `gradient` ⇒ `pspace` 命令对等。

→ **验证：** Core 上 `ssh <core-alias> 'python -c "import torch;print(torch.cuda.is_available())"'`，或在 Notebook 中运行 `print(torch.cuda.is_available())` 单元格。

---

## 2. 存储模型  *(生存矩阵 — 原则 #4)*

定义性事实：**stop/shut-down 保留磁盘** — Paperspace 是此处少数几个在这方面像 AutoDL 的关机的 profile 之一。只有 **destroy/delete** 才移除存储。

**Gradient Notebooks** — `/storage` 和 `/notebooks` 是从 `/` 分叉的**独立分支，非嵌套**
（已验证 DO notebooks/details/storage-architecture 2026-06）：
- `/storage` — **共享持久**，团队范围，限定于**存储区域/集群**。stop 后存活。
  （团队共享 ⇒ 永远不要在这里写密钥 — 见 §7 / `references/gotchas_universal.md`。）
- `/notebooks` — **每 notebook 持久**，通过控制台 File Manager 管理。stop 后存活。
- 其他一切 — **临时工作区**（包括 `pip` 落地的 `/usr/local/lib`），stop 后擦除。

**Core 机器** — 块存储 **50 GB–2 TB**，跨 stop 持久；**扩容是单向的**
（"increasing block storage expands the filesystem and is not reversible"）。区域锁定：存储和自定义模板必须在**同一数据中心**使用。**快照**是独立计费资源
（`$0.29/GB/月`，默认策略为 **"Never" / 0 存储** — 仅在手动启用时计费，且快照
**在机器 destroy 后存活**，因此孤立快照持续收费 — 见 `PS9`）。

| 层级 | 路径 | STOP 后存活？ | DESTROY/DELETE 后存活？ | 容量 / 备注 |
|---|---|---|---|---|
| Notebook 共享持久 | `/storage` | 是 | 是（独立资源） | 按区域/集群团队共享；直到删除才停止计费 |
| Notebook 每 notebook | `/notebooks` | 是 | 否（随 notebook 消亡） | 每 notebook 持久；控制台 File Manager |
| Notebook 工作区 | 其他一切（含 `/usr/local/lib`） | **否** | 否 | 临时；stop 后擦除；`pip` 落地此处 |
| Core 块存储 | 机器 root + 块卷 | 是 | **否** | 50 GB–2 TB；扩容不可逆；区域锁定 |
| Core 快照 | (独立资源) | 是 | **是**（孤立计费！） | `$0.29/GB/月`；默认策略 Never/0；在机器 destroy 后存活 |

**检查点必须写入（对应 §5 拆除动词）：** Notebooks 上写入 `/storage`（跨 stop、
跨 notebook 删除）— `/notebooks` 在 notebook 本身被删除时会消亡。Core 上，块磁盘
跨 stop 存活，但 *destroy* 会擦除它，所以铁律要求的 destroy 前 pull-to-local 仍然适用。
两个层级均无文档化 inode 上限；仍需监控 `df -i`（通用，U7 / 原则 #5）。

---

## 3. 网络

- **出站。** 到 HF/GitHub/PyPI 直连无代理；无 `network_turbo` 风格加速器，无文档化出站费用。中国镜像相关性**不作为平台功能适用** — 仅当从中国境内操作且提供私有镜像时相关（此时 `references/china-network.md`）。
- **公网 IP。** Core 机器通过**公网 IP** 访问，分两种（已验证 DO
  machines/how-to/manage-public-ips 2026-06）：
  - **静态** — "the same IP address every time it powers on … remains in your account until you delete
    it." 用于固定稳定的 SSH/端点寻址。**直到删除前持续计费** — *包括机器关机期间*
    （见 §5 / `PS6`）。API/CLI 可以创建/释放**静态** IP，但**不能为现有机器添加动态 IP** — 动态 IP 必须在机器创建时请求。
  - **动态** — "assigned automatically when a machine powers on and deleted when it powers off"；每次启动获得**新 IP**，所以硬编码的 SSH 别名在重启后失效。**仅在机器运行时计费**（关机时自动释放 → 无空闲 IP 费用）。
  没有**公网 IP** 的机器与互联网隔离（且避免了 IP 费用）。**私有网络**提供团队隔离的地址池。
- **端口 / 服务。** 防火墙自行管理 — 开放端口以暴露服务。在 Core 上通过 SSH 隧道 Jupyter (8888) /
  TensorBoard (6006)：
  `ssh -L 8888:localhost:8888 -L 6006:localhost:6006 paperspace@<machine-ip>`
  （占位主机 — 替换为机器的真实 IP/静态地址）。在 Gradient Notebook 中，在 Jupyter 内启动 TensorBoard，日志写入 `/storage` 下（否则 stop 后消失）。
- **SSH 风格。** Core = 标准 Linux VM → 完整 `ssh`/`scp`/`rsync`（ML-in-a-Box 默认用户
  `paperspace`）。Gradient Notebooks 暴露的是 **Jupyter 沙箱**，不是干净的持久 SSH daemon —
  对于多日无人值守运行没有稳定的 SSH-daemon 方案。

---

## 4. SPOT / 中断 + 恢复  *(原则 #7/#8)*

**没有 AWS 式 spot/抢占层级**带 2 分钟中断警告。两种中断模式在性质上不同，且**都是确定性的，非随机驱逐**：

1. **启动时容量。** 期望的 GPU 类型在启动时可能不可用 — 一个*启动时*
   可用性问题，而非运行时驱逐。在免费 notebook 上这表现为 **"out of capacity" /
   notebook 在队列中等待下一台免费机器**（已验证 DO notebooks/how-to docs
   2026-06）。构建 **retry-launch-until-available** 逻辑，而非 2 分钟宽限刷新处理器；确保访问需使用付费实例类型，可跳过免费队列。
2. **Auto-shutdown 时钟 — 任何长运行的硬上限。** 定时器才是真正的杀手：
   - **Gradient 免费** notebook 硬性停机上限为 **6 小时**（无法提高）。
   - **付费 notebook** 默认 **12 小时** auto-shutdown；范围 **1 小时 – 1 周**。
   - **Core** 机器可配置 **1 小时 – 1 周** auto-shutdown。
   - **陷阱（Core/Linux）：** Core Linux auto-shutdown 是**挂钟时间，而非基于空闲** — "Linux machines
     shut down regardless of whether any users are connected"（仅 Windows 等待空闲）。活动的
     SSH/tmux 会话**不能**让 Linux Core 机器超过定时器继续存活（已验证 DO
     machines/how-to/manage-auto-shutdown 2026-06）。
   - **陷阱（API）：** auto-shutdown **无法通过 API 或 CLI 在现有机器上启用/禁用** —
     "you can only manage the auto-shutdown feature via the Paperspace console"（同来源）。在创建时/控制台中谨慎设置。

   窗口是确定性的，所以提前规划：Notebook 中的 tmux 会话**仍在超时时消亡**
   （§6）。**恢复钩子：** 在 auto-shutdown 窗口*之前*将完整状态检查点到 `/storage`（Notebooks）或块磁盘（Core），然后重启时无条件加载最新状态。因为时钟是预先可知的，间隔可以被规划而非猜测 — 但 load-latest-on-startup 脊柱（原则 #8）才是使重启幂等的关键。Young/Daly 间隔公式 → `references/spot-resilience.md`。

---

## 5. 拆除 / 计费  *(原则 #9 + 铁律 — 最容易出错的章节)*

按小时计费（已验证 DO products/paperspace/pricing 2026-06）。**shut-down/power-off 停止计算（GPU）计费**同时磁盘保留 — 这是类似 AutoDL 的部分。**但它不会停止所有计费。**

- **stop 后仍计费的项目（陷阱）：** "When a Paperspace machine is powered off, attached **storage**,
  **public IP addresses**, and other **add-ons** continue to be billed on an hourly basis until you destroy
  those resources." 超出计划额度的 Gradient `/storage` 和 Core 块存储在机器关机时均继续计费。
- **月度上限缓冲（新事实）：** 非 GPU 资源（存储、公网 IP、快照）有**月度最大费用** — "once a non-GPU resource reaches its monthly maximum, it no longer incurs
  charges for the rest of the billing cycle." 静态公网 IP 上限为 **$3.00/月**（$0.0045/小时）。所以一个被遗忘的静态 IP 是有限的 ~$3/月泄漏，但一个被遗忘的 2 TB 块卷是 **~$120/月**直到销毁（已验证 DO pricing 2026-06）。
- **什么真正停止全部计费：** **销毁机器** + **释放静态 IP** + **删除存储**（+ 删除任何**快照**）— 独立操作。"To stop all charges for a
  machine and its add-ons, destroy the machine and any resources you no longer need." 一台停止但未销毁的带静态 IP、2 TB 块卷和残留快照的机器仍在花钱。
- **不可逆：** **destroy/delete** 机器会移除其块存储（不可恢复）；块存储**扩容**也是单向的。**shut-down 可逆**（稍后恢复）。

**与其他 profile 的净对比：** Paperspace 提供了真正的廉价空闲 *stop*（不像 Lambda 没有 stop），但与 AutoDL 的关机不同，**存储 + IP + 快照继续计费**直到每个被显式销毁/释放。"Stopped" ≠ "free."

> **铁律（拆除门控）：** 在检查点**已 pull 到本地并通过加载验证**，且用户已**明确批准**具体影响成本的操作之前，不得 destroy/delete 机器、释放 IP 或删除 `/storage`/块存储/快照。destroy 是不可逆的 — "日志里看起来完成了"不是证据（原则 #3）。通用形式 →
> `superpowers:verification-before-completion`。

---

## 6. 守护工具

- **Core 机器** — 完整 VM ⇒ `tmux`/`screen`/`nohup` 均可用；SSH 与任何云 VM 一样稳定。
  这是与 AutoDL tmux 弹性模式最接近的类比。tmux 在 SSH 断开后存活；它**不在**机器
  **stop/restart** 后存活（进程消失），且 — 在 Core/Linux 上至关重要 — 活跃的 tmux
  会话**不能**推迟挂钟 auto-shutdown（§4），所以持久性仍依赖于
  checkpoint-to-disk + load-latest（原则 #8），而非分离原语。
- **Gradient Notebooks** — 托管 Jupyter 沙箱：**没有干净的持久 SSH-daemon 方案**，且
  **auto-shutdown 定时器是硬上限** — 在 Notebook 内启动的 tmux 会话**仍在超时时消亡**。Notebook 不是为无人值守多日守护进程设计的。
- **平台原生长作业机制** — **Workflows**（DAG 自动化）和 **Deployments**（始终在线服务）。对于训练即守护进程，优先选择 **Core + tmux**；将 Notebook 视为仅交互/短运行。

如果最小镜像上缺少 `tmux`，回退到 `nohup <cmd> </dev/null >log 2>&1 &`。

---

## 7. 主要陷阱  (平台专属；通用陷阱 → `references/gotchas_universal.md`)

- **PS1 — "停止了机器，仍在被计费。"**
  症状：GPU 计费停止但机器关机时账单持续攀升。
  根因：shut-down 仅停止**计算**计费；挂载的**存储** + **公网 IP** + 附加组件 +
  快照按小时计费直到销毁/释放（已验证 DO pricing 2026-06）。
  修复：要真正停止计费，**销毁机器、释放静态 IP、删除存储和任何快照** — 独立拆除操作。每次 stop 后审计孤立存储/IP/快照。

- **PS2 — 长运行在整点挂钟时间消亡，无报错。**
  症状：训练在恰好 6 小时 / 12 小时（或配置的 Core 窗口）消失；无 traceback。
  根因：**auto-shutdown 时钟**，而非崩溃 — 免费 notebook 6 小时（硬上限），付费 notebook 12 小时
  默认，Core 1 小时–1 周。在 Core/Linux 上时钟是**挂钟时间，非空闲** — 活跃的 SSH/tmux 会话不会延长它（已验证 DO manage-auto-shutdown 2026-06）。
  修复：在窗口**之前**将检查点写入 `/storage`（Notebooks）或块磁盘（Core）；Core 上在**控制台中将** auto-shutdown 提高到所需最长时长（API/CLI 无法在创建后修改）；
  重启 + load-latest 恢复。

- **PS3 — `pip install`（或任何非 `/storage` 写入）在 Notebook 重启后消失。**
  症状：会话中安装的包下次会话不见了；"保存"的文件 stop/restart 后消失。
  根因：`pip` 写入 `/usr/local/lib`，属于**临时工作区** — 只有 `/storage` 和
  `/notebooks` 持久（已验证 fast.ai forum + DO storage-architecture 2026-06）。"Machines are snapshots,
  not servers," 所以会话内安装不会持久。
  修复：安装到持久目录 — `pip install --user`（落在主目录下持久树中）
  或 `pip install --target /storage/pyenv && export PYTHONPATH=/storage/pyenv`；所有
  检查点/日志/输出写入 `/storage`；stop 前验证它们已落地（`ls`/checksum）。

- **PS4 — 自动化 404 / 静默无操作 / 安装了错误的 SDK。**
  症状：`gradient` 时代的 create/stop 调用失败或无效果；或 `pip install gradient`（v3+）导入了一个没有 notebook/machine 命令的推理 SDK。
  根因：**旧版 Gradient REST 端点已于 2024 年 7 月 15 日弃用**；**`gradient-cli` v2 已弃用**；
  **`gradient-python` v3 是 DigitalOcean Gradient AI 推理 SDK — 名称冲突**，不是编排 CLI（已验证 github.com/Paperspace/gradient-cli + digitalocean/gradient-python 2026-06）。
  修复：新工作使用 **`pspace` CLI**（github.com/Paperspace/cli）；保持旧脚本存活则锁定
  `pip install "gradient<3.0"`。在任何自动化中锁定并验证 CLI 二进制 + 版本。

- **PS5 — 自定义模板 / 存储 / 卷在不同数据中心"找不到"。**
  症状：保存的模板或块卷在其他地方启动时不可用；块存储扩容无法撤销。
  根因：存储和模板**区域/DC 锁定**，且**块存储扩容不可逆**（单向文件系统增长）。
  修复：谨慎选择数据中心，保持存储+计算+模板同地；提前预留空间规划块存储（无法缩小）。

- **PS6 — SSH 别名在每次重启后失效。**
  症状：保存的 `ssh` 主机在机器重启后无法连接。
  根因：**动态公网 IP** 在关机时释放，启动时重新分配（每次新 IP）。
  修复：挂载**静态 IP** 获得稳定 SSH/端点寻址（直到删除前计费，上限 $3/月 —
  `PS1`），或在脚本编写前每次启动重新解析地址。注意：API/CLI 可以管理*静态* IP
  但不能为现有机器添加*动态* IP（在创建时请求动态 IP）。

- **PS7 — 免费层级 notebook 代码默认公开。**
  症状：专有/机密代码在 Gradient 免费 notebook 中全球可读。
  根因：免费 Gradient notebook **默认公开；私有 notebook 需要付费计划**
  （已验证 Paperspace blog / pricing 2026-06）。
  修复：永远不要在免费 notebook 中放置机密代码或任何密钥；升级到付费计划获取私有
  notebook。将免费层级视为公共草稿本。（密钥卫生 → `references/gotchas_universal.md`。）

- **PS8 — 免费 notebook 无法启动 / 停在"pending"。**
  症状：免费 GPU notebook 一直 pending 或报"out of capacity"；只有一个 notebook 能运行。
  根因：免费层级 = **1 个并发运行 notebook、≤5 个项目、5 GB `/storage`**，免费机器
  是池化的 — pending 的 notebook 在排队等下一台免费机器（已验证 Paperspace free-instances
  docs + blog 2026-06）。
  修复：预期免费版排队；停止其他免费 notebook（只能运行一个）；确保访问使用付费实例类型跳过免费队列。

- **PS9 — 已销毁的机器通过残留快照继续计费。**
  症状：机器已销毁，但小额月费持续。
  根因：**快照是独立资源，在机器 destroy 后存活**，按
  `$0.29/GB/月` 计费直到删除；自动快照默认为 "Never"/0 但手动启用的策略（默认每日，最多 10 份）会静默累积（已验证 DO pricing + blog/automated-snapshots 2026-06）。
  修复：拆除时也删除快照（控制台或 CLI）；每次机器 destroy 后审计快照列表。受月度上限约束但仍会泄漏。

- **PS10 — Notebook 上传/导入在 5 GB 免费上限失败。**
  症状：上传多 GB 数据集到 `/storage` 对未付费账户失败。
  根因：免费 `/storage` 额度为 **5 GB**；超出部分 **$0.29/GB/月**（付费计划包含更多：
  如 200 GB / 1 TB 层级）（已验证 Paperspace pricing + fast.ai forum 2026-06）。
  修复：流式/分阶段传输数据集而非整体上传，积极清理，或升级计划；
  如果 HF/torch 缓存会超过额度，将它们重定向出 `/storage`。

- **PS11 — ML-in-a-Box CUDA/driver 对当前 PyTorch 和新架构 GPU 太旧。**
  症状：`The NVIDIA driver on your system is too old (found version 110xx). Please update your GPU
  driver`，或新卡上 `no kernel image is available for execution`。
  根因：模板的**宿主 driver/CUDA 栈滞后于较新的 PyTorch wheels**；在租赁机上宿主
  driver 是全局的，租户通常无法升级（已验证 github.com/Paperspace/ml-in-a-box
  issue #13 2026-06）。这是通用 CUDA 三角问题（U28）的平台专属面向。
  修复：安装与机器 CUDA 匹配的 torch 构建（不要在租赁机上强制升级宿主 driver）；
  选择 Ubuntu/driver 与 GPU 匹配的模板（H100/A100 用 22.04）。完整三角 → U28 in
  `references/gotchas_universal.md`。

- **PS12 — Gradient Deployment / 自定义镜像拉取失败或漂移。**
  症状：Deployment 无法拉取 `<user>/img:tag`，或"相同镜像"随时间行为不同。
  根因：移动标签（`:latest`）解析到不同的层集；私有注册表凭据缺失。
  修复：按摘要锁定镜像（`@sha256:`）并将注册表凭据作为 Gradient **secret** 提供，不内联。
  通用形式 → U30 in `references/gotchas_universal.md`。

- **PS13 — 平台专属调试。** 命令 + 检查项（Core 使用标准 Linux 工具；Notebook 专属项是平台增量）：
  - **确认 GPU + driver/torch 匹配：** `nvidia-smi`（driver/CUDA 版本）然后
    `python -c "import torch;print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"` —
    此处不匹配是 `PS11`/U28，不是代码 bug。
  - **查找占用 5 GB / 超额度 `/storage` 的内容（平台推荐命令）：**
    `du -sch .[!.]* * | sort -h`（或在单元格中 `!du -sch …`）；安装 `ncdu` 获取交互式视图
    （已验证 DO notebooks/how-to/manage-storage 2026-06）。检查 `df -h` 和 `df -i`（inodes，U7）。
  - **Notebook 写入是否持久？** `df -h /storage /notebooks` 并确认目标是这两个
    挂载点之一 — 其他一切（含 `/usr/local/lib`）都是临时的（`PS3`）。
  - **运行为什么消失了？** 遵循通用阶梯（U3）：`dmesg | grep -iE 'killed process|out of
    memory'`（OOM？），`uptime`（最近重启 = auto-shutdown 触发，`PS2`），`nvidia-smi`（GPU 空闲 = 已死亡，
    非挂起）。整点 `uptime` 接近窗口且 `dmesg` 干净 ⇒ auto-shutdown，非崩溃。
  - **检测卡住/慢速下载：** 观察目标文件大小增长
    （`watch -n5 'ls -l /storage/<file>'`）；活跃进程但大小不变 = 线路停滞（U12 可恢复
    循环）。此处出站是直连/无代理，所以停滞是路由/对等点问题，非缺失代理钩子。
  - **声明拆除完成前审计孤立计费项：** 在控制台（或 `pspace`）列出
    机器、**公网 IP**、**存储/卷**和**快照** — `PS1`/`PS9` 藏在后两项中。

---

## 8. 脚本覆盖

为 Paperspace 参数化 `scripts/` 模板的值。正斜杠路径；任何主机/IP 的占位符（永远不是真实地址）。Core 和 Gradient 不同 — 均列出。

```sh
# --- Gradient Notebook ---
DATA_DIR=/storage                # 团队共享持久；stop 和 notebook 删除后均存活
DURABLE_DIR=/storage             # 检查点落地此处（不是 /notebooks — 随 notebook 消亡）
SCRATCH=/tmp                     # 临时工作区；stop 后擦除 — 永远不是唯一副本
HF_HOME=/storage/.cache/huggingface     # 将缓存从临时工作区重定向（注意 5 GB 免费上限，PS10）
PROXY_HOOK=                      # 无 — 直连出站（无 network_turbo）
CRED_FILE=""                     # Paperspace 密钥是 Gradient secrets / 环境变量，非文件 — WANDB_API_KEY/HF_TOKEN 通过 secret/env 到达（run_one 的 [ -n "$CRED_FILE" ] 守卫跳过文件读取）；永远不要将密钥写入 /storage（团队共享）
DETACH=                          # 无干净 tmux；Jupyter kernel + 硬性 6h/12h auto-shutdown 上限
# 注意：pip 到 /storage 以持久化 — pip install --target /storage/pyenv && export PYTHONPATH=/storage/pyenv (PS3)

# --- Core 机器（守护化训练的首选）---
DATA_DIR=/path/to/blockstore     # 占位符 — 挂载的块磁盘挂载点
DURABLE_DIR=/path/to/blockstore/ckpts
SCRATCH=/tmp
HF_HOME=/path/to/blockstore/.cache/huggingface
PROXY_HOOK=                      # 无
CRED_FILE=""                     # Paperspace 密钥是 Gradient secrets / 环境变量，非文件 — WANDB_API_KEY/HF_TOKEN 通过 secret/env 到达（run_one 的 [ -n "$CRED_FILE" ] 守卫跳过文件读取）；启动时注入，永远不内联
DETACH=tmux                      # SSH 断开后存活，机器 stop 后不存活，挂钟 auto-shutdown 后也不存活 — 依赖 checkpoint+resume
SSH_HOST=<machine-ip>            # 占位符 — ML-in-a-Box 用户为 `paperspace`；锁定静态 IP 获得稳定别名（PS6）；动态 IP 每次启动变化
```

提醒：密钥仅通过环境变量名或 Gradient secret 引用 — 永远不要内联密钥，永远不要写入团队共享的 `/storage`（通用密钥-离-共享-FS 陷阱 → `references/gotchas_universal.md`）。
