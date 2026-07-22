---
name: deterministic-design
description: "渲染 UI 并证明它既平衡又好用：基于确定性的布局审计（通过显式数学 + 标注截图计算重心 / 视觉中心 / 像素平衡），外加一位独立的全新视角评审员按 Nielsen 可用性启发法进行视觉评判。专为那些只靠审美而缺乏度量层的设计技能补齐短板。"
risk: safe
source: community
source_type: community
source_repo: connerkward/deterministic-design-skill
date_added: "2026-06-16"
author: Conner K Ward
license: MIT
tags:
  - design
  - layout
  - usability
  - audit
  - verification
  - vision
tools:
  - claude-code
  - antigravity
  - cursor
  - gemini-cli
  - codex-cli
---
## 适用场景

用于揪出 AI 生成的 UI 那些"看起来不对劲"、错位或居中发糊的问题，以及可用性缺陷——当你需要**证明**布局既平衡又好用，而不是只相信模型的"眼力"时使用。在汇报设计"完成"之前，与任何只重审美/输出的设计技能配合使用。

_来源：[connerkward/deterministic-design-skill](https://github.com/connerkward/deterministic-design-skill)（MIT 协议）。_

# 确定性设计

核心论点：**确定性胜过 AI 的随机性。** 模型不能相信自己在布局上的眼力——所以别信。正确做法是：把 UI 渲染出来，然后**测量它**。

包含两个子技能（按需加载）：
- **[design-spatial](https://github.com/connerkward/deterministic-design-skill/blob/main/design-spatial/SKILL.md)** — 确定性布局审计：显式栅格 + 8pt 间距节奏，由 `layout-audit.js` 计算重心 / 视觉中心 / 像素平衡，并绘制标注截图。**用数字说话，不用感觉。** 再加上一轮"先渲染再点评"的视觉循环。
- **[design-ux](https://github.com/connerkward/deterministic-design-skill/blob/main/design-ux/SKILL.md)** — 可用性审计：由一位**独立**的全新视角评审员，按 Nielsen 十大启发法及交互启发法对渲染好的 UI 打分，输出按优先级排序的修复清单。

本技能**补强**了现有的设计技能（包括 Anthropic 自带的那一套），补的就是它们缺失的那一层——它不只给审美建议，而是去渲染、测量、并对结果打分。可与任意设计技能组合使用。

在 ckw-design 中，它以子目录形式存在；同时通过 publish-skill **单独发布**为 `deterministic-design-skill`（独立发行包）。这是两条旗舰叙事之一——*确定性*那条；它的兄弟篇是人机协同（lookdev）。

## 局限性

- 布局度量与视觉评判审计能捕获大量空间与可用性缺陷，但仍不能替代产品判断或用户测试。
- 工作流需要有渲染好的 UI 或截图，无法验证那些还没建成或没截到的组件。
- 自动打分可能漏掉品牌细节、文案语气、无障碍需求以及领域专属的用户预期。
