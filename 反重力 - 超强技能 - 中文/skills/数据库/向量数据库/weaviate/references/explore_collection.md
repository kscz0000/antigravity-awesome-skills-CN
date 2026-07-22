# 浏览 Collection

从一个 collection 中获取统计洞察、聚合指标和示例数据。

## 用法

```bash
uv run scripts/explore_collection.py "CollectionName" [--limit 5] [--no-metrics] [--json]
```

## 参数

| 参数 | 标志 | 是否必填 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| `name` | — | 是（位置参数） | — | Collection 名称 |
| `--limit` | `-l` | 否 | `5` | 要展示的示例对象数量 |
| `--no-metrics` | — | 否 | `false` | 跳过计算各属性的指标（更快） |
| `--json` | — | 否 | `false` | 以 JSON 格式输出 |

## 按数据类型的指标

脚本会根据属性数据类型计算聚合指标：

| 数据类型 | 指标 |
|-----------|---------|
| **Text** | count, top_occurrences（取值最高的前 5 个值及其计数） |
| **Int / Number** | count, min, max, mean, median, mode, sum |
| **Boolean** | count, percentage_true, percentage_false, total_true, total_false |
| **Date** | count, min, max, median, mode |

当你只需要示例对象时，使用 `--no-metrics` 跳过指标计算，结果更快。

## 输出

- **默认**：Markdown 格式的报告，包含总计数、各属性指标表和示例对象
- **JSON**：结构化的指标与示例数据

## 示例

使用默认设置浏览：

```bash
uv run scripts/explore_collection.py "Articles"
```

展示更多示例，跳过指标：

```bash
uv run scripts/explore_collection.py "Products" --limit 20 --no-metrics
```
