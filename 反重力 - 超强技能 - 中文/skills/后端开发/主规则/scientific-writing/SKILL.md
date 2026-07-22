---
name: scientific-writing
description: "这是深度研究与写作工具的核心技能——将 AI 驱动的深度研究与格式规范的书面输出相结合。每份生成的文档都基于 comprehensive 文献检索，并通过 research-lookup 技能进行引文验证。触发词：科学写作、学术写作、论文撰写、IMRAD、SCI论文、期刊投稿、学术论文、研究论文、学术写作指导、论文格式化、引用管理、学术报告"
license: MIT license
metadata:
    skill-author: K-Dense Inc.
risk: unknown
source: community
---

# 科学写作

## 概述

**这是深度研究与写作工具的核心技能**——将 AI 驱动的深度研究与格式规范的书面输出相结合。每份生成的文档都基于全面的文献检索，并通过 research-lookup 技能进行引文验证。

科学写作是以精确和清晰的方式交流研究成果的过程。使用 IMRAD 结构撰写稿件，包括引用（APA/AMA/Vancouver）、图表，以及报告规范（CONSORT/STROBE/PRISMA）。将此技能应用于研究论文和期刊投稿。

**核心原则：始终以完整的段落和流畅的散文撰写。绝不在最终稿件中提交要点列表。** 采用两阶段流程：首先使用 research-lookup 创建包含关键要点的章节大纲，然后将这些大纲转化为完整的段落。

## 何时使用此技能

在以下情况下使用此技能：
- 撰写或修改科学稿件的任何章节（摘要、引言、方法、结果、讨论）
- 使用 IMRAD 或其他标准格式构建研究论文
- 按特定格式设置引用和参考文献（APA、AMA、Vancouver、Chicago、IEEE）
- 创建、格式化或改进图表、表格和数据可视化
- 应用研究特定的报告规范（CONSORT 用于试验，STROBE 用于观察性研究，PRISMA 用于综述）
- 撰写符合期刊要求的摘要（结构化或非结构化）
- 准备投稿至特定期刊的稿件
- 提高写作的清晰度、简洁性和精确性
- 确保正确使用领域特定术语和命名规范
- 回应审稿意见并修改稿件

## 使用科学示意图增强视觉效果

**⚠️ 强制要求：每篇科学论文必须包含一张图形摘要，外加 1-2 张使用 scientific-schematics 技能生成的 AI 图片。**

这不是可选项。缺少视觉元素的科学论文是不完整的。在最终定稿前：
1. **必须首先生成图形摘要**作为第一个视觉元素
2. 至少使用 scientific-schematics 生成一张额外的示意图或图表
3. 综合性论文建议 3-4 张图片（图形摘要 + 方法流程图 + 结果可视化 + 概念图）

### 图形摘要（必需）

**每篇科学论文必须包含图形摘要。** 这是论文的视觉摘要，要求：
- 出现在文字摘要之前或紧随其后
- 用一张图捕捉整篇论文的核心信息
- 适合期刊目录展示
- 使用横向版式（通常 1200x600px）

**首先生成图形摘要：**
```bash
python scripts/generate_schematic.py "Graphical abstract for [paper title]: [brief description showing workflow from input → methods → key findings → conclusions]" -o figures/graphical_abstract.png
```

**图形摘要要求：**
- **内容**：展示工作流程、关键方法、主要发现和结论的视觉摘要
- **风格**：简洁、专业、适合期刊目录
- **元素**：包含 3-5 个关键步骤/概念，配有连接箭头或流程线
- **文字**：最少标签，大号可读字体
- 日志：`[HH:MM:SS] GENERATED: Graphical abstract for paper summary`

### 额外图片（大量生成）

**⚠️ 关键：在整个文档中广泛使用 scientific-schematics 和 generate-image。**

每份文档都应配以丰富的插图。大方地生成图片——拿不准时，就加一张图。

**最低图片要求：**

| 文档类型 | 最少数量 | 建议数量 |
|---------|---------|---------|
| 研究论文 | 5 | 6-8 |
| 文献综述 | 4 | 5-7 |
| 市场研究 | 20 | 25-30 |
| 演示文稿 | 每张幻灯片 1 张 | 每张幻灯片 1-2 张 |
| 海报 | 6 | 8-10 |
| 基金申请 | 4 | 5-7 |
| 临床报告 | 3 | 4-6 |

