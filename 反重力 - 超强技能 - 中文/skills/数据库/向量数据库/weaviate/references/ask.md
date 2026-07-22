# 查询代理 - 提问模式

通过 Weaviate Query Agent 生成带来源引用的 AI 回答。

## 用法

```bash
uv run scripts/ask.py --query "USER_QUESTION" --collections "Collection1,Collection2" [--json]
```

## 参数

| 参数 | 标志 | 必填 | 默认值 | 说明 |
|-----------|------|----------|---------|-------------|
| `--query` | `-q` | 是 | — | 自然语言问题 |
| `--collections` | `-c` | 是 | — | 跨查询的集合名称,逗号分隔 |
| `--json` | — | 否 | `false` | 以 JSON 格式输出 |

## 输出

- **默认**: 带来源表格的 Markdown 格式回答
- **JSON**: 包含 `answer` 与 `sources` 字段的结构化响应

## 示例

跨多个集合提问:

```bash
uv run scripts/ask.py --query "What are the main topics in the dataset?" --collections "Articles,Reports"
```

JSON 输出:

```bash
uv run scripts/ask.py --query "Summarize recent findings" --collections "Research" --json
```