---
name: claude-settings-audit
description: 分析仓库并生成推荐的 Claude Code settings.json 权限配置。当用户要求设置新项目、审计现有设置或确定允许哪些只读 bash 命令时使用。检测技术栈、构建工具和 monorepo 结构。
risk: unknown
source: community
---

# Claude 设置审计

分析此仓库并生成推荐的 Claude Code `settings.json` 只读命令权限。

## 使用场景

- 你正在为仓库设置或审计 Claude Code `settings.json` 权限。
- 你需要从仓库的技术栈、工具和 monorepo 结构推断安全的只读允许列表。
- 你想审查或替换现有的 Claude 权限基线，改为基于证据的配置。

## 阶段 1：检测技术栈

运行以下命令检测仓库结构：

```bash
ls -la
find . -maxdepth 2 \( -name "*.toml" -o -name "*.json" -o -name "*.lock" -o -name "*.yaml" -o -name "*.yml" -o -name "Makefile" -o -name "Dockerfile" -o -name "*.tf" \) 2>/dev/null | head -50
```

检查以下指示文件：

| 类别         | 检查文件                                                                               |
| ------------ | -------------------------------------------------------------------------------------- |
| **Python**   | `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile`, `poetry.lock`, `uv.lock`  |
| **Node.js**  | `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`                     |
| **Go**       | `go.mod`, `go.sum`                                                                     |
| **Rust**     | `Cargo.toml`, `Cargo.lock`                                                             |
| **Ruby**     | `Gemfile`, `Gemfile.lock`                                                              |
| **Java**     | `pom.xml`, `build.gradle`, `build.gradle.kts`                                          |
| **构建**     | `Makefile`, `Dockerfile`, `docker-compose.yml`                                         |
| **基础设施** | `*.tf` 文件, `kubernetes/`, `helm/`                                                    |
| **Monorepo** | `lerna.json`, `nx.json`, `turbo.json`, `pnpm-workspace.yaml`                           |

## 阶段 2：检测服务

检查服务集成：

| 服务       | 检测方式                                                                         |
| ---------- | -------------------------------------------------------------------------------- |
| **Sentry** | 依赖中的 `sentry-sdk`，`@sentry/*` 包，`.sentryclirc`，`sentry.properties`      |
| **Linear** | Linear 配置文件，`.linear/` 目录                                                 |

读取依赖文件识别框架：

- `package.json` → 检查 `dependencies` 和 `devDependencies`
- `pyproject.toml` → 检查 `[project.dependencies]` 或 `[tool.poetry.dependencies]`
- `Gemfile` → 检查 gem 名称
- `Cargo.toml` → 检查 `[dependencies]`

## 阶段 3：检查现有设置

```bash
cat .claude/settings.json 2>/dev/null || echo "No existing settings"
```

## 阶段 4：生成建议

通过组合以下内容构建允许列表：

### 基线命令（始终包含）

```json
[
  "Bash(ls:*)",
  "Bash(pwd:*)",
  "Bash(find:*)",
  "Bash(file:*)",
  "Bash(stat:*)",
  "Bash(wc:*)",
  "Bash(head:*)",
  "Bash(tail:*)",
  "Bash(cat:*)",
  "Bash(tree:*)",
  "Bash(git status:*)",
  "Bash(git log:*)",
  "Bash(git diff:*)",
  "Bash(git show:*)",
  "Bash(git branch:*)",
  "Bash(git remote:*)",
  "Bash(git tag:*)",
  "Bash(git stash list:*)",
  "Bash(git rev-parse:*)",
  "Bash(gh pr view:*)",
  "Bash(gh pr list:*)",
  "Bash(gh pr checks:*)",
  "Bash(gh pr diff:*)",
  "Bash(gh issue view:*)",
  "Bash(gh issue list:*)",
  "Bash(gh run view:*)",
  "Bash(gh run list:*)",
  "Bash(gh run logs:*)",
  "Bash(gh repo view:*)",
  "Bash(gh api:*)"
]
```

