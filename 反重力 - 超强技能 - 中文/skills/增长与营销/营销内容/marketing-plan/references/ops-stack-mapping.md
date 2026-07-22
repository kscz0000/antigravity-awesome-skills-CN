# 营销运营栈 — 按 AARRR 阶段映射的技能与 MCP

本文档将每个营销技能和每个相关的 MCP/API 集成映射到其主要服务的 AARRR 阶段。它是每个计划第 11 节的来源。

> **范围说明。** 以下技能位于本 `marketingskills` 仓库中。少数引用指向相邻 Claude Code 市场中的可选工具（例如 `vercel:agent-browser`、`compound-engineering:diagram-maker`）——如未安装，请替换为等效工具。当计划引用了不可用的技能或工具时，回退到底层策略，并在第 13 节的待定决策中指出。

## 核心论点

小团队 + fCMO + 智能体工具 = 传统 15–20 人营销组织的产出。技能 + MCP 将以前每个渠道需要专职人力的工作流编码化。

计划的第 11 节通过以下方式明确这一论点：
1. 将技能映射到阶段，让创始人看到哪些技能执行哪些工作
2. 将 MCP/API 映射到阶段，让创始人看到工具层
3. 给出一个具体的运营示例，证明该栈可行
4. 展示按融资阶段的能力解锁（pre-seed → seed → Series A）

## 营销技能映射到 AARRR

### 获客（Acquisition）技能

| 技能 | 功能 | 在获客中的主要用途 |
|---|---|---|
| `seo-audit` | 审计网站技术和页面 SEO | 季度站点健康检查 |
| `ai-seo` | 优化内容以适配 AI 搜索引擎 / LLM 引用 | 面向未来的内容策略 |
| `programmatic-seo` | 大规模构建模板驱动的 SEO 页面 | 地点页、对比页、集成页系统 |
| `schema` | 添加结构化数据标记 | 富摘要，AI 引用资格 |
| `content-strategy` | 规划内容主题、支柱和节奏 | 制定编辑日历 |
| `competitors` | 构建 vs 页面和替代方案页面 | 捕获针对竞品的高意图 SERP |
| `ads` | 规划和构建付费广告系列 | Apple Search Ads、Meta、Google、LinkedIn |
| `ad-creative` | 生成广告变体和创意素材 | 跨平台迭代广告创意 |
| `social` | 规划和撰写社交媒体内容 | LinkedIn、Twitter/X、Instagram、TikTok |
| `typefully` | 排期/发布推文、帖子串、LinkedIn 内容 | 创始人主导渠道的节奏运营 |
| `cold-email` | 撰写 B2B 冷启动外联 + 序列 | B2B SaaS / 混合业务的出站外联 |
| `analytics` | 设置追踪、GA4、转化事件 | 漏斗埋点 |
| `free-tools` | 规划工程即营销的免费工具 | 构建生成链接 + 线索的工具 |
| `marketing-website-design` | 有意图地设计营销网站 | 支柱页/落地页设计 |
| `launch` | 规划和执行发布（Product Hunt、GA、功能发布） | GTM 关键时刻 — 策略 + 战术执行 |

### 激活（Activation）技能

| 技能 | 功能 | 在激活中的主要用途 |
|---|---|---|
| `onboarding` | 优化用户引导流程 | 引导流程重建、激活率测试 |
| `signup` | 优化注册/注册流程 | 减少激活顶部的摩擦 |
| `cro` | 优化任何营销页面或表单 | 跨页面、表单、落地页的转化测试 |
| `paywalls` | 优化付费墙和升级页面 | 试用 → 付费转化（也属于 Revenue） |
| `popups` | 优化弹窗、模态框、滑入组件 | 线索捕获 + 激活提示 |
| `copywriting` | 撰写营销文案 | 引导页面、付费墙文案、CTA |
| `copy-editing` | 编辑和改进现有文案 | 发布前的语调/清晰度审查 |
| `copycraft` | 实时文案变体叠加 | 审查期间的实时文案迭代 |
| `website-copy` | 撰写完整网站文案（CF 流程的第 8 阶段） | 综合站点文案生产 |
| `ab-testing` | 规划 A/B 测试 | 引导变体测试的结构 |
| `marketing-psychology` | 将行为科学应用于文案和 CRO | 激活时刻的说服原则 |

### 留存（Retention）技能

