# 关键词搜索

对单个集合执行 BM25 关键词匹配搜索。

## 用法

```bash
uv run scripts/keyword_search.py --query "USER_QUERY" --collection "CollectionName" [--limit 10] [--properties "title^2,content"] [--json]
```

## 参数

| 参数 | 标志 | 必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `--query` | `-q` | 是 | — | 关键词搜索查询语句 |
| `--collection` | `-c` | 是 | — | 集合名称 |
| `--limit` | `-l` | 否 | `10` | 返回结果的最大数量 |
| `--properties` | `-p` | 否 | all | 用于搜索的属性,支持可选加权(例如 `title^2,content`) |
| `--json` | — | 否 | `false` | 以 JSON 格式输出 |

## 输出

- **默认**: 包含对象属性与 BM25 评分的 Markdown 表格
- **JSON**: 包含属性与评分元数据的对象数组

## 示例

基础关键词搜索:

```bash
uv run scripts/keyword_search.py --query "Python tutorial" --collection "Articles"
```

带属性加权的搜索:

```bash
uv run scripts/keyword_search.py --query "authentication" --collection "Docs" --properties "title^2,body"
```