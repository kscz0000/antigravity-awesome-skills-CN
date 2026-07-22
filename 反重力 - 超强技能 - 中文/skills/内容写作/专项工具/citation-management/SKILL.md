---
name: citation-management
description: "在研究和写作过程中系统化管理文献引用。当用户要求'管理引用'、'文献引用'、'BibTeX'、'DOI转换'、'PubMed搜索'、'Google Scholar搜索'、'引用验证'时使用。"
license: MIT License
metadata:
    skill-author: K-Dense Inc.
risk: unknown
source: community
---

# 引用管理

## 概述

在研究和写作过程中系统化管理文献引用。本技能提供工具和策略，用于搜索学术数据库（Google Scholar、PubMed），从多个来源（CrossRef、PubMed、arXiv）提取准确的元数据，验证引用信息，并生成格式规范的 BibTeX 条目。

对于维护引用准确性、避免参考文献错误以及确保可复现研究至关重要。与 literature-review 技能无缝集成，支持完整的研究工作流程。

## 何时使用本技能

在以下情况下使用本技能：
- 在 Google Scholar 或 PubMed 上搜索特定论文
- 将 DOI、PMID 或 arXiv ID 转换为格式规范的 BibTeX
- 提取完整的引用元数据（作者、标题、期刊、年份等）
- 验证现有引用的准确性
- 清理和格式化 BibTeX 文件
- 查找特定领域的高被引论文
- 验证引用信息与实际出版物是否匹配
- 为稿件或论文构建参考文献
- 检查重复引用
- 确保引用格式一致性

## 使用科学示意图增强视觉效果

**使用本技能创建文档时，始终考虑添加科学图表和示意图以增强视觉传达效果。**

如果您的文档尚未包含示意图或图表：
- 使用 **scientific-schematics** 技能生成 AI 驱动的出版级图表
- 只需用自然语言描述您想要的图表
- Nano Banana Pro 将自动生成、审查和优化示意图

**对于新文档：** 默认应生成科学示意图，以可视化呈现文本中描述的关键概念、工作流程、架构或关系。

**如何生成示意图：**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

AI 将自动：
- 创建具有正确格式的出版级图像
- 通过多次迭代进行审查和优化
- 确保无障碍性（色盲友好、高对比度）
- 将输出保存到 figures/ 目录

**何时添加示意图：**
- 引用工作流程图
- 文献搜索方法流程图
- 参考文献管理系统架构
- 引用格式决策树
- 数据库集成图
- 任何受益于可视化的复杂概念

有关创建示意图的详细指导，请参阅 scientific-schematics 技能文档。

---

## 核心工作流程

引用管理遵循系统化流程：

### 阶段 1：论文发现与搜索

**目标**：使用学术搜索引擎查找相关论文。

#### Google Scholar 搜索

Google Scholar 提供跨学科最全面的覆盖。

**基本搜索**：
```bash
# 搜索某个主题的论文
python scripts/search_google_scholar.py "CRISPR gene editing" \
  --limit 50 \
  --output results.json

# 带年份过滤的搜索
python scripts/search_google_scholar.py "machine learning protein folding" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --output ml_proteins.json
```

**高级搜索策略**（参见 `references/google_scholar_search.md`）：
- 使用引号搜索精确短语：`"deep learning"`
- 按作者搜索：`author:LeCun`
- 在标题中搜索：`intitle:"neural networks"`
- 排除词汇：`machine learning -survey`
- 使用排序选项查找高被引论文
- 按日期范围过滤以获取最新工作

**最佳实践**：
- 使用具体、有针对性的搜索词
- 包含关键技术术语和缩写
- 对快速发展的领域按近年过滤
- 查看"Cited by"以查找开创性论文
- 导出热门结果以供进一步分析

#### PubMed 搜索

PubMed 专注于生物医学和生命科学文献（3500 万+ 引用）。

**基本搜索**：
```bash
# 搜索 PubMed
python scripts/search_pubmed.py "Alzheimer's disease treatment" \
  --limit 100 \
  --output alzheimers.json

# 使用 MeSH 术语和过滤器搜索
python scripts/search_pubmed.py \
  --query '"Alzheimer Disease"[MeSH] AND "Drug Therapy"[MeSH]' \
  --date-start 2020 \
  --date-end 2024 \
  --publication-types "Clinical Trial,Review" \
  --output alzheimers_trials.json
```

