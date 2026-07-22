# 监控模式 — 远程 GPU 作业的持久化守护

平台无关的配方，用于看护租赁机器上的长运行分离作业。核心是**四层持久监控架构**（§3）：仅会话绑定的监视器随会话消亡，所以要分层。每个配方使用可移植原语 — `tmux` 或 `squeue` 或 `pgrep`，日志标记或产物 `mtime` — 永远不是一个平台的路径。从 `profiles/<platform>.md` 绑定具体路径/别名。

跳转：`grep -in '<keyword>' references/monitoring_patterns.md`。

## 目录

- §0 监控物理 — 每个配方依赖的四个事实
- §1 健壮的短连接 ssh 轮询模板（安全轮询原语）
- §2 快速健康探测（每次一个往返）
- §3 持久监控架构 — 四层（L1 自完成 · L2 巡逻 · L3 哨兵 · L4 手册）
- §4 过时等待器卫生 — 每个活跃运行一个等待器，正确生命周期
- §5 两段式自完成 — 保证结果 + 尽力节奏
- §6 日志上的故障分诊
- §7 跨智能体主机的监控 — 每主机后台/循环/cron 原语 + 2 条可移植性规则（Claude Code · Codex · Cursor · Trae · 通用）

---

## §0 监控物理 — 每个配方依赖的四个事实

在会话中验证，非假设。整个架构围绕这些工程化：

> **工具可移植性说明：** `run_in_background`、约 600 秒前台上限和 `/schedule`（下文及 §5/§3）是 **Claude Code** 线束的原语。在另一个 Agent-Skills 主机（Codex / Cursor / Trae / …）上，将它们映射到该智能体的等价物 — 其后台任务或异步运行器、其自身的前台/回合限制、其调度器。四层架构本身是主机无关的 — 完整的每主机映射（Codex / Cursor / Trae / 通用）和两条可移植性规则在 **§7** 中。

1. **前台 Bash 硬性上限 600 秒（10 分钟）。** 长前台等待/监控在上限处被*杀死* — 所以永远不要前台轮询多小时运行。
2. **`run_in_background` 没有持续时间上限并在退出时通知。** 一个 781 秒的后台任务运行完成并通知（已验证）。完成的长期任务 → 后台运行。
3. **一个永不*退出*的监视器永不通知。** 无退出事件 = 永远无通知。一个持久 `while true` / 一个游离的 `grep` 读取 stdin 静默永远挂起，用户将静默读作"死亡监视器"。每个监视器必须有有界退出。
4. **轮询正则中未加引号的 `|` 永远挂起。** Shell 将 `grep -hE a|b|c log` 拆分为三个管道命令；第一个（`grep -hE a`，无文件名）读取 **stdin** → 阻塞 → 管道永不返回 → ssh 永不返回 → 后台进程永不退出 → 事实 3 触发。始终引用正则并给 grep 提供文件名。

推论 — **信任产物，不是静默。** 当作业"看起来完成"时，Read 其输出文件并重新检查事实（`grep DONE log; tmux ls / squeue; nvidia-smi`）再声称成功。不要盲目等待可能永不触发的通知。这是 `verifying-dl-experiments`（必需）铁律在监控上的应用。

---

## §1 健壮的短连接 ssh 轮询模板（安全轮询原语）

最重要的单一模式：一个不会挂起（事实 4）且不会滞留半开连接的轮询。**永远不要为整个等待持有一个长 ssh** — 本地循环，每次重连。

