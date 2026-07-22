---
name: web-scraper
description: 智能多策略 Web 抓取。从网页中提取结构化数据（表格、列表、价格）。支持分页、监控以及 CSV/JSON 导出。触发词：scraper、scraping、web scraping、抓取数据、网页抓取、数据采集、提取网页数据、批量抓取。
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- scraping
- data-extraction
- automation
- csv
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# 网页抓取器

## 概述

智能多策略 Web 抓取。从网页中提取结构化数据（表格、列表、价格）。支持分页、监控以及 CSV/JSON 导出。

## 何时使用本技能

- 当用户提到 "scraper" 或相关主题
- 当用户提到 "scraping" 或相关主题
- 当用户提到 "extrair dados web"（抓取网页数据）或相关主题
- 当用户提到 "web scraping" 或相关主题
- 当用户提到 "raspar dados"（抓取数据）或相关主题
- 当用户提到 "coletar dados site"（采集网站数据）或相关主题

## 何时不要使用本技能

- 任务与网页抓取无关
- 有更简单、更专门的工具可以处理该请求
- 用户需要的是无领域专业知识的通用协助

## 工作原理

严格按顺序执行各个阶段。每个阶段的输出作为下一阶段的输入。

```
1. 澄清 (CLARIFY)  ->  2. 侦察 (RECON)  ->  3. 策略 (STRATEGY)  ->  4. 提取 (EXTRACT)  ->  5. 转换 (TRANSFORM)  ->  6. 验证 (VALIDATE)  ->  7. 格式化 (FORMAT)
```

切勿跳过阶段 1 或阶段 2。它们能防止徒劳的工作和失败的提取。

**快速路径**：如果用户提供了 URL + 明确的数据目标 + 请求简单（单页、单种数据），可将阶段 1-3 压缩为单步操作：一次 WebFetch 调用完成抓取、分类与提取。但仍需验证和格式化。

---

## 能力

- **多策略**：WebFetch（静态）、浏览器自动化（JS 渲染）、Bash/curl（API）、WebSearch（发现）
- **提取模式**：table、list、article、product、contact、FAQ、pricing、events、jobs、custom
- **输出格式**：Markdown 表格（默认）、JSON、CSV
- **分页**：自动检测并跟进（页码、无限滚动、加载更多）
- **多 URL**：跨源提取相同结构，并支持比较与差异
- **验证**：每次提取附带置信度评级（HIGH/MEDIUM/LOW）
- **自动升级**：WebFetch 静默失败 -> 自动回退到浏览器
- **数据转换**：清洗、规范化、去重、丰富
- **差异模式**：检测多次抓取运行之间的变化

## 网页抓取器

多策略网页数据提取，具有智能方案选择、自动回退升级、数据转换与结构化输出能力。

## 阶段 1：澄清

在接触任何 URL 之前，先确定提取参数。

## 必填参数

| 参数         | 解决方式                            | 默认值        |
|:--------------|:-------------------------------------|:---------------|
| 目标 URL     | 要抓取哪些页面？                     | *(必填)*       |
| 数据目标     | 要提取哪些具体数据？                 | *(必填)*       |
| 输出格式     | Markdown 表格、JSON、CSV 还是文本？  | Markdown 表格 |
| 范围         | 单页、分页还是多 URL？               | 单页          |

## 可选参数

| 参数         | 解决方式                              | 默认值         |
|:--------------|:---------------------------------------|:---------------|
| 分页         | 是否分页？最多几页？                   | 不分页，1 页   |
| 最大条目数   | 最多收集多少条？                       | 不限          |
| 过滤器       | 要排除或包含哪些数据？                 | 无            |
| 排序         | 如何对结果排序？                       | 来源顺序      |
| 保存路径     | 是否保存到文件？哪个路径？             | 仅显示        |
| 语言         | 用哪种语言回复？                       | 用户的语言    |
| 差异模式     | 是否与上次运行对比？                   | 否            |

## 澄清规则

- 如果用户提供了 URL 与明确的数据目标，直接进入阶段 2。
  不要问无关紧要的问题。
