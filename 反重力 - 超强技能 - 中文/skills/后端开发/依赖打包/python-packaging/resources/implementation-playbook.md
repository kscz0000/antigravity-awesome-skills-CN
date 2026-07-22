# Python Packaging 实现手册

本文件包含技能引用的详细模式、清单和代码示例。

# Python Packaging

使用现代打包工具、pyproject.toml 创建、组织和发布 Python 包的完整指南。

## 适用场景

- 创建用于分发的 Python 库
- 构建带 entry points 的命令行工具
- 发布包到 PyPI 或私有仓库
- 搭建 Python 项目结构
- 创建带依赖的可安装包
- 构建 wheel 和 source distribution
- 管理 Python 包的版本和发布
- 创建 namespace packages
- 实现包元数据和 classifiers

## 核心概念

### 1. 包结构
- **Source layout**：`src/package_name/`（推荐）
- **Flat layout**：`package_name/`（更简单但灵活性较低）
- **包元数据**：pyproject.toml、setup.py 或 setup.cfg
- **分发格式**：wheel (.whl) 和 source distribution (.tar.gz)

### 2. 现代打包标准
- **PEP 517/518**：构建系统要求
- **PEP 621**：pyproject.toml 中的元数据
- **PEP 660**：可编辑安装
- **pyproject.toml**：统一配置源

### 3. 构建后端
- **setuptools**：传统方案，使用广泛
- **hatchling**：现代方案，风格统一
- **flit**：轻量级，适用于纯 Python
- **poetry**：依赖管理 + 打包

### 4. 分发渠道
- **PyPI**：Python Package Index（公开）
- **TestPyPI**：发布前测试
- **私有仓库**：JFrog、AWS CodeArtifact 等

## 快速开始

### 最小包结构

```
my-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── module.py
└── tests/
    └── test_module.py
```

### 最小 pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "A short description"
authors = [{name = "Your Name", email = "you@example.com"}]
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=22.0",
]
```

## 包结构模式

### 模式 1：Source Layout（推荐）

```
my-package/
├── pyproject.toml
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       ├── utils.py
│       └── py.typed          # 用于类型提示
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_utils.py
└── docs/
    └── index.md
```

**优势：**
- 防止意外从源码直接导入
- 测试导入更清晰
- 隔离性更好

**source layout 对应的 pyproject.toml：**
```toml
[tool.setuptools.packages.find]
where = ["src"]
```

### 模式 2：Flat Layout

```
my-package/
├── pyproject.toml
├── README.md
├── my_package/
│   ├── __init__.py
│   └── module.py
└── tests/
    └── test_module.py
```

**更简单但：**
- 未安装时也能导入包
- 对库项目来说不够规范

### 模式 3：多包项目

```
project/
├── pyproject.toml
├── packages/
│   ├── package-a/
│   │   └── src/
│   │       └── package_a/
│   └── package-b/
│       └── src/
│           └── package_b/
└── tests/
```

## 完整 pyproject.toml 示例

### 模式 4：功能完整的 pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-awesome-package"
version = "1.0.0"
description = "An awesome Python package"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"},
]
maintainers = [
    {name = "Maintainer Name", email = "maintainer@example.com"},
]
keywords = ["example", "package", "awesome"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "requests>=2.28.0,<3.0.0",
    "click>=8.0.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.0.0",
]
docs = [
    "sphinx>=5.0.0",
    "sphinx-rtd-theme>=1.0.0",
]
all = [
    "my-awesome-package[dev,docs]",
]

[project.urls]
Homepage = "https://github.com/username/my-awesome-package"
Documentation = "https://my-awesome-package.readthedocs.io"
Repository = "https://github.com/username/my-awesome-package"
"Bug Tracker" = "https://github.com/username/my-awesome-package/issues"
Changelog = "https://github.com/username/my-awesome-package/blob/main/CHANGELOG.md"

[project.scripts]
my-cli = "my_package.cli:main"
awesome-tool = "my_package.tools:run"

[project.entry-points."my_package.plugins"]
plugin1 = "my_package.plugins:plugin1"

[tool.setuptools]
package-dir = {"" = "src"}
zip-safe = false

[tool.setuptools.packages.find]
where = ["src"]
include = ["my_package*"]
exclude = ["tests*"]

[tool.setuptools.package-data]
my_package = ["py.typed", "*.pyi", "data/*.json"]

# Black 配置
[tool.black]
line-length = 100
target-version = ["py38", "py39", "py310", "py311"]
include = '\.pyi?$'

# Ruff 配置
[tool.ruff]
line-length = 100
target-version = "py38"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

# MyPy 配置
[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

# Pytest 配置
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "-v --cov=my_package --cov-report=term-missing"

# Coverage 配置
[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
```

### 模式 5：动态版本管理

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm>=8.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
dynamic = ["version"]
description = "Package with dynamic version"

[tool.setuptools.dynamic]
version = {attr = "my_package.__version__"}

