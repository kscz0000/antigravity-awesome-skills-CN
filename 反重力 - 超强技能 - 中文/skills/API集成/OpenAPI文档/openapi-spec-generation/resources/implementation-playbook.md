# OpenAPI 规范生成实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

# OpenAPI 规范生成

用于创建、维护和验证 RESTful API 的 OpenAPI 3.1 规范的完整模式集合。

## 适用场景

- 从零创建 API 文档
- 从现有代码生成 OpenAPI 规范
- 设计 API 契约（设计优先方式）
- 根据规范验证 API 实现
- 从规范生成客户端 SDK
- 搭建 API 文档门户

## 核心概念

### 1. OpenAPI 3.1 结构

```yaml
openapi: 3.1.0
info:
  title: API 标题
  version: 1.0.0
servers:
  - url: https://api.example.com/v1
paths:
  /resources:
    get: ...
components:
  schemas: ...
  securitySchemes: ...
```

### 2. 设计方式

| 方式 | 描述 | 最适合 |
|----------|-------------|----------|
| **设计优先** | 先写规范再写代码 | 新 API、契约 |
| **代码优先** | 从代码生成规范 | 现有 API |
| **混合模式** | 给代码加注解，生成规范 | 演进中的 API |

## 模板

### 模板 1：完整 API 规范

```yaml
openapi: 3.1.0
info:
  title: 用户管理 API
  description: |
    用于管理用户及其个人资料的 API。

    ## 认证
    所有端点都需要 Bearer token 认证。

    ## 限流
    - 标准版每分钟 1000 次请求
    - 企业版每分钟 10000 次请求
  version: 2.0.0
  contact:
    name: API 支持
    email: api-support@example.com
    url: https://docs.example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v2
    description: 生产环境
  - url: https://staging-api.example.com/v2
    description: 预发环境
  - url: http://localhost:3000/v2
    description: 本地开发

tags:
  - name: Users
    description: 用户管理操作
  - name: Profiles
    description: 用户个人资料操作
  - name: Admin
    description: 管理操作

paths:
  /users:
    get:
      operationId: listUsers
      summary: 列出所有用户
      description: 返回分页的用户列表，支持可选过滤。
      tags:
        - Users
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
        - name: status
          in: query
          description: 按用户状态过滤
          schema:
            $ref: '#/components/schemas/UserStatus'
        - name: search
          in: query
          description: 按姓名或邮箱搜索
          schema:
            type: string
            minLength: 2
            maxLength: 100
      responses:
        '200':
          description: 成功响应
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
              examples:
                default:
                  $ref: '#/components/examples/UserListExample'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '429':
          $ref: '#/components/responses/RateLimited'
      security:
        - bearerAuth: []

    post:
      operationId: createUser
      summary: 创建新用户
      description: 创建新用户账户并发送欢迎邮件。
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
            examples:
              standard:
                summary: 普通用户
                value:
                  email: user@example.com
                  name: 张三
                  role: user
              admin:
                summary: 管理员用户
                value:
                  email: admin@example.com
                  name: 管理员
                  role: admin
      responses:
        '201':
          description: 用户创建成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
          headers:
            Location:
              description: 已创建用户的 URL
              schema:
                type: string
                format: uri
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: 邮箱已存在
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
      security:
        - bearerAuth: []

  /users/{userId}:
    parameters:
      - $ref: '#/components/parameters/UserIdParam'

    get:
      operationId: getUser
      summary: 按 ID 获取用户
      tags:
        - Users
      responses:
        '200':
          description: 成功响应
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - bearerAuth: []

    patch:
      operationId: updateUser
      summary: 更新用户
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: 用户已更新
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - bearerAuth: []

    delete:
      operationId: deleteUser
      summary: 删除用户
      tags:
        - Users
        - Admin
      responses:
        '204':
          description: 用户已删除
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - bearerAuth: []
        - apiKey: []

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
        - status
        - createdAt
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
          description: 唯一用户标识符
        email:
          type: string
          format: email
          description: 用户邮箱地址
        name:
          type: string
          minLength: 1
          maxLength: 100
          description: 用户显示名称
        status:
          $ref: '#/components/schemas/UserStatus'
        role:
          type: string
          enum: [user, moderator, admin]
          default: user
        avatar:
          type: string
          format: uri
          nullable: true
        metadata:
          type: object
          additionalProperties: true
          description: 自定义元数据
        createdAt:
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true

    UserStatus:
      type: string
      enum: [active, inactive, suspended, pending]
      description: 用户账户状态

    CreateUserRequest:
      type: object
      required:
        - email
        - name
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        role:
          type: string
          enum: [user, moderator, admin]
          default: user
        metadata:
          type: object
          additionalProperties: true

    UpdateUserRequest:
      type: object
      minProperties: 1
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        status:
          $ref: '#/components/schemas/UserStatus'
        role:
          type: string
          enum: [user, moderator, admin]
        metadata:
          type: object
          additionalProperties: true

    UserListResponse:
      type: object
      required:
        - data
        - pagination
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      required:
        - page
        - limit
        - total
        - totalPages
      properties:
        page:
          type: integer
          minimum: 1
        limit:
          type: integer
          minimum: 1
          maximum: 100
        total:
          type: integer
          minimum: 0
        totalPages:
          type: integer
          minimum: 0
        hasNext:
          type: boolean
        hasPrev:
          type: boolean

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: 用于程序化处理的错误码
        message:
          type: string
          description: 人类可读的错误消息
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
        requestId:
          type: string
          description: 用于支持排查的请求 ID

  parameters:
    UserIdParam:
      name: userId
      in: path
      required: true
      description: 用户 ID
      schema:
        type: string
        format: uuid

    PageParam:
      name: page
      in: query
      description: 页码（从 1 开始）
      schema:
        type: integer
        minimum: 1
        default: 1

    LimitParam:
      name: limit
      in: query
      description: 每页条数
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

  responses:
    BadRequest:
      description: 请求无效
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: VALIDATION_ERROR
            message: 请求参数无效
            details:
              - field: email
                message: 必须是有效的邮箱地址

    Unauthorized:
      description: 需要身份认证
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: UNAUTHORIZED
            message: 需要身份认证

    NotFound:
      description: 资源未找到
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: NOT_FOUND
            message: 用户未找到

    RateLimited:
      description: 请求过多
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
      headers:
        Retry-After:
          description: 限流重置前的等待秒数
          schema:
            type: integer
        X-RateLimit-Limit:
          description: 每个时间窗口的请求上限
          schema:
            type: integer
        X-RateLimit-Remaining:
          description: 时间窗口内剩余的请求数
          schema:
            type: integer

  examples:
    UserListExample:
      value:
        data:
          - id: "550e8400-e29b-41d4-a716-446655440000"
            email: "john@example.com"
            name: "John Doe"
            status: "active"
            role: "user"
            createdAt: "2024-01-15T10:30:00Z"
        pagination:
          page: 1
          limit: 20
          total: 1
          totalPages: 1
          hasNext: false
          hasPrev: false

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: 来自 /auth/login 的 JWT token

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: 用于服务间调用的 API key

security:
  - bearerAuth: []
```

