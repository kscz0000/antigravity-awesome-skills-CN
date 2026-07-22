# 创建集合

创建一个新的 Weaviate 集合，配置自定义 schema、可选 vectorizer，以及多租户支持。

## 用法

```bash
uv run scripts/create_collection.py CollectionName --properties '[...]' [--description "..."] [--vectorizer "..."] [--replication-factor N] [--multi-tenancy] [--auto-tenant-creation] [--json]
```

## 参数

| 参数 | 标记 | 必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `name` | — | 是（位置参数） | — | 集合名称（按 GraphQL 规范自动首字母大写） |
| `--properties` | `-p` | 是 | — | 属性定义的 JSON 数组 |
| `--description` | `-d` | 否 | — | 集合说明 — **强烈建议填写**。Weaviate Agent（Query Agent、Personalization Agent）会读取它来理解集合内容，并决定查询哪个集合 |
| `--vectorizer` | `-v` | 否 | `text2vec_weaviate` | 使用的 vectorizer 模块 |
| `--replication-factor` | `-r` | 否 | — | 副本因子（未设置时采用服务端默认值） |
| `--multi-tenancy` | `-m` | 否 | `false` | 启用多租户以隔离数据 |
| `--auto-tenant-creation` | `-a` | 否 | `false` | 写入时自动创建租户（需要 `--multi-tenancy`） |
| `--json` | — | 否 | `false` | 以 JSON 格式输出 |

## 属性定义格式

```json
{
  "name": "property_name",
  "data_type": "text",
  "description": "Optional description",
  "tokenization": "word",
  "index_filterable": true,
  "index_searchable": true,
  "index_range_filters": false,
  "nested_properties": []
}
```

- `name`（必填）：属性名称
- `data_type`（必填）：下文支持的某一数据类型
- `description`（可选）：人类可读的说明 — **强烈建议填写**。Query Agent 会读取属性说明来理解你的 schema、挑选合适的集合、构造准确的查询。好的说明应包含单位、格式和有效值（例如 `"Price in US dollars (USD)"`、`"ISO two-character country code"`、`"Date the paper was published on arXiv"`）
- `tokenization`（可选）：针对文本类型 — `word`、`lowercase`、`whitespace` 或 `field`
- `index_filterable`（可选）：为 `where` 子句启用 roaring-bitmap 过滤索引。除 `blob`、`geoCoordinates`、`object`、`object[]`、`phoneNumber` 外，其余类型默认 `true`
- `index_searchable`（可选）：为关键字与混合检索启用 BM25/倒排索引。仅对 `text` 和 `text[]` 生效。默认 `true`
- `index_range_filters`（可选）：为 `int`、`int[]`、`number`、`number[]`、`date`、`date[]` 启用范围比较索引（`>`、`<`、`>=`、`<=`、`between`）。默认 `false` — **对计划做范围过滤的数值或日期字段设为 `true`**
- `nested_properties`（可选）：针对 `object` / `object[]` 类型 — 嵌套属性定义数组

## 支持的数据类型

`text`, `text[]`, `boolean`, `boolean[]`, `int`, `int[]`, `number`, `number[]`, `date`, `date[]`, `uuid`, `uuid[]`, `geoCoordinates`, `phoneNumber`, `blob`, `object`, `object[]`

别名：`bool` → `boolean`，`bool[]` → `boolean[]`

## 支持的 Vectorizer

`text2vec_weaviate`, `text2vec_openai`, `text2vec_cohere`, `text2vec_huggingface`, `text2vec_palm`, `text2vec_jinaai`, `text2vec_voyageai`, `text2vec_contextionary`, `text2vec_transformers`, `text2vec_gpt4all`, `text2vec_ollama`, `multi2vec_clip`, `multi2vec_bind`, `multi2vec_palm`, `img2vec_neural`, `ref2vec_centroid`, `none`

## 从数据文件推断 Schema

创建集合前，先从源文件取若干行样本，了解字段名和值类型。使用下面的命令 — 只读取前 3 条对象，对大文件也安全。

**CSV：**
```bash
python3 -c "
import csv, json
with open('data.csv') as f:
    rows = list(csv.DictReader(f))[:3]
print(json.dumps(rows, indent=2))
"
```

**JSON：**
```bash
python3 -c "
import json
print(json.dumps(json.load(open('data.json'))[:3], indent=2))
"
```

**JSONL：**
```bash
python3 -c "
import json
lines = []
with open('data.jsonl') as f:
    for line in f:
        if len(lines) >= 3: break
        if line.strip(): lines.append(json.loads(line))
print(json.dumps(lines, indent=2))
"
```

依据样本，把每个字段映射到一个 Weaviate 数据类型：

| 取值形如 | data_type |
|---|---|
| `"hello"`，任意文本 | `text` |
| `123`，`"123"` | `int` |
| `1.5`，`"1.5"` | `number` |
| `true`/`false` | `boolean` |
| `"2024-01-15"`，`"2024-01-15T10:30:00Z"` | `date` |
| 形如 UUID 的字符串 | `uuid` |
| 字符串列表 | `text[]` |
| 数字列表 | `int[]` 或 `number[]` |
| 嵌套对象 | `object` |

**重要：**`id`、`_id`、`_additional` 是 Weaviate 保留字段，绝不能用作属性名。若数据中包含这些字段，可在 `import.py` 中用 `--skip-fields` 或 `--mapping` 处理。

## 示例

基础集合：

```bash
uv run scripts/create_collection.py Article \
  --description "News articles with title and full body text." \
  --properties '[
    {"name": "title", "data_type": "text", "description": "Title of the article"},
    {"name": "body", "data_type": "text", "description": "Full text body of the article"}
  ]'
```

包含多种数据类型、说明和推荐索引开关的集合：

```bash
uv run scripts/create_collection.py Product \
  --description "E-commerce product catalog with pricing, brand, stock status, and tags." \
  --properties '[
    {"name": "name", "data_type": "text", "description": "Name or title of the product"},
    {"name": "sku", "data_type": "text", "index_searchable": false, "description": "Stock-keeping unit identifier"},
    {"name": "price", "data_type": "number", "index_range_filters": true, "description": "Product price in US dollars (USD)"},
    {"name": "created_at", "data_type": "date", "index_range_filters": true, "description": "Date the product was added to the catalog"},
    {"name": "in_stock", "data_type": "boolean", "description": "Whether the product is currently in stock"},
    {"name": "tags", "data_type": "text[]", "description": "List of descriptive tags for the product"}
  ]'
```

显式指定 vectorizer：

```bash
uv run scripts/create_collection.py Article \
  --description "News articles with title and full body text." \
  --properties '[{"name": "title", "data_type": "text", "description": "Title of the article"}]' \
  --vectorizer "text2vec_openai"
```

启用多租户：

```bash
uv run scripts/create_collection.py Workspace \
  --properties '[{"name": "content", "data_type": "text"}]' \
  --multi-tenancy --auto-tenant-creation
```
