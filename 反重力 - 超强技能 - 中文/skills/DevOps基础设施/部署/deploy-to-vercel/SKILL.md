---
name: deploy-to-vercel
description: "部署应用程序和网站到 Vercel。当用户请求部署操作时使用，例如「部署我的应用」、「部署并把链接给我」、「把这个上线」或「创建预览部署」。触发词：部署到 Vercel、deploy my app、push this live、create a preview deployment、Vercel 部署、部署网站。"
risk: safe
source: "https://github.com/vercel-labs/agent-skills"
date_added: "2026-06-02"
---

# 部署到 Vercel

将任何项目部署到 Vercel。**始终以预览方式部署**（而非生产环境），除非用户明确要求生产部署。

目标是把用户带入最佳长期配置：项目链接到 Vercel 并通过 git push 部署。下面的每种方法都试图让用户更接近这个状态。

## 适用场景
- 任务与以下描述匹配时使用本技能：将应用程序和网站部署到 Vercel。当用户请求部署操作（如「部署我的应用」、「部署并把链接给我」、「把这个上线」或「创建预览部署」）时使用。

## 步骤 1：收集项目状态

在决定使用哪种方法之前，运行所有四项检查：

```bash
# 1. 检查 git remote
git remote get-url origin 2>/dev/null

# 2. 检查是否本地链接到 Vercel 项目（任一文件存在即表示已链接）
cat .vercel/project.json 2>/dev/null || cat .vercel/repo.json 2>/dev/null

# 3. 检查 Vercel CLI 是否已安装并已认证
vercel whoami 2>/dev/null

# 4. 列出可用的团队（如果已认证）
vercel teams list --format json 2>/dev/null
```

### 团队选择

如果用户属于多个团队，将所有可用的团队 slug 以列表形式呈现，询问要部署到哪一个。用户选定团队后，立即进入下一步——不要再次确认。

在所有后续 CLI 命令中通过 `--scope` 传入团队 slug（`vercel deploy`、`vercel link`、`vercel inspect` 等）：

```bash
vercel deploy [path] -y --no-wait --scope <team-slug>
```

如果项目已链接（存在 `.vercel/project.json` 或 `.vercel/repo.json`），则这些文件中的 `orgId` 决定了团队——无需再次询问。如果只有一个团队（或仅个人账户），跳过提示直接使用。

**关于 `.vercel/` 目录：** 已链接的项目有以下任一文件：
- `.vercel/project.json` — 由 `vercel link` 创建（单项目链接）。包含 `projectId` 和 `orgId`。
- `.vercel/repo.json` — 由 `vercel link --repo` 创建（基于仓库的链接）。包含 `orgId`、`remoteName`，以及一个将目录映射到 Vercel 项目 ID 的 `projects` 数组。

任一文件存在即表示项目已链接。需要同时检查两者。

**不要**在未链接的目录中使用 `vercel project inspect`、`vercel ls` 或 `vercel link` 来检测状态——没有 `.vercel/` 配置时，它们会以交互方式提示（或在 `--yes` 下静默链接作为副作用）。只有 `vercel whoami` 在任何地方都安全运行。

## 步骤 2：选择部署方法

### 已链接（`.vercel/` 存在）+ 有 git remote → Git Push

这是理想状态。项目已链接并集成了 git。

1. **推送前询问用户。** 未经明确批准不得推送：
   ```
   此项目通过 git 连接到 Vercel。我可以提交并推送以触发部署。是否继续？
   ```

2. **提交并推送：**
   ```bash
   git add .
   git commit -m "deploy: <变更说明>"
   git push
   ```
   Vercel 自动从推送构建。非生产分支获得预览部署；生产分支（通常是 `main`）获得生产部署。

3. **获取预览 URL。** 如果 CLI 已认证：
   ```bash
   sleep 5
   vercel ls --format json
   ```
   JSON 输出包含一个 `deployments` 数组。找到最新条目——其 `url` 字段即为预览 URL。

   如果 CLI 未认证，告知用户去 Vercel 仪表板或 git 提供商的提交状态检查中查看预览 URL。

---

### 已链接（`.vercel/` 存在）+ 无 git remote → `vercel deploy`

