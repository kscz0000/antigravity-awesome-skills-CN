---
name: re-create
description: "当结构性腐化使修补不可行时，完全删除并从零重写文件或模块。触发词：从零重写、完全重写、删除重做、无法挽救、整个模块坏了、推倒重来、结构腐化重写"
risk: critical
source: community
date_added: "2026-06-27"
---

# re-create — 受控清除与重建协议

## 概述

> 虚式「茈」是五条悟最具破坏力的术式——苍与赫合为一体的彻底抹除。但五条悟不会随意使用。他清楚地知道自己要抹除什么、为什么抹除。此处同理：本技能是核武级选项，仅在修补是错误决策时调用，执行时对"什么被清除"和"什么必须存活"拥有完全控制。

重写之所以危险，不在于重建困难，而在于容易静默地抹除原本正常工作的行为。本技能强制要求：在删除任何一行代码之前，必须完成"什么必须存活"的完整盘点；在重建之后，必须验证所有内容确实存活。

---

## 何时使用本技能

- 当文件、模块或组件需要完全删除并从零重写时使用
- 当结构性腐化深到个别修复只会让情况更糟时使用
- 当累积的技术债使代码无法维护时使用
- 当目标已从根本上损坏且无法挽救时使用
- **不得**用于局部重构、单函数修复或定向编辑

---

## 工作原理

### 阶段 1 — 论证清除的必要性

AI 必须证明全面重写是必要的。必须回答以下所有问题：

1. **具体什么坏了或无法挽救？**
   - 不是"代码很乱"——而是使定向修复不可能或适得其反的具体结构性问题
2. **为什么定向编辑会让情况更糟而非更好？**
   - 在腐化之上打补丁、复合复杂性、架构不匹配
3. **保留当前实现的具体代价是什么？**
   - 维护负担、缺陷暴露面、性能、开发者效率

如果 AI 无法清楚地回答以上三个问题，就必须退回到定向编辑而非重写。重写不是对混乱代码的奖赏——它是最后的手段。

> **门槛很高。** "这段代码很难看"不构成使用虚式「茈」的理由。"架构假设 X 但系统现在需要 Y，且每次修补都让不匹配更严重"才构成。

---

### 阶段 2 — 完整读取目标

在提出删除之前，AI 必须完整读取整个目标（文件、模块或组件）。

AI 必须识别并编目：

1. **公共接口** — 代码库其他部分调用的函数、类、类型或导出
2. **隐式契约** — 其他文件依赖的行为，即使没有正式的类型声明
3. **正常行为** — 当前实现正确处理的事项，必须继续工作
4. **非显而易见的逻辑** — 看似偶然实则有意的边界情况、守卫或特殊处理
5. **影响范围** — 代码库中每一个从目标导入或依赖目标的文件

> **即使 AI 之前读过该文件，也不能跳过此阶段。** 目的不是熟悉——而是构建保留清单。

---

### 阶段 3 — 清除声明（用户必须确认）

AI 输出完整的清除计划，并**在删除或写入任何内容之前等待用户确认。**

```
HOLLOW PURPLE — ERASURE PLAN
─────────────────────────────────────────
TARGET FOR ERASURE:
  [file path or module name]

WHY TARGETED FIXES ARE WRONG:
  [specific justification — architectural rot, fundamental mismatch, etc.]

PRESERVATION LIST (must survive the rewrite):
  - [public interface / export 1] → [what it does, who depends on it]
  - [public interface / export 2] → [what it does, who depends on it]
  - [working behavior 1]          → [what it does, why it must be kept]
  - [non-obvious logic 1]         → [what it guards against]

BLAST RADIUS (files that depend on the target):
  - [file path] → depends on [what specifically]
  - [file path] → depends on [what specifically]

NEW IMPLEMENTATION PLAN:
  [Description of what the rebuild will look like — structure, approach, key decisions]

WHAT WILL NOT BE PRESERVED:
  [Anything intentionally dropped and why — dead code, deprecated behavior, etc.]
─────────────────────────────────────────
Confirm to proceed with erasure and rebuild.
```

> **在用户明确确认之前，不删除任何内容。** 回复"是"、"确认"、"执行"或同等表述才算数。沉默不算。

---

### 阶段 4 — 受控清除

用户确认 → 目标被删除。此阶段的规则：

- **干净地删除。** 不是注释掉，不是改名为 `_old`，不是原地归档——是删除。
- **只删除声明的目标。** 清除期间不触碰声明范围之外的任何内容。
- **范围扩大时暂停。** 如果删除过程中发现影响范围列表之外的意外依赖，AI 必须停止并报告后再继续。

---

### 阶段 5 — 依据保留清单重建

AI 编写新实现。规则：

1. **保留清单上的每一项都是义务。** 重建在每一个保留的接口、行为和边界情况都被实现并勾选之前不算完成。
2. **匹配影响范围预期。** 依赖旧实现的文件必须能无修改地使用新实现——除非在阶段 3 中声明了对依赖文件的变更。
3. **不添加额外功能。** 重建只实现声明的内容。新的改进、额外功能和相邻代码的清理是单独的任务。
4. **遵循现有代码库规范。** 新实现必须使用与周围代码库相同的模式、命名约定和风格——而非 AI 偏好的方式。

