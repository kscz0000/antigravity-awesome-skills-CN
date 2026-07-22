---
name: hierarchical-agent-memory
description: "分层作用域 CLAUDE.md 记忆系统，减少上下文 token 消耗。创建目录级上下文文件，通过仪表盘追踪节省量，并将智能体路由到正确的子上下文。当用户要求'减少 token 消耗'、'分层记忆'、'目录级上下文'、'HAM'、'hierarchical agent memory'时使用。"
risk: safe
source: "https://github.com/kromahlusenii-ops/ham"
date_added: "2026-02-27"
---

# Hierarchical Agent Memory (HAM)

分层作用域记忆系统，为 AI 编码智能体提供每个目录的速查表，而非每次提示都重读整个项目。根 CLAUDE.md 保存全局上下文（约 200 tokens），子目录 CLAUDE.md 文件保存作用域上下文（每个约 250 tokens），`.memory/` 层存储决策、模式和待确认推断的收件箱。

## 何时使用此技能

- 想要减少 Claude Code 会话中的输入 token 成本时
- 项目有 3 个以上目录，智能体反复重读相同文件时
- 想要目录作用域上下文而非单一庞大的 CLAUDE.md 时
- 想要仪表盘可视化 token 节省、会话历史和上下文健康度时
- 启动新项目并希望从第一天就有结构化智能体记忆时

## 工作原理

### 步骤 1：设置（"go ham"）

自动检测项目平台和成熟度，然后生成记忆结构：

```
project/
├── CLAUDE.md              # 根上下文 (~200 tokens)
├── .memory/
│   ├── decisions.md       # 架构决策记录
│   ├── patterns.md        # 可复用模式
│   ├── inbox.md           # 待确认的推断项
│   └── audit-log.md       # 审计历史
└── src/
    ├── api/CLAUDE.md      # api/ 的作用域上下文
    ├── components/CLAUDE.md
    └── lib/CLAUDE.md
```

### 步骤 2：上下文路由

根 CLAUDE.md 包含一个路由部分，明确告诉智能体加载哪个子上下文：

```markdown
## Context Routing

→ api: src/api/CLAUDE.md
→ components: src/components/CLAUDE.md
→ lib: src/lib/CLAUDE.md
```

智能体读取根文件后，立即加载相关子目录上下文——无需猜测。

### 步骤 3：仪表盘（"ham dashboard"）

在 localhost:7777 启动 Web 仪表盘，可视化展示：
- Token 节省（启用 HAM vs 未启用 HAM 会话）
- 每日 token 和成本趋势
- 按目录的会话分解
- 上下文文件健康度（缺失/过期/继承的 CLAUDE.md 覆盖率）
- 路由合规性（智能体遵循路由图的频率）
- 碳排放/能耗估算

## 命令

| 触发词 | 功能 |
|---|---|
| `go ham` | 设置 HAM — 自动检测平台，生成 CLAUDE.md 文件 |
| `ham savings` | 显示 token 和成本节省报告 |
| `ham dashboard` | 启动交互式 Web 仪表盘 |
| `ham audit` | 记忆文件健康检查 |
| `ham insights` | 从会话数据生成可操作洞察 |
| `ham route` | 在根 CLAUDE.md 中添加/更新 Context Routing 部分 |
| `ham carbon` | 显示能耗和碳排放效率数据 |

## 示例

### 示例 1：首次设置

```
User: go ham

Agent: HAM setup complete. Created 8 files.
  - CLAUDE.md (root)
  - .memory/decisions.md
  - .memory/patterns.md
  - .memory/inbox.md
  - src/api/CLAUDE.md
  - src/components/CLAUDE.md
  - src/lib/CLAUDE.md
  - src/utils/CLAUDE.md

Baseline captured in .memory/baseline.json
Run "HAM savings" to see your token and cost savings.
```

### 示例 2：查看节省

```
User: ham savings

Agent:
  Before HAM: ~7,500 tokens/prompt
  After HAM:    ~450 tokens/prompt
  Savings:    7,050 tokens (94%)

  Monthly projection (1,500 prompts):
    Sonnet: ~$31.73 saved
    Opus:   ~$158.63 saved
```

## 最佳实践

- 根 CLAUDE.md 保持在 60 行 / 250 tokens 以内
- 子目录 CLAUDE.md 文件每个保持在 75 行以内
- 每两周运行 `ham audit` 检查过期或缺失的上下文文件
- 添加新目录后使用 `ham route` 保持路由最新
- 定期检查 `.memory/inbox.md` — 确认或拒绝推断项

## 限制

- Token 估算使用约 4 字符 = 1 token 的近似值，非真实分词器
- 基线节省对比基于典型智能体行为的估算
- 仪表盘需要 Node.js 18+，从 `~/.claude/projects/` 读取会话数据
- 上下文路由检测依赖会话 JSONL 文件中 CLAUDE.md 的读取顺序
- 不会自动更新子目录 CLAUDE.md 内容 — 需手动维护或通过 `ham audit`
- 碳排放估算使用区域电网平均值，非实时能耗数据

## 相关技能

- `agent-memory-systems` — 通用智能体记忆架构模式
- `agent-memory-mcp` — 基于 MCP 的记忆集成
