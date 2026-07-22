# 提取模式参考

常见网页抓取场景的 CSS 选择器、JavaScript 片段和领域专属技巧。

---

## CSS 选择器模式

### 表格

```css
/* 标准 HTML 表格 */
table                               /* 所有表格 */
table.data-table                    /* 基于 class */
table[id*="result"]                 /* ID 包含 "result" */
table thead th                      /* 表头单元格 */
table tbody tr                      /* 数据行 */
table tbody tr td                   /* 数据单元格 */
table tbody tr td:nth-child(2)      /* 特定列（第二列） */

/* 充当表格的网格布局 */
[role="table"]                      /* ARIA 表格角色 */
[role="row"]                        /* ARIA 行 */
[role="gridcell"]                   /* ARIA 网格单元格 */
.table-responsive table             /* Bootstrap 响应式包装 */
```

### 商品列表

```css
/* 电商商品网格 */
.product-card, .product-item, .product-tile
[data-product-id]                   /* 数据属性标记 */
.product-name, .product-title, h2.title
.price, .product-price, [data-price]
.price--sale, .price--original      /* 折扣价与原价 */
.rating, .stars, [data-rating]
.availability, .stock-status
.product-image img, .product-thumb img

/* 常见电商模式 */
.search-results .result-item
.catalog-grid .catalog-item
.listing .listing-item
```

### 搜索结果

```css
/* 通用搜索结果模式 */
.search-result, .result-item, .search-entry
.result-title a, .result-link
.result-snippet, .result-description
.result-url, .result-source
.result-date, .result-timestamp
.pagination a, .page-numbers a, [aria-label="Next"]
```

### 联系 / 目录

```css
/* 人员和联系卡片 */
.team-member, .staff-card, .person, .contact-card
.member-name, .person-name, h3.name
.member-title, .job-title, .role
.member-email a[href^="mailto:"]
.member-phone a[href^="tel:"]
.member-bio, .person-description
.vcard                              /* hCard 微格式 */
```

### FAQ / 手风琴

```css
/* FAQ 和手风琴模式 */
.faq-item, .accordion-item, [itemtype*="FAQPage"] [itemprop="mainEntity"]
.faq-question, .accordion-header, [itemprop="name"], summary
.faq-answer, .accordion-body, .accordion-content, [itemprop="acceptedAnswer"]
details, details > summary          /* 原生 HTML 手风琴 */
[role="tabpanel"]                   /* 基于标签的 FAQ */
```

### 定价表

```css
/* SaaS 定价页模式 */
.pricing-table, .pricing-card, .plan-card, .pricing-tier
.plan-name, .tier-name, .pricing-title
.plan-price, .pricing-amount, .price-value
.plan-period, .billing-cycle        /* 月付/年付 */
.plan-features li, .feature-list li
.plan-cta, .pricing-button
[class*="popular"], [class*="recommended"], [class*="featured"]  /* 高亮套餐 */
```

### 招聘列表

```css
/* 招聘板模式 */
.job-listing, .job-card, .job-posting, [itemtype*="JobPosting"]
.job-title, [itemprop="title"]
.company-name, [itemprop="hiringOrganization"]
.job-location, [itemprop="jobLocation"]
.job-salary, [itemprop="baseSalary"]
.job-type, .employment-type
.job-date, [itemprop="datePosted"]
```

### 活动

```css
/* 活动列表模式 */
.event-card, .event-item, [itemtype*="Event"]
.event-title, [itemprop="name"]
.event-date, [itemprop="startDate"], time[datetime]
.event-location, [itemprop="location"]
.event-description, [itemprop="description"]
.event-speaker, .speaker-name
```

### 导航 / 分页

```css
/* 分页控件 */
.pagination, .pager, nav[aria-label*="pagination"]
.pagination .next, a[rel="next"]
.pagination .prev, a[rel="prev"]
.page-numbers, .page-link
button[data-page], a[data-page]
.load-more, button.show-more
```

### 文章 / 博客

```css
/* 文章内容 */
article, .post, .entry, .article-content
article h1, .post-title, .entry-title
.author, .byline, [rel="author"]
time, .date, .published, .post-date
.post-content, .entry-content, .article-body
.tags a, .categories a, .post-tags a
```

