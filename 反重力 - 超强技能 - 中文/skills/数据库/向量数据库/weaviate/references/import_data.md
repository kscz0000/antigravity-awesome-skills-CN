# 导入数据

将一个或多个 CSV、JSON、JSONL 或 PDF 文件导入到 Weaviate 集合，自动完成类型转换与列映射。同一格式的多个文件可在一次调用中传入 — 所有对象都会追加到同一个集合。PDF 文件会逐页转换为 base64 编码的 JPEG 图片；首次导入时自动创建集合，后续运行中复用该集合。

## 用法

```bash
# CSV/JSON/JSONL — collection must already exist
uv run scripts/import.py "data.csv" --collection "CollectionName" [--mapping '{}'] [--tenant "name"] [--batch-size 100] [--json]

# Multiple files of the same format
uv run scripts/import.py a.csv b.csv c.csv --collection "CollectionName"

# PDF — collection is created automatically on first run; appended to on subsequent runs
uv run scripts/import.py "document.pdf" --collection "CollectionName" [--image-field "doc_page"] [--batch-size 100] [--json]

# Multiple PDFs into the same collection
uv run scripts/import.py page1.pdf page2.pdf page3.pdf --collection "PDFDocuments"
```

## 参数

| 参数 | 标记 | 必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `files` | — | 是（位置参数，可多个） | — | 一个或多个 CSV、JSON、JSONL 或 PDF 文件（必须使用同一种格式） |
| `--collection` | `-c` | 是 | — | 目标集合名称（CSV/JSON/JSONL 必须已存在；PDF 若不存在则自动创建，否则追加到现有集合） |
| `--mapping` | `-m` | 否 | — | 将文件列/键映射到集合属性的 JSON 对象（仅 CSV/JSON/JSONL） |
| `--tenant` | `-t` | 否 | — | 多租户集合的租户名称（集合启用多租户时必填） |
| `--batch-size` | `-b` | 否 | `100` | 每批写入的对象数 |
| `--image-field` | `-i` | 否 | `doc_page` | 用于存储 base64 页面图片的 BLOB 属性名（仅 PDF 导入） |
| `--skip-fields` | — | 否 | — | 逗号分隔的不导入字段名（例如 `vector`） |
| `--json` | — | 否 | `false` | 以 JSON 格式输出 |

## 文件格式

### CSV

- 第一行必须是表头 — 列名须与集合属性名一致（区分大小写）
- 分隔符与引号通过 `csv.Sniffer` 自动检测
- 缺少表头的文件会被拒绝并报清晰错误

### JSON

- 必须是对象数组：`[{"prop1": "value1"}, {"prop2": "value2"}]`
- 键须与集合属性名一致
- 整个文件一次性载入内存 — 大数据集请优先使用 JSONL

### JSONL

- 每行一个 JSON 对象
- 每个对象的键须与集合属性名一致
- 按行流式读取 — 大数据集的首选格式

### PDF

- 每一页被转换为 JPEG 图片并做 base64 编码
- 每一页成为一个 Weaviate 对象，包含以下属性：
  - `doc_page`（或 `--image-field` 指定的值）：该页的 base64 编码 JPEG 图片
  - `page_number`：从 1 开始的页码（int）
  - `file_name`：不带扩展名的 PDF 文件名（text）
- 当集合不存在时会**自动创建**，使用 `multi2vec_weaviate`（`ModernVBERT/colmodernvbert` + MUVERA 编码）。若集合已存在，页面会追加到现有集合 — 便于多次运行把多个 PDF 加载到同一集合
- 系统需要安装 `poppler`（Mac 上直接运行 `brew install poppler` 即可）

## 类型转换

对于 CSV、JSON 和 JSONL 导入，脚本依据集合 schema 引导类型转换。非字符串值（JSON/JSONL 原生类型）原样透传。字符串值按声明的属性类型进行强制转换：

| Schema 类型 | 转换方式 |
|---|---|
| `int` / `int[]` | `int(value)` — 失败时回退为字符串 |
| `number` / `number[]` | `float(value)` — 失败时回退为字符串 |
| `boolean` / `boolean[]` | `"true"`/`"false"` → bool — 失败时回退为字符串 |
| `date` / `date[]` | `"YYYY-MM-DD"` → `"YYYY-MM-DDT00:00:00Z"`，`"YYYY-MM-DD HH:MM:SS"` → 带 `Z` 的 RFC3339 |
| `text[]`、`int[]`、`number[]`、`boolean[]`、`date[]`、`uuid[]`、`object`、`object[]`、`geoCoordinates`、`phoneNumber` | JSON/JSONL：原生列表/字典原样透传。CSV：单元格用 `json.loads()` 解析 — 失败时回退为字符串 |
| `text`、`uuid` | 保留为字符串 |
| `blob` | 保留为字符串 — 源数据必须已经是 base64 编码 |
| schema 中不存在的字段 | 保留为字符串 |

`None` 与空字符串一律跳过。

## 保留字段

`id` 和 `_additional` 是 Weaviate 保留字段，不能用作属性名（包括嵌套属性）。若数据中出现这些键/列，导入会失败。可使用 `--skip-fields` 丢弃，或用 `--mapping` 重命名。 

**重要提示：** 当字段含有有意义的数据时，**始终**优先重命名，而非直接丢弃。例如把 `id` 重命名为 `object_id` 或 `product_id`（依据数据而定）。

`--mapping` 与 `--skip-fields` 支持嵌套对象字段的点号语法（例如 `author.id`）。

```bash
# Drop the top-level id field entirely
uv run scripts/import.py data.json --collection "Articles" --skip-fields "id"

# Rename top-level id to source_id
uv run scripts/import.py data.json --collection "Articles" --mapping '{"id": "source_id"}'

# Rename a nested id field inside an object property (e.g. author.id → author.author_id)
uv run scripts/import.py data.json --collection "Articles" --mapping '{"author.id": "author.author_id"}'

# Drop a nested id field
uv run scripts/import.py data.json --collection "Articles" --skip-fields "author.id"
```

## 输出

- **默认**：导入汇总，包含总数、成功数与失败数（如有失败附示例错误）
- **JSON**：结构化的导入统计

任何导入失败时返回退出码 `1`。

## 示例

从 CSV 导入：

```bash
uv run scripts/import.py data.csv --collection "Articles"
```

带列映射的导入：

```bash
uv run scripts/import.py data.csv --collection "Articles" \
  --mapping '{"title_col": "title", "body_col": "content"}'
```

导入到多租户集合：

```bash
uv run scripts/import.py data.jsonl --collection "Workspace" --tenant "tenant1"
```

使用自定义批量大小的 JSON 导入：

```bash
uv run scripts/import.py products.json --collection "Products" --batch-size 500
```

导入 PDF（首次运行自动创建集合）：

```bash
uv run scripts/import.py paper.pdf --collection "PDFDocuments"
```

将多个 PDF 导入到同一集合：

```bash
uv run scripts/import.py chapter1.pdf chapter2.pdf chapter3.pdf --collection "PDFDocuments"
```

使用自定义图片字段名导入 PDF：

```bash
uv run scripts/import.py paper.pdf --collection "PDFDocuments" --image-field "page_image"
```

将多个 CSV 文件导入到同一集合：

```bash
uv run scripts/import.py jan.csv feb.csv mar.csv --collection "Articles"
```

