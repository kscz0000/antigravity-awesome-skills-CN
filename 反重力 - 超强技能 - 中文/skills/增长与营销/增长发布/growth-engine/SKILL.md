---
name: growth-engine
description: "数字产品增长引擎——growth hacking、SEO、ASO、病毒式传播、邮件营销、CRM、推荐计划和自然获客。适用于增长策略、SEO优化、ASO优化、病毒传播、邮件营销、推荐计划、自然增长等场景。"
risk: none
source: community
date_added: '2026-03-06'
author: renat
tags:
- growth
- seo
- marketing
- viral
- acquisition
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# GROWTH-ENGINE -- 指数级增长

## 概述

数字产品增长引擎——growth hacking、SEO、ASO、病毒式传播、邮件营销、CRM、推荐计划和自然获客。适用于：制定增长策略、技术 SEO、应用商店 ASO、推荐计划、邮件营销、病毒系数、获客漏斗、自然增长内容、发布活动。

## 适用场景

- 需要该领域的专业协助时

## 何时不使用此技能

- 任务与增长引擎无关
- 更简单、更具体的工具可以处理请求
- 用户需要无领域专业知识的通用协助

## 工作原理

> 最好的营销是一个人们喜爱的产品。—— Sam Altman
> 真正的增长始于一个值得推荐的产品。

---

## Auri 的海盗指标（AARRR）

获客：人们如何发现 Auri？
                目标：10,000 访客/月 -> 1,000 注册
                渠道：SEO、Product Hunt、科技网红、PR

    激活：用户何时体验第一个价值？
                目标：60% 在 24 小时内完成首次对话
                指标：首次对话率（FCR）

    留存：人们会回来吗？
                目标：D7 = 30%，D30 = 15%，D90 = 8%
                指标：周活跃对话用户（WAC）

    收入：人们会付费吗？
                目标：8% 试用->Pro 转化
                指标：MRR、ARPU、LTV

    推荐：人们会推荐吗？
                目标：NPS > 50，病毒系数 > 0.3
                指标：人均推荐数、K 因子

---

## Auri 落地页 SEO 清单

<title>Auri -- 真正会思考的语音助手 | Alexa</title>
    <meta name="description" content="Auri 将你的 Alexa 变成搭载 Claude AI 的智能助手。商业分析、战略决策和真实记忆。">

    <meta property="og:title" content="Auri -- Alexa 语音 AI">
    <meta property="og:description" content="首个具备真实推理能力的语音助手。Powered by Claude.">

    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "SoftwareApplication",
      "name": "Auri",
      "operatingSystem": "Amazon Alexa",
      "applicationCategory": "AI Assistant",
      "offers": {"@type": "Offer", "price": "0"},
      "aggregateRating": {"@type": "AggregateRating",
                             "ratingValue": "4.8", "ratingCount": "127"}
    }
    </script>

## Auri 战略关键词

高意图（转化）：
    - "智能 alexa skill"
    - "带 AI 的 alexa 助手"
    - "如何在 alexa 上使用 claude"

    信息类（教育）：
    - "AI 语音助手"
    - "最佳中文 alexa skill"

    长尾（低竞争）：
    - "alexa 回答复杂问题"
    - "商业分析 alexa skill"

---

## Amazon Skill Store 优化

skill_name: "Auri -- 智能语音 AI"
    invocation: "auri"

    short_description: >
      Auri 将你的 Alexa 变成真正智能的助手。
      Powered by Claude AI——会思考、会记忆、与你共同成长。

    long_description: >
      告别浅层回答。Auri 是首个具备真实推理能力的语音助手。

      AURI 能做什么：
      - 分析复杂商业问题
      - 记住之前的对话（真实记忆）
      - 提供专家视角
      - 随时间学习你的偏好

      如何开始：说"Alexa，打开 Auri"即可开始自然对话。

    example_phrases:
      - "Alexa，打开 Auri"
      - "帮我在这两个商业选项中做决定"
      - "帮我分析这个问题"

    keywords: "AI, 人工智能, 智能助手, claude, 商业"

---

## Auri 病毒传播类型

循环 1：有机口碑
    触发：用户与 Auri 进行了令人印象深刻的对话
    行动：向朋友/社交网络推荐
    目标：每用户带来 0.3 个新用户（K=0.3）

    循环 2：洞察分享
    触发：Auri 生成了特别好的洞察
    行动："分享这个洞察"按钮 -> 生成社交媒体帖子
    目标：5% 的对话产生分享

    循环 3：推荐计划
    激励：每邀请一位朋友订阅，获得 1 个月 Pro 会员
    目标：10% 的 Pro 用户至少推荐 1 人

## 病毒系数计算器

def calculate_k_factor(percent_who_invite, invites_per_user, conversion_rate):
        k = percent_who_invite * invites_per_user * conversion_rate
        if k >= 1:
            status = "病毒式增长（每用户带来超过 1 人）"
        elif k >= 0.5:
            status = "良好（加速增长）"
        elif k >= 0.2:
            status = "一般（支撑增长）"
        else:
            status = "较低（缓慢增长）"
        return {"k_factor": round(k, 2), "status": status,
                "interpretation": f"每 100 用户带来 {int(k*100)} 新用户"}

---

## 新手引导序列（7 天）

第 0 天——欢迎（注册后立即发送）
    主题："欢迎来到 Auri。这是开始方式。"
    正文：3 步教程、首次对话链接、使用技巧

    第 1 天——激活（若未进行首次对话）
    主题："你的 Auri 在等你"
    正文：最令人印象深刻的 3 类问题、紧急 CTA

    第 3 天——教育
    主题："本周 100 位 Auri 用户发现了什么"
    正文：真实案例 + 惊人洞察 + 隐藏功能

    第 7 天——升级（若至少使用 3 次）
    主题："你已使用 80% 的免费额度"
    正文：Pro 解锁什么、48 小时特惠、社会证明

    第 14 天——召回（若停止使用）
    主题："想念你，[名字]。发生了什么？"
    正文：真诚询问、轻松回归链接、新功能

---

## 发布策略

发布前 1 周：
    - 邀请有影响力的 hunter 猎杀产品
    - 准备素材：logo、标语、截图、60 秒演示视频
    - 预热：在 X/LinkedIn 发布 Auri 解决的问题
    - 招募 50 位早期用户在发布时点赞

    发布日（午夜 PT）：
    - X 发布：令人印象深刻的演示 + PH 链接
    - 给整个候补名单发邮件："今天我们在 Product Hunt 上！"
    - 在 BR 科技社区 Telegram/Discord 发消息
    - 全天在线回复评论

    定位：标语："真正会思考的 Alexa skill"

---

## 7. 命令

| 命令 | 操作 |
|---------|------|
| /growth-audit | 完整增长审计 |
| /seo-analysis | 落地页 SEO 分析 |
| /aso-optimize | 优化 Alexa skill 元数据 |
| /viral-loop | 设计产品病毒传播循环 |
| /email-sequence | 创建邮件营销序列 |
| /launch-plan | 完整发布计划 |
| /referral-program | 设计推荐计划 |

## 最佳实践

- 提供清晰、具体的项目背景和需求
- 应用到生产代码前审查所有建议
- 结合其他互补技能进行全面分析

## 常见陷阱

- 将此技能用于其专业领域之外的任务
- 不理解具体背景就应用建议
- 未提供足够的项目背景进行准确分析

## 相关技能

- `analytics-product` - 互补技能，增强分析
- `monetization` - 互补技能，增强分析
- `product-design` - 互补技能，增强分析
- `product-inventor` - 互补技能，增强分析

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
