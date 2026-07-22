---
name: blueprint
description: "将一句话目标转化为多会话、多智能体工程项目的分步构建计划。每个步骤包含自包含的上下文摘要，使新智能体可以零上下文冷启动执行。触发条件：用户请求复杂多PR任务的计划、蓝图或路线图，或描述需要多次会话才能完成的工作。不触发条件：任务可在单个PR或少于3次工具调用内完成，或用户说\"直接做\"。"
category: planning
risk: safe
source: community
date_added: "2026-03-10"
---

# Blueprint — 构建计划生成器

将一句话目标转化为分步计划，任何编码智能体都能冷启动执行。

## 概述

Blueprint 适用于多会话、多智能体的工程项目，其中每个步骤必须能被从未见过对话历史的新智能体独立执行。安装一次，通过 `/blueprint <project> <objective>` 调用。

## 何时使用此技能

- 任务需要多个 PR 或多次会话时使用
- 多个智能体或团队成员需要共享执行时使用
- 希望在执行前对计划进行对抗性审查时使用
- 并行步骤检测和依赖图很重要时使用

## 工作原理

1. **研究** — 扫描代码库、读取项目记忆、运行预检检查
2. **设计** — 将目标分解为单 PR 规模的步骤、识别并行性、分配模型层级
3. **起草** — 从结构化模板生成计划，内联分支工作流规则、CI 策略和回滚策略
4. **审查** — 委托最强模型子智能体进行对抗性审查（不可用时回退到默认模型）
5. **注册** — 保存计划并更新项目记忆

## 示例

### 示例 1：数据库迁移
```
/blueprint myapp "migrate database to PostgreSQL"
```

### 示例 2：插件提取
```
/blueprint antbot "extract providers into plugins"
```

## 最佳实践

- ✅ 用于需要 3+ PR 或多次会话的任务
- ✅ 让 Blueprint 自动检测 git/gh 可用性 — 它会优雅降级
- ❌ 不要在单个 PR 内可完成的任务上调用
- ❌ 用户说"直接做"时不要调用

## 核心差异

- **冷启动执行**：每个步骤都有自包含的上下文摘要
- **对抗性审查门**：执行前由最强模型审查
- **零运行时风险**：纯 Markdown — 无钩子、无脚本、无可执行代码
- **计划变更协议**：步骤可拆分、插入、跳过，带有审计追踪

## 安装

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/antbotlab/blueprint.git ~/.claude/skills/blueprint
```

## 更多资源

- [GitHub 仓库](https://github.com/antbotlab/blueprint)
- [示例：小型计划](https://github.com/antbotlab/blueprint/blob/main/examples/small-plan.md)
- [示例：大型计划](https://github.com/antbotlab/blueprint/blob/main/examples/large-plan.md)

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
