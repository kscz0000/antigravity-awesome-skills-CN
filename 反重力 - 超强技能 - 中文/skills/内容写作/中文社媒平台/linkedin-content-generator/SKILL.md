---
name: linkedin-content-generator
description: "AI 驱动的 LinkedIn 内容套件：生成帖子、轮播图、Newsletter 及 30 天内容日历，内置领域特定 SEO 规则和强化学习个人记忆系统。触发词：LinkedIn 内容生成、领英发帖、LinkedIn 轮播图、LinkedIn Newsletter、LinkedIn 内容日历、LinkedIn SEO、社媒文案、领英营销"
category: marketing
risk: safe
source: community
source_repo: sarveshtalele/linkedin-content-skill
source_type: community
date_added: "2026-06-04"
author: sarveshkishortalele
tags: [linkedin, content-creation, social-media, marketing, newsletter, carousel, content-calendar, reinforcement-learning, seo, copywriting]
tools: [claude]
license: "MIT"
license_source: "https://github.com/sarveshtalele/linkedin-content-skill/blob/main/LICENSE"
---

# LinkedIn 内容生成器

## 概述

这是一套面向 Claude Code 的完整 LinkedIn 内容创作工具，能够将主题和领域转化为可直接发布的帖子、多页轮播图、长篇 Newsletter 期号以及 30 天内容日历——全部通过个人强化学习记忆系统串联，使每次输出都能根据你的反馈不断改进。

七个协调的命令覆盖了完整的内容工作流：

| 命令 | 用途 |
|---|---|
| `/generate-post` | 单条可发布的 LinkedIn 帖子 |
| `/generate-carousel` | 编号幻灯片内容 + 配文说明 |
| `/generate-newsletter` | 长篇 Newsletter 期号 |
| `/generate-calendar` | 30 天发布日历（Markdown 表格格式） |
| `/show-memory` | 显示当前偏好和反馈日志 |
| `/feedback` | 保存有效模式供后续输出参考 |
| `/clear-memory` | 重置记忆为出厂默认值 |

所有辅助脚本均打包在 `skills/linkedin-content-generator/scripts/` 目录下，与本 `SKILL.md` 同步发布。它们负责构建精心设计的 prompt，注入已保存的偏好设置，并在 Claude 生成输出前强制执行 LinkedIn SEO 规则。
本地 `memory.md` 文件会跨所有会话持久保存你的风格、语调、成功钩子和最佳表现形式。

## 适用场景

- 当你需要一条可即贴即发的 LinkedIn 帖子，且需要经过 SEO 优化的钩子和话题标签时使用。
- 当你在构建面向 LinkedIn Documents 的多页轮播图时使用。
- 当你在撰写结构化章节的长篇 LinkedIn Newsletter 期号时使用。
- 当你在规划整月内容，需要多种格式搭配和节奏控制规则时使用。
- 当你希望内容能通过保存的反馈逐步适应你的个人风格时使用。
- 当你在任何垂直领域（AI、SaaS、市场营销、金融、医疗等）工作，且需要避免常见 LinkedIn 算法陷阱的原生平台格式时使用。

## 前置要求

你的 shell 路径中必须可用 **Python 3.8 或更高版本**。

本技能是自包含的。从 antigravity skills 库安装：

```bash
# 通过 antigravity CLI 安装（推荐）
antigravity install linkedin-content-generator

# 或手动复制到 Claude Code skills 目录
cp -r skills/linkedin-content-generator ~/.claude/skills/
```

全部六个 Python 脚本和默认 `memory.md` 都打包在本技能的 `scripts/` 子目录中。无需额外的克隆或下载操作。不需要 API 密钥、外部服务或网络访问。

## 工作原理

### 架构

```
用户命令 (/generate-post ...)
        │
        ▼
SKILL.md 解析 $ARGUMENTS
        │
        ▼
Python 脚本构建 prompt
  • 注入 LinkedIn SEO 规则
  • 注入 memory.md 偏好
        │
        ▼
Claude 生成可直接发布的内容输出
        │
        ▼
/feedback 保存有效经验 → memory.md
        （循环 —— 每次未来输出都会改进）
```

