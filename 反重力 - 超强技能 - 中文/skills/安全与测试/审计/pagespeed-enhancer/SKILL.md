---
name: pagespeed-enhancer
description: "以结构化批次方式扫描、审计并修复 Lighthouse/PageSpeed Insights 四大支柱（性能、无障碍、最佳实践、SEO）的 Web 性能问题。触发词：PageSpeed、Lighthouse、性能优化、Core Web Vitals、LCP、FCP、CLS、TBT、网页速度优化、安全头配置、CSP、WebP 转换。"
risk: safe
source: personal
date_added: "2026-06-14"
author: WHOISABHISHEKADHIKARI
---

# PageSpeed 性能增强器技能

针对 Lighthouse 四大支柱的结构化批量审计与修复工作流。始终按顺序执行各阶段流程，切勿在未完成扫描和风险评估阶段的情况下直接跳转到修复步骤。

---

## 使用时机

- 用户粘贴了 PageSpeed Insights 报告或提及了 Lighthouse 分数
- 用户要求改善 Core Web Vitals（LCP、FCP、CLS、TBT、SI）
- 用户需要处理渲染阻塞资源、未使用的 JavaScript、图片优化、安全响应头、ARIA 合规性或 SEO meta 标签修复
- 用户提问"为什么我的 LCP 很慢"、"修复无障碍问题"、"提升 SEO 分数"或"我的网站性能得分是 80"
- 任何关于 PageSpeed、Lighthouse、Web Vitals 或网站速度的提及

---

## 高阶工作流

```
阶段 1 → 导入报告并解析分数
阶段 2 → 批量扫描（4 个分区，并行分析）
阶段 3 → 整合风险报告（按影响 vs 风险排序）
阶段 4 → 修复批次（按安全顺序应用：低风险 → 高风险）
阶段 5 → 验证清单
```

---

## 阶段 1 — 导入与分类

当用户提供 PageSpeed Insights 报告（粘贴文本、截图或 URL）时：

1. 提取四大支柱分数：Performance（性能）、Accessibility（无障碍）、Best Practices（最佳实践）、SEO。
2. 提取每个被标记指标及其数值和 Lighthouse 权重。
3. 识别**关键路径瓶颈**（导致最低支柱分数的首要问题）。
4. 输出**分数汇总表**：

```
| 支柱            | 分数 | 状态    | 关键问题                          |
|-----------------|------|---------|-----------------------------------|
| Performance     | 80   | ⚠️ 警告 | LCP 4.0s — 元素渲染延迟           |
| Accessibility   | 100  | ✅ 通过 | —                                 |
| Best Practices  | 100  | ✅ 通过 | CSP 缺失（未计分）                |
| SEO             | 100  | ✅ 通过 | —                                 |
```

随后立即进入阶段 2，除非报告内容存在歧义，否则无需等待用户输入。

---

## 阶段 2 — 批量扫描（4 个分区）

运行全部四个分区扫描，输出时以可折叠区块呈现。

### 批次 A — 性能扫描

按以下顺序审计（Lighthouse 权重从高到低）：

| 审计项             | 影响指标      | 关键问题                                                                 |
|--------------------|---------------|--------------------------------------------------------------------------|
| LCP 拆解          | LCP           | LCP 元素是否使用了懒加载？TTFB 是否 > 600ms？元素渲染延迟是否 > 1s？       |
| 渲染阻塞资源       | FCP, LCP      | 哪些 CSS/JS 文件阻塞了关键路径？能否延迟加载或内联？                      |
| CSS `@import` 规则 | FCP, LCP      | 外部样式表是否通过 CSS 中的 `@import url()` 加载？这是**双重渲染阻塞**——浏览器必须先获取并解析 CSS，再获取导入的 CSS。应改用 `<link>` 替代。 |
| 未使用的 JavaScript | FCP, LCP, TBT | 主打包文件中有多大比例未被使用？是否可以进行代码分割？                     |
| 网络依赖树        | LCP           | 关键路径链是什么？最大延迟是多少？                                        |
| 强制重排          | TBT           | 哪些 JS 函数在 DOM 变更后查询了几何属性？                                  |
| 图片交付           | FCP, LCP      | 图片是否为 WebP/AVIF 格式？首屏图片是否使用了懒加载？                     |
| 速度索引          | SI            | 页面是视觉渐进式呈现还是一次性绘制完毕？                                  |
| CLS 元凶          | CLS           | 是否存在缺少 width/height 的图片？是否有延迟注入的内容？                  |
| JavaScript 执行时间 | TBT          | 解析 + 编译 + 评估总时长？                                               |
| 主线程长任务       | TBT           | 是否有超过 50ms 的任务？何时开始？                                       |
| 打包资源大小       | FCP, LCP, TBT | 检查 `dist/` 输出：是否有单个 JS chunk 压缩后 > 500KB？CSS > 100KB？代码分割是否生成了独立的 vendor chunks？ |

