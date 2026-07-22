---
name: temporal-python-testing
description: "基于 pytest 的 Temporal 工作流全面测试方案，含渐进式资源加载，覆盖各类测试场景。触发词：Temporal测试、工作流测试、pytest、单元测试、集成测试、回放测试、确定性验证"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Temporal Python 测试策略

基于 pytest 的 Temporal 工作流全面测试方案，含渐进式资源加载，覆盖各类测试场景。

## 不适用场景

- 任务与 Temporal Python 测试策略无关
- 需要本范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可执行的步骤和验证方法
- 如需详细示例，打开 `resources/implementation-playbook.md`

## 适用场景

- **工作流单元测试** - 基于时间跳过的快速测试
- **集成测试** - 使用 mock Activity 的工作流测试
- **回放测试** - 基于生产历史验证确定性
- **本地开发** - 搭建 Temporal 服务器和 pytest
- **CI/CD 集成** - 自动化测试流水线
- **覆盖率策略** - 达到 ≥80% 测试覆盖率

## 测试理念

**推荐方案**（来源：docs.temporal.io/develop/python/testing-suite）：

- 以集成测试为主编写测试
- 使用 pytest 配合 async fixtures
- 时间跳过机制实现快速反馈（数月级工作流 → 秒级完成）
- Mock Activity 以隔离工作流逻辑
- 通过回放测试验证确定性

**三种测试类型**：

1. **单元测试**：工作流使用时间跳过，Activity 使用 ActivityEnvironment
2. **集成测试**：Worker 配合 mock Activity
3. **端到端测试**：完整 Temporal 服务器配合真实 Activity（慎用）

## 可用资源

本技能通过渐进式加载提供详细指南。根据测试需求加载对应资源：

### 单元测试资源

**文件**：`resources/unit-testing.md`
**加载时机**：单独测试某个工作流或 Activity
**内容**：

- WorkflowEnvironment 时间跳过
- ActivityEnvironment 测试 Activity
- 长时间运行工作流的快速执行
- 手动时间推进模式
- pytest fixtures 和测试模式

### 集成测试资源

**文件**：`resources/integration-testing.md`
**加载时机**：使用 mock 外部依赖测试工作流
**内容**：

- Activity mock 策略
- 错误注入模式
- 多 Activity 工作流测试
- Signal 和 Query 测试
- 覆盖率策略

### 回放测试资源

**文件**：`resources/replay-testing.md`
**加载时机**：验证确定性或部署工作流变更
**内容**：

- 确定性验证
- 生产历史回放
- CI/CD 集成模式
- 版本兼容性测试

### 本地开发资源

**文件**：`resources/local-setup.md`
**加载时机**：搭建开发环境
**内容**：

- Docker Compose 配置
- pytest 配置和设置
- 覆盖率工具集成
- 开发工作流

## 快速入门

### 基本工作流测试

```python
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

@pytest.fixture
async def workflow_env():
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.mark.asyncio
async def test_workflow(workflow_env):
    async with Worker(
        workflow_env.client,
        task_queue="test-queue",
        workflows=[YourWorkflow],
        activities=[your_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            YourWorkflow.run,
            args,
            id="test-wf-id",
            task_queue="test-queue",
        )
        assert result == expected
```

### 基本 Activity 测试

```python
from temporalio.testing import ActivityEnvironment

async def test_activity():
    env = ActivityEnvironment()
    result = await env.run(your_activity, "test-input")
    assert result == expected_output
```

## 覆盖率目标

**推荐覆盖率**（来源：docs.temporal.io 最佳实践）：

- **工作流**：≥80% 逻辑覆盖率
- **Activity**：≥80% 逻辑覆盖率
- **集成测试**：关键路径配合 mock Activity
- **回放测试**：部署前覆盖所有工作流版本

## 核心测试原则

1. **时间跳过** - 数月级工作流秒级完成测试
2. **Mock Activity** - 将工作流逻辑与外部依赖隔离
3. **回放测试** - 部署前验证确定性
4. **高覆盖率** - 生产工作流目标 ≥80%
5. **快速反馈** - 单元测试毫秒级完成

## 资源使用方式

**按需加载对应资源**：

- "展示单元测试模式" → 加载 `resources/unit-testing.md`
- "如何 mock Activity？" → 加载 `resources/integration-testing.md`
- "搭建本地 Temporal 服务器" → 加载 `resources/local-setup.md`
- "验证确定性" → 加载 `resources/replay-testing.md`

## 参考资料

- Python SDK Testing: docs.temporal.io/develop/python/testing-suite
- Testing Patterns: github.com/temporalio/temporal/blob/main/docs/development/testing.md
- Python Samples: github.com/temporalio/samples-python

## 限制

- 仅在任务明确匹配上述范围时使用本技能
- 不要将输出结果作为环境特定验证、测试或专家评审的替代
- 缺少必要输入、权限、安全边界或成功标准时，应停下来请求澄清
