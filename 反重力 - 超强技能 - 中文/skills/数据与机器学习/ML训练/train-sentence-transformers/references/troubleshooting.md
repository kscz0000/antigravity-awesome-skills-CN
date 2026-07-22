# 故障排查

sentence-transformers 训练中的常见失败，含根因和修法。按症状组织。

## 显存不足（OOM）

**症状：** `torch.cuda.OutOfMemoryError` 或 `CUDA out of memory`。

**按顺序修：**

1. 降低 `per_device_train_batch_size`。对 MNRL，通过 `CachedMultipleNegativesRankingLoss(model, mini_batch_size=...)` 配大外层 batch 补偿。
2. 设 `gradient_accumulation_steps` 在多个更小 batch 上累积梯度（用于非对比损失）。
3. 启用 `gradient_checkpointing=True`。慢 ~30%，激活显存少 ~40%。**与 `Cached*` 损失不兼容。**
4. 用 `bf16=True` 替代 fp32（如果 GPU 支持 Ampere+）。
5. 降低 transformer 模块上的 `max_seq_length`：`model[0].max_seq_length = 128`。
6. 对大 decoder 基座用 LoRA（`peft`）。见 `../scripts/train_sentence_transformer_with_lora_example.py`（docstring 涵盖使用时机、超参、QLoRA、坑）。
7. 换更大 GPU 或多卡（`accelerate launch`）。

**另见**：`hardware_guide.md` 中按 batch 大小的 VRAM 估算。

## Loss 为 NaN 或 Inf

**症状：** 训练 loss 打印为 `nan` 或 `inf`，或突然跳到一个巨大值。

**修法：**

1. **先降学习率**。试 `5e-6` 或 `1e-6`。
2. 启用 `warmup_steps=0.1`（`< 1` 的 float 被解释为总步数的比例），或设绝对值 `warmup_steps=500`。
3. fp16 换 bf16（数值上更稳）。如果只能 fp16（旧 GPU），对健全性跑试一下关掉 fp16。
4. 检查数据集中是否有坏行：空字符串、NaN 标签值、列数不匹配。用 `print(dataset[:5])` 看几行。
5. 自定义损失或异常基座模型（超长上下文）时，考虑给训练参数加 `max_grad_norm=1.0`。
6. 检查 tokenize：某些 tokenizer 对特定 unicode / 纯空白输入产出 0 token，会在 mean pooling 中导致下游 NaN。

## 指标不提升 / 等于基线

**症状：** 训练后 eval 指标和训练前一样。

**修法：**

1. **用 `--loss <your-loss>` 重跑数据检查器**。最常见原因：列序错、标签列没识别、或者损失期望别的形状。
2. 检索场景：**负例太简单**。挖掘 hard negative（`scripts/mine_hard_negatives.py`）。
3. 检查 `metric_for_best_model` —— 如果 key 与 evaluator 写的不匹配，trainer 静默用最终 checkpoint（而不是 best）。
4. 确认 MNRL 系损失设了 `BatchSamplers.NO_DUPLICATES`。不设的话，batch 内负信号被破坏。
5. 基座模型对任务不对（例如短文本 STS 用了 decoder-only LLM）。换基座。
6. 学习率太低。Encoder 默认 `2e-5`；LoRA 要 `1e-4+`；static embedding 要约 `2e-1`（远高于 transformer）。
7. 数据集对所选损失太小。对比损失需要 >10k 对才有意义。

## 训练在第一次 eval 卡住

**症状：** 训练启动，然后在第一次 eval 步无限卡住。

**修法：** 你设了 `eval_strategy="steps"` 或 `"epoch"`，但要么没传 `eval_dataset`，要么传了空的。要么给 `eval_dataset`，要么设 `eval_strategy="no"`。

## 训练在启动时卡住（多卡）

**症状：** `accelerate launch` 跑起来，打印 "Found X GPUs" + 模型加载信息，然后卡住。

**修法：**

1. 如果用自定义 dataset 类，确保实现了 `__len__` 并在进程间返回一致的长度。
2. 如果用 `batch_sampler=BatchSamplers.NO_DUPLICATES` 且数据集相对 world size 太小，可能组不出 batch。用更大数据集或更小 per-device batch。
3. 检查各节点 PyTorch / CUDA 版本是否一致。在每个节点跑 `nvidia-smi` + `python -c "import torch; print(torch.version.cuda)"`。
4. NCCL 超时。设 `NCCL_TIMEOUT=300`（秒）环境变量。

## `CachedMultipleNegativesRankingLoss` 崩溃

**症状：** 报错像 "element 0 of tensors does not require grad"，或某种神秘的 autograd 错误。

**修法：** 你开了 `gradient_checkpointing=True`。cached 损失自己做 forward/backward 编排；gradient checkpointing 与之冲突。关掉 `gradient_checkpointing`。

同样适用于 `CachedSpladeLoss`、`CachedGISTEmbedLoss` 和任何 `Cached*` 损失。

