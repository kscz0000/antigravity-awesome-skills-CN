---
name: langfuse
description: Langfuse 专家 — 开源 LLM 可观测性平台。涵盖追踪、提示词管理、评估、数据集，以及与 LangChain、LlamaIndex 和 OpenAI 的集成。生产环境中调试、监控和改进 LLM 应用的必备工具。
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Langfuse

Langfuse 专家 — 开源 LLM 可观测性平台。涵盖追踪、提示词管理、评估、数据集，以及与 LangChain、LlamaIndex 和 OpenAI 的集成。生产环境中调试、监控和改进 LLM 应用的必备工具。

**角色**：LLM 可观测性架构师

你是 LLM 可观测性和评估方面的专家。你以追踪、跨度和指标的方式思考。你知道 LLM 应用需要像传统软件一样进行监控——但维度不同（成本、质量、延迟）。你使用数据驱动提示词改进并捕获回归问题。

### 专业知识

- 追踪架构
- 提示词版本管理
- 评估策略
- 成本优化
- 质量监控

## 能力

- LLM 追踪和可观测性
- 提示词管理和版本控制
- 评估和评分
- 数据集管理
- 成本追踪
- 性能监控
- 提示词 A/B 测试

## 前置条件

- 0：LLM 应用基础知识
- 1：API 集成经验
- 2：追踪概念理解
- 所需技能：Python 或 TypeScript/JavaScript，Langfuse 账户（云端或自托管），LLM API 密钥

## 范围

- 0：自托管需要基础设施
- 1：高流量可能需要优化
- 2：实时仪表板存在延迟
- 3：评估需要配置

## 生态系统

### 主要组件

- Langfuse Cloud
- Langfuse Self-hosted
- Python SDK
- JS/TS SDK

### 常见集成

- LangChain
- LlamaIndex
- OpenAI SDK
- Anthropic SDK
- Vercel AI SDK

### 平台

- 任何 Python/JS 后端
- 无服务器函数
- Jupyter notebooks

## 模式

### 基础追踪设置

使用 Langfuse 为 LLM 调用添加埋点

**何时使用**：任何 LLM 应用

from langfuse import Langfuse

# 初始化客户端
langfuse = Langfuse(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com"  # 或自托管 URL
)

# 为用户请求创建追踪
trace = langfuse.trace(
    name="chat-completion",
    user_id="user-123",
    session_id="session-456",  # 分组相关追踪
    metadata={"feature": "customer-support"},
    tags=["production", "v2"]
)

# 记录一次生成（LLM 调用）
generation = trace.generation(
    name="gpt-4o-response",
    model="gpt-4o",
    model_parameters={"temperature": 0.7},
    input={"messages": [{"role": "user", "content": "Hello"}]},
    metadata={"attempt": 1}
)

# 执行实际的 LLM 调用
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

# 用输出完成生成记录
generation.end(
    output=response.choices[0].message.content,
    usage={
        "input": response.usage.prompt_tokens,
        "output": response.usage.completion_tokens
    }
)

# 为追踪评分
trace.score(
    name="user-feedback",
    value=1,  # 1 = 正面, 0 = 负面
    comment="用户点击有帮助"
)

# 退出前刷新（在无服务器环境中很重要）
langfuse.flush()

### OpenAI 集成

使用 OpenAI SDK 自动追踪

**何时使用**：基于 OpenAI 的应用

from langfuse.openai import openai

# OpenAI 客户端的直接替换
# 所有调用自动追踪

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    # Langfuse 特定参数
    name="greeting",  # 追踪名称
    session_id="session-123",
    user_id="user-456",
    tags=["test"],
    metadata={"feature": "chat"}
)

# 支持流式输出
stream = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True,
    name="story-generation"
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")

# 支持异步
import asyncio
from langfuse.openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def main():
    response = await async_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
        name="async-greeting"
    )

### LangChain 集成

追踪 LangChain 应用

**何时使用**：基于 LangChain 的应用

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langfuse.callback import CallbackHandler

# 创建 Langfuse 回调处理器
langfuse_handler = CallbackHandler(
    public_key="pk-...",
    secret_key="sk-...",
    host="https://cloud.langfuse.com",
    session_id="session-123",
    user_id="user-456"
)

# 与任何 LangChain 组件一起使用
llm = ChatOpenAI(model="gpt-4o")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

chain = prompt | llm

# 传递处理器给 invoke
response = chain.invoke(
    {"input": "Hello"},
    config={"callbacks": [langfuse_handler]}
)

# 或设置为默认
import langchain
langchain.callbacks.manager.set_handler(langfuse_handler)

# 之后所有调用都会被追踪
response = chain.invoke({"input": "Hello"})

# 与 agents、retrievers 等一起使用
from langchain.agents import create_openai_tools_agent

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

result = agent_executor.invoke(
    {"input": "What's the weather?"},
    config={"callbacks": [langfuse_handler]}
)

### 提示词管理

版本管理和部署提示词

**何时使用**：跨环境管理提示词

from langfuse import Langfuse

langfuse = Langfuse()

# 从 Langfuse 获取提示词
# （先在 UI 或通过 API 创建）
prompt = langfuse.get_prompt("customer-support-v2")

# 获取编译后的提示词（带变量）
compiled = prompt.compile(
    customer_name="John",
    issue="billing question"
)

# 与 OpenAI 一起使用
response = openai.chat.completions.create(
    model=prompt.config.get("model", "gpt-4o"),
    messages=compiled,
    temperature=prompt.config.get("temperature", 0.7)
)

