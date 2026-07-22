---
name: seo-plan
description: >
  为新建或现有网站制定战略性SEO规划。提供行业专属模板、竞争分析、内容策略和实施路线图。
  触发词："SEO计划"、"SEO策略"、"内容策略"、"网站架构"、"SEO路线图"、
  "SEO plan"、"SEO strategy"、"content strategy"、"site architecture"、"SEO roadmap"。
risk: unknown
source: "https://github.com/AgriciDaniel/claude-seo"
date_added: "2026-03-21"
user-invokable: true
argument-hint: "[business-type]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - WebFetch
  - Write
---

# 战略性SEO规划

## 使用时机
- 为新建或现有网站制定SEO策略或路线图时使用。
- 需要同时规划内容、架构和实施阶段时使用。
- 用户需要的是SEO计划而非一次性审计时使用。

## 流程

### 1. 调研发现
- 业务类型、目标受众、竞争对手、目标
- 现有网站评估（如已存在）
- 预算和时间线约束
- 关键绩效指标（KPI）

### 2. 竞争分析
- 识别前5名竞争对手
- 分析其内容策略、Schema使用、技术配置
- 识别关键词差距和内容机会
- 评估其E-E-A-T信号
- 估算其域名权威度

### 3. 架构设计
- 从 `assets/` 目录加载行业模板
- 设计URL层级和内容支柱
- 规划内链策略
- 应用质量门控的站点地图结构
- 面向用户旅程的信息架构

### 4. 内容策略
- 与竞争对手的内容差距
- 页面类型和预估数量
- 博客/资源主题和发布频率
- E-E-A-T建设计划（作者简介、资质、经验信号）
- 按优先级排列的内容日历

### 5. 技术基础
- 托管和性能需求
- 各页面类型的Schema标记计划
- Core Web Vitals基线目标
- AI搜索就绪需求
- 移动优先考量

### 6. 实施路线图（4个阶段）

#### 第1阶段：基础（第1-4周）
- 技术配置和基础设施
- 核心页面（首页、关于、联系、主要服务）
- 基础Schema实施
- 分析和追踪配置

#### 第2阶段：扩展（第5-12周）
- 主要页面的内容创建
- 博客上线及初始文章
- 内链结构
- 本地SEO配置（如适用）

#### 第3阶段：规模化（第13-24周）
- 进阶内容开发
- 链接建设和外联
- GEO优化
- 性能优化

#### 第4阶段：权威建设（第7-12个月）
- 思想领导力内容
- PR和媒体报道
- 高级Schema实施
- 持续优化

## 行业模板

从 `assets/` 目录加载：
- `saas.md`：SaaS/软件公司
- `local-service.md`：本地服务企业
- `ecommerce.md`：电商商店
- `publisher.md`：内容出版商/媒体
- `agency.md`：代理机构和咨询公司
- `generic.md`：通用业务模板

## 输出

### 交付物
- `SEO-STRATEGY.md`：完整战略计划
- `COMPETITOR-ANALYSIS.md`：竞争洞察
- `CONTENT-CALENDAR.md`：内容路线图
- `IMPLEMENTATION-ROADMAP.md`：分阶段行动计划
- `SITE-STRUCTURE.md`：URL层级和架构

### KPI目标
| 指标 | 基线 | 3个月 | 6个月 | 12个月 |
|------|------|-------|-------|--------|
| 自然流量 | ... | ... | ... | ... |
| 关键词排名 | ... | ... | ... | ... |
| 域名权威度 | ... | ... | ... | ... |
| 已索引页面 | ... | ... | ... | ... |
| Core Web Vitals | ... | ... | ... | ... |

### 成功标准
- 每阶段有清晰、可衡量的目标
- 资源需求已定义
- 依赖关系已识别
- 风险缓解策略

## DataForSEO集成（可选）

如果 DataForSEO MCP 工具可用，使用 `dataforseo_labs_google_competitors_domain` 和 `dataforseo_labs_google_domain_intersection` 获取真实竞争情报，`dataforseo_labs_bulk_traffic_estimation` 获取流量估算，`kw_data_google_ads_search_volume` 和 `dataforseo_labs_bulk_keyword_difficulty` 进行关键词研究，`business_data_business_listings_search` 获取本地商家数据。

## 错误处理

| 场景 | 操作 |
|------|------|
| 无法识别的业务类型 | 回退到 `generic.md` 模板。告知用户未找到行业专属模板，使用通用业务模板继续。 |
| 未提供网站URL | 以新站规划模式继续。跳过需要在线URL的现有网站评估和竞争差距分析。 |
| 行业模板未找到 | 检查 `assets/` 目录中的可用模板。如果请求的模板文件缺失，使用 `generic.md` 并在输出中注明缺失的模板。 |

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，停止并请求澄清。
