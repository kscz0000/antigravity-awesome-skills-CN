# 交叉编码器损失（重排器）

所有损失位于 `sentence_transformers.cross_encoder.losses`。

交叉编码器损失分三大族：**pointwise**（独立打分每对）、**pairwise**（对 pair 打分）、**listwise**（一次性对整个排序列表打分）。此外还有针对特定场景的对比 / 蒸馏变体。

## 总览决策表

| 你拥有 | 用 | 族 |
|---|---|---|
| `(query, passage, label)`，`label ∈ {0, 1}` 或 `[0, 1]` | `BinaryCrossEntropyLoss` | Pointwise |
| `(query, passage, class_id)` 多分类 | `CrossEntropyLoss` | Pointwise |
| `(query, passage)` 含隐式正例，想要对比 | `CachedMultipleNegativesRankingLoss` | Contrastive |
| `(query, passages, labels)`（每 query 一行，带平行候选 passage 和相关性分数列表） | `LambdaLoss` | Listwise |
| 同样的 listwise 形状，想要稳健简单的损失 | `ListNetLoss` 或 `ListMLELoss` | Listwise |
| `(query, positive, negative)` pairwise | `RankNetLoss` | Pairwise |
| `(query, passage, teacher_score)` 从更强重排器蒸馏 | `MSELoss` 或 `MarginMSELoss` | Distillation |

## Pointwise 损失

### `BinaryCrossEntropyLoss`

**默认的交叉编码器损失。** 用于 `(query, passage, label)`，label 为 0/1 或连续的 [0, 1] 相关性分数。

```python
loss = BinaryCrossEntropyLoss(model, pos_weight=torch.tensor(5.0))
```

- `pos_weight`：数据集不平衡时上权重正例（例如 1 个正例 + N 个 hard negative）。不错的默认是 `pos_weight = num_hard_negatives`。
- 同时处理二分类标签和连续相关性分数 —— 如果有分级相关性（0.0、0.5、1.0）BCE 也能用。

### `CrossEntropyLoss`

在 passage 上的多分类。与 `CrossEncoder("...", num_labels=N)` 一起用，N 是类别数（如 NLI 为 3：entailment / neutral / contradiction）。

## 对比损失（用于重排器训练）

### `MultipleNegativesRankingLoss`（交叉编码器）

与双编码器 MNRL 对应的对比训练。应用 batch 内负例：对每个 `(query, positive)`，batch 中其他 `positive` 都作为负例。

- **数据**：`(query, positive)` 或 `(query, positive, negative_0, negative_1, ...)`。
- 训练 CrossEncoder 时，**默认优先用 `BinaryCrossEntropyLoss` + 挖掘的 hard negative**；只有当你只有 `(query, positive)` 对、且想避免单独的挖掘步骤时，才把 MNRL 当 fallback。

### `CachedMultipleNegativesRankingLoss`

Cached 变体（GradCache）—— 把每卡 batch 与有效 batch 内负例解耦，与双编码器 cached 版相同。

```python
loss = CachedMultipleNegativesRankingLoss(model, mini_batch_size=16)
```

- 与 `gradient_checkpointing=True` 不兼容。
- 在单卡上训练有效 batch 256+ 的重排器的关键选择。

## 蒸馏损失

> **所有下面蒸馏、listwise、pairwise 损失都强制 `activation_fn=nn.Identity()`** —— 只有 `BinaryCrossEntropyLoss` 和 `CrossEntropyLoss` 容忍默认的 `Sigmoid`。训练时损失看到的是原始 logits，但模型的 `activation_fn` 在评估时通过 `predict()` 应用；默认的 `Sigmoid`（配 `num_labels=1`）会把 `predict()` 内 >5 的原始 logits 压到 ~1.0，静默坍塌评估排名（训练损失看起来正常，但 nDCG 从 ~0.59 跌到 ~0.14）。用 `CrossEncoder("...", num_labels=1, activation_fn=torch.nn.Identity())` 构造。见 `troubleshooting.md`（"CrossEncoder eval nDCG 在蒸馏 / listwise / pairwise 训练后崩溃"）的失败模式走查。

### `MSELoss`（交叉编码器）

把学生输出分数回归到教师分数。用 `activation_fn=nn.Identity()` 构造模型（见上面 callout）。

- **数据**：`(query, passage, teacher_score)`。
- 教师通常是更大/更强的交叉编码器。预先算一次分数，存为 label。

### `MarginMSELoss`（交叉编码器）

把正负例分数的**差**回归到教师的 margin。通常比纯 MSE 蒸馏效果更好。

- **数据**：`(query, positive, negative, score_diff)`，其中 `score_diff = teacher_score(query, positive) - teacher_score(query, negative)`。
- MS MARCO 风格蒸馏的常用配方。

## Listwise 损失

所有 listwise 损失都要求数据按 query 包含**列表**形式的候选 passage 和分数 —— 通常通过 collator 按 query 分组行。

> 下面 listwise 和 pairwise 损失也要求 `activation_fn=nn.Identity()`（见 Distillation 章节的 callout）。

### `LambdaLoss`

当前 SOTA 的 listwise 排序损失。通过加权 pairwise 比较优化 nDCG 的代理。

