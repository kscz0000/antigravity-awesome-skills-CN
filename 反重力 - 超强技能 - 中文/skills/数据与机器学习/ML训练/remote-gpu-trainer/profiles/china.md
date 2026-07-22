---
platform: china-family       # 矩池云 Matpool · 恒源云 Gpushare · Featurize · 揽睿星舟 LanRui
kind: ssh-rental             # 四个平台均为：SSH + Jupyter + tmux，cgroup 隔离，预构建 conda base
meter_stop_verb: per-platform   # 停止并释放 (Matpool) | 关机→释放 (Gpushare) | 实例归还 (Featurize) | 停止+销毁数据盘 (LanRui)
meter_stop_irreversible: mixed  # 释放实例不可逆；持久卷存活 — 但 LanRui 数据盘在停止时仍计费
detach_primitive: tmux       # 大多数镜像预装；后台 python 在关闭标签页后也存活
spot_available: false        # 仅按需 — 无运行中 spot 回收（见 §4）
spot_grace: n/a              # 非自愿丢失向量是 STOPPED 实例的自动释放，而非抢占
shared_fs: per-platform      # /mnt | /hy-netdisk(+/hy-nas) | work+/cloud | /home/user/netdisk/data — 区域/机器范围，见 §2
inode_cap: undocumented      # 容量上限有文档（5/20/30/10 GB 免费）；inode 上限无文档 — 用 df -i 实测
free_egress: true            # 国内流量免费；跨 GFW 拉取需要镜像（见 references/china-network.md）
china_mirror_needed: true    # 四个平台均在 GFW 之后 — 镜像/代理故事共享，非按平台区分
host_driver_cuda_max: image-dependent
local_nvme: per-platform     # Gpushare /hy-tmp，LanRui /home/user/datadisk，Featurize 本地临时
---

# 中国 GPU 租赁平台族 Profile (Matpool · Gpushare · Featurize · LanRui)

一句话定位：AutoDL 形态的中国租赁平台 — 近似克隆，共享 AutoDL 的 SSH+tmux+预构建基础脊柱，但在**什么在 stop 后存活**、**停止的数据盘是否仍计费**、以及**哪个（如果有的话）学术代理可用**上存在分歧。将 AutoDL（`profiles/autodl.md`）视为参考实现；本 profile 仅记录增量，先在族级别，然后在各平台比较表中。

> **前置告知用户（原则 #10）：** ⚠️ 危险时钟（按平台，§5）— **已停止的实例会被自动释放**（Gpushare 约 10 天，其他平台不同）→ 数据消失；**LanRui 的数据盘在停止时仍计费**；Gpushare 的 **`/hy-tmp` 在 stop 24 小时后被清除**且 `/root` 重置为镜像状态。便利设施 — 内置 **JupyterLab / TensorBoard** 快捷工具（四个平台均有）；**在租用时声明任何自定义端口**（"高级选项"）— 之后无法开放。

**快速跳转：** `grep -in '<keyword>' profiles/china.md`（如 `proxy`、`ephemeral`、`bills`、`inode`、`LanRui`）。

## 目录
1. 启动 · 2. 存储模型（生存矩阵 + `/root` 临时陷阱） · 3. 网络（→ `references/china-network.md`）
· 4. SPOT/中断 · 5. 拆除/计费 · 6. 守护工具 · 7. 主要陷阱（通用 → `references/gotchas_universal.md`）
+ 平台专属调试 · 8. 脚本覆盖 · 9. 各平台比较表

> 通用陷阱（CRLF、cgroup OOM、静默同步、tmux-持有脚本、磁盘预算、密钥-离-共享-FS）
> 在此不复述 — 参见 `references/gotchas_universal.md`。镜像/代理/下载故事也不复述 — 它在所有中国平台间共享，位于 `references/china-network.md`。

---

## 1. 启动

四个平台：web 控制台租赁市场机器 → 选择 GPU 数量 + **预构建镜像**（PyTorch/TF + CUDA）即环境 → 通过 SSH（自动生成密码或推送公钥）+ JupyterLab 连接；VS Code Remote-SSH 在所有平台可用。