### 模板 2：代码优先生成（Python/FastAPI）

```python
# FastAPI 自动生成 OpenAPI
from fastapi import FastAPI, HTTPException, Query, Path, Depends
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from enum import Enum

app = FastAPI(
    title="用户管理 API",
    description="用于管理用户和个人资料的 API",
    version="2.0.0",
    openapi_tags=[
        {"name": "Users", "description": "用户操作"},
        {"name": "Profiles", "description": "个人资料操作"},
    ],
    servers=[
        {"url": "https://api.example.com/v2", "description": "生产环境"},
        {"url": "http://localhost:8000", "description": "开发环境"},
    ],
)

# 枚举
class UserStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    suspended = "suspended"
    pending = "pending"

class UserRole(str, Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"

# 模型
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="用户邮箱地址")
    name: str = Field(..., min_length=1, max_length=100, description="显示名称")

class UserCreate(UserBase):
    role: UserRole = Field(default=UserRole.user)
    metadata: Optional[dict] = Field(default=None, description="自定义元数据")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "name": "John Doe",
                    "role": "user"
                }
            ]
        }
    }

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[UserStatus] = None
    role: Optional[UserRole] = None
    metadata: Optional[dict] = None

class User(UserBase):
    id: UUID = Field(..., description="唯一标识符")
    status: UserStatus
    role: UserRole
    avatar: Optional[str] = Field(None, description="头像 URL")
    metadata: Optional[dict] = None
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True}

class Pagination(BaseModel):
    page: int = Field(..., ge=1)
    limit: int = Field(..., ge=1, le=100)
    total: int = Field(..., ge=0)
    total_pages: int = Field(..., ge=0, alias="totalPages")
    has_next: bool = Field(..., alias="hasNext")
    has_prev: bool = Field(..., alias="hasPrev")

class UserListResponse(BaseModel):
    data: List[User]
    pagination: Pagination

class ErrorDetail(BaseModel):
    field: str
    message: str

class ErrorResponse(BaseModel):
    code: str = Field(..., description="错误码")
    message: str = Field(..., description="错误消息")
    details: Optional[List[ErrorDetail]] = None
    request_id: Optional[str] = Field(None, alias="requestId")

# 端点
@app.get(
    "/users",
    response_model=UserListResponse,
    tags=["Users"],
    summary="列出所有用户",
    description="返回分页的用户列表，支持可选过滤。",
    responses={
        400: {"model": ErrorResponse, "description": "请求无效"},
        401: {"model": ErrorResponse, "description": "未授权"},
    },
)
async def list_users(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页条数"),
    status: Optional[UserStatus] = Query(None, description="按状态过滤"),
    search: Optional[str] = Query(None, min_length=2, max_length=100),
):
    """
    分页列出用户并支持过滤。

    - **page**: 页码（从 1 开始）
    - **limit**: 每页条数（最多 100）
    - **status**: 按用户状态过滤
    - **search**: 按姓名或邮箱搜索
    """
    # 实现
    pass

@app.post(
    "/users",
    response_model=User,
    status_code=201,
    tags=["Users"],
    summary="创建新用户",
    responses={
        400: {"model": ErrorResponse},
        409: {"model": ErrorResponse, "description": "邮箱已存在"},
    },
)
async def create_user(user: UserCreate):
    """创建新用户并发送欢迎邮件。"""
    pass

@app.get(
    "/users/{user_id}",
    response_model=User,
    tags=["Users"],
    summary="按 ID 获取用户",
    responses={404: {"model": ErrorResponse}},
)
async def get_user(
    user_id: UUID = Path(..., description="用户 ID"),
):
    """根据 ID 获取特定用户。"""
    pass

@app.patch(
    "/users/{user_id}",
    response_model=User,
    tags=["Users"],
    summary="更新用户",
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def update_user(
    user_id: UUID = Path(..., description="用户 ID"),
    user: UserUpdate = ...,
):
    """更新用户属性。"""
    pass

@app.delete(
    "/users/{user_id}",
    status_code=204,
    tags=["Users", "Admin"],
    summary="删除用户",
    responses={404: {"model": ErrorResponse}},
)
async def delete_user(
    user_id: UUID = Path(..., description="用户 ID"),
):
    """永久删除一个用户。"""
    pass

# 导出 OpenAPI 规范
if __name__ == "__main__":
    import json
    print(json.dumps(app.openapi(), indent=2))
```

