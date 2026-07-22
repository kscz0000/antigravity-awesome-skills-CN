# 链接、资源与校验

## 链接解析

将链接解析视为仓库专属行为。

对于典型的 Hugo 文档站点：

- 内部链接可以是普通 Markdown 目标
- `ref` 与 `relref` 出现在文档示例中，有时也会出现在活跃内容中
- 自定义链接 render hook 会解析页面、页面 resource、section resource 与全局 resource
- 失效链接行为由配置和本地 render-hook 逻辑控制
- 术语表简写可能以恰好等于 `(g)` 的 Markdown 目标形式出现
- fragment 可能针对目标标题进行校验，而不是盲目透传

### 解析顺序

对于自定义的 `render-link.html`，典型的解析顺序是：

1. 内容页面
2. 当前页面 bundle 中的页面 resource
3. 当前 section 的 section resource（仅当页面不是 leaf bundle 时）
4. 来自 `assets` 的全局 resource

对转换的启示：

- 不要假设每个相对链接都指向页面
- 不要将页面 bundle 文件与 section bundle 文件混为一谈
- 当站点将 `content/en` 挂载到逻辑上的 `content` 时，不要保留 `/en/` 文件系统路径
- 在扁平化后仍能解析时，保留查询字符串与 fragment
- 若无法从本地快照确认 fragment 有效性，则保留 fragment 并仅在确实存在歧义时附加说明

转换时：

- 将内部目标解析为普通 Markdown 链接
- 远程链接保留为普通外部链接
- 当 fragment 仍指向稳定标题时予以保留
- 避免将未解析的 Hugo 链接函数复制到输出中
- 若生成的表格或列表使用 front matter 字段作为标签，请在发出最终 Markdown 之前不区分大小写地解析这些字段

## 资源

在改写图片或文件引用之前，先检查所有以下内容：

- 页面 bundle resource
- section resource
- 挂载的资源
- 静态文件

对于 Hugo 仓库，还需区分：

- leaf bundle 与 branch bundle
- 类型为 `page` 的页面 resource 与图片、数据、文档或视频 resource
- front matter 中 `resources` 下定义的 resource 元数据

对于具有自定义链接 render hook 的站点，该 hook 可能显式依赖资源与挂载的 resource。在更改资源路径之前，请阅读 `hugo.toml` 与 `layouts/_markup/render-link.html`。

### Bundle 感知规则

将官方页面 bundle 与页面 resource 文档用作转换约束：

- leaf bundle 中 `index.md` 旁边的文件可以是页面 resource，不应作为独立页面渲染
- branch bundle 下的文件可以是后代内容页面或非页面 resource，取决于其位置
- 本地 render-link 逻辑中，section resource 查找对 leaf bundle 无效
- resource 的 `Name`、`Title` 与 `params` 可来自 front matter 元数据，而不仅来自文件名

若 shortcode 或 render hook 引用 resource，请在扁平化路径之前确认目标是否依赖 bundle 类型。

## 校验清单

运行：

```bash
python3 skills/hugo-to-markdown/scripts/check_standard_markdown.py \
  --root /path/to/output
```

检视命中：

- 活跃的 `{{< ... >}}` 或 `{{% ... %}}`
- 活跃的 Go 模板表达式，如 `{{ if ... }}` 或 `{{ .Page ... }}`
- 在正文中残留的 Hugo 专属链接辅助函数
- 泄漏的本地绝对路径
- 应被降级的可执行 HTML 或脚本残留
- 由 front matter 键不匹配导致的空 Markdown 链接或空表格单元格
- 在内容被剥离却未物化的位置缺失降级说明

## 残留分类

若校验器报告某条构造：

1. 检查它是否位于围栏代码块内。
2. 检查它是否是正文或符号表中的转义字面示例，如 `{{</* foo */>}}` 或 `{{%/* foo */%}}`。
3. 若是字面示例，予以保留。
4. 若是活跃 Hugo 语法，则解析或重写它。
5. 若无法安全解析，请用解释原始行为的显式 Markdown 文本替换。

## 降级审查

转换后，请人工检视你引入的每条说明性注释：

- 确认原始 shortcode 语法已消失
- 确认注释仍能告知读者被省略的内容
- 确认任何安全子集（如内联代码、已解析的链接或图片 URL）已保留

目标是得到带有显式丢失报告的标准 Markdown，而不是静默截断。