对于每个审计项，输出：
- **发现**：报告内容
- **根因**：问题产生原因
- **修复类别**：快速见效 / 中等工作量 / 需要重构

### 批次 B — 无障碍扫描

重点关注任何未通过的审计项。对于满分页面，仍需检查：

| 检查项              | 验证内容                                                        |
|---------------------|-----------------------------------------------------------------|
| ARIA 属性正确性     | 所有 `aria-*` 属性与元素角色匹配                                 |
| 颜色对比度          | 所有文本符合 WCAG AA 标准（普通文本 4.5:1，大字文本 3:1）        |
| 图片 alt 文本质量   | alt 文本具有描述性，而非仅用文件名                               |
| 键盘导航            | 所有交互元素均可通过 Tab 键访问                                  |
| 跳转链接            | 存在且可获得焦点                                                |
| 标题层级            | 无跳级（h1 → h2 → h3）                                          |
| 触摸目标尺寸        | 移动端最小 44×44px                                              |
| 表单标签            | 每个 input 都有关联的 label                                      |
| `lang` 属性         | `<html lang="en">` 存在且符合 BCP 47 规范                       |
| `font-display`      | 设置为 `swap` 或 `optional` 以防止 FOIT（字体不可见闪烁）        |

### 批次 C — 最佳实践扫描

安全响应头通常不会被 Lighthouse 分数标记但至关重要。检查所有部署目标：

| 检查项                        | 头部/设置                                    | 配置位置                                              | 严重程度    |
|-------------------------------|----------------------------------------------|-------------------------------------------------------|-------------|
| 内容安全策略                  | `Content-Security-Policy`                    | `netlify.toml` `[[headers]]` / `vercel.json` `"headers"` | 🔴 高      |
| 跨域开放者策略                | `COOP` header                                | 同上                                                 | 🔴 高      |
| 点击劫持防护                  | `X-Frame-Options` 或 CSP `frame-ancestors`   | 同上                                                 | 🔴 高      |
| HSTS 配置                     | `Strict-Transport-Security` 带 `includeSubDomains` + `preload` | 同上 | 🟡 中等 |
| 可信类型（DOM XSS）           | CSP `require-trusted-types-for 'script'`     | 同上                                                 | 🟡 中等 |
| X-Content-Type-Options        | `nosniff` header                             | 同上                                                 | 🟡 中等 |
| Referrer-Policy               | `strict-origin-when-cross-origin`             | 同上                                                 | 🟡 中等 |
| Permissions-Policy            | 限制摄像头/麦克风/地理位置                    | 同上                                                 | 🟡 中等 |
| 第三方 Cookie                 | 是否存在不带 `Secure` 属性的 `SameSite=None` cookie？ | — | 🟡 中等 |
| 已弃用的 API                  | 是否在使用浏览器已弃用的 JS API？             | —                                                    | 🟢 低      |
| Source maps                   | 是否部署了 source map 用于调试？              | —                                                    | 🟢 低      |

当 `netlify.toml` 和 `vercel.json` 同时存在时，**两者都需检查**。两者语法不同（TOML vs JSON）。

### 批次 D — SEO 扫描

| 检查项              | 验证内容                                                              |
|---------------------|-----------------------------------------------------------------------|
| `<title>` 标签      | 存在，50–60 字符，包含主要关键词                                     |
| Meta description    | 存在，150–160 字符，具有吸引力                                        |
| 规范标签             | `<link rel="canonical">` 指向正确的 URL                              |
| hreflang            | 多语言场景下是否存在；语言代码正确                                    |
| robots.txt          | 有效，不阻止关键资源                                                  |
| 结构化数据          | 存在 JSON-LD；运行 Schema 验证器                                     |
| 图片 alt 属性       | 每个 `<img>` 都有有意义的 alt                                         |
| 链接描述性          | 无"点击这里"/"阅读更多"类链接文本                                     |
| 可爬取性            | 重要页面上无 `noindex` 标记                                           |
| HTTP 状态码         | 主页面和关键资源均返回 200                                            |
| SPA meta 注入       | 若使用 react-helmet-async / Next.js Head：通过"查看源代码"验证，**不要**使用 DevTools Elements——meta 标签可能由 JS 动态注入 |

