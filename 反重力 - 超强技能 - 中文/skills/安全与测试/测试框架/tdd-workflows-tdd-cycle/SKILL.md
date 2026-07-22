---
name: tdd-workflows-tdd-cycle
description: "用于 TDD 工作流中的红-绿-重构循环开发场景"
risk: unknown
source: community
date_added: "2026-02-27"
---

## 适用场景

- 处理 TDD 工作流中的红-绿-重构循环任务或流程
- 需要 TDD 循环相关的指导、最佳实践或检查清单

## 不适用场景

- 任务与 TDD 循环无关
- 需要本范围之外的其他领域或工具

## 指引

- 明确目标、约束和所需输入。
- 运用相关最佳实践并验证产出。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

执行完整的测试驱动开发（TDD）工作流，严格遵循红-绿-重构纪律：

[深度思考：本工作流通过协调的智能体编排来强制执行测试先行开发。TDD 循环的每个阶段都严格实施先失败验证、增量实现和持续重构。工作流支持单测试和测试套件两种模式，并提供可配置的覆盖率阈值。]

## 配置

### 覆盖率阈值
- 最低行覆盖率：80%
- 最低分支覆盖率：75%
- 关键路径覆盖率：100%

### 重构触发条件
- 圈复杂度 > 10
- 方法长度 > 20 行
- 类长度 > 200 行
- 重复代码块 > 3 行

## 阶段一：测试规格与设计

### 1. 需求分析
- 使用 Task 工具，subagent_type="comprehensive-review::architect-review"
- 提示词："Analyze requirements for: $ARGUMENTS. Define acceptance criteria, identify edge cases, and create test scenarios. Output a comprehensive test specification."
- 输出：测试规格、验收标准、边界用例矩阵
- 验证：确保所有需求都有对应的测试场景

### 2. 测试架构设计
- 使用 Task 工具，subagent_type="unit-testing::test-automator"
- 提示词："Design test architecture for: $ARGUMENTS based on test specification. Define test structure, fixtures, mocks, and test data strategy. Ensure testability and maintainability."
- 输出：测试架构、fixture 设计、mock 策略
- 验证：架构支持隔离、快速、可靠的测试

## 阶段二：RED - 编写失败测试

### 3. 编写单元测试（预期失败）
- 使用 Task 工具，subagent_type="unit-testing::test-automator"
- 提示词："Write FAILING unit tests for: $ARGUMENTS. Tests must fail initially. Include edge cases, error scenarios, and happy paths. DO NOT implement production code."
- 输出：失败的单元测试、测试文档
- **关键**：验证所有测试都以预期的错误消息失败

### 4. 验证测试失败
- 使用 Task 工具，subagent_type="tdd-workflows::code-reviewer"
- 提示词："Verify that all tests for: $ARGUMENTS are failing correctly. Ensure failures are for the right reasons (missing implementation, not test errors). Confirm no false positives."
- 输出：测试失败验证报告
- **门禁**：所有测试必须正确失败后才能继续

## 阶段三：GREEN - 使测试通过

### 5. 最小化实现
- 使用 Task 工具，subagent_type="backend-development::backend-architect"
- 提示词："Implement MINIMAL code to make tests pass for: $ARGUMENTS. Focus only on making tests green. Do not add extra features or optimizations. Keep it simple."
- 输出：最小可运行实现
- 约束：不写超出测试所需范围的代码

### 6. 验证测试通过
- 使用 Task 工具，subagent_type="unit-testing::test-automator"
- 提示词："Run all tests for: $ARGUMENTS and verify they pass. Check test coverage metrics. Ensure no tests were accidentally broken."
- 输出：测试执行报告、覆盖率指标
- **门禁**：所有测试必须通过后才能继续

## 阶段四：REFACTOR - 提升代码质量

### 7. 代码重构
- 使用 Task 工具，subagent_type="tdd-workflows::code-reviewer"
- 提示词："Refactor implementation for: $ARGUMENTS while keeping tests green. Apply SOLID principles, remove duplication, improve naming, and optimize performance. Run tests after each refactoring."
- 输出：重构后的代码、重构报告
- 约束：测试必须始终保持绿色

