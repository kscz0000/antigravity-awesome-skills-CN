---
name: train-sentence-transformers
description: 跨 `SentenceTransformer`（双编码器；稠密或静态嵌入模型；用于检索、相似度、聚类、分类、释义挖掘、去重、多模态）、`CrossEncoder`（重排器；二阶段检索/配对评分...）以及 `SparseEncoder`（SPLADE；学习型稀疏向量，作用于倒排索引后端）等 sentence-transformers 模型的训练或微调。涉及训练、sentence transformer、嵌入、微调、损失函数、评估器、双编码器、交叉编码器、稀疏编码器、LoRA、HF Jobs。
risk: unknown
source: https://github.com/huggingface/skills/tree/main/skills/train-sentence-transformers
source_repo: huggingface/skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/huggingface/skills/blob/main/LICENSE
---

# 训练 sentence-transformers 模型
## 使用时机

当你需要训练或微调 sentence-transformers 模型时使用本技能，覆盖 `SentenceTransformer`（双编码器；稠密或静态嵌入模型；用于检索、相似度、聚类、分类、释义挖掘、去重、多模态）、`CrossEncoder`（重排器；用于二阶段检索的配对评分...）


**本 SKILL.md 是路由表，不是使用手册。** 它会告诉你根据任务加载哪些 references 和示例脚本。实际内容——推荐的损失、评估器、训练脚本结构、模型选择、训练参数、故障排查——都在 `references/` 和 `scripts/` 中。

**不要仅凭本文件自行拼凑训练脚本。** 请打开对应类型的生产模板（`scripts/train_<type>_example.py`），并以它为起点复制。模板中包含了关键的脚手架（autocast 辅助函数、model-card 类、logger 静默列表、`force=True`、`seed`、TF32、版本兼容的 import、命名评估器指标处理），这些是早期智能体在自己拼凑片段时反复遗漏的内容。

## 1. 识别模型类型

| 标签 | 类 | 作用 | 何时选择 |
|---|---|---|---|
| **[SentenceTransformer]** | `SentenceTransformer`（双编码器） | 将每个输入映射为定维稠密向量 | 检索、相似度、聚类、分类、释义挖掘、去重 |
| **[CrossEncoder]** | `CrossEncoder`（重排器） | 对 `(query, passage)` 对联合打分 | 二阶段检索（用双编码器检索 top-100 后重排）、配对分类 |
| **[SparseEncoder]** | `SparseEncoder`（SPLADE） | 基于词表的稀疏向量 | 学习型稀疏检索、倒排索引后端（Elasticsearch / OpenSearch / Lucene） |

当需求不明确时的决胜规则：出现"嵌入模型"/"向量搜索"/"相似度" → **[SentenceTransformer]**。出现"rerank"/"ranker"/"two-stage" → **[CrossEncoder]**。出现"SPLADE"/"sparse"/"inverted index" → **[SparseEncoder]**。仍然不明确就提问。

## 2. 必读内容

**在写任何代码之前完整阅读。不要按"看上去是否相关"挑读。**

### 按类型 —— 始终必读

**[SentenceTransformer]**
- `references/losses_sentence_transformer.md` —— 损失到数据形状的映射；MNRL 系列对 `BatchSamplers.NO_DUPLICATES` 的要求；`Cached*` 与 `gradient_checkpointing` 的不兼容。
- `references/evaluators_sentence_transformer.md` —— 评估器到任务的映射；`metric_for_best_model` 键的构造（命名 vs 匿名）；各评估器 `primary_metric` 取值。
- `references/model_architectures.md` —— encoder / decoder / static / Router 流水线；pooling 规则（mean / cls / lasttoken）；新开始 MLM 基座自动 mean-pooling 行为。
- `scripts/train_sentence_transformer_example.py` —— 生产模板；以它为起点复制。

**[CrossEncoder]**
- `references/losses_cross_encoder.md` —— pointwise / pairwise / listwise / distillation；`pos_weight` 推导；非 BCE 损失必须使用 `activation_fn=Identity()`（否则评估排名会静默坍塌）。
- `references/evaluators_cross_encoder.md` —— `CrossEncoderRerankingEvaluator` 配方；命名评估器键格式 `eval_{name}_{primary_metric}`。
- `scripts/train_cross_encoder_example.py` —— 生产模板；以它为起点复制。

**[SparseEncoder]**
- `references/losses_sparse_encoder.md` —— `SpladeLoss` 包装要求；FLOPS 正则权重；smoke-test 中 active-dim 增长行为。
- `references/evaluators_sparse_encoder.md` —— `SparseNanoBEIREvaluator`（仅英文）和 in-domain 替代方案；`eval_{name}_{primary_metric}` 键格式。
- `scripts/train_sparse_encoder_example.py` —— 生产模板；以它为起点复制。

### 横切 —— 始终必读（无论何种任务）

