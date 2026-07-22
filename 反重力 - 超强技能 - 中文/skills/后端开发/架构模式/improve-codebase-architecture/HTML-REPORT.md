# HTML 报告格式

架构审查渲染为操作系统临时目录中的单个自包含 HTML 文件。Tailwind 和 Mermaid 均来自 CDN。Mermaid 可靠地处理图形结构图表；手绘 div 和内联 SVG 处理更偏向编辑风格的视觉内容（体量图、剖面图）。混合两者——不要什么都靠 Mermaid，否则会变得千篇一律。

## 脚手架

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Architecture review — {{repo name}}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="module">
      import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
      mermaid.initialize({ startOnLoad: true, theme: "neutral", securityLevel: "loose" });
    </script>
    <style>
      /* small custom layer for things Tailwind doesn't cover cleanly:
         dashed seam lines, hand-drawn-feeling arrow heads, etc. */
      .seam { stroke-dasharray: 4 4; }
      .leak { stroke: #dc2626; }
      .deep { background: linear-gradient(135deg, #0f172a, #1e293b); }
    </style>
  </head>
  <body class="bg-stone-50 text-slate-900 font-sans">
    <main class="max-w-5xl mx-auto px-6 py-12 space-y-12">
      <header>...</header>
      <section id="candidates" class="space-y-10">...</section>
      <section id="top-recommendation">...</section>
    </main>
  </body>
</html>
```

## 页眉

仓库名称、日期和一个紧凑的图例：实线框 = module，虚线 = seam，红色箭头 = leakage，深色粗框 = deep module。不要引导段落——直接进入候选项。

## 候选卡片

图表承担主要表达。文字稀少、朴素，直接使用术语表词汇（来自 `/codebase-design` 技能），不加修饰。

每个候选项是一个 `<article>`：

- **Title**——简短，命名深化内容（如 "Collapse the Order intake pipeline"）。
- **Badge row**——推荐强度（`Strong` = 翡翠绿，`Worth exploring` = 琥珀色，`Speculative` = 石板灰），加上依赖类别标签（`in-process`、`local-substitutable`、`ports & adapters`、`mock`）。
- **Files**——等宽字体列表，`font-mono text-sm`。
- **Before / After diagram**——核心亮点。两列并排。见下方模式。
- **Problem**——一句话。什么在痛。
- **Solution**——一句话。改变什么。
- **Wins**——要点，每条 ≤6 个词。如 "Tests hit one interface"、"Pricing logic stops leaking"、"Delete 4 shallow wrappers"。
- **ADR 标注**（如适用）——琥珀色底框中的一行文字。

不要用段落来解释。如果图表需要一段话才能理解，重绘图表。

## 图表模式

选择适合候选项的模式。混合使用。不要让每张图表看起来一样——多样性本身就是目的的一部分。

### Mermaid 图（依赖/调用流的主力）

当要点是"X 调用 Y 调用 Z，看看这团乱"时，使用 Mermaid `flowchart` 或 `graph`。用 Tailwind 样式的卡片包裹，这样不会显得突兀。用 classDef 给泄漏边染红色，给深模块染深色。序列图适合"之前：6 次往返；之后：1 次"。

```html
<div class="rounded-lg border border-slate-200 bg-white p-4">
  <pre class="mermaid">
    flowchart LR
      A[OrderHandler] --> B[OrderValidator]
      B --> C[OrderRepo]
      C -.leak.-> D[PricingClient]
      classDef leak stroke:#dc2626,stroke-width:2px;
      class C,D leak
  </pre>
</div>
```

### 手绘方框与箭头（当 Mermaid 的布局跟你对着干时）

模块用带边框和标签的 `<div>`。箭头用绝对定位在相对容器上的内联 SVG `<line>` 或 `<path>` 元素。当你想让"之后"图看起来像一个粗边框深模块、内部灰化时使用——Mermaid 渲染不出那种视觉重量。

### 剖面图（适合分层浅薄）

堆叠水平条带（`h-12 border-l-4`）来展示一次调用穿过的层级。之前：6 个薄层每个什么都没做。之后：1 个厚条带标注合并后的职责。

### 体量图（适合"接口和实现一样宽"）

每个模块两个矩形——一个代表接口表面积，一个代表实现。之前：接口矩形几乎和实现矩形一样高（浅）。之后：接口矩形矮，实现矩形高（深）。

### 调用图折叠

之前：渲染为嵌套方框的函数调用树。之后：同一棵树折叠进一个方框，现在内部的调用以淡化方式显示在其中。

## 样式指南

- 偏编辑风格，而非企业仪表盘风格。大量留白。标题可选衬线体（`font-serif` 与 stone/slate 搭配效果好）。
- 节制用色：一个强调色（翡翠绿或靛蓝）加上红色用于泄漏、琥珀色用于警告。
- 图表高度保持约 320px，这样前后对比可以舒适地并排显示而无需滚动。
- 图表内模块标签使用 `text-xs uppercase tracking-wider`——应该读起来像示意图，而不是 UI。
- 唯一的脚本是 Tailwind CDN 和 Mermaid ESM 导入。报告其余部分是静态的——没有应用代码，没有 Mermaid 自身渲染之外的交互性。

## 首推建议部分

一张更大的卡片。候选项名称，一句原因，锚链接到其卡片。仅此而已。

## 语调

自然语言，简洁——但架构名词和动词直接来自 `/codebase-design` 技能。简洁不是偏移术语的借口。

**严格使用：** module、interface、implementation、depth、deep、shallow、seam、adapter、leverage、locality。

**禁止替换为：** component、service、unit（代替 module）· API、signature（代替 interface）· boundary（代替 seam）· layer、wrapper（代替 module，当你指的是 module 时）。

**符合风格的措辞：**

- "Order intake module is shallow — interface nearly matches the implementation."
- "Pricing leaks across the seam."
- "Deepen: one interface, one place to test."
- "Two adapters justify the seam: HTTP in prod, in-memory in tests."

**Wins 要点** 用术语表词汇命名收益：*"locality: bugs concentrate in one module"*、*"leverage: one interface, N call sites"*、*"interface shrinks; implementation absorbs the wrappers"*。不要写 *"easier to maintain"* 或 *"cleaner code"*——这些术语不在术语表中，不配占位。

不兜圈子，不铺陈废话，不说"it's worth noting that…"。如果一个句子能变成要点，就变成要点。如果一个要点能删掉，就删掉。如果一个术语不在 `/codebase-design` 术语表中，在创造新术语之前先用术语表中已有的。
