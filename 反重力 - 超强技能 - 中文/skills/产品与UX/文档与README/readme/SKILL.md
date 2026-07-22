---
name: readme
description: "专业技术文档撰写工具，用于创建全面的项目文档。当用户要求'写README'、'创建README'、'项目文档'、'文档化这个项目'、'README.md'、'project documentation'时使用。"
risk: safe
source: "https://github.com/Shpigford/skills/tree/main/readme"
date_added: "2026-02-27"
---

# README 生成器

你是一位专业技术文档撰写专家，负责创建全面的项目文档。你的目标是编写一份极其详尽的 README.md——那种你希望每个项目都拥有的文档。

## 何时使用此技能

在以下情况下使用此技能：

- 用户想要创建或更新 README.md 文件
- 用户说"写 readme"或"创建 readme"
- 用户要求"文档化这个项目"
- 用户请求"项目文档"
- 用户请求帮助处理 README.md

## README 的三大目的

1. **本地开发** - 帮助任何开发者在几分钟内在本地运行应用
2. **理解系统** - 详细解释应用的工作原理
3. **生产部署** - 涵盖在生产环境中部署和维护所需的一切

---

## 编写前准备

### 步骤 1：深度代码库探索

在编写任何文档之前，彻底探索代码库。你必须理解：

**项目结构**

- 读取根目录结构
- 识别框架/语言（Rails 的 Gemfile、package.json、go.mod、requirements.txt 等）
- 找到主入口点
- 梳理目录组织

**配置文件**

- .env.example、.env.sample 或已文档化的环境变量
- Rails 配置文件（config/database.yml、config/application.rb、config/environments/）
- 凭证设置（config/credentials.yml.enc、config/master.key）
- Docker 文件（Dockerfile、docker-compose.yml）
- CI/CD 配置（.github/workflows/、.gitlab-ci.yml 等）
- 部署配置（Kamal 的 config/deploy.yml、fly.toml、render.yaml、Procfile 等）

**数据库**

- db/schema.rb 或 db/structure.sql
- db/migrate/ 中的迁移文件
- db/seeds.rb 中的种子数据
- 从 config/database.yml 确定数据库类型

**关键依赖**

- Ruby gems 的 Gemfile 和 Gemfile.lock
- JavaScript 依赖的 package.json
- 注意任何原生 gem 依赖（pg、nokogiri 等）

**脚本和命令**

- bin/ 脚本（bin/dev、bin/setup、bin/ci）
- Procfile 或 Procfile.dev
- Rake 任务（lib/tasks/）

### 步骤 2：识别部署目标

查找以下文件以确定部署平台并定制说明：

- `Dockerfile` / `docker-compose.yml` → 基于 Docker 的部署
- `vercel.json` / `.vercel/` → Vercel
- `netlify.toml` → Netlify
- `fly.toml` → Fly.io
- `railway.json` / `railway.toml` → Railway
- `render.yaml` → Render
- `app.yaml` → Google App Engine
- `Procfile` → Heroku 或类似 Heroku 的平台
- `.ebextensions/` → AWS Elastic Beanstalk
- `serverless.yml` → Serverless Framework
- `terraform/` / `*.tf` → Terraform/基础设施即代码
- `k8s/` / `kubernetes/` → Kubernetes

如果不存在部署配置，提供以 Docker 为推荐方法的通用指导。

### 步骤 3：仅在关键时提问

仅在无法确定以下内容时向用户提问：

- 项目做什么（如果从代码中不明显）
- 需要的特定部署凭证或 URL
- 影响文档的业务上下文

否则，继续探索和编写。

---

## README 结构

按以下顺序编写 README 的各个部分：

### 1. 项目标题和概述

```markdown
# 项目名称

简要描述项目的功能和目标用户。最多 2-3 句话。

## 主要功能

- 功能 1
- 功能 2
- 功能 3
```

### 2. 技术栈

列出所有主要技术：

```markdown
## 技术栈

- **语言**: Ruby 3.3+
- **框架**: Rails 7.2+
- **前端**: Inertia.js with React
- **数据库**: PostgreSQL 16
- **后台任务**: Solid Queue
- **缓存**: Solid Cache
- **样式**: Tailwind CSS
- **部署**: [检测到的平台]
```

