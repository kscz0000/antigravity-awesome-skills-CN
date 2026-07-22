---
name: cv-generator
description: "为 FlowCV、Canva、Google Docs 或 Word 生成专业、ATS 优化的简历。支持多来源合并、JD 定向匹配、资历适配和人化改写。输出可直接粘贴的文本，并附带 ATS 缺陷报告和改进建议。CV生成器、简历生成、ATS优化、FlowCV、Canva、求职简历"
category: content
risk: safe
source: community
date_added: "2026-06-06"
author: "WHOISABHISHEKADHIKARI"
user-invokable: true
tags:
  - cv
  - resume
  - ats
  - career
  - job-application
  - career-change
---

# 简历生成技能 — FlowCV / Canva 版

## 适用场景

以下情况使用本技能：
- 从多个来源（LinkedIn、GitHub、作品集）生成专业、ATS 优化的简历
- 针对具体职位描述（JD）调整现有简历
- 优化草稿简历的语言、数据指标和结构
- 为 FlowCV 或 Canva 等工具准备可直接粘贴的简历版本

将原始资料数据转化为打磨完成、可通过 ATS 的简历。输出为可直接粘贴的纯文本
版本，针对 FlowCV、Canva、Google Docs 或 Word 格式化，并附带缺陷报告和
信息缺失清单。

---

## 缺陷登记册 — 本版本已修复的已知问题

以下问题在前两版技能草稿中已被识别，并在此版本中修正：

| # | 缺陷 | 已应用的修复 |
|---|------|-------------|
| F-01 | 输出以 Markdown 为主，不是可直接粘贴的纯文本 | 最终输出为纯文本；Markdown 仅作内部中转 |
| F-02 | FlowCV/Canva 字段结构从未涉及 | 新增与工具字段的章节映射（第 11c 节） |
| F-03 | 问卷在实践中一次性抛出全部 20 个问题 | 硬性规则：每次只问一题，等待回答 |
| F-04 | 反幻觉规则虽列出但未结构性强制执行 | 在每次输出前加入强制门禁（第 10 节） |
| F-05 | 求职信虽被提供，但未针对这些工具进行范围限定 | 求职信现输出为独立纯文本块，而非内联 |
| F-06 | ATS 检查虽列出但无评分输出 | 缺陷报告现按 0–100 评分，并逐项显示通过/失败 |
| F-07 | 资历识别采用"识别或询问"，无回退方案 | 无法识别时默认中级；告知用户所做的假设 |
| F-08 | 缺少 FlowCV/Canva 无法渲染的内容指南 | 新增明确的逐字段粘贴映射（第 11c 节） |
| F-09 | 时态规则虽声明但未在质量门中校验 | 时态检查现为硬门禁 — 输出被阻止直至修正 |
| F-10 | "Passionate about" 等禁用短语仍出现在示例中 | 短语黑名单现可机器校验（第 7c 节） |
| F-11 | 尼泊尔/南亚市场惯例存在但不完整 | 已确认并扩展（第 14 节） |
| F-12 | LinkedIn 抓取受阻时无明确处理规则 | 硬性回退规则：立即要求 PDF 导出，不得空跑 |
| F-13 | 文件命名约定仅提及一次，从未强制执行 | 文件名规则纳入最终输出块（第 11 节） |
| F-14 | 技能无版本历史或升级路径 | 前置元数据新增版本字段 |
| F-15 | GitHub 被列为来源但缺少提取规则 | 新增 GitHub 提取规则（第 4f 节） |

---

## 1. 调用方式

```
Use @cv-generator to build my CV from my LinkedIn PDF.
Use @cv-generator to tailor my CV for this job description.
Use @cv-generator to improve my existing draft.
Use @cv-generator to create a fresh CV via questionnaire.
Use @cv-generator — I want a FlowCV-ready output.
```

任意来源组合均有效。多个来源在开始撰写前会进行合并与去重。

---

## 来源选择

询问用户使用哪些来源（至少一项必填）。
若未提供来源，立即默认采用问卷（第 4d 节）。