```bash
#!/usr/bin/env bash
set -u
# 短连接轮询：ssh 进 → 检查 → 断开；有界本地循环。
HOST="<alias>"                       # 来自 profiles/<platform>.md
LOG="/path/to/run.log"               # 远程日志路径（profile 绑定）
PATTERN='QUEUE DONE|Training completed'   # 引用 → '|' 是交替，不是管道（事实 4）
MAX=120                               # 有界：120 次轮询 × 90 秒 ≈ 3 小时，然后干净放弃
i=0
while [ "$i" -lt "$MAX" ]; do
  # ConnectTimeout + ServerAlive 将网络抖动限制在约 30 秒而非数分钟的半开挂起。
  if ssh -o ConnectTimeout=15 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 "$HOST" \
       "grep -qE '$PATTERN' '$LOG'"; then          # 引用正则 + 文件名 → grep 读文件，不读 stdin
    echo "DONE marker found"; exit 0
  fi
  i=$((i+1)); sleep 90
done
echo "poll gave up after $MAX ticks — check ground truth manually"; exit 1
```

不可协商的要点：
- **引用正则 + 文件名**在每次远程 `grep` 上 — 防止事实 4 的两个独立守卫。
- **`ConnectTimeout` / `ServerAliveInterval` / `ServerAliveCountMax`** — 断开的连接快速自杀。
- **每次轮询短连接，有界本地循环** — 每次检查一次 ssh，硬性轮询上限使等待器始终退出（事实 3），因此后台化时始终通知。
- **通过日志标记检测"完成"，永远不用 `pgrep` 匹配等待器自身的模式** — `pgrep -f` 匹配等待器自身命令行，循环永不结束。在队列调度器上，`squeue -j <id>` 变空是等价的完成信号。

通过 `run_in_background` 运行（事实 2：无上限，退出时通知），或在 600 秒上限下作为单次前台轮询（事实 1）。在会话调度器上将其作为 L2 巡逻体（§3）。**永远不要前台轮询完整等待。**

---

## §2 快速健康探测（每次一个往返）

每个是单次短 ssh。将多个组合为一次巡逻轮询的 ONE 个往返（§3）。分离原语和路径来自 profile；结构到处相同。

> 空白的实时 **TensorBoard 磁贴 / web 面板**而这些探测显示运行健康**不是**死亡运行 — 它是 `references/gotchas_universal.md` **U39**：面板读取固定 logdir/端口你的 logger 没写入，或 TB/监视器进程已死（前台运行而非在分离原语下），或端口未暴露。按平台 profile 修复；永远不要因空面板重启健康运行。

**作业存活吗？（tmux 或 squeue 或 pgrep — 选择 profile 的原语）**
```bash
ssh "$HOST" "tmux ls 2>/dev/null || true; squeue -u \$USER 2>/dev/null || true; pgrep -af 'train' | grep -v grep | head -3"
```

**自上次检查以来的进度** — grep 运行自身日志，非共享主日志：
```bash
ssh "$HOST" "grep -nE 'Epoch [0-9]+|Training completed|Early stopping|FINISHED|QUEUE DONE' '$RUN_LOG' | tail -6"
```

> **陷阱 — 在每运行日志上做崩溃检测，不是共享主日志。** 症状：轮询报告"运行 D 崩溃"而 D 训练正常。→ 根因：一个 `tee` 的主日志连接了每个运行，所以搜索 `Traceback|OutOfMemory` 匹配了*更早*运行的崩溃文本，在健康的后续运行上误报。→ 修复：将崩溃检测限定在每运行日志（`<name>.log`）；主日志 grep 保留给 `DONE`/`FINISHED`/`QUEUE DONE` 和进度标记。在错误日志上做崩溃检测的等待器会在幻觉故障上旋转到超时。

**资源压力**（cgroup 内存，GPU）— 阈值是粗略的，profile 可调：
```bash
ssh "$HOST" "nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader; \
  [ -f /sys/fs/cgroup/memory.current ] && numfmt --to=iec \$(cat /sys/fs/cgroup/memory.current)/\$(cat /sys/fs/cgroup/memory.max) 2>/dev/null"
```
- cgroup 内存 > 90% 的 max → OOM 风险；GPU 利用率 > 60% → 健康，非数据瓶颈。
- GPU 0% 但 step 日志在推进 ≠ 空闲 — 它是 CPU-数据受限；采样数秒的利用率，永远不要一次快照。（诊断 → `verifying-dl-experiments`，必需。）

