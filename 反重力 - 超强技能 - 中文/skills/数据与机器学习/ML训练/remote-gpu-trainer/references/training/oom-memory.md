# OOM 与模型适配 — 训练期间的 VRAM + 主机内存不足

如何阅读 CUDA OOM 堆栈、理解*什么*占满了显存（参数 vs 优化器 vs 梯度 vs 激活 vs 碎片），并按成本顺序应用修复 — 从免费的缩减批次到 ZeRO-3/QLoRA 分片。本层负责*让训练跑起来并装下*；**verifying-dl-experiments** 负责*结果数字是否正确*。在任何"修复"可能改变科学结论的地方交叉引用它（**必需**）：缩小正在测试的变量、切换精度、改变序列长度。

快速跳转：`grep -in '<keyword>' references/training/oom-memory.md`（例如 `expandable`、`checkpoint`、`zero`、`validation`、`snapshot`、`lora`、`empty_cache`、`longest`、`fragment`）。

## 目录

- **先读** — M1 解剖（VRAM 去了哪里）· M2 阅读 OOM 堆栈 · M3 VRAM-OOM vs 主机内存-OOM
- **按顺序修复** — M4 阶梯（从上往下） · M5 批次/梯度累积 · M6 bf16 混合精度 · M7 激活/梯度检查点 · M8 expandable_segments · M9 FSDP / ZeRO 分片 · M10 CPU/NVMe 卸载 · M11 序列长度/分辨率 · M12 8位与分页优化器 · M13 LoRA/QLoRA
- **特定步骤的 OOM** — M14 首次反向传播 · M15 验证/评估 · M16 最长批次 · M17 第2步（优化器分配）
- **调试** — M18 memory_summary · M19 快照 + 可视化器 · M20 empty_cache 与"内存泄漏"迷思
- **指针** — 主机内存 cgroup-OOM → gotchas_universal.md U9 · VRAM-vs-cgroup → U10 · 僵尸 VRAM → U11

---

## 先读

### M1 — 解剖：VRAM 实际去了哪里（推理能跑的训练 OOM）

训练内存**不只是**权重。对于 **Adam 混合精度**，每个参数：

| 桶 | 字节/参数 | 说明 |
|---|---|---|
| 权重（fp16/bf16 + fp32 主副本） | **6** | 2 B 工作副本 + 4 B fp32 主副本用于稳定更新 |
| 优化器状态（Adam m, v, fp32） | **8** | 动量 4 B + 方差 4 B |
| 梯度（fp32） | **4** | 每个参数一个，反向传播产生 |
| **小计（固定，与批次无关）** | **约 18 B/参数** | 4B 参数的模型 ≈ 72 GB *还没算任何激活* |
| 前向**激活**（为反向缓存） | **可变** | 随 `batch × seq_len × depth × hidden` 缩放；爆发的部分 |
| 临时缓冲区（softmax, matmul scratch） | 峰值 | 单个峰值操作即使稳态能装也会 OOM |

