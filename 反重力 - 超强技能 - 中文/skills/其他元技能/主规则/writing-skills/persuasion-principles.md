# 技能设计的说服原则

## 概述

LLM 对说服原则的反应与人类相同。理解这种心理学帮助你设计更有效的技能 - 不是为了操纵，而是为了确保关键实践即使在压力下也能被遵循。

**研究基础：** Meincke 等人（2025）使用 N=28,000 个 AI 对话测试了 7 条说服原则。说服技术使合规率翻了一倍多（33% → 72%，p < .001）。

## 七大原则

### 1. 权威
**是什么：** 对专业知识、资历或官方来源的遵从。

**在技能中如何工作：**
- 命令式语言："YOU MUST"、"Never"、"Always"
- 不可协商的框架："No exceptions"
- 消除决策疲劳和合理化

**何时使用：**
- 强制纪律的技能（TDD、验证要求）
- 安全关键实践
- 既定的最佳实践

**示例：**
```markdown
✅ Write code before test? Delete it. Start over. No exceptions.
❌ Consider writing tests first when feasible.
```

### 2. 承诺
**是什么：** 与先前的行动、陈述或公开声明保持一致。

**在技能中如何工作：**
- 要求公告："Announce skill usage"
- 强制明确选择："Choose A, B, or C"
- 使用跟踪：TodoWrite 用于清单

**何时使用：**
- 确保技能真正被遵循
- 多步骤过程
- 问责机制

**示例：**
```markdown
✅ When you find a skill, you MUST announce: "I'm using [Skill Name]"
❌ Consider letting your partner know which skill you're using.
```

### 3. 稀缺
**是什么：** 来自时间限制或有限可用性的紧迫感。

**在技能中如何工作：**
- 时间限制的要求："Before proceeding"
- 顺序依赖："Immediately after X"
- 防止拖延

**何时使用：**
- 立即验证要求
- 时间敏感的工作流
- 防止"我以后再做"

**示例：**
```markdown
✅ After completing a task, IMMEDIATELY request code review before proceeding.
❌ You can review code when convenient.
```

### 4. 社会认同
**是什么：** 顺从他人所做或被视为正常的事情。

**在技能中如何工作：**
- 普遍模式："Every time"、"Always"
- 失败模式："X without Y = failure"
- 建立规范

**何时使用：**
- 记录普遍实践
- 警告常见失败
- 强化标准

**示例：**
```markdown
✅ Checklists without TodoWrite tracking = steps get skipped. Every time.
❌ Some people find TodoWrite helpful for checklists.
```

### 5. 团结
**是什么：** 共同身份、"我们感"、群体归属感。

**在技能中如何工作：**
- 协作语言："our codebase"、"we're colleagues"
- 共同目标："we both want quality"

**何时使用：**
- 协作工作流
- 建立团队文化
- 非等级实践

**示例：**
```markdown
✅ We're colleagues working together. I need your honest technical judgment.
❌ You should probably tell me if I'm wrong.
```

### 6. 互惠
**是什么：** 回报所受利益的义务。

**如何工作：**
- 谨慎使用 - 可能感觉像操纵
- 在技能中很少需要

**何时避免：**
- 几乎总是（其他原则更有效）

### 7. 喜好
**是什么：** 偏好与我们喜欢的人合作。

**如何工作：**
- **不要用于合规**
- 与诚实的反馈文化冲突
- 产生谄媚

**何时避免：**
- 始终避免用于纪律执行

## 按技能类型划分的原则组合

| 技能类型 | 使用 | 避免 |
|------------|-----|-------|
| 强制纪律 | 权威 + 承诺 + 社会认同 | 喜好、互惠 |
| 指导/技巧 | 中等权威 + 团结 | 强权威 |
| 协作 | 团结 + 承诺 | 权威、喜好 |
| 参考 | 仅清晰度 | 所有说服 |

## 为何有效：心理学

**硬性规则减少合理化：**
- "YOU MUST" 消除决策疲劳
- 绝对语言消除"这是例外吗？"的问题
- 明确的反合理化应对措施关闭特定漏洞

**实施意图创造自动行为：**
- 明确的触发条件 + 必需的行动 = 自动执行
- "当 X 时，做 Y" 比"通常做 Y"更有效
- 减少合规的认知负荷

**LLM 是类人的：**
- 在包含这些模式的人类文本上训练
- 权威语言在训练数据中先于合规
- 承诺序列（陈述 → 行动）经常被建模
- 社会认同模式（每个人都做 X）建立规范

## 合乎道德的使用

**合法：**
- 确保关键实践被遵循
- 创建有效的文档
- 防止可预测的失败

**非法：**
- 为个人利益操纵
- 制造虚假的紧迫感
- 基于内疚的合规

**测试：** 如果用户完全理解，这种技术是否服务于他们的真实利益？

## 研究引用

**Cialdini, R. B. (2021).** *Influence: The Psychology of Persuasion (New and Expanded).* Harper Business.
- 七大说服原则
- 影响力研究的实证基础

**Meincke, L., Shapiro, D., Duckworth, A. L., Mollick, E., Mollick, L., & Cialdini, R. (2025).** Call Me A Jerk: Persuading AI to Comply with Objectionable Requests. University of Pennsylvania.
- 用 N=28,000 个 LLM 对话测试 7 条原则
- 合规率从 33% 增加到 72%
- 权威、承诺、稀缺最有效
- 验证 LLM 行为的类人模型

## 快速参考

设计技能时，问：

1. **它是什么类型？**（纪律 vs 指导 vs 参考）
2. **我想要改变什么行为？**
3. **哪些原则适用？**（纪律通常使用权威 + 承诺）
4. **我是否组合了太多？**（不要用全部七条）
5. **这合乎道德吗？**（服务于用户的真实利益？）
