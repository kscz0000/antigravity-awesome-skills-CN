# GA4 实施参考

Google Analytics 4 的详细实施指南。

## 目录
- 配置（数据流、增强型衡量事件、推荐事件）
- 自定义事件（gtag.js 实施、Google Tag Manager）
- 转化设置（创建转化、转化价值）
- 自定义维度和指标（使用场景、配置步骤、示例）
- 受众（创建受众、受众示例）
- 调试（DebugView、实时报告、常见问题）
- 数据质量（过滤器、跨域跟踪、会话设置）
- 与 Google Ads 的集成（关联、受众导出）

## 配置

### 数据流

- 每个平台对应一个数据流（Web、iOS、Android）
- 启用增强型衡量以自动跟踪
- 配置数据保留（默认 2 个月，最长 14 个月）
- 启用 Google 信号（如已获得同意，可用于跨设备跟踪）

### 增强型衡量事件（自动）

| 事件 | 描述 | 配置 |
|------|------|------|
| page_view | 页面加载 | 自动 |
| scroll | 滚动深度 90% | 可开关 |
| outbound_click | 点击外部域名 | 自动 |
| site_search | 使用搜索查询 | 配置参数 |
| video_engagement | YouTube 视频播放 | 可开关 |
| file_download | PDF、文档等 | 可配置扩展名 |

### 推荐事件

优先使用 Google 预定义事件以获得更丰富的报告：

**所有属性通用：**
- login, sign_up
- share
- search

**电商：**
- view_item, view_item_list
- add_to_cart, remove_from_cart
- begin_checkout
- add_payment_info
- purchase, refund

**游戏：**
- level_up, unlock_achievement
- post_score, spend_virtual_currency

参考：https://support.google.com/analytics/answer/9267735

---

## 自定义事件

### gtag.js 实施

```javascript
// 基本事件
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});

// 带 value 的事件
gtag('event', 'purchase', {
  'transaction_id': 'T12345',
  'value': 99.99,
  'currency': 'USD',
  'items': [{
    'item_id': 'SKU123',
    'item_name': 'Product Name',
    'price': 99.99
  }]
});

// 用户属性
gtag('set', 'user_properties', {
  'user_type': 'premium',
  'plan_name': 'pro'
});

// User ID（用于已登录用户）
gtag('config', 'GA_MEASUREMENT_ID', {
  'user_id': 'USER_ID'
});
```

### Google Tag Manager（dataLayer）

```javascript
// 自定义事件
dataLayer.push({
  'event': 'signup_completed',
  'method': 'email',
  'plan': 'free'
});

// 设置用户属性
dataLayer.push({
  'user_id': '12345',
  'user_type': 'premium'
});

// 电商购买
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': 'T12345',
    'value': 99.99,
    'currency': 'USD',
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Product Name',
      'price': 99.99,
      'quantity': 1
    }]
  }
});

// 发送前清空 ecommerce（最佳实践）
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'view_item',
  'ecommerce': {
    // ...
  }
});
```

---

## 转化设置

### 创建转化

1. **采集事件** — 确保事件已在 GA4 中触发
2. **标记为转化** — 管理 > 事件 > 标记为转化
3. **设置计数方式**：
   - 每个会话一次（线索、注册）
   - 每次事件（购买）
4. **导入 Google Ads** — 用于出价优化

### 转化价值

```javascript
// 带转化价值的事件
gtag('event', 'purchase', {
  'value': 99.99,
  'currency': 'USD'
});
```

也可以在 GA4 管理后台标记转化时设置默认值。

---

## 自定义维度和指标

### 何时使用

**自定义维度：**
- 需要用于细分或筛选的属性
- 用户属性（套餐类型、行业）
- 内容属性（作者、分类）

**自定义指标：**
- 用于聚合的数值
- 分数、计数、时长

### 配置步骤

1. 管理 > 数据展示 > 自定义定义
2. 创建维度或指标
3. 选择作用域：
   - **事件**：按事件（content_type）
   - **用户**：按用户（account_type）
   - **商品**：按商品（product_category）
4. 输入参数名（必须与事件参数一致）

### 示例

| 维度 | 作用域 | 参数 | 描述 |
|------|--------|------|------|
| User Type | 用户 | user_type | 免费、试用、付费 |
| Content Author | 事件 | author | 博客文章作者 |
| Product Category | 商品 | item_category | 电商分类 |

---

## 受众

### 创建受众

管理 > 数据展示 > 受众

**使用场景：**
- 再营销受众（导出至广告平台）
- 细分分析
- 基于触发的事件

### 受众示例

**高意向访客：**
- 浏览过定价页
- 未完成转化
- 最近 7 天内

**高互动用户：**
- 3 次以上会话
- 或累计互动时长超过 5 分钟

**购买者：**
- 购买事件
- 用于排除或相似受众

---

## 调试

### DebugView

通过以下方式启用：
- URL 参数：`?debug_mode=true`
- Chrome 扩展：GA Debugger
- gtag：在 config 中添加 `'debug_mode': true`

查看位置：报告 > 配置 > DebugView

### 实时报告

查看 30 分钟内的事件：
报告 > 实时

### 常见问题

**事件未出现：**
- 首先检查 DebugView
- 验证 gtag/GTM 是否触发
- 检查过滤器排除项

**参数值缺失：**
- 自定义维度未创建
- 参数名称不匹配
- 数据仍在处理（24-48 小时）

**转化未记录：**
- 事件未标记为转化
- 事件名称不匹配
- 计数方式（每次会话一次 vs 每次事件）

---

## 数据质量

### 过滤器

管理 > 数据流 > [数据流] > 配置标签设置 > 定义内部流量

**排除：**
- 内部 IP 地址
- 开发人员流量
- 测试环境

### 跨域跟踪

针对共享分析的多个域名：

1. 管理 > 数据流 > [数据流] > 配置标签设置
2. 配置你的域名
3. 列出所有应共享会话的域名

### 会话设置

管理 > 数据流 > [数据流] > 配置标签设置

- 会话超时（默认 30 分钟）
- 互动会话时长（默认 10 秒）

---

## 与 Google Ads 的集成

### 关联

1. 管理 > 产品关联 > Google Ads 关联
2. 在 Google Ads 中启用自动标记
3. 在 Google Ads 中导入转化

### 受众导出

在 GA4 中创建的受众可用于 Google Ads 的以下场景：
- 再营销活动
- 客户匹配
- 相似受众