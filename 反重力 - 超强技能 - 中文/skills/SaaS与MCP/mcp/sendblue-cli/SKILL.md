---
name: sendblue-cli
description: "通过 @sendblue/cli npm 包在 shell 中发送 iMessage 和 SMS——支持外发消息、联系人管理和账户设置，无需 API 客户端或 webhook 服务器。涉及：sendblue、@sendblue/cli、iMessage、SMS、CLI、shell 发短信、通知脚本、agent hook 发消息。"
category: api-integration
risk: critical
source: community
source_repo: sendblue-api/sendblue-cli
source_type: official
date_added: "2026-05-22"
author: AnthonyFirth
tags: [sendblue, imessage, sms, cli, messaging, notifications]
tools: [claude, cursor, gemini]
license: "MIT"
license_source: "https://github.com/sendblue-api/sendblue-cli/blob/main/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# Sendblue CLI

## 概述

`@sendblue/cli` 是一个 Node CLI，用于创建 Sendblue 账户、开通 iMessage 号码并发送消息。这是从 shell、脚本或 Claude Code hook 中发送短信的最快方式——无需 API 客户端、无需 webhook 服务器、无需在环境变量中存放凭据。凭据保存在 `~/.sendblue/credentials.json`（权限模式 `600`），需要 Node.js 18+。

## 适用场景

- 适用于用户希望从脚本、shell、hook 或 agent turn 中向手机号发送短信（例如"X 完成后给我发短信""提醒我的手机""完成时通知我"）。
- 适用于用户将 `sendblue` 作为 CLI/二进制工具提及，或要求安装 `@sendblue/cli` 包。
- 当工作发生在 shell 上下文、一次性脚本、定时任务或 agent hook 中时，优先使用本技能而非 [[sendblue-api]]。
- 当编写集成 Sendblue 的应用代码、接收入站 webhook、或需要 CLI 未暴露的功能（发送样式、表情回复、群消息、状态回调、媒体上传）时，改用 [[sendblue-api]]。

## 工作原理

### 第一步：安装

```bash
npm install -g @sendblue/cli       # global, exposes `sendblue`
# or one-shot:
npx @sendblue/cli <command>
```

### 第二步：设置账户

`sendblue setup` 默认以交互模式运行。在 CI/脚本场景下，分两阶段执行——第一次调用通过邮件发送 8 位验证码，第二次调用消费该验证码。

```bash
sendblue setup --email you@example.com                                       # sends code
sendblue setup --email you@example.com --code 12345678 \
               --company my-co --contact +15551234567                        # completes setup
```

| 参数 | 说明 |
|---|---|
| `--email` | 邮箱地址 |
| `--code` | 8 位验证码（来自邮件） |
| `--company` | 小写字母，可含连字符或下划线，长度 3–64 字符 |
| `--contact` | 第一个联系人，E.164 格式 |

### 第三步：发送消息

```bash
sendblue send +15551234567 'Hello from Sendblue!'
sendblue messages --inbound --limit 20
```

手机号必须使用 E.164 格式（`+` + 国家代码 + 数字，不含空格或连字符）。

### 第四步：管理联系人与套餐

在免费套餐下，**联系人必须先向你的 Sendblue 号码发送一次短信，外发到该联系人的消息才能成功送达**。执行 `sendblue setup ... --contact +15551234567` 后，让该联系人向打印出的 Sendblue 号码发送任意短信，然后运行 `sendblue contacts` 确认验证状态。

## 命令参考

| 命令 | 用途 |
|---|---|
| `sendblue setup` | 创建账户、验证邮箱、设置公司名称、添加第一个联系人 |
| `sendblue login` | 登录已有账户 |
| `sendblue send <number> <message>` | 发送 iMessage |
| `sendblue messages [--inbound\|--outbound] [-n <number>] [-l <count>]` | 列出最近的消息 |
| `sendblue add-contact <number>` | 注册联系人 |
| `sendblue contacts` | 列出联系人及其验证状态 |
| `sendblue status` | 账户/套餐信息 |
| `sendblue whoami` | 显示当前凭据并验证有效性 |

