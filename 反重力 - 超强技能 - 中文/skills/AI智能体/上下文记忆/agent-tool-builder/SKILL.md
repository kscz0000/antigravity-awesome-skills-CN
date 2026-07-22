---
name: agent-tool-builder
description: 工具是 AI 智能体与世界交互的方式。设计良好的工具决定了智能体是正常工作还是产生幻觉、静默失败、或消耗 10 倍不必要的 token。本技能涵盖从 schema 到错误处理的工具设计。触发词：agent tool、function calling、工具 schema、工具设计、MCP server、MCP tool、tool use、构建智能体工具、定义函数、input_schema、tool_use、tool_result、智能体工具、函数调用、工具模式、MCP服务器、工具调用
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Agent Tool Builder

工具是 AI 智能体与世界交互的方式。设计良好的工具决定了智能体是正常工作还是产生幻觉、静默失败、或消耗 10 倍不必要的 token。

本技能涵盖从 schema 到错误处理的工具设计。包括 JSON Schema 最佳实践、真正能帮助 LLM 的描述编写、验证，以及正在成为 AI 工具通用语言的 MCP 标准。

核心洞察：工具描述比工具实现更重要。LLM 永远看不到你的代码——它只能看到 schema 和描述。

## 原则

- 描述质量 > 实现质量（对 LLM 准确性而言）
- 工具数量控制在 20 个以内——更多会导致混乱
- 每个工具都需要显式的错误处理——静默失败会毒害智能体
- 返回字符串，而非对象——LLM 处理的是文本
- 执行前设置验证关卡——拒绝、修复或升级，绝不静默失败
- 用 LLM 测试工具，而不只是单元测试

## 能力

- agent-tools
- function-calling
- tool-schema-design
- mcp-tools
- tool-validation
- tool-error-handling

## 范围

- multi-agent-coordination → multi-agent-orchestration
- agent-memory → agent-memory-systems
- api-design → api-designer
- llm-prompting → prompt-engineering

## 工具

### 标准

- JSON Schema - 何时使用：所有工具定义 注意：工具 schema 的通用格式
- MCP (Model Context Protocol) - 何时使用：构建可复用的跨平台工具 注意：Anthropic 的开放标准，已被广泛采用

### 框架

- Anthropic SDK - 何时使用：基于 Claude 的智能体 注意：Beta tool runner 处理了大部分复杂性
- OpenAI Functions - 何时使用：基于 OpenAI 的智能体 注意：使用 strict mode 保证 schema 合规
- Vercel AI SDK - 何时使用：多提供商工具处理 注意：抽象了提供商之间的差异
- LangChain Tools - 何时使用：基于 LangChain 的智能体 注意：将 MCP 工具转换为 LangChain 格式

## 模式

### 工具 Schema 设计

为工具创建清晰、无歧义的 JSON Schema

**何时使用**：为智能体定义任何新工具

# TOOL SCHEMA BEST PRACTICES:

## 1. 详细描述（最重要）
"""
BAD - 太模糊：
{
  "name": "get_stock_price",
  "description": "Gets stock price",
  "input_schema": {
    "type": "object",
    "properties": {
      "ticker": {"type": "string"}
    }
  }
}

GOOD - 全面：
{
  "name": "get_stock_price",
  "description": "Retrieves the current stock price for a given ticker
    symbol. The ticker symbol must be a valid symbol for a publicly
    traded company on a major US stock exchange like NYSE or NASDAQ.
    Returns the latest trade price in USD. Use when the user asks
    about current or recent stock prices. Does NOT provide historical
    data, company info, or predictions.",
  "input_schema": {
    "type": "object",
    "properties": {
      "ticker": {
        "type": "string",
        "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."
      }
    },
    "required": ["ticker"]
  }
}
"""

## 2. 参数描述
"""
每个参数需要：
- 是什么
- 期望格式
- 示例值
- 边缘情况/限制

{
  "location": {
    "type": "string",
    "description": "City and state/country. Format: 'City, State' for US
      (e.g., 'San Francisco, CA') or 'City, Country' for international
      (e.g., 'Tokyo, Japan'). Do not use ZIP codes or coordinates."
  },
  "unit": {
    "type": "string",
    "enum": ["celsius", "fahrenheit"],
    "description": "Temperature unit. Defaults to user's locale if not
      specified. Use 'fahrenheit' for US users, 'celsius' for others."
  }
}
"""

