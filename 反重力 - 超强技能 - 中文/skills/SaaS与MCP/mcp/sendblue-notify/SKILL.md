---
name: sendblue-notify
description: "在长时间运行的任务、智能体回合或定时作业完成时，通过 @sendblue/cli 向用户手机发送 iMessage 通知——可用于一次性发送，也可与 Claude Code Stop 钩子绑定实现自动触发。涉及：通知提醒、外发短信、sendblue、imessage、停机钩子、完成提醒、自动通知。"
category: automation
risk: critical
source: community
source_type: official
date_added: "2026-05-22"
author: AnthonyFirth
tags: [sendblue, imessage, sms, notifications, hooks, claude-code, automation]
tools: [claude, cursor, gemini]
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# Sendblue Notify（Sendblue 通知）

## 概述

从本地 Claude Code 会话、脚本或定时作业向用户手机发送“发后即忘”的外发通知，全部经由 Sendblue 通道。这就是“离开终端”的工作模式：启动一项耗时的活儿，等结果落地时收到一条 iMessage。本技能负责**何时通知以及通知内容**。实际发送由 [[sendblue-cli]] 完成；钩子接线（让通知自动触发）由 [[update-config]] 完成。

## 适用场景

- 涉及用户说“XX 跑完了发我消息”“给手机发个提醒”“完成时通知我”“构建/部署/迁移完成时告诉我一声”，或“完成后发我一条 iMessage”。
- 涉及为智能体 stop、`/loop` 迭代或 `/schedule` 完成事件配置文本通知钩子。
- 涉及智能体回合确实长时间运行，且用户已在忙其他事情时。
- **不适用**于用户盯着终端的短交互任务——那种场景下通知就是噪音。

## 前置条件

必须已安装并完成认证的 CLI：

```bash
npx @sendblue/cli whoami        # confirms creds
# or, if first run:
npx @sendblue/cli setup
```

用户手机号必须是账号下已验证的联系人。在免费套餐下，该联系人必须先给 Sendblue 号码发过一条短信，外发才能成功——在依赖通知做无人值守流程之前，务必先用 `sendblue contacts` 确认。

目的号码每个项目缓存一次即可，不必每次重问。`NOTIFY_NUMBER` 环境变量或一行式 `.notify-number` 文件都可以；具体存储策略沿用所在项目已有的方式即可。

## 工作机制

### 步骤一：判断通知是否合适

通知只服务于**长时间、无人值守**的工作——而不是闲聊。合适的触发场景：

- 智能体回合超过约 2 分钟（构建、大型重构、迁移、数据集处理）。
- `/loop` 与 `/schedule` 任务产生明确的离散结果。
- CI / 部署完成时用户在终端旁等待。
- 多步剧本式任务，用户已转去忙其他事情。

不适合的触发（不要悄悄接上）：

- 任何 `Stop` 事件无差别通知——会产生垃圾短信，让用户习惯性忽略。
- 只读或亚秒级命令。
- 任何紧致循环内部。

如果用户对短任务提“跑完通知我”，就老老实实做一次性的内联发送（示例 1），**不要**安装全局钩子。

### 步骤二：选择投递模式

- **一次性内联发送**——单次临时任务的默认方式。不改动任何配置。
- **`Stop` 钩子**——按需启用、限定在项目范围内，适用于用户明确希望自动通知的会话。务必加时长阈值。
- **`/loop` 或 `/schedule` 末尾 ping**——把发送追加在例程体内。

### 步骤三：撰写通知文案

- **一行、不超过约 140 字符**——能完整显示在锁屏预览里。
- **以结果开头**——✅/❌、“已完成”、“失败”、“需复核”。
- **包含可执行信息**——分支名、错误尾部、PR 编号、耗时。
- **不使用用户没要求的 emoji**——最多一个状态图标。
- **不要让智能体自我叙述**（如“我已按要求完成任务”——直接说发生了什么）。

## 示例

### 示例 1：一次性内联发送

对于单一任务，把发送追加在命令末尾。这是默认方式——不改动配置，后续也没有意外行为。

根据任务的退出状态用 `if`/`else` 分支。**不要**用 `task && send-success || send-failure` 这种链式写法：如果任务成功，但“成功发送”这一步本身返回非零，`||` 会触发失败消息——用户就会看到 ❌，哪怕任务本身已经完成。`if`/`else` 能让结果严格与任务挂钩。

```bash
if long_running_thing; then
  npx @sendblue/cli send +15551234567 "✅ done: $(date +%H:%M)"
else
  npx @sendblue/cli send +15551234567 "❌ failed: $(date +%H:%M)"
fi
```

或者，当结果本身值得一看时，可以加一行摘要：

```bash
RESULT=$(run-migration 2>&1 | tail -1)
npx @sendblue/cli send +15551234567 "migration done — $RESULT"
```

### 示例 2：Claude Code `Stop` 钩子（按需、限定范围）

在 `.claude/settings.json`（项目范围内）中注册一个 `Stop` 钩子——除非用户明确要求，否则不要写到全局配置里。实际的文件改动交给 [[update-config]] 处理。钩子命令本身应该满足：