**磁盘 — 静默杀手** — 监控 `df -i`（inode）和 `df -h`（字节）；inode 在多小文件 eval 输出上先死（→ `references/gotchas_universal.md`）：
```bash
ssh "$HOST" "df -h '$DATA_MOUNT'; df -i '$DATA_MOUNT'"
```

---

## §3 持久监控架构 — 四层（由三次实战故障赚取）

会话绑定的监视器随会话消亡；实例本身可能在监视器下死亡；只说终端事件的监视器读作"没人看着"。一层无法修复所有三个。运行四层 — **L1 正确性、L2 存活性、L3 延迟性、L4 连续性**：

| 层级 | 住在哪 | 作业 | 存活于 |
|---|---|---|---|
| **L1 自完成链** | 在机器上（tmux / nohup / sbatch 依赖） | 工作自行排序：`until grep -q 'Training completed' log; do sleep 150; done && <next stage>`；阶段通过 `touch /path/STAGE_DONE` 标记交接 | 会话死亡、网络丢失 |
| **L2 巡逻循环** | 会话调度器（cron `/loop`） | 每约 30 分钟触发一次自包含巡逻：一次组合 ssh 探测 + 决策表 + "即使没变化也报告" | 空闲间隔（非会话死亡 — 见 L4） |
| **L3 事件哨兵** | 会话后台（`run_in_background`） | §1 短轮询 `until ssh test -f MARKER; …` 用于巡逻轮询间的分钟级反应 | 无 — 可接受；L1/L2 承载正确性 |
| **L4 恢复手册** | 持久笔记/记忆 | 精确恢复命令、链定义、标记路径、"重连第一条命令" — 一个全新会话从一个词接管 | 一切 |

### L1 — 机器自完成链（正确性）
机器无论有无监视器都完成自己的管道。在一个分离原语下链式阶段并用 `&&` 连接，**永远不用 `;`**，这样标记只在成功时落地：
```bash
# tmux / nohup 变体 — 分离原语是可插拔的（Slurm 上是 sbatch 依赖）
nohup bash -c '
  set -u
  until grep -q "Training completed" /path/to/train.log; do sleep 150; done \
    && python -m eval ... \
    && touch /path/to/STAGE_DONE        # 标记仅在干净的 && 链上落地
' </dev/null >/path/to/chain.log 2>&1 &
```
> **陷阱 — 成功门控链标记。** 症状：下游链在幻觉完成上触发。→ 根因：用 `;` 连接阶段（或在崩溃阶段后裸 `touch`）即使阶段死亡也标记 — 一个活的磁盘满 `torch.save` 杀死了阶段 3，`;` 标记仍落地，下一阶段在空上运行。→ 修复：每个阶段和最终 `touch` 之间用 `&&`；通过标记检测完成，永远不用 `pgrep` 匹配等待器自身模式（事实 4 / §1）。

### L2 — 巡逻循环（存活性）：设计清单（让它真正工作的要素）
- **每次轮询一次组合 ssh 探测** — 存活检查（tmux ls / squeue / pgrep）+ `*_DONE` 标记 + 最后 epoch 行 + 产物 `ls` + 数据集文件计数，在单次往返中。
- **显式决策表**，如：ssh 宕机 → 告诉用户检查控制台（只有他们看到余额/电源状态）；分离会话缺失且无完成标记 → 从 `latest` 恢复 + 重建 L1 链；结果 CSV 存在 → `cat` 它并逐字报告数字；远程文件数低于本地源 → 恢复传输；一切完成 → 删除巡逻作业本身。
- **即使没变化也报告一行状态** — 事件之间的静默正是用户读作"死亡监视器"的东西。（"你有定时看吗??" 在一次活动中出现两次是仅 L3 的失败签名。）
- **完整性 = 对本地源的文件计数**（名称冲突时用字节/哈希），永远不用 `test -d` — 被杀死传输创建的目录永远通过存在检查。
- **永远不要盲目重启** — 先探测会话/日志/标记，这样巡逻在运行中途触发时不会双重启动（幂等性）。分类每个结果 → 固定修复；永远不要盲目重试。

