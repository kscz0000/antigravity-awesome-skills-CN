---
name: huggingface-local-models
description: 用于在 CPU、Mac Metal、CUDA 或 ROCm 上选择通过 llama.cpp 与 GGUF 在本地运行的模型。涵盖 GGUF 查找、量化选择、启动服务器、精确 GGUF 文件定位、模型转换以及 OpenAI 兼容本地服务。触发词：本地大模型、GGUF 量化、llama.cpp 部署、CUDA/ROCm/Metal 加速、Hub 模型搜索、Q4_K_M 选择、模型转换、本地推理服务器。
risk: unknown
source: https://github.com/huggingface/skills/tree/main/skills/huggingface-local-models
source_repo: huggingface/skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/huggingface/skills/blob/main/LICENSE
---

# Hugging Face 本地模型
## 何时使用

在需要在 CPU、Mac Metal、CUDA 或 ROCm 上选择通过 llama.cpp 与 GGUF 在本地运行的模型时使用本技能。涵盖 GGUF 查找、量化选择、启动服务器、精确 GGUF 文件定位、模型转换以及 OpenAI 兼容本地服务。


在 Hugging Face Hub 上搜索与 llama.cpp 兼容的 GGUF 仓库，选择合适的量化方案，并使用 `llama-cli` 或 `llama-server` 启动模型。

## 默认工作流

1. 使用 `apps=llama.cpp` 在 Hub 上搜索。
2. 打开 `https://huggingface.co/<repo>?local-app=llama.cpp`。
3. 优先采用 HF local-app 片段中可见的精确量化推荐。
4. 通过 `https://huggingface.co/api/models/<repo>/tree/main?recursive=true` 确认精确的 `.gguf` 文件名。
5. 使用 `llama-cli -hf <repo>:<QUANT>` 或 `llama-server -hf <repo>:<QUANT>` 启动。
6. 当仓库使用自定义文件命名时，回退到 `--hf-repo` 加上 `--hf-file`。
7. 仅当仓库尚未提供 GGUF 文件时，才从 Transformers 权重进行转换。

## 快速开始

### 安装 llama.cpp

```bash
brew install llama.cpp
winget install llama.cpp
```

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
make
```

### 对受限仓库进行身份验证

```bash
hf auth login
```

### 在 Hub 上搜索

```text
https://huggingface.co/models?apps=llama.cpp&sort=trending
https://huggingface.co/models?search=Qwen3.6&apps=llama.cpp&sort=trending
https://huggingface.co/models?search=<term>&apps=llama.cpp&num_parameters=min:0,max:24B&sort=trending
```

### 直接从 Hub 运行

```bash
llama-cli -hf unsloth/Qwen3.6-35B-A3B-GGUF:UD-Q4_K_M
llama-server -hf unsloth/Qwen3.6-35B-A3B-GGUF:UD-Q4_K_M
```

### 运行指定的 GGUF 文件

```bash
llama-server \
    --hf-repo unsloth/Qwen3.6-35B-A3B-GGUF \
    --hf-file Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
    -c 4096
```

### 仅在无 GGUF 时执行转换

```bash
hf download <repo-without-gguf> --local-dir ./model-src
python convert_hf_to_gguf.py ./model-src \
    --outfile model-f16.gguf \
    --outtype f16
llama-quantize model-f16.gguf model-q4_k_m.gguf Q4_K_M
```

### 对本地服务器进行冒烟测试

```bash
llama-server -hf unsloth/Qwen3.6-35B-A3B-GGUF:UD-Q4_K_M
```

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer no-key" \
  -d '{
    "messages": [
      {"role": "user", "content": "Write a limerick about exception handling"}
    ]
  }'
```

## 量化方案选择

- 优先采用 HF 在 `?local-app=llama.cpp` 页面上标注为兼容的精确量化方案。
- 保留仓库原生标签（如 `UD-Q4_K_M`），不要将其标准化。
- 默认选择 `Q4_K_M`，除非仓库页面或硬件配置另有建议。
- 在内存允许的情况下，代码或技术类工作负载优先选择 `Q5_K_M` 或 `Q6_K`。
- 在 RAM 或 VRAM 预算紧张时，可考虑 `Q3_K_M`、`Q4_K_S`，或仓库自有的 `IQ` / `UD-*` 变体。
- 将 `mmproj-*.gguf` 文件视为投影器权重，而非主检查点。

## 加载参考文档

- 阅读 [hub-discovery.md](references/hub-discovery.md) 了解 URL 优先工作流、模型搜索、tree API 提取与命令重构。
- 阅读 [quantization.md](references/quantization.md) 了解格式表、模型规模、权衡与 `imatrix`。
- 阅读 [hardware.md](references/hardware.md) 了解 Metal、CUDA、ROCm 或 CPU 的构建与加速细节。

## 资源

- llama.cpp: `https://github.com/ggml-org/llama.cpp`
- Hugging Face GGUF + llama.cpp 文档: `https://huggingface.co/docs/hub/gguf-llamacpp`
- Hugging Face Local Apps 文档: `https://huggingface.co/docs/hub/main/local-apps`
- Hugging Face Local Agents 文档: `https://huggingface.co/docs/hub/agents-local`
- GGUF 转换 Space: `https://huggingface.co/spaces/ggml-org/gguf-my-repo`

## 限制

- 仅当任务明确匹配其上游产品或 API 范围时使用本技能。
- 在进行修改前，请依据最新的官方文档核实命令、API 行为、价格、配额、凭据以及部署影响。
- 切勿将生成的示例视为环境特定测试、安全审查或用户对破坏性/高成本操作的批准的替代。