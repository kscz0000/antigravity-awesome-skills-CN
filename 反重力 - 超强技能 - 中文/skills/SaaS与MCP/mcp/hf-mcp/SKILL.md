---
name: hf-mcp
description: 通过 MCP 服务器工具使用 Hugging Face Hub。搜索模型、数据集、Spaces、论文。获取仓库详情、抓取文档、运行计算任务，并将 Gradio Spaces 用作 AI 工具。在已连接 HF MCP 服务器时可用。触发词：hf-mcp、Hugging Face、MCP 服务器、HuggingFace Hub、HF MCP。
risk: unknown
source: https://github.com/huggingface/skills/tree/main/hf-mcp/skills/hf-mcp
source_repo: huggingface/skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/huggingface/skills/blob/main/LICENSE
---

# Hugging Face MCP 服务器
## 何时使用

当你需要通过 MCP 服务器工具使用 Hugging Face Hub 时使用本技能。可以搜索模型、数据集、Spaces、论文。获取仓库详情、抓取文档、运行计算任务，并将 Gradio Spaces 用作 AI 工具。在已连接 HF MCP 服务器时可用。


将 AI 助手接入 Hugging Face Hub。配置地址：https://huggingface.co/settings/mcp

## 使用场景与示例

### 为某项任务找到最佳模型

```
User: "Find the best model for code generation"

1. model_search(task="text-generation", query="code", sort="trendingScore", limit=10)
2. hub_repo_details(repo_ids=["top-result-id"], include_readme=true)
```

### 对比不同提供方的模型

```
User: "Compare Llama vs Qwen for text generation"

1. model_search(author="meta-llama", task="text-generation", sort="downloads", limit=5)
2. model_search(author="Qwen", task="text-generation", sort="downloads", limit=5)
3. hub_repo_details(repo_ids=["meta-llama/Llama-3.2-1B", "Qwen/Qwen3-8B"], include_readme=true)
```

### 查找训练数据集

```
User: "Find datasets for sentiment analysis in English"

1. dataset_search(query="sentiment", tags=["language:en", "task_categories:text-classification"], sort="downloads")
2. hub_repo_details(repo_ids=["top-dataset-id"], repo_type="dataset", include_readme=true)
```

### 发现 AI 工具（MCP Spaces）

```
User: "Find a tool that can remove image backgrounds"

1. space_search(query="background removal", mcp=true)
2. dynamic_space(operation="view_parameters", space_name="result-space-id")
3. dynamic_space(operation="invoke", space_name="result-space-id", parameters="{...}")
```

### 生成图像

```
User: "Create an image of a robot reading a book"

1. dynamic_space(operation="discover")  # See available tasks
2. gr1_flux1_schnell_infer(prompt="a robot sitting in a library reading a book, warm lighting, detailed")
```

### 调研某个主题

```
User: "What are the latest papers on RLHF?"

1. paper_search(query="reinforcement learning from human feedback", results_limit=10)
2. hub_repo_details(repo_ids=["paper-linked-model"], include_readme=true)  # If paper links to models
```

### 学习如何使用某个库

```
User: "How do I fine-tune with LoRA using PEFT?"

1. hf_doc_search(query="LoRA fine-tuning", product="peft")
2. hf_doc_fetch(doc_url="https://huggingface.co/docs/peft/...")
```

### 运行一个快速的 GPU 任务

```
User: "Run this Python script on a GPU"

hf_jobs(operation="uv", args={
  "script": "# /// script\n# dependencies = [\"torch\"]\n# ///\nimport torch\nprint(torch.cuda.is_available())",
  "flavor": "t4-small"
})
```

### 在云端 GPU 上训练模型

```
User: "Run my training script on an A10G"

hf_jobs(operation="run", args={
  "image": "pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime",
  "command": ["/bin/sh", "-lc", "pip install transformers trl && python train.py"],
  "flavor": "a10g-small",
  "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

### 查看任务状态

```
User: "What's happening with my training job?"

1. hf_jobs(operation="ps")
2. hf_jobs(operation="logs", args={"job_id": "job-xxxxx"})
```

### 探索热门趋势

```
User: "What models are trending right now?"

model_search(sort="trendingScore", limit=20)
```

### 获取模型卡片详情

```
User: "Tell me about Mistral-7B"

hub_repo_details(repo_ids=["mistralai/Mistral-7B-v0.1"], include_readme=true)
```

### 查找量化模型

```
User: "Find GGUF versions of Llama 3"

model_search(query="Llama 3 GGUF", sort="downloads", limit=10)
```

### 将 Gradio Space 用作工具

```
User: "Transcribe this audio file"

1. space_search(query="speech to text transcription", mcp=true)
2. dynamic_space(operation="view_parameters", space_name="openai/whisper")
3. dynamic_space(operation="invoke", space_name="openai/whisper", parameters="{\"audio\": \"...\"}")
```

### 调度周期任务

```
User: "Run this data sync every day at midnight"

hf_jobs(operation="scheduled uv", args={
  "script": "...",
  "cron": "0 0 * * *",
  "flavor": "cpu-basic"
})
```

## 工具选择指南

| 目标 | 工具 |
|------|------|
| 查找模型 | `model_search` |
| 查找数据集 | `dataset_search` |
| 查找 Spaces/应用 | `space_search` |
| 查找论文 | `paper_search` |
| 获取仓库 README/详情 | `hub_repo_details` |
| 学习库的使用方法 | `hf_doc_search` → `hf_doc_fetch` |
| 在 GPU/CPU 上运行代码 | `hf_jobs` |
| 将 Gradio 应用用作工具 | `dynamic_space` |
| 生成图像 | `gr1_flux1_schnell_infer` 或 `dynamic_space` |
| 检查认证 | `hf_whoami` |

## 提示

- 使用 `sort="trendingScore"` 查找当下热门的内容
- 使用 `sort="downloads"` 查找经过实战检验的方案
- 在 `space_search` 中设置 `mcp=true` 以查找可作为工具使用的 Spaces
- 在 `hub_repo_details` 中使用 `include_readme=true` 获取完整的模型/数据集文档
- 对于需要访问私有仓库的任务，始终包含 `secrets: {"HF_TOKEN": "$HF_TOKEN"}`
- 使用 `dynamic_space(operation="discover")` 查看所有可用的基于 Space 的任务

## 限制

- 仅当任务明确匹配其上游产品或 API 范围时才使用本技能。
- 在进行更改之前，请根据当前官方文档验证命令、API 行为、定价、配额、凭证及部署效果。
- 不要将生成的示例替代特定环境的测试、安全审查或用户对破坏性或高成本操作的批准。