---
name: context-guardian
description: 上下文守护者，在自动压缩前保护关键数据。支持快照、完整性验证和零信息丢失。
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- context
- data-integrity
- snapshots
- verification
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# Context Guardian

## 概述

上下文守护者，在自动压缩前保护关键数据。支持快照、完整性验证和零信息丢失。

## 何时使用此技能

- 当用户提到 "compactacao contexto" 或相关主题时
- 当用户提到 "perda de contexto" 或相关主题时
- 当用户提到 "snapshot contexto" 或相关主题时
- 当用户提到 "preservar contexto" 或相关主题时
- 当用户提到 "contexto critico" 或相关主题时
- 当用户提到 "antes de compactar" 或相关主题时

## 何时不使用此技能

- 任务与上下文守护无关
- 更简单、更具体的工具可以处理请求
- 用户需要通用帮助而非领域专业知识

## 工作原理

上下文完整性系统，保护复杂技术项目在 Claude Code 自动压缩期间免受信息丢失。`context-agent` 在会话结束后操作（保存/加载），而 context-guardian 在会话期间操作，检测压缩临近时执行带冗余验证的保护协议。

## 为什么需要这个

Claude Code 在上下文接近窗口限制时自动压缩旧消息。这种压缩是启发式的——它总结消息以释放空间，但不可避免地会丢失细节。对于简单项目，这运作良好。但对于重型技术项目（如拥有 21+ 技能的生态系统、安全审计、架构重构），丢失一个细节可能导致回归、返工或严重不一致。

context-guardian 通过创建 PRE-压缩保护层来解决这个问题：在自动压缩破坏信息之前，提取、分类、验证并持久化所有关键信息。

## 目录结构

```
C:\Users\renat\skills\context-guardian\
├── SKILL.md                          # 本文件
├── references/
│   ├── extraction-protocol.md        # 详细提取协议
│   └── verification-checklist.md     # 验证和冗余检查清单
└── scripts/
    └── context_snapshot.py           # 自动快照脚本
```

## 与生态系统的集成

```
context-guardian (PRE-压缩)           context-agent (POS-会话)
         │                                    │
         ├── 检测大上下文                      ├── 结束时保存摘要
         ├── 提取关键数据                      ├── 更新 ACTIVE_CONTEXT.md
         ├── 验证完整性                        ├── 同步 MEMORY.md
         ├── 保存已验证快照                    ├── 索引 FTS5 搜索
         └── 生成过渡简报                      └── 归档旧会话
```

context-guardian 和 context-agent 是互补的：
- **context-guardian**：实时保护，在会话期间
- **context-agent**：会话间持久化，在会话结束后

## 自动激活（Claude 应自行启动）

1. **上下文限制**：当感知已消耗约 60-70% 的上下文窗口时（指标：消息开始被总结、压缩警告）
2. **重型项目**：编辑大量文件、大量工具调用的会话，或组件间依赖复杂的项目
3. **长任务前**：当即将进行的任务可能产生大量输出，将上下文推超限制时

## 手动激活（用户请求）

- "压缩前保存状态"
- "做个检查点"
- "上下文快照"
- "不想丢失这次会话的任何内容"
- "准备压缩"
- "上下文大了，保护一下"

## 第一阶段：结构化提取

遍历到目前为止的整个对话，提取关键类别。每个类别按优先级分类（P0 = 致命丢失，P1 = 严重丢失，P2 = 可容忍丢失）。

**P0 — 致命丢失（三重冗余保护）**

| 类别 | 提取内容 | 示例 |
|------|----------|------|
| 技术决策 | 架构、模式、技术选择及原因 | "使用参数化查询，因为 f-string 会导致 SQL 注入" |
| 任务状态 | 已完成、待办、依赖关系 | "18/18 匹配 OK，缺少 ZIP" |
| 已应用的修复 | Bug、根因、精确解决方案、受影响文件 | "instagram/db.py: f-string 导致 SQL 注入 → ? 占位符" |
| 生成/修改的代码 | 精确路径、修改行、变更性质 | "match_skills.py:40-119: 添加了 5 个类别" |
| 遇到的错误 | 精确消息、相关堆栈跟踪、如何解决 | "第 45 行 TypeError → 转换为 int" |
| 成功的命令 | 产生正确结果的完整命令 | "python verify_zips.py → 22/22 OK" |

**P1 — 严重丢失（验证保护）**

| 类别 | 提取内容 |
|------|----------|
| 发现的模式 | 约定、观察到的代码模式 |
| 组件间依赖 | "scan_registry.py 和 match_skills.py 必须有相同类别" |
| 用户偏好 | 语言、风格、详细程度、首选工作流 |
| 项目上下文 | 目录结构、关键文件、目的 |
| 未解决问题 | 未回答的问题、未解决的歧义 |

**P2 — 可容忍丢失（紧凑摘要）**

| 类别 | 提取内容 |
|------|----------|
| 尝试历史 | "尝试了 X，因 Y 失败，然后 Z" |
| 进度指标 | 计数、时间、大小 |
| 探索性讨论 | 头脑风暴、考虑和放弃的选项 |

## 第二阶段：完整性验证

提取后，验证没有遗漏任何关键信息。

**验证检查清单（对每个项目在心中执行）：**

