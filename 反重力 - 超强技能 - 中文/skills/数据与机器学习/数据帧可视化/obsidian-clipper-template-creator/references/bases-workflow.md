# 使用 Obsidian Bases

用户在 `Bases/*.base` 中维护"Bases"，用于定义不同类型笔记（例如食谱、剪藏、人物）的 Schema 和属性。

## 工作流程

1.  **识别类别：** 确定用户要剪藏的内容类型（例如食谱、新闻文章、YouTube 视频）。
2.  **查找 Base：** 在 `Bases/` 中搜索匹配的 `.base` 文件。
    *   示例：对于食谱，查找 `Bases/Recipes.base`。
    *   示例：对于通用文章，查找 `Bases/Clippings.base`。
3.  **读取 Base：** 读取 `.base` 文件的内容以了解所需的属性。

## 解读 .base 文件

Base 文件使用类 YAML 结构。查找 `properties` 部分。

```yaml
properties:
  file.name:
    displayName: name
  note.author:
    displayName: author
  note.type:
    displayName: type
  note.ingredients:
    displayName: ingredients
```

*   `note.X` 对应 frontmatter 中的属性名 `X`。
*   `displayName` 有助于理解用途，但属性键（例如 `author`、`type`、`ingredients`）才是模板中真正重要的。

## 映射到 Clipper 属性

创建 Web Clipper 的 JSON 时，将 Base 属性映射到 JSON 中的 `properties` 数组。

| Base 属性 | Clipper JSON 属性名 | 值策略 |
| :--- | :--- | :--- |
| `note.author` | `author` | `{{author}}` 或 `{{schema:author.name}}` |
| `note.source` | `source` | `{{url}}` |
| `note.published` | `published` | `{{published}}` |
| `note.ingredients` | `ingredients` | `{{schema:Recipe:recipeIngredient}}` |
| `note.type` | `type` | 常量（例如 `Recipe`）或留空 |

**关键步骤：** 询问用户哪些属性应自动填充，哪些应硬编码（例如 `type: Recipe`），哪些应留空供手动输入。
