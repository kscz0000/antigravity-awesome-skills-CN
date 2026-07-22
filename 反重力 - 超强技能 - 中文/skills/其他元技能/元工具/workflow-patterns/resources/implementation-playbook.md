# 工作流模式实施手册

本文件包含该技能引用的详细模式、检查清单和代码示例。

# 工作流模式

使用 Conductor 的 TDD 工作流、管理阶段检查点、处理 git 提交，并执行在整个实施过程中确保质量的验证协议的指南。

## 何时使用此技能

- 从轨道的 plan.md 实施任务
- 遵循 TDD 红-绿-重构循环
- 完成阶段检查点
- 管理 git 提交和注释
- 理解质量保证门槛
- 处理验证协议
- 在计划文件中记录进度

## TDD 任务生命周期

对每个任务遵循以下 11 个步骤：

### 步骤 1：选择下一个任务

阅读 plan.md 并确定下一个待处理的 `[ ]` 任务。在当前阶段内按顺序选择任务。不要跳过到后续阶段。

### 步骤 2：标记为进行中

更新 plan.md 以将任务标记为 `[~]`：

```markdown
- [~] **任务 2.1**：实现用户验证
```

将此状态变更的提交与实施分开。

### 步骤 3：RED - 编写失败的测试

在编写实施代码之前，先编写定义预期行为的测试：

- 必要时创建测试文件
- 编写涵盖正常路径的测试用例
- 编写涵盖边缘情况的测试用例
- 编写涵盖错误条件的测试用例
- 运行测试 — 它们应该失败

示例：

```python
def test_validate_user_email_valid():
    user = User(email="test@example.com")
    assert user.validate_email() is True

def test_validate_user_email_invalid():
    user = User(email="invalid")
    assert user.validate_email() is False
```

### 步骤 4：GREEN - 实现最小代码

编写使测试通过所需的最少代码：

- 专注于让测试通过，而不是追求完美
- 避免过早优化
- 保持实施简单
- 运行测试 — 它们应该通过

### 步骤 5：REFACTOR - 提高清晰度

在测试通过的基础上改进代码：

- 提取通用模式
- 改进命名
- 消除重复
- 简化逻辑
- 每次更改后运行测试 — 它们应保持通过

### 步骤 6：验证覆盖率

检查测试覆盖率达到 80% 的目标：

```bash
pytest --cov=module --cov-report=term-missing
```

如果覆盖率低于 80%：

- 识别未覆盖的代码行
- 为缺失路径添加测试
- 重新运行覆盖率检查

### 步骤 7：记录偏差

如果实施偏离了计划或引入了新的依赖项：

- 使用新的依赖项更新 tech-stack.md
- 在 plan.md 任务注释中注明偏差
- 如果需求发生变化，更新 spec.md

### 步骤 8：提交实施

为该任务创建一个聚焦的提交：

```bash
git add -A
git commit -m "feat(user): implement email validation

- Add validate_email method to User class
- Handle empty and malformed emails
- Add comprehensive test coverage

Task: 2.1
Track: user-auth_20250115"
```

提交消息格式：

- 类型：feat、fix、refactor、test、docs、chore
- 范围：受影响的模块或组件
- 摘要：祈使句、现在时
- 正文：变更的项目符号列表
- 页脚：任务和轨道引用

### 步骤 9：附加 Git 注释

将丰富的任务摘要作为 git 注释添加：

```bash
git notes add -m "Task 2.1: Implement user validation

Summary:
- Added email validation using regex pattern
- Handles edge cases: empty, no @, no domain
- Coverage: 94% on validation module

Files changed:
- src/models/user.py (modified)
- tests/test_user.py (modified)

Decisions:
- Used simple regex over email-validator library
- Reason: No external dependency for basic validation"
```

### 步骤 10：使用 SHA 更新计划

更新 plan.md 以使用提交 SHA 标记任务完成：

```markdown
- [x] **任务 2.1**：实现用户验证 `abc1234`
```

### 步骤 11：提交计划更新

提交计划状态更新：

```bash
git add conductor/tracks/*/plan.md
git commit -m "docs: update plan - task 2.1 complete

Track: user-auth_20250115"
```

## 阶段完成协议

当阶段中的所有任务都完成时，执行验证协议：

### 识别已更改的文件

列出自上一个检查点以来修改的所有文件：

```bash
git diff --name-only <last-checkpoint-sha>..HEAD
```

### 确保测试覆盖率

对于每个修改的文件：

1. 识别对应的测试文件
2. 验证新/更改的代码存在测试
3. 运行修改模块的覆盖率
4. 如果覆盖率 < 80% 则添加测试

