---
name: docs-as-marketing
description: 将文档打造成一个强大的营销渠道，吸引、转化并留住开发者。本技能涵盖如何撰写在搜索中排名靠前、把访客转化为用户，并通过卓越的信息架构加速采用的文档。触发词：开发者文档、信息架构、快速上手、API 参考、文档 SEO、开发者获客、文档驱动增长、自助支持。
risk: unknown
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/docs-as-marketing
source_repo: jonathimer/devmarketing-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/jonathimer/devmarketing-skills/blob/main/LICENSE
---

# 文档即营销
## 何时使用

当你需要把文档打造成一个强大的营销渠道，用以吸引、转化并留住开发者时，请使用本技能。本技能涵盖如何撰写在搜索中排名靠前、把访客转化为用户，并通过卓越的信息架构加速采用的文档。


文档往往是开发者与你的产品之间第一次有意义的接触。优秀的文档不只是解释——它本身就是营销。它降低摩擦、建立信任，并把充满好奇的访客变成会主动向他人推荐你产品的活跃用户。

## 概览

开发者文档承担着多重营销职能：
- **获客**：文档在搜索中获得排名，吸引正在主动寻找解决方案的开发者
- **激活**：结构良好的快速上手可缩短价值达成时间
- **留存**：完整的参考让开发者持续构建
- **转介绍**：开发者分享的是他们喜爱的文档，而不是营销页面

本技能聚焦于技术写作与开发者营销的交叉地带——撰写同时服务于"教育"与"转化"目标的文档。

## 动手之前

先回顾 **developer-audience-context** 技能，了解你的目标开发者：
- 他们正在搜索哪些问题的解决方案？
- 他们的技术水平如何？
- 他们使用哪些框架和语言？
- 他们目前在哪里寻找答案？

你的文档策略应当直接回应这些受众洞察。

## 可转化的信息架构

### 四类文档

围绕开发者真正需要的四类文档来组织内容：

| 类型 | 目的 | 营销职能 |
|------|---------|-------------------|
| **教程（Tutorials）** | 面向学习，循序渐进 | 建立信心，展示产品价值 |
| **操作指南（How-to Guides）** | 面向任务，解决问题 | 展现产品能力广度 |
| **参考（Reference）** | 面向信息，准确无误 | 证明产品深度与可靠性 |
| **解释（Explanation）** | 面向理解，传递概念 | 建立思想领导力 |

### 降低跳出率的导航

**良好的导航结构：**
```
Getting Started
├── Quickstart (< 5 min)
├── Installation
└── Core Concepts

Guides
├── Authentication
├── [Most Common Use Case]
├── [Second Most Common Use Case]
└── ...

API Reference
├── Overview
├── Authentication
├── Endpoints (alphabetical or logical grouping)
└── SDKs

Resources
├── Examples
├── Changelog
└── Support
```

**糟糕的导航结构：**
```
Documentation
├── Chapter 1: Introduction
├── Chapter 2: Getting Started
├── Chapter 3: Advanced Topics
├── Appendix A
└── API (link to separate site)
```

### 信息层次

每个文档页面都应遵循这样的层次：
1. 这是**什么**？（1 句话）
2. 我为什么**要用它**？（1-2 句话）
3. 我**怎么用**？（页面的主体内容）
4. **接下来**做什么？（清晰的下一步指引）

## 快速上手优化

你的快速上手是最重要的转化页面。要毫不留情地优化它。

### 5 分钟法则

开发者应在 5 分钟内达到一个有意义的成功时刻。如果你的快速上手要花更长时间，你正在失去他们。

**度量与优化：**
- 从页面加载到首次成功 API 调用的时间
- 快速上手流程中的流失节点
- 完成率

### 快速上手的结构

```markdown
# Quickstart

Get your first [meaningful result] in under 5 minutes.

## Prerequisites
- [Specific version] of [language/tool]
- [Account/API key] (link to signup)

## Step 1: Install
[Single command, copy-paste ready]

## Step 2: Configure
[Minimal configuration, explain what each part does]

## Step 3: Run
[The payoff—show them it works]

## What You Built
[Explain what just happened and why it matters]

## Next Steps
- [Immediate next tutorial]
- [Reference docs for what they just used]
- [Community/support link]
```

### 好的 vs. 糟糕的快速上手

**好的快速上手：**
```markdown
# Send Your First Message

Send an SMS in under 5 minutes.

## Prerequisites
- Node.js 16 or higher
- A Twilio account ([sign up free](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/docs-as-marketing/link))

## Install the SDK
```bash
npm install twilio
```

## Send a Message
Create `send-sms.js`:
```javascript
const twilio = require('twilio');
const client = twilio('YOUR_ACCOUNT_SID', 'YOUR_AUTH_TOKEN');

client.messages.create({
  body: 'Hello from my app!',
  to: '+15551234567',
  from: '+15559876543'
}).then(message => console.log(`Sent: ${message.sid}`));
```

Run it:
```bash
node send-sms.js
```

You should see: `Sent: SM1234...`

## What Just Happened
You authenticated with your API credentials and sent an SMS...
```

**糟糕的快速上手：**
```markdown
# Getting Started

Welcome to our platform! Before we begin, let's discuss
the architecture of our messaging system...

[500 words of background]

## Installation

First, ensure you have the correct version of Node.js.
You can check this by running...

[200 words on version checking]

You'll also need to configure your environment variables.
Create a .env file and add the following variables...

[Complex configuration with 10+ variables]
```

