---
name: remote-gpu-trainer
description: "在租赁/远程实例（AutoDL、RunPod、vast.ai、Lambda、Slurm、K8s）上部署、监控和调试长时间 GPU 作业：拆机/计费安全、抢占容错、可恢复断点续存、OOM/NaN 分诊。"
risk: safe
source: community
source_type: community
source_repo: Hanyuyuan6/remote-gpu-trainer
date_added: "2026-06-20"
category: ml-ops
license: "MIT"
license_source: "https://github.com/Hanyuyuan6/remote-gpu-trainer/blob/main/LICENSE"
compatibility: |
  任何兼容 Agent-Skills (SKILL.md) 的智能体 — Claude Code、Codex、Cursor、Trae、Gemini CLI 等。
  需要 shell + SSH（或平台 CLI/API）来驱动远程机器；脚本为 bash/python。部分
  持久监控方案假设宿主有后台任务运行器 + 调度器 — 映射到当前运行
  智能体的等价物（references/monitoring_patterns.md §7）。配套技能（verifying-dl-experiments、
  superpowers:*、huggingface-skills:*）为可选的独立安装。
---

# remote-gpu-trainer — 远程 GPU 作业编排

## 概述

在你**不拥有的租赁机器**上部署和照看长时间运行的 GPU 作业，跨任意平台，在计费表或抢占终止之前把结果取下来。核心理念：**你是别人机器上的短期租户** — 所以任务就是*让工作脱离实例、让结果比实例活得更久、安全地停表*，而不是去配置集群。

本技能**核心平台无关，边缘平台相关**：一套固定的操作原则 + 6 阶段生命周期在任何地方都成立，再加上每个平台一份 **profile**（`profiles/<platform>.md`）负责所有具体路径、代理、计费动词和抢占语义。它的防御性价值在于大型编排器跳过的交集：**中国 cgroup 隔离租赁 + 裸 SSH 廉价机器 + 计费硬件上的磁盘预算/监控/拆机现实**。

## 何时使用本技能

当用户在**租赁或远程的不属于自己的实例**上部署、训练、监控或排查长时间运行的 GPU 作业时使用 — 训练、评估、消融扫描、批量推理或大规模数据处理 — 在 AutoDL、RunPod、vast.ai、Lambda、Paperspace、中国平台（恒源云/矩池云/Featurize/揽睿星舟）、裸 SSH 机器、Slurm 或 Kubernetes 上；单实例或多实例均可。触发词（多语言）：
"远程 GPU 训练"、"GPU 租赁"、"GPU rental"、"租卡"、"spot 抢占"、"spot preemption"、"断点续训"、
"resumable training"、"tmux 训练守护"、"防 SSH 断线"、"scp/rsync 上传"、"多实例 ablation"、
"远程 GPU 监控"、"省钱关机/销毁实例"、"stop vs terminate billing"、"checkpoint 磁盘满"、
"CUDA OOM/显存不足"、"loss NaN/loss spike"、"loss 不下降/不收敛"、"overfit 单 batch"、
"FSDP/DeepSpeed 配置"、"多卡训练 hang"、"dataloader worker/数据增广 bug"。**不适用于**纯本地单 GPU 训练、实例内多 GPU DDP（用 torchrun/accelerate）、托管多云比价（用 SkyPilot 的技能）或零运维 serverless（用 Modal）。

## 何时不使用 — 以及该用什么

| 场景 | 替代方案 |
|---|---|
| 本地单 GPU，或**单机内**多 GPU DDP | 直接用 `torchrun` / `accelerate` |
| 托管多云比价 + 跨**西方**云的自动 spot 恢复 | **SkyPilot**（有自己的 Agent Skill）— 然后回来确保你的*代码*恢复逻辑正确，让它的恢复真正生效 |
| 开放 BYOC 开发环境 | **dstack** |
| 零运维 serverless 推理 | **Modal** |
| "这个指标/消融增量是真的吗？" | **必选：** `verifying-dl-experiments`（本技能负责*运行*作业；那个技能负责*数字是否为真*） |

**本技能针对的是那些工具留下的盲区：** AutoDL + 中国平台、裸 SSH/Slurm/K8s 租赁，以及无论你用哪个供给器都存在的运维陷阱（inode 上限、镜像停滞、cgroup OOM、静默同步失败、spot 宽限期、不可逆拆机）。

