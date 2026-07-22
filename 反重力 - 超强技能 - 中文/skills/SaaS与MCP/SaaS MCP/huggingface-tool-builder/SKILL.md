---
name: huggingface-tool-builder
description: 当用户希望构建工具/脚本或完成某项任务，并且使用 Hugging Face API 的数据会带来帮助时使用此技能。在需要链式或组合调用 API，或该任务需要重复/自动化执行时尤为有用。本技能会创建一个可复用的脚本来获取、丰富数据……触发词：HuggingFace、HF、API 工具、脚本生成、链式调用、自动化、Hugging Face API、可复用脚本
risk: unknown
source: https://github.com/huggingface/skills/tree/main/skills/huggingface-tool-builder
source_repo: huggingface/skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/huggingface/skills/blob/main/LICENSE
---

# Hugging Face API 工具构建器
## 何时使用

当用户希望构建工具/脚本或完成某项任务，并且使用 Hugging Face API 的数据会带来帮助时使用此技能。在需要链式或组合调用 API，或该任务需要重复/自动化执行时尤为有用。本技能会创建一个可复用的脚本来获取、丰富数据……


你的目标现在是创建可复用的命令行脚本与工具，以使用 Hugging Face API，并支持在需要时进行链式调用、管道传递与中间处理。你可以直接访问该 API，也可以使用 `hf` 命令行工具。模型与数据集的卡片可以直接从仓库访问。

## 脚本编写规则

请务必遵循以下规则：
 - 脚本必须接受 `--help` 命令行参数，以描述其输入与输出
 - 非破坏性脚本在交付给用户之前应先进行测试
 - 优先使用 Shell 脚本，但如果复杂度或用户需求要求，可使用 Python 或 TSX
 - 重要：使用 `HF_TOKEN` 环境变量作为 Authorization 请求头。例如：`curl -H "Authorization: Bearer ${HF_TOKEN}" https://huggingface.co/api/`。这将提供更高的速率限制和合适的数据访问授权。
 - 在确定最终设计之前，先考察 API 响应的结构形态；在可组合性会带来优势的地方使用管道与链式调用 —— 在可能的情况下优先采用简单的方案。
 - 完成后分享使用示例。

在存在疑问或需要澄清的地方，请务必与用户确认偏好。

## 示例脚本

以下路径相对于本技能目录。

参考示例：
- `references/hf_model_papers_auth.sh` —— 自动使用 `HF_TOKEN`，并链式调用 trending → 模型元数据 → 模型卡片解析（带回退）；演示了多步 API 用法以及对受限/私有内容的鉴权卫生。
- `references/find_models_by_paper.sh` —— 通过 `--token` 可选地使用 `HF_TOKEN`，提供一致的鉴权搜索，并在以 arXiv 前缀的搜索过于狭窄时提供重试路径；展示了具备韧性的查询策略与对用户清晰的帮助信息。
- `references/hf_model_card_frontmatter.sh` —— 使用 `hf` CLI 下载模型卡片，提取 YAML frontmatter，并输出 NDJSON 摘要（license、pipeline tag、tags、gated prompt 标记），便于筛选。

基线示例（极简、最小逻辑、原始 JSON 输出并附带 `HF_TOKEN` 请求头）：
- `references/baseline_hf_api.sh` —— bash
- `references/baseline_hf_api.py` —— python
- `references/baseline_hf_api.tsx` —— typescript 可执行文件

可组合工具（stdin → NDJSON）：
- `references/hf_enrich_models.sh` —— 从 stdin 读取模型 ID，逐个获取元数据，逐行输出一个 JSON 对象，以便构建流式管道。

通过管道实现的可组合性（适合 Shell 的 JSON 输出）：
- `references/baseline_hf_api.sh 25 | jq -r '.[].id' | references/hf_enrich_models.sh | jq -s 'sort_by(.downloads) | reverse | .[:10]'`
- `references/baseline_hf_api.sh 50 | jq '[.[] | {id, downloads}] | sort_by(.downloads) | reverse | .[:10]'`
- `printf '%s\n' openai/gpt-oss-120b meta-llama/Meta-Llama-3.1-8B | references/hf_model_card_frontmatter.sh | jq -s 'map({id, license, has_extra_gated_prompt})'`

## 高级端点

以下是 `https://huggingface.co` 上的主要 API 端点：

```
/api/datasets
/api/models
/api/spaces
/api/collections
/api/daily_papers
/api/notifications
/api/settings
/api/whoami-v2
/api/trending
/oauth/userinfo
```

## 访问 API

该 API 以 OpenAPI 标准进行文档化，地址为 `https://huggingface.co/.well-known/openapi.json`。

**重要：** 不要尝试直接读取 `https://huggingface.co/.well-known/openapi.json`，因为它太大而无法处理。

**重要**：使用 `jq` 查询并提取相关部分。例如：

 获取全部 160 个端点的命令

```bash
curl -s "https://huggingface.co/.well-known/openapi.json" | jq '.paths | keys | sort'
```

模型搜索端点详情

```bash
curl -s "https://huggingface.co/.well-known/openapi.json" | jq '.paths["/api/models"]'
```

你也可以查询端点以了解数据的结构形态。查询时请将结果限制在较小的数量，使其易于处理，同时又具有代表性。

## 使用 HF 命令行工具

`hf` 命令行工具可让你进一步访问 Hugging Face 仓库内容与基础设施。

```bash
❯ hf --help
Usage: hf [OPTIONS] COMMAND [ARGS]...

  Hugging Face Hub CLI

Options:
  --help                Show this message and exit.

Commands:
  auth                 Manage authentication (login, logout, etc.).
  buckets              Commands to interact with buckets.
  cache                Manage local cache directory.
  collections          Interact with collections on the Hub.
  datasets             Interact with datasets on the Hub.
  discussions          Manage discussions and pull requests on the Hub.
  download             Download files from the Hub.
  endpoints            Manage Hugging Face Inference Endpoints.
  env                  Print information about the environment.
  extensions           Manage hf CLI extensions.
  jobs                 Run and manage Jobs on the Hub.
  models               Interact with models on the Hub.
  papers               Interact with papers on the Hub.
  repos                Manage repos on the Hub.
  skills               Manage skills for AI assistants.
  spaces               Interact with spaces on the Hub.
  sync                 Sync files between local directory and a bucket.
  upload               Upload a file or a folder to the Hub.
  upload-large-folder  Upload a large folder to the Hub.
  version              Print information about the hf version.
  webhooks             Manage webhooks on the Hub.
```

`hf` CLI 命令已取代现已弃用的 `huggingface-cli` 命令。

## 局限性

- 仅当任务明确匹配其上游产品或 API 范围时才使用此技能。
- 在进行任何变更之前，请根据当前官方文档验证命令、API 行为、价格、配额、凭据以及部署影响。
- 不要将生成的示例视为环境特定测试、安全审查，或针对破坏性/高成本操作的用户批准的替代品。