**环境契约 — 镜像/基础即环境；不要在租赁机上 `conda create`。** 与 AutoDL 相同的规则，但各平台基础激活有差异（已验证各平台文档 2026-06）：
- **Featurize** — 基础环境已完整配置且直接使用；`pip`/`conda install` 到 base 中在 `work` 工作区上持久。激活并运行。
- **Matpool** — 预装 **`myconda` 环境且启动时自动激活**（解释器在
  `/root/miniconda3/envs/myconda/bin/python`）。直接运行；无需重新启用（已验证 matpool conda docs
  2026-06 — 修正了之前的"自动激活关闭"注释，那仅适用于 Gpushare）。
- **Gpushare** — 预装 miniconda 但 **base 自动激活已关闭**（`登陆终端默认取消了自动进入 base 环境`）。
  重新启用（`conda config --set auto_activate_base true`）或每个会话激活命名环境
  （已验证 gpushare.com/docs/best_practices/conda 2026-06）。
- **LanRui** — 镜像配置（PyTorch 镜像是可购买的镜像选项）；直接使用 base。

不可避免的自定义环境应建在**持久磁盘**上（`--prefix /<persistent-mount>/myenv`），而非小系统盘（§2）— 系统盘环境在 `/root` 为临时时会被擦除。Gpushare 上具体来说，
文档推荐 `conda create -p /hy-netdisk/myenv`（不是 `/hy-tmp` — 那在关机 24 小时后自动清除，GS5）。

→ **验证：** `ssh <alias> 'python -c "import torch;print(torch.cuda.is_available())"'` 对*预构建*解释器返回 `True`，在任何安装之前。

---

## 2. 存储模型  *(生存矩阵 — 原则 #4)*

**族级陷阱，会打破从 AutoDL 移植的习惯：`/root`（系统盘）并非在每个平台上都持久。** AutoDL 跨关机保留 `/root`；这里从"每次重启重置为镜像状态"（Gpushare）到"实例归还时立即擦除"（Featurize）不等。检查点必须写入平台的持久挂载点，不是 `/root`。

每个平台配对一个**小型易重置系统盘**和一个**持久网络/数据盘**：

| 平台 | 系统盘（`/root` 等） | 持久挂载 | 本地快速临时 | 免费额度 |
|---|---|---|---|---|
| Matpool | `/root`（实例本地；快照捕获） | **`/mnt`** 网盘（跨释放存活，可扩展，区域范围） | `/root`（本地） | 5 GB 网盘 |
| Gpushare | `/` 包括 `/root` — **stop/restart 后重置为镜像** | **`/hy-netdisk`**（仅在*标记*的机器上） | **`/hy-tmp`**（本地 SSD；stop 24 小时后自动清除） | 20 GB 系统盘 |
| Featurize | 归还时擦除 | **`work` = `/home/featurize`**（持久）+ **`/cloud`** 同步盘 | 本地（非持久） | **30 GB** 免费云 |
| LanRui | stop 时系统盘丢失 | **数据盘 = `/home/user/datadisk`** + 共享 **`/home/user/netdisk/data`** | 数据盘（块存储，≈ 系统盘速度） | 网盘 10 GB 免费 |

**生存矩阵（族级）：**

| 层级 | STOP 后存活？ | 释放/归还后存活？ | 备注 |
|---|---|---|---|
| 系统盘 / `/root` | 不定（Gpushare：**否，重置为镜像**；Featurize：归还时擦除） | 否 | 永远不是检查点目标 |
| 持久网盘 / 数据盘 | 是 | 是（但 LanRui 数据盘仍**计费** — §5） | 唯一安全的检查点目标 |
| 跨实例共享文件夹 | 是 | 是 | 区域/区域/机器范围；**覆写风险**（见陷阱） |
| Gpushare `/hy-tmp`（本地 SSD） | **否 — 关机 24 小时后自动清除** | 否 | 仅快速临时；stop 前将结果复制到 `/hy-netdisk`（GS5） |