### 第一步：设置你的领域（一次性操作）

打开 `~/.claude/skills/linkedin-content-generator/scripts/memory.md` 并更新**主要领域**字段：

```markdown
## Core Identity & Tone
- **Primary Niche:** AI & Technology   ← 修改此处
```

该字段会被注入到每个 prompt 中。如果不修改，技能默认使用 `"AI & Technology"`。

### 第二步：生成内容

运行下方**命令参考**部分描述的任意七个命令之一。Claude 读取脚本输出后直接在聊天中生成最终内容。

### 第三步：保存有效经验

每次输出后，使用 `/feedback` 保存成功的模式：

```
/feedback 本帖中的故事化钩子获得的评论数是平时的 3 倍
```

反馈会被追加写入 `memory.md`，并自动注入到后续所有生成 prompt 中。

## 命令参考

### `/generate-post` — 单条 LinkedIn 帖子

生成一条令人驻足、SEO 优化的 LinkedIn 文字帖子。

**用法：**
```
/generate-post <主题> [in <领域>] [tone: controversial|storytelling|educational|motivational|professional]
```

**参数：**

| 参数 | 默认值 | 可选值 |
|---|---|---|
| `topic` | 必填 | 任何主题 |
| `niche` | `"AI & Technology"` | 任何行业 |
| `tone` | `professional` | `professional` · `storytelling` · `controversial` · `educational` · `motivational` |
| `style` | `list-based` | `list-based` · `text-only` · `storytelling` · `data-driven` · `contrarian` |

**示例：**

```
/generate-post 为什么大多数开发者时间管理失败 in Software Engineering tone: storytelling
```

```
/generate-post 技术债务的真实成本 in SaaS tone: controversial
```

```
/generate-post 创业前我希望知道的 5 件事 in Entrepreneurship tone: educational style: list-based
```

**输出结构：**
1. 令人驻足的钩子（2 行，触发"展开全文"）
2. 背景 / 问题铺垫（2–3 个短句）
3. 核心价值（编号列表或项目符号，最多 7 项）
4. 关键要点（1–2 句精炼总结）
5. 明确的行动号召（CTA）
6. 3–5 个话题标签（宽泛 + 垂直 + 社区组合）

---

### `/generate-carousel` — LinkedIn 轮播图

生成编号幻灯片内容以及一条可直接使用的 LinkedIn 配文。

**用法：**
```
/generate-carousel <主题> [in <领域>] [<n> 页] [style: how-to|listicle|myth-busting|framework|story-arc]
```

**参数：**

| 参数 | 默认值 | 可选值 |
|---|---|---|
| `topic` | 必填 | 任何主题 |
| `niche` | `"AI & Technology"` | 任何行业 |
| `slides` | `7` | `3`–`12` |
| `style` | `listicle` | `how-to` · `listicle` · `myth-busting` · `framework` · `story-arc` |

**风格指南：**

| 风格 | 结构 |
|---|---|
| `how-to` | 第 1 页 = 问题 → 第 2 至 N 页 = 步骤 → 最后一页 = 结果 / CTA |
| `listicle` | 每页 = 一个条目，加粗标题 + 1–2 句解释 |
| `myth-busting` | 每页 = `MYTH: [认知]` → `TRUTH: [真相]` |
| `framework` | 引入一个原创框架；每页 = 一个组成部分 |
| `story-arc` | 第 1 页 = 之前 → 中间 = 过程 → 最后一页 = 之后 + CTA |

**示例：**

```
/generate-carousel 10 个 prompt 工程错误 8 页 style: myth-busting
```

```
/generate-carousel 构建第二大脑 in Knowledge Management 7 页 style: how-to
```

```
/generate-carousel PARA 效率法 in Personal Development style: framework
```

**输出：** 幻灯片从 `1` 到 `N` 编号，后附一条包含钩子、引导语境、"滑动查看→"提示和话题标签的 LinkedIn 配文。

---

### `/generate-newsletter` — LinkedIn Newsletter 期号

