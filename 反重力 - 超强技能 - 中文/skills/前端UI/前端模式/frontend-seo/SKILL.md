---
name: frontend-seo
description: 面向任意 React 或 React Native-for-web 前端的可移植、框架无关 SEO 系统。把站点元数据集中到一个 constants 模块，从单一基址派生规范 URL，按路由构建元数据（title、description、canonical、Open Graph、Twitter/X 卡片），生成 sitemap、robots 与 RSS，并输出带类型的 JSON-LD。触发词：SEO、搜索引擎优化、sitemap、robots、JSON-LD、canonical、metadata、Open Graph、Twitter cards。
risk: unknown
source: https://github.com/stareezy-1/frontend-architecture-skill/tree/main/skills/frontend-seo
source_repo: stareezy-1/frontend-architecture-skill
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/stareezy-1/frontend-architecture-skill/blob/main/LICENSE
---

# Frontend SEO（可移植、基于 builder）
## 何时使用

当你需要一套面向任意 React 或 React Native-for-web 前端的可移植、框架无关的 SEO 系统时使用本技能。把站点元数据集中到一个 constants 模块，从单一基址派生规范 URL，按路由构建元数据（title、description、canonical、Open Graph、Twitter/X 卡片），生成……


> 可移植技能 — Claude Code、OpenCode、Codex、Cursor、Windsurf 等均可阅读。
> 本技能描述的是一个 **SEO 系统**——一组纯 builder 函数加一个轻量
> 框架适配器——而非组件库或视觉样式。
> 它与 **frontend-architecture** 技能配套使用：SEO 系统位于单一
> 服务模块（`services/seo/`），通过一个 barrel 统一对外暴露。

目标：每条路由都能交付**正确、一致、机器可读的元数据**，无需
任何人手抄 `<meta>` 标签。站点身份集中于**一个** constants 模块，URL
**始终是绝对且规范的**，搜索引擎从应用已经在渲染的同一份内容中派生
**sitemap、robots 规则、RSS 订阅以及类型化的 JSON-LD**。

---

## 0. 五条核心原则

1. **身份信息的唯一来源。** 站点 URL、名称、描述、关键词、作者、社交账号、OG 图片、验证令牌，都集中在一个 `constants/seo` 模块里。任何其他位置都不硬编码站点身份。
2. **URL 始终是绝对且规范的。** 一个 `canonicalUrl(path)` 函数把任意路径转换为绝对、规范化、去除尾部斜杠的 URL。每条 sitemap 条目、每个 RSS 链接、每条 OG URL、每个 JSON-LD `@id` 都经过它。
3. **Builder 是纯函数；适配器很薄。** 元数据、sitemap、robots、RSS 和 JSON-LD 都由纯函数生成，输入数据、返回普通对象。只有一个小函数接触框架的元数据类型。纯函数天然易于单元测试。
4. **结构化数据是类型化且可复用的。** JSON-LD 对象共享 `JsonLd` 类型和一小套 `schema.org` builder（`Person`、`WebSite`、`BlogPosting`、`CreativeWork`、`BreadcrumbList`、`FAQPage`）。实体之间通过稳定的 `@id` 相互引用。
5. **发现面从内容派生。** `sitemap.xml`、`robots.txt` 和 RSS 订阅都由应用渲染的同一份内容集合生成——绝不手写，绝不漂移。

下面所有内容都是这五条原则的机械化落地。

---

## 1. 目录布局

SEO 系统是一个服务模块加上它的常量与类型。它直接对接
`frontend-architecture` 形态（`shared/` 或 `services/`）。

```
src/
├── constants/
│   └── seo.ts                  ← SINGLE source of truth for site identity
├── types/
│   └── seo.ts                  ← SchemaType, RouteDescriptor, SitemapEntry,
│                                  RobotsConfig, RssItem, Redirect, JsonLd
├── services/seo/
│   ├── index.ts                ← barrel: canonicalUrl, buildMetadata,
│   │                              sitemapEntries, robots, rssItems,
│   │                              structuredData, redirects
│   └── structured-data.ts      ← per-type JSON-LD builders (Person, WebSite, …)
└── app/ (or routes/)           ← THIN adapter: route files call the builders
    ├── layout.tsx              ← global default metadata (from constants/seo)
    ├── sitemap.ts              ← mounts sitemapEntries()
    ├── robots.ts               ← mounts robots()
    └── feed.xml/route.ts       ← mounts rssItems()
```