**区域 / 范围锁定**（类似于 AutoDL 的区域范围 FS）：
- **Matpool** — `/mnt` 网盘**区域范围**：不同区域有独立网盘且不互通；在扩展存储前选择区域（已验证 matpool FAQ 2026-06）。
- **Featurize** — `work`/`/cloud` 中的代码持久；据常见使用报告，云同步盘不跨不同区域共享，而*数据集*可复用 — 在扇出前确认 sweep 的所有实例同区域。*（中置信度 — 官方措辞未在 2026-06 重新验证。）*
- **Gpushare** — `/hy-netdisk` 仅存在于标记为支持**内网存储**的机器上；未标记的机器没有共享挂载。独立的 **`/hy-nas`** 共享存储（0.0007 元/GB·h）存在于特定实例上
  （已验证 gpushare.com/docs/data 2026-06）。
- **LanRui** — `/home/user/netdisk/data` 是**每可用区共享文件夹，自动挂载到该区每个工作空间**（`data 文件夹下的任何数据，都可以在该可用区下的所有工作空间中使用`）— 方便，
  但并行消融存在覆写隐患（陷阱 LR2）。网盘不擅长大量小文件*写入*；使用
  数据盘（已验证 docs.lanrui.co storage 2026-06）。

**Inode 上限：** 容量上限有文档（四个平台分别为 5 / 20 / 30 / 10 GB 免费）；**显式 inode 上限四个平台均无文档**。大量小文件的元数据耗尽风险仍适用于任何共享
FS — 在 Phase 0 时在活跃实例上测量 `df -i <persistent-mount>` 而非假定一个数字。将 HF/ModelScope 缓存重定向出小系统盘 → 参见 `references/china-network.md` §2。

为 §5 拆除动词指定检查点挂载点：写入**持久网盘/数据盘**，永远不是 `/root`。
Gpushare 上，也将热数据集暂存到 `/hy-tmp`（本地 SSD）以提升 IO，但在停止前将结果复制回 `/hy-netdisk`
— `/hy-tmp` 是本地的且关机 24 小时后自动擦除（GS5）。

---

## 3. 网络

**整个镜像 / 代理 / 可恢复下载的故事在所有中国平台间共享，位于 `references/china-network.md` — 不要在此重复。** 该参考拥有镜像表
（PyPI/conda/HF）、`HF_ENDPOINT=https://hf-mirror.com`、ModelScope 回退、可恢复下载重试
阶梯、`hf_transfer` 挂起注意事项和 `no_proxy` 陷阱。仅各平台的**出站加速器**
不同，在此记录（已验证各平台文档 2026-06）：

- **Gpushare — 有真正的学术代理**（最接近 AutoDL 的 `/etc/network_turbo`）：
  `export https_proxy=http://turbo.gpushare.com:<PORT> http_proxy=http://turbo.gpushare.com:<PORT>`
  （也有 `turbo2.gpushare.com:<PORT>` 备用主机）。与 AutoDL 的两个关键差异：(a) 它是
  **每次会话 export**，不是自动加载 — 每个新终端/tmux 面板中需重新运行；(b) 它**白名单仅包含 `*.github.com`, `*.github.io`, `*.githubusercontent.com`, `*.githubassets.com`, `*.huggingface.co`,
  `*.pytorch.org`, `*.kaggle.com` 且限制所有其他主机*** — 所以
  `unset http_proxy https_proxy`（或 `unset http_proxy && unset https_proxy`）在加速拉取完成的那一刻执行，否则 `pip`/`apt`/国内镜像会莫名失败（陷阱 GS2）。这正是
  `no_proxy`/路由特定陷阱在原则 #7 中的实例 — 在真实传输使用的同一路由上验证速度测试（已验证 gpushare.com/docs/instance/network_turbo 2026-06）。
- **Matpool** — 无一键出站代理；提供 `/public/script/` 下的源切换脚本
  （`switch_conda_source.sh`、`switch_pip_source.sh`、`switch_apt_source.sh`）。回退到镜像
  （`references/china-network.md`）。
- **Featurize / LanRui** — 无文档化的一键学术代理；仅镜像。

**端口暴露：** JupyterLab/TensorBoard 是内置快捷工具（四个平台均有）。**自定义端口必须在租用时声明**（Matpool 上的"高级选项"，如 HTTP-6006 TensorBoard / HTTP-8888）— 启动后无法开放。端口在重启时可能变化 — 重新读取控制台，不要在别名中硬编码端口。SSH 为标准 OpenSSH（scp/rsync 直接可用；无代理 SSH `scp` 限制）。标准化格式：
`ssh -p <PORT> root@<region>.matpool.com`（Matpool，如 `hz.matpool.com` / `hz-t2.matpool.com`）、
`ssh -p <PORT> root@<host>.gpushare.com`（Gpushare）、
`ssh user@ssh.<region>.lanrui-ai.com -p <PORT> -i ~/.ssh/id_rsa`（LanRui — 公钥必须先上传到控制台）。

