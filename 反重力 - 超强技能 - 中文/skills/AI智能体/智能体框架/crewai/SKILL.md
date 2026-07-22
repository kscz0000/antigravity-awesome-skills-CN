---
name: crewai
description: CrewAI 专家 - 领先的基于角色的多智能体框架，财富 500 强企业 60% 在用。触发词：CrewAI、多智能体团队、智能体角色、crew、协作智能体、角色化智能体
risk: unknown
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# CrewAI

CrewAI 专家 - 领先的基于角色的多智能体框架，财富 500 强企业 60% 在用。涵盖角色与目标驱动的智能体设计、任务定义、Crew 编排、流程类型（顺序、层级、并行）、记忆系统，以及复杂工作流的 Flow。构建协作 AI 智能体团队的核心技能。

**角色**: CrewAI 多智能体架构师

你是使用 CrewAI 设计协作 AI 智能体团队的专家。你以角色、职责和委托的方式思考。你设计具有特定专业知识的清晰智能体人设，创建具有预期输出的明确定义任务，并编排 Crew 以实现最佳协作。你知道何时使用顺序流程与层级流程。

### 专业领域

- 智能体人设设计
- 任务分解
- Crew 编排
- 流程选择
- 记忆配置
- Flow 设计

## 能力

- 智能体定义（角色、目标、背景故事）
- 任务设计与依赖
- Crew 编排
- 流程类型（顺序、层级）
- 记忆配置
- 工具集成
- 复杂工作流的 Flow

## 前置条件

- 0: Python 熟练
- 1: 多智能体概念
- 2: 理解委托机制
- 所需技能: Python 3.10+, crewai 包, LLM API 访问

## 范围

- 0: 仅 Python
- 1: 最适合结构化工作流
- 2: 简单场景可能过于冗长
- 3: Flow 是较新功能

## 生态系统

### 主要

- CrewAI 框架
- CrewAI Tools

### 常见集成

- OpenAI / Anthropic / Ollama
- SerperDev (搜索)
- FileReadTool, DirectoryReadTool
- 自定义工具

### 平台

- Python 应用
- FastAPI 后端
- 企业部署

## 模式

### 使用 YAML 配置的基础 Crew

在 YAML 中定义智能体和任务（推荐）

**何时使用**: 任何 CrewAI 项目

# config/agents.yaml
researcher:
  role: "Senior Research Analyst"
  goal: "Find comprehensive, accurate information on {topic}"
  backstory: |
    You are an expert researcher with years of experience
    in gathering and analyzing information. You're known
    for your thorough and accurate research.
  tools:
    - SerperDevTool
    - WebsiteSearchTool
  verbose: true

writer:
  role: "Content Writer"
  goal: "Create engaging, well-structured content"
  backstory: |
    You are a skilled writer who transforms research
    into compelling narratives. You focus on clarity
    and engagement.
  verbose: true

# config/tasks.yaml
research_task:
  description: |
    Research the topic: {topic}

    Focus on:
    1. Key facts and statistics
    2. Recent developments
    3. Expert opinions
    4. Contrarian viewpoints

    Be thorough and cite sources.
  agent: researcher
  expected_output: |
    A comprehensive research report with:
    - Executive summary
    - Key findings (bulleted)
    - Sources cited

writing_task:
  description: |
    Using the research provided, write an article about {topic}.

    Requirements:
    - 800-1000 words
    - Engaging introduction
    - Clear structure with headers
    - Actionable conclusion
  agent: writer
  expected_output: "A polished article ready for publication"
  context:
    - research_task  # Uses output from research

# crew.py
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class ContentCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(config=self.agents_config['researcher'])

    @agent
    def writer(self) -> Agent:
        return Agent(config=self.agents_config['writer'])

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @task
    def writing_task(self) -> Task:
        return Task(config=self.tasks_config['writing_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

# main.py
crew = ContentCrew()
result = crew.crew().kickoff(inputs={"topic": "AI Agents in 2025"})

### 层级流程

管理智能体委托给工作者智能体

**何时使用**: 需要协调的复杂任务

from crewai import Crew, Process

# Define specialized agents
researcher = Agent(
    role="Research Specialist",
    goal="Find accurate information",
    backstory="Expert researcher..."
)

analyst = Agent(
    role="Data Analyst",
    goal="Analyze and interpret data",
    backstory="Expert analyst..."
)

writer = Agent(
    role="Content Writer",
    goal="Create engaging content",
    backstory="Expert writer..."
)

# Hierarchical crew - manager coordinates
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.hierarchical,
    manager_llm=ChatOpenAI(model="gpt-4o"),  # Manager model
    verbose=True
)

# Manager decides:
# - Which agent handles which task
# - When to delegate
# - How to combine results

result = crew.kickoff()

### 规划功能

运行前生成执行计划

**何时使用**: 需要结构的复杂工作流

from crewai import Crew, Process

# Enable planning
crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research, write, review],
    process=Process.sequential,
    planning=True,  # Enable planning
    planning_llm=ChatOpenAI(model="gpt-4o")  # Planner model
)

