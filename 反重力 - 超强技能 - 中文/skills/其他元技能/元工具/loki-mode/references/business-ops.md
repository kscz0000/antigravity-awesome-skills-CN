# 业务运营参考

业务群体智能体的工作流和流程。

## 营销运营

### 落地页检查清单
```
[ ] 带清晰价值主张的英雄区域
[ ] 问题/解决方案叙述
[ ] 功能亮点（3-5 个关键功能）
[ ] 社会证明（推荐、logo、数据）
[ ] 定价区域（如适用）
[ ] FAQ 区域
[ ] 行动号召（主要和次要）
[ ] 带法律链接的页脚
```

### SEO 优化
```yaml
技术 SEO:
  - meta title: 50-60 字符，包含主关键词
  - meta description: 150-160 字符，有吸引力
  - canonical URL 设置
  - robots.txt 配置
  - sitemap.xml 生成
  - 结构化数据（JSON-LD）
  - Open Graph 标签
  - Twitter Card 标签

性能:
  - Largest Contentful Paint < 2.5s
  - First Input Delay < 100ms
  - Cumulative Layout Shift < 0.1
  - 图片优化（WebP、懒加载）

内容:
  - H1 包含主关键词
  - H2-H6 层级逻辑
  - 内链策略
  - 所有图片 alt 文本
  - 内容长度适合意图
```

### 内容日历模板
```markdown
# [日期] 周

## 周一
- [ ] 博客文章：[标题]
- [ ] 社交：LinkedIn 公告

## 周三  
- [ ] 邮件通讯
- [ ] 社交：Twitter 线程

## 周五
- [ ] 案例研究更新
- [ ] 社交：功能亮点
```

### 邮件序列

**引导序列：**
```
第 0 天：欢迎邮件（即时）
  - 感谢注册
  - 快速入门指南链接
  - 支持联系方式

第 1 天：入门
  - 第一个功能教程
  - 视频演示

第 3 天：价值展示
  - 成功指标
  - 客户故事

第 7 天：回访
  - 使用情况如何？
  - 功能发现

第 14 天：高级功能
  - 高级用户技巧
  - 集成选项
```

**购物车/试用放弃：**
```
第 1 小时：提醒
第 1 天：利益回顾
第 3 天：推荐 + 紧迫感
第 7 天：最后优惠
```

---

## 销售运营

### CRM 管道阶段
```
1. 线索（新联系人）
2. 合格（符合 ICP，有需求）
3. 已安排会议
4. 已完成演示
5. 已发送提案
6. 谈判中
7. 赢单 / 输单
```

### 资格框架（BANT）
```yaml
预算:
  - 分配的预算是多少？
  - 谁控制预算？
  
权限:
  - 谁做最终决定？
  - 还有谁参与？
  
需求:
  - 要解决什么问题？
  - 不解决的后果是什么？
  
时间:
  - 什么时候需要解决方案？
  - 是什么驱动这个时间表？
```

### 外联模板
```markdown
主题：[公司] 的 [具体痛点]

您好 [姓名]，

我注意到 [公司] 正在 [关于他们业务的具体观察]。

许多 [类似角色/公司类型] 都在为 [问题] 烦恼，这导致 [负面结果]。

[产品] 通过 [具体解决方案] 帮助解决，结果是 [带指标的具体收益]。

您愿意进行 15 分钟的通话，看看这是否能帮助 [公司] 吗？

祝好，
[姓名]
```

### 演示脚本结构
```
1. 建立关系（2 分钟）
   - 确认参会者和角色
   - 议程概述

2. 发现（5 分钟）
   - 确认痛点
   - 了解当前流程
   - 成功指标

3. 解决方案（15 分钟）
   - 将功能映射到他们的需求
   - 展示而非讲述
   - 解决具体用例

4. 社会证明（3 分钟）
   - 相关客户故事
   - 指标和结果

5. 定价/下一步（5 分钟）
   - 展示选项
   - 回答异议
   - 定义下一步
```

---

## 财务运营

### 计费设置检查清单（Stripe）
```bash
# 初始化 Stripe
npm install stripe

# 必需配置：
- [ ] 创建产品和价格
- [ ] 启用客户门户
- [ ] 配置 Webhook 端点
- [ ] 税务设置（Stripe Tax 或手动）
- [ ] 自定义发票设置
- [ ] 启用支付方式
- [ ] 欺诈保护规则
```