### 技术栈特定命令

仅包含项目中实际检测到的工具命令。

#### Python（如果检测到 Python 文件或配置）

| 如果检测到                        | 添加这些命令                            |
| --------------------------------- | --------------------------------------- |
| 任意 Python                       | `python --version`, `python3 --version` |
| `poetry.lock`                     | `poetry show`, `poetry env info`        |
| `uv.lock`                         | `uv pip list`, `uv tree`                |
| `Pipfile.lock`                    | `pipenv graph`                          |
| `requirements.txt`（无其他锁文件）| `pip list`, `pip show`, `pip freeze`    |

#### Node.js（如果检测到 package.json）

| 如果检测到              | 添加这些命令                           |
| ----------------------- | -------------------------------------- |
| 任意 Node.js            | `node --version`                       |
| `pnpm-lock.yaml`        | `pnpm list`, `pnpm why`                |
| `yarn.lock`             | `yarn list`, `yarn info`, `yarn why`   |
| `package-lock.json`     | `npm list`, `npm view`, `npm outdated` |
| TypeScript（`tsconfig.json`）| `tsc --version`                   |

#### 其他语言

| 如果检测到    | 添加这些命令                                                         |
| ------------- | -------------------------------------------------------------------- |
| `go.mod`      | `go version`, `go list`, `go mod graph`, `go env`                    |
| `Cargo.toml`  | `rustc --version`, `cargo --version`, `cargo tree`, `cargo metadata` |
| `Gemfile`     | `ruby --version`, `bundle list`, `bundle show`                       |
| `pom.xml`     | `java --version`, `mvn --version`, `mvn dependency:tree`             |
| `build.gradle`| `java --version`, `gradle --version`, `gradle dependencies`          |

#### 构建工具

| 如果检测到          | 添加这些命令                                                         |
| ------------------- | -------------------------------------------------------------------- |
| `Dockerfile`        | `docker --version`, `docker ps`, `docker images`                     |
| `docker-compose.yml`| `docker-compose ps`, `docker-compose config`                         |
| `*.tf` 文件         | `terraform --version`, `terraform providers`, `terraform state list` |
| `Makefile`          | `make --version`, `make -n`                                          |

### 技能（用于 Sentry 项目）

如果是 Sentry 项目（或已安装 sentry-skills 插件），包含：

```json
[
  "Skill(sentry-skills:agents-md)",
  "Skill(sentry-skills:blog-writing-guide)",
  "Skill(sentry-skills:brand-guidelines)",
  "Skill(sentry-skills:claude-settings-audit)",
  "Skill(sentry-skills:code-review)",
  "Skill(sentry-skills:code-simplifier)",
  "Skill(sentry-skills:commit)",
  "Skill(sentry-skills:create-branch)",
  "Skill(sentry-skills:create-pr)",
  "Skill(sentry-skills:django-access-review)",
  "Skill(sentry-skills:django-perf-review)",
  "Skill(sentry-skills:doc-coauthoring)",
  "Skill(sentry-skills:find-bugs)",
  "Skill(sentry-skills:gh-review-requests)",
  "Skill(sentry-skills:gha-security-review)",
  "Skill(sentry-skills:iterate-pr)",
  "Skill(sentry-skills:pr-writer)",
  "Skill(sentry-skills:security-review)",
  "Skill(sentry-skills:skill-creator)",
  "Skill(sentry-skills:skill-scanner)",
  "Skill(sentry-skills:skill-writer)",
  "Skill(sentry-skills:sred-project-organizer)",
  "Skill(sentry-skills:sred-work-summary)"
]
```

### WebFetch 域名

#### 始终包含（Sentry 项目）

```json
[
  "WebFetch(domain:docs.sentry.io)",
  "WebFetch(domain:develop.sentry.dev)",
  "WebFetch(domain:docs.github.com)",
  "WebFetch(domain:cli.github.com)"
]
```

#### 框架特定