经验法则：**builder 永不导入框架**（唯一的 `buildMetadata` 适配器除外）；
**路由文件永不内联构建 SEO 数据**——它们调用 builder 并挂载结果。

---

## 2. 身份信息的唯一来源（`constants/seo`）

站点身份相关的每一项都是一个具名常量。不会有散落在路由文件里的裸字符串，
不会有重复的描述副本，不会有硬编码的基础 URL。

```ts
// constants/seo.ts
export const SITE_URL = "https://example.com"; // no trailing slash
export const SITE_NAME = "Jane Doe";
export const SITE_HANDLE = "@janedoe";
export const SITE_LOCALE = "en_US";

export const SITE_TITLE_DEFAULT = "Jane Doe — Senior Engineer";
export const SITE_TITLE_TEMPLATE = "%s | Jane Doe"; // child pages fill %s

export const SITE_DESCRIPTION =
  "Senior engineer building cross-platform products with React and TypeScript.";

export const SITE_KEYWORDS = ["Jane Doe", "React", "TypeScript", "Engineer"];

export const AUTHOR_NAME = "Jane Doe";
export const AUTHOR_EMAIL = "jane@example.com";
export const AUTHOR_GITHUB = "https://github.com/janedoe";
export const AUTHOR_LINKEDIN = "https://www.linkedin.com/in/janedoe/";

export const OG_IMAGE_PATH = "/og-image.png"; // relative; canonicalized at use
export const OG_IMAGE_WIDTH = 1200;
export const OG_IMAGE_HEIGHT = 630;

export const GOOGLE_SITE_VERIFICATION = "your-search-console-token";
```

原因：修改描述或 OG 图片只需改动**一行**。结构化数据、OG 标签和
Twitter 卡片都读取同一份值，因此它们绝不会相互不一致。

---

## 3. 类型化数据模型（`types/seo`）

精简但带类型。这些是每个 builder 都要遵守的契约。

```ts
// types/seo.ts
export type SchemaType =
  | "Person"
  | "WebSite"
  | "BlogPosting"
  | "CreativeWork"
  | "BreadcrumbList"
  | "FAQPage";

/** Describes a route for metadata generation. */
export interface RouteDescriptor {
  path: string; // e.g. "/blog/my-post"
  title: string;
  description: string;
  ogImage?: string; // falls back to OG_IMAGE_PATH
  indexable?: boolean; // whether it appears in the sitemap
}

export interface SitemapEntry {
  url: string; // absolute
  lastModified?: string;
  changeFrequency?:
    | "always"
    | "hourly"
    | "daily"
    | "weekly"
    | "monthly"
    | "yearly"
    | "never";
  priority?: number;
}

export interface RobotsConfig {
  rules: Array<{ userAgent: string; allow?: string[]; disallow?: string[] }>;
  sitemap: string; // absolute
}

export interface RssItem {
  title: string;
  link: string; // absolute
  description: string;
  pubDate: string; // ISO-8601
  guid: string;
}

export interface Redirect {
  source: string;
  destination: string;
  permanent: boolean; // 301 when true
}

/** A JSON-LD object: always a schema.org context + type, plus type-specific fields. */
export interface JsonLd {
  "@context": "https://schema.org";
  "@type": SchemaType;
  [key: string]: unknown;
}
```

注意：`frontend-architecture` 中 `I` 前缀约定只适用于**有状态的 UI 接口**；
这里的 SEO 数据模型是普通的 DTO，沿用源项目已有的命名约定
（此处为无前缀）。沿用宿主项目已有的约定——一致性更重要。

---

## 4. 规范 URL（系统的脊梁）

一个函数，全局统一使用。它保证 URL 是绝对的、规范化的、不含双斜杠，
搜索引擎绝不会看到同一页面的两个 URL。

```ts
// services/seo/index.ts
import { SITE_URL } from "@/constants/seo";

export function canonicalUrl(path: string): string {
  const normalized = path.startsWith("/") ? path : `/${path}`;
  if (normalized === "/") return SITE_URL; // root → base, no trailing slash
  const withoutTrailing = normalized.endsWith("/")
    ? normalized.slice(0, -1)
    : normalized;
  return `${SITE_URL}${withoutTrailing}`;
}
```

**硬性规则：**

- 永远不要手写 `SITE_URL + path` 拼接——始终使用 `canonicalUrl(path)`。
- 选定一套尾部斜杠策略（本技能：**无尾部斜杠**）并在所有地方一致应用。
- 每条 OG `url`、sitemap `url`、RSS `link` 以及 JSON-LD `@id`/`url` 都必须经过 `canonicalUrl`。