- 如果请求含糊不清（例如"抓取这个网站"），只问：
  "你想从这个页面提取哪些具体数据？"
- 默认使用 Markdown 表格输出。仅在相关时提及替代方案。
- 接受任何语言发起的请求。始终用用户的语言回复。
- 如果用户说"所有"或"全部数据"，先执行侦察，然后呈现可用字段让用户选择。

## 发现模式

当用户只有主题但没有具体 URL 时：
1. 使用 WebSearch 找到最相关的页面
2. 呈现 3-5 个最相关的 URL 及其描述
3. 让用户选择抓取哪些，或全部抓取
4. 用选中的 URL 进入阶段 2

示例："查找并提取 CRM 工具的定价数据"
-> WebSearch("CRM tools pricing comparison 2026")
-> 呈现最相关结果 -> 用户选择 -> 提取

---

## 阶段 2：侦察

在提取之前分析目标页面。

## 步骤 2.1：初始抓取

使用 WebFetch 检索并分析页面结构：

```
WebFetch(
  url = TARGET_URL,
  prompt = "分析此页面结构并报告：
    1. 页面类型：文章、产品列表、搜索结果、数据表格、
       目录、仪表板、API 文档、FAQ、定价页、招聘板、活动页或其他
    2. 主要内容结构：表格、有序/无序列表、卡片网格、自由文本、
       手风琴/可折叠区域、标签页
    3. 可见的不同数据条目的近似数量
    4. JavaScript 渲染迹象：空容器、加载动画、
       SPA 框架标记（React root、Vue app、Angular）、少量 HTML 但 JS 密集
    5. 分页：上/下页链接、页码、加载更多按钮、
       无限滚动指示、总结果数
    6. 数据密度：可被提取的结构化数据有多少
    7. 列出可供提取的主要数据字段/列
    8. 嵌入的结构化数据：JSON-LD、microdata、OpenGraph 标签
    9. 可用的下载链接：CSV、Excel、PDF、API 端点"
)
```

## 步骤 2.2：评估抓取质量

| 信号                                          | 解读                        | 操作                       |
|:----------------------------------------------|:-----------------------------|:---------------------------|
| 内容丰富、数据清晰可见                        | 静态页面                    | 策略 A（WebFetch）         |
| 空容器、"loading..."、文字极少                | JS 渲染                      | 策略 B（浏览器）           |
| 登录墙、CAPTCHA、403/401 响应                 | 被阻止                      | 向用户报告                 |
| 有内容但结构混乱                              | 需要精细化处理              | 策略 B（浏览器）           |
| 响应体为 JSON 或 XML                          | API 端点                    | 策略 C（Bash/curl）        |
| 有 CSV/Excel 下载链接                          | 直接的数据文件              | 策略 C（下载）             |

## 步骤 2.3：内容分类

将内容归类为某种提取模式：

| 模式       | 判定指标                                 | 示例                              |
|:-----------|:-----------------------------------------|:----------------------------------|
| `table`    | HTML `<table>`、带表头的网格布局         | 价格对比、统计、规格              |
| `list`     | 重复的相似元素、卡片网格                 | 搜索结果、商品列表                |
| `article`  | 带标题/段落的长文本                      | 博客文章、新闻、文档              |
| `product`  | 商品名、价格、规格、图片、评分           | 电商商品页                        |
| `contact`  | 姓名、邮箱、电话、地址、职务             | 团队页、员工目录                  |
| `faq`      | 问答对、手风琴                           | FAQ 页、帮助中心                  |
| `pricing`  | 套餐名、价格、功能、层级                 | SaaS 定价页                       |
| `events`   | 日期、地点、标题、描述                   | 活动列表、会议                    |
| `jobs`     | 职位名、公司、地点、薪资                 | 招聘板、职业页                    |
| `custom`   | 用户指定的 CSS 选择器或字段              | 上述未涵盖的情况                  |

记录：**页面类型**、**提取模式**、**是否需要 JS 渲染（是/否）**、**可用字段**、**是否存在结构化数据（JSON-LD 等）**。

