---
name: seo
description: "跨技术 SEO、页面 SEO、Schema、站点地图、内容质量、AI 搜索就绪度和 GEO 的全面 SEO 审计。当用户要求全面 SEO 分析、SEO 策略、SEO 审计、SEO 检查、搜索引擎优化分析时使用此技能。"
risk: unknown
source: "https://github.com/AgriciDaniel/claude-seo"
date_added: "2026-03-21"
user-invokable: true
argument-hint: "[command] [url]"
---

# SEO: 通用 SEO 分析技能

跨所有行业（SaaS、本地服务、电子商务、出版商、代理商）的全面 SEO 分析。编排 12 个专业子技能和 7 个子代理（+ 可选扩展子技能如 seo-dataforseo）。

## 使用场景
- 当用户要求全面 SEO 审计或广泛 SEO 策略时使用
- 当多个 SEO 维度在范围内时，作为总入口点使用
- 当任务同时涵盖技术 SEO、内容、Schema、站点地图和 AI 搜索就绪度时使用

## 快速参考

| 命令 | 功能 |
|---------|-------------|
| `/seo audit <url>` | 通过并行子代理委派进行全面网站审计 |
| `/seo page <url>` | 深度单页分析 |
| `/seo sitemap <url or generate>` | 分析或生成 XML 站点地图 |
| `/seo schema <url>` | 检测、验证和生成 Schema.org 标记 |
| `/seo images <url>` | 图片优化分析 |
| `/seo technical <url>` | 技术 SEO 审计（9 个类别） |
| `/seo content <url>` | E-E-A-T 和内容质量分析 |
| `/seo geo <url>` | AI Overviews / 生成式引擎优化 |
| `/seo plan <business-type>` | 战略 SEO 规划 |
| `/seo programmatic [url\|plan]` | 程序化 SEO 分析和规划 |
| `/seo competitor-pages [url\|generate]` | 竞争对手对比页面生成 |
| `/seo hreflang [url]` | Hreflang/i18n SEO 审计和生成 |
| `/seo dataforseo [command]` | 通过 DataForSEO 获取实时 SEO 数据（扩展） |
| `/seo image-gen [use-case] <description>` | AI 图片生成用于 SEO 资产（扩展） |

## 编排逻辑

当用户调用 `/seo audit` 时，并行委派给子代理：
1. 检测业务类型（SaaS、本地、电子商务、出版商、代理商、其他）
2. 生成子代理：seo-technical、seo-content、seo-schema、seo-sitemap、seo-performance、seo-visual、seo-geo
3. 收集结果并生成包含 SEO 健康评分（0-100）的统一报告
4. 创建优先级行动计划（Critical -> High -> Medium -> Low）

对于单个命令，直接加载相关子技能。

## 行业检测

从首页信号检测业务类型：
- **SaaS**: 定价页面、/features、/integrations、/docs、"free trial"、"sign up"
- **本地服务**: 电话号码、地址、服务区域、"serving [city]"、Google Maps 嵌入
- **电子商务**: /products、/collections、/cart、"add to cart"、产品 schema
- **出版商**: /blog、/articles、/topics、文章 schema、作者页面、发布日期
- **代理商**: /case-studies、/portfolio、/industries、"our work"、客户 logo

## 质量门控

阅读 `references/quality-gates.md` 了解每种页面类型的薄内容阈值。
硬性规则：
- 30+ 位置页面时发出警告（强制 60%+ 唯一内容）
- 50+ 位置页面时硬性停止（需要用户说明理由）
- 永不推荐 HowTo schema（2023 年 9 月已弃用）
- FAQ schema 用于 Google 富媒体结果：仅限政府和医疗网站（2023 年 8 月限制）；商业网站上的现有 FAQPage -> 标记为信息优先级（非 Critical），注明 AI/LLM 引用收益；不建议为 Google 收益添加新的 FAQPage
- 所有 Core Web Vitals 引用使用 INP，而非 FID

## 参考文件

按需加载（不要在启动时全部加载）：
- `references/cwv-thresholds.md`: 当前 Core Web Vitals 阈值和测量详情
- `references/schema-types.md`: 所有支持的 schema 类型及弃用状态
- `references/eeat-framework.md`: E-E-A-T 评估标准（2025 年 9 月 QRG 更新）
- `references/quality-gates.md`: 内容长度下限、唯一性阈值

## 评分方法

### SEO 健康评分（0-100）
所有类别的加权汇总：

| 类别 | 权重 |
|----------|--------|
| 技术 SEO | 22% |
| 内容质量 | 23% |
| 页面 SEO | 20% |
| Schema / 结构化数据 | 10% |
| 性能 (CWV) | 10% |
| AI 搜索就绪度 | 10% |
| 图片 | 5% |

### 优先级级别
- **Critical**: 阻止索引或导致惩罚（需要立即修复）
- **High**: 显著影响排名（1 周内修复）
- **Medium**: 优化机会（1 个月内修复）
- **Low**: 锦上添花（放入待办）

## 子技能

此技能编排 12 个专业子技能（+ 2 个扩展）：

1. **seo-audit** -- 通过并行委派进行全面网站审计
2. **seo-page** -- 深度单页分析
3. **seo-technical** -- 技术 SEO（9 个类别）
4. **seo-content** -- E-E-A-T 和内容质量
5. **seo-schema** -- Schema 标记检测和生成
6. **seo-images** -- 图片优化
7. **seo-sitemap** -- 站点地图分析和生成
8. **seo-geo** -- AI Overviews / GEO 优化
9. **seo-plan** -- 使用模板进行战略规划
10. **seo-programmatic** -- 程序化 SEO 分析和规划
11. **seo-competitor-pages** -- 竞争对手对比页面生成
12. **seo-hreflang** -- Hreflang/i18n SEO 审计和生成
13. **seo-dataforseo** -- 通过 DataForSEO MCP 获取实时 SEO 数据（扩展）
14. **seo-image-gen** -- 通过 Gemini 生成 SEO 资产的 AI 图片（扩展）

## 子代理

用于审计期间的并行分析：
- `seo-technical` -- 可爬取性、可索引性、安全性、CWV
- `seo-content` -- E-E-A-T、可读性、薄内容
- `seo-schema` -- 检测、验证、生成
- `seo-sitemap` -- 结构、覆盖范围、质量门控
- `seo-performance` -- Core Web Vitals 测量
- `seo-visual` -- 截图、移动端测试、首屏
- `seo-geo` -- AI 爬虫访问、llms.txt、可引用性、品牌提及信号
- `seo-dataforseo` -- 实时 SERP、关键词、反向链接、本地 SEO 数据（扩展，可选）
- `seo-image-gen` -- SEO 图片审计和生成计划（扩展，可选）

## 错误处理

| 场景 | 操作 |
|----------|--------|
| 无法识别的命令 | 列出快速参考表中的可用命令。建议最接近的匹配命令。 |
| URL 无法访问 | 报告错误并建议用户验证 URL。不要尝试猜测网站内容。 |
| 审计期间子技能失败 | 报告成功子技能的部分结果。明确说明哪个子技能失败及原因。建议单独重新运行失败的子技能。 |
| 业务类型检测模糊 | 展示检测到的前两种类型及支持信号。在继续行业特定建议之前请用户确认。 |

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
