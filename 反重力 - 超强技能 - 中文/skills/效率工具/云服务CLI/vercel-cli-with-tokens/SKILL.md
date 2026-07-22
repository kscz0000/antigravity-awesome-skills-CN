---
name: vercel-cli-with-tokens
description: "使用基于令牌的身份认证在 Vercel 上部署和管理项目。涉及使用访问令牌（而非交互式登录）操作 Vercel CLI 时使用——例如"部署到 vercel"、"设置 vercel"、"添加环境变量到 vercel"。触发词：Vercel CLI、令牌认证、部署到 Vercel、Vercel 访问令牌、vercel login、无交互登录、部署预览、Vercel 环境变量、Vercel 团队、Vercel 项目链接。"
risk: safe
source: "https://github.com/vercel-labs/agent-skills"
date_added: "2026-06-02"
---

# Vercel CLI 与令牌

使用 CLI 与基于令牌的身份认证在 Vercel 上部署和管理项目，无需依赖 `vercel login`。

## 适用场景
- 任务匹配此描述时使用此技能：使用基于令牌的身份认证在 Vercel 上部署和管理项目。涉及使用访问令牌（而非交互式登录）操作 Vercel CLI 时使用——例如"部署到 vercel"、"设置 vercel"、"添加环境变量到 vercel"。

## 步骤 1：定位 Vercel 令牌

运行任何 Vercel CLI 命令之前，先确认令牌的来源。按顺序排查以下场景：

### A) `VERCEL_TOKEN` 已在环境中设置

```bash
[ -n "${VERCEL_TOKEN:-}" ] && printf 'VERCEL_TOKEN is set\n'
```

如果该命令报告令牌已配置，则可以直接使用。跳到步骤 2。

### B) 令牌在 `.env` 文件中的 `VERCEL_TOKEN` 下

```bash
grep -q '^VERCEL_TOKEN=' .env 2>/dev/null && printf 'VERCEL_TOKEN is present in .env\n'
```

如果找到，将其导出：

```bash
VERCEL_TOKEN="$(sed -n 's/^VERCEL_TOKEN=//p' .env | tail -n 1)"
export VERCEL_TOKEN
```

### C) 令牌在 `.env` 文件中但变量名不同

查找任何看起来像 Vercel 令牌的变量（Vercel 令牌通常以 `vca_` 开头）：

```bash
grep -Eio '^[A-Z0-9_]*VERCEL[A-Z0-9_]*(?==)' .env 2>/dev/null
```

查看输出以确定哪个变量持有令牌，然后将其导出为 `VERCEL_TOKEN`：

```bash
vercel_var="<VARIABLE_NAME>"
VERCEL_TOKEN="$(sed -n "s/^${vercel_var}=//p" .env | tail -n 1)"
export VERCEL_TOKEN
```

### D) 未找到令牌 —— 询问用户

如果以上方法都未找到令牌，请让用户提供。他们可以在 vercel.com/account/tokens 创建 Vercel 访问令牌。

---

**重要：** 将 `VERCEL_TOKEN` 导出为环境变量后，Vercel CLI 会自动读取它 —— **不要将其作为 `--token` 参数传递**。将密钥放在命令行参数中会将其暴露在 shell 历史记录和进程列表中。

```bash
# Bad — token visible in shell history and process listings
vercel deploy --token "vca_abc123"

# Good — CLI reads VERCEL_TOKEN from the environment
[ -n "${VERCEL_TOKEN:-}" ] || { echo "Set VERCEL_TOKEN first" >&2; exit 1; }
vercel deploy
```

## 步骤 2：定位项目和团队

类似地，检查项目 ID 和团队作用域。这让 CLI 能够定位正确的项目，无需运行 `vercel link`。

```bash
# Check environment
[ -n "${VERCEL_PROJECT_ID:-}" ] && printf 'VERCEL_PROJECT_ID is set\n'
[ -n "${VERCEL_ORG_ID:-}" ] && printf 'VERCEL_ORG_ID is set\n'

# Or check .env
grep -Eio '^[A-Z0-9_]*VERCEL[A-Z0-9_]*(?==)' .env 2>/dev/null
```

**如果你有项目 URL**（例如 `https://vercel.com/my-team/my-project`），从中提取团队 slug：

```bash
# e.g. "my-team" from "https://vercel.com/my-team/my-project"
echo "$PROJECT_URL" | sed 's|https://vercel.com/||' | cut -d/ -f1
```

