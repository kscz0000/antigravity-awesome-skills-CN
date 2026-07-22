---
name: postman-openapi-converter
description: 将 OpenAPI 3.x 或 Swagger 2.0 规范（YAML 或 JSON）转换为完整的、可直接导入的 Postman Collection v2.1 JSON 文件。触发词：convert OpenAPI spec、convert Swagger、openapi.yaml、swagger.json、转换 OpenAPI、转换 Swagger、Postman 集合转换、OpenAPI 转 Postman
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/api-skill/postman/postman-openapi-converter
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# OpenAPI → Postman Collection 转换器

## 何时使用

当需要将 OpenAPI 3.x 或 Swagger 2.0 规范（YAML 或 JSON）转换为完整的、可直接导入的 Postman Collection v2.1 JSON 文件时使用本技能。当用户提供或引用 OpenAPI 规范、Swagger 文件、openapi.yaml、swagger.json，或使用"转换我的 OpenAPI 规范"等表述时触发。

将 **OpenAPI 3.x** 或 **Swagger 2.0** 规范转换为有效的 **Postman Collection v2.1**。

---

## 第 1 步 — 检测与验证输入

从输入中识别规范版本：
- `openapi: 3.x.x` → OpenAPI 3
- `swagger: "2.0"` → Swagger 2

如果输入被截断或不完整，转换可用部分并注明缺失的章节。

---

## 第 2 步 — 提取映射

### OpenAPI 3 → Postman

| OpenAPI 字段 | Postman 映射 |
|---|---|
| `info.title` | 集合名称 |
| `info.description` | 集合描述 |
| `servers[0].url` | `{{base_url}}` 变量 |
| `paths.<path>.<method>` | 每个操作对应一个请求项 |
| `operationId` 或 `summary` | 请求名称 |
| `parameters`（path/query/header） | URL 路径变量、查询参数、请求头 |
| `requestBody.content.application/json.schema` | Body（原始 JSON），从 schema 生成示例 |
| `responses` | 保存的示例响应 |
| `components.securitySchemes` | 集合级认证 |
| `tags` | 文件夹分组 |

### Swagger 2 → Postman

| Swagger 字段 | Postman 映射 |
|---|---|
| `host` + `basePath` | `{{base_url}}` |
| `paths.<path>.<method>` | 请求项 |
| `parameters` | Query/path/header/body 参数 |
| `consumes` / `produces` | Content-Type / Accept 请求头 |
| `securityDefinitions` | 集合认证 |
| `tags` | 文件夹 |

---

## 第 3 步 — 生成示例 Body

对于每个包含 `requestBody` 或 `body` 参数的请求，从 schema 生成一个真实的示例 JSON body：
- 使用属性名作为键
- 根据 type + format 推断合理的示例值（例如，`"email"` format → `"user@example.com"`，`"date-time"` → `"2024-01-15T10:30:00Z"`）
- 对于 `$ref` schema，内联解析

---

## 第 4 步 — 认证处理

将安全方案映射到 Postman 认证：

| OpenAPI 方案 | Postman 认证类型 |
|---|---|
| `http: bearer` | `bearer`，使用 `{{token}}` |
| `http: basic` | `basic`，使用 `{{username}}` / `{{password}}` |
| `apiKey: header` | `apikey` 请求头，使用 `{{api_key}}` |
| `apiKey: query` | `apikey` 查询参数 |
| `oauth2` | `oauth2`（注意：需要手动设置 token） |

如果所有端点共享同一方案，在**集合级别**应用认证。对例外情况在请求级别覆盖。

---

## 第 5 步 — 构建 Collection JSON

使用标准 v2.1 结构（与 postman-collection-generator 技能相同的 schema）。

规范转换集合的关键差异：
- 始终按 `tags` 分组为文件夹
- 在每个请求上包含 `description` 字段，内容来自 `operationId` + `summary` + `description`
- 在规范中定义了 `responses` 的地方添加保存的示例响应

```json
"response": [
  {
    "name": "200 OK",
    "status": "OK",
    "code": 200,
    "header": [{ "key": "Content-Type", "value": "application/json" }],
    "body": "{ \"id\": 1, \"name\": \"example\" }",
    "originalRequest": { <copy of the request> }
  }
]
```

---

## 第 6 步 — 环境文件

将所有变量提取到配套环境文件中：
- `base_url` 来自 `servers[0].url` 或 `host + basePath`
- `token`、`api_key`、`username`、`password` 作为空占位符
- 来自 `servers[0].variables` 的任何服务器变量

---

## 第 7 步 — 输出

1. `collection.json` — 完整的 Postman Collection v2.1
2. `environment.json` — 匹配的环境文件
3. **转换摘要**：转换的端点数、创建的文件夹数、检测到的认证类型、任何跳过或近似的字段
4. 导入说明

---

## 边界情况

- **`$ref` 链**：在映射前内联解析所有 `$ref` 指针
- **`allOf` / `oneOf` / `anyOf`**：使用第一个/主 schema 生成 body；在描述中注明替代方案
- **路径参数**：将 URL 路径中的 `{param}` 转换为 `:param`，并添加到 url 对象的 `variable` 数组中
- **多种内容类型**：优先使用 `application/json`；在请求描述中注明其他类型
- **无 operationId**：从 `METHOD /path` 生成名称（例如，`GET /users/{id}` → `Get User by ID`）

---

## 质量检查清单

- [ ] 每个 `paths` 条目至少生成一个请求
- [ ] 路径参数在 Postman URL 中使用 `:param` 格式
- [ ] 所有 `$ref` 已解析 — 输出中没有原始 `$ref` 字符串
- [ ] 认证 token 使用 `{{variables}}`，不硬编码
- [ ] JSON 输出有效且可导入

---

## 完成 API 设计后

交付 API 设计输出后，询问用户：

"是否需要我为这个设计生成 API 文档？（是/否）"

如果用户回答**是**：
- 检查已安装技能列表中是否有 API Documentation 技能
- 如果技能**可用**：
  - 阅读并遵循 API Documentation 技能中的说明
  - 使用上面的 API 设计输出作为输入
- 如果技能**不可用**：
  - 通知用户："看起来 API Documentation 技能未安装。您可以安装后重新运行。"

如果用户回答**否**：
- 在此结束任务

---

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用更改之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代为环境特定测试、安全审查或用户对破坏性/高成本操作的批准。