## 操作原则（WHY — 10 条不变量）

这些原则在每台计费、隔离、租赁的 GPU 上都成立；只是路径/CLI 不同。各一行；带跨平台细节的完整形式见 **`references/principles.md`**（Phase 0 前必读）。

1. **最小化付费挂钟时间。** 计费表一直在转 — 租用前在本地 CPU 上冒烟测试，以脱离方式启动，验证通过后立即释放。
2. **廉价检查先于昂贵计算。** 1-2 个 batch 的 CPU 冒烟（关闭 logger）几乎零成本就能干掉 import/config/shape/scale 类 bug。（冒烟*内容* → `verifying-dl-experiments`。）
3. **信任你加载到的产物，而非声称成功的日志行。** "synced/saved/done" 在静默写入失败时会撒谎；监控器自身的状态也是一种声明 — 要对照真实进程/产物来校验。
4. **了解 stop 与 destroy 各自能保留什么。** 每个平台上，明确哪个挂载在 *stop* 后存活、哪个在 *terminate* 后存活 — 你需要的数据往往在易失的那个上。（最大的可移植性陷阱。）
5. **存储在你没监控的维度上失效。** 磁盘在 **inode** 上先于字节数死亡；真正的吞噬者藏在符号链接缓存里；按价值清理（保留微小证据，丢弃大型临时文件）；监控 `df -i`，不只是 `df -h`。
6. **不要在运行中的作业下修改输入。** 运行中的作业按字节偏移将脚本保持在内存中；运行期间覆写会导致代码块重新执行。版本化文件名。
7. **为重试而设计 — 失败是概率性的，传输是脆弱的，镜像是路由特定的。** 让包装器幂等 + 可恢复；以*相同*配置重试；用 `timeout`+恢复循环包装批量传输；镜像/代理只加速一条路由 — 在真实传输使用的同一路由上验证。
8. **断点存入持久存储 + 幂等恢复是通用骨架。** 将 checkpoint 文件写入平台的持久位置 + 启动时无条件加载最新，这是*唯一*能扛住 SSH 断连、Slurm 墙时杀进程、K8s 重调度、spot 抢占和 Colab 断连的机制。脱离原语（tmux/sbatch/Job/commit）是可替换的插头；这才是不变量。
9. **成本和破坏性操作由用户决定。** 永不自动释放/终止，永不未经确认删除持久文件；如果清理无法释放空间，**请求扩容磁盘**而不是静默缩小实验。
10. **教会用户平台，而不只是驱动它。** 多数用户不了解平台的不明显**便利功能**（一键 SSH 密钥注册、GPU 可用通知、内置面板）或其**危险时钟**（已*停机*机器上的自动释放/自动删除计时器 — AutoDL 在 15 天后释放关机实例 → 数据盘消失；stop 仍在计费；低余额清除）。首次接触时就展示 — #9 阻止智能体*做*危险的事，#10 在时钟触发前*警告人类*。各平台列表 → 每个 profile 的 **Surface to the user** 块。

> **监控物理学（#3 的基础）：** 前台 Bash 硬限制 600 秒；`run_in_background` 无限制且退出时通知；永不退出的监控器永不通知；轮询正则中未加引号的 `|` 会读取 stdin 并永远挂起。四层监控架构建立在这些事实之上 → `references/monitoring_patterns.md`。

## 代码纪律（你编写的包装器和训练脚本）

两条规则管辖本技能让你编写的启动/包装/训练代码 — #1 和 #8 的推论，而非新的不变量：

1. **先复用再编写。** 在添加代码前先用最低层已有的可用方案：基础镜像的预装栈 + 平台功能 → 框架/库工具（`torchrun` / `accelerate` / HF） → 你已有的 `scripts/` 模板 → 最少新代码。在计费机器上不必要的 `pip install` 也在浪费付费挂钟时间，还可能破坏镜像的 ABI — Phase 1 的规则（*预构建镜像就是环境；不要在租赁机上 `conda create`*）正是此原则在依赖管理上的应用。
2. **底线 — `minimum` 限制范围，不限制正确性。** 缩减代码时绝不能丢弃让昂贵运行可存活的部分：断点存入持久存储 + 幂等恢复（#8）、原子写入、防止丢失长时运行的错误处理、或 seed/determinism 日志。对非平凡逻辑保留一个最小自检。