## Hub 推送失败

**症状：** `push_to_hub` 期间 `HTTPError: 401` 或 `403`。

**修法：**

1. 跑 `hf auth whoami`。失败就 `hf auth login`。
2. Token 需要 **write** 权限。从 https://huggingface.co/settings/tokens 重新生成。
3. repo 必须存在且你有写权限，或设了 `hub_private_repo=True` / `False` 让库创建它。
4. HF Jobs 上：在任务提交时传 `secrets={"HF_TOKEN": "$HF_TOKEN"}`。

## Tracker（Trackio / W&B / TensorBoard）不 log

**症状：** 训练跑但 tracker UI 不出指标。

**修法：**

- Trackio：确认 `pip install trackio` 成功。无登录步骤 —— trackio 用你的 `HF_TOKEN`（由 `hf auth login` 或 `HF_TOKEN` 环境变量设）。HF Jobs 上，`HF_TOKEN` 必须在 `secrets` 中。
- W&B：确认 `wandb login` 成功，或设了 `WANDB_API_KEY` 环境变量。HF Jobs 上，`WANDB_API_KEY` 必须在 `secrets` 中。
- `report_to` 没设到正确的 tracker：`report_to="trackio"`（或 `"wandb"`，或 list 如 `["trackio", "tensorboard"]`）。
- TensorBoard：检查 `logging_dir`（默认 `output_dir/runs/<timestamp>`）；把 TB 指向父目录。

## 基座模型能加载但 `encode` 产出垃圾

**症状：** `model.encode(["test"])` 返回常量向量，或全 0，或 NaN。

**修法：**

1. 你把分类微调当基座加载了（例如 SQuAD 微调的 BERT）。CLS 头是 QA 头，不是可用的 pooling 层。用底下的预训练 encoder（`bert-base-uncased`），而不是任务专用 checkpoint。
2. 对 decoder 模型：你在 causal 注意力上用了 mean pooling。换 last-token pooling。
3. 对 SPLADE：模型的 MLM head 没正确初始化。确保基座有 `AutoModelForMaskedLM` 兼容性。

## 数据集加载但 eval 平凡正确

**症状：** 第一次 eval 步 eval 指标就是 1.0（完美）。

**修法：** 你的 eval 集合与训练集合重叠。检查 `dataset.train_test_split(test_size=...)` 是否调用正确，或 Hub 数据集的 `train` / `dev` split 是否真的不相交。

## Model-card 生成失败

**症状：** 关于 model-card 生成的警告，或 `save_pretrained` 后 `README.md` 缺失。

**修法：**

- `codecarbon` 可能在尝试写 emissions 并失败。设 `CODECARBON_LOG_LEVEL=error` 或卸载 codecarbon。
- 某些训练状态无法序列化（有不寻常类型的自定义对象）。传 `model_card_data=SentenceTransformerModelCardData(...)` 显式字段以绕过推断。

## 交叉编码器 `num_labels` 不匹配

**症状：** `BinaryCrossEntropyLoss` 因维度不匹配报错，或 `CrossEntropyLoss` 抱怨。

**修法：** `num_labels=1` 配 `BinaryCrossEntropyLoss`；`num_labels>=2` 配 `CrossEntropyLoss`。BCE 设 `CrossEncoder("...", num_labels=1)`。

## 蒸馏 / listwise / pairwise 训练后交叉编码器 eval nDCG 崩溃

**症状：** 训练 loss 看着健康，基线 eval 看着正常，但训练后 eval nDCG 跌很多（如 0.59 → 0.14）。第一次 eval 之后的每个 checkpoint 都低于基线。

**根因：** `CrossEncoder(num_labels=1, ...)` 的默认 `Sigmoid` 激活把 >5 的原始 logits 压到 ~1.0。蒸馏 / listwise / pairwise 损失（`MSELoss`、`MarginMSELoss`、`LambdaLoss`、`RankNetLoss`、`ListNetLoss`、`ListMLELoss`、`PListMLELoss`、`ADRMSELoss`）作用在原始 logits 上 —— 一旦模型学会把正例推到饱和点之外，排序信息就丢了。

**修法：** 构造模型时用 `Identity` 激活：

```python
import torch.nn as nn
model = CrossEncoder("...", num_labels=1, activation_fn=nn.Identity())
```

只有 `BinaryCrossEntropyLoss` 保留默认 `Sigmoid`（它内部用 BCE-with-logits，需要可 sigmoid 的输入）。

## LambdaLoss 训练 loss 极小（如 1e-4）：训练坏了吗？

**症状：** 用 `LambdaLoss(model, weighting_scheme=NDCGLoss2PPScheme())` 配大 `K`（>=64），训练 loss 在 1e-3 到 1e-5 范围。

**根因：** `NDCGLoss2PPScheme` 按 discount-weighted pair 数归一化，量级大致随 K 缩放。loss 数值大小不是你应该跟踪的信号。