### 模板 3：代码优先（TypeScript/Express with tsoa）

```typescript
// tsoa 从 TypeScript 装饰器生成 OpenAPI

import {
  Controller,
  Get,
  Post,
  Patch,
  Delete,
  Route,
  Path,
  Query,
  Body,
  Response,
  SuccessResponse,
  Tags,
  Security,
  Example,
} from "tsoa";

// 模型
interface User {
  /** 唯一标识符 */
  id: string;
  /** 用户邮箱地址 */
  email: string;
  /** 显示名称 */
  name: string;
  status: UserStatus;
  role: UserRole;
  /** 头像 URL */
  avatar?: string;
  /** 自定义元数据 */
  metadata?: Record<string, unknown>;
  createdAt: Date;
  updatedAt?: Date;
}

enum UserStatus {
  Active = "active",
  Inactive = "inactive",
  Suspended = "suspended",
  Pending = "pending",
}

enum UserRole {
  User = "user",
  Moderator = "moderator",
  Admin = "admin",
}

interface CreateUserRequest {
  email: string;
  name: string;
  role?: UserRole;
  metadata?: Record<string, unknown>;
}

interface UpdateUserRequest {
  name?: string;
  status?: UserStatus;
  role?: UserRole;
  metadata?: Record<string, unknown>;
}

interface Pagination {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
  hasNext: boolean;
  hasPrev: boolean;
}

interface UserListResponse {
  data: User[];
  pagination: Pagination;
}

interface ErrorResponse {
  code: string;
  message: string;
  details?: { field: string; message: string }[];
  requestId?: string;
}

@Route("users")
@Tags("Users")
export class UsersController extends Controller {
  /**
   * 分页列出所有用户并支持过滤
   * @param page 页码（从 1 开始）
   * @param limit 每页条数（最多 100）
   * @param status 按用户状态过滤
   * @param search 按姓名或邮箱搜索
   */
  @Get()
  @Security("bearerAuth")
  @Response<ErrorResponse>(400, "请求无效")
  @Response<ErrorResponse>(401, "未授权")
  @Example<UserListResponse>({
    data: [
      {
        id: "550e8400-e29b-41d4-a716-446655440000",
        email: "john@example.com",
        name: "John Doe",
        status: UserStatus.Active,
        role: UserRole.User,
        createdAt: new Date("2024-01-15T10:30:00Z"),
      },
    ],
    pagination: {
      page: 1,
      limit: 20,
      total: 1,
      totalPages: 1,
      hasNext: false,
      hasPrev: false,
    },
  })
  public async listUsers(
    @Query() page: number = 1,
    @Query() limit: number = 20,
    @Query() status?: UserStatus,
    @Query() search?: string
  ): Promise<UserListResponse> {
    // 实现
    throw new Error("Not implemented");
  }

  /**
   * 创建新用户
   */
  @Post()
  @Security("bearerAuth")
  @SuccessResponse(201, "已创建")
  @Response<ErrorResponse>(400, "请求无效")
  @Response<ErrorResponse>(409, "邮箱已存在")
  public async createUser(
    @Body() body: CreateUserRequest
  ): Promise<User> {
    this.setStatus(201);
    throw new Error("Not implemented");
  }

  /**
   * 按 ID 获取用户
   * @param userId 用户 ID
   */
  @Get("{userId}")
  @Security("bearerAuth")
  @Response<ErrorResponse>(404, "用户未找到")
  public async getUser(
    @Path() userId: string
  ): Promise<User> {
    throw new Error("Not implemented");
  }

  /**
   * 更新用户属性
   * @param userId 用户 ID
   */
  @Patch("{userId}")
  @Security("bearerAuth")
  @Response<ErrorResponse>(400, "请求无效")
  @Response<ErrorResponse>(404, "用户未找到")
  public async updateUser(
    @Path() userId: string,
    @Body() body: UpdateUserRequest
  ): Promise<User> {
    throw new Error("Not implemented");
  }

  /**
   * 删除用户
   * @param userId 用户 ID
   */
  @Delete("{userId}")
  @Tags("Users", "Admin")
  @Security("bearerAuth")
  @SuccessResponse(204, "已删除")
  @Response<ErrorResponse>(404, "用户未找到")
  public async deleteUser(
    @Path() userId: string
  ): Promise<void> {
    this.setStatus(204);
  }
}
```

