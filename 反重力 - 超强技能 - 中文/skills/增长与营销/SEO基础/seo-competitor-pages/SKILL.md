---
name: seo-competitor-pages
description: >
  生成 SEO 优化的竞争对手对比页和替代方案页。涵盖
  "X vs Y" 布局、"X 替代方案"页面、功能矩阵、Schema 标记
  和转化优化。触发词：对比页、vs 页面、替代方案页、competitor comparison、X vs Y
risk: unknown
source: "https://github.com/AgriciDaniel/claude-seo"
date_added: "2026-03-21"
user-invokable: true
argument-hint: "[url or generate] [competitor]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
---

# 竞争对手对比与替代方案页面

创建高转化率的对比页和替代方案页面，以准确、结构化的内容
锁定竞争意图关键词。

## 使用场景
- 创建 "X vs Y" 对比页或替代方案页时使用。
- 通过 SEO 落地页锁定竞争对手意图关键词时使用。
- 需要结构化对比内容、功能矩阵或以转化为导向的竞争对手页面时使用。

## 页面类型

### 1. "X vs Y" 对比页
- 两个产品/服务之间的直接对比
- 逐功能的平衡分析
- 明确的结论或推荐及理由
- 目标关键词：`[产品 A] vs [产品 B]`

### 2. "X 替代方案"页面
- 某个产品/服务的替代方案列表
- 每个替代方案附带简要概述、优缺点、最佳使用场景
- 目标关键词：`[产品] alternatives`、`best alternatives to [产品]`

### 3. "最佳 [品类] 工具" 合集页
- 某品类中精选的顶级工具/服务列表
- 排名标准清晰说明
- 目标关键词：`best [品类] tools [年份]`、`top [品类] software`

### 4. 对比表格页
- 多产品功能矩阵，产品按列排列
- 如为交互式页面，支持排序/筛选
- 目标关键词：`[品类] comparison`、`[品类] comparison chart`

## 对比表格生成

### 功能矩阵布局
```
| 功能             | 你的产品     | 竞争对手 A   | 竞争对手 B   |
|------------------|:------------:|:------------:|:------------:|
| 功能 1           | ✅           | ✅           | ❌           |
| 功能 2           | ✅           | ⚠️ 部分支持  | ✅           |
| 功能 3           | ✅           | ❌           | ❌           |
| 价格（起步）     | $X/月        | $Y/月        | $Z/月        |
| 免费套餐         | ✅           | ❌           | ✅           |
```

### 数据准确性要求
- 所有功能声明必须可从公开来源验证
- 价格必须是最新的（注明"截至 [日期]"）
- 更新频率：每季度或竞争对手发布重大变更时审查
- 尽量为每个竞争对手数据点链接来源

## Schema 标记建议

### 带聚合评分的 Product Schema
```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "[产品名称]",
  "description": "[产品描述]",
  "brand": {
    "@type": "Brand",
    "name": "[品牌名称]"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[评分]",
    "reviewCount": "[评论数]",
    "bestRating": "5",
    "worstRating": "1"
  }
}
```