# 或使用 setuptools-scm 实现基于 git 的版本管理
[tool.setuptools_scm]
write_to = "src/my_package/_version.py"
```

**在 __init__.py 中：**
```python
# src/my_package/__init__.py
__version__ = "1.0.0"

# 或使用 setuptools-scm
from importlib.metadata import version
__version__ = version("my-package")
```

## 命令行接口（CLI）模式

### 模式 6：使用 Click 构建 CLI

```python
# src/my_package/cli.py
import click

@click.group()
@click.version_option()
def cli():
    """My awesome CLI tool."""
    pass

@cli.command()
@click.argument("name")
@click.option("--greeting", default="Hello", help="Greeting to use")
def greet(name: str, greeting: str):
    """Greet someone."""
    click.echo(f"{greeting}, {name}!")

@cli.command()
@click.option("--count", default=1, help="Number of times to repeat")
def repeat(count: int):
    """Repeat a message."""
    for i in range(count):
        click.echo(f"Message {i + 1}")

def main():
    """Entry point for CLI."""
    cli()

if __name__ == "__main__":
    main()
```

**在 pyproject.toml 中注册：**
```toml
[project.scripts]
my-tool = "my_package.cli:main"
```

**用法：**
```bash
pip install -e .
my-tool greet World
my-tool greet Alice --greeting="Hi"
my-tool repeat --count=3
```

### 模式 7：使用 argparse 构建 CLI

```python
# src/my_package/cli.py
import argparse
import sys

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="My awesome tool",
        prog="my-tool"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Add subcommand
    process_parser = subparsers.add_parser("process", help="Process data")
    process_parser.add_argument("input_file", help="Input file path")
    process_parser.add_argument(
        "--output", "-o",
        default="output.txt",
        help="Output file path"
    )

    args = parser.parse_args()

    if args.command == "process":
        process_data(args.input_file, args.output)
    else:
        parser.print_help()
        sys.exit(1)

def process_data(input_file: str, output_file: str):
    """Process data from input to output."""
    print(f"Processing {input_file} -> {output_file}")

if __name__ == "__main__":
    main()
```

## 构建与发布

### 模式 8：本地构建包

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# This creates:
# dist/
#   my-package-1.0.0.tar.gz (source distribution)
#   my_package-1.0.0-py3-none-any.whl (wheel)

# Check the distribution
twine check dist/*
```

### 模式 9：发布到 PyPI

```bash
# Install publishing tools
pip install twine

# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Install from TestPyPI to test
pip install --index-url https://test.pypi.org/simple/ my-package

# If all good, publish to PyPI
twine upload dist/*
```

**使用 API token（推荐）：**
```bash
# Create ~/.pypirc
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-...your-token...

[testpypi]
username = __token__
password = pypi-...your-test-token...
```

