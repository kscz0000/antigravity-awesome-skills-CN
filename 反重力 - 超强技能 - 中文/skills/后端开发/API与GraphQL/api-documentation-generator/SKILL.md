---
name: api-documentation-generator
description: "从代码生成全面、开发者友好的 API 文档，包括端点、参数、示例和最佳实践。触发词：API文档、API文档生成、接口文档、端点文档、OpenAPI、Swagger、REST API文档、GraphQL文档、API说明"
risk: unknown
source: community
date_added: "2026-02-27"
---

# API 文档生成器

## 概述

从代码库自动生成清晰、全面的 API 文档。此技能帮助您创建专业的文档，包括端点描述、请求/响应示例、认证详情、错误处理和使用指南。

适用于 REST API、GraphQL API 和 WebSocket API。

## 何时使用此技能

- 需要为新 API 编写文档时
- 更新现有 API 文档时
- API 缺乏清晰文档时
- 帮助新开发者上手 API 时
- 为外部用户准备 API 文档时
- 创建 OpenAPI/Swagger 规范时

## 工作原理

### 步骤 1：分析 API 结构

首先，我会检查您的 API 代码库以了解：
- 可用的端点和路由
- HTTP 方法（GET、POST、PUT、DELETE 等）
- 请求参数和请求体结构
- 响应格式和状态码
- 认证和授权要求
- 错误处理模式

### 步骤 2：生成端点文档

为每个端点创建文档，包括：

**端点详情：**
- HTTP 方法和 URL 路径
- 功能简要描述
- 认证要求
- 速率限制信息（如适用）

**请求规范：**
- 路径参数
- 查询参数
- 请求头
- 请求体模式（包含类型和验证规则）

**响应规范：**
- 成功响应（状态码 + 响应体结构）
- 错误响应（所有可能的错误码）
- 响应头

**代码示例：**
- cURL 命令
- JavaScript/TypeScript（fetch/axios）
- Python（requests）
- 其他语言（按需）

### 步骤 3：添加使用指南

我会包含：
- 快速入门指南
- 认证设置
- 常见用例
- 最佳实践
- 速率限制详情
- 分页模式
- 过滤和排序选项

### 步骤 4：记录错误处理

清晰的错误文档包括：
- 所有可能的错误码
- 错误消息格式
- 故障排除指南
- 常见错误场景和解决方案

### 步骤 5：创建交互式示例

在可能的情况下，我会提供：
- Postman 集合
- OpenAPI/Swagger 规范
- 交互式代码示例
- 示例响应

## 示例

### 示例 1：REST API 端点文档

```markdown
## 创建用户

创建一个新的用户账户。

**端点：** `POST /api/v1/users`

**认证：** 必需（Bearer token）

**请求体：**
\`\`\`json
{
  "email": "user@example.com",      // 必需：有效的邮箱地址
  "password": "SecurePass123!",     // 必需：最少8个字符，1个大写字母，1个数字
  "name": "John Doe",               // 必需：2-50个字符
  "role": "user"                    // 可选："user" 或 "admin"（默认："user"）
}
\`\`\`

**成功响应（201 Created）：**
\`\`\`json
{
  "id": "usr_1234567890",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "createdAt": "2026-01-20T10:30:00Z",
  "emailVerified": false
}
\`\`\`

**错误响应：**

- `400 Bad Request` - 输入数据无效
  \`\`\`json
  {
    "error": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "field": "email"
  }
  \`\`\`

- `409 Conflict` - 邮箱已存在
  \`\`\`json
  {
    "error": "EMAIL_EXISTS",
    "message": "An account with this email already exists"
  }
  \`\`\`

- `401 Unauthorized` - 缺少或无效的认证令牌

**示例请求（cURL）：**
\`\`\`bash
curl -X POST https://api.example.com/api/v1/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "name": "John Doe"
  }'
\`\`\`

**示例请求（JavaScript）：**
\`\`\`javascript
const response = await fetch('https://api.example.com/api/v1/users', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123!',
    name: 'John Doe'
  })
});

const user = await response.json();
console.log(user);
\`\`\`

**示例请求（Python）：**
\`\`\`python
import requests

response = requests.post(
    'https://api.example.com/api/v1/users',
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    json={
        'email': 'user@example.com',
        'password': 'SecurePass123!',
        'name': 'John Doe'
    }
)

user = response.json()
print(user)
\`\`\`
```

### 示例 2：GraphQL API 文档

```markdown
## 用户查询

通过 ID 获取用户信息。

**查询：**
\`\`\`graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    email
    name
    role
    createdAt
    posts {
      id
      title
      publishedAt
    }
  }
}
\`\`\`

**变量：**
\`\`\`json
{
  "id": "usr_1234567890"
}
\`\`\`

**响应：**
\`\`\`json
{
  "data": {
    "user": {
      "id": "usr_1234567890",
      "email": "user@example.com",
      "name": "John Doe",
      "role": "user",
      "createdAt": "2026-01-20T10:30:00Z",
      "posts": [
        {
          "id": "post_123",
          "title": "My First Post",
          "publishedAt": "2026-01-21T14:00:00Z"
        }
      ]
    }
  }
}
\`\`\`

**错误：**
\`\`\`json
{
  "errors": [
    {
      "message": "User not found",
      "extensions": {
        "code": "USER_NOT_FOUND",
        "userId": "usr_1234567890"
      }
    }
  ]
}
\`\`\`
```

