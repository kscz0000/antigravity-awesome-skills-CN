# 混合搜索

在单个集合上结合向量相似度与关键词（BM25）匹配，实现平衡的搜索结果。

## 用法

```bash
uv run scripts/hybrid_search.py --query "USER_QUERY" --collection "CollectionName" [--alpha 0.7] [--limit 10] [--properties "prop1,prop2"] [--target-vector "vector_name"] [--json]
```

## 参数

| 参数 | 标志 | 是否必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `--query` | `-q` | 是 | — | 搜索查询文本 |
| `--collection` | `-c` | 是 | — | 集合名称 |
| `--alpha` | `-a` | 否 | `0.7` | 向量（1.0）与关键词（0.0）之间的平衡 |
| `--limit` | `-l` | 否 | `10` | 结果最大数量 |
| `--properties` | `-p` | 否 | all | 用于搜索的、用逗号分隔的属性列表 |
| `--target-vector` | `-t` | 否 | — | 命名向量集合的目标向量名称 |
| `--json` | — | 否 | `false` | 以 JSON 格式输出 |

## 输出

- **默认**：包含对象属性和分数的 Markdown 表格
- **JSON**：包含属性与搜索元数据的对象数组

## 示例

基础混合搜索：

```bash
uv run scripts/hybrid_search.py --query "climate change effects" --collection "Articles"
```

关键词为主的搜索（alpha 较低）：

```bash
uv run scripts/hybrid_search.py --query "product SKU-1234" --collection "Products" --alpha 0.3
```

在指定属性上搜索并使用命名向量：

```bash
uv run scripts/hybrid_search.py --query "renewable energy" --collection "Papers" --properties "title,abstract" --target-vector "title_vector"
```