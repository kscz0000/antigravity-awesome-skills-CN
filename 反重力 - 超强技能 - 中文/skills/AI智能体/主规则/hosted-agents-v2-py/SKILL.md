---
name: hosted-agents-v2-py
description: "使用 Azure AI Projects SDK 和 ImageBasedHostedAgentDefinition 构建托管智能体。适用于在 Azure AI Foundry 中创建基于容器的智能体。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure AI 托管智能体（Python）

使用 Azure AI Projects SDK 中的 `ImageBasedHostedAgentDefinition` 构建基于容器的托管智能体。

## 安装

```bash
pip install azure-ai-projects>=2.0.0b3 azure-identity
```

**最低 SDK 版本：** 托管智能体支持需要 `2.0.0b3` 或更高版本。

## 环境变量

```bash
AZURE_AI_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
```

## 前提条件

创建托管智能体前：

1. **容器镜像** - 构建并推送到 Azure Container Registry (ACR)
2. **ACR 拉取权限** - 为项目的托管标识授予 ACR 的 `AcrPull` 角色
3. **能力主机** - 账户级能力主机，启用 `enablePublicHostingEnvironment=true`
4. **SDK 版本** - 确保 `azure-ai-projects>=2.0.0b3`

## 认证

始终使用 `DefaultAzureCredential`：

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

credential = DefaultAzureCredential()
client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=credential
)
```

## 核心工作流

### 1. 导入

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    ImageBasedHostedAgentDefinition,
    ProtocolVersionRecord,
    AgentProtocol,
)
```

### 2. 创建托管智能体

```python
client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)

agent = client.agents.create_version(
    agent_name="my-hosted-agent",
    definition=ImageBasedHostedAgentDefinition(
        container_protocol_versions=[
            ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")
        ],
        cpu="1",
        memory="2Gi",
        image="myregistry.azurecr.io/my-agent:latest",
        tools=[{"type": "code_interpreter"}],
        environment_variables={
            "AZURE_AI_PROJECT_ENDPOINT": os.environ["AZURE_AI_PROJECT_ENDPOINT"],
            "MODEL_NAME": "gpt-4o-mini"
        }
    )
)

print(f"Created agent: {agent.name} (version: {agent.version})")
```

### 3. 列出智能体版本

```python
versions = client.agents.list_versions(agent_name="my-hosted-agent")
for version in versions:
    print(f"Version: {version.version}, State: {version.state}")
```

### 4. 删除智能体版本

```python
client.agents.delete_version(
    agent_name="my-hosted-agent",
    version=agent.version
)
```

## ImageBasedHostedAgentDefinition 参数

| 参数 | 类型 | 必需 | 描述 |
|-----------|------|----------|-------------|
| `container_protocol_versions` | `list[ProtocolVersionRecord]` | 是 | 智能体支持的协议版本 |
| `image` | `str` | 是 | 完整容器镜像路径（registry/image:tag） |
| `cpu` | `str` | 否 | CPU 分配（如 "1"、"2"） |
| `memory` | `str` | 否 | 内存分配（如 "2Gi"、"4Gi"） |
| `tools` | `list[dict]` | 否 | 智能体可用的工具 |
| `environment_variables` | `dict[str, str]` | 否 | 容器的环境变量 |

## 协议版本

`container_protocol_versions` 参数指定智能体支持哪些协议：

```python
from azure.ai.projects.models import ProtocolVersionRecord, AgentProtocol

# RESPONSES 协议 - 标准智能体响应
container_protocol_versions=[
    ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")
]
```

**可用协议：**
| 协议 | 描述 |
|----------|-------------|
| `AgentProtocol.RESPONSES` | 智能体交互的标准响应协议 |

## 资源分配

为容器指定 CPU 和内存：

```python
definition=ImageBasedHostedAgentDefinition(
    container_protocol_versions=[...],
    image="myregistry.azurecr.io/my-agent:latest",
    cpu="2",      # 2 CPU 核心
    memory="4Gi"  # 4 GiB 内存
)
```

**资源限制：**
| 资源 | 最小 | 最大 | 默认 |
|----------|-----|-----|---------|
| CPU | 0.5 | 4 | 1 |
| 内存 | 1Gi | 8Gi | 2Gi |

## 工具配置

为托管智能体添加工具：

### 代码解释器

