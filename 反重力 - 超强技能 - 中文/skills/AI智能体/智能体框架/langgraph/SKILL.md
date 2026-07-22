---
name: langgraph
description: LangGraph 专家——构建有状态、多参与者 AI 应用的生产级框架。
  涵盖图构建、状态管理、循环与分支、检查点持久化、人机协作模式以及 ReAct 代理模式。
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# LangGraph

LangGraph 专家——构建有状态、多参与者 AI 应用的生产级框架。涵盖图构建、状态管理、循环与分支、检查点持久化、人机协作模式以及 ReAct 代理模式。已在 LinkedIn、Uber 及 400+ 家公司投入生产使用。这是 LangChain 推荐的代理构建方案。

**角色**：LangGraph 代理架构师

你是使用 LangGraph 构建生产级 AI 代理的专家。你理解代理需要显式结构——图让流程可见且可调试。你精心设计状态，合理使用归约器，并在生产环境中始终考虑持久化。你知道何时需要循环以及如何防止无限循环。

### 专长

- 图拓扑设计
- 状态模式设计
- 条件分支
- 持久化策略
- 人机协作
- 工具集成
- 错误处理与恢复

## 能力

- 图构建（StateGraph）
- 状态管理与归约器
- 节点与边定义
- 条件路由
- 检查点与持久化
- 人机协作模式
- 工具集成
- 流式与异步执行

## 前置条件

- 0：Python 熟练度
- 1：LLM API 基础
- 2：异步编程概念
- 3：图论基础
- 所需技能：Python 3.9+、langgraph 包、LLM API 访问权限（OpenAI、Anthropic 等）、图概念理解

## 范围

- 0：仅限 Python（TypeScript 尚在早期阶段）
- 1：图概念的学习曲线
- 2：状态管理的复杂性
- 3：调试可能具有挑战性

## 生态系统

### 主要

- LangGraph
- LangChain
- LangSmith（可观测性）

### 常见集成

- OpenAI / Anthropic / Google
- Tavily（搜索）
- SQLite / PostgreSQL（持久化）
- Redis（状态存储）

### 平台

- Python 应用
- FastAPI / Flask 后端
- 云部署

## 模式

### 基础代理图

带工具的简单 ReAct 风格代理

**何时使用**：带工具调用的单代理

from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# 1. 定义状态
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    # add_messages 归约器追加而非覆盖

# 2. 定义工具
@tool
def search(query: str) -> str:
    """搜索网络信息。"""
    # 实现代码
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """计算数学表达式。"""
    return str(eval(expression))

tools = [search, calculator]

# 3. 创建带工具的 LLM
llm = ChatOpenAI(model="gpt-4o").bind_tools(tools)

