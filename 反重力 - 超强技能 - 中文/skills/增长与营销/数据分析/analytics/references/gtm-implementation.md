# Google Tag Manager 实施参考

通过 Google Tag Manager 实施埋点的详细指南。

## 目录
- 容器结构（标签、触发器、变量）
- 命名规范
- 数据层模式
- 常用标签配置（GA4 配置标签、GA4 事件标签、Facebook 像素）
- 预览与调试
- 工作区与版本管理
- 同意管理
- 高级模式（标签排序、异常处理、自定义 JavaScript 变量）

## 容器结构

### 标签

标签是被触发时执行的代码片段。

**常见标签类型：**
- GA4 Configuration（基础设置）
- GA4 Event（自定义事件）
- Google Ads Conversion
- Facebook Pixel
- LinkedIn Insight Tag
- Custom HTML（用于其他像素）

### 触发器

触发器定义标签何时触发。

**内置触发器：**
- 页面浏览：所有页面、DOM 就绪、Window Loaded
- 点击：所有元素、仅链接
- 表单提交
- 滚动深度
- 计时器
- 元素可见性

**自定义触发器：**
- 自定义事件（来自 dataLayer）
- 触发器组（多个条件）

### 变量

变量用于捕获动态值。

**内置（按需启用）：**
- Click Text、Click URL、Click ID、Click Classes
- Page Path、Page URL、Page Hostname
- Referrer
- Form Element、Form ID

**用户自定义：**
- 数据层变量
- JavaScript 变量
- 查找表
- RegEx 表
- 常量

---

## 命名规范

### 推荐格式

```
[类型] - [描述] - [细节]

标签：
GA4 - Event - Signup Completed
GA4 - Config - Base Configuration
FB - Pixel - Page View
HTML - LiveChat Widget

触发器：
Click - CTA Button
Submit - Contact Form
View - Pricing Page
Custom - signup_completed

变量：
DL - user_id
JS - Current Timestamp
LT - Campaign Source Map
```

---

## 数据层模式

### 基础结构

```javascript
// 初始化（在 GTM 之前的 <head> 中）
window.dataLayer = window.dataLayer || [];

// 推送事件
dataLayer.push({
  'event': 'event_name',
  'property1': 'value1',
  'property2': 'value2'
});
```

### 页面加载数据

```javascript
// 在页面加载时设置（在 GTM 容器之前）
window.dataLayer = window.dataLayer || [];
dataLayer.push({
  'pageType': 'product',
  'contentGroup': 'products',
  'user': {
    'loggedIn': true,
    'userId': '12345',
    'userType': 'premium'
  }
});
```

### 表单提交

```javascript
document.querySelector('#contact-form').addEventListener('submit', function() {
  dataLayer.push({
    'event': 'form_submitted',
    'formName': 'contact',
    'formLocation': 'footer'
  });
});
```

### 按钮点击

```javascript
document.querySelector('.cta-button').addEventListener('click', function() {
  dataLayer.push({
    'event': 'cta_clicked',
    'ctaText': this.innerText,
    'ctaLocation': 'hero'
  });
});
```

### 电商事件

```javascript
// 浏览商品
dataLayer.push({ ecommerce: null }); // 清空之前的数据
dataLayer.push({
  'event': 'view_item',
  'ecommerce': {
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Product Name',
      'price': 99.99,
      'item_category': 'Category',
      'quantity': 1
    }]
  }
});

// 加入购物车
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'add_to_cart',
  'ecommerce': {
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Product Name',
      'price': 99.99,
      'quantity': 1
    }]
  }
});

// 购买
dataLayer.push({ ecommerce: null });
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': 'T12345',
    'value': 99.99,
    'currency': 'USD',
    'tax': 5.00,
    'shipping': 10.00,
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Product Name',
      'price': 99.99,
      'quantity': 1
    }]
  }
});
```

---

## 常用标签配置

### GA4 配置标签

**标签类型：** Google Analytics: GA4 Configuration

**设置：**
- Measurement ID：G-XXXXXXXX
- Send page view：勾选（用于页面浏览）
- User Properties：添加任何用户级维度

**触发器：** 所有页面

### GA4 事件标签

**标签类型：** Google Analytics: GA4 Event

**设置：**
- Configuration Tag：选择你的配置标签
- Event Name：`{{DL - event_name}}` 或写死
- Event Parameters：从 dataLayer 添加参数

**触发器：** 事件名匹配的自定义事件

### Facebook Pixel - 基础

**标签类型：** Custom HTML

```html
<script>
  !function(f,b,e,v,n,t,s)
  {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', 'YOUR_PIXEL_ID');
  fbq('track', 'PageView');
</script>
```

**触发器：** 所有页面

### Facebook Pixel - 事件

**标签类型：** Custom HTML

```html
<script>
  fbq('track', 'Lead', {
    content_name: '{{DL - form_name}}'
  });
</script>
```

**触发器：** Custom Event - form_submitted

---

## 预览与调试

### 预览模式

1. 在 GTM 中点击"Preview"
2. 输入站点 URL
3. GTM 调试面板将在底部打开

**检查项：**
- 此事件触发了哪些标签
- 未触发的标签（以及原因）
- 变量及其值
- 数据层内容

### 调试技巧

**标签未触发：**
- 检查触发器条件
- 验证 dataLayer 推送
- 检查标签顺序

**变量值错误：**
- 检查数据层结构
- 验证变量路径（嵌套对象）
- 检查时机（数据可能尚未存在）

**多次触发：**
- 检查触发器唯一性
- 查看是否存在重复标签
- 检查标签触发选项

---

## 工作区与版本管理

### 工作区

使用工作区进行团队协作：
- 默认工作区用于生产环境
- 大改动使用单独的工作区
- 准备就绪后合并

### 版本管理

**最佳实践：**
- 为每个版本起一个描述性名称
- 添加说明备注
- 发布前审查变更
- 标注生产环境版本

**版本备注示例：**
```
v15: 新增购买转化跟踪
- 新标签：GA4 - Event - Purchase
- 新触发器：Custom Event - purchase
- 新变量：DL - transaction_id、DL - value
- 已测试：Chrome、Safari、移动端
```

---

## 同意管理

### 同意模式集成

```javascript
// 默认状态（同意之前）
gtag('consent', 'default', {
  'analytics_storage': 'denied',
  'ad_storage': 'denied'
});

// 同意后更新
function grantConsent() {
  gtag('consent', 'update', {
    'analytics_storage': 'granted',
    'ad_storage': 'granted'
  });
}
```

### GTM 同意概览

1. 在管理中启用 Consent Overview
2. 为每个标签配置同意状态
3. 标签将自动遵守同意状态

---

## 高级模式

### 标签排序

**按顺序触发的标签设置：**
标签配置 > 高级设置 > 标签排序

**使用场景：**
- 配置标签先于事件标签
- 像素先初始化再跟踪
- 转化后清理

### 异常处理

**触发器例外** — 阻止标签触发：
- 排除特定页面
- 排除内部流量
- 测试期间排除

### 自定义 JavaScript 变量

```javascript
// 获取 URL 参数
function() {
  var params = new URLSearchParams(window.location.search);
  return params.get('campaign') || '(not set)';
}

// 获取 Cookie 值
function() {
  var match = document.cookie.match('(^|;) ?user_id=([^;]*)(;|$)');
  return match ? match[2] : null;
}

// 从页面获取数据
function() {
  var el = document.querySelector('.product-price');
  return el ? parseFloat(el.textContent.replace('$', '')) : 0;
}
```