**高级 PubMed 查询**（参见 `references/pubmed_search.md`）：
- 使用 MeSH 术语：`"Diabetes Mellitus"[MeSH]`
- 字段标签：`"cancer"[Title]`、`"Smith J"[Author]`
- 布尔运算符：`AND`、`OR`、`NOT`
- 日期过滤器：`2020:2024[Publication Date]`
- 出版物类型：`"Review"[Publication Type]`
- 结合 E-utilities API 进行自动化

**最佳实践**：
- 使用 MeSH Browser 查找正确的受控词汇
- 先在 PubMed 高级搜索构建器中构建复杂查询
- 使用 OR 包含多个同义词
- 检索 PMID 以便轻松提取元数据
- 导出为 JSON 或直接导出为 BibTeX

### 阶段 2：元数据提取

**目标**：将论文标识符（DOI、PMID、arXiv ID）转换为完整、准确的元数据。

#### 快速 DOI 转 BibTeX

对于单个 DOI，使用快速转换工具：

```bash
# 转换单个 DOI
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2

# 从文件转换多个 DOI
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# 不同输出格式
python scripts/doi_to_bibtex.py 10.1038/nature12345 --format json
```

#### 全面元数据提取

对于 DOI、PMID、arXiv ID 或 URL：

```bash
# 从 DOI 提取
python scripts/extract_metadata.py --doi 10.1038/s41586-021-03819-2

# 从 PMID 提取
python scripts/extract_metadata.py --pmid 34265844

# 从 arXiv ID 提取
python scripts/extract_metadata.py --arxiv 2103.14030

# 从 URL 提取
python scripts/extract_metadata.py --url "https://www.nature.com/articles/s41586-021-03819-2"

# 从文件批量提取（混合标识符）
python scripts/extract_metadata.py --input identifiers.txt --output citations.bib
```

**元数据来源**（参见 `references/metadata_extraction.md`）：

1. **CrossRef API**：DOI 的主要来源
   - 期刊文章的综合元数据
   - 出版商提供的信息
   - 包含作者、标题、期刊、卷、页码、日期
   - 免费，无需 API 密钥

2. **PubMed E-utilities**：生物医学文献
   - 官方 NCBI 元数据
   - 包含 MeSH 术语、摘要
   - PMID 和 PMCID 标识符
   - 免费，大量使用建议使用 API 密钥

3. **arXiv API**：物理、数学、计算机科学、定量生物学的预印本
   - 预印本的完整元数据
   - 版本跟踪
   - 作者机构
   - 免费，开放获取

4. **DataCite API**：研究数据集、软件和其他资源
   - 非传统学术产出的元数据
   - 数据集和代码的 DOI
   - 免费访问

**提取内容**：
- **必填字段**：author、title、year
- **期刊文章**：journal、volume、number、pages、DOI
- **书籍**：publisher、ISBN、edition
- **会议论文**：booktitle、conference location、pages
- **预印本**：repository（arXiv、bioRxiv）、preprint ID
- **附加信息**：abstract、keywords、URL

### 阶段 3：BibTeX 格式化

**目标**：生成干净、格式规范的 BibTeX 条目。

#### 理解 BibTeX 条目类型

完整指南请参见 `references/bibtex_formatting.md`。

**常见条目类型**：
- `@article`：期刊文章（最常见）
- `@book`：书籍
- `@inproceedings`：会议论文
- `@incollection`：书籍章节
- `@phdthesis`：学位论文
- `@misc`：预印本、软件、数据集

**按类型的必填字段**：

```bibtex
@article{citationkey,
  author  = {Last1, First1 and Last2, First2},
  title   = {Article Title},
  journal = {Journal Name},
  year    = {2024},
  volume  = {10},
  number  = {3},
  pages   = {123--145},
  doi     = {10.1234/example}
}

@inproceedings{citationkey,
  author    = {Last, First},
  title     = {Paper Title},
  booktitle = {Conference Name},
  year      = {2024},
  pages     = {1--10}
}

@book{citationkey,
  author    = {Last, First},
  title     = {Book Title},
  publisher = {Publisher Name},
  year      = {2024}
}
```

