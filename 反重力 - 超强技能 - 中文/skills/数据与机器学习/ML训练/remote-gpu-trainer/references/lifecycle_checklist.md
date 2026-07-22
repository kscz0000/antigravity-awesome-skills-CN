# 生命周期检查清单 — 6 阶段操作手册作为按平台检查清单

目的：按平台参数化的、可复制粘贴的复选框操作手册，用于一次远程 GPU 作业，从 Phase 0（环境审计）到 Phase 5（聚合 + 验证 + 拆除）。基底委托给**你的平台 profile**（`profiles/<platform>.md`，`profiles/_schema.md` 中的 8 字段 schema）— 本文件永远不硬编码挂载点、动词或代理。每个阶段以 `SKILL.md` 中可运行的检查结束。

`grep -in <keyword> references/lifecycle_checklist.md` 跳转。

## 目录
- Phase −1 — 一次性设置（复用时跳过）
- Phase 0 — 环境审计
- Phase 1 — SSH + 凭据
- Phase 2 — 封装器 + CPU 冒烟门控
- Phase 3 — 分离启动
- Phase 4 — 持久监控
- Phase 5 — 聚合 + 验证 + 拆除
- 节省成本的拆除表
- 故障处理（内联，任意阶段）

> **如何使用：** 先选择 profile（`SKILL.md` → "选择你的平台 profile"）。任何步骤提到 *profile 数据挂载* / *profile 持久挂载* / *profile 停止计费动词* / *profile 分离原语* 时，从该 profile 的 STORAGE / TEARDOWN / DAEMON 章节读取字面值。跳过已完成的任何阶段。按 ID 引用的通用陷阱位于 `references/gotchas_universal.md` — 此处不复述。

---

## Phase −1 — 一次性设置 *(复用自过去项目时跳过)*

- [ ] **首次接触 — 向用户展示 profile 的"前置告知用户"块**：平台的非显而易见的**便利设施**（一键 SSH 密钥注册、GPU 可用性通知、内置面板）和其**危险时钟**（自动释放/自动删除定时器、stop 仍计费、低余额清除）。不要假设他们知道 — 危险时钟会损失数据或金钱（原则 #10）。
- [ ] 本地 SSH 密钥对存在（`~/.ssh/id_ed25519`）；公钥已在平台注册。
- [ ] 每实例 `~/.ssh/config` 别名，带 keepalive（`ServerAliveInterval`/`ServerAliveCountMax`）— 参见 `references/ssh_transport.md`。
- [ ] 按 profile 配置持久存储（共享 FS / 网络卷 / 持久磁盘），大小 ≥ `ckpt_size × N + buffer`。
- [ ] 保存项目的 env + code 的可复用镜像/快照，如果 profile 支持的话（节省重复冷构建时间 × N 实例）。
- [ ] `.gitattributes` 设置 `*.sh text eol=lf`，这样 Windows 编写的脚本不会带 CRLF（陷阱 U26）。

> **验证：** `ssh <alias> 'echo reachable'` 返回 `reachable` 且持久挂载出现在 profile 的生存矩阵中。

---

## Phase 0 — 环境审计

- [ ] 读取 profile 的 STORAGE 生存矩阵：知道哪个层级在 *stop* vs *destroy* 后存活（原则 #4）。将检查点写入在预期的 *profile 停止计费动词* 后仍存活的层级。
- [ ] 读取 profile 的区域/DC 锁定：如果共享/网络卷是区域范围的，在启动前确认所有实例共享该区域。
- [ ] 实测，不假设：`df -h && df -i <profile 数据挂载>`（inode 先于字节死亡 — 原则 #5），cgroup `cat /sys/fs/cgroup/memory.max`，`nvidia-smi`。
- [ ] `du -sh` 实际挂载上的真实空间占用者（符号链接缓存会隐藏 — 原则 #5），不是假设的目录。
- [ ] 预计算检查点磁盘预算：`ckpt_size × N + scratch`；确认它适合 *profile 数据挂载* 上限。

> **验证：** `nvidia-smi` 显示预期 GPU 且 `df -i <profile 数据挂载>` 未接近 100%。

---

## Phase 1 — SSH + 凭据

