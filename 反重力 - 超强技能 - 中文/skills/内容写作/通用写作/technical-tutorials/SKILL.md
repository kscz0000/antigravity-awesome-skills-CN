---
name: technical-tutorials
description: 当用户想要创建逐步技术教程、快速入门或代码走读时使用。触发短语包括"教程"、"快速入门"、"上手指南"、"走读"、"step by step"、"how to guide"、"hands-on guide"或"code tutorial"。
risk: unknown
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/technical-tutorials
source_repo: jonathimer/devmarketing-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/jonathimer/devmarketing-skills/blob/main/LICENSE
---

# 技术教程
## 何时使用

当用户想要创建逐步技术教程、快速入门或代码走读时使用本技能。触发短语包括"教程"、"快速入门"、"上手指南"、"走读"、"step by step"、"how to guide"、"hands-on guide"或"code tutorial"。


本技能帮你创建真正能跑通的逐步教程。涵盖前置条件处理、渐进式复杂度、故障排查章节，以及打造令人满足的"它跑起来了！"瞬间。

---

## 开始之前

**先加载你的受众上下文。** 阅读 `.agents/developer-audience-context.md` 以了解：

- 开发者技能水平（初级、中级、高级）
- 技术栈熟悉度（你可以假设他们懂什么？）
- 运行环境（macOS、Linux、Windows、云）
- 他们学习的目的（工作、副业项目、好奇心）

如果该上下文文件不存在，请先运行 `developer-audience-context` 技能。

---

## 教程类型

| 类型 | 时长 | 用途 | 示例 |
|------|--------|---------|---------|
| **快速入门** | 5-10 分钟 | 尽快获得首次成功 | "发起你的第一次 API 调用" |
| **教程** | 20-45 分钟 | 深入学习一个概念 | "用 Node.js 构建 REST API" |
| **实战课** | 1-3 小时 | 综合性项目 | "构建一个全栈应用" |
| **代码走读** | 时长不定 | 讲解已有代码 | "理解我们的 SDK 架构" |

---

## 教程结构

### 优秀教程的解剖

```
1. Title & Meta
   - What you'll build
   - Time estimate
   - Prerequisites

2. Overview
   - What you'll learn
   - Final result preview

3. Prerequisites Check
   - Environment setup
   - Verification commands

4. The Build (Progressive Steps)
   - Step 1: Simplest foundation
   - Step 2: Add one concept
   - Step 3: Add complexity
   - [Checkpoint: "It works!" moment]
   - Step 4: Continue building
   - ...
   - [Final checkpoint]

5. What You Built
   - Recap
   - Complete code

6. Troubleshooting
   - Common errors
   - Debugging tips

7. Next Steps
   - Where to go from here
   - Related tutorials
```

---

## 前置条件处理

### 前置条件章节

要明确。不要让开发者去猜他们需要什么。

```markdown
## Prerequisites

Before starting, make sure you have:

| Requirement | Version | Check Command |
|-------------|---------|---------------|
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Git | Any | `git --version` |

You should also be comfortable with:
- Basic JavaScript (variables, functions, async/await)
- Command line basics (cd, mkdir, running commands)
- REST API concepts (HTTP methods, JSON)

**New to any of these?** Check out [link to prerequisite tutorial].
```

### 环境设置章节

让设置过程万无一失：

```markdown
## Setting Up Your Environment

### 1. Create Project Directory

\`\`\`bash
mkdir my-awesome-project
cd my-awesome-project
\`\`\`

### 2. Initialize the Project

\`\`\`bash
npm init -y
\`\`\`

You should see output like:
\`\`\`json
{
  "name": "my-awesome-project",
  "version": "1.0.0",
  ...
}
\`\`\`

### 3. Install Dependencies

\`\`\`bash
npm install express dotenv
\`\`\`

### 4. Verify Installation

\`\`\`bash
node -e "require('express'); console.log('Express installed!')"
\`\`\`

Expected output: `Express installed!`
```

---

## 渐进式复杂度

### 分层蛋糕方法

以可理解的层级逐步构建：

