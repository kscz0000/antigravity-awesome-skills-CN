# 拉取与过滤

按 UUID、过滤条件或随机抽样从集合中拉取对象。支持复杂的嵌套过滤逻辑（AND、OR）。

## 用法

```bash
uv run scripts/fetch_filter.py "CollectionName" [--id "UUID"] [--filters 'JSON'] [--limit 10] [--properties "prop1,prop2"] [--json]
```

## 参数

| 参数 | 标记 | 必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `collection_name` | — | 是（位置参数） | — | 集合名称 |
| `--id` | — | 否 | — | 按 UUID 拉取指定对象 |
| `--filters` | `-f` | 否 | — | 定义过滤器的 JSON 字符串（见下方过滤语法） |
| `--limit` | `-l` | 否 | `10` | 拉取的对象数量 |
| `--properties` | `-p` | 否 | 全部 | 逗号分隔的、要在输出中包含的属性列表 |
| `--json` | — | 否 | `false` | 以 JSON 格式输出 |

## 模式

1. **按 UUID 拉取**：使用 `--id` 获取指定对象
2. **按过滤条件拉取**：使用 `--filters` 获取过滤后的子集
3. **随机抽样拉取**：同时省略 `--id` 与 `--filters`，返回未过滤的全部结果

## 过滤语法

### 简单属性过滤

```json
{"property": "category", "operator": "equal", "value": "Science"}
```

### 逻辑运算符（AND / OR）

```json
{"operator": "and", "filters": [
  {"property": "category", "operator": "equal", "value": "Science"},
  {"property": "year", "operator": "greater_than", "value": 2020}
]}
```

### 过滤器列表（隐式 AND）

```json
[
  {"property": "category", "operator": "equal", "value": "Science"},
  {"property": "year", "operator": "greater_than", "value": 2020}
]
```

### 支持的运算符

`equal`, `not_equal`, `less_than`, `less_or_equal`, `greater_than`, `greater_or_equal`, `like`, `contains_any`, `contains_all`, `is_none`

## 输出

- **默认**：Markdown 表格，包含对象 UUID 与属性
- **JSON**：包含完整元数据的对象数组

## 示例

按 UUID 拉取：

```bash
uv run scripts/fetch_filter.py "Articles" --id "550e8400-e29b-41d4-a716-446655440000"
```

按属性过滤：

```bash
uv run scripts/fetch_filter.py "Products" --filters '{"property": "price", "operator": "less_than", "value": 50}'
```

带 AND/OR 的复合过滤：

```bash
uv run scripts/fetch_filter.py "Articles" --filters '{"operator": "or", "filters": [{"property": "category", "operator": "equal", "value": "Science"}, {"property": "category", "operator": "equal", "value": "Tech"}]}'
```

选取指定属性：

```bash
uv run scripts/fetch_filter.py "Products" --properties "name,price" --limit 5
```

