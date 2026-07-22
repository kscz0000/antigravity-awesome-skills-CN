<div align="center">

# NotebookLM Claude Code 技能

**让 [Claude Code](https://github.com/anthropics/claude-code) 直接与 NotebookLM 对话，获取完全基于您上传文档的源文档锚定答案**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-purple.svg)](https://www.anthropic.com/news/skills)
[![Based on](https://img.shields.io/badge/Based%20on-NotebookLM%20MCP-green.svg)](https://github.com/PleasePrompto/notebooklm-mcp)
[![GitHub](https://img.shields.io/github/stars/PleasePrompto/notebooklm-skill?style=social)](https://github.com/PleasePrompto/notebooklm-skill)

> 使用此技能直接从 Claude Code 查询您的 Google NotebookLM 笔记本，获取来自 Gemini 的源文档锚定、引用支持的答案。浏览器自动化、库管理、持久认证。大幅减少幻觉 - 答案仅来自您上传的文档。

[安装](#安装) • [快速开始](#快速开始) • [为什么选择 NotebookLM](#为什么选择-notebooklm-而非本地-rag) • [工作原理](#工作原理) • [MCP 替代方案](https://github.com/PleasePrompto/notebooklm-mcp)

</div>

---

## ⚠️ 重要：仅限本地 Claude Code

**此技能仅适用于本地 [Claude Code](https://github.com/anthropics/claude-code) 安装，不适用于网页 UI。**

网页 UI 在沙盒中运行技能，没有网络访问权限，而此技能需要网络访问来进行浏览器自动化。您必须在本地机器上使用 [Claude Code](https://github.com/anthropics/claude-code)。

---

## 问题所在

当您告诉 [Claude Code](https://github.com/anthropics/claude-code)「搜索我的本地文档」时，会发生以下情况：
- **大量 token 消耗**：搜索文档意味着反复读取多个文件
- **检索不准确**：搜索关键词，错过上下文和文档间的联系
- **幻觉**：当找不到内容时，它会编造听起来合理的 API
- **手动复制粘贴**：不断在 NotebookLM 浏览器和编辑器之间切换

## 解决方案

此 Claude Code 技能让 [Claude Code](https://github.com/anthropics/claude-code) 直接与 [**NotebookLM**](https://notebooklm.google/) 对话 — Google 的**源文档锚定知识库**，由 Gemini 2.5 驱动，完全基于您上传的文档提供智能、综合的答案。

```
您的任务 → Claude 询问 NotebookLM → Gemini 综合答案 → Claude 编写正确代码
```

**不再有复制粘贴舞**：Claude 直接提问并在 CLI 中获得答案。它通过自动追问建立深度理解，获取具体的实现细节、边缘情况和最佳实践。

---

## 为什么选择 NotebookLM 而非本地 RAG？

| 方法 | Token 成本 | 设置时间 | 幻觉 | 答案质量 |
|------|-----------|---------|------|---------|
| **将文档提供给 Claude** | 🔴 很高（多次文件读取） | 即时 | 是 - 填补空白 | 检索质量不一 |
| **网页搜索** | 🟡 中等 | 即时 | 高 - 来源不可靠 | 看运气 |
| **本地 RAG** | 🟡 中高 | 数小时（嵌入、分块） | 中等 - 检索缺口 | 取决于设置 |
| **NotebookLM 技能** | 🟢 最小 | 5 分钟 | **最小** - 仅源文档锚定 | 专家级综合 |

### NotebookLM 的优势

1. **由 Gemini 预处理**：上传文档一次，即时获得专家知识
2. **自然语言问答**：不只是检索 — 真正的理解和综合
3. **多源关联**：跨 50+ 文档连接信息
4. **引用支持**：每个答案都包含来源引用
5. **无需基础设施**：无需向量数据库、嵌入或分块策略

---

## 安装

### 最简单的安装方式：

```bash
# 1. 创建技能目录（如果不存在）
mkdir -p ~/.claude/skills

# 2. 克隆此仓库
cd ~/.claude/skills
git clone https://github.com/PleasePrompto/notebooklm-skill notebooklm

# 3. 完成！打开 Claude Code 并说：
"我有哪些技能？"
```

首次使用技能时，它会自动：
- 创建隔离的 Python 环境（`.venv`）
- 安装所有依赖，包括 **Google Chrome**
- 使用 Chrome（而非 Chromium）设置浏览器自动化以获得最大可靠性
- 所有内容都包含在技能文件夹中

**注意：** 设置使用真正的 Chrome 而非 Chromium，以实现跨平台可靠性、一致的浏览器指纹识别和更好的 Google 服务反检测

---

## 快速开始

### 1. 检查您的技能

在 Claude Code 中说：
```
"我有哪些技能？"
```

Claude 将列出您的可用技能，包括 NotebookLM。

### 2. Google 认证（一次性）

```
"设置 NotebookLM 认证"
```
*Chrome 窗口打开 → 使用您的 Google 账号登录*

### 3. 创建您的知识库

访问 [notebooklm.google.com](https://notebooklm.google.com) → 创建笔记本 → 上传您的文档：
- 📄 PDF、Google Docs、Markdown 文件
- 🔗 网站、GitHub 仓库
- 🎥 YouTube 视频
- 📚 每个笔记本多个来源

分享：**⚙️ 分享 → 任何有链接的人 → 复制**

### 4. 添加到您的库

**选项 A：让 Claude 自动发现（智能添加）**
```
"查询这个笔记本的内容并将其添加到我的库：[您的链接]"
```
Claude 将自动查询笔记本以发现其内容，然后使用适当的元数据添加它。

**选项 B：手动添加**
```
"将此 NotebookLM 添加到我的库：[您的链接]"
```
Claude 将询问名称和主题，然后保存以供将来使用。

### 5. 开始研究

```
"我的 React 文档关于 hooks 说了什么？"
```

Claude 自动选择正确的笔记本并直接从 NotebookLM 获取答案。

---

## 工作原理

这是一个 **Claude Code 技能** - 一个包含 Claude Code 需要时可以使用的指令和脚本的本地文件夹。与 [MCP 服务器版本](https://github.com/PleasePrompto/notebooklm-mcp)不同，这直接在 Claude Code 中运行，无需单独的服务器。

### 与 MCP 服务器的关键区别

| 特性 | 此技能 | MCP 服务器 |
|------|--------|-----------|
| **协议** | Claude Skills | Model Context Protocol |
| **安装** | 克隆到 `~/.claude/skills` | `claude mcp add ...` |
| **会话** | 每个问题新建浏览器 | 持久聊天会话 |
| **兼容性** | 仅 Claude Code（本地） | Claude Code、Codex、Cursor 等 |
| **语言** | Python | TypeScript |
| **分发** | Git 克隆 | npm 包 |

### 架构

```
~/.claude/skills/notebooklm/
├── SKILL.md              # Claude 的指令
├── scripts/              # Python 自动化脚本
│   ├── ask_question.py   # 查询 NotebookLM
│   ├── notebook_manager.py # 库管理
│   └── auth_manager.py   # Google 认证
├── .venv/                # 隔离的 Python 环境（自动创建）
└── data/                 # 本地笔记本库
```

当您提到 NotebookLM 或发送笔记本 URL 时，Claude：
1. 加载技能指令
2. 运行适当的 Python 脚本
3. 打开浏览器，提问
4. 直接将答案返回给您
5. 使用该知识帮助您完成任务

---

## 核心功能

### **源文档锚定响应**
NotebookLM 通过完全基于您上传的文档回答来显著减少幻觉。如果信息不可用，它会表明不确定性而不是编造内容。

### **直接集成**
无需在浏览器和编辑器之间复制粘贴。Claude 以编程方式提问并接收答案。

### **智能库管理**
使用标签和描述保存 NotebookLM 链接。Claude 自动为您的任务选择正确的笔记本。

### **自动认证**
一次性 Google 登录，然后认证在会话间持久化。

### **自包含**
所有内容都在技能文件夹中运行，使用隔离的 Python 环境。无需全局安装。

### **类人自动化**
使用真实的打字速度和交互模式以避免检测。

---

## 常用命令

| 您说的话 | 发生什么 |
|---------|---------|
| *"设置 NotebookLM 认证"* | 打开 Chrome 进行 Google 登录 |
| *"将 [链接] 添加到我的 NotebookLM 库"* | 使用元数据保存笔记本 |
| *"显示我的 NotebookLM 笔记本"* | 列出所有保存的笔记本 |
| *"问我的 API 文档关于 [主题]"* | 查询相关笔记本 |
| *"使用 React 笔记本"* | 设置活动笔记本 |
| *"清除 NotebookLM 数据"* | 全新开始（保留库） |

---

## 真实示例

### 示例 1：车间手册查询

**用户问**："检查我的铃木 GSR 600 车间手册，了解刹车油类型、发动机机油规格和后轴扭矩。"

**Claude 自动**：
- 与 NotebookLM 认证
- 询问关于每个规格的全面问题
- 当提示「这就是您需要知道的全部吗？」时追问
- 提供准确规格：DOT 4 刹车油、SAE 10W-40 机油、100 N·m 后轴扭矩

![NotebookLM 聊天示例](images/example_notebookchat.png)

### 示例 2：无幻觉构建

**您**："我需要为 Gmail 垃圾邮件过滤构建 n8n 工作流。使用我的 n8n 笔记本。"

**Claude 的内部过程：**
```
→ 加载 NotebookLM 技能
→ 激活 n8n 笔记本
→ 通过追问询问全面问题
→ 从多个查询综合完整答案
```

**结果**：第一次就成功，无需调试幻觉 API。

---

## 技术细节

### 核心技术
- **Patchright**：浏览器自动化库（基于 Playwright）
- **Python**：此技能的实现语言
- **隐身技术**：类人打字和交互模式

注意：MCP 服务器使用相同的 Patchright 库，但通过 TypeScript/npm 生态系统。

### 依赖
- **patchright==1.55.2**：浏览器自动化
- **python-dotenv==1.2.2**：环境配置
- 首次使用时自动安装在 `.venv` 中

### 数据存储

所有数据本地存储在技能目录中：

```
~/.claude/skills/notebooklm/data/
├── library.json       - 您的笔记本库及元数据
├── auth_info.json     - 认证状态信息
└── browser_state/     - 浏览器 cookie 和会话数据
```

**重要安全说明：**
- `data/` 目录包含敏感的认证数据和个人笔记本
- 它通过 `.gitignore` 自动排除
- 绝不要手动提交或分享 `data/` 目录的内容

### 会话模型

与 MCP 服务器不同，此技能使用**无状态模型**：
- 每个问题打开一个新的浏览器
- 提问，获取答案
- 添加追问提示以鼓励 Claude 问更多问题
- 立即关闭浏览器

这意味着：
- 无持久聊天上下文
- 每个问题独立
- 但您的笔记本库持久化
- **追问机制**：每个答案包含「这就是您需要知道的全部吗？」以提示 Claude 进行全面追问

对于多步骤研究，Claude 在需要时自动追问。

---

## 限制

### 技能特定
- **仅本地 Claude Code** - 不适用于网页 UI（沙盒限制）
- **无会话持久化** - 每个问题独立
- **无追问上下文** - 无法引用「上一个答案」

### NotebookLM
- **速率限制** - 免费层有每日查询限制
- **手动上传** - 您必须先将文档上传到 NotebookLM
- **分享要求** - 笔记本必须公开分享

---

## 常见问题

**为什么这在 Claude 网页 UI 中不起作用？**
网页 UI 在没有网络访问的沙盒中运行技能。浏览器自动化需要网络访问才能连接 NotebookLM。

**这与 MCP 服务器有什么不同？**
这是一个更简单的、基于 Python 的实现，直接作为 Claude 技能运行。MCP 服务器功能更丰富，具有持久会话，可与多种工具（Codex、Cursor 等）配合使用。

**我可以同时使用此技能和 MCP 服务器吗？**
可以！它们服务于不同目的。使用技能进行快速 Claude Code 集成，使用 MCP 服务器进行持久会话和多工具支持。

**如果 Chrome 崩溃怎么办？**
运行：`"清除 NotebookLM 浏览器数据"` 然后重试。

**我的 Google 账号安全吗？**
Chrome 在您的机器上本地运行。您的凭据永远不会离开您的计算机。如果您担心，请使用专用的 Google 账号。

---

## 故障排除

### 找不到技能
```bash
# 确保它在正确的位置
ls ~/.claude/skills/notebooklm/
# 应该显示：SKILL.md、scripts/ 等
```

### 认证问题
说：`"重置 NotebookLM 认证"`

### 浏览器崩溃
说：`"清除 NotebookLM 浏览器数据"`

### 依赖问题
```bash
# 如需要手动重新安装
cd ~/.claude/skills/notebooklm
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # 或 Windows 上使用 .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 免责声明

此工具自动化与 NotebookLM 的浏览器交互，使您的工作流程更高效。然而，有几点友好提醒：

**关于浏览器自动化：**
虽然我内置了人性化功能（真实的打字速度、自然延迟、鼠标移动）使自动化行为更自然，但我无法保证 Google 不会检测或标记自动化使用。我建议使用专用的 Google 账号进行自动化，而不是您的主要账号——就像网页抓取一样：可能没问题，但安全总比后悔好！

**关于 CLI 工具和 AI 代理：**
Claude Code、Codex 等类似 AI 驱动助手的 CLI 工具非常强大，但它们可能会犯错。请谨慎使用并注意：
- 始终在提交或部署前审查更改
- 先在安全环境中测试
- 保留重要工作的备份
- 记住：AI 代理是助手，不是不会出错的神谕

我为自己构建了这个工具，因为我厌倦了在 NotebookLM 和编辑器之间的复制粘贴舞。我分享它是希望它也能帮助其他人，但我无法对可能发生的任何问题、数据丢失或账号问题负责。请自行判断使用。

也就是说，如果您遇到问题或有疑问，请随时在 GitHub 上提出问题。我很乐意帮助排除故障！

---

## 致谢

此技能受我的 [**NotebookLM MCP 服务器**](https://github.com/PleasePrompto/notebooklm-mcp) 启发，并作为 Claude Code 技能提供了替代实现：
- 两者都使用 Patchright 进行浏览器自动化（MCP 用 TypeScript，技能用 Python）
- 技能版本直接在 Claude Code 中运行，无需 MCP 协议
- 无状态设计针对技能架构优化

如果您需要：
- **持久会话** → 使用 [MCP 服务器](https://github.com/PleasePrompto/notebooklm-mcp)
- **多工具支持**（Codex、Cursor）→ 使用 [MCP 服务器](https://github.com/PleasePrompto/notebooklm-mcp)
- **快速 Claude Code 集成** → 使用此技能

---

## 底线

**没有此技能**：NotebookLM 在浏览器中 → 复制答案 → 粘贴到 Claude → 复制下一个问题 → 回到浏览器...

**有了此技能**：Claude 直接研究 → 即时获得答案 → 编写正确代码

停止复制粘贴舞。开始在 Claude Code 中直接获取准确、锚定的答案。

```bash
# 30 秒开始使用
cd ~/.claude/skills
git clone https://github.com/PleasePrompto/notebooklm-skill notebooklm
# 打开 Claude Code："我有哪些技能？"
```

---

<div align="center">

构建为我的 [NotebookLM MCP 服务器](https://github.com/PleasePrompto/notebooklm-mcp) 的 Claude Code 技能适配版本

用于直接在 Claude Code 中进行源文档锚定、基于文档的研究

</div>
