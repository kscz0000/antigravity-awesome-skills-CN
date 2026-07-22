---
name: free-tier-strategy
description: "设计能转化为付费且不引发反感或滥用的免费层级。触发词：free tier design, freemium model, free trial strategy, free tier limits, developer free plan, open source commercial, feature gating, upgrade triggers, free tier conversion"
risk: unknown
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/free-tier-strategy
source_repo: jonathimer/devmarketing-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/jonathimer/devmarketing-skills/blob/main/LICENSE
---

# 免费层级策略
## 适用场景

当你需要设计能让开发者转化为付费用户、且不引发反感或滥用的免费层级时使用此技能。触发词：free tier design, freemium model, free trial strategy, free tier limits, developer free plan, open source commercial, feature gating, upgrade triggers, free tier conversion。


设计让开发者能构建真实产品、展现价值、自然转化的免费层级——既不像陷阱，也不引发反感。

## 概述

开发者工具都需要免费层级。开发者期望先试用再购买，且试用必须有实际意义——不是 14 天倒计时，也不是功能阉割的演示。但免费层级也必须能支撑业务。两个方向都容易出错：限制过严会扼杀采用，过度慷慨又会拖垮收入。

最好的免费层级，对个人开发者慷慨相待，而当项目成长时，又能自然地平滑过渡到付费层级。

## 开始之前

请先回顾 `/devmarketing-skills/skills/developer-audience-context` 技能。免费层级设计因目标用户（爱好者、初创公司还是企业）的不同而差异显著。同时要理解你的单位经济模型——每位免费用户实际让你付出多少成本？

## 免费层级 vs 免费试用 vs Freemium

### 定义

**Free trial（免费试用）：** 限时全功能访问（14 或 30 天）
- 最适合：高接触企业销售
- 最不适合：自助式（self-serve）开发者工具

**Free tier（免费层级）：** 永久免费，但有使用/功能限制
- 最适合：自助式采用的开发者工具
- 需要：精细的限制设计

**Freemium（免费增值）：** 免费层级叠加付费专属的高级功能
- 最适合：能清晰区分个人爱好与专业版用途的工具
- 需要：付费功能必须有显而易见的价值

**Open core（开放核心）：** 开源免费版加上商业附加
- 最适合：基础设施与平台
- 需要：活跃的开源社区

### 选择你的模型

| 因素 | 免费试用 | 免费层级 | Freemium | 开放核心 |
|--------|-----------|-----------|----------|-----------|
| 销售模式 | 高接触 | 自助式 | 自助式 | 混合 |
| 评估时长 | 数周 | 数月 | 数月 | 无限 |
| 转化压力 | 高 | 低 | 中 | 无 |
| 社区建设 | 低 | 中 | 中 | 高 |
| 支持成本 | 高 | 低 | 中 | 可变 |

**开发者工具几乎总是需要永久免费层级，而不是免费试用。** 开发者会做副业项目、评估工具以备未来之用、向他人推荐工具——这些场景都需要长期的免费访问。

## 合理的用量限制

### 良好的限制维度

**API 调用/请求数**
- 开发者容易理解且能跟踪
- 随应用增长自然伸缩
- 示例：每月 10,000 次请求

**计算资源**
- 与成本关系清晰
- 开发者可预测
- 示例：每月 500 build 分钟

**存储**
- 易于理解
- 数据增长时自然触发升级
- 示例：1GB 存储

**席位/用户数**
- 适合协作类工具
- 团队扩张时自然升级
- 示例：最多 3 名团队成员

### 不好的限制维度

**披着免费层级外衣的限时试用**
- "免费层级在 90 天不活跃后失效"
- 制造焦虑与反感

**任意拼凑的功能组合**
- "免费版：3 个项目，每项目 2 个环境，每环境最多 5 个数据库，每个数据库 100MB"
- 过于复杂，难以评估

**惩罚成功的限制**
- "免费版支持最多 100 月活用户"
- 最成功的免费用户反而最快撞到限制

### 恰到好处的区间

免费层级限制应当：
1. **允许有意义的用量** —— 能构建并运行一个真实的副业项目
2. **覆盖爱好者场景** —— 个人项目永远不应被收费
3. **因增长触发，而非时间** —— 升级来自项目的成功
4. **易于预测** —— 开发者应能预知何时会撞到限制

### 示例：良好的限制结构

**Vercel：**
- 不限个人项目数
- 每月 100GB 带宽
- Serverless 函数限制
- 爱好者用途永久免费

