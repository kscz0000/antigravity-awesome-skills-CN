---
name: web-performance-optimization
description: "优化网站和 Web 应用性能，包括加载速度、Core Web Vitals、bundle 体积、缓存策略和运行时性能"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Web 性能优化

## 概述

帮助开发者优化网站和 Web 应用性能，提升用户体验、SEO 排名和转化率。本技能提供系统化的方法来度量、分析和改进加载速度、运行时性能以及 Core Web Vitals 指标。

## 何时使用本技能

- 当网站或应用加载缓慢时使用
- 当优化 Core Web Vitals（LCP、FID、CLS）时使用
- 当减少 JavaScript bundle 体积时使用
- 当改进 Time to Interactive（TTI）时使用
- 当优化图片和资源时使用
- 当实现缓存策略时使用
- 当调试性能瓶颈时使用
- 当准备性能审计时使用

## 工作原理

### 步骤 1：度量当前性能

我会帮助你建立基线指标：
- 运行 Lighthouse 审计
- 度量 Core Web Vitals（LCP、FID、CLS）
- 检查 bundle 体积
- 分析网络瀑布图
- 识别性能瓶颈

### 步骤 2：识别问题

分析性能问题：
- JavaScript bundle 过大
- 图片未优化
- 阻塞渲染的资源
- 服务器响应时间过慢
- 缺少缓存头
- 布局偏移
- 长时间任务阻塞主线程

### 步骤 3：确定优化优先级

聚焦于高影响的改进：
- 关键渲染路径优化
- 代码分割与懒加载
- 图片优化
- 缓存策略
- 第三方脚本优化

### 步骤 4：实施优化

应用性能改进：
- 优化资源（图片、字体、CSS、JS）
- 实施代码分割
- 添加缓存头
- 懒加载非关键资源
- 优化关键渲染路径

### 步骤 5：验证改进效果

衡量变更带来的影响：
- 重新运行 Lighthouse 审计
- 对比优化前后的指标
- 监控真实用户指标（RUM）
- 在不同设备和网络下测试

## 示例

### 示例 1：优化 Core Web Vitals

```markdown
## 性能审计结果

### 当前指标（优化前）
- **LCP（Largest Contentful Paint，最大内容绘制）：** 4.2s ❌（应 < 2.5s）
- **FID（First Input Delay，首次输入延迟）：** 180ms ❌（应 < 100ms）
- **CLS（Cumulative Layout Shift，累计布局偏移）：** 0.25 ❌（应 < 0.1）
- **Lighthouse 分数：** 62/100

### 已识别的问题

1. **LCP 问题：** 首屏图片（2.5MB）加载缓慢
2. **FID 问题：** 大体积 JavaScript bundle（850KB）阻塞主线程
3. **CLS 问题：** 未指定尺寸的图片导致布局偏移

### 优化方案

#### 修复 LCP（Largest Contentful Paint）

**问题：** 首屏图片为 2.5MB，加载缓慢

**解决方案：**
\`\`\`html
<!-- 优化前：未优化的图片 -->
<img src="/hero.jpg" alt="Hero">

<!-- 优化后：使用现代格式 -->
<picture>
  <source srcset="/hero.avif" type="image/avif">
  <source srcset="/hero.webp" type="image/webp">
  <img
    src="/hero.jpg"
    alt="Hero"
    width="1200"
    height="600"
    loading="eager"
    fetchpriority="high"
  >
</picture>
\`\`\`

**额外优化：**
- 将图片压缩至 < 200KB
- 使用 CDN 加速分发
- 预加载首屏图片：`<link rel="preload" as="image" href="/hero.avif">`

#### 修复 FID（First Input Delay）

**问题：** 850KB 的 JavaScript bundle 阻塞主线程

**解决方案：**

1. **代码分割：**
\`\`\`javascript
// 优化前：所有内容打包在一个 bundle 中
import { HeavyComponent } from './HeavyComponent';
import { Analytics } from './analytics';
import { ChatWidget } from './chat';

// 优化后：懒加载非关键代码
const HeavyComponent = lazy(() => import('./HeavyComponent'));
const ChatWidget = lazy(() => import('./chat'));

// 在页面可交互后加载分析脚本
if (typeof window !== 'undefined') {
  window.addEventListener('load', () => {
    import('./analytics').then(({ Analytics }) => {
      Analytics.init();
    });
  });
}
\`\`\`

2. **移除未使用的依赖：**
\`\`\`bash
# 分析 bundle
npx webpack-bundle-analyzer

# 移除未使用的包
npm uninstall moment  # 改用 date-fns（更小）
npm install date-fns
\`\`\`

3. **延迟加载非关键脚本：**
\`\`\`html
<!-- 优化前：阻塞渲染 -->
<script src="/analytics.js"></script>

<!-- 优化后：延迟加载 -->
<script src="/analytics.js" defer></script>
\`\`\`

#### 修复 CLS（Cumulative Layout Shift）

**问题：** 未指定尺寸的图片导致布局偏移

**解决方案：**
\`\`\`html
<!-- 优化前：未指定尺寸 -->
<img src="/product.jpg" alt="Product">

<!-- 优化后：指定尺寸 -->
<img
  src="/product.jpg"
  alt="Product"
  width="400"
  height="300"
  style="aspect-ratio: 4/3;"
>
\`\`\`

**针对动态内容：**
\`\`\`css
/* 为稍后加载的内容预留空间 */
.skeleton-loader {
  min-height: 200px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
\`\`\`

### 优化后的结果

- **LCP：** 1.8s ✅（提升 57%）
- **FID：** 45ms ✅（提升 75%）
- **CLS：** 0.05 ✅（提升 80%）
- **Lighthouse 分数：** 94/100 ✅
```