| # | 来源 | 说明 |
|---|--------|-------------|
| 1 | LinkedIn 个人主页 URL | 抓取页面；提取所有可见栏目。**若被拦截或为空：立即要求提供 LinkedIn PDF —— 不得在空提取下继续。** |
| 2 | LinkedIn PDF 导出 | 解析上传文件。若为扫描图像：使用 OCR 并提醒用户核验准确性。 |
| 3 | 作品集 / 个人网站 | 抓取 URL；提取关于、项目、技能、服务、客户评价、案例研究、联系方式。 |
| 4 | 问卷 | 逐步进行（第 4d 节）。每次一问。 |
| 5 | 现有简历或草稿 | 上传或粘贴；仅做优化 —— 绝不改动事实。 |
| 6 | GitHub 个人主页 | 提取置顶仓库、简介、技术栈、贡献摘要（第 4f 节）。 |
| 7 | 简历文件（DOCX / PDF / TXT） | 解析并重写。标记扫描版 PDF；使用 OCR。 |

---

## 用途、资历与格式

### 用途

在来源选择后询问：

> "这份简历的主要用途是什么？"

| 用途 | 关键适配 |
|---------|----------------|
| 申请特定职位 | 完整 JD 分析 + 关键词定向（第 9 节） |
| 通用专业简历 | 均衡、与职位无关、按时间倒序 |
| 实习 / 入门级 | 教育与项目先行；突出可迁移技能 |
| 学术 / 研究 | 发表论文、资助、教学、研究兴趣 |
| 自由职业 / 客户提案 | 交付物、成果、服务 |
| 转行 | 功能型或混合型；重新框定可迁移技能 |
| 高管 / 董事会级别 | 高管摘要、董事会职位、P&L 范围 |
| 军转民 | 将军衔和行话翻译为对应民用表达 |
| 重返职场 / 职业中断 | 正面描述空窗期；强调技能提升 |
| 其他 | 请用户用一句话描述目标 |

### 资历

从数据中识别。若无法识别，**默认中级并告知用户：**
> "我已假设为中级（3–8 年）。如有出入请告知。"

| 级别 | 年限 | 简历侧重点 |
|-------|-------|-------------|
| 应届生 / 刚毕业 | 0–1 | 教育居首；项目；课外活动；1 页 |
| 初级 / 入门 | 1–3 | 技能 + 教育突出；1 页 |
| 中级 | 3–8 | 经验主导；成果重于职责；1–2 页 |
| 高级 | 8–15 | 领导力、范围、影响、辅导；2 页 |
| 高管 / C 级 | 15+ | 战略叙事；董事会角色；P&L；2–3 页 |
| 学术 | 任意 | 无页数限制；发表论文；资助；教学 |

### 格式

| 格式 | 适用场景 |
|--------|----------|
| 时间顺序型（默认） | 清晰的职业晋升；多数求职申请 |
| 功能型 / 技能优先 | 转行者；较长空窗期；军转民 |
| 混合型 / 组合型 | 资深专业人士重塑品牌；经验丰富的转行者 |
| 学术型简历 | 大学、研究、博士、博士后 |
| 高管 / 董事会简介 | C 级、NED、顾问 |
| 作品集主导 | 设计师、建筑师、创意从业者 |

---

## 数据提取规则

### LinkedIn URL

若页面被拦截或返回无内容，**立即停止**并询问：
> "LinkedIn 拦截了抓取。请将你的 LinkedIn 个人资料导出为 PDF
> （LinkedIn → 我 → 设置 → 数据隐私 → 获取数据副本）并上传。"

若可访问，按以下顺序提取：
1. 全名与标题
2. 联系方式（邮箱、电话、地址 — 仅公开部分）
3. 关于 / 专业简介
4. 工作经历：职位、公司、地点、日期、要点
5. 教育：学位、院校、日期、成绩/荣誉
6. 技能（标记最受认可的技能）
7. 证书与执照
8. 项目
9. 成就、荣誉、奖项
10. 志愿者经历
11. 语言及熟练度
12. 发表、专利、课程

### LinkedIn PDF