### 运行完整测试套件

执行完整的测试套件：

```bash
pytest -v --tb=short
```

在继续之前所有测试都必须通过。

### 生成手动验证步骤

创建手动验证的检查清单：

```markdown
## 阶段 1 验证检查清单

- [ ] 用户可以使用有效电子邮件注册
- [ ] 无效的电子邮件显示适当的错误
- [ ] 数据库正确存储用户
- [ ] API 返回预期的响应代码
```

### 等待用户批准

向用户展示验证检查清单：

```
阶段 1 完成。请验证：
1. [ ] 测试套件通过（自动）
2. [ ] 覆盖率达标（自动）
3. [ ] 手动验证项（需要人工）

回复 'approved' 以继续，或注明问题。
```

在未获得明确批准之前不要继续。

### 创建检查点提交

获得批准后，创建检查点提交：

```bash
git add -A
git commit -m "checkpoint: phase 1 complete - user-auth_20250115

Verified:
- All tests passing
- Coverage: 87%
- Manual verification approved

Phase 1 tasks:
- [x] Task 1.1: Setup database schema
- [x] Task 1.2: Implement user model
- [x] Task 1.3: Add validation logic"
```

### 记录检查点 SHA

更新 plan.md 检查点表：

```markdown
## 检查点

| 阶段   | 检查点 SHA | 日期       | 状态     |
| ------ | ---------- | ---------- | -------- |
| 阶段 1 | def5678    | 2025-01-15 | 已验证   |
| 阶段 2 |            |            | 待处理   |
```

## 质量保证门槛

在将任何任务标记为完成之前，请验证这些门槛：

### 测试通过

- 所有现有测试通过
- 新测试通过
- 没有测试回归

### 覆盖率 >= 80%

- 新代码有 80% 以上的覆盖率
- 整体项目覆盖率得以保持
- 关键路径完全覆盖

### 样式合规

- 代码遵循样式指南
- 代码检查通过
- 格式正确

### 文档

- 公共 API 已记录
- 复杂逻辑已解释
- 必要时更新了 README

### 类型安全

- 类型提示存在（如果适用）
- 类型检查器通过
- 没有无理由的 `type: ignore`

### 没有代码检查错误

- 零代码检查错误
- 警告已处理或合理说明
- 静态分析干净

### 移动兼容性

如果适用：

- 响应式设计已验证
- 触摸交互正常工作
- 性能可接受

### 安全审计

- 代码中没有密钥
- 输入验证存在
- 身份验证/授权正确
- 依赖项没有漏洞

## Git 集成

### 提交消息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型：

- `feat`：新功能
- `fix`：错误修复
- `refactor`：代码变更（无功能/修复）
- `test`：添加测试
- `docs`：文档
- `chore`：维护

### 用于丰富摘要的 Git 注释

将详细注释附加到提交：

```bash
git notes add -m "<detailed summary>"
```

查看注释：

```bash
git log --show-notes
```

好处：

- 保留上下文而不使提交消息杂乱
- 启用跨提交的语义查询
- 支持基于轨道的操作

### 在 plan.md 中记录 SHA

完成任务时始终记录提交 SHA：

```markdown
- [x] **任务 1.1**：设置架构 `abc1234`
- [x] **任务 1.2**：添加模型 `def5678`
```

这能够实现：

- 从计划到代码的可追溯性
- 语义回退操作
- 进度审计

## 验证检查点

### 为什么检查点很重要

检查点为语义回退创建还原点：

- 回退到任何阶段的结束
- 维护逻辑代码状态
- 启用安全实验

### 何时创建检查点

在以下情况之后创建检查点：

- 所有阶段任务完成
- 所有阶段验证通过
- 收到用户批准

### 检查点提交内容

在检查点提交中包含：

- 所有未提交的更改
- 已更新的 plan.md
- 已更新的 metadata.json
- 任何文档更新

### 如何使用检查点

用于回退：

```bash
# 回退到阶段 1 结束
git revert --no-commit <phase-2-commits>...
git commit -m "revert: rollback to phase 1 checkpoint"
```

用于审查：

```bash
# 查看阶段 2 中更改的内容
git diff <phase-1-sha>..<phase-2-sha>
```

## 处理偏差

在实施过程中，可能会发生偏离计划的情况。系统地处理它们：

### 偏差的类型

**范围增加**
在原始规范中未发现的需求。

- 在 spec.md 中记录为新需求
- 向 plan.md 添加任务
- 在任务注释中注明增加

**范围减少**
在实施期间认为不必要的功能。

