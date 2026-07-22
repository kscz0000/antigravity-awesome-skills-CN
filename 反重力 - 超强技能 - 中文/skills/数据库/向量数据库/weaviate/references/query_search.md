# 查询代理 - 搜索模式

通过 Weaviate Query Agent，使用自然语言查询跨多个集合检索原始对象。

## 用法

```bash
uv run scripts/query_search.py --query "USER_QUERY" --collections "Collection1,Collection2" [--limit 10] [--json]
```

## 参数

| 参数 | 标志 | 是否必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `--query` | `-q` | 是 | — | 自然语言搜索查询 |
| `--collections` | `-c` | 是 | — | 用逗号分隔、要跨集合搜索的集合名称列表 |
| `--limit` | `-l` | 否 | `10` | 返回结果的最大数量 |
| `--json` | — | 否 | `false` | 以 JSON 格式输出 |

## 输出

- **默认**：包含 UUID、集合名称及全部对象属性的 Markdown 表格（列动态生成）
- **JSON**：包含 `uuid`、`collection` 和 `properties` 的对象数组

## 示例

跨集合搜索：

```bash
uv run scripts/query_search.py --query "machine learning papers" --collections "Articles,Research" --limit 5
```

JSON 输出：

```bash
uv run scripts/query_search.py --query "products under $50" --collections "Products" --json
```