---

## 阶段 3 — 风险报告

完成全部四个批次的扫描后，输出整合后的**风险与影响矩阵**：

```
| 修复操作                         | 影响评分 | 风险等级 | 工作量   | 优先级 |
|----------------------------------|----------|----------|----------|--------|
| 为非关键 JS 添加 defer/async     | 高（预估 LCP -0.8s） | 🟢 低 | 1h     | P1     |
| 将图片转换为 WebP/AVIF           | 中等（LCP -0.3s）   | 🟢 低 | 2h     | P1     |
| 添加 CSP 头                      | 安全相关 | 🟡 中等  | 3h     | P2     |
| 对主 JS 包进行代码分割           | 高（TBT -20ms）     | 🟡 中等 | 1 天  | P2     |
| 修复强制重排                     | 中等（TBT -15ms）   | 🔴 高   | 2 天  | P3     |
| 添加 HSTS preload               | 安全相关 | 🟡 中等  | 30min  | P2     |
```

**风险等级定义：**
- 🟢 低风险：配置/头部变更，无需修改代码。5 分钟内即可回滚。
- 🟡 中等风险：构建配置或资源管道变更。需先在预发布环境测试。
- 🔴 高风险：JavaScript 重构或架构变更。需要完整的 QA 测试周期。

建议优先级：先修复 P1（低风险、高影响）项目，然后是 P2，最后是 P3。

---

## 阶段 4 — 修复批次

按风险顺序应用修复。每项修复提供：

1. **修改内容** — 文件、行号、具体改动
2. **修改前**（代码片段）
3. **修改后**（代码片段）
4. **预期指标改善** — 预估变化值
5. **验证方法** — 部署后如何检查

### 修复批次 1 — 快速见效（低风险，可立即部署）

来自常见审计的示例：

**F1.1 — 将 CSS `@import` 移至 `<link>` 标签**

CSS `@import url()` 会造成双重渲染阻塞。移至 `<head>` 中的 `<link>`：

```css
/* Before: in index.css */
@import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');
```

```html
<!-- After: in index.html <head> -->
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter&display=swap" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter&display=swap" media="print" onload="this.media='all'" />
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter&display=swap" /></noscript>
```

**F1.2 — 延迟渲染阻塞 CSS（若非首屏关键样式）**
```html
<!-- Before -->
<link rel="stylesheet" href="/assets/index.css">

<!-- After: load async, apply on load -->
<link rel="preload" href="/assets/index.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/assets/index.css"></noscript>
```

**F1.3 — 修复失效的 preconnect（crossorigin 不匹配）**
```html
<!-- Before (broken — no crossorigin on font CDN) -->
<link rel="preconnect" href="https://api.rss2json.com">

<!-- After -->
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<!-- Only preconnect origins used in critical path, max 4 -->
```

**F1.4 — 将图片转换为 WebP 格式**
```bash
# Using cwebp
cwebp -q 80 input.jpeg -o output.webp

# Using sharp (Node.js)
sharp('image.jpeg').webp({ quality: 80 }).toFile('image.webp')

# macOS fallback (sips built-in)
sips -s format webp input.jpeg --out output.webp

# Python Pillow fallback
python3 -c "
from PIL import Image
Image.open('input.jpg').save('output.webp', 'WebP', quality=80)
"
```

**F1.5 — 添加明确的图片尺寸（修复 CLS）**
```html
<!-- Before -->
<img src="hero.webp" alt="...">

<!-- After -->
<img src="hero.webp" alt="..." width="800" height="400">
```

**F1.6 — 添加安全响应头（netlify.toml）**
```toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Strict-Transport-Security = "max-age=31536000; includeSubDomains; preload"
    Cross-Origin-Opener-Policy = "same-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"
    Content-Security-Policy = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' https://api.rss2json.com"
```

