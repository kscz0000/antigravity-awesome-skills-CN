# Obsidian Web Clipper 过滤器

**官方文档：** [help.obsidian.md/web-clipper/filters](https://help.obsidian.md/web-clipper/filters)

使用过滤器格式化变量：`{{variable|filter}}`。

## 文本格式化
- `markdown`：将 HTML 转换为 Markdown。
- `strip_tags`：移除 HTML 标签。
- `trim`：移除空白字符。
- `upper`：转换为大写。
- `lower`：转换为小写。
- `title`：首字母大写（Title Case）。
- `capitalize`：首字母大写。
- `camel`：驼峰式（CamelCase）。
- `kebab`：短横线式（kebab-case）。
- `snake`：下划线式（snake_case）。
- `pascal`：帕斯卡式（PascalCase）。
- `replace:"old","new"`：替换文本。
- `safe_name`：转换为安全的文件名。
- `blockquote`：格式化为引用块。
- `link`：创建 Markdown 链接。
- `wikilink`：创建 [[wikilink]]。
- `list`：将数组格式化为列表。
- `table`：将数组格式化为表格。
- `callout`：格式化为标注块。

## 日期
- `date:"format"`：格式化日期（例如 `YYYY-MM-DD`）。
- `date_modify:"+1 day"`：修改日期。
- `duration`：格式化时长。

## 数字
- `calc`：执行计算。
- `length`：获取字符串/数组长度。
- `round`：四舍五入。

## HTML 处理
- `remove_html`：移除 HTML 标签。
- `remove_attr`：移除属性。
- `strip_attr`：去除特定属性。

## 数组和对象
- `map`：转换数组项（例如 `map:item =>> item.text`）。
- `join:"separator"`：连接数组项。
- `split:"separator"`：将字符串拆分为数组。
- `first`：第一项。
- `last`：最后一项。
- `slice:start,end`：切片数组。
- `unique`：去重。
- `template:"format"`：使用模板字符串格式化项。