# With planning enabled:
# 1. CrewAI generates step-by-step plan
# 2. Plan is injected into each task
# 3. Agents see overall structure
# 4. More consistent results

result = crew.kickoff()

# Access the plan
print(crew.plan)

### 记忆配置

启用智能体记忆以保持上下文

**何时使用**: 多轮或复杂工作流

from crewai import Crew

# Memory types:
# - Short-term: Within task execution
# - Long-term: Across executions
# - Entity: About specific entities

crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,  # Enable all memory types
    verbose=True
)

# Custom memory config
from crewai.memory import LongTermMemory, ShortTermMemory

crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,
    long_term_memory=LongTermMemory(
        storage=CustomStorage()  # Custom backend
    ),
    short_term_memory=ShortTermMemory(
        storage=CustomStorage()
    ),
    embedder={
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"}
    }
)

# Memory helps agents:
# - Remember previous interactions
# - Build on past work
# - Maintain consistency

### 复杂工作流的 Flow

带状态的事件驱动编排

**何时使用**: 复杂、多阶段工作流

from crewai.flow.flow import Flow, listen, start, and_, or_, router

class ContentFlow(Flow):
    # State persists across steps
    model_config = {"extra": "allow"}

    @start()
    def gather_requirements(self):
        """First step - gather inputs."""
        self.topic = self.inputs.get("topic", "AI")
        self.style = self.inputs.get("style", "professional")
        return {"topic": self.topic}

    @listen(gather_requirements)
    def research(self, requirements):
        """Research after requirements gathered."""
        research_crew = ResearchCrew()
        result = research_crew.crew().kickoff(
            inputs={"topic": requirements["topic"]}
        )
        self.research = result.raw
        return result

    @listen(research)
    def write_content(self, research_result):
        """Write after research complete."""
        writing_crew = WritingCrew()
        result = writing_crew.crew().kickoff(
            inputs={
                "research": self.research,
                "style": self.style
            }
        )
        return result

    @router(write_content)
    def quality_check(self, content):
        """Route based on quality."""
        if self.needs_revision(content):
            return "revise"
        return "publish"

    @listen("revise")
    def revise_content(self):
        """Revision flow."""
        # Re-run writing with feedback
        pass

    @listen("publish")
    def publish_content(self):
        """Final publishing."""
        return {"status": "published", "content": self.content}

# Run flow
flow = ContentFlow()
result = flow.kickoff(inputs={"topic": "AI Agents"})

### 自定义工具

为智能体创建工具

**何时使用**: 智能体需要外部能力

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# Method 1: Class-based tool
class SearchInput(BaseModel):
    query: str = Field(..., description="Search query")

class WebSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the web for information"
    args_schema: type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        # Implementation
        results = search_api.search(query)
        return format_results(results)

# Method 2: Function decorator
from crewai import tool

@tool("Database Query")
def query_database(sql: str) -> str:
    """Execute SQL query and return results."""
    return db.execute(sql)

# Assign tools to agents
researcher = Agent(
    role="Researcher",
    goal="Find information",
    backstory="...",
    tools=[WebSearchTool(), query_database]
)

## 协作

### 委托触发

- langgraph|state machine|graph -> langgraph (需要显式状态管理)
- observability|tracing -> langfuse (需要 LLM 可观测性)
- structured output|json schema -> structured-output (需要结构化响应)

### 研究与写作 Crew

技能: crewai, structured-output

工作流:

```
1. 定义研究员和写手智能体
2. 创建研究 → 分析 → 写作流水线
3. 使用结构化输出作为研究格式
4. 通过 context 链接任务
```

### 可观测智能体团队

技能: crewai, langfuse

工作流:

```
1. 构建包含智能体和任务的 Crew
2. 添加 Langfuse 回调处理器
3. 监控智能体交互
4. 评估输出质量
```

### 使用 Flow 的复杂工作流

技能: crewai, langgraph

工作流:

```
1. 使用 CrewAI Flow 设计工作流
2. 使用 LangGraph 模式处理状态
3. 在 Flow 步骤中组合 Crew
4. 处理分支和路由
```

## 相关技能

配合使用: `langgraph`, `autonomous-agents`, `langfuse`, `structured-output`

## 何时使用

- 用户提及或暗示: crewai
- 用户提及或暗示: 多智能体团队
- 用户提及或暗示: 智能体角色
- 用户提及或暗示: crew of agents
- 用户提及或暗示: 基于角色的智能体
- 用户提及或暗示: 协作智能体

## 限制

- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
