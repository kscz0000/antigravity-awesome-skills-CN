---
name: recsys-pipeline-architect
description: "使用六阶段 Source→Hydrator→Filter→Scorer→Selector→SideEffect 框架设计可组合的推荐、排序和 Feed 流水线。触发词：推荐系统、排序流水线、Feed 算法、个性化 Feed、for-you feed、RAG 重排序、pipeline 架构、推荐流水线、内容排序、通知分级"
category: data-ai
risk: safe
source: community
source_repo: mturac/recsys-pipeline-architect
source_type: community
date_added: "2026-05-16"
author: mturac
tags: [recommender-system, ranking, feed-algorithm, recsys, personalization, for-you-feed, rag-reranker, pipeline-architecture]
tools: [claude, codex, cursor, gemini, opencode, cline, continue, windsurf]
license: "MIT"
license_source: "https://github.com/mturac/recsys-pipeline-architect/blob/main/LICENSE"
---

# 推荐流水线架构师

## 概述

一个用于构建可组合推荐、排序和 Feed 流水线的规格与脚手架技能。它编码了由 xAI 开源的 [For You 算法](https://github.com/xai-org/x-algorithm)（Apache 2.0）所推广的六阶段 **Source → Hydrator → Filter → Scorer → Selector → SideEffect** 框架。本技能是该模式的独立重新实现——未复制原始代码——以 MIT 许可发布。当你需要"为（用户, 上下文）选取 Top K 条目"时即可使用：社交 Feed、内容 CMS、RAG 重排序器、任务优先级排序、通知分级、搜索重排序、广告排序。

## 何时使用此技能

- 当用户想构建任何"为用户/上下文选取 Top K 条目"的系统时使用
- 当用户问"我应该如何对 X 排序"或描述 Feed/个性化问题时使用
- 当用户已有评分函数，需要围绕它搭建流水线基础设施时使用
- 当用户想从单一相关性分数迁移到可调权重的多行为预测时使用
- 当用户正在封装 LLM/ML 评分器，需要过滤器、填充器、副作用以及在他们的技术栈中可运行的脚手架时使用（TypeScript / Go / Python）

## 工作原理

### 步骤 1：澄清用例

向用户提出三个问题（仅问缺失的部分）：

1. 被排序的条目是什么？（帖子、商品、任务、告警、文档……）
2. 输入上下文是什么？（用户 ID、搜索查询、当前文档、时间窗口……）
3. 使用什么语言/运行时？（TypeScript/Node、Go、Python、Rust……）

### 步骤 2：走完规格的八个步骤

完整的 SKILL 会引导完成：澄清用例 → 识别候选源 → 列出所需填充 → 列出过滤器 → 设计评分器链 → 选择器 → 副作用 → 生成脚手架。每一步都会呈现架构权衡（多行为 vs 单一分数、候选隔离 vs 联合评分、在线 vs 离线批处理），让用户显式决策而非静默使用默认值。

### 步骤 3：输出可运行的脚手架

上游仓库提供了三个可运行的示例脚手架——每个都在其测试套件中全部通过：

- **Strapi v5 插件**（TypeScript，Jest，3/3 通过）— 添加 `GET /api/feed/for-you`，支持多行为评分和作者多样性
- **Zentra 兼容流水线**（Go 泛型，3/3 通过）— 兼容 engine.Module，也可独立使用
- **PMAI 任务优先级排序器**（Python / FastAPI / pytest，3/3 通过）— `GET /tasks/next?user_id=42&limit=10`

当用户的技术栈不匹配时，本技能会按照 `references/interfaces.md` 中的接口定义（TypeScript、Go、Python、Rust）从零生成。

## 示例

### 示例 1：Strapi 内容 Feed

用户："我运行着一个 Strapi v5 实例，有 5 万篇文章。我想要一个根据每个登录用户的阅读历史个性化的 'for you' Feed。"

技能走完 8 个步骤，使用 Strapi 示例作为模板生成 Strapi 插件脚手架。

### 示例 2：RAG 检索重排序器

用户："我的 RAG 从向量数据库返回 Top-50 切片。我想用更昂贵的评分器对它们重排序并返回 Top-5。"

技能识别出这是一个单源流水线搭配评分器链（廉价检索 + 昂贵重排序）。生成 Python 异步流水线。

### 示例 3：通知分级

用户："我们发送了太多通知。我想要一个每日摘要，从最近 24 小时的队列中选出 Top 10。"

技能识别出这是一个离线批处理流水线。生成定时任务脚手架。

## 最佳实践

- ✅ 显式呈现多行为 vs 单一分数的权衡——不要静默使用默认值
- ✅ 按成本排列过滤器（廉价的在前）；通用过滤器在用户特定过滤器之前
- ✅ 将副作用封装在即发即弃模式中（goroutines / 不带 await 的 Promise / asyncio 任务）——绝不阻塞响应
- ✅ 保持评分确定性和可缓存性；将多样性重排序作为单独的阶段
- ✅ 在生成输出时将模式归因为"由 xAI 开源的 For You 算法推广"
- ❌ 不要编造基准测试或延迟数字——说"取决于工作负载，请自行运行"
- ❌ 不要将用户生成的产物命名为"X-like"或使用"For You"品牌——模式是免费的，品牌不是
- ❌ 不要将此与模型架构混淆：本技能是评分器周围的流水线基础设施，不是评分器本身

## 局限性

- 本技能搭建流水线基础设施；不训练 ML 模型——评分函数由用户负责
- 不操作已部署的流水线（无监控、无自动扩缩容决策）
- 不预测流水线性能（取决于数据、硬件、流量）
- 不选择基础设施（向量数据库、缓存、队列）——这些超出范围

## 安全与注意事项

- 生成的脚手架是框架代码，不是应用逻辑——无 shell 命令、无网络请求、无凭证处理
- 生成的参考手册中的过滤器包含资格/付费墙/地域限制检查；本技能建议将这些放在评分之前（这样被拦截的内容永远不会被评分）
- 副作用阶段始终是异步/即发即弃的；本技能在生成的 README 中显式记录了这一点，以防止用户意外用缓存写入或事件发送阻塞响应

## 常见陷阱

- **问题：** 单一分数模型过度拟合到单一指标（点击），在其他指标上退化（长会话、留存）
  **解决方案：** 技能推荐使用可调权重的多行为预测——通过改变权重来改变行为，无需重训练

- **问题：** 联合评分（对整个批次使用 Transformer）不确定且不可缓存
  **解决方案：** 技能默认使用注意力掩码实现候选隔离；仅在有特定理由时（如批次感知的多样性）推荐联合模式

- **问题：** 副作用（缓存写入、曝光事件发送）阻塞响应
  **解决方案：** 技能生成即发即弃模式并记录该约束

## 上游

本技能是上游仓库的轻量适配器。完整的 SKILL.md 内容、5 份参考文档（4 种语言的接口定义、多行为评分、候选隔离、过滤器参考手册、评分器参考手册）以及 3 个带通过测试套件的可运行示例脚手架：

- **仓库：** https://github.com/mturac/recsys-pipeline-architect
- **发布版本：** v0.1.0
- **通过 skills.sh 安装：** `npx skills add mturac/recsys-pipeline-architect`
- **模式来源：** https://github.com/xai-org/x-algorithm （Apache 2.0；本技能为 MIT）
