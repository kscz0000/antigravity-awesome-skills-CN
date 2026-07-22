# web-scraping 参考

子命令：`web-scraping`（10 积分/调用）。单一端点处理任意 URL 爬取，支持 JS 渲染、代理、AI 抽取、截图、markdown 转换。

> **`web-scraping` 是最后手段，不是默认选项。** 在用它之前先问：`google-serp`（或 `google-news` / `google-shopping` / `google-maps`）是不是已经有我需要的字段？Google 的 `.knowledge_graph`、`.organic_results[].snippet`、`.local_results[]` 已经预先抽取好公开事实，不必直接访问页面。只在以下情况调用 `web-scraping`：
> >
> > - 用户给了你具体的 URL 让读，或
> > - SERP 对某个具体字段没用，或
> > - 目标页面渲染的内容不会出现在任何 SERP 摘要里。
> >
> > 仅对公开页面或用户有权访问的内容使用，并遵守站点条款、robots/访问控制、隐私法和速率限制。
> >
> > 参见 `references/enrichment.md` 了解 SERP 优先的模式。

```bash
hasdata web-scraping --url "URL" [flags] --raw | jq .
```

## 必填

- `--url URL` ——目标页

## 输出格式

- `--output-format html|text|markdown|json`（可重复）
  - 单格式 → 直接返回该格式（如 `--output-format markdown` 把 markdown 文本放在 `.markdown` 下）
  - 多格式 → JSON 响应，每个格式一个 key
  - `--output-format json` 配合其他格式 → 把全部包在 JSON 里

```bash
# LLM-friendly markdown for prompt context
hasdata web-scraping --url "$URL" --output-format markdown --raw | jq -r .markdown
```

## 代理与渲染

- `--proxy-type datacenter|residential`（默认 datacenter）
- `--proxy-country US|UK|DE|IE|FR|IT|SE|BR|CA|JP|SG|IN|ID`（默认 US）
- `--js-rendering` / `--no-js-rendering`（默认开启）——完整无头浏览器
- `--block-ads` / `--no-block-ads`（默认开启）
- `--block-resources` / `--no-block-resources`（默认开启）——为加速屏蔽图片/CSS
- `--screenshot` / `--no-screenshot`（默认开启；结果会包含截图 URL）
- `--remove-base64-images` ——从响应中剥除内联 base64 图片
- `--extract-emails` / `--no-extract-emails`（默认开启）
- `--extract-links`（默认关闭）

## 等待控制

- `--wait MS` ——页面加载后固定等待
- `--wait-for "CSS_SELECTOR"` ——等到该选择器出现

## 自定义 JS 场景（复杂数组——仅 JSON）

```bash
hasdata web-scraping --url "$URL" \
  --js-scenario-json '[
    {"wait": 2000},
    {"click": ".load-more"},
    {"waitFor": ".item"},
    {"scrollY": 1000},
    {"fill": ["input#q", "espresso"]}
  ]' --raw
```

支持的动作：`evaluate`、`click`、`wait`、`waitFor`、`waitForAndClick`、`scrollX`、`scrollY`、`fill`。按顺序执行。

接受原始 JSON、`@file.json` 或 `-`（stdin）。

## 请求头（kvSlice + JSON 转义）

```bash
# Repeatable kv form (splits on first `=`)
hasdata web-scraping --url "$URL" \
  --headers "User-Agent=hasdata-cli" \
  --headers "Accept-Language=en-US,en;q=0.9" \
  --headers "Cookie=session=abc=def" \
  --raw

# JSON base + kv overrides
hasdata web-scraping --url "$URL" \
  --headers-json '{"User-Agent":"base","X-Common":"shared"}' \
  --headers "User-Agent=override" \
  --raw
```

## CSS 选择器数据抽取（kvSlice 或 JSON）

```bash
# Lightweight kv form: --extract-rules KEY=SELECTOR
hasdata web-scraping --url "https://quotes.toscrape.com" \
  --extract-rules "quote=.quote .text" \
  --extract-rules "author=.quote .author" \
  --raw | jq .

# JSON form for complex selectors / attributes
hasdata web-scraping --url "$URL" \
  --extract-rules-json '{"title":"h1","links":"a @href","price":".price-now"}' \
  --raw
```

`@href`、`@src` 等抽取属性。不带 `@` 则抽取文本内容。

## AI 抽取（LLM 驱动）

```bash
hasdata web-scraping --url "$URL" \
  --ai-extract-rules-json '{
    "headline": {"type": "string", "description": "the main story headline"},
    "comments_count": {"type": "number"},
    "is_paid_content": {"type": "boolean"},
    "tags": {"type": "list", "description": "topic tags"},
    "author": {"type": "item", "output": {
      "name": {"type": "string"},
      "verified": {"type": "boolean"}
    }}
  }' --raw | jq .
```

