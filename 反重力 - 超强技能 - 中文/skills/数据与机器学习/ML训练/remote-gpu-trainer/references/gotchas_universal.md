# 通用与混合陷阱目录 — 适用于所有计费的远程 GPU 租赁

跨平台陷阱：它们在**任何**计费、隔离、租赁的 GPU 上都会咬人 — 只有具体路径/代理/计费动词不同（那些在 `profiles/<platform>.md` 中）。每条为
**症状 → 根因 → 修复**。"混合"条目的症状是通用的，但修复中带有*平台特定值* — 规则留在这里，值在 profile 中。仅限平台的陷阱（AutoDL 的 TB-pin、wandb-key 分类器、network_turbo 代理字面量）不在本文件 — 参见各 profile 的 TOP GOTCHAS 章节。

跳转：`grep -in '<keyword>' references/gotchas_universal.md`（如 `inode`、`egress`、`xid`、`crlf`、`stdin`、`zombie`）。编号 `U1…` 是稳定的；跨平台新增延续同一序列。

## 目录（按主题）

- **进程与 SSH** — U1 SSH-在-kill-时断开 · U2 tmux-持有-脚本-在-内存 · U3 消失进程-4原因 · U4 kill-在-重启动前断开SSH · U5 钩子安全启动
- **磁盘与存储** — U6 磁盘满崩溃torch.save · U7 存储在inode上失败 · U8 暂存热数据到NVMe
- **内存与 OOM** — U9 cgroup-OOM-num_workers×tensor · U10 VRAM-OOM-与-cgroup-OOM · U11 僵尸持有VRAM-nvidia-smi-无法看到 · U41 宿主指标撒谎/oom_kill计数器
- **传输与下载** — U12 scp-重置→可恢复循环 · U13 scp-到-未创建-目录 · U14 出站附加费+同可用区 · U15 传输前压缩
- **监控** — U16 过时等待器/僵尸监视器 · U17 未引用管道grep挂起+健壮轮询 · U18 两段式远程自完成 · U19 tracker删除延迟 · U20 托管tracker在拆除后存活 · U39 实时面板/TB静默为空（路径/端口/进程不匹配） · U43 块缓冲stdout看起来冻结
- **GPU 健康** — U21 nvidia-smi-util%-撒谎 · U22 Xid-48/79-死亡GPU-重新租赁 · U23 热/功耗节流偷走25-40%
- **数据加载器与 IO** — U24 数据加载器饥饿旋钮 · U25 多小文件→分片为tar · U40 intra-op线程过载饿死GPU
- **环境与容器** — U26 CRLF破坏sh · U27 overlay配置文件 · U28 CUDA-toolkit-与-driver-与-torch · U29 从lockfile安装 · U30 按sha256固定镜像 · U31 容器运行但无GPU · U42 机器代码漂移/验证部署
- **成本与拆除** — U32 任务epoch默认值 · U33 静默检查同步
- **密钥与 tracker** — U34 通过stdin传递密钥 · U35 tracker无key离线
- **委托（仅交叉引用）** — U36 cuDNN非确定性 · U37 matplotlib-2^16 · U38 GPU-0%-利用率-数据受限
- **指针** — spot/抢占 → `references/spot-resilience.md`；多节点/NCCL → `references/multinode.md`

---

## 进程与 SSH

### U1 — SSH 在 `pkill -9` 时断开（exit 255, "Connection reset"）

**症状**：`ssh <host> 'pkill -9 -f train'` 返回 `Connection reset by peer`，exit 255。

**根因**：杀死 python 树会拆毁 PTY 链；SSH 客户端收到 EOF 并退出。远程命令可能已经正常执行。

**修复**：这是**正常现象，不是错误** — 重新 SSH 并验证状态，不要恐慌重试。
```bash
ssh <host> "tmux kill-session -t qN 2>/dev/null; sleep 3; pkill -9 -f 'src.train'"  # SSH 在此处 exit 255
ssh <host> "pgrep -af 'src.train' | head -1 || echo CLEAN"                            # 单独调用验证
```

### U2 — tmux 将脚本保持在内存中；运行中编辑会重新执行代码块

**症状**：队列/启动脚本在运行中被更新，但运行中的作业仍使用旧逻辑；或者一个消融干净完成却**从 epoch 1 重启**，出现第二个 tracker run 且队列永不前进。

**根因**：bash 按字节偏移量**按需**读取脚本。tmux 保持已启动脚本的加载状态；运行中 `scp` 新版本使 bash 寻址到其保存的偏移量，但此时是*另一个*文件，落在命令中间，重新执行代码块（重复运行、停滞队列）。子调用（`bash run_one.sh`）对*下一*项确实会重新读取 — 但仅在没有停在脚本中间时。（原则 #6。）

**修复**：**永远不要覆盖任何进程正在执行的脚本** — 先检查 `pgrep -af <script>`；对热更改版本化文件名（`run_one_v2.sh`），仅将*新*启动指向它。向队列文件追加行是安全的（`while read < file` 看到追加的字节）；更改结构则不安全。热替换：杀死 + 重启分离会话让新 bash 从头读取。恢复：杀死会话，将完成的 `best.pth` 复制到持久存储，重启 `run_queue.sh queue.txt <start_index>` 跳过已完成项，删除任何重复的 tracker run（交叉引用 verifying-dl-experiments **必需**）。

**相关分离陷阱 — 未导出的变量不会进入分离原语。** 在 `tmux new-session` / `nohup` 之前设置的 `VAR=x` **不**在分离作业的环境中，除非**导出**（或在启动命令中内联）— 作业看到它为空，插值它的启动器/监视器静默误导（将输出写到错误路径、误报"已死亡"）。启动前 `export VAR`，或内联：`tmux new-session -d "VAR=$VAR bash run.sh"`。

### U3 — 远程进程消失 ≠ OOM：列举 4 种原因

**症状**：分离运行的日志在 `Starting training` 之后停止，无 epoch 输出也无 traceback；`pgrep` 显示进程消失。第一反应是"OOM-killed"。

