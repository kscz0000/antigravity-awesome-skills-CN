# 稀疏编码器损失（SPLADE）

所有损失位于 `sentence_transformers.sparse_encoder.losses`。

本参考针对 **SPLADE** 架构（Transformer + SpladePooling）。稀疏编码器包还导出 `CSRLoss` 和 `CSRReconstructionLoss` 用于 CSR 架构（Transformer + Pooling + SparseAutoEncoder）；那些不在本节范围内 —— 训练 CSR 模型请看 sbert.net 文档。

选择损失意味着 (a) 选一个 base loss（对比、回归、蒸馏），(b) 用 `SpladeLoss` 包装它以加 FLOPS 正则。

## 总览决策表

| 你拥有 | 用 |
|---|---|
| `(anchor, positive)` 或三元组，SPLADE 架构 | `SpladeLoss(loss=SparseMultipleNegativesRankingLoss(model), ...)` |
| 同上，想要 256+ 有效 batch | `CachedSpladeLoss(...)` |
| `(text1, text2, score)` 带标签对 | `SparseCoSENTLoss` 或 `SparseCosineSimilarityLoss` |
| 从交叉编码器教师蒸馏 | `SparseMarginMSELoss` |
| Listwise 蒸馏 | `SparseDistillKLDivLoss` |
| 显式三元组 | `SparseTripletLoss` |

## 核心包装：`SpladeLoss`

`SpladeLoss` 在另一个稀疏损失之上加 **FLOPS 正则**。FLOPS 正则惩罚非零激活，让嵌入真正稀疏。

```python
loss = SpladeLoss(
    model=model,
    loss=SparseMultipleNegativesRankingLoss(model=model),
    query_regularizer_weight=5e-5,
    document_regularizer_weight=3e-5,
)
```

- `query_regularizer_weight`：对 query 嵌入中非零项的惩罚强度。
- `document_regularizer_weight`：对 document 同上。
- 典型范围：1e-5 到 1e-4。越大 = 嵌入越稀疏，recall 越低；越小 = 越稠密，可能 recall 更好。
- `SparseEncoderTrainer` 在损失是 `SpladeLoss` 时会自动注册 `SpladeRegularizerWeightSchedulerCallback`。回调会把权重在前 ~33% 训练中从 0 ramp 到目标值；默认 shape 是 `SchedulerType.QUADRATIC`（非线性）。ramp 长度和 shape 在 callback 上配置（`SpladeRegularizerWeightSchedulerCallback(loss=..., warmup_ratio=..., scheduler_type=...)`），不在 `SpladeLoss` 上；要覆盖就自己实例化 callback，通过 `callbacks=[...]` 传入。这个 ramp 很重要；从第 0 步就用全正则会卡住学习。

GradCache 变体用 `CachedSpladeLoss`。

## 对比损失（无标签）

### `SparseMultipleNegativesRankingLoss`

双编码器 MNRL 的稀疏版。batch 内对比。

```python
inner = SparseMultipleNegativesRankingLoss(model=model)
loss = SpladeLoss(model=model, loss=inner, query_regularizer_weight=5e-5, document_regularizer_weight=3e-5)
```

- **始终用 `SpladeLoss` 包装**（SPLADE 架构下）。
- 训练参数上设 `batch_sampler=BatchSamplers.NO_DUPLICATES`。

### `SparseTripletLoss`

基于显式 `(anchor, positive, negative)` 的经典三元组 margin 损失。

## 带标签回归损失

### `SparseCoSENTLoss`

`(text1, text2, score)` 的 pairwise 排序损失。对应双编码器 `CoSENTLoss`。

### `SparseCosineSimilarityLoss`

cosine 相似度上的 MSE。简单，通常不如 CoSENT。

### `SparseAnglELoss`

复数空间中基于角度的损失。CoSENT 的替代。

## 蒸馏损失

### `SparseMSELoss`

嵌入 MSE。学生稀疏嵌入应匹配教师嵌入。

- **数据**：`(text, teacher_embedding)`。
- 教师可以是稠密双编码器或另一个稀疏模型。

### `SparseMarginMSELoss`

来自交叉编码器教师的 margin MSE。

- **数据**：`(query, positive, negative, score_diff)`，其中 `score_diff = teacher_score(query, positive) - teacher_score(query, negative)`。
- 从交叉编码器标签训练 SPLADE 的典型配方（ms-marco 蒸馏）。
- SPLADE 场景下用 `SpladeLoss(model, loss=SparseMarginMSELoss(model), ...)` 包装。

### `SparseDistillKLDivLoss`

Listwise KL 散度蒸馏 —— 学生在候选上的 softmax 分布应匹配教师。

## 独立正则

### `FlopsLoss`

独立 FLOPS 正则。通常通过 `SpladeLoss` 用，而不是直接用。

正则权重调节和稠密输出恢复，见 `troubleshooting.md`（"SPLADE 嵌入太稠密"）。MLM head 要求：`base_model_selection.md`（SPARSE 章节）。active-dim 稀疏度目标和监控方法：`evaluators_sparse_encoder.md`（稀疏度跟踪）。

## 常见坑

- **SPLADE 模型上的 `SparseMultipleNegativesRankingLoss` 不被 `SpladeLoss` 包装**：没有 FLOPS 正则 -> 稠密输出，SPLADE 失去意义。始终包装。
- **`CachedSpladeLoss` + `gradient_checkpointing=True`**：崩溃。二选一。
- **训练从第 0 步就用全 FLOPS 正则**：模型各处输出 0 并卡住。内置调度器已避免这点 —— 除非知道原因，不要覆盖。
- **`query_regularizer_weight` == `document_regularizer_weight`**：通常不对。query 应比 doc 更稀疏（每 query 项更少）。正则越大驱动越多零，所以 query 权重取较大值。`query_regularizer_weight=5e-5`、`document_regularizer_weight=3e-5` 是好的起始比例。
