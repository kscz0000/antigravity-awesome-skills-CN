---
name: apify-ecommerce
description: "使用 Apify 电商抓取工具从任意电商平台提取产品数据、价格、评论和卖家信息。触发词：电商数据抓取、产品价格监控、评论分析、卖家情报、竞品分析、MAP合规检测、电商爬虫、商品数据提取、价格追踪、评论采集"
risk: unknown
source: community
---

# 电商数据提取

使用 Apify 电商抓取工具从任意电商平台提取产品数据、价格、评论和卖家信息。

## 何时使用

- 需要从电商网站获取产品、定价、评论、库存或卖家数据
- 任务涉及价格监控、竞品对比、MAP 合规检测或评论分析
- 需要引导式工作流来提取市场数据并汇总发现

## 前置条件

- `.env` 文件中配置 `APIFY_TOKEN`（位于 `~/.claude/.env`）
- Node.js 20.6+（支持原生 `--env-file`）

## 工作流选择

| 用户需求 | 工作流 | 适用场景 |
|----------|--------|----------|
| 追踪价格、对比产品 | 工作流 1：产品与定价 | 价格监控、MAP 合规、竞品分析。添加 AI 摘要获取洞察 |
| 分析评论（情感或质量） | 工作流 2：评论 | 品牌口碑、客户情感、质量问题、缺陷模式 |
| 跨店铺查找卖家 | 工作流 3：卖家 | 未授权经销商、通过 Google Shopping 发现供应商 |

## 进度追踪

```
任务进度：
- [ ] 步骤 1：选择工作流并确定数据源
- [ ] 步骤 2：配置 Actor 输入参数
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行提取脚本
- [ ] 步骤 5：汇总结果
```

---

## 工作流 1：产品与定价

**用例：** 提取产品数据、价格和库存状态。追踪竞品价格、检测 MAP 违规、产品对标或市场研究。

**适用人群：** 定价分析师、产品经理、市场研究员。

### 输入选项

| 输入类型 | 字段 | 描述 |
|----------|------|------|
| 产品 URL | `detailsUrls` | 产品页面的直接 URL（使用对象格式） |
| 分类 URL | `listingUrls` | 分类/搜索结果页面的 URL |
| 关键词搜索 | `keyword` + `marketplaces` | 在选定市场中搜索关键词 |

### 示例 - 产品 URL

```json
{
  "detailsUrls": [
    {"url": "https://www.amazon.com/dp/B09V3KXJPB"},
    {"url": "https://www.walmart.com/ip/123456789"}
  ],
  "additionalProperties": true
}
```

### 示例 - 关键词搜索

```json
{
  "keyword": "Samsung Galaxy S24",
  "marketplaces": ["www.amazon.com", "www.walmart.com"],
  "additionalProperties": true,
  "maxProductResults": 50
}
```

### 可选：AI 摘要

添加以下字段获取 AI 生成的洞察：

| 字段 | 描述 |
|------|------|
| `fieldsToAnalyze` | 要分析的数据点：`["name", "offers", "brand", "description"]` |
| `customPrompt` | 自定义分析指令 |

**带 AI 摘要的示例：**

```json
{
  "keyword": "robot vacuum",
  "marketplaces": ["www.amazon.com"],
  "maxProductResults": 50,
  "additionalProperties": true,
  "fieldsToAnalyze": ["name", "offers", "brand"],
  "customPrompt": "Summarize price range and identify top brands"
}
```

### 输出字段

- `name` - 产品名称
- `url` - 产品 URL
- `offers.price` - 当前价格
- `offers.priceCurrency` - 货币代码（可能因卖家地区而异）
- `brand.slogan` - 品牌名称（嵌套在对象中）
- `image` - 产品图片 URL
- 当 `additionalProperties: true` 时提供额外的卖家/库存信息

> **注意：** 即使是美国搜索，结果中的货币也可能不同，因为价格反映不同卖家地区。

---

## 工作流 2：客户评论

**用例：** 提取评论用于情感分析、品牌口碑监控或质量问题检测。

**适用人群：** 品牌经理、客户体验团队、QA 团队、产品经理。

### 输入选项

| 输入类型 | 字段 | 描述 |
|----------|------|------|
| 产品 URL | `reviewListingUrls` | 要提取评论的产品页面 |
| 关键词搜索 | `keywordReviews` + `marketplacesReviews` | 按关键词搜索产品评论 |

### 示例 - 从产品提取评论

```json
{
  "reviewListingUrls": [
    {"url": "https://www.amazon.com/dp/B09V3KXJPB"}
  ],
  "sortReview": "Most recent",
  "additionalReviewProperties": true,
  "maxReviewResults": 500
}
```

### 示例 - 关键词搜索

```json
{
  "keywordReviews": "wireless earbuds",
  "marketplacesReviews": ["www.amazon.com"],
  "sortReview": "Most recent",
  "additionalReviewProperties": true,
  "maxReviewResults": 200
}
```

### 排序选项

- `Most recent` - 最新评论优先（推荐）
- `Most relevant` - 平台默认相关性
- `Most helpful` - 得票最高的评论
- `Highest rated` - 5 星评论优先
- `Lowest rated` - 1 星评论优先

