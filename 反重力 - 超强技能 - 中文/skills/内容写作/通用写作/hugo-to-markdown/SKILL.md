---
name: hugo-to-markdown
description: 将 Hugo 文档站点和 Hugo 管理的内容转换为标准 Markdown。当智能体需要检视本地 Hugo 仓库、读取 hugo.toml 或配置文件、content/、archetypes/、layouts/_shortcodes/、layouts/_markup/ 以及相关文档内容，然后生成 Markdown 时使用。触发词：Hugo、Markdown 转换、Hugo 转 Markdown、文档迁移、站点转换、Markdown 导出、shortcode、render hook、front matter、Hugo 站点
risk: unknown
source: https://github.com/chaunsin/agent-skills/tree/master/skills/hugo-to-markdown
source_repo: chaunsin/agent-skills
source_type: community
date_added: 2026-07-01
license: Apache-2.0
license_source: https://github.com/chaunsin/agent-skills/blob/master/LICENSE
---

# Hugo 转 Markdown
## 使用时机

当你需要将 Hugo 文档站点和 Hugo 管理的内容转换为标准 Markdown 时使用本技能。当智能体需要检视本地 Hugo 仓库、读取 hugo.toml 或配置文件、content/、archetypes/、layouts/_shortcodes/、layouts/_markup/ 以及相关文档内容，然后生成 Markdown 时使用。


## 概述

当 Markdown 输出必须来源于本地 Hugo 站点、而非凭通用 Hugo 知识猜测时，使用本技能。转换规则是 Hugo 官方行为与仓库自身配置、shortcode 模板、render hook、archetypes 和内容约定的组合。

目标输出是标准 Markdown：

- 保留纯 Markdown 与 YAML front matter。
- 替换或物化 Hugo 专属构造。
- 在无法安全复现精确渲染时保留语义。
- 优先使用显式的 Markdown 文本，而非保留 Hugo 实时模板语法。
- 在重写任何内容之前，先区分字面 Hugo 语法示例与活跃的 Hugo 特性。

## 官方依据

将仓库自身的 Hugo 配置和模板视为首要规则集。对于任何待转换站点，请在用户提供站点根目录内检视以下规则源：

- `hugo.toml`（或 `hugo.yaml`、`hugo.yml`、`hugo.json`、`config/*`）
- `archetypes/*`
- `data/*`
- `layouts/_shortcodes/*` 或 `layouts/shortcodes/*`
- `layouts/_markup/*`
- `content/**`

同时阅读任何定义 shortcode、front matter、bundle、resource 和 render-hook 行为的本地文档。

当仓库在本地覆写了 Hugo 内置默认值时，不要套用通用默认假设。

## 工作流

### 1. 转换文件前先盘点站点

始终先检视站点级规则。

```bash
python3 scripts/inventory_hugo_rules.py --site-root /path/to/hugo-site
```

针对用户站点的调用示例：

```bash
python3 skills/hugo-to-markdown/scripts/inventory_hugo_rules.py \
  --site-root /path/to/your-hugo-site
```

此盘点步骤对批处理为强制要求。它会识别：

- 当前生效的配置文件
- 模块挂载与内容根目录
- 自定义 shortcode
- 自定义 render hook
- 内容中出现的 front matter 键
- 各内容文件中 shortcode 的使用情况

### 2. 基于仓库规则转换，而非套用通用启发式

先阅读 `references/conversion-workflow.md`，再修改文件。然后：

1. 从 `hugo.toml`、`config.*` 和模块挂载中解析出真实的内容根目录。
2. 阅读 archetypes 以了解期望的 front matter 形态。
3. 阅读 front matter 配置以理解日期别名、回退顺序、由文件名衍生的日期以及其他推导得到的元数据。
4. 当 shortcode 或 partial 从结构化内容源拉取数据时，阅读 `data/` 下的站点数据源。
5. 阅读 `layouts/_shortcodes/` 或 `layouts/shortcodes/` 中的自定义 shortcode 模板。
6. 将每个遇到的 shortcode 归类为 embedded、custom 或 inline，再判断其使用命名参数、位置参数、块语法还是自闭合语法。
7. 阅读 `layouts/_markup/` 中的 render hook。
8. 检查仓库是否已经定义了面向 Markdown 或 JSON 的导出模板与 partial；如果有，将它们作为站点自身如何降级 Hugo 构造的证据加以使用。
9. 当文档站点由共享片段组合内容时，沿 `include` 类 shortcode 进入被引用的内容文件。
10. 一次转换一个文件或一个语义连贯的段落。

### 3. 转换过程中保留语义

默认遵循以下规则：