## 3. 尽可能使用枚举
"""
枚举将 LLM 约束到有效值：

"priority": {
  "type": "string",
  "enum": ["low", "medium", "high", "critical"],
  "description": "Task priority level"
}

"action": {
  "type": "string",
  "enum": ["create", "read", "update", "delete"],
  "description": "The CRUD operation to perform"
}
"""

## 4. 必填 vs 可选
"""
明确哪些是必填的：

{
  "type": "object",
  "properties": {
    "query": {...},      // 必填
    "limit": {...},      // 可选，有默认值
    "offset": {...}      // 可选
  },
  "required": ["query"],
  "additionalProperties": false  // 严格模式
}
"""

### 带输入示例的工具

使用示例引导 LLM 工具使用

**何时使用**：具有嵌套对象或格式敏感输入的复杂工具

# TOOL USE EXAMPLES (Anthropic Beta Feature):

"""
示例向 Claude 展示了 schema 无法表达的具体模式。
在复杂操作上将准确率从 72% 提升到 90%。
"""

{
  "name": "create_calendar_event",
  "description": "Creates a calendar event with optional attendees and reminders",
  "input_schema": {
    "type": "object",
    "properties": {
      "title": {"type": "string", "description": "Event title"},
      "start_time": {
        "type": "string",
        "description": "ISO 8601 datetime, e.g. 2024-03-15T14:00:00Z"
      },
      "duration_minutes": {"type": "integer", "description": "Event duration"},
      "attendees": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Email addresses of attendees"
      }
    },
    "required": ["title", "start_time", "duration_minutes"]
  },
  "input_examples": [
    {
      "title": "Team Standup",
      "start_time": "2024-03-15T09:00:00Z",
      "duration_minutes": 30,
      "attendees": ["alice@company.com", "bob@company.com"]
    },
    {
      "title": "Quick Chat",
      "start_time": "2024-03-15T14:00:00Z",
      "duration_minutes": 15
    },
    {
      "title": "Project Review",
      "start_time": "2024-03-15T16:00:00-05:00",
      "duration_minutes": 60,
      "attendees": ["team@company.com"]
    }
  ]
}

# EXAMPLE DESIGN PRINCIPLES:
# - 使用真实数据，而非占位符
# - 展示最小、部分和完整规范模式
# - 保持简洁：每个工具 1-5 个示例
# - 聚焦于歧义情况

### 工具错误处理

返回能帮助 LLM 恢复的错误

**何时使用**：任何可能失败的工具

# ERROR HANDLING BEST PRACTICES:

## 返回有信息量的错误
"""
BAD:
{"error": "Failed"}
{"error": true}

GOOD:
{
  "error": true,
  "error_type": "not_found",
  "message": "Location 'Atlantis' not found in weather database.
    Please provide a real city name like 'San Francisco, CA'.",
  "suggestions": ["San Francisco, CA", "Los Angeles, CA"]
}
"""

## Anthropic Tool Result with Error
"""
{
  "type": "tool_result",
  "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
  "content": "Error: Location 'Atlantis' not found in weather database.
    Please provide a real city name like 'San Francisco, CA'.",
  "is_error": true
}
"""

## 需要处理的错误类别
"""
1. 输入验证错误
   - 缺少必填参数
   - 格式无效
   - 值超出范围

2. 外部服务错误
   - API 不可用
   - 速率限制
   - 超时

3. 业务逻辑错误
   - 资源未找到
   - 权限拒绝
   - 冲突/重复

4. 内部错误
   - 意外异常
   - 数据损坏
"""

## 实现模式
"""
from dataclasses import dataclass
from typing import Union

@dataclass
class ToolResult:
    success: bool
    content: str
    error_type: str = None
    suggestions: list[str] = None

    def to_response(self) -> dict:
        if self.success:
            return {"content": self.content}
        return {
            "content": f"Error ({self.error_type}): {self.content}",
            "is_error": True
        }

def get_weather(location: str) -> ToolResult:
    # Validate input
    if not location or len(location) < 2:
        return ToolResult(
            success=False,
            content="Location must be at least 2 characters",
            error_type="validation_error"
        )

    try:
        data = weather_api.fetch(location)
        return ToolResult(
            success=True,
            content=f"Temperature: {data.temp}°F, Conditions: {data.conditions}"
        )
    except LocationNotFound:
        return ToolResult(
            success=False,
            content=f"Location '{location}' not found",
            error_type="not_found",
            suggestions=weather_api.suggest_locations(location)
        )
    except RateLimitError:
        return ToolResult(
            success=False,
            content="Weather service rate limit exceeded. Try again in 60 seconds.",
            error_type="rate_limit"
        )
    except Exception as e:
        return ToolResult(
            success=False,
            content=f"Unexpected error: {str(e)}",
            error_type="internal_error"
        )
"""

