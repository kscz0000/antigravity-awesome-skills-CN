# Python MCP 服务器实现指南

## 概述

本文档提供使用 MCP Python SDK 实现 MCP 服务器的 Python 特定最佳实践和示例。涵盖服务器设置、工具注册模式、使用 Pydantic 的输入验证、错误处理以及完整可运行示例。

---

## 快速参考

### 关键导入
```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
```

### 服务器初始化
```python
mcp = FastMCP("service_mcp")
```

### 工具注册模式
```python
@mcp.tool(name="tool_name", annotations={...})
async def tool_function(params: InputModel) -> str:
    # 实现
    pass
```

---

## MCP Python SDK 与 FastMCP

官方 MCP Python SDK 提供 FastMCP，一个用于构建 MCP 服务器的高级框架。它提供：
- 从函数签名和文档字符串自动生成描述和 inputSchema
- Pydantic 模型集成用于输入验证
- 基于装饰器的工具注册，使用 `@mcp.tool`

**完整的 SDK 文档，使用 WebFetch 加载：**
`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`

## 服务器命名约定

Python MCP 服务器必须遵循此命名模式：
- **格式**：`{service}_mcp`（小写加下划线）
- **示例**：`github_mcp`、`jira_mcp`、`stripe_mcp`

名称应该是：
- 通用的（不绑定特定功能）
- 描述所集成的服务/API
- 易于从任务描述推断
- 不包含版本号或日期

## 工具实现

### 工具命名

使用 snake_case 命名工具（如 "search_users"、"create_project"、"get_channel_info"），采用清晰、面向操作的名称。

**避免命名冲突**：包含服务上下文以防止重叠：
- 使用 "slack_send_message" 而非仅 "send_message"
- 使用 "github_create_issue" 而非仅 "create_issue"
- 使用 "asana_list_tasks" 而非仅 "list_tasks"

### 使用 FastMCP 的工具结构

工具使用 `@mcp.tool` 装饰器定义，配合 Pydantic 模型进行输入验证：

```python
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("example_mcp")

# 定义 Pydantic 模型用于输入验证
class ServiceToolInput(BaseModel):
    '''服务工具操作的输入模型。'''
    model_config = ConfigDict(
        str_strip_whitespace=True,  # 自动去除字符串空白
        validate_assignment=True,    # 赋值时验证
        extra='forbid'              # 禁止额外字段
    )

    param1: str = Field(..., description="第一个参数描述（如 'user123'、'project-abc'）", min_length=1, max_length=100)
    param2: Optional[int] = Field(default=None, description="带约束的可选整数参数", ge=0, le=1000)
    tags: Optional[List[str]] = Field(default_factory=list, description="要应用的标签列表", max_items=10)

@mcp.tool(
    name="service_tool_name",
    annotations={
        "title": "Human-Readable Tool Title",
        "readOnlyHint": True,     # 工具不修改环境
        "destructiveHint": False,  # 工具不执行破坏性操作
        "idempotentHint": True,    # 重复调用无额外效果
        "openWorldHint": False     # 工具不与外部实体交互
    }
)
async def service_tool_name(params: ServiceToolInput) -> str:
    '''工具描述自动成为 'description' 字段。

    此工具对服务执行特定操作。它在处理前使用 ServiceToolInput
    Pydantic 模型验证所有输入。

    Args:
        params (ServiceToolInput): 已验证的输入参数，包含：
            - param1 (str): 第一个参数描述
            - param2 (Optional[int]): 带默认值的可选参数
            - tags (Optional[List[str]]): 标签列表

    Returns:
        str: 包含操作结果的 JSON 格式响应
    '''
    # 实现此处
    pass
```

## Pydantic v2 关键特性

- 使用 `model_config` 替代嵌套的 `Config` 类
- 使用 `field_validator` 替代已弃用的 `validator`
- 使用 `model_dump()` 替代已弃用的 `dict()`
- 验证器需要 `@classmethod` 装饰器
- 验证器方法需要类型提示

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict

class CreateUserInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    name: str = Field(..., description="用户全名", min_length=1, max_length=100)
    email: str = Field(..., description="用户邮箱地址", pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., description="用户年龄", ge=0, le=150)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Email cannot be empty")
        return v.lower()