来源：HF model-memory-anatomy (https://huggingface.co/docs/transformers/en/model_memory_anatomy) 给出了 6+8+4 分解和"4B 参数，batch 16 ≈ 85 GB"的计算示例。**为什么推理 16 GB 能跑的训练 OOM：** 推理只是 2 B/参数的工作副本 + 少量激活；训练额外加了梯度+优化器的 +12 B/参数**并**保持整个前向激活图存活以供反向传播。固定的 18 B/参数由 M9/M12/M13 解决；激活项由 M5/M6/M7/M11 解决。

### M2 — 阅读 CUDA OOM 堆栈（数字告诉你用哪个修复）

**症状**：`torch.OutOfMemoryError: CUDA out of memory. Tried to allocate X MiB (GPU 0; Y GiB total capacity; Z GiB already allocated; A GiB free; B GiB reserved in total by PyTorch ...)`。

**根因 — 解读四个数字**：
- **Tried to allocate X** — 失败的*单次*请求大小。大 X = 大张量（长序列注意力得分矩阵，最长批次 M16）；小 X 失败但有 GB 级"空闲" = **碎片化**。
- **reserved B vs allocated Z** — `reserved` = 缓存分配器从驱动获取的总量；`allocated` = 活跃张量。**`reserved` ≫ `allocated` 且失败 X 小 ⇒ 碎片化**（空闲块存在但没有足够连续的）。这是 PyTorch 的明确诊断："如果 reserved 但 unallocated 很大，设置 `expandable_segments:True`"（M8）。
- **free A** — 驱动可见的显存空闲；如果 A 很大但分配仍失败，怀疑另一个进程（M3）或僵尸进程持有 VRAM（gotchas_universal.md **U11**）。

来源：PyTorch 论坛关于堆栈字段的讨论 (https://discuss.pytorch.org/t/torch-outofmemoryerror-cuda-out-of-memory/217669)；reserved-vs-allocated → 碎片化规则来自分配器文档（M8 URL）。

### M3 — VRAM OOM 不是主机内存 OOM（不同的故障，不同的修复）

`torch.OutOfMemoryError: CUDA out of memory`（Python 回溯）是 **VRAM** 耗尽。裸 `Killed` / **exit 137** 且**无回溯**是 Linux 内核因**主机内存**（cgroup `memory.max`）耗尽杀掉进程 — 几乎总是 `num_workers × 一个大的内存对象`。它们的修复方向相反，收录在通用目录中：
- 主机内存 cgroup-OOM（`Killed`，exit 137，dataloader workers）→ **gotchas_universal.md U9**。
- VRAM-OOM 与 cgroup 的区分、碎片化、并发作业大小 → **gotchas_universal.md U10**。
- "空 GPU"仍然 OOM（僵尸持有 nvidia-smi 无法归属的 VRAM）→ **gotchas_universal.md U11**。

在"修复"前确认是哪一个：`dmesg | grep -iE 'killed process|out of memory'` 非空 ⇒ 主机内存内核杀死（U9），**不是** CUDA OOM。不要为了"修复"主机内存杀死而缩小模型。

---

## 按顺序修复（最便宜 / 最不影响科学结论的优先）

### M4 — 阶梯：从上往下应用，装下就停

每一步代价更高（速度、复杂度或对结果的风险）。只爬到需要的高度：

1. **缩减 micro-batch + 梯度累积**（M5）— 免费，完全相同的有效批次，零精度变化。
2. **bf16 混合精度**（M6）— 激活减半，通常是加速；bf16 不需要 loss scaling。
3. **激活 / 梯度检查点**（M7）— 以约 20–30% 计算量换取大幅激活削减。
4. **`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`**（M8）— 免费；仅修复*碎片化* OOM。
5. **SDPA / FlashAttention** — 停止物化完整的 O(seq²) 注意力矩阵（M11）。
6. **缩短序列长度 / 降低分辨率**（M11）— 便宜但**改变了科学结论** → 验证（必需）。
7. **8 位 / 分页优化器**（M12）— 将 8 B/参数的优化器状态降至约 2 B，几乎无精度损失。
8. **FSDP / DeepSpeed ZeRO-1→2→3**（M9）— 跨 GPU 分片优化器→梯度→参数（需要 ≥2 GPU）。
9. **CPU / NVMe 卸载**（M10）— 单 GPU 的最后手段；以大量速度损失换取装下。
10. **LoRA / QLoRA**（M13）— 仅用于*微调*：冻结基座，训练适配器；QLoRA 将基座量化为 4 位。

阶梯 1–4 和 7 **不**改变模型/优化数学；阶梯 6 会（声明它，按 verifying-dl-experiments 重新验证）。阶梯 8–10 改变状态*存放位置*，不改变数学（LoRA 改变容量）。

### M5 — 缩减 micro-batch + 梯度累积（免费的首选）

**症状**：OOM 随 batch size 缩放；有效 batch 必须保持固定以维持结果。

**修复**：降低 `per_device_train_batch_size` 到能装下的值，提高 `gradient_accumulation_steps` 保持*有效*批次不变（`effective = micro_batch × accum × world_size`）。梯度在子批次间累积后才做一次优化器步 — 相同数学，更低峰值激活内存。保持 micro-batch 尽量大（batch 4 × accum 16 优于 batch 1 × accum 64 — 更好的 GPU 利用率）。
来源：https://huggingface.co/docs/transformers/main/en/perf_train_gpu_one（gradient accumulation）。
注意：使用 token 级 loss + 自定义循环时，朴素累积可能因不均匀的子批次 token 数而错误加权 loss — 这是 **verifying-dl-experiments**（必需）负责的正确性问题。

### M6 — bf16 混合精度（Ampere+ 上优先 bf16 而非 fp16）

**症状**：fp32 训练；激活占主导；GPU 是 Ampere（A100/30xx）或更新。

**修复**：`bf16=True`（HF `TrainingArguments`）或 `torch.autocast("cuda", dtype=torch.bfloat16)`。主要收益是**激活以 16 位存储**。**bf16 优于 fp16**：bf16 拥有 fp32 的指数范围，不需要 loss scaling，不会溢出/下溢 — NaN 故障更少。注意 fp16 在小批次时可能*增加*内存（保持 fp16 和 fp32 两份权重副本）；bf16 在支持的硬件上是更安全的默认选择。
来源：https://huggingface.co/docs/transformers/main/en/perf_train_gpu_one（混合精度；bf16 需要 Ampere+）。切换精度后 NaN/发散 = 数值问题 → **verifying-dl-experiments**。

### M7 — 激活 / 梯度检查点（以计算换激活内存）

**症状**：18 B/参数的固定成本能装但**激活** OOM（深层模型、长序列、大批次）。

**修复**：`gradient_checkpointing=True`（HF）、`model.gradient_checkpointing_enable()` 或手动 `torch.utils.checkpoint.checkpoint(...)`。只存储一部分激活；其余在反向传播期间**重新计算** — 大幅削减激活内存，代价是训练**慢约 20–30%**。
来源：https://huggingface.co/docs/transformers/main/en/perf_train_gpu_one（"约 20% 更慢"）。陷阱：使用 HF generate/caching 时在检查点模式下设置 `model.config.use_cache=False`，否则会警告并忽略；使用 DDP 时，reentrant 检查点可能出问题 — 使用 `use_reentrant=False`。

### M8 — `expandable_segments:True`（免费的碎片化修复）

**症状**：OOM 时**失败分配很小**但 `reserved` ≫ `allocated` 且看起来有 GB 级"空闲"（M2）；常见于**可变形状**（变化的 batch/seq-len、动态填充）。

**修复**：启动时设置 `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`（环境变量，在进程启动*前*设置；现代别名是 `PYTORCH_ALLOC_CONF`）。它用 CUDA VMM 支持段使其可增长/缩小，而不是每次 `cudaMalloc` 成为一个不可合并的块 — 这正是碎片化的根源。
来源：PyTorch CUDA notes (https://docs.pytorch.org/docs/stable/notes/cuda.html) 和分配器开发日志 (https://docs.pytorch.org/devlogs/eager/2026-06-01-cuda-caching-allocator/)。替代旋钮：如果在*大*块上碎片化，用 `max_split_size_mb:<N>`（阻止分配器拆分 N MiB 以上的块）。这与 **gotchas_universal.md U10** 引用的是同一个旋钮 — 在机器上设为默认值，几乎免费。
版本注意：`expandable_segments` 仍标记为实验性；它与某些 VMM 分配器（如 NCCL `ncclMemAlloc`、pytorch/pytorch#165419）存在已知互操作边界 — 如果自定义分配器栈行为异常，去掉它。

### M9 — FSDP / DeepSpeed ZeRO 分片（≥2 GPU：分片 18 B/参数）

**症状**：固定的 18 B/参数状态单卡装不下；有多 GPU 可用。

**修复 — 跨数据并行组分片训练状态**，按阶段升级：
- **ZeRO-1 / `optim_state_dict` 分片** — 分区**优化器状态**（8 B/参数）。通信变化最小；DP 因优化器状态 OOM 时从这里开始。
- **ZeRO-2 / FSDP `SHARD_GRAD_OP`** — 同时分区**梯度**（4 B）。内存/通信的良好平衡。
- **ZeRO-3 / FSDP `FULL_SHARD`** — 同时分区**参数**（6 B）。最大节省；需要高带宽互连（NVLink/NVSwitch），因为参数每层 all-gather。
来源：DeepSpeed ZeRO 教程 (https://www.deepspeed.ai/tutorials/zero/) 和 HF DeepSpeed 集成 (https://huggingface.co/docs/transformers/en/deepspeed)；FSDP 的 `ShardingStrategy` 与这些阶段 1:1 对应。
多 GPU 启动 + NCCL fabric 陷阱（错误 NIC、超时、MTU）→ **references/multinode.md**。

### M10 — CPU / NVMe 卸载（单 GPU 最后手段）

**症状**：即使 ZeRO-3（或单 GPU）也装不下参数/优化器；愿意用大量速度换取装下。

**修复**：将优化器状态（以及 ZeRO-3 下参数）卸载到 **CPU 内存或 NVMe**。DeepSpeed `offload_optimizer: {device: cpu|nvme}`（适用于 ZeRO-1/2/3），`offload_param: {device: nvme}`（仅 ZeRO-3）；**ZeRO-Infinity** 两者都卸载用于超大模型。QLoRA 的**分页优化器**（M12）是更轻的形式 — 优化器状态仅在内存峰值时页面换出到 CPU。
来源：DeepSpeed ZeRO 文档 (https://deepspeed.readthedocs.io/en/stable/zero3.html)；ZeRO-Infinity (https://www.deepspeed.ai/2021/03/07/zero3-offload.html)。代价：PCIe/NVMe 带宽成为瓶颈 — 预期数倍减速；在计费机器上，要权衡是租更大的卡（原则 #1、#9）。

### M11 — 减少序列长度 / 分辨率 / 注意力占用

**症状**：激活（尤其是 **O(seq²)** 注意力得分矩阵）占主导；OOM 随 seq-len/分辨率超线性增长。

**修复（最便宜的变体优先）**：
- **使用 SDPA / FlashAttention** 避免物化完整 seq² 注意力矩阵 — `attn_implementation="sdpa"`（PyTorch 2.1.1+ 默认）或 `"flash_attention_2"`。无精度变化。
- 然后才**缩短 seq-len / 降低图像分辨率 / patchify** — 这**改变了任务/科学结论**；声明并重新验证（分辨率变化破坏训练的故障模式由 **verifying-dl-experiments** 负责，必需）。
来源：https://huggingface.co/docs/transformers/main/en/perf_train_gpu_one（SDPA、注意力后端）和 model-memory-anatomy（注意力得分矩阵随 seq² 增长）。

### M12 — 8 位与分页优化器（将 8 B/参数优化器状态降至约 2 B）

**症状**：优化器状态是最大的桶（M1）；想要几乎无精度损失的削减。

**修复**：将 AdamW 换成**量化**优化器 — HF `optim="adamw_bnb_8bit"` / `"paged_adamw_8bit"`（bitsandbytes 8 位 Adam，状态以 8 位保存，每步反量化 → 约 2 B/参数 vs 8 B），或 `optim="adafactor"`（存储行/列矩而非逐元素 → 少得多的内存，**更慢的收敛**）。**分页**变体额外在峰值时将优化器状态页面换出到 CPU 以度过瞬时峰值。
来源：https://huggingface.co/docs/transformers/main/en/perf_train_gpu_one（优化器）和 model-memory-anatomy（"量化 Adam → 2 字节/参数"）。Adafactor 的收敛变化是科学问题 → 在信任其消融差值前需 **verifying-dl-experiments**（必需）。

### M13 — LoRA / QLoRA（仅微调：不训练完整模型）

**症状**：*微调*大型预训练模型；全量微调状态装不下。

**修复**：**LoRA** 冻结基座权重，训练小型低秩适配器 → 梯度+优化器仅存在于适配器（参数的极小部分），因此基座的 18 B/参数成本几乎消失。**QLoRA** 更进一步：将**冻结基座量化为 4 位 NF4**（+ 双量化 + 分页优化器），在其上训练 fp16/bf16 适配器 — 据报告可在单张 48 GB GPU 上微调 **65B 模型**，与 16 位相比无精度退化。
来源：QLoRA 论文 (https://arxiv.org/abs/2305.14314) 和仓库 (https://github.com/artidoro/qlora)。注意：LoRA *改变了模型容量* — 它是不同的优化目标，不是免费的 OOM 技巧。LoRA 结果是否匹配全量微调是科学声明 → **verifying-dl-experiments**（必需）。

---

## 特定步骤的 OOM（步骤编号就是诊断）

### M14 — 在**首次反向传播**时 OOM（而非前向）

**症状**：前向传播完成，OOM 出现在 `.backward()`。

**根因**：前向只分配激活；**反向**额外分配完整的**梯度**缓冲区（4 B/参数）且需要所有缓存激活同时存活 — 峰值内存在反向，不在前向。前向没问题的模型仍可能在此 OOM。

**修复**：M7（检查点 — 重计算而非存储激活）是针对性修复；然后 M5/M6。如果峰值来自单个巨大层，对该块专门做梯度检查点。

### M15 — 仅在**验证 / 评估**时 OOM，训练正常

**症状**：训练 epoch 正常跑；首次评估 OOM — 即使有 `torch.no_grad()` / `model.eval()`，有时甚至 eval batch size 1 也 OOM。

**根因 — 两个不同的原因**：
1. **评估批次 > 训练批次**，或 no-grad 评估允许尝试*更大*批次超过训练峰值。激活图不需要保留，但单次大前向 + 其临时缓冲区仍可 OOM。
2. **HF Trainer 在 GPU 上累积预测**：默认情况下 eval logits/labels 在整个评估集上**在 GPU 上**拼接后才移到 CPU — 大评估集无论 batch size 如何都会 OOM（huggingface/transformers#7232）。

**修复**：显式设置 `per_device_eval_batch_size`（不要继承过大的值）；设置 **`eval_accumulation_steps=N`** 使预测每 N 步移到 CPU 而非堆在 GPU 上 (https://huggingface.co/docs/transformers/main_classes/trainer)。自定义循环中：用 `torch.no_grad()` / `torch.inference_mode()` 包裹评估，并在追加到列表前 `.cpu()` / `.detach()` 输出。评估产物*大小*（逐样本转储膨胀）由 **verifying-dl-experiments** 负责。

### M16 — 训练中期在**最长批次**上 OOM（变长/桶化数据）

**症状**：数千步成功，然后某步 OOM；从那里重启在同一条数据再次 OOM；固定批次从不 OOM。

**根因**：使用变长输入（NLP token 批次、点云、可变分辨率图像）时，峰值激活内存由批次中**最长序列**决定，而非平均值。内存按最坏情况分配，只出现在特定批次。

**修复**：为**最大**长度而非平均值分配一切：设 `max_length` 上限 / 使用**长度桶或排序批处理**使长样本共享小批次；设 `group_by_length=True`（HF）和硬性 `max_length`。`expandable_segments:True`（M8）也有帮助，因为可变形状否则会碎片化。不要从第 N 步 OOM 得出"数据损坏"的结论 — 这是最长批次。

### M17 — 在**第 2 步** OOM（首次优化器步之后），第 1 步正常

**症状**：第 1 步训练正常；第 2 步 OOM 或首次 `optimizer.step()` 时 OOM。

**根因**：Adam **延迟分配**其 m/v 状态（8 B/参数）在*首次* `optimizer.step()` 时，而非构建时。因此峰值在第 1 步后跳升。预留内存也随分配器缓存反向缓冲区而攀升。
来源：内存快照时间线显示优化器状态在 iter 1 后出现 (https://pytorch.org/blog/understanding-gpu-memory-1/)。

**修复**：为**步后**峰值而非第 1 步做预算 — 在两整步*之后*用 `max_memory_allocated()` 测量峰值，而非一步。然后应用 M12（8 位优化器将此跳变减半）或 M5。

---

## 调试工具（测量，不要猜）

### M18 — `torch.cuda.memory_summary()` + 统计函数（初步查看）

**症状**：需要知道*什么*驻留内存才能选择修复。

**修复**：在 OOM 点（或在 `except torch.cuda.OutOfMemoryError` 中）打印 `torch.cuda.memory_summary()` 获取按大小类别的 allocated/reserved/active 表。编程方式：`torch.cuda.memory_allocated()`（活跃张量）vs `torch.cuda.memory_reserved()`（分配器总量）— 差距大 = 碎片化/缓存（→ M8）；`torch.cuda.max_memory_allocated()` 获取真实峰值（在阶段间用 `reset_peak_memory_stats()` 重置以隔离前向 vs 反向 vs 优化器）。
来源：https://docs.pytorch.org/docs/stable/notes/cuda.html（内存管理函数）。

### M19 — CUDA 内存快照 + 可视化器（找到确切的罪魁分配）

**症状**：汇总统计不够 — 需要*哪行代码*分配了 OOM 的内存。

**修复 — 在 OOM 周围录制快照并查看时间线**：
```python
torch.cuda.memory._record_memory_history(max_entries=100000)   # 在步骤前开始
try:
    train_a_few_steps()
finally:
    torch.cuda.memory._dump_snapshot("oom_snapshot.pickle")     # 写入历史
    torch.cuda.memory._record_memory_history(enabled=None)      # 停止
```
将 `oom_snapshot.pickle` 拖到 **https://pytorch.org/memory_viz**（快照不会上传到服务器端），或 `python torch/cuda/_memory_viz.py trace_plot oom_snapshot.pickle -o snapshot.html`。时间线分别着色**参数 / 梯度 / 优化器状态 / 激活 / 临时变量**，因此 OOM 时刻最高的带标明了要攻击的桶（→ 映射回 M5–M13）。PyTorch **2.1+** 可用。
来源：https://pytorch.org/blog/understanding-gpu-memory-1/。在远程机器上：导出 pickle，`scp` 下来（references/ssh_transport.md），本地查看 — 不要试图通过 ssh 运行可视化器。

### M20 — `empty_cache()` 与"内存泄漏"迷思

**症状**：相信 `torch.cuda.empty_cache()`"释放内存并修复 OOM"，或认为持续上升的预留内存是泄漏。

**根因 / 迷思澄清**：
- `torch.cuda.empty_cache()` 将缓存但未使用的块**归还给驱动**；它**不**释放活跃张量，也**不**为*你自己的*进程腾出更多空间（分配器本就会复用那个缓存）。它只帮助同 GPU 上的*另一个*进程，或以约 10% 速度代价减少碎片化（HF `torch_empty_cache_steps=N` 每 N 步运行一次 — https://huggingface.co/docs/transformers/main/en/perf_train_gpu_one）。它**不是**真正装不下模型的修复方案。
- **`reserved` 上升 ≠ 泄漏。** 缓存分配器持有释放的块待复用；reserved 上升后趋于平稳是正常的。*真正的*泄漏是**跨步骤 `memory_allocated()` 上升**且 batch 固定 — 通常是累积了仍需梯度的张量（追加 `loss` 而非 `loss.item()`、在 Python 列表中保持引用）。修复引用，而非用 `empty_cache()`。
- 每步调用 `empty_cache()` 以"保持安全"只会减慢训练且可能*增加*碎片化。

真正的 OOM 机制泄漏（累积 loss 张量、未 `detach`）属于这里；*指标*漂移是真正效果还是 bug 属于 **verifying-dl-experiments**（必需）。

---

## 指针 — 其他地方收录的内存陷阱（不要重复）

- **主机内存 cgroup-OOM**（裸 `Killed` / exit 137，`num_workers × 大张量`）→ **gotchas_universal.md U9**。
- **VRAM-OOM 与 cgroup-OOM 的区分**、并发作业大小、`expandable_segments` 一行命令 → **gotchas_universal.md U10**。
- **僵尸持有 nvidia-smi 看不到的 VRAM**（"空" GPU 上 OOM）→ **gotchas_universal.md U11**。
- **磁盘满导致 `torch.save` 崩溃**（非内存，但另一种"空间不足"）→ **gotchas_universal.md U6**。
- **多 GPU NCCL / fabric** 用于 FSDP/ZeRO 启动 → **references/multinode.md**。
- **适配后的数字是否正确**（精度切换、seq-len 变化、LoRA vs 全量、累积 loss 加权、确定性）→ **verifying-dl-experiments**（必需 — 本层负责*让它装下并运行*；那个技能决定*结果是否真实*）。
