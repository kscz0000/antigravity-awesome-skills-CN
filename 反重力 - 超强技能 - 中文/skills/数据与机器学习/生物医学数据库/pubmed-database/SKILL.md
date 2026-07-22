---
name: pubmed-database
description: 通过 REST API 直接访问 PubMed 数据库。支持高级 Boolean/MeSH 查询、E-utilities API、批量处理、引用管理。Python 工作流优先使用 biopython（Bio.Entrez）。适用于直接 HTTP/REST 调用或自定义 API 实现。触发词：PubMed、PubMed搜索、NCBI、生物医学文献、MeSH查询、PMID查找、引文检索、文献监控、E-utilities、MEDLINE搜索、PubMed数据库、NCBI数据库。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
risk: unknown
source: community
---

# PubMed Database

## 概述

PubMed 是美国国家医学图书馆的综合数据库，免费提供 MEDLINE 和生命科学文献的检索服务。可通过 Boolean 运算符、MeSH 术语和字段标签构建高级查询，也可通过 E-utilities API 以编程方式访问数据，用于系统性综述和文献分析。

## 何时使用此技能

以下场景应使用此技能：
- 搜索生物医学或生命科学研究论文
- 使用 Boolean 运算符、字段标签或 MeSH 术语构建复杂检索式
- 开展系统性文献综述或 Meta 分析
- 通过 E-utilities API 以编程方式访问 PubMed 数据
- 按特定条件查找论文（作者、期刊、发表日期、文章类型）
- 获取引用信息、摘要或全文文章
- 处理 PMID（PubMed ID）或 DOI
- 创建文献监控或数据提取的自动化工作流

## 核心能力

### 1. 高级检索式构建

使用 Boolean 运算符、字段标签和专用语法构建复杂 PubMed 查询。

**基础检索策略**：
- 使用 Boolean 运算符（AND、OR、NOT）组合概念
- 使用字段标签将检索限定在记录的特定部分
- 使用双引号进行短语精确匹配
- 使用通配符匹配词形变体
- 使用邻近检索查找指定距离内的术语

**查询示例**：
```
# Recent systematic reviews on diabetes treatment
diabetes mellitus[mh] AND treatment[tiab] AND systematic review[pt] AND 2023:2024[dp]

# Clinical trials comparing two drugs
(metformin[nm] OR insulin[nm]) AND diabetes mellitus, type 2[mh] AND randomized controlled trial[pt]

# Author-specific research
smith ja[au] AND cancer[tiab] AND 2023[dp] AND english[la]
```

**何时查阅 search_syntax.md**：
- 需要完整的可用字段标签列表
- 需要检索运算符的详细说明
- 构建复杂的邻近检索
- 了解自动术语映射行为
- 需要日期范围、通配符或特殊字符的具体语法

字段标签 Grep 模式：`\[au\]|\[ti\]|\[ab\]|\[mh\]|\[pt\]|\[dp\]`

### 2. MeSH 术语与受控词表

使用医学主题词表（MeSH）在生物医学文献中进行精确、一致的检索。

**MeSH 检索**：
- [mh] 标签搜索 MeSH 术语并自动包含更窄的下位词
- [majr] 标签限定主题为主要焦点的文章
- 将 MeSH 术语与副主题词组合以提高特异性（如 diabetes mellitus/therapy[mh]）

**常用 MeSH 副主题词**：
- /diagnosis — 诊断方法
- /drug therapy — 药物治疗
- /epidemiology — 疾病模式与流行率
- /etiology — 病因
- /prevention & control — 预防措施
- /therapy — 治疗方法

**示例**：
```
# Diabetes therapy with specific focus
diabetes mellitus, type 2[mh]/drug therapy AND cardiovascular diseases[mh]/prevention & control
```

### 3. 文章类型与发表过滤

按发表类型、日期、文本可用性及其他属性筛选结果。

**发表类型**（使用 [pt] 字段标签）：
- Clinical Trial
- Meta-Analysis
- Randomized Controlled Trial
- Review
- Systematic Review
- Case Reports
- Guideline