---

## 5. 逐路由元数据

### 5.1 纯 builder

`buildMetadata` 是**唯一**允许感知框架元数据类型的函数。
其余一切都不依赖框架。

```ts
// services/seo/index.ts  (Next.js example — swap the return type for other frameworks)
import type { Metadata } from "next";
import { OG_IMAGE_PATH } from "@/constants/seo";
import type { RouteDescriptor } from "@/types/seo";

export function buildMetadata(route: RouteDescriptor): Metadata {
  const canonical = canonicalUrl(route.path);
  const ogImageUrl = canonicalUrl(route.ogImage ?? OG_IMAGE_PATH);

  return {
    title: route.title,
    description: route.description,
    alternates: { canonical },
    openGraph: { images: [ogImageUrl] },
  };
}
```

### 5.2 全局默认值放在根 layout

在根位置**一次**设置标题模板、默认 OG/Twitter 卡片、robots 策略、图标、manifest 和
验证信息。子路由只覆盖不同的部分。

```tsx
// app/layout.tsx — global metadata, all values from constants/seo
import type { Metadata } from "next";
import {
  SITE_URL,
  SITE_NAME,
  SITE_HANDLE,
  SITE_LOCALE,
  SITE_TITLE_DEFAULT,
  SITE_TITLE_TEMPLATE,
  SITE_DESCRIPTION,
  SITE_KEYWORDS,
  AUTHOR_NAME,
  OG_IMAGE_PATH,
  OG_IMAGE_WIDTH,
  OG_IMAGE_HEIGHT,
  GOOGLE_SITE_VERIFICATION,
} from "@/constants/seo";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { default: SITE_TITLE_DEFAULT, template: SITE_TITLE_TEMPLATE },
  description: SITE_DESCRIPTION,
  keywords: SITE_KEYWORDS,
  authors: [{ name: AUTHOR_NAME, url: SITE_URL }],
  alternates: {
    canonical: SITE_URL,
    types: { "application/rss+xml": `${SITE_URL}/feed.xml` },
  },
  openGraph: {
    type: "website",
    locale: SITE_LOCALE,
    url: SITE_URL,
    siteName: SITE_NAME,
    title: SITE_TITLE_DEFAULT,
    description: SITE_DESCRIPTION,
    images: [
      { url: OG_IMAGE_PATH, width: OG_IMAGE_WIDTH, height: OG_IMAGE_HEIGHT },
    ],
  },
  twitter: {
    card: "summary_large_image",
    site: SITE_HANDLE,
    creator: SITE_HANDLE,
    title: SITE_TITLE_DEFAULT,
    description: SITE_DESCRIPTION,
    images: [OG_IMAGE_PATH],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  verification: { google: GOOGLE_SITE_VERIFICATION },
  manifest: "/manifest.webmanifest",
};
```

### 5.3 逐路由覆盖（动态页面）

动态路由读取其实体并返回该路由专属的元数据。标题模板会自动填入
`%s`，所以只需传入页面标题。

```tsx
// app/blog/[slug]/page.tsx
import { buildMetadata } from "@/services/seo";

export async function generateMetadata({ params }) {
  const post = await loadPost(params.slug);
  return buildMetadata({
    path: `/blog/${post.slug}`,
    title: post.title,
    description: post.description,
    ogImage: post.heroImage,
  });
}
```

**硬性规则：**

- 在 layout 里设置一次默认值；逐路由只在差异处覆盖。
- 使用标题**模板**，让子页面不再重复站点名。
- 每个页面解析出一个唯一的 `canonical`——绝不输出重复或相对的 canonical。

---

## 6. 发现面（由内容生成）

### 6.1 Sitemap

从应用渲染的**同一份内容集合**构建条目，去重，全部为绝对 URL。