> **现成的轮询：** `scripts/health_patrol.sh.template` 是这个清单作为一个可运行的、只读 ssh 往返 — 存活 + 完成计数 + 最后 epoch + 崩溃扫描 + `df -h`/`df -i`，升级谓词，即使没变化也一行报告 — 从 profile 的 §8 参数化。从宿主的循环运行器触发（§7：`/loop`，cron `3,33 * * * *`，…）。

### L3 — 事件哨兵（延迟性）
§1 短轮询循环用于巡逻轮询间的分钟级反应。不存活任何东西 — 它是一次性快速反应层；L1/L2 承载正确性。每次会话恢复后只重新武装一个。

> **`run_in_background` 不是无人值守等待上 `/loop` 的替代品。** 一次性的 `run_in_background` 哨兵在退出时通知 — 在活跃会话中工作时没问题，但如果会话空闲数小时，其退出通知落在关闭/重置的会话上，你什么也听不到（静默监视器数小时的失败）。任何超过约 1 小时的无人值守等待 → 绑定 **L2 `/loop` 巡逻**（一个循环智能体重唤醒），永远不是孤立的一次性哨兵。

### L4 — 恢复手册（连续性）
持久笔记，全新会话从一个词继承（"继续"）：精确恢复命令、L1 链定义、每个标记路径、"重连第一条命令"。两个持久强化：
- **将传输/监控状态外部化到稳定的 OS 路径** + 一个在会话目录*之外*的 DONE 标记文件，这样任何未来会话通过读取文件恢复而非重新上传。
- **真正的重启免疫意味着 OS 拥有的进程**（Task Scheduler / cron）— 但创建一个是权限分类器认定的未授权持久化：**先获取用户的明确一行批准**，或把启动命令交给他们自己运行。

> **陷阱 — 上下文压缩后，将 UI 任务芯片与 OS 进程表对账。** 症状：5 个芯片显示"Running"2–6 小时，而零 ssh/scp 进程存在，"运行中"的上传实际在 2/10 检查点处死了，静默门控下游 eval 整晚。→ 根因：后台 shell 随旧会话死亡，但其芯片继续显示"Running"；新会话的任务列表为空，所以唯一的事实是进程扫描。→ 修复：**任何压缩后的第一个动作是进程扫描**（如 `Get-CimInstance Win32_Process` 匹配远程主机字符串，或 `pgrep`/`ps` 查找 ssh/scp），用字节大小验证重新启动死亡传输，重新武装一个新鲜哨兵，并告诉用户清除残骸。

---

## §4 过时等待器卫生 — 每个活跃运行一个等待器，正确生命周期

> **陷阱 — 过时后台等待器堆积。** 症状：Background-tasks 面板显示 8+ 个 "Running" 等待循环，500–740 分钟已过，每约 20 秒 ssh 轮询，而 GPU 空闲，实验数小时前已完成。→ 根因：每次杀死+重启不稳定网络 saga 都武装了一个新的 `until ssh grep MARKER; do sleep 20; done` 等待器但从未停止旧的 — 其标记（在已取代日志中）永不出现，所以它永远循环（事实 3）。→ 修复如下。