**日期过滤**：
- 单年份：`2024[dp]`
- 日期范围：`2020:2024[dp]`
- 具体日期：`2024/03/15[dp]`

**文本可用性**：
- 免费全文：在查询中添加 `AND free full text[sb]`
- 有摘要：在查询中添加 `AND hasabstract[text]`

**示例**：
```
# Recent free full-text RCTs on hypertension
hypertension[mh] AND randomized controlled trial[pt] AND 2023:2024[dp] AND free full text[sb]
```

### 4. 通过 E-utilities API 编程访问

使用 NCBI E-utilities REST API 以编程方式访问 PubMed 数据，实现自动化和批量操作。

**核心 API 端点**：
1. **ESearch** — 搜索数据库并获取 PMID
2. **EFetch** — 以多种格式下载完整记录
3. **ESummary** — 获取文档摘要
4. **EPost** — 上传 UID 进行批量处理
5. **ELink** — 查找相关文章和关联数据

**基本工作流**：
```python
import requests

# Step 1: Search for articles
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
search_url = f"{base_url}esearch.fcgi"
params = {
    "db": "pubmed",
    "term": "diabetes[tiab] AND 2024[dp]",
    "retmax": 100,
    "retmode": "json",
    "api_key": "YOUR_API_KEY"  # Optional but recommended
}
response = requests.get(search_url, params=params)
pmids = response.json()["esearchresult"]["idlist"]

# Step 2: Fetch article details
fetch_url = f"{base_url}efetch.fcgi"
params = {
    "db": "pubmed",
    "id": ",".join(pmids),
    "rettype": "abstract",
    "retmode": "text",
    "api_key": "YOUR_API_KEY"
}
response = requests.get(fetch_url, params=params)
abstracts = response.text
```

**速率限制**：
- 无 API key：3 次请求/秒
- 有 API key：10 次请求/秒
- 始终包含 User-Agent 头部

**最佳实践**：
- 大结果集使用 history server（usehistory=y）
- 多个 UID 通过 EPost 实现批量操作
- 本地缓存结果以减少冗余调用
- 遵守速率限制以避免服务中断

**何时查阅 api_reference.md**：
- 需要详细的端点文档
- 需要各 E-utility 的参数规格
- 构建批量操作或 history server 工作流
- 了解响应格式（XML、JSON、text）
- 排查 API 错误或速率限制问题

API 端点 Grep 模式：`esearch|efetch|esummary|epost|elink|einfo`

### 5. 引用匹配与文章检索

通过部分引用信息或特定标识符查找文章。

**按标识符**：
```
# By PMID
12345678[pmid]

# By DOI
10.1056/NEJMoa123456[doi]

# By PMC ID
PMC123456[pmc]
```

**引用匹配**（通过 ECitMatch API）：
使用期刊名、年份、卷号、页码和作者查找 PMID：
```
Format: journal|year|volume|page|author|key|
Example: Science|2008|320|5880|1185|key1|
```

**按作者和元数据**：
```
# First author with year and topic
smith ja[1au] AND 2023[dp] AND cancer[tiab]

# Journal, volume, and page
nature[ta] AND 2024[dp] AND 456[vi] AND 123-130[pg]
```

### 6. 系统性文献综述

为系统性综述和 Meta 分析开展全面的文献检索。

**PICO 框架**（Population、Intervention、Comparison、Outcome）：
系统化构建临床研究问题：
```
# Example: Diabetes treatment effectiveness
# P: diabetes mellitus, type 2[mh]
# I: metformin[nm]
# C: lifestyle modification[tiab]
# O: glycemic control[tiab]

diabetes mellitus, type 2[mh] AND
(metformin[nm] OR lifestyle modification[tiab]) AND
glycemic control[tiab] AND
randomized controlled trial[pt]
```

