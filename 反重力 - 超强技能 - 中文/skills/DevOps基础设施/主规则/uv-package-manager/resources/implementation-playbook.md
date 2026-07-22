# UV 包管理器实战手册

本文件包含技能引用的详细模式、检查清单和代码示例。

# UV 包管理器

使用 uv 的全面指南——一个用 Rust 编写的极速 Python 包安装器和解析器，用于现代 Python 项目管理和依赖工作流。

## 适用场景

- 快速搭建新的 Python 项目
- 比 pip 更高效地管理 Python 依赖
- 创建和管理虚拟环境
- 安装 Python 解释器
- 高效解决依赖冲突
- 从 pip/pip-tools/poetry 迁移
- 加速 CI/CD 流水线
- 管理 monorepo Python 项目
- 使用 lockfile 实现可复现构建
- 优化含 Python 依赖的 Docker 构建

## 核心概念

### 1. uv 是什么？
- **超快的包安装器**：比 pip 快 10-100 倍
- **用 Rust 编写**：充分利用 Rust 的性能优势
- **pip 的直接替代品**：兼容 pip 工作流
- **虚拟环境管理器**：创建和管理 venv
- **Python 安装器**：下载和管理 Python 版本
- **依赖解析器**：高级依赖解析能力
- **支持 lockfile**：可复现的安装

### 2. 核心特性
- 极速安装
- 全局缓存，节省磁盘空间
- 兼容 pip、pip-tools、poetry
- 全面的依赖解析
- 跨平台支持（Linux、macOS、Windows）
- 安装时不需要 Python
- 内置虚拟环境支持

### 3. uv 与传统工具对比
- **对比 pip**：快 10-100 倍，解析器更强
- **对比 pip-tools**：更快、更简洁、体验更好
- **对比 poetry**：更快、更灵活、更轻量
- **对比 conda**：更快、专注 Python

## 安装

### 快速安装

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Using pip (if you already have Python)
pip install uv

# Using Homebrew (macOS)
brew install uv

# Using cargo (if you have Rust)
cargo install --git https://github.com/astral-sh/uv uv
```

### 验证安装

```bash
uv --version
# uv 0.x.x
```

## 快速开始

### 创建新项目

```bash
# Create new project with virtual environment
uv init my-project
cd my-project

# Or create in current directory
uv init .

# Initialize creates:
# - .python-version (Python version)
# - pyproject.toml (project config)
# - README.md
# - .gitignore
```

### 安装依赖

```bash
# Install packages (creates venv if needed)
uv add requests pandas

# Install dev dependencies
uv add --dev pytest black ruff

# Install from requirements.txt
uv pip install -r requirements.txt

# Install from pyproject.toml
uv sync
```

## 虚拟环境管理

### 模式 1：创建虚拟环境

```bash
# Create virtual environment with uv
uv venv

# Create with specific Python version
uv venv --python 3.12

# Create with custom name
uv venv my-env

# Create with system site packages
uv venv --system-site-packages

# Specify location
uv venv /path/to/venv
```

### 模式 2：激活虚拟环境

```bash
# Linux/macOS
source .venv/bin/activate

# Windows (Command Prompt)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Or use uv run (no activation needed)
uv run python script.py
uv run pytest
```

### 模式 3：使用 uv run

```bash
# Run Python script (auto-activates venv)
uv run python app.py

# Run installed CLI tool
uv run black .
uv run pytest

# Run with specific Python version
uv run --python 3.11 python script.py

# Pass arguments
uv run python script.py --arg value
```

## 包管理

### 模式 4：添加依赖

```bash
# Add package (adds to pyproject.toml)
uv add requests

# Add with version constraint
uv add "django>=4.0,<5.0"

# Add multiple packages
uv add numpy pandas matplotlib

# Add dev dependency
uv add --dev pytest pytest-cov

# Add optional dependency group
uv add --optional docs sphinx

# Add from git
uv add git+https://github.com/user/repo.git

# Add from git with specific ref
uv add git+https://github.com/user/repo.git@v1.0.0

# Add from local path
uv add ./local-package

# Add editable local package
uv add -e ./local-package
```

### 模式 5：移除依赖

```bash
# Remove package
uv remove requests

# Remove dev dependency
uv remove --dev pytest

# Remove multiple packages
uv remove numpy pandas matplotlib
```

### 模式 6：升级依赖

```bash
# Upgrade specific package
uv add --upgrade requests

# Upgrade all packages
uv sync --upgrade

# Upgrade package to latest
uv add --upgrade requests

# Show what would be upgraded
uv tree --outdated
```

### 模式 7：锁定依赖

```bash
# Generate uv.lock file
uv lock

# Update lock file
uv lock --upgrade

