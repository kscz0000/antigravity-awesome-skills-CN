---
name: textme
description: "从手机给 Claude 发短信 — 配置 njerschow/textme 守护进程，让入站 iMessage 驱动你笔记本上的 Claude Code 会话，支持语音消息、图片输入、代码执行以及手机号白名单。"
category: automation
risk: critical
source: community
source_repo: njerschow/textme
source_type: community
date_added: "2026-05-26"
author: AnthonyFirth
tags: [textme, sendblue, imessage, sms, claude-code, daemon, remote-control, automation]
tools: [claude, cursor, gemini]
license: "MIT"
license_source: "https://github.com/njerschow/textme/blob/main/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# TextMe（短信触发 Claude）

## 概述

[`njerschow/textme`](https://github.com/njerschow/textme) 是一个本地守护进程，它通过 [Sendblue](https://sendblue.com) 把入站的 iMessage 桥接到用户机器上的 Claude Code 会话。白名单内的手机号可以发送文本、语音消息、图片，并通过文件系统操作、代码执行和基于 `cd` 的目录切换来驱动 Claude —— 把用户的手机变成笔记本上 Claude 的遥控器。这是出站通知模式（[[sendblue-notify]]）的**入站**对应物：textme 是手机 → Claude；sendblue-notify 是 Claude → 手机。

## 适用场景

- 当用户说"给 Claude 发短信""短信发到我的笔记本""从手机驱动 Claude""我想给 Claude 发 iMessage""让我从手机上写代码"时使用。
- 当用户正在专注做事、远离办公桌，想要通过 SMS/iMessage 启动、监督或打断一个 Claude 会话时使用。
- 当设置一个长期运行的无人值守工作站，希望用户在旅行或离开键盘时远程控制它时使用。
- 与 [[sendblue-notify]] 配合，实现双向流 —— 同一个 Sendblue 账号上既可发出站完成通知，也可收入站指令。
- **不要**用于纯出站模式（例如"X 完成时给我发短信"）。那是 [[sendblue-notify]] 的范畴，不需要守护进程。

## 先决条件

- 持续在线的 macOS 或 Linux 主机（守护进程会持续轮询 Sendblue）。
- Node.js 18+。
- 一个有效的 Sendblue 账号，具备 API 凭据和一个已开通的 iMessage 号 —— 通过 [[sendblue-cli]] 设置（先 `sendblue setup`，再 `sendblue show-keys` 获取 API key/secret）。
- 主机上已安装并完成认证的 Claude Code（`npm install -g @anthropic-ai/claude-code`）。
- 可选：用于 Whisper 语音转录的 OpenAI API key。

## 工作原理

### 步骤 1：安装守护进程

```bash
git clone https://github.com/njerschow/textme.git
cd textme/daemon
npm install
npm run build
mkdir -p ~/.config/claude-imessage
```

### 步骤 2：配置凭据和白名单

创建 `~/.config/claude-imessage/config.json`：

```json
{
  "sendblue": {
    "apiKey": "YOUR_SENDBLUE_API_KEY",
    "apiSecret": "YOUR_SENDBLUE_API_SECRET",
    "phoneNumber": "+1SENDBLUE_NUMBER"
  },
  "whitelist": ["+1YOUR_PHONE"],
  "pollIntervalMs": 5000,
  "conversationWindowSize": 20
}
```

`whitelist` 是入站 iMessage 与主机上代码执行之间的**唯一**授权关口。请把它视作安全边界，而不是用户体验偏好。仅添加用户自己控制的手机号；永远不要"以防万一"地把共享号、工作号或家庭号加进去。

若需语音转录，可选择在守护进程目录的 `.env` 中加入：

```bash
OPENAI_API_KEY=sk-...
```

### 步骤 3：运行守护进程

快速试运行：

```bash
cd textme/daemon
npm start
```

若需长期运行（在用户验证行为无误后推荐）：

```bash
pm2 start dist/index.js --name textme
pm2 save
pm2 startup
```

或者在 macOS 上，安装 launchd 服务：

```bash
./scripts/install-launchd.sh
```

### 步骤 4：从 iMessage 驱动 Claude

守护进程运行后，白名单内的号码向 Sendblue 手机号发送的 iMessage 即可送达 Claude。内置命令：

| 命令 | 效果 |
|---|---|
| `?` | 列出可用命令 |
| `status` | 显示当前守护进程状态和工作目录 |
| `queue` | 显示待处理的消息队列 |
| `history` | 最近的消息历史 |
| `home` | `cd` 回到主目录 |
| `reset` | 返回主目录并清空对话历史 |
| `cd /path` | 切换工作目录 |
| `stop` | 取消当前 Claude 任务 |
| `yes` / `no` | 批准或拒绝待执行的动作 |

其他任何内容都会被视作 Claude 提示，并路由到当前会话。

### 步骤 5：依赖它之前先验证

在无人值守的工作流中使用 textme 之前，用户必须：

1. 从白名单手机发送 `status` —— 应收到一个目录 + 状态的回复。
2. 发送一条无害命令（`pwd`、`ls`），并确认收到输出。
3. 从一个**非白名单**号码发送内容，确认它被**忽略**，而不是回显出来。
4. 拔掉电源：杀掉守护进程，确认消息不再被处理（无僵尸进程）。

如果上述任何一项失败，请不要启用 launchd / pm2 自启动。

## 示例

### 示例 1：初次设置走查

```bash
# 1. Make sure sendblue CLI is set up and creds work
sendblue whoami

# 2. Grab Sendblue API key & secret (these are NOT the CLI's bearer token)
sendblue show-keys

# 3. Clone + build the daemon
git clone https://github.com/njerschow/textme.git
cd textme/daemon && npm install && npm run build

# 4. Fill in ~/.config/claude-imessage/config.json with the values from step 2
#    and YOUR personal phone number as the only whitelist entry

# 5. Start, send "?" from your phone, confirm response
npm start
```

### 示例 2：与 `sendblue-notify` 组合

通过 [[sendblue-notify]] 接线出站完成通知，*同时*通过 textme 接线入站控制 —— 它们共用同一个 Sendblue 账号，但解决相反的问题：

- Claude 完成长任务 → 通过 [[sendblue-notify]]（`Stop` 钩子）给用户发短信。
- 用户回复"看一下 diff" → textme 把消息路由进 Claude → Claude 再通过 Sendblue 回复。

### 示例 3：跟踪守护进程日志

```bash
# pm2
pm2 logs textme

# Standalone
tail -f ~/.local/log/claude-imessage.log
```

### 示例 4：纯 MCP 替代方案（无守护进程）

如果用户希望 Claude Code 把 Sendblue 消息作为工具可用，但**不想**运行一个轮询的守护进程来监听入站命令，可以改为把 Sendblue 注册为 MCP 服务器：

```bash
claude mcp add sendblue_api \
  --env SENDBLUE_API_API_KEY=your-api-key \
  --env SENDBLUE_API_API_SECRET=your-api-secret \
  -- npx -y sendblue-api-mcp --client=claude-code --tools=all
```

这会让 Claude 在会话内获得出站的 Sendblue 工具，但**不会**开启 textme 所提供的"入站手机控制 Claude"通道。如果目标是"随时随地向 Claude 发短信"，选 textme；如果只是让 Claude 能发短信，选 MCP 更轻量。

## 最佳实践

- ✅ **起步时白名单只放一个手机号。** 白名单就是安全边界；要慢慢扩展，且只能加用户自己控制的号。
- ✅ **以普通用户身份运行守护进程**，绝不要用 root 或通过 `sudo` 运行。
- ✅ **首次测试在沙箱目录中进行**（`cd ~/textme-sandbox`），而不是在 `~` 或真实仓库里。
- ✅ **启用自启动前，先验证非白名单忽略路径。** 一旦守护进程处理任何发送者，就等同于在主机上开了一个 shell。
- ✅ **保持 `pollIntervalMs` ≥ 5000**，除非用户清楚 Sendblue 的速率限制和费用影响。
- ❌ **不要公开分享 Sendblue 号。** 即便有白名单，主机也会对每条消息做处理；来自未知发送者的洪泛依然会消耗轮询周期。
- ❌ **不要把 `config.json` 存到仓库、dotfiles 备份或云同步中** —— 它包含 API 凭据和用户的手机号。
- ❌ **不要在共享机器上运行守护进程**，而不考虑该机器的其他用户现在都可以通过发送 SMS 来触达什么。

## 局限性

- **纯出站流程不需要本技能。** "X 完成时给我发短信"用 [[sendblue-notify]]；跑守护进程属于杀鸡用牛刀。
- **语音转录需要单独的 OpenAI API key。** 没有它时，语音消息可能被丢弃或以未转录音频的形式呈现（取决于守护进程版本）。
- **守护进程按间隔轮询** —— 没有推送投递。预计从消息接收到 Claude 响应之间有秒级延迟。
- **一个会话，一台机器。** 这是按主机的守护进程，不是多租户服务。两个守护进程共享同一个 Sendblue 号时，都会尝试处理每一条入站消息。
- **Sendblue 免费套餐的验证仍然适用。** 在 Claude 的出站回复能送达用户之前，用户的手机必须先给 Sendblue 号发过一次短信（见 [[sendblue-cli]] 的局限性）。

## 安全与风险提示

textme 是一个**仅由手机号白名单把关的远程代码执行面**。请按这个定位对待它。

- **白名单就是安全边界。** 任何能仿冒或劫持白名单号码的人都可以在主机上驱动 Claude。要审慎决定哪些号码上名单，并在不再需要访问权时移除它们。<!-- security-allowlist: documented remote-control daemon; required disclosure per quality-bar.md -->
- **Sendblue API 凭据很敏感。** `config.json` 包含 API key、API secret 和用户的手机号。将其权限设为 `600`，不要放进 dotfile 仓库，也永远不要粘贴到共享日志、Gist 或截图中。
- **守护进程继承用户的权限。** 它能读、写、执行该运行用户能做的任何事。不要以 root 运行；不要从包含用户不想被入站 SMS 暴露的密钥目录中运行；如果有专用主机或 VM，优先使用它们。
- **Claude Code 的权限模型在守护进程驱动的会话内仍然生效** —— 破坏性动作仍会弹出确认提示。textme 暴露了 `yes`/`no` 回复路径来处理这些提示，这意味着**手机号本身在做审批决定**。请确保白名单与"远程批准破坏性操作"这一信任级别相匹配。
- **入站消息是不可信输入。** 把 textme 提示视作来自开放互联网的用户输入（带手机号身份验证）。不要把其内容塞进 `eval`、shell 替换或绕过 Claude Code 审查的脚本。
- **回复的锁屏预览会泄露。** Claude 响应消息时，回复会未脱敏地落到用户的锁屏上。不要通过 textme 让 Claude 通过 SMS 暴露密钥、token 或客户数据 —— 改为链接到本地日志或 PR。
- **守护进程的存活是一把双刃剑。** 若 pm2/launchd 正在自动重启守护进程，用户必须记住在修改白名单条目、轮换凭据或重启进入不可信状态之前先停掉它。

## 常见陷阱

- **白名单漂移。** 一个"为了演示"加进去的号码永远不会被移除。每当主机换人或范围变化时，审计一下 `whitelist`。
- **`apiKey` / `apiSecret` 混淆。** Sendblue 的 API 凭据（来自 `sendblue show-keys`）与 CLI 在 `~/.sendblue/credentials.json` 中的本地 bearer token 是不同的。textme 需要的是 *API* 凭据，不是 CLI 的认证文件。
- **免费套餐的静默发送失败。** 如果用户的手机从未先给 Sendblue 号发过短信，Claude 的出站回复会静默失败。在依赖这条回路之前，用 `sendblue contacts` 验证一下。
- **未验证就自启动。** 在测试非白名单忽略路径之前就安装 launchd plist 或 `pm2 save` 守护进程，会在开机时基线化一个可能开放的守护进程。先验证，再持久化。
- **在 `~` 或包含密钥的仓库里运行守护进程。** 启动时的工作目录会暴露给 textme 被要求做的任何事（`ls`、`cat` 等）。从沙箱目录启动，并刻意 `cd`。
- **把 textme 和 Sendblue MCP 搞混。** 它们看起来很像，但 MCP 变体只给 Claude **出站**的 Sendblue 工具 —— 不会开启入站通道。如果用户想要"从手机给 Claude 发短信"，他们需要 textme；如果想要"Claude 能在会话中发短信"，MCP 更轻量。

## 相关技能

- `@sendblue-notify` —— 出站对应物（Claude → 手机）。可与 textme 组合，形成双向回路。
- `@sendblue-cli` —— 账号设置、凭据管理，以及暴露 textme 所需的 API key/secret 的 `show-keys` 命令。
- `@sendblue-api` —— HTTP API 参考，适合想自己构建入站处理器、不使用 textme 守护进程的用户。
- `@update-config` —— 若要将 textme 与 Claude Code 钩子（例如给用户发提醒的 `Stop` 钩子）一同接入，用它来编辑 settings.json。

## 链接

- 仓库：<https://github.com/njerschow/textme>
- 许可证：<https://github.com/njerschow/textme/blob/main/LICENSE>（MIT）
- Sendblue：<https://sendblue.com>
- Sendblue 文档：<https://docs.sendblue.com>