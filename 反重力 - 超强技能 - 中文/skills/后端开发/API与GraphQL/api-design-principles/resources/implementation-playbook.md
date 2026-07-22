# API 设计原则实现手册

本文件包含技能引用的详细模式、检查清单和代码示例。

## 核心概念

### 1. RESTful 设计原则

**面向资源的架构**

- 资源是名词（users、orders、products），而非动词
- 使用 HTTP 方法表示动作（GET、POST、PUT、PATCH、DELETE）
- URL 表示资源层级
- 统一的命名约定

**HTTP 方法语义：**

- `GET`：获取资源（幂等、安全）
- `POST`：创建新资源
- `PUT`：替换整个资源（幂等）
- `PATCH`：部分更新资源
- `DELETE`：删除资源（幂等）

### 2. GraphQL 设计原则

**Schema 优先开发**

- 类型定义领域模型
- Query 用于读取数据
- Mutation 用于修改数据
- Subscription 用于实时更新

**查询结构：**

- 客户端精确请求所需数据
- 单一端点，多个操作
- 强类型 Schema
- 内置内省功能

### 3. API 版本控制策略

**URL 版本控制：**

```
/api/v1/users
/api/v2/users
```

**请求头版本控制：**

```
Accept: application/vnd.api+json; version=1
```

**查询参数版本控制：**

```
/api/users?version=1
```

## REST API 设计模式

### 模式 1：资源集合设计

```python
# 好的做法：面向资源的端点
GET    /api/users              # 列出用户（带分页）
POST   /api/users              # 创建用户
GET    /api/users/{id}         # 获取特定用户
PUT    /api/users/{id}         # 替换用户
PATCH  /api/users/{id}         # 更新用户字段
DELETE /api/users/{id}         # 删除用户

# 嵌套资源
GET    /api/users/{id}/orders  # 获取用户的订单
POST   /api/users/{id}/orders  # 为用户创建订单

# 不好的做法：面向动作的端点（避免）
POST   /api/createUser
POST   /api/getUserById
POST   /api/deleteUser
```

### 模式 2：分页与过滤

```python
from typing import List, Optional
from pydantic import BaseModel, Field

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页条数")

class FilterParams(BaseModel):
    status: Optional[str] = None
    created_after: Optional[str] = None
    search: Optional[str] = None

class PaginatedResponse(BaseModel):
    items: List[dict]
    total: int
    page: int
    page_size: int
    pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1

# FastAPI 端点示例
from fastapi import FastAPI, Query, Depends

app = FastAPI()

@app.get("/api/users", response_model=PaginatedResponse)
async def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    # 应用过滤条件
    query = build_query(status=status, search=search)

    # 计算总数
    total = await count_users(query)

    # 获取当前页
    offset = (page - 1) * page_size
    users = await fetch_users(query, limit=page_size, offset=offset)

    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size
    )
```

### 模式 3：错误处理与状态码

```python
from fastapi import HTTPException, status
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = None
    timestamp: str
    path: str

class ValidationErrorDetail(BaseModel):
    field: str
    message: str
    value: Any

# 统一的错误响应
STATUS_CODES = {
    "success": 200,
    "created": 201,
    "no_content": 204,
    "bad_request": 400,
    "unauthorized": 401,
    "forbidden": 403,
    "not_found": 404,
    "conflict": 409,
    "unprocessable": 422,
    "internal_error": 500
}

def raise_not_found(resource: str, id: str):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": "NotFound",
            "message": f"{resource} 未找到",
            "details": {"id": id}
        }
    )

def raise_validation_error(errors: List[ValidationErrorDetail]):
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail={
            "error": "ValidationError",
            "message": "请求验证失败",
            "details": {"errors": [e.dict() for e in errors]}
        }
    )

# 使用示例
@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    user = await fetch_user(user_id)
    if not user:
        raise_not_found("用户", user_id)
    return user
```

### 模式 4：HATEOAS（超媒体作为应用状态引擎）

```python
class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    _links: dict

    @classmethod
    def from_user(cls, user: User, base_url: str):
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            _links={
                "self": {"href": f"{base_url}/api/users/{user.id}"},
                "orders": {"href": f"{base_url}/api/users/{user.id}/orders"},
                "update": {
                    "href": f"{base_url}/api/users/{user.id}",
                    "method": "PATCH"
                },
                "delete": {
                    "href": f"{base_url}/api/users/{user.id}",
                    "method": "DELETE"
                }
            }
        )
```

## GraphQL 设计模式

### 模式 1：Schema 设计

```graphql
# schema.graphql

# 清晰的类型定义
type User {
  id: ID!
  email: String!
  name: String!
  createdAt: DateTime!

  # 关系
  orders(first: Int = 20, after: String, status: OrderStatus): OrderConnection!

  profile: UserProfile
}

type Order {
  id: ID!
  status: OrderStatus!
  total: Money!
  items: [OrderItem!]!
  createdAt: DateTime!

  # 反向引用
  user: User!
}

# 分页模式（Relay 风格）
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# 类型安全的枚举
enum OrderStatus {
  PENDING
  CONFIRMED
  SHIPPED
  DELIVERED
  CANCELLED
}

# 自定义标量
scalar DateTime
scalar Money

# Query 根类型
type Query {
  user(id: ID!): User
  users(first: Int = 20, after: String, search: String): UserConnection!

  order(id: ID!): Order
}

# Mutation 根类型
type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!

  createOrder(input: CreateOrderInput!): CreateOrderPayload!
}

# 变更的输入类型
input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

# 变更的 Payload 类型
type CreateUserPayload {
  user: User
  errors: [Error!]
}

type Error {
  field: String
  message: String!
}
```

