# 事件库参考

按业务类型和场景分类的待埋点事件清单。

## 目录
- 营销站点事件（导航与互动、CTA 与表单交互、转化事件）
- 产品/应用事件（引导、核心使用、错误与支持）
- 变现事件（定价与结账、订阅管理）
- 电商事件（浏览、购物车、结账、购后）
- B2B / SaaS 专属事件（团队与协作、集成事件、账户事件）
- 事件属性（参数）
- 漏斗事件序列

## 营销站点事件

### 导航与互动

| 事件名 | 描述 | 属性 |
|--------|------|------|
| page_view | 页面加载（增强型） | page_title, page_location, content_group |
| scroll_depth | 用户滚动到阈值 | depth (25, 50, 75, 100) |
| outbound_link_clicked | 点击外部网站 | link_url, link_text |
| internal_link_clicked | 站内点击 | link_url, link_text, location |
| video_played | 视频开始播放 | video_id, video_title, duration |
| video_completed | 视频播放完毕 | video_id, video_title, duration |

### CTA 与表单交互

| 事件名 | 描述 | 属性 |
|--------|------|------|
| cta_clicked | 行动号召按钮被点击 | button_text, cta_location, page |
| form_started | 用户开始填写表单 | form_name, form_location |
| form_field_completed | 字段填写完成 | form_name, field_name |
| form_submitted | 表单成功提交 | form_name, form_location |
| form_error | 表单校验失败 | form_name, error_type |
| resource_downloaded | 资源下载 | resource_name, resource_type |

### 转化事件

| 事件名 | 描述 | 属性 |
|--------|------|------|
| signup_started | 发起注册 | source, page |
| signup_completed | 完成注册 | method, plan, source |
| demo_requested | 提交演示申请 | company_size, industry |
| contact_submitted | 提交联系表单 | inquiry_type |
| newsletter_subscribed | 订阅邮件列表 | source, list_name |
| trial_started | 开始免费试用 | plan, source |

---

## 产品/应用事件

### 引导

| 事件名 | 描述 | 属性 |
|--------|------|------|
| signup_completed | 账户已创建 | method, referral_source |
| onboarding_started | 开始引导流程 | - |
| onboarding_step_completed | 引导步骤完成 | step_number, step_name |
| onboarding_completed | 全部步骤完成 | steps_completed, time_to_complete |
| onboarding_skipped | 用户跳过引导 | step_skipped_at |
| first_key_action_completed | 达成"顿悟时刻" | action_type |

### 核心使用

| 事件名 | 描述 | 属性 |
|--------|------|------|
| session_started | 应用会话开始 | session_number |
| feature_used | 功能交互 | feature_name, feature_category |
| action_completed | 核心动作完成 | action_type, count |
| content_created | 用户创建内容 | content_type |
| content_edited | 用户修改内容 | content_type |
| content_deleted | 用户删除内容 | content_type |
| search_performed | 应用内搜索 | query, results_count |
| settings_changed | 设置已修改 | setting_name, new_value |
| invite_sent | 用户邀请他人 | invite_type, count |

### 错误与支持

| 事件名 | 描述 | 属性 |
|--------|------|------|
| error_occurred | 发生错误 | error_type, error_message, page |
| help_opened | 访问帮助 | help_type, page |
| support_contacted | 提交支持请求 | contact_method, issue_type |
| feedback_submitted | 提交用户反馈 | feedback_type, rating |

---

## 变现事件

### 定价与结账

| 事件名 | 描述 | 属性 |
|--------|------|------|
| pricing_viewed | 浏览定价页面 | source |
| plan_selected | 选定套餐 | plan_name, billing_cycle |
| checkout_started | 开始结账 | plan, value |
| payment_info_entered | 提交支付信息 | payment_method |
| purchase_completed | 购买成功 | plan, value, currency, transaction_id |
| purchase_failed | 购买失败 | error_reason, plan |

### 订阅管理

| 事件名 | 描述 | 属性 |
|--------|------|------|
| trial_started | 试用开始 | plan, trial_length |
| trial_ended | 试用到期 | plan, converted (bool) |
| subscription_upgraded | 套餐升级 | from_plan, to_plan, value |
| subscription_downgraded | 套餐降级 | from_plan, to_plan |
| subscription_cancelled | 已取消订阅 | plan, reason, tenure |
| subscription_renewed | 已续订 | plan, value |
| billing_updated | 支付方式变更 | - |

