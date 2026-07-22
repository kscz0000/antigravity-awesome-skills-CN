# Shortcode 与 Render Hook

## Shortcode 符号

Hugo 有两种 shortcode 符号：

- `{{< ... >}}`
- `{{% ... %}}`

请使用官方 shortcode 文档中记录的 Hugo 规则：

- `%` 符号在 Markdown 之前渲染
- `<` 符号在 Markdown 之后渲染

对于转换，除非文档明确是在讲解 Hugo 语法，否则不要在最终标准 Markdown 中保留这种活跃语法。

## Shortcode 调用规则

在重写 shortcode 之前，请确定以下所有信息：

1. embedded、custom 或 inline
2. 开闭块形式、自闭合形式，或两者皆可
3. 命名参数、位置参数，或两者皆可
4. 是否禁止在同一调用中混用命名与位置参数
5. 该 shortcode 必须使用 `%` 符号还是 `<` 符号调用

这些不是装饰性细节。它们会影响可见输出、目录行为以及内层 Markdown 是否会被渲染。

来自官方 shortcode 文档的重要 Hugo 规则：

- inline shortcode 是一项独立特性，除非显式启用，否则默认禁用
- 某些 shortcode 要求有 body 内容，某些禁止 body，某些则同时支持两种形式
- 命名参数区分大小写
- 命名参数与位置参数不能在同一个 shortcode 调用中混用
- 多行参数与裸字符串字面量都是合法的 shortcode 语法
- 除 inline shortcode 之外，允许嵌套 shortcode

## 首先对 shortcode 进行分类

在重写任何 shortcode 之前，请将其归入以下组之一：

1. 字面文档示例
2. 围绕本地内容或资源的静态包装器
3. 内容图谱展开器
4. 数据驱动渲染器
5. 外部示例抽取器

该分类应驱动转换策略：

- 字面文档示例：按字面保留
- 静态包装器：替换为普通 Markdown 或 HTML
- 内容图谱展开器：递归解析本地页面或 section
- 数据驱动渲染器：读取所引用的 `data/*` 或本地元数据源
- 外部示例抽取器：检视所引用的本地示例文件，或在无法确定性重建时通过显式注释降级

## 文档站点的自定义 Shortcode

典型的 Hugo 文档站点可能在 `layouts/_shortcodes/` 中定义如下自定义 shortcode：

- `code-toggle`
- `datatable`
- `deprecated-in`
- `eturl`
- `get-page-desc`
- `glossary`
- `glossary-term`
- `hl`
- `img`
- `imgproc`
- `include`
- `module-mounts-note`
- `new-in`
- `newtemplatesystem`
- `per-lang-config-keys`
- `quick-reference`
- `render-list-of-pages-in-section`
- `render-table-of-pages-in-section`
- `root-configuration-keys`
- `syntax-highlighting-styles`

在决定替换方式之前，请阅读本地模板文件。

如果仓库已包含面向 Markdown 导出的 partial 或面向 AI 的模板，请将它们作为站点自身如何扁平化这些构造的证据。在不理解哪些 shortcode 被有意展开、哪些被有意保留的情况下，请勿盲目复制。

## 高影响的本地规则

### 逻辑内容路径

某些 Hugo 文档站点将语言子目录（如 `content/en`）挂载到逻辑上的 `content` 根目录。请基于逻辑路径（而非保留语言前缀的文件系统路径）来解析链接和 `include` 目标。

### `include`

`include` 通过 `RenderShortcodes` 渲染另一内容页面。这意味着：

- 被包含的文件可能包含更多 shortcode
- 被包含的文件是最终可见内容的一部分
- 转换必须递归解析所引用的文件
- 被包含的文件应贡献正文内容，而非重复 front matter

### `quick-reference`

此 shortcode 动态渲染 section 与子页面。请用物化后的 Markdown 结构替换它。

### `render-list-of-pages-in-section`

此 shortcode 基于 section 路径构建列表。请用普通 Markdown 列表与描述替换它。

### `render-table-of-pages-in-section`

此 shortcode 基于 section 路径与筛选器构建表格。在可行时替换为标准 Markdown 表格，否则替换为清晰的列表。

### `glossary-term` 与 `glossary`

它们会注入术语表链接或术语表内容。请保留渲染得到的正文或链接，而非 shortcode 语法。

### `new-in` 与 `deprecated-in`

请将它们转换为纯 Markdown 标注或内联标签，例如：

- `New in Hugo 0.144.0.`
- `Deprecated in Hugo 0.144.0.`

### `code-toggle`

请将底层的示例内容保留为围栏代码，而非 UI 切换机制。

需要留意的常见参数模式：

- `file=hugo` 或类似参数表示仓库风格的配置示例
- `fm=true` 表示所发出的示例包含 front matter 语义
- `config=` 与 `dataKey=` 风格的用法可以从数据中拉取代码片段，因此在扁平化该 shortcode 之前请阅读本地数据文件

如果所需数据源在本地并不明显，或需要你无法安全复现的重新序列化逻辑，请将该 shortcode 替换为：

- 当存在可见的内联示例时使用该示例，或
- 一段简短说明，解释仓库在渲染时由数据生成多种代码变体

### `datatable`

此 shortcode 基于 `hugo.Data.docs` 渲染表格。当所选包、列表与字段集清晰时，请从本地数据物化该表格。

### `per-lang-config-keys` 与 `root-configuration-keys`

这些 shortcode 用于汇总配置元数据。请将它们视为数据驱动展开器，而非简单的徽章或链接。

### `syntax-highlighting-styles` 与 `chroma-lexers`

这些 shortcode 从本地数据或模板逻辑物化大量生成的列表。在可行时优先使用显式的 Markdown 表格或列表，否则以清晰说明降级，描述被省略的生成画廊。