如果用户要求"全部"，呈现可用字段让用户选择。

---

## 阶段 3：策略选择

根据侦察结果选择提取方法。

## 决策树

```
结构化数据（JSON-LD、microdata）已经包含所需内容？
 |
 +-- 是 --> 策略 E：直接提取结构化数据
 |
 +-- 否：内容在 WebFetch 中是否完全可见？
      |
      +-- 是：是否需要精确的元素定位？
      |    |
      |    +-- 否  --> 策略 A：WebFetch + AI 提取
      |    +-- 是 --> 策略 B：浏览器自动化
      |
      +-- 否：是否检测到 JavaScript 渲染？
           |
           +-- 是 --> 策略 B：浏览器自动化
           +-- 否：是否有 API/JSON/XML 端点或下载链接？
                |
                +-- 是 --> 策略 C：Bash（curl + jq）
                +-- 否  --> 向用户报告访问问题
```

## 策略 A：WebFetch + AI 提取

**最适合**：静态页面、文章、简单表格、结构良好的 HTML。

使用 WebFetch 配合针对该模式定制的提取提示：

```
WebFetch(
  url = URL,
  prompt = "从此页面提取 [DATA_TARGET]。
    仅以 [FORMAT] 形式返回提取的数据，列/字段为：[FIELDS]。
    规则：
    - 如果值缺失或不明确，使用 'N/A'
    - 不要包含导航、广告、页脚或无关内容
    - 准确保留原始值（数字、货币、日期）
    - 包含所有匹配项，不要只取前几条
    - 对每条数据，如果可用，也提取其 URL/链接"
)
```

**自动升级**：如果 WebFetch 返回的项目数过少（少于侦察预期的 50%），或字段大多为空，无需询问用户，自动升级到策略 B。在备注中记录此次升级。

## 策略 B：浏览器自动化

**最适合**：JS 渲染的页面、SPA、交互式内容、懒加载数据。

执行顺序：
1. 获取标签上下文：`tabs_context_mcp(createIfEmpty=true)` -> 获取 tabId
2. 导航到 URL：`navigate(url=TARGET_URL, tabId=TAB)`
3. 等待内容加载：`computer(action="wait", duration=3, tabId=TAB)`
4. 检查 cookie/同意横幅：`find(query="cookie consent or accept button", tabId=TAB)`
   - 如果发现，关闭它（优先选择保护隐私的选项）
5. 读取页面结构：`read_page(tabId=TAB)` 或 `get_page_text(tabId=TAB)`
6. 定位目标元素：`find(query="[DESCRIPTION]", tabId=TAB)`
7. 使用 JavaScript 通过 `javascript_tool` 精确提取数据

```javascript
// 表格提取
const rows = document.querySelectorAll('TABLE_SELECTOR tr');
const data = Array.from(rows).map(row => {
  const cells = row.querySelectorAll('td, th');
  return Array.from(cells).map(c => c.textContent.trim());
});
JSON.stringify(data);
```

```javascript
// 列表/卡片提取
const items = document.querySelectorAll('ITEM_SELECTOR');
const data = Array.from(items).map(item => ({
  field1: item.querySelector('FIELD1_SELECTOR')?.textContent?.trim() || null,
  field2: item.querySelector('FIELD2_SELECTOR')?.textContent?.trim() || null,
  link: item.querySelector('a')?.href || null,
}));
JSON.stringify(data);
```

8. 对于懒加载内容，滚动后再次提取：
   `computer(action="scroll", scroll_direction="down", tabId=TAB)`
   然后 `computer(action="wait", duration=2, tabId=TAB)`

## 策略 C：Bash（curl + jq）

**最适合**：REST API、JSON 端点、XML 源、CSV/Excel 下载。

```bash

## JSON API

curl -s "API_URL" | jq '[.items[] | {field1: .key1, field2: .key2}]'

## CSV 下载

curl -s "CSV_URL" -o /tmp/scraped_data.csv

## XML 解析

curl -s "XML_URL" | python3 -c "
import xml.etree.ElementTree as ET, json, sys
tree = ET.parse(sys.stdin)

## ... 解析并输出 JSON

"
```

