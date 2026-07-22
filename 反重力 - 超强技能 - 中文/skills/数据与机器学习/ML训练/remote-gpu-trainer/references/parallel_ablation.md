# 并行消融扇出 — FS共享部署、隔离写路径、对账

跨实例/队列并行运行 N 个消融单元而不损坏共享状态，然后在任何拆除之前对账并重新验证每个单元。机制是**每个单元一个作业、隔离写路径**；纪律是 **`superpowers:dispatching-parallel-agents` 的独立性谓词 + 对账**。**必需：** `superpowers:dispatching-parallel-agents` 和 **必需：** `superpowers:verification-before-completion`。

快速跳转：`grep -in <keyword> references/parallel_ablation.md`。

## 目录

1. 扇出模型（每单元一个作业）
2. FS共享封装部署（放置一次，运行中永不修改）
3. 独立性谓词（隔离写路径 = git worktree 的类比）
4. 可移植作业请求（描述一次，在任何 Profile 上运行）
5. 队列文件格式 + 通过 `start_index` 恢复
6. 扇出后强制对账 + 完整重验证
7. 陷阱

---

## 1. 扇出模型

并行性来自**在多个实例上同时运行多个队列** — 绝不是在一个实例内并行作业（每实例串行执行保持内存可预测，防止磁盘争用）。工作单元是**消融单元**：一行 `(cfg, task, epochs)` → 一次 `run_one` 调用 → 一个隔离的输出目录。

```
共享 FS: /path/to/shared/run_one.sh, run_queue.sh   （一个版本，所有实例读取它）
实例 A  tmux ──> run_queue.sh queueA.txt ──> 单元 a1 ──> 单元 a2 ──> ...
实例 B  tmux ──> run_queue.sh queueB.txt ──> 单元 b1 ──> 单元 b2 ──> ...
实例 C  tmux ──> run_queue.sh queueC.txt ──> 单元 c1 ──> ...
                                       每个单元仅写入自己的 /ckpt/<name>/ + FS/<name>/
```

按成本而非数量将 N 个单元分配到队列文件（每个实例一个）— 将长单元（检测 50 epochs）路由到更快/空闲的实例，使队列近乎同时完成。

---

## 2. FS共享封装部署

在跨实例共享文件系统上放置 `run_one`/`run_queue` 的**单份副本**（`profiles/<platform>.md` 的 STORAGE 节命名了挂载点；AutoDL 上是 FS 层，RunPod 上是 Network Volume，裸机上是用 NFS/`rsync` 同步的目标）。每个实例读取**相同版本** — 没有每实例漂移，没有"A 上修了但 B 没有"。

**回顾原则 #6 — 永远不要在运行中的作业下修改输入。** 运行中的队列按字节偏移持有 `run_queue.sh`/`run_one.sh`；中途覆盖任何一个会让 bash 读到另一个文件的中间并重新执行代码块（重复运行、队列卡死）。因此：

- **在启动任何队列之前部署封装。** 将 FS 副本视为扇出生命期内的不可变对象。仅在不被读取时编辑（每个实例上 `pgrep -af run_queue.sh` 为空）。
- **运行中途向队列*文件*追加是安全的**（流式读取每次迭代会重新读取）；编辑*脚本*则不行。新单元 → 追加一行，或启动新的队列文件。
- 必须传达到运行中作业的修复 → **对文件名版本化**（`run_one.v2.sh`），排空旧队列，将新队列指向新文件。永远不要 `scp` 覆盖正在被运行中队列读取的路径。

FS 副本也是持久安全网：`run_one` 的成功后步骤将 `best.pth` + 指标 + 日志同步到 `FS/<name>/`，因此已释放/死亡的实例仍会在 FS 上留下其单元的结果。

---

## 3. 独立性谓词

