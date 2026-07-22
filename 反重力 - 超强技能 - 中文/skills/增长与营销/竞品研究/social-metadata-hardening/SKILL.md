---
name: social-metadata-hardening
description: "修复社交分享预览，使 URL 在 Facebook、LinkedIn、X/Twitter、WhatsApp、Telegram 等平台上渲染为富卡片。涵盖 OG 标签、Twitter 卡片、绝对图片 URL 及调试方法。"
category: seo
risk: safe
source: self
source_type: self
date_added: "2026-05-31"
author: Whoisabhishekadhikari
tags: [seo, open-graph, twitter-card, social-sharing, og-image, nextjs, metadata]
tools: [claude, cursor, gemini, claude-code]
version: 1.0.0
---

# Social Metadata Hardening Skill

修复社交分享，使每个重要 URL 在所有平台上都能展开为富卡片。

---

## 何时使用

- 当分享链接在社交和聊天平台上出现缺失、过期、裁剪或错误的预览时使用。
- 当需要审计 Web 应用中的 Open Graph、Twitter/X 卡片、图片 URL、alt 文本或 `metadataBase` 覆盖情况时使用。
- 上线前使用，当每个公开页面都需要在 LinkedIn、X、Facebook、WhatsApp、Slack、Discord 和 Telegram 上呈现可预期的富预览时。

---

## 预览为何会出问题

| 问题 | 根本原因 |
|------|----------|
| 完全没有预览 | 缺少 og:title、og:description 或 og:image |
| 图片损坏 | 使用了相对 URL（必须是绝对 URL） |
| 图片尺寸不对 | 图片不是 1200×630px（OG 标准） |
| 纯文本卡片 | Twitter 卡片类型缺失或设为 `summary` |
| 预览过期 | 平台缓存了旧元数据 |
| 爬取时元数据缺失 | 标签由客户端 JS 添加（爬虫不执行 JS） |

---

## 黄金标准元数据块

每个可分享页面都需要在静态 HTML 中包含以下全部内容：

```js
// Next.js App Router — lib/socialMetadata.js
export function buildSocialMetadata({
  title,
  description,
  path,          // '/blog/my-post'
  image,         // '/images/og/my-post.jpg' or full URL
  imageAlt,
  imageWidth = 1200,
  imageHeight = 630,
}) {
  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'https://www.yourdomain.com';
  
  // Always produce an absolute URL
  const imageUrl = image?.startsWith('http') ? image : `${baseUrl}${image}`;
  const pageUrl  = `${baseUrl}${path}`;
  
  // Detect MIME type from extension
  const ext = imageUrl.split('.').pop().toLowerCase();
  const mimeMap = { jpg: 'image/jpeg', jpeg: 'image/jpeg', png: 'image/png', webp: 'image/webp' };
  const imageType = mimeMap[ext] || 'image/jpeg';

  return {
    title,
    description,
    alternates: { canonical: pageUrl },
    openGraph: {
      title,
      description,
      url: pageUrl,
      type: 'website',  // use 'article' for blog posts
      images: [{
        url: imageUrl,
        secureUrl: imageUrl,   // explicit HTTPS version
        width: imageWidth,
        height: imageHeight,
        alt: imageAlt || title,
        type: imageType,
      }],
    },
    twitter: {
      card: 'summary_large_image',  // NOT 'summary' — that shows a tiny image
      title,
      description,
      images: [imageUrl],
    },
  };
}
```

---

## 应用该辅助函数

### 静态页面
```js
// app/about/page.js
import { buildSocialMetadata } from '@/lib/socialMetadata';

export const metadata = buildSocialMetadata({
  title: 'About Us | My Site',
  description: 'Learn about our team and mission.',
  path: '/about',
  image: '/images/og/about.jpg',
  imageAlt: 'The My Site team',
});
```

### 动态页面（博客文章、工具页）
```js
// app/blog/[slug]/page.js
import { buildSocialMetadata } from '@/lib/socialMetadata';

export async function generateMetadata({ params }) {
  const post = await getPost(params.slug);
  return buildSocialMetadata({
    title: `${post.title} | My Blog`,
    description: post.excerpt,
    path: `/blog/${params.slug}`,
    image: post.ogImage || '/images/og/default.jpg',
    imageAlt: post.title,
  });
}
```