生成一篇完整的、针对 LinkedIn Newsletter 编辑器结构化的长篇期号。

**用法：**
```
/generate-newsletter <主题> [in <领域>] [length: short|medium|long] [title: "<系列标题>"]
```

**参数：**

| 参数 | 默认值 | 可选值 |
|---|---|---|
| `topic` | 必填 | 任何主题 |
| `niche` | `"AI & Technology"` | 任何行业 |
| `length` | `medium` | `short`（约 700 词）· `medium`（约 1,200 词）· `long`（约 2,000 词） |
| `title` | 自动生成 | 可选的系列名称 |

**示例：**

```
/generate-newsletter AI 如何重塑招聘流程 in HR & Recruiting length: medium
```

```
/generate-newsletter 2026 年开发者工具现状 in DevTools length: long title: "Build Layer Weekly"
```

**输出结构：**
1. SEO 优化的 H1 标题
2. 开场钩子（个人轶事、数据或大胆论断）
3. 带 H2 二级标题的正文段落
4. 关键要点（3–5 个要点列表）
5. 本周具体行动步骤
6. 互动问题以激发评论

---

### `/generate-calendar` — 30 天内容日历

生成一个 Markdown 表格格式的日历，包含月度主题、SEO 关键词和格式分布。

**用法：**
```
/generate-calendar [niche: <领域>] [days: <天数>] [frequency: <频率>] [goal: awareness|engagement|leads|authority|growth]
```

**参数：**

| 参数 | 默认值 | 可选值 |
|---|---|---|
| `niche` | 必填 | 任何行业 |
| `days` | `30` | 任意正整数 |
| `frequency` | `"每周 3 次"` | 任意发布节奏 |
| `goal` | `growth` | `awareness` · `engagement` · `leads` · `authority` · `growth` |

**目标指南：**

| 目标 | 策略 |
|---|---|
| `awareness` | 易分享、有共鸣、追热点；大量使用轮播图和反向观点 |
| `engagement` | 观点帖、投票、问答、故事叙述以最大化评论量 |
| `leads` | 教育价值帖 + 权威建设 + 明确私信 CTA |
| `authority` | 深度洞察、数据支撑帖、思想领导力、Newsletter |
| `growth` | 病毒式传播格式（轮播图、列表、反向观点）与高价值教育内容混合 |

**示例：**

```
/generate-calendar niche: Fintech days: 30 frequency: daily goal: authority
```

```
/generate-calendar niche: Marketing Agencies days: 14 frequency: 5 times a week goal: leads
```

**输出：** Markdown 表格（`# | Day | Format | Topic / Angle | Hook | CTA`）+ 月度主题 + Top 5 SEO 关键词 + 格式分布汇总。

---

### `/show-memory` — 显示偏好设置

显示当前记忆内容：领域、语调、风格及所有已保存的反馈记录。

**用法：**
```
/show-memory
```

**输出：** 完整的 `memory.md` 内容，含记录数量、主要领域和语调摘要。

---

### `/feedback` — 保存成功模式

向 `memory.md` 追加一条带标签的反馈记录。后续输出将自动融合已保存的模式。

**用法：**
```
/feedback <哪些做法有效>
```

**示例：**

```
/feedback 反向观点钩子"关于 X 的普遍看法都是错的"带来了 400% 更多曝光
```

```
/feedback DevOps 领域的辟谣类轮播图的收藏量是清单体的 3 倍
```

```
/feedback 用个人失败故事的故事化语调在我的受众群体中胜过数据驱动风格
```

---

### `/clear-memory` — 重置记忆

将 `memory.md` 重置为出厂默认值。执行前命令会要求确认。

**用法：**
```
/clear-memory
```

## LinkedIn SEO 规则（自动强制执行）

技能通过打包的 `scripts/utils.py` 将这些规则注入每个 prompt。它们**不是可选的**；它们是使输出符合平台原生特性的 prompt 工程的一部分。

### 钩子工程
- 第一行必须令人驻足（大胆论断、惊人数据、挑衅性问题或个人故事开场）。
- 第二行必须制造模式中断，迫使用户点击"展开全文"。
- 禁用开头语：`"In today's..."`、`"I am excited to..."`、`"Happy to share..."`、`"Thrilled to announce..."`。

