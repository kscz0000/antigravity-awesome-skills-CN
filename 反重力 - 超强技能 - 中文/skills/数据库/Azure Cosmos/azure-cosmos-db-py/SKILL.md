---
name: azure-cosmos-db-py
description: "构建生产级 Azure Cosmos DB NoSQL 服务，遵循整洁代码、安全最佳实践和 TDD 原则。触发词：Cosmos DB、Azure Cosmos、NoSQL数据库、Python Cosmos、Azure数据库、Cosmos DB Python SDK、文档数据库、分区键、RU优化、Cosmos容器"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Cosmos DB 服务实现

构建生产级 Azure Cosmos DB NoSQL 服务，遵循整洁代码、安全最佳实践和 TDD 原则。

## 安装

```bash
pip install azure-cosmos azure-identity
```

## 环境变量

```bash
COSMOS_ENDPOINT=https://<account>.documents.azure.com:443/
COSMOS_DATABASE_NAME=<database-name>
COSMOS_CONTAINER_ID=<container-id>
# 仅用于模拟器（不用于生产环境）
COSMOS_KEY=<emulator-key>
```

## 身份认证

**DefaultAzureCredential（推荐）**:
```python
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

client = CosmosClient(
    url=os.environ["COSMOS_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

**模拟器（本地开发）**:
```python
from azure.cosmos import CosmosClient

client = CosmosClient(
    url="https://localhost:8081",
    credential=os.environ["COSMOS_KEY"],
    connection_verify=False
)
```

## 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                         FastAPI Router                          │
│  - Auth dependencies (get_current_user, get_current_user_required)
│  - HTTP error responses (HTTPException)                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                        Service Layer                            │
│  - Business logic and validation                                │
│  - Document ↔ Model conversion                                  │
│  - Graceful degradation when Cosmos unavailable                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────┐
│                     Cosmos DB Client Module                     │
│  - Singleton container initialization                           │
│  - Dual auth: DefaultAzureCredential (Azure) / Key (emulator)   │
│  - Async wrapper via run_in_threadpool                          │
└─────────────────────────────────────────────────────────────────┘
```

## 快速开始

### 1. 客户端模块设置

创建支持双重认证的单例 Cosmos 客户端：

```python
# db/cosmos.py
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
from starlette.concurrency import run_in_threadpool

_cosmos_container = None

def _is_emulator_endpoint(endpoint: str) -> bool:
    return "localhost" in endpoint or "127.0.0.1" in endpoint

async def get_container():
    global _cosmos_container
    if _cosmos_container is None:
        if _is_emulator_endpoint(settings.cosmos_endpoint):
            client = CosmosClient(
                url=settings.cosmos_endpoint,
                credential=settings.cosmos_key,
                connection_verify=False
            )
        else:
            client = CosmosClient(
                url=settings.cosmos_endpoint,
                credential=DefaultAzureCredential()
            )
        db = client.get_database_client(settings.cosmos_database_name)
        _cosmos_container = db.get_container_client(settings.cosmos_container_id)
    return _cosmos_container
```

**完整实现**：参见 references/client-setup.md

### 2. Pydantic 模型层级

使用五层模型模式实现清晰分离：

```python
class ProjectBase(BaseModel):           # 共享字段
    name: str = Field(..., min_length=1, max_length=200)

class ProjectCreate(ProjectBase):       # 创建请求
    workspace_id: str = Field(..., alias="workspaceId")

class ProjectUpdate(BaseModel):         # 部分更新（全部可选）
    name: Optional[str] = Field(None, min_length=1)

class Project(ProjectBase):             # API 响应
    id: str
    created_at: datetime = Field(..., alias="createdAt")

class ProjectInDB(Project):             # 内部使用，含 docType
    doc_type: str = "project"
```

### 3. 服务层模式

```python
class ProjectService:
    def _use_cosmos(self) -> bool:
        return get_container() is not None
    
    async def get_by_id(self, project_id: str, workspace_id: str) -> Project | None:
        if not self._use_cosmos():
            return None
        doc = await get_document(project_id, partition_key=workspace_id)
        if doc is None:
            return None
        return self._doc_to_model(doc)
```

**完整模式**：参见 references/service-layer.md

## 核心原则

### 安全要求

1. **RBAC 认证**：在 Azure 中使用 `DefaultAzureCredential` — 绝不在代码中存储密钥
2. **仅模拟器使用密钥**：仅在本地开发时硬编码已知的模拟器密钥
3. **参数化查询**：始终使用 `@parameter` 语法 — 绝不使用字符串拼接
4. **分区键验证**：验证分区键访问与用户授权匹配

### 整洁代码规范

1. **单一职责**：客户端模块处理连接；服务层处理业务逻辑
2. **优雅降级**：Cosmos 不可用时服务返回 `None`/`[]`
3. **一致命名**：`_doc_to_model()`、`_model_to_doc()`、`_use_cosmos()`
4. **类型提示**：所有公共方法使用完整类型标注
5. **驼峰别名**：使用 `Field(alias="camelCase")` 进行 JSON 序列化

### TDD 要求

在实现之前编写测试，使用以下模式：

```python
@pytest.fixture
def mock_cosmos_container(mocker):
    container = mocker.MagicMock()
    mocker.patch("app.db.cosmos.get_container", return_value=container)
    return container

@pytest.mark.asyncio
async def test_get_project_by_id_returns_project(mock_cosmos_container):
    # Arrange
    mock_cosmos_container.read_item.return_value = {"id": "123", "name": "Test"}
    
    # Act
    result = await project_service.get_by_id("123", "workspace-1")
    
    # Assert
    assert result.id == "123"
    assert result.name == "Test"
```

**完整测试指南**：参见 references/testing.md

## 参考文件

| 文件 | 阅读时机 |
|------|----------|
| references/client-setup.md | 设置双重认证的 Cosmos 客户端、SSL 配置、单例模式 |
| references/service-layer.md | 实现完整的 CRUD 服务类、转换、优雅降级 |
| references/testing.md | 编写 pytest 测试、模拟 Cosmos、集成测试设置 |
| references/partitioning.md | 选择分区键、跨分区查询、移动操作 |
| references/error-handling.md | 处理 CosmosResourceNotFoundError、日志、HTTP 错误映射 |

## 模板文件

| 文件 | 用途 |
|------|------|
| assets/cosmos_client_template.py | 开箱即用的客户端模块 |
| assets/service_template.py | 服务类骨架 |
| assets/conftest_template.py | Cosmos 模拟的 pytest fixtures |

## 质量属性（非功能性需求）

### 可靠性
- Cosmos 不可用时优雅降级
- 瞬态故障的指数退避重试逻辑
- 通过单例模式实现连接池

### 安全性
- 代码中零密钥（通过 DefaultAzureCredential 实现 RBAC）
- 参数化查询防止注入
- 分区键隔离强制数据边界

### 可维护性
- 五层模型模式支持模式演进
- 服务层解耦业务逻辑与存储
- 所有实体服务采用一致模式

### 可测试性
- 通过 `get_container()` 实现依赖注入
- 模块级全局变量便于模拟
- 清晰分离支持无 Cosmos 的单元测试

### 性能
- 分区键查询避免跨分区扫描
- 异步包装防止阻塞 FastAPI 事件循环
- 最小化文档转换开销

## 使用时机
本技能适用于执行概览中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