# Lock without installing
uv lock --no-install

# Lock specific package
uv lock --upgrade-package requests
```

## Python 版本管理

### 模式 8：安装 Python 版本

```bash
# Install Python version
uv python install 3.12

# Install multiple versions
uv python install 3.11 3.12 3.13

# Install latest version
uv python install

# List installed versions
uv python list

# Find available versions
uv python list --all-versions
```

### 模式 9：设置 Python 版本

```bash
# Set Python version for project
uv python pin 3.12

# This creates/updates .python-version file

# Use specific Python version for command
uv --python 3.11 run python script.py

# Create venv with specific version
uv venv --python 3.12
```

## 项目配置

### 模式 10：uv 的 pyproject.toml 配置

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
    "click>=8.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.5.0",
]
docs = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.3.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    # Additional dev dependencies managed by uv
]

[tool.uv.sources]
# Custom package sources
my-package = { git = "https://github.com/user/repo.git" }
```

### 模式 11：在现有项目中使用 uv

```bash
# Migrate from requirements.txt
uv add -r requirements.txt

# Migrate from poetry
# Already have pyproject.toml, just use:
uv sync

# Export to requirements.txt
uv pip freeze > requirements.txt

# Export with hashes
uv pip freeze --require-hashes > requirements.txt
```

## 高级工作流

### 模式 12：Monorepo 支持

```bash
# Project structure
# monorepo/
#   packages/
#     package-a/
#       pyproject.toml
#     package-b/
#       pyproject.toml
#   pyproject.toml (root)

# Root pyproject.toml
[tool.uv.workspace]
members = ["packages/*"]

# Install all workspace packages
uv sync

# Add workspace dependency
uv add --path ./packages/package-a
```

### 模式 13：CI/CD 集成

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v2
        with:
          enable-cache: true

      - name: Set up Python
        run: uv python install 3.12

      - name: Install dependencies
        run: uv sync --all-extras --dev

      - name: Run tests
        run: uv run pytest

      - name: Run linting
        run: |
          uv run ruff check .
          uv run black --check .
```

### 模式 14：Docker 集成

```dockerfile
# Dockerfile
FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Run application
CMD ["uv", "run", "python", "app.py"]
```

**优化的多阶段构建：**

```dockerfile
# Multi-stage Dockerfile
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install dependencies to venv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-editable

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy venv from builder
COPY --from=builder /app/.venv .venv
COPY . .

# Use venv
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "app.py"]
```

### 模式 15：Lockfile 工作流

```bash
# Create lockfile (uv.lock)
uv lock

# Install from lockfile (exact versions)
uv sync --frozen

# Update lockfile without installing
uv lock --no-install

# Upgrade specific package in lock
uv lock --upgrade-package requests

# Check if lockfile is up to date
uv lock --check

# Export lockfile to requirements.txt
uv export --format requirements-txt > requirements.txt

# Export with hashes for security
uv export --format requirements-txt --hash > requirements.txt
```

## 性能优化

### 模式 16：使用全局缓存

```bash
# UV automatically uses global cache at:
# Linux: ~/.cache/uv
# macOS: ~/Library/Caches/uv
# Windows: %LOCALAPPDATA%\uv\cache

# Clear cache
uv cache clean

# Check cache size
uv cache dir
```

### 模式 17：并行安装

```bash
# UV installs packages in parallel by default

# Control parallelism
uv pip install --jobs 4 package1 package2

# No parallel (sequential)
uv pip install --jobs 1 package
```

### 模式 18：离线模式

```bash
# Install from cache only (no network)
uv pip install --offline package

# Sync from lockfile offline
uv sync --frozen --offline
```

## 与其他工具对比

### uv vs pip

```bash
# pip
python -m venv .venv
source .venv/bin/activate
pip install requests pandas numpy
# ~30 seconds

# uv
uv venv
uv add requests pandas numpy
# ~2 seconds (10-15x faster)
```

### uv vs poetry

```bash
# poetry
poetry init
poetry add requests pandas
poetry install
# ~20 seconds

# uv
uv init
uv add requests pandas
uv sync
# ~3 seconds (6-7x faster)
```

### uv vs pip-tools

```bash
# pip-tools
pip-compile requirements.in
pip-sync requirements.txt
# ~15 seconds

# uv
uv lock
uv sync --frozen
# ~2 seconds (7-8x faster)
```

## 常用工作流

### 模式 19：启动新项目

```bash
# Complete workflow
uv init my-project
cd my-project

# Set Python version
uv python pin 3.12

# Add dependencies
uv add fastapi uvicorn pydantic

# Add dev dependencies
uv add --dev pytest black ruff mypy

# Create structure
mkdir -p src/my_project tests

# Run tests
uv run pytest

