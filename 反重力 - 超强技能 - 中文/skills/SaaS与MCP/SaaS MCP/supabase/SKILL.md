---
name: supabase
description: "当执行任何涉及 Supabase 的任务时使用。触发词：Supabase 产品（Database、Auth、Edge Functions、Realtime、Storage、Vectors、Cron、Queues）；客户端库和 SSR 集成（supabase-js、@supabase/ssr）在 Next.js、React、SvelteKit、Astro、Remix 中；认证问题（登录、登出……"
risk: unknown
source: https://github.com/supabase/agent-skills/tree/main/skills/supabase
source_repo: supabase/agent-skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/supabase/agent-skills/blob/main/LICENSE
---

# Supabase
## 何时使用

当执行任何涉及 Supabase 的任务时使用。触发词：Supabase 产品（Database、Auth、Edge Functions、Realtime、Storage、Vectors、Cron、Queues）；客户端库和 SSR 集成（`supabase-js`、`@supabase/ssr`）在 Next.js、React、SvelteKit、Astro、Remix 中；认证问题（登录、登出……


## 核心原则

**1. Supabase 变更频繁 — 实现前务必对照更新日志和当前文档进行验证。**
不要依赖训练数据来了解 Supabase 特性。函数签名、`config.toml` 设置和 API 约定在不同版本间会发生变化。

首先，获取 `https://supabase.com/changelog.md`（一个轻量级的摘要索引 — 不是大量拉取），扫描与你任务相关的 `breaking-change` 标签，并按照链接查看适用的页面。然后使用下面的文档访问方法查找相关主题。

**2. 验证你的工作。**
在实现任何修复后，运行测试查询来确认更改是否生效。没有验证的修复是不完整的。

**3. 从错误中恢复，不要循环。**
如果一种方法在 2-3 次尝试后失败，停下来重新思考。尝试不同的方法、查阅文档、更仔细地检查错误，并在可用时查看相关日志。Supabase 的问题并不总是通过重试相同的命令来解决，答案也不总是在日志中，但在继续之前查看日志通常是值得的。