| 技能 | 功能 | 在留存中的主要用途 |
|---|---|---|
| `emails` | 设计邮件序列 | Customer.io / Mailchimp / Resend 流程构建 |
| `churn-prevention` | 构建取消流程、挽回优惠、赢回方案 | 降低流失、恢复失败付款 |
| `copywriting` / `copy-editing` | 邮件文案生产 | 生命周期邮件内容 |
| `paywalls` | （交叉）— 留存邮件中的升级提示 | 生命周期内追加销售 |
| `ab-testing` | 测试邮件变体 | 主题行、CTA、时间测试 |

### 推荐（Referral）技能

| 技能 | 功能 | 在推荐中的主要用途 |
|---|---|---|
| `referrals` | 规划和启动推荐 / 联盟 / 大使计划 | 第 7 节的核心技能 |
| `social` | 创建大使可分享的内容 | 话术要点、帖子模板 |
| `copywriting` | 大使 / 联盟邮件文案 | 招募、引导、沟通 |
| `marketing-website-design` | 每位大使的专属落地页 | 归因面 |
| `emails` | 大使生命周期邮件 | 引导、月度摘要、支付通知 |

### 变现（Revenue）技能

| 技能 | 功能 | 在变现中的主要用途 |
|---|---|---|
| `pricing` | 审计和优化定价 | 规划层级结构、年度默认值、价值指标 |
| `paywalls` | 付费墙优化 | 试用 → 付费、免费 → 付费转化 |
| `sales-enablement` | 构建销售演示文稿、一页纸、Demo | B2B 销售支持材料 |
| `revops` | 变现运营、线索生命周期 | 营销 → 销售交接 |
| `ab-testing` | 定价实验 | 测试年度默认、入门定价、层级整合 |

### 横切 / 品牌基础技能

| 技能 | 功能 | 主要用途 |
|---|---|---|
| `product-marketing` | 设置 `.agents/product-marketing.md` 上下文文件（定位、ICP、语调） | 基础性 — 最先运行；计划的每个节都引用此文件 |
| `customer-research` | 进行客户访谈 + 调研 | 第 2 节 + 第 3 节（当前状态） |
| `marketing-psychology` | 应用行为科学 | 横切文案、CRO、付费墙 |
| `marketing-ideas` | 139 个想法库 | 计划第 12 节（想法库） |

## MCP 和 API 映射到 AARRR

### 获客工具

| 工具 | 提供的功能 | 客户端对接检查 |
|---|---|---|
| **Ahrefs API** | SEO 数据：关键词研究、反向链接、竞品分析 | 需要 `.env` 中的 `AHREFS_API_KEY` |
| **DataForSEO API** | SERP 数据、关键词量、竞品 SERP 分析 | 需要 API 密钥 |
| **GA4 MCP** | 按渠道的流量、转化事件、留存曲线 | 通过 GCP 项目 + 服务账号对接 |
| **GitHub MCP** | 仓库工作：营销站点（`site-name-promo` 模式）、内容创作 | 标准 `gh` CLI 认证 + MCP 服务器 |
| **Typefully MCP** | 社交发布（LinkedIn、X、Threads、Bluesky） | Typefully 账号 + API 密钥 |
| **Google Ads MCP** | 广告账号管理、广告系列创建、效果数据拉取 | 预算解锁后对接 |
| **agent-browser** | 浏览器自动化（表单填写、截图、抓取） | CLI 安装：`npm install -g agent-browser` |
| **dev-browser** | 通用浏览器自动化 | MCP 服务器安装 |
| **defuddle** | 从网页提取干净的 Markdown | CLI 安装 |
| **Notion** | 内部知识目录访问 | Notion API 密钥 |
| **Stripe MCP** | LTV 计算、付费 CAC 核对（横切到 Revenue） | Stripe 账号 + 受限密钥 |

### 激活工具

| 工具 | 提供的功能 |
|---|---|
| **App Store Connect** | 按列表变体的转化率、安装漏斗 | 通常手动 + `dev-browser` 截图 |
| **GitHub MCP** | 移动应用仓库用于引导代码编辑 |
| **Figma / Pencil MCP** | 引导页面设计 + 迭代 |
| **Customer.io MCP** | 应用内消息 + 生命周期邮件协调 |
| **Stripe MCP** | 付费墙逻辑的订阅状态 |
| **GA4 MCP** | 激活事件埋点 |

### 留存工具