# Format code
uv run black .
uv run ruff check .
```

### 模式 20：维护现有项目

```bash
# Clone repository
git clone https://github.com/user/project.git
cd project

# Install dependencies (creates venv automatically)
uv sync

# Install with dev dependencies
uv sync --all-extras

# Update dependencies
uv lock --upgrade

# Run application
uv run python app.py

# Run tests
uv run pytest

# Add new dependency
uv add new-package

# Commit updated files
git add pyproject.toml uv.lock
git commit -m "Add new-package dependency"
```

## 工具集成

### 模式 21：Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: uv-lock
        name: uv lock
        entry: uv lock
        language: system
        pass_filenames: false

      - id: ruff
        name: ruff
        entry: uv run ruff check --fix
        language: system
        types: [python]

      - id: black
        name: black
        entry: uv run black
        language: system
        types: [python]
```

### 模式 22：VS Code 集成

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["-v"],
  "python.linting.enabled": true,
  "python.formatting.provider": "black",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  }
}
```

## 故障排查

### 常见问题

```bash
# Issue: uv not found
# Solution: Add to PATH or reinstall
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc

# Issue: Wrong Python version
# Solution: Pin version explicitly
uv python pin 3.12
uv venv --python 3.12

# Issue: Dependency conflict
# Solution: Check resolution
uv lock --verbose

# Issue: Cache issues
# Solution: Clear cache
uv cache clean

# Issue: Lockfile out of sync
# Solution: Regenerate
uv lock --upgrade
```

## 最佳实践

### 项目设置

1. **始终使用 lockfile** 以确保可复现性
2. **固定 Python 版本** 使用 .python-version
3. **分离开发依赖** 与生产依赖
4. **使用 uv run** 代替手动激活虚拟环境
5. **提交 uv.lock** 到版本控制
6. **在 CI 中使用 --frozen** 以确保构建一致性
7. **利用全局缓存** 提升速度
8. **使用 workspace** 管理 monorepo
9. **导出 requirements.txt** 保持兼容性
10. **保持 uv 更新** 获取最新特性

### 性能技巧

```bash
# Use frozen installs in CI
uv sync --frozen

# Use offline mode when possible
uv sync --offline

# Parallel operations (automatic)
# uv does this by default

# Reuse cache across environments
# uv shares cache globally

# Use lockfiles to skip resolution
uv sync --frozen  # skips resolution
```

## 迁移指南

### 从 pip + requirements.txt 迁移

```bash
# Before
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# After
uv venv
uv pip install -r requirements.txt
# Or better:
uv init
uv add -r requirements.txt
```

### 从 Poetry 迁移

```bash
# Before
poetry install
poetry add requests

# After
uv sync
uv add requests

# Keep existing pyproject.toml
# uv reads [project] and [tool.poetry] sections
```

### 从 pip-tools 迁移

```bash
# Before
pip-compile requirements.in
pip-sync requirements.txt

# After
uv lock
uv sync --frozen
```

## 命令速查

### 核心命令

```bash
# Project management
uv init [PATH]              # Initialize project
uv add PACKAGE              # Add dependency
uv remove PACKAGE           # Remove dependency
uv sync                     # Install dependencies
uv lock                     # Create/update lockfile

# Virtual environments
uv venv [PATH]              # Create venv
uv run COMMAND              # Run in venv

# Python management
uv python install VERSION   # Install Python
uv python list              # List installed Pythons
uv python pin VERSION       # Pin Python version

# Package installation (pip-compatible)
uv pip install PACKAGE      # Install package
uv pip uninstall PACKAGE    # Uninstall package
uv pip freeze               # List installed
uv pip list                 # List packages

# Utility
uv cache clean              # Clear cache
uv cache dir                # Show cache location
uv --version                # Show version
```

## 参考资源

- **官方文档**：https://docs.astral.sh/uv/
- **GitHub 仓库**：https://github.com/astral-sh/uv
- **Astral 博客**：https://astral.sh/blog
- **迁移指南**：https://docs.astral.sh/uv/guides/
- **工具对比**：https://docs.astral.sh/uv/pip/compatibility/

## 最佳实践总结

1. **所有新项目都用 uv** — 从 `uv init` 开始
2. **提交 lockfile** — 确保可复现构建
3. **固定 Python 版本** — 使用 .python-version
4. **使用 uv run** — 避免手动激活虚拟环境
5. **利用缓存** — 让 uv 管理全局缓存
6. **在 CI 中使用 --frozen** — 精确复现
7. **保持 uv 更新** — 项目迭代很快
8. **使用 workspaces** — 管理 monorepo 项目
9. **导出兼容格式** — 需要时生成 requirements.txt
10. **阅读文档** — uv 功能丰富且持续演进