#### 格式化与清理

使用格式化工具标准化 BibTeX 文件：

```bash
# 格式化和清理 BibTeX 文件
python scripts/format_bibtex.py references.bib \
  --output formatted_references.bib

# 按引用键排序
python scripts/format_bibtex.py references.bib \
  --sort key \
  --output sorted_references.bib

# 按年份排序（最新优先）
python scripts/format_bibtex.py references.bib \
  --sort year \
  --descending \
  --output sorted_references.bib

# 删除重复项
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --output clean_references.bib

# 验证并报告问题
python scripts/format_bibtex.py references.bib \
  --validate \
  --report validation_report.txt
```

**格式化操作**：
- 标准化字段顺序
- 统一缩进和间距
- 标题中正确的大写（用 {} 保护）
- 标准化的作者姓名格式
- 统一的引用键格式
- 删除不必要的字段
- 修复常见错误（缺少逗号、大括号）

### 阶段 4：引用验证

**目标**：验证所有引用准确且完整。

#### 全面验证

```bash
# 验证 BibTeX 文件
python scripts/validate_citations.py references.bib

# 验证并修复常见问题
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --output validated_references.bib

# 生成详细验证报告
python scripts/validate_citations.py references.bib \
  --report validation_report.json \
  --verbose
```

**验证检查**（参见 `references/citation_validation.md`）：

1. **DOI 验证**：
   - DOI 通过 doi.org 正确解析
   - BibTeX 与 CrossRef 之间的元数据匹配
   - 无损坏或无效的 DOI

2. **必填字段**：
   - 条目类型的所有必填字段都存在
   - 无空缺或缺失的关键信息
   - 作者姓名格式正确

3. **数据一致性**：
   - 年份有效（4 位数字，合理范围）
   - 卷/号为数字
   - 页码格式正确（如 123--145）
   - URL 可访问

4. **重复检测**：
   - 同一 DOI 被多次使用
   - 相似标题（可能是重复项）
   - 相同的作者/年份/标题组合

5. **格式合规性**：
   - 有效的 BibTeX 语法
   - 正确的大括号和引号
   - 引用键唯一
   - 特殊字符处理正确

**验证输出**：
```json
{
  "total_entries": 150,
  "valid_entries": 145,
  "errors": [
    {
      "citation_key": "Smith2023",
      "error_type": "missing_field",
      "field": "journal",
      "severity": "high"
    },
    {
      "citation_key": "Jones2022",
      "error_type": "invalid_doi",
      "doi": "10.1234/broken",
      "severity": "high"
    }
  ],
  "warnings": [
    {
      "citation_key": "Brown2021",
      "warning_type": "possible_duplicate",
      "duplicate_of": "Brown2021a",
      "severity": "medium"
    }
  ]
}
```

### 阶段 5：与写作工作流程集成

#### 为稿件构建参考文献

创建参考文献的完整工作流程：

```bash
# 1. 搜索您主题的论文
python scripts/search_pubmed.py \
  '"CRISPR-Cas Systems"[MeSH] AND "Gene Editing"[MeSH]' \
  --date-start 2020 \
  --limit 200 \
  --output crispr_papers.json

# 2. 从搜索结果中提取 DOI 并转换为 BibTeX
python scripts/extract_metadata.py \
  --input crispr_papers.json \
  --output crispr_refs.bib

# 3. 通过 DOI 添加特定论文
python scripts/doi_to_bibtex.py 10.1038/nature12345 >> crispr_refs.bib
python scripts/doi_to_bibtex.py 10.1126/science.abcd1234 >> crispr_refs.bib

# 4. 格式化和清理 BibTeX 文件
python scripts/format_bibtex.py crispr_refs.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output references.bib

# 5. 验证所有引用
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --report validation.json \
  --output final_references.bib

# 6. 查看验证报告并修复任何剩余问题
cat validation.json

# 7. 在您的 LaTeX 文档中使用
# \bibliography{final_references}
```

