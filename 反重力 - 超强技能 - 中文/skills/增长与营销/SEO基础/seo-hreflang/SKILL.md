---
name: seo-hreflang
description: >
  Hreflang 和国际化 SEO 审计、验证与生成。检测常见错误、验证语言/地区代码并生成正确的 hreflang 实现。当用户提到"hreflang"、"国际化SEO"、"多语言"、"多地区"或"语言标签"时使用。触发词：hreflang、国际化SEO、多语言SEO、多地区SEO、语言标签、i18n SEO
risk: unknown
source: "https://github.com/AgriciDaniel/claude-seo"
date_added: "2026-03-21"
user-invokable: true
argument-hint: "[url]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# Hreflang 与国际化 SEO

## 适用场景
- 验证或生成多语言/多地区网站的 hreflang 时使用
- 用户提到国际化 SEO、语言标签、x-default 或 hreflang 问题时使用
- 审计 HTML、HTTP 头或 sitemap 中的区域替代页面实现时使用

验证现有的 hreflang 实现或为多语言、多地区网站生成正确的 hreflang 标签。支持 HTML、HTTP 头和 XML sitemap 三种实现方式。

## 验证检查项

### 1. 自引用标签
- 每个页面必须包含指向自身的 hreflang 标签
- 自引用 URL 必须与页面的 canonical URL 完全一致
- 缺少自引用标签会导致 Google 忽略整个 hreflang 集合

### 2. 返回标签
- 如果页面 A 通过 hreflang 链接到页面 B，页面 B 也必须链回页面 A
- 每个 hreflang 关系必须是双向的（A→B 和 B→A）
- 缺少返回标签会使两个页面的 hreflang 信号均失效
- 检查所有语言版本是否相互引用（全网格）

### 3. x-default 标签
- 必需：指定未匹配语言/地区的后备页面
- 通常指向语言选择页面或英文版本
- 每组替代页面只能有一个 x-default
- 也必须有来自所有其他语言版本的返回标签

### 4. 语言代码验证
- 必须使用 ISO 639-1 两位字母代码（例如 `en`、`fr`、`de`、`ja`）
- 常见错误：
  - `eng` 而非 `en`（ISO 639-2，hreflang 不接受）
  - `jp` 而非 `ja`（日语的错误代码）
  - `zh` 无地区限定（有歧义；使用 `zh-Hans` 或 `zh-Hant`）

### 5. 地区代码验证
- 可选的地区限定使用 ISO 3166-1 Alpha-2（例如 `en-US`、`en-GB`、`pt-BR`）
- 格式：`language-REGION`（语言小写，地区大写）
- 常见错误：
  - `en-uk` 而非 `en-GB`（UK 不是有效的 ISO 3166-1 代码）
  - `es-LA`（拉丁美洲不是国家；使用具体国家代码）
  - 地区缺少语言前缀

### 6. Canonical URL 对齐
- hreflang 标签只能出现在 canonical URL 上
- 如果页面的 `rel=canonical` 指向其他地址，该页面上的 hreflang 会被忽略
- canonical URL 和 hreflang URL 必须完全匹配（包括尾部斜杠）
- 非 canonical 页面不应出现在任何 hreflang 集合中

### 7. 协议一致性
- 同一 hreflang 集合中的所有 URL 必须使用相同协议（HTTPS 或 HTTP）
- hreflang 集合中混合 HTTP/HTTPS 会导致验证失败
- HTTPS 迁移后，将所有 hreflang 标签更新为 HTTPS

### 8. 跨域支持
- hreflang 可跨不同域名工作（例如 example.com 和 example.de）
- 跨域 hreflang 需要在两个域名上都有返回标签
- 验证两个域名均已在 Google Search Console 中验证
- 跨域场景推荐使用基于 sitemap 的实现方式

## 常见错误

| 问题 | 严重程度 | 修复 |
|------|----------|------|
| 缺少自引用标签 | 严重 | 添加指向同一页面 URL 的 hreflang |
| 缺少返回标签（A→B 但无 B→A） | 严重 | 在所有替代页面上添加匹配的返回标签 |
| 缺少 x-default | 高 | 添加指向后备/选择页面的 x-default |
| 无效的语言代码（如 `eng`） | 高 | 使用 ISO 639-1 两位字母代码 |
| 无效的地区代码（如 `en-uk`） | 高 | 使用 ISO 3166-1 Alpha-2 代码 |
| 非 canonical URL 上的 hreflang | 高 | 将 hreflang 仅放在 canonical URL 上 |
| URL 中 HTTP/HTTPS 不匹配 | 中 | 将所有 URL 统一为 HTTPS |
| 尾部斜杠不一致 | 中 | 严格匹配 canonical URL 格式 |
| hreflang 同时存在于 HTML 和 sitemap 中 | 低 | 选择一种方式（大站推荐 sitemap） |
| 需要地区时仅使用语言 | 低 | 为地理定向内容添加地区限定 |

