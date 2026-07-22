---
name: agent-framework-azure-ai-py
description: "使用 Microsoft Agent Framework Python SDK 在 Azure AI Foundry 上构建持久化智能体。触发词：Azure AI Agent、持久化智能体、Agent Framework、Azure 托管智能体、Python SDK、AzureAIAgentsProvider、Hosted Tools、MCP 工具、对话线程持久化"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Agent Framework Azure 托管智能体

使用 Microsoft Agent Framework Python SDK 在 Azure AI Foundry 上构建持久化智能体。

## 架构

```
用户查询 → AzureAIAgentsProvider → Azure AI Agent Service (持久化)
                    ↓
              Agent.run() / Agent.run_stream()
                    ↓
              工具: 函数 | 托管 (代码/搜索/网页) | MCP
                    ↓
              AgentThread (对话持久化)
```

## 安装

```bash
# 完整框架（推荐）
pip install agent-framework --pre

# 或仅安装 Azure 专用包
pip install agent-framework-azure-ai --pre
```

## 环境变量

```bash
export AZURE_AI_PROJECT_ENDPOINT="https://<project>.services.ai.azure.com/api/projects/<project-id>"
export AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
export BING_CONNECTION_ID="your-bing-connection-id"  # 用于网页搜索
```

## 身份认证

```python
from azure.identity.aio import AzureCliCredential, DefaultAzureCredential

# 开发环境
credential = AzureCliCredential()

# 生产环境
credential = DefaultAzureCredential()
```

## 核心工作流

### 基础智能体

```python
import asyncio
from agent_framework.azure import AzureAIAgentsProvider
from azure.identity.aio import AzureCliCredential

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="MyAgent",
            instructions="You are a helpful assistant.",
        )
        
        result = await agent.run("Hello!")
        print(result.text)

asyncio.run(main())
```

### 带函数工具的智能体

```python
from typing import Annotated
from pydantic import Field
from agent_framework.azure import AzureAIAgentsProvider
from azure.identity.aio import AzureCliCredential

def get_weather(
    location: Annotated[str, Field(description="City name to get weather for")],
) -> str:
    """Get the current weather for a location."""
    return f"Weather in {location}: 72°F, sunny"

def get_current_time() -> str:
    """Get the current UTC time."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="WeatherAgent",
            instructions="You help with weather and time queries.",
            tools=[get_weather, get_current_time],  # 直接传递函数
        )
        
        result = await agent.run("What's the weather in Seattle?")
        print(result.text)
```

### 带托管工具的智能体

```python
from agent_framework import (
    HostedCodeInterpreterTool,
    HostedFileSearchTool,
    HostedWebSearchTool,
)
from agent_framework.azure import AzureAIAgentsProvider
from azure.identity.aio import AzureCliCredential

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="MultiToolAgent",
            instructions="You can execute code, search files, and search the web.",
            tools=[
                HostedCodeInterpreterTool(),
                HostedWebSearchTool(name="Bing"),
            ],
        )
        
        result = await agent.run("Calculate the factorial of 20 in Python")
        print(result.text)
```

### 流式响应

```python
async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="StreamingAgent",
            instructions="You are a helpful assistant.",
        )
        
        print("Agent: ", end="", flush=True)
        async for chunk in agent.run_stream("Tell me a short story"):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print()
```

### 对话线程

```python
from agent_framework.azure import AzureAIAgentsProvider
from azure.identity.aio import AzureCliCredential

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="ChatAgent",
            instructions="You are a helpful assistant.",
            tools=[get_weather],
        )
        
        # 创建线程用于对话持久化
        thread = agent.get_new_thread()
        
        # 第一轮
        result1 = await agent.run("What's the weather in Seattle?", thread=thread)
        print(f"Agent: {result1.text}")
        
        # 第二轮 - 上下文保持
        result2 = await agent.run("What about Portland?", thread=thread)
        print(f"Agent: {result2.text}")
        
        # 保存线程 ID 以便后续恢复
        print(f"Conversation ID: {thread.conversation_id}")
```