**F1.7 — 添加安全响应头（vercel.json）**
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Strict-Transport-Security", "value": "max-age=31536000; includeSubDomains; preload" },
        { "key": "Cross-Origin-Opener-Policy", "value": "same-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" },
        { "key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self' https://api.rss2json.com" }
      ]
    }
  ]
}
```

**F1.8 — 自托管 Google Fonts（消除外部 CSS 请求）**

下载 woff2 文件并在本地提供服务，彻底消除 Google Fonts 的 CSS 往返请求：

```bash
# 1. 从 Google Fonts CSS URL 下载 woff2 文件
#    在浏览器中打开 https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap
#    然后下载 @font-face 块中列出的每个 woff2 URL。

# 2. 将文件放入 public/fonts/ 或 src/assets/fonts/
public/fonts/
  inter-v12-latin-400.woff2
  inter-v12-latin-700.woff2

# 3. 添加 @font-face CSS（只加载一次，无外部请求）
```

```css
/* src/styles/fonts.css */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/fonts/inter-v12-latin-400.woff2') format('woff2');
}

@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url('/fonts/inter-v12-latin-700.woff2') format('woff2');
}
```

```css
/* Remove the old Google Fonts <link> from index.html */
/* Before: */
<link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet">

/* After: just use the font-family normally */
body { font-family: 'Inter', sans-serif; }
```

**效果**：零外部 CSS 请求、FCP/LCP 更快、无 FOIT 风险、支持离线使用。

**F1.9 — 调整过大尺寸的图标**

图标（favicon、apple-touch-icon、OG image）不应超过 50KB。检查并调整尺寸：
```bash
python3 -c "
from PIL import Image
img = Image.open('favicon.png')
img.resize((192, 192)).save('favicon.png', 'PNG', optimize=True)
img.resize((32, 32)).save('favicon-32x32.png', 'PNG', optimize=True)
img.resize((16, 16)).save('favicon-16x16.png', 'PNG', optimize=True)
"
```

### 修复批次 2 — 中等工作量（建议在预发布环境测试）

**F2.1 — 移除 LCP 元素的懒加载**

LCP 元素**绝对不能**使用懒加载：
```html
<!-- Before: wrong — LCP image is lazy -->
<img src="hero.webp" loading="lazy" ...>

<!-- After: eager load the above-fold LCP element -->
<img src="hero.webp" loading="eager" fetchpriority="high" ...>
```

**F2.2 — 预加载 LCP 图片**

⚠️ 仅适用于 `public/` 目录中的文件或具有稳定 URL 的资源。如果使用 Vite/Webpack（带 content hash 的文件名），请改用 `<picture>` + `fetchPriority="high"`：
```html
<!-- For stable URLs (public/ directory): -->
<link rel="preload" as="image" href="/hero.webp" fetchpriority="high">

<!-- For hashed filenames (Vite/Rollup): use component-level approach -->
<picture>
  <source srcSet={webpImage} type="image/webp" />
  <img src={jpgImage} fetchPriority="high" loading="eager" width="1920" height="1080" />
</picture>
```

**F2.3 — 减少未使用的 JS（Vite/Rollup 配置）**
```js
// vite.config.js — enable manual chunking
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        vendor: ['react', 'react-dom'],
        rss: ['rss-parser'],
      }
    }
  }
}
```

**F2.4 — 消除强制重排**
```js
// Before: reads layout property inside animation loop
element.addEventListener('scroll', () => {
  const h = element.offsetHeight; // triggers reflow
  doSomething(h);
});

// After: cache geometry reads outside event handlers
const h = element.offsetHeight; // read once
element.addEventListener('scroll', () => {
  doSomething(h);
});
```

**F2.5 — 优化 DOM 大小**

若 DOM 节点数 > 1,500：
- 长列表使用虚拟滚动（react-virtual、TanStack Virtual）
- 懒渲染屏幕外区域
- 移除永远不会可见的 hidden/display:none 节点

### 修复批次 3 — 需要重构（完整 QA 测试周期）

**F3.1 — 关键路径中的外部 API（如 api.rss2json.com）**

当前流程：HTML → JS 包 → 外部 API（给关键路径增加 1,574ms）

解决方案：将外部 API 调用移至构建时或服务端：
```js
// Option A: Fetch at build time (Astro/Next.js SSG)
export async function getStaticProps() {
  const res = await fetch('https://api.rss2json.com/v1/api.json?rss_url=...');
  const data = await res.json();
  return { props: { posts: data.items }, revalidate: 3600 };
}