### 3. 前置要求

开始前必须安装的内容：

```markdown
## 前置要求

- Node.js 20 或更高版本
- PostgreSQL 15 或更高版本（或 Docker）
- pnpm（推荐）或 npm
- 用于 OAuth 的 Google Cloud 项目（开发环境可选）
```

### 4. 快速开始

完整的本地开发指南：

```markdown
## 快速开始

### 1. 克隆仓库

\`\`\`bash
git clone https://github.com/user/repo.git
cd repo
\`\`\`

### 2. 安装 Ruby 依赖

确保已安装 Ruby 3.3+（通过 rbenv、asdf 或 mise）：

\`\`\`bash
bundle install
\`\`\`

### 3. 安装 JavaScript 依赖

\`\`\`bash
yarn install
\`\`\`

### 4. 环境设置

复制示例环境文件：

\`\`\`bash
cp .env.example .env
\`\`\`

配置以下变量：

| 变量               | 描述                  | 示例                                    |
| ------------------ | ---------------------------- | ------------------------------------------ |
| `DATABASE_URL`     | PostgreSQL 连接字符串 | `postgresql://localhost/myapp_development` |
| `REDIS_URL`        | Redis 连接（如使用）   | `redis://localhost:6379/0`                 |
| `SECRET_KEY_BASE`  | Rails 密钥             | `bin/rails secret`                         |
| `RAILS_MASTER_KEY` | 用于凭证加密   | 检查 `config/master.key`                  |

### 5. 数据库设置

启动 PostgreSQL（如使用 Docker）：

\`\`\`bash
docker run --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16
\`\`\`

创建并设置数据库：

\`\`\`bash
bin/rails db:setup
\`\`\`

此命令运行 `db:create`、`db:schema:load` 和 `db:seed`。

对于已存在的数据库，运行迁移：

\`\`\`bash
bin/rails db:migrate
\`\`\`

### 6. 启动开发服务器

使用 Foreman/Overmind（推荐，运行 Rails + Vite）：

\`\`\`bash
bin/dev
\`\`\`

或手动启动：

\`\`\`bash

# 终端 1：Rails 服务器

bin/rails server

# 终端 2：Vite 开发服务器（用于 Inertia/React）

bin/vite dev
\`\`\`

在浏览器中打开 [http://localhost:3000](http://localhost:3000)。
```

包含每个步骤。假设读者是在全新机器上设置。

### 5. 架构概览

这是你要极其详尽的地方：

```markdown
## 架构

### 目录结构

\`\`\`
├── app/
│ ├── controllers/ # Rails 控制器
│ │ ├── concerns/ # 共享控制器模块
│ │ └── api/ # API 专用控制器
│ ├── models/ # ActiveRecord 模型
│ │ └── concerns/ # 共享模型模块
│ ├── jobs/ # 后台任务（Solid Queue）
│ ├── mailers/ # 邮件模板
│ ├── views/ # Rails 视图（使用 Inertia 时最小化）
│ └── frontend/ # Inertia.js React 组件
│ ├── components/ # 可复用 UI 组件
│ ├── layouts/ # 页面布局
│ ├── pages/ # Inertia 页面组件
│ └── lib/ # 前端工具
├── config/
│ ├── routes.rb # 路由定义
│ ├── database.yml # 数据库配置
│ └── initializers/ # 应用初始化器
├── db/
│ ├── migrate/ # 数据库迁移
│ ├── schema.rb # 当前模式
│ └── seeds.rb # 种子数据
├── lib/
│ └── tasks/ # 自定义 Rake 任务
└── public/ # 静态资源
\`\`\`

### 请求生命周期

1. 请求到达 Rails 路由器（`config/routes.rb`）
2. 中间件栈处理请求（认证、会话等）
3. 控制器动作执行
4. 模型通过 ActiveRecord 与 PostgreSQL 交互
5. Inertia 渲染 React 组件并传递 props
6. 响应发送到浏览器

### 数据流

\`\`\`
用户操作 → React 组件 → Inertia Visit → Rails 控制器 → ActiveRecord → PostgreSQL
↓
React Props ← Inertia 响应 ←
\`\`\`

### 关键组件

**认证**

- 使用 Devise/Rodauth 进行用户认证
- 基于会话的认证，使用加密 cookie
- 受保护路由使用 `authenticate_user!` before_action

**Inertia.js 集成（`app/frontend/`）**

- React 组件从 Rails 控制器接收 props
- 控制器中的 `inertia_render` 将数据传递到前端
- 通过 `inertia_share` 共享布局 props 数据

**后台任务（`app/jobs/`）**

- 使用 Solid Queue 处理任务
- 任务存储在 PostgreSQL 中（无需 Redis）
- 仪表板位于 `/jobs` 用于监控

**数据库（`app/models/`）**

- ActiveRecord 模型与关联
- 复杂查询使用查询对象
- 使用 concerns 共享模型行为

### 数据库模式

\`\`\`
users
├── id (bigint, PK)
├── email (string, unique, not null)
├── encrypted_password (string)
├── name (string)
├── created_at (datetime)
└── updated_at (datetime)

posts
├── id (bigint, PK)
├── title (string, not null)
├── content (text)
├── published (boolean, default: false)
├── user_id (bigint, FK → users)
├── created_at (datetime)
└── updated_at (datetime)

solid_queue_jobs（后台任务）
├── id (bigint, PK)
├── queue_name (string)
├── class_name (string)
├── arguments (json)
├── scheduled_at (datetime)
└── ...
\`\`\`
```

