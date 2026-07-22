---
name: multi-agent-task-orchestrator
description: "将任务路由到专门的 AI 智能体，具备防重复、质量门控和30分钟心跳监控功能。当用户要求协调多智能体任务时使用。"
category: agent-orchestration
risk: safe
source: community
source_repo: milkomida77/guardian-agent-prompts
source_type: community
date_added: "2026-04-09"
author: milkomida77
tags: [multi-agent, orchestration, task-routing, quality-gates, anti-duplication]
tools: [claude, cursor, gemini]
---

# 多智能体任务编排器

## 概述

一种经过生产验证的模式，用于通过单个编排器协调多个 AI 智能体。与让智能体独立工作（并产生冲突）不同，一个编排器负责分解任务、将其路由到专业人员、防止重复工作，并在标记完成之前验证结果。经过6个月超过10,000个任务的实战检验。

## 何时使用此技能

- 当你有3个以上需要协调复杂任务的专业智能体时使用
- 当智能体正在做重复或冲突的工作时使用
- 当你需要审计追踪来显示谁在什么时候做了什么时使用
- 当智能体输出质量不一致且需要验证门控时使用

## 工作原理

### 步骤1：定义编排器身份

编排器必须清楚自己是什么以及不是什么。这可以防止它自己去做工作而不是委派：

```
You are the Task Orchestrator. You NEVER do specialized work yourself.
You decompose tasks, delegate to the right agent, prevent conflicts,
and verify quality before marking anything done.

WHAT YOU ARE NOT:
- NOT a code writer — delegate to code agents
- NOT a researcher — delegate to research agents
- NOT a tester — delegate to test agents
```

这种"NOT-block"模式在生产环境中将任务漂移减少了约35%。

### 步骤2：构建任务注册表

在分配工作之前，检查是否有人已经在执行此任务：

```python
import sqlite3
from difflib import SequenceMatcher

def check_duplicate(description, threshold=0.55):
    conn = sqlite3.connect("task_registry.db")
    c = conn.cursor()
    c.execute("SELECT id, description, agent, status FROM tasks WHERE status IN ('pending', 'in_progress')")
    for row in c.fetchall():
        ratio = SequenceMatcher(None, description.lower(), row[1].lower()).ratio()
        if ratio >= threshold:
            return {"id": row[0], "description": row[1], "agent": row[2]}
    return None
```

### 步骤3：将任务路由到专业人员

使用关键词评分将任务匹配到最佳智能体：

```python
AGENTS = {
    "code-architect": ["code", "implement", "function", "bug", "fix", "refactor", "api"],
    "security-reviewer": ["security", "vulnerability", "audit", "cve", "injection"],
    "researcher": ["research", "compare", "analyze", "benchmark", "evaluate"],
    "doc-writer": ["document", "readme", "explain", "tutorial", "guide"],
    "test-engineer": ["test", "coverage", "unittest", "pytest", "spec"],
}

def route_task(description):
    scores = {}
    for agent, keywords in AGENTS.items():
        scores[agent] = sum(1 for kw in keywords if kw in description.lower())
    return max(scores, key=scores.get) if max(scores.values()) > 0 else "code-architect"
```

### 步骤4：强制质量门控

智能体的输出是声明，测试输出才是证据。

```
After agent reports completion:
1. Were files actually modified? (git diff --stat)
2. Do tests pass? (npm test / pytest)
3. Were secrets introduced? (grep for API keys, tokens)
4. Did the build succeed? (npm run build)
5. Were only intended files touched? (scope check)

Mark done ONLY after ALL checks pass.
```

### 步骤5：运行30分钟心跳

```
Every 30 minutes, ask:
1. "What have I DELEGATED in the last 30 minutes?"
2. If nothing → open the task backlog and assign the next task
3. Check for idle agents (no message in >30min on assigned task)
4. Relance idle agents or reassign their tasks
```

## 示例

### 示例1：委派代码任务

```
[ORCHESTRATOR -> code-architect] TASK: Add rate limiting to /api/users
SCOPE: src/middleware/rate-limit.ts only
VERIFICATION: npm test -- --grep "rate-limit"
DEADLINE: 30 minutes
```

### 示例2：处理重复任务

```
User asks: "Fix the login bug"
Registry check: Task #47 "Fix authentication bug" is IN_PROGRESS by security-reviewer
Decision: SKIP — similar task already assigned (78% match)
Action: Notify user of existing task, wait for completion
```

## 最佳实践

- 为每个智能体定义 NOT-block（它们必须拒绝做的事情）
- 使用 SQLite 作为任务注册表（轻量级，无需服务器）
- 将相似度阈值设置为55%用于防重复（太低会产生过多误报）
- 要求基于证据的质量门控（不仅仅是智能体的声明）
- 记录每次委派的任务 ID、智能体、范围、截止时间和验证命令

## 常见陷阱

- **问题：** 编排器开始自己做工作而不是委派
  **解决方案：** 添加明确的 NOT-block 和角色边界

- **问题：** 两个智能体同时修改同一个文件
  **解决方案：** 使用带文件级锁定和队列系统的任务注册表

- **问题：** 智能体声称"完成"但没有实际更改
  **解决方案：** 质量门控在接受完成之前检查 git diff

- **问题：** 任务堆积但没有进展
  **解决方案：** 30分钟心跳机制捕获过期分配并重新分配

## 相关技能

- `@code-review` - 用于在委派后审查代码更改
- `@test-driven-development` - 用于确保智能体输出的质量
- `@project-management` - 用于跟踪多智能体项目进度

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。