### 示例 3：认证文档

```markdown
## 认证

所有 API 请求需要使用 Bearer 令牌进行认证。

### 获取令牌

**端点：** `POST /api/v1/auth/login`

**请求：**
\`\`\`json
{
  "email": "user@example.com",
  "password": "your-password"
}
\`\`\`

**响应：**
\`\`\`json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": 3600,
  "refreshToken": "refresh_token_here"
}
\`\`\`

### 使用令牌

在 Authorization 头中包含令牌：

\`\`\`
Authorization: Bearer YOUR_TOKEN
\`\`\`

### 令牌过期

令牌在 1 小时后过期。使用刷新令牌获取新的访问令牌：

**端点：** `POST /api/v1/auth/refresh`

**请求：**
\`\`\`json
{
  "refreshToken": "refresh_token_here"
}
\`\`\`
```

## 最佳实践

### ✅ 应该这样做

- **保持一致性** - 对所有端点使用相同的格式
- **包含示例** - 提供多种语言的可运行代码示例
- **记录错误** - 列出所有可能的错误码及其含义
- **展示真实数据** - 使用真实的示例数据，而非 "foo" 和 "bar"
- **解释参数** - 描述每个参数的作用及其约束
- **版本化 API** - 在 URL 中包含版本号（/api/v1/）
- **添加时间戳** - 显示文档最后更新时间
- **链接相关端点** - 帮助用户发现相关功能
- **包含速率限制** - 记录任何速率限制策略
- **提供 Postman 集合** - 便于测试您的 API

### ❌ 不应该这样做

- **不要跳过错误情况** - 用户需要知道可能出现的问题
- **不要使用模糊描述** - "获取数据" 这样的描述没有帮助
- **不要忘记认证** - 始终记录认证要求
- **不要忽略边界情况** - 记录分页、过滤、排序
- **不要留下损坏的示例** - 测试所有代码示例
- **不要使用过时信息** - 保持文档与代码同步
- **不要过度复杂化** - 保持简单且易于浏览
- **不要忘记响应头** - 记录重要的响应头

## 文档结构

### 推荐章节

1. **简介**
   - API 的功能
   - 基础 URL
   - API 版本
   - 支持联系方式

2. **认证**
   - 如何认证
   - 令牌管理
   - 安全最佳实践

3. **快速入门**
   - 简单示例帮助开始
   - 常见用例演示

4. **端点**
   - 按资源组织
   - 每个端点的完整详情

5. **数据模型**
   - 模式定义
   - 字段描述
   - 验证规则

6. **错误处理**
   - 错误码参考
   - 错误响应格式
   - 故障排除指南

7. **速率限制**
   - 限制和配额
   - 需要检查的响应头
   - 处理速率限制错误

8. **更新日志**
   - API 版本历史
   - 破坏性变更
   - 废弃通知

9. **SDK 和工具**
   - 官方客户端库
   - Postman 集合
   - OpenAPI 规范

## 常见问题

### 问题：文档与代码不同步
**症状：** 示例无法运行、参数错误、端点返回不同数据
**解决方案：**
- 从代码注释/注解生成文档
- 使用 Swagger/OpenAPI 等工具
- 添加验证文档的 API 测试
- 每次 API 变更时审查文档

### 问题：缺少错误文档
**症状：** 用户不知道如何处理错误，支持工单增加
**解决方案：**
- 记录每个可能的错误码
- 提供清晰的错误消息
- 包含故障排除步骤
- 展示示例错误响应

### 问题：示例无法运行
**症状：** 用户无法开始使用，挫败感增加
**解决方案：**
- 测试每个代码示例
- 使用真实可用的端点
- 包含完整示例（而非片段）
- 提供沙盒环境

### 问题：参数要求不清晰
**症状：** 用户发送无效请求，验证错误
**解决方案：**
- 清晰标记必需与可选参数
- 记录数据类型和格式
- 展示验证规则
- 提供示例值

## 工具和格式

### OpenAPI/Swagger
生成交互式文档：
```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
paths:
  /users:
    post:
      summary: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
```

### Postman 集合
导出集合便于测试：
```json
{
  "info": {
    "name": "My API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create User",
      "request": {
        "method": "POST",
        "url": "{{baseUrl}}/api/v1/users"
      }
    }
  ]
}
```

## 相关技能

- `@doc-coauthoring` - 用于协作编写文档
- `@copywriting` - 用于清晰、用户友好的描述
- `@test-driven-development` - 确保 API 行为与文档匹配
- `@systematic-debugging` - 用于排查 API 问题

## 其他资源

- [OpenAPI Specification](https://swagger.io/specification/)
- [REST API Best Practices](https://restfulapi.net/)
- [GraphQL Documentation](https://graphql.org/learn/)
- [API Design Patterns](https://www.apiguide.com/)
- [Postman Documentation](https://learning.postman.com/docs/)

---

**专业提示：** 让 API 文档尽可能接近代码。使用从代码注释生成文档的工具，确保它们保持同步！

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