```ts
// services/seo/index.ts
import { ROUTES } from "@/constants/routes";
import type { SitemapEntry } from "@/types/seo";

const PRIMARY_ROUTES: Array<{
  path: string;
  changeFrequency: SitemapEntry["changeFrequency"];
  priority: number;
}> = [
  { path: ROUTES.HOME, changeFrequency: "weekly", priority: 1.0 },
  { path: ROUTES.BLOG, changeFrequency: "daily", priority: 0.9 },
  // …other primary routes
];

export function sitemapEntries(options: {
  blogSlugs: string[];
  projectSlugs: string[];
}): SitemapEntry[] {
  const seen = new Set<string>();
  const entries: SitemapEntry[] = [];
  const add = (e: SitemapEntry) => {
    if (!seen.has(e.url)) {
      seen.add(e.url);
      entries.push(e);
    }
  };
  const today = new Date().toISOString().split("T")[0];

  for (const r of PRIMARY_ROUTES)
    add({
      url: canonicalUrl(r.path),
      lastModified: today,
      changeFrequency: r.changeFrequency,
      priority: r.priority,
    });
  for (const slug of options.blogSlugs)
    add({
      url: canonicalUrl(`/blog/${slug}`),
      lastModified: today,
      changeFrequency: "monthly",
      priority: 0.7,
    });
  for (const slug of options.projectSlugs)
    add({
      url: canonicalUrl(`/projects/${slug}`),
      lastModified: today,
      changeFrequency: "monthly",
      priority: 0.8,
    });

  return entries;
}
```

```ts
// app/sitemap.ts — thin adapter
import type { MetadataRoute } from "next";
import { sitemapEntries } from "@/services/seo";

export default function sitemap(): MetadataRoute.Sitemap {
  const entries = sitemapEntries({
    blogSlugs: loadPublishedBlogSlugs(),
    projectSlugs: loadProjectSlugs(),
  });
  return entries.map((e) => ({
    url: e.url,
    lastModified: e.lastModified ? new Date(e.lastModified) : new Date(),
    changeFrequency:
      e.changeFrequency as MetadataRoute.Sitemap[0]["changeFrequency"],
    priority: e.priority,
  }));
}
```

### 6.2 Robots

```ts
// app/robots.ts
import type { MetadataRoute } from "next";
import { SITE_URL } from "@/constants/seo";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: "*", allow: "/", disallow: ["/api/", "/_next/", "/admin/"] },
      { userAgent: "Googlebot", allow: "/" },
    ],
    sitemap: `${SITE_URL}/sitemap.xml`,
    host: SITE_URL,
  };
}
```

始终**禁止抓取私有路径**（`/api/`、`/admin/`、构建内部产物），并**指向 sitemap**。

### 6.3 RSS 订阅

```ts
// services/seo/index.ts
import type { RssItem } from "@/types/seo";

export function rssItems(posts: BlogPost[]): RssItem[] {
  return posts.map((post) => {
    const link = canonicalUrl(`/blog/${post.slug}`);
    return {
      title: post.title,
      link,
      description: post.description,
      pubDate: post.publishDate,
      guid: link,
    };
  });
}
```

```ts
// app/feed.xml/route.ts — sort newest-first, CDATA-wrap free text
import { rssItems } from "@/services/seo";
import { SITE_NAME, SITE_URL, SITE_DESCRIPTION } from "@/constants/seo";

export function GET(): Response {
  const items = rssItems(loadPublishedPostsNewestFirst());
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>${SITE_NAME}</title><link>${SITE_URL}</link>
  <description>${SITE_DESCRIPTION}</description>
  ${items
    .map(
      (i) => `<item>
    <title><![CDATA[${i.title}]]></title><link>${i.link}</link>
    <description><![CDATA[${i.description}]]></description>
    <pubDate>${i.pubDate}</pubDate><guid>${i.guid}</guid>
  </item>`,
    )
    .join("")}
</channel></rss>`;
  return new Response(xml, {
    headers: { "Content-Type": "application/rss+xml; charset=utf-8" },
  });
}
```

用 CDATA 包裹标题与描述，避免撇号或标记破坏订阅源。

---

## 7. 结构化数据（类型化的 JSON-LD）

### 7.1 通用 builder

```ts
// services/seo/index.ts
import type { JsonLd, SchemaType } from "@/types/seo";

export function structuredData(
  type: SchemaType,
  data: Record<string, unknown>,
): JsonLd {
  return { "@context": "https://schema.org", "@type": type, ...data };
}
```

### 7.2 各类型 builder，通过稳定的 `@id` 互相引用

```ts
// services/seo/structured-data.ts
import { structuredData } from "./index";
import { SITE_URL, AUTHOR_NAME, SITE_DESCRIPTION } from "@/constants/seo";
import type { JsonLd } from "@/types/seo";

export function personJsonLd(): JsonLd {
  return structuredData("Person", {
    "@id": `${SITE_URL}/#person`, // stable identity others reference
    name: AUTHOR_NAME,
    url: SITE_URL,
    description: SITE_DESCRIPTION,
    sameAs: [
      /* social profile URLs */
    ],
  });
}