| 层级 | 作用 | 示例 |
|-------|--------------|---------|
| **1. 骨架** | 能跑的最小代码 | "Hello World" 服务器 |
| **2. 核心功能** | 主要功能 | 加入一个 API 端点 |
| **3. 真实数据** | 替换硬编码值 | 连接数据库 |
| **4. 错误处理** | 生产级模式 | 加入 try/catch、参数校验 |
| **5. 打磨** | 锦上添花 | 日志、配置、测试 |

### 展示进度，而非完美

**错误做法**（让人窒息）：
```javascript
// Here's the complete file with everything
const express = require('express');
const { Pool } = require('pg');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const winston = require('winston');
// ... 200 more lines
```

**正确做法**（渐进式）：

**第 1 步：基础服务器**
```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
```

**第 2 步：加入你的第一个路由**
```javascript
// Add this below your existing route
app.get('/api/users', (req, res) => {
  res.json([{ id: 1, name: 'Jane' }]);
});
```

---

## 可直接复制粘贴的代码

### 复制粘贴检查表

每个代码块都必须通过以下测试：

| 测试 | 如何验证 |
|------|---------------|
| **可独立运行** | 复制到新文件，执行，能跑通 |
| **包含 import** | 所有 `require`/`import` 语句齐全 |
| **无未定义变量** | 不引用其他步骤的代码而未展示 |
| **环境无关** | 在 Mac/Linux/Windows 都能用 |
| **注释解释为什么** | 而非是什么（代码本身说明是什么） |

### 代码块模式

**文件上下文至关重要：**

```javascript
// server.js - Add this to your existing file
const rateLimit = require('express-rate-limit');

// Add this BEFORE your routes
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per window
});

app.use(limiter);
```

**展示文件结构：**

```
my-project/
├── src/
│   ├── index.js      ← You're editing this
│   ├── routes/
│   │   └── users.js
│   └── db/
│       └── connection.js
├── package.json
└── .env
```

**在上下文中高亮变更：**

```javascript
// src/index.js
const express = require('express');
const app = express();

// ✅ ADD THIS: Import your new route
const userRoutes = require('./routes/users');

// ✅ ADD THIS: Use the route
app.use('/api/users', userRoutes);

app.listen(3000);
```

---

## "它跑起来了！"瞬间

### 检查点创造动力

每 3-5 步，给开发者一个小胜利：

```markdown
## Checkpoint: Test Your API

Let's make sure everything works before continuing.

**Start your server:**
\`\`\`bash
node server.js
\`\`\`

**In a new terminal, test the endpoint:**
\`\`\`bash
curl http://localhost:3000/api/users
\`\`\`

**You should see:**
\`\`\`json
[{"id": 1, "name": "Jane"}]
\`\`\`

🎉 **It works!** Your API is returning data.

If you don't see this output, check the [Troubleshooting](#troubleshooting) section.
```

### 可视化确认

在可能的情况下，展示成功的样貌：

| 输出类型 | 如何展示 |
|-------------|-------------|
| **终端输出** | 带预期文本的代码块 |
| **浏览器结果** | 截图或文字描述 |
| **API 响应** | 格式化后的 JSON |
| **日志** | 含日志输出的代码块 |

---

## 故障排查章节

### 常见错误模板

```markdown
## Troubleshooting

### "Error: Cannot find module 'express'"

**Cause:** Dependencies weren't installed.

**Fix:**
\`\`\`bash
npm install
\`\`\`

---

### "EADDRINUSE: address already in use :::3000"

**Cause:** Another process is using port 3000.

**Fix (macOS/Linux):**
\`\`\`bash
# Find the process
lsof -i :3000

# Kill it (replace PID with actual number)
kill -9 PID
\`\`\`

**Or use a different port:**
\`\`\`javascript
app.listen(process.env.PORT || 3001);
\`\`\`

---

### "SyntaxError: Unexpected token"

**Cause:** Likely a typo or missing bracket.

**Debug steps:**
1. Check the line number in the error
2. Look for missing `,`, `}`, or `)`
3. Verify all strings are closed with matching quotes
```

### 主动预防错误

在常见坑前加入警告：

```markdown
⚠️ **Windows users:** Use `set` instead of `export`:
\`\`\`bash
# macOS/Linux
export API_KEY=your_key

# Windows Command Prompt
set API_KEY=your_key

# Windows PowerShell
$env:API_KEY="your_key"
\`\`\`
```

---

## 教程模板