- [ ] 按 profile 的 NETWORK 章节设置 SSH 别名/环境变量；注意 SSH 风格（代理/基础 SSH 可能无法 `scp`/`rsync` — 需要直连 TCP；重启时端口可能变化）。
- [ ] 使用预构建镜像/基础作为环境 — 不要在租赁机上 `conda create`（一次性实例例外：镜像即环境）。
- [ ] 通过 **stdin 推送密钥，永远不放到共享/持久 FS 上**（共享 FS 是多项目的）— 模式见 `references/ssh_transport.md`。按环境变量名/文件路径引用凭据，永远不内联密钥。
- [ ] 如果 profile 在 GFW 之后，现在布线中国镜像端点（`references/china-network.md`）；在真实传输使用的**相同路由**上验证速度测试（原则 #7）。

> **验证：** `ssh <alias> 'python -c "import torch;print(torch.cuda.is_available())"'` 打印 `True`。

---

## Phase 2 — 封装器 + CPU 冒烟门控

- [ ] 从 `scripts/`（`run_one.sh.template`、`run_queue.sh.template`）构建幂等的 `run_one` / `run_queue`，按 profile 的脚本覆盖参数化（`DATA_DIR=`、`DURABLE_DIR=`、`PROXY_HOOK=`、`CRED_FILE=`、`SCRATCH=`、`HF_HOME=`、`DETACH=`）。
- [ ] 封装器可恢复：启动时无条件加载最新状态，使相同启动命令恢复而非重启（原则 #8）。
- [ ] 构建每单元队列/配置文件，每单元一个隔离写入路径（无共享可变输出 — 并行消融需要此；`references/parallel_ablation.md`）。
- [ ] **在租用前本地运行便宜的 CPU 冒烟测试** — 1–2 个 batch，logger 关闭，微小 shape；它几乎免费消灭 import/配置/shape/规模 bug（原则 #2）。冒烟*内容* → **verifying-dl-experiments**（必需）。

> **验证：** 冒烟在 2 个 batch 且 logger 关闭时 exit 0，无 Traceback。

---

## Phase 3 — 分离启动

- [ ] 通过 *profile 分离原语*（tmux / `sbatch` / k8s Job / commit）启动 — 在 SSH 断开后存活；确认它是否也在实例重启后存活（profile DAEMON 章节）。
- [ ] 用可恢复传输推送代码/数据（`rsync --partial` 或 `timeout`+恢复循环 — 原则 #7）；永远不要在活跃运行下编辑脚本 — 版本化文件名（原则 #6）。
- [ ] 短暂探测：日志头部 + 进程存活 + 无 traceback，然后**交还控制权**。永远不要阻塞前台 `sleep`（前台 Bash 在 600 秒硬性上限）。

> **验证：** 60 秒内，分离会话存活且第一行日志显示预期的 step/epoch。

---

## Phase 4 — 持久监控

- [ ] 对于超过约 1–2 小时的任何运行，部署**四层架构**（`references/monitoring_patterns.md`）：机上自完成链 + 会话巡逻循环 + 事件哨兵 + 恢复手册。仅会话绑定的监视器随会话消亡（原则 #3）。
- [ ] 使用 `run_in_background`（无持续时间上限，退出时通知；Claude Code 原语 — 其他主机按 `monitoring_patterns.md` §7 映射）等待长时间运行；永远不要前台轮询。永远不要在轮询正则中放未加引号的 `|` — 它读取 stdin 并永远挂起。
- [ ] 监控 `df -i` 趋势（不只是 `df -h`）、cgroup 内存百分比、新的 FINISHED/ERROR/Traceback 标记和快速完成（< 约预期时间的 50% → 可能失败）。
- [ ] 将每个监视器与作业的真实进程/产物协调（`tmux ls`/`squeue`/`pgrep` + 输出 `mtime`）— 监视器自身状态是声明，不是事实真相（原则 #3）。当其作业被取代时拆除监视器。
- [ ] 分类每个失败 → 其固定修复（见下方故障处理）；**永远不要盲目重试**。

> **验证：** 巡逻即使无变化也报告一行状态（证明它活着，不是静默死亡）。

---

## Phase 5 — 聚合 + 验证 + 拆除

