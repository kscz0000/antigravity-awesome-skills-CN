---
name: seo-sitemap
description: >
  分析现有 XML 站点地图或使用行业模板生成新的站点地图。
  验证格式、URL 和结构。当用户提到"站点地图"、"sitemap"、"生成站点地图"、
  "站点地图问题"、"XML站点地图"、"sitemap问题"、"站点地图验证"时使用。
risk: unknown
source: "https://github.com/AgriciDaniel/claude-seo"
date_added: "2026-03-21"
user-invokable: true
argument-hint: "[url or generate]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# 站点地图分析与生成

## 何时使用
- 分析现有 XML 站点地图或生成新的站点地图时使用。
- 用户提到站点地图问题、站点地图生成或站点地图验证时使用。
- 检查 URL 覆盖范围、站点地图限制和站点地图质量规则时使用。

## 模式 1：分析现有站点地图

### 验证检查
- 有效的 XML 格式
- 单文件 URL 数量 <50,000（协议限制）
- 所有 URL 返回 HTTP 200
- `<lastmod>` 日期准确（非全部相同）
- 无已弃用标签：`<priority>` 和 `<changefreq>` 已被 Google 忽略
- 站点地图在 robots.txt 中被引用
- 对比已抓取页面与站点地图；标记缺失页面

### 质量信号
- 超过 50k URL 时使用站点地图索引文件
- 按内容类型拆分（页面、文章、图片、视频）
- 站点地图中无非规范 URL
- 站点地图中无 noindex URL
- 站点地图中无重定向 URL
- 仅使用 HTTPS URL（不含 HTTP）

### 常见问题
| 问题 | 严重程度 | 修复方式 |
|------|----------|----------|
| 单文件超过 50k URL | 严重 | 使用站点地图索引拆分 |
| 非 200 URL | 高 | 移除或修复失效 URL |
| 包含 noindex URL | 高 | 从站点地图中移除 |
| 包含重定向 URL | 中 | 更新为最终 URL |
| 所有 lastmod 相同 | 低 | 使用实际修改日期 |
| 使用了 priority/changefreq | 提示 | 可移除（Google 已忽略） |

## 模式 2：生成新站点地图

### 流程
1. 询问业务类型（或从现有网站自动检测）
2. 从 `../seo-plan/assets/` 目录加载行业模板
3. 与用户进行交互式结构规划
4. 应用质量门控：
   - ⚠️ 30+ 地理位置页面时警告（要求 60%+ 独特内容）
   - 🛑 50+ 地理位置页面时硬停止（需要提供理由）
5. 生成有效的 XML 输出
6. 超过 50k URL 时使用站点地图索引拆分
7. 生成 STRUCTURE.md 文档

### 安全的程序化页面（可大规模生成）
✅ 集成页面（附带真实设置文档）
✅ 模板/工具页面（附带可下载内容）
✅ 术语页面（200+ 词的定义）
✅ 产品页面（独特规格、评论）
✅ 用户资料页面（用户生成内容）

### 惩罚风险（避免大规模生成）
❌ 仅替换城市名的地理位置页面
❌ 缺乏行业特定价值的"最佳 [工具] 适用于 [行业]"页面
❌ 缺乏真实对比数据的"[竞品] 替代方案"页面
❌ 未经人工审核和独特价值的 AI 生成页面

## 站点地图格式

### 标准站点地图
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page</loc>
    <lastmod>2026-02-07</lastmod>
  </url>
</urlset>
```

### 站点地图索引（用于 >50k URL）
```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap-pages.xml</loc>
    <lastmod>2026-02-07</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap-posts.xml</loc>
    <lastmod>2026-02-07</lastmod>
  </sitemap>
</sitemapindex>
```

## 错误处理

- **URL 不可达**：报告 HTTP 状态码，建议检查网站是否在线
- **未找到站点地图**：先检查常见位置（/sitemap.xml、/sitemap_index.xml、robots.txt 引用），再报告"未找到"
- **无效 XML 格式**：报告具体解析错误及行号
- **检测到速率限制**：退避并报告部分结果，附加重试时间说明

## 输出

### 分析输出
- `VALIDATION-REPORT.md`：分析结果
- 按严重程度排列的问题列表
- 改进建议

### 生成输出
- `sitemap.xml`（或带索引的拆分文件）
- `STRUCTURE.md`：站点架构文档
- URL 数量和组织摘要

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不能替代针对特定环境的验证、测试或专家审查。
- 如缺少必要输入、权限、安全边界或成功标准，请停止并请求澄清。
