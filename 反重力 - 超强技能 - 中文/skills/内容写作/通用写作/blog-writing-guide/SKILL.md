---
name: blog-writing-guide
description: "本技能在每篇博文中贯彻 Sentry 的写作标准——无论你是帮工程师写第一篇博文，还是帮营销人员起草产品公告。当用户要求'写博客文章'、'起草博文'、'博客写作规范'、'Sentry风格博文'时使用。"
risk: unknown
source: community
date_added: '2026-03-06'
---

# Sentry 博客写作技能

本技能在每篇博文中贯彻 Sentry 的写作标准——无论你是帮工程师写第一篇博文，还是帮营销人员起草产品公告。

**门槛：** 每篇 Sentry 博文都应该是资深工程师愿意分享到团队 Slack、或在技术决策中引用的内容。

以下是需要内化并应用于每篇内容的核心原则。

## 何时使用
- 你需要起草或编辑 Sentry 博文。
- 任务涉及技术叙事、产品公告或以 Sentry 博客风格撰写的工程深度解析。
- 你想要有态度、有细节、技术可信的博客内容，而非泛泛的营销文案。

## Sentry 的声音

**我们听起来像：** 技术大会 afterparty 上一个资深开发者正兴奋地解释某个东西——聪明、具体、有点不羁、底蕴深厚。

**我们听起来不像：** 企业博客、新闻稿、销售 PPT 或 AI 生成的摘要。

技术上要精准，有态度，直截了当。幽默可以，但要为内容服务，不能替代内容。讽刺管用。每篇一个好笑话就够了。

用"我们"（Sentry）和"你"（读者）。这是对话，不是论文。

## 禁用措辞

永远不要用这些。它们是自动红旗：

- "We're excited/thrilled to announce"——直接宣布就行
- "Best-in-class" / "industry-leading" / "cutting-edge"——用事实说话，别自夸
- "Seamless" / "seamlessly"——没有什么是无缝的
- "Empower" / "leverage" / "unlock"——说你真正想表达的意思
- "Robust"——描述是什么让它 robust，而不是用这个词
- "At [Company], we believe..."——直接陈述你的观点
- "Streamline"——人人都在 streamline，别再用了
- 废话过渡语："That being said," "It's worth noting that," "At the end of the day," "Without further ado," "As you might know"
- "In this blog post, we will explore..."——直接开始，别铺垫

## 开头（前 2-3 句）

开头必须做两件事之一：**陈述问题** 或 **陈述结论**。永远不要以背景介绍、公司历史或炒作开场。

**好：** "Two weeks before launch, we killed our entire metrics product. Here's why pre-aggregating time-series metrics breaks down for debugging, and how we rebuilt the system from scratch."

**差：** "At Sentry, we're always looking for ways to improve the developer experience. Today, we're thrilled to share some exciting updates to our metrics product that we think you'll love."

## 结构：跟随读者的问题

每篇文章的结构都要围绕读者真正想知道的，而不是你的内部叙事：

1. **这解决了什么问题？**（最多 1-2 段）
2. **它到底怎么工作的？** 不是点哪个按钮，而是底层技术原理。（文章主体——要具体）
3. **权衡和替代方案是什么？**（这是区分好与优秀的关键）
4. **我怎么使用/试用/实现？**（具体的下一步）

对于工程深度解析，还要回答：
5. **我们试过什么行不通的方案？**（建立信任）
6. **已知的局限是什么？**（展现智识诚实）

## 章节标题必须传达信息

**弱标题：** "Background," "Architecture," "Results," "Conclusion"

**强标题：** "Why time-series pre-aggregation destroys debugging context," "The scatter-gather approach to distributed GROUP BY," "Where this breaks down: the cardinality wall"

## 技术质量标准

**数字优于形容词。** 如果你做性能声明，带上数字。
- 差："This significantly reduced our error processing time."
- 好："This reduced our p99 error processing time from 340ms to 45ms — a 7.5× improvement."