---

## JavaScript 提取片段

### 通用表格提取器

```javascript
function extractTable(selector) {
  const table = document.querySelector(selector || 'table');
  if (!table) return { error: 'No table found' };

  const headers = Array.from(
    table.querySelectorAll('thead th, tr:first-child th, tr:first-child td')
  ).map(el => el.textContent.trim());

  const rows = Array.from(table.querySelectorAll('tbody tr, tr:not(:first-child)'))
    .map(tr => {
      const cells = Array.from(tr.querySelectorAll('td'))
        .map(td => td.textContent.trim());
      return cells.length > 0 ? cells : null;
    })
    .filter(Boolean);

  return { headers, rows, rowCount: rows.length };
}
JSON.stringify(extractTable());
```

### 多表格提取器

```javascript
function extractAllTables() {
  const tables = document.querySelectorAll('table');
  return Array.from(tables).map((table, idx) => {
    const caption = table.querySelector('caption')?.textContent?.trim()
      || table.getAttribute('aria-label') || `Table ${idx + 1}`;
    const headers = Array.from(
      table.querySelectorAll('thead th, tr:first-child th')
    ).map(el => el.textContent.trim());
    const rows = Array.from(table.querySelectorAll('tbody tr'))
      .map(tr => Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim()))
      .filter(r => r.length > 0);
    return { caption, headers, rows, rowCount: rows.length };
  });
}
JSON.stringify(extractAllTables());
```

### 通用列表提取器

```javascript
function extractList(containerSelector, itemSelector, fieldMap) {
  // fieldMap: { fieldName: { selector: 'CSS', attr: 'href'|'src'|null } }
  const container = document.querySelector(containerSelector);
  if (!container) return { error: 'Container not found' };

  const items = Array.from(container.querySelectorAll(itemSelector));
  const data = items.map(item => {
    const record = {};
    for (const [key, config] of Object.entries(fieldMap)) {
      const sel = typeof config === 'string' ? config : config.selector;
      const attr = typeof config === 'object' ? config.attr : null;
      const el = item.querySelector(sel);
      if (!el) { record[key] = null; continue; }
      record[key] = attr ? el.getAttribute(attr) : el.textContent.trim();
    }
    return record;
  });
  return { data, itemCount: data.length };
}

// 使用示例：
JSON.stringify(extractList('.results', '.result-item', {
  title: '.result-title',
  description: '.result-snippet',
  url: { selector: '.result-title a', attr: 'href' },
  date: '.result-date'
}));
```

### JSON-LD 结构化数据提取器

许多页面嵌入了比 DOM 更易解析的结构化数据：

```javascript
function extractJsonLd(targetType) {
  const scripts = document.querySelectorAll('script[type="application/ld+json"]');
  const allData = Array.from(scripts).map(s => {
    try { return JSON.parse(s.textContent); } catch { return null; }
  }).filter(Boolean);

  // 扁平化 @graph 数组
  const flat = allData.flatMap(d => d['@graph'] || [d]);

  if (targetType) {
    return flat.filter(d =>
      d['@type'] === targetType ||
      (Array.isArray(d['@type']) && d['@type'].includes(targetType))
    );
  }
  return flat;
}
// 提取商品：extractJsonLd('Product')
// 提取文章：extractJsonLd('Article')
// 提取全部：extractJsonLd()
JSON.stringify(extractJsonLd());
```

常见 JSON-LD 类型及其有用字段：
- `Product`：name、offers.price、offers.priceCurrency、aggregateRating、brand.name
- `Article`：headline、author.name、datePublished、description、wordCount
- `Organization`：name、address、telephone、email、url
- `BreadcrumbList`：itemListElement[].name（导航路径）
- `FAQPage`：mainEntity[].name（问题）、mainEntity[].acceptedAnswer.text
- `JobPosting`：title、hiringOrganization.name、jobLocation、baseSalary
- `Event`：name、startDate、endDate、location、performer

### OpenGraph / Meta 标签提取器