**根因是以下四种之一** — OOM 只是其中之一：
1. **机器重启 / reboot** — `dmesg` *干净*，GPU 空闲，cgroup 宽裕，`uptime` 很低。最常被遗漏：日志中没有任何提示。
2. **OOM-kill (`-9`)** — `dmesg | grep -i 'killed process'` 显示，内存紧张（U9）。
3. **SSH HUP** — 前台（非 `nohup`/`tmux`/`setsid`）启动在其父 SSH 断开时死亡。
4. **手动 kill** — 之前的 `pkill` 匹配了超出预期的范围。

**修复 — 先低成本诊断，确认后再"修复"**：
```bash
dmesg 2>/dev/null | grep -iE 'killed process|out of memory' | tail   # OOM？空 = 不是 OOM
nvidia-smi --query-gpu=memory.used,memory.free --format=csv,noheader  # 现在空闲 = 已死亡，非挂起
cat /sys/fs/cgroup/memory.max | numfmt --to=iec                       # 宽裕 = OOM 不太可能
uptime                                                                # 低 = 近期重启（原因1）
```
干净的 `dmesg` + 空闲 GPU + 宽裕 cgroup + 低 `uptime` ⇒ **重启，不是 OOM**。不要通过缩小 batch size 来"修复"幻觉 OOM — 那会掩盖被测试的唯一变量。**独立陷阱**：轮询连接断开 ≠ 训练死亡 — 在断定运行已死之前，重新 SSH 并直接检查进程/产物（`pgrep -af train`，日志尾部，`best.pth` mtime）（原则 #3）。

### U4 — `kill` 在同一命令中的重启动执行之前断开 SSH

**症状**：`ssh <host> 'pkill -f X; relaunch X'` 杀死了 X 但 X **没有**重新启动；ssh 返回 255。

**根因**：杀死会话绑定的进程在 kill 时断开 SSH（U1，正常），所以该命令中之后的所有内容都不执行。

**修复**：拆分 — 一个 ssh 调用中 kill，下一个（无 kill）中重启动。为防止 kill/poll 模式匹配到匹配器自身的命令行，拆分字面量：`A=base; B=lines.; pgrep -f "${A}${B}"`（连续字符串 `baselines.` 永远不会出现在运行 `pgrep` 的 cmdline 中）。

### U5 — 钩子安全远程启动：在启动命令中保持环境激活可见

**症状**：环境守卫钩子（如"不在 conda base 中做 DL"）在 `ssh <host> 'nohup bash /root/job.sh ...'` 上阻止或询问，即使 `job.sh` 内部激活了正确的环境；它也在内联 `python -m <pkg>.train` 的 heredoc 上误触。

**根因**：钩子扫描**命令字符串** — 它无法看到 scp 脚本内部，裸 `bash job.sh` 启动没有可见的 `conda activate <env>`，所以守卫假设是 base。

**修复**：通过 Write/`scp` 编写重脚本（这样 `python -m ...train` 在文件中，不在命令中），并在启动 ssh 命令中放置可见的激活：
`ssh <host> 'source /path/to/conda.sh; conda activate <env>; nohup bash /root/job.sh ...'` — 脚本重新激活是无害的。永远不要 `--no-verify` / 永远不要绕过守卫。（在 base 就是环境的单租户租赁机上，正确的做法是豁免远程/临时 base，而非克隆它 — 这是 profile 事实。）

---

## 磁盘与存储

### U6 — 磁盘满导致 `torch.save` 崩溃并出现 `iostream error`

**症状**：训练中 exit=1；日志显示 `RuntimeError: basic_ios::clear: iostream error` 和 `torch.serialization` 内部的 `unexpected pos N vs M`；检查点目录中残留 `latest.pth.tmp`；`df` 显示数据挂载点 100%。

**根因**：`torch.save` 原子写入（写 `.tmp` → 重命名）；`.tmp` 写入遇到磁盘满并出错。任何有配额/cgroup 磁盘的租赁机都会发生这种情况。

**修复 — 预防**：预先预算 `ckpt_size × N_runs + 最坏情况latest + tracker本地缓存`；如果超过挂载点，安排运行中聚合到持久存储 + 删除已完成并聚合的目录；在 `run_one.sh` 中，成功时修剪滚动 `latest.pth` 只保留 `best.pth`（交叉引用 verifying-dl-experiments **必需**，用于可保留检查点策略）。**恢复**：删除 `*.tmp`/`latest.pth` 释放几 GB — `best.pth` 存活，队列可以恢复。

### U7 — 存储在你未监控的维度（和位置）上失败

**症状**：`cp`/`mkdir` 失败 `No space left on device`，但 `df -h` 显示约 34% 使用 — 因为 `df -i` 读到 `100%`（inode 耗尽）。或者数据挂载点填满，尽管 `runs/` 看起来很小。

**根因**：磁盘在 **inode 先于字节**死亡 — 经典触发因素是**每样本 eval 输出**，写入数量级为 `files_per_sample × N_samples × N_conditions` 的小文件。真正的字节占用者常常隐藏在没人看的地方：一个**符号链接缓存**（`~/.cache/huggingface` 映射到数据盘上）可能超过运行创建的一切。

**修复**：在 Phase 0 和每次空间检查时监控 `df -i`，不只是 `df -h`。**用 `du` 审计实际挂载点，而非假设**（`du -sh ~/.cache/huggingface/hub/models--* | sort -rh`）。按**价值**清理 — 保留微小不可替代的证据（metric/eval JSON），丢弃大量可复现的临时数据（周期性检查点、未使用的缓存）。限制每样本 eval 可视化（交叉引用 verifying-dl-experiments **必需**，用于大小策略）。*inode 上限数字*是 profile 事实（一些平台强制约 200K 硬上限；GB 配额平台无文档上限）；多小文件的通用形式是**分片为 tar**（U25）。在 `rm -rf` 目标时获取用户明确确认；提供"清理 vs 扩展磁盘"选项（原则 #9）。