---

## 4. SPOT / 中断 + 恢复  *(原则 #7/#8)*

**这些是纯按需平台 — 没有 spot 竞价，也没有文档化的运行中回收。** 不要在这里构建 SIGTERM 宽限抢占处理；激进的抢占重试在这个族上是过度工程化。真正的非自愿丢失向量是：

1. **已停止实例的自动释放。** Gpushare 自动释放（删除，不可恢复）已停止的按量计费实例
   **停止 10 天后**（`实例停止 10 天后，会自动释放` — 已验证
   gpushare.com/docs/instance/manage 2026-06）。欠费时，**第 15 天中午** Gpushare 删除
   个人数据 + `/hy-nas` 共享存储 + 自定义镜像。已停止的机器不是停泊的机器 — 在该窗口前 pull 出所需的一切。
2. **`/hy-tmp` 24 小时自动清除（Gpushare）。** 与实例释放不同：即使在*运行中*的服务器上，
   `/hy-tmp` 数据在**实例关机 24 小时后**被删除，实例迁移时也会擦除
   （GS5）。
3. **GPU 空闲自动关机。** 大多数平台提供可选的"空闲→自动停止"策略以防止浪费；如果启用，它可能停止一个仅仅安静下来的作业（如 epoch 之间无 GPU 利用率时）— 除非有心跳保证，否则长时间单 GPU 作业应关闭此功能。
4. **平台变动（LanRui）。** LanRui 将域名 `lanrui-ai.com` 迁移至 **`lanrui.co`**（旧域名数据在 **2024-11-01** 后不保留）并于 **2025-06-30** 退役其 **T1/T2 区域**，将用户迁移至新"Cova"平台 — **在编写脚本使用任何缓存的 LanRui 路径前，重新验证当前控制台路径/域名**。

**恢复钩子：** checkpoint-to-durable + load-latest-on-startup（原则 #8）仍然是正确的脊柱 — 这里它防护的是被遗忘的停止、10 天自动释放和 `/hy-tmp` 24 小时擦除，而非 spot 杀死。`references/spot-resilience.md` 中的间隔公式在作业足够长以至于跨过强制停止时仍然适用。

---

## 5. 拆除 / 计费  *(原则 #9 + 铁律)*

**停止计费的动词按平台不同 — 在点击任何东西之前从下表中绑定。** 铁律
（SKILL.md Phase 5）保持不变：在检查点**已 pull 到本地并通过加载验证**，且用户已批准影响成本的操作之前，不得释放/归还/销毁。

| 平台 | 停止计费动词 | 保留什么 | 成本陷阱 |
|---|---|---|---|
| Matpool | **停止并释放** (stop+release) | `/mnt` 网盘持久（区域范围） | `.snap` 快照静默消耗 5 GB 网盘（MP1） |
| Gpushare | **关机**停止计算 → **释放**删除 | `/hy-netdisk` 持久；`/hy-tmp` stop 24 小时后清除；`/root` **重置为镜像** | 停止的实例 **10 天后自动释放**（GS4）；欠费第 15 天中午清除 |
| Featurize | **实例归还** (return) | 仅 `work` (`/home/featurize`) + `/cloud` 持久 | 其他一切**在归还时立即擦除**（FZ1） |
| LanRui | **停止**停止计算；**必须*销毁数据盘***才能停止磁盘计费 | 网盘 + 数据盘持久 | **数据盘在工作空间仅 STOPPED 时仍按小时计费**（LR1） |

**最危险的单点分歧：在 LanRui 上，"停止以省钱"是错误的。** 数据盘
（`/home/user/datadisk`，块存储，按 200 G / 500 G 规格购买）从*创建*到*销毁*按小时计费，即使工作空间已停止 — `工作空间停止运行，未销毁的数据盘也将持续计费`（已验证
docs.lanrui.co storage + lanrui.co/pricing 2026-06）。所以一个已停止的 LanRui 工作空间仍有计费在运转。要真正停止所有计费：停止工作空间并销毁数据盘（在铁律 pull+verify 之后）。网盘
（10 GB 免费，超出 0.15 元/GB·月）独立持久。对比：在 Matpool/Gpushare/Featurize 上，
释放/归还/归还结束计算计费，持久卷简单存活（Gpushare /hy-netdisk 和
/hy-nas 按 GB 计费但不因停止而销毁）。