- 将任务标记为 `[-]`（已跳过）并注明原因
- 更新 spec.md 范围部分
- 记录决策理由

**技术偏差**
与计划不同的实施方法。

- 在任务完成注释中注明偏差
- 如果依赖项已更改则更新 tech-stack.md
- 记录原始方法不适合的原因

**需求变更**
在工作中对需求的理解发生变化。

- 使用更正后的需求更新 spec.md
- 必要时调整 plan.md 任务
- 重新验证验收标准

### 偏差文档格式

当使用偏差完成任务时：

```markdown
- [x] **任务 2.1**：实现验证 `abc1234`
  - 偏差：使用库而不是自定义代码
  - 原因：更好的边缘情况处理
  - 影响：将 email-validator 添加到依赖项
```

## 错误恢复

### GREEN 之后测试失败

如果在达到 GREEN 后测试失败：

1. 不要继续 REFACTOR
2. 识别哪个测试开始失败
3. 检查重构是否破坏了某些内容
4. 回退到最后一个已知的 GREEN 状态
5. 重新尝试实施

### 检查点被拒绝

如果用户拒绝检查点：

1. 在 plan.md 中注明拒绝原因
2. 创建任务以解决问题
3. 完成补救任务
4. 再次请求检查点批准

### 被依赖项阻塞

如果任务无法继续：

1. 将任务标记为 `[!]` 并附上阻塞描述
2. 检查其他任务是否可以继续
3. 记录预期的解决时间表
4. 考虑创建依赖项解决轨道

## 按任务类型的 TDD 变体

### 数据模型任务

```
RED：编写模型创建和验证的测试
GREEN：使用字段实现模型类
REFACTOR：添加计算属性，改进类型
```

### API 端点任务

```
RED：编写请求/响应契约的测试
GREEN：实现端点处理程序
REFACTOR：提取验证，改进错误处理
```

### 集成任务

```
RED：编写组件交互的测试
GREEN：将组件连接在一起
REFACTOR：改进错误传播，添加日志
```

### 重构任务

```
RED：为当前行为添加表征测试
GREEN：应用重构（测试应保持通过）
REFACTOR：清理任何引入的复杂性
```

## 使用现有测试

修改带有现有测试的代码时：

### 扩展，不要替换

- 保持现有测试通过
- 为新行为添加新测试
- 仅在需求变化时更新测试

### 测试迁移

当重构改变测试结构时：

1. 运行现有测试（应该通过）
2. 为重构后的代码添加新测试
3. 将测试用例迁移到新结构
4. 仅在新测试通过后删除旧测试

### 回归预防

任何更改之后：

1. 运行完整测试套件
2. 检查意外失败
3. 调查任何新失败
4. 在继续之前修复回归

## 检查点验证详细信息

### 自动验证

在请求批准之前运行：

```bash
# 测试套件
pytest -v --tb=short

# 覆盖率
pytest --cov=src --cov-report=term-missing

# 代码检查
ruff check src/ tests/

# 类型检查（如果适用）
mypy src/
```

### 手动验证指导

对于手动项，提供具体说明：

```markdown
## 手动验证步骤

### 用户注册

1. 导航到 /register
2. 输入有效电子邮件：test@example.com
3. 输入满足要求的密码
4. 单击提交
5. 验证是否出现成功消息
6. 验证用户是否出现在数据库中

### 错误处理

1. 输入无效的电子邮件："notanemail"
2. 验证是否显示错误消息
3. 验证表单是否保留其他输入的数据
```

## 性能考虑

### 测试套件性能

保持测试套件快速：

- 使用 fixtures 避免冗余设置
- 模拟缓慢的外部调用
- 在开发期间运行子集，在检查点运行完整套件

### 提交性能

保持提交原子性：

- 每个提交一个逻辑变更
- 完成的想法，而不是正在进行的工作
- 每次提交后测试都应该通过

## 最佳实践

1. **永远不要跳过 RED**：始终先编写失败的测试
2. **小型提交**：每个提交一个逻辑变更
3. **立即更新**：任务完成后立即更新 plan.md
4. **等待批准**：永远不要跳过检查点验证
5. **丰富的 git 注释**：包含有助于未来理解的上下文
6. **覆盖率纪律**：不接受低于目标的覆盖率
7. **质量门槛**：在标记完成之前检查所有门槛
8. **顺序阶段**：按顺序完成阶段
9. **记录偏差**：注意任何与原始计划的变化
10. **干净状态**：每次提交都应使代码处于工作状态
11. **快速反馈**：在开发期间频繁运行相关测试
12. **明确的阻塞**：及时解决阻塞，不要绕道
