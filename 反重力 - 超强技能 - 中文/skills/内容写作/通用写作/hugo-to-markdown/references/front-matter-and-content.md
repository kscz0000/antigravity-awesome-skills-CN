# Front Matter 与内容规则

## Front Matter 策略

默认在输出中使用 YAML front matter，除非用户明确要求去除元数据。

当字段在目标产物中仍承载语义时予以保留：

- `title`
- `linkTitle`
- `description`
- `date`
- `publishDate`
- `lastmod`
- `expiryDate`
- `draft`
- `aliases`
- `slug`
- `url`
- `weight`
- `categories`
- `keywords`
- `params`
- `menus` 或类似菜单的数据

不要凭空添加原本不存在的字段。

若仓库为保留的 Hugo 字段混用大小写，请在输出中规范化为文档化的规范形式：

- `Title` -> `title`
- `Description` -> `description`
- `LinkTitle` -> `linkTitle`

在使用 front matter 构建列表、表格或链接标签前先进行该规范化。除非用户要求改写 schema，否则以原始拼写保留未知的自定义键。

## 有效值规则

不要把 front matter 当作扁平键值拷贝问题。在 Hugo 中，某些可见值是由配置、别名、文件名或 Git 元数据推导而来。

对于源站点，请在判定哪个值是权威值之前，先查阅站点专属的 front matter 文档以及本地的 `[frontmatter]` 配置。

重要的别名规则：

- `publishDate` 可来源于 `publishdate`、`pubdate` 或 `published`
- `lastmod` 可来源于 `lastmod` 或 `modified`
- `expiryDate` 可来源于 `expirydate` 或 `unpublishdate`

重要的令牌规则：

- `:default` 表示 Hugo 会按文档化的默认日期顺序回退
- `:filename` 可由日期前缀的文件名推导 `date`，有时也推导 `slug`
- `:fileModTime` 可由文件修改时间提供日期
- `:git` 在启用时可由 Git 历史提供日期

转换指引：

- 当源字段已是具体且有意义的，予以保留。
- 若仓库依赖别名或令牌解析，请勿因缺少规范键就误删相关元数据。
- 若能从本地快照确定性地解析派生的日期或 slug，且用户希望扁平化输出，请显式物化。
- 若确定性解析需要 Git 状态、构建执行或缺失的元数据，请保留源字段并附加简短的转换说明，而非猜测。

## Resource 元数据

Front matter 还可以描述页面 resource，而不仅仅是页面元数据。

当 `resources` 元数据影响以下方面时，请保留：

- 图片或文件标签
- 按 `Name` 查找 resource
- 用于生成链接文本的标题
- 自定义 `params`
- 通配符驱动的赋值

在 Hugo 的页面 resource 规则中，匹配顺序至关重要，且 `name` 和 `title` 可使用 `:counter` 占位符。除非目标明确不需要，否则不要将这些结构简化掉。

## Archetype 信号

在规范化 front matter 之前先阅读 archetypes。在典型的 Hugo 文档站点中：

- `archetypes/default.md` 确立了公共字段
- `archetypes/functions.md` 添加嵌套的 `params.functions_and_methods`
- `archetypes/methods.md` 遵循同样的方法元数据模式
- `archetypes/glossary.md` 与 `archetypes/news.md` 引入了内容类型专属字段

当 archetype 或本地内容约定引入嵌套字段时，请保留其形态，除非用户要求简化的 schema。

## 内容组合规则

页面文件并不总是完整的事实来源。还需检查：

- 共享的 `_common` 内容片段
- 由 shortcode 生成的正文
- 来自 `data/*` 的数据驱动 shortcode 输入
- 本地 shortcode 引用的生成式示例源文件
- 由 render hook 驱动的链接行为
- 页面 bundle resource 与 section resource
- 来自页面自身 front matter 的页面 resource 元数据
- 决定日期、slug 与发布状态如何派生的 front matter 配置

## 字面示例与活跃语法

在以下情况下保留字面 Hugo 示例：

- 位于围栏代码块内
- 通过注释标记（如 `/* ... */`）明确转义
- 属于解释 Hugo 语法的教程正文

需要保留的重要转义形式：

- `{{</* foo */>}}`
- `{{%/* foo */%}}`
- 在表格或内联代码中比较 `%` 与 `<` shortcode 形式的符号示例

不要仅因为它们出现在围栏代码块之外就将其视为活跃 shortcode 调用。

对于改变渲染页面的活跃语法，请执行转换。

## 显式降级策略

当本地 shortcode 无法安全物化时：

- 移除活跃 Hugo 语法
- 用简短的 Markdown 说明替换
- 保留页面源中已经可见的任何安全子集

示例：

- 即使无法重建多语言 tabset，也保留内联的 Redis CLI 文本
- 即使外层展示包装是自定义的，也保留已解析的图片 URL
- 在无法重建构建期数据表时，保留 section 用途并附加说明

## 应保留的 Markdown 特性

在可能的情况下保留：

- 围栏代码块
- 表格
- 引用块
- 当目标 Markdown 方言支持时的定义列表
- 当目标支持数学时的数学 passthrough 分隔符
- 仅当目标方言支持时的块属性
- 标题属性，如 `## Heading {#id .class}`
- 当目标方言支持时的代码围栏属性与高亮选项

如果目标不支持某项特性，请显式降级，而不是丢弃内容。