**广泛使用 scientific-schematics 制作技术图表：**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

- 研究设计和方法学流程图（CONSORT、PRISMA、STROBE）
- 概念框架图
- 实验工作流程图
- 数据分析流程图
- 生物通路或机制图
- 系统架构可视化
- 神经网络架构
- 决策树、算法流程图
- 对比矩阵、时间线图
- 任何适合示意图可视化的技术概念

**广泛使用 generate-image 制作视觉内容：**
```bash
python scripts/generate_image.py "your image description" -o figures/output.png
```

- 概念的写实插图
- 医学/解剖学插图
- 环境/生态场景
- 设备和实验室设置可视化
- 艺术可视化、信息图
- 封面图片、题图
- 产品模型、原型可视化
- 任何增强理解或参与度的视觉元素

AI 将自动：
- 创建具有适当格式的出版级图片
- 通过多次迭代审查和优化
- 确保无障碍性（色盲友好、高对比度）
- 将输出保存到 figures/ 目录

**拿不准时，就生成图片：**
- 复杂概念 → 生成示意图
- 数据讨论 → 生成可视化
- 流程描述 → 生成流程图
- 对比分析 → 生成对比图
- 读者受益 → 生成视觉元素

详细指导请参考 scientific-schematics 和 generate-image 技能文档。

---

## 核心能力

### 1. 稿件结构与组织

**IMRAD 格式**：引导论文遵循大多数科学学科使用的标准引言（Introduction）、方法（Methods）、结果（Results）和讨论（And Discussion）结构。包括：
- **引言**：建立研究背景，识别知识空白，陈述研究目标
- **方法**：详细说明研究设计、人群、程序和分析方法
- **结果**：客观呈现研究发现，不做解释
- **讨论**：解释结果，承认局限性，提出未来方向

有关 IMRAD 结构的详细指导，请参阅 `references/imrad_structure.md`。

**替代结构**：支持学科特定格式，包括：
- 综述文章（叙述性、系统性、范围综述）
- 病例报告和病例系列
- Meta 分析和汇总分析
- 理论/建模论文
- 方法学论文和方案

### 2. 各章节写作指导

**摘要撰写**：撰写简洁、独立的摘要（100-250 词），涵盖论文的目的、方法、结果和结论。支持结构化摘要（带标记章节）和非结构化单段格式。

**引言撰写**：构建引人入胜的引言：
- 确立研究问题的重要性
- 系统回顾相关文献
- 识别知识空白或争议
- 提出明确的研究问题或假设
- 阐明研究的创新性和意义

**方法文档**：确保可重复性：
- 详细的参与者/样本描述
- 清晰的程序文档
- 带有论证的统计方法
- 设备和材料规格
- 伦理批准和知情同意声明

**结果呈现**：以以下方式呈现发现：
- 从主要结局到次要结局的逻辑流程
- 与图表的整合
- 带有效应量的统计显著性
- 不含解释的客观报告

**讨论撰写**：综合研究发现：
- 将结果与研究问题关联
- 与现有文献比较
- 诚实地承认局限性
- 提出机制解释
- 建议实际意义和未来研究

### 3. 引用和参考文献管理

在各学科间正确应用引用格式。详细的格式指南请参阅 `references/citation_styles.md`。

**主要引用格式：**
- **AMA（美国医学会）**：上标数字引用，常见于医学领域
- **Vancouver**：方括号数字引用，生物医学标准
- **APA（美国心理学会）**：正文作者-日期引用，常见于社会科学
- **Chicago**：注释-参考文献或作者-日期格式，人文学科和科学领域
- **IEEE**：方括号数字引用，工程和计算机科学

**最佳实践：**
- 尽可能引用原始来源
- 包含近期文献（活跃领域近 5-10 年）
- 在引言和讨论中平衡引用分布
- 核实所有引用与原始来源一致
- 使用参考文献管理软件（Zotero、Mendeley、EndNote）

### 4. 图表

创建有效的数据可视化以增强理解。详细的最佳实践请参阅 `references/figures_tables.md`。

**何时使用表格 vs. 图片：**
- **表格**：精确数值数据、复杂数据集、需要精确值的多变量
- **图片**：趋势、模式、关系、适合视觉理解的比较