### SoftwareApplication（用于软件对比）
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "[软件名称]",
  "applicationCategory": "[分类]",
  "operatingSystem": "[操作系统]",
  "offers": {
    "@type": "Offer",
    "price": "[价格]",
    "priceCurrency": "USD"
  }
}
```

### ItemList（用于合集页）
```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Best [品类] Tools [年份]",
  "itemListOrder": "https://schema.org/ItemListOrderDescending",
  "numberOfItems": "[数量]",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "[产品名称]",
      "url": "[产品 URL]"
    }
  ]
}
```

## 关键词定位

### 对比意图模式
| 模式 | 示例 | 搜索量信号 |
|---------|---------|---------------------|
| `[A] vs [B]` | "Slack vs Teams" | 高 |
| `[A] alternative` | "Figma alternatives" | 高 |
| `[A] alternatives [年份]` | "Notion alternatives 2026" | 高 |
| `best [品类] tools` | "best project management tools" | 高 |
| `[A] vs [B] for [使用场景]` | "AWS vs Azure for startups" | 中 |
| `[A] review [年份]` | "Monday.com review 2026" | 中 |
| `[A] vs [B] pricing` | "HubSpot vs Salesforce pricing" | 中 |
| `is [A] better than [B]` | "is Notion better than Confluence" | 中 |

### 标题标签公式
- X vs Y：`[A] vs [B]：[核心差异点]（[年份]）`
- 替代方案：`[N] 个最佳 [A] 替代方案（[年份]）（免费和付费）`
- 合集：`[N] 个最佳 [品类] 工具（[年份]），对比排名`

### H1 模式
- 匹配标题标签的搜索意图
- 自然融入核心关键词
- 控制在 70 个字符以内

## 转化优化布局

### CTA 放置位置
- **首屏**：简要对比摘要 + 主要 CTA
- **对比表格下方**："免费试用 [你的产品]" CTA
- **页面底部**：最终推荐 + CTA
- 避免在竞争对手描述区域放置过于激进的 CTA（会降低信任感）

### 社会证明板块
- 与对比标准相关的客户评价
- G2/Capterra/TrustPilot 评分（附来源链接）
- 从竞争对手迁移的案例研究
- "从 [竞争对手] 切换" 的用户故事

### 价格亮点
- 清晰的价格对比表格
- 突出价值优势（不仅仅是最低价）
- 包含隐藏费用（设置费、按用户定价、超额费用）
- 链接到完整定价页面

### 信任信号
- "最后更新于 [日期]" 时间戳
- 具有相关专业知识的作者
- 方法论说明（对比是如何进行的）
- 披露自家产品的关联关系

## 公平性准则

- **准确性**：所有竞争对手信息必须可从公开来源验证
- **不诽谤**：绝不发布关于竞争对手的虚假或误导性声明
- **引用来源**：链接到竞争对手网站、评测网站或文档
- **及时更新**：竞争对手发布重大变更时及时审查和更新
- **披露关联**：明确说明哪个产品是你的
- **平衡呈现**：如实承认竞争对手的优势
- **价格准确性**：所有价格数据注明"截至 [日期]"
- **功能验证**：尽可能测试竞争对手功能，否则引用文档

## 内链策略

- 从对比区域链接到自家产品/服务页面
- 在相关对比页之间交叉链接（例如"A vs B"链接到"A vs C"）
- 讨论单个功能时链接到功能专页
- 面包屑导航：首页 > 对比 > [当前页面]
- 页面底部设置相关对比区域
- 链接到对比中提到的案例研究和客户评价

## 输出

### 对比页模板
- `COMPARISON-PAGE.md`：可直接实施的页面结构，包含各板块
- 功能矩阵表格
- 内容大纲及字数目标（最少 1,500 字）

### Schema 标记
- `comparison-schema.json`：Product/SoftwareApplication/ItemList 的 JSON-LD

### 关键词策略
- 核心关键词和辅助关键词
- 相关长尾关键词机会
- 与现有竞争对手页面的内容差距

### 建议
- 现有对比页的内容改进
- 新对比页机会
- Schema 标记补充
- 转化优化建议

## 错误处理

| 场景 | 处理方式 |
|----------|--------|
| 竞争对手 URL 无法访问 | 报告哪些竞争对手 URL 访问失败。使用可用数据继续，并在对比中标注缺失部分。 |
| 竞争对手数据不足（价格、功能不可用） | 明确标注缺失数据。在对比表中使用"未公开"而非猜测。 |
| 未发现产品/服务重叠 | 报告产品服务于不同市场。建议功能重叠的替代竞争对手，或改为品类合集格式。 |

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为对环境特定验证、测试或专家审查的替代。
- 如果所需输入、权限、安全边界或成功标准缺失，请停下来寻求澄清。
