---
name: unslop-commit
description: 改写提交信息，让它读起来像一位严谨的工程师亲手写的。去除 AI/营销腔（"comprehensive solution"、"robust implementation"、"leverage"、"enhance"、"seamlessly"、"This commit..."）。保留 Conventional Commits 规范。主题行 ≤72 字符（目标 ≤50），...
risk: unknown
source: https://github.com/MohamedAbdallah-14/unslop/tree/main/plugins/unslop/skills/unslop-commit
source_repo: MohamedAbdallah-14/unslop
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/MohamedAbdallah-14/unslop/blob/main/LICENSE
---

# 清除提交信息中的 AI 腔
## 适用场景

改写提交信息，让它读起来像一位严谨的工程师亲手写的。去除 AI/营销腔（"comprehensive solution"、"robust implementation"、"leverage"、"enhance"、"seamlessly"、"This commit..."）。保留 Conventional Commits 规范。主题行 ≤72 字符（目标 ≤50），...


## 目的

生成或改写提交信息，让它读起来像一位真正收工时的工程师写的东西。Conventional Commits 规范。直接、具体，不要模板化的英文。说"为什么"而不是"做了什么"。

## 触发词

`/unslop-commit`、`/commit`、"写一个提交"、"提交信息"、"humanize this commit"、"de-slop this commit"。当用户已暂存改动并要求生成提交信息时自动触发。

## 规则

### 主题行

- 格式：`<type>(<scope>): <imperative summary>`
- scope 可选。type：`feat`、`fix`、`chore`、`refactor`、`docs`、`test`、`perf`、`build`、`ci`、`revert`。
- 命令式：`add`、`fix`、`move`、`remove`，不要 `added`、`fixes`、`fixing`。
- 尽可能 ≤50 字符。硬上限 72。
- 不带结尾句号。
- `:` 后小写，除非项目习惯大写。

### 正文（仅在主题行无法承载时）

- 用于：非显而易见的"为什么"、破坏性变更、数据迁移、安全上下文、数据完整性。
- 72 字符换行。两个及以上独立要点用 `-` 项目符号。一个想法用单段落。
- 末尾引用：`Closes #42`、`Refs #17`。除非真正破坏性变更，否则不要写 `BREAKING CHANGE:`，要写就写清楚。

### 绝不包含

- 模板化前缀："This commit..."、"This change..."、"We are..."、"I have..."
- 营销动词：comprehensive、robust、enhance、leverage、seamless、holistic
- 凑数副词：just、really、basically、simply、actually
- 在 scope 已经点名的前提下重复文件名
- "As requested by..."（如需归属用 `Co-authored-by:`）
- AI 归属声明，除非项目要求
- 表情符号，除非项目约定

### 必须包含正文（自动清晰化）

- 破坏性变更
- 安全修复
- 数据迁移
- 撤销（注明被撤销的提交）

## 示例

### 坏 → 好（腔调主题行，无正文）

- 坏：`feat: implement a comprehensive, robust solution for user profile retrieval with enhanced error handling`
- 好：`feat(api): return profile fields the mobile client actually needs`

### 坏 → 好（模糊正文）

坏：
```
fix: fixed the bug

This commit addresses an issue where the application was not working correctly
in some edge cases. We've improved the logic to handle these scenarios.
```

好：
```
fix(checkout): ignore stale cart id from localStorage

Stale cart ids came from tabs that hadn't refreshed after a deploy. Server
now treats unknown ids as empty cart instead of 500.

Closes #842
```

### 破坏性变更

```
feat(api)!: rename /v1/orders to /v1/customer-orders

The old route stays in place until the next major release but logs a
deprecation warning. Internal services have been migrated.

BREAKING CHANGE: third-party integrations using /v1/orders directly need
to switch to /v1/customer-orders by 2026-07-01.

Closes #1290
```

## 边界

- 只输出提交信息，单个围栏代码块，可直接粘贴。
- 不要执行 `git commit`、暂存或 amend。
- 如果改动确实琐碎（`docs(readme): fix typo`），就保持琐碎。不要凑字数。
- 不要编造用户没有提供的上下文。如果"为什么"不清楚，就问，或省略正文。

## 局限

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用变更前，验证命令、生成的代码、依赖、凭据和外部服务行为。
- 不要把示例当作环境特定测试、安全审查或用户对破坏性/高成本操作的批准替代品。