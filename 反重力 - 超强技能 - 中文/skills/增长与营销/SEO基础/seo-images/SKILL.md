---
name: seo-images
description: >
  图片优化分析，用于 SEO 和性能优化。检查 alt 文本、文件大小、格式、响应式图片、懒加载和 CLS 防护。当用户说"图片优化"、"alt 文本"、"图片 SEO"、"图片大小"、"图片审计"、"image optimization"、"alt text"、"image SEO"时使用。
risk: safe
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

# 图片优化分析

## 何时使用
- 审计图片 SEO、alt 文本、文件大小、格式或懒加载时使用。
- 用户需要图片相关的性能建议时使用。
- 检查影响 SEO 和 Core Web Vitals 的媒体质量信号时使用。

## 检查项

### Alt 文本
- 所有 `<img>` 元素都应有 alt 属性（装饰性图片除外：`role="presentation"`）
- 描述性：描述图片内容，而非 "image.jpg" 或 "photo"
- 在自然的情况下包含相关关键词，避免关键词堆砌
- 长度：10-125 个字符

**好的示例：**
- "Professional plumber repairing kitchen sink faucet"
- "Red 2024 Toyota Camry sedan front view"
- "Team meeting in modern office conference room"

**差的示例：**
- "image.jpg"（文件名，非描述）
- "plumber plumbing plumber services"（关键词堆砌）
- "Click here"（无描述性）

### 文件大小

**按图片类别分层的阈值：**

| 图片类别 | 目标值 | 警告值 | 严重值 |
|----------|--------|--------|--------|
| 缩略图 | < 50KB | > 100KB | > 200KB |
| 内容图片 | < 100KB | > 200KB | > 500KB |
| Hero/横幅图片 | < 200KB | > 300KB | > 700KB |

建议在不损失质量的情况下压缩至目标阈值。

### 格式
| 格式 | 浏览器支持 | 使用场景 |
|------|------------|----------|
| WebP | 97%+ | 默认推荐 |
| AVIF | 92%+ | 最佳压缩，较新 |
| JPEG | 100% | 照片的后备格式 |
| PNG | 100% | 需要透明度的图形 |
| SVG | 100% | 图标、Logo、插图 |

推荐使用 WebP/AVIF 替代 JPEG/PNG。检查是否有带格式后备的 `<picture>` 元素。

#### 推荐的 `<picture>` 元素模式

使用渐进增强，优先使用最高效的格式：

```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Descriptive alt text" width="800" height="600" loading="lazy" decoding="async">
</picture>
```

浏览器将使用第一个支持的格式。当前浏览器支持率：AVIF 93.8%，WebP 95.3%。

#### JPEG XL：新兴格式

2025 年 11 月，Google 的 Chromium 团队推翻了 2022 年的决定，宣布将在 Chrome 中使用基于 Rust 的解码器恢复 JPEG XL 支持。该实现已功能完整但尚未进入 Chrome 稳定版。JPEG XL 提供无损 JPEG 重压缩（约 20% 节省且零质量损失）和有竞争力的有损压缩。目前尚未准备好用于 Web 部署，但值得持续关注以备将来采用。

### 响应式图片
- 使用 `srcset` 属性提供多种尺寸
- 使用 `sizes` 属性匹配布局断点
- 为设备像素比提供适当的分辨率

```html
<img
  src="image-800.jpg"
  srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Description"
>
```

### 懒加载
- 首屏以下的图片使用 `loading="lazy"`
- 不要对首屏/Hero 图片使用懒加载（会损害 LCP）
- 检查是原生懒加载还是基于 JavaScript 的懒加载

```html
<!-- 首屏以下 - 懒加载 -->
<img src="photo.jpg" loading="lazy" alt="Description">

<!-- 首屏 - 立即加载（默认） -->
<img src="hero.jpg" alt="Hero image">
```

### LCP 图片使用 `fetchpriority="high"`

为 Hero/LCP 图片添加 `fetchpriority="high"` 以在浏览器网络队列中优先下载：

```html
<img src="hero.webp" fetchpriority="high" alt="Hero image description" width="1200" height="630">
```

**关键：** 不要对首屏/LCP 图片使用懒加载。在 LCP 图片上使用 `loading="lazy"` 会直接损害 LCP 分数。`loading="lazy"` 仅用于首屏以下的图片。

### 非 LCP 图片使用 `decoding="async"`

为非 LCP 图片添加 `decoding="async"` 以防止图片解码阻塞主线程：

```html
<img src="photo.webp" alt="Description" width="600" height="400" loading="lazy" decoding="async">
```

### CLS 防护
- 所有 `<img>` 元素都应设置 `width` 和 `height` 属性
- 或使用 CSS `aspect-ratio` 作为替代方案
- 标记没有尺寸的图片

```html
<!-- 好 - 设置了尺寸 -->
<img src="photo.jpg" width="800" height="600" alt="Description">

<!-- 好 - CSS 宽高比 -->
<img src="photo.jpg" style="aspect-ratio: 4/3" alt="Description">

<!-- 差 - 无尺寸 -->
<img src="photo.jpg" alt="Description">
```

### 文件名
- 描述性：`blue-running-shoes.webp` 而非 `IMG_1234.jpg`
- 使用连字符分隔、小写、无特殊字符
- 包含相关关键词

### CDN 使用
- 检查图片是否从 CDN 提供（不同域名、CDN 响应头）
- 对图片密集型网站推荐使用 CDN
- 检查边缘缓存响应头

## 输出

### 图片审计摘要

| 指标 | 状态 | 数量 |
|------|------|------|
| 图片总数 | - | XX |
| 缺少 Alt 文本 | ❌ | XX |
| 过大（>200KB） | ⚠️ | XX |
| 格式错误 | ⚠️ | XX |
| 无尺寸 | ⚠️ | XX |
| 未懒加载 | ⚠️ | XX |

### 优先优化列表

按文件大小影响排序（节省空间最大的优先）：

| 图片 | 当前大小 | 格式 | 问题 | 预计节省 |
|------|----------|------|------|----------|
| ... | ... | ... | ... | ... |

### 建议
1. 将 X 张图片转换为 WebP 格式（预计节省 XX KB）
2. 为 X 张图片添加 alt 文本
3. 为 X 张图片添加尺寸属性
4. 为 X 张首屏以下图片启用懒加载
5. 压缩 X 张过大的图片

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| URL 无法访问 | 报告连接错误及状态码。建议验证 URL 并检查网站是否需要身份验证。 |
| 页面未找到图片 | 报告未检测到 `<img>` 元素。建议检查图片是否通过 JavaScript 或 CSS background-image 加载。 |
| 图片位于 CDN 或需要身份验证 | 说明无法直接访问图片文件进行大小分析。报告可用的元数据（alt 文本、尺寸、从标记获取的格式）并标记无法访问的资源。 |

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
