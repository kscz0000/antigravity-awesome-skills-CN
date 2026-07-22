---
name: tdd-workflows-tdd-refactor
description: "用于 TDD 工作流中的安全重构任务。触发词：TDD重构、安全重构、代码重构、重构阶段"
risk: unknown
source: community
date_added: "2026-02-27"
---

## 适用场景

- 处理 TDD 重构阶段的任务或工作流
- 需要 TDD 重构相关的指导、最佳实践或检查清单

## 不适用场景

- 任务与 TDD 重构无关
- 需要超出此范围的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可执行的步骤和验证方法
- 如需详细示例，请打开 `resources/implementation-playbook.md`

借助全面的测试安全网，放心重构代码：

[深度思考：此工具使用 tdd-orchestrator 智能体（opus 模型）执行精细重构，同时保持所有测试通过。它应用设计模式、提升代码质量、优化性能，并以全面的测试覆盖作为安全保障。]

## 用法

使用 Task 工具，设置 subagent_type="tdd-orchestrator" 执行安全重构。

提示词："在保持所有测试通过的前提下重构以下代码：$ARGUMENTS。应用 TDD 重构阶段：

## 核心流程

**1. 预评估**
- 运行测试建立绿色基线
- 分析代码异味和测试覆盖率
- 记录当前性能指标
- 制定增量重构计划

**2. 代码异味检测**
- 重复代码 → 提取方法/类
- 过长方法 → 拆分为职责单一的函数
- 过大类 → 分离职责
- 参数列表过长 → 参数对象
- Feature Envy → 将方法移至合适的类
- Primitive Obsession → 值对象
- Switch 语句 → 多态
- 死代码 → 删除

**3. 设计模式**
- 创建型（Factory、Builder、Singleton）
- 结构型（Adapter、Facade、Decorator）
- 行为型（Strategy、Observer、Command）
- 领域型（Repository、Service、Value Objects）
- 仅在模式能带来明确价值时使用

**4. SOLID 原则**
- 单一职责：只有一个变更理由
- 开闭原则：对扩展开放，对修改封闭
- 里氏替换：子类型可替换
- 接口隔离：小而专注的接口
- 依赖反转：依赖抽象而非具体

**5. 重构手法**
- 提取方法/变量/接口
- 内联不必要的间接层
- 重命名以提升清晰度
- 将方法/字段移至合适的类
- 用常量替换魔法数字
- 封装字段
- 用多态替换条件分支
- 引入 Null Object

**6. 性能优化**
- 性能分析定位瓶颈
- 优化算法和数据结构
- 在有益处的地方实现缓存
- 减少数据库查询（消除 N+1）
- 懒加载和分页
- 优化前后必须测量对比

**7. 增量步骤**
- 做小而原子化的变更
- 每次修改后运行测试
- 每次成功的重构后提交
- 将重构与行为变更分离
- 需要时使用脚手架

**8. 架构演进**
- 分层与依赖管理
- 模块边界与接口定义
- 事件驱动模式实现解耦
- 数据库访问模式优化

**9. 安全验证**
- 每次变更后运行完整测试套件
- 性能回归测试
- 变异测试验证测试有效性
- 重大变更的回滚计划

**10. 高级模式**
- 绞杀者模式：渐进式替换遗留系统
- 抽象分支：大规模变更
- 并行变更：扩展-收缩模式
- Mikado 方法：依赖图导航

## 输出要求

- 应用改进后的重构代码
- 测试结果（全部通过）
- 重构前后指标对比
- 已应用的重构手法清单
- 性能提升测量数据
- 剩余技术债务评估

## 安全检查清单

提交前：
- ✓ 所有测试通过（100% 绿色）
- ✓ 无功能回归
- ✓ 性能指标可接受
- ✓ 代码覆盖率保持或提升
- ✓ 文档已更新

## 恢复协议

如果测试失败：
- 立即回退最近的变更
- 定位导致破坏的重构
- 采用更小的增量变更
- 使用版本控制进行安全实验

## 示例：提取方法模式

**重构前：**
```typescript
class OrderProcessor {
  processOrder(order: Order): ProcessResult {
    // Validation
    if (!order.customerId || order.items.length === 0) {
      return { success: false, error: "Invalid order" };
    }

    // Calculate totals
    let subtotal = 0;
    for (const item of order.items) {
      subtotal += item.price * item.quantity;
    }
    let total = subtotal + (subtotal * 0.08) + (subtotal > 100 ? 0 : 15);

    // Process payment...
    // Update inventory...
    // Send confirmation...
  }
}
```

**重构后：**
```typescript
class OrderProcessor {
  async processOrder(order: Order): Promise<ProcessResult> {
    const validation = this.validateOrder(order);
    if (!validation.isValid) return ProcessResult.failure(validation.error);

    const orderTotal = OrderTotal.calculate(order);
    const inventoryCheck = await this.inventoryService.checkAvailability(order.items);
    if (!inventoryCheck.available) return ProcessResult.failure(inventoryCheck.reason);

    await this.paymentService.processPayment(order.paymentMethod, orderTotal.total);
    await this.inventoryService.reserveItems(order.items);
    await this.notificationService.sendOrderConfirmation(order, orderTotal);

    return ProcessResult.success(order.id, orderTotal.total);
  }

  private validateOrder(order: Order): ValidationResult {
    if (!order.customerId) return ValidationResult.invalid("Customer ID required");
    if (order.items.length === 0) return ValidationResult.invalid("Order must contain items");
    return ValidationResult.valid();
  }
}
```

**应用手法：** Extract Method、Value Objects、Dependency Injection、Async patterns

待重构代码：$ARGUMENTS"

## 使用限制
- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出视为环境特定验证、测试或专家评审的替代品
- 如果缺少必要的输入、权限、安全边界或成功标准，停下来请求澄清