### 模板 4：验证与 Lint

```bash
# 安装验证工具
npm install -g @stoplight/spectral-cli
npm install -g @redocly/cli

# Spectral 规则集（.spectral.yaml）
cat > .spectral.yaml << 'EOF'
extends: ["spectral:oas", "spectral:asyncapi"]

rules:
  # 强制要求 operation ID
  operation-operationId: error

  # 要求提供描述
  operation-description: warn
  info-description: error

  # 命名规范
  operation-operationId-valid-in-url: true

  # 安全
  operation-security-defined: error

  # 响应码
  operation-success-response: error

  # 自定义规则
  path-params-snake-case:
    description: 路径参数应使用 snake_case
    severity: warn
    given: "$.paths[*].parameters[?(@.in == 'path')].name"
    then:
      function: pattern
      functionOptions:
        match: "^[a-z][a-z0-9_]*$"

  schema-properties-camelCase:
    description: Schema 属性应使用 camelCase
    severity: warn
    given: "$.components.schemas[*].properties[*]~"
    then:
      function: casing
      functionOptions:
        type: camel
EOF

# 运行 Spectral
spectral lint openapi.yaml

# Redocly 配置（redocly.yaml）
cat > redocly.yaml << 'EOF'
extends:
  - recommended

rules:
  no-invalid-media-type-examples: error
  no-invalid-schema-examples: error
  operation-4xx-response: warn
  request-mime-type:
    severity: error
    allowedValues:
      - application/json
  response-mime-type:
    severity: error
    allowedValues:
      - application/json
      - application/problem+json

theme:
  openapi:
    generateCodeSamples:
      languages:
        - lang: curl
        - lang: python
        - lang: javascript
EOF

# 运行 Redocly
redocly lint openapi.yaml
redocly bundle openapi.yaml -o bundled.yaml
redocly preview-docs openapi.yaml
```

## SDK 生成

```bash
# OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# 生成 TypeScript 客户端
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-fetch \
  -o ./generated/typescript-client \
  --additional-properties=supportsES6=true,npmName=@myorg/api-client

# 生成 Python 客户端
openapi-generator-cli generate \
  -i openapi.yaml \
  -g python \
  -o ./generated/python-client \
  --additional-properties=packageName=api_client

# 生成 Go 客户端
openapi-generator-cli generate \
  -i openapi.yaml \
  -g go \
  -o ./generated/go-client
```

## 最佳实践

### 推荐做法
- **使用 $ref** - 复用 schema、参数和响应
- **添加示例** - 真实值可帮助使用者理解
- **文档化错误** - 列出所有可能的错误码
- **对 API 进行版本管理** - 通过 URL 或 header
- **使用语义化版本** - 用于规范变更

### 不推荐做法
- **不要使用泛化描述** - 要具体
- **不要省略安全** - 定义所有方案
- **不要忘记 nullable** - 明确标注可空
- **不要混用风格** - 全程保持命名一致
- **不要硬编码 URL** - 使用 server 变量

## 资源

- [OpenAPI 3.1 规范](https://spec.openapis.org/oas/v3.1.0)
- [Swagger Editor](https://editor.swagger.io/)
- [Redocly](https://redocly.com/)
- [Spectral](https://stoplight.io/open-source/spectral)
