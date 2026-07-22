# HTTP 错误码参考

本文档记录 Claude API 返回的 HTTP 错误码、常见原因及处理方法。有关语言特定的错误处理示例，请参阅 `python/` 或 `typescript/` 文件夹。

## 错误码摘要

| Code | Error Type              | 可重试 | 常见原因                         |
| ---- | ----------------------- | ------ | -------------------------------- |
| 400  | `invalid_request_error` | 否     | 请求格式或参数无效               |
| 401  | `authentication_error`  | 否     | API 密钥无效或缺失               |
| 403  | `permission_error`      | 否     | API 密钥缺少权限                 |
| 404  | `not_found_error`       | 否     | 端点或模型 ID 无效               |
| 413  | `request_too_large`     | 否     | 请求超过大小限制                 |
| 429  | `rate_limit_error`      | 是     | 请求过多                         |
| 500  | `api_error`             | 是     | Anthropic 服务问题               |
| 529  | `overloaded_error`      | 是     | API 暂时过载                     |

## 详细错误信息

### 400 Bad Request

**原因：**

- 请求体中的 JSON 格式错误
- 缺少必需参数（`model`、`max_tokens`、`messages`）
- 参数类型无效（例如，应为整数的位置传入字符串）
- messages 数组为空
- 消息未在 user/assistant 之间交替

**示例错误：**

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "message": "messages: roles must alternate between \"user\" and \"assistant\""
  }
}
```

**修复：** 发送前验证请求结构。检查：

- `model` 是有效的模型 ID
- `max_tokens` 是正整数
- `messages` 数组非空且正确交替

---

### 401 Unauthorized

**原因：**

- 缺少 `x-api-key` 请求头或 `Authorization` 请求头
- API 密钥格式无效
- API 密钥已被撤销或删除

**修复：** 确保 `ANTHROPIC_API_KEY` 环境变量设置正确。

---

### 403 Forbidden

**原因：**

- API 密钥无权访问请求的模型
- 组织级别的限制
- 尝试在没有 beta 访问权限的情况下访问 beta 功能

**修复：** 在控制台中检查你的 API 密钥权限。你可能需要不同的 API 密钥或申请特定功能的访问权限。

---

### 404 Not Found

**原因：**

- 模型 ID 拼写错误（例如 `claude-sonnet-4.6` 而非 `claude-sonnet-4-6`）
- 使用已弃用的模型 ID
- API 端点无效

**修复：** 使用模型文档中的精确模型 ID。你可以使用别名（例如 `claude-opus-4-6`）。

---

### 413 Request Too Large

**原因：**

- 请求体超过最大大小
- 输入中的 token 过多
- 图像数据过大

**修复：** 减少输入大小 — 截断对话历史、压缩/调整图像大小，或将大文档拆分为块。

---

### 400 验证错误

某些 400 错误专门与参数验证相关：

- `max_tokens` 超过模型限制
- `temperature` 值无效（必须为 0.0-1.0）
- 扩展思考中 `budget_tokens` >= `max_tokens`
- 工具定义 schema 无效

**扩展思考的常见错误：**

```
# 错误：budget_tokens 必须 < max_tokens
thinking: budget_tokens=10000, max_tokens=1000  → 错误！

# 正确
thinking: budget_tokens=10000, max_tokens=16000
```

---

### 429 Rate Limited

**原因：**

- 超过每分钟请求数（RPM）
- 超过每分钟 token 数（TPM）
- 超过每天 token 数（TPD）

**检查请求头：**

- `retry-after`：重试前等待的秒数
- `x-ratelimit-limit-*`：你的限制
- `x-ratelimit-remaining-*`：剩余配额

**修复：** Anthropic SDK 自动使用指数退避重试 429 和 5xx 错误（默认：`max_retries=2`）。有关自定义重试行为，请参阅语言特定的错误处理示例。

---

### 500 Internal Server Error

**原因：**

- Anthropic 服务临时问题
- API 处理中的 bug

**修复：** 使用指数退避重试。如果持续存在，请检查 [status.anthropic.com](https://status.anthropic.com)。

---

### 529 Overloaded

**原因：**

- API 需求高
- 服务容量已达上限

**修复：** 使用指数退避重试。考虑使用不同的模型（Haiku 通常负载较低）、分散请求时间或实现请求队列。

---

## 常见错误和修复

| 错误                            | 错误码 | 修复                                                     |
| ------------------------------- | ------ | ------------------------------------------------------- |
| `budget_tokens` >= `max_tokens` | 400    | 确保 `budget_tokens` < `max_tokens`                     |
| 模型 ID 拼写错误                | 404    | 使用有效的模型 ID，如 `claude-opus-4-6`                  |
| 第一条消息是 `assistant`        | 400    | 第一条消息必须是 `user`                                  |
| 连续相同角色的消息              | 400    | `user` 和 `assistant` 必须交替                           |
| 代码中硬编码 API 密钥           | 401    | 使用环境变量                                             |
| 需要自定义重试                  | 429/5xx| SDK 自动重试；通过 `max_retries` 自定义                   |

## SDK 中的类型化异常

**始终使用 SDK 的类型化异常类**，而不是用字符串匹配检查错误消息。每个 HTTP 错误码映射到特定的异常类：

| HTTP Code | TypeScript Class                  | Python Class                      |
| --------- | --------------------------------- | --------------------------------- |
| 400       | `Anthropic.BadRequestError`       | `anthropic.BadRequestError`       |
| 401       | `Anthropic.AuthenticationError`   | `anthropic.AuthenticationError`   |
| 403       | `Anthropic.PermissionDeniedError` | `anthropic.PermissionDeniedError` |
| 404       | `Anthropic.NotFoundError`         | `anthropic.NotFoundError`         |
| 429       | `Anthropic.RateLimitError`        | `anthropic.RateLimitError`        |
| 500+      | `Anthropic.InternalServerError`   | `anthropic.InternalServerError`   |
| Any       | `Anthropic.APIError`              | `anthropic.APIError`              |

```typescript
// ✅ 正确：使用类型化异常
try {
  const response = await client.messages.create({...});
} catch (error) {
  if (error instanceof Anthropic.RateLimitError) {
    // 处理速率限制
  } else if (error instanceof Anthropic.APIError) {
    console.error(`API error ${error.status}:`, error.message);
  }
}

// ❌ 错误：不要用字符串匹配检查错误消息
try {
  const response = await client.messages.create({...});
} catch (error) {
  const msg = error instanceof Error ? error.message : String(error);
  if (msg.includes("429") || msg.includes("rate_limit")) { ... }
}
```

所有异常类都继承自 `Anthropic.APIError`，它有一个 `status` 属性。使用 `instanceof` 检查时，从最具体到最不具体（例如，先检查 `RateLimitError` 再检查 `APIError`）。