**修法：** 对 LambdaLoss 忽略训练 loss；改为看 eval 指标（`eval_NanoBEIR_R100_mean_ndcg@10` 或你的 `metric_for_best_model`）。如果 eval 在向对的方向走，loss "太小"是预期的。

## LambdaLoss OOM：先降什么

**症状：** LambdaLoss 训练 step 期间 `CUDA out of memory`，尤其是 K>=64。

**恢复顺序：**

1. **先降 loss 上的 `mini_batch_size`**。内部 forward chunking 保留 K 列表语义 —— 这是最便宜的旋钮，不改实验。
2. 降 `per_device_train_batch_size` 并用 `gradient_accumulation_steps` 补偿以保持总 batch 固定。
3. **只把降 K（每 query 候选列表长度）当最后手段。** 降 K 改变 loss 计算的东西；这是实验变更，不是显存调节。

对非常大 K（>=128），`NDCGLoss2PPScheme` 每 query 物化 O(K²) 权重 buffer，这些不在 forward chunking 覆盖内，所以单靠小 `mini_batch_size` 可能不够 —— 这种时候 K 才是对的旋钮。

## 加载带自定义内联 `nn.Module` 的模型抛 `ImportError`

**症状：** 通过 `train.py` 训练和保存能跑；但从任何其他脚本（`predict.py`、notebook 或另一个包）加载保存的模型时失败：

```
ImportError: Module "__main__" does not define a "ClassifierHead" attribute
```

**根因：** 当自定义 `nn.Module` 在脚本里内联定义时，Python 把它的 qualname 记为 `__main__.ClassifierHead`。ST 在保存时把这个 qualname 写到 `modules.json`。从其他入口加载时无法解析 `__main__.ClassifierHead` —— 类的定义在 loader 的 `__main__` 里不存在。

**修法（任选其一）：**

1. 把类移到可 import 的模块：`from my_pkg.heads import ClassifierHead`。再保存一次让 `modules.json` 记 `my_pkg.heads.ClassifierHead`。
2. 改用 stock ST 模块（`Dense + LayerNorm + Dense`）搭出相同形状 —— 那些总是可加载的。
3. 文档说明模型只能从同一脚本加载（一次性实验可接受，发版模型不行）。

## SPLADE 嵌入太稠密（不稀疏）

**症状：** 训练后 `(embedding != 0).sum(dim=-1)` 在几千量级，而不是 ~30-250。

**修法：**

1. 你漏了 `SpladeLoss` 包装。`SparseMultipleNegativesRankingLoss` 本身不加 FLOPS 正则。包装：`SpladeLoss(model, loss=inner_loss, query_regularizer_weight=5e-5, document_regularizer_weight=3e-5)`。
2. 正则权重太低。提到 1e-4 或更高。
3. 调度器提前清零。`SpladeRegularizerWeightSchedulerCallback` 在前 ~33% 训练中把权重从 0 ramp 到目标值（默认 `warmup_ratio=1/3`；可配）。很短的运行上到不了目标。要么训更久，要么把 `query_regularizer_weight` / `document_regularizer_weight` 调高补偿。

## `ValueError: The dataset has ... columns but the loss expects N`

**修法：** 列数不匹配。丢多余列（`dataset.remove_columns([...])`）或用 `select_columns` 重排。名字无关；数量和顺序有关。

## CPU 上编码奇慢

**症状：** 每秒几十个句子，而不是几千个。

**修法：**

- 确保模型在 GPU 上：`model.to("cuda")`（或加载时 `device_map="auto"`）。
- 真要 CPU 推理（无 GPU），考虑换 `StaticEmbedding` 基础模型 —— CPU 上比 transformer 快约 1000 倍。

## Hub 模型能加载，但 `model.encode(prompt_name="query")` 像没应用 prompt

**修法：** 保存模型的 `config_sentence_transformers.json` 里没有 `prompts`。训练时 `save_pretrained` 之前设 `model.prompts = args.prompts`，或用 `SentenceTransformerModelCardData(prompts=...)`。

## `accelerate launch` 只跑在单卡

**修法：** 先跑 `accelerate config`，设 GPU 数量和精度。或显式传：`accelerate launch --multi_gpu --num_processes=4 train.py`。

## Cached 损失 + PEFT adapter 反向传播失败

**症状：** 用 Cached* 损失 + LoRA adapter 时报 "None of the inputs have requires_grad=True"。

**修法：** `add_adapter` 之后调：

```python
model.transformers_model.enable_input_require_grads()
```

这确保梯度能穿过冻结的基座 + 可训练的 adapter。

## 相关参考文档

- `training_args.md`（共享）—— 影响上述所有内容的参数。
- `hardware_guide.md`（共享）—— VRAM 估算与多卡。
- `dataset_formats.md`（共享）—— 列 / 损失验证。
- `losses_sentence_transformer.md` / `losses_cross_encoder.md` / `losses_sparse_encoder.md`（按模型类型分类）—— 各损失特有的怪癖。