```

## 响应格式选项

支持多种输出格式以提供灵活性：

```python
from enum import Enum

class ResponseFormat(str, Enum):
    '''工具响应的输出格式。'''
    MARKDOWN = "markdown"
    JSON = "json"

class UserSearchInput(BaseModel):
    query: str = Field(..., description="搜索查询")
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="输出格式：'markdown' 为人类可读，'json' 为机器可读"
    )
```

**Markdown 格式**：
- 使用标题、列表和格式化以增强清晰度
- 将时间戳转换为人类可读格式（如 "2024-01-15 10:30:00 UTC" 而非 epoch）
- 显示名称并在括号中附上 ID（如 "@john.doe (U123456)"）
- 省略冗长的元数据（如仅显示一个头像 URL，而非所有尺寸）
- 逻辑分组相关信息

**JSON 格式**：
- 返回适合程序化处理的完整结构化数据
- 包含所有可用字段和元数据
- 使用一致的字段名和类型

## 分页实现

用于列出资源的工具：

```python
class ListInput(BaseModel):
    limit: Optional[int] = Field(default=20, description="最大返回结果数", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="分页跳过的结果数", ge=0)

async def list_items(params: ListInput) -> str:
    # 带分页发起 API 请求
    data = await api_request(limit=params.limit, offset=params.offset)

    # 返回分页信息
    response = {
        "total": data["total"],
        "count": len(data["items"]),
        "offset": params.offset,
        "items": data["items"],
        "has_more": data["total"] > params.offset + len(data["items"]),
        "next_offset": params.offset + len(data["items"]) if data["total"] > params.offset + len(data["items"]) else None
    }
    return json.dumps(response, indent=2)
```

## 错误处理

提供清晰、可操作的错误消息：

```python
def _handle_api_error(e: Exception) -> str:
    '''所有工具的一致错误格式化。'''
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            return "Error: Resource not found. Please check the ID is correct."
        elif e.response.status_code == 403:
            return "Error: Permission denied. You don't have access to this resource."
        elif e.response.status_code == 429:
            return "Error: Rate limit exceeded. Please wait before making more requests."
        return f"Error: API request failed with status {e.response.status_code}"
    elif isinstance(e, httpx.TimeoutException):
        return "Error: Request timed out. Please try again."
    return f"Error: Unexpected error occurred: {type(e).__name__}"
```

## 共享工具

将通用功能提取为可复用函数：

```python
# 共享 API 请求函数
async def _make_api_request(endpoint: str, method: str = "GET", **kwargs) -> dict:
    '''所有 API 调用的可复用函数。'''
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{API_BASE_URL}/{endpoint}",
            timeout=30.0,
            **kwargs
        )
        response.raise_for_status()
        return response.json()