硬性规则：
- 仅提取文件中实际存在的内容。
- 严格按原文保留所有日期。
- 若某节缺失，标记 **[Not provided]** —— 不得静默跳过。
- 不得合并不同角色的要点。
- 若为扫描件：使用 OCR 并在继续前显示以下警告：
  > "已使用 OCR 读取此文档。请在继续前核验以下提取文本的准确性。"

### 作品集 / 个人网站

提取：
- 关于 / 简介 → 专业简介
- 项目：名称、描述、技术、成果、上线/仓库链接
- 技能与服务
- 客户评价或客户标识 → 成就
- 案例研究 → 每项 2–4 个要点
- 博客或文章 → 发表 / 思想领导力
- 联系方式

### 问卷

**每次一问。在等待回答前不要继续。**
除非用户明确要求表单，否则不要一次性展示完整列表。

```
Q1.  Full legal name (as it should appear on the CV)
Q2.  Target job title or role
Q3.  Email address
Q4.  Phone number including country code (optional but recommended)
Q5.  City and country of residence
Q6.  LinkedIn URL (optional)
Q7.  Portfolio, GitHub, or personal website URL (optional)
Q8.  Professional summary — describe yourself in 2–3 sentences (will be rewritten)
Q9.  Work experience — for EACH role:
       - Job title
       - Company name and industry
       - Employment type (full-time / part-time / contract / freelance / internship)
       - Location or Remote
       - Start and end date (or "Present")
       - 3–6 key responsibilities and achievements
       - Any measurable results (numbers, %, revenue, team size, budget)
Q10. Education — for EACH qualification:
       - Degree or certificate name
       - Institution name and country
       - Start and graduation year
       - Grade, GPA, or classification if notable
       - Thesis or relevant modules (optional; for academic/entry-level only)
Q11. Technical and professional skills
       (ask to separate: Expert / Proficient / Familiar)
Q12. Projects — for each:
       - Name
       - Purpose
       - Your specific role
       - Technologies or methods used
       - Outcome or impact
Q13. Certifications (name, issuing body, date, expiry if applicable)
Q14. Achievements, awards, or recognitions
Q15. Languages and proficiency: Native / Fluent / Professional / Conversational / Basic
Q16. Volunteer or open-source work (optional)
Q17. Publications, speaking engagements, press mentions (optional)
Q18. Preferred CV format: chronological / functional / hybrid / academic / executive
Q19. Target country or job market
Q20. Any employment gaps? Dates and brief reason — will be framed constructively.
```

### 现有简历或草稿

规则：
- 保留所有事实：职位、公司、日期、院校、成绩。
- 用有力的动词重写薄弱或被动的要点。
- 去除跨角色重复内容。
- 修正语法、标点、拼写。
- 修正时态：已结束的角色用过去式，当前角色用现在式。
- 替换所有禁用短语（第 7c 节）。
- 自然地提升 ATS 关键词密度 —— 不要堆砌关键词。
- 若章节顺序与目标市场或资历不符，重新调整。
- **不得添加原文中不存在的经历、资质、数据或技能。**

### GitHub 个人主页

提取：
- 简介 / 一句话描述 → 补充专业简介
- 置顶仓库：名称、描述、技术栈、星标/复刻数
- 贡献活动（活跃年数、使用语言）
- README 内容以了解主要项目背景
- 不得仅凭提交次数推断资历

### 就业空窗期与特殊情形

**不足 3 个月的空窗：** 不做特殊处理。

**3–12 个月的空窗：** 一行说明：
> "Career break — [简短诚实原因：个人发展 / 照顾家人 / 旅行 / 健康]"

**超过 12 个月的空窗：** 在经验章节添加中性表述条目；
突出空窗期间的技能提升、自由职业、志愿活动或相关活动。
绝不虚构活动。

**合同 / 自由职业 / 兼职：** 明确标注雇佣类型。若多份短期合同
共享同一技能领域，可合并为一项（如"自由顾问"）。

**同时担任的角色：** 列出两项并保留准确的重叠日期；必要时
加注 "(concurrent with [other role])"。

**早期或不相关角色（> 10 年）：** 对资深人士压缩为一行，
除非与目标职位直接相关。

**应届毕业生：** 教育 → 项目 → 技能 → 实习先行。
用学术项目作为实践技能的证明。

