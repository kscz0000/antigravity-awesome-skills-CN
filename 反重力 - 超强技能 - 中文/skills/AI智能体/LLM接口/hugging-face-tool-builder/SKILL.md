---
name: hugging-face-tool-builder
description: "创建可复用的命令行脚本和工具，用于调用 Hugging Face API，支持链式调用、管道操作和中间处理。可直接访问 API，也可使用 hf 命令行工具。当用户要求'构建 Hugging Face 工具'、'创建 HF API 脚本'、'Hugging Face CLI 工具'时使用。"
risk: unknown
source: community
---

# Hugging Face API 工具构建器

创建可复用的命令行脚本和工具，用于调用 Hugging Face API，支持链式调用、管道操作和中间处理。可直接访问 API，也可使用 `hf` 命令行工具。模型和数据集卡片可直接从仓库访问。

## 适用场景
- 需要围绕 Hugging Face API 或 `hf` 命令行工具构建可复用的 CLI 脚本。
- 需要支持链式调用、管道操作和中间处理的 shell 友好工具。
- 自动化重复的 Hub 任务，需要可组合的接口而非临时 API 调用。

## 脚本规则

务必遵循以下规则：
 - 脚本必须提供 `--help` 命令行参数，描述其输入和输出
 - 非破坏性脚本应在交付给用户前进行测试
 - 优先使用 Shell 脚本，复杂度高或用户需要时可使用 Python 或 TSX
 - 重要：使用 `HF_TOKEN` 环境变量作为 Authorization 请求头。例如：`curl -H "Authorization: Bearer ${HF_TOKEN}" https://huggingface.co/api/`。这提供了更高的速率限制和适当的数据访问授权。
 - 在确定最终设计前，先调查 API 返回结果的结构；在可组合性有优势的地方利用管道和链式调用——尽可能选择简单方案。
 - 完成后分享使用示例。

如有疑问或需要澄清，务必先确认用户偏好。

## 示例脚本

以下路径相对于本技能目录。

参考示例：
- `references/hf_model_papers_auth.sh` — 自动使用 `HF_TOKEN`，链式调用 trending → 模型元数据 → 模型卡片解析（含回退机制）；演示了多步 API 调用和受限/私有内容的认证规范。
- `references/find_models_by_paper.sh` — 通过 `--token` 可选使用 `HF_TOKEN`，一致的认证搜索，以及 arXiv 前缀搜索范围过窄时的重试路径；展示了弹性查询策略和清晰的用户帮助。
- `references/hf_model_card_frontmatter.sh` — 使用 `hf` CLI 下载模型卡片，提取 YAML frontmatter，输出 NDJSON 摘要（license、pipeline tag、tags、gated prompt flag），便于过滤。

基线示例（极简、最少逻辑、带 `HF_TOKEN` 请求头的原始 JSON 输出）：
- `references/baseline_hf_api.sh` — bash
- `references/baseline_hf_api.py` — python
- `references/baseline_hf_api.tsx` — typescript 可执行文件

可组合工具（stdin → NDJSON）：
- `references/hf_enrich_models.sh` — 从 stdin 读取模型 ID，逐个获取元数据，每行输出一个 JSON 对象，适用于流式管道。

通过管道实现可组合性（shell 友好的 JSON 输出）：
- `references/baseline_hf_api.sh 25 | jq -r '.[].id' | references/hf_enrich_models.sh | jq -s 'sort_by(.downloads) | reverse | .[:10]'`
- `references/baseline_hf_api.sh 50 | jq '[.[] | {id, downloads}] | sort_by(.downloads) | reverse | .[:10]'`
- `printf '%s\n' openai/gpt-oss-120b meta-llama/Meta-Llama-3.1-8B | references/hf_model_card_frontmatter.sh | jq -s 'map({id, license, has_extra_gated_prompt})'`

## 主要端点

以下是 `https://huggingface.co` 上可用的主要 API 端点

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

API 使用 OpenAPI 标准文档化，地址为 `https://huggingface.co/.well-known/openapi.json`。

**重要：** 不要尝试直接读取 `https://huggingface.co/.well-known/openapi.json`，文件过大无法处理。

**重要** 使用 `jq` 查询和提取相关部分。例如，

获取全部 160 个端点的命令

```bash
curl -s "https://huggingface.co/.well-known/openapi.json" | jq '.paths | keys | sort'
```

模型搜索端点详情

```bash
curl -s "https://huggingface.co/.well-known/openapi.json" | jq '.paths["/api/models"]'
```

你也可以查询端点以了解数据结构。查询时请限制返回数量，使其易于处理且具有代表性。

## 使用 HF 命令行工具

`hf` 命令行工具可进一步访问 Hugging Face 仓库内容和基础设施。

```bash
❯ hf --help
Usage: hf [OPTIONS] COMMAND [ARGS]...

  Hugging Face Hub CLI

Options:
  --help                Show this message and exit.

Commands:
  auth                 Manage authentication (login, logout, etc.).
  cache                Manage local cache directory.
  download             Download files from the Hub.
  endpoints            Manage Hugging Face Inference Endpoints.
  env                  Print information about the environment.
  jobs                 Run and manage Jobs on the Hub.
  repo                 Manage repos on the Hub.
  repo-files           Manage files in a repo on the Hub.
  upload               Upload a file or a folder to the Hub.
  upload-large-folder  Upload a large folder to the Hub.
  version              Print information about the hf version.
```

`hf` CLI 命令已取代现已弃用的 `huggingface_hub` CLI 命令。

## 限制
- 仅在任务明确符合上述范围时使用本技能。
- 输出不能替代特定环境的验证、测试或专家审查。
- 若缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
