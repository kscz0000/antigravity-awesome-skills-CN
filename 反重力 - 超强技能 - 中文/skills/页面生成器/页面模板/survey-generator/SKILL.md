---
name: survey-generator
description: "生成有来源支撑的 AI/ML 综述论文制品，含精选参考文献和 Fireworks/Kimi HTML 渲染。"
allowed-tools: Read, Write, Bash, WebFetch, AskUserQuestion
category: "research"
risk: "safe"
source: "official"
source_repo: "dair-ai/dair-academy-plugins"
source_type: "official"
date_added: "2026-06-19"
author: "DAIR.AI"
license: "MIT"
license_source: "https://github.com/dair-ai/dair-academy-plugins/blob/main/README.md#license"
tags:
  - dair-academy
  - ai
  - workflow
tools:
  - claude-code
  - codex-cli
  - cursor
---

# Survey Generator

## 何时使用

当用户请求与此工作流匹配时使用：使用本技能执行其所文档化的工作流。

_来源：[dair-ai/dair-academy-plugins](https://github.com/dair-ai/dair-academy-plugins)（MIT）。_

生成学术风格的综述论文，输出为单个自包含 HTML 文件。

## 本技能的功能

给定一个主题和一个公开的锚点资源，本技能会：
1. 读取锚点资源，提取相关工作的全景概览。
2. 构建结构化的 `research_bundle.json`（标题、分类体系、章节、真实论文参考文献）。
3. 通过 Fireworks chat completions API 调用 Kimi K2.6，传入 research bundle 和固定的 `style_spec.json`。
4. 写出单文件 HTML 制品，包含内联 SVG 图表、学术排版、编号章节和参考文献列表。

使用本技能的智能体仅负责研究策展。所有正文、图表和 HTML 均由 Kimi K2.6 在一次 API 调用中生成。

## 用户输入

用户调用本技能时至少需提供：

- `topic`：简明的综述主题，例如 "Agentic Engineering" 或 "Reasoning Models"。
- `source_url`：公开的锚点资源。任何精选列表、权威博客文章、arXiv 综述、GitHub awesome-list 或索引页面均可。推荐起点：[DAIR.AI AI Papers of the Week](https://github.com/dair-ai/AI-Papers-of-the-Week)（持续更新的开源 AI/ML 重要论文索引，适合广泛主题），GitHub awesome-* 仓库，arXiv 综述 PDF，或维护良好的论文页面。

可选：

- `bibliography_size`：目标参考文献数量。默认 20 篇（快速综述）。40 到 50 篇适合全面综述，80 到 100 篇适合穷尽式综述。章节长度和 token 预算随此缩放。
- `section_count`：章节数量，默认 6 到 10。

如果用户未提供这些信息，使用 AskUserQuestion 在继续之前收集。

## 环境要求

- 环境中已导出 `FIREWORKS_API_KEY`。构建脚本从 `os.environ` 读取。
- Python 3，仅使用标准库（urllib）。无外部依赖。

## 智能体工作流

按顺序执行以下步骤。不要跳过步骤。

### 步骤 1. 读取锚点资源

获取并阅读 `source_url`。如果是 GitHub 仓库，获取 README 及任何相关的 `README-*.md` 或 `papers.md` 索引。如果是 arXiv 综述，使用摘要、图表和章节标题。如果是博客文章，通读全文。提取关键子主题及其引用的论文或系统名称。

对于广泛的 AI/ML 主题，[DAIR.AI AI Papers of the Week](https://github.com/dair-ai/AI-Papers-of-the-Week) 是特别丰富的锚点：它有回溯数年的每周期刊，每期包含 6 到 10 篇重要论文的简短摘要，便于跨时间扫描并筛选出与主题匹配的子集。

如果智能体有论文搜索工具可用（Papers-of-the-Week MCP、arXiv 搜索、Semantic Scholar、Google Scholar、组织的内部索引等），使用它来扩展锚点资源直接引用之外的候选论文池。

### 步骤 2. 定义分类体系和章节

起草一个以主题为根的分类体系，包含 4 到 8 个分支，每个分支有 2 到 4 个子项。分支应覆盖主题的不同子领域，不重叠。起草 6 到 10 个编号章节，与分类体系进展匹配：引言、基础、方法、评估、开放问题。图 1 的视口高度通过 `style_spec.json` 中的几何约定根据总叶节点数自动缩放，因此更深的分类体系也能正确渲染。

### 步骤 3. 策展参考文献

按 `bibliography_size` 选取真实论文。对于全面综述，40 到 50 篇是最佳数量；本技能已在 `build_artifact.py` 中使用 `max_tokens=81920` 测试至 100 篇。每条必须包含：`key`、`authors`、`year`、`title`、`venue`，以及 1 到 2 句的 `summary`。不要编造论文。每个章节的 `papers` 数组必须引用参考文献中存在的 key。

### 步骤 4. 写入 `research_bundle.json`

在技能目录中（`build_artifact.py` 旁边）写入 `research_bundle.json`。使用 `templates/research_bundle_template.json` 作为结构脚手架。必需的顶层字段：`title`、`authors_placeholder`、`anchor_source`、`abstract_hints`、`taxonomy`、`paradigms`、`stack`、`sections`、`table`、`bibliography`。完整示例参见 `examples/agentic-engineering/research_bundle.json`。

### 步骤 5. 运行生成器

```bash
python3 build_artifact.py
```

从技能目录运行此命令。脚本读取 `research_bundle.json` 和 `style_spec.json`，调用 Fireworks 上的 Kimi K2.6，并写入 `output/survey_kimi-k2p6_v{N}.html`。每次运行生成一个新的版本化文件。

要使用不同的 Fireworks 模型（例如 Kimi K2.5 进行并排比较）：

```bash
FIREWORKS_MODEL=accounts/fireworks/models/kimi-k2p5 python3 build_artifact.py
```

输出文件名按模型 slug 命名，可以跨模型比较版本。

### 步骤 6. 预览和迭代

在本地打开 HTML 文件。它是完全自包含的 HTML 文档，因此也可以从任何静态主机提供服务、嵌入仪表盘，或交给智能体暴露的任何制品预览机制。

如果图表效果不佳，优化 `style_spec.json`（`required_figures` 和 `figure_quality_note` 键）后重新运行。如果正文不够充实或章节缺失，收紧 `research_bundle.json` 中章节的 `guidance` 字段。不要直接编辑 Kimi 输出；迭代输入端。

常见图表故障模式及修复它们的 style_spec 模式：
- 不同面板的节点坍缩到同一面板：要求 `<g transform="translate(OFFSET,0)">` 分组使用面板局部坐标（图 2 已强制执行）。
- 叶节点矩形垂直重叠导致标签被裁剪：强制 rect_pitch 大于 rect_height，使用显式公式和健全性检查（图 1 已强制执行）。
- 根标签溢出其胶囊：在规范中固定最小矩形宽度（图 1 已强制执行，width=200）。
- 同行兄弟节点水平重叠（例如协调者-工作者面板中的 Worker A、Worker B、Worker C）：强制 N 个节点在固定宽度面板中使用确定性的 rect_width 和 center_x 公式，相邻矩形间有最小水平间距（图 2 多节点行已强制执行）。
- 面板内容偏左或偏右而非居中于面板背景中间：固定每个分组的 translate 偏移量以匹配面板背景的 x 位置（10、270、530），所有内容在面板局部 x=120 居中（图 2 已强制执行）。
- 图表因模型偏好不同叙事流程而以错误数字顺序输出：要求标题按 required_figures 的确切 ID 顺序使用序列号（图 1 先于图 2 先于图 3），即使这意味着将两个图放在同一章节中（通过 hard_rules_for_generation 强制执行）。
- 栈图右侧标签在视口边缘被裁剪：将栈 SVG 视口宽度设为 720，要求 role-text 的 tspan 在 x=710 内适配（图 3 已强制执行）。

添加新图或更改现有图时，遵循相同模式：声明绝对视口、逐元素坐标或确定性公式，以及描述末尾的硬不变量检查条款。

## 本技能的文件

- `SKILL.md` - 本文件。
- `build_artifact.py` - 调用 Fireworks 的 Python 脚本。
- `style_spec.json` - 视觉和结构规范（与主题无关）。
- `templates/research_bundle_template.json` - 新主题的空模板。
- `examples/agentic-engineering/` - 参考 100 篇论文运行（research_bundle.json + survey.html）。

## 智能体必须遵守的硬性规则

1. 永远不要编造参考文献条目。每篇引用的论文必须是真实存在的作品，有真实的发表场所。
2. 每个章节的 `papers` 数组必须引用参考文献中的 key。
3. 永远不要编辑生成的 HTML。在 `research_bundle.json` 或 `style_spec.json` 上迭代后重新运行。
4. 不要修改 `style_spec.json.hard_rules_for_generation` 中的硬性规则。
5. 保持 style_spec 与主题无关。特定主题的内容只存在于 `research_bundle.json` 中。
6. 不要在 research bundle 的正文字段中使用破折号或箭头符号。

## 局限性

- 当工作流指定上游工具、账户、API 密钥或本地设置时，需要相应的配置。
- 未经用户明确批准，不执行破坏性、生产环境、付费或外部消息操作。
- 在将生成的制品或建议视为最终结果之前，应根据用户的实际来源进行验证。