**成本暂停类比（比完全释放便宜，数据保留）：** Gpushare **无卡模式 / 无卡启动**（低核 CPU-only 重启，无 GPU）是 AutoDL 无 GPU 重启的类比 — 以 GPU 费率的一小部分暂停并保持 `/hy-netdisk` 数据，适合环境配置 + 数据集下载（已验证 gpushare 无卡启动公告 2026-06）。LanRui 支持**自动停止定时器**（在工作空间开始时设置停止时间）和按小时计费。

---

## 6. 守护工具

**tmux** 是族内分离原语 — 大多数镜像预装。注意（来自 Matpool 文档，全族适用）：**从本地 SSH 会话运行 tmux，不是从 Jupyter web 终端** — 按键与 tmux 前缀冲突。后台 `nohup python … </dev/null >log 2>&1 &` 也在 Featurize 上关闭标签页/刷新页面后存活（进程不被杀；仅 notebook 单元格状态丢失）— 但 tmux 因命名可重连会话而更受偏好。

tmux 在 **SSH 断开**后存活，但在任何平台上**不在**实例 **stop/restart** 后存活
（Gpushare 上 restart 重置 `/root`，带走 tmux 服务器和任何 `/root` 日志）— 所以持久脊柱是
checkpoint-to-persistent-disk（§2，原则 #8），而非 tmux 会话。LanRui 还支持
**多机多 GPU 分布式训练** — 如使用，参见 `references/multinode.md`。

---

## 7. 主要陷阱  *(平台专属；通用陷阱 → `references/gotchas_universal.md`)*

### 族级（中国特定，不在通用目录中）

**CN1 — `/root` 临时性静默丢失工作。**
症状：写入 `/root` 的代码/检查点在 stop/restart（Gpushare）或实例归还
（Featurize）后消失。→ 根因：系统盘重置为镜像状态 / 归还时擦除 — 不同于 AutoDL 跨关机保留 `/root`。→ 修复：将*一切*写入持久挂载点（§2）；将 `/root` 视为 RAM。在信任真实运行之前，用 `ls <persistent-mount>` 测试 stop 后审计。

**CN2 — GPU 空闲自动停止杀死安静作业。**
症状：长时间作业在运行中间消亡无报错；控制台显示"auto-stopped (idle)"。→ 根因：可选的空闲关机策略在低 GPU 利用率阶段（数据加载、评估、epoch 之间）停止了实例。
→ 修复：长作业禁用空闲自动停止，或发出周期性 GPU 触碰心跳；在 Phase 0 确认策略状态。

### Matpool (matpool.com)

**MP1 — `.snap` 快照静默消耗 5 GB 网盘。**
症状："保存环境" / 快照保存失败或网盘填满但无明显原因。→ 根因：快照作为 `.snap` 文件写入**网盘内**并计入其微小的 5 GB 配额（已验证 matpool snapshot docs 2026-06）。→ 修复：清理旧 `.snap` 文件（删除一个释放配额）；仅保留最新需要的环境快照。

**MP2 — `/mnt` 不在快照范围内，且保存时机器被锁定。**
症状："保存环境"不捕获 `/mnt` 下的代码；保存期间实例不可用。→ 根因：快照捕获**除 `/mnt` 外的一切**（网盘挂载点），且机器在快照写入时不可使用。→ 修复：要*缩小*快照，先将代码/数据移到 `/mnt`（不会被捕获）；要通过快照*保留*代码，将其放在 `/mnt` 之外。触发保存前确保无运行中的进程。

**MP3 — 区域范围网盘在跨区域 sweep 时困住数据。**
症状：另一区域的第二个实例看不到第一个实例写入的文件；扩展存储"失踪"。
→ 根因：`/mnt` 网盘按区域独立且不互通。→ 修复：将 sweep 的所有实例保持在同一区域；扩展前选择区域（已验证 matpool FAQ 2026-06）。