项目已链接但没有 git 仓库。直接用 CLI 部署。

```bash
vercel deploy [path] -y --no-wait
```

使用 `--no-wait` 让 CLI 立即返回部署 URL，而不是阻塞等待构建完成（构建可能需要一些时间）。然后用以下命令检查部署状态：

```bash
vercel inspect <deployment-url>
```

生产部署（仅当用户明确要求时）：
```bash
vercel deploy [path] --prod -y --no-wait
```

---

### 未链接 + CLI 已认证 → 先链接，再部署

CLI 可用但项目尚未链接。这是把用户带入最佳状态的契机。

1. **询问用户要部署到哪个团队。** 以列表形式呈现步骤 1 中的团队 slug。如果只有一个团队（或仅个人账户），跳过此步。

2. **选定团队后，直接进入链接流程。** 告诉用户将会发生什么，但不要请求单独确认：
   ```
   正在将此项目链接到 Vercel 上的 <team name>。这将创建一个用于部署的 Vercel 项目，并启用未来 git 推送的自动部署。
   ```

3. **如果存在 git remote**，使用基于仓库的链接并指定团队范围：
   ```bash
   vercel link --repo --scope <team-slug>
   ```
   这会读取 git remote URL，并将其与从该仓库部署的现有 Vercel 项目匹配。它会创建 `.vercel/repo.json`。这比不带 `--repo` 的 `vercel link` 可靠得多，后者按目录名匹配，在本地文件夹和 Vercel 项目名称不一致时常常失败。

   **如果没有 git remote**，回退到标准链接：
   ```bash
   vercel link --scope <team-slug>
   ```
   这会提示用户选择或创建一个项目。它会创建 `.vercel/project.json`。

4. **然后用最佳可用方法部署：**
   - 如果存在 git remote → 提交并推送（见上文的 git push 方法）
   - 如果没有 git remote → `vercel deploy [path] -y --no-wait --scope <team-slug>`，然后用 `vercel inspect <url>` 检查状态

---

### 未链接 + CLI 未认证 → 安装、认证、链接、部署

Vercel CLI 完全未配置。

1. **安装 CLI（如果尚未安装）：**
   ```bash
   npm install -g vercel
   ```

2. **认证：**
   ```bash
   vercel login
   ```
   用户在浏览器中完成认证。如果在无法登录的非交互式环境中运行，跳到下面的 **无认证回退**。

3. **询问要部署到哪个团队**——以列表形式呈现 `vercel teams list --format json` 中的团队 slug。如果只有一个团队或个人账户，跳过。选定后立即继续。

4. **链接项目**，并指定所选团队范围（如果存在 git remote 则用 `--repo`，否则用普通的 `vercel link`）：
   ```bash
   vercel link --repo --scope <team-slug>   # 如果存在 git remote
   vercel link --scope <team-slug>          # 如果没有 git remote
   ```

5. **使用最佳可用方法部署**（如果存在 remote 则用 git push，否则用 `vercel deploy -y --no-wait --scope <team-slug>`，然后用 `vercel inspect <url>` 检查状态）。

---

### 无认证回退 — claude.ai 沙箱

**适用场景：** 最后手段——当 CLI 在 claude.ai 沙箱中无法安装或认证时使用。这不需要认证——会返回 **Preview URL**（线上站点）和 **Claim URL**（转移到你的 Vercel 账户）。

```bash
bash /mnt/skills/user/deploy-to-vercel/resources/deploy.sh [path]
```

**参数：**
- `path` - 要部署的目录，或一个 `.tgz` 文件（默认为当前目录）

**示例：**
```bash
# 部署当前目录
bash /mnt/skills/user/deploy-to-vercel/resources/deploy.sh

# 部署指定项目
bash /mnt/skills/user/deploy-to-vercel/resources/deploy.sh /path/to/project

# 部署已有的 tarball
bash /mnt/skills/user/deploy-to-vercel/resources/deploy.sh /path/to/project.tgz
```

脚本自动从 `package.json` 检测框架，打包项目（排除 `node_modules`、`.git`、`.env`），上传并等待构建完成。