### 模式 2：Resolver 设计

```python
from typing import Optional, List
from ariadne import QueryType, MutationType, ObjectType
from dataclasses import dataclass

query = QueryType()
mutation = MutationType()
user_type = ObjectType("User")

@query.field("user")
async def resolve_user(obj, info, id: str) -> Optional[dict]:
    """根据 ID 解析单个用户。"""
    return await fetch_user_by_id(id)

@query.field("users")
async def resolve_users(
    obj,
    info,
    first: int = 20,
    after: Optional[str] = None,
    search: Optional[str] = None
) -> dict:
    """解析分页用户列表。"""
    # 解码游标
    offset = decode_cursor(after) if after else 0

    # 获取用户
    users = await fetch_users(
        limit=first + 1,  # 多获取一个以检查 hasNextPage
        offset=offset,
        search=search
    )

    # 分页处理
    has_next = len(users) > first
    if has_next:
        users = users[:first]

    edges = [
        {
            "node": user,
            "cursor": encode_cursor(offset + i)
        }
        for i, user in enumerate(users)
    ]

    return {
        "edges": edges,
        "pageInfo": {
            "hasNextPage": has_next,
            "hasPreviousPage": offset > 0,
            "startCursor": edges[0]["cursor"] if edges else None,
            "endCursor": edges[-1]["cursor"] if edges else None
        },
        "totalCount": await count_users(search=search)
    }

@user_type.field("orders")
async def resolve_user_orders(user: dict, info, first: int = 20) -> dict:
    """解析用户的订单（使用 DataLoader 防止 N+1）。"""
    # 使用 DataLoader 批量请求
    loader = info.context["loaders"]["orders_by_user"]
    orders = await loader.load(user["id"])

    return paginate_orders(orders, first)

@mutation.field("createUser")
async def resolve_create_user(obj, info, input: dict) -> dict:
    """创建新用户。"""
    try:
        # 验证输入
        validate_user_input(input)

        # 创建用户
        user = await create_user(
            email=input["email"],
            name=input["name"],
            password=hash_password(input["password"])
        )

        return {
            "user": user,
            "errors": []
        }
    except ValidationError as e:
        return {
            "user": None,
            "errors": [{"field": e.field, "message": e.message}]
        }
```

### 模式 3：DataLoader（N+1 问题预防）

```python
from aiodataloader import DataLoader
from typing import List, Optional

class UserLoader(DataLoader):
    """按 ID 批量加载用户。"""

    async def batch_load_fn(self, user_ids: List[str]) -> List[Optional[dict]]:
        """单次查询加载多个用户。"""
        users = await fetch_users_by_ids(user_ids)

        # 按输入顺序映射结果
        user_map = {user["id"]: user for user in users}
        return [user_map.get(user_id) for user_id in user_ids]

class OrdersByUserLoader(DataLoader):
    """按用户 ID 批量加载订单。"""

    async def batch_load_fn(self, user_ids: List[str]) -> List[List[dict]]:
        """单次查询加载多个用户的订单。"""
        orders = await fetch_orders_by_user_ids(user_ids)

        # 按用户 ID 分组
        orders_by_user = {}
        for order in orders:
            user_id = order["user_id"]
            if user_id not in orders_by_user:
                orders_by_user[user_id] = []
            orders_by_user[user_id].append(order)

        # 按输入顺序返回
        return [orders_by_user.get(user_id, []) for user_id in user_ids]

# 上下文设置
def create_context():
    return {
        "loaders": {
            "user": UserLoader(),
            "orders_by_user": OrdersByUserLoader()
        }
    }
```

## 最佳实践

### REST API

1. **命名一致**：集合使用复数名词（`/users`，而非 `/user`）
2. **无状态**：每个请求包含所有必要信息
3. **正确使用 HTTP 状态码**：2xx 成功，4xx 客户端错误，5xx 服务器错误
4. **版本控制**：从第一天起就为破坏性变更做准备
5. **分页**：始终对大型集合进行分页
6. **速率限制**：用速率限制保护 API
7. **文档**：使用 OpenAPI/Swagger 提供交互式文档

### GraphQL API

1. **Schema 优先**：在编写 resolver 前先设计 schema
2. **避免 N+1**：使用 DataLoader 高效获取数据
3. **输入验证**：在 schema 和 resolver 层面都要验证
4. **错误处理**：在 mutation payload 中返回结构化错误
5. **分页**：使用游标分页（Relay 规范）
6. **弃用**：使用 `@deprecated` 指令进行渐进式迁移
7. **监控**：追踪查询复杂度和执行时间

## 常见陷阱

- **过度获取/获取不足（REST）**：GraphQL 解决了这个问题，但需要 DataLoader
- **破坏性变更**：对 API 进行版本控制或使用弃用策略
- **错误格式不一致**：标准化错误响应
- **缺少速率限制**：没有限制的 API 容易被滥用
- **文档缺失**：无文档的 API 会让开发者沮丧
- **忽略 HTTP 语义**：对幂等操作使用 POST 会破坏预期
- **紧耦合**：API 结构不应镜像数据库 schema

## 资源

- **references/rest-best-practices.md**：全面的 REST API 设计指南
- **references/graphql-schema-design.md**：GraphQL schema 模式与反模式
- **references/api-versioning-strategies.md**：版本控制方法与迁移路径
- **assets/rest-api-template.py**：FastAPI REST API 模板
- **assets/graphql-schema-template.graphql**：完整的 GraphQL schema 示例
- **assets/api-design-checklist.md**：实现前审查检查清单
- **scripts/openapi-generator.py**：从代码生成 OpenAPI 规范