## 策略 D：混合

当单一策略不够用时组合使用：
1. WebSearch 发现相关 URL
2. WebFetch 评估初始内容
3. 浏览器自动化处理 JS 密集部分
4. Bash 做后处理（jq、python 数据清洗）

## 策略 E：结构化数据提取

当页面存在 JSON-LD、microdata 或 OpenGraph 时：
1. 使用浏览器 `javascript_tool` 提取结构化数据：
```javascript
const scripts = document.querySelectorAll('script[type="application/ld+json"]');
const data = Array.from(scripts).map(s => {
  try { return JSON.parse(s.textContent); } catch { return null; }
}).filter(Boolean);
JSON.stringify(data);
```
2. 这种方式通常比 DOM 抓取提供更干净、更可靠的数据
3. 仅对结构化数据未覆盖的字段回退到 DOM 提取

## 分页处理

当检测到分页且用户希望获取多页时：

**页码分页（任意策略）：**
1. 从当前页提取数据
2. 识别 URL 模式（例如 `?page=N`、`/page/N`、`&offset=N`）
3. 按用户上限迭代各页（默认：5 页）
4. 显示进度："正在提取第 2/5 页..."
5. 拼接所有结果，必要时去重

**无限滚动（仅浏览器）：**
1. 提取当前可见数据
2. 记录条目数
3. 向下滚动：`computer(action="scroll", scroll_direction="down", tabId=TAB)`
4. 等待：`computer(action="wait", duration=2, tabId=TAB)`
5. 提取新加载的数据
6. 对比数量 - 如果 2 次滚动后仍无新条目，停止
7. 重复直到无新内容或达到最大迭代次数（默认：5）

**"加载更多"按钮（仅浏览器）：**
1. 提取当前可见数据
2. 找到按钮：`find(query="load more button", tabId=TAB)`
3. 点击：`computer(action="left_click", ref=REF, tabId=TAB)`
4. 等待并提取新内容
5. 重复直到按钮消失或达到最大迭代次数

---

## 阶段 4：提取

使用选定策略按模式专属模式执行。

参见 [references/extraction-patterns.md](references/extraction-patterns.md)
获取 CSS 选择器和 JavaScript 片段。

## 表格模式

WebFetch 提示：
```
"从此页面的表格中提取所有行。
以 markdown 表格形式返回，列标题要完全一致。
包含每一行 —— 不要截断或概括。
保留数字精度、货币和单位。"
```

## 列表模式

WebFetch 提示：
```
"从此页面提取每个 [ITEM_TYPE]。
对每条数据，提取：[FIELD_LIST]。
以 JSON 数组形式返回，对象的键为：[KEY_LIST]。
包含所有项，不要只取前几条。如果可用，每条都包含链接/URL。"
```

## 文章模式

WebFetch 提示：
```
"提取文章元数据：
- 标题、作者、日期、标签/分类、字数估计
- 关键事实数据点、统计数据、命名实体
以结构化 markdown 形式返回。概括内容，不要复制全文。"
```

## 产品模式

WebFetch 提示：
```
"按以下字段提取产品数据：
- name、brand、price、currency、originalPrice（如有折扣）、
  availability、description（前 200 字符）、rating、reviewCount、
  specifications（键值对）、productUrl、imageUrl
以 JSON 形式返回。缺失字段使用 null。"
```

同时先检查 JSON-LD 的 `Product` schema（策略 E）。

## 联系模式

WebFetch 提示：
```
"为每个人/实体提取联系信息：
- name、title、role、email、phone、address、organization、website、linkedinUrl
以 markdown 表格形式返回。仅提取页面上真实的联系信息。"
```

## FAQ 模式

WebFetch 提示：
```
"从此页面提取所有问答对。
对每个 FAQ 条目提取：
- question：问题原文
- answer：答案文本（长则取前 300 字符）
- category：分组所在的小节/分类
以 JSON 数组形式返回。"
```

## 定价模式