### MCP 工具模式

使用 Model Context Protocol 构建工具

**何时使用**：创建可复用的跨平台工具

# MCP TOOL IMPLEMENTATION:

"""
MCP (Model Context Protocol) 是 Anthropic 的开放标准，
用于将 AI 智能体连接到外部系统。一次构建，随处使用。
"""

## Basic MCP Server (TypeScript)
"""
import { Server } from "@modelcontextprotocol/sdk/server";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio";

const server = new Server({
  name: "weather-server",
  version: "1.0.0"
});

// Define tools
server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "get_weather",
      description: "Get current weather for a location. Returns
        temperature, conditions, and humidity. Use for weather
        queries about specific cities.",
      inputSchema: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "City and state, e.g. 'San Francisco, CA'"
          },
          unit: {
            type: "string",
            enum: ["celsius", "fahrenheit"],
            default: "fahrenheit"
          }
        },
        required: ["location"]
      }
    }
  ]
}));

// Handle tool calls
server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "get_weather") {
    try {
      const weather = await fetchWeather(args.location, args.unit);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(weather)
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error.message}`
          }
        ],
        isError: true
      };
    }
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
"""

## MCP 优势
"""
- 跨 LLM 提供商的通用兼容性
- 可复用的工具库
- 流式传输和 SSE 传输支持
- 内置可观测性
- 工具访问控制
"""

### Tool Runner 模式

使用 SDK tool runner 进行自动处理

**何时使用**：构建工具循环而无需手动管理

# TOOL RUNNER (Anthropic SDK Beta):

"""
Tool runner 自动处理工具调用循环：
- 当 Claude 调用工具时执行它们
- 管理对话状态
- 处理错误重试
- 提供流式支持
"""

## Python 示例
"""
import anthropic
from anthropic import beta_tool

client = anthropic.Anthropic()

@beta_tool
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    '''Get the current weather in a given location.

    Args:
        location: The city and state, e.g. San Francisco, CA
        unit: Temperature unit, either 'celsius' or 'fahrenheit'
    '''
    # Implementation
    return json.dumps({"temperature": "72°F", "conditions": "Sunny"})

@beta_tool
def search_web(query: str) -> str:
    '''Search the web for information.

    Args:
        query: The search query
    '''
    # Implementation
    return json.dumps({"results": [...]})

# Tool runner handles the loop
runner = client.beta.messages.tool_runner(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=[get_weather, search_web],
    messages=[
        {"role": "user", "content": "What's the weather in Paris?"}
    ]
)

# Process each message
for message in runner:
    print(message.content[0].text)

# Or just get final result
final = runner.until_done()
"""

## TypeScript with Zod
"""
import { Anthropic } from '@anthropic-ai/sdk';
import { betaZodTool } from '@anthropic-ai/sdk/helpers/beta/zod';
import { z } from 'zod';

const anthropic = new Anthropic();

const getWeatherTool = betaZodTool({
  name: 'get_weather',
  description: 'Get the current weather in a given location',
  inputSchema: z.object({
    location: z.string().describe('City and state, e.g. San Francisco, CA'),
    unit: z.enum(['celsius', 'fahrenheit']).default('fahrenheit')
  }),
  run: async (input) => {
    // Type-safe input!
    return JSON.stringify({temperature: '72°F'});
  }
});

const runner = anthropic.beta.messages.toolRunner({
  model: 'claude-sonnet-4-5',
  max_tokens: 1024,
  tools: [getWeatherTool],
  messages: [{ role: 'user', content: "What's the weather in Paris?" }]
});

for await (const message of runner) {
  console.log(message.content[0].text);
}
"""

### 并行工具执行

同时运行多个工具

**何时使用**：可以并行运行的独立工具调用

# PARALLEL TOOL EXECUTION:

"""
默认情况下，Claude 可以在一个响应中调用多个工具。
这显著减少了独立操作的延迟。
"""

