---
name: agent-orchestrator
description: 编排生态系统中所有智能体的元技能。自动扫描技能、按能力匹配、协调多技能工作流和注册表管理。触发词：智能体编排、多智能体协调、技能匹配、工作流编排、agent orchestrator、multi-agent、skill orchestration、技能调度、多技能协调
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- orchestration
- multi-agent
- workflow
- automation
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# Agent Orchestrator

## 概述

编排生态系统中所有智能体的元技能。自动扫描技能、按能力匹配、协调多技能工作流和注册表管理。

## 何时使用此技能

- 当你需要此领域的专业协助时

## 何时不使用此技能

- 任务与智能体编排无关
- 更简单、更具体的工具可以处理请求
- 用户需要无领域专业知识的通用协助

## 工作原理

作为整个技能生态系统核心决策和协调层的元技能。执行自动扫描、识别相关智能体，并为复杂任务编排多个技能。

## 原则：零手动干预

- **始终执行扫描**，在处理任何请求之前
- 新技能在任意子文件夹创建 SKILL.md 后**自动检测并纳入**
- 被移除的技能从注册表中**自动排除**
- 无需手动命令即可注册新技能

---

## 必要工作流（每次请求）

在处理任何用户请求之前执行这些步骤。
脚本自动使用相对路径——可在任意目录运行。

## 步骤 1：自动发现（扫描）

```bash
python agent-orchestrator/scripts/scan_registry.py
```

通过 MD5 哈希缓存实现超快速（<100ms）。仅重新处理已更改的文件。
返回包含所有已发现技能摘要的 JSON。

## 步骤 2：技能匹配

```bash
python agent-orchestrator/scripts/match_skills.py "<用户请求>"
```

返回按相关性排序的技能 JSON。解读结果：

| 结果              | 操作                                                    |
|:-----------------------|:--------------------------------------------------------|
| `matched: 0`          | 无相关技能。正常操作，不使用技能。  |
| `matched: 1`          | 一个相关技能。加载其 SKILL.md 并执行。     |
| `matched: 2+`         | 多个技能。执行步骤 3（编排）。      |

## 步骤 3：编排（若匹配数 >= 2）

```bash
python agent-orchestrator/scripts/orchestrate.py --skills skill1,skill2 --query "<请求>"
```

返回包含模式、步骤顺序和技能间数据流的执行计划。

## 快速步骤（快捷方式）

对于简单查询，步骤 1+2 可按顺序组合：
```bash
python agent-orchestrator/scripts/scan_registry.py && python agent-orchestrator/scripts/match_skills.py "<请求>"
```

---

## 技能注册表

注册表位于：
```
agent-orchestrator/data/registry.json
```

## 搜索位置

扫描器在以下位置查找 SKILL.md：
1. `.claude/skills/*/`（Claude Code 中注册的技能）
2. `*/`（顶层的独立技能）
3. `*/*\`（子文件夹中的技能，深度至 3 层）

## 每个技能的元数据

注册表中的每个条目包含：

| 字段          | 描述                                          |
|:---------------|:---------------------------------------------------|
| name           | 技能名称（来自 YAML frontmatter）                |
| description    | 完整描述（包含触发词）             |
| location       | 目录的绝对路径                      |
| skill_md       | SKILL.md 的绝对路径                       |
| registered     | 是否在 .claude/skills/ 中（true/false）            |
| capabilities   | 能力标签（自动提取 + 显式声明）   |
| triggers       | 从描述中提取的激活关键词      |
| language       | 主要语言（python/nodejs/bash/none）      |
| status         | active / incomplete / missing                      |

## 注册表命令

```bash

## 快速扫描（使用哈希缓存）

python agent-orchestrator/scripts/scan_registry.py

## 详细状态表

python agent-orchestrator/scripts/scan_registry.py --status

## 完整重新扫描（忽略缓存）