```javascript
function extractMeta() {
  const meta = {};
  document.querySelectorAll('meta[property^="og:"], meta[name^="twitter:"]')
    .forEach(el => {
      const key = el.getAttribute('property') || el.getAttribute('name');
      meta[key] = el.getAttribute('content');
    });
  meta.title = document.title;
  meta.description = document.querySelector('meta[name="description"]')
    ?.getAttribute('content');
  meta.canonical = document.querySelector('link[rel="canonical"]')
    ?.getAttribute('href');
  return meta;
}
JSON.stringify(extractMeta());
```

### 定价套餐提取器

```javascript
function extractPricingPlans() {
  const cards = document.querySelectorAll(
    '.pricing-card, .plan-card, .pricing-tier, [class*="pricing"] [class*="card"]'
  );
  return Array.from(cards).map(card => ({
    name: card.querySelector('[class*="name"], [class*="title"], h2, h3')
      ?.textContent?.trim() || null,
    price: card.querySelector('[class*="price"], [class*="amount"]')
      ?.textContent?.trim() || null,
    period: card.querySelector('[class*="period"], [class*="billing"]')
      ?.textContent?.trim() || null,
    features: Array.from(card.querySelectorAll('[class*="feature"] li, ul li'))
      .map(li => li.textContent.trim()),
    highlighted: card.matches('[class*="popular"], [class*="recommended"], [class*="featured"]'),
    ctaText: card.querySelector('a, button')?.textContent?.trim() || null,
    ctaUrl: card.querySelector('a')?.href || null,
  }));
}
JSON.stringify(extractPricingPlans());
```

### FAQ 提取器

```javascript
function extractFAQ() {
  // 优先尝试 JSON-LD
  const ldFaq = extractJsonLd('FAQPage');
  if (ldFaq.length > 0 && ldFaq[0].mainEntity) {
    return ldFaq[0].mainEntity.map(q => ({
      question: q.name,
      answer: q.acceptedAnswer?.text || null
    }));
  }

  // 尝试 <details>/<summary> 模式
  const details = document.querySelectorAll('details');
  if (details.length > 0) {
    return Array.from(details).map(d => ({
      question: d.querySelector('summary')?.textContent?.trim() || null,
      answer: Array.from(d.children).filter(c => c.tagName !== 'SUMMARY')
        .map(c => c.textContent.trim()).join(' ')
    }));
  }

  // 尝试手风琴模式
  const items = document.querySelectorAll(
    '.faq-item, .accordion-item, [class*="faq"] [class*="item"]'
  );
  return Array.from(items).map(item => ({
    question: item.querySelector(
      '[class*="question"], [class*="header"], [class*="title"], h3, h4'
    )?.textContent?.trim() || null,
    answer: item.querySelector(
      '[class*="answer"], [class*="body"], [class*="content"], p'
    )?.textContent?.trim() || null
  }));
}
JSON.stringify(extractFAQ());
```

### 链接提取器

```javascript
function extractLinks(scope) {
  const container = scope ? document.querySelector(scope) : document;
  const links = Array.from(container.querySelectorAll('a[href]'))
    .map(a => ({
      text: a.textContent.trim(),
      href: a.href,
      title: a.title || null
    }))
    .filter(l => l.text && l.href && !l.href.startsWith('javascript:'));
  return { links, count: links.length };
}
JSON.stringify(extractLinks());
```

### 图片提取器

```javascript
function extractImages(scope) {
  const container = scope ? document.querySelector(scope) : document;
  const images = Array.from(container.querySelectorAll('img'))
    .map(img => ({
      src: img.src,
      alt: img.alt || null,
      width: img.naturalWidth,
      height: img.naturalHeight
    }))
    .filter(i => i.src && !i.src.includes('data:image/gif'));
  return { images, count: images.length };
}
JSON.stringify(extractImages());
```

### 滚动并收集模式

对于有懒加载内容的页面，将此模式与浏览器自动化配合使用：

```javascript
// 滚动前统计条目
function countItems(selector) {
  return document.querySelectorAll(selector).length;
}
```