# 将生成链接到提示词版本
trace = langfuse.trace(name="support-chat")
generation = trace.generation(
    name="response",
    model="gpt-4o",
    prompt=prompt  # 链接到特定版本
)

# 通过 API 创建/更新提示词
langfuse.create_prompt(
    name="customer-support-v3",
    prompt=[
        {"role": "system", "content": "You are a support agent..."},
        {"role": "user", "content": "{{user_message}}"}
    ],
    config={
        "model": "gpt-4o",
        "temperature": 0.7
    },
    labels=["production"]  # 或 ["staging", "development"]
)

# 获取特定标签的提示词
prompt = langfuse.get_prompt(
    "customer-support-v3",
    label="production"  # 获取带有此标签的最新版本
)

### 评估和评分

系统化评估 LLM 输出

**何时使用**：质量保证和改进

from langfuse import Langfuse

langfuse = Langfuse()

# 在代码中手动评分
trace = langfuse.trace(name="qa-flow")

# 获取响应后
trace.score(
    name="relevance",
    value=0.85,  # 0-1 刻度
    comment="响应解决了问题"
)

trace.score(
    name="correctness",
    value=1,  # 二进制: 0 或 1
    data_type="BOOLEAN"
)

# LLM 作为评判者的评估
def evaluate_response(question: str, response: str) -> float:
    eval_prompt = f"""
    Rate the response quality from 0 to 1.

    Question: {question}
    Response: {response}

    Output only a number between 0 and 1.
    """

    result = openai.chat.completions.create(
        model="gpt-4o-mini",  # 使用更便宜的模型进行评估
        messages=[{"role": "user", "content": eval_prompt}]
    )

    return float(result.choices[0].message.content.strip())

# 异步评分
score = evaluate_response(question, response)
trace.score(
    name="quality-llm-judge",
    value=score
)

# 创建评估数据集
dataset = langfuse.create_dataset(name="support-qa-v1")

# 向数据集添加项目
langfuse.create_dataset_item(
    dataset_name="support-qa-v1",
    input={"question": "How do I reset my password?"},
    expected_output="Go to settings > security > reset password"
)

# 在数据集上运行评估
dataset = langfuse.get_dataset("support-qa-v1")

for item in dataset.items:
    # 生成响应
    response = generate_response(item.input["question"])

    # 链接到数据集项目
    trace = langfuse.trace(name="eval-run")
    trace.generation(
        name="response",
        input=item.input,
        output=response
    )

    # 与期望值对比评分
    similarity = calculate_similarity(response, item.expected_output)
    trace.score(name="similarity", value=similarity)

    # 将追踪链接到数据集项目
    item.link(trace, "eval-run-1")

### 装饰器模式

使用装饰器实现简洁的埋点

**何时使用**：基于函数的应用

from langfuse.decorators import observe, langfuse_context

@observe()  # 创建一个追踪
def chat_handler(user_id: str, message: str) -> str:
    # 所有嵌套的 @observe 调用变成跨度
    context = get_context(message)
    response = generate_response(message, context)
    return response

@observe()  # 变成父追踪下的一个跨度
def get_context(message: str) -> str:
    # RAG 检索
    docs = retriever.get_relevant_documents(message)
    return "\n".join([d.page_content for d in docs])

@observe(as_type="generation")  # LLM 生成跨度
def generate_response(message: str, context: str) -> str:
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"Context: {context}"},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

# 添加元数据和评分
@observe()
def main_flow(user_input: str):
    # 更新当前追踪
    langfuse_context.update_current_trace(
        user_id="user-123",
        session_id="session-456",
        tags=["production"]
    )

    result = process(user_input)

    # 为追踪评分
    langfuse_context.score_current_trace(
        name="success",
        value=1 if result else 0
    )

    return result

# 支持异步
@observe()
async def async_handler(message: str):
    result = await async_generate(message)
    return result

## 协作

### 委派触发器

- agent|langgraph|graph -> langgraph（需要构建 agent 来监控）
- crewai|multi-agent|crew -> crewai（需要构建 crew 来监控）
- structured output|extraction -> structured-output（需要构建提取流程来监控）

### 可观测的 LangGraph Agent

技能：langfuse, langgraph

工作流：

```
1. 使用 LangGraph 构建 agent
2. 添加 Langfuse 回调处理器
3. 追踪所有 LLM 调用和工具使用
4. 为输出质量评分
5. 监控并迭代
```

### 监控的 RAG 流水线

技能：langfuse, structured-output

工作流：

```
1. 构建带检索和生成的 RAG
2. 追踪检索和 LLM 调用
3. 评分相关性和准确性
4. 追踪成本和延迟
5. 基于数据优化
```

### 评估的 Agent 系统

技能：langfuse, langgraph, structured-output

工作流：

```
1. 使用结构化输出构建 agent
2. 创建评估数据集
3. 带追踪运行评估
4. 比较提示词版本
5. 部署最佳表现者
```

## 相关技能

配合使用效果良好：`langgraph`, `crewai`, `structured-output`, `autonomous-agents`

## 何时使用
- 用户提到或暗示：langfuse
- 用户提到或暗示：llm observability（LLM 可观测性）
- 用户提到或暗示：llm tracing（LLM 追踪）
- 用户提到或暗示：prompt management（提示词管理）
- 用户提到或暗示：llm evaluation（LLM 评估）
- 用户提到或暗示：monitor llm（监控 LLM）
- 用户提到或暗示：debug llm（调试 LLM）

## 限制
- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出替代为环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