**全面检索策略**：
```
# Include multiple synonyms and MeSH terms
(disease name[tiab] OR disease name[mh] OR synonym[tiab]) AND
(treatment[tiab] OR therapy[tiab] OR intervention[tiab]) AND
(systematic review[pt] OR meta-analysis[pt] OR randomized controlled trial[pt]) AND
2020:2024[dp] AND
english[la]
```

**检索优化**：
1. 从宽泛检索开始，查看结果
2. 用字段标签增加特异性
3. 应用日期和发表类型过滤
4. 使用 Advanced Search 查看查询翻译
5. 合并检索历史构建复杂查询

**何时查阅 common_queries.md**：
- 需要特定疾病类型或研究领域的示例查询
- 需要不同研究设计的模板
- 查找针对特定人群的查询模式（儿科、老年科等）
- 构建特定方法学的检索
- 需要质量过滤器或最佳实践模式

查询示例 Grep 模式：`diabetes|cancer|cardiovascular|clinical trial|systematic review`

### 7. 检索历史与保存的检索

使用 PubMed 的检索历史和 My NCBI 功能提高研究效率。

**检索历史**（通过 Advanced Search）：
- 最多保存 100 条检索
- 8 小时不活动后过期
- 使用 # 引用组合之前的检索
- 执行前可预览结果数量

**示例**：
```
#1: diabetes mellitus[mh]
#2: cardiovascular diseases[mh]
#3: #1 AND #2 AND risk factors[tiab]
```

**My NCBI 功能**：
- 无限期保存检索
- 为新匹配文章设置邮件提醒
- 创建已保存文章的收藏集
- 按项目或主题组织研究

**RSS 订阅**：
为任意检索创建 RSS 订阅，监控感兴趣领域的新发表文献。

### 8. 相关文章与引用发现

查找相关研究，探索引用网络。

**相似文章功能**：
每篇 PubMed 文章都包含预先计算的相关文章，基于：
- 标题和摘要相似度
- MeSH 术语重叠
- 加权算法匹配

**ELink 关联数据**：
```
# Find related articles programmatically
elink.fcgi?dbfrom=pubmed&db=pubmed&id=PMID&cmd=neighbor
```

**引用链接**：
- LinkOut 到出版商全文
- 链接到 PubMed Central 免费文章
- 连接到相关 NCBI 数据库（GenBank、ClinicalTrials.gov 等）

### 9. 导出与引用管理

以多种格式导出检索结果，用于引用管理和进一步分析。

**导出格式**：
- .nbib 文件供参考管理器使用（Zotero、Mendeley、EndNote）
- AMA、MLA、APA、NLM 引用格式
- CSV 用于数据分析
- XML 用于编程处理

**剪贴板与收藏集**：
- 剪贴板：临时存储最多 500 条目（8 小时过期）
- 收藏集：通过 My NCBI 账户永久存储

**通过 API 批量导出**：
```python
# Export citations in MEDLINE format
efetch.fcgi?db=pubmed&id=PMID1,PMID2&rettype=medline&retmode=text
```

## 使用参考文件

此技能在 `references/` 目录中包含三个全面的参考文件：

### references/api_reference.md
完整的 E-utilities API 文档，包含全部九个端点、参数、响应格式和最佳实践。以下情况查阅：
- 实现编程方式访问 PubMed
- 构建 API 请求
- 了解速率限制和认证
- 通过 history server 处理大数据集
- 排查 API 错误

### references/search_syntax.md
PubMed 检索语法的详细指南，包含字段标签、Boolean 运算符、通配符和特殊字符。以下情况查阅：
- 构建复杂检索式
- 了解自动术语映射
- 使用高级检索功能（邻近检索、通配符）
- 应用过滤器和限制
- 排查意外的检索结果

### references/common_queries.md
涵盖各种研究场景、疾病类型和方法学的大量示例查询。以下情况查阅：
- 开始新的文献检索
- 需要特定研究领域的模板
- 查找最佳实践查询模式
- 开展系统性综述
- 检索特定研究设计或人群

