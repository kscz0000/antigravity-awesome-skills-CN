---
name: neon-postgres-branches
description: 选择并创建适合的 Neon 分支类型，用于测试和开发。当用户提到 Neon 分支、分支创建、迁移测试、真实数据迁移、隔离测试环境、仅模式分支、敏感数据处理、Neon CLI 分支或 Neon MCP 分支时使用。触发词：Neon分支、迁移测试、隔离测试环境、仅模式分支、敏感数据、Neon CLI、Neon MCP、分支创建。
risk: unknown
source: https://github.com/neondatabase/agent-skills/tree/main/skills/neon-postgres-branches
source_repo: neondatabase/agent-skills
source_type: official
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/neondatabase/agent-skills/blob/main/LICENSE
---

# Neon Postgres 分支管理
## 何时使用

当你需要为测试和开发选择并创建合适的 Neon 分支类型时使用此技能。当用户提到 Neon 分支、用真实数据做迁移测试、隔离测试环境、敏感数据的仅模式分支工作流，或通过 Neon CLI / Neon MCP 创建分支时触发。


此技能的输出应为一个已创建的 Neon 分支（若创建无法继续，则给出明确的下一步操作）。
先选择正确的分支类型，再通过 MCP 或 CLI 执行分支创建。

- **普通分支**——用于使用真实数据进行逼真的迁移和查询测试。
- **仅模式分支（Beta）**——用于需要表结构但不需要复制数据行的敏感数据工作流。

## 分支类型决策

首先使用此决策规则：

1. 如果用户需要针对类生产数据测试复杂迁移、性能或行为，选择**普通分支**。
2. 如果用户需要避免复制敏感数据，选择**仅模式分支**。

如果请求不明确，问一个澄清问题：
"你需要真实数据来测试，还是只需要表结构因为数据是敏感的？"

## 工具选择：CLI 还是 MCP

始终同时支持 Neon CLI 和 Neon MCP 服务器。优先使用用户已安装并认证的工具。

MCP 文档：https://neon.com/docs/ai/neon-mcp-server.md
CLI 文档：https://neon.com/docs/reference/cli-quickstart

### 选择顺序

1. 先在支持 MCP 的环境中检查 MCP：
   - 如果 Neon MCP 工具可用且已认证（例如列出项目成功），使用 MCP。
2. 如果 MCP 不可用或未认证，检查 CLI：
   - 运行 `neon --version` 确认 CLI 已安装。
   - 运行 `neon projects list` 确认认证/上下文。
3. 如果 CLI 未安装，引导用户通过快速入门安装。
4. 如果 CLI 已安装但未认证，引导用户执行 `neon auth`（或 API 密钥认证），然后继续。
5. 如果 MCP 和 CLI 都不可用，使用 Neon REST API：
   - https://neon.com/docs/guides/branching-neon-api.md

### MCP 分支流程

1. 根据数据敏感性和迁移测试目标选择普通分支或仅模式分支。
2. 使用分支工具（例如 `create_branch`）创建分支。
3. 用读取工具（例如 `describe_branch`）验证。
4. 对于迁移工作流，优先使用基于分支的迁移流程，再应用到主分支。

## 创建普通分支（真实数据迁移测试的首选）

当用户需要逼真的测试条件时使用此方式。
类生产的真实数据能暴露种子数据或迁移脚本遗漏的边界情况，有助于在上线前发现迁移问题。

文档：https://neon.com/docs/introduction/branching.md

### 步骤

1. 如果 MCP 已可用/已认证则使用 MCP；否则用 `neon --version` 验证 CLI。
2. 确保项目上下文已设置（`neon set-context --project-id <your-project-id>`）或在命令中包含 `--project-id`。
3. 创建分支：

```bash
neon branches create \
  --name <branch-name> \
  --parent <parent-branch-id-or-name> \
  --expires-at 2026-12-15T18:02:16Z
```

4. 可选：获取新分支的连接字符串：

```bash
neon connection-string <branch-name>
```

## 创建仅模式分支（Beta，敏感数据场景）

当用户不得将生产数据行复制到测试分支时使用此方式。

文档：https://neon.com/docs/guides/branching-schema-only.md

### 步骤

1. 如果 MCP 已可用/已认证则使用 MCP；否则用 `neon --version` 验证 CLI。
2. 创建仅模式分支：

```bash
neon branches create \
  --name <schema-only-branch-name> \
  --parent <parent-branch-id-or-name> \
  --schema-only \
  --expires-at 2026-12-15T18:02:16Z
```

