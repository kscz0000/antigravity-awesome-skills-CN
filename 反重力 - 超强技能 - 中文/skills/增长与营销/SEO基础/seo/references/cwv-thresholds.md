<!-- 更新时间: 2026-02-07 -->
# Core Web Vitals 阈值（2026 年 2 月）

## 当前指标

| 指标 | 良好 | 需改进 | 较差 |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤2.5s | 2.5s–4.0s | >4.0s |
| INP (Interaction to Next Paint) | ≤200ms | 200ms–500ms | >500ms |
| CLS (Cumulative Layout Shift) | ≤0.1 | 0.1–0.25 | >0.25 |

## 关键事实
- INP 于 **2024 年 3 月 12 日**取代了 FID (First Input Delay)。FID 于 **2024 年 9 月 9 日**从所有 Chrome 工具（CrUX API、PageSpeed Insights、Lighthouse）中完全移除。INP 是唯一的交互性指标。
- 评估使用真实用户数据的 **75 百分位数**（来自 CrUX 的现场数据）。
- Google 在**页面级别**和**源站级别**进行评估。
- Core Web Vitals 是**决胜局**排名信号：当竞争对手的内容质量相似时，它们最为重要。
- **阈值自最初定义以来未改变**：忽略 SEO 博客中关于"阈值收紧"的说法。
- 2025 年 12 月核心更新似乎对**移动端 CWV** 赋予了更高权重。
- 截至 2025 年 10 月：**57.1%** 的桌面网站和 **49.7%** 的移动网站通过全部三项 CWV。

## LCP 子部分（2025 年 2 月 CrUX 新增）

LCP 现在可以分解为诊断子部分：

| 子部分 | 测量内容 | 目标 |
|---------|------------------|--------|
| **TTFB** | Time to First Byte（服务器响应） | <800ms |
| **Resource Load Delay** | 从 TTFB 到资源请求开始的时间 | 最小化 |
| **Resource Load Time** | 下载 LCP 资源的时间 | 取决于大小 |
| **Element Render Delay** | 从资源加载到渲染的时间 | 最小化 |

**总 LCP = TTFB + Resource Load Delay + Resource Load Time + Element Render Delay**

使用此分解来识别哪个阶段导致 LCP 问题。

## Soft Navigations API（实验性）

**Chrome 139+ Origin Trial（2025 年 7 月）**：迈向在 SPA 中测量 CWV 的第一步。

- 解决了长期存在的 SPA 测量盲点
- 目前为实验性，**尚无排名影响**
- 检测"软导航"（无完整页面加载的 URL 变更）
- 可能影响未来的 SPA CWV 测量

**检测：**检查 SPA 框架（React、Vue、Angular、Svelte）并警告当前 CWV 测量限制。

## 测量来源

### 现场数据（真实用户）
- Chrome User Experience Report (CrUX)
- PageSpeed Insights（使用 CrUX 数据）
- Search Console Core Web Vitals 报告

### 实验室数据（模拟）
- Lighthouse
- WebPageTest
- Chrome DevTools

> 现场数据是 Google 用于排名的数据。实验室数据对调试有用。

## 常见瓶颈

### LCP (Largest Contentful Paint)
- 未优化的主图（压缩、使用 WebP/AVIF、添加预加载）
- 渲染阻塞 CSS/JS（defer、async、关键 CSS 内联）
- 服务器响应慢（TTFB >200ms：使用边缘 CDN、缓存）
- 第三方脚本阻塞（延迟分析、聊天小部件）
- Web 字体加载延迟（使用 font-display: swap + 预加载）

### INP (Interaction to Next Paint)
- 主线程上的长 JavaScript 任务（分解为 <50ms 的小任务）
- 繁重的事件处理程序（防抖、使用 requestAnimationFrame）
- 过大的 DOM 大小（>1,500 个元素需要关注）
- 第三方脚本劫持主线程
- 同步 XHR 或 localStorage 操作
- 布局抖动（多次强制重排）

### CLS (Cumulative Layout Shift)
- 图片/iframe 缺少宽度/高度尺寸
- 在现有内容上方动态注入内容
- Web 字体导致布局偏移（使用 font-display: swap + 预加载）
- 广告/嵌入内容未预留空间
- 延迟加载的内容将页面推下

## 优化优先级

1. **LCP**：对感知性能影响最大
2. **CLS**：影响用户体验的最常见问题
3. **INP**：对交互式应用程序最重要

## 工具

```bash
# PageSpeed Insights API
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL&key=API_KEY"

# Lighthouse CLI
npx lighthouse URL --output json --output-path report.json
```

## 性能工具更新（2025）

- **Lighthouse 13.0**（2025 年 10 月）：重大审计重组，重新组织了性能类别并更新了评分权重。Lighthouse 是实验室工具（模拟条件）：始终与 CrUX 现场数据交叉验证以了解真实性能。
- **CrUX Vis** 于 2025 年 11 月取代了 CrUX Dashboard。旧的 Looker Studio 仪表板已弃用。使用 [CrUX Vis](https://cruxvis.withgoogle.com) 或直接使用 CrUX API。
- **LCP 子部分**于 2025 年 2 月添加到 CrUX：Time to First Byte (TTFB)、资源加载延迟、资源加载时间和元素渲染延迟现在作为 CrUX 数据中 LCP 的子组件可用。
- **Google Search Console 2025 功能**（2025 年 12 月）：AI 驱动的自动分析配置。品牌与非品牌查询过滤器。API 中提供每小时数据。自定义图表注释。社交渠道跟踪。

> **移动优先索引**已于 2024 年 7 月 5 日 100% 完成。Google 现在仅使用移动 Googlebot 用户代理抓取和索引所有网站。确保您的移动版本包含所有关键内容、结构化数据和元标签。
