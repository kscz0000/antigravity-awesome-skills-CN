# 获取集合详情

获取指定集合的详细配置,包括向量化器、属性、复制与多租户设置。

## 用法

```bash
uv run scripts/get_collection.py --name "CollectionName" [--json]
```

## 参数

| 参数 | 标志 | 必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `--name` | `-n` | 是 | — | 集合名称 |
| `--json` | — | 否 | `false` | 以 JSON 格式输出 |

## 输出

- **默认**: 包含属性表格的 Markdown 格式集合详情
- **JSON**: 完整的集合配置对象

## 示例

```bash
uv run scripts/get_collection.py --name "Articles"
```

```bash
uv run scripts/get_collection.py --name "Products" --json
```