1. 运行成本低（它在*每一次* `Stop` 时都会触发）。
2. 按时长门控——低于阈值的回合跳过发送（例如 90 秒）。
3. 永远不能让父流程失败——接 `|| true`，避免通知错误表现为钩子失败。

```bash
[ "$CLAUDE_TURN_DURATION_SECONDS" -ge 90 ] && \
  npx @sendblue/cli send "$NOTIFY_NUMBER" "turn done in ${CLAUDE_TURN_DURATION_SECONDS}s" || true
```

（环境变量名以钩子契约实际提供的为准——写配置前务必对照当前 Claude Code 钩子参考；这些命名由承载环境而非本技能决定。）

在调用 [[update-config]] 之前，把拟用的钩子配置展示给用户并获得确认。自动化外发消息一旦阈值设错，就是个隐患。

### 示例 3：`/loop` 或 `/schedule` 末尾 ping

```bash
/loop 10m "check deploy; npx @sendblue/cli send +15551234567 \"deploy: \$(deploy-status)\""
```

对 `/schedule`，例程本身可以在末尾调用 shell。同样的文案规则适用。

## 与 textme 协作

如果用户安装了 `@textme`（njerschow/textme——一个让用户*从手机给 Claude 发短信*的守护进程），通知仍然有用且不冗余。两者方向相反：

- **textme**：手机 → Claude（由用户在手机上发起）。
- **sendblue-notify**：本地 Claude → 手机（由本地会话中的 Claude 发起）。

两者可以同时安装：在服务器上装 textme 用于入站，在本地用 `Stop` 钩子挂 notify 用于出站。不同问题，同一个 Sendblue 账号。

## 最佳实践

- ✅ **默认使用一次性内联发送**处理单个任务。只有用户明确要求自动通知时，才升级到钩子。
- ✅ **按时长门控钩子**。90 秒阈值是合理的默认起点。
- ✅ **安装钩子前先把配置展示给用户**，并获取明确确认。
- ✅ **目的号码按用户存储**（环境变量或 gitignore 文件），不要放进提交的配置里。
- ❌ **不要安装全局钩子**，除非用户明确要求。默认是项目范围。
- ❌ **不要让一次失败的通知搞挂父流程**。末尾接 `|| true`。

## 限制

- 通知仅支持外发。如果要“从手机给 Claude 发短信”，请改用 `@textme` 技能。
- 在 Sendblue 免费套餐下，目的手机必须至少给 Sendblue 号码发过一条短信，外发才能成功。在依赖通知做无人值守流程之前，先用 `sendblue contacts` 验证。
- 本技能不负责凭据、账号配置或钩子配置文件格式。那些归 [[sendblue-cli]] 与 [[update-config]]。

## 安全与合规要点

- **锁屏预览会泄露内容**。任何拿着手机的人都能读到通知文案。不要把密钥、客户数据、完整错误堆栈或认证令牌塞进去。改成给出日志、看板或 PR 的链接。
- **发送或接入钩子前务必确认**。把目的号码、消息模板、触发条件与时长阈值一并预览；在执行 `sendblue send` 或改动钩子配置前，必须等待用户明确确认。
- **自动化外发是个隐患**。一个配错的 `Stop` 钩子可以一分钟发几十条消息。务必按时长门控，并在提交前用空跑证明阈值合理。
- **按用户存储号码**。目的手机号是个人标识——放在用户本地配置（环境变量、gitignore 文件）里，不要写进仓库提交文件或 CI 日志。
- **免费套餐的验证是静默的**。如果目的联系人从未发过短信，发送会返回 API 错误，但用户只会看到“短信没到”。在接入无人值守钩子前，先确认对方已发过。

## 常见坑

- **`Stop` 钩子过度热心导致的骚扰**。务必按时长门控。被每 4 秒 ping 一次的用户，一小时内就会把钩子拆掉。
- **把目的号码硬编码进提交文件**。请用环境变量或 gitignore 文件；号码是按用户而非按仓库的。
- **让一次失败的通知搞挂父流程**。钩子末尾务必接 `|| true`；失败体现在日志里，而不是中断智能体回合。
- **免费套餐联系人陷阱**。如果免费套餐账号下的目的联系人从未发过短信，发送会在用户视角静默失败。在接入无人值守钩子前用 `sendblue contacts` 验证；或用 `sendblue upgrade` 升到 AI Agent 套餐。
- **通知文案里带个人敏感信息**。锁屏预览任何拿手机的人都看得到。不要嵌入密钥、客户数据或完整错误堆栈——改成给出日志或 PR 的链接。
- **把结果埋在长文里**。如“任务完成。以下是我所做工作的摘要……”会浪费预览行。直接用 ✅/❌ 加动词打头。

## 相关技能

- `@sendblue-cli`——负责真正的发送机制。本技能调用它。
- `@sendblue-api`——面向应用代码的 HTTP 替代方案，适用于通知内嵌在长时服务里的场景。
- `@update-config`——把 `Stop` 钩子接入 `.claude/settings.json`。本技能负责“是什么、何时触发”，update-config 负责“写到哪里”。
- `@textme`——入站方向的对应物（手机 → Claude）。与 notify 搭配良好。

## 链接

- 底层 CLI：<https://github.com/sendblue-api/sendblue-cli>
- Sendblue：<https://sendblue.com>
- API 文档：<https://docs.sendblue.com>