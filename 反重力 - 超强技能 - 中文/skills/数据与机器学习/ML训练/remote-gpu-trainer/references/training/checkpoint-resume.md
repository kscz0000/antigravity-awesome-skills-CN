# 正确的检查点与幂等恢复 — 完整状态、原子写入、分片检查点、框架 API

让训练作业在任何终止后从**确切停止位置**恢复 — 而非"重新加载权重然后静默重启 epoch"。本层负责*机制*：保存什么完整状态、如何无损写入、如何无条件加载，以及框架特定的旋钮（FSDP / DeepSpeed / HF Trainer / Accelerate / Lightning），加上那些让作业看起来已恢复但实际静默丢失进度的恢复 **bug**。**verifying-dl-experiments**（**必需**）负责*恢复后的数值是否正确* — 例如证明 step/epoch/loss 确实继续而非重置，是其可复现性检查在此处的应用。Spot/抢占的*频率*（何时 + 多久一次，Young/Daly）位于 `references/spot-resilience.md`（**必需**，任何可中断/spot 层级）— 本文件是每个检查点的*内容和正确性*；那个文件是*时机*。

跳转：`grep -in '<keyword>' references/training/checkpoint-resume.md`（例如 `atomic`、`rename`、`scaler`、`ema`、`sampler`、`fsdp`、`sharded`、`zero_to_fp32`、`dcp`、`resume_from_checkpoint`、`save_state`、`ckpt_path`、`save_total_limit`、`reshuffle`）。

## 目录

- **契约** — C1 完整状态列表 · C2 原子写入 · C3 无条件加载最新 · C4 持久位置
- **分片检查点（多 GPU）** — C5 FSDP-FULL_STATE_DICT-rank0-OOOM · C6 FSDP-SHARDED_STATE_DICT · C7 DCP-(dcp.save/load) · C8 DeepSpeed-ZeRO-dir+zero_to_fp32
- **框架 API** — C9 HF-Trainer-resume_from_checkpoint+save_total_limit · C10 Accelerate-save_state/load_state · C11 Lightning-ModelCheckpoint+ckpt_path
- **恢复 BUG** — C12 epoch 重启 · C13 数据重排/顺序 · C14 LR 计划重置 · C15 scaler 未恢复 · C16 EMA 未保存 · C17 save_total_limit 删除最佳 · C18 strict-load 键不匹配
- **指针** — 保存时磁盘满 → gotchas_universal.md U6 · 静默同步 → U33 · keepable-policy/save_top_k → verifying-dl-experiments（技能）· 频率/Young-Daly → spot-resilience.md

---

## 契约

### C1 — 只恢复权重的检查点不是恢复 — 保存完整训练状态

**症状**：恢复"成功"（无崩溃）但 loss 跳升、准确率倒退、或训练比不间断运行需要更多 epoch — 因为恢复静默重启了 epoch、重置了优化器动量、重新打乱了数据。

**根因**：`torch.save(model.state_dict())` 只捕获*权重*。优化器动量/方差、LR 调度器位置、epoch/step 计数器、RNG 状态、AMP scaler 和 dataloader 位置全部丢失，所以重启的运行是一条*不同的*轨迹，而非延续。

