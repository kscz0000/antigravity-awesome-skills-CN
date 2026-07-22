---
name: multi-agent-architect
description: "使用 LangGraph、LangChain 和 DeepAgents 设计和优化生产级多智能体系统，用于复杂 AI 工作流。适用于多智能体系统、智能体编排、LangGraph、LangChain、DeepAgents、RAG、工具调用等场景。"
risk: safe
source: community
metadata:
  category: ai-engineering
  source_repo: pravin-python/antigravity-awesome-skills
  source_type: community
  date_added: "2025-05-07"
  author: community
  tags: [langgraph, langchain, multi-agent, orchestration, deepagents, rag, tool-calling]
  tools: [claude, cursor, gemini]
  license: "MIT"
  license_source: "https://github.com/pravin-python/antigravity-awesome-skills/blob/main/LICENSE"
---


# 多智能体架构师与更新技能

## 概述

本技能将 Claude 转化为专注于 LangGraph、LangChain 和 DeepAgents 的资深 AI 多智能体架构师。它提供结构化工作流，用于创建和更新生产级多智能体系统——包括监督智能体、规划智能体、研究智能体、编码智能体以及支持记忆的自主流水线。当需要设计、构建、调试或扩展任何多智能体 AI 系统时使用。

若本技能改编自外部 GitHub 仓库，需声明：

- `source_repo: owner/repo`
- `source_type: official` 或 `source_type: community`

## 何时使用本技能

- 需要从零创建新智能体或多智能体工作流时使用
- 处理 LangGraph 状态图、节点、边或条件路由时使用
- 用户询问智能体通信、记忆系统或工具调用流水线时使用
- 调试或优化现有 LangChain/LangGraph 智能体系统时使用
- 架构监督、规划、研究、编码或验证智能体角色时使用
- 将 DeepAgents 与分层规划和委托集成时使用

## 工作原理

### 第一步：理解目标

编写代码前先澄清：
- 该智能体系统必须达成什么**业务目标**？
- 需要哪些**智能体角色**（监督者、规划者、研究者、编码者、验证者）？
- 每个智能体需要什么**工具**？
- 需要什么**记忆**策略（Redis、向量数据库、LangChain Memory）？
- 连接智能体的**通信协议**是什么（共享状态、消息传递）？

### 第二步：定义状态 Schema

所有智能体共享一个在图中传递的类型化状态对象：

```python
from typing import TypedDict

class AgentState(TypedDict):
    user_goal: str
    tasks: list[str]
    completed_tasks: list[str]
    next_agent: str
    context: dict
    step_count: int          # guards against infinite loops
    error: str | None
```

### 第三步：定义智能体节点

每个智能体是一个**异步函数**，从状态读取并返回更新后的状态：

```python
import logging
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

async def research_node(state: AgentState) -> AgentState:
    logger.info("research_node: starting")
    llm = ChatOpenAI(model="gpt-4o")
    result = await llm.bind_tools(research_tools).ainvoke(state["user_goal"])
    state["context"]["research"] = result.content
    state["next_agent"] = "coder"
    return state
```

### 第四步：构建 LangGraph

用边和条件路由将节点连接：

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("research",   research_node)
    graph.add_node("coder",      coding_node)
    graph.add_node("validator",  validation_node)
    graph.add_node("tools",      ToolNode(all_tools))

    graph.set_entry_point("supervisor")

    graph.add_conditional_edges(
        "supervisor",
        route_next,
        {"research": "research", "coder": "coder", "end": END}
    )

    graph.add_edge("research",  "supervisor")
    graph.add_edge("coder",     "validator")
    graph.add_edge("validator", "supervisor")

    return graph.compile()

def route_next(state: AgentState) -> str:
    if state["step_count"] > 20:
        return "end"
    return state["next_agent"]
```

### 第五步：添加记忆

```python
from langchain_community.chat_message_histories import RedisChatMessageHistory

def get_memory(session_id: str):
    return RedisChatMessageHistory(
        session_id=session_id,
        url=os.getenv("REDIS_URL"),
        ttl=3600
    )
```

### 第六步：运行图

```python
async def run(user_goal: str, session_id: str):
    graph = build_graph()
    initial_state = AgentState(
        user_goal=user_goal,
        tasks=[],
        completed_tasks=[],
        next_agent="supervisor",
        context={},
        step_count=0,
        error=None,
    )
    return await graph.ainvoke(initial_state)
```

### 第七步：通过 FastAPI 暴露（可选）

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RunRequest(BaseModel):
    goal: str
    session_id: str

@app.post("/run")
async def run_agent(req: RunRequest):
    result = await run(req.goal, req.session_id)
    return {"result": result}
```

---

## 更新现有智能体

当用户想更新或调试现有智能体时，按此结构组织回复：

```
## 现有问题
[描述当前问题]

## 根本原因
[在架构层面识别发生原因]

## 建议更新
[在架构层面概述变更]

## 更新后的代码
[仅生成变更的模块]

## 迁移说明
[什么会破坏、什么向后兼容]

## 性能影响
[延迟 / token / 内存变化]
```

---

## 标准文件夹结构

始终按此布局生成代码：

```
multi_agent_system/
├── agents/          # One file per agent role
├── tools/           # Tool definitions and wrappers
├── memory/          # Redis, VectorDB, LangChain memory helpers
├── prompts/         # Prompt templates (one per agent)
├── workflows/       # High-level orchestration logic
├── graphs/          # LangGraph state + compiled graph definitions
├── api/             # FastAPI routes (optional)
├── configs/         # Config loader — no secrets in code
├── tests/           # Unit + integration tests per agent
└── main.py
```