```

## Async/Await 最佳实践

网络请求和 I/O 操作始终使用 async/await：

```python
# 好的做法：异步网络请求
async def fetch_data(resource_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/resource/{resource_id}")
        response.raise_for_status()
        return response.json()

# 不好的做法：同步请求
def fetch_data(resource_id: str) -> dict:
    response = requests.get(f"{API_URL}/resource/{resource_id}")  # 阻塞
    return response.json()
```

## 类型提示

全程使用类型提示：

```python
from typing import Optional, List, Dict, Any

async def get_user(user_id: str) -> Dict[str, Any]:
    data = await fetch_user(user_id)
    return {"id": data["id"], "name": data["name"]}
```

## 工具文档字符串

每个工具必须有包含显式类型信息的全面文档字符串：

```python
async def search_users(params: UserSearchInput) -> str:
    '''
    在 Example 系统中按姓名、邮箱或团队搜索用户。

    此工具搜索 Example 平台中的所有用户资料，
    支持部分匹配和各种搜索过滤器。它不会
    创建或修改用户，仅搜索现有用户。

    Args:
        params (UserSearchInput): 已验证的输入参数，包含：
            - query (str): 用于匹配姓名/邮箱的搜索字符串（如 "john"、"@example.com"、"team:marketing"）
            - limit (Optional[int]): 最大返回结果数，1-100 之间（默认：20）
            - offset (Optional[int]): 分页跳过的结果数（默认：0）

    Returns:
        str: 包含搜索结果的 JSON 格式字符串，schema 如下：

        成功响应：
        {
            "total": int,           # 找到的匹配总数
            "count": int,           # 本次响应中的结果数
            "offset": int,          # 当前分页偏移
            "users": [
                {
                    "id": str,      # 用户 ID（如 "U123456789"）
                    "name": str,    # 全名（如 "John Doe"）
                    "email": str,   # 邮箱地址（如 "john@example.com"）
                    "team": str     # 团队名称（如 "Marketing"）- 可选
                }
            ]
        }

        错误响应：
        "Error: <error message>" 或 "No users found matching '<query>'"

    Examples:
        - 使用场景："查找所有营销团队成员" -> params 中 query="team:marketing"
        - 使用场景："搜索 John 的账户" -> params 中 query="john"
        - 不使用场景：需要创建用户（改用 example_create_user）
        - 不使用场景：有用户 ID 需要完整详情（改用 example_get_user）

    Error Handling:
        - 输入验证错误由 Pydantic 模型处理
        - 请求过多时返回 "Error: Rate limit exceeded"（429 状态）
        - API 密钥无效时返回 "Error: Invalid API authentication"（401 状态）
        - 返回格式化的结果列表或 "No users found matching 'query'"
    '''
```

## 完整示例

以下是一个完整的 Python MCP 服务器示例：

```python
#!/usr/bin/env python3
'''
Example Service 的 MCP 服务器。

此服务器提供与 Example API 交互的工具，包括用户搜索、
项目管理和数据导出功能。
'''

from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("example_mcp")

# 常量
API_BASE_URL = "https://api.example.com/v1"

# 枚举
class ResponseFormat(str, Enum):
    '''工具响应的输出格式。'''
    MARKDOWN = "markdown"
    JSON = "json"

# Pydantic 模型用于输入验证
class UserSearchInput(BaseModel):
    '''用户搜索操作的输入模型。'''
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    query: str = Field(..., description="用于匹配姓名/邮箱的搜索字符串", min_length=2, max_length=200)
    limit: Optional[int] = Field(default=20, description="最大返回结果数", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="分页跳过的结果数", ge=0)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="输出格式")

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty or whitespace only")
        return v.strip()

# 共享工具函数
async def _make_api_request(endpoint: str, method: str = "GET", **kwargs) -> dict:
    '''所有 API 调用的可复用函数。'''
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{API_BASE_URL}/{endpoint}",
            timeout=30.0,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

def _handle_api_error(e: Exception) -> str:
    '''所有工具的一致错误格式化。'''
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            return "Error: Resource not found. Please check the ID is correct."
        elif e.response.status_code == 403:
            return "Error: Permission denied. You don't have access to this resource."
        elif e.response.status_code == 429:
            return "Error: Rate limit exceeded. Please wait before making more requests."
        return f"Error: API request failed with status {e.response.status_code}"
    elif isinstance(e, httpx.TimeoutException):
        return "Error: Request timed out. Please try again."
    return f"Error: Unexpected error occurred: {type(e).__name__}"