**参考文件加载策略**：
根据具体任务按需将参考文件加载到上下文中。简短查询或基础检索时，本 SKILL.md 中的信息可能已足够。复杂操作请查阅相应的参考文件。

## 常用工作流

### 工作流 1：基础文献检索

1. 确定关键概念和同义词
2. 使用 Boolean 运算符和字段标签构建查询
3. 查看初始结果并优化查询
4. 应用过滤器（日期、文章类型、语言）
5. 导出结果进行分析

### 工作流 2：系统性综述检索

1. 使用 PICO 框架定义研究问题
2. 确定所有相关 MeSH 术语和同义词
3. 构建全面的检索策略
4. 检索多个数据库（包含 PubMed）
5. 记录检索策略和日期
6. 导出结果进行筛选和审查

### 工作流 3：编程数据提取

1. 设计检索式并在 Web 界面中测试
2. 使用 ESearch API 实现检索
3. 大结果集使用 history server
4. 使用 EFetch 获取详细记录
5. 解析 XML/JSON 响应
6. 本地缓存存储数据
7. 实现速率限制和错误处理

### 工作流 4：引用发现

1. 从已知的相关文章开始
2. 使用相似文章功能查找相关研究
3. 检查引用文章（如有）
4. 从相关文章中探索 MeSH 术语
5. 基于发现构建新的检索
6. 使用 ELink 查找相关数据库条目

### 工作流 5：持续文献监控

1. 构建全面的检索式
2. 测试并优化检索精度
3. 将检索保存到 My NCBI 账户
4. 为新匹配设置邮件提醒
5. 创建 RSS 订阅供阅读器监控
6. 定期审查新文章

## 提示与最佳实践

### 检索策略
- 从宽泛检索开始，再用字段标签和过滤器收窄
- 包含同义词和 MeSH 术语以提高覆盖率
- 使用引号进行精确短语匹配
- 在 Advanced Search 中检查 Search Details 以验证查询翻译
- 使用检索历史合并多次检索

### API 使用
- 获取 API key 以获得更高速率限制（10 次/秒 vs 3 次/秒）
- 结果集超过 500 篇文章时使用 history server
- 实现指数退避处理速率限制
- 本地缓存结果以减少冗余请求
- 始终包含描述性的 User-Agent 头部

### 质量过滤
- 优先选择系统性综述和 Meta 分析获取综合证据
- 使用发表类型过滤器查找特定研究设计
- 按日期过滤获取最新研究
- 按需应用语言过滤器
- 使用免费全文过滤器实现即时访问

### 引用管理
- 及早且频繁导出以避免丢失检索结果
- 使用 .nbib 格式确保与大多数参考管理器兼容
- 创建 My NCBI 账户实现永久收藏
- 记录检索策略以确保可复现性
- 使用收藏集按项目组织研究

## 限制与注意事项

### 数据库覆盖范围
- 主要涵盖生物医学和生命科学文献
- 1975 年前的文章通常缺少摘要
- 2002 年起可获取完整作者姓名
- 非英文摘要可用但可能默认显示英文

### 检索限制
- 最多显示 10,000 条结果
- 检索历史 8 小时不活动后过期
- 剪贴板最多容纳 500 条目，8 小时过期
- 自动术语映射可能产生意外结果

### API 注意事项
- 存在速率限制（3-10 次请求/秒）
- 大型查询可能超时（使用 history server）
- 详细数据提取需要 XML 解析
- 生产环境建议使用 API key

### 访问限制
- PubMed 提供引用和摘要（不一定有全文）
- 全文访问取决于出版商、机构访问权限或开放获取状态
- LinkOut 可用性因期刊和机构而异
- 部分内容需要订阅或付费

## 支持资源

- **PubMed Help**: https://pubmed.ncbi.nlm.nih.gov/help/
- **E-utilities Documentation**: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **NLM Help Desk**: 1-888-FIND-NLM (1-888-346-3656)
- **Technical Support**: vog.hin.mln.ibcn@seitilitue
- **Mailing List**: utilities-announce@ncbi.nlm.nih.gov
