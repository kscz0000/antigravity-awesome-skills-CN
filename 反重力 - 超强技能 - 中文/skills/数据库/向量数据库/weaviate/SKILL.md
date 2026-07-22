---
name: weaviate
description: "使用官方脚本和参考文档对 Weaviate 向量数据库的 collection 进行搜索、查询、检视、创建与数据导入。涉及 Weaviate、向量数据库、collection、混合搜索、语义搜索、向量检索、HNSW、嵌入、embedding、批量导入、CSV/JSON/JSONL/PDF 入库、Query Agent。"
category: databases
risk: critical
source: community
source_repo: weaviate/agent-skills
source_type: official
date_added: "2026-06-29"
author: Weaviate
tags: [weaviate, vector-database, semantic-search, hybrid-search, data-import]
tools: [python, weaviate]
license: "BSD-3-Clause"
license_source: "https://github.com/weaviate/agent-skills/blob/main/LICENSE"
---

# Weaviate 数据库操作

本技能提供对 Weaviate 向量数据库的全面访问能力，包括搜索操作、自然语言查询、schema 检视、数据探索、带过滤条件的拉取、collection 创建以及数据导入。

## 适用场景

- 需要检视 Weaviate 的 collection、schema 或数据分布时。
- 需要对 Weaviate 执行语义、混合、关键词、过滤或 Query Agent 搜索时。
- 需要将 CSV、JSON、JSONL 或 PDF 数据导入到 Weaviate collection 时。
- 需要为基于 Weaviate 的工作流创建示例数据或 collection 时。

### Weaviate Cloud 实例

如果用户还没有实例，引导他们前往 Cloud Console 注册并创建一个免费沙箱。通过 [Weaviate Cloud](https://console.weaviate.cloud/signin?utm_source=github&utm_campaign=agent_skills) 创建 Weaviate 实例。

## 环境变量

**必填项：**

- `WEAVIATE_URL` — 你的 Weaviate Cloud 集群 URL
- `WEAVIATE_API_KEY` — 你的 Weaviate API key

**外部 Provider Key（自动检测）：**
只设置你 collection 用到的 key，详情参见 [Environment Requirements](references/environment_requirements.md)。

## 脚本索引

### 搜索与查询

- [Query Agent — Ask 模式](references/ask.md)：用户希望基于 collection 数据获得**直接答案**时使用。Query Agent 会综合一个或多个 collection 的信息，返回带有来源引用（collection 名称与对象 ID）的结构化响应。
- [Query Agent — Search 模式](references/query_search.md)：用户希望在一个或多个 collection 中**探索或浏览原始对象**时使用。与 ask 模式不同，该模式返回实际的数据对象，而非合成的答案。
- [混合搜索](references/hybrid_search.md)：**大多数搜索的默认选择。** 在语义理解与精确关键词匹配之间提供良好平衡。不确定选哪种搜索类型时，建议使用此模式。
- [语义搜索](references/semantic_search.md)：用于查找**概念相似**的内容，不拘泥于具体措辞。当意图比关键词更重要时效果最佳。
- [关键词搜索](references/keyword_search.md)：用于查找**精确的词、ID、SKU 或特定文本模式**。当需要精确的关键词匹配而非语义相似度时效果最佳。

### Collection 管理

- [列出 Collection](references/list_collections.md)：用于**发现 Weaviate 实例中存在哪些 collection**。在执行任何搜索或数据操作前，通常应先执行此步骤。
- [获取 Collection 详情](references/get_collection.md)：用于**理解某个 collection 的 schema**——包括属性、数据类型、vectorizer 配置、副本因子以及多租户状态。在执行搜索或导入前使用。
- [探索 Collection](references/explore_collection.md)：用于**分析 collection 内的数据分布、Top 值，并检视实际内容**。有助于在查询前了解数据形态。
- [创建 Collection](references/create_collection.md)：用于在导入数据前**以自定义 schema 创建新 collection**。除非用户明确要求，否则不要指定 vectorizer（默认使用 `text2vec_weaviate`）。

### 数据操作

- [拉取与过滤](references/fetch_filter.md)：用于**按 ID 检索特定对象**或**严格过滤后的数据子集**。适合精确数据检索而非搜索。
- [导入数据](references/import_data.md)：**用户要求将文件（CSV、JSON、JSONL、PDF）导入、加载或摄取到 collection 时使用。**
- [创建示例数据](references/example_data.md)：在没有可用数据，或用户请求一些玩具数据时，用以为其他技能立即提供示例数据。

## 推荐流程

1. **先列出 collection**，如果你还不清楚有哪些可用：

   ```bash
   uv run scripts/list_collections.py
   ```

2. **询问用户**是否要**创建示例数据**，当没有任何数据且用户提出此需求时。否则继续。

   ```bash
   uv run scripts/example_data.py
   ```

3. **获取 collection 详情**以理解其 schema：

   ```bash
   uv run scripts/get_collection.py --name "COLLECTION_NAME"
   ```

4. **探索 collection 数据**以查看取值与统计信息：

   ```bash
   uv run scripts/explore_collection.py "COLLECTION_NAME"
   ```

5. **创建 collection**（如果要导入新的 CSV、JSON 或 JSONL 文件）—— 导入前 collection 必须已经存在：

   ```bash
   uv run scripts/create_collection.py CollectionName \
     --properties '[{"name": "title", "data_type": "text"}, {"name": "body", "data_type": "text"}]'
   ```
   > 除非用户明确要求，否则不要指定 vectorizer。

6. **导入数据**到已存在的 collection 中：

   ```bash
   uv run scripts/import.py "data.csv" --collection "CollectionName"
   ```
   > PDF 导入会自动创建 collection —— 跳过第 5 步。

7. **选择合适的搜索类型：**
   - 需要跨多个 collection 的带来源引用的 AI 答案 → `ask.py`
   - 需要从多个 collection 获取原始对象 → `query_search.py`
   - 通用搜索 → `hybrid_search.py`（默认）
   - 概念相似度 → `semantic_search.py`
   - 精确词/ID → `keyword_search.py`

## 输出格式

所有脚本均支持：

- **Markdown 表格**（默认且推荐）
- **JSON**（`--json` 标志）

## 错误处理

常见错误：

- `WEAVIATE_URL not set` → 设置该环境变量
- `Collection not found` → 使用 `list_collections.py` 查看可用的 collection
- `Authentication error` → 检查 Weaviate 与 vectorizer provider 的 API key

## 局限性

- 本技能要求 Weaviate 实例可达且凭据有效，才能成功执行实时操作。
- 数据导入、collection 创建与 query-agent 操作可能变更或暴露用户数据；在运行脚本前请确认目标实例与 collection。
- 自带脚本专注于 Weaviate，不能替代更广泛的数据治理、备份或生产迁移流程。
