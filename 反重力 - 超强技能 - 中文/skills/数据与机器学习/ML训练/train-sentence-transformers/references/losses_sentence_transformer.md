# 双编码器损失（SentenceTransformer）

所有损失位于 `sentence_transformers.sentence_transformer.losses`。

损失按数据形状分组。首要规则：**选择与数据匹配的损失**，而不是反过来。

## 总览决策表

| 你拥有 | 用 |
|---|---|
| `(anchor, positive)` 对 | `MultipleNegativesRankingLoss`（或 Cached 变体用于大 batch） |
| `(anchor, positive, negative)` 三元组 | `MultipleNegativesRankingLoss` —— 原生支持三元组 |
| `(text1, text2, score)`，`score ∈ [-1, 1]` 或 `[0, 1]` | `CoSENTLoss`（强烈推荐） |
| `(text1, text2, label)`，`label ∈ {0, 1}` | `OnlineContrastiveLoss` |
| `(text, class_id)` 单列 + 整数类别 | `BatchAllTripletLoss` |
| `(query, positive, negative, score_diff)` | `MarginMSELoss`（蒸馏） |
| `(text, teacher_embedding)` | `MSELoss`（嵌入蒸馏） |
| 一次训练得到多个输出维度 | 用 `MatryoshkaLoss` 包装上述任一 |
| 完全没有标签，只有句子 | `DenoisingAutoEncoderLoss` 或 `ContrastiveTensionLossInBatchNegatives` |

## 对比损失（对 + 三元组，无标签）

### `MultipleNegativesRankingLoss`（MNRL）

默认的双编码器损失。使用 **batch 内负例**：batch 中每个其他 `positive` 都作为当前 `anchor` 的负例。

```python
loss = MultipleNegativesRankingLoss(model, scale=20.0)  # similarity_fct defaults to cos_sim
```

- **数据**：`(anchor, positive)` 或 `(anchor, positive, negative)`。列越多 = 每行显式 hard negative 越多。
- **Scale**：温度。默认 `scale=20.0` 把相似度放大 20 倍（等价于 softmax 温度 0.05）。仅当 cosine 相似度饱和时才调。
- **关键**：在训练参数上设 `batch_sampler=BatchSamplers.NO_DUPLICATES`。否则重复 anchor 会产生假负例。
- **提示**：batch 大小影响很大 —— batch 内负例越多 = 梯度越丰富。

### `CachedMultipleNegativesRankingLoss`

相同损失，但带 gradient caching（GradCache）：按 mini-batch 前向，但在完整 batch 上计算对比损失。当你想要 256+ 的有效 batch 但 GPU 只能装 32 个 forward 时用这个。

```python
loss = CachedMultipleNegativesRankingLoss(model, mini_batch_size=32)
```

- **与 `gradient_checkpointing=True` 不兼容**。
- 把 `mini_batch_size` 设成"如果不能用这个的话"对应的 `per_device_train_batch_size`。再把实际 `per_device_train_batch_size` 拉到你想要的有效 batch（256+、1024+）。

### `MultipleNegativesSymmetricRankingLoss`

MNRL 双向计算 —— 从 (anchor -> positive) 和 (positive -> anchor) 两个方向对正例打分。在"anchor"和"positive"区分较软（释义、去重）的检索任务上略好。

### `CachedMultipleNegativesSymmetricRankingLoss`

上述的 Cached 版本。

### `GISTEmbedLoss`

类似 MNRL，但用一个 **guide model**（独立的预训练 Sentence Transformer）在计算对比损失前 **过滤假负例**。guide model 给每个潜在负例打分；如果它看起来太像正例，就排除。

```python
guide = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
loss = GISTEmbedLoss(model, guide=guide)
```

- 贵：guide model 每 batch 做一次 forward。
- batch 内负例噪声大时强（小语料，多近重复）。

### `CachedGISTEmbedLoss`

Cached + GIST。

### `MegaBatchMarginLoss`

基于 batch 内 margin 的三元组：对每个 anchor 找 batch 中最难负例并施加 margin 损失。老范式，通常被 MNRL 超过。

### `TripletLoss`

经典三元组 margin 损失，基于显式 `(anchor, positive, negative)`。使用固定 margin，不考虑 batch 内最难 —— 只有给的三元组。

```python
loss = TripletLoss(model, distance_metric=TripletDistanceMetric.EUCLIDEAN, triplet_margin=5)
```

- 比 MNRL 简单；当 batch 中有有用的负例时没那么强。
- 适合有 *可信* 预挖掘三元组、想避免 batch 内噪声的场景。

## Batch 三元组损失（单列 + 整数标签）

这些在 batch 内从共享标签的样本中挖掘三元组。

### `BatchAllTripletLoss`

对每个 anchor，用 batch 中所有正/负组合形成三元组。每 batch 信号最大。

```python
loss = BatchAllTripletLoss(model, margin=5)
```

- **数据**：单个 text 列 + 整数 `label`。需要每 batch 中同一标签出现多次（设 `batch_sampler=BatchSamplers.GROUP_BY_LABEL`）。

### `BatchHardTripletLoss`

同上，但每 anchor 只取单个最难正例 + 最难负例。

### `BatchSemiHardTripletLoss`

Semi-hard 挖掘：负例比正例难但比 margin 易。通常比完全 hard 更稳定。

### `BatchHardSoftMarginTripletLoss`

用 soft margin（log-sum-exp）代替固定 margin hinge 的变体。

**何时用 batch 三元组损失**：分类式数据集（标签是类别 ID，不是对标注）。例如"训练一个 embedder 让同类样本近"。

## 打分回归损失（带标签对，浮点分数）

### `CoSENTLoss`