```
□ 每个修改的文件都有：路径、变更性质、原因
□ 每个修复的 bug 都有：症状、根因、解决方案、文件
□ 每个决策都有：内容、原因、放弃的替代方案
□ 每个待办任务都有：描述、优先级、依赖关系
□ 每个模式/约定都有：规则、原因、示例
□ 没有任何一节的信息与另一节矛盾
□ 交叉引用一致（如："测试了 18 个查询" 在多处出现相同数字）
□ 文件路径完整（绝对路径，非相对路径）
```

如果任何项目失败，返回第一阶段重新提取缺失信息。

关于高级验证的详情，请阅读 `references/verification-checklist.md`。

## 第三阶段：冗余持久化

将提取的信息保存到 3 层冗余：

**第一层 — 结构化快照（.md 文件）**

```bash
python C:\Users\renat\skills\context-guardian\scripts\context_snapshot.py save
```

生成 `C:\Users\renat\skills\context-guardian\data\snapshot-YYYYMMDD-HHMMSS.md`，包含所有提取的结构化信息。

如果脚本不可用，按照 `references/extraction-protocol.md` 描述的格式手动创建文件。

**第二层 — 更新 MEMORY.md**

更新 `C:\Users\renat\.claude\projects\C--Users-renat-Skill-JUD\memory\MEMORY.md`，以超紧凑格式添加最关键的 P0 信息。MEMORY.md 在每次新会话自动加载，是最后一道防线。

**第三层 — Context-agent 保存**

```bash
python C:\Users\renat\skills\context-agent\scripts\context_manager.py save
```

触发 context-agent 保存完整会话并建立 FTS5 索引。

## 第四阶段：过渡简报

生成格式化的文本块，作为压缩后继续的 Claude 的"名片"。此简报应在压缩前最后写入，以便位于压缩上下文的顶部。

**简报格式：**

```markdown

## 当前状态

- 项目：[名称]
- 阶段：[当前阶段]
- 进度：[X/Y 任务完成]

## 本次会话已完成

1. [任务 1 — 结果]
2. [任务 2 — 结果]
...

## 待办事项

1. [待办任务 — 优先级] [依赖关系如有]
2. ...

## 关键决策（无理由不要更改）

- [决策 1]：[原因]
- [决策 2]：[原因]

## 已应用修复（不要回滚）

- [文件]：[修复] — [原因]

## 重要路径

- [路径 1]：[用途]
- [路径 2]：[用途]

## 警告

- [任何陷阱、边界情况或特殊注意事项]

## 在哪里恢复更多信息

- 快照：C:\Users\renat\skills\context-guardian\data\snapshot-[时间戳].md
- MEMORY.md：自动加载
- Context-agent：`python context_manager.py load`
- 历史搜索：`python context_manager.py search "术语"`
```

## 快速协议（时间紧迫时）

如果压缩迫在眉睫且没有时间执行完整的 4 阶段协议：

1. **30 秒** — 编写迷你简报：待办任务、关键决策、修改的文件路径
2. **1 分钟** — 用 P0 信息更新 MEMORY.md
3. **2 分钟** — 执行 context-agent save

即使是快速协议也比没有保护好。

## 压缩后完整性检测

当会话在压缩后继续时，验证保留的上下文是否完整：

1. 读取 MEMORY.md（已自动加载）
2. 如可用，读取 `data/` 中最近的快照
3. 与过渡简报比较（如压缩上下文中可见）
4. 如发现缺口，执行：
   ```bash
   python C:\Users\renat\skills\context-agent\scripts\context_manager.py load
   ```
5. 如仍有缺口，按术语搜索：
   ```bash
   python C:\Users\renat\skills\context-agent\scripts\context_manager.py search "术语"
   ```

## 真实使用示例

**场景**：长会话创建 advogado-especialista（46KB），修复 match_skills（5 个新类别），审计安全（10 个漏洞），生成 22 个 ZIP。

**无 context-guardian**：
压缩将所有内容总结为"创建法律技能、修复 bug、生成 zip"。下一个 Claude 不知道添加了哪些类别、修复了哪些漏洞、每个 ZIP 的状态，或为什么做出某些决策。
结果：返工、不一致、回归。

**有 context-guardian**：
压缩前执行完整协议：
- 快照列出 5 个新类别（legal、auction、security、image-generation、monitoring）
- 10 个漏洞编目，包含文件、类型和精确修复
- 22 个 ZIP 已验证并带校验和
- 决策已记录（"从 monitoring 移除 'saude' 因为导致误报"）
- 过渡简报位于上下文顶部
下一个 Claude 以完全精确继续，零返工。

## 性能考虑

- 完整协议需要 Claude 2-5 分钟工作
- 对于简单项目，仅使用快速协议
- 不要为短会话或随意对话激活
- 3 层持久化（快照 + MEMORY.md + context-agent）确保即使一层失败，其他两层仍保留信息
- 旧快照（>10）可手动清理

## 最佳实践

- 提供清晰、具体的项目和需求上下文
- 在将建议应用到生产代码前进行审查
- 与其他互补技能结合进行全面分析

## 常见陷阱

- 将此技能用于其领域专业知识之外的任务
- 在不了解具体上下文的情况下应用建议
- 未提供足够的项目上下文以进行准确分析

## 相关技能

- `context-agent` - 用于增强分析的互补技能

## 局限性
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