### 8. 测试重构
- 使用 Task 工具，subagent_type="unit-testing::test-automator"
- 提示词："Refactor tests for: $ARGUMENTS. Remove test duplication, improve test names, extract common fixtures, and enhance test readability. Ensure tests still provide same coverage."
- 输出：重构后的测试、改进的测试结构
- 验证：覆盖率指标保持不变或有所提升

## 阶段五：集成与系统测试

### 9. 编写集成测试（先行失败）
- 使用 Task 工具，subagent_type="unit-testing::test-automator"
- 提示词："Write FAILING integration tests for: $ARGUMENTS. Test component interactions, API contracts, and data flow. Tests must fail initially."
- 输出：失败的集成测试
- 验证：测试因缺少集成逻辑而失败

### 10. 实现集成
- 使用 Task 工具，subagent_type="backend-development::backend-architect"
- 提示词："Implement integration code for: $ARGUMENTS to make integration tests pass. Focus on component interaction and data flow."
- 输出：集成实现
- 验证：所有集成测试通过

## 阶段六：持续改进循环

### 11. 性能与边界测试
- 使用 Task 工具，subagent_type="unit-testing::test-automator"
- 提示词："Add performance tests and additional edge case tests for: $ARGUMENTS. Include stress tests, boundary tests, and error recovery tests."
- 输出：扩展测试套件
- 指标：测试覆盖率和场景覆盖范围提升

### 12. 最终代码审查
- 使用 Task 工具，subagent_type="comprehensive-review::architect-review"
- 提示词："Perform comprehensive review of: $ARGUMENTS. Verify TDD process was followed, check code quality, test quality, and coverage. Suggest improvements."
- 输出：审查报告、改进建议
- 行动：在保持测试绿色的前提下实施关键建议

## 增量开发模式

逐测试开发流程：
1. 编写一个失败测试
2. 仅让该测试通过
3. 按需重构
4. 对下一个测试重复上述步骤

通过添加 `--incremental` 标志启用此模式，逐个聚焦单个测试。

## 测试套件模式

全面测试套件开发流程：
1. 为功能/模块编写全部测试（预期失败）
2. 实现代码使全部测试通过
3. 重构整个模块
4. 添加集成测试

通过添加 `--suite` 标志启用此模式，批量开发测试。

## 验证检查点

### RED 阶段验证
- [ ] 所有测试在实现之前编写
- [ ] 所有测试都以有意义的错误消息失败
- [ ] 测试失败是因为缺少实现
- [ ] 没有测试意外通过

### GREEN 阶段验证
- [ ] 所有测试通过
- [ ] 没有超出测试需求的额外代码
- [ ] 覆盖率满足最低阈值
- [ ] 没有为使测试通过而修改测试本身

### REFACTOR 阶段验证
- [ ] 重构后所有测试仍然通过
- [ ] 代码复杂度降低
- [ ] 消除了重复代码
- [ ] 性能提升或保持不变
- [ ] 测试可读性改善

## 覆盖率报告

每个阶段结束后生成覆盖率报告：
- 行覆盖率
- 分支覆盖率
- 函数覆盖率
- 语句覆盖率

## 失败恢复

如果 TDD 纪律被打破：
1. **立即停止**
2. 确认违反了哪个阶段
3. 回滚到上一个有效状态
4. 从正确的阶段恢复
5. 记录经验教训

## TDD 指标追踪

跟踪并报告：
- 各阶段耗时（Red/Green/Refactor）
- 测试-实现循环次数
- 覆盖率变化趋势
- 重构频率
- 缺陷逃逸率

## 应避免的反模式

- 先写实现后写测试
- 编写已经通过的测试
- 跳过重构阶段
- 连续开发多个功能而不写测试
- 修改测试使其通过
- 忽略失败的测试
- 实现完成后再补测试

## 成功标准

- 100% 的代码以测试先行方式编写
- 所有测试持续通过
- 覆盖率超过阈值
- 代码复杂度在限制范围内
- 已覆盖代码零缺陷
- 测试文档清晰完整
- 测试执行快速（单元测试 < 5 秒）

## 备注

- 严格遵循 RED-GREEN-REFACTOR 纪律
- 每个阶段必须完成后才能进入下一阶段
- 测试即规格
- 如果测试难以编写，说明设计需要改进
- 重构不是可选项
- 保持测试执行快速
- 测试应相互独立且隔离

TDD 实现对象：$ARGUMENTS

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不可将输出视为对环境特定验证、测试或专家审查的替代。
- 如缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。