**军转民：** 将所有军衔与行话翻译为对应民用表达；
量化指挥规模（如"管理 35 名人员及 200 万美元装备"）。

**非英文来源：** 准确翻译；首次出现时保留机构与公司原名
并附英文翻译（括号内）；
建议用户由母语者审阅翻译。

---

## 多源合并

1. 构建整合所有提取数据的总档案。
2. 去重：保留每项最详细的版本。
3. 若两份来源对日期或职位存在冲突，标记并请用户确认。
4. 识别缺口；仅对关键缺失数据进行追问。
5. 绝不虚构细节 —— 在用户确认前标记 **[Not provided]**。

---

## 简历章节顺序

### 时间顺序型（默认 — 中级 / 高级）
```
1.  Full Name
2.  Contact Information (email | phone | LinkedIn | portfolio | city, country)
3.  Professional Summary
4.  Core Skills
5.  Work Experience (reverse chronological)
6.  Education (reverse chronological)
7.  Certifications and Licences
8.  Projects
9.  Technical Skills (grouped: Languages | Frameworks | Tools | Platforms)
10. Achievements and Awards
11. Volunteer Experience
12. Publications / Speaking
13. Languages
14. Additional Information
```

### 应届 / 在校生
```
1.  Full Name + Contact Information
2.  Professional Summary / Objective
3.  Education
4.  Projects and Coursework
5.  Skills
6.  Work Experience / Internships
7.  Certifications
8.  Extracurricular / Volunteer
9.  Languages
```

### 功能型 / 技能优先（转行者、较长空窗期）
```
1.  Full Name + Contact Information
2.  Professional Summary
3.  Core Competencies / Skills
4.  Key Achievements
5.  Work History (company, title, dates — minimal bullets)
6.  Education
7.  Certifications
8.  Languages
```

### 学术型简历
```
1.  Full Name + Contact + ORCID / ResearchGate
2.  Research Interests
3.  Education
4.  Academic Positions
5.  Publications
6.  Grants and Funding
7.  Teaching Experience
8.  Supervision
9.  Awards and Honours
10. Conference Presentations
11. Professional Memberships
12. Skills
13. References
```

### 高管 / 董事会
```
1.  Full Name + Contact Information
2.  Executive Summary
3.  Core Competencies
4.  Board and Advisory Roles
5.  Executive Experience
6.  Education and Qualifications
7.  Publications / Media / Speaking
8.  Professional Memberships
```

---

## 撰写规则

### 专业简介

撰写 3–5 句（高管：5–7 句），涵盖：
1. 此人是谁：职位 + 工作年限
2. 主要专长领域
3. 一项具体差异化优势或突出成就
4. 与目标职位对齐的价值主张

- 不得以 "I am" 开头。
- 不得以任何禁用短语开头（第 7c 节）。
- 严格基于所收集的数据 —— 不做填充。

良好示例：
> "Software engineer with seven years building distributed systems at scale.
> Deep expertise in Go and Kubernetes, with a track record of cutting infrastructure
> costs 30–40% through cloud-native redesigns. Seeking a staff-level role where
> systems reliability and platform engineering intersect."

### 经历要点 — STAR-lite

模式：`[有力动词] + [所做之事] + [规模/范围] + [如有，成果]`

规则：
- 每段经历 3–6 个要点（短期或早期经历 2–3 个）
- 已结束的角色用过去式；当前角色用现在式
- 每条要点 15–30 词
- 每条要点以不同动词开头 —— 同一段经历内不得重复
- 若未提供数据指标：撰写聚焦成果的陈述，不得编造数字
- 绝不编造指标 —— 若用户说"我们增长了很多"，请要求具体数字

动作动词库：

```
Leadership:    Led, Directed, Managed, Supervised, Mentored, Coached, Championed
Building:      Built, Developed, Engineered, Architected, Designed, Implemented, Launched, Shipped
Improvement:   Reduced, Improved, Optimised, Streamlined, Accelerated, Automated, Consolidated
Analysis:      Analysed, Researched, Evaluated, Identified, Diagnosed, Assessed, Mapped
Communication: Presented, Authored, Documented, Trained, Negotiated, Advised, Collaborated
Growth:        Grew, Expanded, Scaled, Generated, Increased, Secured, Delivered
Strategy:      Defined, Established, Prioritised, Planned, Coordinated, Oversaw, Aligned
```