**数据形状**：每行 `(query, [doc1...docN], [score1...scoreN])`；一个 query、候选 doc 列表、平行相关性分数列表。用 `mine_hard_negatives(..., output_format="labeled-list", ...)` 从 `(query, positive)` 对构造这个形状。

```python
import torch.nn as nn
from sentence_transformers.cross_encoder.losses import LambdaLoss, NDCGLoss2PPScheme

model = CrossEncoder("...", num_labels=1, activation_fn=nn.Identity())
loss = LambdaLoss(model, weighting_scheme=NDCGLoss2PPScheme())
```

- 当每个 query 有多个候选和分级相关性时的强默认。
- `weighting_scheme`：`NDCGLoss2PPScheme`（默认）、`NDCGLoss2Scheme`、`LambdaRankScheme`。原 LambdaLoss 论文中 `NDCGLoss2PPScheme` 默认达到了最强性能。

#### LambdaLoss 特有的操作注意

- **OOM 恢复顺序**：先降 `mini_batch_size`（loss 内部 chunking 保留 K 列表语义），再降 `per_device_train_batch_size` 同时增 `gradient_accumulation_steps`，最后才考虑减小 K（per-query 候选列表长度）。降低 K 改变实验本身；其他两项不改变。
- **大 K 下 loss 数值很小是预期的。** 用 `NDCGLoss2PPScheme` 时，loss 会按 discount-weighted pair 数归一化 —— K=128 时 loss 数值上能缩到 ~`1e-4`。这并不是"训练坏了"；用 `eval_NanoBEIR_R100_mean_ndcg@10`（或你的等价指标）而不是训练 loss 来判断进度。
- 非常大的 K（>=128），每 query 的 O(K²) 权重 buffer 是在 forward chunking 之外物化的，所以单靠小 `mini_batch_size` 可能不够。可以考虑打分策略：top-K hard negative 通常胜过随机 K。

### `ListNetLoss`

把排序看作概率分布（通过 softmax），最小化与教师分布的交叉熵。

### `ListMLELoss`

对排列做最大似然估计。比 LambdaLoss 简单；不错的默认。

### `PListMLELoss`

位置感知的 ListMLE —— 给排名靠前的项更大权重。在 top-k 指标上常常优于纯 ListMLE。

### `RankNetLoss`

Pairwise 分类：对每对候选，通过交叉熵预测哪个排得更高。

- 比 LambdaLoss 简单、快。
- 与列表长度平方级扩展；长候选列表（>20）效果不好。

### `ADRMSELoss`

另一种 listwise 形式（Approx Discounted Rank MSE），来自 Rank-DistiLLM 论文。数据形状与 `LambdaLoss` 相同。实践中 LambdaLoss 是更强的默认；论文的 LLM 蒸馏设置中 `RankNetLoss` 略优于 ADRMSELoss（~0.002 nDCG@10），LambdaLoss 通常又优于两者。

任何对比重排器都离不开 hard-negative 挖掘（随机负例教不出东西）。见 `dataset_formats.md`（Hard-negative 挖掘章节）和 `../scripts/mine_hard_negatives.py`。

## 常见坑

- **没有 `pos_weight` 的 `BinaryCrossEntropyLoss`**，当每个正例配 5+ hard negative：loss 会欠权重正信号。设 `pos_weight=num_hard_negatives`。
- **`CachedMultipleNegativesRankingLoss` + `gradient_checkpointing=True`**：崩溃。二选一。
- **不同 query 列表长度差异巨大的 listwise 损失**：有些损失处理 ragged list 不行。pad 或截断到固定长度。
- **`MarginMSELoss` 缺预计算的教师分数差**：这个 loss 需要 `score_diff` 标签列由教师 pass 填充，它不会在内部调用教师。
- **用 `num_labels=1` 训交叉编码器后用 `CrossEntropyLoss`**：不匹配 —— BCE 对应 num_labels=1，CE 对应 num_labels>=2。
- **任何非 BCE 损失下默认的 `Sigmoid` 激活**：静默毁掉评估排名。给 `CrossEncoder(...)` 传 `activation_fn=torch.nn.Identity()` 用于蒸馏、listwise、pairwise 损失（BCE/CE 除外）。见 Distillation 和 Listwise 章节的 callout。
- **自定义 CE head 写到错误的 feature key**：自定义打分 head 必须填 `features["scores"]`（不是 `features["sentence_embedding"]`）。否则 `CrossEncoder.predict()` 推理时会抛 `KeyError: 'scores'`，即使训练成功。
- **从其它脚本加载带自定义类 head 的 CE 失败**：如果你在 `train.py` 里 `class ClassifierHead(nn.Module)` 内联定义了类并保存了模型，`modules.json` 会记录 `__main__.ClassifierHead`。从任何其它入口用 `CrossEncoder("path")` 加载时会抛 `ImportError: Module '__main__' does not define a 'ClassifierHead' attribute`。要么把类移到可 import 的文件（`my_pkg/heads.py`），要么用 ST 现成模块（`Dense + LayerNorm + Dense`）搭出相同形状，要么明确文档化模型只能从同一脚本加载。
