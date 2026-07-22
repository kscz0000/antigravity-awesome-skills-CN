---
name: m365-agents-py
description: Microsoft 365 Agents SDK 的 Python 版本。使用 aiohttp 托管、AgentApplication 路由、流式响应和基于 MSAL 的认证，构建面向 Teams/M365/Copilot Studio 的多渠道智能体。当用户要求'构建 M365 智能体'、'Teams 机器人开发'、'Copilot Studio 集成'、'aiohttp 托管 AgentApplication'、'M365 Agents SDK Python'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Microsoft 365 Agents SDK (Python)

使用 Microsoft Agents SDK，配合 aiohttp 托管、AgentApplication 路由、流式响应和基于 MSAL 的认证，构建面向 Microsoft 365、Teams 和 Copilot Studio 的企业级智能体。

## 实现前须知
- 使用 microsoft-docs MCP 验证 AgentApplication、start_agent_process 和认证选项的最新 API 签名。
- 在 PyPI 上确认你计划使用的 microsoft-agents-* 包的版本。

## 重要通知 — 导入变更

> **⚠️ 破坏性变更**：近期更新将 Python 导入结构从 `microsoft.agents` 改为 `microsoft_agents`（使用下划线代替点号）。

## 安装

```bash
pip install microsoft-agents-hosting-core
pip install microsoft-agents-hosting-aiohttp
pip install microsoft-agents-activity
pip install microsoft-agents-authentication-msal
pip install microsoft-agents-copilotstudio-client
pip install python-dotenv aiohttp
```

## 环境变量 (.env)

```bash
CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENTID=<client-id>
CONNECTIONS__SERVICE_CONNECTION__SETTINGS__CLIENTSECRET=<client-secret>
CONNECTIONS__SERVICE_CONNECTION__SETTINGS__TENANTID=<tenant-id>

# Optional: OAuth handlers for auto sign-in
AGENTAPPLICATION__USERAUTHORIZATION__HANDLERS__GRAPH__SETTINGS__AZUREBOTOAUTHCONNECTIONNAME=<connection-name>

# Optional: Azure OpenAI for streaming
AZURE_OPENAI_ENDPOINT=<endpoint>
AZURE_OPENAI_API_VERSION=<version>
AZURE_OPENAI_API_KEY=<key>

# Optional: Copilot Studio client
COPILOTSTUDIOAGENT__ENVIRONMENTID=<environment-id>
COPILOTSTUDIOAGENT__SCHEMANAME=<schema-name>
COPILOTSTUDIOAGENT__TENANTID=<tenant-id>
COPILOTSTUDIOAGENT__AGENTAPPID=<app-id>
```

## 核心工作流：aiohttp 托管的 AgentApplication

```python
import logging
from os import environ

from dotenv import load_dotenv
from aiohttp.web import Request, Response, Application, run_app

from microsoft_agents.activity import load_configuration_from_env
from microsoft_agents.hosting.core import (
    Authorization,
    AgentApplication,
    TurnState,
    TurnContext,
    MemoryStorage,
)
from microsoft_agents.hosting.aiohttp import (
    CloudAdapter,
    start_agent_process,
    jwt_authorization_middleware,
)
from microsoft_agents.authentication.msal import MsalConnectionManager

# Enable logging
ms_agents_logger = logging.getLogger("microsoft_agents")
ms_agents_logger.addHandler(logging.StreamHandler())
ms_agents_logger.setLevel(logging.INFO)

# Load configuration
load_dotenv()
agents_sdk_config = load_configuration_from_env(environ)

# Create storage and connection manager
STORAGE = MemoryStorage()
CONNECTION_MANAGER = MsalConnectionManager(**agents_sdk_config)
ADAPTER = CloudAdapter(connection_manager=CONNECTION_MANAGER)
AUTHORIZATION = Authorization(STORAGE, CONNECTION_MANAGER, **agents_sdk_config)

# Create AgentApplication
AGENT_APP = AgentApplicationTurnState


@AGENT_APP.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, _state: TurnState):
    await context.send_activity("Welcome to the agent!")


@AGENT_APP.activity("message")
async def on_message(context: TurnContext, _state: TurnState):
    await context.send_activity(f"You said: {context.activity.text}")


@AGENT_APP.error
async def on_error(context: TurnContext, error: Exception):
    await context.send_activity("The agent encountered an error.")


# Server setup
async def entry_point(req: Request) -> Response:
    agent: AgentApplication = req.app["agent_app"]
    adapter: CloudAdapter = req.app["adapter"]
    return await start_agent_process(req, agent, adapter)


APP = Application(middlewares=[jwt_authorization_middleware])
APP.router.add_post("/api/messages", entry_point)
APP["agent_configuration"] = CONNECTION_MANAGER.get_default_connection_configuration()
APP["agent_app"] = AGENT_APP
APP["adapter"] = AGENT_APP.adapter

if __name__ == "__main__":
    run_app(APP, host="localhost", port=environ.get("PORT", 3978))
```

