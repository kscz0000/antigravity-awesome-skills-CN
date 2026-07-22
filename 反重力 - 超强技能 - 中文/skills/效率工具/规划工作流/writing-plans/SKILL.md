---
name: writing-plans
description: "当你拥有多步任务的规范或需求时使用，在动手编写代码之前。触发词：编写计划、实施方案、任务分解、实施规划、写计划、开发计划、分步计划"
risk: critical
source: community
date_added: "2026-02-27"
---

# 编写计划

## 概述

撰写全面的实施计划，假设工程师对我们的代码库零背景且品味存疑。记录他们需要知道的一切：每个任务涉及哪些文件、代码、测试、可能需要查阅的文档，以及如何测试它。以小到可以一口吞下的任务为单位给出整个计划。DRY。YAGNI。TDD。频繁提交。

假设他们是一名熟练的开发人员，但对我们工具集和问题域几乎一无所知。假设他们也不太懂良好的测试设计。

**开始时宣告：** "我正在使用 writing-plans 技能创建实施计划。"

**上下文：** 应在专属 worktree（由 brainstorming 技能创建）中运行。

**计划保存路径：** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## 细粒度任务拆分

**每个步骤是一个动作（2-5 分钟）：**
- "编写失败的测试" - 一个步骤
- "运行它以确保失败" - 一个步骤
- "编写最少代码使测试通过" - 一个步骤
- "运行测试并确保通过" - 一个步骤
- "提交" - 一个步骤

## 计划文档头部

**每个计划必须以此头部开头：**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## 任务结构

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## 切记
- 始终使用精确的文件路径
- 计划中提供完整代码（而非"添加校验"）
- 精确的命令及预期输出
- 使用 @ 语法引用相关技能
- DRY、YAGNI、TDD、频繁提交

## 执行交接

保存计划后，提供执行选择：

**"计划已完成并保存到 `docs/plans/<filename>.md`。两种执行方式：**

**1. 子代理驱动（当前会话）** - 我为每个任务派遣全新的子代理，任务之间进行审查，快速迭代

**2. 并行会话（独立会话）** - 在新会话中打开 executing-plans，带检查点的批量执行

**选择哪种方式？"**

**如果选择子代理驱动：**
- **必需的子技能：** 使用 superpowers:subagent-driven-development
- 留在当前会话
- 每个任务使用全新子代理 + 代码审查

**如果选择并行会话：**
- 引导他们在 worktree 中打开新会话
- **必需的子技能：** 新会话使用 superpowers:executing-plans

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