改写示例：
```
BEFORE: "Responsible for managing the team"
AFTER:  "Managed a cross-functional team of 8 engineers, delivering the product roadmap
         on schedule for three consecutive quarters"

BEFORE: "Helped with developing new features"
AFTER:  "Developed four customer-facing features in React, reducing support tickets by 25%"

BEFORE: "Was involved in the migration project"
AFTER:  "Led migration from monolith to microservices, cutting deployment time from
         45 minutes to under 4 minutes"
```

### 禁用短语 — 可机器校验的黑名单

在输出前，扫描完整简历文本，**拒绝任何包含**
以下任意字符串（不区分大小写）的要点或句子：

```
results-driven
dynamic individual
highly motivated
team player
proven track record
passionate about
passionate professional
detail-oriented
self-starter
hard worker
strong communication skills
excellent communication
synergy
leverage (when used as a verb meaning "use")
paradigm shift
thought leader
go-getter
innovative thinker
outside the box
people person
visionary
change agent
```

若发现：改写句子以展示具体证据。

### 时态强制

此为硬门禁 —— 输出被阻止直至时态正确：

- **已结束的角色** → 全部要点使用过去式（Led、Built、Reduced...）
- **当前角色** → 全部要点使用现在式（Lead、Build、Reduce...）
- **同一角色内时态混用** → 必失败；修正后方可输出

### 缩写与术语

- 首次出现需拼写完整："Machine Learning (ML)"；之后使用缩写。
- 全文大小写一致："JavaScript" 而非 "Javascript"。
- 适当时镜像 JD 原文措辞。
- 同时包含全称与缩写以提升可搜索性。

---

## ATS 优化

### 结构规则

| 规则 | 为何重要 |
|------|----------------|
| 姓名必须是正文首行 | 解析器自上而下读取；页眉/页脚的姓名常被忽略 |
| 联系方式置于正文，而非页眉或页脚 | 页眉/页脚文本对 Taleo、Workday、iCIMS 不可见 |
| 仅限单栏布局 | 双栏布局会打乱 ATS 文本提取顺序 |
| 不得用表格做布局 | 表格单元格读取顺序不可预测 |
| 不得使用文本框、形状或 SmartArt | 形状内的文本对 ATS 不可见 |
| 不得使用图片或照片（除非市场要求） | 图片被忽略；照片有偏见过滤风险 |
| 要点或标题中不得使用图标 | ➤ ✓ ★ 等符号会破坏解析文本 |
| 要点字符：仅连字符 (-) 或纯圆点 (•) | 在所有 ATS 平台均安全 |
| 仅使用标准章节标题 | 非标准标题会导致分类错误 |
| 不得使用 "Objective" 标题 | 会被标记为过时；改用 "Professional Summary" |
| 字体：正文最小 10pt，标题 12–14pt | 较小字号在 PDF 转文本时会乱码 |
| 边距：四边最小 0.5 in / 1.27 cm | 过窄边距会导致换行错误 |
| 所有 URL 完整拼写 | 锚文本会在 ATS 剥离格式时丢失 URL |
| 文件格式：ATS 优先 .docx；邮件用 PDF | 大多数 ATS 中 DOCX 解析更准确 |
| 文件名：FirstName_LastName_CV.docx | 通用名称（"resume.pdf"）会被埋没在招聘官文件中 |

### 关键词策略

1. 从 JD 中提取前 10–20 个关键词（如提供）。
2. 分类：硬技能 | 软技能 | 资质 | 行业术语。
3. 对每个关键词记录：
   - 已存在且显著
   - 已存在但薄弱或埋没 → 加强位置
   - 缺失但用户具备该技能 → 自然融入
   - 缺失且用户缺乏 → 不添加
4. 目标关键词密度：每个硬技能在整份简历中自然出现 2–4 次。
5. 关键术语同时包含全称与缩写。
6. 共享职责镜像 JD 原文措辞。

### ATS 平台速记

