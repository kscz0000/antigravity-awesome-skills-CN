---
name: astro-static
description: Astro 静态站点模板原则。内容导向网站、博客、文档。触发词：Astro站点、静态博客、文档站、Astro项目
---
# Astro 静态站点模板

## 技术栈

| 组件 | 技术 |
|-----------|------------|
| 框架 | Astro 4.x |
| 内容 | MDX + Content Collections |
| 样式 | Tailwind CSS |
| 集成 | Sitemap、RSS、SEO |
| 输出 | 静态/SSG |

---

## 目录结构

```
project-name/
├── src/
│   ├── components/      # .astro 组件
│   ├── content/         # MDX 内容
│   │   ├── blog/
│   │   └── config.ts    # 集合模式
│   ├── layouts/         # 页面布局
│   ├── pages/           # 基于文件的路由
│   └── styles/
├── public/              # 静态资源
├── astro.config.mjs
└── package.json
```

---

## 核心概念

| 概念 | 描述 |
|---------|-------------|
| Content Collections | 使用 Zod 模式的类型安全内容 |
| Islands 架构 | 部分水合实现交互 |
| 默认零 JS | 默认静态 HTML，按需添加 |
| MDX 支持 | Markdown 中使用组件 |

---

## 设置步骤

1. `npm create astro@latest {{name}}`
2. 添加集成: `npx astro add mdx tailwind sitemap`
3. 配置 `astro.config.mjs`
4. 创建 content collections
5. `npm run dev`

---

## 部署

| 平台 | 方法 |
|----------|--------|
| Vercel | 自动检测 |
| Netlify | 自动检测 |
| Cloudflare Pages | 自动检测 |
| GitHub Pages | 构建 + 部署 action |

---

## 最佳实践

- 使用 Content Collections 确保类型安全
- 利用静态生成
- 仅在需要的地方添加 islands
- 使用 Astro Image 优化图片
