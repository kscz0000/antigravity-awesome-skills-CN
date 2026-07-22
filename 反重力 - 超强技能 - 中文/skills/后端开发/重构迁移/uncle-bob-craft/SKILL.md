---
name: uncle-bob-craft
description: "在代码审查、编写或重构代码、讨论架构时使用；补充 clean-code 项目，不替代 linter/formatter。触发词：代码审查、重构、架构讨论、设计模式、Uncle Bob"
category: code-quality
risk: safe
source: community
date_added: "2026-03-06"
author: antigravity-contributors
tags: [clean-code, clean-architecture, solid, code-review, craftsmanship, uncle-bob]
tools: [claude, cursor, gemini]
---

# Uncle Bob 工程实践

运用 Robert C. Martin（Uncle Bob）的准则进行**代码审查和生产开发**：Clean Code、Clean Architecture、The Clean Coder、Clean Agile 以及设计模式规范。本技能与现有的 `@clean-code`（聚焦 Clean Code 一书）以及项目的 linter/formatter **互补**，而非替代它们。

## 概述

本技能汇集了 Uncle Bob 系列著作中的核心原则，用于**审查**和**编写**代码：命名与函数（通过 `@clean-code`）、架构与边界（Clean Architecture）、职业素养与估算（The Clean Coder）、敏捷价值观与实践（Clean Agile）、设计模式的正确使用与误用。用它来评估结构、依赖关系、SOLID 原则、代码异味和职业实践。它只提供工程和设计层面的准则——语法和格式化仍由你的 linter 和 formatter 负责。

## 使用场景

- **代码审查**：应用依赖规则、边界、SOLID 和异味启发式方法；提出具体重构建议。
- **重构**：判断哪些该提取、边界划在哪里、设计模式是否合理。
- **架构讨论**：检查分层边界、依赖方向、关注点分离。
- **设计模式**：在引入模式前，评估是否正确使用还是盲目套用或过度使用。
- **估算与职业素养**：应用 Clean Coder 的理念（敢于说不、可持续节奏、三点估算）。
- **敏捷实践**：在讨论流程时引用 Clean Agile（铁十字、TDD、重构、结对编程）。
- **不要用**它替代或覆盖项目的 linter、formatter 或自动化测试。

## 按来源索引

| 来源 | 关注点 | 参考位置 |
|--------|--------|-------------|
| **Clean Code** | 命名、函数、注释、格式化、测试、类、异味 | 使用 `@clean-code` 获取详情；本技能在审查/生产中引用它。 |
| **Clean Architecture** | 依赖规则、分层、边界、架构中的 SOLID | 见 [reference.md](./reference.md) 和 [references/clean-architecture.md](./references/clean-architecture.md)。 |
| **The Clean Coder** | 职业素养、估算、说不、可持续节奏 | 见 [reference.md](./reference.md) 和 [references/clean-coder.md](./references/clean-coder.md)。 |
| **Clean Agile** | 价值观、铁十字、TDD、重构、结对编程 | 见 [reference.md](./reference.md) 和 [references/clean-agile.md](./references/clean-agile.md)。 |
| **设计模式** | 何时使用、误用、盲目套用 | 见 [reference.md](./reference.md) 和 [references/design-patterns.md](./references/design-patterns.md)。 |

## 设计模式：正确使用 vs 误用

- **使用模式**的时机是解决真正的设计问题（如行为变化、生命周期或横切关注点），而不是为了看起来"企业级"。
- **避免盲目套用**：不要因为代码库"应该"有 Factory/Strategy/Repository 就添加它们；只有在重复或僵化确实需要抽象时才添加。
- **误用的信号**：每个类名都包含模式名称、只有转发没有逻辑的层、让简单代码更难理解的模式。
- **经验法则**：当你感受到第三次重复或第二次变更理由时引入模式；在代码或文档中命名模式以明确意图。

## 代码异味与启发式（摘要）

| 异味 / 启发式 | 含义 |
|-------------------|--------|
| **僵化** | 小改动迫使多处修改。 |
| **脆弱** | 修改破坏了不相关的区域。 |
| **不可移植** | 难以在其他上下文中复用。 |
| **粘滞** | 走捷径容易，做正确的事很难。 |
| **不必要复杂** | 投机性或未使用的抽象。 |
| **不必要重复** | 违反 DRY；同一概念出现在多处。 |
| **不透明** | 代码难以理解。 |

完整列表（包括 C1–T9 风格的启发式规则）在 [reference.md](./reference.md) 中。在审查中用它们命名问题并建议重构（提取、移动依赖、引入边界）。

## 审查 vs 生产

| 场景 | 应用方式 |
|---------|--------|
| **代码审查** | 依赖规则和边界；SOLID 在上下文中的应用；列出异味；建议一两个具体重构（如提取函数、反转依赖）；检查测试和职业素养（测试是否存在、无明显的压力妥协）。 |
| **编写新代码** | 优先使用小函数和单一职责；向内依赖（Clean Architecture）；做 TDD 时先写测试；在重复或变化证明其合理性之前避免使用模式。 |
| **重构** | 每次识别一个异味；小步重构并保持测试通过；在添加行为之前先改善命名和结构。 |

