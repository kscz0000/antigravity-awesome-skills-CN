---
name: "landing-page-generator"
description: "生成高转化率的 Next.js/React 落地页，使用 Tailwind CSS。采用 PAS、AIDA、BAB 文案框架优化文案和组件（首屏、功能、定价），聚焦 Core Web Vitals 和 SEO。当用户要求'生成落地页'、'创建着陆页'、'制作产品落地页'或 'landing page generator' 时使用。"
category: "front-end"
risk: "safe"
source: "community"
date_added: "2026-03-18"
author: "alirezarezvani"
tags: ["nextjs", "react", "tailwind", "landing-page", "marketing", "seo", "cro"]
tools: ["claude", "cursor", "gemini"]
---

# 落地页生成器

根据产品描述生成高转化率落地页。输出完整的 Next.js/React 组件，包含多种区块变体、经过验证的文案框架、SEO 优化和性能优先模式。不是 lorem ipsum 占位符——而是真正能转化的文案。

**目标：** LCP < 1s · CLS < 0.1 · FID < 100ms
**输出：** TSX 组件 + Tailwind 样式 + SEO 元数据 + 文案变体

## 适用场景
- 你需要在 Next.js 或 React 中生成营销落地页。
- 任务涉及以转化为导向的页面结构、区块变体、Tailwind 样式，或 SEO 友好的文案。
- 你希望从产品描述直接产出完整落地页，而不是零散的 UI 片段。

## 核心能力

- 5 种首屏区块变体（居中、左右分栏、渐变背景、视频背景、极简）
- 功能展示区（网格布局、交替排列、带图标卡片）
- 定价表（2–4 档位，含功能列表和切换开关）
- 带 Schema 标记的 FAQ 手风琴
- 客户证言（网格、轮播、单条引用）
- CTA 区块（横幅、全页、行内）
- 页脚（简单、大型导航、极简）
- 4 套设计风格及对应 Tailwind 类名集合

---

## 生成流程

每个落地页请求都按以下顺序执行：

1. **收集输入** — 按下方触发格式收集产品名称、标语、受众、痛点、核心收益、定价档位、设计风格和文案框架。仅询问缺失字段。
2. **分析品牌调性**（推荐）— 如果用户已有品牌内容（网站文案、博客文章、营销物料），将其传入 `marketing-skill/content-production/scripts/brand_voice_analyzer.py` 获取调性画像（正式度、语气、视角）。用画像指导设计风格和文案框架选择：
   - 正式 + 专业 → **enterprise** 风格，**AIDA** 框架
   - 轻松 + 友好 → **bold-startup** 风格，**BAB** 框架
   - 专业 + 权威 → **dark-saas** 风格，**PAS** 框架
   - 轻松 + 对话式 → **clean-minimal** 风格，**BAB** 框架
3. **选择设计风格** — 将用户选择（或从品牌调性分析推断）映射到设计风格参考中的四套 Tailwind 类名之一。
4. **应用文案框架** — 生成组件前，先用选定框架（PAS / AIDA / BAB）撰写所有标题和正文。全文保持与调性画像一致的正式度和语气。
5. **按顺序生成区块** — 首屏 → 功能 → 定价 → FAQ → 证言 → CTA → 页脚。跳过与产品无关的区块。
6. **对照 SEO 清单验证** — 输出最终代码前逐项检查 SEO 清单，内联修复所有遗漏。
7. **输出最终组件** — 交付完整的、可直接粘贴使用的 TSX 文件，包含所有 Tailwind 类名、SEO 元数据和结构化数据。

---

## 触发格式

```
Product: [名称]
Tagline: [一句话价值主张]
Target audience: [目标用户]
Key pain point: [解决什么问题]
Key benefit: [核心收益]
Pricing tiers: [free/pro/enterprise 或自定义描述]
Design style: dark-saas | clean-minimal | bold-startup | enterprise
Copy framework: PAS | AIDA | BAB
```