**设计原则：**
- 每个表格/图片都应配有完整标题，做到自解释
- 在所有展示项中使用一致的格式和术语
- 为所有坐标轴、列和行标注单位
- 包含样本量 (n) 和统计注释
- 遵循"每 1000 字一个表格/图片"的指导原则
- 避免在正文、表格和图片之间重复信息

**常见图表类型：**
- 柱状图：比较离散类别
- 折线图：展示随时间变化的趋势
- 散点图：展示相关性
- 箱线图：展示分布和异常值
- 热力图：可视化矩阵和模式

### 5. 按研究类型分类的报告规范

遵循既定的报告标准以确保完整性和透明度。详细的规范内容请参阅 `references/reporting_guidelines.md`。

**关键规范：**
- **CONSORT**：随机对照试验
- **STROBE**：观察性研究（队列、病例对照、横断面）
- **PRISMA**：系统综述和 Meta 分析
- **STARD**：诊断准确性研究
- **TRIPOD**：预测模型研究
- **ARRIVE**：动物研究
- **CARE**：病例报告
- **SQUIRE**：质量改进研究
- **SPIRIT**：临床试验研究方案
- **CHEERS**：经济学评价

每项规范提供检查清单，确保所有关键方法学要素都被报告。

### 6. 写作原则和风格

应用基本的科学写作原则。详细指导请参阅 `references/writing_principles.md`。

**清晰性**：
- 使用精确、无歧义的语言
- 首次使用时定义技术术语和缩写
- 保持段落内部和段落之间的逻辑流畅
- 适当时使用主动语态以增强清晰度

**简洁性**：
- 消除冗余词语和短语
- 优先使用较短的句子（平均 15-20 词）
- 删除不必要的修饰词
- 严格遵守字数限制

**准确性**：
- 以适当的精度报告精确数值
- 全文使用一致的术语
- 区分观察结果和解释
- 适当地承认不确定性

**客观性**：
- 无偏差地呈现结果
- 避免过度陈述发现或意义
- 承认相互矛盾的证据
- 保持专业、中立的语气

### 7. 写作过程：从大纲到完整段落

**关键要求：始终以完整段落撰写，绝不在科学论文中提交要点列表。**

科学论文必须以完整、流畅的散文撰写。使用以下两阶段方法进行有效写作：

**第一阶段：创建包含关键要点的章节大纲**

开始新章节时：
1. 使用 research-lookup 技能收集相关文献和数据
2. 创建结构化大纲，用要点标记：
   - 要呈现的主要论点或发现
   - 要引用的关键研究
   - 要包含的数据点和统计数据
   - 逻辑流程和组织
3. 这些要点仅作为脚手架——它们不是最终稿件

**大纲示例（引言部分）：**
```
- Background: AI in drug discovery gaining traction
  * Cite recent reviews (Smith 2023, Jones 2024)
  * Traditional methods are slow and expensive
- Gap: Limited application to rare diseases
  * Only 2 prior studies (Lee 2022, Chen 2023)
  * Small datasets remain a challenge
- Our approach: Transfer learning from common diseases
  * Novel architecture combining X and Y
- Study objectives: Validate on 3 rare disease datasets
```

**第二阶段：将关键要点转化为完整段落**

大纲完成后，将每个要点扩展为正式的散文：

1. **将要点转化为完整的句子**，包含主语、谓语和宾语
2. **添加过渡语**连接句子和思想（然而、此外、相比之下、随后）
3. **自然地融入引用**到句子中，而非作为列表
4. **用上下文和解释扩展**要点中省略的内容
5. **确保逻辑流畅**，每个段落内句子之间衔接自然
6. **变换句式结构**以保持读者兴趣

**转化为散文的示例：**

```
Artificial intelligence approaches have gained significant traction in drug discovery 
pipelines over the past decade (Smith, 2023; Jones, 2024). While these computational 
methods show promise for accelerating the identification of therapeutic candidates, 
traditional experimental approaches remain slow and resource-intensive, often requiring 
years of laboratory work and substantial financial investment. However, the application 
of AI to rare diseases has been limited, with only two prior studies demonstrating 
proof-of-concept results (Lee, 2022; Chen, 2023). The primary obstacle has been the 
scarcity of training data for conditions affecting small patient populations. 

To address this challenge, we developed a transfer learning approach that leverages 
knowledge from well-characterized common diseases to predict therapeutic targets for 
rare conditions. Our novel neural architecture combines convolutional layers for 
molecular feature extraction with attention mechanisms for protein-ligand interaction 
modeling. The objective of this study was to validate our approach across three 
independent rare disease datasets, assessing both predictive accuracy and biological 
interpretability of the results.
```

