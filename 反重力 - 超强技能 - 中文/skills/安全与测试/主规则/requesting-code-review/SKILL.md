---
name: requesting-code-review
description: "完成任务、实现主要功能或合并前使用，以验证工作满足需求。触发词：请求代码审查、代码审查、合并前检查、PR审查、提交审查、功能完成审查、子任务审查"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 请求代码审查

调度 superpowers:code-reviewer 子智能体，在问题扩散前将其捕获。

**核心原则：** 早审查，勤审查。

## 何时请求审查

**必须审查：**
- 子智能体驱动开发中每完成一个任务后
- 完成主要功能后
- 合并到 main 之前

**建议审查（很有价值）：**
- 卡住时（换个视角）
- 重构前（建立基线）
- 修复复杂 bug 后

## 如何请求审查

**1. 获取 git SHA：**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 调度 code-reviewer 子智能体：**

使用 Task 工具，类型为 superpowers:code-reviewer，填写 `code-reviewer.md` 中的模板

**占位符说明：**
- `{WHAT_WAS_IMPLEMENTED}` - 你刚刚构建的内容
- `{PLAN_OR_REQUIREMENTS}` - 它应该做什么
- `{BASE_SHA}` - 起始 commit
- `{HEAD_SHA}` - 结束 commit
- `{DESCRIPTION}` - 简要概述

**3. 处理反馈：**
- Critical 问题立即修复
- Important 问题在继续之前修复
- Minor 问题记录下来后续处理
- 如果审查者判断有误，有理有据地反驳

## 示例

```
[刚完成任务 2：添加验证函数]

You: 继续之前先请求代码审查。

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[调度 superpowers:code-reviewer 子智能体]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[子智能体返回]:
  优点：架构清晰，测试真实
  问题：
    Important: 缺少进度指示器
    Minor: 报告间隔使用了魔法数字 (100)
  评估：可以继续

You: [修复进度指示器]
[继续任务 3]
```

## 与工作流集成

**子智能体驱动开发：**
- 每个任务完成后都审查
- 在问题累积前发现并修复
- 修完再进入下一个任务

**执行计划：**
- 每批任务（3个）完成后审查
- 获取反馈，应用，继续

**临时开发：**
- 合并前审查
- 卡住时审查

## 红线

**绝不：**
- 因为"这个很简单"跳过审查
- 忽视 Critical 问题
- 带着未修复的 Important 问题继续
- 与正确的技术反馈争论

**如果审查者有误：**
- 用技术论据反驳
- 展示能证明代码可用的代码/测试
- 请求进一步澄清

模板参见：requesting-code-review/code-reviewer.md

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