支持的类型：`string`、`number`、`boolean`、`list`、`item`（嵌套对象——其形状在 `output` 下定义）。

## 标签过滤

- `--include-only-tags "main,article"`（逗号连接的 CSS 选择器）——只保留匹配的元素
- `--exclude-tags script --exclude-tags style`（可重复）——移除元素

```bash
hasdata web-scraping --url "$URL" \
  --output-format markdown \
  --include-only-tags "article,main" \
  --exclude-tags script --exclude-tags style --exclude-tags nav \
  --raw | jq -r .markdown
```

## URL 黑名单

```bash
--block-urls-json '["**.googletagmanager.com/**","**.doubleclick.net/**"]'
```

Glob 模式屏蔽特定子资源 URL 加载。

## 保存二进制输出

`web-scraping` 响应是 JSON，但如果 `--output-format` 设置为单一非 JSON 格式，包出来的结果仍是 JSON。用 `jq -r .markdown > file.md` 提取文本。截图特殊一点，响应里包含截图 URL——用 `curl` 单独取。

## 非显式用例

- **页 → prompt grounding** ——`--output-format markdown` 从任意 URL 生成干净的 LLM 可用文本。用 `--exclude-tags script --exclude-tags style --exclude-tags nav` 剥掉导航/广告。比 fetch + 正则强。
- **`curl` 读不到的 JS 渲染 SPA** ——默认 `--js-rendering` 用真实浏览器，React/Vue/Angular 页面会返回水合后的 DOM，不会是空壳。
- **合法范围内的地理/可用性测试** ——`--proxy-type residential` 可模拟住宅网络可用性；仅在目标条款和访问控制允许的授权测试中使用。
- **地理定向内容** ——`--proxy-country DE` 看德国用户看到什么（不同的价格、币种、A/B 版本或地理限制内容）。
- **快速"页面真假"检查** ——`--screenshot`（默认开启）在响应里返回截图 URL；不用手动打开 URL 就能视觉验证。
- **通用价格抽取器** ——`--ai-extract-rules-json '{"price":{"type":"number"},"currency":{"type":"string"},"in_stock":{"type":"boolean"}}'` 可作用于任意零售页面，不必写 CSS 选择器。当用户只需要偶尔抽查时，比维护每个站点的选择器便宜。
- **用户授权的认证内容** ——`--headers Cookie=session=...` 注入认证 cookie。仅在用户明确许可并有权访问该账号/内容时使用；绝不用 cookie 绕过他人的访问控制。
- **分页列表转干净记录集** ——组合 `--js-scenario-json`（点 5 次"加载更多"）和 `--ai-extract-rules-json`（拉取列表形状）。一次 CLI 调用就能扫分页 SPA，不用 N 次。
- **布局的无头截图** ——设 `--js-rendering`、`--no-block-resources`（让 CSS 加载），从响应里拿截图 URL。用于"渲染这个 URL 让我看看长什么样"。
- **RAG 摄取用的 markdown** ——把多个 URL 的 `.markdown` 灌进 JSONL 语料；嵌入并存储。CLI 自己处理 JS、广告、图片，不需要自定义流水线。
- **其他 API 都不存在时的回退** ——当某个垂直没有专用 API（小众目录、政府页面、冷门房产站），`web-scraping` 就是兜底。
- **检测内容变更** ——定时跑 `web-scraping --url X --output-format markdown` 并对多次输出做 diff，捕获定价页或服务条款变更。
- **读 PDF / 非 HTML 资源** ——`--output-format text` 可作用于 URL 可达、可提取文本的 PDF（底层渲染器会处理）。
- **表单/表格的 AI 抽取** ——HTML 表格里结构化数据很容易：`--ai-extract-rules-json '{"rows":{"type":"list","output":{"name":{"type":"string"},"value":{"type":"number"}}}}'`。模型填充嵌套行。

## 常见模式

```bash
# Full-page markdown for RAG
hasdata web-scraping --url "$URL" \
  --output-format markdown --no-screenshot --no-block-resources \
  --raw | jq -r .markdown >> corpus.md

# JS-heavy SPA: wait + scroll
hasdata web-scraping --url "$URL" \
  --js-scenario-json '[{"wait":2000},{"scrollY":2000},{"wait":1500}]' \
  --wait-for ".item" \
  --output-format html --raw | jq -r .html

# Extract structured data from an arbitrary page
hasdata web-scraping --url "$URL" \
  --ai-extract-rules-json '{"price":{"type":"number"},"in_stock":{"type":"boolean"}}' \
  --raw | jq .
```