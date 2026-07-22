---
name: wiki-vitepress
description: "将生成的 wiki Markdown 文件转换为带有暗色主题和交互式 Mermaid 图表的精致 VitePress 静态站点。当用户要求"构建站点"或"打包为 VitePress"、用户运行 /deep-wiki，或希望从已生成的 wiki 页面获得可浏览的 HTML 输出时使用。触发词：VitePress、wiki 站点打包、构建静态站点、暗色主题 Mermaid、可浏览 HTML。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Wiki VitePress 打包器

将生成的 wiki Markdown 文件转换为带有暗色主题和交互式 Mermaid 图表的精致 VitePress 静态站点。

## 使用场景
- 用户要求"构建站点"或"打包为 VitePress"
- 用户运行 `/deep-wiki:build` 命令
- 用户希望从已生成的 wiki 页面获得可浏览的 HTML 输出

## VitePress 脚手架

在 `wiki-site/` 目录下生成以下结构：

```
wiki-site/
├── .vitepress/
│   ├── config.mts
│   └── theme/
│       ├── index.ts
│       └── custom.css
├── public/
├── [generated .md pages]
├── package.json
└── index.md
```

## 配置要求（`config.mts`）

- 使用 `vitepress-plugin-mermaid` 中的 `withMermaid` 包装器
- 设置 `appearance: 'dark'` 以启用仅暗色主题
- 根据目录结构配置 `themeConfig.nav` 和 `themeConfig.sidebar`
- Mermaid 配置必须设置暗色主题变量：

```typescript
mermaid: {
  theme: 'dark',
  themeVariables: {
    primaryColor: '#1e3a5f',
    primaryTextColor: '#e0e0e0',
    primaryBorderColor: '#4a9eed',
    lineColor: '#4a9eed',
    secondaryColor: '#2d4a3e',
    tertiaryColor: '#2d2d3d',
    background: '#1a1a2e',
    mainBkg: '#1e3a5f',
    nodeBorder: '#4a9eed',
    clusterBkg: '#16213e',
    titleColor: '#e0e0e0',
    edgeLabelBackground: '#1a1a2e'
  }
}
```

## 暗色模式 Mermaid：三层修复

### 第一层：主题变量（位于 config.mts）
如上所示，通过 `mermaid.themeVariables` 设置。

### 第二层：CSS 覆盖（`custom.css`）
使用 `!important` 精准定位 Mermaid SVG 元素：

```css
.mermaid .node rect,
.mermaid .node circle,
.mermaid .node polygon { fill: #1e3a5f !important; stroke: #4a9eed !important; }
.mermaid .edgeLabel { background-color: #1a1a2e !important; color: #e0e0e0 !important; }
.mermaid text { fill: #e0e0e0 !important; }
.mermaid .label { color: #e0e0e0 !important; }
```

### 第三层：内联样式替换（`theme/index.ts`）
Mermaid 的内联 `style` 属性会覆盖其他所有设置。请使用 `onMounted` 加轮询来替换它们：

```typescript
import { onMounted } from 'vue'

// In setup()
onMounted(() => {
  let attempts = 0
  const fix = setInterval(() => {
    document.querySelectorAll('.mermaid svg [style]').forEach(el => {
      const s = (el as HTMLElement).style
      if (s.fill && !s.fill.includes('#1e3a5f')) s.fill = '#1e3a5f'
      if (s.stroke && !s.stroke.includes('#4a9eed')) s.stroke = '#4a9eed'
      if (s.color) s.color = '#e0e0e0'
    })
    if (++attempts >= 20) clearInterval(fix)
  }, 500)
})
```

请使用 `setup()` 配合 `onMounted`，**不要**使用 `enhanceApp()` —— DOM 在 SSR 阶段尚不存在。

## Mermaid 图表的点击缩放

将每个 `.mermaid` 容器包裹在可点击的包装器中，点击时打开全屏模态框：

```typescript
document.querySelectorAll('.mermaid').forEach(el => {
  el.style.cursor = 'zoom-in'
  el.addEventListener('click', () => {
    const modal = document.createElement('div')
    modal.className = 'mermaid-zoom-modal'
    modal.innerHTML = el.outerHTML
    modal.addEventListener('click', () => modal.remove())
    document.body.appendChild(modal)
  })
})
```

模态框 CSS：
```css
.mermaid-zoom-modal {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.9);
  display: flex; align-items: center; justify-content: center;
  z-index: 9999; cursor: zoom-out;
}
.mermaid-zoom-modal .mermaid { transform: scale(1.5); }
```

## 后处理规则

在 VitePress 构建之前，扫描所有 `.md` 文件并修复：
- 将 `<br/>` 替换为 `<br>`（Vue 模板编译器兼容性）
- 在代码块之外，将裸的 `<T>` 泛型参数用反引号包裹
- 确保每个页面都包含带有 `title` 和 `description` 的 YAML frontmatter

## 构建

```bash
cd wiki-site && npm install && npm run docs:build
```

输出至 `wiki-site/.vitepress/dist/`。

## 已知陷阱

- Mermaid 异步渲染 —— 当 `onMounted` 触发时 SVG 还不存在。必须轮询。
- 针对裸 `<T>` 的 `isCustomElement` 编译器选项会导致更严重的崩溃 —— 请**不要**使用它
- Mermaid 中的节点文本使用具有最高优先级的内联 `style` —— 单纯 CSS 无法修复
- `enhanceApp()` 在 SSR 阶段运行，而此时 `document` 不存在 —— 请仅使用 `setup()`

## 使用场景
本技能适用于执行上述概览中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 若缺少必需的输入、权限、安全边界或成功标准，请停下来询问以澄清。