## 先选好你的平台 Profile

在 **Phase 0 之前**读取对应的 profile — 它负责所有路径、代理、凭证位置、计费动词和抢占规则，下面各阶段都会委托给它。每个 profile 遵循相同的 8 字段模式（`profiles/_schema.md`）。

> **新来的？路径是：** (1) 在下表中找到你的平台 → (2) 阅读该 profile 的 **LAUNCH** 部分（它会引导你完成租赁 → 注册 SSH 密钥 → 连接机器） → (3) 回来从 Phase 0 开始执行 6 个阶段。
> 已经有一台可以 `ssh` 进去的机器？直接跳到 Phase 0。

| 你在用… | Profile | 类型 | 脱离原语 | 停表动词 |
|---|---|---|---|---|
| AutoDL（最深，实战验证） | `profiles/autodl.md` | ssh-rental | tmux | 关机（停止计费，**保留磁盘** — AutoDL 的例外） |
| RunPod | `profiles/runpod.md` | ssh-rental | tmux | **terminate**（stop 仍以 2 倍计费；销毁卷磁盘） |
| vast.ai | `profiles/vastai.md` | ssh-rental (spot) | tmux | **destroy**（stop 永远计费磁盘） |
| Lambda | `profiles/lambda.md` | cloud-api | tmux | **terminate**（无 stop 状态） |
| Paperspace | `profiles/paperspace.md` | cloud-api | tmux | **destroy + release IP + delete storage**（shut-down 仅停止计算） |
| 恒源云 / 矩池云 / Featurize / 揽睿星舟 | `profiles/china.md` | ssh-rental | tmux | 各平台不同（数据盘停机时常仍计费） |
| 裸 SSH 机器 / Slurm / K8s / Colab-Kaggle | `profiles/generic-ssh.md` | ssh / slurm / k8s | tmux / sbatch / Job / commit | **手动**（遗忘的机器 24/7 计费） |

> **Profile 置信度：** AutoDL 经作者日常使用实战验证；其余六个 profile 基于各平台官方文档 + 社区报告构建（内联引用，`verified <month>`），尚未独立实战测试 — 依赖 Phase 0 的实时测量，并**在押上金钱或数据前，对照当前文档重新验证任何拆机/计费事实**（`references/self-improvement.md` §5）。

**心智动词模型**（跨所有平台的统一 API；profile 将每个动词绑定到实际命令）：
`up`（租赁+连接）→ `push`（代码/数据上传）→ `run`（脱离+断点续存）→ `watch`（持久监控）→ `pull`（结果下载+验证）→ `down`（停止计费）。

## 默认工作流（6 个阶段）

跳过已完成的阶段。每个阶段将底层细节委托给 profile，并以**可运行的检查**结束。

**Phase 0 — 环境审计。** 读取 profile 的 STORAGE 存活矩阵 + 区域/数据中心锁定。实时测量：
`df -h && df -i <data-mount>`、cgroup `memory.max`、`nvidia-smi`。预计算断点磁盘预算（`ckpt_size × N + scratch`）。→ **验证：** `nvidia-smi` 显示预期 GPU 且 `df -i` 不接近 100%。

**Phase 1 — SSH + 凭证。** 按 profile 设置别名/环境（预构建镜像/基础镜像就是环境 — 不要在租赁机上 `conda create`）。**从未租过？profile 的 LAUNCH 部分会引导你完成租赁 → 注册 SSH 密钥 → 连接。** 通过 **stdin 推送密钥，绝不写入共享/持久文件系统**（`references/ssh_transport.md`）。→ **验证：** `ssh <alias> 'python -c "import torch;print(torch.cuda.is_available())"'`。

**Phase 2 — 包装器 + CPU 冒烟门槛。** 从 `scripts/` 构建幂等的 `run_one`/`run_queue`（参数化自 profile 的 OVERRIDES；**独立运行时按机器设置 batch/workers 大小，但跨 cell 比较时 PIN 住它们** — `references/training/throughput-profiling.md`）。**租用前在本地运行廉价 CPU 冒烟** — 干掉那些低级且昂贵的失败（如 `python -m <your.train.module> --limit-batches 2 --epochs 1` — 替换为你自己的入口点；此门槛需要你的训练代码接入）。→ **验证：** 冒烟在 2 个 batch、logger 关闭时以退出码 0 结束。

