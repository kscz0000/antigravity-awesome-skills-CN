---
name: pydantic-ai
description: "使用 PydanticAI 构建生产级 AI 智能体——类型安全的工具调用、结构化输出、依赖注入与多模型支持。触发词：PydanticAI、Python AI 智能体、结构化输出、依赖注入、工具调用、LLM 应用、AI 智能体开发、Agent、@agent.tool、RunContext、ModelRetry、result_type"
category: ai-agents
risk: safe
source: community
date_added: "2026-03-18"
author: suhaibjanjua
tags: [pydantic-ai, ai-agents, llm, openai, anthropic, gemini, tool-use, structured-output, python]
tools: [claude, cursor, gemini]
---

# PydanticAI — Python 中的类型化 AI 智能体

## 概述

PydanticAI 是 Pydantic 团队推出的 Python 智能体框架，将 Pydantic 同样的类型安全和验证保障引入 LLM 应用。它支持结构化输出（通过 Pydantic 模型验证）、依赖注入以提升可测试性、流式响应、多轮对话和工具调用——兼容 OpenAI、Anthropic、Google Gemini、Groq、Mistral 和 Ollama。当你构建的生产级 AI 智能体、聊天机器人或 LLM 管道对正确性和可测试性有要求时，使用此技能。

## 使用场景

- 构建需要调用工具并返回结构化数据的 Python AI 智能体时使用
- 需要经过验证的类型化 LLM 输出（而非原始字符串）时使用
- 希望在不调用真实 LLM 的情况下为智能体逻辑编写单元测试时使用
- 需要在不同 LLM 提供商之间切换而不重写智能体代码时使用
- 用户询问 `Agent`、`@agent.tool`、`RunContext`、`ModelRetry` 或 `result_type` 时使用

## 工作原理

### 步骤 1：安装

```bash
pip install pydantic-ai

# 安装特定提供商的额外依赖
pip install 'pydantic-ai[openai]'       # OpenAI / Azure OpenAI
pip install 'pydantic-ai[anthropic]'    # Anthropic Claude
pip install 'pydantic-ai[gemini]'       # Google Gemini
pip install 'pydantic-ai[groq]'         # Groq
pip install 'pydantic-ai[vertexai]'     # Google Vertex AI
```

### 步骤 2：最小化智能体

```python
from pydantic_ai import Agent

# Simple agent — returns a plain string
agent = Agent(
    'anthropic:claude-sonnet-4-6',
    system_prompt='You are a helpful assistant. Be concise.',
)

result = agent.run_sync('What is the capital of Japan?')
print(result.data)  # "Tokyo"
print(result.usage())  # Usage(requests=1, request_tokens=..., response_tokens=...)
```

### 步骤 3：使用 Pydantic 模型实现结构化输出

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class MovieReview(BaseModel):
    title: str
    year: int
    rating: float  # 0.0 to 10.0
    summary: str
    recommended: bool

agent = Agent(
    'openai:gpt-4o',
    result_type=MovieReview,
    system_prompt='You are a film critic. Return structured reviews.',
)

result = agent.run_sync('Review Inception (2010)')
review = result.data  # Fully typed MovieReview instance
print(f"{review.title} ({review.year}): {review.rating}/10")
print(f"Recommended: {review.recommended}")
```

### 步骤 4：工具调用

使用 `@agent.tool` 注册工具——LLM 在运行过程中可以调用它们：

```python
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
import httpx

class WeatherReport(BaseModel):
    city: str
    temperature_c: float
    condition: str

weather_agent = Agent(
    'anthropic:claude-sonnet-4-6',
    result_type=WeatherReport,
    system_prompt='Get current weather for the requested city.',
)

@weather_agent.tool
async def get_temperature(ctx: RunContext, city: str) -> dict:
    """Fetch the current temperature for a city from the weather API."""
    async with httpx.AsyncClient() as client:
        r = await client.get(f'https://wttr.in/{city}?format=j1')
        data = r.json()
        return {
            'temp_c': float(data['current_condition'][0]['temp_C']),
            'description': data['current_condition'][0]['weatherDesc'][0]['value'],
        }

