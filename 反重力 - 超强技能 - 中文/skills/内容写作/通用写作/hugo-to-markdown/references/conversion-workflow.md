# 转换工作流

## 目的

当把 Hugo 文档站点转换为不再依赖 Hugo 运行时特性的标准 Markdown 时，请使用本工作流。

## 步骤 1：定位真实的规则源

按顺序阅读以下内容：

1. `hugo.toml`、`hugo.yaml`、`hugo.yml`、`hugo.json` 或 `config/*`
2. `archetypes/*`
3. `data/*`
4. 定义 shortcode、front matter、bundle、resource 与 render-hook 行为的官方或本地文档
5. `layouts/_shortcodes/*` 或 `layouts/shortcodes/*`
6. `layouts/_markup/*`
7. 面向 Markdown 或 JSON 的导出模板与 partial，如 `layouts/_default/*.md`、`layouts/_default/*.json` 或 `layouts/partials/markdown-*.html`
8. `content/*`

## 步骤 2：构建站点清单

运行：

```bash
python3 skills/hugo-to-markdown/scripts/inventory_hugo_rules.py \
  --site-root /path/to/your-hugo-site
```

检视输出，关注：

- 内容根目录与模块挂载
- 当前生效的 shortcode 名称
- render hook 名称
- 高频使用的 shortcode
- front matter 键
- 影响可见日期或 slug 的 front matter 别名或令牌用法
- shortcode 使用是否聚集在内容图谱展开、section 列表、数据驱动的表格或外部示例抽取

使用清单按复杂度对文件分批：

- 仅纯 Markdown
- 仅 front matter
- 字面 Hugo 文档示例
- 必须保留 Markdown 属性或代码围栏选项的页面
- 使用内置 shortcode 的页面
- 内容图谱类 shortcode（如 `include`、`embed-md`、`glossary-term`、`table-children`）
- 使用自定义 shortcode 的页面
- 使用数据驱动 shortcode 的页面
- 受 render hook 影响的链接与资源

## 步骤 3：一次转换一片

推荐顺序：

1. 纯页面
2. 仅需规范化 front matter 的页面
3. 主要记录 Hugo 语法并包含字面 shortcode 示例的页面
4. 使用共享 include 的页面
5. 使用自定义 shortcode 的页面
6. 内容部分由 section 或数据文件生成的页面
7. 内容依赖于生成式代码示例或外部本地源的页面

这能让回退局部化，并使校验更容易。

## 步骤 4：物化动态内容

若 shortcode 生成正文、列表、表格或徽章，请用渲染结果的 Markdown 替换。

来自 Hugo 文档站点的示例：

- `include` 拉取另一内容文件并渲染其 shortcode
- `quick-reference` 展开 section 内容
- `render-list-of-pages-in-section` 从 section 构建列表
- `render-table-of-pages-in-section` 从 section 页面构建表格
- `glossary` 物化术语表内容

不要在最终的标准 Markdown 中保留这些活跃 Hugo shortcode。

在评估 shortcode 时，请先做以下归类：

1. 围绕内层 Markdown 或简单资源的静态包装器
2. 内容图谱展开至其他页面或 section
3. 使用 `data/*` 的数据驱动展开
4. 从当前页面之外的文件中抽取生成式示例

该归类决定了你能直接物化输出、需要进行递归页面解析、需要读取数据文件，还是必须降级为显式注释。

同时确认 shortcode 是否：

- embedded、custom 或 inline
- 块形式、自闭合形式，或两者皆有
- 命名参数、位置参数，或两者皆可

这些选择会影响你如何解析调用，以及需要物化多少 Hugo 原本会渲染的周边 Markdown。

## 步骤 5：保持字面 Hugo 示例的字面性

文档站点经常记录 Hugo 语法本身。请区分：

- 影响渲染的活跃 shortcode 调用
- 面向读者的转义 shortcode 示例

常见的字面示例模式：

```text
{{</* shortcode arg=value */>}}
```

当该构造位于围栏代码块内或显然是文档内容时，请按字面保留。

当以下转义形式出现在正文或表格中时，同样按字面保留：

```text
{{%/* foo */%}}
{{</* foo */>}}
```

不要仅仅因为它们匹配了宽松的 shortcode 正则就将其剥离。

## 步骤 6：在构建衍生内容前规范化 front matter

在使用 front matter 填充生成的表格或列表之前：

- 不区分大小写地映射保留键，例如将 `Title` 映射为 `title`
- 将 `linkTitle` 与 `LinkTitle` 视为同一逻辑字段
- 考虑 `publishdate` 或 `modified` 等别名
- 在判断元数据是否派生时，考虑 `:filename` 与 `:fileModTime` 等 front matter 令牌
- 保留未知的自定义键不变

这样可避免仓库混用 Hugo 键大小写约定时出现空链接与缺失描述。

## 步骤 7：积极校验

每一批处理后，运行：

```bash
python3 skills/hugo-to-markdown/scripts/check_standard_markdown.py \
  --root /path/to/output
```

除非校验命中是围栏代码块内的有意示例，否则将其视为未完成的工作。

如果你有意将某个 shortcode 降级为说明性注释，则该注释应保留在输出中，而原始 shortcode 不应再出现。