### 6. 环境变量

所有环境变量的完整参考：

```markdown
## 环境变量

### 必需变量

| 变量               | 描述                       | 获取方式                             |
| ------------------ | --------------------------------- | -------------------------------------- |
| `DATABASE_URL`     | PostgreSQL 连接字符串      | 你的数据库提供商                 |
| `SECRET_KEY_BASE`  | Rails 会话/cookie 密钥 | 运行 `bin/rails secret`                 |
| `RAILS_MASTER_KEY` | 解密凭证文件         | 检查 `config/master.key`（不在 git 中） |

### 可选变量

| 变量                | 描述                                       | 默认值                      |
| ------------------- | ------------------------------------------------- | ---------------------------- |
| `REDIS_URL`         | Redis 连接字符串（用于缓存/ActionCable） | -                            |
| `RAILS_LOG_LEVEL`   | 日志详细程度                                 | `debug`（开发），`info`（生产） |
| `RAILS_MAX_THREADS` | Puma 线程数                                 | `5`                          |
| `WEB_CONCURRENCY`   | Puma 工作进程数                                 | `2`                          |
| `SMTP_ADDRESS`      | 邮件服务器主机名                              | -                            |
| `SMTP_PORT`         | 邮件服务器端口                                  | `587`                        |

### Rails 凭证

敏感值应存储在 Rails 加密凭证中：

\`\`\`bash

# 编辑凭证（在 $EDITOR 中打开）

bin/rails credentials:edit

# 或编辑特定环境的凭证

RAILS_ENV=production bin/rails credentials:edit
\`\`\`

凭证文件结构：
\`\`\`yaml
secret_key_base: xxx
stripe:
public_key: pk_xxx
secret_key: sk_xxx
google:
client_id: xxx
client_secret: xxx
\`\`\`

在代码中访问：`Rails.application.credentials.stripe[:secret_key]`

### 特定环境配置

**开发环境**
\`\`\`
DATABASE_URL=postgresql://localhost/myapp_development
REDIS_URL=redis://localhost:6379/0
\`\`\`

**生产环境**
\`\`\`
DATABASE_URL=<生产环境连接字符串>
RAILS_ENV=production
RAILS_SERVE_STATIC_FILES=true
\`\`\`
```

### 7. 可用脚本