### Gpushare (gpushare.com)

**GS1 — `/root` 在每次关机/重启后重置为镜像状态。** （需要记住名称的 CN1 实例。）
症状：`/root` 下安装的包 / 代码 / 日志在重启后消失。→ 根因：仅 `/hy-tmp` 和 `/hy-netdisk` 持久；`/` 恢复为镜像。→ 修复：环境放在 `/hy-netdisk`，热数据放在 `/hy-tmp`，结果在停止前同步到 `/hy-netdisk`。

**GS2 — turbo 代理未关闭会阻塞非白名单主机。**
症状：执行 `export …turbo.gpushare.com…` 后，`pip install` / `apt` / 国内镜像挂起或 `ProxyError`。
→ 根因：学术代理仅白名单 GitHub/HF/PyTorch/Kaggle 且**限制其他一切**
（已验证 network_turbo docs 2026-06）。→ 修复：加速拉取完成时立即 `unset http_proxy https_proxy`（§3）。与 `references/china-network.md` 中的 `no_proxy` 陷阱形式相同。

**GS3 — `/hy-netdisk` 在未标记的机器上不存在。**
症状：引用 `/hy-netdisk` 的脚本在某些租赁机上失败。→ 根因：共享网盘仅存在于标记为支持内网存储的机器上。→ 修复：Phase 0 时检查 `mount | grep hy-netdisk`；如缺失则通过 `oss cp` 回退到个人云存储（OSS 工具，~300 Mbps，仅压缩归档）。

**GS4 — 停止的实例 10 天后自动释放；欠费第 15 天清除。** 症状：停泊的已停止实例消失，或共享/个人数据在未付款后消失。→ 根因：按量计费自动释放停止 10 天后（`实例停止 10 天后自动释放`）；欠费时，第 15 天中午删除个人数据 +
`/hy-nas` + 自定义镜像（已验证 gpushare docs 2026-06）。→ 修复：及时从停止的机器 pull 出结果；不要将"stopped"视为持久停泊；保持余额为正。

**GS5 — `/hy-tmp` 关机 24 小时后自动清除（迁移时也会）。** *（新增 — 修正了之前"/hy-tmp 持久"的假设。）* 症状：`/hy-tmp` 下的训练数据/临时文件在 stop 后第二天消失，即使实例仍存在。→ 根因：`/hy-tmp` 是每服务器本地临时，关机 24 小时后自动删除，实例迁移时也会擦除（已验证 gpushare.com/docs/data/storage 2026-06）。→ 修复：将 `/hy-tmp` 视为仅 IO 临时；停止前将任何持久内容同步到 `/hy-netdisk`；不要 `conda create -p /hy-tmp/...` 创建持久环境（使用 `/hy-netdisk`）。

### Featurize (featurize.cn)

**FZ1 — `work`/`/cloud` 之外的任何内容在实例归还时立即擦除。** （四个平台中最严格的"什么存活"规则。）症状：`/home/featurize` 或 `/cloud` 之外的结果在归还后消失。
→ 根因：仅 `work`（每用户云存储，`工作区可以一直保存项目文件`）和 `/cloud` 同步盘持久；其他一切在归还时销毁（已验证 Featurize tutorials 2026-06）。→ 修复：将所有持久输出写入 `work`/`/cloud`；归还前验证。

**FZ2 — `/cloud` 同步盘延迟使编辑*看起来*已保存但实际未落地。** 症状：VS Code 编辑/文件在本地显示已保存但重连或归还后缺失（"工作区中修改代码后无法保存"投诉）。→ 根因：Remote-SSH 到云盘的同步并非总是实时的，特别是在慢速连接或大文件时。
→ 修复：显式 `Ctrl+S`，然后在服务器上验证（`ls -la` / `cat` 文件）后才信任它；连接不稳定时，关闭并重新打开 Remote-SSH 会话（瞬时故障是预期的）。

**FZ3 — 30 GB 免费云配额静默阻断大写入 / `conda create`。** *（修正了之前的"~20 GB"数字。）* 症状：env 创建或大量复制到 `work`/`/cloud` 失败或截断。→ 根因：免费云存储为 **30 GB**（已验证 featurize.cn 2026-06）；超出后写入失败。→ 修复：`du -sh ~/work /cloud` 观察剩余空间；仅保留活跃环境；大型可复现临时数据属于本地非持久磁盘，而非云盘。

