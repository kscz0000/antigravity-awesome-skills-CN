---
name: pytest-skill
description: '生成生产级 Python pytest 测试，涵盖 fixtures、参数化、标记、mock 和 conftest 模式。当用户提到"pytest"、"conftest"、"@pytest.fixture"、"@pytest.mark"、"Python 测试"时使用。触发词：pytest、conftest、Python 测试、parametrize、Python...'
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/pytest-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# Pytest 测试技能
## 何时使用

当需要生成生产级 Python pytest 测试时使用此技能，涵盖 fixtures、参数化、标记、mock 和 conftest 模式。当用户提到 "pytest"、"conftest"、"@pytest.fixture"、"@pytest.mark"、"Python 测试"时使用。触发词：pytest、conftest、Python 测试、parametrize、Python...


## 核心模式

### 基础测试

```python
import pytest

def test_addition():
    assert 2 + 3 == 5

def test_exception():
    with pytest.raises(ValueError, match="invalid"):
        int("not_a_number")

class TestCalculator:
    def test_add(self):
        calc = Calculator()
        assert calc.add(2, 3) == 5

    def test_divide_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            Calculator().divide(10, 0)
```

### Fixtures

```python
@pytest.fixture
def calculator():
    return Calculator()

@pytest.fixture
def db_connection():
    conn = Database.connect("test_db")
    yield conn  # teardown after yield
    conn.rollback()
    conn.close()

@pytest.fixture(scope="module")
def api_client():
    client = APIClient(base_url="http://localhost:8000")
    yield client
    client.logout()

# conftest.py - shared fixtures
@pytest.fixture(autouse=True)
def reset_state():
    State.reset()
    yield
    State.cleanup()

# Usage
def test_add(calculator):
    assert calculator.add(2, 3) == 5
```

### 参数化

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", 5), ("", 0), ("pytest", 6),
])
def test_string_length(input, expected):
    assert len(input) == expected

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5), (-1, 1, 0), (0, 0, 0),
])
def test_add(calculator, a, b, expected):
    assert calculator.add(a, b) == expected
```

### 标记

```python
@pytest.mark.slow
def test_large_dataset(): ...

@pytest.mark.skip(reason="Not implemented")
def test_future_feature(): ...

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_permissions(): ...

@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug(): ...
```

### Mock

```python
from unittest.mock import patch, MagicMock

def test_send_email(mocker):
    mock_smtp = mocker.patch("myapp.email.smtplib.SMTP")
    send_welcome_email("user@test.com")
    mock_smtp.return_value.sendmail.assert_called_once()

def test_api_call(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"users": [{"name": "Alice"}]}
    mocker.patch("myapp.service.requests.get", return_value=mock_response)
    users = get_users()
    assert len(users) == 1

@patch("myapp.service.database")
def test_save_user(mock_db):
    mock_db.save.return_value = True
    assert save_user({"name": "Alice"}) is True
    mock_db.save.assert_called_once()
```

### 断言

```python
assert x == y
assert x != y
assert x in collection
assert isinstance(obj, MyClass)
assert 0.1 + 0.2 == pytest.approx(0.3)

with pytest.raises(ValueError) as exc_info:
    raise ValueError("bad")
assert "bad" in str(exc_info.value)
```

### 反模式

| 反面示例 | 正面示例 | 原因 |
|-----|------|-----|
| `self.assertEqual()` | `assert x == y` | pytest 重写提供更好的输出 |
| 在 `__init__` 中初始化 | `@pytest.fixture` | 生命周期管理 |
| 全局状态 | 带 `yield` 的 fixture | 正确清理 |
| 臃肿的测试函数 | 小而聚焦的测试 | 更易调试 |

## 快速参考

| 任务 | 命令 |
|------|---------|
| 运行全部 | `pytest` |
| 运行文件 | `pytest tests/test_login.py` |
| 运行指定用例 | `pytest tests/test_login.py::test_login_success` |
| 按标记 | `pytest -m slow` |
| 按关键字 | `pytest -k "login and not invalid"` |
| 详细输出 | `pytest -v` |
| 首次失败即停 | `pytest -x` |
| 上次失败 | `pytest --lf` |
| 覆盖率 | `pytest --cov=myapp --cov-report=html` |
| 并行执行 | `pytest -n auto` (pytest-xdist) |

## pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = ["slow: slow tests", "integration: integration tests"]
addopts = "-v --tb=short"
```

## 深度模式

生产级模式请参考 `reference/playbook.md`：

| 章节 | 内容 |
|---------|--------------|
| §1 配置 | pytest.ini + pyproject.toml 含标记、覆盖率 |
| §2 Fixtures | 作用域、工厂、teardown、autouse、tmp_path |
| §3 参数化 | 基础、带 ID、笛卡尔积、indirect |
| §4 Mock | pytest-mock、monkeypatch、spy、环境变量 |
| §5 异步 | pytest-asyncio、异步 fixture、异步客户端 |
| §6 异常 | pytest.raises(match=)、警告 |
| §7 标记与插件 | 自定义标记、收集钩子 |
| §8 基于类的测试 | 嵌套类、autouse setup |
| §9 CI/CD | GitHub Actions 矩阵、覆盖率门控 |
| §10 调试表 | 10 个常见问题及修复方案 |
| §11 最佳实践 | 15 条生产检查清单 |

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用更改前，请验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定的测试、安全审查，或用户对破坏性/高成本操作的审批。
