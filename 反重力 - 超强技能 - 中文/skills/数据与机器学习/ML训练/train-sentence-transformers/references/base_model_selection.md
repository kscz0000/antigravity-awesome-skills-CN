# 基础模型选择

排行榜每隔几个月就会轮换；不要相信任何写死的"最佳"选择。应当实时发现当前可选——**同时**运行两种排序，因为下载量最多能浮现成熟选项，而热门趋势能浮现近期 SOTA（它们可能下载量还不够）。

## 发现命令

**[BI]**：
```bash
hf models list --filter sentence-transformers --sort downloads --limit 20
hf models list --filter sentence-transformers --sort trending  --limit 20
```

**[CE]**：
```bash
hf models list --filter sentence-transformers --filter text-ranking --sort downloads --limit 20
hf models list --filter sentence-transformers --filter text-ranking --sort trending  --limit 20
```

**[SPARSE]**：
```bash
hf models list --filter sentence-transformers --filter sparse-encoder --sort downloads --limit 20
hf models list --filter sentence-transformers --filter sparse-encoder --sort trending  --limit 20
```

可选的语言收窄（任意类型）：加 `--filter <language-code>`。并非所有多语言模型都会标记所有语言，所以匹配不到并不意味着模型不能处理该语言——可以不带 filter 再跑一次对比。

```bash
hf models card <id> --text                        # confirm dimensions, max_seq_length, license, languages
```

