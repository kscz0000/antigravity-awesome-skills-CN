---
name: mesh-memory
description: "通过 MCP 为 AI 智能体提供自托管的语义记忆服务。保存工作日志、决策和笔记，跨会话按语义而非关键词召回。基于 Postgres + pgvector，支持自动标签。"
risk: safe
source: dklymentiev/mesh-memory (MIT)
date_added: "2026-05-23"
---

# Mesh Memory

Mesh Memory 是一款自带 MCP 服务器的自托管语义记忆服务。它将文档（工作日志、决策、笔记、研究资料）存储于带有 pgvector 扩展的 PostgreSQL 中，并按语义检索——因此像"我们选了什么数据库？"这样的查询，即使关键词零重叠，也能找到那条写着"选择 Redis 用于缓存"的已保存笔记。嵌入向量本地生成，使用 `multilingual-e5-base`（768 维），核心流程无需外部 API 密钥。

当智能体需要跨会话持久记忆——保存自身工作、召回过往决策，或构建多智能体共享的项目知识库时，使用本技能。

## 使用场景

- 保存会话工作日志、决策或研究笔记，供后续会话查找。
- 按主题召回过往工作，即使不记得当时用的确切词汇。
- 在多个智能体、终端或团队成员之间共享长期知识库。
- 通过工作区（每个角色/项目一个工作区）按角色或项目组织上下文。
- 查询结构化标签（如某项目的所有 `type:decision` 条目）。

## 前置条件

- 一个可从 MCP 服务器访问的运行中的 Mesh Memory 实例。本地 Docker 是常用方式——在上游仓库执行 `docker compose up -d` 即可启动；完整快速入门参见 https://github.com/dklymentiev/mesh-memory。
- MCP 服务器（`mcp_server.py`）已注册到你的客户端（Claude Code、Cursor、Claude Desktop 或任何支持 MCP 的智能体）。
- `MESH_API_URL` 指向运行中的实例（默认：`http://localhost:8000`）。

## 设置

在客户端配置中注册 MCP 服务器：

```json
{
  "mcpServers": {
    "mesh": {
      "command": "python3",
      "args": ["/path/to/mesh-memory/mcp_server.py"],
      "env": {
        "MESH_API_URL": "http://localhost:8000"
      }
    }
  }
}
```

服务器可达后，下方列出的 13 个工具即可使用。

## MCP 工具

| 工具 | 用途 |
|------|------|
| `mesh_focus` | 切换活跃工作区（可选预取最近文档）。 |
| `mesh_add` | 保存文档并可选标签。自动添加 `date:YYYY-MM-DD` 和 `source:`。 |
| `mesh_update` | 更新已有文档的内容、标签或置顶状态。 |
| `mesh_delete` | 按 GUID 删除文档。 |
| `mesh_get` | 按 GUID 获取单个文档。 |
| `mesh_search` | 按查询语句语义搜索，可跨多个工作区并设置权重。 |
| `mesh_bytag` | 列出匹配一个或多个标签的文档（AND 逻辑）。 |
| `mesh_recent` | 列出最近创建的文档，可选按 `type:` 标签过滤。 |
| `mesh_projects` | 列出各项目的文档计数（以 `guid:` 标签作为项目标识）。 |
| `mesh_tags` | 列出已有标签及其计数；可选前缀过滤。 |
| `mesh_versions` | 展示文档的版本链（相似度关联的修订版本）。 |
| `mesh_stats` | 活跃工作区的记忆统计信息。 |
| `mesh_schema` | 展示标签模式（识别的前缀和类型）。 |

## 工作流

### 保存会话工作日志

完成工作后，持久化供未来会话使用：

```
mesh_add(
  content="Investigated 502s on the checkout flow. Root cause: missing CORS header on the cart API. Fix shipped in commit abc123.",
  tags="type:worklog,topic:checkout,date:2026-05-23",
  workspace="developer"
)
```

省略时 `date:` 和 `source:` 会自动添加。嵌入完成后，类型和主题标签从最近邻推断（需要 5-10 个种子文档后推断才会生效）。

### 按语义召回过往工作

跨会话搜索相关上下文，即使词汇不同：

```
mesh_search(query="checkout was failing for some users", limit=5, workspace="developer")
```

查询语句与原始笔记（"502s"、"CORS"）没有关键词重叠，但基于嵌入的搜索能找到它。

### 切换角色/上下文

对于多角色智能体，在会话开始时切换活跃工作区：

```
mesh_focus(workspace="sysadmin", prefetch=true, limit=5)
```

后续调用默认使用该工作区。在每个工作区顶部置顶一个角色提示文档，使智能体每次预取时重新定位。

### 带权重的跨工作区搜索

从相关领域提取上下文而不稀释主信号：

```
mesh_search(
  query="nginx rate limit recipe",
  workspaces={"sysadmin": 0.7, "security": 0.2, "developer": 0.1},
  limit=10
)
```

结果跨工作区合并，并按工作区权重重评分。

### 按标签结构化查询

当需要精确过滤而非语义相似度：

```
mesh_bytag(tags="type:decision,status:active,guid:my-project", limit=20)
```

## 标签约定

Mesh 接受任意标签。推荐前缀（用于自动推断并由 `mesh_schema` 展示）：

| 前缀 | 含义 |
|------|------|
| `type:worklog` | 已完成工作；最常见类型。 |
| `type:note` | 快速笔记、观察记录。 |
| `type:decision` | 架构或产品决策。 |
| `type:research` | 调研结果、发现。 |
| `type:task` | 待办事项。 |
| `type:rfc` | 待评审提案。 |
| `status:active` / `status:completed` / `status:archived` | 生命周期状态。 |
| `date:YYYY-MM-DD` | 文档创建日期（自动添加）。 |
| `source:` | 文档来源方式（自动添加：`mcp`、`api` 等）。 |
| `guid:<project-id>` | 项目标识——在项目所有文档中使用一致的 slug。 |

工作区文档少于约 5-10 条时，邻居推断被跳过；手动标注种子文档直至语料库自组织。

## 故障排查

**工具调用因连接错误失败。** MCP 服务器无法访问 `MESH_API_URL`。验证实例已运行（`curl $MESH_API_URL/health` 应返回 `{"status":"healthy"}`）且 MCP 配置中的环境变量已设置。

**已保存文档在语义搜索中暂未出现。** 嵌入生成在后台运行。保存后预计有 1-2 秒延迟才能被语义搜索命中。`mesh_get(guid=...)` 可立即确认文档已存在。

**搜索返回错误领域的结果。** 活跃工作区与预期不符。显式调用 `mesh_focus(workspace="<name>")`，或在每次调用时传入 `workspace=`。无焦点且无显式参数时，调用落入 `default` 工作区。

**自动标签从未添加任何内容。** 工作区文档太少无法进行邻居推断（最少约 5-10 条）。手动标注若干种子文档后，自动推断将接管。

**已删除文档仍出现在搜索结果中。** 嵌入索引最终一致；几秒后重试搜索，或用 `mesh_get(guid=...)` 确认删除。

## 限制

- Mesh 是知识存储，不是聊天记忆。长对话转录应在保存前总结。
- 向量相似度可靠但不完美；高精度结构化查询请用 `mesh_bytag` 而非 `mesh_search`。
- 嵌入默认在 CPU 上运行；超大语料库（数十万文档）需专用实例和 pgvector 调优，本文档未涵盖。
- 可选的 AI 分类器需要 OpenAI 兼容的 LLM 端点，默认禁用。