#### 与文献综述技能集成

本技能与 `literature-review` 技能互补：

**文献综述技能** → 系统化搜索和综合
**引用管理技能** → 技术性引用处理

**组合工作流程**：
1. 使用 `literature-review` 进行全面的多数据库搜索
2. 使用 `citation-management` 提取和验证所有引用
3. 使用 `literature-review` 按主题综合发现
4. 使用 `citation-management` 验证最终参考文献的准确性

```bash
# 完成文献综述后
# 验证综述文档中的所有引用
python scripts/validate_citations.py my_review_references.bib --report review_validation.json

# 如需要，按特定引用格式格式化
python scripts/format_bibtex.py my_review_references.bib \
  --style nature \
  --output formatted_refs.bib
```

## 搜索策略

### Google Scholar 最佳实践

**查找开创性和高影响力论文**（关键）：

始终根据引用次数、期刊质量和作者声誉对论文进行优先级排序：

**引用次数阈值：**
| 论文年龄 | 引用次数 | 分类 |
|-----------|-----------|----------------|
| 0-3 年 | 20+ | 值得关注 |
| 0-3 年 | 100+ | 高影响力 |
| 3-7 年 | 100+ | 重要 |
| 3-7 年 | 500+ | 里程碑论文 |
| 7+ 年 | 500+ | 开创性工作 |
| 7+ 年 | 1000+ | 基础性 |

**期刊质量层级：**
- **第一梯队（优先）：** Nature、Science、Cell、NEJM、Lancet、JAMA、PNAS
- **第二梯队（高优先级）：** 影响因子 >10，顶级会议（NeurIPS、ICML、ICLR）
- **第三梯队（良好）：** 专业期刊（IF 5-10）
- **第四梯队（谨慎使用）：** 影响力较低的同行评审期刊

**作者声誉指标：**
- h-index >40 的资深研究者
- 在第一梯队期刊发表多篇论文
- 知名机构的领导职位
- 奖项和编委职位

**高影响力论文搜索策略：**
- 按引用次数排序（最多引用优先）
- 查看第一梯队期刊的综述文章以获取概述
- 查看"Cited by"进行影响力评估和追踪最新后续工作
- 使用引用提醒跟踪关键论文的新引用
- 使用 `source:Nature` 或 `source:Science` 按顶级期刊过滤
- 使用 `author:LastName` 按已知领域领袖搜索论文

**高级运算符**（完整列表见 `references/google_scholar_search.md`）：
```
"exact phrase"           # 精确短语匹配
author:lastname          # 按作者搜索
intitle:keyword          # 仅在标题中搜索
source:journal           # 搜索特定期刊
-exclude                 # 排除词汇
OR                       # 替代词汇
2020..2024              # 年份范围
```

**搜索示例**：
```
# 查找某主题的最新综述
"CRISPR" intitle:review 2023..2024

# 查找特定作者在某主题的论文
author:Church "synthetic biology"

# 查找高被引基础性工作
"deep learning" 2012..2015 sort:citations

# 排除调查并专注于方法
"protein folding" -survey -review intitle:method
```

### PubMed 最佳实践

**使用 MeSH 术语**：
MeSH（医学主题词）提供受控词汇以实现精确搜索。

1. 在 https://meshb.nlm.nih.gov/search **查找 MeSH 术语**
2. **在查询中使用**：`"Diabetes Mellitus, Type 2"[MeSH]`
3. **与关键词结合**以实现全面覆盖

**字段标签**：
```
[Title]              # 仅在标题中搜索
[Title/Abstract]     # 在标题或摘要中搜索
[Author]             # 按作者姓名搜索
[Journal]            # 搜索特定期刊
[Publication Date]   # 日期范围
[Publication Type]   # 文章类型
[MeSH]              # MeSH 术语
```