export function websiteJsonLd(): JsonLd {
  return structuredData("WebSite", {
    "@id": `${SITE_URL}/#website`,
    url: SITE_URL,
    name: AUTHOR_NAME,
    author: { "@id": `${SITE_URL}/#person` }, // reference, not a copy
    potentialAction: {
      "@type": "SearchAction",
      target: {
        "@type": "EntryPoint",
        urlTemplate: `${SITE_URL}/blog?q={search_term_string}`,
      },
      "query-input": "required name=search_term_string",
    },
  });
}

export function blogPostingJsonLd(post: BlogPost, url: string): JsonLd {
  return structuredData("BlogPosting", {
    "@id": url,
    headline: post.title,
    description: post.description,
    datePublished: post.publishDate,
    dateModified: post.publishDate,
    author: {
      "@type": "Person",
      "@id": `${SITE_URL}/#person`,
      name: post.author,
    },
    publisher: {
      "@type": "Person",
      "@id": `${SITE_URL}/#person`,
      name: AUTHOR_NAME,
    },
    url,
    mainEntityOfPage: { "@type": "WebPage", "@id": url },
    image: {
      "@type": "ImageObject",
      url: post.heroImage,
      width: 1200,
      height: 630,
    },
    keywords: post.tags.join(", "),
  });
}

export function breadcrumbListJsonLd(
  items: Array<{ name: string; url: string }>,
): JsonLd {
  return structuredData("BreadcrumbList", {
    itemListElement: items.map((item, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: item.name,
      item: item.url,
    })),
  });
}

export function faqPageJsonLd(
  faqs: Array<{ question: string; answer: string }>,
): JsonLd {
  return structuredData("FAQPage", {
    mainEntity: faqs.map((f) => ({
      "@type": "Question",
      name: f.question,
      acceptedAnswer: { "@type": "Answer", text: f.answer },
    })),
  });
}
```

`CreativeWork` 沿用相同形态，用于项目/作品集条目（name、description、按
`@id` 关联的 author、`keywords`，可选 `codeRepository`/`sameAs`/`image`）。

### 7.3 将 JSON-LD 注入页面

用 `JSON.stringify` 渲染一个 `<script type="application/ld+json">`。
面包屑路径要与页面在站点中的真实位置一致。

```tsx
// app/blog/[slug]/page.tsx
import { canonicalUrl } from "@/services/seo";
import {
  blogPostingJsonLd,
  breadcrumbListJsonLd,
} from "@/services/seo/structured-data";

export default async function Page({ params }) {
  const post = await loadPost(params.slug);
  const url = canonicalUrl(`/blog/${post.slug}`);
  const postLd = blogPostingJsonLd(post, url);
  const crumbLd = breadcrumbListJsonLd([
    { name: "Home", url: canonicalUrl("/") },
    { name: "Blog", url: canonicalUrl("/blog") },
    { name: post.title, url },
  ]);
  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(postLd) }}
        suppressHydrationWarning
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(crumbLd) }}
        suppressHydrationWarning
      />
      {/* …page content */}
    </>
  );
}
```

**硬性规则：**

- 为每个实体赋予一个**稳定的 `@id`**（例如 `${SITE_URL}/#person`），并在别处通过**引用**使用，而不是重复字段。
- 每个详情页一个 `BlogPosting`/`CreativeWork`；每个嵌套页一份 `BreadcrumbList`。
- `Person` + `WebSite` 放在首页；只在真正展示 Q&A 的页面使用 `FAQPage`。
- 上线前用 Google 的 Rich Results Test / Schema Markup Validator 验证输出。

---

## 8. 框架适配器

Builder 与框架无关。只有挂载层会因框架而异。

