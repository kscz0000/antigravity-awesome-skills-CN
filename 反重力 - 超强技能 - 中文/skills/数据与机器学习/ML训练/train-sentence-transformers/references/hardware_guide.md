# 硬件指南

训练嵌入模型更多是访存受限，而不是算力受限。

## 如果遇到 OOM

按以下顺序尝试：

1. **降低 `per_device_train_batch_size`**。提高 `gradient_accumulation_steps` 以保持回归损失的有效 batch。（对 MNRL 而言，用 grad-accum 模拟的有效 batch **并不等价** —— 见第 3 点。）
2. **启用 `gradient_checkpointing=True`**。慢 ~30%，激活显存减少 ~40%。与 `Cached*` 损失不兼容。
3. **切换到 `Cached*` 损失**：
   - `CachedMultipleNegativesRankingLoss(model, mini_batch_size=32)` —— 按 mini-batch 前向，在完整 batch 上累积对比损失。可在 24GB GPU 上模拟 1024+ batch。
   - `CachedSpladeLoss(model, loss=..., mini_batch_size=16)` —— 稀疏版的同样技巧。
   - `CachedGISTEmbedLoss(model, guide_model, mini_batch_size=32)` —— GIST 变体。
4. **对 >1B 的 decoder 模型启用 PEFT / LoRA**。`LoraConfig(r=64, lora_alpha=128, task_type="FEATURE_EXTRACTION")`。见 `../scripts/train_sentence_transformer_with_lora_example.py`（docstring 涵盖使用时机、超参、QLoRA、共享）。
5. **迁移到多卡**。见下文。
6. **缩短序列**。如果截断到 128 已能满足任务，就在 transformer 模块上设 `max_seq_length`。

## 多卡

`sentence-transformers` 底层使用 `accelerate`。分布式训练无需改代码。

### 数据并行（DDP）

启动：

```bash
accelerate launch train.py

# or explicitly:
accelerate launch --multi_gpu --num_processes=4 train.py
```

`per_device_train_batch_size` 保持每卡大小。有效 batch 线性扩展。MNRL 的 batch 内负例默认**仅在单卡内**，除非向支持的损失传 `gather_across_devices=True`（`MultipleNegativesRankingLoss`、`CachedMultipleNegativesRankingLoss`、对称变体、`GISTEmbedLoss`、`CachedGISTEmbedLoss`、`SparseMultipleNegativesRankingLoss`）。

### FSDP / DeepSpeed

>3B 模型用 `accelerate config` 启用 FSDP 或 DeepSpeed。两者都支持 —— `sentence-transformers` 不需要改代码，只需启动配置。

```bash
accelerate config                   # interactive; choose FSDP or DeepSpeed
accelerate launch train.py
```

用 FSDP full-shard：7B 模型可以在 4×24GB GPU 上训练，而单卡则会 OOM。

**FSDP 注意事项**（来自 [分布式训练文档](https://sbert.net/docs/sentence_transformer/training/distributed.html)）：
- **撰写本文时，evaluator 不能在 FSDP 下运行** —— eval 钩子会调用 `model.encode()`，FSDP 包装的模块在训练中无法响应。改为在训练后用单卡加载最终检查点评估；若需要训练中评估，用 DDP。
- **必须显式指定 layer 包装**，例如 `fsdp_config={"transformer_layer_cls_to_wrap": "BertLayer"}`（按你的模型替换为对应层类：`BertLayer`、`LlamaDecoderLayer`、`Qwen2DecoderLayer` 等）。不指定的话，FSDP 分片可能静默出错。
- **比 DDP 慢**（对单卡能装下的模型而言）—— 只有真的需要省显存时才上 FSDP。

DeepSpeed ZeRO-2/3 是替代方案，有自己的 config；在 `accelerate config` 这一层行为相同。

## 对比损失的有效 batch

对 `MultipleNegativesRankingLoss` 及其变体，**batch 大小是质量旋钮**，不仅仅是速度旋钮。batch 越大 = 负例越多 = 梯度越丰富。

每个 anchor 的有效 batch 内负例池：

| 部署 | 每个 anchor 的 batch 内负例数 |
|---|---|
| 单卡，batch 64 | 63 |
| 4× DDP，每卡 batch 64 | 默认仅本卡 63；用 `MultipleNegativesRankingLoss(model, gather_across_devices=True)` 可达 255 |
| 单卡，CachedMNRL，mini_batch 32，batch 256 | 255 |
| 4× DDP，CachedMNRL，每卡 256 | 本卡 255；用 `gather_across_devices=True` 可达 1023 |

对大语料（检索），推到 512+ 有效负例。对小而干净的数据（STS），64 足够。

## 按 GPU 选精度

| GPU 世代 | 推荐 |
|---|---|
| T4、V100、GTX 1xxx、RTX 2xxx | `fp16=True` |
| RTX 3xxx、A10G、A100、L4 | `bf16=True` |
| RTX 4xxx、H100、B200 | `bf16=True`（H100 上可通过特定 kernel 用 fp8 —— 非默认） |
| Apple M 系列 / ROCm | MPS/ROCm 支持不稳定；`fp16` 或 `fp32` 最稳 |

bf16 数值上更稳定，几乎总是首选。

## Hugging Face Jobs flavor 指南

Hugging Face Jobs 需要 Pro/Team/Enterprise 套餐。价格为大致估算，可能变化 —— 见 [Jobs 价格页](https://huggingface.co/docs/huggingface_hub/guides/jobs)。

| Flavor | 显存 | 典型用途 | 约 $/小时 |
|---|---|---|---|
| `cpu-basic` | ~2 GB | 数据准备、验证、小规模 hard-neg 挖掘 | <$0.10 |
| `cpu-upgrade` | ~4 GB | 同上，稍大 | $0.10 |
| `t4-small` | 16 GB | Demo、MiniLM/DistilBERT 小 batch | ~$0.75 |
| `t4-medium` | 16 GB | MiniLM / DistilBERT 较大 batch | ~$1.50 |
| `l4x1` | 24 GB | BERT-base、MPNet、ModernBERT-base | ~$2.50 |
| `a10g-small` | 24 GB | BERT-base 到 BERT-large | ~$3.50 |
| `a10g-large` | 48 GB | ModernBERT-large、Qwen3-0.6B | ~$5.00 |
| `a10g-largex2` | 96 GB（2× 48GB） | 中型多卡 | ~$10 |
| `a100-large` | 80 GB | 大模型或大对比 batch | ~$10–12 |
| `h100` | 80 GB | 最大单卡 | ~$12 |
| `h100x8` | 640 GB | LLM 规模分布式 | ~$96 |

按基座模型的默认 flavor：
- MiniLM / DistilBERT -> `t4-small`
- BERT-base / MPNet / ModernBERT-base -> `a10g-small` 或 `l4x1`
- BERT-large / ModernBERT-large -> `a10g-large`
- Qwen3-0.6B decoder 基座 -> `a10g-large`
- 1B+ decoder 基座 + LoRA -> `a10g-large` 或 `a100-large`

总是比想象的小一档 flavor 起步：Jobs 上 OOM 成本低（$0.50–$5 就一次失败）。第一次先少配，再加。预算 `timeout` 时留 **20–30% 缓冲**给模型加载、检查点保存和 Hub 推送。