// Option B: Edge function / serverless proxy
// Cache RSS response at CDN edge, return stale-while-revalidate
```

**F3.2 — 内容安全策略（完整 CSP）**

迭代式构建 CSP：
1. 先以仅报告模式部署：`Content-Security-Policy-Report-Only`
2. 在浏览器控制台监控违规情况 48 小时
3. 将必需的来源加入白名单
4. 升级至强制执行模式

---

## 部署前检查

部署任何修复批次前，运行以下检查：

```
Build:
□ npm run build（或等效命令）— 退出码 0
□ npm run lint / typecheck — 相较基线无新增错误
□ 检查 dist/ 输出：
   - 无单个 JS chunk 压缩后 > 500KB
   - CSS < 100KB
   - 代码分割已生成独立的 vendor chunks

Asset verification:
□ 对于 Vite/Rollup/Webpack 项目：index.html 中的 preload <link> 无法匹配带 hash 的文件名。
  应改用组件上的 fetchPriority="high" + <picture> 方案。
□ 图标和 favicon 均 < 50KB（避免将多 MB 的源图直接用作图标）
□ 存在与原图对应的 WebP/AVIF 版本

Deploy target:
□ 如果双平台部署（Netlify + Vercel），需**两者都**验证响应头
□ 如果使用 SPA 框架：通过"查看源代码"验证 meta 标签，**不要**使用 DevTools Elements
  （react-helmet-async 在运行时注入——应检查预渲染/SSR 输出）
```

---

## 阶段 5 — 验证清单

每部署完一个修复批次后，进行以下验证：

```
Performance:
□ 在移动端和桌面端重新运行 PageSpeed Insights
□ LCP < 2.5s（良好）
□ FCP < 1.8s（良好）
□ TBT < 200ms（良好）
□ CLS < 0.1（良好）
□ SI < 3.4s（良好）

Accessibility:
□ 运行 axe DevTools 浏览器扩展
□ 仅使用键盘导航页面（Tab、Shift+Tab、Enter、Space）
□ 使用屏幕阅读器测试（NVDA/VoiceOver）
□ 通过浏览器 DevTools 无障碍面板检查颜色对比度

Best Practices:
□ 在 https://securityheaders.com 验证安全响应头
□ 检查 HTTPS 配置：DevTools 中无混合内容警告
□ 重新运行 Lighthouse Best Practices 审计

