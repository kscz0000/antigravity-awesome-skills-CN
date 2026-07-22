---
title: 为 DBOS 使用正确的测试 fixtures
impact: LOW-MEDIUM
impactDescription: 确保测试之间状态干净
tags: testing, pytest, fixtures, reset
---

## 为 DBOS 使用正确的测试 fixtures

使用 pytest fixtures 在每个测试之间正确重置 DBOS 状态。

**错误（测试之间没有重置）：**

```python
def test_workflow_one():
    DBOS.launch()
    result = my_workflow()
    assert result == "expected"

def test_workflow_two():
    # 上一个测试的 DBOS 状态还在！
    result = another_workflow()
```

**正确（使用重置 fixture）：**

```python
import pytest
import os
from dbos import DBOS, DBOSConfig

@pytest.fixture()
def reset_dbos():
    DBOS.destroy()
    config: DBOSConfig = {
        "name": "test-app",
        "database_url": os.environ.get("TESTING_DATABASE_URL"),
    }
    DBOS(config=config)
    DBOS.reset_system_database()
    DBOS.launch()
    yield
    DBOS.destroy()

def test_workflow_one(reset_dbos):
    result = my_workflow()
    assert result == "expected"

def test_workflow_two(reset_dbos):
    # 干净的 DBOS 状态
    result = another_workflow()
    assert result == "other_expected"
```

该 fixture 的执行步骤：
1. 销毁已有的 DBOS 实例
2. 创建新的配置
3. 重置系统数据库
4. 启动 DBOS
5. yield 给测试执行
6. 测试结束后清理

参考：[测试 DBOS](https://docs.dbos.dev/python/tutorials/testing)