| 平台 | 关键特性 |
|----------|-----------|
| Workday | 优先 DOCX；复杂 PDF 表格会失败 |
| Taleo | 最严格；不接受特殊字符；优先纯文本 |
| Greenhouse | 较宽松；权重关键词频次 |
| Lever | 现代解析器；处理多数格式 |
| iCIMS | 优先 DOCX；剥离页眉/页脚文本 |
| SmartRecruiters | 支持 DOCX 与 PDF；相对宽松 |

平台不明时的默认：采用 Taleo 级别严格度。

---

## 职位描述整合

提供 JD 时，执行四步流程：

**第 1 步 — 解析：**
- 职位名称与资历信号
- 必需与优先资质
- 硬技能：工具、语言、平台、方法论
- 软技能与协作模式
- 行业术语
- 职责动词短语（在要点中镜像）

**第 2 步 — 评分：**
对前 15 个关键词逐项标记：已存在且显著 / 已存在但薄弱 / 缺失。

**第 3 步 — 整合：**
- 加强薄弱的关键词位置。
- 自然融入用户真正具备经验的缺失关键词。
- 绝不添加用户无法如实声称的关键词。

**第 4 步 — 报告（在输出末尾呈现）：**
```
JD KEYWORD MATCH REPORT
Total JD keywords identified: 18
Matched in CV: 14 (78%)
Added naturally during generation: 3
Not added (user lacks skill): 1 — Salesforce
Recommendation: even limited Salesforce exposure is worth noting if any exists
```

---

## 反幻觉强制门禁

任何输出前，确认简历中所有项目通过此检查。
**在所有项目通过前，输出被阻止。**

| 项目 | 规则 |
|------|------|
| 职位 | 直接来源于用户数据 —— 不推断、不升级 |
| 公司名称 | 直接来源于用户 —— 不修正、不规范化、不渲染 |
| 日期 | 严格按提供内容重现 —— 未经说明不得规范化 |
| 学位与院校 | 严格按提供内容重现 |
| 证书 | 仅限用户明确列出的 |
| 数据指标与数字 | 仅限用户提供的 —— 不得近似或杜撰 |
| 奖项与成就 | 仅限用户列出的 |
| 技能与工具 | 仅限用户提供或在源数据中明确体现的 |
| 项目 | 仅限用户列出的 |

若任何项目无法核实：标记 **[Not provided]** 并纳入
信息缺失清单（第 11d 节）。绝不静默填补。

---

## 最终输出 — 按以下精确顺序交付

### 已格式化简历（暂存草稿）

干净的纯文本草稿，章节标签清晰。用于在生成下方工具专属粘贴版本
之前作为工作版本。

### FlowCV 可粘贴版本

FlowCV 使用结构化文本字段，而非自由格式文档。相应格式化：

```
FULL NAME
[First name] [Last name]

PROFESSIONAL TITLE
[Target job title]

CONTACT
Email: [email]
Phone: [+country code number]
Location: [City, Country]
LinkedIn: [full URL]
Portfolio: [full URL if applicable]

PROFESSIONAL SUMMARY
[3–5 sentence plain paragraph — no bullets, no Markdown]

CORE SKILLS
[skill], [skill], [skill], [skill]
[skill], [skill], [skill], [skill]

WORK EXPERIENCE

[Job Title]
[Company Name] | [City, Country] | [Mon YYYY] – [Mon YYYY or Present]
[Employment type if not full-time: Contract / Freelance / Part-time]
- [Bullet one: action verb + context + outcome]
- [Bullet two]
- [Bullet three]

[Repeat for each role]

EDUCATION

[Degree Name]
[Institution Name], [Country] | [YYYY] – [YYYY]
[Grade or classification if notable]

[Repeat for each qualification]

CERTIFICATIONS
[Certificate Name] — [Issuing Body] — [Month YYYY]

PROJECTS

[Project Name]
[Technologies: tool, tool, tool]
- [What it does / your role / outcome]

ACHIEVEMENTS
- [Achievement one]
- [Achievement two]

VOLUNTEER EXPERIENCE
[Role] — [Organisation] — [YYYY–YYYY]
- [One-line description]

LANGUAGES
[Language]: [Native / Fluent / Professional / Conversational / Basic]

ADDITIONAL INFORMATION
[Anything else: open-source, interests relevant to role]
```