`(text1, text2, score)` 的 **推荐回归损失**。按 pairwise 排序训练：任意两对 `(a, b)` 与 `(c, d)`，若 `score(a,b) > score(c,d)`，模型应对 `(a, b)` 打更高分。比平方误差好得多。

```python
loss = CoSENTLoss(model, scale=20.0)
```

- **数据**：`(text1, text2, float_score)`。标签可 `[0, 1]` 或 `[-1, 1]`。
- 小数据集（STS-B，5k 对）上表现也好。

### `AnglELoss`

类似 CoSENT 但在复数空间用基于角度的优化。在有细粒度相似度等级的任务上偶尔超过 CoSENT。强替代。

### `CosineSimilarityLoss`

在 cosine 相似度上的平方误差损失：`mse(cos(text1, text2), label)`。比 CoSENT 简单，通常更差。留给遗留 / 复现用。

## 对比带标签损失（带标签对，二值标签）

### `ContrastiveLoss`

用于 `(text1, text2, label)`，`label ∈ {0, 1}`。对正例最小化距离；把负例推过 margin。

```python
loss = ContrastiveLoss(model, margin=0.5, distance_metric=SiameseDistanceMetric.COSINE_DISTANCE)
```

### `OnlineContrastiveLoss`

同样设置但 **忽略"简单"对**（正例已经近、负例已经远的）只优化难例。对标签噪声稳健得多。

```python
loss = OnlineContrastiveLoss(model, margin=0.5)
```

**大多数实际带标签对数据集上优于 `ContrastiveLoss`**。

### `SoftmaxLoss`

在拼接的 `(u, v, |u-v|)` 嵌入上加分类头，用交叉熵训练。有 NLI 风格多分类标签（entailment / neutral / contradiction）并想要分类损失时有用。历史地位重要（早期流行句嵌入模型就是它训出来的），但 **通常被 MNRL 超过**。

## 蒸馏损失

### `MSELoss`

把学生嵌入回归到教师嵌入。

- **数据**：`(text, teacher_embedding)`。教师嵌入是每行固定的向量。
- 从更大双编码器蒸馏到小的双编码器时用。

### `MarginMSELoss`

用于 `(query, positive, negative, score_diff)`：最小化 `mse(student_score_diff, teacher_score_diff)`。教师通常是产出分数差的交叉编码器。

- **数据**：3 个 text 列 + 1 个 float 列。
- 用交叉编码器教师训练稠密检索器的主力（ms-marco 蒸馏）。

### `DistillKLDivLoss`

KL 散度蒸馏：学生 softmax 分布应匹配教师。

- **数据**：`(query, passages[], teacher_scores[])`。
- 适合每个 query 有多个候选的 listwise 蒸馏。

端到端模式见 `../scripts/train_sentence_transformer_distillation_example.py`（docstring 涵盖 Embedding MSE / Margin MSE / Listwise KL 的完整配方）。

## 正则 / 包装损失

这些没有自己的数据形状 —— 包装另一个损失并加正则目标。

### `MatryoshkaLoss`

**一次训练**，可部署到任意几个维度。包装任意损失，在多个截断维度上计算它并加权求和。

```python
base_loss = MultipleNegativesRankingLoss(model)
loss = MatryoshkaLoss(
    model,
    base_loss,
    matryoshka_dims=[768, 512, 256, 128, 64],
    matryoshka_weights=[1, 1, 1, 1, 1],   # relative weighting per dim
)
```

- 推理时 `SentenceTransformer(..., truncate_dim=128)` 给出 128 维输出，保留 ~95% 全量质量。
- 默认 matryoshka_dims：选你希望部署的维度。更小维度换更高压缩，代价是质量略降。

### `Matryoshka2dLoss`

2D-Matryoshka：在单个包装里同时减 **维度** 和 transformer 层数。内部组合 `MatryoshkaLoss` + `AdaptiveLayerLoss`，所以只需这一个（不要自己再套 `AdaptiveLayerLoss`）。推理时可部署到任意 (dim, layer) 组合。

### `AdaptiveLayerLoss`

包装任意损失；加一项让 transformer 每层都成为有效 exit point。推理时用更少层加速编码。

```python
loss = AdaptiveLayerLoss(
    model,
    base_loss,
    n_layers_per_step=1,
    last_layer_weight=1.0,
    prior_layers_weight=1.0,
)
```

### `GlobalOrthogonalRegularizationLoss`（GOR）

独立正则（不是包装，尽管放在本节）。惩罚点积偏离正交的嵌入对，鼓励模型把嵌入分散到整个向量空间。配合主对比损失用（自己在训练 step 中把两者相加），可提升下游检索多样性。

## 无监督损失

### `DenoisingAutoEncoderLoss`（TSDAE）

句子级降噪自编码器：损坏一个句子（丢 token），让模型重建。预训练风格 —— 在有未标领域内句子、要做领域适配时有用。

### `ContrastiveTensionLoss`

无监督对比：模型的两个副本编码同一句子；它们应一致。纯自监督。

### `ContrastiveTensionLossInBatchNegatives`

带 batch 内负例的 CT。比 vanilla CT 强。

## 常见坑

- **`MultipleNegativesRankingLoss` 不设 `BatchSamplers.NO_DUPLICATES`** 会把重复 anchor 放进同一 batch，毁掉训练信号。始终设采样器。
- **任何 `Cached*` 损失 + `gradient_checkpointing=True` = 崩溃**。二选一。
- **坏负例的 `TripletLoss`**（太简单）= loss 快速降到 0，模型停止学习。先挖掘 hard negative。
- **Matryoshka 包装 `CachedMultipleNegativesRankingLoss`**：支持，但 cached 损失的 mini-batch 语义只作用于 base loss。三思后再组合。