如果存在多个项目，需包含：

```bash
neon branches create \
  --name <schema-only-branch-name> \
  --parent <parent-branch-id-or-name> \
  --schema-only \
  --project-id <your-project-id> \
  --expires-at 2026-12-15T18:02:16Z
```

### Beta 支持指引（必须遵守）

仅模式分支目前处于 Beta 阶段。如果用户报告了异常行为、错误或缺失的功能：

1. 请他们在 Neon 控制台分享反馈：
   - https://console.neon.tech/app/projects?modal=feedback
2. 建议在 Neon Discord 开启支持对话：
   - https://discord.gg/92vNTzKDGp

## 从父分支重置

当子分支已经偏移，用户想要从父分支的最新模式和数据做一次干净刷新时使用。

文档：https://neon.com/docs/guides/reset-from-parent.md

### 功能说明

- 用父分支的最新状态完全替换子分支的模式和数据。
- 不合并；子分支上的本地更改会丢失。
- 保持相同的连接信息，但重置期间活动连接会短暂中断。

### 何时推荐

- 开发或预发布分支落后生产环境太多。
- 用户想从与父分支对齐的干净状态开始新功能开发。
- 团队想从生产环境刷新预发布环境以保持一致的测试基准。

### 硬性约束和阻断条件

- 只有子分支可以重置（根分支和仅模式根分支无法从父分支重置）。
- 如果目标分支有子分支，必须先删除这些子分支才能执行重置。
- 父分支从快照恢复后，从父分支重置可能在最长 24 小时内不可用。
- 从父分支重置始终使用当前父分支状态；需要时间点恢复时请使用即时恢复（Instant restore）。

### CLI 用法

```bash
neon branches reset <id|name> --parent --preserve-under-name <backup-branch-name>
```

如果项目上下文尚未设置，需包含项目 ID：

```bash
neon branches reset <id|name> --parent --preserve-under-name <backup-branch-name> --project-id <project-id>
```

`--preserve-under-name` 将重置前的状态保留为备份分支以便回滚，但会增加一个后续需要清理的额外分支。

可选：设置上下文以避免重复 `--project-id`：

```bash
neon set-context --project-id <project-id>
```

### 控制台和 API 用法

- **控制台：** 打开目标子分支，然后从 **Actions** 中选择 **Reset from parent**。
- **API：** 对分支使用 restore 端点，并将 `source_branch_id` 设为父分支 ID。

## 注意事项

- 仅模式分支仅用于结构克隆和敏感/合规数据管控。
- 仅模式分支是独立的根分支（没有父分支，也没有共享历史），因此从父分支重置不适用。
- 依赖真实数据行形态、数据量和边界情况的迁移测试，优先使用普通分支。
- 根分支配额和每分支存储限制可能限制用户能创建的仅模式分支数量。
- 如果用户不确定，默认推荐：
  - **普通分支**——用于迁移验证。
  - **仅模式分支**——用于合规和隐私约束。

## 常用工作流模式

如果用户需要流程建议（而不只是单条命令），推荐以下模式：

- **每个 PR 一个分支：** PR 打开时创建分支，合并/关闭时删除，保持迁移测试隔离。
- **每次测试运行一个分支：** 流水线开始时创建分支，运行迁移/测试，结束时删除，确保 CI 确定性。
- **每个开发者一个分支：** 独立开发环境，数据形态与生产一致；避免团队在共享测试数据上冲突。
- **PII 感知分支：** 如果生产环境有敏感数据，从匿名化分支派生开发/PR 分支，或使用仅模式分支。
- **临时分支生命周期管理：** 设置分支过期时间并自动化清理，避免旧分支累积不必要的存储/历史成本。

### 创建后环境更新提示

分支创建后，询问用户是否需要更新本地环境凭据指向新分支。

- 问："需要我更新你的 `.env` 中的 `DATABASE_URL` 为新分支的连接字符串吗？"
- 如果是，将新分支连接字符串写入指定的环境文件/键。
- 如果否，保持凭据不变，将连接字符串提供给用户手动使用。
- 未经明确确认，绝不覆盖已有的环境变量键。

## Neon 基础设施即代码（`neon.ts`）

除了通过命令式方式创建分支（上面提到的 CLI / MCP / API），你还可以在 `neon.ts` 中**声明式地定义新分支的配置**——这是 Neon 的基础设施即代码文件（完整参考见 `neon` 技能）。`branch` 属性是一个以被评估分支为参数的函数，返回其设置，因此项目中诞生的每个分支都会获得一致的生命周期和计算配置，无需逐分支传参。