```markdown
## 可用脚本

| 命令                       | 描述                                         |
| ----------------------------- | --------------------------------------------------- |
| `bin/dev`                     | 启动开发服务器（通过 Foreman 运行 Rails + Vite） |
| `bin/rails server`            | 仅启动 Rails 服务器                             |
| `bin/vite dev`                | 仅启动 Vite 开发服务器                          |
| `bin/rails console`           | 打开 Rails 控制台（加载应用的 IRB）            |
| `bin/rails db:migrate`        | 运行待处理的数据库迁移                     |
| `bin/rails db:rollback`       | 回滚最后一次迁移                             |
| `bin/rails db:seed`           | 运行数据库种子                                  |
| `bin/rails db:reset`          | 删除、创建、迁移并填充数据库            |
| `bin/rails routes`            | 列出所有路由                                     |
| `bin/rails test`              | 运行测试套件（Minitest）                           |
| `bundle exec rspec`           | 运行测试套件（RSpec，如使用）                     |
| `bin/rails assets:precompile` | 为生产环境编译资源                       |
| `bin/rubocop`                 | 运行 Ruby 代码检查                                     |
| `yarn lint`                   | 运行 JavaScript/TypeScript 代码检查                    |
```

### 8. 测试

```markdown
## 测试

### 运行测试

\`\`\`bash

# 运行所有测试（Minitest）

bin/rails test

# 运行所有测试（RSpec，如使用）

bundle exec rspec

# 运行特定测试文件

bin/rails test test/models/user_test.rb
bundle exec rspec spec/models/user_spec.rb

# 运行匹配模式的测试

bin/rails test -n /creates_user/
bundle exec rspec -e "creates user"

# 运行系统测试（浏览器测试）

bin/rails test:system

# 带覆盖率运行（SimpleCov）

COVERAGE=true bin/rails test
\`\`\`

### 测试结构

\`\`\`
test/ # Minitest 结构
├── controllers/ # 控制器测试
├── models/ # 模型单元测试
├── integration/ # 集成测试
├── system/ # 系统/浏览器测试
├── fixtures/ # 测试数据
└── test_helper.rb # 测试配置

spec/ # RSpec 结构（如使用）
├── models/
├── requests/
├── system/
├── factories/ # FactoryBot 工厂
├── support/
└── rails_helper.rb
\`\`\`

### 编写测试

**Minitest 示例：**
\`\`\`ruby
require "test_helper"

class UserTest < ActiveSupport::TestCase
test "creates user with valid attributes" do
user = User.new(email: "test@example.com", name: "Test User")
assert user.valid?
end

test "requires email" do
user = User.new(name: "Test User")
assert_not user.valid?
assert_includes user.errors[:email], "can't be blank"
end
end
\`\`\`

**RSpec 示例：**
\`\`\`ruby
require "rails_helper"

RSpec.describe User, type: :model do
describe "validations" do
it "is valid with valid attributes" do
user = build(:user)
expect(user).to be_valid
end

    it "requires an email" do
      user = build(:user, email: nil)
      expect(user).not_to be_valid
      expect(user.errors[:email]).to include("can't be blank")
    end

end
end
\`\`\`

### 前端测试

对于 Inertia/React 组件：

\`\`\`bash
yarn test
\`\`\`

\`\`\`typescript
import { render, screen } from '@testing-library/react'
import { Dashboard } from './Dashboard'

describe('Dashboard', () => {
it('renders user name', () => {
render(<Dashboard user={{ name: 'Josh' }} />)
expect(screen.getByText('Josh')).toBeInTheDocument()
})
})
\`\`\`
```

### 9. 部署

根据检测到的平台定制（查找 Dockerfile、fly.toml、render.yaml、kamal/ 等）：

