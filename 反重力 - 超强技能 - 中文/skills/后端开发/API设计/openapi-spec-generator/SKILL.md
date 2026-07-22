---
name: openapi-spec-generator
description: 从自然语言描述、代码或部分规范生成完整的生产级 OpenAPI 3.x 和 Swagger 2.0 规范文档。当用户提及 OpenAPI、Swagger、API 规范、REST API 文档、YAML/JSON API 模式、端点文档、API 文档生成、接口定义、OpenAPI 规范编写时使用此技能。
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/api-skill/openapi-spec-generator
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# OpenAPI / Swagger 规范生成器

## 使用场景

当需要从自然语言描述、代码或部分规范生成完整、生产级 OpenAPI 3.x 和 Swagger 2.0 规范时使用此技能。当用户提及 OpenAPI、Swagger、API 规范、REST API 文档、YAML/JSON API 模式、端点文档、API 文档生成、接口定义、OpenAPI 规范编写时触发此技能。

从描述、代码或部分规范生成完整且有效的 OpenAPI 3.x 或 Swagger 2.0 规范。

## 工作流程

### 第一步 — 收集上下文

在编写任何 YAML/JSON 之前，先询问（或从上下文推断）以下信息：

| 问题 | 为什么重要 |
|---|---|
| OpenAPI 3.x 还是 Swagger 2.0？ | `info`、`servers`/`host`、`components`/`definitions` 的结构不同 |
| 输出格式：YAML 还是 JSON？ | 默认 YAML，除非用户指定 JSON |
| 这个 API 做什么？ | 决定 `info.title`、`info.description`、tags |
| 端点列表（或要从中提取的代码）？ | 核心路径对象 |
| 认证类型有哪些？ | `securitySchemes` — 详见参考文件 |
| 是否有通用数据模型或实体？ | `components/schemas` / `definitions` |
| 是否有现有部分规范需要扩展？ | 合并而非覆盖 |

如果用户提供了代码（Express 路由、FastAPI、Django URL、Spring 控制器等），**自动提取端点**——不要重复问用户已经告诉你的内容。

### 第二步 — 构建规范

遵循所选版本的结构指南。始终输出**完整且有效的规范**——不要留下类似 `# TODO: add schema` 的占位注释。

#### OpenAPI 3.x 骨架模板

```yaml
openapi: "3.1.0"
info:
  title: <API Title>
  version: "1.0.0"
  description: <Short description>
  contact:
    name: <Team or Author>
    email: <contact@example.com>
servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging
tags:
  - name: <Tag>
    description: <Tag description>
paths:
  /resource:
    get:
      summary: List resources
      operationId: listResources
      tags: [<Tag>]
      parameters: []
      responses:
        "200":
          description: Success
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ResourceList"
              example:
                items: []
                total: 0
        "401":
          $ref: "#/components/responses/Unauthorized"
        "500":
          $ref: "#/components/responses/InternalError"
      security:
        - BearerAuth: []
components:
  schemas: {}
  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
    InternalError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: "#/components/schemas/Error"
  securitySchemes: {}
```

#### Swagger 2.0 骨架模板

```yaml
swagger: "2.0"
info:
  title: <API Title>
  version: "1.0.0"
  description: <Short description>
host: api.example.com
basePath: /v1
schemes: [https]
consumes: [application/json]
produces: [application/json]
tags: []
paths: {}
definitions: {}
securityDefinitions: {}
```

### 第三步 — Schema 与模型

- **始终使用 `$ref`** 引用在多处使用的 schema。
- 每个 schema 和响应体都要包含 `example` 或 `examples`。
- 使用 `required` 数组标记必填字段。
- 可空可选字段使用 `nullable: true`（OAS 3.0）或 `x-nullable: true`（Swagger 2.0）。
- 优先使用 `format` 关键字：`int32`、`int64`、`float`、`date`、`date-time`、`uuid`、`email`、`uri`、`byte`、`binary`。

**常用 Schema 模式：**

```yaml
# Pagination wrapper
PagedResult:
  type: object
  required: [items, total, page, pageSize]
  properties:
    items:
      type: array
      items:
        $ref: "#/components/schemas/Resource"
    total:
      type: integer
      format: int64
      example: 100
    page:
      type: integer
      format: int32
      example: 1
    pageSize:
      type: integer
      format: int32
      example: 20

# Standard error
Error:
  type: object
  required: [code, message]
  properties:
    code:
      type: string
      example: RESOURCE_NOT_FOUND
    message:
      type: string
      example: The requested resource was not found.
    details:
      type: object
      additionalProperties: true

# Timestamps mixin (use allOf)
Timestamps:
  type: object
  properties:
    createdAt:
      type: string
      format: date-time
    updatedAt:
      type: string
      format: date-time
```

### 第四步 — 安全认证方案

详细模式请参阅 `reference/security-schemes.md`。快速参考：

| 方案 | OAS 3.x 类型 | 说明 |
|---|---|---|
| Bearer JWT | `http`, scheme `bearer` | REST API 最常用方式 |
| API Key（请求头） | `apiKey`, in `header` | 如 `X-API-Key` |
| API Key（查询参数） | `apiKey`, in `query` | 不推荐——会泄露到日志中 |
| OAuth 2 | `oauth2` | 使用 `flows` 定义授权类型 |
| Basic Auth | `http`, scheme `basic` | 仅限 HTTPS |
| OpenID Connect | `openIdConnect` | 提供 `openIdConnectUrl` |