WebFetch 提示：
```
"从此页面提取所有定价套餐/层级。
对每个套餐提取：
- planName、monthlyPrice、annualPrice、currency
- features（包含的功能数组）
- limitations（限制或排除项的数组）
- ctaText（行动按钮文案）
- highlighted（标记为推荐/热门则为 true）
以 JSON 形式返回。缺失字段使用 null。"
```

## 活动模式

WebFetch 提示：
```
"从此页面提取所有活动/会议。
对每个活动提取：
- title、date、time、endTime、location、description（前 200 字符）
- speakers（演讲者姓名数组）、category、registrationUrl
以 JSON 形式返回。缺失字段使用 null。"
```

## 招聘模式

WebFetch 提示：
```
"从此页面提取所有职位列表。
对每个职位提取：
- title、company、location、salary、salaryRange、type（全职/兼职/合同）
- postedDate、description（前 200 字符）、applyUrl、tags
以 JSON 形式返回。缺失字段使用 null。"
```

## 自定义模式

当用户提供具体选择器或字段描述时：
- 使用浏览器自动化配合 `javascript_tool` 与用户给定的 CSS 选择器
- 或使用 WebFetch，配合基于用户字段描述构建的提示
- 在进入多 URL 提取前务必先与用户确认已提取的 schema

## 多 URL 提取

当从多个 URL 提取时：
1. 从**第一个 URL** 提取，以建立数据 schema
2. 向用户展示首条结果并确认 schema 正确
3. 用相同 schema 从其余 URL 提取
4. 每条记录都加上 `source` 列/字段注明来源 URL
5. 将所有结果合并为单一输出
6. 显示进度："正在提取 3/7 个 URL..."

---

## 阶段 5：转换

在验证前对提取的数据进行清洗、规范化与丰富。
参见 [references/data-transforms.md](references/data-transforms.md) 了解模式。

## 自动转换（始终应用）

| 转换                 | 操作                                                 |
|:----------------------|:------------------------------------------------------|
| 空白字符清理          | 去除首尾空白、合并多个空格、删除单元格内 `\n`         |
| HTML 实体解码         | `&amp;` -> `&`，`&lt;` -> `<`，`&#39;` -> `'`         |
| Unicode 规范化         | 使用 NFKC 规范化以统一字符                            |
| 空字符串转为 null     | `""` -> `null`（JSON），`""` -> `N/A`（表格）          |

## 条件转换（在相关时应用）

| 转换                | 适用场景                      | 操作                                    |
|:---------------------|:-------------------------------|:----------------------------------------|
| 价格规范化          | 商品/定价模式                 | 提取数值 + 货币符号                     |
| 日期规范化          | 任何日期                      | 规范为 ISO-8601（YYYY-MM-DD）           |
| URL 解析            | 提取到相对 URL                | 转换为绝对 URL                          |
| 电话规范化          | 联系模式                      | 尽可能统一为 E.164 格式                 |
| 去重                | 多页或多 URL                  | 移除完全重复的行                        |
| 排序                | 用户要求或自然排序            | 按用户指定字段排序                      |

## 数据丰富（仅在有用时）

| 丰富项               | 适用场景                      | 操作                                    |
|:----------------------|:-------------------------------|:----------------------------------------|
| 货币转换              | 用户要求单一货币              | 标注原值 + 近似转换                     |
| 域名提取              | 数据中有 URL                  | 从完整 URL 中添加域名列                 |
| 字数统计              | 文章模式                      | 统计提取文本的词数                      |
| 相对日期              | 存在日期                      | 如有用则添加 "X 天前" 列                |

## 去重策略

合并多页或多 URL 的数据时：
1. 完全匹配：所有字段值相同的行 -> 保留第一条
2. 近似匹配：关键字段（名称+来源）相同但详情不同的行
   -> 保留最完整（null 最少）的那条，并在备注中标记
3. 报告："已移除 N 条重复行" 写入交付备注

---

## 阶段 6：验证

在交付结果前验证提取质量。

## 验证检查

