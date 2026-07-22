---
name: mailtrap-sending-emails
description: 配置或排查 Mailtrap 实际邮件发送，涵盖 Email API、SMTP、事务流、批量流或批次请求。触发词：Mailtrap发送邮件、邮件发送配置、Email API、SMTP发送、事务邮件、批量邮件、批次发送、mailtrap sending emails
risk: critical
source: community
date_added: "2026-06-19"
---

# 发送邮件（Mailtrap）

## 概述

Mailtrap 通过 **Email API**（REST）或 **SMTP** 发送实际邮件。API/SMTP 适用两种 **流（stream）**：**Transactional**（非推广、应用生成的邮件）和 **Bulk**（**推广** / 营销大批量邮件）。**Batch** 不是第三种流：它是在匹配内容的流上**用一个请求提交多条消息**的方式。**Campaigns** 是向 **Mailtrap 联系人**发送推广邮件的独立产品路径。在构建或调试集成（包括 AI 辅助编码）时，请将本文档与 [Transactional](https://docs.mailtrap.io/developers/email-sending/transactional.md) / [Bulk](https://docs.mailtrap.io/developers/email-sending/bulk.md) 开发者页面配合使用。

## 使用时机

在集成、配置或排查 Mailtrap 实际邮件发送时使用，涵盖 Email API、SMTP、事务流、批量流或批次请求。

## 集成方式（优先顺序）

**推荐顺序：**

1. **用户平台的插件或集成**（零代码或最小配置）_在可用的情况下_
2. **官方 SDK**，当你的语言有官方 SDK 时（维护良好的客户端、类型化辅助、减少 URL/认证出错的可能性）。
3. **HTTP Email API**，当没有 SDK 或 SDK 不适用时（直接 `POST` 到 `/api/send` 或 `/api/batch`，使用 JSON）。
4. **SMTP**，仅当你**确实需要**时（遗留技术栈、只支持 SMTP 的主机/平台，或排除了 HTTP 的硬性约束）。

## 选择发送方式

| 方式                    | 使用场景                                                                                                                                                                                                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Transactional，单条消息** | **由你的应用生成**的邮件（密码重置、收据、通知、告警）。每 `POST https://send.api.mailtrap.io/api/send` 一条逻辑消息                                                                                                                                                             |
| **Bulk**                    | **推广**邮件，发送给你**自行管理的联系人**，通过 Mailtrap 大批量发送。与"batch"不同：bulk 是**流**，不是批次端点。                                                                                                                                                               |
| **Batch**                   | 你有**多条不同的消息**需要**同时**提交（每次请求最多 500 条）。减少 HTTP 开销；可同时应用于 transactional 和 bulk                                                                                                                                                                   |
| **Campaigns**               | **推广**邮件，发送给存储为 **Mailtrap 联系人**的收件人，使用 Mailtrap **Campaigns**（受众、排期、产品内报告）。**推荐使用**以避免自行实现联系人管理和邮件发送逻辑；**需要先在 UI 中完成设置**才能发送——本技能不替代该工作流。|

**生成 SDK 代码之前：**阅读下方 **SDKs** 章节中链接的相关 SDK 仓库的 README，了解当前的方法签名、构造函数选项和示例。不要凭记忆猜测。

**关联技能：**`mailtrap-testing-with-sandbox`（安全测试）和 `mailtrap-setting-up-sending-domain`（发送前验证）。

## 不适用场景

- **仅 Sandbox**——捕获邮件但不投递，在沙盒中读取消息（`mailtrap-testing-with-sandbox`）。
- 主要需求是 **webhooks**、**Campaigns UI 分步设置**或**送达率深入分析**。
- **详尽的 API 参考**——当用户路径明确后，链接官方发送文档获取完整 schema、可选字段和边缘情况。

## 快速参考

### Email API

| 流                          | 发送端点                                      | 批次端点                                       | Authorization 请求头                        |
| --------------------------- | --------------------------------------------- | ---------------------------------------------- | ------------------------------------------- |
| Transactional               | `POST https://send.api.mailtrap.io/api/send`  | `POST https://send.api.mailtrap.io/api/batch`  | `Authorization: Bearer $MAILTRAP_API_TOKEN` |
| Bulk（推广 / 营销大批量）   | `POST https://bulk.api.mailtrap.io/api/send`  | `POST https://bulk.api.mailtrap.io/api/batch`  | `Authorization: Bearer $MAILTRAP_API_TOKEN` |

### SMTP

| 设置     | Transactional                    | Bulk                              |
| -------- | -------------------------------- | --------------------------------- |
| Host     | `live.smtp.mailtrap.io`          | `bulk.smtp.mailtrap.io`           |
| Port     | 587（也支持 25、2525、465 with SSL） | 587（也支持 25、2525、465 with SSL） |
| Username | `api`                            | `api`                             |
| Password | API token（`$MAILTRAP_API_TOKEN`） | API token（`$MAILTRAP_API_TOKEN`） |

### Token

在 `Authorization: Bearer ...` 或 `Api-Token: ...` 中使用 `$MAILTRAP_API_TOKEN`。只要 token 的范围覆盖了对应流，同一个 token 可以同时用于 `send.api.mailtrap.io` 和 `bulk.api.mailtrap.io`。将 token 存储在环境变量或密钥管理器中，并在访问权限变更时轮换。

### 速率限制

| 范围              | 限制         | 窗口       |
| ----------------- | ------------ | ---------- |
| Sending API（每 token） | 150 请求 | 10 秒 |

遇到 `429` 时使用退避策略。

### JSON 请求体（非模板）

典型字段包括 `from`、`to`、`subject`，以及 `text` 和/或 `html`。可选字段：`category`、`custom_variables`。完整请求体参见：[Transactional send](https://docs.mailtrap.io/developers/email-sending/transactional.md#post-api-send) 和 [Bulk send](https://docs.mailtrap.io/developers/email-sending/bulk.md#post-api-send)。

### 示例（`curl`）

Transactional 发送（`send.api.mailtrap.io`）：

```bash
curl -X POST https://send.api.mailtrap.io/api/send \
  -H "Authorization: Bearer $MAILTRAP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "from": {"email": "hello@yourdomain.com", "name": "Your App"},
    "to": [{"email": "user@example.com"}],
    "subject": "Hello",
    "text": "Plain text body"
  }'
```

Bulk 流在 bulk 主机上使用**相同**的路径和 JSON 结构（相同的环境变量；token 只需要 bulk-stream 范围）：

```bash
curl -X POST https://bulk.api.mailtrap.io/api/send \
  -H "Authorization: Bearer $MAILTRAP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "from": {"email": "hello@yourdomain.com", "name": "Your App"},
    "to": [{"email": "user@example.com"}],
    "subject": "Promotional",
    "html": "<p>HTML body</p>"
  }'
```

Batch（消息数组；每次请求最多 500 条——完整 schema 参见 API 文档）：

```bash
curl -X POST https://send.api.mailtrap.io/api/batch \
  -H "Authorization: Bearer $MAILTRAP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"from":{"email":"a@example.com"},"to":[{"email":"b@example.com"}],"subject":"One","text":"..."}]}'
```

### JSON 请求体（模板）

使用 `template_uuid` 和 `template_variables` 替代原始 `text`/`html`，以使用 Mailtrap 托管的模板。最小示例：

```bash
curl -X POST https://send.api.mailtrap.io/api/send \
  -H "Authorization: Bearer $MAILTRAP_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "from": {"email": "hello@yourdomain.com", "name": "Your App"},
    "to": [{"email": "user@example.com"}],
    "template_uuid": "your-template-uuid",
    "template_variables": {"user_name": "Jane"}
  }'
```

使用与非模板发送相同的 API 操作。

### SDK

- [Node.js](https://github.com/mailtrap/mailtrap-nodejs)
- [Python](https://github.com/mailtrap/mailtrap-python)
- [PHP](https://github.com/mailtrap/mailtrap-php)
- [Ruby](https://github.com/mailtrap/mailtrap-ruby)
- [Java](https://github.com/mailtrap/mailtrap-java)
- [.NET](https://github.com/mailtrap/mailtrap-dotnet)
- [CLI](https://github.com/mailtrap/mailtrap-cli)

## 抑制（Suppressions）

Mailtrap 自动管理硬退信、垃圾邮件举报或取消订阅的地址的抑制列表，不会再次向这些被抑制的收件人发送邮件。详情参见 [Suppressions 文档](https://docs.mailtrap.io/developers/email-sending/suppressions.md)。

## 常见错误

| 错误                                       | 修复                                                                                                                        |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| 混淆 **batch** 和 **bulk**                 | **Batch** = 一个 `/api/batch` 请求中的多条消息。**Bulk** = 推广流/主机和 token                                               |
| 在 transactional 主机上发送推广 API 邮件   | 对于代码中生成的推广内容，使用 bulk base URL 和 bulk token                                                                  |
| Bulk 流量走了 `send.api.mailtrap.io`       | 推广/bulk 流使用 `bulk.api.mailtrap.io`                                                                                     |
| 用 sandbox SMTP 主机发送实际邮件           | 实际发送使用 `live.smtp.mailtrap.io` 或 `bulk.smtp.mailtrap.io`                                                              |
| SMTP 用户名填了邮箱地址                    | 用户名是 `api`；密码是 API token                                                                                             |
| 域名未验证就发送                           | 完成 **Sending Domains** 设置和合规要求（参见 `mailtrap-setting-up-sending-domain`）                                         |
| 凭记忆猜测 SDK API                         | 阅读 SDK README 和 OpenAPI 关联的示例；不要臆造构造函数或方法名                                                              |
| 新项目首选 **SMTP**                        | 优先选择**平台集成**（如有），然后 **SDK**，然后 **HTTP API**；仅在必要时使用 SMTP（参见**集成方式**）                        |

## 限制

- 本技能概述了 Mailtrap 发送方式的选择；完整 schema 和产品限制请使用 Mailtrap 当前 API 文档。