### LanRui (lanrui.co / lanrui-ai.com)

**LR1 — 数据盘在工作空间仅 *stopped* 时仍持续计费。** （最昂贵的分歧 — 见 §5。）症状：已停止的 LanRui 工作空间仍在产生费用。→ 根因：数据盘
（`/home/user/datadisk`）从创建到*销毁*按小时计费，与工作空间运行状态无关
（`工作空间停止运行，未销毁的数据盘也将持续计费` — 已验证 docs.lanrui.co storage 2026-06）。→ 修复：要停止所有计费，停止工作空间**并**销毁数据盘 — 仅在铁律 pull+verify 之后；网盘保留数据。

**LR2 — 共享 `netdisk/data` 文件夹挂载到同区每个工作空间 → 跨运行覆写。** 症状：并行消融覆写了另一个运行的输出。→ 根因：`/home/user/netdisk/data` 自动挂载且在*同一*可用区的所有工作空间间共享。→ 修复：每作业隔离写入路径
（`references/parallel_ablation.md`）；永远不要在 `netdisk/data` 下共享可变输出目录。此外：网盘不擅长大量小文件*写入* — 将这些路由到数据盘。

**LR3 — 平台/域名变动使缓存路径失效。** 症状：迁移后脚本化路径/域名失败。
→ 根因：域名 `lanrui-ai.com` → `lanrui.co`（旧数据在 2024-11-01 后丢弃）；T1/T2 区域于 2025-06-30 退役 → "Cova" 平台。→ 修复：在编写脚本使用任何缓存的 LanRui 路径前，在会话中重新验证控制台域名 + 路径。

### 平台专属调试

在信任运行之前，Phase 0 时执行（按平台）：
- **确认持久路径是真实的，不是 `/root`。** `mount | grep -E 'mnt|hy-netdisk|cloud|datadisk|netdisk'`
  然后 `touch <persistent-mount>/.probe && ls -l <persistent-mount>/.probe`。Gpushare 上还需确认
  `/hy-netdisk` 存在（GS3）— `mount | grep hy-netdisk`（未标记机器上不存在）。
- **GPU + driver 健康检查。** `nvidia-smi`（GPU 可见、显存空闲、driver/CUDA），然后
  `python -c "import torch;print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"`
  对预构建解释器运行。本地与服务器 PyTorch 版本不匹配会在 Featurize 上静默破坏检查点加载 — 匹配版本。
- **检测卡住 / 限速下载。** `du -sh <cache-dir>` 两次间隔约 30 秒 — 大小不变 = 停滞（通常是 GFW 或 Gpushare turbo 代理限制非白名单主机，GS2）。交叉检查
  `curl -sI -x "$https_proxy" https://hf-mirror.com` / `env | grep -i proxy`；`unset http_proxy https_proxy`
  并在镜像上重试。
- **磁盘 / inode 压力（§2 的静默风险）。** `df -h <persistent-mount>` 和 `df -i <persistent-mount>` —
  满的 inode 表导致写入失败而 `df -h` 仍显示空闲 GB。Matpool 上，填满的 5 GB 网盘
  通常是陈旧 `.snap` 文件（`ls -la /mnt/*.snap`，MP1）。
- **验证停止计费确实达到预期。** "stop" 后，重新检查控制台计费行 — LanRui 上
  停止但**未**销毁数据盘的工作空间仍在计费（LR1）；Gpushare 上停止的机器
  仍计入 10 天自动释放倒计时（GS4）。
- **读取运行中作业的日志，不要从静默推断。** 作业在 tmux/nohup 中 → `tmux capture-pane -pt
  <session>` 或 `tail -f <persistent-mount>/run.log`。"restart" 后消失的 tmux 服务器意味着 `/root`
  重置（GS1）— 日志必须位于持久挂载点上才能存活。

---

## 8. 脚本覆盖

按平台参数化 `scripts/` 模板。`PROXY_HOOK`、`HF_HOME` 和镜像环境变量均参照
`references/china-network.md`；仅**挂载点**真正不同。

