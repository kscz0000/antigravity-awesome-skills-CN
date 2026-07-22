# 数据集格式

本参考涵盖：数据集如何映射到损失、数据不匹配时如何 reshape、以及如何挖掘 hard negative。

## 两条规则

来自 sentence-transformers 训练概览：

1. 如果损失需要标签，数据集必须包含名为 **`label`、`labels`、`score` 或 `scores`** 的列。任何同名列都会被视作标签。
2. 其余列都是 **输入**。损失决定它期望多少输入列。**列名无关，列序有关**。

示例：`CoSENTLoss` 期望 2 个输入 + 一个 float 标签。列名为 `["premise", "hypothesis", "score"]` 的数据集可用。列名为 `["score", "premise", "hypothesis"]` 不可用 —— 必须先重排。

## 按损失划分的数据形状

按类型划分的损失参考（`losses_sentence_transformer.md`、`losses_cross_encoder.md`、`losses_sparse_encoder.md`）是数据形状到损失的标准映射。跨损失的细节补充（表格中没列的）：

- **`CosineSimilarityLoss`** 要求 `score` 归一化到 `[0, 1]`；`CoSENTLoss` / `AnglELoss` 是 pairwise-ranking，忽略绝对量级，所以 `stsb`（原始 0–5）只有用 cosine-similarity 时才除以 5。
- **`BatchAllTripletLoss` / `BatchHardTripletLoss` / `BatchSemiHardTripletLoss`** 需要 `batch_sampler=BatchSamplers.GROUP_BY_LABEL`，让同一 batch 中同一标签出现多次。
- **`MSELoss`（蒸馏）** 的标签是教师的完整嵌入向量（float 列表），不是标量分数。
- **`MarginMSELoss`（蒸馏）** 的标签是 `teacher_score(q, pos) - teacher_score(q, neg)`，按行预计算。
- MNRL 的 **N-tuple 形状** `(anchor, positive, negative_1, negative_2, ..., negative_N)`（1-indexed）由 `mine_hard_negatives(..., output_format="n-tuple")` 产生；`"labeled-list"` 输出格式产生 CrossEncoder 的 listwise 形状。

## Reshape 操作

如果数据不符合损失的期望形状：

### 重排列

```python
# Columns are ["hypothesis", "premise", "score"] but CoSENTLoss expects premise first.
dataset = dataset.select_columns(["premise", "hypothesis", "score"])
```

### 重命名标签列

```python
# Your label is called "relevance" but ST wants "label".
dataset = dataset.rename_column("relevance", "label")
```

### 去掉多余列

```python
# ST will treat every non-label column as an input. Drop metadata.
dataset = dataset.remove_columns(["source_id", "created_at", "language"])
```

### 转换 dtype

```python
# Label is str, need float for CoSENTLoss.
dataset = dataset.map(lambda x: {"label": float(x["label"])})
```

## Hard-negative 挖掘

`mine_hard_negatives`（位于 `sentence_transformers.util`）使用一个 retriever 产生带挖掘 negative 的训练数据集。Hard negative 是检索模型质量最高杠杆的单一手段。

### 基本用法

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import mine_hard_negatives

retriever = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

mined = mine_hard_negatives(
    dataset=train_pairs,                # has (anchor, positive) or (q, a) columns
    model=retriever,
    num_negatives=5,
    range_min=0, range_max=100,         # rank window to sample hard negatives from
    sampling_strategy="top",            # "top" = rank-1 hardest; "random" = random in window
    output_format="n-tuple",            # "triplet" | "n-tuple" | "labeled-pair" | "labeled-list"
    use_faiss=True,
)
```

### 输出格式

- `"triplet"` —— `(anchor, positive, negative)` 三元组。每个 `(query, negative)` 对一行。
- `"n-tuple"` —— `(anchor, positive, negative_1, negative_2, ..., negative_N)`（1-indexed）—— 每个 query 一行。
- `"labeled-pair"` —— `(anchor, text, label)`，正例 `label=1`，负例 `label=0`。适合 `BinaryCrossEntropyLoss`。
- `"labeled-list"` —— `(anchor, texts, labels)` —— 每个 query 一行，包含候选列表。适合 listwise 损失。

### 过滤假负例

如果 retriever 返回的"负例"其实是相关的，它们就成了假负例，伤害训练。过滤掉：

```python
mined = mine_hard_negatives(
    dataset=train_pairs,
    model=retriever,
    cross_encoder=CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2"),   # score candidates
    num_negatives=5,
    max_score=0.9,                      # drop candidates scoring above 0.9
    relative_margin=0.05,               # require neg_score < pos_score * (1 - 0.05)
    absolute_margin=0.2,                # require neg_score < pos_score - 0.2
    output_format="n-tuple",
    use_faiss=True,
)
```

**`relative_margin` 和 `absolute_margin` 二选一**，通常不要同时用。`max_score` 作为硬上限独立有用。

### CLI

`scripts/mine_hard_negatives.py` 是 CLI 封装 —— 直接看它就能拿到可运行命令。

## 选择合适的 `range_min` / `range_max`

`range_max=None` 是默认；传一个整数来限制从排名列表往下采样的范围。

- `range_min=0`、`range_max=100` —— 从检索 top-100 中采样。不错的默认。
- `range_min=10`、`range_max=100` —— 跳过 top-10（常含真正正例）。没有 cross-encoder 时更稳。
- `range_min=0`、`range_max=1000` —— 撒得更广，负例更多样，更慢。
- `sampling_strategy="top"` —— 总是挑 rank-1 最难。每行训练信号最大。
- `sampling_strategy="random"` —— 在范围内随机选。retriever 本身噪声大时更稳。

## 快速 Hub 端数据集检查

`hf datasets sql "SELECT * FROM 'hf://datasets/<id>/<split>' LIMIT 5"` 通过 DuckDB 流式取行而无需 `load_dataset(...)` —— 在完整验证运行前确认列名匹配的最快方式。`hf datasets info <id>` 显示 config / splits / size；`hf datasets card <id> --text` 渲染 README。

## 常见坑

- **`remove_unused_columns=True`（默认）**：trainer 会丢掉没传给 model forward 的列。一般没问题，但如果依赖使用元数据列的自定义 collator，请设 `remove_unused_columns=False`。
- **CSV 加载后浮点变成字符串**：`load_dataset("csv", ...)` 默认保留列类型为 str。用 `.map(lambda x: {"label": float(x["label"])}` 转换。
- **`include_positives=True` 的挖掘 hard negative** 会把正例也作为负例放进输出列表 —— 只有在构建 evaluator 或想衡量正例的排名时有用。训练时保持 `False`。
