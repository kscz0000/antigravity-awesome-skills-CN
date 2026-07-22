# CSO 指南 - Claude 搜索优化

使技能可被智能体发现的高级技术。

## 发现问题

你有 100+ 个技能。智能体收到一个任务。它如何找到正确的技能？

**答案**：`description` 字段。

## 关键规则：描述 = 触发词，而非工作流

### 陷阱

当描述概述工作流时，智能体会走捷径。

**失败的真实示例**：

```yaml
# Agent did ONE review instead of TWO
description: Code review between tasks

# Skill body had flowchart showing TWO reviews:
# 1. Spec compliance
# 2. Code quality
```

**失败原因**：智能体读取描述，认为"任务之间的代码审查意味一次审查"，从未读取流程图。

**修复**：

```yaml
# Agent now reads full skill and follows flowchart
description: Use when executing implementation plans with independent tasks
```

### 模式

```yaml
# ❌ BAD: 工作流概述
description: Analyzes git diff, generates commit message in conventional format

# ✅ GOOD: 仅触发条件
description: Use when generating commit messages or reviewing staged changes
```

## 技能的 Token 效率至关重要

**问题**：频繁加载的技能在每个对话中消耗 token。

**目标字数**：

- 频繁加载的技能：总共 <200 词
- 其他技能：<500 词

### 技术

**1. 将细节移至工具帮助**：

```bash
# ❌ BAD: 在 SKILL.md 中记录所有标志
search-conversations supports --text, --both, --after DATE, --before DATE, --limit N

# ✅ GOOD: 引用 --help
search-conversations supports multiple modes. Run --help for details.
```

**2. 使用交叉引用**：

```markdown
# ❌ BAD: 重复工作流

When searching, dispatch agent with template...
[20 lines of repeated instructions]

# ✅ GOOD: 引用其他技能

Use subagents for searches. See [delegating-to-subagents] for workflow.
```

**3. 压缩示例**：

```markdown
# ❌ BAD: 冗长（42 词）

Partner: "How did we handle auth errors in React Router?"
You: I'll search past conversations for patterns.
[Dispatch subagent with query: "React Router authentication error handling 401"]

# ✅ GOOD: 极简（20 词）

Partner: "Auth errors in React Router?"
You: Searching...
[Dispatch subagent → synthesis]
```

## 关键词策略

### 错误消息

包含用户将看到的精确错误文本：

- "Hook timed out after 5000ms"
- "ENOTEMPTY: directory not empty"
- "jest --watch is not responding"

### 症状

使用用户自然说出的词：

- "flaky"、"hangs"、"zombie process"
- "slow"、"timeout"、"race condition"
- "cleanup failed"、"pollution"

### 工具和命令

使用实际名称，而非描述：

- "pytest"，而非"Python testing"
- "git rebase"，而非"rebasing"
- ".docx files"，而非"Word documents"

### 同义词

覆盖描述同一事物的多种方式：

- timeout/hang/freeze
- cleanup/teardown/after Each
- mock/stub/fake

## 命名约定

### 动名词（-ing）用于过程

✅ `creating-skills`、`debugging-with-logs`、`testing-async-code`

### 动词优先用于动作

✅ `flatten-with-flags`、`reduce-complexity`、`trace-root-cause`

### ❌ 避免

- `skill-creation`（被动，难以搜索）
- `async-test-helpers`（过于宽泛）
- `debugging-techniques`（模糊）

## 描述模板

```yaml
description: "Use when [SPECIFIC TRIGGER]."
metadata:
  triggers: [error1], [symptom2], [tool3]
```

**示例**：

```yaml
# Technique skill
description: "Use when tests have race conditions, timing dependencies, or pass/fail inconsistently."
metadata:
  triggers: flaky tests, timeout, race condition

# Pattern skill
description: "Use when complex data structures make code hard to follow."
metadata:
  triggers: nested loops, multiple flags, confusing state

# Reference skill
description: "Use when working with React Router and authentication."
metadata:
  triggers: 401 redirect, login flow, protected routes

# Discipline skill
description: "Use when implementing any feature or bugfix, before writing implementation code."
metadata:
  triggers: new feature, bug fix, code change
```

## 第三人称规则

描述被注入系统提示。不一致的视角会破坏发现。

```yaml
# ❌ BAD: 第一人称
description: "I can help you with async tests"

# ❌ BAD: 第二人称
description: "You can use this for race conditions"

# ✅ GOOD: 第三人称
description: "Handles async tests with race conditions"
```

## 交叉引用其他技能

**记录引用其他技能的技能时**：

仅使用技能名称，并带有明确的要求标记：

```markdown
# ✅ GOOD: 明确的要求

**REQUIRED BACKGROUND**: You MUST understand test-driven-development before using this skill.

**REQUIRED SUB-SKILL**: Use defensive-programming for error handling.

# ❌ BAD: 不清楚是否必需

See test-driven-development skill for context.

# ❌ NEVER: 强制加载（消耗上下文）

@skills/testing/test-driven-development/SKILL.md
```

**为什么没有 @ 链接**：`@` 语法立即强制加载文件，在需要之前消耗 token。

## 验证清单

部署前：

- [ ] 描述以 "Use when..." 开头？
- [ ] 描述 <500 个字符？
- [ ] 描述仅列出触发词，不包含工作流？
- [ ] 包含 3+ 关键词（错误/症状/工具）？
- [ ] 全文使用第三人称？
- [ ] 名称使用动名词或动词优先格式？
- [ ] 名称仅包含字母、数字、连字符？
- [ ] 交叉引用没有 @ 语法？
- [ ] 字数 <200（频繁）或 <500（其他）？

## 真实示例

### 前后对比：TDD 技能

❌ **之前**（工作流在描述中）：

```yaml
description: Write test first, watch it fail, write minimal code, refactor
```

结果：智能体遵循描述，跳过阅读完整技能。

✅ **之后**（仅触发词）：

```yaml
description: Use when implementing any feature or bugfix, before writing implementation code
```

结果：智能体读取完整技能，遵循完整的 TDD 循环。

### 前后对比：BigQuery 技能

❌ **之前**（太模糊）：

```yaml
description: Helps with database queries
```

结果：从未加载（太通用，智能体无法识别相关性）。

✅ **之后**（具体触发词）：

```yaml
description: Use when analyzing BigQuery data. Triggers: revenue metrics, pipeline data, API usage, campaign attribution.
```

结果：为相关查询加载，包含领域关键词。
