---
name: seo-aeo-internal-linking
description: "映射页面间的内部链接机会，包含锚文本、放置说明、孤立页面检测和关键词蚕食检查。当用户需要构建内部链接策略或查找链接机会时触发。触发词：内部链接、链接策略、锚文本、孤立页面、链接机会、internal linking、link strategy"
risk: safe
source: community
date_added: "2026-04-01"
---

# SEO-AEO 内部链接

## 概述

分析一组页面，输出按优先级排序的内部链接机会列表，包含精确的锚文本、展示每个链接应出现位置的上下文句子、孤立页面检测、锚文本蚕食警告，以及展示权威如何在内容间流动的链接权重图。

属于 [SEO-AEO Engine](https://github.com/mrprewsh/seo-aeo-engine) 的一部分。

## 使用场景

- 在新支柱页面和其集群文章之间建立内部链接时使用
- 审计现有网站的孤立页面时使用
- 内容集群生成主题地图后使用
- 需要带放置上下文的锚文本建议时使用

## 工作原理

### 步骤 1：检测孤立页面
标记所有零入站内部链接的页面。这些页面对搜索引擎不可见，必须立即添加链接。

### 步骤 2：构建语义重叠矩阵
按主要关键词相似度和内容摘要匹配页面，识别自然的链接机会。

### 步骤 3：分配链接类型
每个建议标记为以下四种之一：
- **集群 → 支柱** — 最高优先级，向上汇聚权威
- **支柱 → 集群** — 向下分发权威
- **集群 → 集群** — 构建语义深度
- **上下文增强** — 将权重集中在目标页面

### 步骤 4：编写上下文句子
为每个链接机会编写锚文本应出现的句子 — 自然放置，不要生硬插入。

### 步骤 5：检查锚文本
标记同一目标页面使用超过一次的完全匹配锚文本为蚕食风险。永远不要使用"点击这里"之类的通用锚文本。

## 示例

### 示例：链接机会输出
🔴 高优先级 — 链接 1
类型：集群 → 支柱
来源："How to Build a Budget That Actually Works"
目标："The Complete Guide to Automated Budgeting"
锚文本："automated budgeting guide"
上下文："For a full breakdown of every method available,
see our [automated budgeting guide]."
影响：在支柱页面汇聚主题权威。
孤立页面警报：
"PennyWise Pricing Page" 没有入站链接。
修复：从文章 2 的对比表格中添加链接。

## 最佳实践

- ✅ **推荐：** 每篇集群文章至少有一条集群 → 支柱链接
- ✅ **推荐：** 为每个建议编写上下文句子 — 锚文本需要自然放置
- ✅ **推荐：** 在添加新链接之前先修复孤立页面
- ❌ **避免：** 对同一目标页面使用超过一次相同的完全匹配锚文本
- ❌ **避免：** 使用"点击这里"、"了解更多"或"阅读更多"作为锚文本 — 永远不要
- ❌ **避免：** 单个页面的出站内部链接超过 100 条

## 常见陷阱

- **问题：** 所有集群文章都链接到支柱但彼此之间没有链接
  **解决方案：** 在语义相关的文章之间添加集群 → 集群链接以构建深度。

- **问题：** 多个页面对同一目标使用相同的锚文本
  **解决方案：** 在首次使用完全匹配锚文本后，后续链接使用部分匹配和品牌锚文本。

## 相关技能

- `@seo-aeo-content-cluster` — 生成本技能链接的集群地图
- `@seo-aeo-schema-generator` — 使用链接图输出生成 BreadcrumbList schema

## 附加资源

- [SEO-AEO Engine 仓库](https://github.com/mrprewsh/seo-aeo-engine)
- [完整 Internal Linking SKILL.md](https://github.com/mrprewsh/seo-aeo-engine/blob/main/.agent/skills/internal-linking/SKILL.md)

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