- **每个活跃运行一个等待器。** 取代运行 → 先停止其旧等待器（TaskStop，或从 UI 解除跨会话芯片 — 恢复的会话 ID 无法编程停止）。
- **匹配监视器生命周期到等待。** 多小时等待 → 持久 Monitor（无 10 分钟上限）加上停滞检测器使挂起运行仍通知。持久监视器仍在会话恢复时死亡 → 任何恢复后，**直接检查远程事实**（tmux ls / squeue，`grep DONE log`，`nvidia-smi`）；不要信任可能已消失的监视器（事实 3 + §0 推论）。
- **断开的轮询连接 ≠ 作业死亡。** 长后台 ssh 轮询被远程的空闲 SSH 超时杀死，而分离训练独立继续。重新 SSH 并直接验证进程/产物，再断定任何东西已死。

---

## §5 两段式自完成 — 保证结果 + 尽力节奏

"我会定期检查"是谎言，除非武装了触发器 — 回合之间助手不运行。两段，永不混淆：

- **段 1 — 远程自完成（保证的，存活于会话/SSH 死亡）：** L1 链（在一个分离原语下 `train → eval → touch marker`）。通过日志/标记检测完成，永远不用 `pgrep` 匹配等待器自身模式。这保证结果但不给报告节奏。
- **段 2 — 实时进度（尽力而为）：** 会话绑定的巡逻循环（L2，如 `/loop 30m` 或 cron `3,33 * * * *`）用*本地* SSH 密钥轮询。坦诚它在会话关闭时死亡 — 远程仍完成；用户重新 ping 来拉取。

> **云调度器无法到达租赁机器。** 云调度（`/schedule` / RemoteTrigger）在隔离沙箱中运行，有自己的检出且**无法访问本地 SSH 密钥或网络** → 它无法 ssh 机器，且 SSH 私钥**绝不能**放入云智能体（密钥泄漏）。诚实的循环检查是远程自监控 + 会话循环，不是云机器人 ping 机器。不要承诺无法兑现的自主跨会话轮询。

对于度量在拆除后存活且可作为结构化监视器轮询而非脆弱 ssh-tail 的托管 tracker，使用 `huggingface-skills:huggingface-trackio`（该路径必需）— 轮询其告警而非 grep 远程日志。

---

## §6 日志上的故障分诊

当探测显示问题时，从每运行日志拉取完整 traceback（§2）并分类 — 每个结果映射到固定修复；永远不要盲目重试：

```bash
ssh "$HOST" "grep -B2 -A20 'Traceback' '$RUN_LOG' | head -50"
```
- `basic_ios::clear: iostream error` + `unexpected pos N vs M` → **检查点保存期间磁盘满**；检查 `df -h`/`df -i`，修剪 `latest`/周期快照以恢复（→ `references/gotchas_universal.md`）。
- 裸 `Killed` / exit 137，无 traceback → **cgroup OOM**（workers × 大内存 tensor）；根据 `memory.max` 调整 workers，不是 CPU 数量。
- `CUDA out of memory` → VRAM，通常跨运行一致（batch 太大 / 并发作业），极少瞬态。
- `KeyError` / `AttributeError` → 配置/代码不匹配；调查代码，不要重试。
- 在 epoch 1–2 中远低于基线提前停止并伴随 grad_norm P99 尖峰 → 可能是**概率性发散**；是否是 bug 或真实效应，以及重试相同配置规则，属于 `verifying-dl-experiments`（必需）— 本技能拥有*运行*重试，不是评判数字。
- 日志冻结（无新行）但检查点 `mtime` 推进 → **块缓冲 stdout**，非挂起（`references/gotchas_universal.md` U43；运行 `python -u`/`PYTHONUNBUFFERED=1`）。
- 机器上 `uptime`/`free` 看起来爆满但你的 cgroup 宽裕 → 共享宿主上的**吵闹邻居**，不是你的作业（`references/gotchas_universal.md` U41；权威 OOM 检查是 `/sys/fs/cgroup/memory.events` 中的 `oom_kill` 计数器）。
- GPU SM% 固定低位而 python 线程风暴占满核心 → vCPU 切片上的**intra-op 线程过载**（`references/gotchas_universal.md` U40；将 `OMP_NUM_THREADS` 上限设为 cgroup 配额）。

