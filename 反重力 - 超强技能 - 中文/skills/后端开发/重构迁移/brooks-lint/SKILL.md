---
name: brooks-lint
description: "基于经典软件工程书籍的 AI 代码审查器，用于捕捉设计异味、耦合问题和架构风险。触发词：代码审查、架构审查、设计异味、耦合分析、代码质量、brooks-lint、设计评审、重构前检查、代码审查工具"
category: development
risk: safe
source: community
source_repo: hyhmrright/brooks-lint
source_type: community
license: "MIT"
license_source: "https://github.com/hyhmrright/brooks-lint/blob/main/LICENSE"
date_added: "2026-04-29"
author: hyhmrright
tags: [code-review, architecture, software-design, refactoring, claude-code]
tools: [claude, codex, cursor, gemini]
---

# Brooks Lint

## 概述

Brooks Lint 是一个 Claude Code 技能，通过 12 本经典软件工程书籍的视角来审查你的代码。它不检查风格规则，而是问：《程序员修炼之道》、《代码整洁之道》和《数据密集型应用系统设计》的作者会如何评价这段代码？

它将里程碑式工程书籍中的原则综合为可操作的、结构化的反馈——捕捉设计异味、紧耦合、缺失的抽象以及 linter 和 AI 工具通常遗漏的架构风险。

以《人月神话》作者 Fred Brooks 命名——因为最难的 bug 是概念性的，而非语法性的。

## 12 本书籍

| 书籍 | 应用的核心原则 |
|------|----------------------|
| *The Pragmatic Programmer* | DRY、正交性、曳光弹 |
| *Clean Code* | 命名、函数大小、注释清晰度 |
| *The Mythical Man-Month* | 概念完整性、第二系统效应 |
| *Designing Data-Intensive Applications* | 数据一致性、容错性、可扩展性 |
| *A Philosophy of Software Design* | 深模块、信息隐藏、复杂度 |
| *Refactoring* | 代码异味、提取方法、封装 |
| *Working Effectively with Legacy Code* | 接缝、特征测试、依赖破解 |
| *Domain-Driven Design* | 统一语言、限界上下文、聚合 |
| *Release It!* | 稳定性模式、超时、隔舱、熔断器 |
| *Structure and Interpretation of Computer Programs* | 抽象、递归、元语言抽象 |
| *The Art of UNIX Programming* | 模块化、可组合性、最小惊讶原则 |
| *Extreme Programming Explained* | YAGNI、简单设计、集体所有权 |

## 何时使用此技能

- 当你需要超越 linter 提供的架构反馈时使用
- 在大规模重构前识别结构性债务时使用
- 当审查"能工作但感觉不对"的代码时使用
- 当入职新代码库以快速定位风险区域时使用
- 在开始新模块或服务前进行设计评审时使用

## 工作原理

Brooks Lint 将每本书的核心原则作为审查视角应用：

1. **异味检测**：标记违反 DRY、SRP、迪米特法则等的情况
2. **耦合分析**：识别紧依赖和缺失的抽象层
3. **命名批评**：将 Clean Code 命名规则应用于变量、方法、类
4. **架构审查**：检查 DDIA 风格的数据一致性和容错缺口
5. **稳定性模式**：标记缺失的超时、重试和熔断器（Release It!）
6. **复杂度评分**：应用 APOSD 复杂度指标识别过度工程化部分

## 安装

```bash
# Install via Claude Code plugin marketplace
# Search: "brooks-lint" in Claude Code > Extensions

# Or install via NPX (Antigravity)
npx antigravity-awesome-skills --claude
# Then invoke: @brooks-lint
```

## 示例

### 示例 1：审查服务类

```
@brooks-lint review src/services/PaymentService.ts
```

**Brooks Lint 输出：**
```
[Pragmatic Programmer] DRY violation: payment validation logic duplicated in 3 places
[Clean Code] Method processPayment() does 4 things — violates Single Responsibility
[Release It!] No timeout on external payment gateway call — risk of cascade failure
[DDIA] No idempotency key — retry on network error will double-charge
[APOSD] PaymentService knows too much about UserRepository — high coupling
```

### 示例 2：完整代码库架构审查

```
@brooks-lint analyze the overall architecture of this codebase
```

### 示例 3：重构前审查

```
@brooks-lint what are the biggest design smells in this module before I refactor it?
```

## 审查类别

| 类别 | 应用的书籍 | 捕捉的问题 |
|----------|--------------|-----------------|
| **DRY / 重复** | PP, Refactoring | 复制粘贴代码、未提取的共享逻辑 |
| **命名** | Clean Code, DDD | 不清晰的名称、违反领域语言 |
| **耦合** | APOSD, PP | 紧依赖、缺失接口 |
| **稳定性** | Release It! | 缺失超时、无重试逻辑、无熔断器 |
| **数据完整性** | DDIA | 竞态条件、非幂等操作 |
| **复杂度** | APOSD, SICP | 过度工程化、不必要的抽象 |
| **遗留债务** | WELC | 难以测试的代码、缺失接缝 |
| **领域清晰度** | DDD, XP | 贫血模型、缺失限界上下文 |

## 最佳实践

- 在编写新的服务层或数据管道后运行 `@brooks-lint`
- 与 `@logic-lens` 结合使用以获得完整覆盖：逻辑 bug + 设计异味
- 在增长的代码库上每周使用 `@brooks-lint analyze architecture`
- 首先关注 CRITICAL 和 HIGH 发现——LOW 发现是风格建议

## 相关技能

- `@logic-lens` — 互补：捕捉逻辑 bug；brooks-lint 捕捉设计问题
- `@security-auditor` — 专门的仅安全深度扫描
- `@lint-and-validate` — 风格/语法检查，与设计审查并行运行

## 其他资源

- [GitHub Repository](https://github.com/hyhmrright/brooks-lint)
- [Dev.to Article: I Synthesized 12 Classic Engineering Books into an AI Code Reviewer](https://dev.to/hyhmrright/i-synthesized-12-classic-engineering-books-into-an-ai-code-reviewer-heres-what-it-caught-3ed1)
- [Related skill: logic-lens](https://github.com/hyhmrright/logic-lens)

## 限制

仅当任务明确匹配上述范围（设计审查和架构分析）时使用此技能。Brooks Lint 应用基于既定工程原则的 AI 驱动分析。它应该补充——而非替代——针对生产关键决策的人工设计审查。结果反映 12 本源书籍的原则，可能不适用于所有架构风格或领域。