```bash
npm i @neon/config
```

```typescript
// neon.ts
import { defineConfig } from "@neon/config/v1";

export default defineConfig({
  branch: (branch) => {
    if (branch.exists) return {}; // never reconcile existing branches
    if (branch.isDefault) return { protected: true };
    if (branch.name.startsWith("preview/") || branch.name.startsWith("dev")) {
      return {
        parent: "main",
        ttl: "7d", // ephemeral: auto-expire 7 days after creation (max 30d)
        postgres: {
          computeSettings: {
            autoscalingLimitMinCu: 0.25, // scale to zero
            autoscalingLimitMaxCu: 1, // keep throwaway branches cheap
            suspendTimeout: "5m",
          },
        },
      };
    }
    return {};
  },
});
```

该闭包接收目标分支的只读描述符——`name`、`exists`、`isDefault`、`parentId` 等——并返回要应用的调优参数：`parent`、`ttl`（自动过期）、`protected` 和 `postgres.computeSettings`。这是上述**临时分支生命周期管理**和每 PR / 每测试模式的声明式补充：无需在每次 `neon branches create` 时记住 `--expires-at`，TTL 和计算配置存放在版本控制中并自动应用于每个匹配的分支。

由于 `neon checkout` 在**创建**分支时应用此策略，新的 `preview/*` 或 `dev-*` 分支一启动就已设置过期和缩放到零。检出已存在的分支不会调谐它——运行 `neon deploy`（即 `neon config apply` 的别名）以将变更应用到已存在的分支。

## CI/CD 中的分支使用

Neon 分支在 CI/CD 中的常见用途：

- **每个 PR 的预览部署：** PR 打开时创建分支，将预览部署到该分支，关闭时删除。每个 PR 获得独立的数据库分支。将分支的 `DATABASE_URL` 注入到部署的应用中取决于托管服务商——参见 [preview-branches-with-cloudflare](https://github.com/neondatabase/preview-branches-with-cloudflare)、[preview-branches-with-vercel](https://github.com/neondatabase/preview-branches-with-vercel) 或 [preview-branches-with-fly](https://github.com/neondatabase/preview-branches-with-fly) 中的已验证模式。
- **CI 中的迁移测试：** 在合并前针对拥有类生产数据的分支运行高风险模式变更。
- **模式差异可见性：** 使用 [schema-diff GitHub Action](https://github.com/marketplace/actions/neon-schema-diff-github-action) 在 PR 上自动评论数据库层差异。

## 示例

### 示例 1：使用真实数据进行迁移测试

**用户输入：** "我需要针对类生产数据测试一个高风险迁移。"

**智能体输出结构：**

1. 推荐普通分支并解释原因。
2. 提供文档链接：https://neon.com/docs/introduction/branching
3. 先检查可用/已认证的工具路径（MCP，否则用 `neon --version` 检查 CLI）。
4. 提供命令：
   - `neon branches create --name migration-test --parent main --expires-at 2026-12-15T18:02:16Z`
   - `neon connection-string migration-test`

### 示例 2：敏感数据开发工作流

**用户输入：** "出于合规原因我们不能复制生产数据。"

**智能体输出结构：**

1. 推荐仅模式分支并解释原因。
2. 提供文档链接：https://neon.com/docs/guides/branching-schema-only
3. 先检查可用/已认证的工具路径（MCP，否则用 `neon --version` 检查 CLI）。
4. 提供命令：
   - `neon branches create --name compliance-dev --parent main --schema-only --project-id <your-project-id> --expires-at 2026-12-15T18:02:16Z`
5. 提及 Beta 支持渠道：
   - https://console.neon.tech/app/projects?modal=feedback
   - https://discord.gg/92vNTzKDGp

## 延伸阅读

- https://neon.com/docs/guides/branch-expiration.md
- https://neon.com/docs/guides/neon-github-integration.md
- https://neon.com/docs/ai/neon-mcp-server.md
- https://neon.com/branching

## 限制

- 仅当任务明确匹配其上游产品或 API 范围时才使用此技能。
- 在执行变更前，务必对照当前官方文档验证命令、API 行为、定价、配额、凭据和部署影响。
- 不要将生成的示例替代针对具体环境的测试、安全审查，或用户对破坏性/高成本操作的审批。