| 变量 | Matpool | Gpushare | Featurize | LanRui |
|---|---|---|---|---|
| `DURABLE_DIR=` (持久) | `/mnt` | `/hy-netdisk` | `/home/featurize` (+`/cloud`) | `/home/user/datadisk` (或 `/home/user/netdisk/data`) |
| `DATA_DIR=` (快速/临时) | `/root` | `/hy-tmp` (stop 24 小时后擦除) | 本地 tmp | `/home/user/datadisk` 临时 |
| `SCRATCH=` (本地，修剪) | `/root` | `/hy-tmp` | 本地 tmp | 数据盘临时 |
| `HF_HOME=` | `/mnt/.cache/hf` | `/hy-netdisk/.cache/hf` | `/cloud/.cache/hf` | `/home/user/datadisk/.cache/hf` |
| `PROXY_HOOK=` | (仅镜像) | `export …turbo.gpushare.com:<PORT>…` 然后 `unset` | (仅镜像) | (仅镜像) |
| `CRED_FILE=""` (无文件 — 环境变量) | `$WANDB_API_KEY` / `$HF_TOKEN` 在**临时**磁盘上，从不在共享网盘上 | 同 | 同 | 同 |
| `DETACH=` | tmux | tmux | tmux | tmux |

`CRED_FILE=""` 因为在这些中国平台上凭据是**环境变量**（或 `.netrc`）在临时
磁盘上，而非网盘上的文件 — 留空使 run_one 的 `[ -n "$CRED_FILE" ]` 守卫跳过文件读取，`$WANDB_API_KEY` / `$HF_TOKEN` 从平台环境传递。

所有平台通用：凭据存在于**临时系统盘**上的环境变量或 `.netrc` 中，从不在共享/持久网盘上（一个挂载到同区每个工作空间的共享 `data` 文件夹，如 LanRui 的，尤其容易泄漏 — 通用密钥-离-共享-FS 陷阱见 `references/gotchas_universal.md`）。

---

## 9. 各平台比较 — 承载差异一览

schema 提出的六个问题，按平台回答。这是选择适用哪个增量时首先阅读的表格。

| 问题 | Matpool | Gpushare | Featurize | LanRui |
|---|---|---|---|---|
| 预构建 base-conda env？ | 是（**`myconda`，自动激活**） | 是（miniconda，base 自动激活**关闭**） | 是（完整 PyTorch/TF base，pip 在 `work` 上持久） | 是（镜像配置；PyTorch 镜像可购买） |
| 学术加速代理？ | 无（仅源切换脚本） | **有** `turbo.gpushare.com:<PORT>`（每次会话，7 主机白名单） | 无（仅镜像） | 无（仅镜像） |
| 共享 / 区域 FS？ | `/mnt` 网盘（**区域范围**，可扩展） | `/hy-netdisk`（仅*标记*机器）+ `/hy-nas` | `work`+`/cloud`（云同步；不跨区域，中置信） | `/home/user/netdisk/data`（挂载到*每同区*工作空间） |
| Inode 上限？ | 无文档 — 测量 `df -i` | 无文档 — 测量 `df -i` | 无文档 — 测量 `df -i` | 无文档 — 测量 `df -i` |
| 数据盘在**停止**时仍计费？ | 否（释放结束计费） | 否（但停止的机器 10 天后自动释放；`/hy-tmp` 24 小时后清除） | 否（归还结束计费） | **是 — 数据盘计费直到销毁** |
| 停止计费动词 | 停止并释放 | 关机 → 释放 (+ 无卡模式暂停) | 实例归还 | **停止 + 销毁数据盘** |
| `/root` stop 后存活？ | 本地，释放时丢失 | **否 — 重置为镜像** | **否 — 归还时擦除** | 系统盘丢失；使用数据盘 |

**移植 AutoDL 工作流的底线：** SSH/tmux/冒烟测试/检查点脊柱原样迁移；按平台重新绑定的三件事是 (1) **持久挂载点**（永远不是 `/root`；Gpushare 上永远不是 `/hy-tmp`），(2) **停止计费动词** — 在 LanRui 上，停止还不够，数据盘必须销毁 — 以及 (3) **代理钩子**（仅 Gpushare 有真正的代理，带严格白名单；其他平台仅镜像 → `references/china-network.md`）。