---

## 设计风格参考

| 风格 | 背景 | 强调色 | 卡片 | CTA 按钮 |
|---|---|---|---|---|
| **Dark SaaS** | `bg-gray-950 text-white` | `violet-500/400` | `bg-gray-900 border border-gray-800` | `bg-violet-600 hover:bg-violet-500` |
| **Clean Minimal** | `bg-white text-gray-900` | `blue-600` | `bg-gray-50 border border-gray-200 rounded-2xl` | `bg-blue-600 hover:bg-blue-700` |
| **Bold Startup** | `bg-white text-gray-900` | `orange-500` | `shadow-xl rounded-3xl` | `bg-orange-500 hover:bg-orange-600 text-white` |
| **Enterprise** | `bg-slate-50 text-slate-900` | `slate-700` | `bg-white border border-slate-200 shadow-sm` | `bg-slate-900 hover:bg-slate-800 text-white` |

> **Bold Startup** 标题：给所有 `<h1>`/`<h2>` 元素添加 `font-black tracking-tight`。

---

## 文案框架

**PAS（Problem 问题 → Agitate 煽动 → Solution 方案）**
- H1：他们当前所处的痛苦状态
- 副标题：不解决会怎样
- CTA：你提供什么
- *示例 — H1：* "你的团队每天花 3 小时做手工报表" / *副标题：* "花在电子表格上的每一小时，都是没在成交的一小时。你的竞争对手已经自动化了。" / *CTA：* "10 分钟自动完成报表 →"

**AIDA（Attention 注意 → Interest 兴趣 → Desire 渴望 → Action 行动）**
- H1：大胆抓眼球的陈述 → 副标题：有趣的事实或收益 → 功能：建立渴望的证据点 → CTA：明确行动

**BAB（Before 之前 → After 之后 → Bridge 桥梁）**
- H1："[之前的状态] → [之后的状态]" → 副标题："[产品] 如何填补差距" → 功能：运作原理（桥梁）

---

## 代表组件：首屏（居中渐变 — Dark SaaS）

以此作为所有首屏变体的结构模板。替换布局类名、渐变方向和图片位置即可得到分栏、视频背景和极简版本。

```tsx
export function HeroCentered() {
  return (
    <section className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden bg-gray-950 px-4 text-center">
      <div className="absolute inset-0 bg-gradient-to-b from-violet-900/20 to-transparent" />
      <div className="pointer-events-none absolute -top-40 left-1/2 h-[600px] w-[600px] -translate-x-1/2 rounded-full bg-violet-600/20 blur-3xl" />
      <div className="relative z-10 max-w-4xl">
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-violet-500/30 bg-violet-500/10 px-4 py-1.5 text-sm text-violet-300">
          <span className="h-1.5 w-1.5 rounded-full bg-violet-400" />
          Now in public beta
        </div>
        <h1 className="mb-6 text-5xl font-bold tracking-tight text-white md:text-7xl">
          Ship faster.<br />
          <span className="bg-gradient-to-r from-violet-400 to-pink-400 bg-clip-text text-transparent">
            Break less.
          </span>
        </h1>
        <p className="mx-auto mb-10 max-w-2xl text-xl text-gray-400">
          The deployment platform that catches errors before your users do.
          Zero config. Instant rollbacks. Real-time monitoring.
        </p>
        <div className="flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Button size="lg" className="bg-violet-600 text-white hover:bg-violet-500 px-8">
            Start free trial
          </Button>
          <Button size="lg" variant="outline" className="border-gray-700 text-gray-300">
            See how it works →
          </Button>
        </div>
        <p className="mt-4 text-sm text-gray-500">No credit card required · 14-day free trial</p>
      </div>
    </section>
  )
}
```

---

## 其他区块模式

### 功能展示区（交替排列）

