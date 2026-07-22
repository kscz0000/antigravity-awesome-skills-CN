# 主题参考

使用 Liquid 模板开发 Shopify 主题的指南。

## Liquid 模板

### 语法基础

**对象（输出）：**
```liquid
{{ product.title }}
{{ product.price | money }}
{{ customer.email }}
```

**标签（逻辑）：**
```liquid
{% if product.available %}
  <button>Add to Cart</button>
{% else %}
  <p>Sold Out</p>
{% endif %}

{% for product in collection.products %}
  {{ product.title }}
{% endfor %}

{% case product.type %}
  {% when 'Clothing' %}
    <span>Apparel</span>
  {% when 'Shoes' %}
    <span>Footwear</span>
  {% else %}
    <span>Other</span>
{% endcase %}
```

**过滤器（转换）：**
```liquid
{{ product.title | upcase }}
{{ product.price | money }}
{{ product.description | strip_html | truncate: 100 }}
{{ product.image | img_url: 'medium' }}
{{ 'now' | date: '%B %d, %Y' }}
```

### 常用对象

**产品：**
```liquid
{{ product.id }}
{{ product.title }}
{{ product.handle }}
{{ product.description }}
{{ product.price }}
{{ product.compare_at_price }}
{{ product.available }}
{{ product.type }}
{{ product.vendor }}
{{ product.tags }}
{{ product.images }}
{{ product.variants }}
{{ product.featured_image }}
{{ product.url }}
```

**集合：**
```liquid
{{ collection.title }}
{{ collection.handle }}
{{ collection.description }}
{{ collection.products }}
{{ collection.products_count }}
{{ collection.image }}
{{ collection.url }}
```

**购物车：**
```liquid
{{ cart.item_count }}
{{ cart.total_price }}
{{ cart.items }}
{{ cart.note }}
{{ cart.attributes }}
```

**客户：**
```liquid
{{ customer.email }}
{{ customer.first_name }}
{{ customer.last_name }}
{{ customer.orders_count }}
{{ customer.total_spent }}
{{ customer.addresses }}
{{ customer.default_address }}
```

**商店：**
```liquid
{{ shop.name }}
{{ shop.email }}
{{ shop.domain }}
{{ shop.currency }}
{{ shop.money_format }}
{{ shop.enabled_payment_types }}
```

### 常用过滤器

**字符串：**
- `upcase`, `downcase`, `capitalize`
- `strip_html`, `strip_newlines`
- `truncate: 100`, `truncatewords: 20`
- `replace: 'old', 'new'`

**数字：**
- `money` - 格式化货币
- `round`, `ceil`, `floor`
- `times`, `divided_by`, `plus`, `minus`

**数组：**
- `join: ', '`
- `first`, `last`
- `size`
- `map: 'property'`
- `where: 'property', 'value'`

**URL：**
- `img_url: 'size'` - 图片 URL
- `url_for_type`, `url_for_vendor`
- `link_to`, `link_to_type`

**日期：**
- `date: '%B %d, %Y'`

## 主题架构

### 目录结构

```
theme/
├── assets/              # CSS、JS、图片
├── config/              # 主题设置
│   ├── settings_schema.json
│   └── settings_data.json
├── layout/              # 基础模板
│   └── theme.liquid
├── locales/             # 翻译文件
│   └── en.default.json
├── sections/            # 可复用块
│   ├── header.liquid
│   ├── footer.liquid
│   └── product-grid.liquid
├── snippets/            # 小组件
│   ├── product-card.liquid
│   └── icon.liquid
└── templates/           # 页面模板
    ├── index.json
    ├── product.json
    ├── collection.json
    └── cart.liquid
```

### 布局

包裹所有页面的基础模板（`layout/theme.liquid`）：

```liquid
<!DOCTYPE html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ page_title }}</title>

  {{ content_for_header }}

  <link rel="stylesheet" href="{{ 'theme.css' | asset_url }}">
</head>
<body>
  {% section 'header' %}

  <main>
    {{ content_for_layout }}
  </main>

  {% section 'footer' %}

  <script src="{{ 'theme.js' | asset_url }}"></script>
</body>
</html>
```

### 模板

页面特定结构（`templates/product.json`）：

```json
{
  "sections": {
    "main": {
      "type": "product-template",
      "settings": {
        "show_vendor": true,
        "show_quantity_selector": true
      }
    },
    "recommendations": {
      "type": "product-recommendations"
    }
  },
  "order": ["main", "recommendations"]
}
```

旧版格式（`templates/product.liquid`）：
```liquid
<div class="product">
  <div class="product-images">
    <img src="{{ product.featured_image | img_url: 'large' }}" alt="{{ product.title }}">
  </div>

  <div class="product-details">
    <h1>{{ product.title }}</h1>
    <p class="price">{{ product.price | money }}</p>

    {% form 'product', product %}
      <select name="id">
        {% for variant in product.variants %}
          <option value="{{ variant.id }}">{{ variant.title }} - {{ variant.price | money }}</option>
        {% endfor %}
      </select>

      <button type="submit">Add to Cart</button>
    {% endform %}
  </div>
</div>
```

### Sections

可复用的内容块（`sections/product-grid.liquid`）：

