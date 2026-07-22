---
name: logic-lens
description: "AI 驱动的 Claude Code 技能，使用形式逻辑和推理框架进行深度代码审查，检测 linter 无法发现的 bug、反模式和安全风险。触发词：logic-lens、逻辑审查、代码审查、深度审查、安全审查、逻辑分析、bug 检测、反模式检测"
category: development
risk: safe
source: community
source_repo: hyhmrright/logic-lens
source_type: community
license: "MIT"
license_source: "https://github.com/hyhmrright/logic-lens/blob/main/LICENSE"
date_added: "2026-04-29"
author: hyhmrright
tags: [code-review, logic-analysis, debugging, security-review, claude-code]
tools: [claude, codex, cursor, gemini]
---

# Logic Lens

## 概述

Logic Lens 是一个 Claude Code 技能，使用形式推理框架进行深度、逻辑驱动的代码审查。与传统检查语法和风格的 linter 不同，Logic Lens 分析代码中的逻辑错误、竞态条件、安全漏洞、类型不匹配和算法缺陷——这些问题只有在推理代码行为时才会显现。

借助结构化 AI 分析，Logic Lens 在 9 个风险类别中应用系统性逻辑检查：空值/未定义处理、类型安全、并发、资源管理、安全注入、边界条件、算法正确性、状态管理和 API 契约违规。

## 何时使用此技能

- 在合并 PR 之前需要彻底的逻辑审查时使用
- 当 bug 难以发现且标准 linter 无法帮助时使用
- 在审查安全敏感代码路径（认证、支付、文件访问）时使用
- 在重构复杂业务逻辑时使用
- 在上手新代码库并需要了解风险区域时使用

## 工作原理

Logic Lens 使用 Claude Code 的推理能力：

1. 解析代码结构并构建数据流心智模型
2. 在 9 个风险类别中应用形式逻辑检查
3. 追踪边缘情况和边界条件的执行路径
4. 识别安全反模式（注入、权限提升、数据泄露）
5. 报告发现结果，包含严重级别和可操作的修复建议

## 安装

```bash
# Install via Claude Code plugin marketplace
# Search: "logic-lens" in Claude Code > Extensions

# Or install via NPX (Antigravity)
npx antigravity-awesome-skills --claude
# Then invoke: @logic-lens
```

## 示例

### 示例 1：审查单个文件

```
@logic-lens review src/auth/login.ts for security issues
```

**Logic Lens 输出：**
```
[CRITICAL] SQL Injection risk at line 42: user input concatenated into query string
[HIGH] Missing rate limiting on login attempts
[MEDIUM] Password comparison uses == instead of timing-safe comparison
[LOW] Error messages may leak valid usernames (user enumeration)
```

### 示例 2：全仓库扫描

```
@logic-lens scan the entire codebase and prioritize by severity
```

### 示例 3：PR 前审查

```
@logic-lens review all files changed in this branch before I open a PR
```

## 9 个风险类别

| 类别 | 检查内容 |
|----------|----------------|
| **空值/未定义** | 缺少空值检查、可选链缺口 |
| **类型安全** | 隐式类型转换、any 类型边界 |
| **并发** | 竞态条件、共享可变状态 |
| **资源管理** | 未关闭的句柄、内存泄漏 |
| **安全注入** | SQL/XSS/命令注入、路径遍历 |
| **边界条件** | 差一错误、整数溢出 |
| **算法正确性** | 错误的复杂度、不正确的假设 |
| **状态管理** | 不一致的状态、缺少回滚 |
| **API 契约** | 未记录的副作用、损坏的接口 |

## 最佳实践

- 每次发布前对认证和支付代码运行 `@logic-lens`
- 结合 `@lint-and-validate` 实现完整覆盖：风格 + 逻辑
- 优先审查 CRITICAL 和 HIGH 级别的发现；LOW 级别可以延后处理
- 在修改遗留代码之前使用 `@logic-lens` 了解风险面

## 基准测试结果

Logic Lens 在真实代码库上进行了测试，发现了 ESLint、TypeScript 严格模式和 Snyk 遗漏的问题：

- **47% 的关键 bug** 对 linter 不可见
- 在异步代码中检测到**竞态条件**，静态分析未能发现
- 在 CI 流水线部署前识别出**安全漏洞**

## 相关技能

- `@lint-and-validate` — 互补：在 logic-lens 之后运行以检查风格/语法
- `@security-auditor` — 专门的安全深度扫描
- `@debugging-strategies` — 当需要追踪 logic-lens 的发现时使用

## 更多资源

- [GitHub 仓库](https://github.com/hyhmrright/logic-lens)
- [Dev.to 文章：为什么 AI 代码审查会遗漏最危险的 Bug](https://dev.to/hyhmrright/why-ai-code-review-misses-the-most-dangerous-bugs-logic-lens-fixes-that-4a8l)
- [Claude Code 技能文档](https://docs.anthropic.com/claude-code)

## 限制

仅当任务明确匹配上述范围（代码审查和逻辑分析）时使用此技能。Logic Lens 提供 AI 驱动的分析，应与人工审查结合用于生产关键决策。不要将输出视为环境特定测试或安全审计的替代品。
