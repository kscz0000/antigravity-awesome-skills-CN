---
name: mdpr-skill
description: "审查 MDPR Markdown 演示文稿工作流，提供语义提示、视觉检查与确定性渲染器边界约束。"
category: productivity
risk: safe
source: community
source_repo: ch040602/mdpr-skill
source_type: community
date_added: "2026-07-01"
author: ch040602
tags: [mdpr, presentations, markdown, powerpoint, codex, visual-review, agent-hints]
tools: [claude, cursor, gemini, codex, antigravity]
license: "MIT"
license_source: "https://github.com/ch040602/mdpr-skill/blob/main/LICENSE"
---

# mdpr-skill

## 概述

将此技能作为 [MDPR](https://github.com/ch040602/MdPr) 的可选智能体伴侣使用。MDPR 是一个确定性的 Markdown 转演示文稿运行时，负责解析、布局、主题、验证以及最终的 PPTX/HTML/PDF 渲染。本技能帮助智能体审查 MDPR 工作流、提出弱语义提示、解释视觉发现，但不控制幻灯片几何。

上游技能源为 [`ch040602/mdpr-skill`](https://github.com/ch040602/mdpr-skill)，包含模式定义、审查命令、兼容性产物、视觉证据示例和 MDPR 边界文档。

## 何时使用此技能

- 当用户询问 MDPR、`mdpresent`、Markdown 转 PPTX 或 Markdown 演示文稿审查时使用。
- 当生成的 MDPR 产物需要语义、叙事、无障碍或视觉审查意见时使用。
- 当用户需要 Codex 风格的演示文稿工作流提示，同时保持 MDPR 作为确定性渲染器时使用。
- 当需要将 MDPR 输出与仅生成图片的幻灯片生成器（如 codex-ppt 风格工作流）进行比较时使用。
- 当可复用的主题或样式包提案应以需审批的 MDPR 候选形式表达，而非直接编辑最终幻灯片时使用。

## 核心边界

- 让 MDPR 负责解析、幻灯片拆分、配方、布局、坐标、几何、排版、颜色、z 序、箭头、效果、精确图标资源、渲染器对象 ID 和最终 PPTX 对象。
- 保持智能体输出为语义化、基于证据且模式合法的。
- 以 Markdown 清理、MDPR 规则手册变更、配置变更、确定性策略变更或需审批的提案形式表达修复。
- 保留在禁用所有智能体提示的情况下仍能构建同一套幻灯片的能力。
- 除非用户明确要求提供清理后的源稿，否则不得修改源 Markdown。

## 工作原理

### 步骤 1：识别 MDPR 表面

在给出建议前先对用户请求分类：

- `semantic hints`（语义提示）：精简的意图、分组、重要性和图标关键词建议。
- `review report`（审查报告）：基于渲染证据、清单或验证报告的视觉或叙事问题。
- `layout intent`（布局意图）：来自摘要模板目录的高层布局目标，绝非具体的占位符坐标。
- `theme candidate`（主题候选）：供后续 MDPR 审批/导入门控的可复用令牌与样式包提案。
- `codex-ppt compatibility`（codex-ppt 兼容性）：仅提供功能映射与比较说明；不要将 MDPR 变成全幻灯片图片渲染器。

### 步骤 2：为每个发现提供依据

引用可用证据，例如：

- 源 Markdown 路径或标题文本
- MDPR 清单摘要
- 渲染预览图片路径
- 验证报告 ID
- 来源说明或引用元数据
- 模式名称，如 `agent-hint.json`、`review-report.json` 或 `mdpr-theme-candidate-v1`

如果缺少证据，说明需要什么产物，而非捏造通过/失败结果。

### 步骤 3：保持提示弱化

允许的提示：

- 幻灯片或章节意图
- 内容分组
- 相对重要性
- 图标搜索关键词
- 无障碍或引用审查意见
- 当图标过小或语义过于模糊时，生成图片候选简述

禁止的提示：

- 最终坐标、尺寸、z 序、几何或对象 ID
- 精确颜色、排版、箭头、效果或图标资源选择
- 最终布局 ID 或占位符 ID
- 未经 MDPR 验证支持的通过/失败决策

### 步骤 4：将修复路由至 MDPR 管控的变更

当相同问题反复出现时，推荐确定性的后续处理面：

- Markdown 清理
- MDPR 规则手册变更
- MDPR 配置/档案变更
- MDPR 主题包注册
- MDPR 验证改进
- 需审批的套牌局部覆盖或样式包候选

## 实用本地命令

仅当上游 `mdpr-skill` CLI 在当前工作区可用且引用的输入文件存在时运行这些命令。

```bash
node bin/mdpr-skill.js hint --source-sha256 <64hex> --out .mdpresent/proposals/agent-hint.json
node bin/mdpr-skill.js review --manifest dist/mdpresent-manifest.json --out .mdpresent/review/review-report.json
node bin/mdpr-skill.js narrative --markdown deck.md --manifest dist/mdpresent-manifest.json --out .mdpresent/review/narrative-review.json
node bin/mdpr-skill.js layout-intent --layout-catalog template-layout-catalog.json --out .mdpresent/review/layout-intent.json
node bin/mdpr-skill.js accessibility --markdown deck.md --audience "executive review" --out .mdpresent/review/accessibility-review.json
```

## 示例

### 审查已渲染的 MDPR 幻灯片组

1. 阅读源 Markdown、清单摘要、渲染图片列表和任何验证报告。
2. 区分源内容问题与渲染器/规则手册问题。
3. 仅报告有证据支撑的视觉问题。
4. 当相同问题反复出现时，推荐确定性的 MDPR 修复。

```markdown
Finding: Slide 4 has weak visual hierarchy between the metric and explanation.
Evidence: rendered/slide-04.png, manifest slide id `s4`, heading "Revenue Mix".
MDPR-owned fix: adjust the metric-card recipe spacing rule or choose a
deterministic layout profile with stronger numeric emphasis.
```

### 提出主题候选

1. 将源设计视为视觉系统，而非要复制的内容。
2. 提取可复用令牌、语义布局蓝图、装饰语法和最佳适配场景。
3. 输出需审批的 `mdpr-theme-candidate-v1`。
4. 保持 `mdprOwnsFinalLayout`、`mdprOwnsFinalThemeBinding` 和 `noRawUseInAgentHints` 为 true。

```json
{
  "schema": "mdpr-theme-candidate-v1",
  "source": "rendered reference set approved by user",
  "useCases": ["executive review", "research update"],
  "constraints": {
    "mdprOwnsFinalLayout": true,
    "mdprOwnsFinalThemeBinding": true,
    "noRawUseInAgentHints": true
  }
}
```

### 与 codex-ppt 风格工作流比较

仅将 codex-ppt 作为能力参考或仅图片基线使用。保持输出模型的区别：codex-ppt 风格工作流可能生成全幻灯片图片，而 MDPR 默认生成可编辑的 PPTX/HTML/PDF 并带有确定性验证。

```markdown
Comparison note: codex-ppt style output may optimize for a single rasterized
slide image. MDPR should instead preserve editable slide objects and route
visual improvements through recipes, themes, and validation policies.
```

## 最佳实践

- 推荐：优先使用简洁的语义提示，而非复述源内容。
- 推荐：保持审查意见对 MDPR 维护者可操作。
- 推荐：在做质量声明前先指出缺失的证据。
- 推荐：将 LLM 判断仅视为分诊；MDPR 验证仍是发布门控。
- 避免：将生成的资源提示当作最终资源选择。
- 避免：仅凭智能体判断推荐原始颜色、坐标或渲染器对象 ID。

## 局限性

- 本技能不替代 MDPR 运行时验证。
- 本技能不生成最终幻灯片坐标或最终 PPTX 对象。
- 本技能不使 MDPR 依赖 LLM。
- 本技能不应用于复制私有幻灯片设计或专有幻灯片内容。

## 常见陷阱

- **问题：** 将 mdpr-skill 输出当作最终幻灯片布局。
  **解决：** 保持提示语义化，让 MDPR 选择最终布局、几何和渲染器对象。

- **问题：** 报告视觉问题时没有证据。
  **解决：** 将每个发现关联到源 Markdown、清单条目、渲染预览、验证报告或其他具体产物。

- **问题：** 将 codex-ppt 仅图片行为复制到 MDPR 中。
  **解决：** 将仅图片生成器作为比较基线，同时保持 MDPR 可编辑的 PPTX/HTML/PDF 输出模型。

## 安全与注意事项

- 仅审查用户已提供或授权的文件。
- 未经明确许可，不获取私有引用、凭据或付费资源。
- 不在生成的审查报告或主题候选中包含密钥、API 密钥或私有源内容。
- 将所有 CLI 命令视为本地工作区命令；运行前确认输入路径存在。

## 相关技能

- `@frontend-slides` - 用于浏览器原生 HTML 演示文稿生成。
- `@2slides-ppt-generator` - 用于基于托管 API 的演示文稿生成。
- `@office-productivity` - 用于更广泛的文档、电子表格和幻灯片工作流协调。