## 实现方式

### 方式一：HTML Link 标签
适用于：每页少于 50 个语言/地区变体的网站。

```html
<link rel="alternate" hreflang="en-US" href="https://example.com/page" />
<link rel="alternate" hreflang="en-GB" href="https://example.co.uk/page" />
<link rel="alternate" hreflang="fr" href="https://example.com/fr/page" />
<link rel="alternate" hreflang="x-default" href="https://example.com/page" />
```

放在 `<head>` 部分。每个页面必须包含所有替代版本（包括自身）。

### 方式二：HTTP 头
适用于：非 HTML 文件（PDF、文档）。

```
Link: <https://example.com/page>; rel="alternate"; hreflang="en-US",
      <https://example.com/fr/page>; rel="alternate"; hreflang="fr",
      <https://example.com/page>; rel="alternate"; hreflang="x-default"
```

通过服务器配置或 CDN 规则设置。

### 方式三：XML Sitemap（推荐用于大型网站）
适用于：语言变体多、跨域部署或超过 50 页的网站。

参见下方 Hreflang Sitemap 生成部分。

### 方式对比
| 方式 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| HTML link 标签 | 小型网站（<50 变体） | 实现简单，源码中可见 | 膨胀 `<head>`，大规模难维护 |
| HTTP 头 | 非 HTML 文件 | 适用于 PDF、图片 | 服务器配置复杂，HTML 中不可见 |
| XML sitemap | 大型网站、跨域 | 可扩展，集中管理 | 页面中不可见，需维护 sitemap |

## Hreflang 生成

### 流程
1. **检测语言**：扫描网站的语言标识（URL 路径、子域名、TLD、HTML lang 属性）
2. **映射等价页面**：匹配不同语言/地区间的对应页面
3. **验证语言代码**：对照 ISO 639-1 和 ISO 3166-1 验证所有代码
4. **生成标签**：为每个页面创建 hreflang 标签（包括自引用）
5. **验证返回标签**：确认所有关系均为双向
6. **添加 x-default**：为每组页面设置后备
7. **输出**：生成实现代码（HTML、HTTP 头或 sitemap XML）

## Hreflang Sitemap 生成

### 带 Hreflang 的 Sitemap
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.com/page</loc>
    <xhtml:link rel="alternate" hreflang="en-US" href="https://example.com/page" />
    <xhtml:link rel="alternate" hreflang="fr" href="https://example.com/fr/page" />
    <xhtml:link rel="alternate" hreflang="de" href="https://example.de/page" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/page" />
  </url>
  <url>
    <loc>https://example.com/fr/page</loc>
    <xhtml:link rel="alternate" hreflang="en-US" href="https://example.com/page" />
    <xhtml:link rel="alternate" hreflang="fr" href="https://example.com/fr/page" />
    <xhtml:link rel="alternate" hreflang="de" href="https://example.de/page" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/page" />
  </url>
</urlset>
```

关键规则：
- 包含 `xmlns:xhtml` 命名空间声明
- 每个 `<url>` 条目必须包含所有语言替代版本（包括自身）
- 每个替代版本必须作为单独的 `<url>` 条目出现，并包含其自身的完整集合
- 每个 sitemap 文件最多 50,000 个 URL

## 输出

### Hreflang 验证报告

#### 摘要
- 已扫描页面总数：XX
- 检测到的语言变体：XX
- 发现的问题：XX（严重：X，高：X，中：X，低：X）

#### 验证结果
| 语言 | URL | 自引用 | 返回标签 | x-default | 状态 |
|------|-----|--------|----------|-----------|------|
| en-US | https://... | ✅ | ✅ | ✅ | ✅ |
| fr | https://... | ❌ | ⚠️ | ✅ | ❌ |
| de | https://... | ✅ | ❌ | ✅ | ❌ |

### 生成的 Hreflang 标签
- HTML `<link>` 标签（如选择 HTML 方式）
- HTTP 头值（如选择 HTTP 头方式）
- `hreflang-sitemap.xml`（如选择 sitemap 方式）

### 建议
- 需要补充的缺失实现
- 需要修复的错误代码
- 方式迁移建议（例如从 HTML 迁移到 sitemap 以应对规模化需求）

## 错误处理

| 场景 | 操作 |
|------|------|
| URL 不可达（DNS 失败、连接被拒） | 清晰报告错误。不要猜测网站结构。建议用户验证 URL 后重试。 |
| 未找到 hreflang 标签 | 报告缺失情况。检查其他国际化信号（子目录、子域名、ccTLD）并推荐合适的 hreflang 实现方式。 |
| 检测到无效的语言/地区代码 | 列出每个无效代码及正确替换。提供可直接实现的修正后 hreflang 标签集。 |

## 限制条件
- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出视为环境特定验证、测试或专家评审的替代品
- 如缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清