**Supabase：**
- 500MB 数据库存储
- 2GB 带宽
- 50,000 月活用户
- 社交登录不限量

**PlanetScale：**
- 1 个数据库
- 每月 10 亿次行读取
- 每月 1,000 万次行写入
- 5GB 存储

## 功能门控策略

### 免费功能的原则

免费层级应包含完成以下任务所需的一切：
1. 充分评估产品
2. 构建并发布真实项目
3. 在小规模生产环境中运行

### 应保持免费的功能

- 核心功能
- 所有集成与 SDK
- 标准身份认证
- 基础监控与日志
- 文档与社区支持
- 开发与测试环境

### 应放在付费层级后的功能

**协作功能：**
- 超出单人开发者的团队成员
- 访问控制与权限
- 审计日志

**规模与性能：**
- 更高的速率限制
- 更多的计算/存储
- 高级基础设施（专用实例）

**企业级要求：**
- SSO/SAML
- SLA 与可用性保证
- 优先支持
- 合规认证
- 定制合同

### 功能门控的反模式

**门控基础开发者需求：**
```
Bad: Custom domains require paid plan
(Custom domains are table stakes)

Bad: CI/CD integration requires paid plan
(This is how developers deploy)

Bad: Environment variables limited on free
(This is basic functionality)
```

**破坏评估的门控：**
```
Bad: "Advanced features" available for 7 days then locked
(Developers can't properly evaluate)

Bad: Production deploys require credit card
(Can't demonstrate to stakeholders)
```

## 避免"免费层级税"带来的反感

### 反感从何而来

1. **隐性降级** —— 免费层级更慢、更不稳定
2. **功能移除** —— 功能从免费移至付费
3. **意外的限制** —— 撞到限制却毫无预警
4. **居高临下的措辞** —— "升级以解锁基础功能"
5. **支持歧视** —— 免费用户被当作二等公民

### 营造积极的免费层级体验

**清晰的预期：**
```
Free tier includes:
- Everything you need to build and launch
- No credit card required
- No time limits

Upgrade when you need:
- Team collaboration
- Higher usage limits
- Priority support
```

**优雅的限制处理：**
```
You've used 8,000 of 10,000 free API calls this month.

Options:
- Wait for reset on March 1st
- Upgrade to Pro ($29/mo) for 100,000 calls
- Request temporary limit increase (for launches)
```

**诚实的功能对比：**
不要人为削弱免费层级以让付费版看起来更好。

### GitHub 模式

GitHub 免费层级的演进示范了如何做好这件事：
1. 私有仓库免费（此前需付费）
2. 公开仓库免费 CI/CD 分钟
3. 为开源维护者提供免费 Copilot
4. 为组织提供慷慨的免费层级

结果：开发者喜爱 GitHub，在需要更多时愉快付费。

## 升级触发点与时机

### 自然的升级触发点

**增长触发点：**
- 撞到用量上限（带宽、存储、API 调用）
- 添加团队成员
- 创建更多项目/环境
- 需要更长的历史/保留期

**成熟触发点：**
- 进入生产环境
- 需要可用性 SLA
- 合规要求
- 想要高级支持

### 触发的沟通方式

**坏：骚扰式**
```
[Popup every login]
Upgrade to Pro! 50% off this week only!
[Dismiss] [Upgrade]
```

**好：场景化**
```
[When approaching limits]
You're at 85% of your free tier API calls.
Your current usage suggests you'll hit the limit in 3 days.

[View usage] [Explore plans]
```

**更好：乐于助人**
```
[When adding 4th team member]
Free tier includes 3 team members.

To add more collaborators, upgrade to Team ($25/user/mo).
This includes: [benefits relevant to teams]

[Not now - stay with 3] [Upgrade to Team]
```

### 时机原则

1. **绝不打断工作流** —— 不要用升级提示阻塞操作
2. **提前预警** —— 70%、85%、95% 三档通知
3. **解释触发原因** —— "你看到这条提示是因为……"
4. **提供替代方案** —— 不只是"升级或受罪"
5. **记住用户选择** —— 不要每天重复已关闭的提示

## 开源 + 商业化模式

### 开放核心模型

```
Open Source (MIT/Apache)          Commercial
─────────────────────────────────────────────────
Self-hosted core                  Cloud hosting
Community support                 Priority support
Standard features                 Enterprise features (SSO, audit)
                                  Compliance and SLAs
```

### 让开放核心跑通

