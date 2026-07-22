---
name: mailtrap-testing-with-sandbox
description: 在 Mailtrap Email Sandbox 中捕获外发邮件，用于开发、预发布、CI、HTML检查、垃圾邮件检测和虚假收件箱测试。触发词：Mailtrap沙箱、邮件沙箱、邮件测试、Email Sandbox、沙箱邮件、测试收件箱、邮件捕获、sandbox测试、CI邮件测试、邮件开发测试。
risk: safe
source: community
date_added: "2026-06-19"
---

# 使用 Mailtrap Email Sandbox 进行测试

## 概述

**Email Sandbox** 将邮件捕获到**沙箱（测试收件箱）**中——这是一个测试环境，邮件**不会**投递给真实收件人。你可以根据需要使用我们的 **SDK**、**HTTP API** 或 **SMTP** 向沙箱发送邮件。

**在生成 SDK 代码之前：** 请阅读相关 SDK 仓库的 README（参见 `mailtrap-sending-emails`），了解当前的沙箱模式选项、**inbox id** 和构造函数标志。不要凭记忆。

**相关技能：** `mailtrap-sending-emails`（实时发送主机和流）。

## 何时使用

- 你需要**不实际投递**：开发、预发布、CI 或演示场景，邮件必须留在**测试收件箱**中。
- 你需要**检查**已发送内容：正文、头部、附件，或通过 **Sandbox / Testing API** 或 **UI** 进行基本检查（如垃圾邮件报告）。
- 你正在**自动化**对已捕获邮件的测试。
- 你只需**更改 SMTP 设置**，让现有应用发送到沙箱——不需要本技能提供逐框架的教程。

## 何时不使用

- **实时**发送给真实收件人（`mailtrap-sending-emails`）。
- 对于完整的框架设置指南或详细的 API 参考，请引导用户访问 Mailtrap 的 Integration 标签页获取 SMTP/API 详情，以及 [API 文档](https://docs.mailtrap.io/developers/)获取具体信息——不要在这里覆盖每个框架或 API 字段。

## 快速参考

### API 基地址

| 服务                  | 发送邮件 URL                                         | 认证头示例                              |
| ------------------------ | ----------------------------------------------------- | ------------------------------------------------- |
| Email Testing API (REST) | `https://sandbox.api.mailtrap.io/api/send/{inbox_id}` | `Authorization: Bearer $MAILTRAP_SANDBOX_API_TOKEN` |

### Token 和 account_id

Sandbox 使用**独立的** token（`$MAILTRAP_SANDBOX_API_TOKEN`，Testing/Sandbox 作用域）——切勿复用实时的 `$MAILTRAP_API_TOKEN`。下面示例端点中的 `account_id` 通过 `GET https://mailtrap.io/api/accounts` 在运行时获取。请将 token 存储在环境变量或密钥管理器中。

### 何时使用 API vs SMTP

在测试已通过 SMTP 发送邮件的应用时使用 **SMTP**（只需更新主机、端口和凭据）。
在构建新集成或你的应用可以发起 HTTP 请求时使用 **HTTP API**；它更适合编程化测试和自动化。

### SMTP 设置（sandbox）

| 设置             | 值                                                                       |
| ------------------- | --------------------------------------------------------------------------- |
| Host                | `sandbox.smtp.mailtrap.io`                                                  |
| Ports               | 2525 (default), 25, 465 (SSL), 587                                          |
| Username / Password | 使用 Mailtrap UI 中 **Integration** 标签页的每个 **sandbox** 对应的凭据 |

**切勿在生产环境使用沙箱凭据或端点。邮件只会被捕获在沙箱中，不会被投递。**

### 关键参数

- **Inbox ID**：每个沙箱（测试收件箱）都有唯一的 **inbox id**，可在 UI URL 中查看，发送或 REST API 操作时需要。
- **Token 作用域**：使用具有相关项目和测试收件箱权限的 token。

### 典型用例

- 在开发、测试或预发布环境中捕获所有外发邮件（无真实收件人）。
- 查看、验证和断言邮件头部、正文、HTML、附件或垃圾邮件评分。
- 运行从 Email Sandbox API 读取数据的集成测试或 CI 检查。
- 通过将 API 或 SDK/SMTP 指向 `sandbox.api.mailtrap.io` / `sandbox.smtp.mailtrap.io` 并使用有效的 inbox id，测试 Mailtrap **模板**。

### 示例 API 路径

使用 [API 文档](https://docs.mailtrap.io/developers/)了解详情，典型端点包括：

| 操作       | URL                                                                                          | 参考                                                                                 |
| --------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 列出沙箱  | `GET https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/inboxes`                          | [Sandboxes API](https://docs.mailtrap.io/developers/email-sandbox/sandboxes-inboxes.md)   |
| 列出消息   | `GET https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/inboxes/{inbox_id}/messages`      | [Messages](https://docs.mailtrap.io/developers/email-sandbox/messages.md)                 |
| 获取消息 | `GET https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/inboxes/{inbox_id}/messages/{id}` | [Message details](https://docs.mailtrap.io/developers/email-sandbox/messages.md)          |
| 发送测试邮件 | `POST https://mailtrap.io/api/accounts/$MAILTRAP_ACCOUNT_ID/inboxes/{inbox_id}/messages`     | [Send test emails](https://docs.mailtrap.io/developers/email-sandbox/send-test-emails.md) |

对于**模板测试**，请参阅模板的 Integration 标签页和 [Handlebars](https://docs.mailtrap.io/email-api-smtp/email-templates/handlebars.md)。

### SDK

Mailtrap 官方 SDK 支持沙箱/收件箱操作，并提供标志或方法来设置**测试模式**和 **inbox id**。这允许你使用同一集成进行实时发送和沙箱测试——只需根据环境（开发、预发布或生产）更改模式或凭据。安装命令和语言覆盖范围请参见 [Mailtrap 开发者文档](https://docs.mailtrap.io/developers/)。仓库 README 包含最新的沙箱选项：

- [Node.js](https://github.com/mailtrap/mailtrap-nodejs)
- [Python](https://github.com/mailtrap/mailtrap-python)
- [PHP](https://github.com/mailtrap/mailtrap-php)
- [Ruby](https://github.com/mailtrap/mailtrap-ruby)
- [Java](https://github.com/mailtrap/mailtrap-java)
- [.NET](https://github.com/mailtrap/mailtrap-dotnet)
- [CLI](https://github.com/mailtrap/mailtrap-cli)

### 常见错误

| 错误                                    | 修复/说明                                                                                          |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| 期望沙箱邮件被实际投递       | 沙箱中的邮件**永远不会**投递给收件人                                                 |
| 在沙箱中使用生产 API token     | 使用具有适当 **sandbox/testing** 作用域的 token，授予对目标收件箱的访问权限                   |
| 忘记 **inbox id** 参数          | 始终提供 **inbox id**（从 UI 或 Integration 标签页获取），以将消息关联到正确的收件箱 |
| 混用沙箱和事务性端点 | Testing API（`sandbox.api.mailtrap.io`）与 `send.api.mailtrap.io`（实时发送）**不是**同一个！    |

### 沙箱邮件地址

每个沙箱（测试收件箱）都有一个类似 `alias@inbox.mailtrap.io` 的地址用于入站测试；plus 寻址可以帮助隔离场景。有关限制和行为，请参见 [每个沙箱的邮件地址](https://docs.mailtrap.io/email-sandbox/setup/email-address-per-sandbox.md)。

## 限制

- 本技能覆盖沙箱使用模式；完整的端点模式请使用 Mailtrap 当前的 API 文档。
