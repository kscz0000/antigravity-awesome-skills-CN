---
name: unship
description: "在真实应用中本地对比 AI 智能体生成的 UI 方案，挑选保留版本并清理未中选的临时代码。"
category: development
risk: critical
source: community
source_repo: mbenhard/unship
source_type: community
date_added: "2026-06-07"
author: Marcus Benhard
tags: [ui-variants, frontend, local-first, coding-agents]
tools: [claude-code, antigravity, cursor, gemini-cli, codex-cli, opencode]
license: "MIT"
license_source: "https://github.com/mbenhard/unship/blob/main/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# Unship

## 概述

Unship 是一个本地工作流，用于在真实应用中对比 AI 生成的 UI 方案，而不是一次只接受一个生成版本。它会在源码层面添加临时变体，弹出本地浏览器选择器，待用户选定后清理未中选的选项。

本技能用于编码智能体做前端迭代。它不是生产级 A/B 测试、分析平台、特性开关，也不是托管的实验服务。

## 适用场景

- 用户希望对比多种 UI、布局、文案、状态、流程或设计系统方案时使用。
- 编码智能体应在真实源码中创建若干临时选项，让用户在本地运行的应用里做判断时使用。
- 用户选定了可见方案，希望在发布前移除落选的临时代码时使用。

## 不适用场景

- 用户需要生产级实验、流量分流、分析或特性开关时不要使用。
- 由于重复的活跃 ID、全局脚本、分析触发器、焦点陷阱、破坏性操作或自动播放副作用，应用无法安全渲染未激活的隐藏变体时不要使用。
- 用户未授权本地源码修改时不要使用。

## 工作原理

### 1. 安装或复用 Unship

优先使用项目本地的二进制（如果存在）：

```bash
./node_modules/.bin/unship doctor --json --no-update-check
```

否则将经过审核的、确定版本的 CLI 安装到项目中，然后运行本地二进制：

```bash
npm install --save-dev @unship/cli@<reviewed-version>
./node_modules/.bin/unship doctor --json --no-update-check
```

如果本地选择器需要额外设置，运行：

```bash
./node_modules/.bin/unship setup --json
```

只改动最小化的、仅限开发环境的挂载点，使选择器能够在本地预览中加载。

### 2. 创建临时变体

审视相关页面、组件、路由或渲染产物。添加最小化的源码级对比，让用户能够在真实场景下做判断。

使用 Unship 标记：

```html
<section data-unship-pick="Hero">
  <div data-unship-option="Current">...</div>
  <div data-unship-option="Proof-led" hidden>...</div>
  <div data-unship-option="Visual" hidden>...</div>
</section>
```

选项标签保持简短且可见。除非用户指定数量，否则建议 2-4 个有意义的备选。

### 3. 验证对比就绪状态

交付给用户之前，检查以下条件：

- 预期的 `data-unship-pick` 分组存在；
- 预期的选项标签存在；
- 选项是分组的直接子元素；
- 初始状态下恰好一个选项可见；
- 隐藏的未激活选项保持隐藏。

### 4. 让用户做选择

向用户告知分组标签、选项标签、设置状态以及检测到的本地预览服务提示。用户通过在聊天中点名某个可见选项标签来选择。

### 5. 选择后清理

当用户选定胜出方案后，保留该选项的真实源码，移除该分组中其他落选的选项。从已定稿的源码中移除临时的 `data-unship-*` 属性。

发布前的最终清理，移除所有 Unship 残留并运行：

```bash
./node_modules/.bin/unship check --json
```

在 check 报告清白之前，不得声称清理完成。

## 最佳实践

- Unship 的工作保持本地化和临时性。
- 除非用户明确要求改变方向，否则保留应用现有的设计语言。
- 在变体为临时状态期间，避免做无关的重构。
- 不要把自定义标签页、应用偏好或永久切换器塞进产品 UI 来做 Unship 对比。
- 保持未激活选项的安全：避免重复的活跃 ID、提交控件、全局脚本、分析触发器、焦点陷阱、破坏性副作用以及有状态的 Provider。

## 局限性

- Unship 不决定哪个变体获胜，由人来做选择。
- Unship 不能替代设计评审、浏览器 QA、无障碍检查或生产发布验证。
- Unship 不用于生产流量、远程分析或持久化的产品实验。

## 安全注意事项

- 仅在用户已授权你修改的本地项目中执行命令。
- 在自动化智能体工作流中，不要运行 `npx @unship/cli@latest` 或任何未固定版本的远程 CLI。先固定并审核包版本，再执行项目本地的二进制。
- 把生成的变体视为发布前必须清理的临时代码。
- 进行破坏性清理之前，当用户的选择存在歧义时，要再次确认所选选项标签。
- 如果在 Unship 编辑之前基线构建或类型检查就已经失败，请报告该基线状态，并将变体工作隔离开。

## 常见陷阱

- **问题：** 隐藏变体通过 CSS 覆盖了 `hidden` 属性。
  **解决：** 在必要时保留 `[hidden] { display: none !important; }`，紧邻变体相关 CSS。

- **问题：** 经过多轮修改后，用户说"保留第二个"。
  **解决：** 在编辑源码前确认准确的分组和选项标签。

- **问题：** 对比工作蔓延成了大范围的重设计。
  **解决：** 缩小范围到能在运行应用中评判的最小段落、状态或流程。

## 相关技能

- `@webapp-testing` - 前端变更后用于基于浏览器的功能检查。
- `@mobile-design` - 对比移动端特定的 UI 模式和平台约束时使用。