在投入多小时的训练前，交叉验证 [MTEB 排行榜](https://huggingface.co/spaces/mteb/leaderboard)（选对应 tab）。

## [BI] 双编码器

在已有检索器上继续微调通常胜过从头开始 + 10 万–50 万对。截至 2026-Q2 的常见命名空间（请用发现命令核对——领域一直在变）：

- **英文编码器检索器**：`sentence-transformers/all-*`（MiniLM-L6-v2、mpnet-base-v2 仍是 Hub 上下载量最高的模型）、`BAAI/bge-*-en-v1.5`、`nomic-ai/nomic-embed-text-v1.5`、`mixedbread-ai/mxbai-embed-large-v1`、`Alibaba-NLP/gte-*`、`Snowflake/snowflake-arctic-embed-*`、`jinaai/jina-embeddings-v5-text-small` / `-nano`、`microsoft/harrier-oss-v1-270m` / `-0.6b`。
- **多语言编码器检索器**：`sentence-transformers/paraphrase-multilingual-*`、`intfloat/multilingual-e5-*`、`ibm-granite/granite-embedding-*-multilingual-r2`、`google/embeddinggemma-300m`、`voyageai/voyage-4-nano`。
- **长文档（8k+）**：`nomic-ai/modernbert-embed-*`、`answerdotai/ModernBERT-large`。
- **Decoder LLM 检索器**（多语言；**需要 last-token pooling**）：`Qwen/Qwen3-Embedding-*`（0.6B / 4B / 8B）、`Qwen/Qwen3-VL-Embedding-*`（多模态）、`codefuse-ai/F2LLM-v2-*`。
- **英文从头开始**（≥50 万对 + 领域适配理由）：`microsoft/mpnet-base`、`answerdotai/ModernBERT-base`、`google-bert/bert-base-uncased`、`jhu-clsp/ettin-encoder-*`（17m / 32m / 68m / 150m / 400m / 1b —— 成对的 ModernBERT encoder 系列）。
- **多语言从头开始**：`FacebookAI/xlm-roberta-base`（仅 MLM，需要对比训练）、`microsoft/mdeberta-v3-base`、`jhu-clsp/mmBERT-base` / `-small`。
- **CPU / 小体积**（`StaticEmbedding`）：`StaticEmbedding(tokenizer, embedding_dim=...)`。**模型体积 = `vocab_size × dim × 4 字节`** —— 选小词表的 tokenizer，否则模型会巨大：30k 词表的 `bert-base-uncased` × 128 dim ≈ 15 MB；**250k 词表的 `paraphrase-multilingual-MiniLM-L12-v2` × 256 dim ≈ 256 MB**。随机初始化需要 100 万+ 对；热启动（`StaticEmbedding.from_distillation(...))` 在 <10 万对时有用。

架构变体（encoder / decoder / static / Router）、pooling 规则、decoder 与 encoder 的配置路径：`model_architectures.md`。

**ModernBERT 系列基座默认 `max_seq_length=8192`。** 这会按 8192 token 的序列长度分配激活显存，与你的数据长度无关，并悄悄把 Windows 显存挤进"共享内存"溢出。加载任何 ModernBERT / mmBERT / Ettin / gte-modernbert / nomic-modernbert 基座后，**显式设置 `model.max_seq_length = 256`（文档用 512）**，除非你真的需要长上下文。

## [CE] 交叉编码器

在已有重排器上继续微调在多数领域胜过从头开始 + 10 万–50 万对；除非有充分理由，默认这种做法。截至 2026-Q2 的常见命名空间：

- **英文编码器重排器**：`cross-encoder/ms-marco-*`、`BAAI/bge-reranker-*`、`mixedbread-ai/mxbai-rerank-*-v1` / `-v2`、`Alibaba-NLP/gte-reranker-modernbert-*`、`ibm-granite/granite-embedding-reranker-english-*`。
- **多语言编码器重排器**：`cross-encoder/mmarco-*`、`BAAI/bge-reranker-v2-m3`、`Alibaba-NLP/gte-multilingual-reranker-*`、`ibm-granite/granite-embedding-reranker-multilingual-*`。
- **Decoder LLM 重排器**（多语言；`num_labels=1` 的 last-token 风格打分）：`Qwen/Qwen3-Reranker-*`（0.6B / 4B / 8B）、`Qwen/Qwen3-VL-Reranker-*`（多模态）。
- **从头开始**：`microsoft/MiniLM-L12-H384-uncased`、`answerdotai/ModernBERT-base` / `-large`、`jhu-clsp/ettin-encoder-*`、`FacebookAI/xlm-roberta-base`（多语言）、`microsoft/mdeberta-v3-base`（多语言）、`jhu-clsp/mmBERT-base` / `-small`（多语言）。分类交叉编码器传 `num_labels >= 2`。

Encoder-only 基座仍然是延迟高效的默认（双向注意力在小参数量下非常适合重排场景），但在 MTEB Reranking 顶部，当延迟/显存预算允许时，decoder LLM 重排器已具备竞争力。

**最小数据量：** 生产用 50 万+ 带标签的 `(query, passage, label)` 三元组；领域数据继续训练用 1 万–10 万带标签对。资源稀缺的语言可能少于 1 万对；此时应依赖多语言基座的预训练，并接受更嘈杂的信号。

**"小型"多语言约 1 亿+ 参数**，不像英文小型模型只有 1700 万–5000 万。mMiniLMv2-L12-H384（~117M）大致是可用多语言重排器的小端。

## [SPARSE] 稀疏编码器（SPLADE）

SPLADE 需要兼容 fill-mask / `AutoModelForMaskedLM` 的检查点。Encoder-only 的 MLM 模型开箱即用；**decoder LLM 不行**。

- **从已有 SPLADE 继续 —— 英文**：`naver/splade-*`（标杆系列）、`opensearch-project/opensearch-neural-sparse-encoding-*`（含 `-doc-v2-distill`、`-doc-v3-distill` / `-doc-v3-gte`）、`prithivida/Splade_PP_en_v*`、`ibm-granite/granite-embedding-30m-sparse`。
- **从已有 SPLADE 继续 —— 多语言**：`opensearch-project/opensearch-neural-sparse-encoding-multilingual-v1`。
- **英文从头开始**（≥50 万对）：任何带 MLM 头的 encoder —— `distilbert/distilbert-base-uncased`、`google-bert/bert-base-uncased`。没有 MLM 头的纯 `AutoModel` 检查点不行。发现 MLM 基座：`hf models list --filter fill-mask --sort downloads --limit 20`。
- **多语言从头开始**：`FacebookAI/xlm-roberta-base`（带 MLM 头）。其他多语言 MLM 基座：加 `--filter <language-code>`。

**最小数据量：** 竞标级 SPLADE 需要 50 万+ 三元组（带挖掘的 hard negative）；在已有 SPLADE 上做领域适配需要 5 万+ 三元组。

## 横切提示

- **非英文检索起点**（当语言标签返回 0 结果时）：查 `intfloat/multilingual_e5_train_data` 找平行对数据；通过 `sentence-transformers/miracl` 镜像找 MIRACL 多语言检索数据；通过 `unicamp-dl/mmarco`（14 种语言，parquet 支持）找 mMARCO。
- **避免基于脚本的数据集加载器。** `datasets >= 4` 会用 `RuntimeError: Dataset scripts are no longer supported` 拒绝。寻找 parquet 镜像（例如用 `sentence-transformers/miracl` 替代 `miracl/miracl`）。
- **`hf datasets sql` 需要 DuckDB**（`pip install duckdb`）。没有就回退到 `python -c "from datasets import load_dataset; ds = load_dataset('<id>', ...); print(ds.column_names, ds[0])"`。