**必需：** `superpowers:dispatching-parallel-agents` — 仅对工作单元不共享可变状态的任务扇出。此处的谓词是具体的：**每个单元写入自己的输出目录，不写其他任何地方。** 每作业输出目录是 **git worktree** 的平台类比 — 一个隔离的工作空间，一个智能体的写入永远不会与另一个的冲突。

通过将每个单元的写入路由到名称作用域路径来维持谓词：

| 写入目标 | 隔离键 | 设置方式 |
|---|---|---|
| checkpoints | `<ckpt_root>/<name>/` | `training.checkpoint_dir` 覆盖（每个 `<name>`） |
| FS 最终副本 | `FS/final_ckpts/<name>/` | `run_one` 成功后同步 |
| tracker 运行 | `group=<task>_<cat>`，唯一运行名 | `wandb.group` / `wandb.tags` 覆盖 |
| 每单元日志 | `<name>.log` | `run_queue` 逐行日志 |

**永远不要在共享可变输出上扇出。** 两个单元写 `latest.pth`、同一个 `checkpoint_dir`、或一个 tracker 运行 id = 谓词禁止的精确共享状态违规 — 它会产生静默交叉的 checkpoint 和无法归属的指标，事后对账也无法理清。`<name>` 从 cfg 1:1 派生，因此不同 cfg → 不同路径自动成立；**两个队列行绝不能共享同一个 `<name>`。**

读取共享的内容（不可变的封装、数据集、基础镜像）是可以的 — 谓词仅禁止共享**可变**状态。

---

## 4. 可移植作业请求

一次描述一个 sweep，使*同一*扇出可以在任何 Profile 上运行（启动器根据 `profiles/<platform>.md` 解析；Profile 提供路径/动词，作业提供工作 — 见 `profiles/_schema.md`）：

```yaml
resources:
  gpu: {name: A100, count: 1, memory: 24GB+}    # 约束条件，不是平台 SKU
  disk: 100GB                                    # ckpt_size × 每实例单元数 + scratch
candidates: [autodl, china, runpod]              # 有序回退 → 描述一次，随处运行
run: "bash run_queue.sh queue.txt"               # 每实例入口点
```

每实例磁盘预算 = `ckpt_size × 此队列单元数 + scratch`（原则 #5）。在 Phase 0 预先计算；磁盘预算不足的扇出会使每个队列*最后*的单元失败，而不是前面的。

---

## 5. 队列文件格式 + 恢复

每行一个消融单元，空格分隔（`while IFS=' ' read -r cfg task epochs`）：

```
<cfg_path> <task> [epochs]
```

- `cfg_path` — 相对于 repo 根目录的 yaml 文件；其基名是单元的 `<name>`（隔离键）。
- `task` — reconstruction / segmentation / detection（或其他受支持的任务）— 设置 tracker group/tags。
- `epochs` — 可选整数；省略 → 封装默认值（例如 `20`）。可选的第 3 字段允许一个队列混合每任务预算（检测 50，重建/分割 20）。

```
configs/experiments/ablation/recon/baseline.yaml      reconstruction 20
configs/experiments/ablation/det/baseline.yaml        detection      50
configs/experiments/ablation/seg/no_aug.yaml          segmentation
```

**通过 `start_index` 恢复。** 在单元 k 处被杀死的队列（SSH 断开、抢占、OOM）通过 `bash run_queue.sh queue.txt <k>` 恢复 — 它跳过前 k 行然后继续。这是原则 #8（幂等恢复）的队列级形式；结合每单元的启动时 checkpoint 加载，半完成的单元可从单元内恢复，而非从头开始。保持 `start_index` 与队列文件对齐：追加行是安全的，**重新排序或删除前面的行会移动每个索引** — 仅追加。

---

## 6. 扇出后强制对账 + 完整重验证

