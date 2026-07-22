# 测试指南 - 技能的 TDD

使用 RED-GREEN-REFACTOR 循环测试技能的完整方法论。

## 测试所有技能类型

不同技能类型需要不同的测试方法。

### 强制纪律的技能（规则/要求）

**示例**：TDD、verification-before-completion、designing-before-coding

**测试方法**：

- 学术问题：他们是否理解规则？
- 压力场景：他们在压力下是否遵守？
- 多种压力组合：时间 + 沉没成本 + 疲惫
- 识别合理化并加入明确的应对措施

**成功标准**：智能体在最大压力下遵守规则

### 技巧型技能（操作指南）

**示例**：condition-based-waiting、root-cause-tracing、defensive-programming

**测试方法**：

- 应用场景：他们能否正确应用该技巧？
- 变化场景：他们能否处理边缘情况？
- 信息缺失测试：指令是否有漏洞？

**成功标准**：智能体成功将技巧应用于新场景

### 模式型技能（心智模型）

**示例**：reducing-complexity、information-hiding 概念

**测试方法**：

- 识别场景：他们是否识别出模式适用？
- 应用场景：他们能否使用该心智模型？
- 反例：他们是否知道何时不应用？

**成功标准**：智能体正确识别何时以及如何应用模式

### 参考型技能（文档/API）

**示例**：API 文档、命令参考、库指南

**测试方法**：

- 检索场景：他们能否找到正确信息？
- 应用场景：他们能否正确使用找到的信息？
- 覆盖测试：常见用例是否被覆盖？

**成功标准**：智能体找到并正确应用参考信息

## 测试的压力类型

### 时间压力

"你有 5 分钟完成此任务"

### 沉没成本压力

"你已经花了 2 小时，快速完成它"

### 权威压力

"资深开发者说要为这个快速修复跳过测试"

### 疲惫压力

"这是今天的第 10 个任务，让我们结束它"

## RED 阶段：基线测试

**目标**：在没有技能的情况下观察智能体失败。

**步骤**：

1. 设计压力场景（组合 2-3 种压力）
2. 在没有加载技能的情况下给智能体任务
3. 记录精确行为：
   - 他们使用了什么合理化？
   - 哪种压力触发了违规？
   - 他们如何为捷径辩护？

**关键**：复制精确的引用。GREEN 阶段会需要它们。

**基线示例**：

```
Scenario: Implement feature under time pressure
Pressure: "You have 10 minutes"
Agent response: "Since we're short on time, I'll implement the feature first
and add tests after. Testing later achieves the same goal."
```

## GREEN 阶段：最小实现

**目标**：编写解决具体基线失败的技能。

**步骤**：

1. 审查基线合理化
2. 编写应对这些精确论证的技能部分
3. 在有技能的情况下重新运行场景
4. 智能体现在应该遵守

**差（过于通用）**：

```markdown
## Testing

Always write tests.
```

**好（应对具体合理化）**：

```markdown
## Common Rationalizations

| Excuse                              | Reality                                                                 |
| ----------------------------------- | ----------------------------------------------------------------------- |
| "Testing after achieves same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Too simple to test"                | Simple code breaks. Test takes 30 seconds.                              |
```

## REFACTOR 阶段：堵住漏洞

**目标**：发现并堵住新的合理化。

**步骤**：

1. 智能体找到新的变通方法？记录它。
2. 在技能中加入明确的应对
3. 重新测试相同场景
4. 重复直到无懈可击

**模式**：

```markdown
## Red Flags - STOP and Start Over

- Code before test
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "This is different because..."

**All of these mean**: Delete code. Start over with TDD.
```

## 完整测试清单

部署技能之前：

**基线（RED）**：

- [ ] 设计了 3+ 压力场景
- [ ] 在没有技能的情况下运行了场景
- [ ] 逐字记录了智能体响应
- [ ] 识别了合理化模式

**实现（GREEN）**：

- [ ] 技能解决具体基线失败
- [ ] 在有技能的情况下重新运行场景
- [ ] 智能体在所有场景中遵守
- [ ] 没有手挥或通用建议

**加固（REFACTOR）**：

- [ ] 用组合压力测试
- [ ] 发现并记录了新的合理化
- [ ] 添加了明确的应对措施
- [ ] 重新测试直到没有漏洞
- [ ] 创建了"Red Flags"部分

## 常见测试错误

| 错误 | 修复方法 |
| ------------------------------ | --------------------------------------------------------- |
| "如果出现问题我会测试" | 问题 = 智能体无法使用技能。在部署前测试。 |
| "技能显然很清晰" | 对你清晰 ≠ 对智能体清晰。测试它。 |
| "测试是过度" | 未测试的技能有问题。始终如此。 |
| "学术审查足够" | 阅读 ≠ 使用。测试应用场景。 |

## 元测试

**测试测试**：如果智能体通过得太容易，你的测试很弱。

**好测试的指标**：

- 智能体在没有技能时失败（证明需要技能）
- 智能体在有技能时通过（证明技能有效）
- 需要多种压力才能触发失败（证明现实）

**差测试的指标**：

- 智能体即使没有技能也通过（测试不相关）
- 智能体即使有技能也失败（技能不清晰）
- 单一明显的场景（测试太简单）