**大纲与最终文本的关键区别：**

| 大纲（规划阶段） | 最终稿件 |
|-----------------|---------|
| 要点和片段 | 完整的句子和段落 |
| 电报式笔记 | 带上下文的完整解释 |
| 引用列表 | 融入散文的引用 |
| 简略的想法 | 带过渡语的展开论证 |
| 仅供自己参考 | 供发表和同行评审 |

**应避免的常见错误：**

- ❌ **绝不**在最终稿件中保留要点列表
- ❌ **绝不**在应为段落的地方提交列表
- ❌ **不要**在结果或讨论部分使用编号或项目符号列表（研究假设或纳入标准等特定情况除外）
- ❌ **不要**写句子片段或不完整的想法
- ✅ **可以**仅在方法部分偶尔使用列表（如纳入/排除标准、材料清单）
- ✅ **确保**每个章节以连贯的散文形式呈现
- ✅ **朗读**段落以检查自然流畅度

**列表可接受的有限情况：**

列表仅在以下特定情境中可出现在科学论文中：
- **方法部分**：纳入/排除标准、材料和试剂、参与者特征
- **补充材料**：扩展方案、设备清单、详细参数
- **绝不出现于**：摘要、引言、结果、讨论、结论

**摘要格式规则：**
- ❌ **绝不**使用标记章节（Background:、Methods:、Results:、Conclusions:）
- ✅ **始终**以带有自然过渡的流畅段落撰写
- 例外：仅当期刊作者指南明确要求时才使用结构化格式

**与 Research Lookup 的整合：**

research-lookup 技能对第一阶段（创建大纲）至关重要：
1. 使用 research-lookup 搜索相关论文
2. 提取关键发现、方法和数据
3. 将发现组织为大纲中的要点
4. 然后在第二阶段将大纲转化为完整段落

这个两阶段流程确保你：
- 系统地收集和组织信息
- 在写作前创建逻辑结构
- 产出精炼的、可发表的散文
- 保持叙述流程的连贯性

### 8. 专业报告格式化（非期刊文档）

对于研究报告、技术报告、白皮书和其他非期刊稿件的专业文档，使用 `scientific_report.sty` LaTeX 样式包实现精炼、专业的外观。

**何时使用专业报告格式化：**
- 研究报告和技术报告
- 白皮书和政策简报
- 基金报告和进展报告
- 行业报告和技术文档
- 内部研究摘要
- 可行性研究和项目交付物

**何时不使用（改用特定场合格式化）：**
- 期刊稿件 → 使用 `venue-templates` 技能
- 会议论文 → 使用 `venue-templates` 技能
- 学术论文 → 使用机构模板

**`scientific_report.sty` 样式包提供：**

| 功能 | 描述 |
|-----|------|
| 排版 | Helvetica 字体家族，现代、专业的外观 |
| 配色方案 | 专业的蓝色、绿色和强调色 |
| 方框环境 | 彩色方框用于关键发现、方法、建议、局限性 |
| 表格 | 交替行颜色、专业表头 |
| 图片 | 一致的标题格式 |
| 科学命令 | p 值、效应量、置信区间的快捷命令 |

**用于内容组织的方框环境：**

```latex
% Key findings (blue) - for major discoveries
\begin{keyfindings}[Title]
Content with key findings and statistics.
\end{keyfindings}

% Methodology (green) - for methods highlights
\begin{methodology}[Study Design]
Description of methods and procedures.
\end{methodology}

% Recommendations (purple) - for action items
\begin{recommendations}[Clinical Implications]
\begin{enumerate}
    \item Specific recommendation 1
    \item Specific recommendation 2
\end{enumerate}
\end{recommendations}

% Limitations (orange) - for caveats and cautions
\begin{limitations}[Study Limitations]
Description of limitations and their implications.
\end{limitations}
```

**专业表格格式化：**