- 除非用户明确要求无 front matter 的 Markdown，否则保留 YAML front matter。
- 保留仍承载语义的核心里段，如 `title`、`description`、`date`、`draft`、`aliases`、`slug`、`url`、`weight` 以及嵌套的 `params`。
- 当 `publishDate`、`lastmod`、`expiryDate` 及页面 resource 元数据仍影响语义或下游路由时，予以保留。
- 当仓库混用大小写时，将保留的 Hugo front matter 键规范化为规范名称，例如 `Title` 归一为 `title`、`Description` 归一为 `description`、`LinkTitle` 归一为 `linkTitle`。
- 在判定字段是否未使用前，先考虑 Hugo front matter 的别名与令牌。官方 Hugo 文档认可的别名包括 `pubdate`、`published`、`modified` 和 `unpublishdate`，令牌包括 `:default`、`:filename`、`:fileModTime` 与 `:git`。
- 将 Hugo 内部链接转换为具有已解析目标的普通 Markdown 链接。
- 仅在阅读本地 shortcode 实现之后，再将 Hugo shortcode 替换为纯 Markdown、HTML 或显式注释。
- 按照 shortcode 的真实调用约定保留或物化其参数。不要假设每个 shortcode 都是命名参数、自闭合或支持块的。
- 当 shortcode 从 section 或数据文件渲染内容时，物化其动态生成的列表与表格。
- 当文档本身是在记录 Hugo 语法而非调用 Hugo 时，保持其 Hugo 字面示例不变。此规则同时适用于围栏代码块内部，以及正文、表格或符号示例中出现的转义形式（如 `{{</* foo */>}}` 或 `{{%/* foo */%}}`）。
- 当目标 Markdown 方言支持时，保留诸如 `{.class #id}` 的块属性语义以及代码围栏属性。如果不支持，则显式降级，而非静默丢弃。

### 4. 谨慎应用 Hugo 专属正文规则

许多 Hugo 文档站点使用复杂的本地行为。请留意以下常见模式：

- `hugo.toml` 将 `content/en` 挂载到逻辑上的 `content` 根目录，因此链接与 include 解析必须基于 Hugo 逻辑路径，而非盲目保留 `/en/`。
- 文档基础依赖于 Hugo front matter 配置以决定日期解析、别名与文件名衍生的元数据；在规范化日期或 slug 之前，请阅读 `configuration/front-matter.md` 与 `hugo.toml` 中的 `[frontmatter]`。
- `include` 通过 `RenderShortcodes` 渲染另一页面；请跟随被引用的内容文件并将其渲染结果以 Markdown 内联。
- `quick-reference`、`render-list-of-pages-in-section` 与 `render-table-of-pages-in-section` 从 section 生成导航内容；请将它们替换为物化后的 Markdown 列表或表格。
- `glossary-term`、`glossary`、`get-page-desc`、`module-mounts-note`、`new-in` 与 `deprecated-in` 会展开为正文或徽章；请将它们转换为显式的 Markdown 文本或标注。
- `code-toggle` 可能读取配置片段和数据驱动的示例；请保留底层的代码示例，而非 UI 切换控件。
- `datatable`、`per-lang-config-keys`、`root-configuration-keys`、`syntax-highlighting-styles`、`chroma-lexers`、`newtemplatesystem` 与 `hl` 也都是本地 shortcode；在决定是物化、扁平化还是降级之前，请先检视它们的实现。
- 如果仓库存在数据驱动或示例抽取类的 shortcode（如 `features-table`、`optional-features-table`、`clients-example` 或 `jupyter-example`），请在决定物化还是降级之前，检视其引用的 `data/` 文件、本地示例源以及 Markdown 导出 partial。
- 术语表链接可能使用特殊的 Markdown 目标 `(g)`；请将它们解析为稳定的术语表链接，而非保留该占位符。
- `img` 与 `imgproc` 是围绕页面、全局或远程资源的展示辅助；请保留底层的图片引用与说明语义。
- `eturl` 输出指向内嵌模板源码的链接；若目标已知则转换为普通 Markdown 链接，否则以文本注释形式保留。
- 本地链接 render hook 按以下顺序解析目标：内容页面、页面 resource、section resource（仅当页面不是 leaf bundle 时）、全局 resource。它还会校验 fragment 与术语表简写。
- blockquote 与 code-block render hook 会附加 alert、file-label、summary 与 detail 语义；请在 Markdown 或显式注释中保留这些语义。
- 在现代 Hugo 文档中，内嵌的 `ref` 与 `relref` 已不适用于 Markdown，且可能与自定义链接 render hook 产生不良交互；请解析最终目标，而非保留 shortcode。
- 本地文档使用的 Markdown 属性与代码围栏选项可能改变渲染输出。当目标方言支持时，请保留这些语义。

