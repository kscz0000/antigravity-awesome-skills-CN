---
name: environment-setup-guide
description: "指导开发者搭建开发环境，包括工具、依赖和配置的正确设置"
risk: unknown
source: community
date_added: "2026-02-27"
---

<!-- security-allowlist: curl-pipe-bash -->

# 环境搭建指南

## 概述

帮助开发者从零开始搭建完整的开发环境。本技能提供分步指导，涵盖工具安装、依赖配置、环境变量设置以及验证环境是否正常工作。

## 何时使用本技能

- 启动新项目需要搭建开发环境时使用
- 新成员加入项目团队时使用
- 切换到新机器或操作系统时使用
- 排查环境相关问题时使用
- 为项目编写搭建说明时使用
- 创建开发环境文档时使用

## 工作原理

### 步骤 1：识别需求

我会帮你确定需要安装的内容：
- 编程语言及版本（Node.js、Python、Go 等）
- 包管理器（npm、pip、cargo 等）
- 数据库系统（PostgreSQL、MongoDB、Redis 等）
- 开发工具（Git、Docker、IDE 扩展等）
- 环境变量和配置文件

### 步骤 2：检查当前环境

在安装任何内容之前，我会帮你检查已安装的工具：
```bash
# 检查已安装工具的版本
node --version
python --version
git --version
docker --version
```

### 步骤 3：提供安装说明

我会提供特定平台的安装命令：
- **macOS：** 使用 Homebrew
- **Linux：** 使用 apt、yum 或包管理器
- **Windows：** 使用 Chocolatey、Scoop 或直接安装程序

### 步骤 4：配置环境

帮助设置：
- 环境变量（.env 文件）
- 配置文件（.gitconfig、.npmrc 等）
- IDE 设置（VS Code、IntelliJ 等）
- Shell 配置（.bashrc、.zshrc 等）

### 步骤 5：验证安装

提供验证步骤确保一切正常：
- 运行版本检查
- 测试基本命令
- 验证数据库连接
- 检查环境变量是否加载

## 示例

### 示例 1：Node.js 项目搭建

```markdown
## 搭建 Node.js 开发环境

### 前置条件
- macOS、Linux 或 Windows
- 终端/命令提示符访问权限
- 网络连接

### 步骤 1：安装 Node.js

**macOS（使用 Homebrew）：**
\`\`\`bash
# 如果未安装 Homebrew，先安装
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Node.js
brew install node
\`\`\`

**Linux（Ubuntu/Debian）：**
\`\`\`bash
# 更新包列表
sudo apt update

# 安装 Node.js 和 npm
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
\`\`\`

**Windows（使用 Chocolatey）：**
\`\`\`powershell
# 如果未安装 Chocolatey，先安装
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 安装 Node.js
choco install nodejs
\`\`\`

### 步骤 2：验证安装

\`\`\`bash
node --version  # 应显示 v20.x.x 或更高版本
npm --version   # 应显示 10.x.x 或更高版本
\`\`\`

### 步骤 3：安装项目依赖

\`\`\`bash
# 克隆仓库
git clone https://github.com/your-repo/project.git
cd project

# 安装依赖
npm install
\`\`\`

### 步骤 4：设置环境变量

创建 \`.env\` 文件：
\`\`\`bash
# 复制示例环境文件
cp .env.example .env

# 编辑并填入你的值
nano .env
\`\`\`

示例 \`.env\` 内容：
\`\`\`
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://localhost:5432/mydb
API_KEY=your-api-key-here
\`\`\`

### 步骤 5：运行项目

\`\`\`bash
# 启动开发服务器
npm run dev

# 应显示：Server running on http://localhost:3000
\`\`\`

### 故障排除

**问题：** "node: command not found"
**解决方案：** 重启终端或运行 \`source ~/.bashrc\`（Linux）或 \`source ~/.zshrc\`（macOS）

**问题：** "Permission denied" 错误
**解决方案：** 不要在 npm 中使用 sudo。修复权限：
\`\`\`bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
\`\`\`
```

### 示例 2：Python 项目搭建

```markdown
## 搭建 Python 开发环境

### 步骤 1：安装 Python

**macOS：**
\`\`\`bash
brew install python@3.11
\`\`\`

**Linux：**
\`\`\`bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
\`\`\`

**Windows：**
\`\`\`powershell
choco install python --version=3.11
\`\`\`

### 步骤 2：验证安装

\`\`\`bash
python3 --version  # 应显示 Python 3.11.x
pip3 --version     # 应显示 pip 23.x.x
\`\`\`

### 步骤 3：创建虚拟环境

\`\`\`bash
# 进入项目目录
cd my-project

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
\`\`\`

### 步骤 4：安装依赖

\`\`\`bash
# 从 requirements.txt 安装
pip install -r requirements.txt

# 或单独安装包
pip install flask sqlalchemy python-dotenv
\`\`\`

### 步骤 5：设置环境变量

创建 \`.env\` 文件：
\`\`\`
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=your-secret-key-here
\`\`\`

### 步骤 6：运行应用

\`\`\`bash
# 运行 Flask 应用
flask run

# 应显示：Running on http://127.0.0.1:5000
\`\`\`
```

### 示例 3：Docker 开发环境

