# Weaviate 环境要求

在构建需要连接 Weaviate 与外部推理服务密钥的应用时，请阅读本指引。

## 必需的 Weaviate 鉴权

- `WEAVIATE_URL`
- `WEAVIATE_API_KEY`

## 外部服务商环境变量与请求头

| 服务商 | 环境变量 | 发往 Weaviate 的请求头 |
|----------|--------------------------|-----------------------------|
| Anthropic | `ANTHROPIC_API_KEY` | `X-Anthropic-Api-Key` |
| Anyscale | `ANYSCALE_API_KEY` | `X-Anyscale-Api-Key` |
| AWS | `AWS_ACCESS_KEY`, `AWS_SECRET_KEY` | `X-Aws-Access-Key`, `X-Aws-Secret-Key` |
| Cohere | `COHERE_API_KEY` | `X-Cohere-Api-Key` |
| Databricks | `DATABRICKS_TOKEN` | `X-Databricks-Token` |
| Friendli | `FRIENDLI_TOKEN` | `X-Friendli-Api-Key` |
| Google Vertex AI | `VERTEX_API_KEY` | `X-Goog-Vertex-Api-Key` |
| Google AI Studio | `STUDIO_API_KEY` | `X-Goog-Studio-Api-Key` |
| HuggingFace | `HUGGINGFACE_API_KEY` | `X-HuggingFace-Api-Key` |
| Jina AI | `JINAAI_API_KEY` | `X-JinaAI-Api-Key` |
| Mistral | `MISTRAL_API_KEY` | `X-Mistral-Api-Key` |
| NVIDIA | `NVIDIA_API_KEY` | `X-Nvidia-Api-Key` |
| OpenAI | `OPENAI_API_KEY` | `X-OpenAI-Api-Key` |
| Azure OpenAI | `AZURE_API_KEY` | `X-Azure-Api-Key` |
| Voyage AI | `VOYAGE_API_KEY` | `X-Voyage-Api-Key` |
| xAI | `XAI_API_KEY` | `X-Xai-Api-Key` |

## 使用说明

- 仅设置当前集合配置真正用到的服务商密钥。
- 若配置了多个服务商，请一并填入对应的请求头。

## 官方 `.env` 模板

在所有 cookbook 应用中均使用本模板，随后仅提示用户填写其应用实际需要的键值。

`WEAVIATE_URL` 与 `WEAVIATE_API_KEY` 对连接 Weaviate 的应用为必填项。

```dotenv
# Required for Weaviate cookbook apps (must be filled by user)
WEAVIATE_URL=
WEAVIATE_API_KEY=

# Common app-level settings (uncomment when needed by the selected cookbook)
# COLLECTIONS=
# CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173

# External provider keys (uncomment only what the target collection uses)
# ANTHROPIC_API_KEY=
# ANYSCALE_API_KEY=
# AWS_ACCESS_KEY=
# AWS_SECRET_KEY=
# AZURE_API_KEY=
# COHERE_API_KEY=
# DATABRICKS_TOKEN=
# FRIENDLI_TOKEN=
# HUGGINGFACE_API_KEY=
# JINAAI_API_KEY=
# MISTRAL_API_KEY=
# NVIDIA_API_KEY=
# OPENAI_API_KEY=
# STUDIO_API_KEY=
# VERTEX_API_KEY=
# VOYAGE_API_KEY=
# XAI_API_KEY=
```

## 用户填写指引（必须遵循）

1. 基于本模板创建本地 `.env` 文件。
2. 始终提示用户填写：
   - `WEAVIATE_URL`
   - `WEAVIATE_API_KEY`
3. 仅让其取消注释并填写其 Weaviate 集合真正需要的服务商密钥。
4. `.env` 仅保留在本地，并加入 `.gitignore`。