```latex
\begin{table}[htbp]
\centering
\caption{Results Summary}
\begin{tabular}{@{}lccc@{}}
\toprule
\textbf{Variable} & \textbf{Treatment} & \textbf{Control} & \textbf{p} \\
\midrule
Outcome 1 & \meansd{42.5}{8.3} & \meansd{35.2}{7.9} & <.001\sigthree \\
\rowcolor{tablealt} Outcome 2 & \meansd{3.8}{1.2} & \meansd{3.1}{1.1} & .012\sigone \\
Outcome 3 & \meansd{18.2}{4.5} & \meansd{17.8}{4.2} & .58\signs \\
\bottomrule
\end{tabular}

{\small \siglegend}
\end{table}
```

**科学记数法命令：**

| 命令 | 输出 | 用途 |
|------|------|------|
| `\pvalue{0.023}` | *p* = 0.023 | p 值 |
| `\psig{< 0.001}` | ***p* = < 0.001** | 显著 p 值（粗体） |
| `\CI{0.45}{0.72}` | 95% CI [0.45, 0.72] | 置信区间 |
| `\effectsize{d}{0.75}` | d = 0.75 | 效应量 |
| `\samplesize{250}` | *n* = 250 | 样本量 |
| `\meansd{42.5}{8.3}` | 42.5 ± 8.3 | 均值 ± 标准差 |
| `\sigone`, `\sigtwo`, `\sigthree` | *, **, *** | 显著性星号 |

**快速开始：**

```latex
\documentclass[11pt,letterpaper]{report}
\usepackage{scientific_report}

\begin{document}
\makereporttitle
    {Report Title}
    {Subtitle}
    {Author Name}
    {Institution}
    {Date}

% Your content with professional formatting
\end{document}
```

**编译**：使用 XeLaTeX 或 LuaLaTeX 以正确渲染 Helvetica 字体：
```bash
xelatex report.tex
```

完整文档请参阅：
- `assets/scientific_report.sty`：样式包
- `assets/scientific_report_template.tex`：完整模板示例
- `assets/REPORT_FORMATTING_GUIDE.md`：快速参考指南
- `references/professional_report_formatting.md`：完整格式化指南

### 9. 特定期刊格式化

将稿件调整为符合期刊要求：
- 遵循作者指南中的结构、长度和格式要求
- 应用特定期刊的引用格式
- 满足图表规格（分辨率、文件格式、尺寸）
- 包含必需的声明（资金、利益冲突、数据可用性、伦理批准）
- 遵守各章节的字数限制
- 按照提供的模板要求进行格式化

### 10. 领域特定语言和术语

将语言、术语和惯例与特定科学学科相匹配。每个领域都有既定的词汇、首选表述和领域特定惯例，用以表明专业性并确保目标受众的清晰理解。

**识别领域特定的语言惯例：**
- 查阅目标期刊近期高影响力论文中使用的术语
- 注意领域特定的缩写、单位和符号系统
- 识别首选术语（如"participants"vs."subjects"，"compound"vs."drug"，"specimens"vs."samples"）
- 观察方法、生物体或技术的典型描述方式

**生物医学和临床科学：**
- 使用精确的解剖学和临床术语（如正式写作中用"myocardial infarction"而非"heart attack"）
- 遵循标准化疾病命名法（ICD、DSM、SNOMED-CT）
- 药物名称先用通用名，需要时括号注明商品名
- 临床研究用"patients"，社区研究用"participants"
- 遵循人类基因组变异学会（HGVS）遗传变异命名法
- 使用标准单位报告实验室数值（国际期刊多用 SI 单位）

**分子生物学和遗传学：**
- 基因符号用斜体（如 *TP53*），蛋白质用正体（如 p53）
- 遵循物种特定的基因命名法（人类大写：*BRCA1*；小鼠句首大写：*Brca1*）
- 首次提及时写全生物体名称，之后使用公认缩写（如 *Escherichia coli*，之后 *E. coli*）
- 使用标准遗传学符号（如 +/+、+/-、-/- 表示基因型）
- 使用分子技术的既定术语（如"quantitative PCR"或"qPCR"，而非"real-time PCR"）

**化学和药学：**
- 遵循 IUPAC 化合物命名法
- 新化合物用系统命名，知名物质用通用名
- 使用标准符号指定化学结构（如数据库用 SMILES、InChI）
- 以适当单位报告浓度（mM、μM、nM，或 % w/v、v/v）
- 使用公认反应命名法描述合成路线
- 一致使用"bioavailability"、"pharmacokinetics"、"IC50"等领域定义术语