遍历 `features` 数组（每项 `{ title, description, image, badge }`）。用 `i % 2 === 1 ? "lg:flex-row-reverse" : ""` 切换排列方向。`<Image>` 设置明确的 `width`/`height` 和 `rounded-2xl shadow-xl`。外层 `<section className="py-24">` + `max-w-6xl` 容器。

### 定价表

遍历 `plans` 数组（每项 `{ name, price, description, features[], cta, highlighted }`）。高亮方案使用 `border-2 border-violet-500 bg-violet-950/50 ring-4 ring-violet-500/20`；其余使用 `border border-gray-800 bg-gray-900`。`null` 价格渲染为 "Custom"。每行功能前加 `<Check>` 图标。布局：`grid gap-8 lg:grid-cols-3`。

### 带 Schema 标记的 FAQ

在区块内通过 `<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />` 注入 `FAQPage` JSON-LD。将 `{ q, a }` 格式的 FAQ 映射到 shadcn `<Accordion>`（`type="single" collapsible`）。容器：`max-w-3xl`。

### 证言、CTA、页脚

- **证言：** 网格布局（`grid-cols-1 md:grid-cols-3`）或单条引用大图块，含头像、姓名、职位和引用文字。
- **CTA 横幅：** 全宽区块，包含标题、副标题和两个按钮（主按钮 + 幽灵按钮）。紧接其下放置信任信号（退款保障、Logo 条）。
- **页脚：** Logo + 导航栏目 + 社交链接 + 法律信息。分隔线使用 `border-t border-gray-800`。

---

## SEO 清单

- [ ] `<title>` 标签：主关键词 + 品牌名（50–60 字符）
- [ ] Meta description：收益 + CTA（150–160 字符）
- [ ] OG 图片：1200×630px，包含产品名称和标语
- [ ] H1：每页一个，包含主关键词
- [ ] 结构化数据：FAQPage、Product 或 Organization schema
- [ ] Canonical URL 已设置
- [ ] 所有 `<Image>` 组件的图片 alt 文本
- [ ] robots.txt 和 sitemap.xml 已配置
- [ ] Core Web Vitals：LCP < 1s，CLS < 0.1
- [ ] 移动端 viewport meta 标签存在
- [ ] 内链指向定价和文档页面

> **验证步骤：** 输出最终代码前，确认上述每项均已满足。内联修复所有遗漏——不得跳过任何项目。

---

## 性能指标

| 指标 | 目标 | 技术手段 |
|---|---|---|
| LCP | < 1s | 预加载首屏图片，Next/Image 使用 `priority` |
| CLS | < 0.1 | 所有图片设置明确 width/height |
| FID/INP | < 100ms | 延迟非关键 JS，使用 `loading="lazy"` |
| TTFB | < 200ms | 落地页使用 ISR 或静态生成 |
| 包体积 | < 100KB JS | 用 `@next/bundle-analyzer` 审计 |

---

## 常见陷阱

- 首屏图片未预加载 —— 给第一个 `<Image>` 加上 `priority` 属性
- 缺少移动端断点 —— 始终用 `sm:` 前缀做移动端优先设计
- CTA 文案太模糊 —— "Get started" 优于 "Learn more"；"Start free trial" 优于 "Sign up"
- 定价页缺少信任信号 —— 在 CTA 附近加上退款保障和客户证言
- 移动端首屏没有 CTA —— 确保 375px 视口下无需滚动就能看到按钮

---

## 相关技能

- **Brand Voice Analyzer**（`marketing-skill/content-production/scripts/brand_voice_analyzer.py`）—— 生成前运行，建立调性画像并确保文案一致性
- **UI Design System**（`product-team/ui-design-system/`）—— 构建页面之前从品牌色生成设计令牌
- **Competitive Teardown**（`product-team/competitive-teardown/`）—— 竞品定位为落地页信息传递和差异化提供依据

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出替代针对具体环境的验证、测试或专家评审。
- 如缺少必要输入、权限、安全边界或成功标准，应暂停并请求澄清。