### 示例 2：减少 JavaScript Bundle 体积

```markdown
## Bundle 体积优化

### 当前状态
- **总 Bundle：** 850KB（gzip 后：280KB）
- **主 Bundle：** 650KB
- **第三方 Bundle：** 200KB
- **加载时间（3G）：** 8.2s

### 分析

\`\`\`bash
# 分析 bundle 构成
npx webpack-bundle-analyzer dist/stats.json
\`\`\`

**发现：**
1. Moment.js：67KB（可替换为 date-fns：12KB）
2. Lodash：72KB（导入了整个库，实际只用了 5 个函数）
3. 未使用代码：约 150KB 死代码
4. 没有代码分割：所有内容都打包在一个 bundle 中

### 优化步骤

#### 1. 替换重量级依赖

\`\`\`bash
# 移除 moment.js（67KB）→ 改用 date-fns（12KB）
npm uninstall moment
npm install date-fns

# 优化前
import moment from 'moment';
const formatted = moment(date).format('YYYY-MM-DD');

# 优化后
import { format } from 'date-fns';
const formatted = format(date, 'yyyy-MM-dd');
\`\`\`

**节省：** 55KB

#### 2. 按需使用 Lodash

\`\`\`javascript
// 优化前：导入整个库（72KB）
import _ from 'lodash';
const unique = _.uniq(array);

// 优化后：仅导入需要的部分（5KB）
import uniq from 'lodash/uniq';
const unique = uniq(array);

// 或使用原生方法
const unique = [...new Set(array)];
\`\`\`

**节省：** 67KB

#### 3. 实施代码分割

\`\`\`javascript
// Next.js 示例
import dynamic from 'next/dynamic';

// 懒加载重量级组件
const Chart = dynamic(() => import('./Chart'), {
  loading: () => <div>Loading chart...</div>,
  ssr: false
});

const AdminPanel = dynamic(() => import('./AdminPanel'), {
  loading: () => <div>Loading...</div>
});

// 基于路由的代码分割（Next.js 自动支持）
// pages/admin.js - 仅在访问 /admin 时加载
// pages/dashboard.js - 仅在访问 /dashboard 时加载
\`\`\`

#### 4. 移除死代码

\`\`\`javascript
// 在 webpack.config.js 中启用 tree shaking
module.exports = {
  mode: 'production',
  optimization: {
    usedExports: true,
    sideEffects: false
  }
};

// 在 package.json 中
{
  "sideEffects": false
}
\`\`\`

#### 5. 优化第三方脚本

\`\`\`html
<!-- 优化前：立即加载 -->
<script src="https://analytics.com/script.js"></script>

<!-- 优化后：页面可交互后加载 -->
<script>
  window.addEventListener('load', () => {
    const script = document.createElement('script');
    script.src = 'https://analytics.com/script.js';
    script.async = true;
    document.body.appendChild(script);
  });
</script>
\`\`\`

### 结果

- **总 Bundle：** 380KB ✅（减少 55%）
- **主 Bundle：** 180KB ✅
- **第三方 Bundle：** 80KB ✅
- **加载时间（3G）：** 3.1s ✅（提升 62%）
```

### 示例 3：图片优化策略