### U8 — 训练前将热数据暂存到本地 NVMe

**症状**：训练 I/O 受限，从网络/共享/HDD 支持的卷读取；GPU 在 batch 间饥饿。

**根因**：远程/网络文件系统（或旋转数据盘）的随机读取吞吐量远低于实例本地 NVMe — HDD-vs-NVMe 差距可达约 35 倍。

**修复**：作业开始时，将工作数据集从持久/共享层复制到实例本地 NVMe 暂存区，针对本地副本训练，将检查点写回持久存储。本地 NVMe 路径是 profile 事实（frontmatter 中的 `local_nvme`）；暂存后训练的纪律是通用的。与 U24/U25 配对。

---

## 内存与 OOM

### U9 — `num_workers` × 大内存 tensor → cgroup OOM-kill（裸 "Killed"，exit 137）

**症状**：训练早期死亡，显示裸 `Killed` / `killed by signal: Killed (-9)` 且**无 Python traceback**；降低 `num_workers` 使其消失。

**根因**：每个 DataLoader worker 是一个 `fork`，获取 dataset 持有的任何大对象的**自身副本**（16384² float32 矩阵 ≈ 1 GB）。`num_workers=W` ⇒ 约 `(W+1)×` 该占用，这超出了实例的 cgroup `memory.max`，即使单进程运行能够放下。内核 OOM-kill 没有 Python 级别错误，所以看起来像神秘崩溃。

**修复**：根据 `memory.max` 和每 worker 常驻集来调整 `num_workers`，**不是** CPU 核心数。跨 worker 共享一份副本（memmap / 模块级单例构建一次）或即时生成对象。缩小问题也能修复 — 更小的矩阵维度*二次方*缩小占用（dim 1024 ≈ 4 MB，比 16384 小 256 倍）。确认是 OOM：`dmesg | tail` 显示 `Out of memory: Killed process`，且相同配置在 `num_workers=0` 下存活。

### U10 — VRAM OOM（大模型或并发作业）不同于 cgroup-RAM OOM (U9)

**症状**：启动第二个 train/eval 时 `torch.OutOfMemoryError: CUDA out of memory`（同时有另一个运行），或大模型（深度 transformer / 高分辨率展开网络）单独 OOM。

**根因**：**VRAM** — 并发作业的分配总和加碎片超过显卡。不是宿主 RAM (U9)。

**修复**：先检查空闲 VRAM（`nvidia-smi --query-gpu=memory.free --format=csv,noheader`）；将 batch 调整为*与*任何并发作业*共存*；设置 `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` 减少碎片。（在租赁机上运行重量级 DL；本地做静态/shape 检查 — 交叉引用 verifying-dl-experiments **必需**，用于本地 OOM 原因。）

### U11 — 僵尸持有 VRAM，`nvidia-smi` 无法看到 → "空" GPU 上 OOM

**症状**：`nvidia-smi` 列出无进程且显示空闲内存，但新作业立即 OOM；常见于崩溃的 DDP 运行或被杀死的容器之后。

**根因**：一个失效/孤立进程（或死亡容器的命名空间）仍持有 CUDA 上下文和 VRAM，但 `nvidia-smi` 的进程表无法归属 — 所以 GPU *看起来*空闲而内存被锁定。

**修复**：通过设备节点枚举真正的持有者并收割：
```bash
fuser -v /dev/nvidia* 2>/dev/null   # 或：lsof /dev/nvidia*  → kill -9 列出的 PIDs
```
如果是容器化，重启容器。附带一个小型收割器，标记任何持有持久 VRAM + 约 0% 利用率超过超时的 PID — 交叉引用 `scripts/reap_vram_zombies.sh`。

### U41 — 共享机器上，`uptime`/`free` 描述整个物理宿主，而非你的容器 — 使用 cgroup 作用域读数 + `oom_kill` 计数器

**症状**：分离运行看起来"死了"或"宿主过载" — `uptime` 显示负载平均 400+，`top`/`free -m` 看起来爆满 — 所以你怀疑争用或 OOM-kill。但作业自身的检查点 `mtime` 持续推进，日志仍在增长。

**根因**：在多租户租赁机上，宿主工具（`uptime`、`top`、`free -m`、`vmstat`）报告你**与其他租户共享的物理节点**，而非你的 cgroup。邻居的作业将宿主负载平均推至约 490，而你的容器近乎空闲（你的进程在 `R`/`S`，无卡在不可中断 `D` 的）。将宿主负载读为自己的 → 虚假的"过载 / OOM-killed"判断和不必要的杀死-重启健康运行。

**修复**：从 cgroup 作用域读数判断你的容器，而非宿主工具：
- 内存 — `/sys/fs/cgroup/memory.current` 对比 `memory.max`（不是 `free -m`）；
- 你是否被 OOM-kill — `/sys/fs/cgroup/memory.events` 中的 **`oom_kill` 计数器**
  （`grep oom_kill /sys/fs/cgroup/memory.events`）；非递增的计数器意味着你**没有**被 OOM-kill，无论宿主 `free` 看起来多红；
- CPU 压力 — `/sys/fs/cgroup/cpu.stat` / `cpu.pressure`。

高宿主负载加上你 cgroup 宽裕和 `oom_kill 0` 是**吵闹邻居**，不是你的 bug — 不要缩小你的 batch 或怪罪你的代码（邻居真正在共享显卡上饿死你是 U21/U23 节流领域或重新租赁，不是代码修复）。强化 **U3** 消失进程阶梯：权威的 OOM 检查是 cgroup `oom_kill` 计数器，而非宿主 `dmesg`/`free` 噪声。

---

## 传输与下载

### U12 — `scp -r` 大目录在传输中途重置 → 按目录可恢复循环

**症状**：`scp -r host:...130GB ./` 30–60 分钟后，连接断开
（`Read from remote host ... reset by peer`）；本地有几个目录，其余消失。scp 不支持恢复。

**根因**：单个 SSH 连接承载整个传输；任何网络抖动都会杀死全部。

