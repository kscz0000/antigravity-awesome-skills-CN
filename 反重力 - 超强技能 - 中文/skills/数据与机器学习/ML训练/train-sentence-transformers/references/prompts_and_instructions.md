# 提示与指令

现代嵌入模型（E5、BGE、GTE、Qwen3-Embedding、Nomic、Instructor 等）在 encode 时用 **prompts** / **instructions** —— 诸如 `"query: "`、`"passage: "`、`"Represent this sentence for retrieval:"` 的短前缀 —— 来传达任务意图。

在 sentence-transformers 中，prompts 在 **训练** 和 **推理** 都生效，库自动保持它们一致。

prompt 实际就是 tokenize 前拼到输入文本的开头。

## 模型级 prompts

在模型上设 prompts，使 `encode()`、`encode_query()`、`encode_document()` 自动用它们：

```python
model = SentenceTransformer("your-base-model")
model.prompts = {
    "query":    "query: ",
    "document": "passage: ",
}
model.default_prompt_name = "document"        # used when none is specified
```

推理时：

```python
q_emb = model.encode_query("What is the capital of France?")
# Internally: encodes "query: What is the capital of France?"

d_emb = model.encode_document(["Paris is the capital of France.", "Berlin is the capital of Germany."])
# Internally: encodes "passage: Paris..." etc.

# Explicit prompt_name:
emb = model.encode(["some text"], prompt_name="query")
```

## 训练时用 prompts

在训练参数上设 prompts，让它们在训练时自动作用到对应列。四种形状，依次更具体：

### 1. 单一 prompt（作用于所有列）

```python
args = SentenceTransformerTrainingArguments(
    ...,
    prompts="Represent this sentence for similarity: ",
)
```

每个输入列都加该前缀。最简单，单任务训练常常够用。

### 2. 按列 prompts

```python
prompts = {
    "anchor":   "query: ",
    "positive": "passage: ",
    "negative": "passage: ",
}
```

键是 **列名**。不同角色用不同前缀。

### 3. 按数据集 prompts（多数据集）

```python
prompts = {
    "all-nli": "Classify the entailment relationship: ",
    "stsb":    "Score semantic similarity: ",
}
```

键是 **数据集名**（匹配 `train_dataset` 字典的键）。

### 4. 按数据集 + 按列

```python
prompts = {
    "all-nli": "",                                          # all-nli: no prompt
    "msmarco": {                                            # msmarco: per-column
        "query":    "query: ",
        "positive": "passage: ",
        "negative": "passage: ",
    },
}
```

## 交叉编码器细节

交叉编码器把 prompts 限制为单值或按数据集（不按列）。因为交叉编码器接受文本对，不是独立列。

```python
args = CrossEncoderTrainingArguments(
    ...,
    prompts="Rank this passage for the query: ",   # single prompt
)
# or
args = CrossEncoderTrainingArguments(
    ...,
    prompts={"msmarco": "...", "gooaq": "..."},    # per-dataset
)
```

## 稀疏编码器（SPLADE）

稀疏编码器支持与双编码器相同的四种 prompts 形状（v5.x 加入）。同样的 `model.prompts = {...}` API。

## Pooling 与 prompt token（双编码器）

用 mean / last-token pooling 配合 prompt 前缀时，prompt 自身可以：
- **包含**在 pooled 嵌入里（默认行为）。简单，多数模型这么做。
- **排除** —— 只 pool 实际内容 token。

要排除，把 Pooling 模块上的 `include_prompt` 翻过来 —— 用 `isinstance` 找，因为多模态 / Router 流水线的 Pooling 不总在位置 1：

```python
from sentence_transformers.sentence_transformer.modules import Pooling

for module in model:
    if isinstance(module, Pooling):
        module.include_prompt = False
```

或用模型自带的辅助（如 `SparseEncoder.set_pooling_include_prompt(False)`）。

**何时排除**：当 prompt 纯是任务信号、不想让它稀释语义表示时。大多数 E5 / BGE / GTE 模型保持 prompt 包含。

用 `prompts=` 训练时，`include_prompt` 设置会被尊重；trainer 内部也会跟踪 `include_prompt_lengths`，在 `include_prompt=False` 时正确跳过 prompt token。

## 推理对齐

如果你用 `prompts={"query": "query: ", ...}` 训练，必须：

1. **把 prompts 存到模型上**：`save_pretrained` 之前 `model.prompts = args.prompts`，或让库通过 model card data 自动做。
2. **推理时用相同 prompts**：调 `encode_query()` / `encode_document()`，保存的 prompts 会被应用。

如果保存模型的 `config_sentence_transformers.json` 有 `prompts` + `default_prompt_name`，任何加载它的人都自动得到正确 prompts。

## 指令调优（不同于 prompts）

一些模型（Instructor、Qwen3-Embedding）使用 **instructions** —— 更长的描述，如 `"Represent the biomedical query for retrieving relevant passages:"`。在 sentence-transformers 中建模方式相同：就把它们当作 prompts 设置。

model-card 约定是把可用的 instructions / prompts 列在 dict 中：

```python
model.prompts = {
    "msmarco-query":    "Represent the query for MS MARCO retrieval: ",
    "msmarco-doc":      "Represent the passage for MS MARCO retrieval: ",
    "sts":              "Represent the sentence for semantic similarity: ",
    "classification":   "Represent the sentence for topic classification: ",
}
```

用户调用 `model.encode(["..."], prompt_name="msmarco-query")`。

## 常见坑

- **训练时用了 prompts，但 `save_pretrained` 前忘了在模型上设**：保存的模型不知道 prompts。用户会在 *没有* 前缀的情况下 encode，得到差的结果。修法：`save_pretrained` 之前 `model.prompts = args.prompts`，或用 `SentenceTransformerModelCardData(...)` 带上 prompt 信息。
- **推理时用 `encode_query()`，但训练时没设 "query" prompt**：方法会调普通 `encode`（不应用前缀），没事。但文档暗示你该用它，用户可能困惑。
- **末尾空格要紧**：`"query: "` vs `"query:"` —— 前者在真实文本前有空格。检查训练数据知道模型训练用的是哪种。
- **多数据集训练中混用带 prompt 与不带 prompt 的数据** 没问题，只要 `prompts` dict 按数据集覆盖（例如 `{"dataset_a": "query: ", "dataset_b": ""}`）。
- **`include_prompt=False` 配小数据集**：模型可能欠拟合，因为你实际上缩短了每个输入。通常保持 True。