**必需：** `superpowers:dispatching-parallel-agents`（对账）和 **必需：** `superpowers:verification-before-completion`（任何成功声明前需证据）。当队列报告完成时，观察者的"完成"是一个**声明**（原则 #3），不是事实 — 一个单元可能在静默失败的同步上报告成功、OOM 中途写入、或因为实例死亡而从未运行过。

在任何拆除之前对账并重新验证**每个单元** — 这是硬门控，不是抽样检查：

1. **花名册。** 从所有队列文件枚举期望的单元 `<name>` 集合（事实来源花名册）。
2. **对账。** 对每个 `<name>`，确认 `FS/final_ckpts/<name>/` 存在并包含 `best.pth` + 指标 + 日志。列出差异：缺失、零字节、或重复 `<name>` 冲突（漏网的谓词违规 — 见陷阱）。
3. **加载重验证。** 在持久副本上运行 `scripts/verify_local.py` — *加载*每个 checkpoint 和指标文件。"文件存在" / "日志说已同步"不是证据；加载成功才是（原则 #3，`verifying-dl-experiments` 边界负责判断*数值*是否真实 — **必需：** `verifying-dl-experiments`）。
4. **修复，不要盲目重试。** 每个缺失/失败的单元 → 分类原因，然后在活跃实例上通过 `start_index` 重新启动**完全相同的配置**（原则 #7），或将其行追加到新队列。不要修改某个单元的配置使其通过 — 那会破坏可比性。

只有当花名册 100% 对账完成且每个单元加载通过后，拆除铁律才解锁（SKILL.md Phase 5）：在结果拉取到本地且通过加载验证且用户批准影响成本的操作之前，不执行 `release`/`terminate`/`destroy`。

---

## 7. 陷阱

**两个单元共享同一个 `<name>` → 交叉的 checkpoint，无法归属的指标。**
症状：一个单元的 `best.pth` 被覆盖，tracker 运行出现混合曲线，对账发现 N 个单元只有 N-1 个输出目录。 → 根因：独立性谓词违规 — 两个队列行映射到相同的隔离键（相同的 cfg 基名 / 手动设置的相同 `checkpoint_dir`）。 → 修复：启动前强制每行 `<name>` 唯一（cfg→`<name>` 映射必须是单射）；冲突时重命名一个 cfg 并重跑两者 — 交叉的输出事后无法拆分。

**扇出期间编辑 FS 封装 → 跨实例重复/卡死的单元。**
症状：在 FS 上对 `run_queue.sh`/`run_one.sh` 做"快速修复"后单元重复运行或队列卡死。 → 根因：原则 #6 — 运行中的 bash 按字节偏移持有脚本；覆盖共享副本同时损坏所有读取者。 → 修复：将 FS 封装视为扇出生命期内的不可变对象；对文件名版本化并重新指向新队列；仅在所有实例上 `pgrep -af run_queue.sh` 为空时才编辑。

**队列报告"全部完成"但某个单元从未运行。**
症状：花名册有 N 个单元，FS 上少于 N 个；存活日志中无错误。 → 根因：实例死亡（释放、抢占、主机故障），其队列的"完成"从未发出 — 没有失败不等于成功（原则 #3）。 → 修复：根据**花名册**对账，而非观察者的最后状态；在活跃实例上用 `start_index` 重新启动缺失的单元。

**队列编辑后 `start_index` 恢复到错误的单元。**
症状：恢复时跳过或重跑错误的行。 → 根因：一行被插入/删除/重排，移动了后续所有索引。 → 修复：运行中的队列文件仅追加；要丢弃单元，注释掉（不要删除）以保持索引稳定，或为剩余部分启动新的队列文件。

> 通用陷阱（`pkill` 时的 SSH 断开、CRLF、cgroup OOM、静默同步、共享 FS 上多小文件 eval 输出的 inode 耗尽）在此**不**重复 — 见 `references/gotchas_universal.md`。共享 FS inode 压力（原则 #5）在扇出期间最为严重，此时 N 个单元同时向一个 FS 写入 eval 产物。
