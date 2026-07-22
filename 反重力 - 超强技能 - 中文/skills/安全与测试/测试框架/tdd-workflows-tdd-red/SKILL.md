---
name: tdd-workflows-tdd-red
description: "为 TDD 红阶段生成失败测试，定义预期行为和边界情况。触发词：TDD红阶段、失败测试、红绿重构、测试先行、red phase"
risk: unknown
source: community
date_added: "2026-02-27"
---

按照 TDD 红阶段原则编写全面的失败测试。

[深度思考：通过 test-automator 子代理生成能正确定义预期行为的失败测试。]

## 适用场景

- 为新行为启动 TDD 红阶段
- 需要捕获预期行为的失败测试
- 实现前需要边界情况覆盖

## 不适用场景

- 处于绿阶段或重构阶段
- 只需要性能基准测试
- 测试必须在生产环境运行

## 操作步骤

1. 识别行为、约束和边界情况
2. 生成定义预期结果的失败测试
3. 确保失败原因是缺少行为实现，而非配置错误
4. 记录如何运行测试并验证失败

## 安全事项

- 测试数据保持隔离，避免使用生产环境
- 红阶段避免引入不稳定的外部依赖

## 角色

使用 Task 工具，指定 subagent_type="unit-testing::test-automator" 生成失败测试。

## 提示词模板

"为以下内容生成全面的失败测试：$ARGUMENTS

## 核心要求

1. **测试结构**
   - 框架适配的初始化（Jest/pytest/JUnit/Go/RSpec）
   - Arrange-Act-Assert 模式
   - should_X_when_Y 命名规范
   - 隔离的 fixture，无相互依赖

2. **行为覆盖**
   - 正常路径场景
   - 边界情况（空值、null、边界值）
   - 错误处理和异常
   - 并发访问（如适用）

3. **失败验证**
   - 测试运行时必须失败
   - 失败原因正确（非语法/导入错误）
   - 有意义的诊断错误信息
   - 无级联失败

4. **测试分类**
   - 单元测试：隔离的组件行为
   - 集成测试：组件交互
   - 契约测试：API/接口契约
   - 属性测试：数学不变量

## 框架模式

**JavaScript/TypeScript (Jest/Vitest)**
- 使用 `vi.fn()` 或 `jest.fn()` 模拟依赖
- React 组件使用 `@testing-library`
- 属性测试使用 `fast-check`

**Python (pytest)**
- 使用合适作用域的 fixture
- 使用 parametrize 处理多组测试用例
- 属性测试使用 Hypothesis

**Go**
- 表驱动测试配合子测试
- `t.Parallel()` 并行执行
- 使用 `testify/assert` 简化断言

**Ruby (RSpec)**
- `let` 懒加载，`let!` 立即加载
- 使用 context 区分不同场景
- 共享示例处理公共行为

## 质量检查清单

- 测试名称可读，体现意图
- 每个测试只验证一个行为
- 不泄露实现细节
- 使用有意义的测试数据（非 'foo'/'bar'）
- 测试即活文档

## 需避免的反模式

- 测试首次运行就通过
- 测试实现而非行为
- 复杂的初始化代码
- 单个测试承担多重职责
- 与具体实现绑定的脆弱测试

## 边界情况分类

- **空值/空集**：undefined、null、空字符串/数组/对象
- **边界值**：最小/最大值、单元素、容量上限
- **特殊字符**：Unicode、空白字符、特殊符号
- **状态**：非法状态转换、并发修改
- **错误**：网络故障、超时、权限不足

## 输出要求

- 包含导入语句的完整测试文件
- 测试目的说明
- 运行和验证失败的命令
- 指标：测试数量、覆盖范围
- 进入绿阶段的后续步骤"

## 验证

生成后：
1. 运行测试 — 确认失败
2. 检查失败信息是否有帮助
3. 确认测试之间相互独立
4. 确保覆盖全面

## 示例（最小化）

```typescript
// auth.service.test.ts
describe('AuthService', () => {
  let authService: AuthService;
  let mockUserRepo: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockUserRepo = { findByEmail: jest.fn() } as any;
    authService = new AuthService(mockUserRepo);
  });

  it('should_return_token_when_valid_credentials', async () => {
    const user = { id: '1', email: 'test@example.com', passwordHash: 'hashed' };
    mockUserRepo.findByEmail.mockResolvedValue(user);

    const result = await authService.authenticate('test@example.com', 'pass');

    expect(result.success).toBe(true);
    expect(result.token).toBeDefined();
  });

  it('should_fail_when_user_not_found', async () => {
    mockUserRepo.findByEmail.mockResolvedValue(null);

    const result = await authService.authenticate('none@example.com', 'pass');

    expect(result.success).toBe(false);
    expect(result.error).toBe('INVALID_CREDENTIALS');
  });
});
```

测试需求：$ARGUMENTS

## 限制

- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家评审
- 缺少必要输入、权限、安全边界或成功标准时，应停下来请求澄清