### 要处理的 Webhook 事件
```javascript
const relevantEvents = [
  'customer.subscription.created',
  'customer.subscription.updated', 
  'customer.subscription.deleted',
  'invoice.paid',
  'invoice.payment_failed',
  'payment_intent.succeeded',
  'payment_intent.payment_failed',
  'customer.updated',
  'charge.refunded'
];
```

### 关键指标仪表盘
```yaml
收入指标:
  - MRR（月度经常性收入）
  - ARR（年度经常性收入）
  - 净收入留存
  - 扩展收入
  - 流失率

客户指标:
  - CAC（客户获取成本）
  - LTV（生命周期价值）
  - LTV:CAC 比率（目标：3:1）
  - 回收期

产品指标:
  - 试用转付费率
  - 激活率
  - 功能采用
  - NPS 分数
```

### 现金流计算
```
月度消耗 = 月度总支出 - 月度收入
现金流（月）= 现金余额 / 月度消耗

健康：> 18 个月
警告：6-12 个月
危险：< 6 个月
```

---

## 法律运营

### 服务条款模板章节
```
1. 条款接受
2. 服务描述
3. 用户账户和注册
4. 用户行为和内容
5. 知识产权
6. 付款条款（如适用）
7. 终止
8. 免责声明和限制
9. 赔偿
10. 争议解决
11. 条款变更
12. 联系信息
```

### 隐私政策要求（GDPR）
```
必需披露：
- [ ] 数据控制者身份
- [ ] 收集的数据类型
- [ ] 处理目的
- [ ] 处理的法律依据
- [ ] 数据保留期限
- [ ] 第三方共享
- [ ] 用户权利（访问、更正、删除）
- [ ] Cookie 使用
- [ ] 国际传输
- [ ] 联系信息
- [ ] DPO 联系方式（如适用）
```

### GDPR 合规检查清单
```
数据收集：
- [ ] 实施同意机制
- [ ] 文档化目的限制
- [ ] 实践数据最小化

用户权利：
- [ ] 访问权（数据导出）
- [ ] 更正权（编辑资料）
- [ ] 删除权（删除账户）
- [ ] 携带权（下载数据）
- [ ] 反对权（营销退出）

技术：
- [ ] 静态加密
- [ ] 传输加密
- [ ] 访问日志
- [ ] 违规通知流程
```

### Cookie 同意实现
```javascript
// Cookie 类别
const cookieCategories = {
  necessary: true,      // 始终启用
  functional: false,    // 用户偏好
  analytics: false,     // 追踪/分析
  marketing: false      // 广告
};

// 必需：在非必要 cookie 前显示横幅
// 必需：允许精细控制
// 必需：易于撤回同意
// 必需：记录同意时间戳
```

---

## 客户支持运营

### 工单优先级矩阵
| 优先级 | 描述 | 响应 SLA | 解决 SLA |
|--------|------|----------|----------|
| P1 - 严重 | 服务宕机、数据丢失 | 15 分钟 | 4 小时 |
| P2 - 高 | 主要功能故障 | 1 小时 | 8 小时 |
| P3 - 中 | 功能受损 | 4 小时 | 24 小时 |
| P4 - 低 | 一般问题 | 24 小时 | 72 小时 |

### 响应模板

**确认：**
```
您好 [姓名]，

感谢您的联系！我已收到您关于 [问题摘要] 的消息。

我正在调查，将在 [SLA 时间] 内回复您。

同时，[如有适用的有用资源或变通方法]。

祝好，
[客服姓名]
```

**解决：**
```
您好 [姓名]，

好消息 - 我已解决 [具体问题] 的问题。

发生的情况：[简要解释]

我的修复方法：[解决方案摘要]

为防止将来发生：[如适用]

如有任何问题请告诉我！

祝好，
[客服姓名]
```

### 知识库结构
```
/help
├── /getting-started
│   ├── quick-start-guide
│   ├── account-setup
│   └── first-steps
├── /features
│   ├── feature-a
│   ├── feature-b
│   └── feature-c
├── /billing
│   ├── plans-and-pricing
│   ├── payment-methods
│   └── invoices
├── /integrations
│   ├── integration-a
│   └── integration-b
├── /troubleshooting
│   ├── common-issues
│   └── error-messages
└── /api
    ├── authentication
    ├── endpoints
    └── examples
```