| 检查              | 操作                                                   |
|:-------------------|:--------------------------------------------------------|
| 条目数            | 对比提取数量与侦察阶段的预期数量                        |
| 空字段            | 统计每字段中 N/A 或 null 的数量                         |
| 数据类型一致性    | 数字应为数字类型、日期可解析                            |
| 重复              | 标记完全重复的行（去重后）                              |
| 编码              | 检查 HTML 实体、乱码字符                                |
| 完整性            | 输出包含用户要求的所有字段                              |
| 截断              | 验证数据未被截断（检查末尾条目）                        |
| 异常值            | 标记明显异常的值（如 $0.00 价格）                       |

## 置信度评级

为每次提取给出评级：

| 评级      | 标准                                                              |
|:-----------|:-------------------------------------------------------------------|
| **HIGH**  | 所有字段已填充、数量与预期一致、无异常                            |
| **MEDIUM**| 存在少量空缺（<10% 空字段）或数量略有偏差                        |
| **LOW**   | 大量空缺（>10% 空字段）、结构问题、数据不完整                    |

始终报告具体的置信度：
> 置信度：**HIGH** - 提取 47 条数据，6 个字段全部填充，
> 与页面分析的预期数量一致。

## 自动恢复（在报告问题前尝试）

| 问题              | 自动恢复操作                                          |
|:-------------------|:--------------------------------------------------------|
| 数据缺失          | 若使用 WebFetch 则改用浏览器重试                        |
| 编码问题          | 应用 HTML 实体解码 + Unicode 规范化                     |
| 结果不完整        | 检查分页或懒加载，再抓取                                |
| 数量不符          | 滚动/翻页以找到剩余条目                                |
| 所有字段都为空    | 页面很可能是 JS 渲染，切换到浏览器策略                  |
| 字段部分缺失      | 尝试 JSON-LD 提取作为补充                              |

在交付备注中记录所有恢复尝试。
就任何无法恢复的空缺向用户提供具体细节。

---

## 阶段 7：格式化与交付

按用户偏好组织结果结构。
参见 [references/output-templates.md](references/output-templates.md)
获取完整格式化模板。

## 交付封装

始终用以下元数据头包裹结果：

```markdown

## 提取结果

**来源：** [页面标题](http://example.com)
**日期：** YYYY-MM-DD HH:MM UTC
**条目数：** N 条记录（每条 M 个字段）
**置信度：** HIGH | MEDIUM | LOW
**策略：** A（WebFetch）| B（浏览器）| C（API）| E（结构化数据）
**格式：** Markdown 表格 | JSON | CSV

---

[数据在此]

---

**备注：**
- [任何空缺、问题或观察]
- [已应用的转换：去重、规范化等]
- [分页抓取情况："已抓取 1-5 页，共 12 页"]
- [如发生自动升级："已从 WebFetch 升级到浏览器"]
```

## Markdown 表格规则

- 文本列左对齐（`:---`），数字列右对齐（`---:`）
- 列宽一致以提高可读性
- 数值数据可酌情包含汇总行（合计、平均）
- 每个表格最多 10 列；更宽的数据应拆成多个表格或建议使用 JSON 格式
- 长单元格值截断至 60 字符并以 `...` 提示
- 缺失值使用 `N/A`，永远不要留空
- 多页结果应展示合并后的表格（不按页）

## JSON 规则

- 键使用 camelCase（如 `productName`、`unitPrice`）
- 包裹元数据封装：
  ```json
  {
    "metadata": {
      "source": "URL",
      "title": "页面标题",
      "extractedAt": "ISO-8601",
      "itemCount": 47,
      "fieldCount": 6,
      "confidence": "HIGH",
      "strategy": "A",
      "transforms": ["deduplication", "priceNormalization"],
      "notes": []
    },
    "data": [ ... ]
  }
  ```
- 2 空格缩进美化输出
- 数字以数字形式（非字符串），布尔以布尔形式
- 缺失值用 null（非空字符串）

## CSV 规则

- 第一行始终为表头
- 含逗号、引号或换行的字段需加引号
- UTF-8 编码带 BOM 以兼容 Excel
- 使用 `,` 作为分隔符（标准）
- 元数据以注释形式包含：`# Source: URL`

