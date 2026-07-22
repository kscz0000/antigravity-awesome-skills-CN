# 列出集合

展示所有可用的 Weaviate 集合及其属性。

## 用法

```bash
uv run scripts/list_collections.py [--json]
```

## 参数

| 参数 | 标志 | 必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `--json` | — | 否 | `false` | 以 JSON 格式输出 |

## 输出

- **默认**: 包含集合名称、描述与属性列表的 Markdown 表格
- **JSON**: 包含完整属性详情的集合对象数组

## 示例

```bash
uv run scripts/list_collections.py
```

```bash
uv run scripts/list_collections.py --json
```

