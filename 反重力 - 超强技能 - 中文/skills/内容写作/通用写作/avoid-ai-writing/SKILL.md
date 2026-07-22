---
name: avoid-ai-writing
description: "审计并重写内容，移除21类AI写作模式，提供43条替换表。触发词：AI写作、AI痕迹、去AI化、机器生成、AI腔调、AI风格、去除AI感、人工写作、自然写作、AI文本检测"
risk: none
source: https://github.com/conorbronsdon/avoid-ai-writing
date_added: "2026-03-06"
---

# Avoid AI Writing — 审计与重写

检测并修复让文本听起来像机器生成的AI写作模式（"AI腔调"）。覆盖21种模式类别，提供43条词汇/短语替换表，将每个标记词映射到具体、更朴素的替代词。

## 何时使用此技能

- 当被要求"移除AI痕迹"、"清理AI写作"或"让这听起来不像AI"时
- 使用AI起草内容后、发布之前
- 编辑任何听起来像是生成而非撰写的文本时
- 审计文档、博客文章、营销文案或内部沟通中的AI特征时

## 检测内容

**21种模式类别：** 格式问题（破折号、粗体滥用、表情符号标题、项目符号过多）、句子结构问题（模糊表达、空洞强调词、三段式规则）、词汇/短语替换（43条，如leverage→use、utilize→use、robust→reliable）、模板短语、过渡短语、结构问题、重要性夸大、系词回避、同义词循环、模糊归因、填充短语、通用结论、聊天机器人痕迹、名人点名、肤浅的-ing分析、促销语言、公式化挑战、虚假范围、内联标题列表、标题大小写、截断免责声明。

## 示例

**提示词：**
```
审计这段文字的AI写作模式：

"In today's rapidly evolving AI landscape, developers are embarking on a pivotal journey to leverage cutting-edge tools that streamline their workflows. Moreover, these robust solutions serve as a testament to the industry's commitment to fostering seamless experiences."
```

**输出：** 技能返回四个部分：
1. **发现的问题** — 引用每个AI腔调词（landscape、embarking、pivotal、leverage、cutting-edge、streamline、robust、serves as、testament to、fostering、seamless、Moreover、In today's rapidly evolving...）
2. **重写版本** — "Developers are starting to use newer AI tools to simplify their work. These tools are reliable, and they're making development less painful."
3. **变更说明** — 编辑摘要
4. **二次审计** — 重新阅读重写版本以捕捉任何残留特征

## 局限性

- 不检测AI生成的代码，仅检测文本
- 模式匹配基于指导原则，非绝对 — 某些标记词在上下文中可能是恰当的
- 替换表建议替代词，但最佳选择取决于上下文
- 无法验证事实声明或找到真实引用来替换模糊归因
