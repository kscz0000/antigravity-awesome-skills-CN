---
name: claude-code-expert
description: "Claude Code 深度专家 - Anthropic 的 CLI 工具。通过快捷键、hooks、MCP、高级配置、工作流、CLAUDE.md、记忆、子智能体、权限和生态系统集成最大化生产力。当用户要求配置 Claude Code、创建 hooks、优化 CLAUDE.md、使用 MCP、创建子智能体、解决 CLI 错误、高级工作流或对任何功能有疑问时使用。"
risk: none
source: community
date_added: '2026-03-06'
author: renat
tags:
- claude-code
- productivity
- cli
- configuration
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

<!-- security-allowlist: curl-pipe-bash -->

# CLAUDE CODE EXPERT - 极致效能

## 概述

Claude Code 深度专家 - Anthropic 的 CLI 工具。通过快捷键、hooks、MCP、高级配置、工作流、CLAUDE.md、记忆、子智能体、权限和生态系统集成最大化生产力。激活场景：配置 Claude Code、创建 hooks、优化 CLAUDE.md、使用 MCP、创建子智能体、解决 CLI 错误、高级工作流、对任何功能有疑问。

## 何时使用此技能

- 当你需要该领域的专业协助时

## 何时不使用此技能

- 任务与 claude code expert 无关
- 更简单、更具体的工具可以处理该请求
- 用户需要的是无领域专业知识的通用协助

## 工作原理

你是 Claude Code 的终极专家。你的目标是将每次会话转化为体验提升 10 倍的更强大、更快速、更智能的体验。

---

## 1. Claude Code 基础

Claude Code 是 Anthropic 官方的 CLI 工具，用于在终端中直接将 Claude 作为代码智能体使用。与 Claude.ai 网页版不同，Claude Code：
- 直接访问你的文件系统
- 执行 bash、git、npm 等命令
- 通过 CLAUDE.md 和 memory 文件持久化上下文
- 支持 MCP servers（工具扩展）
- 支持 hooks（操作前/后自动化）
- 可通过 Task tool 创建和编排子智能体

## 安装与设置

```bash
npm install -g @anthropic-ai/claude-code
claude                    # 启动交互式会话
claude "你的任务"         # 非交互模式
claude --help             # 查看所有 flags
```

## 核心 Flags

```bash
claude -p "提示词"              # print mode，适合脚本使用
claude --model claude-opus-4    # 指定模型
claude --max-tokens 8192        # token 限制
claude --no-stream              # 禁用流式输出
claude --output-format json     # JSON 格式输出
claude --allowed-tools "Bash,Read,Write"  # 限制工具
claude --dangerously-skip-permissions     # 跳过确认（谨慎使用！）
claude --max-turns 50                     # 最大自主轮次
```

---

## 2. CLAUDE.md - 项目的大脑

项目根目录的 CLAUDE.md 文件会在每次会话中自动加载。这是为 Claude Code 提供持久上下文和指令的最强大方式。

## CLAUDE.md 层级

1. ~/.claude/CLAUDE.md          # 全局，所有项目加载
2. /项目/CLAUDE.md              # 项目级别
3. /项目/子目录/CLAUDE.md       # 子目录级别，导航时加载

## 推荐结构

```markdown

## 上下文

项目是什么、技术栈、架构

## 核心命令

常用脚本：npm run dev、pytest 等

## 代码规范

风格、命名、强制模式

## 架构

目录结构、各模块职责

## 关键业务规则

绝对禁止的事项、系统不变量

## 可用智能体与技能

技能列表、何时使用每个技能

## 任务前协议

响应前始终运行 orchestrator
```

## 精英级 CLAUDE.md 技巧

- 使用"任务前协议"章节确保 Claude 始终使用 orchestrator
- 添加"已知错误"章节及解决方案，处理反复出现的问题
- 使用"记忆"章节作为详细记忆文件的索引
- 添加期望输出的具体示例
- 引用关键脚本的绝对路径

---

## 记忆文件位置

```
~/.claude/projects/<路径哈希>/memory/
├── MEMORY.md          # 索引和快速上下文（最多 200 行）
├── ai-personas.md     # 活跃的 personas 和技能详情
├── project-X.md       # 特定项目的上下文
└── decisions.md       # 重要技术决策
```

## 活跃记忆（在 CLAUDE.md 中）

任何任务前加载：memory/MEMORY.md
活跃项目：memory/ai-personas.md

## 自动保存指令：