## 工作方式

### 审查代码时

1. **边界和依赖规则**：检查依赖是否指向内层（如用例不依赖 UI 或 DB 细节）。见 [references/clean-architecture.md](./references/clean-architecture.md)。
2. **SOLID 在上下文中**：检查单一职责、开闭原则、里氏替换、接口隔离、依赖倒置是否适用于被修改的代码。
3. **异味**：扫描僵化、脆弱、不可移植、粘滞、不必要复杂/重复、不透明；列出文件/区域。
4. **具体建议**：提出一两个重构（如"将此提取为名为 X 的函数"、"引入接口使该层不依赖具体的 DB 客户端"）。
5. **测试与工程素养**：注意测试是否存在、变更是否尊重可持续节奏（没有明显的"以后再修"这类违反职业素养的注释）。

### 编写或重构代码时

1. 优先使用**小而单一职责**的函数和类；使用 `@clean-code` 处理命名和结构。
2. 保持**依赖指向内层**；业务规则放中心，适配器放边缘。
3. 仅在重复或变化证明其合理性时才引入**设计模式**。
4. **小步重构**并保持测试通过。

## 示例

### 示例 1：代码审查提示词（可直接复制粘贴）

用此请求一次 Uncle Bob 风格的审查：

```markdown
Please review this change using Uncle Bob craft criteria (@uncle-bob-craft):
1. Dependency Rule and boundaries — do dependencies point inward?
2. SOLID in context — any violations in the touched code?
3. Smells — list rigidity, fragility, immobility, viscosity, needless complexity/repetition, or opacity.
4. Suggest one or two concrete refactors (e.g., extract function, invert dependency).
Do not duplicate lint/format; focus on structure and design.
```

### 示例 2：重构前后（提取并命名）

**重构前（不透明，职责不单一）：**

```python
def process(d):
    if d.get("t") == 1:
        d["x"] = d["a"] * 1.1
    elif d.get("t") == 2:
        d["x"] = d["a"] * 1.2
    return d
```

**重构后（意图清晰，抽象层级一致）：**

```python
def apply_discount(amount: float, discount_type: int) -> float:
    if discount_type == 1:
        return amount * 1.1
    if discount_type == 2:
        return amount * 1.2
    return amount

def process(order: dict) -> dict:
    order["x"] = apply_discount(order["a"], order.get("t", 0))
    return order
```

## 最佳实践

- ✅ 使用 `@clean-code` 处理命名、函数、注释和格式化；使用本技能处理架构、边界、SOLID、异味和流程。
- ✅ 审查时命名异味或原则（如"依赖规则违反：用例从 web 框架导入"）。
- ✅ 每次审查至少提出一个具体重构建议（提取、重命名、反转依赖）。
- ✅ 单独运行项目的 linter 和 formatter；本技能不替代它们。
- ❌ 不要用本技能强制语法或格式；那是 linter 的工作。
- ❌ 不要在没有明确重复或变化理由的情况下添加设计模式。

## 常见陷阱

- **问题：** 把每个类都当作需要 Factory 或 Strategy。
  **解决：** 只在有真正设计需求时（第三次重复、第二个变更轴）才引入模式。

- **问题：** 审查只列出"违反 SOLID"却不说明在哪里、如何违反。
  **解决：** 指出具体的文件/函数和违反的原则（如"SRP：这个函数既解析又持久化；应拆分为解析和持久化"）。

- **问题：** 因为"我们用了 Uncle Bob"就跳过项目 linter。
  **解决：** 本技能关注工程素养和设计；始终运行项目的 lint 和 format。

## 相关技能

- **`@clean-code`** — Clean Code 一书的详细内容（命名、函数、注释、格式化、测试、类、异味）。用于日常代码质量；uncle-bob-craft 用于架构和跨书准则。
- **`@architecture`** — 通用架构决策和权衡。用于选择高层结构；uncle-bob-craft 用于依赖规则和边界。
- **`@code-review-excellence`** — 代码审查实践。与 uncle-bob-craft 结合用于基于原则的审查。
- **`@refactor-clean-code`** — 向 Clean Code 重构。在为边界和 SOLID 重构时与 uncle-bob-craft 配合使用。
- **`@test-driven-development`** — TDD 工作流。与 Clean Agile 和 Clean Coder 对齐（测试即需求、可持续节奏）。

## 局限性

- **不替代项目的 linter 或 formatter。** 单独运行 lint 和 format；本技能仅提供设计和工程准则。
- **不替代自动化测试。** 它可以提醒你写测试（Clean Coder、Clean Agile），但不运行或生成测试。
- **与工具互补。** 与现有的 CI、lint 和测试套件配合使用。
- **不强制语法或样式。** 它聚焦于结构、依赖、异味和职业实践，而非花括号风格或行长度。
- **是摘要，不是原书。** 完整的 Clean Code 启发式规则、组件原则（REP/CCP/CRP、ADP/SDP/SAP）和详细案例在书中；我们引用最常用的部分。见 [reference.md](./reference.md) 的"范围与出处"。