| 工具 | 提供的功能 |
|---|---|
| **Customer.io MCP** | 留存基础设施 — 流程构建、分群、发送 |
| **Shopify** | 硬件购买者事件作为生命周期触发器 |
| **Stripe MCP** | 订阅状态、流失群组、计划变更 |
| **GA4 MCP** | 会话事件、留存曲线 |
| **Resend / Mailchimp / SendGrid** | 不同技术栈中 Customer.io 的替代方案 |

### 推荐工具

| 工具 | 提供的功能 |
|---|---|
| **Dub.co** | 大使归因、短链接、每位大使的追踪 |
| **Stripe MCP** | 佣金核算 + 通过 Connect 支付 |
| **GitHub MCP** | 每位大使的专属落地页 |
| **Customer.io MCP** | 大使生命周期（招募 → 引导 → 月度摘要 → 支付通知） |
| **Rewardful / Tolt / Mention Me** | Dub 的联盟管理替代方案 |

### 变现工具

| 工具 | 提供的功能 |
|---|---|
| **Stripe MCP** | 定价测试、订阅分析、流失群组分析、综合 CAC 计算 |
| **Shopify** | 硬件交易 |
| **GA4 MCP** | 变现事件 |
| **Customer.io MCP** | 付费墙 / 定价相关的生命周期 |
| **Notion** | 商业知识目录 |

### 横切工具

| 工具 | 提供的功能 |
|---|---|
| **Notion** | 共享知识库 |
| **GitHub MCP** | 共享上下文仓库（`{client-org}/{client-context}`） |
| **defuddle** | 研究提取 |
| **obsidian-cli** | fCMO 的工作笔记 |
| **Pencil MCP** | 设计文件 |
| **Figma MCP** | 设计文件（如果使用 Figma） |

## 按融资阶段的能力解锁

计划的第 11 节必须包含此表（或等效内容），针对客户当前和预期的融资阶段。

| 阶段 | 人力 | 工具 | 活跃渠道 |
|---|---|---|---|
| **Pre-seed / 自举** | fCMO + 创始人团队 | 所有当前工具 + marketing-skills 库 + MCP 层 | 仅有机（SEO、内容、App Store、创始人主导社交、活动、口碑、大使） |
| **Seed 关账** | + 首位营销招聘（生命周期/内容负责人） | + 付费广告账号（Apple Search Ads、Meta、LinkedIn）+ `ads` 技能激活 | + 付费获客试点（$5–15K/月 — 参见 `funding-stage-unlocks.md` 的标准层级） |
| **Seed 部署** | + 设计师（可能是兼职） | + 分析扩展（如需要，Mixpanel / Amplitude） | + 付费扩展（$20–50K/月）+ 首次发布（PH、GA） |
| **Series A** | + 效果营销负责人 + 内容负责人 | + 专用工具支出（$2–5K/月软件）+ 赞助活动预算 | + 付费扩展（$50–150K/月）+ 国际化考量 + B2B 垂直扩展 |
| **Series B+** | 全栈营销组织（10+ 人） | + 机构合作 + PR 公司 | + 品牌广告 + 收购 + 品类级赞助 |

## 具体示例测试

计划的第 11 节必须包含至少一个具体的运营示例，证明栈论点。示例应该是：
- 一个具体事件（而非抽象声明）
- 尽可能来自该客户的真实历史（最有说服力）
- 由非技术人员通过该栈执行（证明无需专职工程即可运作）

来自真实项目的示例：
- *"在启动会上，Alex 使用 Customer.io 的 Claude MCP 现场起草了一个可用的 Customer.io 购物车放弃流程。验证了非技术创始人可以独立使用技能模式交付生命周期工作。"*
- *"两周内，团队使用 `programmatic-seo` 对接 Ahrefs API + GitHub MCP，将排名关键词从 0 扩展到 14 个 — 无需专职 SEO 招聘。"*
- *"首个邮件营销系列在 `cold-email` 技能 + GA4 MCP + Stripe MCP 为团队提供高 LTV 但近期无活跃的验证目标用户列表后，产生了 24% 的回复率。"*

如果客户历史上还没有这样的时刻，将示例构建为*第一步行动* — "以下是团队将在第一周运行的验证栈的演示："

## 当栈尚未适用时

对于未设置 MCP 连接的客户，第 11 节应采用不同的表述方式：
- 列出在当前工具下确实适用的技能
- 指出哪些 MCP 会解锁计划的哪些部分
- 将 MCP 设置作为 Q1 优先事项，与基础修复并行

如果栈未对接，计划不能声称智能体栈论点。对现状保持诚实。