在转换任何包含 Hugo 语法的文件之前，请阅读 `references/shortcodes-and-render-hooks.md`。

### 5. 校验输出

转换后，扫描生成的 Markdown 中残留的 Hugo 专属语法。

```bash
python3 skills/hugo-to-markdown/scripts/check_standard_markdown.py \
  --root /path/to/output
```

若校验器报告围栏代码块之外存在活跃 Hugo 语法，请二选一：

- 完全解析它，或
- 以安全的文本说明替换

不要在产物中遗留未解析的 `{{< ... >}}`、`{{% ... %}}` 或 Go 模板表达式。

### 6. 在无法安全完整物化时显式降级

如果某个 shortcode 依赖于构建期数据、生成式示例或外部源文件，而你无法从本地仓库快照中确定性解析，请将其替换为显式的 Markdown 注释。

使用简短、平实的格式，例如：

- `> Conversion note: <该 shortcode 通常渲染的内容>。`
- 后跟任何能够安全保留的子集，例如内联的 Redis CLI 文本、已解析的图片 URL 或已知的 section 列表

不要留下空链接、损坏的表格单元格或被剥离却没有任何说明的内容。

## Hugo 文档站点的常见模式

在转换表现出类似模式的 Hugo 文档站点时，请参考以下事实：

- `hugo.toml` 将 `content/en` 挂载为 `content`，因此英文文档即为当前生效的内容树。
- Goldmark 配置了 passthrough 分隔符，因此 `$$...$$`、`\\(...\\)` 与 `\\[...\\]` 都是有意义的内容，而非噪声。
- `markup.goldmark.parser.attribute.block = true`，因此块属性语法可能出现在围栏代码块与其他块元素之后。
- `markup.goldmark.parser.wrapStandAloneImageWithinParagraph = false`，因此独立图片的属性可作用于图片本身，而非包裹段落。
- 仓库为 blockquote、code block、link、passthrough 与 table 定义了自定义 render hook。它记录了 heading 与 image render hook，但站点并未在本地覆写。
- 仓库大量使用通过 `% include %` 引用的共享 `_common` 片段，因此仅阅读单个页面文件不足以理解渲染结果。
- 仓库记录了 embedded、custom 与 inline 三类 shortcode，转换逻辑必须在扁平化语法之前区分它们。
- 仓库在示例与 render-hook 解析中大量使用 page bundle 与 page resource，包括 section resource 与挂载的全局 resource。
- 仓库包含大量转义 shortcode 示例，如 `{{</* foo */>}}` 与 `{{%/* foo */%}}`；它们是文档示例，当出现在代码示例、符号表或教程正文中时必须保持字面。

## 安全规则

- 永远不要执行 Hugo 模板、shortcode 或 Go 模板表达式。
- 永远不要将内容文件视为受信任的可执行输入。
- 除非用户明确要求，否则永远不要运行 `hugo`、`npm install`、`go install`、下载的 shell 安装器或任何网络安装步骤。
- 所有转换脚本须保持离线与确定性。
- 读取仅限指定的站点根目录，写入仅限指定的输出根目录。
- 拒绝路径遍历、符号链接逃逸或向所请求输出目录之外写入的企图。
- 不要在生成的 Markdown 中泄漏本地绝对路径、密钥、环境变量或 git 凭据。
- 当无法安全复现精确渲染时，请降级为显式的 Markdown 文本，而非保留 Hugo 实时语法。

## 资源

按需阅读以下文件：

- `references/conversion-workflow.md`
  仓库感知的端到端转换流程。
- `references/front-matter-and-content.md`
  front matter 映射、常见内容约定与字面示例处理。
- `references/shortcodes-and-render-hooks.md`
  Hugo shortcode 符号、文档站自定义 shortcode 与 render hook 的影响。
- `references/links-assets-and-validation.md`
  链接解析、资源、校验与残留处理。

在以下脚本有帮助时使用：

- `scripts/inventory_hugo_rules.py`
  扫描 Hugo 站点并输出规则清单。
- `scripts/check_standard_markdown.py`
  在 Markdown 输出中检测残留的 Hugo 语法与常见的不安全残片。

## 局限性

- 仅当任务明确匹配其上游来源与本地项目上下文时才使用本技能。
- 在应用变更前，请校验命令、生成代码、依赖、凭据以及外部服务行为。
- 不要将示例视为环境专属测试、安全审查或用户对破坏性或高成本操作的批准之替代。