**如果环境中同时有 `VERCEL_ORG_ID` 和 `VERCEL_PROJECT_ID`**，将它们导出 —— CLI 会自动使用它们并跳过任何 `.vercel/` 目录：

```bash
export VERCEL_ORG_ID="<org-id>"
export VERCEL_PROJECT_ID="<project-id>"
```

注意：`VERCEL_ORG_ID` 和 `VERCEL_PROJECT_ID` 必须一起设置 —— 只设置其中一个会导致错误。

## CLI 安装

确保 Vercel CLI 已安装并为最新版本：

```bash
npm install -g vercel
vercel --version
```

## 部署项目

除非用户明确要求部署到生产环境，否则始终部署为 **预览（preview）**。根据可用资源选择合适的方式。

### 快速部署（已有项目 ID —— 无需 link）

当环境中已设置 `VERCEL_TOKEN` 和 `VERCEL_PROJECT_ID` 时，直接部署：

```bash
vercel deploy -y --no-wait
```

使用团队作用域（通过 `VERCEL_ORG_ID` 或 `--scope`）：

```bash
vercel deploy --scope <team-slug> -y --no-wait
```

部署到生产环境（仅在明确要求时）：

```bash
vercel deploy --prod --scope <team-slug> -y --no-wait
```

检查部署状态：

```bash
vercel inspect <deployment-url>
```

### 完整部署流程（无项目 ID —— 需要 link）

当你有令牌和团队但没有预先存在的项目 ID 时使用此流程。

#### 首先检查项目状态

```bash
# Does the project have a git remote?
git remote get-url origin 2>/dev/null

# Is it already linked to a Vercel project?
cat .vercel/project.json 2>/dev/null || cat .vercel/repo.json 2>/dev/null
```

#### 链接项目

**有 git remote（推荐）：**

```bash
vercel link --repo --scope <team-slug> -y
```

读取 git remote 并连接至匹配的 Vercel 项目。会创建 `.vercel/repo.json`。比普通的 `vercel link` 更可靠，因为后者按目录名匹配。

**没有 git remote：**

```bash
vercel link --scope <team-slug> -y
```

会创建 `.vercel/project.json`。

**按名称链接到特定项目：**

```bash
vercel link --project <project-name> --scope <team-slug> -y
```

如果项目已经链接，检查 `.vercel/project.json` 或 `.vercel/repo.json` 中的 `orgId`，确认它与目标团队一致。

#### 链接后部署

**A) Git Push 部署 —— 有 git remote（推荐）**

Git 推送会触发 Vercel 自动部署。

1. **推送前先询问用户。** 未经明确批准，绝不推送。
2. 提交并推送：
   ```bash
   git add .
   git commit -m "deploy: <description of changes>"
   git push
   ```
3. Vercel 自动构建。非生产分支会获得预览部署。
4. 获取部署 URL：
   ```bash
   sleep 5
   vercel ls --format json --scope <team-slug>
   ```
   在 `deployments` 数组中找最新一条记录。

**B) CLI 部署 —— 没有 git remote**

```bash
vercel deploy --scope <team-slug> -y --no-wait
```

检查部署状态：

```bash
vercel inspect <deployment-url>
```

### 从远程仓库部署（代码未在本地克隆）

1. 克隆仓库：
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```
2. 链接到 Vercel：
   ```bash
   vercel link --repo --scope <team-slug> -y
   ```
3. 通过 git push 部署（如果有推送权限）或 CLI 部署。

### 关于 `.vercel/` 目录

已链接的项目会包含以下之一：
- `.vercel/project.json` —— 由 `vercel link` 创建。包含 `projectId` 和 `orgId`。
- `.vercel/repo.json` —— 由 `vercel link --repo` 创建。包含 `orgId`、`remoteName` 和一个 `projects` 映射。

当环境中同时设置了 `VERCEL_ORG_ID` + `VERCEL_PROJECT_ID` 时不需要该目录。

**不要**在未链接的目录中运行 `vercel project inspect` 或 `vercel link` 来检测状态 —— 它们会交互式提示或产生意外的链接副作用。`vercel ls` 是安全的（在未链接目录中默认显示该作用域下的所有部署）。`vercel whoami` 在任何位置都是安全的。

## 管理环境变量

```bash
# Set for all environments
echo "value" | vercel env add VAR_NAME --scope <team-slug>

