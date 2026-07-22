# 分析工作流程：验证变量

为确保模板正常工作，你必须验证目标页面确实包含你要提取的数据。

## 1. 获取页面

使用 `WebFetch` 工具或浏览器 DOM 快照来获取用户提供的代表性 URL 的内容。

```text
WebFetch(url="https://example.com/recipe/chocolate-cake")
```

## 2. 分析输出

### 检查 Schema.org（推荐）

查找 `<script type="application/ld+json">`。这包含结构化数据，是提取信息最可靠的方式。

**在 HTML 中找到的示例：**

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "Recipe",
  "name": "Chocolate Cake",
  "author": {
    "@type": "Person",
    "name": "John Doe"
  }
}
```

**结论：**

- `{{schema:Recipe:name}}` 有效。
- `{{schema:Recipe:author.name}}` 有效。
- **提示：** 你可以在 `triggers` 数组中使用 `schema:Recipe`，以便对任何包含此 Schema 的页面自动选择此模板。

### 检查 Meta 标签

在 `<head>` 部分查找 `<meta>` 标签。

**在 HTML 中找到的示例：**

```html
<meta property="og:title" content="The Best Chocolate Cake" />
<meta name="description" content="A rich, moist chocolate cake recipe." />
```

**结论：**

- `{{meta:og:title}}` 有效。
- `{{meta:description}}` 有效。

### 检查 CSS 选择器（已验证）

如果缺少 Schema 和 Meta 标签，查找 HTML 结构（class 和 ID）以配合 `{{selector:...}}` 使用。
选择器必须针对获取的 HTML 或 DOM 快照进行验证。不要猜测选择器。

**在 HTML 中找到的示例：**

```html
<div class="article-body">
  <h1 id="main-title">Chocolate Cake</h1>
  <span class="author-name">By John Doe</span>
</div>
```

**结论：**

- `{{selector:h1#main-title}}` 或 `{{selector:h1}}` 可以提取标题。
- `{{selector:.author-name}}` 可以提取作者。

## 3. 与 Base 对比验证

将分析中获得的可用数据与用户 Base 所需的属性进行对比（参见 [bases-workflow.md](bases-workflow.md)）。

- 如果 Base 需要 `ingredients` 但页面没有 Schema 或清晰的列表结构，警告用户该字段可能需要手动输入或使用 Prompt 变量。