**Phase 3 — 脱离启动。** 通过 profile 的脱离原语启动；短暂探测（日志头部 + 存活 + 无 traceback），然后**交还控制** — 绝不做阻塞式前台 `sleep`。→ **验证：** 60 秒内，脱离会话存活且首行日志显示预期的 step/epoch。

**Phase 4 — 持久监控。** 超过约 1-2 小时的任务，部署**四层架构**（`references/monitoring_patterns.md`）：机上自完成链 + 会话巡逻循环 + 事件哨兵 + 恢复手册。**在 Claude Code 上，通过 `/loop 30m`（或 `ScheduleWakeup`）运行 `scripts/health_patrol.sh.template` 触发 L2 巡逻**；没有本地定期运行器的宿主则改用机上自推送（`references/monitoring_patterns.md` §7）。仅绑定会话的监控器会随会话消亡。对每个结果分类 → 固定修复方案；**绝不盲目重试**。→ **验证：** 即使没有变化，巡逻也会报告。

**Phase 5 — 聚合 + 验证 + 拆机。** 校验同步到持久存储（以复制结果作为成功行的门槛 — 原则 #3），然后**加载并验证每个产物**（`scripts/verify_local.py`），再执行 profile 的停表操作。→ **验证：** `verify_local.py` 在任何拆机前报告 100% OK。

> **铁律 — 拆机门槛：** 在 checkpoint **已拉到本地且通过加载验证**之前，不得执行 `release` / `terminate` / `destroy` / 文件删除，且用户已明确批准影响成本的操作。
> "日志里看起来完成了"不算证据（原则 #3）。大多数平台上停表操作是**不可逆的**（删除磁盘）— 确认的重要性只会更高，不会更低。

## 并行消融扇出

对于 N 个消融 cell：每个 cell 一个作业，每个作业一条**隔离的写入路径**（无共享可变输出），跨实例/队列启动。**必选：** `superpowers:dispatching-parallel-agents` 提供独立性谓词（不要在共享状态上扇出）和扇出后必须的对账。文件系统共享部署模式 → `references/parallel_ablation.md`。

## 快速参考 — 每个平台咬人的四个事实

完整细节见各 profile；本表为速览。

| 平台 | **stop** 后存活 | **destroy** 后存活 | Spot 宽限期 | 需要中国镜像 |
|---|---|---|---|---|
| AutoDL | /root + data + FS | 仅 FS | n/a | 是（`/etc/network_turbo`、hf-mirror） |
| RunPod | 卷磁盘（2 倍计费） | 仅 Network Volume | ~5 s SIGTERM→KILL | 否（`hf_transfer`） |
| vast.ai | 磁盘（永远计费） | 无 | ~0 s（突然） | 否 |
| Lambda | n/a（无 stop） | 无 | n/a（按需） | 否 |
| 中国（恒源云/矩池云/…） | 各异；数据盘计费 | 各平台持久卷 | n/a | 是 |
| generic-SSH/Slurm/K8s | 你自己管 | 你自己管 | Slurm SIGTERM→KillWait（默认 30 s） | 仅在中国时 |

## 常见陷阱（前 8 条内联 — 完整目录在 references/）

最费 GPU 时长的通用陷阱。症状 → 修复；根因 + 其余内容见 **`references/gotchas_universal.md`**（运行 `grep -i '<keyword>' references/gotchas_universal.md` 跳转）。