## AgentApplication 路由

```python
import re
from microsoft_agents.hosting.core import (
    AgentApplication, TurnState, TurnContext, MessageFactory
)
from microsoft_agents.activity import ActivityTypes

AGENT_APP = AgentApplicationTurnState

# Welcome handler
@AGENT_APP.conversation_update("membersAdded")
async def on_members_added(context: TurnContext, _state: TurnState):
    await context.send_activity("Welcome!")

# Regex-based message handler
@AGENT_APP.message(re.compile(r"^hello$", re.IGNORECASE))
async def on_hello(context: TurnContext, _state: TurnState):
    await context.send_activity("Hello!")

# Simple string message handler
@AGENT_APP.message("/status")
async def on_status(context: TurnContext, _state: TurnState):
    await context.send_activity("Status: OK")

# Auth-protected message handler
@AGENT_APP.message("/me", auth_handlers=["GRAPH"])
async def on_profile(context: TurnContext, state: TurnState):
    token_response = await AGENT_APP.auth.get_token(context, "GRAPH")
    if token_response and token_response.token:
        # Use token to call Graph API
        await context.send_activity("Profile retrieved")

# Invoke activity handler
@AGENT_APP.activity(ActivityTypes.invoke)
async def on_invoke(context: TurnContext, _state: TurnState):
    invoke_response = Activity(
        type=ActivityTypes.invoke_response, value={"status": 200}
    )
    await context.send_activity(invoke_response)

# Fallback message handler
@AGENT_APP.activity("message")
async def on_message(context: TurnContext, _state: TurnState):
    await context.send_activity(f"Echo: {context.activity.text}")

# Error handler
@AGENT_APP.error
async def on_error(context: TurnContext, error: Exception):
    await context.send_activity("An error occurred.")
```

## 使用 Azure OpenAI 的流式响应

```python
from openai import AsyncAzureOpenAI
from microsoft_agents.activity import SensitivityUsageInfo

CLIENT = AsyncAzureOpenAI(
    api_version=environ["AZURE_OPENAI_API_VERSION"],
    azure_endpoint=environ["AZURE_OPENAI_ENDPOINT"],
    api_key=environ["AZURE_OPENAI_API_KEY"]
)

@AGENT_APP.message("poem")
async def on_poem_message(context: TurnContext, _state: TurnState):
    # Configure streaming response
    context.streaming_response.set_feedback_loop(True)
    context.streaming_response.set_generated_by_ai_label(True)
    context.streaming_response.set_sensitivity_label(
        SensitivityUsageInfo(
            type="https://schema.org/Message",
            schema_type="CreativeWork",
            name="Internal",
        )
    )
    context.streaming_response.queue_informative_update("Starting a poem...\n")

    # Stream from Azure OpenAI
    streamed_response = await CLIENT.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a creative assistant."},
            {"role": "user", "content": "Write a poem about Python."}
        ],
        stream=True,
    )
    
    try:
        async for chunk in streamed_response:
            if chunk.choices and chunk.choices[0].delta.content:
                context.streaming_response.queue_text_chunk(
                    chunk.choices[0].delta.content
                )
    finally:
        await context.streaming_response.end_stream()
```