## 示例

### 示例 1：长时间任务完成时通知

```bash
long_running_thing && sendblue send +15551234567 "✅ done: $(date)"
```

### 示例 2：读取特定联系人的最近入站消息

```bash
sendblue messages -n +15551234567 --inbound --limit 50
```

### 示例 3：批量发送前验证凭据有效

```bash
sendblue whoami || sendblue login
```

### 示例 4：接入 Claude Code `Stop` hook

若要在每次 agent turn 结束时向自己发短信，可在 `settings.json` 中注册一个 `Stop` hook，通过 shell 调用 `sendblue send`。具体的 hook 接线交由 [[update-config]] 处理，触发逻辑交由 [[sendblue-notify]] 处理——本技能只负责 CLI 调用本身。

## 最佳实践

- ✅ **全程使用 E.164 格式号码。** `+15551234567`，不要使用 `5551234567` 或 `(555) 123-4567`。
- ✅ **在无人值守的批量发送前运行 `sendblue whoami`**，以便在凭据过期或缺失时快速失败。
- ✅ **以拥有 `~/.sendblue/credentials.json` 的同一操作系统用户身份重新运行 `setup`**。
- ❌ **不要使用 `sudo`**——它会把凭据写入 root 的家目录，下一次非 sudo 运行将无法读取。
- ❌ **不要将凭据嵌入环境变量**，CLI 已从每用户的凭据文件中读取它们。

## 局限性

- 以外发为主：没有内建的 webhook 服务器处理入站。如需完整的入站处理，请使用 [[sendblue-api]] 的 webhook。
- CLI 不暴露发送样式/特效、表情回复、群消息、状态回调、媒体上传，也不支持联系人 API 的高级 CRUD。如需这些功能，请使用 HTTP API。
- 免费套餐账户在外发前需要先完成接收方验证。

## 安全与注意事项

- 凭据以 `600` 权限模式写入 `~/.sendblue/credentials.json`。请像对待 API 密钥一样对待该文件——不要提交到仓库，也不要在同等安全防护缺失的情况下跨机器复制。
- 将每次外发、联系人设置、登录或账户设置操作视为状态变更操作。在执行前应预览收件人、消息正文以及账户/邮箱目标，并等待用户的明确确认。
- 以拥有凭据文件的操作系统用户身份运行 CLI。`sudo` 会在 root 家目录下写入一份独立副本，造成静默失同步。
- 向手机号发送外发消息并非毫无后果——只有在按耗时或成功条件加以门控之后，再将 `sendblue send` 接入 hook 或循环，避免对收件人造成骚扰。
- 验证码通过邮件送达；请将你注册的邮箱地址视为账户的恢复凭据之一。

## 常见陷阱

- **只能使用 E.164 格式。** `5551234567` 或 `(555) 123-4567` 会失败——务必使用 `+15551234567`。
- **免费套餐下未验证的联系人。** 向尚未发过短信的联系人外发会返回错误——让对方先向你的 Sendblue 号码发一次短信，再用 `sendblue contacts` 确认。
- **非交互模式下的两步设置。** 仅使用 `--email` 只会发送验证码；必须再发起一次调用，同时传入 `--code` 和其余参数才能完成设置。
- **凭据按用户隔离。** `~/.sendblue/credentials.json` 仅属所有者本人（`600`）。不要 `sudo` 污染 root 家目录——以运行 `setup` 的同一用户身份重新执行才能生效。

## 相关技能

- `@sendblue-api` — 用于应用代码、webhook 以及 CLI 未暴露功能的 HTTP/JSON 替代方案。
- `@sendblue-notify` — 建立在 CLI 之上的"X 完成后给我发短信"工作流的模式与文案规则。
- `@update-config` — 将 `sendblue send` 接入 Claude Code hooks（`Stop`、`Notification`），但不负责消息逻辑本身。

## 链接

- README 与完整参数参考：<https://github.com/sendblue-api/sendblue-cli>
- Sendblue：<https://sendblue.com>
- API 文档（更详细的协议说明）：<https://docs.sendblue.com>