```markdown
## 部署

### Kamal（Rails 推荐）

如果使用 Kamal 部署：

\`\`\`bash

# 设置 Kamal（首次）

kamal setup

# 部署

kamal deploy

# 回滚到上一版本

kamal rollback

# 查看日志

kamal app logs

# 在生产环境运行控制台

kamal app exec --interactive 'bin/rails console'
\`\`\`

配置文件位于 `config/deploy.yml`。

### Docker

构建并运行：

\`\`\`bash

# 构建镜像

docker build -t myapp .

# 使用环境变量运行

docker run -p 3000:3000 \
 -e DATABASE_URL=postgresql://... \
 -e SECRET_KEY_BASE=... \
 -e RAILS_ENV=production \
 myapp
\`\`\`

### Heroku

\`\`\`bash

# 创建应用

heroku create myapp

# 添加 PostgreSQL

heroku addons:create heroku-postgresql:mini

# 设置环境变量

heroku config:set SECRET_KEY_BASE=$(bin/rails secret)
heroku config:set RAILS_MASTER_KEY=$(cat config/master.key)

# 部署

git push heroku main

# 运行迁移

heroku run bin/rails db:migrate
\`\`\`

### Fly.io

\`\`\`bash

# 启动（首次）

fly launch

# 部署

fly deploy

# 运行迁移

fly ssh console -C "bin/rails db:migrate"

# 打开控制台

fly ssh console -C "bin/rails console"
\`\`\`

### Render

如果存在 `render.yaml`，将你的仓库连接到 Render，它会自动部署。

手动设置：

1. 创建新的 Web Service
2. 连接 GitHub 仓库
3. 设置构建命令：`bundle install && bin/rails assets:precompile`
4. 设置启动命令：`bin/rails server`
5. 在仪表板中添加环境变量

### 手动/VPS 部署

\`\`\`bash

# 在服务器上：

# 拉取最新代码

git pull origin main

# 安装依赖

bundle install --deployment

# 编译资源

RAILS_ENV=production bin/rails assets:precompile

# 运行迁移

RAILS_ENV=production bin/rails db:migrate

# 重启应用服务器（如通过 systemd 的 Puma）

sudo systemctl restart myapp
\`\`\`
```

### 10. 故障排除

```markdown
## 故障排除

### 数据库连接问题

**错误：** `could not connect to server: Connection refused`

**解决方案：**

1. 验证 PostgreSQL 正在运行：`pg_isready` 或 `docker ps`
2. 检查 `DATABASE_URL` 格式：`postgresql://USER:PASSWORD@HOST:PORT/DATABASE`
3. 确保数据库存在：`bin/rails db:create`

### 待处理迁移

**错误：** `Migrations are pending`

**解决方案：**
\`\`\`bash
bin/rails db:migrate
\`\`\`

### 资源编译问题

**错误：** `The asset "application.css" is not present in the asset pipeline`

**解决方案：**
\`\`\`bash

# 清除并重新编译资源

bin/rails assets:clobber
bin/rails assets:precompile
\`\`\`

### Bundle 安装失败

**错误：** 原生扩展构建失败

**解决方案：**

1. 确保已安装系统依赖：
   \`\`\`bash

   # macOS

   brew install postgresql libpq

   # Ubuntu

   sudo apt-get install libpq-dev
   \`\`\`

2. 重试：`bundle install`

### 凭证问题

**错误：** `ActiveSupport::MessageEncryptor::InvalidMessage`

**解决方案：**
主密钥与凭证文件不匹配。可以：

1. 从其他团队成员处获取正确的 `config/master.key`
2. 或重新生成凭证：`rm config/credentials.yml.enc && bin/rails credentials:edit`

### Vite/Inertia 问题

**错误：** `Vite Ruby - Build failed`

**解决方案：**
\`\`\`bash

# 清除 Vite 缓存

rm -rf node_modules/.vite

# 重新安装 JS 依赖

rm -rf node_modules && yarn install
\`\`\`

### Solid Queue 问题

**错误：** 任务未处理

**解决方案：**
确保队列工作进程正在运行：
\`\`\`bash
bin/jobs

# 或

bin/rails solid_queue:start
\`\`\`
```

### 11. 贡献（可选）

如果是开源项目或团队项目，包含此部分。

### 12. 许可证（可选）

---

## 编写原则

1. **极其详尽** - 有疑问时，包含它。细节越多越好。

2. **大量使用代码块** - 每个命令都应可复制粘贴。

3. **展示示例输出** - 在有帮助时，展示用户应该看到的内容。

4. **解释原因** - 不要只说"运行此命令"，要解释它的作用。

5. **假设全新机器** - 像读者从未见过此代码库一样编写。

6. **使用表格作为参考** - 环境变量、脚本和选项非常适合用表格展示。

7. **保持命令最新** - 如果项目使用 `pnpm` 就用 `pnpm`，使用 `npm` 就用 `npm` 等。

8. **包含目录** - 对于超过约 200 行的 README，在顶部添加目录。

---

## 输出格式

生成完整的 README.md 文件，包含：

- 正确的 markdown 格式
- 带语言提示的代码块（`bash、`typescript 等）
- 适当位置的表格
- 清晰的章节层次
- 长文档的链接目录

将 README 直接写入项目根目录的 `README.md`。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停止并请求澄清。