---

## 分析运营

### 事件追踪计划
```yaml
用户生命周期:
  - user_signed_up:
      properties: [source, referrer, plan]
  - user_activated:
      properties: [activation_method, time_to_activate]
  - user_converted:
      properties: [plan, trial_length, conversion_path]
  - user_churned:
      properties: [reason, lifetime_value, last_active]

核心操作:
  - feature_used:
      properties: [feature_name, context]
  - action_completed:
      properties: [action_type, duration, success]
  - error_encountered:
      properties: [error_type, page, context]

参与度:
  - page_viewed:
      properties: [page_name, referrer, duration]
  - button_clicked:
      properties: [button_name, page, context]
  - search_performed:
      properties: [query, results_count]
```

### A/B 测试框架
```yaml
测试结构:
  name: "首页 CTA 测试"
  hypothesis: "将 CTA 从 '注册' 改为 '免费开始' 将提高转化率"
  primary_metric: signup_rate
  secondary_metrics: [time_on_page, bounce_rate]
  
  variants:
    control:
      description: "原始 '注册' 按钮"
      allocation: 50%
    variant_a:
      description: "'免费开始' 按钮"
      allocation: 50%
  
  sample_size: 1000_per_variant
  duration: 14_days
  significance_level: 0.95

分析:
  - 计算每个变体的转化率
  - 运行卡方检验确定显著性
  - 检查新奇效应
  - 如需要按用户类型分段
  - 文档化学习
```

### 漏斗分析
```
注册漏斗：
  1. 落地页访问    → 100%（基准）
  2. 注册页查看    → 40%（60% 流失）
  3. 表单提交      → 25%（15% 流失）
  4. 邮箱验证      → 20%（5% 流失）
  5. 引导完成      → 12%（8% 流失）
  6. 首次价值操作  → 8%（4% 流失）

优化目标：
  - 最大流失：落地页 → 注册页（改进 CTA、价值主张）
  - 第二大流失：注册页 → 提交（简化表单）
```

### 周度指标报告模板
```markdown
# 周度指标报告：[日期范围]

## 关键指标摘要
| 指标 | 本周 | 上周 | 变化 |
|------|------|------|------|
| 新用户 | X | Y | +Z% |
| 激活用户 | X | Y | +Z% |
| 收入 | $X | $Y | +Z% |
| 流失 | X% | Y% | -Z% |

## 亮点
- [正面趋势 1]
- [正面趋势 2]

## 关注点
- [问题 1 及行动计划]
- [问题 2 及行动计划]

## 运行中的实验
- [测试名称]：[当前结果]

## 下周重点
- [优先级 1]
- [优先级 2]
```

---

## 跨职能工作流

### 功能发布检查清单
```
发布前：
[ ] 功能完成并测试
[ ] 文档更新
[ ] 帮助文章撰写
[ ] 邮件公告草拟
[ ] 社交内容准备
[ ] 销售团队简报
[ ] 支持团队培训
[ ] 分析事件添加
[ ] 功能开关就绪

发布：
[ ] 部署到生产
[ ] 启用功能开关（% 滚动）
[ ] 发送邮件公告
[ ] 发布博客文章
[ ] 社交媒体发布
[ ] 更新变更日志

发布后：
[ ] 监控错误率
[ ] 追踪功能采用
[ ] 收集用户反馈
[ ] 基于数据迭代
```

### 事件沟通模板
```markdown
# [事件类型] - [简要描述]

## 状态：[调查中 | 已识别 | 监控中 | 已解决]

## 时间线
- [HH:MM] 问题报告
- [HH:MM] 团队介入
- [HH:MM] 根因识别
- [HH:MM] 修复部署
- [HH:MM] 监控中

## 影响
- 受影响：[用户百分比、具体功能]
- 持续时间：[X 小时/分钟]

## 根因
[简要解释]

## 解决方案
[修复措施]

## 预防
[什么变更将防止再次发生]

## 下次更新
[下次更新时间或"已解决"]
```