### 首页（app/layout.js 或 app/page.js）
```js
export const metadata = {
  metadataBase: new URL('https://www.yourdomain.com'), // REQUIRED for absolute URLs
  ...buildSocialMetadata({
    title: 'My Site — Tagline Here',
    description: 'Site-wide description.',
    path: '/',
    image: '/images/og/home.jpg',
  }),
};
```

> ⚠️ **使用相对元数据 URL 时务必设置 `metadataBase`。** 如果你的辅助函数已经输出绝对的 canonical/OG URL，即使不设置也能正常工作。

---

## OG 图片检查清单

好的 OG 图片应满足：
- **1200 × 630px**（2:1 比例 — 适用于所有平台）
- **8MB 以下**（Facebook 限制）
- 通过 **HTTPS** 提供
- 文件名**不含空格**（用连字符代替）
- 格式：**JPEG 或 PNG**（WebP 在大部分平台可用，但并非所有爬虫都支持）
- **可通过 GET 请求访问**，无需身份验证

```bash
# Verify your OG image is reachable and correct size
curl -sI https://www.yourdomain.com/images/og/home.jpg | grep -i "content-type\|content-length\|status"
```

---

## 各平台注意事项

### Facebook / Meta
- 缓存非常激进 — 使用 [Sharing Debugger](https://developers.facebook.com/tools/debug/) 强制重新抓取
- 最小图片：200×200px（但建议用 1200×630 以保证质量）
- 需要：`og:title`、`og:description`、`og:image`、`og:url`

### X / Twitter
- 使用 `twitter:card = summary_large_image` 获得全宽图片
- `twitter:image` 必须是绝对 URL
- 使用 [Card Validator](https://cards-dev.twitter.com/validator) 测试

### LinkedIn
- 缓存很顽固 — 使用 [Post Inspector](https://www.linkedin.com/post-inspector/) 刷新
- 只认 `og:` 标签；忽略 `twitter:` 标签
- 图片宽高比必须 ≥1.91:1

### WhatsApp / Telegram
- 首次分享时读取 OG 标签；缓存可持续数小时
- 几小时后重新分享，等待缓存自然清除

### Slack / Discord
- 两者都使用 OG 标签；都会缓存
- Discord 还支持 `og:type = article` 以获得更丰富的嵌入

---

## 调试社交预览

### 1. 检查原始 HTML 中的标签
```bash
curl -s https://www.yourdomain.com/blog/my-post | grep -i "og:\|twitter:"
```
如果标签没有出现 → 说明它们是由 JavaScript 添加的（爬虫无法读取）。修复方法：移到 `export const metadata` 或 `generateMetadata` 中。

### 2. 使用平台工具验证

| 平台 | 工具 |
|------|------|
| Facebook | https://developers.facebook.com/tools/debug/ |
| LinkedIn | https://www.linkedin.com/post-inspector/ |
| Twitter/X | https://cards-dev.twitter.com/validator |
| 通用 | https://metatags.io |

### 3. 强制刷新缓存
部署修复后，将 URL 粘贴到各平台的调试器中，点击"Fetch new scrape information"（或等效按钮）。

---

## 社交元数据检查清单

- [ ] 根布局中设置了 `metadataBase`
- [ ] 所有可分享页面都使用共享的 `buildSocialMetadata` 辅助函数
- [ ] OG 图片 URL 为绝对路径（以 `https://` 开头）
- [ ] OG 图片块中 `secureUrl` 等于 `url`
- [ ] 图片尺寸 1200×630px，8MB 以下，HTTPS
- [ ] `twitter:card` 设为 `summary_large_image`（而非 `summary`）
- [ ] 图片 alt 文本已填写
- [ ] 标签在原始 HTML 中可见（非 JavaScript 渲染）
- [ ] 所有平台调试器显示正确预览
- [ ] 部署后已在所有平台上刷新缓存

## 局限性

- 无法在每个社交平台上强制立即刷新缓存；部分预览在正确修复后可能仍然显示旧内容。
- 需要公开可访问的已部署 URL 才能通过平台调试器进行可靠验证。
- 不替代对图片文字、alt 文本和预览文案的品牌、无障碍或法律审查。