# Set for a specific environment (production, preview, development)
echo "value" | vercel env add VAR_NAME production --scope <team-slug>

# List environment variables
vercel env ls --scope <team-slug>

# Pull env vars to local .env.local file
vercel env pull --scope <team-slug>

# Remove a variable
vercel env rm VAR_NAME --scope <team-slug> -y
```

## 检查部署

```bash
# List recent deployments
vercel ls --format json --scope <team-slug>

# Inspect a specific deployment
vercel inspect <deployment-url>

# View build logs (requires Vercel CLI v35+)
vercel inspect <deployment-url> --logs

# View runtime request logs (follows live by default; add --no-follow for a one-shot snapshot)
vercel logs <deployment-url>
```

## 管理域名

```bash
# List domains
vercel domains ls --scope <team-slug>

# Add a domain to the project — linked or env-linked directory (1 arg)
vercel domains add <domain> --scope <team-slug>

# Add a domain — unlinked directory (requires <project> positional)
vercel domains add <domain> <project> --scope <team-slug>
```

## Stripe 项目套餐变更

如果该项目由 Stripe Projects 管理。**运行任何付费或破坏性的套餐变更前请先询问用户** —— 升级会向真实信用卡计费，降级会移除席位。

首先运行 `stripe projects status --json` 确认 Vercel 资源的本地名称。下面的示例假设默认名称（`vercel-plan`）；如果在 `stripe projects add` 时被重命名，请替换为实际名称。

- **升级到 Pro：** `stripe projects add vercel/pro`（或 `stripe projects upgrade vercel-plan pro`）
- **降级到 Hobby：** `stripe projects downgrade vercel-plan hobby`

### Pro 套餐内容

- 每月 $20 平台费，包含每月 $20 的使用额度。
- 新项目默认使用 Turbo 构建机器（30 vCPUs，60 GB 内存）—— 比 Hobby 构建速度显著更快。
- 1 个部署席位 + 无限免费 Viewer 席位（只读协作者、预览评论）。
- 更高的包含配额（每月 1 TB 快速数据传输、1000 万次 Edge 请求）。
- 可用付费附加项：SAML SSO、HIPAA BAA、Flags Explorer、Observability Plus、Speed Insights、Web Analytics Plus。

完整详情：https://vercel.com/docs/plans/pro-plan

## 工作约定

- **绝不将 `VERCEL_TOKEN` 作为 `--token` 参数传递。** 将其导出为环境变量，让 CLI 自动读取。
- **询问用户之前先检查环境中的令牌。** 先查看当前环境和 `.env` 文件。
- **默认部署为预览版本。** 仅在明确要求时部署到生产环境。
- **推送到 git 之前先询问。** 未经用户批准，绝不推送提交。
- **不要直接修改 `.vercel/` 文件。** 该目录由 CLI 管理。读取它们（例如验证 `orgId`）是可以的。
- **不要 curl/fetch 已部署的 URL 来验证。** 直接将链接返回给用户即可。
- **需要结构化输出以便后续处理时，使用 `--format json`。**
- **会提示确认的命令使用 `-y`**，避免交互式阻塞。

## 故障排查

### 找不到令牌

检查环境和任何存在的 `.env` 文件：

```bash
env | grep -Eio '^[A-Z0-9_]*VERCEL[A-Z0-9_]*(?==)'
grep -Eio '^[A-Z0-9_]*VERCEL[A-Z0-9_]*(?==)' .env 2>/dev/null
```

### 认证错误

如果 CLI 报 `Authentication required`：
- 令牌可能已过期或无效。
- 验证：`vercel whoami`（使用环境中的 `VERCEL_TOKEN`）。
- 向用户索取新的令牌。

### 错误的团队

验证作用域是否正确：

```bash
vercel whoami --scope <team-slug>
```

### 构建失败

查看构建日志：

```bash
vercel inspect <deployment-url> --logs
```

常见原因：
- 缺少依赖 —— 确保 `package.json` 完整并已提交。
- 缺少环境变量 —— 使用 `vercel env add` 添加。
- 框架配置错误 —— 检查 `vercel.json`。Vercel 会从 `package.json` 自动检测框架（Next.js、Remix、Vite 等）；如果检测有误，可通过 `vercel.json` 覆盖。

### 未安装 CLI

```bash
npm install -g vercel
```

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将其输出作为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来并询问澄清。