在根级别**全局应用**安全配置，仅在需要覆盖的特定操作上**逐操作覆盖**（如公开端点使用 `security: []`）。

### 第五步 — 参数定义

**路径参数**——始终设为 `required: true`：
```yaml
parameters:
  - name: userId
    in: path
    required: true
    schema:
      type: string
      format: uuid
    example: 123e4567-e89b-12d3-a456-426614174000
```

**查询参数**——记录默认值和枚举值：
```yaml
  - name: status
    in: query
    schema:
      type: string
      enum: [active, inactive, pending]
      default: active
```

**请求头**——将 `X-Request-ID`、correlation ID 等作为通用参数定义在 `components/parameters` 下。

### 第六步 — 响应状态码

至少包含以下状态码：

| 状态码 | 使用场景 |
|---|---|
| `200` | 成功的 GET、PUT、PATCH 操作 |
| `201` | 成功创建资源的 POST 操作 |
| `204` | 成功的 DELETE 操作（无响应体） |
| `400` | 校验失败 / 请求错误 |
| `401` | 缺少或无效的身份认证 |
| `403` | 已认证但无权限 |
| `404` | 资源未找到 |
| `409` | 冲突（重复、状态不一致） |
| `422` | 无法处理的实体（语义错误） |
| `429` | 请求频率受限 |
| `500` | 内部服务器错误 |

对 `401`、`403`、`404`、`429`、`500` 使用 `$ref` 引用 `components/responses` 以避免重复。

### 第七步 — 质量检查清单

交付规范前，逐一确认：

- [ ] `openapi` 或 `swagger` 版本字段已填写
- [ ] 每个路径至少有一个操作
- [ ] 每个操作都有 `operationId`（驼峰命名，唯一）
- [ ] 每个操作至少有 `200`/`201`/`204` 响应
- [ ] 所有操作都定义了 `4xx` 和 `5xx` 响应
- [ ] 所有 `$ref` 目标都存在于 `components/` 或 `definitions/`
- [ ] 所有的请求/响应体必填字段已列在 `required` 数组中
- [ ] 安全方案已定义并已应用
- [ ] 每个 schema 或响应体至少有一个 `example`
- [ ] 根级别 tags 已定义并与操作的 tags 匹配
- [ ] 无孤立的 schema（`components/schemas` 中所有项均被引用）

### 第八步 — 输出交付

1. 在标注为 `yaml` 或 `json` 的代码块中输出完整的 YAML（或 JSON）规范。
2. 在规范之后提供生成的端点**摘要表**。
3. 提供以下选项：
   - 导出为 `.yaml` / `.json` 文件
   - 使用 Spectral 或 swagger-parser 进行校验
   - 生成 mock 服务配置（Prism）
   - 生成客户端 SDK 存根（自选语言）

---

## 从代码提取

当用户提供了源代码时，按框架分别提取：

**Express / Koa / Fastify（Node.js）**
- 查找 `.get()`、`.post()`、`.put()`、`.patch()`、`.delete()` 调用
- 路由参数 `:param` → 路径参数 `{param}`
- 中间件如 `authenticate` → 标记安全需求
- `req.body`、`req.query`、`req.params` 的使用 → 推断请求 schema

**FastAPI / Flask（Python）**
- 装饰器：`@app.get()`、`@router.post()` 等
- Pydantic 模型 → 直接转换为 JSON Schema
- `Query()`、`Path()`、`Body()` → 映射为对应位置的参数

**Spring Boot（Java）**
- `@GetMapping`、`@PostMapping` 等
- `@PathVariable`、`@RequestParam`、`@RequestBody`
- DTO 类 → schema

**Django REST Framework**
- `ViewSet` 和 `Router` → CRUD 端点
- `Serializer` 字段 → schema 属性

**Rails**
- `routes.rb` 资源路由 → 标准 REST 端点
- Strong params → 请求体 schema

---

## 参考文件

- `reference/security-schemes.md` — 所有认证类型的详细安全方案示例
- `reference/common-patterns.md` — 分页、HATEOAS、problem+json、webhook、文件上传模式

当用户询问特定模式或需要生成复杂的认证/分页方案时，请阅读这些参考文件。

---

## 完成 OpenAPI/Swagger 规范设计后

一旦 OpenAPI/Swagger 规范输出已交付，询问用户：

"是否需要我为此设计生成 API 测试用例？（是/否）"

如果用户回答**是**：
- 检查已安装技能列表中是否有 API Test Case Generator 技能
- 如果技能**可用**：
  - 阅读并遵循 API Test Case Generator 技能中的说明
  - 将上述规范输出作为输入
- 如果技能**不可用**：
  - 通知用户："看起来 API Documentation 技能未安装。您可以安装后重新运行。"

如果用户回答**否**：
- 结束任务

---

## 局限性

- 仅在与上游来源和本地项目上下文明确匹配时使用此技能。
- 应用变更前，务必验证命令、生成的代码、依赖、凭证以及外部服务行为。
- 不要将示例替代为针对具体环境的安全测试、安全审查，或在执行破坏性或高成本操作前获取用户批准。