## 文件输出

当用户要求保存文件时：
- Markdown：`.md` 扩展名
- JSON：`.json` 扩展名
- CSV：`.csv` 扩展名
- 写入前先确认路径
- 保存后报告完整文件路径与条目数

## 多 URL 比较格式

跨多个数据源比较时：
- 将 `Source` 添加为第一列/字段
- 使用简短的来源标识符（域名或用户标签）
- 按用户偏好按来源分组或交错
- 用户要求对比时高亮差异
- 包含摘要："最低价：store-b.com 上的 $X"

## 差异输出

当用户要求变更检测（差异模式）时：
- 对比当前提取与上一次运行
- 新增项标记 `[NEW]`
- 删除项标记 `[REMOVED]`
- 变更值标记 `[WAS: old_value]`
- 包含摘要："自上次运行以来变化：+5 新增、-2 删除、3 修改"

---

## 速率限制

- 顺序页面抓取最大 1 请求/2 秒
- 多 URL 任务按顺序处理并加入暂停
- 若网站返回 429（Too Many Requests），停止并向用户报告

## 访问尊重

- 若页面阻止访问（403、CAPTCHA、登录墙），向用户报告
- 不要尝试绕过机器人检测、CAPTCHA 或访问控制
- 未经用户明确提供访问权限，不要抓取需要认证的内容
- 在已知的情况下遵守 robots.txt 指令

## 版权

- 不要复制大段受版权保护的文章原文
- 对于文章：提取事实数据、统计和结构化信息；概括叙述内容
- 输出中始终包含来源归属（http://example.com）

## 数据范围

- 仅提取用户明确要求的内容
- 在大规模收集潜在敏感数据（邮箱、电话、个人信息）前警告用户
- 不要存储或传输用户未查看的提取数据

## 失败协议

当提取失败或被阻止时：
1. 说明具体原因（JS 渲染、机器人检测、登录等）
2. 建议替代方案（不同 URL、可用 API、手动方法）
3. 切勿激进重试或升级访问尝试

---

## 快速参考：模式速查表

| 用户说……                              | 模式      | 策略       | 默认输出          |
|:-------------------------------------|:----------|:-----------|:------------------|
| "提取表格"                            | table     | A 或 B     | Markdown 表格     |
| "获取所有商品/价格"                  | product   | 先 E 再 A  | Markdown 表格     |
| "抓取列表"                            | list      | A 或 B     | Markdown 表格     |
| "提取联系信息/团队页"                | contact   | A          | Markdown 表格     |
| "获取文章数据"                        | article   | A          | Markdown 文本     |
| "提取 FAQ"                            | faq       | A 或 B     | JSON              |
| "获取定价套餐"                        | pricing   | A 或 B     | Markdown 表格     |
| "抓取职位列表"                        | jobs      | A 或 B     | Markdown 表格     |
| "获取活动日程"                        | events    | A 或 B     | Markdown 表格     |
| "查找并提取 [主题]"                   | discovery | WebSearch  | Markdown 表格     |
| "跨站比较价格"                        | multi-URL | A 或 B     | 对比表            |
| "自上次以来有什么变化"                | diff      | 任意       | 差异格式          |

---

## 参考资料

- **提取模式**：[references/extraction-patterns.md](references/extraction-patterns.md)
  CSS 选择器、JavaScript 片段、JSON-LD 解析、领域技巧。

- **输出模板**：[references/output-templates.md](references/output-templates.md)
  Markdown、JSON、CSV 模板与完整示例。

- **数据转换**：[references/data-transforms.md](references/data-transforms.md)
  清洗、规范化、去重、丰富模式。

## 最佳实践

- 提供关于项目和需求的清晰、具体上下文
- 在应用到生产代码前审查所有建议
- 与其他互补技能结合进行全面的分析

## 常见陷阱

- 将本技能用于其领域专业之外的任务
- 在不理解特定上下文的情况下应用建议
- 没有为准确分析提供足够的项目上下文

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并寻求澄清。