### `newtemplatesystem` 与 `hl`

这些是本地的展示辅助。在决定降级格式之前，请检视它们发出的是正文、徽章还是内联高亮代码。

## 内嵌 Shortcode

官方 Hugo 文档同样记录了内嵌 shortcode。即使源站点主要使用自定义 shortcode，也应将内嵌 shortcode 视为第一类转换用例，因为其他 Hugo 仓库常常直接依赖它们。

高价值的内嵌 shortcode 指引：

- `details`：转换为 Markdown 标注或 HTML `<details>` 块，同时保留 summary 文本与 body 内容
- `figure`：保留图片目标、alt 文本、说明、title 与来源语义；纯 Markdown 图片加周围说明文本通常比保留 shortcode 语法更安全
- `highlight`：当渲染结果是代码示例时，转换为围栏代码；仅在必要时以内联代码或 HTML 形式保留内联高亮
- `param`：若本地可知，则解析为所引用的站点参数；否则替换为转换说明
- `qr`：保留编码后的文本，且仅在本地可解析生成资源时附加说明或图片链接
- `ref` 与 `relref`：用最终解析得到的 Markdown 目标替换，而非保留 shortcode 本身
- `youtube`、`vimeo`、`instagram` 与 `x`：仅当目标明确且安全时才转换为稳定的普通链接或嵌入

如果仓库在 `layouts/_shortcodes` 中覆写了某个内嵌 shortcode，请将本地覆写视为权威。

## Inline Shortcode

Inline shortcode 较为罕见但很重要，因为它们可以在内容中定义可执行的模板逻辑。

转换规则：

- 如果页面是在记录 inline shortcode 语法，请按字面保留示例。
- 如果页面实际上在使用 inline shortcode，且渲染文本在本地是显而易见的，请保留渲染文本而非模板体。
- 如果渲染值依赖于运行时状态（如 `now`、环境变量或构建上下文），请替换为显式说明，而非猜测。

### `glossary-term` 与术语表链接

某些 Hugo 文档站点以两种形式使用术语表快捷方式：

- 使用 `glossary-term` shortcode
- 目标恰好等于 `(g)` 的 Markdown 链接

两者都应在输出中转换为显式的 Markdown 链接或显式的术语表标签。

### `ref` 与 `relref`

当它们以活跃 shortcode 调用而非字面文档示例的形式出现时：

- 将其解析为最终目标
- 在有效时保留查询字符串与 fragment
- 不要在最终 Markdown 中字面发出 `ref` 或 `relref`

在许多现代 Hugo 文档站点中，Markdown 页面通常更倾向于采用基于 render-hook 的目标解析，而非这些 shortcode。

### 其他 Hugo 站点中的内容图谱展开器

其他 Hugo 仓库可能在不同名称下使用具有类似图谱展开行为的 shortcode，例如：

- `embed-md`
- `table-children`
- `command-group`

请将它们视为仓库专属特性。在决定展开的是兄弟页面、子 section 还是数据文件之前，请阅读本地的 shortcode 或 partial 实现。

### 其他 Hugo 站点中的数据驱动与示例抽取型 shortcode

在 Redis 或 Rclone 等文档仓库中，预期会出现如下 shortcode：

- `features-table`
- `optional-features-table`
- `clients-example`
- `jupyter-example`

它们通常依赖于：

- `data/*`
- 生成的元数据文件
- 本地示例源树
- 面向 Markdown 导出的 partial

仅在本地依赖链清晰且确定时进行物化。否则，降级为 `Conversion note:` 块，并保留任何安全的内联内容。

## 字面示例护栏

即使转义的 shortcode 示例出现在围栏代码块之外，当它们属于以下内容时也按字面保留：

- 符号对照表
- 语法教程
- 演示如何调用 shortcode 的内联正文

示例：

```text
{{%/* foo */%}}
{{</* foo */>}}
```

不要使用通用的 shortcode 移除器将其剥离。

## Render Hook

待转换的站点可能为以下对象定义 render hook：

- blockquote
- 代码块
- 链接
- passthrough
- 表格

重要含义：

- Markdown 链接可能针对页面、页面 resource、section resource 或全局 resource 进行解析
- 内容可能依赖于本地对失效链接的校验逻辑
- 渲染得到的 HTML 可能与通用 CommonMark 默认值不同
- blockquote 可以携带 alert 语义，如 note、tip、important、warning 与 caution
- 代码块可以携带文件标签、复制标志、details 包装器、summary、trim 行为与语言重映射
- passthrough hook 可以让数学分隔符成为有意义的内容，而不是原始噪声
- Markdown 属性可能在 render hook 上下文中显现，因此不能盲目剥离

对于具有类似 render-hook 模式的站点：

- 本地仓库覆写了 blockquote、code block、link、passthrough 与 table 的 render hook
- 它记录了 heading 与 image render hook，但并未在 `layouts/_markup/` 中本地覆写
- 本地 link hook 处理术语表简写 `(g)`、校验 fragment，且仅在当前页面不是 leaf bundle 时检查 section resource
- 本地 code block hook 可以基于代码围栏属性添加文件标签、复制按钮、details 包装器、summary、trim 行为与语言重映射

对于链接密集的页面，请在改写链接之前阅读本地的 `render-link.html` 与官方 render-hook 文档。

## 安全的后备格式

如果某个 shortcode 在检视后仍未解析，请用最终 Markdown 中简短的显式说明替换，例如：

```text
> Conversion note: `clients-example` normally renders multi-language tabs. This sample keeps only the inline Redis CLI content.
```

这优于在产物中保留活跃 Hugo 语法或静默丢失语义。