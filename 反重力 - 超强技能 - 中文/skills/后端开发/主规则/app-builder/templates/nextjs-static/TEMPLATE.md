---
name: nextjs-static
description: Next.js 静态站点模板原则。落地页、作品集、营销页面。触发词：静态网站、落地页、作品集、Next.js静态
---
# Next.js 静态站点模板

## 技术栈

| 组件 | 技术 |
|-----------|------------|
| 框架 | Next.js 14 (静态导出) |
| 语言 | TypeScript |
| 样式 | Tailwind CSS |
| 动画 | Framer Motion |
| 图标 | Lucide React |
| SEO | Next SEO |

---

## 目录结构

```
project-name/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx      # 落地页
│   │   ├── about/
│   │   ├── contact/
│   │   └── blog/
│   ├── components/
│   │   ├── layout/       # Header, Footer
│   │   ├── sections/     # Hero, Features, CTA
│   │   └── ui/
│   └── lib/
├── content/              # Markdown 内容
├── public/
└── next.config.js
```

---

## 静态导出配置

```javascript
// next.config.js
const nextConfig = {
  output: 'export',
  images: { unoptimized: true },
  trailingSlash: true,
};
```

---

## 落地页区块

| 区块 | 用途 |
|---------|---------|
| Hero | 主标题、CTA |
| Features | 产品优势 |
| Testimonials | 社会证明 |
| Pricing | 定价方案 |
| CTA | 最终转化 |

---

## 动画模式

| 模式 | 用途 |
|---------|-----|
| 淡入上移 | 内容入场 |
| 交错 | 列表项 |
| 滚动显示 | 进入视口时 |
| 悬停 | 交互反馈 |

---

## 设置步骤

1. `npx create-next-app {{name}} --typescript --tailwind --app`
2. 安装: `npm install framer-motion lucide-react next-seo`
3. 配置静态导出
4. 创建区块
5. `npm run dev`

---

## 部署

| 平台 | 方法 |
|----------|--------|
| Vercel | 自动 |
| Netlify | 自动 |
| GitHub Pages | gh-pages 分支 |
| 任意主机 | 上传 `out` 文件夹 |

---

## 最佳实践

- 静态导出以获得最佳性能
- Framer Motion 实现高级动画
- 移动优先的响应式设计
- 每个页面配置 SEO 元数据