**构建复杂查询**：
```bash
# 最近发表的糖尿病治疗临床试验
"Diabetes Mellitus, Type 2"[MeSH] AND "Drug Therapy"[MeSH] 
AND "Clinical Trial"[Publication Type] AND 2020:2024[Publication Date]

# 特定期刊中关于 CRISPR 的综述
"CRISPR-Cas Systems"[MeSH] AND "Nature"[Journal] AND "Review"[Publication Type]

# 特定作者的近期工作
"Smith AB"[Author] AND cancer[Title/Abstract] AND 2022:2024[Publication Date]
```

**E-utilities 自动化**：
脚本使用 NCBI E-utilities API 进行程序化访问：
- **ESearch**：搜索并检索 PMID
- **EFetch**：检索完整元数据
- **ESummary**：获取摘要信息
- **ELink**：查找相关文章

完整 API 文档请参见 `references/pubmed_search.md`。

## 工具与脚本

### search_google_scholar.py

搜索 Google Scholar 并导出结果。

**功能**：
- 带速率限制的自动搜索
- 分页支持
- 年份范围过滤
- 导出为 JSON 或 BibTeX
- 引用次数信息

**用法**：
```bash
# 基本搜索
python scripts/search_google_scholar.py "quantum computing"

# 带过滤器的高级搜索
python scripts/search_google_scholar.py "quantum computing" \
  --year-start 2020 \
  --year-end 2024 \
  --limit 100 \
  --sort-by citations \
  --output quantum_papers.json

# 直接导出为 BibTeX
python scripts/search_google_scholar.py "machine learning" \
  --limit 50 \
  --format bibtex \
  --output ml_papers.bib
```

### search_pubmed.py

使用 E-utilities API 搜索 PubMed。

**功能**：
- 支持复杂查询（MeSH、字段标签、布尔）
- 日期范围过滤
- 出版物类型过滤
- 批量检索元数据
- 导出为 JSON 或 BibTeX

**用法**：
```bash
# 简单关键词搜索
python scripts/search_pubmed.py "CRISPR gene editing"

# 带过滤器的复杂查询
python scripts/search_pubmed.py \
  --query '"CRISPR-Cas Systems"[MeSH] AND "therapeutic"[Title/Abstract]' \
  --date-start 2020-01-01 \
  --date-end 2024-12-31 \
  --publication-types "Clinical Trial,Review" \
  --limit 200 \
  --output crispr_therapeutic.json

# 导出为 BibTeX
python scripts/search_pubmed.py "Alzheimer's disease" \
  --limit 100 \
  --format bibtex \
  --output alzheimers.bib
```

### extract_metadata.py

从论文标识符提取完整元数据。

**功能**：
- 支持 DOI、PMID、arXiv ID、URL
- 查询 CrossRef、PubMed、arXiv API
- 处理多种标识符类型
- 批量处理
- 多种输出格式

**用法**：
```bash
# 单个 DOI
python scripts/extract_metadata.py --doi 10.1038/s41586-021-03819-2

# 单个 PMID
python scripts/extract_metadata.py --pmid 34265844

# 单个 arXiv ID
python scripts/extract_metadata.py --arxiv 2103.14030

# 从 URL
python scripts/extract_metadata.py \
  --url "https://www.nature.com/articles/s41586-021-03819-2"

# 批量处理（文件中每行一个标识符）
python scripts/extract_metadata.py \
  --input paper_ids.txt \
  --output references.bib

# 不同输出格式
python scripts/extract_metadata.py \
  --doi 10.1038/nature12345 \
  --format json  # 或 bibtex、yaml
```

### validate_citations.py

验证 BibTeX 条目的准确性和完整性。

**功能**：
- 通过 doi.org 和 CrossRef 验证 DOI
- 必填字段检查
- 重复检测
- 格式验证
- 自动修复常见问题
- 详细报告

**用法**：
```bash
# 基本验证
python scripts/validate_citations.py references.bib

# 带自动修复
python scripts/validate_citations.py references.bib \
  --auto-fix \
  --output fixed_references.bib

# 详细验证报告
python scripts/validate_citations.py references.bib \
  --report validation_report.json \
  --verbose

# 仅检查 DOI
python scripts/validate_citations.py references.bib \
  --check-dois-only
```

### format_bibtex.py

格式化和清理 BibTeX 文件。

