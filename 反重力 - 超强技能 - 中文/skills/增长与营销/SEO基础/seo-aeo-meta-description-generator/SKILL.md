---
name: seo-aeo-meta-description-generator
description: "为每个页面生成 3 个标题标签变体和 3 个 meta description 变体，附带 SERP 预览、OG 标签和 Twitter Card 标签。当用户需要为任何页面撰写 meta 标签、标题标签或社交分享标签时激活。触发词：meta description、标题标签、meta标签、OG标签、Twitter Card、社交分享标签、SERP预览、CTR优化"
risk: safe
source: community
date_added: "2026-04-01"
---

# SEO-AEO Meta Description 生成器

## 概述

为任何页面生成 3 个标题标签变体和 3 个 meta description 变体，每个变体使用不同的 CTR 策略（收益前置、问题钩子、社会证明/数据）。同时生成 Open Graph 和 Twitter Card 标签。包含 SERP 预览模块和变体对比表，并给出推荐选择。

本技能是 [SEO-AEO Engine](https://github.com/mrprewsh/seo-aeo-engine) 的一部分。

## 使用场景

- 页面需要撰写或优化标题标签和 meta description 时
- 为 LinkedIn、X 或 WhatsApp 准备社交分享标签时
- 对搜索结果进行 A/B 测试 CTR 时
- 落地页撰写器或博客撰写器技能完成后使用

## 工作原理

### 第一步：确定每个变体的 CTR 角度
- **V1 收益前置** — 以结果或收益开头
- **V2 问题钩子** — 以搜索者正在问的问题开头
- **V3 社会证明/具体数据** — 以数字、统计或具体声明开头

### 第二步：应用字符限制
- 标题标签：50-60 个字符（硬性上限：60）
- Meta description：140-155 个字符（硬性上限：160）
- 描述不要在接近字数限制处断句

### 第三步：应用 CTR 规则
- 每个标题变体的前 3 个词必须包含主关键词
- 每个描述变体的前半部分必须包含主关键词
- 每条描述至少包含一个有说服力的词
- 每条描述以 CTA 动词结尾
- 不要使用"点击这里"、被动开头或全大写

### 第四步：撰写社交标签
OG 和 Twitter 标签可以比 SERP 标签更口语化。写成独立的文案——不要直接复制 meta description。

## 示例

### 示例 1：落地页变体
标题 V1：远程项目管理软件 | Syncro
（51 个字符）— 关键词在前，品牌在后
标题 V2：告别混乱，轻松管理远程团队 | Syncro
（54 个字符）— 痛点驱动 + 有说服力的词
描述 V1（收益前置）：
让分布式团队交付更快。Syncro 将任务、异步更新和冲刺整合在一个工具中。立即免费试用。
（141 个字符）✅
描述 V2（问题钩子）：
远程团队难以对齐？Syncro 用一个异步优先工作区取代分散的工具。免费试用。
（140 个字符）✅

## 最佳实践

- ✅ **应该做：** 写 3 个变体——始终给用户测试的选择
- ✅ **应该做：** OG 和 Twitter 描述比 SERP 版本更口语化
- ✅ **应该做：** 输出前验证每个变体的字符数
- ❌ **不应该做：** 每条描述中不要重复使用完全相同的锚文本或关键词
- ❌ **不应该做：** 不要将 meta description 直接复制粘贴到 OG description
- ❌ **不应该做：** 不要让任何描述在接近字数限制处断句

## 常见陷阱

- **问题：** 描述在搜索结果中被截断到词中间
  **解决：** 与其让搜索引擎自然截断，不如主动删减一个从句。

- **问题：** 3 个变体听起来一模一样
  **解决：** 每个变体必须使用真正不同的 CTR 策略——不只是换词顺序。

## 相关技能

- `@seo-aeo-landing-page-writer` — 提供本技能为其撰写标签的页面内容
- `@seo-aeo-content-quality-auditor` — 在完整审计中验证 meta 元素

## 相关资源

- [SEO-AEO Engine 仓库](https://github.com/mrprewsh/seo-aeo-engine)
- [完整版 Meta Description 生成器 SKILL.md](https://github.com/mrprewsh/seo-aeo-engine/blob/main/.agent/skills/meta-description-generator/SKILL.md)

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
