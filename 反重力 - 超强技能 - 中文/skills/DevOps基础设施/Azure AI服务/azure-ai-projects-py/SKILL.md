---
name: azure-ai-projects-py
description: "使用 azure-ai-projects SDK 在 Microsoft Foundry 上构建 AI 应用。触发词：Azure AI Projects、Foundry SDK、Azure AI 开发、AIProjectClient、Azure 智能体、Azure AI 搜索、Azure 评估、Azure 连接"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure AI Projects Python SDK (Foundry SDK)

使用 `azure-ai-projects` SDK 在 Microsoft Foundry 上构建 AI 应用。

## 安装

```bash
pip install azure-ai-projects azure-identity
```

## 环境变量

```bash
AZURE_AI_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
```

## 身份认证

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

credential = DefaultAzureCredential()
client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=credential,
)
```

## 客户端操作概览

| 操作 | 访问方式 | 用途 |
|-----------|--------|---------|
| `client.agents` | `.agents.*` | 智能体 CRUD、版本、线程、运行 |
| `client.connections` | `.connections.*` | 列出/获取项目连接 |
| `client.deployments` | `.deployments.*` | 列出模型部署 |
| `client.datasets` | `.datasets.*` | 数据集管理 |
| `client.indexes` | `.indexes.*` | 索引管理 |
| `client.evaluations` | `.evaluations.*` | 运行评估 |
| `client.red_teams` | `.red_teams.*` | 红队测试操作 |

## 两种客户端方式

### 1. AIProjectClient（Foundry 原生）

```python
from azure.ai.projects import AIProjectClient

client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# 使用 Foundry 原生操作
agent = client.agents.create_agent(
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    name="my-agent",
    instructions="You are helpful.",
)
```

### 2. OpenAI 兼容客户端

```python
# 从项目获取 OpenAI 兼容客户端
openai_client = client.get_openai_client()

# 使用标准 OpenAI API
response = openai_client.chat.completions.create(
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    messages=[{"role": "user", "content": "Hello!"}],
)
```

## 智能体操作

### 创建智能体（基础）

```python
agent = client.agents.create_agent(
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    name="my-agent",
    instructions="You are a helpful assistant.",
)
```

### 创建带工具的智能体

```python
from azure.ai.agents import CodeInterpreterTool, FileSearchTool

agent = client.agents.create_agent(
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    name="tool-agent",
    instructions="You can execute code and search files.",
    tools=[CodeInterpreterTool(), FileSearchTool()],
)
```

### 使用 PromptAgentDefinition 的版本化智能体

```python
from azure.ai.projects.models import PromptAgentDefinition

# 创建版本化智能体
agent_version = client.agents.create_version(
    agent_name="customer-support-agent",
    definition=PromptAgentDefinition(
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        instructions="You are a customer support specialist.",
        tools=[],  # 按需添加工具
    ),
    version_label="v1.0",
)
```

详细智能体模式请参阅 references/agents.md。

## 工具概览

| 工具 | 类 | 用途 |
|------|-------|----------|
| Code Interpreter | `CodeInterpreterTool` | 执行 Python、生成文件 |
| File Search | `FileSearchTool` | 对上传文档进行 RAG |
| Bing Grounding | `BingGroundingTool` | 网页搜索（需要连接） |
| Azure AI Search | `AzureAISearchTool` | 搜索你的索引 |
| Function Calling | `FunctionTool` | 调用你的 Python 函数 |
| OpenAPI | `OpenApiTool` | 调用 REST API |
| MCP | `McpTool` | Model Context Protocol 服务器 |
| Memory Search | `MemorySearchTool` | 搜索智能体内存存储 |
| SharePoint | `SharepointGroundingTool` | 搜索 SharePoint 内容 |

所有工具模式请参阅 references/tools.md。

## 线程和消息流程

```python
# 1. 创建线程
thread = client.agents.threads.create()

# 2. 添加消息
client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="What's the weather like?",
)

# 3. 创建并处理运行
run = client.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
)

# 4. 获取响应
if run.status == "completed":
    messages = client.agents.messages.list(thread_id=thread.id)
    for msg in messages:
        if msg.role == "assistant":
            print(msg.content[0].text.value)
```

## 连接

```python
# 列出所有连接
connections = client.connections.list()
for conn in connections:
    print(f"{conn.name}: {conn.connection_type}")

# 获取特定连接
connection = client.connections.get(connection_name="my-search-connection")
```

连接模式请参阅 references/connections.md。

## 部署

```python
# 列出可用的模型部署
deployments = client.deployments.list()
for deployment in deployments:
    print(f"{deployment.name}: {deployment.model}")
```

部署模式请参阅 references/deployments.md。

## 数据集和索引

```python
# 列出数据集
datasets = client.datasets.list()

# 列出索引
indexes = client.indexes.list()
```

数据操作请参阅 references/datasets-indexes.md。

## 评估

```python
# 使用 OpenAI 客户端进行评估
openai_client = client.get_openai_client()

# 使用内置评估器创建评估
eval_run = openai_client.evals.runs.create(
    eval_id="my-eval",
    name="quality-check",
    data_source={
        "type": "custom",
        "item_references": [{"item_id": "test-1"}],
    },
    testing_criteria=[
        {"type": "fluency"},
        {"type": "task_adherence"},
    ],
)
```

评估模式请参阅 references/evaluation.md。

## 异步客户端

```python
from azure.ai.projects.aio import AIProjectClient

async with AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
) as client:
    agent = await client.agents.create_agent(...)
    # ... 异步操作
```

异步模式请参阅 references/async-patterns.md。

## 内存存储

```python
# 为智能体创建内存存储
memory_store = client.agents.create_memory_store(
    name="conversation-memory",
)

# 附加到智能体以实现持久化内存
agent = client.agents.create_agent(
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    name="memory-agent",
    tools=[MemorySearchTool()],
    tool_resources={"memory": {"store_ids": [memory_store.id]}},
)
```

## 最佳实践

1. **使用上下文管理器**处理异步客户端：`async with AIProjectClient(...) as client:`
2. **完成后清理智能体**：`client.agents.delete_agent(agent.id)`
3. **简单运行使用 `create_and_process`**，**实时 UX 使用流式传输**
4. **生产部署使用版本化智能体**
5. **外部服务集成优先使用连接**（AI Search、Bing 等）

## SDK 对比

| 特性 | `azure-ai-projects` | `azure-ai-agents` |
|---------|---------------------|-------------------|
| 层级 | 高层（Foundry） | 底层（Agents） |
| 客户端 | `AIProjectClient` | `AgentsClient` |
| 版本控制 | `create_version()` | 不可用 |
| 连接 | 是 | 否 |
| 部署 | 是 | 否 |
| 数据集/索引 | 是 | 否 |
| 评估 | 通过 OpenAI 客户端 | 否 |
| 适用场景 | 完整 Foundry 集成 | 独立智能体应用 |

## 参考文件

- references/agents.md: 使用 PromptAgentDefinition 的智能体操作
- references/tools.md: 所有智能体工具及示例
- references/evaluation.md: 评估操作概览
- references/built-in-evaluators.md: 完整内置评估器参考
- references/custom-evaluators.md: 基于代码和提示词的评估器模式
- references/connections.md: 连接操作
- references/deployments.md: 部署枚举
- references/datasets-indexes.md: 数据集和索引操作
- references/async-patterns.md: 异步客户端使用
- references/api-reference.md: 完整 API 参考（v2.0.0b4 全部 373 个 SDK 导出）
- scripts/run_batch_evaluation.py: 批量评估 CLI 工具

## 适用场景
本技能适用于执行概览中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不应替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
