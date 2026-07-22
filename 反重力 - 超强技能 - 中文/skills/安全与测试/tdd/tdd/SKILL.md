---
name: tdd
description: 测试驱动开发。当用户希望以测试先行方式构建功能或修复 bug、提到"红绿重构"、或希望编写集成测试时使用。
category: "development"
risk: "safe"
source: "community"
source_repo: "mattpocock/skills"
source_type: "community"
date_added: "2026-06-19"
author: "Matt Pocock"
license: "MIT"
license_source: "https://github.com/mattpocock/skills/blob/main/LICENSE"
tags:
  - engineering
  - workflow
  - coding-agents
tools:
  - claude-code
  - codex-cli
  - cursor
---

# 测试驱动开发

## 适用场景

当工作流与用户请求匹配时使用本技能：按其文档化的工作流执行。

_来源：[mattpocock/skills](https://github.com/mattpocock/skills)（MIT）。_

## 理念

**核心原则**：测试应当通过公共接口验证行为，而非实现细节。代码可以彻底改变；测试不应随之改变。

**好测试**是集成风格的：通过公共 API 走真实的代码路径。它们描述系统_做什么_，而非_怎么做_。好的测试读起来像一份规约——"用户能用有效购物车完成结算"，一眼就能看出系统具备什么能力。这类测试不关心内部结构，因此扛得住重构。

**坏测试**与实现细节紧耦合：它们 mock 内部协作者、测试私有方法，或通过外部手段验证（例如绕过接口直接查数据库）。警报信号：测试在重构时挂掉，而行为并未变化。如果你改了内部函数的名字，测试就挂了，那这些测试当初测的就是实现，而非行为。

可参考 [tests.md](tests.md) 中的示例，以及 [mocking.md](mocking.md) 中的 mock 使用准则。

## 反模式：水平切片

**绝对不要先写完所有测试，再去写所有实现。** 这就是"水平切片"——把 RED 理解为"写完所有测试"，把 GREEN 理解为"写完所有代码"。

这会产生**糟糕的测试**：

- 批量写出的测试，测的是_想象中的_行为，而非_实际的_行为
- 你最终测的是_形状_（数据结构、函数签名），而非面向用户的行为
- 测试对真实变更不敏感——行为坏了它通过，行为正常它又挂
- 你跑得比车灯还快，在理解实现之前就锁定了测试结构

**正确做法**：用追踪子弹走纵向切片。一个测试 → 一份实现 → 循环往复。每个测试都在响应你从上一步学到的东西。因为刚刚写过代码，你清楚什么行为重要，以及如何验证。

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## 工作流

### 1. 规划

探索代码库时，先阅读 `CONTEXT.md`（如果存在），让测试命名和接口用词贴合项目的领域语言，并尊重你所触及区域的 ADR。

开始写代码之前：

- [ ] 与用户确认需要哪些接口变更
- [ ] 与用户确认要测试哪些行为（排出优先级）
- [ ] 寻找深度模块的机会（小接口、深实现）——运行 `/codebase-design` 技能获取用词与可测试性检查
- [ ] 列出要测试的行为（不是实现步骤）
- [ ] 取得用户对计划的确认

提问："公共接口应当长什么样？哪些行为最重要、必须先测？"

**你不可能什么都测。** 与用户明确确认哪些行为最重要。把测试精力集中在关键路径和复杂逻辑上，而非每一个可能的边界情况。

### 2. 追踪子弹

写一个测试，只验证系统的一件事：

```
RED:   Write test for first behavior → test fails
GREEN: Write minimal code to pass → test passes
```

这就是你的追踪子弹——证明这条端到端路径走得通。

### 3. 增量循环

对剩下每一个行为：

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

规则：

- 一次一个测试
- 只写刚好让当前测试通过的代码
- 不要为未来的测试做预判
- 测试聚焦于可观察的行为

### 4. 重构

所有测试通过后，再寻找[重构候选](refactoring.md)：

- [ ] 抽取重复
- [ ] 加深模块（把复杂度藏在简单接口之后）
- [ ] 在自然处应用 SOLID 原则
- [ ] 思考新代码揭示出的现有代码问题
- [ ] 每一步重构后跑一遍测试

**RED 期间绝不重构。** 先走到 GREEN。

## 每次循环的检查清单

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```

## 局限性

- 当工作流点名了上游工具、账号、API key 或本地设置时，需要相应准备。
- 未取得用户明确同意前，不会执行破坏性、生产级、付费或对外消息类操作。
- 在把生成的产物或建议当作最终结果之前，请用用户的真实来源进行核验。
