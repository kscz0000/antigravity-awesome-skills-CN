# 评估器（稀疏编码器）

所有稀疏编码器评估器位于 `sentence_transformers.sparse_encoder.evaluation`。它们是双编码器版本的镜像，带 `Sparse` 前缀，默认使用 **dot product** 相似度（cosine 在稀疏向量上意义不大）。

## 选择合适的评估器

| 任务 | 评估器 |
|---|---|
| 检索（nDCG、MRR、Recall）—— 快速默认 | `SparseNanoBEIREvaluator` |
| 在自己的语料 / qrels 上检索 | `SparseInformationRetrievalEvaluator` |
| STS / 连续相似度 | `SparseEmbeddingSimilarityEvaluator` |
| 二分类 | `SparseBinaryClassificationEvaluator` |
| 三元组准确率 | `SparseTripletEvaluator` |
| 重排（基于检索候选） | `SparseRerankingEvaluator` |
| 与教师的 MSE（蒸馏） | `SparseMSEEvaluator` |
| 翻译（跨语言对齐） | `SparseTranslationEvaluator` |
| BM25 + 稀疏混合检索 | `ReciprocalRankFusionEvaluator` |

用 `SequentialEvaluator`（来自 `sentence_transformers.base.evaluation`）把多个包起来：

```python
from sentence_transformers.base.evaluation import SequentialEvaluator
evaluator = SequentialEvaluator([sparse_nano_beir, my_custom_ir])
```

## 默认值：`SparseNanoBEIREvaluator`

BEIR 的小子集，为稀疏检索做了适配。中端 GPU 上通常 <1 分钟跑完。

```python
from sentence_transformers.sparse_encoder.evaluation import SparseNanoBEIREvaluator

evaluator = SparseNanoBEIREvaluator(
    dataset_names=["msmarco", "nfcorpus", "nq"],   # default: all 13 NanoBEIR datasets
    batch_size=32,
    show_progress_bar=False,
)
```

`metric_for_best_model` 的输出键： **`eval_NanoBEIR_mean_dot_ndcg@10`**（稀疏默认 = dot product）。

### 稀疏度跟踪

与稠密版本不同，稀疏评估器还会报告 **active dim 数量**，便于训练中监控稀疏度：

- `query_active_dims` —— 每个 query 向量的非零条目数
- `document_active_dims` —— 每个 doc 向量的非零条目数

健康的 SPLADE 检查点通常 query 约 30–50 个 active dim，doc 约 150–250 个。如果这些值漂向词表大小（~30k），说明 FLOPS 正则没起作用 —— 调高 `SpladeLoss` 中的 `query_regularizer_weight` / `document_regularizer_weight`。

## 在自己的语料上检索

### `SparseInformationRetrievalEvaluator`

与稠密版形状相同，但内部处理稀疏向量：

```python
from sentence_transformers.sparse_encoder.evaluation import SparseInformationRetrievalEvaluator

evaluator = SparseInformationRetrievalEvaluator(
    queries={qid: text for qid, text in ...},
    corpus={doc_id: text for doc_id, text in ...},
    relevant_docs={qid: {doc_id, ...} for qid in ...},
    name="my-sparse-ir",
    ndcg_at_k=[10],
    mrr_at_k=[10],
    accuracy_at_k=[1, 5, 10],
    map_at_k=[100],
    batch_size=32,
)
```

输出键：`eval_{name}_dot_ndcg@10`、`eval_{name}_dot_mrr@10` 等。也会报告 active-dims。

大语料很重。训练中用 `SparseNanoBEIREvaluator`；完整 IR 留给训练后。

## 混合检索

### `ReciprocalRankFusionEvaluator`

衡量把你的稀疏编码器与 BM25（或任何其他 retriever）通过 reciprocal-rank fusion 组合后的表现。当实际部署目标是混合系统时很有用。

## 其它稀疏评估器

### `SparseEmbeddingSimilarityEvaluator`

STS 风格。计算稀疏向量相似度与 gold 标签的 Pearson/Spearman。默认用 dot product。

### `SparseBinaryClassificationEvaluator`

用于带标签配对分类（稀疏嵌入）。

### `SparseTripletEvaluator`

用于 `(anchor, positive, negative)` 三元组 —— 报告 positive 比 negative 更靠近 anchor（按 dot product）的比例。

### `SparseRerankingEvaluator`

用于自定义重排（稀疏嵌入）。语义与稠密 `RerankingEvaluator` 相同。

### `SparseMSEEvaluator`

用于蒸馏场景。比较稀疏学生嵌入与教师输出。

### `SparseTranslationEvaluator`

用于跨语言 / `make_multilingual` 风格的对齐检查（稀疏嵌入）。

## 编写 `metric_for_best_model`

模式：`f"eval_{evaluator.primary_metric}"`。构造完后检查：`print(evaluator.primary_metric)`。常见取值：
- `eval_NanoBEIR_mean_dot_ndcg@10` —— `SparseNanoBEIREvaluator` 默认
- `eval_{name}_dot_ndcg@10` —— `SparseInformationRetrievalEvaluator`
- `eval_{name}_spearman_dot` —— `SparseEmbeddingSimilarityEvaluator`

## 常见坑

- **训练前始终先跑一次 `evaluator(model)`** —— 确认流水线能跑（fill-mask 基座在训练前检索得分 ~0）。
- 稀疏评估器默认 dot product；cosine 在稀疏向量上无意义。
- 不要直接比较稠密和稀疏指标 —— 量纲不同（cosine ∈ [-1, 1] vs. dot ∈ [0, ∞)）。
- 始终检查 `query_active_dims` / `document_active_dims` —— 每个 doc 几千个 active dim 意味着 FLOPS 正则没调好，即使 nDCG 看起来还行。