## 处理并行结果
"""
# Claude returns multiple tool_use blocks:
response.content = [
    {"type": "text", "text": "I'll check both locations..."},
    {"type": "tool_use", "id": "toolu_01", "name": "get_weather",
     "input": {"location": "San Francisco, CA"}},
    {"type": "tool_use", "id": "toolu_02", "name": "get_weather",
     "input": {"location": "New York, NY"}},
    {"type": "tool_use", "id": "toolu_03", "name": "get_time",
     "input": {"timezone": "America/Los_Angeles"}},
    {"type": "tool_use", "id": "toolu_04", "name": "get_time",
     "input": {"timezone": "America/New_York"}}
]

# Execute in parallel
import asyncio

async def execute_tools_parallel(tool_uses):
    tasks = [execute_tool(t) for t in tool_uses]
    return await asyncio.gather(*tasks)

results = await execute_tools_parallel(tool_uses)

# Return ALL results in SINGLE user message (critical!)
tool_results = [
    {"type": "tool_result", "tool_use_id": "toolu_01", "content": "72°F, Sunny"},
    {"type": "tool_result", "tool_use_id": "toolu_02", "content": "45°F, Cloudy"},
    {"type": "tool_result", "tool_use_id": "toolu_03", "content": "2:30 PM PST"},
    {"type": "tool_result", "tool_use_id": "toolu_04", "content": "5:30 PM EST"}
]

# CORRECT: All results in one message
messages.append({"role": "user", "content": tool_results})

# WRONG: Separate messages (breaks parallel execution pattern)
# messages.append({"role": "user", "content": [tool_results[0]]})
# messages.append({"role": "user", "content": [tool_results[1]]})
"""

## 鼓励并行工具使用
"""
添加到系统提示词：
"For maximum efficiency, whenever you need to perform multiple
independent operations, invoke all relevant tools simultaneously
rather than sequentially."
"""

## 禁用并行（需要时）
"""
response = client.messages.create(
    model="claude-sonnet-4-5",
    tools=tools,
    tool_choice={"type": "auto", "disable_parallel_tool_use": True},
    messages=messages
)
"""

## 验证检查

### 工具描述必须全面

严重程度：WARNING

工具描述应至少 100 个字符

消息：工具描述太短。添加关于何时使用、参数和返回值的详细信息。

### 参数描述必填

严重程度：WARNING

每个参数都应有描述

消息：参数缺少描述。描述它是什么以及期望的格式。

### Schema 应指定必填字段

严重程度：INFO

明确定义哪些字段是必填的

消息：Schema 未指定必填字段。添加 'required' 数组。

### 工具实现需要错误处理

严重程度：ERROR

工具函数应处理异常

消息：工具函数没有 try/except 块。添加错误处理。

### 错误结果需要 is_error 标志

严重程度：WARNING

返回错误时，设置 is_error 为 true

消息：错误结果没有 is_error 标志。添加 'is_error': true。

### 工具应返回字符串

严重程度：WARNING

返回 JSON 字符串，而非 dict/object

消息：返回 dict 而非 string。使用 json.dumps() 或 JSON.stringify()。

### 工具应验证输入

严重程度：WARNING

执行前验证 LLM 提供的输入

消息：工具函数没有可见的输入验证。执行前进行验证。

### SQL 查询必须使用参数化

严重程度：ERROR

永远不要将用户输入拼接到 SQL 中

消息：SQL 查询似乎使用了字符串拼接。使用参数化查询。

### 外部调用需要超时设置

严重程度：WARNING

HTTP 请求和外部调用应有超时设置

消息：外部 API 调用没有超时设置。添加 timeout 参数。

### MCP 工具必须有 Input Schema

严重程度：ERROR

所有 MCP 工具都需要 inputSchema

消息：MCP 工具定义缺少 inputSchema。

## 协作

### 委托触发

- user needs to coordinate multiple tools -> multi-agent-orchestration (跨智能体的工具编排)
- user needs persistent memory between tool calls -> agent-memory-systems (工具的状态管理)
- user building voice agent tools -> voice-agents (音频/语音特定的工具需求)
- user needs computer control tools -> computer-use-agents (桌面自动化工具)
- user wants to test their tools -> agent-evaluation (工具测试和评估)

## 相关技能

与以下技能配合良好：`multi-agent-orchestration`、`api-designer`、`llm-architect`、`backend`

## 何时使用

- 用户提及或暗示：agent tool
- 用户提及或暗示：function calling
- 用户提及或暗示：tool schema
- 用户提及或暗示：tool design
- 用户提及或暗示：mcp server
- 用户提及或暗示：mcp tool
- 用户提及或暗示：tool use
- 用户提及或暗示：build tool for agent
- 用户提及或暗示：define function
- 用户提及或暗示：input_schema
- 用户提及或暗示：tool_use
- 用户提及或暗示：tool_result

## 限制

- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