### 快速入门模板（5-10 分钟）

```markdown
# [Product] Quickstart: [What You'll Do] in 5 Minutes

Get [specific outcome] in under 5 minutes.

## Prerequisites

- [Requirement 1]
- [Requirement 2]

## Step 1: Install

\`\`\`bash
npm install your-package
\`\`\`

## Step 2: Configure

Create a `.env` file:
\`\`\`
API_KEY=your_key_here
\`\`\`

## Step 3: Write Code

Create `index.js`:
\`\`\`javascript
// Complete, working code
\`\`\`

## Step 4: Run It

\`\`\`bash
node index.js
\`\`\`

Expected output:
\`\`\`
[Output here]
\`\`\`

## 🎉 You Did It!

You just [accomplished thing].

**Next steps:**
- [Link to full tutorial]
- [Link to API docs]
- [Link to examples repo]
```

### 完整教程模板（20-45 分钟）

```markdown
# Build a [Thing] with [Technology]

Learn how to [outcome] by building [specific project].

| | |
|---|---|
| **Time** | 30 minutes |
| **Level** | Intermediate |
| **Prerequisites** | Node.js 18+, basic JavaScript |

## What You'll Build

[Screenshot or diagram of final result]

By the end, you'll have:
- ✅ [Capability 1]
- ✅ [Capability 2]
- ✅ [Capability 3]

## Prerequisites

### Required Software

| Tool | Version | Verify |
|------|---------|--------|
| Node.js | 18+ | `node -v` |

### Required Knowledge

- [Concept 1] — [link to learn]
- [Concept 2] — [link to learn]

## Step 1: Project Setup

[Setup instructions with verification]

**Checkpoint:** You should see `[expected output]`.

## Step 2: [First Feature]

[Instructions]

**Checkpoint:** Test with `[command]`.

## Step 3: [Second Feature]

[Instructions]

## Step 4: [Third Feature]

[Instructions]

**Checkpoint:** Your app should now [do thing].

## Complete Code

Here's everything together:

\`\`\`javascript
// Full final code
\`\`\`

## Troubleshooting

### [Common Error 1]
[Solution]

### [Common Error 2]
[Solution]

## What You Learned

- [Key concept 1]
- [Key concept 2]
- [Key concept 3]

## Next Steps

- **Go deeper:** [Link to advanced tutorial]
- **Explore:** [Link to related feature]
- **Get help:** [Link to Discord/community]
```

---

## 质量检查表

发布前请验证：

### 代码质量
- [ ] 每个代码块无需修改即可运行
- [ ] 所有 import/require 均已包含
- [ ] 展示了预期输出
- [ ] 包含错误处理
- [ ] 环境变量使用 `.env` 模式

### 结构质量
- [ ] 前置条件明确列出
- [ ] 时长预估准确（自己测一下！）
- [ ] 每 3-5 步一个检查点
- [ ] 提供了最终完整代码
- [ ] 故障排查覆盖可能的错误

### 可访问性
- [ ] 在 Mac、Linux 与 Windows 上均可运行
- [ ] 命令在 bash/zsh/PowerShell 中均可用
- [ ] 文件路径使用正确的分隔符
- [ ] 不对已安装的工具做假设

---

## 工具

| 工具 | 用途 |
|------|----------|
| **[Octolens](https://octolens.com)** | 查找开发者常问的常见问题与错误。监控 Stack Overflow 与 GitHub issues 以获取故障排查素材。 |
| **Replit/CodeSandbox** | 嵌入可运行示例 |
| **Carbon/Ray.so** | 美观的代码截图 |
| **Excalidraw** | 架构图 |
| **Terminalizer** | 录制终端会话 |
| **Loom** | 快速视频补充 |

---

## 相关技能

- `developer-audience-context` — 了解技能水平与运行环境
- `devrel-content` — 通用技术写作原则
- `developer-onboarding` — 优化首次成功的时间
- `developer-seo` — 让教程被搜索发现

## 限制

- 仅在任务明确匹配上游来源与本地项目上下文时使用本技能。
- 在应用变更前，请验证命令、生成的代码、依赖、凭证以及外部服务的行为。
- 不要将示例当作针对特定环境的测试、安全审查或用户对破坏性/高成本操作的审批的替代品。