**修复**：按**目录**循环，每个有自己的 SSH 会话 — 一个失败不会丢失其他，重新运行跳过已完成的目录。优先使用 `rsync -avz --partial --append-verify`（恢复半文件）。在 `timeout … && break` 重试循环中包装批量 pull：停滞≠永久失败，可恢复传输在多次杀死间积累进度。在真实传输使用的**相同路由**上验证任何速度测试（原则 #7）。参见 `scripts/download_loop.sh` 的按目录模式。

### U13 — `scp` 到一个应由兄弟命令创建的远程目录（竞争）

**症状**：后台 `scp big.tar host:/root/x/` 立即失败 `dest open "/root/x/": Failure` — 本应 `mkdir` 创建 `/root/x` 的前台命令运行更晚，或被阻塞/取消。

**根因**：并行/兄弟命令之间的排序假设；目标目录尚不存在。

**修复**：让每次传输在自己的重试循环中自足：
`ssh host 'mkdir -p /root/x' && scp … || retry`。永远不要假设兄弟命令创建了目标。

### U14 — 出站是静默的约 20% 附加费；同区部署并保持在同一可用区

**症状**：月度账单比租赁 GPU 小时超出约 20%；每日从超大规模存储桶重新拉取大模型/数据集主导成本（每日从 S3 拉取 140 GB 模型 ≈ 仅出站 $378/月）。

**根因**：超大规模云**出站**按流量计费（AWS 约 $0.09/GB，GCP 约 $0.08，Azure 约 $0.087），而大多数 GPU 云（Lambda/RunPod/vast/CoreWeave）收费 $0。更糟的是，**跨可用区流量每个方向约 $0.01/GB，即使在同一提供商内** — 存储在不同区域而非计算区域会静默计量每次读取。

**修复**：将存储与计算同地部署在**同一提供商 AND 同一可用区/区域**。将数据集拉取一次到持久本地存储，而非每个 epoch 从远程存储桶拉取。将 `free_egress` / `egress_per_gb` / `cross_az_per_gb` 记录为 profile 字段，对传输密集型作业优先选择 $0 出站的 GPU 云。

### U15 — 传输前压缩

**症状**：检查点/数据集传输缓慢且（在计费出站时）昂贵。

**根因**：原始 tensor 和 JSON 未经压缩穿越网络。

**修复**：传输前用 zstd/gzip 压缩负载 — 削减检查点+数据集 30–60%，JSON 60–80%；在任务容忍时以 fp16/int8 存储权重。与 U14（更少出站费用）和 U12（更少字节需恢复）叠加。与 U25 配对（tar 分片压缩并作为单一流传输）。

---

## 监控

### U16 — 过时后台等待器堆积；取代一个运行 → 停止其等待器；选择正确的生命周期

**症状**："Background tasks" 面板显示 8+ 个 "Running" 等待循环，已耗时 500–740 分钟，每个约每 20 秒 ssh 轮询，而 GPU 空闲，实验数小时前已完成。

**根因**：每次杀死+重启不稳定 saga 都武装了一个新的 `until ssh grep MARKER; do sleep; done` 等待器但从未停止旧的 — 其标记（在已取代的日志中）永远不会出现，所以它永远循环。`run_in_background` 等待器**没有**时间上限（一个 781 秒任务运行完成 + 通知了；约 600 秒上限是**前台** Bash 的）。真正的静默失败模式是从不退出的等待器（U17）。

**修复**：每个活跃运行一个等待器 — 取代运行时，先停止旧等待器（`TaskStop`；跨会话 ID 无法从恢复的会话中停止 — 从 UI 中解除）。多小时等待 → 一个**持久 Monitor**（无 10 分钟上限）+ 一个停滞检测器 emit，这样挂起的运行仍能通知。持久 Monitor 在会话恢复时死亡 → 任何恢复后，直接检查远程事实（`tmux ls`，`grep DONE log`，`nvidia-smi`）；永远不要信任可能已消失的监视器（原则 #3）。

### U17 — 静默后台监视器永不返回：通常是 grep 中未加引号的 `|`

**症状**：一个 `run_in_background` ssh 监视器永不返回 / 永不通知；`pgrep` 显示进程"活跃"。运行看起来挂起了 — 但实际作业已完成并写入了结果。

**根因**：封装器从未退出，因为子命令永远阻塞。经典 bug 是 grep 中**未加引号的 `|`** — `grep -hE noise-sweep|snr=|wrote log` — shell 将其拆分为三个管道命令，第一个（`grep -hE noise-sweep`，无文件名）读取 **stdin** → 永远阻塞 → 管道永不返回 → ssh 永不返回 → 本地后台进程永不退出 → 无完成通知。（后台任务仅在退出时通知 — 无 600 秒上限；前台 Bash 是有上限的那个，U16。）

**修复 — 健壮的远程轮询模板**：
- **给每个正则加引号并给 grep 提供文件名**：`grep -hE 'noise-sweep|snr=|wrote' log`（引号内 `|` 是交替；文件名意味着读文件，不读 stdin）。
- **限制 ssh**：`ssh -o ConnectTimeout=15 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 …` — 抖动在约 30 秒内自杀死，而非半开挂起几分钟。
- **短连接轮询，而非一个长持 ssh**：每次轮询 = ssh 进 → 检查 → 断开；本地用有界计数器循环。
- **按产物验证，而非通知**：当它"看起来完成"时，Read 本地输出 + 一次新鲜的 `ssh 'grep DONE log; tmux ls; nvidia-smi'` 确认事实（交叉引用 verifying-dl-experiments **必需**）；不要等待可能永不触发的通知。

### U18 — "我会定期检查" 是谎言，除非武装了触发器；两段式远程自完成

**症状**：承诺监控多小时远程运行，然后一天没有报告 — 因为在回合之间助手不运行。设置来"ssh 进去看看"的云调度器静默无法连接机器。

