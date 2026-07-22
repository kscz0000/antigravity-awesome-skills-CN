# 评估器（交叉编码器）

所有交叉编码器评估器位于 `sentence_transformers.cross_encoder.evaluation`。

## 选择合适的评估器

| 任务 | 评估器 |
|---|---|
| 重排检索结果（在 BM25 top-N 上 nDCG@k）—— 快速默认 | `CrossEncoderNanoBEIREvaluator` |
| 每个 query 自定义候选的重排 | `CrossEncoderRerankingEvaluator` |
| 二分类 / 多分类配对分类 | `CrossEncoderClassificationEvaluator` |
| 连续配对打分（STS 风格） | `CrossEncoderCorrelationEvaluator` |

用 `SequentialEvaluator`（来自 `sentence_transformers.base.evaluation`）把多个评估器包起来一起跟踪：

```python
from sentence_transformers.base.evaluation import SequentialEvaluator
evaluator = SequentialEvaluator([nano_beir_eval, custom_rerank_eval])
```

## 默认值：`CrossEncoderNanoBEIREvaluator`

对应重排器的 `NanoBEIREvaluator`。取每个 NanoBEIR query 的 BM25 top-100，衡量交叉编码器对它们的重排效果。

```python
from sentence_transformers.cross_encoder.evaluation import CrossEncoderNanoBEIREvaluator

evaluator = CrossEncoderNanoBEIREvaluator(
    dataset_names=["msmarco", "nfcorpus", "nq"],   # default: 11 of 13 NanoBEIR datasets (excludes "arguana", "touche2020")
    batch_size=64,
    rerank_k=100,                                   # rerank the BM25 top-K
)
```

`metric_for_best_model` 的输出键： **`eval_NanoBEIR_R100_mean_ndcg@10`**。`R100` 表示"重排 top-100"；改 `rerank_k` 时前缀会变（例如 `R50`）。

每个独立数据集也会贡献 `eval_Nano{DatasetName}_R100_ndcg@10`（例如 `eval_NanoMSMARCO_R100_ndcg@10`）。

## 用自己的候选做自定义重排

当你有 query + positive + distractor 候选，且不在 NanoBEIR 中时使用：

```python
from sentence_transformers.cross_encoder.evaluation import CrossEncoderRerankingEvaluator

samples = [
    {"query": "...", "positive": ["the gold answer"], "documents": ["...", "...", ...]}
    for ...
]

evaluator = CrossEncoderRerankingEvaluator(
    samples=samples,
    batch_size=64,
    name="my-rerank",
    always_rerank_positives=False,   # default is True; override to False for realistic eval
)
```

- `always_rerank_positives=True`（库默认）会强制把 positive 放进候选池，即使 retriever 没找到。重排器只对实际能打分的候选打分，所以指标反映的是纯粹的重排器质量。
- `always_rerank_positives=False`：positive 只有在 `documents` 中才会被重排。如果 retriever 漏了，排名记为 N+1。这反映端到端 retriever+reranker 质量。retriever 漏掉的话，再强的 reranker 也没用。

输出键：`eval_{name}_ndcg@10`、`eval_{name}_map`、`eval_{name}_mrr@10`。

## 分类式交叉编码器

### `CrossEncoderClassificationEvaluator`

同时支持二分类（`num_labels=1`）和多分类（`num_labels>=2`）的交叉编码器。内部分支：
- `num_labels=1`：二分类模式。扫描阈值后报告 accuracy、F1、precision、recall 和 **average_precision**（主要）。
- `num_labels>=2`：多分类模式（如 NLI：entailment / neutral / contradiction）。报告 **f1_macro**（主要）、f1_micro、f1_weighted，以及每类的 precision / recall。

```python
from sentence_transformers.cross_encoder.evaluation import CrossEncoderClassificationEvaluator

evaluator = CrossEncoderClassificationEvaluator(
    sentence_pairs=[(premise, hypothesis), ...],
    labels=[0, 1, 2, ...],
    batch_size=64,
    name="nli-dev",
)
```

输出键（二分类，`num_labels=1`）：`eval_{name}_accuracy`、`eval_{name}_f1`、`eval_{name}_average_precision`（主要）。
输出键（多分类，`num_labels>=2`）：`eval_{name}_f1_macro`（主要）、`eval_{name}_f1_micro`、`eval_{name}_f1_weighted`。

### `CrossEncoderCorrelationEvaluator`

用于连续分数的交叉编码器（如输出相似度的 STS 交叉编码器）。报告与 gold 分数的 Pearson/Spearman 相关系数。

```python
from sentence_transformers.cross_encoder.evaluation import CrossEncoderCorrelationEvaluator

evaluator = CrossEncoderCorrelationEvaluator(
    sentence_pairs=[(a, b), ...],
    scores=[0.4, 0.8, ...],
    name="stsb-dev",
)
```

输出键：`eval_{name}_spearman`、`eval_{name}_pearson`。

## 编写 `metric_for_best_model`

模式：`f"eval_{evaluator.primary_metric}"`。构造完后检查：`print(evaluator.primary_metric)`。常见取值：
- `eval_NanoBEIR_R100_mean_ndcg@10` —— `CrossEncoderNanoBEIREvaluator` 默认
- `eval_{name}_ndcg@10` —— `CrossEncoderRerankingEvaluator`
- `eval_{name}_average_precision` —— `CrossEncoderClassificationEvaluator`（二分类，`num_labels=1`）
- `eval_{name}_f1_macro` —— `CrossEncoderClassificationEvaluator`（多分类，`num_labels>=2`）
- `eval_{name}_spearman` —— `CrossEncoderCorrelationEvaluator`

## 常见坑

- **训练前始终先跑一次 `evaluator(model)`** —— 预训练基线。训练后增量很小说明损失/数据/基座有问题。
- `CrossEncoderClassificationEvaluator` 同时接受 `num_labels=1`（二分类，主要 `average_precision`）和 `num_labels>=2`（多分类，主要 `f1_macro`）；`CrossEncoderCorrelationEvaluator` 要求 `num_labels=1`。
- 默认的 `dataset_names=None` 排除了 `arguana` 和 `touche2020`（Argument-Retrieval 任务与其它不同）；传 `dataset_names=list(DATASET_NAME_TO_HUMAN_READABLE)`（来自 `sentence_transformers.cross_encoder.evaluation.nano_beir`）才能真正跑全 13 个。
- 训练时使用 NanoBEIR 的子集（3–4 个）以保持评估廉价；训练后跑全量。