---

## 示例

### 示例1：研究+编码多智能体工作流

```python
# agents/research_agent.py
async def research_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o").bind_tools([web_search, rag_search])
    response = await llm.ainvoke(
        f"Research the following and return structured findings:\n{state['user_goal']}"
    )
    state["context"]["research"] = response.content
    state["next_agent"] = "coder"
    return state

# agents/coding_agent.py
async def coding_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o").bind_tools([python_repl, github_tool])
    response = await llm.ainvoke(
        f"Given this research:\n{state['context']['research']}\n\nWrite production Python code."
    )
    state["context"]["code"] = response.content
    state["next_agent"] = "validator"
    return state
```

### 示例2：带动态委托的监督者

```python
# agents/supervisor_agent.py
DELEGATION_PROMPT = """
You are a supervisor. Given the current state, decide the next agent.
Available agents: research, coder, validator, end.
Respond with ONLY the agent name.

Goal: {goal}
Completed: {completed}
Context keys available: {context}
"""

async def supervisor_node(state: AgentState) -> AgentState:
    state["step_count"] += 1
    llm = ChatOpenAI(model="gpt-4o")
    decision = await llm.ainvoke(
        DELEGATION_PROMPT.format(
            goal=state["user_goal"],
            completed=state["completed_tasks"],
            context=list(state["context"].keys()),
        )
    )
    next_agent = decision.content.strip().lower()
    # Validate against allowlist before setting
    allowed = {"research", "coder", "validator", "end"}
    state["next_agent"] = next_agent if next_agent in allowed else "end"
    return state
```

### 示例3：DeepAgents 反思循环

```python
async def reflection_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(model="gpt-4o")
    critique = await llm.ainvoke(
        f"Evaluate this output critically:\n{state['context'].get('code', '')}\n"
        "List any bugs, gaps, or improvements. Be concise."
    )
    state["context"]["critique"] = critique.content
    state["next_agent"] = "coder" if "bug" in critique.content.lower() else "end"
    return state
```

---

## 最佳实践

- ✅ 一个智能体 = 一个职责——永不将规划+编码+测试合并在一个节点
- ✅ 所有状态 schema 使用 `TypedDict`——启用类型检查和图验证
- ✅ 仅绑定每个智能体需要的工具——减少幻觉工具调用
- ✅ 始终添加 `step_count` 守卫以防止无限路由循环
- ✅ 全程使用 `async`/`await`——LangGraph原生支持异步
- ✅ 所有密钥存入通过 `os.getenv()` 加载的环境变量
- ✅ 所有 Redis 键设置 TTL 并限定到 `session_id`
- ✅ 每个节点入口和工具调用处记录日志以提升可观测性
- ✅ 监督者路由输出必须对照智能体名称白名单校验
- ❌ 不要硬编码 API 密钥、模型名或 Redis URL
- ❌ 不要跨不需要它们的智能体共享工具列表
- ❌ 不要跳过错误处理——工具失败和空LLM响应很常见
- ❌ 不要信任未校验的LLM路由决策——始终对照白名单检查

---

## 局限性

- 本技能不替代生产部署前的环境测试、负载测试或安全审查。
- 生成的 LangGraph 代码面向当前稳定 API——始终用已安装版本验证方法签名（`pip show langgraph`）。
- 若智能体目标、工具权限或路由逻辑模糊，停止并在生成完整架构前请求澄清。
- DeepAgents集成模式假设库已安装并在目标环境配置。

---

## 安全与注意事项

- 永不在生成代码中暴露 API 密钥。所有密钥必须使用环境变量：
  ```python
  OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")   # ✅ correct
  OPENAI_API_KEY = "sk-..."                        # ❌ never do this
  ```
- 注入智能体提示前始终校验和清理用户输入——将所有用户输入视为不可信。
- 允许智能体执行 shell 命令或写入文件系统前添加权限层。
- 若生成 Python REPL 工具节点，文档必须注明仅在沙箱隔离环境中运行。
  <!-- security-allowlist: python_repl tool examples are for sandboxed execution environments only -->
- 生产部署时，所有 LLM 和外部 API 调用需添加速率限制处理和指数退避。
- 所有 Redis 会话键限定到 `session_id` 并设置 TTL 以防止跨会话内存泄漏。

---

## 常见陷阱

- **问题：**智能体在监督者和子智能体间无限循环  
  **方案：**状态添加 `step_count: int`；`route_next()` 中 `step_count > N` 时返回 `"end"`

- **问题：**监督者路由到不存在智能体名  
  **方案：**将LLM路由输出对照硬编码白名单校验后再设 `next_agent`

- **问题：**跨用户会话内存泄漏  
  **方案：**Redis 键限定到 `session_id` 并始终设 TTL（`ttl=3600`）

- **问题：**工具结果被下个智能体忽略  
  **方案：**工具输出必须写入 `state["context"]`，并确认下个节点读取它

- **问题：**智能体共享过多工具并幻觉错误调用  
  **方案：**按智能体使用 `.bind_tools([only_relevant_tools])` 而非全局工具列表

- **问题：**图在 API 速率限制时静默失败  
  **方案：**LLM调用用 `tenacity` 包装重试逻辑和指数退避

---

## 相关技能

- `@langchain-rag` - 专门用于检索增强生成流水线
- `@fastapi-backend` - 将智能体系统部署为生产 REST API
- `@python-async` - 深化智能体节点中使用的 async/await 模式