```markdown
## 搭建 Docker 开发环境

### 步骤 1：安装 Docker

**macOS：**
\`\`\`bash
brew install --cask docker
# 或从 docker.com 下载 Docker Desktop
\`\`\`

**Linux：**
\`\`\`bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 将用户添加到 docker 组
sudo usermod -aG docker $USER
newgrp docker
\`\`\`

**Windows：**
从 docker.com 下载 Docker Desktop

### 步骤 2：验证安装

\`\`\`bash
docker --version        # 应显示 Docker version 24.x.x
docker-compose --version # 应显示 Docker Compose version 2.x.x
\`\`\`

### 步骤 3：创建 docker-compose.yml

\`\`\`yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:password@db:5432/mydb
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
\`\`\`

### 步骤 4：启动服务

\`\`\`bash
# 构建并启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
\`\`\`

### 步骤 5：验证服务

\`\`\`bash
# 检查运行中的容器
docker ps

# 测试数据库连接
docker-compose exec db psql -U postgres -d mydb
\`\`\`
```

## 最佳实践

### ✅ 推荐做法

- **记录一切** - 编写清晰的搭建说明
- **使用版本管理器** - Node 用 nvm，Python 用 pyenv
- **创建 .env.example** - 展示必需的环境变量
- **在干净系统上测试** - 验证说明从零开始也能工作
- **包含故障排除** - 记录常见问题和解决方案
- **使用 Docker** - 实现跨机器的一致环境
- **锁定版本** - 在包文件中指定确切版本
- **自动化搭建** - 尽可能创建搭建脚本
- **检查前置条件** - 开始前列出所需工具
- **提供验证步骤** - 帮助用户确认搭建成功

### ❌ 避免做法

- **不要假设工具已安装** - 始终检查并提供安装说明
- **不要遗漏环境变量** - 记录所有必需的变量
- **不要在 npm 中使用 sudo** - 应修复权限问题
- **不要忽略平台差异** - 提供特定操作系统的说明
- **不要省略验证** - 始终包含测试步骤
- **不要使用全局安装** - 优先使用本地/虚拟环境
- **不要忽略错误** - 记录如何处理常见错误
- **不要跳过数据库设置** - 包含数据库初始化步骤

## 常见陷阱

### 问题：安装后出现 "Command not found"
**症状：** 已安装工具但终端无法识别
**解决方案：**
- 重启终端或重新加载 shell 配置
- 检查 PATH 环境变量
- 验证安装位置
```bash
# 检查 PATH
echo $PATH

# 添加到 PATH（示例）
export PATH="/usr/local/bin:$PATH"
```

### 问题：npm/pip 权限错误
**症状：** "EACCES" 或 "Permission denied" 错误
**解决方案：**
- 不要使用 sudo
- 修复 npm 权限或使用 nvm
- Python 使用虚拟环境
```bash
# 修复 npm 权限
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
```

### 问题：端口已被占用
**症状：** "Port 3000 is already in use"
**解决方案：**
- 查找并终止占用端口的进程
- 使用不同的端口
```bash
# 查找占用 3000 端口的进程
lsof -i :3000

# 终止进程
kill -9 <PID>

# 或使用不同端口
PORT=3001 npm start
```

### 问题：数据库连接失败
**症状：** "Connection refused" 或 "Authentication failed"
**解决方案：**
- 验证数据库是否运行
- 检查连接字符串
- 验证凭据
```bash
# 检查 PostgreSQL 是否运行
sudo systemctl status postgresql

# 测试连接
psql -h localhost -U postgres -d mydb
```

## 搭建脚本模板

创建 `setup.sh` 脚本自动化搭建：

```bash
#!/bin/bash

echo "🚀 正在搭建开发环境..."

# 检查前置条件
command -v node >/dev/null 2>&1 || { echo "❌ Node.js 未安装"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git 未安装"; exit 1; }

echo "✅ 前置条件检查通过"

# 安装依赖
echo "📦 正在安装依赖..."
npm install

# 复制环境文件
if [ ! -f .env ]; then
    echo "📝 正在创建 .env 文件..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 填入你的配置"
fi

# 运行数据库迁移
echo "🗄️  正在运行数据库迁移..."
npm run migrate

# 验证搭建
echo "🔍 正在验证搭建..."
npm run test:setup

echo "✅ 搭建完成！运行 'npm run dev' 启动"
```

## 相关技能

- `@brainstorming` - 在搭建前规划环境需求
- `@systematic-debugging` - 调试环境问题
- `@doc-coauthoring` - 创建搭建文档
- `@git-pushing` - 设置 Git 配置

## 更多资源

- [Node.js 安装指南](https://nodejs.org/en/download/)
- [Python 虚拟环境](https://docs.python.org/3/tutorial/venv.html)
- [Docker 文档](https://docs.docker.com/get-started/)
- [Homebrew（macOS）](https://brew.sh/)
- [Chocolatey（Windows）](https://chocolatey.org/)
- [nvm（Node 版本管理器）](https://github.com/nvm-sh/nvm)
- [pyenv（Python 版本管理器）](https://github.com/pyenv/pyenv)

---

**专业提示：** 创建 `setup.sh` 或 `setup.ps1` 脚本自动化整个搭建流程。在干净系统上测试以确保其正常工作！

## 局限性
- 仅当任务明确符合上述范围时使用本技能。
- 输出内容不能替代特定环境的验证、测试或专家评审。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