**功能**：
- 标准化格式
- 排序条目（按键、年份、作者）
- 删除重复项
- 验证语法
- 修复常见错误
- 强制引用键约定

**用法**：
```bash
# 基本格式化
python scripts/format_bibtex.py references.bib

# 按年份排序（最新优先）
python scripts/format_bibtex.py references.bib \
  --sort year \
  --descending \
  --output sorted_refs.bib

# 删除重复项
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --output clean_refs.bib

# 完整清理
python scripts/format_bibtex.py references.bib \
  --deduplicate \
  --sort year \
  --validate \
  --auto-fix \
  --output final_refs.bib
```

### doi_to_bibtex.py

快速 DOI 转 BibTeX。

**功能**：
- 快速单个 DOI 转换
- 批量处理
- 多种输出格式
- 剪贴板支持

**用法**：
```bash
# 单个 DOI
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2

# 多个 DOI
python scripts/doi_to_bibtex.py \
  10.1038/nature12345 \
  10.1126/science.abc1234 \
  10.1016/j.cell.2023.01.001

# 从文件（每行一个 DOI）
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# 复制到剪贴板
python scripts/doi_to_bibtex.py 10.1038/nature12345 --clipboard
```

## 最佳实践

### 搜索策略

1. **先广后窄**：
   - 从通用术语开始以了解领域
   - 用特定关键词和过滤器细化
   - 使用同义词和相关术语

2. **使用多个来源**：
   - Google Scholar 用于全面覆盖
   - PubMed 用于生物医学重点
   - arXiv 用于预印本
   - 合并结果以实现完整性

3. **利用引用**：
   - 查看"Cited by"查找开创性论文
   - 查看关键论文的参考文献
   - 使用引用网络发现相关工作

4. **记录您的搜索**：
   - 保存搜索查询和日期
   - 记录结果数量
   - 注明应用的任何过滤器或限制

### 元数据提取

1. **有 DOI 时始终使用 DOI**：
   - 最可靠的标识符
   - 出版物的永久链接
   - 通过 CrossRef 获取最佳元数据来源

2. **验证提取的元数据**：
   - 检查作者姓名是否正确
   - 验证期刊/会议名称
   - 确认出版年份
   - 验证页码和卷号

3. **处理边缘情况**：
   - 预印本：包含存储库和 ID
   - 后来发表的预印本：使用发表版本
   - 会议论文：包含会议名称和地点
   - 书籍章节：包含书名和编辑

4. **保持一致性**：
   - 使用一致的作者姓名格式
   - 标准化期刊缩写
   - 使用相同的 DOI 格式（首选 URL）

### BibTeX 质量

1. **遵循约定**：
   - 使用有意义的引用键（FirstAuthor2024keyword）
   - 用 {} 保护标题中的大写
   - 页码范围使用 --（而非单个短横线）
   - 所有现代出版物包含 DOI 字段

2. **保持整洁**：
   - 删除不必要的字段
   - 无冗余信息
   - 格式一致
   - 定期验证语法

3. **系统化组织**：
   - 按年份或主题排序
   - 分组相关论文
   - 不同项目使用单独文件
   - 谨慎合并以避免重复

### 验证

1. **尽早且经常验证**：
   - 添加引用时检查
   - 提交前验证完整参考文献
   - 任何手动编辑后重新验证

2. **及时修复问题**：
   - 损坏的 DOI：查找正确标识符
   - 缺失字段：从原始来源提取
   - 重复项：选择最佳版本，删除其他
   - 格式错误：安全时使用自动修复

3. **对关键引用进行手动审查**：
   - 验证关键论文引用正确
   - 检查作者姓名与出版物匹配
   - 确认页码和卷号
   - 确保 URL 是最新的

## 常见陷阱及避免方法

1. **单一来源偏见**：仅使用 Google Scholar 或 PubMed
   - **解决方案**：搜索多个数据库以实现全面覆盖

2. **盲目接受元数据**：不验证提取的信息
   - **解决方案**：抽查提取的元数据与原始来源

3. **忽略 DOI 错误**：参考文献中的损坏或错误 DOI
   - **解决方案**：最终提交前运行验证

