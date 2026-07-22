# Python 测试模式实现手册

本文件包含本技能引用的详细模式、检查清单和代码示例。

# Python 测试模式

使用 pytest、fixtures、mocking、参数化和测试驱动开发实践在 Python 中实现健壮测试策略的全面指南。

## 何时使用本技能

- 为 Python 代码编写单元测试
- 设置测试套件和测试基础设施
- 实施测试驱动开发（TDD）
- 为 API 和服务创建集成测试
- 模拟外部依赖和服务
- 测试异步代码和并发操作
- 在 CI/CD 中设置持续测试
- 实施基于属性的测试
- 测试数据库操作
- 调试失败的测试

## 核心概念

### 1. 测试类型
- **单元测试**：独立测试各个函数/类
- **集成测试**：测试组件之间的交互
- **功能测试**：端到端测试完整功能
- **性能测试**：测量速度和资源使用

### 2. 测试结构（AAA 模式）
- **Arrange**：设置测试数据和前置条件
- **Act**：执行被测代码
- **Assert**：验证结果

### 3. 测试覆盖率
- 衡量测试覆盖了哪些代码
- 识别未测试的代码路径
- 追求有意义的覆盖率，而不仅仅是高百分比

### 4. 测试隔离
- 测试应该是独立的
- 测试之间没有共享状态
- 每个测试都应自行清理

## 快速上手

```python
# test_example.py
def add(a, b):
    return a + b

def test_add():
    """基本测试示例。"""
    result = add(2, 3)
    assert result == 5

def test_add_negative():
    """使用负数测试。"""
    assert add(-1, 1) == 0

# 运行：pytest test_example.py
```

## 基本模式

### 模式 1：基本 pytest 测试

```python
# test_calculator.py
import pytest

class Calculator:
    """用于测试的简单计算器。"""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


def test_addition():
    """测试加法。"""
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0
    assert calc.add(0, 0) == 0


def test_subtraction():
    """测试减法。"""
    calc = Calculator()
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(0, 5) == -5


def test_multiplication():
    """测试乘法。"""
    calc = Calculator()
    assert calc.multiply(3, 4) == 12
    assert calc.multiply(0, 5) == 0


def test_division():
    """测试除法。"""
    calc = Calculator()
    assert calc.divide(6, 3) == 2
    assert calc.divide(5, 2) == 2.5


def test_division_by_zero():
    """测试除以零引发错误。"""
    calc = Calculator()
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(5, 0)
```

### 模式 2：用于设置和拆卸的 Fixtures

```python
# test_database.py
import pytest
from typing import Generator

class Database:
    """简单的数据库类。"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False

    def connect(self):
        """连接到数据库。"""
        self.connected = True

    def disconnect(self):
        """断开数据库连接。"""
        self.connected = False

    def query(self, sql: str) -> list:
        """执行查询。"""
        if not self.connected:
            raise RuntimeError("Not connected")
        return [{"id": 1, "name": "Test"}]


@pytest.fixture
def db() -> Generator[Database, None, None]:
    """提供已连接数据库的 fixture。"""
    # 设置
    database = Database("sqlite:///:memory:")
    database.connect()

    # 提供给测试
    yield database

    # 拆卸
    database.disconnect()


def test_database_query(db):
    """使用 fixture 测试数据库查询。"""
    results = db.query("SELECT * FROM users")
    assert len(results) == 1
    assert results[0]["name"] == "Test"


@pytest.fixture(scope="session")
def app_config():
    """会话级 fixture - 每个测试会话创建一次。"""
    return {
        "database_url": "postgresql://localhost/test",
        "api_key": "test-key",
        "debug": True
    }


@pytest.fixture(scope="module")
def api_client(app_config):
    """模块级 fixture - 每个测试模块创建一次。"""
    # 设置昂贵资源
    client = {"config": app_config, "session": "active"}
    yield client
    # 清理
    client["session"] = "closed"


def test_api_client(api_client):
    """使用 api client fixture 的测试。"""
    assert api_client["session"] == "active"
    assert api_client["config"]["debug"] is True
```

### 模式 3：参数化测试