| 如果检测到    | 添加域名                                           |
| ------------- | -------------------------------------------------- |
| **Django**    | `docs.djangoproject.com`                           |
| **Flask**     | `flask.palletsprojects.com`                        |
| **FastAPI**   | `fastapi.tiangolo.com`                             |
| **React**     | `react.dev`                                        |
| **Next.js**   | `nextjs.org`                                       |
| **Vue**       | `vuejs.org`                                        |
| **Express**   | `expressjs.com`                                    |
| **Rails**     | `guides.rubyonrails.org`, `api.rubyonrails.org`    |
| **Go**        | `pkg.go.dev`                                       |
| **Rust**      | `docs.rs`, `doc.rust-lang.org`                     |
| **Docker**    | `docs.docker.com`                                  |
| **Kubernetes**| `kubernetes.io`                                    |
| **Terraform** | `registry.terraform.io`                            |

### MCP 服务器建议

MCP 服务器在 `.mcp.json` 中配置（而非 `settings.json`）。检查现有配置：

```bash
cat .mcp.json 2>/dev/null || echo "No existing .mcp.json"
```

#### Sentry MCP（如果检测到 Sentry SDK）

添加到 `.mcp.json`（将 `{org-slug}` 和 `{project-slug}` 替换为你的 Sentry 组织和项目标识）：

```json
{
  "mcpServers": {
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp/{org-slug}/{project-slug}"
    }
  }
}
```

#### Linear MCP（如果检测到 Linear 使用）

添加到 `.mcp.json`：

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": {
        "LINEAR_API_KEY": "${LINEAR_API_KEY}"
      }
    }
  }
}
```

**注意**：永远不要建议 GitHub MCP。GitHub 相关操作始终使用 `gh` CLI 命令。

## 输出格式

按以下方式呈现结果：

1. **摘要表格** - 检测到的内容
2. **推荐的 settings.json** - 完整的可复制 JSON
3. **MCP 建议** - 如适用
4. **合并说明** - 如果存在现有设置

示例输出结构：

```markdown
## 检测到的技术栈

| 类别           | 发现           |
| -------------- | -------------- |
| 语言           | Python 3.x     |
| 包管理器       | poetry         |
| 框架           | Django, Celery |
| 服务           | Sentry         |
| 构建工具       | Docker, Make   |

## 推荐的 .claude/settings.json

\`\`\`json
{
"permissions": {
"allow": [
// ... 按类别分组并带注释
],
"deny": []
}
}
\`\`\`

## 推荐的 .mcp.json（如适用）

如果你使用 Sentry 或 Linear，将 MCP 配置添加到 `.mcp.json`...
```

## 重要规则

### 应包含的内容

- 仅包含无法修改状态的只读命令
- 仅包含项目实际使用的工具（通过锁文件检测）
- 标准系统命令（ls、cat、find 等）
- `:*` 后缀允许基础命令接受任意参数

### 永远不要包含的内容

- **绝对路径** - 永远不要包含用户特定路径，如 `/home/user/scripts/foo` 或 `/Users/name/bin/bar`
- **自定义脚本** - 永远不要包含可能有副作用的项目脚本（如 `./scripts/deploy.sh`）
- **替代包管理器** - 如果项目使用 pnpm，不要包含 npm/yarn 命令
- **修改状态的命令** - 不包含 install、build、run、write 或 delete 命令

### 包管理器规则

仅包含项目实际使用的包管理器：

| 如果检测到         | 包含           | 不要包含                               |
| ------------------ | -------------- | -------------------------------------- |
| `pnpm-lock.yaml`   | pnpm 命令      | npm, yarn                              |
| `yarn.lock`        | yarn 命令      | npm, pnpm                              |
| `package-lock.json`| npm 命令       | yarn, pnpm                             |
| `poetry.lock`      | poetry 命令    | pip（除非同时有 requirements.txt）      |
| `uv.lock`          | uv 命令        | pip, poetry                            |
| `Pipfile.lock`     | pipenv 命令    | pip, poetry                            |

如果存在多个锁文件，仅包含每个检测到的管理器的命令。

## 限制

- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
