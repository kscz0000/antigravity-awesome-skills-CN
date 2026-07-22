---
name: concise-planning
description: "当用户请求为编码任务制定计划时使用，生成清晰、可执行、原子化的检查清单。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Concise Planning

## 目标

将用户请求转化为**单一、可执行的计划**，包含原子化步骤。

## 工作流程

### 1. 扫描上下文

- 阅读 `README.md`、文档和相关代码文件。
- 识别约束条件（语言、框架、测试）。

### 2. 最小化交互

- 仅在真正阻塞时提问，**最多 1-2 个问题**。
- 对非阻塞的未知项做出合理假设。

### 3. 生成计划

使用以下结构：

- **方法**：1-3 句话说明做什么和为什么。
- **范围**：用要点列出"包含"和"不包含"。
- **行动项**：6-10 个原子化、有序的任务列表（动词开头）。
- **验证**：至少包含一项测试相关内容。

## 计划模板

```markdown
# Plan

<High-level approach>

## Scope

- In:
- Out:

## Action Items

[ ] <Step 1: Discovery>
[ ] <Step 2: Implementation>
[ ] <Step 3: Implementation>
[ ] <Step 4: Validation/Testing>
[ ] <Step 5: Rollout/Commit>

## Open Questions

- <Question 1 (max 3)>
```

## 检查清单指南

- **原子化**：每个步骤应是单一逻辑工作单元。
- **动词开头**："添加..."、"重构..."、"验证..."。
- **具体化**：尽可能指明具体文件或模块名称。

## 使用时机

本技能适用于执行概述中描述的工作流程或操作。

## 限制

- 仅当任务明确符合上述范围时使用本技能。
- 输出内容不能替代环境特定的验证、测试或专家评审。
- 若缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