**根因**：两件被混淆的事。(a) 让远程自完成（一个等待日志标记然后运行 eval 的等待器）保证结果但不给*报告节奏* — 没有东西按定时器重新调用助手。(b) 云调度在隔离沙箱中运行，有自己的检出且**无法访问本地 SSH 密钥或网络** → 它无法 `ssh` 租赁的机器，且 SSH 私钥**绝不能**进入云智能体（密钥泄漏）。

**修复 — 两段式模式**：
- **远程自完成（保证的，存活于会话/SSH 死亡）**：在一个 `nohup ... </dev/null >log 2>&1 &` 下链式执行 `train → eval → touch marker`。通过**日志标记**检测"完成"（`grep -q 'QUEUE DONE' master.log`），永远不用 `pgrep` — 等待器自身的命令行包含模式，所以 `pgrep -f` 匹配自身并永远循环（U17）。
- **实时进度（尽力而为）**：一个会话绑定的本地循环（如 `/loop 30m` / cron `3,33 * * * *`）用*本地*密钥 ssh 轮询。坦诚它在会话关闭时死亡 — 远程仍完成；用户重新 ping 来拉取。
- **不要承诺你无法兑现的自主跨会话轮询。**（`tmux` 在新机器上通常缺失且 `apt-get install` 离线失败 — `nohup ... </dev/null >log 2>&1 &` 是零依赖的且在 SSH 断开后存活；用 `pgrep -af <script>` 验证。）完整架构 → `references/monitoring_patterns.md`。

### U19 — Tracker run 删除延迟；新导出复活"已删除"的 run

**症状**：`run.delete()` 返回，但立即 `api.runs()` 仍列出每个已删除的 run；几分钟后的批量历史导出愉快地重新下载刚删除 run 的 `<run>__history.csv`。

**根因**：删除在服务端是异步的；list/export 端点在几分钟内提供过时列表。

**修复**：删除 → 在**稍后**的监控轮次重新验证（不是紧凑循环；第二次 `delete(delete_artifacts=True)` 传递是安全的）。顺序重要：在本地导出**之前**做云删除，然后重新检查导出目录是否有复活的文件并移除它们。（交叉引用 verifying-dl-experiments **必需**，用于 tracker 取证。）

### U20 — 本地日志随实例消亡：使用托管 tracker

**症状**：写入临时机器的 TensorBoard 事件文件在拆除后消失 — 计费停止动词运行后所有曲线都没了。

**根因**：租赁机器的本地磁盘在 `terminate`/`destroy` 后不持久（原则 #4）；度量历史仅存在于那里。

**修复**：将度量记录到**托管 tracker** 使其在拆除后存活 — `trackio.init(space_id=...)` 或在线 `wandb`（在防火墙后通过平台代理推送）。轮询 tracker 的结构化告警作为监视器而非脆弱的 ssh-tail。交叉引用 huggingface-skills:huggingface-trackio **必需**，用于 `init/log/finish/alert` 机制和 `space_id` 同步。

### U43 — 分离运行的日志看起来冻结了数分钟但训练正常：stdout 在非 TTY 下是块缓冲的

**症状**：`nohup`/`tmux` 运行打印几行然后数分钟无输出；读起来像"挂起 / 已死"，本能是杀掉它 — 但检查点 `mtime`、TB 标量和 `nvidia-smi` 都显示在推进。

**根因**：Python（和 libc stdio）在 stdout 是 TTY 时**行缓冲，但在管道或文件时块缓冲（约 4–8 KB）** — 正是分离的情况。日志只在缓冲区填满时刷新，所以健康运行看起来静默，`grep`-on-log 存活检查在间隙上误报。

**修复**：无缓冲运行 — `python -u` 或 `PYTHONUNBUFFERED=1`（附带的 `scripts/run_one.sh.template` 已导出）；对 shell 管道使用 `stdbuf -oL`。并按**产物判断存活，不是 stdout 节奏** — 检查点 `mtime`、TB 标量 API、`nvidia-smi`（monitoring_patterns §0 推论；更深层的"它真的挂了吗？"挂接是 py-spy，throughput-profiling **T21**）。冻结日志是最常见的虚假"运行已死"。

---

## GPU 健康

### U21 — `nvidia-smi` GPU-Util % 撒谎

**症状**：性能磁贴读取 100% 利用率但吞吐量差；或利用率看起来"忙碌"而作业实际上饥饿（U38 的逆情况，后者是 0%-但在运行的情况）。

**根因**：`GPU-Util` 意味着"采样窗口内有 ≥1 个内核运行"，不是"有用工作填满了窗口"。微小内核的涓流读为 100%。

**修复**：将利用率与 **SM 时钟**（`clocks.current.sm`）、内存带宽利用率和功耗关联 — `nvidia-smi dmon -s pucvmet -d 1`。"100% 利用率"下低 SM 时钟或低功耗意味着 GPU 营养不足（转至 U24）。始终采样数秒，不要一次快照。

### U22 — Xid 48/79 = 死亡 GPU；在租赁机上，重新租赁

**症状**：训练崩溃或 GPU 掉线；`dmesg | grep -i xid` 显示 Xid 错误。

**根因**：Xid 是 NVIDIA 的规范硬件故障信号。**Xid 48 = 双比特 ECC（GPU 已死）；Xid 79 = "GPU 已从总线脱落"。** 这些是硬件问题，不是代码。

**修复**：在*租赁机*上，显卡无法重新插拔 — **停止实例并重新租赁另一台机器**；不要浪费数小时调试硬件故障的代码。将 `dmesg | grep -i xid` 作为"消失进程"阶梯（U3）的一部分，在 GPU 意外空闲时检查。

### U23 — 热/功耗节流静默偷走 25–40% 且无错误

**症状**："相同代码比昨天慢" — 无错误，无崩溃，只是吞吐量更低。

**根因**：GPU 在温度或功耗节流（H100 在约 83 °C 时节流；目标 <75 °C）。在共享租赁机上，冷却/功耗余量不在租户控制范围内。

