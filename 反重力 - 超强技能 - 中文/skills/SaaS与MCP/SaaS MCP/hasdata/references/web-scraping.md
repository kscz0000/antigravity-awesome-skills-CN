# 网页抓取 API —— `POST /scrape/web`

一个端点用于抓取任意 URL，可选地支持 JS 渲染、代理、AI 提取和截图。同步。

> 仅在用户提供具体 URL 或没有对应的 Scraper API 时才使用此端点。否则平台专用 API 返回预提取的 JSON 而无需直接访问页面。仅用于公开页面或用户有权访问的内容。

## 最简请求

```python
import requests

# Multiple outputs (or include "json") → response is a JSON object
resp = requests.post(
    "https://api.hasdata.com/scrape/web",
    headers={"x-api-key": API_KEY},
    json={"url": "https://example.com", "outputFormat": ["markdown", "json"]},
    timeout=300,
)
data = resp.json()
assert data["requestMetadata"]["status"] == "ok"
print(data["markdown"])

# Single non-JSON output → response IS the raw content (markdown/html/text bytes)
resp = requests.post(
    "https://api.hasdata.com/scrape/web",
    headers={"x-api-key": API_KEY},
    json={"url": "https://example.com", "outputFormat": ["markdown"]},
    timeout=300,
)
print(resp.text)            # raw markdown — no JSON parsing
```

## Body 参数

| 参数 | 类型 | 说明 |
|---|---|---|
| `url` | string | **必填。** 绝对 URL。 |
| `outputFormat` | string[] | `html`、`text`、`markdown`、`json`。**单一非 JSON 格式 → 原始内容作为 body**（不包裹在 JSON 中）；多种格式 → 每个格式对应一个键的 JSON 对象。当您还需要 `requestMetadata` 时，请始终包含 `"json"`（或另一种格式）。 |
| `proxyType` | enum | `datacenter`（默认）或 `residential` —— 仅在条款和访问控制允许的授权地理 / 可用性测试中使用 residential。 |
| `proxyCountry` | string | ISO 3166-1 alpha-2 —— `US`、`UK`、`DE`、`FR`、`IT`、`SE`、`BR`、`CA`、`JP`、`SG`、`IN`、`ID`、`IE`。 |
| `jsRendering` | bool | 无头浏览器 —— SPA 和动态注入内容所必需。 |
| `wait` / `waitFor` | int (ms) / CSS string | 固定延迟 vs. 等待选择器出现。优先使用 `waitFor`。 |
| `jsScenario` | array | 一系列 click/fill/wait/scroll/evaluate 操作。需要 `jsRendering`。 |
| `headers` | object | 自定义请求头。**Cookie 也放在这里 —— 没有单独的 `cookies` 参数。** |
| `screenshot` | bool | 在响应中返回一个 CDN URL。 |
| `extractRules` | object | CSS 选择器 → 字段文本。`@attr` 提取属性。**仅第一条匹配**，缺失 → `null`。 |
| `aiExtractRules` | object | 类型化的 LLM 提取。类型：`string`、`number`、`boolean`、`list`、`item`。 |
| `extractEmails` / `extractLinks` | bool | 快速助手。 |
| `blockResources` / `blockAds` | bool | 跳过图片 / CSS / 广告 —— 加速纯文本抓取。 |
| `blockUrls` | string[] | 用于屏蔽子资源的 Glob 模式。 |
| `removeBase64Images` | bool | 从响应中移除内联 base64。 |
| `includeOnlyTags` / `excludeTags` | string[] | 在序列化前裁剪 DOM。 |

## CSS 提取（`extractRules`）

```python
"extractRules": {
    "title": "h1",
    "links": "a @href",   # @attr extracts attribute
    "price": ".price-now",
}
```

每个选择器只取第一条匹配。对于记录列表，请使用 `aiExtractRules` 配合 `type: "list"`。

## AI 提取（`aiExtractRules`）