## OAuth / 自动登录

```python
@AGENT_APP.message("/logout")
async def logout(context: TurnContext, state: TurnState):
    await AGENT_APP.auth.sign_out(context, "GRAPH")
    await context.send_activity(MessageFactory.text("You have been logged out."))


@AGENT_APP.message("/me", auth_handlers=["GRAPH"])
async def profile_request(context: TurnContext, state: TurnState):
    user_token_response = await AGENT_APP.auth.get_token(context, "GRAPH")
    if user_token_response and user_token_response.token:
        # Use token to call Microsoft Graph
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {user_token_response.token}",
                "Content-Type": "application/json",
            }
            async with session.get(
                "https://graph.microsoft.com/v1.0/me", headers=headers
            ) as response:
                if response.status == 200:
                    user_info = await response.json()
                    await context.send_activity(f"Hello, {user_info['displayName']}!")
```

## Copilot Studio 客户端（直连引擎）

```python
import asyncio
from msal import PublicClientApplication
from microsoft_agents.activity import ActivityTypes, load_configuration_from_env
from microsoft_agents.copilotstudio.client import (
    ConnectionSettings,
    CopilotClient,
)

# Token cache (local file for interactive flows)
class LocalTokenCache:
    # See samples for full implementation
    pass

def acquire_token(settings, app_client_id, tenant_id):
    pca = PublicClientApplication(
        client_id=app_client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
    )
    
    token_request = {"scopes": ["https://api.powerplatform.com/.default"]}
    accounts = pca.get_accounts()
    
    if accounts:
        response = pca.acquire_token_silent(token_request["scopes"], account=accounts[0])
        return response.get("access_token")
    else:
        response = pca.acquire_token_interactive(**token_request)
        return response.get("access_token")


async def main():
    settings = ConnectionSettings(
        environment_id=environ.get("COPILOTSTUDIOAGENT__ENVIRONMENTID"),
        agent_identifier=environ.get("COPILOTSTUDIOAGENT__SCHEMANAME"),
    )
    
    token = acquire_token(
        settings,
        app_client_id=environ.get("COPILOTSTUDIOAGENT__AGENTAPPID"),
        tenant_id=environ.get("COPILOTSTUDIOAGENT__TENANTID"),
    )
    
    copilot_client = CopilotClient(settings, token)
    
    # Start conversation
    act = copilot_client.start_conversation(True)
    async for action in act:
        if action.text:
            print(action.text)
    
    # Ask question
    replies = copilot_client.ask_question("Hello!", action.conversation.id)
    async for reply in replies:
        if reply.type == ActivityTypes.message:
            print(reply.text)


asyncio.run(main())
```

## 最佳实践

1. 使用 `microsoft_agents` 导入前缀（下划线，不是点号）。
2. `MemoryStorage` 仅用于开发环境；生产环境请使用 BlobStorage 或 CosmosDB。
3. 始终使用 `load_configuration_from_env(environ)` 加载 SDK 配置。
4. 在 aiohttp Application 的 middlewares 中加入 `jwt_authorization_middleware`。
5. 使用 `MsalConnectionManager` 进行基于 MSAL 的认证。
6. 使用流式响应时，在 finally 块中调用 `end_stream()`。
7. 在消息装饰器上使用 `auth_handlers` 参数保护 OAuth 路由。
8. 密钥存放在环境变量中，不要写在源代码里。

## 参考文件

| 文件 | 内容 |
| --- | --- |
| references/acceptance-criteria.md | 导入路径、托管管线、流式响应、OAuth 和 Copilot Studio 模式 |

## 参考链接

| 资源 | URL |
| --- | --- |
| Microsoft 365 Agents SDK | https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/ |
| GitHub 示例 (Python) | https://github.com/microsoft/Agents-for-python |
| PyPI 包 | https://pypi.org/search/?q=microsoft-agents |
| 集成 Copilot Studio | https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/integrate-with-mcs |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 输出内容不能替代针对具体环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