> **注意：** `sortReview: "Lowest rated"` 选项在所有市场可能不一致。对于质量分析，建议收集大样本并在后处理中按评分过滤。

### 质量分析技巧

- 设置较高的 `maxReviewResults` 以获得统计显著性
- 查找重复关键词："broke"、"defect"、"quality"、"returned"
- 如果排序不如预期，可按评分过滤结果
- 与竞品交叉对比进行对标

---

## 工作流 3：卖家情报

**用例：** 跨店铺查找卖家、发现未授权经销商、评估供应商选项。

**适用人群：** 品牌保护团队、采购、供应链经理。

> **注意：** 此工作流使用 Google Shopping 跨店铺查找卖家。不直接支持卖家档案 URL。

### 输入配置

```json
{
  "googleShoppingSearchKeyword": "Nike Air Max 90",
  "scrapeSellersFromGoogleShopping": true,
  "countryCode": "us",
  "maxGoogleShoppingSellersPerProduct": 20,
  "maxGoogleShoppingResults": 100
}
```

### 选项

| 字段 | 描述 |
|------|------|
| `googleShoppingSearchKeyword` | 要搜索的产品名称 |
| `scrapeSellersFromGoogleShopping` | 设为 `true` 以提取卖家 |
| `scrapeProductsFromGoogleShopping` | 设为 `true` 同时提取产品详情 |
| `countryCode` | 目标国家（如 `us`、`uk`、`de`） |
| `maxGoogleShoppingSellersPerProduct` | 每个产品的最大卖家数 |
| `maxGoogleShoppingResults` | 总结果限制 |

---

## 支持的市场

### Amazon（20+ 地区）

`www.amazon.com`、`www.amazon.co.uk`、`www.amazon.de`、`www.amazon.fr`、`www.amazon.it`、`www.amazon.es`、`www.amazon.ca`、`www.amazon.com.au`、`www.amazon.co.jp`、`www.amazon.in`、`www.amazon.com.br`、`www.amazon.com.mx`、`www.amazon.nl`、`www.amazon.pl`、`www.amazon.se`、`www.amazon.ae`、`www.amazon.sa`、`www.amazon.sg`、`www.amazon.com.tr`、`www.amazon.eg`

### 美国主要零售商

`www.walmart.com`、`www.costco.com`、`www.costco.ca`、`www.homedepot.com`

### 欧洲零售商

`allegro.pl`、`allegro.cz`、`allegro.sk`、`www.alza.cz`、`www.alza.sk`、`www.alza.de`、`www.alza.at`、`www.alza.hu`、`www.kaufland.de`、`www.kaufland.pl`、`www.kaufland.cz`、`www.kaufland.sk`、`www.kaufland.at`、`www.kaufland.fr`、`www.kaufland.it`、`www.cdiscount.com`

### IKEA（40+ 国家/语言组合）

支持所有主要 IKEA 区域站点，提供多种语言选项。

### Google Shopping

用于跨多店铺的卖家发现。

---

## 运行提取

### 步骤 1：设置技能路径

```bash
SKILL_PATH=~/.claude/skills/apify-ecommerce
```

### 步骤 2：运行脚本

**快速回答（在聊天中显示）：**

```bash
node --env-file=~/.claude/.env $SKILL_PATH/reference/scripts/run_actor.js \
  --actor "apify/e-commerce-scraping-tool" \
  --input 'JSON_INPUT'
```

**CSV 导出：**

```bash
node --env-file=~/.claude/.env $SKILL_PATH/reference/scripts/run_actor.js \
  --actor "apify/e-commerce-scraping-tool" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_filename.csv \
  --format csv
```

**JSON 导出：**

```bash
node --env-file=~/.claude/.env $SKILL_PATH/reference/scripts/run_actor.js \
  --actor "apify/e-commerce-scraping-tool" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_filename.json \
  --format json
```

### 步骤 3：汇总结果

报告内容：
- 提取的项目数量
- 文件位置（如已导出）
- 基于工作流的关键洞察：
  - **产品：** 价格范围、异常值、MAP 违规
  - **评论：** 平均评分、情感趋势、质量问题
  - **卖家：** 卖家数量、发现的未授权卖家

---

## 错误处理

| 错误 | 解决方案 |
|------|----------|
| `APIFY_TOKEN not found` | 确保 `~/.claude/.env` 包含 `APIFY_TOKEN=your_token` |
| `Actor not found` | 验证 Actor ID：`apify/e-commerce-scraping-tool` |
| `Run FAILED` | 检查错误输出中的 Apify 控制台链接 |
| `Timeout` | 减少 `maxProductResults` 或增加 `--timeout` |
| `No results` | 验证 URL 有效且可访问 |
| `Invalid marketplace` | 检查市场值是否完全匹配支持列表 |

## 限制

- 仅当任务明确匹配上述范围时使用此技能
- 不要将输出替代特定环境的验证、测试或专家审查
- 如果缺少必需输入、权限、安全边界或成功标准，请停下来询问澄清