**修复**：每个检查点必须携带完整状态（PyTorch 教程 [saving multiple / general checkpoint](https://docs.pytorch.org/tutorials/recipes/recipes/saving_and_loading_a_general_checkpoint.html)；spot-resilience §3 列表）：

| 必须保存 | 丢失它为何破坏恢复 |
|---|---|
| model `state_dict` | 权重（显而易见） |
| optimizer `state_dict` | Adam m/v 动量 — 丢失 = 冷启动优化器（C12） |
| LR-scheduler `state_dict` | 基于 step 的 LR 位置 — 丢失 = 重置计划（C14） |
| `epoch` **和** 全局 `step`/iteration | 恢复到精确位置，而非 epoch 起始（C12） |
| RNG 状态：Python `random`、NumPy、`torch`、**CUDA**（`torch.cuda.get_rng_state_all()`） | 重启后可复现的增强/dropout 流 |
| dataloader / sampler 位置 | 使下一个 batch 是*下一个*未见过的，而非重新打乱（C13） |
| AMP `GradScaler` `state_dict` | loss-scale + 增长追踪器 — 丢失触发 inf-scale 停滞（C15） |
| EMA / SWA 影子权重（如果使用） | EMA 拷贝通常是评估用的 — 丢失 = 在错误权重上评估（C16） |
| 目前最佳指标 + `best.pth` 选择状态 | 使"最佳"在重启后存活而非重置 |

组装此字典的可运行原子骨架在 `references/spot-resilience.md` §5 — 不要重复；本表是*清单*，那个是*代码*。

### C2 — 原子写入：tmp → fsync → os.replace（写入中途被杀会损坏朴素保存）

**症状**：抢占/OOM 后，`latest.pth` 被截断/零字节或 `torch.load` 抛出 `RuntimeError: PytorchStreamReader failed reading zip archive`；留下一个 `latest.pth.tmp`。

**根因**：原地覆盖 `latest.pth` **不是**原子的 — 写到一半被杀会留下损坏文件且（如果是唯一检查点）零个好的。`torch.save` 本身*不会* fsync。

**修复**：写入临时文件，强制刷盘，然后原子重命名（POSIX `rename`/`os.replace` 在**同一文件系统**上是原子的）：
```python
tmp = ckpt_path + ".tmp"
with open(tmp, "wb") as f:
    torch.save(state, f); f.flush(); os.fsync(f.fileno())   # 字节在交换前落盘
os.replace(tmp, ckpt_path)                                   # 全有或全无；直到此返回前保留旧的
```
保留前一个 `latest.pth` 有效直到重命名返回（任何时刻被杀都留下一个完整文件）。`os.replace`（而非 `os.rename`）在 Windows 本地测试路径上也能工作。完整方案 + 理由：`references/spot-resilience.md` §3。保存*期间*磁盘满是另一种失败，同样留下 `.tmp` → `references/gotchas_universal.md` U6（预预算 + 修剪 `latest`，保留 `best`）。

### C3 — 启动时无条件加载最新 → 幂等恢复

**症状**：重新启动从零开始，因为恢复被 `--resume` 标志门控而启动封装器忘记传递；或两条代码路径（全新 vs 恢复）分叉。

**根因**：使恢复*可选*意味着通用重启（spot 恢复、SSH 断连重启、队列重试）从零重训。分叉的"首次启动"代码路径也会偏离恢复路径。

**修复**：一条代码路径：如果存在最新检查点则加载，否则全新开始 — 使**相同的启动命令**无论运行多少次都收敛到相同终态。这就是原则 #7 的"重试相同配置"真正*恢复*而非重启，也是 SSH 断连 / Slurm-walltime / K8s-reschedule / spot-preemption 下的通用脊骨（原则 #8）。骨架：`references/spot-resilience.md` §3（`load_latest_if_any`）。

### C4 — 检查点保存到平台的持久位置，而非本地暂存

**症状**：managed-spot 替换（或 `terminate`/`destroy`）后恢复找不到检查点 — 机器*全新启动*且唯一副本在死亡实例的本地磁盘上。

**根因**：替换节点是干净的；不在云桶/网络卷/共享文件系统上的任何东西都消失了（原则 #4 — 知道什么在 stop vs destroy 后存活）。

**修复**：将检查点写入配置文件的持久挂载（`profiles/<platform>.md` §8 中的 `DURABLE_DIR`），或在检查点定时器上镜像 本地→持久。最大的可移植性陷阱是假设本地磁盘存活 — 见每个配置文件的 STORAGE 生存矩阵和 SKILL 快速参考表。在实际复制结果上门控同步，绝不无条件 `echo synced` → `references/gotchas_universal.md` U33。

---

## 分片检查点（多 GPU）

### C5 — FSDP `FULL_STATE_DICT` 在 rank 0 聚合大模型时 OOM

**症状**：FSDP 作业训练正常但在**第一个检查点时崩溃**，rank 0 上 CUDA OOM；模型大于单张 GPU。

**根因**：`StateDictType.FULL_STATE_DICT` 将每个分片 all-gather 到**一个 rank** 上组装未分片字典。对于仅因分片才放得下的模型，在 rank 0 上物化整个字典超出该 GPU 的 VRAM。

**修复**：取完整（合并的）字典时，卸载到 CPU 并仅在 rank 0 上构建 — `FullStateDictConfig(offload_to_cpu=True, rank0_only=True)`。这逐个 all-gather 参数，在 rank 0 上逐个卸载到 CPU，所以峰值 GPU 内存保持有限，非 rank-0 工作进程完全跳过 GPU→CPU 拷贝
（[HF Accelerate FSDP 指南](https://huggingface.co/docs/accelerate/en/usage_guides/fsdp)，
[Lightning issue #11207](https://github.com/Lightning-AI/pytorch-lightning/issues/11207)）。完整字典仅在能放入 CPU RAM 时可行；超过此范围，使用分片（C6）。仅在**最后**保存完整字典用于可移植的单文件产物；训练*期间*以分片形式检查点。

### C6 — `SHARDED_STATE_DICT`：每个 rank 保存自己的分片（无 gather，无 rank-0 OOM）

**症状**：需要检查点一个大到即使在 CPU 上也无法合并的模型，或想要快速恢复到*不同* world size 的重新分片。

**根因**：`FULL_STATE_DICT` 本质上是单 rank 物化；它不扩展且无法重新分片。

**修复**：使用 `StateDictType.SHARDED_STATE_DICT` — 每个 rank 只写入自己的分片，所以没有 all-gather 且没有 OOM，每个 rank 的文件并行加载回。搭配 Distributed Checkpoint（C7），这是分片保存/加载的生产路径，支持**重新分片**（在不同 GPU 数量上恢复）。权衡：分片检查点是*N 个文件的目录*，不是单个 `.pth` — 转换为完整字典用于导出/推理（C7 的 `get_model_state_dict`，或 DeepSpeed 类比 C8）。

### C7 — Distributed Checkpoint (DCP)：用于 FSDP/分片模型的 `dcp.save` / `dcp.load`

**症状**：手工管理 FSDP state-dict 上下文管理器脆弱、缓慢，且在 save 和 resume 之间 world size 变化时出错。

**根因**：`torch.save` 产生单个文件，没有分片或 FQN 重映射的概念；手动切换 `FSDP.state_dict_type` 容易出错。

**修复**：使用 `torch.distributed.checkpoint`（DCP），当前 PyTorch 2.x 分片检查点 API
（[DCP 方案](https://docs.pytorch.org/tutorials/recipes/distributed_checkpoint_recipe.html)，
[2.12 参考](https://docs.pytorch.org/docs/2.12/distributed.checkpoint.html)）。**保存**：用 `torch.distributed.checkpoint.state_dict` 中的 `get_state_dict(model, optimizer)` 获取规范字典，然后 `dcp.save(state_dict, checkpoint_id=DIR)` — 它**并行写入每个 rank ≥1 个文件**并自动管理 FQN 映射。**加载**：先分配模型，然后 `dcp.load(state_dict, checkpoint_id=DIR)`（**原地**加载且**自动重新分片**到当前 world size），然后 `set_state_dict(...)`。DCP 对任何分布式模型都优于 `torch.save`，因为它跨 rank 分片写入（无 rank-0 gather，C5）并在加载时重新分片。对于单个可移植推理文件，离线转换：`torch.distributed.checkpoint.format_utils.dcp_to_torch_save(DIR, "out.pt")`（或 CLI `python -m torch.distributed.checkpoint.format_utils dcp_to_torch DIR out.pt`）。

### C8 — DeepSpeed ZeRO：每次保存一个检查点*目录* + `zero_to_fp32.py` 合并

**症状**：`model_engine.save_checkpoint(dir)` 写入一个包含 `mp_rank_*` / `zero_pp_rank_*` 文件的*文件夹*，不是 `.pth`；将权重加载到普通（非 DeepSpeed）模型用于推理失败。

**根因**：ZeRO 在各 rank 间**分区**优化器状态（stage 1）、梯度（stage 2）和参数（stage 3）；磁盘上的检查点本质上是跨每个 rank 的文件分片的 — 不是单个 fp32 模型。

**修复**（[DeepSpeed 模型检查点](https://deepspeed.readthedocs.io/en/stable/model-checkpointing.html)，
[ZeRO 教程](https://www.deepspeed.ai/tutorials/zero/)）：

- **保存/恢复训练** — `model_engine.save_checkpoint(save_dir, tag)` /
  `model_engine.load_checkpoint(save_dir, tag)`。**所有 rank 必须调用两者**（它们是集合操作；仅 rank-0 调用会死锁/损坏）。完整往返分片的 optimizer+param 状态。
- **导出单个 fp32 模型** — DeepSpeed 自动在检查点目录中放入 `zero_to_fp32.py`；运行
  `python zero_to_fp32.py <checkpoint_dir> pytorch_model.bin`，或在进程内
  `from deepspeed.utils.zero_to_fp32 import get_fp32_state_dict_from_zero_checkpoint(dir)` /
  `convert_zero_checkpoint_to_fp32_state_dict(...)` / `load_state_dict_from_zero_checkpoint(model, dir)`
  （最后一个返回的模型**不能继续训练**除非重新初始化）。合并后的文件不再需要 DeepSpeed。对于 ZeRO-3，设置
  `"zero_optimization": {"stage3_gather_16bit_weights_on_model_save": true}` + `engine.save_16bit_model(dir)`。

---

## 框架 API

### C9 — HF Trainer：`resume_from_checkpoint` + `save_total_limit`（以及它实际保存了什么）

**症状**：假设 `Trainer.save_model()` 是一个恢复点（它只保存*权重*）；或重新启动因未传 `resume_from_checkpoint` 而从 step 0 重训；或磁盘被 `checkpoint-*` 目录填满。

**根因**：`save_model` ≠ 训练检查点。真正的 Trainer 检查点目录（`checkpoint-<step>`）包含模型**加上** `optimizer.pt`、`scheduler.pt`、`rng_state.pth`、`trainer_state.json` 和 AMP `scaler.pt` — 完整状态。没有 `resume_from_checkpoint` 运行从冷启动开始。

**修复**（[Trainer 文档](https://huggingface.co/docs/transformers/main/en/main_classes/trainer)）：
`trainer.train(resume_from_checkpoint="path/to/checkpoint-1500")` 恢复该精确目录；
`resume_from_checkpoint=True` 自动查找 `args.output_dir` 中的**最后**一个检查点（幂等写法，C3；代码中 `trainer_utils.get_last_checkpoint(output_dir)` 查找）。`save_strategy="steps"` +
`save_steps=N`（或 `"epoch"`）设置频率；**`save_total_limit=k`** 只保留 `k` 个最近的 `checkpoint-*` 并**删除 `output_dir` 中更早的** — 内置磁盘预算旋钮（与 `references/gotchas_universal.md` U6 配对）。`load_best_model_at_end=True` + `metric_for_best_model` + `greater_is_better` 在最后重新加载最佳检查点**并**保护它不被 `save_total_limit` 删除（C17）。

### C10 — Accelerate：`accelerator.save_state(dir)` / `load_state(dir)` + dataloader 跳过

**症状**：自定义（非 Trainer）Accelerate 循环恢复时优化器/scaler 是冷的，或 LR 调度器重置，或重放已经见过的 batch。

**根因**：只保存 `accelerator.get_state_dict(model)` 丢弃了 optimizer/scaler/RNG；且 epoch 中途的恢复从 batch 0 重新迭代 dataloader。

**修复**（[Accelerate 检查点指南](https://huggingface.co/docs/accelerate/en/usage_guides/checkpoint)）：
`accelerator.save_state(output_dir)` 一次调用保存模型、优化器、**GradScaler** 和 RNG 生成器；`accelerator.load_state(output_dir)` 恢复所有内容（对象必须来自*同一脚本*）。LR 调度器（及任何有 `state_dict`/`load_state_dict` 的对象）**必须**先注册 — `accelerator.register_for_checkpointing(my_scheduler)` — 否则不会保存并重置（C14）。对于 epoch 中途恢复，在第一个恢复的 epoch 上用 `accelerator.skip_first_batches(train_dataloader, N)` 跳过已消费的 batch，然后回退到完整 dataloader（C13）。
`ProjectConfiguration(automatic_checkpoint_naming=True, total_limit=k)` 提供滚动 `checkpoints/checkpoint_<n>` 目录及内置限制。

### C11 — Lightning：`ModelCheckpoint` + `trainer.fit(ckpt_path=...)`（不要使用 `resume_from_checkpoint`）

**症状**：旧教程的 `Trainer(resume_from_checkpoint=...)` 被忽略/已弃用；或 `save_top_k` 悄悄删除了恢复所需的检查点。

**根因**：`resume_from_checkpoint` 移到了 `fit(ckpt_path=...)`（自 1.x 起弃用）。Lightning `.ckpt` 是完整转储 — epoch、全局 step、LightningModule `state_dict`、**所有**优化器 + LR-scheduler 状态、回调状态、循环状态和 16 位缩放因子（AMP）（[Lightning 检查点基础](https://lightning.ai/docs/pytorch/stable/common/checkpointing_basic.html)）。

**修复**：
- 配置 `ModelCheckpoint(dirpath=..., monitor="val_loss", mode="min", save_top_k=k, save_last=True)`；
  用 `trainer.fit(model, datamodule, ckpt_path="path/to/last.ckpt")` 恢复，或
  `ckpt_path="last"` 自动选择 `save_last=True` 文件（幂等写法，C3）。最佳/最后路径从 `cb.best_model_path` / `cb.last_model_path` 读回。
- `save_top_k` 只保留按 `monitor` 排名的 k 个最佳；**始终设置 `save_last=True`** 这样即使最近 step 不是 top-k 指标也存在恢复目标（否则恢复可能没有最近的检查点）。
  通过模块或有状态回调的 `on_save_checkpoint` / `on_load_checkpoint` 添加自定义状态（EMA，C16）。Lightning 的 DeepSpeed 策略写入 ZeRO 目录 — 用 `lightning.pytorch.utilities.deepspeed.convert_zero_checkpoint_to_fp32_state_dict` 转换（C8 类比）。

---

## 恢复 BUG（看起来已恢复，静默丢失进度）

这些是"没有报错但结果错误"的陷阱 — 用 `verifying-dl-experiments` 可复现性检查（**必需**）确认修复：运行中杀掉，重新启动*相同*命令，验证 step/epoch/loss **继续**而非重置。

### C12 — Epoch/step 从 0 重启尽管"正在恢复"

**症状**：追踪器显示第二次运行从 epoch 1 开始；总训练 epoch 超出计划；LR warm-up 重放。（远程运维版本 — tmux 脚本中途重新执行 — 是 `references/gotchas_universal.md` U2。）

**根因**：循环是 `for epoch in range(total_epochs)` 带硬编码的 `0` 起始；保存的 `epoch`/`step` 从未被读回，或保存了但未用于播种范围。

**修复**：`start_epoch, start_step = load_latest_if_any(...)` 然后 `for epoch in range(start_epoch, total_epochs)` 并从 `start_step` 播种 step 计数器。计数器**必须**在检查点中（C1）*且*在加载时被消费。

### C13 — 恢复后数据重新打乱 / 重复相同顺序

**症状**：恢复重新显示已见过的样本（更糟的是，即使不恢复每个 epoch 也是*相同* batch），损害收敛或造成泄露。

**根因**：两个不同的 bug。(a) 恢复从 batch 0 重启 epoch 而不跳过已消费的 batch。(b) `DistributedSampler` 从内部 epoch 播种其打乱，默认为 0 且除非每个 epoch 调用 `sampler.set_epoch(epoch)` 否则永远如此 — 所以每个 epoch（和每次恢复）产生**相同**顺序
（[PyTorch #31771](https://github.com/pytorch/pytorch/issues/31771)，
[DistributedSampler 文档](https://docs.pytorch.org/docs/stable/data.html#torch.utils.data.distributed.DistributedSampler)）。

**修复**：在每个 epoch 顶部调用 `train_sampler.set_epoch(epoch)`（恢复时恢复 epoch 计数器使打乱流继续）。对于 epoch 中途恢复，快进已消费的 batch（`accelerator.skip_first_batches`，C10）或使用可恢复/有状态 sampler（`torchdata` `StatefulDataLoader`），其偏移量在检查点中（C1）。

### C14 — LR 计划重置（cosine 重启，warm-up 重放）

**症状**：LR 曲线从初始/warm-up 值重启；最终 LR 错误；cosine decay 永远达不到其底部。

**根因**：LR 调度器的 `state_dict`（其 `last_epoch`/step 计数器）未被保存或未被恢复。使用 Accelerate 时，调度器未被 `register_for_checkpointing`（C10）。

**修复**：保存 `scheduler.state_dict()` 并在恢复时调用 `scheduler.load_state_dict(...)`（C1）。注意：基于 optimizer step 推进的 step-based 调度器必须恢复**step**而非 epoch — 仅恢复 `epoch` 会导致计划偏少/偏多。

### C15 — AMP `GradScaler` 未恢复 → "No inf checks were recorded" / scale 停滞

**症状**：恢复混合精度运行时抛出 `AssertionError: No inf checks were recorded for this optimizer`，或训练停滞/NaN 因为 loss-scale 弹回默认值并重新进入 scale-search。

**根因**：`GradScaler` 持有动态状态 — `scale`、`growth_factor`、`backoff_factor`、`growth_interval`、`_growth_tracker` — 在训练中演化；丢弃它重置了 scaler
（[PyTorch AMP 方案](https://docs.pytorch.org/tutorials/recipes/recipes/amp_recipe.html)，
[论坛：No inf checks were recorded](https://discuss.pytorch.org/t/resume-training-with-mixed-precision-lead-to-no-inf-checks-were-recorded-for-this-optimizer/115828)）。

**修复**：保存 `scaler.state_dict()`（在迭代中 `scaler.update()` **之后**调用）并在恢复时 `scaler.load_state_dict(checkpoint["scaler"])`。HF Trainer（`scaler.pt`）、Accelerate（`save_state`）和 Lightning（16 位因子）都自动完成 — 这个 bug 咬手写循环。将*非 AMP* 检查点恢复到 AMP 运行没有保存的 scaler → 启动一个**全新** `GradScaler`。

### C16 — EMA / SWA 影子权重未保存 → 恢复后在错误权重上评估

**症状**：恢复前评估（使用 EMA 权重）良好；恢复后评估急剧下降，然后经过很多 step 才恢复 — 因为 EMA 拷贝从原始权重重新开始。

**根因**：EMA/SWA 维护一个*独立的*影子参数集，用于评估/导出；只保存活跃模型 `state_dict` 会丢失它，所以 EMA 从（更嘈杂的）活跃权重重新初始化。

**修复**：在检查点字典中包含 `ema.state_dict()`（和 SWA `AveragedModel` / `swa_scheduler` 状态）（C1）并恢复它。在 Lightning 中，通过 `on_save_checkpoint`/`on_load_checkpoint` 持久化（C11）。这是边界上的*哪些权重正确*问题 — 交叉引用 **verifying-dl-experiments**（**必需**）确认评估的权重是预期的。

### C17 — `save_total_limit` / `save_top_k` 删除了恢复恰恰需要的检查点

**症状**：恢复失败因为目标检查点被自动修剪；或 `load_best_model_at_end` 报错因为最佳检查点被轮转出去了。

**根因**：滚动限制按*时间性*（`save_total_limit`）或按*指标*（`save_top_k`）修剪，两者都不保证保留最新 step 的检查点 — 所以恢复锚点可能是被删除的那个。

**修复**：在 top-k 旁边保留一个显式的 `last`/`latest`（Lightning 中 `save_last=True`，C11；HF 中 `load_best_model_at_end=True` 使 Trainer 在 `save_total_limit` 之外保留最佳检查点）。通用可保留检查点*策略*（保留多少、哪个选择标准、`save_top_k ≤ 3`、修剪 `latest`）由 **verifying-dl-experiments**（**必需**）拥有；磁盘预算后果是 `references/gotchas_universal.md` U6。

### C18 — 恢复时 `load_state_dict` 键不匹配（`module.` 前缀、编译模型前缀）

**症状**：恢复抛出 `Missing key(s)` / `Unexpected key(s) ... module.<name>` 或 `_orig_mod.<name>`，或在切换 DDP/`torch.compile` 开关后 strict load 失败。

**根因**：`DataParallel`/DDP 包装添加 `module.` 前缀，`torch.compile` 给每个键添加 `_orig_mod.`；已包装保存的检查点以未包装方式加载（或反之）在 `strict=True` 下键不匹配。

**修复**：保存**未包装**模块 — `model.module.state_dict()`（DDP）/ `accelerator.unwrap_model(model).state_dict()` / `model._orig_mod.state_dict()`（compiled）— 使检查点与包装器无关。加载时，如存在前缀则去除
（`{k.replace("module.", "").replace("_orig_mod.", ""): v for k, v in sd.items()}`）。调试恢复时保持 `strict=True` 使静默部分加载不能伪装为成功；仅在有意识时放松。

---

## 指针 — 由别处拥有，不要在此复述

- **频率 — 何时/多久**（Young/Daly `W = sqrt(2·mu·C)`，宽限窗口，机会性 SIGTERM 最后刷盘，可运行的原子骨架）→ `references/spot-resilience.md`（**必需**，spot 层级）。
- **保存时磁盘满**（预预算，修剪 `latest`，保留 `best`，`.tmp` 恢复）→ `references/gotchas_universal.md` U6；**静默"已同步"行** → U33；**inode 耗尽** → U7。
- **分片一个放不下的模型**（FSDP 包装策略，ZeRO 阶段，卸载）是*适配*问题 → `references/training/oom-memory.md` M9/M10；本文件负责分片状态的*检查点*。
- **多 rank 保存/加载集合操作 + 弹性重启**（torchrun `--max-restarts` 从检查点恢复）→ `references/training/distributed-launch.md`、`references/multinode.md`。
- **可保留检查点策略 + "恢复后的/最佳数值是否真实"**（选择标准、`save_top_k`、证明 step/epoch/loss 继续）→ **verifying-dl-experiments**（**必需**）。