import asyncio
result = asyncio.run(weather_agent.run('What is the weather in Tokyo?'))
print(result.data)
```

### 步骤 5：依赖注入

向智能体注入服务（数据库、HTTP 客户端、配置），提升可测试性：

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel

@dataclass
class Deps:
    db: Database
    user_id: str

class SupportResponse(BaseModel):
    message: str
    escalate: bool

support_agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=Deps,
    result_type=SupportResponse,
    system_prompt='You are a support agent. Use the tools to help customers.',
)

@support_agent.tool
async def get_order_history(ctx: RunContext[Deps]) -> list[dict]:
    """Fetch recent orders for the current user."""
    return await ctx.deps.db.get_orders(ctx.deps.user_id, limit=5)

@support_agent.tool
async def create_refund(ctx: RunContext[Deps], order_id: str, reason: str) -> dict:
    """Initiate a refund for a specific order."""
    return await ctx.deps.db.create_refund(order_id, reason, ctx.deps.user_id)

# Usage
async def handle_support(user_id: str, message: str):
    deps = Deps(db=get_db(), user_id=user_id)
    result = await support_agent.run(message, deps=deps)
    return result.data
```

### 步骤 6：使用 TestModel 测试

无需调用真实 LLM 即可编写单元测试：

```python
from pydantic_ai.models.test import TestModel

def test_support_agent_escalates():
    with support_agent.override(model=TestModel()):
        # TestModel returns a minimal valid response matching result_type
        result = support_agent.run_sync(
            'I want to cancel my account',
            deps=Deps(db=FakeDb(), user_id='user-123'),
        )
    # Test the structure, not the LLM's exact words
    assert isinstance(result.data, SupportResponse)
    assert isinstance(result.data.escalate, bool)
```

**FunctionModel** 用于确定性测试响应：

```python
from pydantic_ai.models.function import FunctionModel, ModelContext

def my_model(messages, info):
    return ModelResponse(parts=[TextPart('Always this response')])

with agent.override(model=FunctionModel(my_model)):
    result = agent.run_sync('anything')
```

### 步骤 7：流式响应

```python
import asyncio
from pydantic_ai import Agent

agent = Agent('anthropic:claude-sonnet-4-6')

async def stream_response():
    async with agent.run_stream('Write a haiku about Python') as result:
        async for chunk in result.stream_text():
            print(chunk, end='', flush=True)
    print()  # newline
    print(f"Total tokens: {result.usage()}")

asyncio.run(stream_response())
```

### 步骤 8：多轮对话

```python
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessagesTypeAdapter

agent = Agent('openai:gpt-4o', system_prompt='You are a helpful assistant.')

# First turn
result1 = agent.run_sync('My name is Alice.')
history = result1.all_messages()

# Second turn — passes conversation history
result2 = agent.run_sync('What is my name?', message_history=history)
print(result2.data)  # "Your name is Alice."
```

## 示例

### 示例 1：代码审查智能体

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from typing import Literal

class CodeReview(BaseModel):
    quality: Literal['excellent', 'good', 'needs_work', 'poor']
    issues: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    approved: bool

code_review_agent = Agent(
    'anthropic:claude-sonnet-4-6',
    result_type=CodeReview,
    system_prompt="""
    You are a senior engineer performing code review.
    Evaluate code quality, identify issues, and provide actionable suggestions.
    Set approved=True only for good or excellent quality code with no security issues.
    """,
)

def review_code(diff: str) -> CodeReview:
    result = code_review_agent.run_sync(f"Review this code:\n\n{diff}")
    return result.data
```

### 示例 2：带重试逻辑的智能体

```python
from pydantic_ai import Agent, ModelRetry
from pydantic import BaseModel, field_validator

class StrictJson(BaseModel):
    value: int

    @field_validator('value')
    def must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('value must be positive')
        return v

agent = Agent('openai:gpt-4o-mini', result_type=StrictJson)