# 4. 定义节点
def agent(state: AgentState) -> dict:
    """代理节点——调用 LLM。"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 工具节点处理工具执行
tool_node = ToolNode(tools)

# 5. 定义路由
def should_continue(state: AgentState) -> str:
    """根据是否调用了工具进行路由。"""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 6. 构建图
graph = StateGraph(AgentState)

# 添加节点
graph.add_node("agent", agent)
graph.add_node("tools", tool_node)

# 添加边
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, ["tools", END])
graph.add_edge("tools", "agent")  # 循环返回

# 编译
app = graph.compile()

# 7. 运行
result = app.invoke({
    "messages": [("user", "What is 25 * 4?")]
})

### 带归约器的状态

使用自定义归约器的复杂状态管理

**何时使用**：多个代理更新共享状态

from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import StateGraph

# 用于合并字典的自定义归约器
def merge_dicts(left: dict, right: dict) -> dict:
    return {**left, **right}

# 带多个归约器的状态
class ResearchState(TypedDict):
    # 消息追加（不覆盖）
    messages: Annotated[list, add_messages]

    # 研究发现合并
    findings: Annotated[dict, merge_dicts]

    # 来源累积
    sources: Annotated[list[str], add]

    # 当前步骤（覆盖——无归约器）
    current_step: str

    # 错误计数（自定义归约器）
    errors: Annotated[int, lambda a, b: a + b]

# 节点返回部分状态更新
def researcher(state: ResearchState) -> dict:
    # 仅返回正在更新的字段
    return {
        "findings": {"topic_a": "New finding"},
        "sources": ["source1.com"],
        "current_step": "researching"
    }

def writer(state: ResearchState) -> dict:
    # 访问累积状态
    all_findings = state["findings"]
    all_sources = state["sources"]

    return {
        "messages": [("assistant", f"Report based on {len(all_sources)} sources")],
        "current_step": "writing"
    }

# 构建图
graph = StateGraph(ResearchState)
graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
# ... 添加边

### 条件分支

基于状态路由到不同路径

**何时使用**：多种可能的工作流

from langgraph.graph import StateGraph, START, END

class RouterState(TypedDict):
    query: str
    query_type: str
    result: str

def classifier(state: RouterState) -> dict:
    """分类查询类型。"""
    query = state["query"].lower()
    if "code" in query or "program" in query:
        return {"query_type": "coding"}
    elif "search" in query or "find" in query:
        return {"query_type": "search"}
    else:
        return {"query_type": "chat"}

def coding_agent(state: RouterState) -> dict:
    return {"result": "Here's your code..."}

def search_agent(state: RouterState) -> dict:
    return {"result": "Search results..."}

def chat_agent(state: RouterState) -> dict:
    return {"result": "Let me help..."}

# 路由函数
def route_query(state: RouterState) -> str:
    """路由到合适的代理。"""
    query_type = state["query_type"]
    return query_type  # 返回节点名称

# 构建图
graph = StateGraph(RouterState)

graph.add_node("classifier", classifier)
graph.add_node("coding", coding_agent)
graph.add_node("search", search_agent)
graph.add_node("chat", chat_agent)

graph.add_edge(START, "classifier")

# 从分类器的条件边
graph.add_conditional_edges(
    "classifier",
    route_query,
    {
        "coding": "coding",
        "search": "search",
        "chat": "chat"
    }
)

# 所有代理通向 END
graph.add_edge("coding", END)
graph.add_edge("search", END)
graph.add_edge("chat", END)

app = graph.compile()

### 检查点持久化

保存和恢复代理状态

**何时使用**：多轮对话、长时间运行的代理

from langgraph.graph import StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver

# SQLite 用于开发
memory = SqliteSaver.from_conn_string(":memory:")
# 或持久化文件
memory = SqliteSaver.from_conn_string("agent_state.db")

# PostgreSQL 用于生产
# memory = PostgresSaver.from_conn_string(DATABASE_URL)

# 带检查点编译
app = graph.compile(checkpointer=memory)

# 使用 thread_id 运行以保持对话连续性
config = {"configurable": {"thread_id": "user-123-session-1"}}

# 第一条消息
result1 = app.invoke(
    {"messages": [("user", "My name is Alice")]},
    config=config
)

# 第二条消息——代理记住上下文
result2 = app.invoke(
    {"messages": [("user", "What's my name?")]},
    config=config
)
# 代理知道名字是 Alice！

# 获取对话历史
state = app.get_state(config)
print(state.values["messages"])

# 列出所有检查点
for checkpoint in app.get_state_history(config):
    print(checkpoint.config, checkpoint.values)

### 人机协作

在执行操作前暂停等待人工审批

**何时使用**：敏感操作、执行前审核

from langgraph.graph import StateGraph, START, END

class ApprovalState(TypedDict):
    messages: Annotated[list, add_messages]
    pending_action: dict | None
    approved: bool

def agent(state: ApprovalState) -> dict:
    # 代理决定操作
    action = {"type": "send_email", "to": "user@example.com"}
    return {
        "pending_action": action,
        "messages": [("assistant", f"I want to: {action}")]
    }

def execute_action(state: ApprovalState) -> dict:
    action = state["pending_action"]
    # 执行已批准的操作
    result = f"Executed: {action['type']}"
    return {
        "messages": [("assistant", result)],
        "pending_action": None
    }

def should_execute(state: ApprovalState) -> str:
    if state.get("approved"):
        return "execute"
    return END  # 等待审批

# 构建图
graph = StateGraph(ApprovalState)
graph.add_node("agent", agent)
graph.add_node("execute", execute_action)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_execute, ["execute", END])
graph.add_edge("execute", END)

# 使用 interrupt_before 编译以实现人工审核
app = graph.compile(
    checkpointer=memory,
    interrupt_before=["execute"]  # 执行前暂停
)

# 运行直到中断
config = {"configurable": {"thread_id": "approval-flow"}}
result = app.invoke({"messages": [("user", "Send report")]}, config)

# 代理暂停——获取待处理状态
state = app.get_state(config)
pending = state.values["pending_action"]
print(f"Pending: {pending}")  # 人工审核

# 人工批准——更新状态并继续
app.update_state(config, {"approved": True})
result = app.invoke(None, config)  # 恢复执行

### 并行执行（Map-Reduce）

并行运行多个分支

**何时使用**：并行研究、批量处理

from langgraph.graph import StateGraph, START, END, Send
from langgraph.constants import Send

class ParallelState(TypedDict):
    topics: list[str]
    results: Annotated[list[str], add]
    summary: str

def research_topic(state: dict) -> dict:
    """研究单个主题。"""
    topic = state["topic"]
    result = f"Research on {topic}..."
    return {"results": [result]}

def summarize(state: ParallelState) -> dict:
    """汇总所有研究结果。"""
    all_results = state["results"]
    summary = f"Summary of {len(all_results)} topics"
    return {"summary": summary}

def fanout_topics(state: ParallelState) -> list[Send]:
    """为每个主题创建并行任务。"""
    return [
        Send("research", {"topic": topic})
        for topic in state["topics"]
    ]

# 构建图
graph = StateGraph(ParallelState)
graph.add_node("research", research_topic)
graph.add_node("summarize", summarize)

# 扇出到并行研究
graph.add_conditional_edges(START, fanout_topics, ["research"])
# 所有研究节点通向汇总
graph.add_edge("research", "summarize")
graph.add_edge("summarize", END)

app = graph.compile()

result = app.invoke({
    "topics": ["AI", "Climate", "Space"],
    "results": []
})
# 研究并行运行，然后汇总

## 协作

### 委派触发

- crewai|role-based|crew -> crewai（需要基于角色的多代理方案）
- observability|tracing|langsmith -> langfuse（需要 LLM 可观测性）
- structured output|json schema -> structured-output（需要结构化 LLM 响应）
- evaluate|benchmark|test agent -> agent-evaluation（需要评估代理性能）

### 生产代理技术栈

技能：langgraph、langfuse、structured-output

工作流：

```
1. 使用 LangGraph 设计代理图
2. 为工具响应添加结构化输出
3. 集成 Langfuse 实现可观测性
4. 在生产环境中测试和监控
```

### 多代理系统

技能：langgraph、crewai、agent-communication

工作流：

```
1. 设计代理角色（CrewAI 模式）
2. 使用子图实现为 LangGraph
3. 添加代理间通信
4. 使用监督者模式编排
```

### 已评估代理

技能：langgraph、agent-evaluation、langfuse

工作流：

```
1. 使用 LangGraph 构建代理
2. 创建评估套件
3. 使用 Langfuse 监控
4. 基于指标迭代
```

## 相关技能

配合使用：`crewai`、`autonomous-agents`、`langfuse`、`structured-output`

## 何时使用
- 用户提及或暗示：langgraph
- 用户提及或暗示：langchain agent
- 用户提及或暗示：stateful agent
- 用户提及或暗示：agent graph
- 用户提及或暗示：react agent
- 用户提及或暗示：agent workflow
- 用户提及或暗示：multi-step agent

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
