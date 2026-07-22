# Obsidian Web Clipper 变量

**官方文档：** [help.obsidian.md/web-clipper/variables](https://help.obsidian.md/web-clipper/variables)

## 预设变量
从页面自动提取。

- `{{content}}`：文章主要内容（Markdown）。
- `{{contentHtml}}`：文章主要内容（HTML）。
- `{{title}}`：页面标题。
- `{{url}}`：页面 URL。
- `{{author}}`：作者姓名。
- `{{date}}`：当前日期。
- `{{published}}`：发布日期（如检测到）。
- `{{site}}`：站点名称。
- `{{description}}`：Meta 描述。
- `{{highlights}}`：高亮文本（如有）。
- `{{selection}}`：选中文本。
- `{{fullHtml}}`：完整页面 HTML。
- `{{favicon}}`：Favicon URL。
- `{{image}}`：社交分享图片 URL。
- `{{words}}`：字数统计。
- `{{domain}}`：域名。

## Prompt 变量（AI）
使用 `{{"Your prompt here"}}` 请求 AI 解释器提取或汇总信息。
*需要启用 Interpreter。*

示例：
- `{{"Summarize in 3 bullet points"}}`
- `{{"Extract the ingredients list"}}`
- `{{"Translate to English"}}`

## 选择器变量
使用 CSS 选择器提取内容。
语法：`{{selector:css-selector}}` 或 `{{selector:css-selector?attribute}}`

示例：
- `{{selector:h1}}`：H1 标签的文本。
- `{{selector:img.hero?src}}`：class 为 'hero' 的图片的 src。
- `{{selector:.author}}`：class 为 'author' 的元素的文本。
- `{{selectorHtml:body|markdown}}`：完整 HTML 转换为 Markdown。

## Meta 变量
从 Meta 标签提取数据。
语法：`{{meta:name}}` 或 `{{meta:property}}`

示例：
- `{{meta:description}}`
- `{{meta:og:title}}`

## Schema.org 变量
提取结构化数据。
语法：`{{schema:Property}}` 或 `{{schema:@Type:Property}}`

示例：
- `{{schema:Recipe:recipeIngredient}}`
- `{{schema:author.name}}`
- `{{schema:Article:headline}}`

## 回退值
当变量为空时，你可以提供默认值（回退值）。
回退值可以链式使用（先尝试变量 A，再尝试 B，再使用字面量默认值）并配合过滤器使用。
有关语法和求值顺序，参见 [logic.md](logic.md)。
