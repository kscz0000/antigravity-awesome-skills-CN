---
id: image-optimization-cost-control
title: Image optimization cost control
status: active
candidateKinds: ["image_optimization"]
frameworks: ["*"]
priority: 90
citations: ["https://vercel.com/docs/image-optimization", "https://vercel.com/docs/image-optimization/managing-image-optimization-costs", "https://vercel.com/docs/image-optimization/limits-and-pricing"]
maxBriefChars: 850
---

## 调查简报
图像建议应区分真实的面向用户的图像工作和浪费的转换。

## 需要检查的证据
检查采样文件的原始图像标签、尺寸、远程源、重复转换、源图像限制、图标、SVG、GIF 以及现有的框架图像组件。

## 何时不建议
不要仅仅因为它们是图像就将微小图标、SVG UI 资产或动画 GIF 路由到图像优化。不要在未检查现有配置的情况下更改远程源策略。

## 验证
命名图像文件或组件、当前渲染路径以及使优化有意义的指标或扫描器证据。