通用陷阱（静默同步、CRLF、运行中脚本覆写、inode 上限）在此不重复 — 参见 `references/gotchas_universal.md`（`grep -in '<keyword>' references/gotchas_universal.md` 跳转）。

---

## §7 跨智能体主机的监控（可移植性映射）

四层是主机无关的；只有**哪个原语运行 L2/L3**随主机变化。两条规则将整个架构移植到 Codex / Cursor / Trae / 任何 Agent-Skills 主机：

**规则 1 — 持久层不需要智能体。** L1（机器自完成 + `touch` 标记）加上机器在 `&&` 链末端**推送自己的通知** — 一个 `curl` webhook / email / 一个 `huggingface-skills:huggingface-trackio` 告警 — 在每个主机上都有效，因为它完全运行在租赁机器上。在没有后台/调度器原语的主机上，这*就是*监视器；智能体只是在下一个回合拉取结果。

**规则 2 — 云调度器无法到达租赁机器（§5），在任何主机上。** 每个主机的托管自动化在隔离沙箱中运行，没有本地 SSH 密钥或网络，所以它无法 ssh 你的机器（且密钥绝不能放入其中 — 密钥泄漏）。仅用云 cron **重新唤醒智能体**或**轮询托管 tracker**，永不探测机器。到达机器的轮询必须使用主机的**本地/会话**运行器（持有你的 SSH 密钥），或是 L1 机器循环。

| 智能体主机 | 本地运行器 — 到达机器（L3） | 循环 / loop（L2） | 云 cron/自动化 — 仅重唤醒 / tracker | 前台/回合限制 |
|---|---|---|---|---|
| **Claude Code** | `run_in_background`（分离 + 退出时通知）；`Monitor` 工具 | `/loop` + `ScheduleWakeup`（间隔或自步） | `/schedule`（cron 云智能体） | 约 600 秒前台 |
| **OpenAI Codex** | Codex Cloud 后台任务（异步、并行） | 调度自身唤醒的线程 | **Automations** — cron 语法，结果 → 审查队列 | 每云任务 |
| **Cursor** | Background Agents（异步） | — | **Automations** — cron（每小时/每天/每周）+ 事件触发 | 每智能体 |
| **Trae** (ByteDance) | Agent / `trae-agent` CLI 无人值守运行；CI/CD | 通过 CI/CD 管道 | **未发现原生 cron** → 外部 cron / CI-CD，或依赖规则 1 | 每次运行 |
| **通用 / 无** | 任何本地后台等价物（否则无） | 回合限制下的 shell `while` 循环 | 无 | 宿主回合限制 |

> **不在表中的主机**（Gemini CLI、VS Code / Copilot、Goose、Kiro、…）采用**通用**行，直到它们暴露持有你 SSH 密钥的本地循环运行器 — 在此之前，布线**规则 1**（机器自推送）并让智能体在下一个回合拉取。

**绑定层：** L1 到处不变（机器上）。将 **L2** 绑定到主机的本地循环运行器*如果*它到达机器，否则绑定到机器自身的 `cron`/`at` + 推送（规则 1）。将 **L3** 绑定到主机的本地后台运行器，每次恢复后重新武装一个。当主机仅提供云自动化（或无）时，**不要承诺智能体侧的机器轮询** — 布线规则 1 并让智能体在下一个回合拉取（§0 推论：信任产物，不是静默）。

主机能力已验证 2026-06：Codex Automations (cron) + Cloud 后台任务 — `developers.openai.com/codex/app/automations` + `/codex/cloud`；Cursor Automations (cron + 事件触发) + Background Agents — `cursor.com/docs/cloud-agent/automations`；Trae Agent / `trae-agent` CLI + CI/CD，未发现原生 cron — `docs.trae.ai/ide` + `github.com/bytedance/trae-agent`。