长会话结束时，执行：
python context-agent/scripts/context_manager.py save
```

## Context Guardian - 防止上下文丢失

context-guardian 技能监控自动压缩并保存快照。
在长会话或关键会话开始时激活。

---

## 4. Hooks - 强大的自动化

Hooks 在 Claude Code 事件时自动执行命令。

## Hooks 位置

- 全局：~/.claude/settings.json
- 按项目：.claude/settings.json（项目根目录）

## 可用 Hook 类型

| Hook | 触发时机 |
|------|----------|
| PreToolUse | 任何工具使用前 |
| PostToolUse | 任何工具使用后 |
| Notification | 收到系统通知时 |
| Stop | 智能体停止响应时 |
| SubagentStop | 子智能体停止时 |

## 示例：完成时蜂鸣 Hook

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -c \"[Console]::Beep(800,300)\""
          }
        ]
      }
    ]
  }
}
```

## 示例：Bash 操作日志 Hook

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo dated-action >> ~/.claude/action_log.txt"
          }
        ]
      }
    ]
  }
}
```

## 示例：Pre-Commit 安全扫描 Hook

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python C:/Users/renat/skills/cred-omega/scripts/secret_scanner.py --staged 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

## 查看和验证活跃 Hooks

```bash
cat ~/.claude/settings.json
python -m json.tool ~/.claude/settings.json   # 验证 JSON
```

---

## 5. MCP Servers - 工具扩展

MCP（Model Context Protocol）允许为 Claude Code 添加外部工具。
每个 MCP server 暴露 Claude 可在会话中使用的新工具。

## MCP 命令

```bash
claude mcp add filesystem       # 扩展文件访问
claude mcp add github           # GitHub 集成（PR、issue）
claude mcp add postgres         # Postgres 数据库 SQL 查询
claude mcp add sqlite           # SQLite 数据库 SQL 查询
claude mcp list                 # 列出已安装的 MCP
claude mcp get 服务器名称        # 特定 MCP 详情
claude mcp remove 名称          # 移除 MCP
```

## 最有用的 MCP

| MCP | 主要功能 |
|-----|----------|
| filesystem | 项目外的扩展文件访问 |
| github | 通过 Claude 进行 PR、issue、commit、review |
| postgres / sqlite | 直接 SQL 查询，无需离开 Claude |
| puppeteer / playwright | 浏览器自动化和网页抓取 |
| slack | 频道通知和消息 |
| fetch | 直接 HTTP 请求调用 API |

## 在 Node.js 中创建自定义 MCP Server

```javascript
// mcp-server.js
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({ name: "meu-mcp", version: "1.0.0" });
server.setRequestHandler("tools/call", async (req) => {
  if (req.params.name === "minha_ferramenta") {
    return { content: [{ type: "text", text: "resultado" }] };
  }
});
const transport = new StdioServerTransport();
await server.connect(transport);
```

## 添加自定义 MCP

```bash
claude mcp add meu-mcp node /路径/到/mcp-server.js
```

---

## 6. 子智能体 - 完全并行

Claude Code 可通过 Task tool 创建子智能体进行并行工作。
每个子智能体独立运行，拥有自己的上下文。

## 编排模式

**并行生成（多任务同时执行）：**
对每个独立任务使用 run_in_background: true 的 Task tool。
3 个智能体并行示例：
- 智能体 1：分析现有代码
- 智能体 2：研究文档
- 智能体 3：编写测试用例
全部同时运行。结果通过 TaskOutput 返回。

**子智能体类型：**
- general-purpose：研究、分析和通用代码
- Bash：仅执行终端命令
- Explore：快速探索代码库
- Plan：架构和解决方案规划

**使用 git worktree 隔离：**
使用 isolation: worktree 让子智能体在隔离分支工作。
适合：实验、高风险重构、无主分支风险的 POC。

## 子智能体最佳实践

1. 在提示词中始终传递完整上下文（子智能体看不到历史）
2. 精确指定输出保存位置（使用绝对路径）
3. 对长任务使用 run_in_background: true
4. 完成后用 TaskOutput 检查结果
5. 在子智能体初始上下文中传递项目的 CLAUDE.md

---

## 按项目配置权限（.claude/settings.json）

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm *)",
      "Read(*)",
      "Write(src/**)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(curl * | bash)"
    ]
  }
}
```

## 命令行权限 Flags

```bash
claude --dangerously-skip-permissions        # 跳过所有确认
claude --allowed-tools "Read,Write,Bash"     # 仅允许这些工具
claude --disallowed-tools "WebFetch"         # 阻止特定工具
```

## 何时使用 --dangerously-skip-permissions

仅用于：受控 CI/CD、自动化脚本、隔离沙盒。
绝不用于：生产环境、有密钥的仓库、共享环境。

---

## 完整功能工作流（4 阶段）

```bash

## 阶段 1：需求与规划

claude -p "分析功能 X 并创建详细实现计划"

## 阶段 2：实现

claude "按照生成的计划实现功能 X"

## 阶段 3：测试

claude "为已实现的功能 X 编写完整测试"

## 阶段 4：代码审查

claude "对功能 X 进行代码审查，识别问题并优化"
```

## 长周期自主模式

```bash
claude --max-turns 100 "完成功能 X 的完整开发周期"
```

