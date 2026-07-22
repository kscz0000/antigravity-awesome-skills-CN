---
name: context-agent
description: 会话连续性上下文代理。保存摘要、决策、待办任务，并在下次会话自动加载简报。
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- context
- session-management
- continuity
- memory
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# Context Agent

## 概述

会话连续性上下文代理。保存摘要、决策、待办任务，并在下次会话自动加载简报。

## 何时使用此技能

- 当用户提到 "salvar contexto" 或相关话题时
- 当用户提到 "salva o contexto" 或相关话题时
- 当用户提到 "proxima sessao" 或相关话题时
- 当用户提到 "briefing sessao" 或相关话题时
- 当用户提到 "resumo sessao" 或相关话题时
- 当用户提到 "continuidade sessao" 或相关话题时

## 不应使用此技能的情况

- 任务与上下文代理无关
- 更简单、更具体的工具可以处理请求
- 用户需要无领域专业知识的一般性帮助

## 工作原理

Claude Code 会话间的完美连续性。自动捕获、压缩和恢复上下文——包括话题、决策、任务、错误、修改的文件和技术发现。

## 目录结构

```
C:\Users\renat\skills\context-agent\
├── SKILL.md
├── scripts/
│   ├── config.py               # 路径和常量
│   ├── models.py               # 数据类
│   ├── session_parser.py       # Claude Code JSONL 解析器
│   ├── session_summary.py      # 摘要生成器
│   ├── active_context.py       # 管理 ACTIVE_CONTEXT.md
│   ├── project_registry.py     # 项目注册表
│   ├── compressor.py           # 压缩和归档
│   ├── search.py               # FTS5 搜索
│   ├── context_loader.py       # 加载上下文
│   └── context_manager.py      # CLI 入口点
├── references/
│   ├── context-format.md       # 格式规范
│   └── compression-rules.md    # 压缩规则
└── data/
    ├── sessions/               # session-001.md, session-002.md, ...
    ├── archive/                # 已归档会话
    ├── ACTIVE_CONTEXT.md       # 合并上下文（最多 150 行）
    ├── PROJECT_REGISTRY.md     # 所有项目状态
    └── context.db              # SQLite FTS5 用于搜索
```

## 初始化（首次使用）

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py init
```

## 保存当前会话上下文

当会话即将结束或在长任务之前，保存上下文：

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py save
```

执行操作：
1. 找到最新的会话 JSONL 文件
2. 分析所有消息、工具调用和结果
3. 生成结构化摘要（session-NNN.md）
4. 用新信息更新 ACTIVE_CONTEXT.md
5. 与 MEMORY.md 同步（加载到 system prompt）
6. 建立全文搜索索引

## 加载上下文（简报）

在新会话开始时，加载上下文：

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py load
```

生成简报，包含：活跃项目、待办任务（按优先级）、阻塞项、近期决策、约定和最近会话摘要。

## 快速状态

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py status
```

简短摘要：项目、关键待办、阻塞项。

## 搜索历史记录

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py search "rate limit"
```

在所有会话中进行全文搜索（SQLite FTS5）——话题、决策、错误、文件等。

## 维护

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py maintain
```

归档旧会话、压缩文件、重新同步 MEMORY.md、重建搜索索引。

## 工作流程

```
[会话结束]
  → save → session-NNN.md + ACTIVE_CONTEXT.md + MEMORY.md

[新会话开始]
  → MEMORY.md 已在 system prompt 中（自动）
  → load → 详细简报，包含所有需要知道的内容

[上下文增长过大]
  → maintain → 归档旧会话、压缩、优化
```

## 每次会话捕获的内容

- **话题**：讨论的主题
- **决策**：技术和架构选择
- **已完成任务**：已完成的工作
- **待办任务**：剩余工作（带优先级）
- **修改的文件**：编辑/创建的文件
- **发现**：重要的技术洞察
- **已解决的错误**：问题及其解决方案
- **未解决的问题**：待回答的问题
- **指标**：消耗的 token、消息数、工具调用数

## 与 Memory.md 集成

ACTIVE_CONTEXT.md 自动复制到：
`C:\Users\renat\.claude\projects\C--Users-renat-skills\memory\MEMORY.md`

由于 MEMORY.md 包含在每次会话的 system prompt 中，Claude 总是能知道项目的当前状态、待办任务和已做出的决策——无需任何手动操作。

## 参考资料

- 文件详细格式：`references/context-format.md`
- 压缩和归档规则：`references/compression-rules.md`

## 最佳实践

- 提供清晰、具体的项目和需求上下文
- 在应用到生产代码之前审查所有建议
- 结合其他互补技能进行全面分析

## 常见陷阱

- 将此技能用于其领域专业之外的任务
- 在不了解具体上下文的情况下应用建议
- 未提供足够的项目上下文以进行准确分析

## 相关技能

- `context-guardian` - 用于增强分析的互补技能

## 局限性
- 仅当任务明显符合上述描述的范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
