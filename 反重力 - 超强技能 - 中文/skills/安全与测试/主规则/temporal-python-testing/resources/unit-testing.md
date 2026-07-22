# Temporal 工作流与 Activity 单元测试

针对单独测试工作流和 Activity 的专项指南，使用 WorkflowEnvironment 和 ActivityEnvironment。

## WorkflowEnvironment 时间跳过

**目的**：隔离测试工作流，实现即时时间推进（数月级工作流 → 秒级完成）

### 基本配置模式

```python
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

@pytest.fixture
async def workflow_env():
    """Reusable time-skipping test environment"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.mark.asyncio
async def test_workflow_execution(workflow_env):
    """Test workflow with time-skipping"""
    async with Worker(
        workflow_env.client,
        task_queue="test-queue",
        workflows=[YourWorkflow],
        activities=[your_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            YourWorkflow.run,
            "test-input",
            id="test-wf-id",
            task_queue="test-queue",
        )
        assert result == "expected-output"
```

**核心优势**：

- `workflow.sleep(timedelta(days=30))` 瞬间完成
- 快速反馈循环（毫秒级 vs 小时级）
- 确定性测试执行

### 时间跳过示例

**睡眠推进**：

```python
@pytest.mark.asyncio
async def test_workflow_with_delays(workflow_env):
    """Workflow sleeps are instant in time-skipping mode"""

    @workflow.defn
    class DelayedWorkflow:
        @workflow.run
        async def run(self) -> str:
            await workflow.sleep(timedelta(hours=24))  # Instant in tests
            return "completed"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[DelayedWorkflow],
    ):
        result = await workflow_env.client.execute_workflow(
            DelayedWorkflow.run,
            id="delayed-wf",
            task_queue="test",
        )
        assert result == "completed"
```

**手动时间控制**：

```python
@pytest.mark.asyncio
async def test_workflow_manual_time(workflow_env):
    """Manually advance time for precise control"""

    handle = await workflow_env.client.start_workflow(
        TimeBasedWorkflow.run,
        id="time-wf",
        task_queue="test",
    )

    # Advance time by specific amount
    await workflow_env.sleep(timedelta(hours=1))

    # Verify intermediate state via query
    state = await handle.query(TimeBasedWorkflow.get_state)
    assert state == "processing"

    # Advance to completion
    await workflow_env.sleep(timedelta(hours=23))
    result = await handle.result()
    assert result == "completed"
```

### 测试工作流逻辑

**分支测试**：

```python
@pytest.mark.asyncio
async def test_workflow_branching(workflow_env):
    """Test different execution paths"""

    @workflow.defn
    class ConditionalWorkflow:
        @workflow.run
        async def run(self, condition: bool) -> str:
            if condition:
                return "path-a"
            return "path-b"

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[ConditionalWorkflow],
    ):
        # Test true path
        result_a = await workflow_env.client.execute_workflow(
            ConditionalWorkflow.run,
            True,
            id="cond-wf-true",
            task_queue="test",
        )
        assert result_a == "path-a"

        # Test false path
        result_b = await workflow_env.client.execute_workflow(
            ConditionalWorkflow.run,
            False,
            id="cond-wf-false",
            task_queue="test",
        )
        assert result_b == "path-b"
```

## ActivityEnvironment 测试

**目的**：无需工作流或 Temporal 服务器即可隔离测试 Activity

### 基本 Activity 测试

```python
from temporalio.testing import ActivityEnvironment

async def test_activity_basic():
    """Test activity without workflow context"""

    @activity.defn
    async def process_data(input: str) -> str:
        return input.upper()

    env = ActivityEnvironment()
    result = await env.run(process_data, "test")
    assert result == "TEST"
```

### 测试 Activity 上下文

**心跳测试**：

```python
async def test_activity_heartbeat():
    """Verify heartbeat calls"""

    @activity.defn
    async def long_running_activity(total_items: int) -> int:
        for i in range(total_items):
            activity.heartbeat(i)  # Report progress
            await asyncio.sleep(0.1)
        return total_items

    env = ActivityEnvironment()
    result = await env.run(long_running_activity, 10)
    assert result == 10
```

**取消测试**：

```python
async def test_activity_cancellation():
    """Test activity cancellation handling"""

    @activity.defn
    async def cancellable_activity() -> str:
        try:
            while True:
                if activity.is_cancelled():
                    return "cancelled"
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            return "cancelled"

    env = ActivityEnvironment(cancellation_reason="test-cancel")
    result = await env.run(cancellable_activity)
    assert result == "cancelled"
```

### 测试错误处理

**异常传播**：

```python
async def test_activity_error():
    """Test activity error handling"""

    @activity.defn
    async def failing_activity(should_fail: bool) -> str:
        if should_fail:
            raise ApplicationError("Validation failed", non_retryable=True)
        return "success"

    env = ActivityEnvironment()

    # Test success path
    result = await env.run(failing_activity, False)
    assert result == "success"

    # Test error path
    with pytest.raises(ApplicationError) as exc_info:
        await env.run(failing_activity, True)
    assert "Validation failed" in str(exc_info.value)
```

## Pytest 集成模式

### 共享 Fixtures

```python
# conftest.py
import pytest
from temporalio.testing import WorkflowEnvironment

@pytest.fixture(scope="module")
async def workflow_env():
    """Module-scoped environment (reused across tests)"""
    env = await WorkflowEnvironment.start_time_skipping()
    yield env
    await env.shutdown()

@pytest.fixture
def activity_env():
    """Function-scoped environment (fresh per test)"""
    return ActivityEnvironment()
```

### 参数化测试

```python
@pytest.mark.parametrize("input,expected", [
    ("test", "TEST"),
    ("hello", "HELLO"),
    ("123", "123"),
])
async def test_activity_parameterized(activity_env, input, expected):
    """Test multiple input scenarios"""
    result = await activity_env.run(process_data, input)
    assert result == expected
```

## 最佳实践

1. **快速执行**：所有工作流测试使用时间跳过
2. **隔离测试**：分别测试工作流和 Activity
3. **共享 Fixtures**：跨相关测试复用 WorkflowEnvironment
4. **覆盖率目标**：工作流逻辑 ≥80%
5. **Mock Activity**：使用 ActivityEnvironment 测试 Activity 特定逻辑
6. **确定性**：确保测试结果跨运行一致
7. **错误场景**：同时测试成功和失败路径

## 常见模式

**测试重试逻辑**：

```python
@pytest.mark.asyncio
async def test_workflow_with_retries(workflow_env):
    """Test activity retry behavior"""

    call_count = 0

    @activity.defn
    async def flaky_activity() -> str:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise Exception("Transient error")
        return "success"

    @workflow.defn
    class RetryWorkflow:
        @workflow.run
        async def run(self) -> str:
            return await workflow.execute_activity(
                flaky_activity,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(
                    initial_interval=timedelta(milliseconds=1),
                    maximum_attempts=5,
                ),
            )

    async with Worker(
        workflow_env.client,
        task_queue="test",
        workflows=[RetryWorkflow],
        activities=[flaky_activity],
    ):
        result = await workflow_env.client.execute_workflow(
            RetryWorkflow.run,
            id="retry-wf",
            task_queue="test",
        )
        assert result == "success"
        assert call_count == 3  # Verify retry attempts
```

## 参考资料

- Python SDK Testing: docs.temporal.io/develop/python/testing-suite
- pytest Documentation: docs.pytest.org
- Temporal Samples: github.com/temporalio/samples-python
