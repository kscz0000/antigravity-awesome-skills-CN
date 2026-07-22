---
name: hf-mem
description: Hugging Face CLI 工具，通过 HTTP Range 请求估算从 Hugging Face Hub 加载 Safetensors 或 GGUF 模型权重进行推理所需的内存（无需下载或本地加载任何权重）。触发词：hf-mem、Hugging Face 内存估算、模型显存查询、Safetensors 内存、GGUF 内存、模型权重估算、VRAM 估算、KV 缓存估算
risk: unknown
source: https://github.com/huggingface/skills/tree/main/skills/hf-mem
source_repo: huggingface/skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/huggingface/skills/blob/main/LICENSE
---

`hf_mem` 用于估算推理所需的内存（包括模型权重以及可选的 KV 缓存），支持 Hugging Face Hub 上的 Safetensors 和 GGUF 模型。它通过 HTTP Range 请求实现，无需在本地下载或加载任何权重。

## 何时使用？

- 用户询问模型运行所需的 VRAM 或内存大小
- 用户想了解模型是否能装入其 GPU 或指定的实例
- 用户引用了 Hugging Face 模型 ID 或 URL，并询问推理所需资源

## 前置要求是什么？

- 已安装 `uv`（用于 `uvx`）
- `HF_TOKEN` 环境变量或 `--hf-token` 参数（仅限受门控或私有模型需要）

## 如何运行？

通过 `--model-id` 指定 Hugging Face Hub 仓库，工具会校验其内部是否包含 Safetensors 权重（通过 `model.safetensors`、分片时的 `model.safetensors.index.json`，或 Diffusers 的 `model_index.json`）或 GGUF 模型权重。

```bash
uvx hf-mem --model-id <model-id> --json-output
```

若仓库内包含多种精度 / 量化的 GGUF 模型权重，估算会按文件逐个进行；而实际推理时不会同时加载所有这些文件，只会加载单一精度版本。话虽如此，对于 GGUF 你可能仍需通过 `--gguf-file` 指定想要运行的具体文件（若是分片则填写路径）。

```bash
uvx hf-mem --model-id <model-id> --gguf-file <file-or-path> --json-output
```

此外，`hf-mem` 还提供 `--experimental` 参数，用于额外计算 KV 缓存的内存需求。这对大语言模型场景非常有用，适用范围包括 LLM（`...ForCausalLM`）、VLM（`...ForConditionalGeneration`）以及 GGUF 模型。

上下文窗口长度会从默认配置读取，也可通过 `--max-model-len` 覆盖（用法参考 vLLM）。同理，KV 缓存精度默认与模型精度一致，除非通过 `--kv-cache-dtype` 手动指定（同样参考 vLLM 用法）。

Safetensors 用法示例：

```bash
uvx hf-mem --model-id <model-id> --experimental [--max-model-len N] [--batch-size N] [--kv-cache-dtype auto|bfloat16|fp8|fp8_ds_mla|fp8_e4m3|fp8_e5m2|fp8_inc] --json-output
```

GGUF 用法示例：

```bash
uvx hf-mem --model-id <model-id> --gguf-file <file-or-path> --experimental [--max-model-len N] [--batch-size N] [--kv-cache-dtype auto|F32|F16|Q4_0|Q4_1|Q5_0|Q5_1|Q8_0|Q8_1|Q2_K|Q3_K|Q4_K|Q5_K|Q6_K|Q8_K|IQ2_XXS|IQ2_XS|IQ3_XXS|IQ1_S|IQ4_NL|IQ3_S|IQ2_S|IQ4_XS|I8|I16|I32|I64|F64|IQ1_M|BF16|TQ1_0|TQ2_0|MXFP4] --json-output
```

## 示例

Transformers 框架 + Safetensors 权重：

```bash
uvx hf-mem --model-id MiniMaxAI/MiniMax-M2 --json-output
```

Diffusers 框架 + Safetensors 权重：

```bash
uvx hf-mem --model-id Qwen/Qwen-Image --json-output
```

Sentence Transformers + Safetensors 权重：

```bash
uvx hf-mem --model-id google/embeddinggemma-300m --json-output
```

使用 `--experimental` 包含 LLM 与 VLM 的 KV 缓存估算：

```bash
uvx hf-mem --model-id mistralai/Mistral-7B-v0.1 --experimental --json-output
```

LLM 或 VLM + GGUF 权重：

```bash
uvx hf-mem --model-id unsloth/Qwen3.5-397B-A17B-GGUF --gguf-file Q4_K_M --experimental --json-output
```

## 注意事项

- 仅在任务与上游产品或 API 范围明确匹配时使用本技能。
- 在执行任何变更前，请依据最新的官方文档核实命令、API 行为、定价、配额、凭证及部署影响。
- 切勿将生成的示例视为针对具体环境的测试、安全审查，或用户对破坏性 / 高成本操作的授权依据。