**代码必须能跑。** 如果文章包含代码，测试它。包含 import、配置和上下文。注释应该解释*为什么*，而不是*是什么*。

**系统要配图。** 如果你描述的系统有超过两个交互组件，加一张图。标注真实的服务名，别用通用方框。

**诚实胜过炒作。** 永远不要夸大功能。承认局限。如果是 beta，就说 beta。如果竞品某方面做得好，提一下也没关系。不要声称 AI 功能比实际更强大——"Seer suggests a likely root cause" ≠ "Seer finds the root cause."

## 标题指南

标题是文章中杠杆最高的句子。它必须能让刷 RSS 或 Twitter 的开发者停下来。

**强标题** 做出具体声明、讲述故事或承诺具体收获：
- "The metrics product we built worked. But we killed it and started over anyway"
- "How we reduced release delays by 5% by fixing Salt"
- "Your JavaScript bundle has 47% dead code. Here's how to find it."

**弱标题** 是模糊的公告：
- "Introducing our new metrics product"
- "Performance improvements in Sentry"
- "AI-powered debugging with Seer"

## 结尾

用有用的东西结尾——文档链接、试用方式、反馈入口。永远不要用泛泛的炒作（"We can't wait to see what you build!"）或重复你刚说过的内容。

## 文章类型

按类型的快速对照：

| 类型 | 目标 | 署名 |
|------|------|------|
| 工程深度解析 | 解释技术系统/决策，让其他工程师学到东西 | 构建它的工程师。永远是。 |
| 产品发布 | 解释发布了什么、为什么重要、怎么用 | PM、工程师或 DevEx。除非是市场部做的，否则不是 PMM。 |
| 事后复盘 | 透明的故障分析，含时间线和修复 | 工程管理层 |
| 数据/研究 | 来自 Sentry 独特数据优势的原创洞察 | 数据团队、工程或研究 |
| 教程/指南 | 帮开发者完成一件具体的事 | DevEx、工程师或社区贡献者 |

## "我会分享这篇吗？"测试

发布前问自己：开发者会分享这篇文章吗？有机会上 Hacker News 吗？如果答案是否，说明文章要么需要更多深度、更多原创洞察，要么它只配放在 changelog 里。

值得分享的文章至少包含以下之一：
- 附带权衡分析的技术决策
- 别处找不到的原创数据或研究
- 有具体细节的真实调试故事
- 对出问题的东西的诚实复盘
- 能为读者省下真时间的实操指南

## 不可妥协项（速查）

1. 永远不要在没有真人署名的情况下发布。不要 "The Sentry Team" 署名。
2. 永远不要发布跑不通的代码。
3. 永远不要说 "we're excited to announce"。直接宣布。
4. 如果你描述一个系统，加图。
5. 如果你做性能声明，带数字。
6. 如果你讨论一个决策，解释你没选什么以及为什么。
7. 每篇文章动笔前，作者心中必须有明确的"这是写给谁的"。
8. Changelog 的内容放 changelog。博文应该提供更多价值。
9. 拿不准时，往深了写。太浅的风险远大于太详细。
10. 写那篇你当初解决这个问题时希望存在的文章。

## 审阅或编辑草稿时

过一遍这两份清单：

**技术审阅：**
- 所有技术声明准确
- 代码示例能跑
- 架构描述与实际一致
- 数字和基准测试正确
- 没有会让专家皱眉的过度简化

**编辑审阅：**
- 开头 2 句内抓住读者
- 通过"我会分享这篇吗？"测试
- 没有企业腔、废话或水分
- 标题传达信息
- 长度合适（不注水，不太薄）
- 标题具体且有吸引力

**最终检查：**
- 作者署名正确（真人姓名）
- 包含文档/入门链接
- 文章不重复 changelog 已有的内容

给出反馈时，要具体、有建设性。引用写得差的段落，解释为什么差，然后重写一遍示范标准。

## 局限
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，停下来请求澄清。