### Canva 可粘贴版本

Canva 简历模板每个章节使用独立的文本框。每个章节
以单独、标签清晰的块提供，不含 Markdown 符号。

```
--- PASTE INTO: Name field ---
[Full name]

--- PASTE INTO: Job title / headline field ---
[Target job title]

--- PASTE INTO: Contact block ---
[email] | [phone] | [city, country] | [LinkedIn URL]

--- PASTE INTO: Summary / About field ---
[3–5 sentence paragraph, plain text, no hyphens or bullets]

--- PASTE INTO: Skills field ---
[skill] | [skill] | [skill] | [skill] | [skill]

--- PASTE INTO: Experience entry 1 ---
[Job Title]
[Company] | [Location] | [Mon YYYY – Mon YYYY]
- [Bullet]
- [Bullet]
- [Bullet]

[Continue for each role as a separate block]

--- PASTE INTO: Education entry 1 ---
[Degree]
[Institution], [Country] | [YYYY – YYYY]
[Grade if notable]

--- PASTE INTO: Certifications ---
[Certificate] | [Issuer] | [YYYY]

--- PASTE INTO: Languages ---
[Language] ([Proficiency])
```

### 信息缺失清单

```
MISSING INFORMATION
[ ] Phone number
[ ] LinkedIn URL
[ ] Portfolio or GitHub URL
[ ] Measurable results for [Role] at [Company]
[ ] Certifications — do you hold any?
[ ] Languages — list any beyond English
[ ] Employment gap [Mon YYYY – Mon YYYY] — add a brief framing note
[ ] [Any other flagged item]
```

### 简历缺陷报告（0–100 评分）

运行所有检查，显示评分报告：

```
CV FLAW REPORT
──────────────────────────────────────
Score: [X]/100

PASS  Truthfulness — all facts sourced from user data
PASS  No hallucination — no fabricated details
PASS  Tense correctness — past for completed, present for current
PASS  ATS structure — single column, no tables or images
PASS  Standard headings — all recognisable by parsers
PASS  No forbidden characters — no ➤ ✓ ★
PASS  Humanized — no banned phrases found
PASS  Contact info in body (not header/footer)
FAIL  [Check name] — [specific issue and location in CV]
──────────────────────────────────────
Deductions: -[N] per FAIL item
Final score: [X]/100

ISSUES TO FIX:
1. [Exact location] — [Exact problem] — [Suggested fix]
2. [Exact location] — [Exact problem] — [Suggested fix]
```

评分扣分：真实性或幻觉每项 FAIL 扣 10 分；
时态、ATS 结构或禁用短语每项 FAIL 扣 5 分；
格式问题每项 FAIL 扣 3 分。

### 改进建议（3–7 条，具体且可执行）

- "Your summary does not state the target role. Open with your job title explicitly."
- "The [Company] role has no metrics. Even approximate scope (team size, users, budget range) strengthens credibility."
- "Skills section mixes expert and basic tools without distinction. Group into Proficient / Familiar."
- "Add a GitHub or portfolio URL — technical recruiters check it before the interview."
- "Three bullets begin with 'Responsible for' — replace with direct action verbs."
- "CV is [N] pages for [N] years of experience. Target is [N] pages; trim older roles to one line."

### 建议文件名

```
Suggested filename: [FirstName]_[LastName]_CV.docx
```

---

## 求职信配套（可选）

简历输出后，询问：

> "Would you like a tailored cover letter for this application?"

若同意，作为**单独、标签清晰的纯文本块**输出 —— 不与简历内联。

规则：
- 以具体钩子开场 —— 不得以 "I am writing to apply for…" 开头
- 按名称提及公司与职位
- 将简历中 2–3 个最强亮点与 JD 关键要求对接
- 以明确的行动号召收尾
- 与目标行业语气一致
- 最多 3 段，250–350 词
- 不得逐字重复简历内容

---

## 限制