```python
tools=[{"type": "code_interpreter"}]
```

### MCP 工具

```python
tools=[
    {"type": "code_interpreter"},
    {
        "type": "mcp",
        "server_label": "my-mcp-server",
        "server_url": "https://my-mcp-server.example.com"
    }
]
```

### 多工具

```python
tools=[
    {"type": "code_interpreter"},
    {"type": "file_search"},
    {
        "type": "mcp",
        "server_label": "custom-tool",
        "server_url": "https://custom-tool.example.com"
    }
]
```

## 环境变量

向容器传递配置：

```python
environment_variables={
    "AZURE_AI_PROJECT_ENDPOINT": os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    "MODEL_NAME": "gpt-4o-mini",
    "LOG_LEVEL": "INFO",
    "CUSTOM_CONFIG": "value"
}
```

**最佳实践：** 切勿硬编码密钥。使用环境变量或 Azure Key Vault。

## 完整示例

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    ImageBasedHostedAgentDefinition,
    ProtocolVersionRecord,
    AgentProtocol,
)

def create_hosted_agent():
    """使用自定义容器镜像创建托管智能体。"""
    
    client = AIProjectClient(
        endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential()
    )
    
    agent = client.agents.create_version(
        agent_name="data-processor-agent",
        definition=ImageBasedHostedAgentDefinition(
            container_protocol_versions=[
                ProtocolVersionRecord(
                    protocol=AgentProtocol.RESPONSES,
                    version="v1"
                )
            ],
            image="myregistry.azurecr.io/data-processor:v1.0",
            cpu="2",
            memory="4Gi",
            tools=[
                {"type": "code_interpreter"},
                {"type": "file_search"}
            ],
            environment_variables={
                "AZURE_AI_PROJECT_ENDPOINT": os.environ["AZURE_AI_PROJECT_ENDPOINT"],
                "MODEL_NAME": "gpt-4o-mini",
                "MAX_RETRIES": "3"
            }
        )
    )
    
    print(f"Created hosted agent: {agent.name}")
    print(f"Version: {agent.version}")
    print(f"State: {agent.state}")
    
    return agent

if __name__ == "__main__":
    create_hosted_agent()
```

## 异步模式

```python
import os
from azure.identity.aio import DefaultAzureCredential
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import (
    ImageBasedHostedAgentDefinition,
    ProtocolVersionRecord,
    AgentProtocol,
)

async def create_hosted_agent_async():
    """异步创建托管智能体。"""
    
    async with DefaultAzureCredential() as credential:
        async with AIProjectClient(
            endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
            credential=credential
        ) as client:
            agent = await client.agents.create_version(
                agent_name="async-agent",
                definition=ImageBasedHostedAgentDefinition(
                    container_protocol_versions=[
                        ProtocolVersionRecord(
                            protocol=AgentProtocol.RESPONSES,
                            version="v1"
                        )
                    ],
                    image="myregistry.azurecr.io/async-agent:latest",
                    cpu="1",
                    memory="2Gi"
                )
            )
            return agent
```

## 常见错误

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `ImagePullBackOff` | ACR 拉取权限被拒绝 | 为项目的托管标识授予 `AcrPull` 角色 |
| `InvalidContainerImage` | 镜像未找到 | 验证镜像路径和标签在 ACR 中存在 |
| `CapabilityHostNotFound` | 未配置能力主机 | 创建账户级能力主机 |
| `ProtocolVersionNotSupported` | 无效协议版本 | 使用 `AgentProtocol.RESPONSES` 配合版本 `"v1"` |

## 最佳实践

1. **版本化镜像** - 生产环境使用特定标签，而非 `latest`
2. **最小资源** - 从最小 CPU/内存开始，按需扩展
3. **环境变量** - 用于所有配置，绝不硬编码
4. **错误处理** - 将智能体创建包装在 try/except 块中
5. **清理** - 删除未使用的智能体版本以释放资源

## 参考链接

- [Azure AI Projects SDK](https://pypi.org/project/azure-ai-projects/)
- [Hosted Agents Documentation](https://learn.microsoft.com/azure/ai-services/agents/how-to/hosted-agents)
- [Azure Container Registry](https://learn.microsoft.com/azure/container-registry/)

## 何时使用
本技能适用于执行概述中描述的工作流程或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
