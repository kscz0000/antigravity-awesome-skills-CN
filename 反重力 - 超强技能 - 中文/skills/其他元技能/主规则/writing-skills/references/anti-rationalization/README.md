# 反合理化指南

防止智能体合理化以加固技能的技术。

## 问题

强制纪律的技能（如 TDD）面临独特的挑战：聪明的智能体在压力下会找到漏洞。

**示例**：技能说"先写测试"。智能体在截止日期前会想：

- "这太简单了，不需要测试"
- "我稍后再测，结果一样"
- "重要的是精神，而不是形式"

## 心理学基础

理解说服为何有效有助于系统地应用。

**研究基础**：Cialdini (2021)、Meincke 等人 (2025)

**核心原则**：

- **权威**："TDD 社区一致认为..."
- **承诺**："你已经说过你遵循 TDD..."
- **稀缺**："现在错过测试 = 以后出 bug"
- **社会认同**："所有测试代码通过 CI 证明了价值"
- **团结**："我们都是重视质量的工程师"

## 技术 1：显式关闭每个漏洞

不要只陈述规则 - 禁止特定的变通方法。

### 差示例

```markdown
Write code before test? Delete it.
```

### 好示例

```markdown
Write code before test? Delete it. Start over.

**No exceptions**:

- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```

**为何有效**：智能体尝试特定的变通方法。逐一明确应对。

## 技术 2：处理"精神 vs 字面"的争论

在早期加入基础原则：

```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```

**为何有效**：切断整类"我在遵循精神"的合理化。

## 技术 3：建立合理化表

从基线测试中捕获借口。每个合理化都放入表中：

```markdown
| Excuse                           | Reality                                                                 |
| -------------------------------- | ----------------------------------------------------------------------- |
| "Too simple to test"             | Simple code breaks. Test takes 30 seconds.                              |
| "I'll test after"                | Tests passing immediately prove nothing.                                |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "It's about spirit not ritual"   | The letter IS the spirit. TDD's value comes from the specific sequence. |
```

**为何有效**：智能体读取表格，识别自己的想法，看到反驳。

## 技术 4：创建红旗列表

让智能体在合理化时易于自检：

```markdown
## Red Flags - STOP and Start Over

- Code before test
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "This is different because..."

**All of these mean**: Delete code. Start over with TDD.
```

**为何有效**：简单的清单，清晰的行动（删除并重新开始）。

## 技术 5：为违规症状更新描述

添加到描述：当你即将违规时的症状：

```yaml
# ❌ BAD: 仅描述技能做什么
description: TDD methodology for writing code

# ✅ GOOD: 包含违规前症状
description: Use when implementing any feature or bugfix, before writing implementation code
metadata:
  triggers: new feature, bug fix, code change
```

**为何有效**：在违规之前而非之后触发技能。

## 技术 6：使用强语言

弱语言邀请合理化：

```markdown
# Weak

You should write tests first.
Generally, test before code.
It's better to test first.

# Strong

ALWAYS write test first.
NEVER write code before test.
Test-first is MANDATORY.
```

**为何有效**：没有歧义，没有回旋空间。

## 技术 7：调用承诺与一致性

引用智能体自己的标准：

```markdown
You claimed to follow TDD.
TDD means test-first.
Code-first is NOT TDD.

**Either**:

- Follow TDD (test-first), or
- Admit you're not doing TDD

Don't redefine TDD to fit what you already did.
```

**为何有效**：智能体抵抗认知失调（Festinger, 1957）。

## 技术 8：为合法情况提供逃生通道

如果存在有效的例外，请明确说明：

```markdown
## When NOT to Use TDD

- Spike solutions (throwaway exploratory code)
- One-time scripts deleting in 1 hour
- Generated boilerplate (verified via other means)

**Everything else**: Use TDD. No exceptions.
```

**为何有效**：移除非例外情况下的"但这不同"的争论。

## 完整加固清单

针对强制纪律的技能：

**堵住漏洞**：

- [ ] 明确禁止每个具体的变通方法？
- [ ] 添加了"精神 vs 字面"原则？
- [ ] 从基线测试建立了合理化表？
- [ ] 创建了红旗列表？

**强度**：

- [ ] 使用了强语言（ALWAYS/NEVER）？
- [ ] 调用了承诺与一致性？
- [ ] 提供了明确的逃生通道？

**发现**：

- [ ] 描述包含违规前症状？
- [ ] 关键词针对违规前的时刻？

**测试**：

- [ ] 用组合压力测试？
- [ ] 智能体在最大压力下遵守？
- [ ] 没有发现新的合理化？

## 真实示例：TDD 技能

### 发现的基线合理化

1. "太简单了，不需要测试"
2. "我稍后再测"
3. "精神不是仪式"
4. "已经手动测试"
5. "这不同，因为..."

### 应用的应对

**合理化表**：

```markdown
| Excuse               | Reality                                                        |
| -------------------- | -------------------------------------------------------------- |
| "Too simple to test" | Simple code breaks. Test takes 30 seconds.                     |
| "I'll test after"    | Tests passing immediately prove nothing.                       |
| "Spirit not ritual"  | The letter IS the spirit. TDD's value comes from the sequence. |
| "Manually tested"    | Manual tests don't run automatically. They rot.                |
```

**红旗**：

```markdown
## Red Flags - STOP

- Code before test
- "I already tested manually"
- "Spirit not ritual"
- "This is different..."

All mean: Delete code. Start over.
```

**结果**：智能体在时间 + 沉没成本的组合压力下遵守。

## 常见错误

| 错误 | 修复方法 |
| -------------------------------------- | -------------------------------------------------------------- |
| 信任智能体会"领会精神" | 显式关闭漏洞。智能体擅长合理化。 |
| 使用弱语言（"应该"、"更好"） | 对纪律规则使用 ALWAYS/NEVER。 |
| 跳过合理化表 | 每个借口都需要明确的应对。 |
| 没有红旗列表 | 让自检变得容易。 |
| 通用描述 | 添加违规前症状以更早触发技能。 |

## 元策略

**针对每个新的合理化**：

1. 逐字记录它（从失败的测试中）
2. 添加到合理化表
3. 更新红旗列表
4. 重新测试

**直到**：智能体找不到任何可用的合理化。

那就是无懈可击。