**生态学和环境科学：**
- 使用双名法命名物种（斜体：*Homo sapiens*）
- 首次提及物种时指定分类权威（相关时）
- 采用标准化的栖息地和生态系统分类
- 生态指标使用一致术语（如"species richness"、"Shannon diversity index"）
- 使用领域标准术语描述采样方法（如"transect"、"quadrat"、"mark-recapture"）

**物理学和工程学：**
- 一致使用 SI 单位，除非领域惯例另有规定
- 物理量使用标准符号（标量 vs. 向量、张量）
- 使用现象的既定术语（如"quantum entanglement"、"laminar flow"）
- 相关时注明设备型号和制造商
- 使用与领域标准一致的数学符号（如 ℏ 表示约化普朗克常数）

**神经科学：**
- 使用标准化脑区命名法（如参考 Allen Brain Atlas 等图谱）
- 使用既定的立体定位系统指定脑区坐标
- 遵循神经学术语惯例（如正式写作中用"action potential"而非"spike"）
- 根据测量方法恰当使用"neural activity"、"neuronal firing"、"brain activation"
- 以适当的精确度描述记录技术（如"whole-cell patch clamp"、"extracellular recording"）

**社会和行为科学：**
- 适当时使用以人为本的语言（如"people with schizophrenia"而非"schizophrenics"）
- 采用标准化心理构念和经验证的评估名称
- 遵循 APA 减少语言偏见的指南
- 使用既定术语指定理论框架
- 人类研究使用"participants"而非"subjects"

**一般原则：**

**匹配受众专业水平：**
- 专业期刊：自由使用领域特定术语，仅定义高度专业化或新颖的术语
- 高影响力期刊（如 *Nature*、*Science*）：定义更多技术术语，为专业概念提供背景
- 跨学科受众：平衡精确性和可及性，首次使用时定义术语

**策略性地定义技术术语：**
- 首次使用时定义缩写："messenger RNA (mRNA)"
- 面向更广泛受众时为专业技术提供简要解释
- 避免过度定义目标受众熟知的术语（表明对领域不熟悉）
- 如果不可避免地出现大量专业术语，创建术语表

**保持一致性：**
- 全文使用同一术语指代同一概念（不要在"medication"、"drug"和"pharmaceutical"之间交替使用）
- 缩写使用一致的体系（首次定义后决定使用"PCR"或"polymerase chain reaction"）
- 全文应用同一命名体系（尤其是基因、物种、化学品）

**避免领域混用错误：**
- 不要将临床术语用于基础科学（如不要称小鼠为"patients"）
- 避免用口语或过于笼统的术语替代精确的领域术语
- 不要从相邻领域引入术语而不确定其正确用法

**验证术语使用：**
- 查阅领域特定的风格指南和命名资源
- 检查目标期刊近期论文中术语的使用方式
- 使用领域特定的数据库和本体（如 Gene Ontology、MeSH 术语）
- 不确定时，引用建立该术语的关键参考文献

### 11. 应避免的常见陷阱

**主要拒稿原因：**
1. 统计方法不当、不完整或描述不足
2. 结果过度解释或结论缺乏支持
3. 方法描述不清影响可重复性
4. 样本量小、有偏倚或不当
5. 写作质量差或文本难以理解
6. 文献综述或背景不足
7. 图表不清晰或设计不佳
8. 未遵循报告规范

**写作质量问题：**
- 时态使用不当（方法/结果用过去时，既定事实用现在时）
- 过多术语或未定义的缩写
- 段落分割破坏逻辑流畅性
- 章节之间缺少过渡
- 符号或术语不一致

## 稿件开发工作流程

**第一阶段：规划**
1. 确定目标期刊并查阅作者指南
2. 确定适用的报告规范（CONSORT、STROBE 等）
3. 规划稿件结构（通常为 IMRAD）
4. 将图表作为论文的骨架进行规划

**第二阶段：起草**（每个章节使用两阶段写作流程）
1. 从图表开始（核心数据故事）
2. 对每个章节遵循两阶段流程：
   - **第一步**：使用 research-lookup 创建带要点的大纲
   - **第二步**：将要点转化为流畅散文的完整段落
3. 撰写方法（通常最容易先起草）
4. 起草结果（客观描述图表）
5. 撰写讨论（解释研究发现）
6. 撰写引言（建立研究问题）
7. 撰写摘要（综合完整故事）
8. 创建标题（简洁且描述性）

**记住**：要点仅用于规划——最终稿件必须是完整的段落。