@agent.result_validator
async def validate_result(ctx, result: StrictJson) -> StrictJson:
    if result.value > 1000:
        raise ModelRetry('Value must be under 1000. Try again with a smaller number.')
    return result
```

### 示例 3：多智能体管道

```python
from pydantic_ai import Agent
from pydantic import BaseModel

class ResearchSummary(BaseModel):
    key_points: list[str]
    conclusion: str

class BlogPost(BaseModel):
    title: str
    body: str
    meta_description: str

researcher = Agent('openai:gpt-4o', result_type=ResearchSummary)
writer = Agent('anthropic:claude-sonnet-4-6', result_type=BlogPost)

async def research_and_write(topic: str) -> BlogPost:
    # Stage 1: research
    research = await researcher.run(f'Research the topic: {topic}')

    # Stage 2: write based on research
    post = await writer.run(
        f'Write a blog post about: {topic}\n\nResearch:\n' +
        '\n'.join(f'- {p}' for p in research.data.key_points) +
        f'\n\nConclusion: {research.data.conclusion}'
    )
    return post.data
```

## 最佳实践

- ✅ 始终用 Pydantic 模型定义 `result_type`——生产环境中避免返回原始字符串
- ✅ 用 dataclass 配合 `deps_type` 实现依赖注入——让智能体可测试
- ✅ 在单元测试中使用 `TestModel`——CI 中不要调用真实 LLM
- ✅ 添加 `@agent.result_validator` 实现超出 Pydantic 验证范围的业务逻辑检查
- ✅ 在面向用户的应用中对长输出使用 `run_stream`，逐步展示结果
- ❌ 不要在 `Agent()` 参数中放置密钥（API key）——使用环境变量
- ❌ 如果依赖不同，不要在异步任务间共享同一个 `Agent` 实例——为每次请求创建实例或在 `agent.run()` 中传入每次调用的 `deps`
- ❌ 不要宽泛地捕获 `ValidationError`——让 PydanticAI 通过 `ModelRetry` 重试可恢复的 LLM 输出错误

## 安全与防护

- 通过环境变量设置 API key（`OPENAI_API_KEY`、`ANTHROPIC_API_KEY` 等）——永远不要硬编码。
- 在传递给外部系统之前验证所有工具输入——使用 Pydantic 模型或手动检查。
- 会修改数据的工具（写数据库、发邮件、调用支付 API）在生产环境中应要求用户显式确认后才能调用。
- 当智能体执行重要操作时，记录 `result.all_messages()` 用于审计追踪。
- 在 `Agent()` 上设置 `retries=` 限制，防止持续验证失败时出现失控循环。

## 常见陷阱

- **问题：** 每次 LLM 响应都报 `ValidationError`——结构化输出始终无法验证
  **解决方案：** 简化 `result_type` 字段。在合适的地方使用 `Optional` 和 `default`。模型可能难以应对过于严格的 schema。

- **问题：** 工具从未被 LLM 调用
  **解决方案：** 为工具函数编写清晰、具体的 docstring——PydanticAI 会将 docstring 作为工具描述发送给 LLM。

- **问题：** 工具内部 `RunContext` 依赖为 `None`
  **解决方案：** 调用 `agent.run()` 或 `agent.run_sync()` 时传入 `deps=`。依赖不是全局设置的。

- **问题：** 在 FastAPI 内调用 `agent.run()` 时出现 `asyncio.run()` 错误
  **解决方案：** 在异步 FastAPI 路由处理器中直接使用 `await agent.run()`——不要用 `asyncio.run()` 包裹。

## 相关技能

- `@langchain-architecture` — 替代性 Python AI 框架（更灵活，类型安全性较低）
- `@llm-application-dev-ai-assistant` — 通用 LLM 应用开发模式
- `@fastapi-templates` — 通过 FastAPI 端点提供 PydanticAI 智能体服务
- `@agent-orchestration-multi-agent-optimize` — 编排多个 PydanticAI 智能体

## 限制

- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清。