**修复**：检测 — SM 时钟低于基频同时温度 >83 °C，或 `nvidia-smi -q -d PERFORMANCE` 显示节流原因。租户无法修复冷却 → **标记并重新租赁**更健康的机器；不要将减速解读为模型/数据退化。与 U21 配对（时钟暴露它而利用率百分比隐藏它）。

---

## 数据加载器与 IO

### U24 — GPU 在 10–70% 等待数据加载器，而非计算

**症状**：利用率远低于 100%（但非零），step 日志推进缓慢；profiling 显示时间花在数据获取，而非前向/反向。

**根因**：输入管道无法喂饱 GPU — 太少 worker、无预取、host↔device 复制在关键路径上。（区别于 U38 的*0%* CPU-数据受限变换情况；这是部分饥饿旋钮设置。）

**修复 — 按顺序调优**：`num_workers = cores − 1`（根据每 worker 占用调整，U9），`persistent_workers=True`，`pin_memory=True`，`prefetch_factor=2`。病理情况仅凭这些就显示 >100 倍差距。如果重量级每样本变换是瓶颈，将其移到 GPU（交叉引用 verifying-dl-experiments **必需**，用于 0%-利用率诊断，U38）。与 U8（暂存到 NVMe）和 U25 配对。

### U25 — 网络/对象存储上数百万小文件 → 事务开销死亡；分片为 tar

**症状**：许多小文件的数据集从共享/对象存储流式读取极慢；或数万个每样本文件的 eval 输出耗尽 inode（U7）或撑爆可视化网格（U37）。

**根因**：每文件 open/stat/close 开销在网络/对象存储上占主导；inode 和元数据成本随文件*数量*而非字节缩放。

**修复**：打包为**分片 tar**（WebDataset），每分片几百 MB → 3–10 倍更快的顺序 I/O 且是从 S3 流式读取的唯一合理模式。这是 inode 耗尽陷阱（U7）和每样本可视化陷阱的**通用形式** — 限制并分片，而非每样本发射一个文件。与 U8（将分片暂存到本地 NVMe）和 U15（分片压缩为单一流传输）配对。

### U40 — vCPU 切片的租赁机饿死自己的 GPU：torch intra-op 线程默认为宿主核心数，而非你的 cgroup 配额

**症状**：GPU `sm%` 约为 5–15% 且运行缓慢，但数据加载器不是瓶颈（少/无 worker，数据已在设备上，U24 旋钮没帮助）；`top` 显示数十个 python 线程争夺少量核心。

**根因**：你租了一个 **cgroup CPU 切片**（如 64 核宿主的 12 vCPU），但 torch/OpenMP 将其 intra-op 线程池设置为**物理**核心数 — `torch.get_num_threads()` / `OMP_NUM_THREADS` 约为 64。约 57 个可运行线程在 12 个核心上争抢，将切片消耗在上下文切换上，所以启动内核和喂给 GPU 的 CPU 侧跟不上，显卡空闲。无 OOM，无错误 — 纯调度器颠簸（*宿主调度*饿死 GPU，数据受限的逆情况）。

**修复**：启动前将线程池上限设为你的**切片**的 vCPU 数 — `export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4`（和/或 `torch.set_num_threads(4)`）；确认 torch 遵守（`python -c "import torch; print(torch.get_num_threads())"` → 4，不是 64）。从 cgroup 读取真实配额，不是 `nproc`（它报告宿主核心）：`cat /sys/fs/cgroup/cpu.max` → `quota period`，vCPU ≈ quota/period。将上限写入启动封装器，使每个队列单元继承。区别于 **U9**（worker × RAM → cgroup OOM）和 **U24**（数据加载器饥饿）；捕获它的分诊是 throughput-profiling **T3**（GPU SM% 低而 python 线程风暴占满核心）。

---

## 环境与容器

### U26 — CRLF 破坏 Linux 上的 `.sh`（在 Windows 上创作）

**症状**：同步的启动器静默不做任何事（空日志）；手动运行报错 `set: -: invalid option`，`cd: /path\r: No such file or directory`，`syntax error near unexpected token $'do\r'` — 每行"以 `\r` 结尾"。

**根因**：Windows `core.autocrlf=true`（或 `git archive` 导出工作树 EOL）以 CRLF 写入 `.sh`；Linux `bash` 将尾随 `\r` 视为每个 token 的一部分。`.py` 不受影响（Python 的通用换行符）；具体破坏的是 `bash`/`.sh`。

**修复**：添加 `.gitattributes` 包含 `*.sh text eol=lf`（这样 `git archive`/checkout 总是发出 LF）；即时在机器上解除：`sed -i 's/\r$//' scripts/*.sh`。

### U27 — `-o dotted.key=value` 覆盖在 null 父节点上爆炸 → 将协议冻结为 overlay 配置文件

**症状**：`-o evaluation.sps_augmentation.enable=true` 崩溃
`KeyError: Override path '...' is not a mapping`，因为基础 YAML 有一个 `null` 父节点。更糟糕的长期影响：仅作为一次性 CLI 字符串存在的协议变体几个月后无法复现。

**根因**：点分键覆盖遍历无法下降通过 `null` 父节点；且仅 CLI 字符串的协议没有可 diff、可审查的记录。

**修复**：将每个协议变体定义为小型 overlay 配置（`configs/eval_overlays/<protocol>.yaml`，用 `_base_:` 指向规范叶节点）并通过 `-c` 传入。可审查、可 diff、免疫 null 父节点遍历。这也是**重试相同配置机制**（原则 #7）：overlay 文件是重试逐字节复用的稳定配置。要重建历史协议，读取产物清单（`*_manifest.json` 逐字记录解析的覆盖）。

### U28 — CUDA-toolkit ↔ 宿主-driver ↔ torch-构建 三角

**症状**：`detected CUDA version mismatches the version used to compile PyTorch`；或在新型架构 GPU 上首次前向时 `no kernel image is available for execution`。