---

## 电商事件

### 浏览

| 事件名 | 描述 | 属性 |
|--------|------|------|
| product_viewed | 浏览商品页 | product_id, product_name, category, price |
| product_list_viewed | 浏览分类/列表 | list_name, products[] |
| product_searched | 发起搜索 | query, results_count |
| product_filtered | 应用筛选 | filter_type, filter_value |
| product_sorted | 应用排序 | sort_by, sort_order |

### 购物车

| 事件名 | 描述 | 属性 |
|--------|------|------|
| product_added_to_cart | 商品加入购物车 | product_id, product_name, price, quantity |
| product_removed_from_cart | 商品移出购物车 | product_id, product_name, price, quantity |
| cart_viewed | 浏览购物车 | cart_value, items_count |

### 结账

| 事件名 | 描述 | 属性 |
|--------|------|------|
| checkout_started | 开始结账 | cart_value, items_count |
| checkout_step_completed | 结账步骤完成 | step_number, step_name |
| shipping_info_entered | 填写收货地址 | shipping_method |
| payment_info_entered | 填写支付信息 | payment_method |
| coupon_applied | 使用优惠券 | coupon_code, discount_value |
| purchase_completed | 订单已下单 | transaction_id, value, currency, items[] |

### 购后

| 事件名 | 描述 | 属性 |
|--------|------|------|
| order_confirmed | 查看订单确认 | transaction_id |
| refund_requested | 发起退款 | transaction_id, reason |
| refund_completed | 退款处理完成 | transaction_id, value |
| review_submitted | 提交商品评价 | product_id, rating |

---

## B2B / SaaS 专属事件

### 团队与协作

| 事件名 | 描述 | 属性 |
|--------|------|------|
| team_created | 新建团队/组织 | team_size, plan |
| team_member_invited | 发送邀请 | role, invite_method |
| team_member_joined | 成员加入 | role |
| team_member_removed | 移除成员 | role |
| role_changed | 权限更新 | user_id, old_role, new_role |

### 集成事件

| 事件名 | 描述 | 属性 |
|--------|------|------|
| integration_viewed | 浏览集成页 | integration_name |
| integration_started | 开始集成设置 | integration_name |
| integration_connected | 集成连接成功 | integration_name |
| integration_disconnected | 解除集成 | integration_name, reason |

### 账户事件

| 事件名 | 描述 | 属性 |
|--------|------|------|
| account_created | 新建账户 | source, plan |
| account_upgraded | 套餐升级 | from_plan, to_plan |
| account_churned | 账户关闭 | reason, tenure, mrr_lost |
| account_reactivated | 客户回流 | previous_tenure, new_plan |

---

## 事件属性（参数）

### 应包含的标准属性

**用户上下文：**
```
user_id: "12345"
user_type: "free" | "trial" | "paid"
account_id: "acct_123"
plan_type: "starter" | "pro" | "enterprise"
```

**会话上下文：**
```
session_id: "sess_abc"
session_number: 5
page: "/pricing"
referrer: "https://google.com"
```

**营销上下文：**
```
source: "google"
medium: "cpc"
campaign: "spring_sale"
content: "hero_cta"
```

**产品上下文（电商）：**
```
product_id: "SKU123"
product_name: "Product Name"
category: "Category"
price: 99.99
quantity: 1
currency: "USD"
```

**时间：**
```
timestamp: "2024-01-15T10:30:00Z"
time_on_page: 45
session_duration: 300
```

---

## 漏斗事件序列

### 注册漏斗
1. signup_started
2. signup_step_completed (email)
3. signup_step_completed (password)
4. signup_completed
5. onboarding_started

### 购买漏斗
1. pricing_viewed
2. plan_selected
3. checkout_started
4. payment_info_entered
5. purchase_completed

### 电商漏斗
1. product_viewed
2. product_added_to_cart
3. cart_viewed
4. checkout_started
5. shipping_info_entered
6. payment_info_entered
7. purchase_completed