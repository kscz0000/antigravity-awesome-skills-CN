---
source: "https://github.com/huggingface/skills/tree/main/skills/huggingface-datasets"
name: hugging-face-dataset-viewer
description: 通过 Dataset Viewer API 查询 Hugging Face 数据集，获取分片、行数据、搜索、过滤和 parquet 链接。
risk: unknown
---

# Hugging Face Dataset Viewer

## 适用场景
适用于需要通过 Dataset Viewer API 对 Hugging Face 数据集进行只读探索的场景。

本技能用于执行只读的 Dataset Viewer API 调用，实现数据集探索与提取。

## 核心工作流

1. 可选：通过 `/is-valid` 验证数据集可用性。
2. 通过 `/splits` 解析 `config` 和 `split`。
3. 通过 `/first-rows` 预览数据。
4. 使用 `offset` 和 `length`（最大 100）通过 `/rows` 分页获取内容。
5. 使用 `/search` 进行文本匹配，使用 `/filter` 进行行条件过滤。
6. 通过 `/parquet` 获取 parquet 链接，通过 `/size` 和 `/statistics` 获取总量和元数据。

## 默认配置

- 基础 URL：`https://datasets-server.huggingface.co`
- 默认 API 方法：`GET`
- 查询参数应进行 URL 编码。
- `offset` 从 0 开始。
- `length` 最大值通常为 `100`（行相关端点）。
- 受限/私有数据集需要 `Authorization: Bearer <HF_TOKEN>`。

## Dataset Viewer

- `验证数据集`：`/is-valid?dataset=<namespace/repo>`
- `列出子集和分片`：`/splits?dataset=<namespace/repo>`
- `预览首行`：`/first-rows?dataset=<namespace/repo>&config=<config>&split=<split>`
- `分页获取行`：`/rows?dataset=<namespace/repo>&config=<config>&split=<split>&offset=<int>&length=<int>`
- `文本搜索`：`/search?dataset=<namespace/repo>&config=<config>&split=<split>&query=<text>&offset=<int>&length=<int>`
- `条件过滤`：`/filter?dataset=<namespace/repo>&config=<config>&split=<split>&where=<predicate>&orderby=<sort>&offset=<int>&length=<int>`
- `列出 parquet 分片`：`/parquet?dataset=<namespace/repo>`
- `获取数据总量`：`/size?dataset=<namespace/repo>`
- `获取列统计信息`：`/statistics?dataset=<namespace/repo>&config=<config>&split=<split>`
- `获取 Croissant 元数据（如可用）`：`/croissant?dataset=<namespace/repo>`

分页模式：

```bash
curl "https://datasets-server.huggingface.co/rows?dataset=stanfordnlp/imdb&config=plain_text&split=train&offset=0&length=100"
curl "https://datasets-server.huggingface.co/rows?dataset=stanfordnlp/imdb&config=plain_text&split=train&offset=100&length=100"
```

当分页不完整时，使用响应字段 `num_rows_total`、`num_rows_per_page` 和 `partial` 来驱动续取逻辑。

搜索/过滤说明：

- `/search` 匹配字符串列（全文检索行为由 API 内部实现）。
- `/filter` 需要在 `where` 中使用谓词语法，可选 `orderby` 排序。
- 保持过滤和搜索为只读操作，无副作用。

## 查询数据集

使用 `npx parquetlens` 配合 Hub parquet 别名路径进行 SQL 查询。

Parquet 别名格式：

```text
hf://datasets/<namespace>/<repo>@~parquet/<config>/<split>/<shard>.parquet
```

从 Dataset Viewer `/parquet` 推导 `<config>`、`<split>` 和 `<shard>`：

```bash
curl -s "https://datasets-server.huggingface.co/parquet?dataset=cfahlgren1/hub-stats" \
  | jq -r '.parquet_files[] | "hf://datasets/\(.dataset)@~parquet/\(.config)/\(.split)/\(.filename)"'
```

执行 SQL 查询：

```bash
npx -y -p parquetlens -p @parquetlens/sql parquetlens \
  "hf://datasets/<namespace>/<repo>@~parquet/<config>/<split>/<shard>.parquet" \
  --sql "SELECT * FROM data LIMIT 20"
```

### SQL 导出

- CSV：`--sql "COPY (SELECT * FROM data LIMIT 1000) TO 'export.csv' (FORMAT CSV, HEADER, DELIMITER ',')"`
- JSON：`--sql "COPY (SELECT * FROM data LIMIT 1000) TO 'export.json' (FORMAT JSON)"`
- Parquet：`--sql "COPY (SELECT * FROM data LIMIT 1000) TO 'export.parquet' (FORMAT PARQUET)"`

## 创建和上传数据集

根据依赖约束选择以下流程之一。

零本地依赖（Hub UI）：

- 在浏览器中创建数据集仓库：`https://huggingface.co/new-dataset`
- 在仓库的"Files and versions"页面上传 parquet 文件。
- 验证分片是否出现在 Dataset Viewer：

```bash
curl -s "https://datasets-server.huggingface.co/parquet?dataset=<namespace>/<repo>"
```

低依赖 CLI 流程（`npx @huggingface/hub` / `hfjs`）：

- 设置认证令牌：

```bash
export HF_TOKEN=<your_hf_token>
```

- 上传 parquet 文件夹到数据集仓库（若不存在则自动创建）：

```bash
npx -y @huggingface/hub upload datasets/<namespace>/<repo> ./local/parquet-folder data
```

- 创建时上传为私有仓库：

```bash
npx -y @huggingface/hub upload datasets/<namespace>/<repo> ./local/parquet-folder data --private
```

上传后，调用 `/parquet` 发现 `<config>/<split>/<shard>` 值，用于 `@~parquet` 查询。

## 限制
- 仅在任务明确符合上述范围时使用本技能。
- 输出内容不能替代环境特定的验证、测试或专家评审。
- 若缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