```python
# test_validation.py
import pytest

def is_valid_email(email: str) -> bool:
    """检查 email 是否有效。"""
    return "@" in email and "." in email.split("@")[1]


@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("test.user@domain.co.uk", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("user@domain", False),
    ("", False),
])
def test_email_validation(email, expected):
    """使用各种输入测试 email 验证。"""
    assert is_valid_email(email) == expected


@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
    (-5, -5, -10),
])
def test_addition_parameterized(a, b, expected):
    """使用多组参数测试加法。"""
    from test_calculator import Calculator
    calc = Calculator()
    assert calc.add(a, b) == expected


# 使用 pytest.param 处理特殊情况
@pytest.mark.parametrize("value,expected", [
    pytest.param(1, True, id="positive"),
    pytest.param(0, False, id="zero"),
    pytest.param(-1, False, id="negative"),
])
def test_is_positive(value, expected):
    """使用自定义测试 ID 进行测试。"""
    assert (value > 0) == expected
```

### 模式 4：使用 unittest.mock 进行 Mocking

```python
# test_api_client.py
import pytest
from unittest.mock import Mock, patch, MagicMock
import requests

class APIClient:
    """简单的 API 客户端。"""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_user(self, user_id: int) -> dict:
        """从 API 获取用户。"""
        response = requests.get(f"{self.base_url}/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def create_user(self, data: dict) -> dict:
        """创建新用户。"""
        response = requests.post(f"{self.base_url}/users", json=data)
        response.raise_for_status()
        return response.json()


def test_get_user_success():
    """使用 mock 测试成功的 API 调用。"""
    client = APIClient("https://api.example.com")

    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "name": "John Doe"}
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response) as mock_get:
        user = client.get_user(1)

        assert user["id"] == 1
        assert user["name"] == "John Doe"
        mock_get.assert_called_once_with("https://api.example.com/users/1")


def test_get_user_not_found():
    """使用 404 错误测试 API 调用。"""
    client = APIClient("https://api.example.com")

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")

    with patch("requests.get", return_value=mock_response):
        with pytest.raises(requests.HTTPError):
            client.get_user(999)


@patch("requests.post")
def test_create_user(mock_post):
    """使用装饰器语法测试用户创建。"""
    client = APIClient("https://api.example.com")

    mock_post.return_value.json.return_value = {"id": 2, "name": "Jane Doe"}
    mock_post.return_value.raise_for_status.return_value = None

    user_data = {"name": "Jane Doe", "email": "jane@example.com"}
    result = client.create_user(user_data)

    assert result["id"] == 2
    mock_post.assert_called_once()
    call_args = mock_post.call_args
    assert call_args.kwargs["json"] == user_data
```

### 模式 5：测试异常

```python
# test_exceptions.py
import pytest

def divide(a: float, b: float) -> float:
    """a 除以 b。"""
    if b == 0:
        raise ZeroDivisionError("Division by zero")
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Arguments must be numbers")
    return a / b


def test_zero_division():
    """测试除以零引发异常。"""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


def test_zero_division_with_message():
    """测试异常消息。"""
    with pytest.raises(ZeroDivisionError, match="Division by zero"):
        divide(5, 0)


def test_type_error():
    """测试类型错误异常。"""
    with pytest.raises(TypeError, match="must be numbers"):
        divide("10", 5)


def test_exception_info():
    """测试访问异常信息。"""
    with pytest.raises(ValueError) as exc_info:
        int("not a number")

    assert "invalid literal" in str(exc_info.value)
```

## 高级模式

### 模式 6：测试异步代码

```python
# test_async.py
import pytest
import asyncio

async def fetch_data(url: str) -> dict:
    """异步获取数据。"""
    await asyncio.sleep(0.1)
    return {"url": url, "data": "result"}


@pytest.mark.asyncio
async def test_fetch_data():
    """测试异步函数。"""
    result = await fetch_data("https://api.example.com")
    assert result["url"] == "https://api.example.com"
    assert "data" in result


@pytest.mark.asyncio
async def test_concurrent_fetches():
    """测试并发异步操作。"""
    urls = ["url1", "url2", "url3"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)

    assert len(results) == 3
    assert all("data" in r for r in results)


@pytest.fixture
async def async_client():
    """异步 fixture。"""
    client = {"connected": True}
    yield client
    client["connected"] = False


@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    """使用异步 fixture 的测试。"""
    assert async_client["connected"] is True
```

### 模式 7：用于测试的 Monkeypatch