1. **`pkill -9` 导致 SSH 断连**（退出码 255 + "Connection reset"）— 正常；重新 ssh 验证，不要慌。
2. **tmux 将脚本保持在内存中** — 运行期间编辑会重新执行代码块；版本化文件名。
3. **磁盘满导致 `torch.save` 崩溃**（`iostream error`）— 提前预算；自动清理 `latest.pth`，保留 `best`。
4. **cgroup OOM 无 traceback**（仅 `Killed` / 退出码 137）— `num_workers × 大张量`；按 `memory.max` 设置 workers，而非 CPU 数。
5. **静默同步失败** — `cp … 2>/dev/null; echo synced` 在磁盘满/inode 耗尽时撒谎；以实际复制结果作为成功行的门槛。
6. **Spot 抢占宽限期极短（~5 s → ~0 s，本技能所列平台；AWS 式 2 分钟宽限仅在未列出的云上）** — SIGTERM 刷写处理程序不是安全网；按定时器将 checkpoint 写入持久存储，启动时无条件加载最新（`references/spot-resilience.md`）。
7. **"Stop" 很少停止计费** — 只有 `terminate`/`destroy` 才行，且不可逆（删除磁盘）。点击前从 profile 了解动词，RunPod 上停止的 Pod 甚至可能以零 GPU 重启。
8. **CRLF 在 Linux 上破坏 `.sh`** — 在 Windows 上编写 → `.gitattributes` `*.sh text eol=lf`；在机器上解除 `sed -i 's/\r$//'`。

## 当训练本身出问题时（模型问题，非平台问题）

平台运维只是工作的一半 — 机器跑起来后，训练有自己的崩溃方式。`references/training/` 层是针对运行本身的调试知识。边界：**本层负责"让它跑起来、跑得快、不崩溃"；`verifying-dl-experiments` 负责"数字是否为真"** — 交叉链接用于崩塌/泄漏/指标有效性。每条都是症状 → 根因 → 修复，引用当前文档。

- `references/training/oom-memory.md` — CUDA/VRAM + 主机 RAM OOM 及适配阶梯（grad-accum → bf16 → activation-checkpointing → `expandable_segments` → FSDP/ZeRO → CPU/NVMe offload → LoRA/QLoRA）；特定步骤的 OOM（首次反向传播 / 验证 / 最长 batch）；内存快照 + 可视化器。
- `references/training/distributed-launch.md` — `torchrun`/`accelerate`/`deepspeed` 启动 + 环境约定，DDP/FSDP/ZeRO 配置，以及多 GPU **HANGS** 工具包（单 rank 分叉、rank 条件集合通信、dataloader 长度不匹配）。多节点连线 → `references/multinode.md`。
- `references/training/precision-stability.md` — fp16/bf16/tf32 + AMP/GradScaler，NaN/Inf 追踪（`detect_anomaly`），LLM **loss 尖峰** + 发散（warmup、clip、init、z-loss）。
- `references/training/throughput-profiling.md` — GPU 受限 vs 数据受限 vs 通信受限；dataloader 旋钮；`torch.compile` 陷阱；flash-attention；`torch.profiler` / Nsight。
- `references/training/checkpoint-resume.md` — 全状态保存/恢复机制，分片（FSDP/DeepSpeed）checkpoint，以及恢复 bug（epoch 重启、数据重新洗牌、scaler/EMA 丢失）。Spot 频率 → `references/spot-resilience.md`。
- `references/training/by-domain.md` — 各领域陷阱：LLM/transformer、视觉（检测/分割）、扩散、RL、多模态/VLM。
- `references/training/convergence-debugging.md` — **"能跑但学不到 / 学得差"** 层：overfit-one-batch 冒烟、参数不更新、优化器/LR/weight-decay/schedule 配置、loss 函数陷阱（double-softmax、BCEWithLogits、CE-target 格式）、微调/冻结（frozen-BN 漂移、判别式 LR、LoRA 接线），以及训练动态面板（update:weight 比率、dead-ReLU、GradScaler-scale）。
- `references/training/data-pipeline.md` — dataloader/dataset **正确性**（非速度）：worker-RNG 增强重复 bug、IterableDataset worker/rank 分片、collate/`__len__`/`pin_memory`/`spawn` 约定，以及预处理/标签/洗牌陷阱（RGB-vs-BGR、ToTensor ÷255、`set_epoch`）。

## 配套技能（独立安装；存在时必读）

这些是**独立的** Agent Skills，不包含在本技能中 — 安装它们以获得完整体验。在未安装某个配套技能的智能体上，将其下方的指针视为可选交叉引用；本技能仍可独立工作。

