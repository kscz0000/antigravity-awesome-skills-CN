# Weaviate 环境要求

在构建连接 Weaviate 且需要外部推理 provider 密钥的应用时参考此文档。

## 必需的 Weaviate 认证

- `WEAVIATE_URL`
- `WEAVIATE_API_KEY`

## 外部 Provider 环境变量与请求头

| Provider | 环境变量 | 发送到 Weaviate 的请求头 |
|----------|----------|--------------------------|
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

- Provider 密钥不会自动转发。将 `WEAVIATE_PROVIDER_KEYS` 设置为以逗号分隔的允许列表，例如 `OPENAI_API_KEY,COHERE_API_KEY`。
- 只设置你的 collection 配置实际用到的 provider 密钥。
- 如果配置了多个 provider，则只包含与这些 provider 对应的请求头。