**告诉用户：** "你的部署已就绪，访问 [previewUrl]。前往 [claimUrl] 将其认领到你的 Vercel 账户进行管理。"

---

### 无认证回退 — Codex 沙箱

**适用场景：** 在 Codex 沙箱中 CLI 可能未认证。Codex 默认在沙箱环境中运行——先尝试 CLI，认证失败时回退到部署脚本。

1. **检查 Vercel CLI 是否已安装**（此检查无需提权）：
   ```bash
   command -v vercel
   ```

2. **如果已安装 `vercel`**，尝试用 CLI 部署：
   ```bash
   vercel deploy [path] -y --no-wait
   ```

3. **如果未安装 `vercel`，或 CLI 报 "No existing credentials found"**，使用回退脚本：
   ```bash
   skill_dir="<path-to-skill>"

   # 部署当前目录
   bash "$skill_dir/resources/deploy-codex.sh"

   # 部署指定项目
   bash "$skill_dir/resources/deploy-codex.sh" /path/to/project

   # 部署已有的 tarball
   bash "$skill_dir/resources/deploy-codex.sh" /path/to/project.tgz
   ```

脚本处理框架检测、打包和部署。它会等待构建完成并返回包含 `previewUrl` 和 `claimUrl` 的 JSON。

**告诉用户：** "你的部署已就绪，访问 [previewUrl]。前往 [claimUrl] 将其认领到你的 Vercel 账户进行管理。"

**提权网络访问：** 仅当沙箱阻止网络调用（`sandbox_permissions=require_escalated`）时才为实际的部署命令提权。**不要**为 `command -v vercel` 检查提权。

---

## 智能体特定说明

### Claude Code / 基于终端的智能体

你拥有完整的 shell 访问权限。不要使用 `/mnt/skills/` 路径。直接按上面的决策流程使用 CLI。

对于无认证回退，从技能的安装位置运行部署脚本：
```bash
bash ~/.claude/skills/deploy-to-vercel/resources/deploy.sh [path]
```
路径可能因用户安装技能的位置而异。

### 沙箱环境（claude.ai）

你可能无法运行 `vercel login` 或 `git push`。直接进入 **无认证回退 — claude.ai 沙箱**。

### Codex

Codex 在沙箱中运行。先检查 CLI 是否可用，然后回退到部署脚本。进入 **无认证回退 — Codex 沙箱**。

---

## 输出

始终向用户展示部署 URL。

- **Git push：** 使用 `vercel ls --format json` 查找预览 URL。如果 CLI 未认证，告知用户去 Vercel 仪表板或提交状态检查查看。
- **CLI 部署：** 显示 `vercel deploy --no-wait` 返回的 URL。使用 `vercel inspect <url>` 检查构建状态并向用户报告。
- **无认证回退：** 同时显示预览 URL 和认领 URL：
  ```
  部署成功！

  Preview URL: https://my-app-abc123.vercel.app
  Claim URL:   https://vercel.com/claim-deployment?code=...

  在 Preview URL 查看你的站点。
  要将此部署转移到你的 Vercel 账户，请访问 Claim URL。
  ```

**不要**用 curl 或 fetch 访问已部署的 URL 来验证它是否工作。直接返回链接即可。

---

## 故障排查

### 网络出口错误（claude.ai）

如果因 claude.ai 的网络限制导致部署失败，告知用户：

```
部署因网络限制失败。修复方法：

1. 访问 https://claude.ai/settings/capabilities
2. 将 *.vercel.com 添加到允许的域名
3. 重新尝试部署
```

### 提权网络访问（Codex / 沙箱环境）

如果沙箱环境中因网络问题（超时、DNS 错误、连接重置）导致部署失败，使用提权权限重新运行（`sandbox_permissions=require_escalated`）。不要为初始的 CLI 可用性检查提权——只为实际的部署命令提权。

给用户的示例指引：
```
部署到 Vercel 需要提权的网络访问。我可以用提权权限重新运行该命令——是否继续？
```

### CLI 认证失败

如果 `vercel login` 或 `vercel deploy` 报认证错误，回退到无认证部署脚本（根据环境选择 claude.ai 或 Codex 版本）。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，应停止并请求澄清。
