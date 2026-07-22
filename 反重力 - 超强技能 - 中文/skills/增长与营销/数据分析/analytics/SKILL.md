---
name: analytics
description: 当用户需要搭建、优化或审计分析埋点与度量时使用本技能。也适用于用户提及"搭建埋点"、"GA4"、"Google Analytics"、"转化跟踪"、"事件跟踪"、"UTM 参数"、"标签管理器"、"GTM"、"分析实施"、"tracking..."等场景时启用。触发词：搭建埋点、GA4、Google Analytics、转化跟踪、事件跟踪、UTM 参数、标签管理器、GTM、分析实施、埋点审计。
risk: unknown
source: https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics
source_repo: coreyhaines31/marketingskills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/coreyhaines31/marketingskills/blob/main/LICENSE
---

# 分析埋点
## 适用场景

当用户需要搭建、优化或审计分析埋点和度量体系时使用本技能。也适用于用户提及"搭建埋点"、"GA4"、"Google Analytics"、"转化跟踪"、"事件跟踪"、"UTM 参数"、"标签管理器"、"GTM"、"分析实施"、"tracking..."等场景时启用。


你是一名分析实施与度量方面的专家。目标是帮助搭建能为营销和产品决策提供可执行洞察的埋点体系。

## 初始评估

**优先查看产品营销上下文：**
如果存在 `.agents/product-marketing.md`（或 `.claude/product-marketing.md`，以及旧版 `product-marketing-context.md`），请在提问之前先阅读其内容。结合已有上下文，仅询问该任务未覆盖或特定的信息。

在实施埋点之前，需先理解：

1. **业务背景** — 这些数据将支撑哪些决策？关键转化动作是什么？
2. **现状** — 已有哪些埋点？当前在使用哪些工具？
3. **技术背景** — 技术栈是什么？是否存在隐私或合规要求？

---

## 核心原则

### 1. 为决策埋点，而非为数据埋点
- 每个事件都应服务于某个决策
- 规避虚荣指标
- 事件质量优于数量

### 2. 从问题出发
- 需要回答哪些问题？
- 基于这些数据会采取哪些行动？
- 反推需要埋点的事件

### 3. 保持命名一致
- 命名规范至关重要
- 在实施前确立模式
- 文档化所有决策

### 4. 维护数据质量
- 验证实施效果
- 持续监控异常
- 干净的数据胜过更多的数据

---

## 埋点计划框架

### 结构

```
事件名 | 分类 | 属性 | 触发条件 | 备注
------ | ---- | ---- | -------- | ----
```

### 事件类型

| 类型 | 示例 |
|------|------|
| 页面浏览 | 自动采集，可附加元数据 |
| 用户行为 | 按钮点击、表单提交、功能使用 |
| 系统事件 | 注册完成、购买、订阅变更 |
| 自定义转化 | 目标达成、漏斗阶段 |

**完整事件清单**：参见 [references/event-library.md](references/event-library.md)

---

## 事件命名规范

### 推荐格式：对象-动作

```
signup_completed
button_clicked
form_submitted
article_read
checkout_payment_completed
```

### 最佳实践
- 全小写并使用下划线
- 命名具体：使用 `cta_hero_clicked` 而非 `button_clicked`
- 将上下文放在属性中，而非事件名里
- 避免空格和特殊字符
- 文档化所有决策

---

## 核心事件

### 营销站点

| 事件 | 属性 |
|------|------|
| cta_clicked | button_text, location |
| form_submitted | form_type |
| signup_completed | method, source |
| demo_requested | - |

### 产品/应用

| 事件 | 属性 |
|------|------|
| onboarding_step_completed | step_number, step_name |
| feature_used | feature_name |
| purchase_completed | plan, value |
| subscription_cancelled | reason |

**按业务类型分类的完整事件库**：参见 [references/event-library.md](references/event-library.md)

---

## 事件属性

### 标准属性

| 分类 | 属性 |
|------|------|
| 页面 | page_title, page_location, page_referrer |
| 用户 | user_id, user_type, account_id, plan_type |
| 营销活动 | source, medium, campaign, content, term |
| 产品 | product_id, product_name, category, price |

### 最佳实践
- 属性命名保持一致
- 包含相关上下文
- 不要与自动采集的属性重复
- 属性中避免 PII

---

## GA4 实施

### 快速搭建

1. 创建 GA4 属性和数据流
2. 部署 gtag.js 或 GTM
3. 启用增强型衡量
4. 配置自定义事件
5. 在管理后台标记为转化

### 自定义事件示例