```markdown
## 图片优化

### 当前问题
- 15 张图片总计 12MB
- 未使用现代格式（WebP、AVIF）
- 没有响应式图片
- 没有懒加载

### 优化策略

#### 1. 转换为现代格式

\`\`\`bash
# 安装图片优化工具
npm install sharp

# 转换脚本（optimize-images.js）
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

async function optimizeImage(inputPath, outputDir) {
  const filename = path.basename(inputPath, path.extname(inputPath));

  // 生成 WebP
  await sharp(inputPath)
    .webp({ quality: 80 })
    .toFile(path.join(outputDir, \`\${filename}.webp\`));

  // 生成 AVIF（最佳压缩率）
  await sharp(inputPath)
    .avif({ quality: 70 })
    .toFile(path.join(outputDir, \`\${filename}.avif\`));

  // 生成优化后的 JPEG 兜底
  await sharp(inputPath)
    .jpeg({ quality: 80, progressive: true })
    .toFile(path.join(outputDir, \`\${filename}.jpg\`));
}

// 处理所有图片
const images = fs.readdirSync('./images');
images.forEach(img => {
  optimizeImage(\`./images/\${img}\`, './images/optimized');
});
\`\`\`

#### 2. 实现响应式图片

\`\`\`html
<!-- 使用现代格式的响应式图片 -->
<picture>
  <!-- 支持 AVIF 的浏览器（最佳压缩率） -->
  <source
    srcset="
      /images/hero-400.avif 400w,
      /images/hero-800.avif 800w,
      /images/hero-1200.avif 1200w
    "
    type="image/avif"
    sizes="(max-width: 768px) 100vw, 50vw"
  >

  <!-- 支持 WebP 的浏览器 -->
  <source
    srcset="
      /images/hero-400.webp 400w,
      /images/hero-800.webp 800w,
      /images/hero-1200.webp 1200w
    "
    type="image/webp"
    sizes="(max-width: 768px) 100vw, 50vw"
  >

  <!-- JPEG 兜底 -->
  <img
    src="/images/hero-800.jpg"
    srcset="
      /images/hero-400.jpg 400w,
      /images/hero-800.jpg 800w,
      /images/hero-1200.jpg 1200w
    "
    sizes="(max-width: 768px) 100vw, 50vw"
    alt="Hero image"
    width="1200"
    height="600"
    loading="lazy"
  >
</picture>
\`\`\`

#### 3. 懒加载

\`\`\`html
<!-- 原生懒加载 -->
<img
  src="/image.jpg"
  alt="Description"
  loading="lazy"
  width="800"
  height="600"
>

<!-- 首屏图片立即加载 -->
<img
  src="/hero.jpg"
  alt="Hero"
  loading="eager"
  fetchpriority="high"
>
\`\`\`

#### 4. Next.js Image 组件

\`\`\`javascript
import Image from 'next/image';

// 自动优化
<Image
  src="/hero.jpg"
  alt="Hero"
  width={1200}
  height={600}
  priority  // 用于首屏图片
  quality={80}
/>

// 懒加载
<Image
  src="/product.jpg"
  alt="Product"
  width={400}
  height={300}
  loading="lazy"
/>
\`\`\`

### 结果

| 指标 | 优化前 | 优化后 | 提升幅度 |
|--------|--------|-------|-------------|
| 图片总大小 | 12MB | 1.8MB | 减少 85% |
| LCP | 4.5s | 1.6s | 提升 64% |
| 页面加载（3G） | 18s | 4.2s | 提升 77% |
```

## 最佳实践

### ✅ 推荐做法

- **先度量** - 优化前务必建立基线指标
- **使用 Lighthouse** - 定期运行审计，跟踪进度
- **优化图片** - 使用现代格式（WebP、AVIF）和响应式图片
- **代码分割** - 将大 bundle 拆分为更小的块
- **懒加载** - 延迟加载非关键资源
- **积极缓存** - 为静态资源设置合适的缓存头
- **减少主线程工作** - 将 JavaScript 执行控制在 50ms 以内
- **预加载关键资源** - 使用 `<link rel="preload">` 预加载关键资源
- **使用 CDN** - 通过 CDN 分发静态资源以提升速度
- **监控真实用户** - 跟踪真实用户的 Core Web Vitals

### ❌ 应避免的做法

- **不要盲目优化** - 先度量，再优化
- **不要忽略移动端** - 在真实移动设备和慢速网络下测试
- **不要阻塞渲染** - 避免阻塞渲染的 CSS 和 JavaScript
- **不要一次性加载所有内容** - 懒加载非关键资源
- **不要忘记指定尺寸** - 始终为图片指定 width/height
- **不要使用同步脚本** - 使用 async 或 defer 属性
- **不要忽略第三方脚本** - 它们常常导致性能问题
- **不要跳过压缩** - 始终对资源进行压缩和最小化