- **`verifying-dl-experiments`** — 负责*数字是否为真*：冒烟内容、重试 vs 安全保障、可保留 checkpoint、评估规模、tracker 取证、GPU-0%-利用率诊断。本技能负责*在哪里/何时/花多少钱*。
- **`huggingface-skills:hf-cli`** — 传输动词（`hf download --resume`、`hf upload-large-folder`、`hf cache verify`）；本技能负责中国镜像切换 + 停滞重试（`references/china-network.md`）。
- **`huggingface-skills:huggingface-trackio`** — 托管 tracker，让指标在拆机后存活（陷阱 U20）；轮询 `trackio` 告警作为结构化监控，替代脆弱的 ssh-tail。
- **`superpowers:verification-before-completion`** — 铁律的通用形式；为每个"训练完成 / 已同步 / 拆机完成"声明设门槛。
- **`superpowers:dispatching-parallel-agents`** — 消融扇出的独立性谓词 + 对账。

## 随时间自我改进（捕获新陷阱 + 个性化）

本技能是静态的，但每次运行都能教会它新东西 — 而不会破坏它。协议 → **`references/self-improvement.md`**。简言之：当某次运行暴露了目录中缺少的陷阱时，**只沉淀经过根因分析、可复现、可泛化的那类**（一次性的偶然抖动是假说，不是陷阱 — 原则 #3）；**路由它** — 用户/项目特定的 → 宿主的记忆系统，可泛化的 → 提议添加到 `references/gotchas_universal.md` / profile §7 / `references/training/`（并提供上游 PR）；**绝不静默重写技能文件 — 起草 `症状 → 根因 → 修复` 并让用户批准。** 首次使用时，将用户的平台 + 路径 + tracker 实体捕获到记忆中，以便后续运行预参数化。平台事实带有 `verified <month>` 戳 — 在押上金钱或数据前，对照当前文档重新验证任何拆机/计费事实。

## 局限性

- 不替代真正的云编排器或托管供给器；用它让租赁机器上的工作可存活，而非优化多云采购。
- 平台计费、stop、destroy 和数据保留行为可能漂移；在破坏性或影响金钱的操作前重新检查当前提供商文档。
- 需要用户自有凭证、SSH/API 访问，以及在拆机、删除或其他不可逆清理前的明确确认。
- 上述配套技能不包含在本技能中；除非安装在当前智能体环境中，否则视为可选引用。

## 打包资源

仅加载当前阶段所需的内容。

- `references/principles.md` — 10 条不变量的展开，含各条背后的跨平台细节。
- `references/lifecycle_checklist.md` — 6 阶段操作手册，按平台列出检查项。
- `references/gotchas_universal.md` — 通用 + 混合陷阱（顶部有 TOC + grep 索引）。
- `references/monitoring_patterns.md` — 四层持久监控架构 + 健壮 ssh-poll 模板。
- `references/ssh_transport.md` — ssh 配置、rsync/scp 可恢复模式、密钥通过 stdin 传输、CRLF、两种 SSH 风格注意事项。
- `references/china-network.md` — 镜像表 + HF_ENDPOINT + 可恢复下载阶梯 + `no_proxy` 陷阱（所有中国平台）。
- `references/spot-resilience.md` — 抢占信号、Young/Daly checkpoint 频率、原子写入恢复。
- `references/parallel_ablation.md` — 文件系统共享扇出 + 独立性谓词 + 对账。
- `references/multinode.md` — （高级）NCCL / fabric-manager / elastic-training 陷阱；单机用户跳过。
- `references/training/` — **DL 训练调试层**（8 个文件：oom-memory、distributed-launch、precision-stability、throughput-profiling、checkpoint-resume、by-domain、convergence-debugging、data-pipeline）— 见上方"当训练出问题时"。
- `references/self-improvement.md` — 反馈循环：从（酒吧里）捕获新陷阱到记忆或目录，首次运行时个性化，保持平台事实新鲜。
- `scripts/` — 包装器模板（`run_one`/`run_queue`）、监控器（`mem_monitor`、`gpu_health`、`reap_vram_zombies`）、只读巡逻（`health_patrol.sh.template`）、传输/聚合（`download_loop`、`aggregate_to_fs`、`setup-china-mirrors`）、加载验证检查器（`verify_local.py`），以及 `verified` 戳新鲜度检查器（`check_staleness.py`）。
- `profiles/<platform>.md` — 各平台底层细节（每平台一份；`_schema.md` 定义 8 个字段）。
- `examples/autodl_sweep/` — 一个完整的、可运行的端到端实战案例。
