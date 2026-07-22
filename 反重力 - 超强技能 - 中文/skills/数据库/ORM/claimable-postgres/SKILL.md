---
name: claimable-postgres
description: 通过 Neon 的 Claimable Postgres (pg.new) 快速配置临时 Postgres 数据库。无需登录或信用卡。当用户要求快速配置 Postgres 环境、获取临时 DATABASE_URL 用于原型开发时使用。
risk: unknown
source: community
---

# Claimable Postgres

用于本地开发、演示、原型开发和测试环境的即时 Postgres 数据库。无需账户。数据库在 72 小时后过期，除非认领到 Neon 账户。

## 快速开始

```bash
curl -s -X POST "https://pg.new/api/v1/database" \
  -H "Content-Type: application/json" \
  -d '{"ref": "agent-skills"}'
```

从 JSON 响应中解析 `connection_string` 和 `claim_url`。将 `connection_string` 写入项目的 `.env` 文件作为 `DATABASE_URL`。

其他方法（CLI、SDK、Vite 插件）请参见下方的[选择哪种方法？](#选择哪种方法)。

## 选择哪种方法？

- **REST API**：返回结构化 JSON。除 `curl` 外无需其他运行时依赖。当智能体需要可预测的输出和错误处理时首选。
- **CLI**（`npx get-db@latest --yes`）：一条命令完成配置并写入 `.env`。当 Node.js 可用且用户希望简单设置时很方便。
- **SDK**（`get-db/sdk`）：在 Node.js 中进行脚本化或编程式配置。
- **Vite 插件**（`vite-plugin-db`）：如果 `DATABASE_URL` 缺失，在 `vite dev` 时自动配置。当用户有 Vite 项目时使用。
- **浏览器**：用户无法运行 CLI 或 API。引导用户访问 https://pg.new。

## REST API

**Base URL:** `https://pg.new/api/v1`

### 创建数据库

```bash
curl -s -X POST "https://pg.new/api/v1/database" \
  -H "Content-Type: application/json" \
  -d '{"ref": "agent-skills"}'
```

| 参数 | 必填 | 说明 |
|-----------|----------|-------------|
| `ref` | 是 | 追踪标签，用于标识谁配置了数据库。通过此技能配置时使用 `"agent-skills"`。 |
| `enable_logical_replication` | 否 | 启用逻辑复制（默认：false，启用后无法禁用） |

API 返回的 `connection_string` 是连接池连接 URL。对于直接（非池化）连接（如 Prisma 迁移），从主机名中移除 `-pooler`。CLI 会自动写入池化和直接两种 URL。

**响应：**

```json
{
  "id": "019beb39-37fb-709d-87ac-7ad6198b89f7",
  "status": "UNCLAIMED",
  "neon_project_id": "gentle-scene-06438508",
  "connection_string": "postgresql://...",
  "claim_url": "https://pg.new/claim/019beb39-...",
  "expires_at": "2026-01-26T14:19:14.580Z",
  "created_at": "2026-01-23T14:19:14.580Z",
  "updated_at": "2026-01-23T14:19:14.580Z"
}
```

### 检查状态

```bash
curl -s "https://pg.new/api/v1/database/{id}"
```

返回相同的响应结构。状态转换：`UNCLAIMED` -> `CLAIMING` -> `CLAIMED`。数据库被认领后，`connection_string` 返回 `null`。

### 错误响应

| 条件 | HTTP | 消息 |
|-----------|------|---------|
| `ref` 缺失或为空 | 400 | `Missing referrer` |
| 无效的数据库 ID | 400 | `Database not found` |
| 无效的 JSON 请求体 | 500 | `Failed to create the database.` |

## CLI

```bash
npx get-db@latest --yes
```

一步完成数据库配置并将连接字符串写入 `.env`。始终使用 `@latest` 和 `--yes`（跳过会导致智能体停滞的交互式提示）。

### 运行前检查

检查目标 `.env` 中是否已存在 `DATABASE_URL`（或选定的键名）。如果 CLI 发现该键存在，将退出而不进行配置。

如果键已存在，向用户提供三个选项：

1. 删除或注释掉现有行，然后重新运行。
2. 使用 `--env` 写入不同文件（如 `--env .env.local`）。
3. 使用 `--key` 以不同的变量名写入。

继续之前需获得确认。

### 选项

| 选项 | 别名 | 说明 | 默认值 |
|--------|-------|-------------|---------|
| `--yes` | `-y` | 跳过提示，使用默认值 | `false` |
| `--env` | `-e` | .env 文件路径 | `./.env` |
| `--key` | `-k` | 连接字符串环境变量键名 | `DATABASE_URL` |
| `--prefix` | `-p` | 生成的公共环境变量前缀 | `PUBLIC_` |
| `--seed` | `-s` | 种子 SQL 文件路径 | 无 |
| `--logical-replication` | `-L` | 启用逻辑复制 | `false` |
| `--ref` | `-r` | 引用者 id（通过此技能配置时使用 `agent-skills`） | 无 |

替代包管理器：`yarn dlx get-db@latest`、`pnpm dlx get-db@latest`、`bunx get-db@latest`、`deno run -A get-db@latest`。

### 输出

CLI 写入目标 `.env`：

```
DATABASE_URL=postgresql://...              # 池化（用于应用查询）
DATABASE_URL_DIRECT=postgresql://...       # 直接（用于迁移，如 Prisma）
PUBLIC_POSTGRES_CLAIM_URL=https://pg.new/claim/...
```

## SDK

用于脚本和编程式配置流程。

```typescript
import { instantPostgres } from 'get-db';

const { databaseUrl, databaseUrlDirect, claimUrl, claimExpiresAt } = await instantPostgres({
  referrer: 'agent-skills',
  seed: { type: 'sql-script', path: './init.sql' },
});
```

返回 `databaseUrl`（池化）、`databaseUrlDirect`（直接，用于迁移）、`claimUrl` 和 `claimExpiresAt`（Date 对象）。`referrer` 参数为必填。

## Vite 插件

对于 Vite 项目，如果 `DATABASE_URL` 缺失，`vite-plugin-db` 会在 `vite dev` 时自动配置数据库。使用 `npm install -D vite-plugin-db` 安装。配置请参见 [Claimable Postgres 文档](https://neon.com/docs/reference/claimable-postgres#vite-plugin)。

## 智能体工作流

### API 路径

1. **确认意图：** 如果请求模糊，确认用户需要临时的、无需注册的数据库。如果用户明确要求快速或临时数据库，则跳过此步。
2. **配置：** POST 请求 `https://pg.new/api/v1/database`，携带 `{"ref": "agent-skills"}`。
3. **解析响应：** 从 JSON 响应中提取 `connection_string`、`claim_url` 和 `expires_at`。
4. **写入 .env：** 将 `DATABASE_URL=<connection_string>` 写入项目的 `.env`（或用户指定的文件和键名）。未经确认不要覆盖现有键。
5. **种子数据（如需要）：** 如果用户有种子 SQL 文件，对新数据库运行：
   ```bash
   psql "$DATABASE_URL" -f seed.sql
   ```
6. **报告：** 告知用户连接字符串写入位置、使用的键名，并分享认领 URL。提醒：数据库现在可用；72 小时内认领以永久保留。
7. **可选：** 提供快速连接测试（如 `SELECT 1`）。

### CLI 路径

1. **检查 .env：** 检查目标 `.env` 是否已有 `DATABASE_URL`（或选定的键名）。如果存在，不要运行。提供删除、`--env` 或 `--key` 选项并获得确认。
2. **确认意图：** 如果请求模糊，确认用户需要临时的、无需注册的数据库。如果用户明确要求快速或临时数据库，则跳过此步。
3. **收集选项：** 使用默认值，除非上下文另有提示（如用户提到自定义 env 文件、种子 SQL 或逻辑复制）。
4. **运行：** 使用 `@latest --yes` 加上确认的选项执行。始终使用 `@latest` 避免缓存过期版本。`--yes` 跳过会导致智能体停滞的交互式提示。
   ```bash
   npx get-db@latest --yes --ref agent-skills --env .env.local --seed ./schema.sql
   ```
5. **验证：** 确认连接字符串已写入目标文件。
6. **报告：** 告知用户连接字符串写入位置、使用的键名，以及 env 文件中有认领 URL。提醒：数据库现在可用；72 小时内认领以永久保留。
7. **可选：** 提供快速连接测试（如 `SELECT 1`）。

### 输出检查清单

始终报告：

- 连接字符串写入位置（如 `.env`）
- 使用的变量键名（`DATABASE_URL` 或自定义键名）
- 认领 URL（来自 `.env` 或 API 响应）
- 未认领的数据库是临时的（72 小时）

## 认领

认领是可选的。数据库无需认领即可立即使用。要认领，用户在浏览器中打开认领 URL，登录或创建 Neon 账户来认领数据库。

- **API/SDK：** 将创建响应中的 `claim_url` 提供给用户。
- **CLI：** `npx get-db@latest claim` 从 `.env` 读取认领 URL 并自动打开浏览器。

用户无法认领到 Vercel 关联的组织；必须选择其他 Neon 组织。

## 默认值和限制

| 参数 | 值 |
|-----------|-------|
| 提供商 | AWS |
| 区域 | us-east-2 |
| Postgres | 17 |

可认领数据库的区域无法更改。未认领数据库有更严格的配额。认领后重置为免费计划默认限制。

| | 未认领 | 已认领（免费计划） |
|---|-----------|---------------------|
| 存储 | 100 MB | 512 MB |
| 传输 | 1 GB | ~5 GB |
| 分支 | 无 | 有 |
| 过期 | 72 小时 | 无 |

## 自动配置

如果智能体需要数据库来完成任务（如"用真实数据库帮我构建一个待办应用"）而用户未提供连接字符串，通过 API 配置一个并通知用户。包含认领 URL 以便用户保留数据库。

## 安全和用户体验注意事项

- 不要覆盖现有环境变量。先检查，然后使用 `--env` 或 `--key`（CLI）或跳过写入（API）以避免冲突。
- 运行破坏性种子 SQL（`DROP`、`TRUNCATE`、批量 `DELETE`）前先询问。
- 对于生产工作负载，建议使用标准 Neon 配置而非临时可认领数据库。
- 如果用户需要长期持久化，指导他们立即打开认领 URL。
- 将凭据写入 .env 文件后，检查它是否被 .gitignore 覆盖。如果没有，警告用户。未经确认不要修改 `.gitignore`。


## 何时使用
当任务涉及上述主要领域或功能时使用此技能。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
