# 评估器（双编码器）

所有双编码器评估器位于 `sentence_transformers.sentence_transformer.evaluation`。

## 选择合适的评估器

| 任务 | 评估器 |
|---|---|
| 检索（nDCG、MRR、Recall）—— 快速默认 | `NanoBEIREvaluator` |
| 在自己的语料 / qrels 上检索 | `InformationRetrievalEvaluator` |
| STS / 连续相似度 | `EmbeddingSimilarityEvaluator` |
| 二分类 | `BinaryClassificationEvaluator` |
| 三元组准确率 | `TripletEvaluator` |
| 重排（基于检索候选） | `RerankingEvaluator` |
| 与教师的 MSE（蒸馏） | `MSEEvaluator`、`MSEEvaluatorFromDataFrame` |
| 释义挖掘 | `ParaphraseMiningEvaluator` |
| 翻译（跨语言对齐） | `TranslationEvaluator` |
| 标签准确率（训练中分类） | `LabelAccuracyEvaluator` |

用 `SequentialEvaluator` 把多个评估器包起来一起跟踪：

```python
from sentence_transformers.sentence_transformer.evaluation import SequentialEvaluator
evaluator = SequentialEvaluator([evaluator1, evaluator2, evaluator3])
```

## 三大主力

### `NanoBEIREvaluator`（检索）

BEIR 的小子集，速度快。中端 GPU 上通常 <1 分钟跑完。检索训练的默认选择。

```python
from sentence_transformers.sentence_transformer.evaluation import NanoBEIREvaluator

evaluator = NanoBEIREvaluator(
    dataset_names=["msmarco", "nfcorpus", "nq"],   # default: all 13 NanoBEIR datasets
    batch_size=128,
    show_progress_bar=False,
)
```

- 默认数据集列表覆盖 13 个任务；训练中为速度可以选子集。
- `metric_for_best_model` 的输出键： **`eval_NanoBEIR_mean_cosine_ndcg@10`**（双编码器默认 = cosine 相似度）。

### `EmbeddingSimilarityEvaluator`（STS 风格）

计算模型 cosine 相似度与 gold 标签之间的 Pearson/Spearman 相关系数。

```python
from sentence_transformers.sentence_transformer.evaluation import EmbeddingSimilarityEvaluator
from sentence_transformers.util.similarity import SimilarityFunction

evaluator = EmbeddingSimilarityEvaluator(
    sentences1=stsb["sentence1"],
    sentences2=stsb["sentence2"],
    scores=stsb["score"],
    main_similarity=SimilarityFunction.COSINE,
    name="sts-dev",
)
```

- `main_similarity` 可为 `COSINE`、`DOT_PRODUCT`、`EUCLIDEAN`、`MANHATTAN`。
- `name` 用于输出键：`eval_sts-dev_spearman_cosine`、`eval_sts-dev_pearson_cosine` 等。

### `InformationRetrievalEvaluator`（完整检索）

当你有**自己**的语料 + queries + qrels（不是 NanoBEIR 任务）时使用。

```python
from sentence_transformers.sentence_transformer.evaluation import InformationRetrievalEvaluator

evaluator = InformationRetrievalEvaluator(
    queries={qid: query_text for qid, query_text in ...},
    corpus={doc_id: doc_text for doc_id, doc_text in ...},
    relevant_docs={qid: {doc_id, ...} for qid in ...},   # qid -> set of relevant doc_ids
    name="my-retrieval",
    mrr_at_k=[10],
    ndcg_at_k=[10],
    accuracy_at_k=[1, 5, 10],
    precision_recall_at_k=[1, 5, 10],
    map_at_k=[100],
    show_progress_bar=False,
    batch_size=64,
)
```

输出键：`eval_{name}_cosine_ndcg@10`、`eval_{name}_cosine_mrr@10` 等。

大语料很重 —— 每次评估都要对全量语料编码。不要每 100 步跑一次。训练中频繁评估用 `NanoBEIREvaluator`，完整 IR 留给里程碑 / 训练后。

## 其它双编码器评估器

### `BinaryClassificationEvaluator`

用于带标签的配对分类（如去重检测、二分类蕴含）。报告 accuracy、F1、precision/recall、AP。支持所有距离指标 —— 对每个指标找最优阈值。

### `TripletEvaluator`

用于 `(anchor, positive, negative)` 三元组。报告 positive 比 negative 更靠近 anchor 的三元组比例。

### `RerankingEvaluator`

用于自定义重排数据集：你为每个 query 提供候选，评估器计算 MAP 和 MRR。适合在留出集上衡量检索质量。

### `MSEEvaluator` / `MSEEvaluatorFromDataFrame`

用于蒸馏场景。比较学生嵌入与教师嵌入（或教师分数），报告 MSE。

### `ParaphraseMiningEvaluator`

用于释义挖掘任务。给定带标签的释义对语料，计算挖掘质量（不同阈值下的 F1）。

### `TranslationEvaluator`

用于跨语言 / `make_multilingual` 风格的对齐检查。衡量学生是否能在语言之间对齐句子。

### `LabelAccuracyEvaluator`

用于 `SoftmaxLoss` 训练的分类头。报告在留出数据上的准确率。

## 编写 `metric_for_best_model`

模式：`f"eval_{evaluator.primary_metric}"`。构造完后检查：`print(evaluator.primary_metric)`。常见取值：
- `eval_NanoBEIR_mean_cosine_ndcg@10` —— `NanoBEIREvaluator`
- `eval_sts-dev_spearman_cosine` —— `EmbeddingSimilarityEvaluator(name="sts-dev")`
- `eval_{name}_cosine_ndcg@10` —— `InformationRetrievalEvaluator(name=...)`

## 多维度评估（Matryoshka）

对 Matryoshka 训练的模型，按每个目标维度评估：

```python
per_dim_evaluators = [
    EmbeddingSimilarityEvaluator(
        sentences1=..., sentences2=..., scores=...,
        main_similarity=SimilarityFunction.COSINE,
        name=f"sts-dev-{dim}",
        truncate_dim=dim,
    ) for dim in [768, 512, 256, 128, 64]
]
evaluator = SequentialEvaluator(per_dim_evaluators, main_score_function=lambda scores: scores[0])
```

第一个评估器的分数驱动 `load_best_model_at_end`。

## 常见坑

- **训练前始终先跑一次 `evaluator(model)`** —— 预训练基线。训练后增量很小说明损失/数据/基座有问题。
- 不要在频繁的 `eval_steps` 下用 `InformationRetrievalEvaluator` 跑大语料（>10 万 doc）—— 训练中用 `NanoBEIREvaluator`，完整 IR 留给训练末。
- `greater_is_better=True` 是默认；适用于 nDCG / MRR / accuracy。
