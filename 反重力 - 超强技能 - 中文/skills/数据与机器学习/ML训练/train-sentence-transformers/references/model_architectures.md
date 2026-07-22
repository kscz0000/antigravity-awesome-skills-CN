# 模型架构（SentenceTransformer）

`SentenceTransformer` 类是 `torch.nn.Sequential` 的模块。常见形状是 `Transformer` + `Pooling`（+ 可选 `Normalize` / `Dense`），但支持四种不同的架构族，正确选择取决于任务。

## 四种架构族

| 族 | Backbone | Pooling | 场景 |
|---|---|---|---|
| **Encoder（双向）** | BERT、RoBERTa、DeBERTa、MPNet、ModernBERT、XLM-R | `mean`（默认）或 `cls` | 短/中等文本，通用默认 |
| **Decoder（causal LLM）** | Qwen、Llama、Mistral、Gemma | `lasttoken` | 长上下文，指令可调，质量上限更高 |
| **Static embedding** | `StaticEmbedding` 模块 | 无 | 仅 CPU，<10MB，极快 |
| **多模态 / Router** | VLM backbone 或组合 encoder | 视情况 | 文本 + 图像 / 音频 / 视频 |

下面给出每族的具体设置。

## Encoder 模型（默认）

历史默认，现在也仍是文本嵌入的正确选择。

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("microsoft/mpnet-base")
# Auto-constructs: Transformer(feature-extraction) -> Pooling(mean).
```

用裸 HF encoder 调 `SentenceTransformer("<checkpoint>")` 时，它会自动包装 transformer 并加 `Pooling(..., pooling_mode="mean")`。

要自定义 pooling 或加模块：

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.modules import Normalize, Pooling, Transformer

transformer = Transformer("answerdotai/ModernBERT-base")
pooling = Pooling(transformer.get_embedding_dimension(), pooling_mode="cls")    # or "mean", "lasttoken", ...
model = SentenceTransformer(modules=[transformer, pooling, Normalize()])
```

**Pooling 模式**：
- `mean`（默认）—— token 嵌入在 attention mask 下的平均。最强的默认。
- `cls` —— `[CLS]` token 的嵌入。如果基座是按 CLS 预训练的可用。
- `max` —— token 间 element-wise max。少见。
- `mean_sqrt_len_tokens` —— 按 √seq_len 缩放的 mean。经验上对一些任务有帮助。
- `weightedmean` —— token 位置加权的 mean。对 decoder 基座可作为非 last-token 替代。
- `lasttoken` —— 最后一个 token 的嵌入。causal-LM 基座必需（见下文 decoder 章节）。

不要中途切换 pooling。一次定。

## Decoder / causal LLM 模型

长上下文、指令跟随、多语言上强。吃显存 —— 通常 LoRA 训练而不是全参数微调。

**两种设置路径，取决于模型是否已经为嵌入做过适配：**

```python
# Path A: already-adapted embedding checkpoint (ships with the right modules):
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")   # just works

# Path B: raw decoder LLM, build the pipeline manually:
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.modules import Normalize, Pooling, Transformer

transformer = Transformer(
    "Qwen/Qwen2.5-0.5B",
    transformer_task="text-generation",         # critical: causal attention, no bidirectional
    processor_kwargs={"padding_side": "left"},  # last-token pooling wants left-padding
)
pooling = Pooling(transformer.get_embedding_dimension(), pooling_mode="lasttoken")
model = SentenceTransformer(modules=[transformer, pooling, Normalize()])
```

裸 decoder 上漏了 `transformer_task="text-generation"` 或 `pooling_mode="lasttoken"`，嵌入会看起来合理，直到做 benchmark 才发现问题。

**为什么用 last-token pooling：** causal 注意力下只有最后一个 token 看过完整序列。给 causal 模型做 mean-pooling 平均的是那些只看过前缀的嵌入 —— 结果不表示整个输入。

训练 decoder 基座：
- 学习率：通常 `1e-4` 或更高（不是 encoder 的 `2e-5`）。
- 对 >1B 参数的基座 LoRA 几乎总是对的选择；见 `../scripts/train_sentence_transformer_with_lora_example.py`（docstring 涵盖使用时机、超参、7B+ 的 QLoRA、adapter 共享）。

## Static embedding

`StaticEmbedding` 完全跳过 transformer —— 每个 token 通过查找表映射到预先算好的向量。无注意力，无上下文。

**何时用：**
- CPU 推理，无 GPU，浏览器 / 边缘 / 设备端部署。
- 需要 <10MB 模型大小。
- 延迟预算 <1ms 每嵌入。
- 有 >100 万训练对（用每 token 优化替代上下文化；这需要数据量）。