AI 显式追踪保留进度：

```
REBUILD PROGRESS
─────────────────────────────────────────
Preservation List:
  ✓ [interface 1]         → implemented
  ✓ [working behavior 1]  → implemented
  ✗ [non-obvious logic 1] → pending
─────────────────────────────────────────
```

---

### 阶段 6 — 影响范围验证

重建完成后，AI 检查影响范围中的每一个文件：

1. **重新读取每个依赖文件**并确认它仍可使用新实现
2. **验证每个依赖项**——它依赖的函数签名、导出和行为在重建中存在
3. **标记任何断裂**——如果依赖文件现在出现不匹配，报告并提出修复方案后再宣布完成

最终验证报告：

```
HOLLOW PURPLE — VERIFICATION
─────────────────────────────────────────
Preservation List:          ALL ITEMS ✓
Blast radius files checked:
  - [file] → ✓ compatible with new implementation
  - [file] → ✓ compatible with new implementation
New issues introduced:      NONE / [describe if found]
─────────────────────────────────────────
Status: CLEAN ✓  /  NEEDS FOLLOW-UP ⚠
```

---

## 清除前自检

AI 在阶段 4 开始前必须回答以下全部四个问题：

| # | 问题 | 要求 |
|---|---|---|
| 1 | 我是否已完整读取目标并构建了完整的保留清单？ | 是——否则继续读取 |
| 2 | 我是否已识别完整的影响范围？ | 是——否则继续搜索 |
| 3 | 用户是否已确认清除计划？ | 是——否则等待 |
| 4 | 清除范围是否准确限定在声明内容之内？ | 是——否则重新声明 |

---

## 硬性规则（绝不违反）

- **用户确认前不得删除。** 绝无例外。
- **保留清单完成前不得删除。** 你无法保护尚未盘点的东西。
- **重建期间不得"顺手清理"。** 重建范围严格限定在声明内容内。
- **不得有未声明的影响范围扩展。** 如果依赖文件不在列表中，停止并报告。
- **不得跳过阶段 6。** 在影响范围文件验证完成之前，重建不算完成。
- **不得将重写伪装为重构。** 如果文件变更超过 80%，适用本协议。

---

## 本技能防止的问题

- 重写静默丢弃未记录的、正常工作的边界情况逻辑
- 重建因接口变更而破坏依赖文件
- 因错误原因（风格偏好、无聊）进行重写，而定向修复本可胜任
- 部分重建使代码库处于半旧半新的损坏状态
- 影响范围文件静默断裂，直到运行时才被发现

---

## 快速参考

| 阶段 | 动作 | 是否删除/写入代码？ |
|---|---|---|
| 1 — 论证 | 证明清除的必要性 | 否 |
| 2 — 读取 | 完整读取目标，构建保留清单 | 否 |
| 3 — 声明 | 输出清除计划，等待确认 | 否 |
| 4 — 清除 | 删除声明的目标 | 仅删除 |
| 5 — 重建 | 依据保留清单编写新实现 | 写入 |
| 6 — 验证 | 检查保留清单 + 影响范围 | 否 |

---

## 安全注意事项

- **仅限授权使用：** 本技能涉及破坏性能力（删除文件）。在触发完整重建之前，始终确保你拥有适当的授权和备份。
- **必须明确确认：** 在用户明确确认清除计划之前，绝不删除任何代码。

---

## 示例

### 示例 1：触发完整模块重写
```text
User: "The authentication module is beyond saving. Rewrite this from scratch."

AI: [Outputs HOLLOW PURPLE — ERASURE PLAN]
"Confirm to proceed with erasure and rebuild."

User: "Confirmed."

AI: [Executes Phase 4 and 5: Controlled Erasure and Rebuild against the Preservation List]
```

### 示例 2：阶段 1 正确拒绝清除
```text
User: "This data formatting script is a mess, rewrite it from scratch."

AI: [Evaluates Phase 1 criteria]
"I cannot justify a full rewrite. While the code is messy, the structural rot is not deep enough to make patching impossible. The blast radius is limited, and targeted edits will improve it without the risk of erasing undocumented behaviors. I will proceed with surgical refactoring instead."
```

---

## 触发词

- "从零重写" / "rewrite this from scratch"
- "删除重做" / "delete this and redo it"
- "无法挽救 / 无法修复" / "beyond saving / beyond repair"
- "整个模块 / 组件 / 文件坏了" / "the whole module / component / file is broken"
- "推倒重来" / "start over on this"
- 任何修补会使问题恶化而非解决的情况

---

## 局限性

- AI 必须显式论证重写的必要性，并在删除任何内容前获得用户确认。
- 重建范围必须精确匹配声明内容（不得添加额外功能或额外清理）。
- 不适用于局部重构、单函数修复或定向缺陷修复。
- 需要预先识别完整的影响范围，以避免静默破坏依赖关系。