python agent-orchestrator/scripts/scan_registry.py --force
```

---

## 匹配算法

对于每个请求，匹配器使用以下标准对技能评分：

| 标准                     | 分数 | 示例                               |
|:-----------------------------|:-------|:--------------------------------------|
| 查询中包含技能名称       | +15    | "use web-scraper" -> web-scraper      |
| 精确关键词触发        | +10    | "scrape" -> web-scraper               |
| 能力类别      | +5     | data-extraction -> web-scraper        |
| 词汇重叠     | +1     | 查询词出现在描述中      |
| 项目加成             | +20    | 技能分配给活跃项目      |

最低阈值：5 分。低于此分数的技能将被忽略。

## 按项目匹配

```bash
python agent-orchestrator/scripts/match_skills.py --project meu-projeto "查询内容"
```

分配给项目的技能自动获得 +20 加成。

---

## 编排模式

当多个技能相关时，编排器对模式进行分类：

## 1. 顺序管道

技能形成链式结构，一个的输出作为下一个的输入。

**适用场景：** "生产者"技能（data-extraction、government-data）与"消费者"技能（messaging、social-media）的组合。

**示例：** web-scraper 收集价格 -> whatsapp-cloud-api 发送警报

```
user_query -> web-scraper -> whatsapp-cloud-api -> result
```

## 2. 并行执行

技能独立处理请求的不同方面。

**适用场景：** 所有技能角色相同（全部为生产者或全部为消费者）。

**示例：** instagram 发布帖子 + whatsapp 发送通知（两者接收相同内容）

```
user_query -> [instagram, whatsapp-cloud-api] -> aggregated_result
```

## 3. 主技能 + 支援

一个主技能主导；其他提供辅助数据。

**适用场景：** 一个技能的分数远高于其他（>= 2 倍）。

**示例：** whatsapp-cloud-api 发送消息（主）+ web-scraper 提供数据（支援）

```
user_query -> whatsapp-cloud-api (primary) + web-scraper (support) -> result
```

## 详情见 `references/Orchestration-Patterns.md`

---

## 项目管理

将技能分配给项目可实现相关性加成和持久上下文。

## 项目文件

```
agent-orchestrator/data/projects.json
```

## 操作

**创建项目：**
向 projects.json 添加条目：
```json
{
  "name": "nome-do-projeto",
  "created_at": "2026-02-25T12:00:00",
  "skills": ["web-scraper", "whatsapp-cloud-api"],
  "description": "项目描述"
}
```

**将技能添加到项目：** 更新项目的 `skills` 数组。

**从项目移除技能：** 从 `skills` 数组中删除。

**查询项目技能：** 读取 projects.json 并列出已分配的技能。

---

## 添加新技能

向生态系统添加新技能：

1. 在 `skills root:` 下的任意位置创建文件夹
2. 创建包含 YAML frontmatter 的 `SKILL.md`：
```yaml
---
name: minha-nova-skill
description: "包含激活关键词的描述..."
---

## 技能文档

```
3. **完成！** 自动发现将在下次请求时自动检测。

可选地，为 Claude Code 原生发现：
4. 将 SKILL.md 复制到 `.claude/skills/<nome>/SKILL.md`

## 显式能力标签（可选）

添加到 frontmatter 以实现更精确的匹配：
```yaml
capabilities: [data-extraction, web-automation]
```

---

## 查看所有技能状态

```bash
python agent-orchestrator/scripts/scan_registry.py --status
```

## 解读状态

| 状态     | 含义                                        |
|:-----------|:---------------------------------------------------|
| active     | SKILL.md 包含 name + description          |
| incomplete | SKILL.md 存在但缺少 name 或 description      |
| missing    | 目录存在但没有 SKILL.md                  |

---

## 生态系统当前技能

| 技能              | 能力                           | 状态  |
|:-------------------|:--------------------------------------|:--------|
| web-scraper        | data-extraction, web-automation       | active  |
| junta-leiloeiros   | government-data, data-extraction      | active  |
| whatsapp-cloud-api | messaging, api-integration            | active  |
| instagram          | social-media, api-integration         | partial |

*此表通过 `scan_registry.py --status` 自动更新。*

## 最佳实践

- 提供清晰、具体的项目和需求上下文
- 在将建议应用到生产代码之前进行审查
- 与其他互补技能结合以进行全面分析

## 常见陷阱

- 将此技能用于其领域专长之外的任务
- 在不了解具体上下文的情况下应用建议
- 未提供足够的项目上下文以进行准确分析

## 相关技能

- `multi-advisor` - 用于增强分析的互补技能
- `task-intelligence` - 用于增强分析的互补技能

## 局限性
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