**何时不用：**
- 任务需要上下文理解（一词多义、句法、长距离依赖）。
- 训练对 <10 万 —— 模型学不够。

**设置：**

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.modules import StaticEmbedding
from tokenizers import Tokenizer

tokenizer = Tokenizer.from_pretrained("google-bert/bert-base-uncased")
static_embedding = StaticEmbedding(tokenizer, embedding_dim=512)
model = SentenceTransformer(modules=[static_embedding])
```

在大对比数据集（100 万+ 对）上用 `MultipleNegativesRankingLoss` 训练。

**热启动 vs 随机初始化** —— 训练样本 **>100 万** 时，随机初始化胜过 `StaticEmbedding.from_model2vec(...)` 或 `.from_distillation(...)` 热启动。数据集更小，热启动有帮助。

```python
# For smaller datasets (<100k), warm-start:
static_embedding = StaticEmbedding.from_model2vec("minishlab/potion-base-8M")
# or:
static_embedding = StaticEmbedding.from_distillation("sentence-transformers/all-MiniLM-L6-v2", vocabulary=list(tokenizer.get_vocab().keys()))
```

可跑的端到端配方见 `../scripts/train_sentence_transformer_static_embedding_example.py`（随机初始化 + MNRL + Matryoshka + bf16 + lr=2e-1），基准见 [Static Embeddings 博文](https://huggingface.co/blog/static-embeddings)。

## 通过 VLM backbone 的多模态

现代视觉-语言模型可直接加载并产出联合文本+图像嵌入：

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "Qwen/Qwen3-VL-Embedding-2B",
    model_kwargs={"attn_implementation": "flash_attention_2"},  # do NOT set torch_dtype here; see training_args.md
    processor_kwargs={"min_pixels": 28 * 28, "max_pixels": 600 * 600},
)

# Check which modalities this model supports:
print(model.modalities)
# ['text', 'image', 'video', 'message']
```

训练数据可混合文本、PIL 图像、图像路径/URL、音频和混合模态 dict 如 `{"image": <PIL>, "text": "describe this"}`。数据 collator 通过模型的 `preprocess` 方法处理预处理。

安装多模态 extras：`pip install "sentence-transformers[image]"`（或 `[audio]`、`[video]`）。

**精度**：以 fp32 加载，对 TrainingArguments 传 `bf16=True`（或 `fp16=True`）—— autocast 处理推理路径。不要在 `model_kwargs` 里设 `torch_dtype="bfloat16"`：会让 Adam state 进入 bf16 并静默降低质量（见 `training_args.md`）。

## 通过 Router 的多模态

不用单一 VLM backbone，而是按模态组合独立 encoder：

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer.modules import Dense, Pooling, Router, Transformer

# Text encoder
text_encoder = Transformer("sentence-transformers/all-MiniLM-L6-v2")
text_pooling = Pooling(text_encoder.get_embedding_dimension(), pooling_mode="mean")
# Project text to match image encoder's dim
text_projection = Dense(text_encoder.get_embedding_dimension(), 768)

# Image encoder (SigLIP outputs pooled embeddings directly)
image_encoder = Transformer("google/siglip2-base-patch16-224")

router = Router(
    sub_modules={
        "text": [text_encoder, text_pooling, text_projection],
        "image": [image_encoder],
    },
)
model = SentenceTransformer(modules=[router])
```

**警告**：基于 Router 的模型初始化时各嵌入空间不对齐 —— 必须训练对齐。维度不同时用 `Dense` 投影层。也支持 query vs document 用不同 encoder 的任务路由（通过 `route_mappings`）；见 `Router` docstring。

## 常见坑

- **Decoder 基座 + mean pooling**：静默产出垃圾嵌入。始终用 `lasttoken`。
- **未训练的 Router 多模态**：初始化时各 encoder 的嵌入空间不对齐。在用对齐空间的损失训练之前，别期望有用的跨模态相似度。
- **<10 万对的 `StaticEmbedding`**：模型学不够。要么通过 `from_model2vec` / `from_distillation` 热启动，要么用普通 encoder。
- **消费级 GPU 上的大型 VLM backbone**：组合 LoRA + `attn_implementation="flash_attention_2"`。只用 LoRA 时，可以额外传 `torch_dtype="bfloat16"` —— bf16 基座权重被冻结，上面精度规则里 Adam state 精度的担忧不适用（LoRA adapter 保持 fp32，所以其 optimizer state 保持 fp32）。不用 LoRA 时，按精度规则：保持权重 fp32，依赖 `bf16=True` autocast。