SEO:
□ 在 https://search.google.com/test/rich-results 验证结构化数据
□ 检查 /robots.txt 的 robots.txt 文件
□ 在页面源代码中验证规范标签（使用"查看源代码"，非 DevTools）
□ 向 Google Search Console 提交更新的站点地图
```

---

## 输出格式规范

- 始终标注输出类型：**[SCAN]**、**[RISK]**、**[FIX]**、**[VERIFY]**
- 使用 emoji 严重程度指示器：🔴 严重 / 🟡 警告 / 🟢 通过 / ℹ️ 信息
- 每个修复都必须展示"修改前"和"修改后"代码
- 始终包含预期指标变化（如"预估 LCP 改善：-0.8s"）
- 不要推荐相互冲突的修复方案——执行顺序很重要

---

## 快速参考：指标阈值

| 指标 | 良好   | 需改进     | 较差     |
|------|--------|------------|----------|
| FCP  | < 1.8s | 1.8–3.0s   | > 3.0s   |
| LCP  | < 2.5s | 2.5–4.0s   | > 4.0s   |
| TBT  | < 200ms| 200–600ms  | > 600ms  |
| CLS  | < 0.1  | 0.1–0.25   | > 0.25   |
| SI   | < 3.4s | 3.4–5.8s   | > 5.8s   |

---

## 示例

### 示例 1：用户粘贴 PageSpeed 报告

**用户**："我的网站性能得分 65。LCP 是 4.2s。"

**智能体**：
1. 解析分数汇总表 — 识别 LCP 为关键瓶颈
2. 运行批次 A 扫描 — 发现懒加载的主图和渲染阻塞 CSS
3. 输出风险报告：F1.1（CSS @import → link）列为 P1，F1.5（LCP 图片改为 eager 加载）列为 P1
4. 应用修复批次 1，通过复测验证

### 示例 2：用户询问 LCP 过慢的原因

**用户**："为什么我的 LCP 很慢？"

**智能体**：
1. 要求提供 PageSpeed 报告 URL 或粘贴结果
2. 运行批次 A 中针对 LCP 的专项审计 — 检查 TTFB、元素渲染延迟、懒加载情况
3. 识别 LCP 元素、其当前加载策略以及关键路径链
4. 推荐针对性修复方案（预加载、eager 加载或服务器响应时间优化）

---

## 局限性

- 不实际运行 Lighthouse 或 PageSpeed 测试 — 用户必须提供报告或 URL
- 安全响应头建议假设用户拥有部署平台的控制权（Netlify、Vercel 等）
- 修复方案为通用模式；具体文件路径和配置语法因项目而异
- 不涵盖服务器层面的优化（CDN 配置、PHP opcode 缓存、数据库查询等）
- 图片转换命令假设用户已安装所需工具（cwebp、sharp、Pillow）
- CSP 指南采用仅报告模式的迭代方法 — 最终策略需根据每个项目的实际资源来源进行调整

---

## 变更日志与回滚清单

每完成一个修复批次后，记录更改内容及是否导致构建失败：

| 修复操作                        | 修改的文件                                                      | 构建通过？ | 错误信息 | 回滚步骤                                   |
|---------------------------------|-----------------------------------------------------------------|-----------|----------|--------------------------------------------|
| F1.1 — CSS @import → `<link>`   | `index.html`, `src/styles/*.css`                                | □ 是 □ 否 |          | 恢复原始 `<link>` 标签                    |
| F1.2 — 延迟渲染阻塞 CSS         | `index.html`                                                   | □ 是 □ 否 |          | 移除 `media="print"` + `onload`           |
| F1.4 — WebP 转换               | `public/images/*.webp`                                          | □ 是 □ 否 |          | 删除 .webp 文件，恢复原始图片              |
| F1.5 — 图片尺寸                | `src/components/*.tsx`                                          | □ 是 □ 否 |          | 移除 `width`/`height`/`loading` 属性      |
| F1.6 — 安全响应头（Netlify）    | `netlify.toml`                                                 | □ 是 □ 否 |          | 删除 `[[headers]]` 区块                   |
| F1.7 — 安全响应头（Vercel）     | `vercel.json`                                                   | □ 是 □ 否 |          | 删除 `"headers"` 数组条目                 |
| F1.8 — 自托管字体              | `public/fonts/*.woff2`, `src/styles/fonts.css`, `index.html`    | □ 是 □ 否 |          | 删除字体文件，移除 `@font-face`，恢复 Google Fonts `<link>` |
| F1.9 — 调整图标尺寸            | `public/favicon*`, `public/apple-touch-icon*`, `public/og-image*` | □ 是 □ 否 |          | 恢复原始图标文件                           |
| F2.1 — LCP eager 加载          | `src/components/*.tsx`                                          | □ 是 □ 否 |          | 将 `loading="eager"` 改回 `loading="lazy"` |
| F2.2 — 预加载 LCP 图片          | `index.html` 或 `src/components/*.tsx`                           | □ 是 □ 否 |          | 移除 `<link rel="preload">` 或还原 `<picture>` |
| F2.3 — JS 代码分割             | `vite.config.ts`                                                | □ 是 □ 否 |          | 移除 `manualChunks` 配置                  |
| F2.4 — 修复强制重排            | `src/**/*.ts`                                                   | □ 是 □ 否 |          | 还原几何属性缓存相关的改动                |
| F2.5 — 优化 DOM                | `src/components/*.tsx`                                          | □ 是 □ 否 |          | 恢复已删除的隐藏节点                     |
| F3.1 — 外部 API 移至构建时      | `src/**/*.ts`, config files                                      | □ 是 □ 否 |          | 恢复客户端 fetch 调用                     |
| F3.2 — CSP 响应头              | `netlify.toml` / `vercel.json`                                  | □ 是 □ 否 |          | 删除或放宽 CSP 指令                       |

若**构建通过？**为**否**，运行 `npm run build` 查看具体错误，立即回滚失败的修复，在应用下一批次前重新测试。

---

## 参考资料

详见 `references/` 目录下的深入资料：
- `references/performance-deep-dive.md` — LCP、CLS、TBT 根因分析树
- `references/security-headers.md` — 完整的 CSP/HSTS/COOP 参考手册
- `references/image-optimization.md` — WebP/AVIF 转换流水线
