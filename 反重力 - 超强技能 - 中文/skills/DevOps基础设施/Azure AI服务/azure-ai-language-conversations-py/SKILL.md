---
name: azure-ai-language-conversations-py
description: 使用 azure-ai-language-conversations Python SDK 实现对话语言理解（CLU）。在处理 ConversationAnalysisClient 以分析对话意图和实体、构建 NLP 功能或将语言理解集成到应用程序时使用。
risk: unknown
source: https://github.com/microsoft/skills/tree/main/.github/plugins/azure-sdk-python/skills/azure-ai-language-conversations-py
source_repo: microsoft/skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/microsoft/skills/blob/main/LICENSE
---

# 适用于 Python 的 Azure AI 语言对话
## 何时使用

当需要使用 azure-ai-language-conversations Python SDK 实现对话语言理解（CLU）时使用本技能。在处理 ConversationAnalysisClient 以分析对话意图和实体、构建 NLP 功能，或将语言理解集成到应用程序时使用。


## 系统提示

你是一位专注于 Azure AI 服务和自然语言处理的资深 Python 开发者。
你的任务是帮助用户使用 `azure-ai-language-conversations` SDK 实现对话语言理解（CLU）。

在响应有关 Azure AI 语言对话的请求时：
1. 始终使用最新版本的 `azure-ai-language-conversations` SDK。
2. 强调将 `ConversationAnalysisClient` 与 `DefaultAzureCredential` 配合使用。
3. 提供清晰的代码示例，演示如何构建对话负载。
4. 妥善处理异常。

## 身份验证与生命周期

> **🔑 以下两条规则适用于下面的所有代码示例：**
>
> 1. **优先使用 `DefaultAzureCredential`。** 它在本地（Azure CLI / VS Code / Developer CLI）和 Azure 中（托管标识、工作负载标识）均可使用，无需修改代码。避免使用连接字符串、账户/API 密钥——它们会绕过 Entra 审计与密钥轮换。
>    - 本地开发：`DefaultAzureCredential` 可直接使用。
>    - 生产环境：设置 `AZURE_TOKEN_CREDENTIALS=prod`（或 `AZURE_TOKEN_CREDENTIALS=<specific_credential>`），将凭据链限制为生产安全的凭据。
> 2. **将每个客户端包裹在上下文管理器中**，以便以确定性的方式释放 HTTP 传输、套接字和令牌缓存：
>    - 同步：`with <Client>(...) as client:`
>    - 异步：`async with <Client>(...) as client:` **以及** `async with DefaultAzureCredential() as credential:`（来自 `azure.identity.aio`）
>
> 代码片段可能会对上述设置进行缩写，但生产代码应始终遵循这两条规则。

`ConversationAnalysisClient` 接受 `TokenCredential`，例如 `DefaultAzureCredential`。使用令牌凭据——它在本地（Azure CLI / VS Code / Developer CLI）和 Azure 中（托管标识、工作负载标识）均可使用，无需修改代码。

### 遗留方案：API 密钥（现有的密钥部署）

新代码应使用 `DefaultAzureCredential`。仅当存在尚未迁移到 Entra ID 的现有密钥部署时才使用 `AzureKeyCredential`——例如，仍在完成 Entra 推广的受监管环境。

```python
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

endpoint = os.environ["AZURE_CONVERSATIONS_ENDPOINT"]
key = os.environ["AZURE_CONVERSATIONS_KEY"]

with ConversationAnalysisClient(endpoint, AzureKeyCredential(key)) as client:
    # 有关 analyze_conversation 负载，请参阅下方"基础对话分析"
    ...
```

## 最佳实践
- **选择同步或异步，并保持一致。** 不要在同一调用链中混用 `azure.ai.language.conversations` 同步客户端和 `azure.ai.language.conversations.aio` 异步客户端。每个模块选择一种模式。
- **始终对客户端和异步凭据使用上下文管理器。** 将每个客户端包裹在 `with ConversationAnalysisClient(...) as client:`（同步）或 `async with ConversationAnalysisClient(...) as client:`（异步）中。对于来自 `azure.identity.aio` 的异步 `DefaultAzureCredential`，还需要使用 `async with credential:`，以确保令牌和传输资源被正确清理。
- **使用 `DefaultAzureCredential`** 实现跨本地开发和 Azure 的可移植身份验证（避免使用 API 密钥；它们会绕过 Entra 审计与密钥轮换）。
- 使用环境变量配置终结点、项目名称和部署名称。
- 在 `conversationItem` 负载中清晰映射 `participantId` 和 `id` 字段。

## 示例

### 基础对话分析
```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.language.conversations import ConversationAnalysisClient

endpoint = os.environ["AZURE_CONVERSATIONS_ENDPOINT"]
project_name = os.environ["AZURE_CONVERSATIONS_PROJECT"]
deployment_name = os.environ["AZURE_CONVERSATIONS_DEPLOYMENT"]

# DefaultAzureCredential 在本地和 Azure 中均可使用，无需修改代码。
credential = DefaultAzureCredential()

with ConversationAnalysisClient(endpoint, credential) as client:
    query = "Send an email to Carol about the tomorrow's meeting"
    result = client.analyze_conversation(
        task={
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "participantId": "1",
                    "id": "1",
                    "modality": "text",
                    "language": "en",
                    "text": query
                },
                "isLoggingEnabled": False
            },
            "parameters": {
                "projectName": project_name,
                "deploymentName": deployment_name,
                "verbose": True
            }
        }
    )

    print(f"Top intent: {result['result']['prediction']['topIntent']}")

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时才使用本技能。
- 在应用更改之前，请验证命令、生成的代码、依赖项、凭据以及外部服务的行为。
- 不要将示例视为特定环境测试、安全评审或用户对破坏性或高成本操作的批准。
