# Obsidian Web Clipper JSON Schema

Obsidian Web Clipper 通过 JSON 文件导入模板。

## 根结构

```json
{
	"schemaVersion": "0.1.0",
	"name": "Template Name",
	"behavior": "create",
	"noteContentFormat": "Markdown content here...",
	"properties": [],
	"triggers": [],
	"noteNameFormat": "{{title}}",
	"path": "Inbox/"
}
```

### 字段

*   **`schemaVersion`**：始终为 "0.1.0"。
*   **`name`**：模板在 Clipper 中的显示名称。
*   **`behavior`**：笔记的创建方式。
    *   `create`：创建新笔记。
    *   `append-specific`：追加到指定笔记（需要 `path` 为完整文件路径）。
    *   `append-daily`：追加到每日笔记。
*   **`noteContentFormat`**：笔记正文。
    *   使用 `\n` 表示换行。
    *   可使用所有变量（例如 `{{content}}`、`{{selection}}`）。
    *   支持**模板逻辑**（条件判断、循环、变量赋值），详见 [logic.md](logic.md)。
*   **`noteNameFormat`**：文件名模式（例如 `{{date}} - {{title}}`）。
*   **`path`**：笔记保存位置。
    *   对于 `create` 行为：保存笔记的*文件夹*（例如 `Clippings/` 或 `Recipes/`）。
    *   对于 `append-specific` 行为：要追加到的笔记的*完整文件路径*（例如 `Databases/Recipes.md`）。
*   **`triggers`**：用于自动选择此模板的字符串数组。
    *   **URL 模式**：`["https://www.youtube.com/watch"]`（简单字符串或正则表达式）。
    *   **Schema 类型**：`["schema:Recipe"]`（当页面包含此 Schema.org 类型时触发）。

## 属性

`properties` 数组定义笔记的 YAML frontmatter。

```json
"properties": [
    {
        "name": "category",
        "value": "Recipes",
        "type": "text"
    },
    {
        "name": "published",
        "value": "{{published}}",
        "type": "datetime"
    }
]
```

### 属性类型

*   **`text`**：简单文本字符串。
*   **`multitext`**：文本字符串列表（用于标签/别名）。
*   **`number`**：数值。
*   **`checkbox`**：布尔值 true/false。
*   **`date`**：日期字符串（YYYY-MM-DD）。
*   **`datetime`**：日期时间字符串。

### 属性对象结构

*   **`name`**：YAML frontmatter 中的键。
*   **`value`**：要填充的值。可包含变量和与 `noteContentFormat` 相同的**模板逻辑**（条件判断、循环、变量赋值）；详见 [logic.md](logic.md)。
*   **`type`**：上述类型之一。

## 模板验证

Clipper 模板编辑器会检查模板语法。
`noteContentFormat` 或属性 `value` 字段中的无效逻辑会在编辑器中报告；请使用 [Logic](https://help.obsidian.md/web-clipper/logic) 文档中描述的有效语法。