| 框架                | 逐路由元数据                                                                                  | sitemap / robots / feed                                                                    |
| -------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **Next.js App Router** | `export const metadata`（静态）或 `generateMetadata`（动态），返回 `buildMetadata(...)`           | `app/sitemap.ts`、`app/robots.ts`、`app/feed.xml/route.ts`                                 |
| **Remix**              | 每路由的 `meta` 导出，把 `buildMetadata` 的字段映射为 `<meta>` 描述符                              | 资源路由（`routes/sitemap[.]xml.ts` 等）以 XML/文本形式返回 builder 输出                   |
| **Astro**              | 在 layout 的 `<head>` 里读取同一份常量；按页面 frontmatter 覆盖                                  | `src/pages/sitemap.xml.ts`、`robots.txt.ts`、`rss.xml.ts` 端点                             |
| **React + Vite (SPA)** | `react-helmet-async`（或其他 head 管理器）消费 `buildMetadata` 返回的纯对象                       | 构建时脚本，基于同一份 builder 生成 `sitemap.xml`/`robots.txt`                             |
| **Expo Router (web)**  | 静态 head 配置 / `expo-router` head；SEO 仅在 web 端目标下有意义                                  | 一个仅 web 的轻量构建步骤调用 `sitemapEntries`/`rssItems`                                 |

如果 `buildMetadata` 必须保持框架中立，可让其返回纯对象
（`{ title, description, canonical, ogImage }`），再由各适配器转换——
`Metadata` 返回类型只在 Next.js 项目里出现。

---

## 9. 规约检查清单（在评审中强制执行）

- [ ] 所有站点身份（URL、名称、描述、关键词、作者、账号、OG 图片、验证信息）都集中在**一个** `constants/seo` 模块——无重复、无硬编码基础 URL。
- [ ] 每条绝对 URL 都由 `canonicalUrl()` 生成——没有手写 `SITE_URL + path`。
- [ ] 一套尾部斜杠策略，在所有地方一致应用。
- [ ] 全局元数据（标题模板、默认 OG/Twitter、robots、验证信息、manifest）在根 layout 中**一次**设置。
- [ ] 动态路由通过 `buildMetadata`（或框架适配器）覆盖元数据，只传入差异部分。
- [ ] 每个页面恰好解析出一个 `canonical`；没有相对的或重复的 canonical。
- [ ] `sitemap.xml`、`robots.txt` 和 RSS 订阅**由内容集合生成**，去重，全部为绝对 URL；robots 中禁止抓取私有路由。
- [ ] JSON-LD 使用统一的 `structuredData`/`JsonLd` builder；实体之间通过稳定 `@id` 互相引用。
- [ ] 每个详情页输出主 schema（`BlogPosting`/`CreativeWork`）+ `BreadcrumbList`；首页输出 `Person` + `WebSite`。
- [ ] Builder 函数是纯函数并经过单元测试；框架代码只留在轻量适配器（路由文件）里。
- [ ] OG 图片、语言环境、Twitter 账号在 OG 和 Twitter 卡片上同时存在并保持一致。
- [ ] 上线前用 Google 的 Rich Results Test 验证结构化数据。

---

## 10. 如何应用本技能

**为站点添加 SEO：** 创建 `constants/seo`、`types/seo` 与 `services/seo/`（barrel 加
`structured-data.ts`）。在根 layout 接入全局元数据，然后添加 `sitemap`、`robots`、
`feed.xml` 适配器挂载 builder。

**新增内容类型（例如案例研究）：** 把它的 slug 加入 `sitemapEntries`，如需专属 schema 则添加
JSON-LD builder，并为该详情页提供 `generateMetadata` 与 `BreadcrumbList`。

**排查重复内容/索引问题：** 检查每页都经过 `canonicalUrl`，确认尾部斜杠策略统一，并
确认 sitemap 只包含可索引、绝对的 URL。同时确认 robots 没有错误地屏蔽应当被索引的页面。

**评审 SEO 覆盖情况：** 跑 §9 的检查清单。价值最高的发现是绕过 `canonicalUrl`
的硬编码 URL（重复内容风险），以及重复实体字段而非引用稳定 `@id` 的 JSON-LD。

---

## 发布 / 安装本技能

本技能遵循 Anthropic `SKILL.md` 格式，可在各 Agent 间移植。

1. 将其保存在公开 GitHub 仓库的 `skills/frontend-seo/SKILL.md` 路径下。
2. 保留 frontmatter 中的 `name` 与高信号 `description`——发现索引依赖它匹配。
3. 安装命令：`npx skills add <org>/<repo> --skill "frontend-seo"`。
4. 非 `SKILL.md` 形态的 Agent 可以通过 `AGENTS.md` / `CLAUDE.md` 指向本文件；Kiro 可将其镜像为 steering 文件。

## 局限性

- 仅当任务明确匹配其上游来源与本地项目上下文时使用本技能。
- 在落地前验证命令、生成代码、依赖、凭证以及外部服务的行为。
- 不要把示例当作环境专属测试、安全审查或用户对破坏性/高成本操作的批准的替代品。