```javascript
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});
```

**详细 GA4 实施**：参见 [references/ga4-implementation.md](references/ga4-implementation.md)

---

## Google Tag Manager

### 容器结构

| 组件 | 用途 |
|------|------|
| 标签 | 执行代码（GA4、像素） |
| 触发器 | 标签触发时机（页面浏览、点击） |
| 变量 | 动态值（点击文本、数据层） |

### 数据层模式

```javascript
dataLayer.push({
  'event': 'form_submitted',
  'form_name': 'contact',
  'form_location': 'footer'
});
```

**详细 GTM 实施**：参见 [references/gtm-implementation.md](references/gtm-implementation.md)

---

## UTM 参数策略

### 标准参数

| 参数 | 用途 | 示例 |
|------|------|------|
| utm_source | 流量来源 | google, newsletter |
| utm_medium | 营销媒介 | cpc, email, social |
| utm_campaign | 营销活动名称 | spring_sale |
| utm_content | 区分版本 | hero_cta |
| utm_term | 付费搜索关键词 | running+shoes |

### 命名规范
- 全部使用小写
- 下划线或连字符保持一致
- 命名具体而简洁：使用 `blog_footer_cta`，而非 `cta1`
- 将所有 UTM 记录在电子表格中

---

## 调试与验证

### 测试工具

| 工具 | 用途 |
|------|------|
| GA4 DebugView | 实时事件监控 |
| GTM 预览模式 | 发布前测试触发器 |
| 浏览器扩展 | Tag Assistant、dataLayer Inspector |

### 验证清单

- [ ] 事件在正确的触发条件下触发
- [ ] 属性值正确填充
- [ ] 没有重复事件
- [ ] 跨浏览器和移动端正常工作
- [ ] 转化正确记录
- [ ] 没有 PII 泄露

### 常见问题

| 问题 | 检查项 |
|------|--------|
| 事件未触发 | 触发器配置、GTM 加载状态 |
| 值错误 | 变量路径、数据层结构 |
| 事件重复 | 多个容器、触发器重复触发 |

---

## 隐私与合规

### 注意事项
- 欧盟/英国/加州地区需要 Cookie 同意
- 分析属性中禁止 PII
- 数据保留设置
- 用户删除能力

### 实施要点
- 使用同意模式（等待同意后再上报）
- IP 匿名化
- 按需采集
- 与同意管理平台集成

---

## 输出格式

### 埋点计划文档

```markdown
# [站点/产品] 埋点计划

## 概览
- 工具：GA4、GTM
- 最后更新：[日期]

## 事件

| 事件名 | 描述 | 属性 | 触发条件 |
|--------|------|------|----------|
| signup_completed | 用户完成注册 | method, plan | 成功页面 |

## 自定义维度

| 名称 | 作用域 | 参数 |
|------|--------|------|
| user_type | 用户 | user_type |

## 转化

| 转化 | 事件 | 计数方式 |
|------|------|----------|
| 注册 | signup_completed | 每个会话一次 |
```

---

## 任务专属问题

1. 在使用哪些工具（GA4、Mixpanel 等）？
2. 希望跟踪哪些关键行为？
3. 这些数据将支撑哪些决策？
4. 谁负责实施——开发团队还是市场团队？
5. 是否存在隐私/同意相关要求？
6. 当前已埋点哪些事件？

---

## 工具集成

关于实施细节，请参见 [工具注册表](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/REGISTRY.md)。关键分析工具：

| 工具 | 最适合 | MCP | 指南 |
|------|--------|:---:|------|
| **GA4** | Web 分析，Google 生态 | ✓ | [ga4.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/ga4.md) |
| **Mixpanel** | 产品分析，事件跟踪 | - | [mixpanel.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/mixpanel.md) |
| **Amplitude** | 产品分析，群组分析 | - | [amplitude.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/amplitude.md) |
| **PostHog** | 开源分析，会话回放 | - | [posthog.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/posthog.md) |
| **Segment** | 客户数据平台，路由分发 | - | [segment.md](https://github.com/coreyhaines31/marketingskills/tree/main/skills/analytics/../../tools/integrations/segment.md) |

---

## 相关技能

- **ab-testing**：用于实验跟踪
- **seo-audit**：用于自然流量分析
- **cro**：用于转化优化（使用本技能的数据）
- **revops**：用于管线指标、CRM 跟踪和收入归因

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更前，请验证命令、生成代码、依赖项、凭证和外部服务行为。
- 不要将示例视为特定环境测试、安全审查或用户对破坏性/高成本操作授权的替代品。