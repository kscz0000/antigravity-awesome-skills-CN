---
name: codebase-design
description: 用于设计深层模块的共享词汇。当用户希望设计或改进模块的接口、寻找深化机会、决定接缝位置、让代码更易测试或更易被 AI 导航，或当其他技能需要"深层模块"词汇时使用。触发词：深层模块、深度设计、接口设计、模块深化、接缝设计、可测试性、AI 导航、共享词汇。
category: "architecture"
risk: "safe"
source: "community"
source_repo: "mattpocock/skills"
source_type: "community"
date_added: "2026-06-19"
author: "Matt Pocock"
license: "MIT"
license_source: "https://github.com/mattpocock/skills/blob/main/LICENSE"
tags:
  - architecture
  - workflow
  - coding-agents
tools:
  - claude-code
  - codex-cli
  - cursor
---

# 代码库设计

## 何时使用

当该工作流匹配用户请求时使用：用于设计深层模块的共享词汇。当用户希望设计或改进模块的接口、寻找深化机会、决定接缝放在哪里、让代码更易测试或更易被 AI 导航，或当其他技能需要"深层模块"词汇时使用。


_来源：[mattpocock/skills](https://github.com/mattpocock/skills)（MIT）。_

设计**深层模块**：在干净的接缝背后，小接口承载大量行为，并且能通过该接口进行测试。无论代码是被设计还是被重构，都请使用这套语言和这些原则。目标是让调用者获得杠杆，让维护者获得局部性，让所有人都能轻松测试。

## 术语表

请严格使用这些术语——不要用"component（组件）"、"service（服务）"、"API"或"boundary（边界）"来替代。统一语言正是关键所在。

**Module（模块）** — 任何拥有接口和实现的东西。刻意保持规模无关：可以是函数、类、包，或横跨多个层次的切片。_避免使用_：unit、component、service。

**Interface（接口）** — 调用者为了正确使用模块而必须知晓的一切：类型签名，以及不变式、顺序约束、错误模式、必需配置、性能特征。_避免使用_：API、signature（过于狭窄——它们仅指类型层面的表面）。

**Implementation（实现）** — 模块内部的内容，即其代码主体。与 **Adapter（适配器）** 不同：同一个东西既可以是小型适配器配大型实现（例如 Postgres 仓储），也可以是大型适配器配小型实现（例如内存版伪实现）。当话题围绕接缝时使用"adapter"；其他情况下使用"implementation"。

**Depth（深度）** — 接口处的杠杆：调用者（或测试）每学习一单位接口所能驱动多少行为。当大量行为位于小接口背后时，模块是**深**的；当接口几乎和实现一样复杂时，模块是**浅**的。

**Seam（接缝）** _（Michael Feathers）_ — 可以在不修改该处的前提下改变行为的地方；即模块接口所栖息的*位置*。接缝放在哪里本身就是一个独立的设计决策，与背后放什么无关。_避免使用_：boundary（与 DDD 的 bounded context 含义重叠）。

**Adapter（适配器）** — 在接缝处满足接口的具体事物。它描述的是*角色*（它填补什么槽位），而非实质（里面有什么）。

**Leverage（杠杆）** — 调用者从深度中获得的收益：每学习一单位接口就能获得更多能力。一份实现在 N 个调用点和 M 个测试中被反复兑现。

**Locality（局部性）** — 维护者从深度中获得的收益：变更、缺陷、知识和验证都集中在一处，而不是分散在各个调用点。改一处，处处生效。

## 深层 vs 浅层

**深层模块** = 小接口 + 大量实现：

```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**浅层模块** = 大接口 + 少量实现（应避免）：

```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

在设计接口时，问自己：

- 能否减少方法数量？
- 能否简化参数？
- 能否把更多复杂度藏在内部？

## 原则

- **深度是接口的属性，而非实现的属性。** 深层模块在内部可以由小巧、可 mock、可替换的部分组成——它们只是不构成接口的一部分。模块既可以有**内部接缝**（对实现私有、由其自身测试使用），也可以在接口处拥有**外部接缝**。
- **删除测试。** 想象删除该模块。如果复杂度随之消失，它就是一个透传层；如果复杂度在 N 个调用点重新出现，那它就值得保留。
- **接口即测试表面。** 调用者和测试穿越的是同一条接缝。如果你想越过接口去测试，那模块的形状多半是错的。
- **一个适配器意味着假设的接缝，两个适配器意味着真实的接缝。** 除非真的有事物跨接缝变化，否则不要引入接缝。

## 为可测试性而设计

好的接口让测试变得自然：

1. **接受依赖，不要创建依赖。**

   ```typescript
   // Testable
   function processOrder(order, paymentGateway) {}

   // Hard to test
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **返回结果，不要产生副作用。**

   ```typescript
   // Testable
   function calculateDiscount(cart): Discount {}

   // Hard to test
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **较小的表面积。** 方法越少，所需测试越少；参数越少，测试装配越简单。

## 关系

- 一个 **Module** 恰好有一个 **Interface**（它向调用者和测试呈现的表面）。
- **Depth** 是 **Module** 的属性，针对其 **Interface** 衡量。
- **Seam** 是 **Module** 的 **Interface** 所栖息的所在。
- **Adapter** 位于 **Seam** 之上，并满足 **Interface**。
- **Depth** 为调用者带来 **Leverage**，为维护者带来 **Locality**。

## 被拒斥的框架

- **以"实现行数 / 接口行数"衡量深度**（Ousterhout）：会鼓励把实现写得更长。我们采用"深度即杠杆"的定义。
- **把"Interface"理解为 TypeScript 的 `interface` 关键字或类的公共方法**：过于狭窄——这里的接口涵盖调用者必须知晓的每一项事实。
- **"Boundary"**：与 DDD 的 bounded context 含义重叠。请说 **seam** 或 **interface**。

## 进一步深入

- **在已知依赖的前提下深化模块簇** —— 参见 [DEEPENING.md](DEEPENING.md)：依赖分类、接缝纪律，以及"替换而非堆叠"的测试方法。
- **探索替代接口** —— 参见 [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md)：并行启动多个子智能体，以截然不同的方式设计接口，再在深度、局部性和接缝位置上进行比较。


## 局限性

- 当工作流明确指定上游工具、账号、API 密钥或本地配置时，需要具备相应条件。
- 未经用户明确批准，不会执行破坏性、生产性、付费或对外发送消息的操作。
- 在把生成的产物或建议当作最终结论之前，需根据用户的真实来源进行验证。