### 结构化输出

```python
from pydantic import BaseModel, ConfigDict
from agent_framework.azure import AzureAIAgentsProvider
from azure.identity.aio import AzureCliCredential

class WeatherResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    location: str
    temperature: float
    unit: str
    conditions: str

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="StructuredAgent",
            instructions="Provide weather information in structured format.",
            response_format=WeatherResponse,
        )
        
        result = await agent.run("Weather in Seattle?")
        weather = WeatherResponse.model_validate_json(result.text)
        print(f"{weather.location}: {weather.temperature}°{weather.unit}")
```

## Provider 方法

| 方法 | 描述 |
|------|------|
| `create_agent()` | 在 Azure AI 服务上创建新智能体 |
| `get_agent(agent_id)` | 通过 ID 获取现有智能体 |
| `as_agent(sdk_agent)` | 包装 SDK Agent 对象（无 HTTP 调用） |

## 托管工具快速参考

| 工具 | 导入 | 用途 |
|------|------|------|
| `HostedCodeInterpreterTool` | `from agent_framework import HostedCodeInterpreterTool` | 执行 Python 代码 |
| `HostedFileSearchTool` | `from agent_framework import HostedFileSearchTool` | 搜索向量存储 |
| `HostedWebSearchTool` | `from agent_framework import HostedWebSearchTool` | Bing 网页搜索 |
| `HostedMCPTool` | `from agent_framework import HostedMCPTool` | 服务管理的 MCP |
| `MCPStreamableHTTPTool` | `from agent_framework import MCPStreamableHTTPTool` | 客户端管理的 MCP |

## 完整示例

```python
import asyncio
from typing import Annotated
from pydantic import BaseModel, Field
from agent_framework import (
    HostedCodeInterpreterTool,
    HostedWebSearchTool,
    MCPStreamableHTTPTool,
)
from agent_framework.azure import AzureAIAgentsProvider
from azure.identity.aio import AzureCliCredential


def get_weather(
    location: Annotated[str, Field(description="City name")],
) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: 72°F, sunny"


class AnalysisResult(BaseModel):
    summary: str
    key_findings: list[str]
    confidence: float


async def main():
    async with (
        AzureCliCredential() as credential,
        MCPStreamableHTTPTool(
            name="Docs MCP",
            url="https://learn.microsoft.com/api/mcp",
        ) as mcp_tool,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="ResearchAssistant",
            instructions="You are a research assistant with multiple capabilities.",
            tools=[
                get_weather,
                HostedCodeInterpreterTool(),
                HostedWebSearchTool(name="Bing"),
                mcp_tool,
            ],
        )
        
        thread = agent.get_new_thread()
        
        # 非流式
        result = await agent.run(
            "Search for Python best practices and summarize",
            thread=thread,
        )
        print(f"Response: {result.text}")
        
        # 流式
        print("\nStreaming: ", end="")
        async for chunk in agent.run_stream("Continue with examples", thread=thread):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print()
        
        # 结构化输出
        result = await agent.run(
            "Analyze findings",
            thread=thread,
            response_format=AnalysisResult,
        )
        analysis = AnalysisResult.model_validate_json(result.text)
        print(f"\nConfidence: {analysis.confidence}")


if __name__ == "__main__":
    asyncio.run(main())
```

## 约定

- 始终使用异步上下文管理器：`async with provider:`
- 将函数直接传递给 `tools=` 参数（自动转换为 AIFunction）
- 使用 `Annotated[type, Field(description=...)]` 定义函数参数
- 使用 `get_new_thread()` 进行多轮对话
- 服务管理的 MCP 优先使用 `HostedMCPTool`，客户端管理的使用 `MCPStreamableHTTPTool`

## 参考文件

- references/tools.md: 详细的托管工具模式
- references/mcp.md: MCP 集成（托管 + 本地）
- references/threads.md: 线程和对话管理
- references/advanced.md: OpenAPI、引用、结构化输出

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出内容不能替代特定环境的验证、测试或专家评审。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