**根因**：三个独立版本化的层必须一致 — **宿主 driver 是宿主全局的，租户通常无法在租赁机上更改；CUDA toolkit 是每环境的且可更改；torch 构建必须匹配两者。** toolkit 必须 ≤ 宿主 driver 支持的版本；一个锁定 `torch<2.9` 的项目可能*降级*了唯一包含新架构显卡内核的构建（如 sm_120）。

**修复**：保持镜像的工作 torch — 从远程安装中过滤掉框架锁定：
```bash
grep -ivE '^(torch|torchvision|torchaudio)' requirements.txt > /root/req_remote.txt
pip install -r /root/req_remote.txt
```
当每环境 toolkit 必须胜出时设置 `LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH`。启动前冒烟测试 `torch.cuda.get_device_capability()` + 一个重量级项目 import；非频带 torch 版本进入运行时快照 — 随结果披露。`host_driver_cuda_max` 是 profile 字段。

### U29 — "相同版本，不同结果"：顶层锁定让传递依赖漂移 → 从 lockfile 安装

**症状**：两次安装"相同" `requirements.txt` 产生不同行为/结果。

**根因**：手编辑的 `requirements.txt` 只锁定顶层包；传递依赖在安装间漂移。

**修复**：从**lock file**（`uv lock` / `pip-tools` / `conda-lock`）安装，它锁定完整解析图，而非手编辑的顶层列表。与 U28 配对（过滤框架锁定，然后锁定其余）。

### U30 — Dockerfile 不可复现：按 `@sha256:` 摘要固定基础镜像

**症状**：从"相同" Dockerfile 间隔数月构建的容器行为不同。

**根因**：`FROM image:latest`（或任何移动标签）随时间解析到不同层集。

**修复**：按内容摘要固定基础镜像 — `FROM image@sha256:<digest>`，不是 `:latest` — 这样构建是位级可复现的。（`pin_image_by_sha256` 是镜像作为环境契约时的每平台期望。）

### U31 — 容器运行但训练慢 100 倍 = GPU 从未挂载（仅 CPU）

**症状**：容器化作业运行完成但异常缓慢；损失曲线看起来正常，只是极慢。

**根因**：容器没有 GPU — 启动时没有 `--gpus all`，或 NVIDIA Container Toolkit 缺失/太旧，所以 CUDA 静默回退到 CPU。

**修复**：`docker run --gpus all …`，NVIDIA Container Toolkit ≥1.14，并在训练前**在容器内部验证 `nvidia-smi`** — 永远不要从干净的 `docker run` 假设 GPU 挂载。

### U42 — 机器运行手动同步的副本，无 git remote；你"提交"的修复可能未部署 — 在信任运行或拆除前验证它确实在机器上

**症状**：你本地修复并提交的 bug 在机器上仍然复现，或 eval 在过时逻辑上运行（错误的默认值、缺失的加速、病理性的缓慢），即使本地 `git log` 显示修复已落地。

**根因**：大多数租赁机**没有 git remote** — 机器持有你通过 `scp`/`rsync`/`tar-over-ssh` 推送的工作树，所以代码只在你重新同步时推进。本地提交不改变机器上的任何东西；中断或错误路径的同步，或单纯忘记，使机器停留在修复前。"我提交了" ≠ "它在机器上运行"。

**修复**：将代码部署视为检查同步（**U33**）— **验证，不要假设**。同步后，在依赖之前 grep 机器上的更改：
```bash
ssh "$HOST" "grep -n '<new symbol / changed line>' /root/<proj>/path/file.py" || echo 'NOT DEPLOYED'
```
或比较哈希（`ssh host 'sha256sum file'` vs 本地）。使其成为任何结果依赖该修复的运行的预检，以及 **Phase-5 拆除门控**的一部分 — 由过时代码产生的判断不是你以为的判断（原则 #3）。与 **U29/U30** 配对（锁定依赖/镜像）：代码和环境都必须是你认为的版本。

---

## 成本与拆除

### U32 — 一个任务的默认 epoch 不同于另一个任务；CLI `--epochs` 静默覆盖了正确的值

**症状**：一个 CLI `--epochs N` 被应用到所有消融；一个子集（如检测 vs 重建/分割）持续表现不佳；审查者标记了它。

**根因**：一些任务族需要更多 epoch 才能收敛，其 YAML 中默认更高值；一个统一的 CLI `--epochs` 静默覆盖了每任务默认值。

**修复**：让队列支持每行 epoch 字段（如 重建/分割 `20`，检测 `50`）；在部署前审计代码库的 YAML 中的 `epochs:` 声明（`grep -rE '^\s*epochs:' configs/ | sort -u`）。这是配置漂移的实例 — 实际上是冒烟/健全性目标（交叉引用 verifying-dl-experiments **必需**）。

### U33 — 静默同步失败：将成功行门控在实际复制结果上

**症状**：封装器为每个作业打印 `auto-synced <name> to durable storage`，但在下载时持久目录缺失或为空。

**根因**：同步块执行 `mkdir -p "$DST"; cp -f ... 2>/dev/null` 然后**无条件** `echo synced` — 它从不检查退出码。当持久 FS inode 耗尽（U7）时 `mkdir` 失败但成功行仍然触发，所以监控看起来绿色而什么都没落地（原则 #3）。

**修复 — 检查、门控同步**：
```bash
if mkdir -p "$DST" && cp -f "$CKPT_DIR/best.pth" "$DST/" && [ -f "$DST/best.pth" ]; then
    echo "[$(date +%H:%M:%S)] auto-synced $NAME to durable storage"
else
    echo "[$(date +%H:%M:%S)] !! SYNC FAILED for $NAME (check df -i) — data disk is still source-of-truth"
fi
```
直到下载在本地验证前，信任**数据磁盘**副本，不是"已同步"日志行。附带的 `scripts/run_one.sh.template` 携带检查版本。

---

## 密钥与 tracker

### U34 — 将凭据移到机器上，不让密钥出现在命令中

**症状**：将密钥粘贴到 ssh/scp 命令中会泄漏到 shell 历史、记录和钩子日志中；安全钩子（正确地）阻止 scp 整个 `~/.netrc`（它携带其他机器的凭据）。