然后在流程中：
1. `javascript_tool`：`countItems('.item')` -> 获取初始数量
2. `computer(action="scroll", scroll_direction="down")`
3. `computer(action="wait", duration=2)`
4. `javascript_tool`：`countItems('.item')` -> 获取新数量
5. 如果新数量 > 旧数量，从第 2 步重复
6. 如果 2 次滚动后数量不变，则所有条目已加载
7. 一次性提取所有条目

---

## 领域专属技巧

### 电商网站
- 优先检查 JSON-LD 的 `Product` schema - 通常比 DOM 数据更干净
- 价格可能藏在原价/折扣价元素中
- 库存状态通常编码在 data 属性中（`data-available="true"`）
- 商品变体（尺寸、颜色）可能需要点击交互
- 评价数据经常懒加载 - 先滚动到评价区
- 许多站点在 `/api/products` 有内部 API - 检查 Network 标签页

### 维基百科
- 表格使用 class `.wikitable` - 始终优先使用此选择器
- 信息框使用 class `.infobox`
- 引用位于 `<sup class="reference">` - 排除在文本提取外
- 表格单元格可能包含复杂嵌套 HTML - 使用 `.textContent.trim()`
- 可排序表格的 class 为 `.sortable`，表头有排序按钮

### 新闻网站
- 文章正文通常在 `<article>` 或 `[itemprop="articleBody"]` 中
- 付费墙指示：`.paywall`、`.subscribe-wall`、并以 "Read more" 截断
- 发布日期在 `<time>` 元素或 `[itemprop="datePublished"]` 中
- 作者在 `[itemprop="author"]` 或 `.byline` 中
- JSON-LD 的 `NewsArticle` 通常包含完整元数据

### 政府 / 数据门户
- 经常使用不带 JavaScript 的 HTML 表格
- 可能有 CSV/Excel 的下载链接 - 寻找 `.csv`、`.xlsx` 链接
- 数据字典可能在单独的页面上
- 在页面源码中寻找 API 端点（`/api/`、`.json` 链接）
- CORS 可能会阻止直接 API 访问；改用 Bash curl

### 社交媒体（公开主页）
- 内容几乎总是 JS 渲染 - 使用浏览器自动化
- 速率限制较激进 - 保持请求数量最少
- 无限滚动是常态 - 设置明确的条目上限
- 结构经常变化 - 优先文本提取而非选择器

### SaaS 定价页
- 定价经常动态变化（月付 vs 年付切换）
- 可能需要点击"年付"切换以查看年付价格
- 功能对比表经常使用对勾（Unicode 或 SVG）
- 检查由账期选择器切换的隐藏元素

### 招聘板
- 多数使用 JSON-LD 的 `JobPosting` schema
- 薪资范围经常隐藏在"查看薪资"按钮后
- 地点可能包含远程/混合办公标识
- 过滤器基于 URL 参数 - 对分页很有用

---

## 应避免的反模式

| 反模式                                  | 为何失败                              | 更好的做法                              |
|:------------------------------------------|:----------------------------------------|:------------------------------------------|
| 使用生成哈希的选择器（`.css-1a2b3c`）    | 每次部署都会变化                      | 使用语义化选择器、ARIA 角色、data 属性 |
| 深度嵌套路径（`div > div > div > span`） | 布局变化时容易失效                    | 使用最近的有意义 class 或属性           |
| 对动态列表使用索引选择器（`:nth-child(3)`） | 顺序可能变化                          | 使用基于内容的识别                      |
| 通过内联样式选择                          | 表现而非语义                          | 使用 class、ID 或 data 属性             |
| 对 JS 内容硬编码等待时间                  | 过短或过长                            | 在循环中检查内容是否出现                |
| 对变体页使用单一选择器                    | 不同页面差异                          | 先在多个页面上测试选择器                |

## 健壮的选择器优先级

按以下顺序优先选择（从最稳定到最不稳定）：

1. `[data-testid="..."]`、`[data-id="..."]` - 测试/data 属性
2. `#unique-id` - 唯一 ID
3. `[role="..."]`、`[aria-label="..."]` - ARIA 属性
4. `[itemprop="..."]`、`[itemtype="..."]` - microdata / schema.org
5. `.semantic-class` - 有意义的 class 名
6. `tag.class` - 元素类型 + class
7. 结构选择器 - 最后的手段