### 可读性规则
- 每段最多 2 个句子。
- 积极换行 —— 空白在 LinkedIn 上获胜。
- 加粗谨慎使用，仅用于关键信息。
- 目标阅读水平：8 年级或以下。

### 话题标签策略
- 1 个宽泛标签（`#AI`、`#Marketing`、`#Leadership`）。
- 2 个垂直领域标签（`#AIAgents`、`#ContentMarketing`、`#StartupLife`）。
- 1–2 个社区标签（`#LinkedInTips`、`#PersonalBranding`）。
- 硬性上限：**总共不得超过 5 个**。

## 最佳实践

- ✅ 在 `memory.md` 中设置 **Primary Niche** 后再生成任何内容。
- ✅ 任何表现良好的帖子之后都运行 `/feedback` —— 记忆效果会随时间复利增长。
- ✅ 在规划内容冲刺时先使用 `/generate-calendar`；它能为 `/generate-post` 和 `/generate-carousel` 运行提供选题。
- ✅ 日历周期内混用轮播图风格：listicle、myth-busting 和 story-arc 表现各异，有助于防止受众疲劳。
- ✅ 对你持有真实、可辩护立场的议题尝试 `controversial` 语调；对于细微差别比冲击力更重要的议题则避免使用。
- ❌ 不要跳过 `/feedback` 循环 —— 缺少它的话，每次输出都是从通用 LinkedIn 最佳实践起步，而非基于你的特定受众数据。
- ❌ 不要发布超过 5 个话题标签；LinkedIn 算法会对标签堆砌进行降权。
- ❌ 没有真实统计数据可引用时不要使用 `data-driven` 风格；编造数字对可信度的破坏速度超过任何其他 LinkedIn 错误。
- ❌ 不指定 `goal` 就不要生成 30 天日历；默认的 `growth` 目标广泛混合各种格式，可能不匹配特定活动目标。

## 局限性

- 本技能不会直接发布到 LinkedIn。所有输出均可复制粘贴，但需通过 LinkedIn 网页端或移动端手动发布。
- 记忆系统是基于文件且本地的。除非手动同步 `memory.md`，否则不会跨机器或团队成员共享。
- 技能不会验证 LinkedIn 实时算法变更。SEO 规则基于截至 2025 年中期的文档化最佳实践，随着平台演进可能需要手动更新。
- 日历输出不会自动排期或集成排程工具（Buffer、Hootsuite 等）。它仅生成一个可供手动导入的 Markdown 表格。
- `slides` 参数会被钳制在范围 `3–12` 内。超出此范围的轮播图将被静默调整至最近的边界值。
- 随着 feedback 累积，`memory.md` 会无限增长。过大的记忆文件（500+ 条记录）可能超出 prompt 上下文限制并导致截断。定期使用 `/clear-memory` 归档旧条目并用核心经验重新播种。
- 在 `python3` 不可用或 `Bash` 工具调用被阻止的沙箱环境中无法工作。

## 安全与安全提示

本技能使用 `Bash` allowed-tool 来运行位于 `~/.claude/skills/linkedin-content-generator/scripts/` 的 Python 脚本。除 `memory_manager.py` 外，所有脚本均为只读操作，而 `memory_manager.py` 仅写入同一打包目录内的 `memory.md`。

- 任何脚本都不发起网络请求。
- 不读取、写入或记录任何凭据、token 或密钥。
- 不修改 `~/.claude/skills/linkedin-content-generator/scripts/` 以外的文件。
- `memory_manager.py` 中的 `clear` 命令仅覆盖打包的 `memory.md`；它不会删除其他任何文件。
- 所有传给 `memory_manager.py` 的 `--feedback` 和 `--id` 参数都会原样写入 `memory.md`。不要将 shell 元字符或敏感数据作为反馈字符串传递。

本技能中的所有 Bash 命令均为本地 Python 调用，无需提升权限：