# 工具定义
@mcp.tool(
    name="example_search_users",
    annotations={
        "title": "Search Example Users",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def example_search_users(params: UserSearchInput) -> str:
    '''在 Example 系统中按姓名、邮箱或团队搜索用户。

    [如上所示的完整文档字符串]
    '''
    try:
        # 使用已验证的参数发起 API 请求
        data = await _make_api_request(
            "users/search",
            params={
                "q": params.query,
                "limit": params.limit,
                "offset": params.offset
            }
        )

        users = data.get("users", [])
        total = data.get("total", 0)

        if not users:
            return f"No users found matching '{params.query}'"

        # 根据请求的格式格式化响应
        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [f"# User Search Results: '{params.query}'", ""]
            lines.append(f"Found {total} users (showing {len(users)})")
            lines.append("")

            for user in users:
                lines.append(f"## {user['name']} ({user['id']})")
                lines.append(f"- **Email**: {user['email']}")
                if user.get('team'):
                    lines.append(f"- **Team**: {user['team']}")
                lines.append("")

            return "\n".join(lines)

        else:
            # 机器可读的 JSON 格式
            import json
            response = {
                "total": total,
                "count": len(users),
                "offset": params.offset,
                "users": users
            }
            return json.dumps(response, indent=2)

    except Exception as e:
        return _handle_api_error(e)

if __name__ == "__main__":
    mcp.run()
```

---

## 高级 FastMCP 特性

### 上下文参数注入

FastMCP 可以自动将 `Context` 参数注入工具，用于日志记录、进度报告、资源读取和用户交互等高级功能：

```python
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("example_mcp")

@mcp.tool()
async def advanced_search(query: str, ctx: Context) -> str:
    '''带上下文访问的高级工具，用于日志和进度。'''

    # 为长时间操作报告进度
    await ctx.report_progress(0.25, "Starting search...")

    # 记录调试信息
    await ctx.log_info("Processing query", {"query": query, "timestamp": datetime.now()})

    # 执行搜索
    results = await search_api(query)
    await ctx.report_progress(0.75, "Formatting results...")

    # 访问服务器配置
    server_name = ctx.fastmcp.name

    return format_results(results)

@mcp.tool()
async def interactive_tool(resource_id: str, ctx: Context) -> str:
    '''可向用户请求额外输入的工具。'''

    # 需要时请求敏感信息
    api_key = await ctx.elicit(
        prompt="Please provide your API key:",
        input_type="password"
    )

    # 使用提供的密钥
    return await api_call(resource_id, api_key)
```

**上下文能力：**
- `ctx.report_progress(progress, message)` - 为长时间操作报告进度
- `ctx.log_info(message, data)` / `ctx.log_error()` / `ctx.log_debug()` - 日志记录
- `ctx.elicit(prompt, input_type)` - 向用户请求输入
- `ctx.fastmcp.name` - 访问服务器配置
- `ctx.read_resource(uri)` - 读取 MCP 资源

### 资源注册

将数据作为资源暴露，用于高效的基于模板的访问：

```python
@mcp.resource("file://documents/{name}")
async def get_document(name: str) -> str:
    '''将文档暴露为 MCP 资源。

    资源适用于不需要复杂参数的静态或半静态数据。
    它们使用 URI 模板进行灵活访问。
    '''
    document_path = f"./docs/{name}"
    with open(document_path, "r") as f:
        return f.read()

@mcp.resource("config://settings/{key}")
async def get_setting(key: str, ctx: Context) -> str:
    '''将配置暴露为带上下文的资源。'''
    settings = await load_settings()
    return json.dumps(settings.get(key, {}))
```

**何时使用资源 vs 工具：**
- **资源**：用于带简单参数的数据访问（URI 模板）
- **工具**：用于带验证和业务逻辑的复杂操作

### 结构化输出类型

FastMCP 支持字符串以外的多种返回类型：

```python
from typing import TypedDict
from dataclasses import dataclass
from pydantic import BaseModel

# TypedDict 用于结构化返回
class UserData(TypedDict):
    id: str
    name: str
    email: str

@mcp.tool()
async def get_user_typed(user_id: str) -> UserData:
    '''返回结构化数据 - FastMCP 处理序列化。'''
    return {"id": user_id, "name": "John Doe", "email": "john@example.com"}

# Pydantic 模型用于复杂验证
class DetailedUser(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    metadata: Dict[str, Any]

@mcp.tool()
async def get_user_detailed(user_id: str) -> DetailedUser:
    '''返回 Pydantic 模型 - 自动生成 schema。'''
    user = await fetch_user(user_id)
    return DetailedUser(**user)
```

### 生命周期管理

初始化跨请求持久化的资源：

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan():
    '''管理服务器生命周期内的资源。'''
    # 初始化连接、加载配置等
    db = await connect_to_database()
    config = load_configuration()

    # 使所有工具可用
    yield {"db": db, "config": config}

    # 关闭时清理
    await db.close()

mcp = FastMCP("example_mcp", lifespan=app_lifespan)

@mcp.tool()
async def query_data(query: str, ctx: Context) -> str:
    '''通过上下文访问生命周期资源。'''
    db = ctx.request_context.lifespan_state["db"]
    results = await db.query(query)
    return format_results(results)
```

### 传输选项

FastMCP 支持两种主要传输机制：

```python
# stdio 传输（用于本地工具）- 默认
if __name__ == "__main__":
    mcp.run()

# Streamable HTTP 传输（用于远程服务器）
if __name__ == "__main__":
    mcp.run(transport="streamable_http", port=8000)
```

**传输选择：**
- **stdio**：命令行工具、本地集成、子进程执行
- **Streamable HTTP**：Web 服务、远程访问、多客户端

---

## 代码最佳实践

### 代码组合性与可复用性

你的实现必须优先考虑组合性和代码复用：

1. **提取通用功能**：
   - 为跨多个工具使用的操作创建可复用的辅助函数
   - 构建共享的 API 客户端处理 HTTP 请求，而非重复代码
   - 将错误处理逻辑集中在工具函数中
   - 将业务逻辑提取到可组合的专用函数中
   - 提取共享的 Markdown 或 JSON 字段选择与格式化功能

2. **避免重复**：
   - 绝不在工具间复制粘贴相似代码
   - 如果发现自己两次编写相似逻辑，将其提取为函数
   - 分页、过滤、字段选择和格式化等通用操作应共享
   - 认证/授权逻辑应集中化

### Python 特定最佳实践

1. **使用类型提示**：始终为函数参数和返回值包含类型注解
2. **Pydantic 模型**：为所有输入验证定义清晰的 Pydantic 模型
3. **避免手动验证**：让 Pydantic 通过约束处理输入验证
4. **正确的导入**：分组导入（标准库、第三方、本地）
5. **错误处理**：使用特定的异常类型（httpx.HTTPStatusError，而非通用 Exception）
6. **异步上下文管理器**：对需要清理的资源使用 `async with`
7. **常量**：以 UPPER_CASE 定义模块级常量

## 质量检查清单

在完成 Python MCP 服务器实现之前，确保：

### 战略设计
- [ ] 工具支持完整工作流，而非仅仅是 API 端点包装器
- [ ] 工具名称反映自然的任务细分
- [ ] 响应格式优化智能体上下文效率
- [ ] 适当使用人类可读标识符
- [ ] 错误消息引导智能体正确使用

### 实现质量
- [ ] 聚焦实现：实现了最重要和最有价值的工具
- [ ] 所有工具有描述性名称和文档
- [ ] 相似操作的返回类型一致
- [ ] 所有外部调用实现了错误处理
- [ ] 服务器名称遵循格式：`{service}_mcp`
- [ ] 所有网络操作使用 async/await
- [ ] 通用功能已提取为可复用函数
- [ ] 错误消息清晰、可操作且具有教育意义
- [ ] 输出经过适当验证和格式化

### 工具配置
- [ ] 所有工具在装饰器中实现了 'name' 和 'annotations'
- [ ] 注解正确设置（readOnlyHint、destructiveHint、idempotentHint、openWorldHint）
- [ ] 所有工具使用 Pydantic BaseModel 进行输入验证，带 Field() 定义
- [ ] 所有 Pydantic Field 有显式类型和带约束的描述
- [ ] 所有工具有包含显式输入/输出类型的全面文档字符串
- [ ] 文档字符串包含 dict/JSON 返回的完整 schema 结构
- [ ] Pydantic 模型处理输入验证（无需手动验证）

### 高级特性（适用时）
- [ ] 上下文注入用于日志、进度或请求
- [ ] 为适当的数据端点注册了资源
- [ ] 为持久连接实现了生命周期管理
- [ ] 使用了结构化输出类型（TypedDict、Pydantic 模型）
- [ ] 配置了适当的传输（stdio 或 Streamable HTTP）

### 代码质量
- [ ] 文件包含正确的导入，包括 Pydantic 导入
- [ ] 适用的地方正确实现了分页
- [ ] 为可能较大的结果集提供了过滤选项
- [ ] 所有异步函数使用 `async def` 正确定义
- [ ] HTTP 客户端使用遵循带适当上下文管理器的异步模式
- [ ] 代码中全程使用类型提示
- [ ] 常量以 UPPER_CASE 定义在模块级别

### 测试
- [ ] 服务器成功运行：`python your_server.py --help`
- [ ] 所有导入正确解析
- [ ] 示例工具调用按预期工作
- [ ] 错误场景优雅处理