```python
"aiExtractRules": {
    "title":    {"type": "string"},
    "price":    {"type": "number"},
    "in_stock": {"type": "boolean"},
    "tags":     {"type": "list", "description": "category tags"},
    "author":   {"type": "item", "output": {
        "name":     {"type": "string"},
        "verified": {"type": "boolean"},
    }},
    "reviews":  {"type": "list", "output": {
        "rating": {"type": "number"},
        "text":   {"type": "string"},
    }},
}
```

在页面布局多变时使用；否则优先使用 `extractRules` 以获得确定性和可预测性。

## JS 场景

```python
"jsScenario": [
    {"fill": ["#email", "user@example.com"]},
    {"fill": ["#password", PASSWORD]},
    {"click": "#login"},
    {"waitFor": ".dashboard"},
    {"scrollY": 2000},
    {"waitForAndClick": ".load-more"},
    {"evaluate": "window.__APP_STATE__"},
]
```

操作：`click`、`fill: [sel, val]`、`wait: ms`、`waitFor: sel`、`waitForAndClick: sel`、`scrollX/scrollY: px`、`evaluate: "JS"`。顺序执行。在 `click`/`fill` 时元素缺失会让请求失败 —— 先用 `waitFor` 包裹。

## 通过 Cookie 进行认证

```python
"headers": {
    "User-Agent": "Mozilla/5.0 ...",
    "Cookie": "session=abc; csrf=xyz",
    "Accept-Language": "en-US,en;q=0.9",
}
```

在真实浏览器中抓取一次 Cookie（devtools → Storage → Cookies），通过 `Cookie` 头转发。仅在用户明确许可且您有权访问该账户/内容时使用；切勿使用 Cookie 绕过他人的访问控制。

## 精简响应与提速

```python
{
    "blockResources": True,                       # skip images/CSS/fonts
    "blockAds": True,                             # skip ad/tracking
    "blockUrls": ["**.googletagmanager.com/**", "**.doubleclick.net/**"],
    "removeBase64Images": True,
    "excludeTags": ["script", "style", "nav", "footer"],
}
```

在嘈杂的页面上可将响应大小减少 60–90%。

## 响应结构

包装器仅在响应被 JSON 包裹时为 JSON —— 即多个 `outputFormat` 值，或单个值包含 `"json"`。对于单个非 JSON 格式，响应 body 即原始内容（`text/markdown`、`text/html`、`text/plain`）。

```json
{
  "requestMetadata": { "id": "uuid", "status": "ok", "url": "..." },
  "headers": { "content-type": "text/html" },
  "screenshot": "https://...jpeg",
  "content": "<!DOCTYPE html>...",     // outputFormat: html
  "markdown": "# Title\n...",           // outputFormat: markdown
  "text":     "Title\n...",
  "extractRules":    { ... },           // present iff sent
  "aiExtractRules":  { ... },           // present iff sent
  "extractedEmails": [ ... ],           // iff extractEmails: true
  "extractedLinks":  [ ... ]            // iff extractLinks: true
}
```

## 批处理（`POST /scrape/batch/web`）

>1k URL 运行相同提取的异步包装器。返回 `jobId`；轮询状态，分页 `/results`。单批上限 **10,000 个 URL**。对于小型工作负载，在并发数 = 套餐限额的情况下循环调用同步端点。

## 陷阱

- **优先禁用 `jsRendering`**，仅在页面需要时启用 —— 大多数静态页面无需无头浏览器即可正常解析。
- **`waitFor` > `wait`。** 基于选择器的等待可适应网络速度。
- **Cookie 仅通过 `headers["Cookie"]` 传递。**
- **`extractRules` 返回第一条匹配** —— 对于数组请使用 `aiExtractRules` 的 `type: "list"`。
- **设置客户端超时 ≥ 300 秒** 以匹配服务端截止时间。
- **`requestMetadata.status === "ok"` 是唯一成功信号。**