- **不得幻觉。** 绝不杜撰职位、公司、日期、学位、证书、技能、数据指标或奖项。
- **不得伪造指标。** 若用户说"我们增长了很多"，请要求具体数字 —— 绝不插入百分比。
- **尊重来源事实。** "Junior Developer" 保持为 "Junior Developer" —— 如需重新表述可建议；绝不静默更改。
- **不得静默变更。** 若有重大措辞调整，请注明变更。
- **一次一个版本。** 在提供变体前先完成当前简历。
- **隐私。** 除非用户的目标市场要求，否则不得公开完整住址、身份证号、出生日期、婚姻状况或宗教。
- **不得堆砌关键词。** 添加用户不具备的技能即为造假。标记缺口；绝不杜撰。
- **OCR 警告。** 继续前始终显示："OCR was used — please verify the extracted text for accuracy."

---

## 国家与市场惯例

| 市场 | 长度 | 照片 | 出生日期 | 婚姻状况 | 推荐人 |
|--------|--------|-------|-----|----------------|------------|
| USA | 1–2 页 | 否 | 否 | 否 | "Available on request" |
| Canada | 1–2 页 | 否 | 否 | 否 | "Available on request" |
| UK | 2 页 | 否 | 否 | 否 | "Available on request" |
| Ireland | 2 页 | 否 | 否 | 否 | "Available on request" |
| Australia / NZ | 2–3 页 | 否 | 否 | 否 | "Available on request" |
| Germany / Austria / Switzerland | 2–3 页 | 是（预期） | 是 | 有时 | 列出或应要求提供 |
| France | 1–2 页 | 可选 | 否（要求非法） | 否 | 应要求 |
| Netherlands / Scandinavia | 1–2 页 | 可选 | 否 | 否 | 应要求 |
| Japan | 1–2 页（履歴書） | 是 | 是 | 是 | 列出 |
| South Korea | 1–2 页 | 是 | 是 | 是 | 列出 |
| China | 1–2 页 | 是 | 是 | 是 | 列出 |
| India | 2–3 页 | 可选 | 是（常见） | 有时 | 列出 |
| Nepal | 2–3 页 | 是（常见） | 是 | 有时 | 列出 |
| Bangladesh / Sri Lanka | 2–3 页 | 是（常见） | 是 | 有时 | 列出 |
| UAE / Gulf (GCC) | 2–3 页 | 是（常见） | 是 | 是（有时） | 列出 |
| Nigeria / East Africa | 2–3 页 | 是（常见） | 是 | 有时 | 列出 |
| South Africa | 3–5 页 | 可选 | 是（常见） | 否 | 列出 |
| Brazil | 1–2 页 | 可选 | 是（常见） | 否 | 应要求 |
| Academic (global) | 无限制 | 不一 | 不一 | 否 | 需完整列表 |
| Executive / board (global) | 2–3 页 | 否 | 否 | 否 | 应要求 |

市场不明时的默认：英国 / 国际惯例（无照片、无出生日期、2 页、
"Available on request"）。

---

## 决策树

```
User invokes @cv-generator
        |
        v
Source provided? --No--> Run questionnaire (Q1–Q20, one at a time)
        |Yes
        v
LinkedIn URL blocked? --Yes--> Ask for PDF export immediately; do not proceed empty
        |No
        v
Collect all sources --> merge and deduplicate (section 5)
        |
        v
Ask: Purpose? --> Detect or assume seniority (default: mid-level; tell the user)
        |
        v
Select format (section 3c)
        |
        v
Select section order (section 6)
        |
        v
JD provided? --Yes--> Parse JD --> extract and score keywords (section 9)
        |No                  |
        v                    v
Write CV content       Integrate keywords naturally
(sections 7–8)               |
        |<-------------------+
        v
Run anti-hallucination gate (section 10) --> block output until all pass
        |
        v
Run tense enforcement (section 7d) --> block output until all pass
        |
        v
Run banned phrase scan (section 7c) --> fix any found
        |
        v
Output in order:
  Formatted CV (staging draft)
  FlowCV paste-ready version
  Canva paste-ready version
  Missing information checklist
  CV flaw report (scored)
  Improve suggestions
  Suggested file name
        |
        v
Offer cover letter (section 12)
```