```liquid
<div class="product-grid">
  {% for product in section.settings.collection.products %}
    <div class="product-card">
      <a href="{{ product.url }}">
        <img src="{{ product.featured_image | img_url: 'medium' }}" alt="{{ product.title }}">
        <h3>{{ product.title }}</h3>
        <p>{{ product.price | money }}</p>
      </a>
    </div>
  {% endfor %}
</div>

{% schema %}
{
  "name": "Product Grid",
  "settings": [
    {
      "type": "collection",
      "id": "collection",
      "label": "Collection"
    },
    {
      "type": "range",
      "id": "products_per_row",
      "min": 2,
      "max": 5,
      "step": 1,
      "default": 4,
      "label": "Products per row"
    }
  ],
  "presets": [
    {
      "name": "Product Grid"
    }
  ]
}
{% endschema %}
```

### Snippets

小型可复用组件（`snippets/product-card.liquid`）：

```liquid
<div class="product-card">
  <a href="{{ product.url }}">
    {% if product.featured_image %}
      <img src="{{ product.featured_image | img_url: 'medium' }}" alt="{{ product.title }}">
    {% endif %}
    <h3>{{ product.title }}</h3>
    <p class="price">{{ product.price | money }}</p>
    {% if product.compare_at_price > product.price %}
      <p class="sale-price">{{ product.compare_at_price | money }}</p>
    {% endif %}
  </a>
</div>
```

引入 snippet：
```liquid
{% render 'product-card', product: product %}
```

## 开发工作流

### 初始化

```bash
# 初始化新主题
shopify theme init

# 选择 Dawn（参考主题）或空白主题
```

### 本地开发

```bash
# 启动本地服务器
shopify theme dev

# 预览地址 http://localhost:9292
# 修改自动同步到开发主题
```

### 拉取主题

```bash
# 拉取线上主题
shopify theme pull --live

# 拉取指定主题
shopify theme pull --theme=123456789

# 仅拉取模板
shopify theme pull --only=templates
```

### 推送主题

```bash
# 推送到开发主题
shopify theme push --development

# 创建新的未发布主题
shopify theme push --unpublished

# 推送指定文件
shopify theme push --only=sections,snippets
```

### 主题检查

检查主题代码：
```bash
shopify theme check
shopify theme check --auto-correct
```

## 常用模式

### 带变体的产品表单

```liquid
{% form 'product', product %}
  {% unless product.has_only_default_variant %}
    {% for option in product.options_with_values %}
      <div class="product-option">
        <label>{{ option.name }}</label>
        <select name="options[{{ option.name }}]">
          {% for value in option.values %}
            <option value="{{ value }}">{{ value }}</option>
          {% endfor %}
        </select>
      </div>
    {% endfor %}
  {% endunless %}

  <input type="hidden" name="id" value="{{ product.selected_or_first_available_variant.id }}">
  <input type="number" name="quantity" value="1" min="1">

  <button type="submit" {% unless product.available %}disabled{% endunless %}>
    {% if product.available %}Add to Cart{% else %}Sold Out{% endif %}
  </button>
{% endform %}
```

### 分页

```liquid
{% paginate collection.products by 12 %}
  {% for product in collection.products %}
    {% render 'product-card', product: product %}
  {% endfor %}

  {% if paginate.pages > 1 %}
    <div class="pagination">
      {% if paginate.previous %}
        <a href="{{ paginate.previous.url }}">Previous</a>
      {% endif %}

      {% for part in paginate.parts %}
        {% if part.is_link %}
          <a href="{{ part.url }}">{{ part.title }}</a>
        {% else %}
          <span class="current">{{ part.title }}</span>
        {% endif %}
      {% endfor %}

      {% if paginate.next %}
        <a href="{{ paginate.next.url }}">Next</a>
      {% endif %}
    </div>
  {% endif %}
{% endpaginate %}
```

### 购物车 AJAX

```javascript
// 添加到购物车
fetch('/cart/add.js', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    id: variantId,
    quantity: 1
  })
})
.then(res => res.json())
.then(item => console.log('Added:', item));

// 获取购物车
fetch('/cart.js')
  .then(res => res.json())
  .then(cart => console.log('Cart:', cart));

// 更新购物车
fetch('/cart/change.js', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    id: lineItemKey,
    quantity: 2
  })
})
.then(res => res.json());
```

## 主题中的 Metafields

访问自定义数据：

```liquid
{{ product.metafields.custom.care_instructions }}
{{ product.metafields.custom.material.value }}

{% if product.metafields.custom.featured %}
  <span class="badge">Featured</span>
{% endif %}
```

## 最佳实践

**性能：**
- 优化图片（使用合适的尺寸）
- 最小化 Liquid 逻辑复杂度
- 图片使用懒加载
- 延迟加载非关键 JavaScript

**无障碍：**
- 使用语义化 HTML
- 为图片添加 alt 文本
- 支持键盘导航
- 确保足够的颜色对比度

**SEO：**
- 使用描述性页面标题
- 包含 meta 描述
- 使用标题结构化内容
- 实现 schema 标记

**代码质量：**
- 遵循 Shopify 主题指南
- 使用一致的命名规范
- 为复杂逻辑添加注释
- 保持 sections 聚焦且可复用

## 资源

- 主题开发：https://shopify.dev/docs/themes
- Liquid 参考：https://shopify.dev/docs/api/liquid
- Dawn 主题：https://github.com/Shopify/dawn
- Theme Check：https://shopify.dev/docs/themes/tools/theme-check