**4. 将表暴露给 Data API：** 根据用户的 [Data API 设置](https://supabase.com/dashboard/project/<ref>/integrations/data_api/settings)，新创建的表可能不会自动通过 Data（REST）API 暴露。如果是这种情况，需要显式授予 `anon` 和 `authenticated` 角色访问权限。

> 注意，这与 RLS 是分开的，RLS 控制的是表可访问后哪些_行_可见，而不是表本身是否可访问。

当用户报告通过 SQL 创建的表意外不可访问时，检查他们的 Data API 设置以及角色是否已通过显式 `GRANT` SQL 被授予访问权限。当授予公共（`anon`/`authenticated`）访问权限时，务必同时启用 RLS。完整设置工作流请参见[将表暴露给 Data API](https://supabase.com/docs/guides/api/securing-your-api.md)。

**5. 已暴露 schema 中的 RLS。**
在每个已暴露 schema 中的每个表上启用 RLS，默认包括 `public`。这在 Supabase 中至关重要，因为当 `anon`/`authenticated` 角色拥有访问权限时，已暴露 schema 中的表可以通过 Data API 访问（参见[将表暴露给 Data API](https://supabase.com/docs/guides/api/securing-your-api.md)）。对于私有 schema，建议将 RLS 作为纵深防御。启用 RLS 后，创建与实际访问模型匹配的策略，而不是将每个表都默认为相同的 `auth.uid()` 模式。

**6. 安全检查清单。**
在处理任何涉及认证、RLS、视图、存储或用户数据的 Supabase 任务时，请过一遍此检查清单。这些是 Supabase 特有的安全陷阱，会静默地产生漏洞：

- **认证和会话安全**
  - **永远不要在基于 JWT 的授权决策中使用 `user_metadata` 声明。** 在 Supabase 中，`raw_user_meta_data` 是用户可编辑的，并且可能出现在 `auth.jwt()` 中，因此对 RLS 策略或任何其他授权逻辑来说是不安全的。请将授权数据存储在 `raw_app_meta_data` / `app_metadata` 中。
  - **删除用户不会使现有访问令牌失效。** 请先注销或撤销会话，对敏感应用保持较短的 JWT 过期时间，对于严格的保证，在敏感操作上根据 `auth.sessions` 验证 `session_id`。
  - **如果使用 `app_metadata` 或 `auth.jwt()` 进行授权，请记住 JWT 声明在用户令牌刷新之前不一定是最新的。**

- **API 密钥和客户端暴露**
  - **永远不要在公共客户端中暴露 `service_role` 或密钥。** 前端代码优先使用可发布密钥。旧版 `anon` 密钥仅用于兼容性。在 Next.js 中，任何 `NEXT_PUBLIC_` 环境变量都会发送到浏览器。

- **RLS、视图和特权数据库代码**
  - **视图默认绕过 RLS。** 在 Postgres 15 及以上版本中，使用 `CREATE VIEW ... WITH (security_invoker = true)`。在较旧版本的 Postgres 中，通过撤销 `anon` 和 `authenticated` 角色的访问权限或将视图放在未暴露的 schema 中来保护你的视图。
  - **UPDATE 需要 SELECT 策略。** 在 Postgres RLS 中，UPDATE 需要先 SELECT 该行。没有 SELECT 策略，更新会静默返回 0 行 — 没有错误，只是没有更改。
  - **`auth.role()` 已弃用 — 改用 `TO` 子句。** Supabase 已弃用 `auth.role()`，改为在策略上直接使用 `TO authenticated` 或 `TO anon` 指定目标角色。除了弃用之外，当启用匿名登录时，`auth.role() = 'authenticated'` 会静默失效，因为匿名用户携带 `authenticated` Postgres 角色，无论用户是否真正登录都会通过检查。
    ```sql
    -- Deprecated (do not use)
    create policy "example" on table_name for select
    using ( auth.role() = 'authenticated' );
    ```
  - **仅使用 `TO authenticated` 是认证而非授权（BOLA / IDOR）。** 使用 `TO authenticated` 只检查角色 — 它不限制用户可以访问哪些行。正确的模式是将 `TO authenticated` 与 `USING` 中的所有权谓词结合使用：
    ```sql
    create policy "example" on table_name for select
    to authenticated
    using ( (select auth.uid()) = user_id );
    ```
  - **UPDATE 策略需要同时包含 `USING` 和 `WITH CHECK`。** 没有 `WITH CHECK`，用户可以将行的 `user_id` 重新分配给另一个用户：
    ```sql
    create policy "example" on table_name for update
    to authenticated
    using ( (select auth.uid()) = user_id )
    with check ( (select auth.uid()) = user_id );
    ```
  - **`SECURITY DEFINER` 函数绕过 RLS。** `SECURITY DEFINER` 函数以其创建者的权限运行 — 通常是具有 `bypassrls` 的角色（例如 `postgres`）。永远不要为了解决权限错误而添加 `SECURITY DEFINER`；它会静默地移除访问控制而不修复根本原因。优先使用 `SECURITY INVOKER`。
  - **`public` 中的 `SECURITY DEFINER` 函数可被所有角色调用。** Postgres 默认为每个新函数授予 `EXECUTE` 给 `PUBLIC`，因此 `public` 中任何 `SECURITY DEFINER` 函数都是一个公共 API 端点，`anon` 和 `authenticated`（继承自 `PUBLIC`）无需额外授权即可调用。当确实需要 `SECURITY DEFINER`（例如在内部查找表上绕过 RLS）时，将函数保留在非暴露的 schema 中，始终在函数体中包含 `auth.uid()` 检查，并在进行更改后运行 `supabase db advisors`。

- **存储访问控制**
  - **Storage upsert 需要 INSERT + SELECT + UPDATE。** 仅授予 INSERT 允许新上传但文件替换（upsert）会静默失败。你需要全部三种权限。

- **依赖和供应链安全**
  - **在安装 Supabase 包（`supabase-js`、`@supabase/ssr`、`supabase-py` 等）时，始终固定包版本并提交锁文件。** 完整检查清单参见 [npm 安全指南](https://supabase.com/docs/guides/security/npm-security.md)。

对于上述未涵盖的任何安全问题，获取 Supabase 产品安全索引：`https://supabase.com/docs/guides/security/product-security.md`

## Supabase CLI

始终通过 `--help` 发现命令 — 永远不要猜测。CLI 结构在不同版本间会变化。

```bash
supabase --help                    # All top-level commands
supabase <group> --help            # Subcommands (e.g., supabase db --help)
supabase <group> <command> --help  # Flags for a specific command
```

**Supabase CLI 已知陷阱：**

- `supabase db query` 需要 **CLI v2.79.0+** → 使用 MCP `execute_sql` 或 `psql` 作为备选
- `supabase db advisors` 需要 **CLI v2.81.3+** → 使用 MCP `get_advisors` 作为备选
- 当你需要新的迁移 SQL 文件时，**始终**先用 `supabase migration new <name>` 创建。永远不要编造迁移文件名或依赖记忆中的预期格式。

**版本检查和升级：** 运行 `supabase --version` 检查。有关 CLI 更新日志和版本特定功能，请查阅 [CLI 文档](https://supabase.com/docs/reference/cli/introduction)或 [GitHub releases](https://github.com/supabase/cli/releases)。

## Supabase MCP 服务器

有关设置说明、服务器 URL 和配置，请参见 [MCP 设置指南](https://supabase.com/docs/guides/getting-started/mcp)。

**连接问题排查** — 按以下顺序执行：

1. **检查服务器是否可达：**
   `curl -so /dev/null -w "%{http_code}" https://mcp.supabase.com/mcp`
   返回 `401` 是预期的（无令牌），意味着服务器正常运行。超时或"connection refused"意味着服务器可能已宕机。

2. **检查 `.mcp.json` 配置：**
   验证项目根目录有一个有效的 `.mcp.json`，其中包含正确的服务器 URL。如果缺失，创建一个指向 `https://mcp.supabase.com/mcp` 的配置。

3. **认证 MCP 服务器：**
   如果服务器可达且 `.mcp.json` 正确但工具不可见，用户需要进行认证。Supabase MCP 服务器使用 OAuth 2.1 — 告诉用户在其智能体中触发认证流程，在浏览器中完成，然后重新加载会话。

## Supabase 文档

在实现任何 Supabase 功能之前，先找到相关文档。按以下优先级顺序使用这些方法：

1. **MCP `search_docs` 工具**（首选 — 直接返回相关片段）
2. **以 markdown 格式获取文档页面** — 任何文档页面都可以通过在 URL 路径后附加 `.md` 来获取。
3. **网络搜索** Supabase 特定主题，当你不知道该查看哪个页面时使用。

## 创建和提交 Schema 变更

**要创建 schema 变更，请使用 `execute_sql`（MCP）或 `supabase db query`（CLI）。** 这些命令直接在数据库上运行 SQL，不会创建迁移历史记录条目，因此你可以自由迭代，在准备好时生成干净的迁移。

不要使用 `apply_migration` 来更改本地数据库 schema — 它每次调用都会写入一条迁移历史记录，这意味着你无法迭代，而且 `supabase db diff` / `supabase db pull` 会产生空或冲突的差异。如果你使用了它，你将被困在第一次传入的 SQL 上。

**当准备好提交**你的变更到迁移文件时：

1. **运行 advisors** → `supabase db advisors`（CLI v2.81.3+）或 MCP `get_advisors`。修复任何问题。
2. **审查上面的安全检查清单** 如果你的变更涉及视图、函数、触发器或存储。
3. **生成迁移** → `supabase db pull <descriptive-name> --local --yes`
4. **验证** → `supabase migration list --local`

## 参考指南

- **技能反馈** → [references/skill-feedback.md](references/skill-feedback.md)
  **必须阅读的场景**：用户报告本技能给出了错误指导或缺少信息时。

## 限制

- 仅当任务明确匹配其上游产品或 API 范围时使用本技能。
- 在进行更改之前，务必根据当前官方文档验证命令、API 行为、定价、配额、凭证和部署效果。
- 不要将生成的示例替代针对特定环境的测试、安全审查或用户对破坏性或高成本操作的批准。