**清晰的边界：**
开发者应能准确知道哪些是开源、哪些是商业。

**好例子（GitLab）：**
- 社区版：完整的 Git 平台
- 企业版：高级安全与合规
- SaaS：托管服务，包含 CE 或 EE 功能

**开源必须真的可用：**
开源版本应当真正有用，而非残缺版本。开发者会察觉并反感"开源洗白"。

### 商业化策略

**云 vs 自托管：**
- 开源：自托管免费
- 商业：托管云服务
- 示例：Plausible、Metabase、Supabase

**企业级功能：**
- 开源：满足个人/小团队完整需求
- 商业：SSO、审计日志、合规
- 示例：GitLab、Sourcegraph

**支持与 SLA：**
- 开源：社区支持
- 商业：优先支持、可用性 SLA
- 示例：大多数开源数据库

### 与社区的关系

**应该做的：**
- 真正为开源做贡献
- 接纳社区贡献
- 对商业决策保持透明
- 为开源项目提供免费商业层级

**不要做的：**
- 突然更换许可证或条款（参见 HashiCorp、Redis、Elastic）
- 将社区共建功能商业化，与社区竞争
- 把开源主要当作营销手段
- 忽视社区对商业边界的反馈

## 定价页的沟通

### 清晰地展示限制

```
Free                    Pro ($29/mo)           Enterprise
─────────────────────────────────────────────────────────
10,000 API calls        100,000 API calls      Unlimited
1GB storage             50GB storage           Unlimited
3 team members          25 team members        Unlimited
Community support       Email support          Priority + SLA
```

### 免费层级 FAQ

每个定价页都需要：
- "免费层级真的永久免费吗？"
- "撞到限制后会发生什么？"
- "免费层级能用于商业项目吗？"
- "免费层级需要信用卡吗？"

### 定价页示例

**优秀：Vercel**
- 清晰的免费层级描述
- 按功能维度对比限制
- 用量计算器
- "Hobby"框架（而非"受限"）

**优秀：Supabase**
- 慷慨的免费层级突出展示
- 清晰的限制数字
- 功能对比表
- 开源状态可见

## 成功案例：做得好的免费层级

### Stripe

- 免费层级无月费
- 仅按交易收费（2.9% + 30¢）
- 测试模式不限量、永久免费
- 完整功能访问
- 为何有效：成本与收入对齐

### Cloudflare

- 慷慨的免费层级（无限带宽）
- 高级功能差异化清晰
- 对大多数网站而言免费层级真的有用
- 为何有效：免费用户变成布道者

### MongoDB Atlas

- 512MB 存储永久免费
- 共享集群（学习够用）
- 所有功能可测试
- 为何有效：开发者在免费版学习，企业付费

### Algolia

- 10,000 条记录免费
- 每月 10,000 次搜索请求
- 完整 API 访问
- 为何有效：随应用成功而伸缩

## 反面案例：失败的免费层级

### 反模式：隐藏的试用

"免费层级"在 90 天不活跃后失效，或在初始期后下调限制。

### 反模式：功能监狱

核心功能被锁在付费后，导致免费层级根本无法用于评估。

### 反模式：支持荒漠

免费用户只能使用 AI 聊天机器人，连 bug 都找不到真人帮忙。

### 反模式：突然拔线

此前免费的功能未给老用户缓冲期就被移到付费墙后。

## 工具

### 用量跟踪与限制

- **Lago** - 开源基于用量的计费
- **Metronome** - 用量计量与计费
- **Orb** - 基于用量的计费平台
- **Stripe Billing** - 按量计费支持

### 用于门控的 Feature Flag

- **LaunchDarkly** - Feature flag 管理
- **Flagsmith** - 开源替代方案
- **PostHog** - 带分析的 Feature flag

### 转化分析

- **Amplitude** - 跟踪免费到付费的转化
- **Mixpanel** - 漏斗分析
- **ProfitWell** - SaaS 指标与定价

## 相关技能

- `/devmarketing-skills/skills/usage-based-pricing` - 开发者工具的定价模型
- `/devmarketing-skills/skills/developer-signup-flow` - 引导开发者进入免费层级
- `/devmarketing-skills/skills/developer-onboarding` - 激活免费层级用户

## 局限

- 仅在任务与上游来源及本地项目上下文明确匹配时使用此技能。
- 在应用变更前，请验证命令、生成的代码、依赖、凭据以及外部服务行为。
- 不要将示例当作环境特定测试、安全审查或对破坏性/高成本操作的用户批准的替代品。