4. **格式不一致**：混合引用键样式、格式
   - **解决方案**：使用 format_bibtex.py 标准化

5. **重复条目**：同一论文以不同键被多次引用
   - **解决方案**：在验证中使用重复检测

6. **缺失必填字段**：不完整的 BibTeX 条目
   - **解决方案**：验证并确保所有必填字段存在

7. **过时的预印本**：当存在发表版本时引用预印本
   - **解决方案**：检查预印本是否已发表，更新为期刊版本

8. **特殊字符问题**：因字符导致 LaTeX 编译失败
   - **解决方案**：在 BibTeX 中使用正确的转义或 Unicode

9. **提交前无验证**：带引用错误提交
   - **解决方案**：始终运行验证作为最终检查

10. **手动 BibTeX 条目**：手工输入条目
    - **解决方案**：始终使用脚本从元数据来源提取

## 示例工作流程

### 示例 1：为论文构建参考文献

```bash
# 步骤 1：查找您主题的关键论文
python scripts/search_google_scholar.py "transformer neural networks" \
  --year-start 2017 \
  --limit 50 \
  --output transformers_gs.json

python scripts/search_pubmed.py "deep learning medical imaging" \
  --date-start 2020 \
  --limit 50 \
  --output medical_dl_pm.json

# 步骤 2：从搜索结果提取元数据
python scripts/extract_metadata.py \
  --input transformers_gs.json \
  --output transformers.bib

python scripts/extract_metadata.py \
  --input medical_dl_pm.json \
  --output medical.bib

# 步骤 3：添加您已知道的特定论文
python scripts/doi_to_bibtex.py 10.1038/s41586-021-03819-2 >> specific.bib
python scripts/doi_to_bibtex.py 10.1126/science.aam9317 >> specific.bib

# 步骤 4：合并所有 BibTeX 文件
cat transformers.bib medical.bib specific.bib > combined.bib

# 步骤 5：格式化和去重
python scripts/format_bibtex.py combined.bib \
  --deduplicate \
  --sort year \
  --descending \
  --output formatted.bib

# 步骤 6：验证
python scripts/validate_citations.py formatted.bib \
  --auto-fix \
  --report validation.json \
  --output final_references.bib

# 步骤 7：查看任何问题
cat validation.json | grep -A 3 '"errors"'

# 步骤 8：在 LaTeX 中使用
# \bibliography{final_references}
```

### 示例 2：转换 DOI 列表

```bash
# 您有一个包含 DOI 的文本文件（每行一个）
# dois.txt 包含：
# 10.1038/s41586-021-03819-2
# 10.1126/science.aam9317
# 10.1016/j.cell.2023.01.001

# 全部转换为 BibTeX
python scripts/doi_to_bibtex.py --input dois.txt --output references.bib

# 验证结果
python scripts/validate_citations.py references.bib --verbose
```

### 示例 3：清理现有 BibTeX 文件

```bash
# 您有一个来自各种来源的混乱 BibTeX 文件
# 系统化清理

# 步骤 1：格式化和标准化
python scripts/format_bibtex.py messy_references.bib \
  --output step1_formatted.bib

# 步骤 2：删除重复项
python scripts/format_bibtex.py step1_formatted.bib \
  --deduplicate \
  --output step2_deduplicated.bib

# 步骤 3：验证和自动修复
python scripts/validate_citations.py step2_deduplicated.bib \
  --auto-fix \
  --output step3_validated.bib

# 步骤 4：按年份排序
python scripts/format_bibtex.py step3_validated.bib \
  --sort year \
  --descending \
  --output clean_references.bib

# 步骤 5：最终验证报告
python scripts/validate_citations.py clean_references.bib \
  --report final_validation.json \
  --verbose

# 查看报告
cat final_validation.json
```

### 示例 4：查找和引用开创性论文

```bash
# 查找某主题的高被引论文
python scripts/search_google_scholar.py "AlphaFold protein structure" \
  --year-start 2020 \
  --year-end 2024 \
  --sort-by citations \
  --limit 20 \
  --output alphafold_seminal.json

# 按引用次数提取前 10 篇
# （脚本将在 JSON 中包含引用次数）

# 转换为 BibTeX
python scripts/extract_metadata.py \
  --input alphafold_seminal.json \
  --output alphafold_refs.bib

# BibTeX 文件现在包含最具影响力的论文
```