```bash
# SKILL_SCRIPTS 解析为 ~/.claude/skills/linkedin-content-generator/scripts
SKILL_SCRIPTS="${HOME}/.claude/skills/linkedin-content-generator/scripts"
python3 "${SKILL_SCRIPTS}/generate_post.py" --topic "..." --niche "..." --tone professional --style list-based
python3 "${SKILL_SCRIPTS}/memory_manager.py" add --id "..." --feedback "..." --tags "..."
python3 "${SKILL_SCRIPTS}/memory_manager.py" read
python3 "${SKILL_SCRIPTS}/memory_manager.py" clear
```

<!-- security-allowlist: approved — all commands are local Python script invocations with no network access, no credential handling, and writes scoped to the skill's own bundled scripts/memory.md only -->

## 常见问题排查

- **问题：** 脚本退出时报 `ModuleNotFoundError` 或 `No module named 'utils'`。
  **解决方案：** 每个脚本使用 `sys.path.insert(0, SCRIPT_DIR)` 定位相对于自身的 `utils.py`，因此必须使用绝对路径调用 —— 不能从 `scripts/` 目录内部调用。使用
  `python3 "${HOME}/.claude/skills/linkedin-content-generator/scripts/generate_post.py" ...`。

- **问题：** 记忆未被应用到生成的内容中。
  **解决方案：** 检查 `memory.md` 是否存在于
  `~/.claude/skills/linkedin-content-generator/scripts/memory.md`。运行 `/show-memory` 确认。如果缺失，运行任意一次生成器命令 —— 它会从打包模板自动创建文件。

- **问题：** 日历输出缺少天数或表格格式异常。
  **解决方案：** 验证 `--days` 值是否为正整数，以及 `--frequency` 如果包含空格是否加了引号（例如 `"3 times a week"`）。脚本会将这些值直接传入 prompt 字符串。

- **问题：** 轮播图幻灯片数量超过请求的数量。
  **解决方案：** `slides` 值在服务端被钳制至 `[3, 12]` 范围内。如果 Claude 生成的幻灯片多于请求量，是因为它遵循了风格指南的结构（封面 + 内容 + CTA）。指定精确数量和风格可获得精准控制。

- **问题：** 已保存反馈的情况下生成的帖子听起来仍然很泛泛。
  **解决方案：** 记忆条目作为上下文注入，而非硬性规则。使用具体的、可操作的反馈：`"以个人失败故事开头的表现优于数据统计"` 比 `"故事化不错"` 更有用。

- **问题：** Windows 上找不到 `python3`。
  **解决方案：** 从 python.org 安装 Python 3.8+ 并确保其在 PATH 中，或通过
  `py "%USERPROFILE%\.claude\skills\linkedin-content-generator\scripts\generate_post.py" ...` 运行。在没有 WSL 的 Windows 上，`Bash` 工具调用可能需要在 SKILL.md 的 `allowed-tools` 上下文中进行调整。

## 相关技能

- `@content-creator` — 更广泛的品牌声音分析、SEO 优化和跨平台内容框架。在构建超越 LinkedIn 的完整内容营销系统时使用。
- `@content-strategy` — 主题集群规划、编辑路线图和内容组合策略。在运行 `/generate-calendar` 前需要先定义支柱主题时使用。
- `@content-marketer` — 跨渠道的活动级内容规划。当 LinkedIn 是更广泛多平台发布中的一个渠道时，可作为本技能的补充。
- `@linkedin-automation` — 通过 Composio/Rube MCP 进行程序化 LinkedIn 发布。当在此处生成内容后希望自动化发布步骤时，与本技能配合使用。
- `@linkedin-profile-optimizer` — LinkedIn 个人资料和个人品牌优化。在使用本技能之前运行，以便让生成内容的语气与你资料的标题、简介和精选板块保持一致。

## 扩展资源

- [LinkedIn 算法指南（官方）](https://www.linkedin.com/help/linkedin/answer/a522537)
- [LinkedIn Newsletter 最佳实践](https://www.linkedin.com/help/linkedin/answer/a544800)
- [源仓库 — linkedin-content-skill](https://github.com/sarveshtalele/linkedin-content-skill)