### 模式 10：使用 GitHub Actions 自动发布

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  publish:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install build twine

      - name: Build package
        run: python -m build

      - name: Check package
        run: twine check dist/*

      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

## 进阶模式

### 模式 11：包含数据文件

```toml
[tool.setuptools.package-data]
my_package = [
    "data/*.json",
    "templates/*.html",
    "static/css/*.css",
    "py.typed",
]
```

**访问数据文件：**
```python
# src/my_package/loader.py
from importlib.resources import files
import json

def load_config():
    """Load configuration from package data."""
    config_file = files("my_package").joinpath("data/config.json")
    with config_file.open() as f:
        return json.load(f)

# Python 3.9+
from importlib.resources import files

data = files("my_package").joinpath("data/file.txt").read_text()
```

### 模式 12：Namespace Packages

**适用于跨多个仓库拆分的大型项目：**

```
# Package 1: company-core
company/
└── core/
    ├── __init__.py
    └── models.py

# Package 2: company-api
company/
└── api/
    ├── __init__.py
    └── routes.py
```

**不要在 namespace 目录（company/）中包含 __init__.py：**

```toml
# company-core/pyproject.toml
[project]
name = "company-core"

[tool.setuptools.packages.find]
where = ["."]
include = ["company.core*"]

# company-api/pyproject.toml
[project]
name = "company-api"

[tool.setuptools.packages.find]
where = ["."]
include = ["company.api*"]
```

**用法：**
```python
# 两个包可以在同一 namespace 下导入
from company.core import models
from company.api import routes
```

### 模式 13：C 扩展

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel", "Cython>=0.29"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
ext-modules = [
    {name = "my_package.fast_module", sources = ["src/fast_module.c"]},
]
```

**或使用 setup.py：**
```python
# setup.py
from setuptools import setup, Extension

setup(
    ext_modules=[
        Extension(
            "my_package.fast_module",
            sources=["src/fast_module.c"],
            include_dirs=["src/include"],
        )
    ]
)
```

## 版本管理

### 模式 14：语义化版本

```python
# src/my_package/__init__.py
__version__ = "1.2.3"

# Semantic versioning: MAJOR.MINOR.PATCH
# MAJOR: Breaking changes
# MINOR: New features (backward compatible)
# PATCH: Bug fixes
```

**依赖中的版本约束：**
```toml
dependencies = [
    "requests>=2.28.0,<3.0.0",  # Compatible range
    "click~=8.1.0",              # Compatible release (~= 8.1.0 means >=8.1.0,<8.2.0)
    "pydantic>=2.0",             # Minimum version
    "numpy==1.24.3",             # Exact version (avoid if possible)
]
```

### 模式 15：基于 Git 的版本管理

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools-scm>=8.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
dynamic = ["version"]

[tool.setuptools_scm]
write_to = "src/my_package/_version.py"
version_scheme = "post-release"
local_scheme = "dirty-tag"
```

**生成的版本号示例：**
- `1.0.0`（来自 git tag）
- `1.0.1.dev3+g1234567`（tag 之后 3 个 commit）

## 测试安装

### 模式 16：可编辑安装

```bash
# Install in development mode
pip install -e .

# With optional dependencies
pip install -e ".[dev]"
pip install -e ".[dev,docs]"

# Now changes to source code are immediately reflected
```

### 模式 17：在隔离环境中测试

```bash
# Create virtual environment
python -m venv test-env
source test-env/bin/activate  # Linux/Mac
# test-env\Scripts\activate  # Windows

# Install package
pip install dist/my_package-1.0.0-py3-none-any.whl

# Test it works
python -c "import my_package; print(my_package.__version__)"

# Test CLI
my-tool --help

# Cleanup
deactivate
rm -rf test-env
```

## 文档

### 模式 18：README.md 模板

```markdown
# My Package

[![PyPI version](https://badge.fury.io/py/my-package.svg)](https://pypi.org/project/my-package/)
[![Python versions](https://img.shields.io/pypi/pyversions/my-package.svg)](https://pypi.org/project/my-package/)
[![Tests](https://github.com/username/my-package/workflows/Tests/badge.svg)](https://github.com/username/my-package/actions)

Brief description of your package.

## Installation

```bash
pip install my-package
```

## Quick Start

```python
from my_package import something

result = something.do_stuff()
```

## Features

- Feature 1
- Feature 2
- Feature 3

## Documentation

Full documentation: https://my-package.readthedocs.io

## Development

```bash
git clone https://github.com/username/my-package.git
cd my-package
pip install -e ".[dev]"
pytest
```

## License

MIT
```

## 常用模式

### 模式 19：多架构 Wheel 构建

```yaml
# .github/workflows/wheels.yml
name: Build wheels

on: [push, pull_request]

jobs:
  build_wheels:
    name: Build wheels on ${{ matrix.os }}
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]

    steps:
      - uses: actions/checkout@v3

      - name: Build wheels
        uses: pypa/cibuildwheel@v2.16.2

      - uses: actions/upload-artifact@v3
        with:
          path: ./wheelhouse/*.whl
```

### 模式 20：私有包索引

```bash
# Install from private index
pip install my-package --index-url https://private.pypi.org/simple/

# Or add to pip.conf
[global]
index-url = https://private.pypi.org/simple/
extra-index-url = https://pypi.org/simple/

# Upload to private index
twine upload --repository-url https://private.pypi.org/ dist/*
```

## 文件模板

### Python 包的 .gitignore

```gitignore
# Build artifacts
build/
dist/
*.egg-info/
*.egg
.eggs/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp

# Testing
.pytest_cache/
.coverage
htmlcov/

# Distribution
*.whl
*.tar.gz
```

### MANIFEST.in

```
# MANIFEST.in
include README.md
include LICENSE
include pyproject.toml

recursive-include src/my_package/data *.json
recursive-include src/my_package/templates *.html
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
```

## 发布清单

- [ ] 代码已测试（pytest 通过）
- [ ] 文档完整（README、docstrings）
- [ ] 版本号已更新
- [ ] CHANGELOG.md 已更新
- [ ] LICENSE 文件已包含
- [ ] pyproject.toml 配置完整
- [ ] 包构建无报错
- [ ] 在干净环境中测试过安装
- [ ] CLI 工具正常运行（如适用）
- [ ] PyPI 元数据正确（classifiers、keywords）
- [ ] GitHub 仓库已关联
- [ ] 已在 TestPyPI 上测试
- [ ] 已为发布创建 git tag

## 资源

- **Python Packaging Guide**: https://packaging.python.org/
- **PyPI**: https://pypi.org/
- **TestPyPI**: https://test.pypi.org/
- **setuptools documentation**: https://setuptools.pypa.io/
- **build**: https://pypa-build.readthedocs.io/
- **twine**: https://twine.readthedocs.io/

## 最佳实践总结

1. **使用 src/ layout** 获得更清晰的包结构
2. **使用 pyproject.toml** 进行现代打包
3. **锁定构建依赖** 版本写在 build-system.requires 中
4. **合理管理版本** 采用语义化版本
5. **包含完整元数据**（classifiers、URLs 等）
6. **在干净环境中测试安装**
7. **先发布到 TestPyPI** 再发正式版
8. **完善文档** 编写 README 和 docstrings
9. **包含 LICENSE** 文件
10. **自动化发布** 使用 CI/CD