```python
# test_environment.py
import os
import pytest

def get_database_url() -> str:
    """从环境获取数据库 URL。"""
    return os.environ.get("DATABASE_URL", "sqlite:///:memory:")


def test_database_url_default():
    """测试默认数据库 URL。"""
    # 如果设置了实际环境变量将使用它
    url = get_database_url()
    assert url


def test_database_url_custom(monkeypatch):
    """使用 monkeypatch 测试自定义数据库 URL。"""
    monkeypatch.setenv("DATABASE_URL", "postgresql://localhost/test")
    assert get_database_url() == "postgresql://localhost/test"


def test_database_url_not_set(monkeypatch):
    """测试未设置环境变量的情况。"""
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert get_database_url() == "sqlite:///:memory:"


class Config:
    """配置类。"""

    def __init__(self):
        self.api_key = "production-key"

    def get_api_key(self):
        return self.api_key


def test_monkeypatch_attribute(monkeypatch):
    """测试 monkeypatch 对象属性。"""
    config = Config()
    monkeypatch.setattr(config, "api_key", "test-key")
    assert config.get_api_key() == "test-key"
```

### 模式 8：临时文件和目录

```python
# test_file_operations.py
import pytest
from pathlib import Path

def save_data(filepath: Path, data: str):
    """将数据保存到文件。"""
    filepath.write_text(data)


def load_data(filepath: Path) -> str:
    """从文件加载数据。"""
    return filepath.read_text()


def test_file_operations(tmp_path):
    """使用临时目录测试文件操作。"""
    # tmp_path 是一个 pathlib.Path 对象
    test_file = tmp_path / "test_data.txt"

    # 保存数据
    save_data(test_file, "Hello, World!")

    # 验证文件存在
    assert test_file.exists()

    # 加载并验证数据
    data = load_data(test_file)
    assert data == "Hello, World!"


def test_multiple_files(tmp_path):
    """使用多个临时文件进行测试。"""
    files = {
        "file1.txt": "Content 1",
        "file2.txt": "Content 2",
        "file3.txt": "Content 3"
    }

    for filename, content in files.items():
        filepath = tmp_path / filename
        save_data(filepath, content)

    # 验证所有文件已创建
    assert len(list(tmp_path.iterdir())) == 3

    # 验证内容
    for filename, expected_content in files.items():
        filepath = tmp_path / filename
        assert load_data(filepath) == expected_content
```

### 模式 9：自定义 Fixtures 和 Conftest

```python
# conftest.py
"""所有测试共享的 fixtures。"""
import pytest

@pytest.fixture(scope="session")
def database_url():
    """为所有测试提供数据库 URL。"""
    return "postgresql://localhost/test_db"


@pytest.fixture(autouse=True)
def reset_database(database_url):
    """在每个测试之前自动运行的 fixture。"""
    # 设置：清空数据库
    print(f"Clearing database: {database_url}")
    yield
    # 拆卸：清理
    print("Test completed")


@pytest.fixture
def sample_user():
    """提供示例用户数据。"""
    return {
        "id": 1,
        "name": "Test User",
        "email": "test@example.com"
    }


@pytest.fixture
def sample_users():
    """提供示例用户列表。"""
    return [
        {"id": 1, "name": "User 1"},
        {"id": 2, "name": "User 2"},
        {"id": 3, "name": "User 3"},
    ]


# 参数化 fixture
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def db_backend(request):
    """使用不同数据库后端运行测试的 fixture。"""
    return request.param


def test_with_db_backend(db_backend):
    """此测试将使用不同后端运行 3 次。"""
    print(f"Testing with {db_backend}")
    assert db_backend in ["sqlite", "postgresql", "mysql"]
```

### 模式 10：基于属性的测试

```python
# test_properties.py
from hypothesis import given, strategies as st
import pytest

def reverse_string(s: str) -> str:
    """反转字符串。"""
    return s[::-1]


@given(st.text())
def test_reverse_twice_is_original(s):
    """属性：反转两次返回原始值。"""
    assert reverse_string(reverse_string(s)) == s


@given(st.text())
def test_reverse_length(s):
    """属性：反转后的字符串长度相同。"""
    assert len(reverse_string(s)) == len(s)


@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    """属性：加法满足交换律。"""
    assert a + b == b + a


@given(st.lists(st.integers()))
def test_sorted_list_properties(lst):
    """属性：排序后的列表是有序的。"""
    sorted_lst = sorted(lst)

    # 长度相同
    assert len(sorted_lst) == len(lst)

    # 所有元素都存在
    assert set(sorted_lst) == set(lst)

    # 是有序的
    for i in range(len(sorted_lst) - 1):
        assert sorted_lst[i] <= sorted_lst[i + 1]
```