**根因**：命令字符串中的任何密钥都会被历史/记录/钩子日志捕获。

**修复**：通过 **stdin** 精确流式传输一个 machine 块 — 值从文件→管道→文件流动，永不出现在任何命令文本或输出中：
```bash
grep -A 2 'machine api.wandb.ai' ~/.netrc | ssh <host> 'umask 077; cat > /root/.netrc && chmod 600 /root/.netrc'
```
按能力验证，不是回显值：
`python -c "import wandb; print(wandb.Api(timeout=20).default_entity)"`。永远不要将密钥写入平台分类器扫描的共享/持久 FS（那个平台细节是 profile 事实）。

### U35 — `WANDB_MODE=offline` 在封装器栈中仍因无 API key 而死 → 零曲线

**症状**：以 `WANDB_MODE=offline` 启动的运行期望"本地记录，稍后同步"却**根本不产生离线运行目录**；训练日志显示 `Disabled WandB due to initialization error: No API key configured`。

**根因**：裸 SDK 离线模式无需密钥，但项目 logger *封装器*通常在 `init` 之前探测 API
（`wandb.login()` / `wandb.Api()`）并将密钥缺失视为致命 → 它们翻转为完全禁用，而非离线。

**修复**：在首次启动前推送凭据（U34）并在平台代理下在线运行；验证第一行日志显示 `Syncing run <name>` + 一个 run URL — 将该行的*缺失*视为失败。运行已完成但无 tracker？从训练日志回填（正则每 epoch 摘要 → `init(..., tags=["backfilled"]) → run.log(..., step=epoch)`）。仍在运行？杀死并用 `--resume <latest.pth>` 重启动（成本 ≤1 epoch）。优先使用托管 tracker 使度量在拆除后存活（U20）。

---

## 委托 — 仅交叉引用，不在本文件重述

### U36 — cuDNN 非确定性

相同配置 + seed 在运行间给出略有不同的度量（`cudnn.benchmark=True` 通过首批计时选择最快内核）。由 **verifying-dl-experiments** 拥有（确定性）。交叉引用 verifying-dl-experiments **必需**；不要在这里重述修复。

### U37 — matplotlib 在大型 eval 可视化上的 `2^16` 每轴限制

大型测试集上的组合网格（每样本一行）崩溃
`Image size … must be less than 2^16`，通常中止摘要保存。由 **verifying-dl-experiments** 拥有（eval-产物大小）。交叉引用 verifying-dl-experiments **必需**；用 U25 预防（限制 + 分片，不要每样本发射文件/行）。

### U38 — GPU 利用率 0% 但训练正在运行（CPU-数据受限，非停滞）

`nvidia-smi` 读取约 0% 利用率但 step 日志在推进且模型内存已加载 — 重量级每样本 CPU 变换配合 `num_workers=0` 串行化数据准备饿死 GPU。由 **verifying-dl-experiments** 拥有（0%-利用率诊断）。交叉引用 verifying-dl-experiments **必需**；修复旋钮是 U24，移到 GPU 的补救在该技能中。

### U39 — 实时监控显示无内容（TensorBoard 面板空白 / `INACTIVE`）但训练正常

**症状**：平台的 TensorBoard 磁贴 / web 面板为空白或 `INACTIVE`，或后台监视器静默 — 但运行健康：loss 在机器上推进，事件/日志文件存在。你断定"监控坏了"或更糟"运行死了"，浪费一次检查或重启了一个正常运行的运行。

**根因**：实时可观测性以三种平台形态的方式断裂，都不是训练失败。(1) **路径不匹配** — 平台内置面板读取一个固定 logdir/端口，你的 logger 写在了别处，所以面板看到零个运行（AutoDL 固定 `tensorboard --logdir /root/tf-logs`；`SummaryWriter(log_dir="runs/<exp>")` 对它不可见）。(2) **进程已死 / 从未后台化** — TB 服务器或监视器在前台或会话下运行，在前台上限或会话/SSH 断开时被杀死，所以没有东西服务曲线。(3) **端口未暴露** — 服务在机器上启动但端口从未隧道/声明，所以面板无法到达。

**修复**（规则是通用的；*值*是每 profile 的）：(1) **对齐路径** — 将 logger 指向面板的固定目录，或在你的输出处符号链接固定目录（`ln -sfn <your-runs>/<exp> <pinned>/<exp>`）；无需重新训练 — 运行中的写入器持续追加，面板会重新加载它。固定路径在 profile 中（AutoDL `/root/tf-logs`，**AD7**；其他平台写在持久挂载点下）。(2) **在分离原语下运行 TB + 监视器**（tmux / nohup / profile 的 `DETACH`），永远不要前台，这样它们存活于会话和约 600 秒上限（`references/monitoring_patterns.md` §1；跨宿主后台 → §7）。(3) **以平台方式暴露端口** — 中国平台内置磁贴在租用时声明（`china.md`），RunPod 通过其 HTTP 代理（100 秒 Cloudflare 上限，对 TB UI 足够，`runpod.md`），Lambda / Paperspace / 裸 SSH 通过 `ssh -L 6006:localhost:6006` 隧道（`generic-ssh.md`，`lambda.md`）。在怪罪面板前，验证事实：事件文件非空（`ls -la <logdir>; du -sh <logdir>`）且 TB 本地响应（`curl -s localhost:<port>/ | head`）。对于必须**在拆除后存活**的曲线，根本不要依赖机器本地面板 → 托管 tracker（**U20**）。

---

## 指针 — 其他位置编目的陷阱

- **Spot / 抢占**（宽限窗口 2 分钟 → 约 0 秒，Young/Daly 频率，原子写入恢复，托管 spot 框架重启你的进程）→ `references/spot-resilience.md`。
- **多节点 / NCCL**（fabric-manager 挂起、错误 NIC、NCCL 超时、巨帧 MTU 不匹配、torchrun/Horovod 弹性状态恢复）→ `references/multinode.md`。单机用户跳过。
