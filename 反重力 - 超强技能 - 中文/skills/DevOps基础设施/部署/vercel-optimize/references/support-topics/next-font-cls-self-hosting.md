---
id: next-font-cls-self-hosting
title: Next.js font CLS guardrail
status: active
candidateKinds: ["cwv_poor"]
frameworks: ["next@>=13.2.0"]
metrics: ["CLS"]
priority: 86
citations: ["https://nextjs.org/docs/app/api-reference/components/font", "https://web.dev/articles/optimize-cls"]
maxBriefChars: 800
---

## 调查简报
对于不佳的 CLS，仅当路由实际加载外部字体 CSS 或在渲染后交换文本时才检查字体。

## 需要检查的证据
检查布局和全局样式中的外部字体链接、CSS 导入、自定义 font-face 规则、延迟加载的字体类以及是否已使用 `next/font`。

## 何时不建议
当 CLS 由图像、广告、嵌入或注入的 UI 引起时，不要迁移字体。不要为不受支持的 Next.js 版本建议 `next/font`。

## 验证
命名 CLS 值、字体加载机制以及要更改的确切布局或样式表行。