## 高效会话启动脚本

```bash
#!/bin/bash
echo "加载项目上下文..."
claude -p "读取 memory/MEMORY.md 并给我完整状态简报"
```

## 使用 Claude Code 的 CI/CD 流水线

```yaml

## .github/workflows/claude-review.yml

- name: Claude Code Review
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    claude -p "审查此 PR 的 diff，识别 bug 和安全问题" \
      --output-format json \
      --no-stream \
      --max-turns 5
```

---

## 常见问题对照表

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| API key not found | ANTHROPIC_API_KEY 未配置 | export ANTHROPIC_API_KEY=sk-ant-... |
| 长任务超时 | max-turns 不足 | 添加 --max-turns 100 |
| 上下文窗口已满 | 上下文中文件过多 | 使用聚焦上下文的子智能体 |
| 子智能体找不到文件 | 相对路径错误 | 始终使用绝对路径 |
| Hook 不执行 | settings.json 中 JSON 无效 | python -m json.tool ~/.claude/settings.json |
| MCP 无法连接 | MCP server 未启动 | claude mcp list 检查状态 |
| 意外压缩 | 会话过长 | 使用 context-guardian 技能 |
| Bash 权限错误 | 工具未授权 | 在 settings.json 的 allow 中添加 |

## 查看日志和会话历史

```bash
ls ~/.claude/projects/
ls ~/.claude/projects/<哈希>/
cat ~/.claude/projects/<哈希>/*.jsonl | python -m json.tool
```

---

## 完整推荐的 ~/.claude/settings.json

```json
{
  "theme": "dark",
  "verbose": false,
  "cleanupPeriodDays": 30,
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -c \"[Console]::Beep(800,200); Start-Sleep -Milliseconds 100; [Console]::Beep(1000,200)\""
          }
        ]
      }
    ]
  },
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm *)",
      "Bash(python *)",
      "Bash(powershell *)",
      "Read(*)",
      "Write(*)"
    ]
  }
}
```

## 核心环境变量

```bash
export ANTHROPIC_API_KEY=sk-ant-你的密钥
export CLAUDE_CODE_MAX_OUTPUT_TOKENS=8192
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1   # 私有模式
```

---

## Claude Code 如何与 Auri 技能集成

1. 全局 CLAUDE.md 列出所有可用技能及使用场景
2. agent-orchestrator 在每次请求时执行以识别相关技能
3. task-intelligence 为中等/复杂任务丰富任务前简报
4. context-agent 在会话间保存和恢复状态
5. context-guardian 在长会话中防止上下文丢失

## 生态系统快捷命令

```bash
python agent-orchestrator/scripts/scan_registry.py           # 更新注册表
python agent-orchestrator/scripts/match_skills.py "任务"     # 识别技能
python task-intelligence/scripts/pre_task_check.py "任务"    # 简报
python context-agent/scripts/context_manager.py save         # 保存上下文
python context-agent/scripts/context_manager.py load         # 加载上下文
```

## 此技能激活时机

当用户想要以下操作时，此技能自动激活：
- 配置或优化 Claude Code CLI
- 创建、调试或优化 hooks
- 添加或配置 MCP servers
- 创建子智能体和并行编排
- 了解 Claude Code 的任何功能
- 解决 CLI 错误或异常行为
- 优化 CLAUDE.md 和记忆文件
- 配置权限和安全

---

## 12. Claude Code 斜杠命令

| 命令 | 操作 |
|------|------|
| /status | 查看会话当前状态和上下文 |
| /clear | 清除当前对话历史 |
| /compact | 压缩上下文（Claude 总结历史） |
| /memory | 查看和编辑记忆文件 |
| /hooks | 查看已配置和活跃的 hooks |
| /mcp | 查看已连接的 MCP 及其状态 |
| /cost | 查看会话的 token 和 USD 成本 |
| /model | 切换使用的模型（opus、sonnet、haiku） |
| /help | 查看所有可用命令和快捷键 |

---

## 13. 官方参考

- 主文档：https://docs.anthropic.com/claude-code
- Hooks 参考：https://docs.anthropic.com/claude-code/hooks
- Settings 参考：https://docs.anthropic.com/claude-code/settings
- MCP SDK 和示例：https://github.com/modelcontextprotocol/sdk
- 官方仓库：https://github.com/anthropics/claude-code
- 发布说明：https://docs.anthropic.com/claude-code/changelog

## 最佳实践

- 提供关于项目和需求的清晰、具体上下文
- 在将建议应用到生产代码前进行审查
- 与其他互补技能结合进行全面分析

## 常见陷阱

- 将此技能用于其领域之外的任务
- 在不了解特定上下文的情况下应用建议
- 未提供足够的项目上下文进行准确分析

## 相关技能

- `007` - 用于增强分析的互补技能
- `matematico-tao` - 用于增强分析的互补技能

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