## API 参考最佳实践

### 每个接口都应具备

1. 一句话**功能描述**
2. **认证要求**清晰列出
3. **请求格式**，所有参数都有说明
4. **响应格式**，附示例
5. **错误响应**，列出常见原因
6. **可复制粘贴的示例**，且确实能跑通

### 可复制粘贴且能跑的代码

**关键**：示例代码复制后必须能运行。请实际测试一遍。

**好的示例：**
```markdown
## Create a User

Creates a new user in your organization.

### Request
```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "developer@example.com",
    "name": "Jane Developer"
  }'
```

### Response
```json
{
  "id": "usr_123abc",
  "email": "developer@example.com",
  "name": "Jane Developer",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Errors
| Code | Meaning |
|------|---------|
| 400 | Invalid email format |
| 409 | Email already exists |
| 401 | Invalid or missing API key |
```

**糟糕的示例：**
```markdown
## POST /users

Parameters:
- email (string)
- name (string)
- org_id (string, optional)
- role (enum, optional)
- metadata (object, optional)
- ...

Returns a user object.
```

### 针对不同语言的示例

提供你的开发者真正使用的语言示例：
- cURL（通用，始终包含）
- JavaScript/Node.js
- Python
- Go
- Ruby
- PHP
- 你用得最多的 SDK 语言

## 面向文档的搜索优化

### 能排上名的文档

开发者文档能捕获高意向的搜索流量。

**重点查询类型：**
1. **问题型查询**："how to send sms from node.js"
2. **对比型查询**："[your product] vs [competitor]"
3. **集成型查询**："integrate [your product] with [popular tool]"
4. **错误型查询**："[specific error message]"

### 文档的 SEO 基础

**页面标题：**
```
Good: "Send SMS with Node.js | Twilio Docs"
Bad: "Documentation - Messaging - SMS - Send"
```

**Meta 描述：**
```
Good: "Learn how to send SMS messages using Node.js and the
Twilio API. Includes code examples and troubleshooting tips."

Bad: "This page contains documentation for the SMS sending
functionality of our messaging product."
```

**URL 结构：**
```
Good: /docs/sms/send-messages/nodejs
Bad: /docs/section/3/page/27?lang=nodejs
```

### 内链建设

打造一张文档网，而不是一个个文档孤岛：
- 互链相关概念
- 从参考文档链接到教程
- 从教程链接到参考文档
- 在不同 SDK 文档之间交叉链接

## 度量文档效果

### 关键指标

| 指标 | 它能告诉你什么 |
|--------|------------------|
| 在快速上手页的停留时长 | 参与度（也可能是困惑度） |
| 快速上手完成率 | 转化效果 |
| 搜索 → 注册的转化率 | 文档作为获客渠道的能力 |
| 工单分流率 | 文档完备程度 |
| 页面评分/反馈 | 内容质量 |
| 站内搜索查询 | 内容缺口 |

### 反馈闭环

**实施：**
- 在每个页面加上"本页是否有帮助"
- 站内搜索分析（大家在搜什么？）
- 工单分析（哪些问题是文档没回答好的？）
- 开发者访谈（哪里让人困惑？还缺什么？）

## 常见的文档反模式

### "一堵文字墙"
**问题**：页面里没有代码、没有结构、没有任何视觉断点
**解法**：以代码打头，大量使用小标题，把段落切短

### "假设你已经懂了"的陷阱
**问题**：默认开发者懂得你的术语
**解法**：首次出现的术语给定义，链到术语表

### "万能页面"
**问题**：一个页面试图覆盖所有用例
**解法**：按不同任务拆分页面，并在它们之间互链

### "过时的快速上手"
**问题**：快速上手里的代码已经跑不通了
**解法**：对文档中的代码示例做自动化测试

### "藏起来的前置条件"
**问题**：到了教程中途才发现还需要某些条件
**解法**：把全部前置条件放在开头，并标明版本号

## 工具

### 文档平台
- **GitBook**：适合小团队，默认设置就不错
- **ReadMe**：交互式 API 文档，内置指标
- **Mintlify**：现代、快速，DX 出色
- **Docusaurus**：灵活、自托管，基于 React
- **Notion**：上手快，但定制能力有限

### 代码示例测试
- **Doctest**：Python 文档中的代码
- **mdx-js**：Markdown 中的 JSX
- **Custom CI**：把代码示例当作测试来运行

### 搜索与分析
- **Algolia DocSearch**：开源项目免费，功能强大
- **Google Analytics**：基础流量指标
- **FullStory/Hotjar**：会话录制与热力图
- **Internal search analytics**：开发者在站内搜什么？

## 相关技能

- **api-onboarding**：优化从零到首次 API 调用的完整体验
- **sdk-dx**：设计让文档更简单的 SDK
- **developer-sandbox**：与文档互补的交互式演练环境
- **technical-content-strategy**：涵盖文档在内的更广泛内容策略
- **developer-audience-context**：理解你正在为谁写作

## 使用边界

- 仅在任务与上游来源及本地项目上下文明确匹配时使用本技能。
- 在落地修改前，请先核实命令、生成的代码、依赖、凭证以及外部服务行为。
- 不要把示例当成环境专项测试、安全审查或破坏性/高成本操作的用户审批的替代品。