# 语义搜索

在单个集合上使用嵌入向量进行纯向量相似度搜索。

## 用法

```bash
uv run scripts/semantic_search.py --query "USER_QUERY" --collection "CollectionName" [--limit 10] [--distance 0.5] [--target-vector "vector_name"] [--json]
```

## 参数

| 参数 | 标志 | 是否必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `--query` | `-q` | 是 | — | 搜索查询文本 |
| `--collection` | `-c` | 是 | — | 集合名称 |
| `--limit` | `-l` | 否 | `10` | 结果最大数量 |
| `--distance` | `-d` | 否 | — | 最大距离阈值（过滤掉相似度较低的结果） |
| `--target-vector` | `-t` | 否 | — | 命名向量集合的目标向量名称 |
| `--json` | — | 否 | `false` | 以 JSON 格式输出 |

## 输出

- **默认**：包含对象属性与距离分数的 Markdown 表格
- **JSON**：包含属性与距离元数据的对象数组

## 示例

基础语义搜索：

```bash
uv run scripts/semantic_search.py --query "environmental impact of urbanization" --collection "Research"
```

带距离阈值：

```bash
uv run scripts/semantic_search.py --query "machine learning" --collection "Papers" --distance 0.3 --limit 5
```

使用命名向量：

```bash
uv run scripts/semantic_search.py --query "abstract art" --collection "Artworks" --target-vector "description_vector"
```