- `references/training_args.md` —— `TrainingArguments` 参数、精度规则（以 fp32 加载 + autocast bf16/fp16；禁止 `torch_dtype=bfloat16`）、`warmup_steps`（float）与已废弃的 `warmup_ratio`、`save_steps` 必须是 `eval_steps` 的倍数以启用 `load_best_model_at_end`、调度器、HPO、tracker、resume、hub-push 变体。
- `references/dataset_formats.md` —— 列匹配规则（标签名自动检测；列顺序优先于列名）；reshape 方案；hard-negative 挖掘选项。
- `references/base_model_selection.md` —— 发现命令；按类型划分的模型命名空间；ModernBERT 系列 `max_seq_length=8192` 陷阱；`datasets >= 4` 脚本加载器拒绝；非英文起点的捷径。
- `references/troubleshooting.md` —— 按症状索引的故障处理配方。每次运行都扫一眼章节标题，即使运行健康；"指标不提升"和"Hub 推送失败"两条对应经常咬人的 bug，事先认出来比事后调试成本更低。

### 横切 —— 视情况加载

- `references/hardware_guide.md` —— 显存估算、多卡、FSDP / DeepSpeed、HF Jobs 规格。>24GB 模型、多卡或 HF Jobs 运行时必读。
- `references/hf_jobs_execution.md` —— 在 HF Jobs 上运行时必读。
- `references/prompts_and_instructions.md` —— 使用 prompt-tuned 基座（E5、BGE、GTE、Qwen3-Embedding、Instructor、Nomic 等）或添加 `query: ` / `passage: ` 风格前缀时必读。

### 变体脚本（任务匹配时打开）
- **[SentenceTransformer]** `scripts/train_sentence_transformer_<matryoshka|multi_dataset|with_lora|distillation|make_multilingual|static_embedding>_example.py`。
- **[CrossEncoder]** `scripts/train_cross_encoder_<distillation|listwise>_example.py`。
- **[SparseEncoder]** `scripts/train_sparse_encoder_distillation_example.py`。
- Hard-negative 挖掘 CLI —— `scripts/mine_hard_negatives.py`。

## 3. 默认行为

除非用户另有指定，否则按默认：
- **本地执行。** 只有在本地硬件跑不下时才建议 HF Jobs。
- **单次运行。** 跑完后，如果用户可能受益（结论弱/边缘、要求"看你能推到多高"等措辞），提议多轮实验。迭代规则见 `references/training_args.md`（Experimentation 章节）。
- **运行结束时推送公共 Hub，包裹在 try-except 中。** 在 HF Jobs（临时环境）上，还需在训练中启用推送（`push_to_hub=True` + `hub_strategy="every_save"`）；详见 `references/hf_jobs_execution.md`。

## 4. 生成脚本必须满足的约束

以下是不可协商的契约。实现位于生产模板和 references 中，不要重新发明。
- 在 `trainer.train()` **之前**将预训练评估分数记为 `baseline_eval`。
- 在运行结束时输出单行：`VERDICT: WIN|MARGINAL|REGRESSION | score=... | baseline=... | delta=...`。监控器会抓取这行。
- 将 `httpx`、`httpcore`、`huggingface_hub`、`urllib3`、`filelock`、`fsspec` 的日志级别静默到 WARNING（否则 HF 下载 URL 会刷爆智能体上下文）。
- Tee 日志到 `logs/{RUN_NAME}.log`。
- 以 `model.push_to_hub(...)` 包裹在 `try/except` 中作为结尾。
- 长跑前先 smoke-test（`max_steps=1` + 极小数据集切片）。生产模板展示了常见模式（`SMOKE_TEST` 环境变量）。
- **[CrossEncoder]** 包含 `EarlyStoppingCallback(patience>=3)` —— CE 重排器经常在训练中段达到峰值后回退。
- **[SparseEncoder]** 在 verdict 行记录 `query_active_dims` / `corpus_active_dims`；高 nDCG 但稀疏度坍塌不算赢。键带名称前缀返回（例如 `..._query_active_dims`）；使用后缀匹配提取——参见 SPARSE 生产模板中的精确模式。

## 5. 工作流

1. 识别模型类型（§1）。不明确就问。
2. 加载该类型对应的 §2 必读文件。
3. 打开 `scripts/train_<type>_example.py`，以它为起点复制。
4. 把 `MODEL_NAME`、`DATASET_NAME`、`RUN_NAME`、损失和评估器替换为用户任务。交叉检查损失/数据形状是否匹配 `references/losses_<type>.md`；交叉检查 `metric_for_best_model` 键是否匹配 `references/evaluators_<type>.md`（命名评估器将键格式化为 `eval_{name}_{primary_metric}`）。
5. Smoke-test（`max_steps=1`）。
6. 跑训练。
7. 跑完后追加到 `logs/experiments.md`，如果 verdict 弱/边缘就提议迭代。

## 前置依赖

```bash
pip install "sentence-transformers[train]>=5.0"        # add [train,image] / [audio] / [video] for [SentenceTransformer] multimodal
pip install trackio                                    # optional tracker; or wandb / tensorboard / mlflow
hf auth login                                          # or set HF_TOKEN with write scope (for Hub push)
```

强烈推荐 GPU。CPU 只能用于 demo 和 `[SentenceTransformer]` `StaticEmbedding`。

## 限制

- 仅当任务明确匹配其上游产品或 API 范围时使用本技能。
- 在做改动前，请根据最新的官方文档验证命令、API 行为、价格、配额、凭据和部署效果。
- 不要把生成的示例当作环境专属测试、安全审查或用户对破坏性/高成本操作授权的替代。