## 与其他技能集成

### 文献综述技能

**引用管理**为**文献综述**提供技术基础设施：

- **文献综述**：多数据库系统化搜索和综合
- **引用管理**：元数据提取和验证

**组合工作流程**：
1. 使用 literature-review 进行系统化搜索方法论
2. 使用 citation-management 提取和验证引用
3. 使用 literature-review 综合发现
4. 使用 citation-management 确保参考文献准确性

### 科学写作技能

**引用管理**为**科学写作**确保准确的参考文献：

- 为 LaTeX 稿件导出验证过的 BibTeX
- 验证引用符合出版标准
- 按期刊要求格式化参考文献

### 期刊模板技能

**引用管理**与**期刊模板**配合生成可提交的稿件：

- 不同期刊需要不同的引用格式
- 生成格式正确的参考文献
- 验证引用符合期刊要求

## 资源

### 内置资源

**参考文档**（位于 `references/`）：
- `google_scholar_search.md`：完整 Google Scholar 搜索指南
- `pubmed_search.md`：PubMed 和 E-utilities API 文档
- `metadata_extraction.md`：元数据来源和字段要求
- `citation_validation.md`：验证标准和质量检查
- `bibtex_formatting.md`：BibTeX 条目类型和格式化规则

**脚本**（位于 `scripts/`）：
- `search_google_scholar.py`：Google Scholar 搜索自动化
- `search_pubmed.py`：PubMed E-utilities API 客户端
- `extract_metadata.py`：通用元数据提取器
- `validate_citations.py`：引用验证和核实
- `format_bibtex.py`：BibTeX 格式化和清理
- `doi_to_bibtex.py`：快速 DOI 转 BibTeX 转换器

**资产**（位于 `assets/`）：
- `bibtex_template.bib`：所有类型的示例 BibTeX 条目
- `citation_checklist.md`：质量保证检查清单

### 外部资源

**搜索引擎**：
- Google Scholar: https://scholar.google.com/
- PubMed: https://pubmed.ncbi.nlm.nih.gov/
- PubMed Advanced Search: https://pubmed.ncbi.nlm.nih.gov/advanced/

**元数据 API**：
- CrossRef API: https://api.crossref.org/
- PubMed E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- arXiv API: https://arxiv.org/help/api/
- DataCite API: https://api.datacite.org/

**工具和验证器**：
- MeSH Browser: https://meshb.nlm.nih.gov/search
- DOI Resolver: https://doi.org/
- BibTeX Format: http://www.bibtex.org/Format/

**引用格式**：
- BibTeX 文档: http://www.bibtex.org/
- LaTeX 参考文献管理: https://www.overleaf.com/learn/latex/Bibliography_management

## 依赖

### 必需的 Python 包

```bash
# 核心依赖
pip install requests  # 用于 API 的 HTTP 请求
pip install bibtexparser  # BibTeX 解析和格式化
pip install biopython  # PubMed E-utilities 访问

# 可选（用于 Google Scholar）
pip install scholarly  # Google Scholar API 包装器
# 或
pip install selenium  # 用于更稳健的 Scholar 抓取
```

### 可选工具

```bash
# 用于高级验证
pip install crossref-commons  # 增强的 CrossRef API 访问
pip install pylatexenc  # LaTeX 特殊字符处理
```

## 总结

citation-management 技能提供：

1. **全面的搜索能力**，支持 Google Scholar 和 PubMed
2. **自动化元数据提取**，支持 DOI、PMID、arXiv ID、URL
3. **引用验证**，包含 DOI 核实和完整性检查
4. **BibTeX 格式化**，提供标准化和清理工具
5. **质量保证**，通过验证和报告实现
6. **集成**，支持科学写作工作流程
7. **可复现性**，通过文档化的搜索和提取方法实现

使用本技能在整个研究过程中维护准确、完整的引用，并确保参考文献达到出版就绪状态。

## 局限性
- 仅当任务明显符合上述描述的范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