- [ ] 运行聚合步骤（`scripts/aggregate_to_fs.sh`，幂等 — 安全重运行）将结果检查同步到 *profile 持久挂载*。**将成功行门控在实际复制结果上** — `cp …; echo synced` 在满/inode 耗尽的 FS 上撒谎（原则 #3，陷阱 U33）。
- [ ] 确认持久挂载有预期产物数量：`ssh <alias> 'ls <profile 持久挂载>/final_ckpts/ | wc -l'`。
- [ ] 将结果拉取到本地（可恢复的按目录 scp/rsync 循环）；对本地目标硬性消毒为 `/path/to/local` — 永远不是真实个人路径。
- [ ] **在拆除前加载并验证每个产物**：`python scripts/verify_local.py /path/to/local/final_ckpts/` → 期望 `OK N/N, errors 0`。重新拉取 + 重新验证任何错误。
- [ ] 记录论文可披露的运行事实：CLI 覆盖、tracker 摘要 URL（托管 tracker 在拆除后存活 — **huggingface-skills:huggingface-trackio**）。传输动词（`hf download --resume`、`hf upload-large-folder`）→ **huggingface-skills:hf-cli**。
- [ ] 仅在此之后执行 *profile 停止计费动词*，在用户明确批准具体影响成本的操作之后。

> **验证：** `verify_local.py` 在任何拆除前报告 100% OK。

> **铁律 — 拆除门控：** 在检查点**已拉取到本地并通过加载验证**，且用户已明确批准影响成本的操作之前，不得 `stop` / `release` / `terminate` / `destroy` / 删除文件。"日志里看起来完成了"不是证据（原则 #3）。在大多数平台上，停止计费的动词是**不可逆的**（删除磁盘）— 确认*更加*重要，而非更少。通用形式是 **superpowers:verification-before-completion**（必需）。

---

## 节省成本的拆除表

停止计费的动词、每个保留什么、以及不可逆性 — 从 profile 的 TEARDOWN 章节绑定平台特定动词。**最大的可移植性陷阱："stop" 很少停止计费，而且做的那个操作通常不可逆**（原则 #4/#9）。

| 操作 | 停止 GPU 计费？ | 什么存活 | 可逆？ |
|---|---|---|---|
| **stop / 关机 (power-off)** | 有时 — 取决于 profile（AutoDL：是，保留磁盘；RunPod/vast：仍计费存储 1–2×） | 按 profile 生存矩阵的磁盘层级 | 是 — 实例可重启 |
| **释放空闲实例** | 是 | 仅持久/共享挂载（数据磁盘消失） | 否 — 实例 + 容器磁盘销毁 |
| **terminate** | 是 | 仅网络/持久卷，如果挂载了的话 | **否 — 不可逆**，磁盘删除 |
| **destroy** | 是 | 机器上什么都没有 | **否 — 不可逆**，完全丢失 |
| **删除持久文件（保留订阅）** | 仅存储滴漏 | 订阅为新数据存活 | 否 — 那些文件没了 |
| **取消持久存储订阅** | 仅存储成本 | 什么都没有 | **否 — 不可逆**，所有持久数据丢失 |

**默认保守计划：** 先停止/释放 GPU 实例（立即节省 $，产物验证本地后低风险）。保留持久存储 1–3 个月直到论文提交。最后取消持久订阅，仅在本地副本验证且用户批准后。

---

## 故障处理 *(内联，任意阶段)*

分类后再反应；重试**相同**配置 — 手动修补一个运行破坏可比性（原则 #7；**verifying-dl-experiments** 拥有这是 bug 还是真实效应的判断权）。

- [ ] **概率性的**（epoch-1 停滞、瞬态 `wandb.init` 抖动、spot 抢占）：用相同配置排队重试，无保护措施。恢复因检查点加载而有效（原则 #8）。
- [ ] **磁盘满**（exit 1 + `iostream` / "No space left"）：修剪 *profile 暂存*（`SCRATCH=` — 周期性检查点、未使用缓存），保留 `best`；如果清理释放不够，**要求扩展磁盘**，永远不要静默缩小实验（原则 #9）。然后重试。
- [ ] **真正的 bug**（CUDA OOM、代码错误、全零度量）：停止，调查代码 — 不要盲目重试。

> 每种的症状 → 根因 → 修复，加上完整目录：`references/gotchas_universal.md`
> （`grep -in <keyword> references/gotchas_universal.md` 跳转）。