**第三阶段：修订**
1. 检查全文的逻辑流畅性和"红线"
2. 验证术语和符号的一致性
3. 确保图表自解释
4. 确认遵循报告规范
5. 验证所有引用准确且格式正确
6. 检查各章节字数
7. 校对语法、拼写和清晰度

**第四阶段：最终准备**
1. 按期刊要求格式化
2. 准备补充材料
3. 撰写突出重要性的投稿信
4. 完成提交清单
5. 收集所有必需的声明和表格

## 与其他科学技能的整合

此技能可与以下技能有效配合：
- **数据分析技能**：用于生成要报告的结果
- **统计分析**：用于确定适当的统计呈现方式
- **文献综述技能**：用于将研究置于背景中
- **图表创建工具**：用于开发出版级可视化
- **venue-templates 技能**：用于特定场合的写作风格和格式化（期刊稿件）
- **scientific_report.sty**：用于专业报告、白皮书和技术文档

### 专业报告 vs. 期刊稿件

**选择正确的格式化方法：**

| 文档类型 | 格式化方法 |
|---------|-----------|
| 期刊稿件 | 使用 `venue-templates` 技能 |
| 会议论文 | 使用 `venue-templates` 技能 |
| 研究报告 | 使用 `scientific_report.sty`（本技能） |
| 白皮书 | 使用 `scientific_report.sty`（本技能） |
| 技术报告 | 使用 `scientific_report.sty`（本技能） |
| 基金报告 | 使用 `scientific_report.sty`（本技能） |

### 特定场合的写作风格

**在为特定期刊撰写前，查阅 venue-templates 技能获取写作风格指南：**

不同场合的写作期望差异巨大：
- **Nature/Science**：通俗易懂、故事驱动、广泛意义
- **Cell Press**：机制深度、图形摘要、亮点
- **医学期刊（NEJM、Lancet）**：结构化摘要、循证语言
- **ML 会议（NeurIPS、ICML）**：贡献要点、消融实验
- **CS 会议（CHI、ACL）**：领域特定惯例

venue-templates 技能提供：
- `venue_writing_styles.md`：主风格对比
- 特定场合指南：`nature_science_style.md`、`cell_press_style.md`、`medical_journal_styles.md`、`ml_conference_style.md`、`cs_conference_style.md`
- `reviewer_expectations.md`：各场合审稿人关注要点
- `assets/examples/` 中的写作示例

**工作流程**：首先使用本技能学习一般科学写作原则（IMRAD、清晰性、引用），然后查阅 venue-templates 进行特定场合的风格适配。

## 参考资料

此技能包含涵盖科学写作各方面的综合参考文件：

- `references/imrad_structure.md`：IMRAD 格式和章节特定内容的详细指南
- `references/citation_styles.md`：完整引用格式指南（APA、AMA、Vancouver、Chicago、IEEE）
- `references/figures_tables.md`：创建有效数据可视化的最佳实践
- `references/reporting_guidelines.md`：研究特定的报告标准和检查清单
- `references/writing_principles.md`：有效科学传播的核心原则
- `references/professional_report_formatting.md`：使用 `scientific_report.sty` 的专业报告样式指南

## 资源

此技能包含用于专业报告格式化的 LaTeX 样式包和模板：

- `assets/scientific_report.sty`：专业 LaTeX 样式包，包含 Helvetica 字体、彩色方框和美观表格
- `assets/scientific_report_template.tex`：展示所有样式功能的完整报告模板
- `assets/REPORT_FORMATTING_GUIDE.md`：样式包的快速参考指南

**`scientific_report.sty` 的主要特性：**
- Helvetica 字体家族，现代、专业的外观
- 专业配色方案（蓝色、绿色、橙色、紫色）
- 方框环境：`keyfindings`、`methodology`、`resultsbox`、`recommendations`、`limitations`、`criticalnotice`、`definition`、`executivesummary`、`hypothesis`
- 交替行颜色和专业表头的表格
- p 值、效应量、置信区间的科学记数法命令
- 专业的页眉和页脚

**有关特定场合的写作风格**（语气、语态、摘要格式、审稿人期望），请参阅 **venue-templates** 技能，它提供 Nature/Science、Cell Press、医学期刊、ML 会议和 CS 会议的综合风格指南。

在处理科学写作的特定方面时，按需加载这些参考资料。

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。