## 常见陷阱

### 问题：桌面端优化良好但移动端缓慢
**症状：** 桌面端 Lighthouse 分数良好，移动端却很差
**解决方案：**
- 在真实移动设备上测试
- 使用 Chrome DevTools 的移动节流功能
- 针对 3G/4G 网络优化
- 减少 JavaScript 执行时间
```bash
# 使用节流进行测试
lighthouse https://yoursite.com --throttling.cpuSlowdownMultiplier=4
```

### 问题：JavaScript Bundle 体积过大
**症状：** Time to Interactive（TTI）过长，FID 偏高
**解决方案：**
- 使用 webpack-bundle-analyzer 分析 bundle
- 移除未使用的依赖
- 实施代码分割
- 懒加载非关键代码
```bash
# 分析 bundle
npx webpack-bundle-analyzer dist/stats.json
```

### 问题：图片导致布局偏移
**症状：** CLS 分数偏高，内容跳动
**解决方案：**
- 始终指定 width 和 height
- 使用 aspect-ratio CSS 属性
- 使用骨架屏预留空间
```css
img {
  aspect-ratio: 16 / 9;
  width: 100%;
  height: auto;
}
```

### 问题：服务器响应时间过慢
**症状：** TTFB（Time to First Byte）过高
**解决方案：**
- 实施服务端缓存
- 使用 CDN 分发静态资源
- 优化数据库查询
- 考虑使用静态站点生成（SSG）
```javascript
// Next.js：静态生成
export async function getStaticProps() {
  const data = await fetchData();
  return {
    props: { data },
    revalidate: 60 // 每 60 秒重新生成
  };
}
```

## 性能检查清单

### 图片
- [ ] 转换为现代格式（WebP、AVIF）
- [ ] 实现响应式图片
- [ ] 添加懒加载
- [ ] 指定尺寸（width/height）
- [ ] 压缩图片（每张 < 200KB）
- [ ] 使用 CDN 分发

### JavaScript
- [ ] Bundle 体积 < 200KB（gzip 后）
- [ ] 实施代码分割
- [ ] 懒加载非关键代码
- [ ] 移除未使用的依赖
- [ ] 最小化和压缩
- [ ] 脚本使用 async/defer

### CSS
- [ ] 内联关键 CSS
- [ ] 延迟加载非关键 CSS
- [ ] 移除未使用的 CSS
- [ ] 最小化 CSS 文件
- [ ] 使用 CSS containment

### 缓存
- [ ] 为静态资源设置缓存头
- [ ] 实施 service worker
- [ ] 使用 CDN 缓存
- [ ] 缓存 API 响应
- [ ] 为静态资源添加版本号

### Core Web Vitals
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1
- [ ] TTFB < 600ms
- [ ] TTI < 3.8s

## 性能工具

### 度量工具
- **Lighthouse** - 综合性能审计
- **WebPageTest** - 详细的瀑布图分析
- **Chrome DevTools** - 性能剖析
- **PageSpeed Insights** - 真实用户指标
- **Web Vitals Extension** - 监控 Core Web Vitals

### 分析工具
- **webpack-bundle-analyzer** - 可视化 bundle 构成
- **source-map-explorer** - 分析 bundle 体积
- **Bundlephobia** - 安装前检查包体积
- **ImageOptim** - 图片压缩工具

### 监控工具
- **Google Analytics** - 跟踪 Core Web Vitals
- **Sentry** - 性能监控
- **New Relic** - 应用性能监控
- **Datadog** - 真实用户监控

## 相关技能

- `@react-best-practices` - React 性能模式
- `@frontend-dev-guidelines` - 前端开发规范
- `@systematic-debugging` - 调试性能问题
- `@senior-architect` - 面向性能的架构

## 补充资源

- [Web.dev Performance](https://web.dev/performance/)
- [Core Web Vitals](https://web.dev/vitals/)
- [Lighthouse Documentation](https://developers.google.com/web/tools/lighthouse)
- [MDN Performance Guide](https://developer.mozilla.org/en-US/docs/Web/Performance)
- [Next.js Performance](https://nextjs.org/docs/advanced-features/measuring-performance)
- [Image Optimization Guide](https://web.dev/fast/#optimize-your-images)

---

**专业建议：** 优先关注 Core Web Vitals（LCP、FID、CLS），它们对用户体验和 SEO 排名的影响最大！

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出结果替代环境相关的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并寻求澄清。