## 测试最佳实践

### 测试组织

```python
# tests/
#   __init__.py
#   conftest.py           # 共享的 fixtures
#   test_unit/            # 单元测试
#     test_models.py
#     test_utils.py
#   test_integration/     # 集成测试
#     test_api.py
#     test_database.py
#   test_e2e/            # 端到端测试
#     test_workflows.py
```

### 测试命名

```python
# 良好的测试名称
def test_user_creation_with_valid_data():
    """清晰的名称描述了正在测试的内容。"""
    pass


def test_login_fails_with_invalid_password():
    """名称描述了预期行为。"""
    pass


def test_api_returns_404_for_missing_resource():
    """关于输入和预期结果的具体描述。"""
    pass


# 不良的测试名称
def test_1():  # 不具描述性
    pass


def test_user():  # 过于模糊
    pass


def test_function():  # 没有说明测试什么
    pass
```

### 测试标记

```python
# test_markers.py
import pytest

@pytest.mark.slow
def test_slow_operation():
    """标记慢速测试。"""
    import time
    time.sleep(2)


@pytest.mark.integration
def test_database_integration():
    """标记集成测试。"""
    pass


@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    """临时跳过测试。"""
    pass


@pytest.mark.skipif(os.name == "nt", reason="Unix only test")
def test_unix_specific():
    """条件跳过。"""
    pass


@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    """标记预期失败。"""
    assert False


# 运行：
# pytest -m slow          # 仅运行慢速测试
# pytest -m "not slow"    # 跳过慢速测试
# pytest -m integration   # 运行集成测试
```

### 覆盖率报告

```bash
# 安装 coverage
pip install pytest-cov

# 运行测试并显示覆盖率
pytest --cov=myapp tests/

# 生成 HTML 报告
pytest --cov=myapp --cov-report=html tests/

# 如果覆盖率低于阈值则失败
pytest --cov=myapp --cov-fail-under=80 tests/

# 显示未覆盖的行
pytest --cov=myapp --cov-report=term-missing tests/
```

## 测试数据库代码

```python
# test_database_models.py
import pytest
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()


class User(Base):
    """用户模型。"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)


@pytest.fixture(scope="function")
def db_session() -> Session:
    """为测试创建内存数据库。"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()


def test_create_user(db_session):
    """测试创建用户。"""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert user.name == "Test User"


def test_query_user(db_session):
    """测试查询用户。"""
    user1 = User(name="User 1", email="user1@example.com")
    user2 = User(name="User 2", email="user2@example.com")

    db_session.add_all([user1, user2])
    db_session.commit()

    users = db_session.query(User).all()
    assert len(users) == 2


def test_unique_email_constraint(db_session):
    """测试唯一 email 约束。"""
    from sqlalchemy.exc import IntegrityError

    user1 = User(name="User 1", email="same@example.com")
    user2 = User(name="User 2", email="same@example.com")

    db_session.add(user1)
    db_session.commit()

    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()
```

## CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          pip install pytest pytest-cov

      - name: Run tests
        run: |
          pytest --cov=myapp --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## 配置文件

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=myapp
    --cov-report=term-missing
markers =
    slow: marks tests as slow
    integration: marks integration tests
    unit: marks unit tests
    e2e: marks end-to-end tests
```

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "-v",
    "--cov=myapp",
    "--cov-report=term-missing",
]

[tool.coverage.run]
source = ["myapp"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

## 资源

- **pytest 文档**：https://docs.pytest.org/
- **unittest.mock**：https://docs.python.org/3/library/unittest.mock.html
- **hypothesis**：基于属性的测试
- **pytest-asyncio**：测试异步代码
- **pytest-cov**：覆盖率报告
- **pytest-mock**：mock 的 pytest 包装器

## 最佳实践总结

1. **先写测试**（TDD）或与代码一起编写
2. **每个测试一个断言**（如果可能）
3. **使用描述性的测试名称**以解释行为
4. **保持测试独立**且隔离
5. **使用 fixtures** 进行设置和拆卸
6. **适当地模拟外部依赖**
7. **参数化测试**以减少重复
8. **测试边界情况**和错误条件
9. **衡量覆盖率**但注重质量
10. **在 CI/CD 中运行测试**于每次提交
