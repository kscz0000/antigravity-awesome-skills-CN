# 技能编写最佳实践

> 学习如何编写能被 Claude 发现并成功使用的有效技能。

好的技能应该简洁、结构清晰，并经过真实使用测试。本指南提供实用的编写决策，帮助你编写 Claude 能够发现并有效使用的技能。

关于技能工作原理的概念性背景，请参见 [Skills 概览](/en/docs/agents-and-tools/agent-skills/overview)。

## 核心原则

### 简洁是关键

[上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows) 是公共资源。你的技能与 Claude 所需了解的所有其他内容共享上下文窗口，包括：

* 系统提示
* 对话历史
* 其他技能的元数据
* 你的实际请求

并非技能中的每个 token 都有直接成本。启动时，只会预加载所有技能的元数据（名称和描述）。Claude 仅在技能相关时才读取 SKILL.md，并且仅在需要时读取其他文件。然而，保持 SKILL.md 简洁仍然重要：一旦 Claude 加载它，每个 token 都会与对话历史和其他上下文竞争。

**默认假设**：Claude 已经非常聪明

只添加 Claude 还不具备的上下文。审视每条信息：

* "Claude 真的需要这个解释吗？"
* "我能假设 Claude 知道这一点吗？"
* "这段话是否值得它的 token 成本？"

**好示例：简洁**（约 50 个 token）：

````markdown  theme={null}
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**坏示例：过于冗长**（约 150 个 token）：

```markdown  theme={null}
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but we
recommend pdfplumber because it's easy to use and handles most cases well.
First, you'll need to install it using pip. Then you can use the code below...
```

简洁版本假设 Claude 已经知道 PDF 是什么以及库的工作方式。

### 设定适当的自由度

将具体程度与任务的脆弱性和可变性相匹配。

**高自由度**（基于文本的指令）：

使用时机：

* 多种方法都有效
* 决策取决于上下文
* 启发式方法指导做法

示例：

```markdown  theme={null}
## Code review process

1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability and maintainability
4. Verify adherence to project conventions
```

**中自由度**（伪代码或带参数的脚本）：

使用时机：

* 存在首选模式
* 允许一定变化
* 配置影响行为

示例：

````markdown  theme={null}
## Generate report

Use this template and customize as needed:

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```
````

**低自由度**（特定脚本，无参数或参数很少）：

使用时机：

* 操作脆弱且容易出错
* 一致性至关重要
* 必须遵循特定顺序

示例：

````markdown  theme={null}
## Database migration

Run exactly this script:

```bash
python scripts/migrate.py --verify --backup
```

Do not modify the command or add additional flags.
````

**类比**：将 Claude 想象成一个在路径上行走的机器人：

* **两边都是悬崖的窄桥**：只有一种安全的前进方式。提供具体的护栏和精确的指令（低自由度）。示例：必须按精确顺序运行的数据库迁移。
* **没有危险的空旷原野**：许多路径都能成功。给出总体方向并信任 Claude 找到最佳路线（高自由度）。示例：代码审查中由上下文决定最佳方法。

### 使用你计划使用的所有模型进行测试

技能作为模型的扩展而发挥作用，因此效果取决于底层模型。使用你计划使用的所有模型测试你的技能。

**按模型的测试考虑**：

* **Claude Haiku**（快速、经济）：技能是否提供了足够的指导？
* **Claude Sonnet**（平衡型）：技能是否清晰且高效？
* **Claude Opus**（强推理能力）：技能是否避免了过度解释？

对 Opus 完美的方案可能需要为 Haiku 增加更多细节。如果你计划跨多个模型使用你的技能，请让指令在所有模型上都能良好工作。

## 技能结构

<Note>
  **YAML Frontmatter**：SKILL.md frontmatter 支持两个字段：

  * `name` - 技能的可读名称（最多 64 个字符）
  * `description` - 技能做什么以及何时使用的一句话描述（最多 1024 个字符）

  有关完整的技能结构详情，请参见 [Skills 概览](/en/docs/agents-and-tools/agent-skills/overview#skill-structure)。
</Note>

### 命名约定

使用一致的命名模式使技能更易于引用和讨论。我们建议对技能名称使用 **动名词形式**（动词 + -ing），因为这能清晰地描述技能提供的活动或能力。

**好的命名示例（动名词形式）**：

* "Processing PDFs"
* "Analyzing spreadsheets"
* "Managing databases"
* "Testing code"
* "Writing documentation"

**可接受的替代方案**：

* 名词短语："PDF Processing"、"Spreadsheet Analysis"
* 动作导向："Process PDFs"、"Analyze Spreadsheets"

**避免**：

* 模糊的名称："Helper"、"Utils"、"Tools"
* 过于宽泛："Documents"、"Data"、"Files"
* 技能集合中的命名模式不一致

一致的命名便于：

* 在文档和对话中引用技能
* 一眼理解技能的功能
* 组织和搜索多个技能
* 维护专业且有凝聚力的技能库

### 编写有效的描述

`description` 字段使技能可被发现，应包含技能做什么以及何时使用。

<Warning>
  **始终使用第三人称编写**。描述被注入到系统提示中，不一致的视角会导致发现问题。

  * **好：** "Processes Excel files and generates reports"
  * **避免：** "I can help you process Excel files"
  * **避免：** "You can use this to process Excel files"
</Warning>

**要具体并包含关键术语**。同时包含技能做什么以及何时使用的具体触发条件/上下文。

每个技能有且仅有一个 description 字段。描述对技能选择至关重要：Claude 用它来从可能 100+ 个可用技能中选择正确的技能。你的描述必须提供足够细节让 Claude 知道何时选择本技能，而 SKILL.md 的其余部分提供实现细节。

有效示例：

**PDF 处理技能：**

```yaml  theme={null}
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Excel 分析技能：**

```yaml  theme={null}
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

**Git 提交助手技能：**

```yaml  theme={null}
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

避免像这样含糊的描述：

```yaml  theme={null}
description: Helps with documents
```

```yaml  theme={null}
description: Processes data
```

```yaml  theme={null}
description: Does stuff with files
```

### 渐进披露模式

SKILL.md 充当概览，将 Claude 指向所需的详细材料，如同入职指南中的目录。有关渐进披露工作原理的解释，请参见概览中的 [技能如何工作](/en/docs/agents-and-tools/agent-skills/overview#how-skills-work)。

**实用指导：**

* 将 SKILL.md 正文保持在 500 行以下以获得最佳性能
* 接近此限制时将内容拆分为单独文件
* 使用下面的模式有效地组织指令、代码和资源

#### 视觉概览：从简单到复杂

一个基础技能从一个 SKILL.md 文件开始，其中包含元数据和指令：

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=87782ff239b297d9a9e8e1b72ed72db9" alt="Simple SKILL.md file showing YAML frontmatter and markdown body" data-og-width="2048" width="2048" data-og-height="1153" height="1153" data-path="images/agent-skills-simple-file.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=c61cc33b6f5855809907f7fda94cd80e 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=90d2c0c1c76b36e8d485f49e0810dbfd 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=ad17d231ac7b0bea7e5b4d58fb4aeabb 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f5d0a7a3c668435bb0aee9a3a8f8c329 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0e927c1af9de5799cfe557d12249f6e6 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-simple-file.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=46bbb1a51dd4c8202a470ac8c80a893d 2500w" />

随着技能的成长，你可以捆绑 Claude 仅在需要时加载的额外内容：

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=a5e0aa41e3d53985a7e3e43668a33ea3" alt="Bundling additional reference files like reference.md and forms.md." data-og-width="2048" width="2048" data-og-height="1327" height="1327" data-path="images/agent-skills-bundling-content.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=f8a0e73783e99b4a643d79eac86b70a2 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=dc510a2a9d3f14359416b706f067904a 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=82cd6286c966303f7dd914c28170e385 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=56f3be36c77e4fe4b523df209a6824c6 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=d22b5161b2075656417d56f41a74f3dd 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-bundling-content.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=3dd4bdd6850ffcc96c6c45fcb0acd6eb 2500w" />

完整的技能目录结构可能如下所示：

```
pdf/
├── SKILL.md              # Main instructions (loaded when triggered)
├── FORMS.md              # Form-filling guide (loaded as needed)
├── reference.md          # API reference (loaded as needed)
├── examples.md           # Usage examples (loaded as needed)
└── scripts/
    ├── analyze_form.py   # Utility script (executed, not loaded)
    ├── fill_form.py      # Form filling script
    └── validate.py       # Validation script
```

#### 模式 1：带有引用的高层指南

````markdown  theme={null}
---
name: PDF Processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

## Quick start

Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features

**Form filling**: See FORMS.md for complete guide
**API reference**: See REFERENCE.md for all methods
**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
````

Claude 仅在需要时加载 FORMS.md、REFERENCE.md 或 EXAMPLES.md。

#### 模式 2：领域特定组织

对于多领域技能，按领域组织内容以避免加载不相关的上下文。当用户询问销售指标时，Claude 只需要读取销售相关的 schema，而不需要财务或营销数据。这降低了 token 使用量并使上下文更聚焦。

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

````markdown SKILL.md theme={null}
# BigQuery Data Analysis

## Available datasets

**Finance**: Revenue, ARR, billing → See reference/finance.md
**Sales**: Opportunities, pipeline, accounts → See reference/sales.md
**Product**: API usage, features, adoption → See reference/product.md
**Marketing**: Campaigns, attribution, email → See reference/marketing.md

## Quick search

Find specific metrics using grep:

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
```
````

#### 模式 3：条件性细节

展示基本内容，链接到高级内容：

```markdown  theme={null}
# DOCX Processing

## Creating documents

Use docx-js for new documents. See DOCX-JS.md.

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See REDLINING.md
**For OOXML details**: See OOXML.md
```

Claude 仅在用户需要这些功能时读取 REDLINING.md 或 OOXML.md。

### 避免深度嵌套引用

当文件被从其他被引用的文件中引用时，Claude 可能会部分读取文件。遇到嵌套引用时，Claude 可能会使用 `head -100` 等命令预览内容而不是读取整个文件，导致信息不完整。

**保持引用距 SKILL.md 一层深**。所有引用文件都应直接从 SKILL.md 链接，以确保 Claude 在需要时读取完整文件。

**坏示例：太深**：

```markdown  theme={null}
# SKILL.md
See advanced.md...

# advanced.md
See details.md...

# details.md
Here's the actual information...
```

**好示例：一层深**：

```markdown  theme={null}
# SKILL.md

**Basic usage**: [instructions in SKILL.md]
**Advanced features**: See advanced.md
**API reference**: See reference.md
**Examples**: See [examples.md](examples.md)
```

### 用目录结构化较长的参考文件

对于超过 100 行的参考文件，在顶部包含目录。这确保 Claude 即使在使用部分读取预览时也能看到可用信息的完整范围。

**示例**：

```markdown  theme={null}
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns
- Code examples

## Authentication and setup
...

## Core methods
...
```

Claude 然后可以读取完整文件或根据需要跳到特定章节。

有关基于此文件系统的架构如何实现渐进披露的详细信息，请参见下面"高级"部分中的 [运行时环境](#runtime-environment) 部分。

## 工作流和反馈循环

### 对复杂任务使用工作流

将复杂操作分解为清晰的、顺序的步骤。对于特别复杂的工作流，提供一个 Claude 可以复制到其回复中并在推进过程中勾掉的清单。

**示例 1：研究综合工作流**（针对无代码的技能）：

````markdown  theme={null}
## Research synthesis workflow

Copy this checklist and track your progress:

```
Research Progress:
- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create structured summary
- [ ] Step 5: Verify citations
```

**Step 1: Read all source documents**

Review each document in the `sources/` directory. Note the main arguments and supporting evidence.

**Step 2: Identify key themes**

Look for patterns across sources. What themes appear repeatedly? Where do sources agree or disagree?

**Step 3: Cross-reference claims**

For each major claim, verify it appears in the source material. Note which source supports each point.

**Step 4: Create structured summary**

Organize findings by theme. Include:
- Main claim
- Supporting evidence from sources
- Conflicting viewpoints (if any)

**Step 5: Verify citations**

Check that every claim references the correct source document. If citations are incomplete, return to Step 3.
````

此示例展示了工作流如何应用于不需要代码的分析任务。清单模式适用于任何复杂的多步骤过程。

**示例 2：PDF 表单填写工作流**（针对带代码的技能）：

````markdown  theme={null}
## PDF form filling workflow

Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze the form**

Run: `python scripts/analyze_form.py input.pdf`

This extracts form fields and their locations, saving to `fields.json`.

**Step 2: Create field mapping**

Edit `fields.json` to add values for each field.

**Step 3: Validate mapping**

Run: `python scripts/validate_fields.py fields.json`

Fix any validation errors before continuing.

**Step 4: Fill the form**

Run: `python scripts/fill_form.py input.pdf fields.json output.pdf`

**Step 5: Verify output**

Run: `python scripts/verify_output.py output.pdf`

If verification fails, return to Step 2.
````

清晰的步骤防止 Claude 跳过关键验证。清单帮助 Claude 和你跟踪多步骤工作流的进度。

### 实施反馈循环

**常见模式**：运行验证器 → 修复错误 → 重复

此模式显著提高输出质量。

**示例 1：风格指南合规**（针对无代码的技能）：

```markdown  theme={null}
## Content review process

1. Draft your content following the guidelines in STYLE_GUIDE.md
2. Review against the checklist:
   - Check terminology consistency
   - Verify examples follow the standard format
   - Confirm all required sections are present
3. If issues found:
   - Note each issue with specific section reference
   - Revise the content
   - Review the checklist again
4. Only proceed when all requirements are met
5. Finalize and save the document
```

此示例展示了使用参考文档而非脚本的验证循环模式。"验证器"是 STYLE\_GUIDE.md，Claude 通过阅读和比较来执行检查。

**示例 2：文档编辑流程**（针对带代码的技能）：

```markdown  theme={null}
## Document editing process

1. Make your edits to `word/document.xml`
2. **Validate immediately**: `python ooxml/scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues in the XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. Test the output document
```

验证循环尽早捕获错误。

## 内容指南

### 避免时间敏感信息

不要包含会过时的信息：

**坏示例：时间敏感**（将变得不正确）：

```markdown  theme={null}
If you're doing this before August 2025, use the old API.
After August 2025, use the new API.
```

**好示例**（使用 "old patterns" 部分）：

```markdown  theme={null}
## Current method

Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>

The v1 API used: `api.example.com/v1/messages`

This endpoint is no longer supported.
</details>
```

"old patterns" 部分提供历史背景而不杂乱主要内容。

### 使用一致的术语

选择一个术语并在整个技能中一致使用：

**好 - 一致**：

* 始终 "API endpoint"
* 始终 "field"
* 始终 "extract"

**坏 - 不一致**：

* 混用 "API endpoint"、"URL"、"API route"、"path"
* 混用 "field"、"box"、"element"、"control"
* 混用 "extract"、"pull"、"get"、"retrieve"

一致性帮助 Claude 理解和遵循指令。

## 常见模式

### 模板模式

为输出格式提供模板。将严格程度与你的需求相匹配。

**对于严格要求**（如 API 响应或数据格式）：

````markdown  theme={null}
## Report structure

ALWAYS use this exact template structure:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```
````

**对于灵活指导**（当适应有用时）：

````markdown  theme={null}
## Report structure

Here is a sensible default format, but use your best judgment based on the analysis:

```markdown
# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]
```

Adjust sections as needed for the specific analysis type.
````

### 示例模式

对于输出质量依赖于看示例的技能，像常规提示中一样提供输入/输出对：

````markdown  theme={null}
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

**Example 3:**
Input: Updated dependencies and refactored error handling
Output:
```
chore: update dependencies and refactor error handling

- Upgrade lodash to 4.17.21
- Standardize error response format across endpoints
```

Follow this style: type(scope): brief description, then detailed explanation.
````

示例帮助 Claude 比仅凭描述更清晰地理解期望的风格和细节水平。

### 条件性工作流模式

引导 Claude 通过决策点：

```markdown  theme={null}
## Document modification workflow

1. Determine the modification type:

   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   - Use docx-js library
   - Build document from scratch
   - Export to .docx format

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
   - Repack when complete
```

<Tip>
  如果工作流变得大或复杂且有许多步骤，请考虑将它们推入单独文件并告诉 Claude 根据手头的任务读取适当的文件。
</Tip>

## 评估和迭代

### 先构建评估

**在编写大量文档之前创建评估。** 这确保了你的技能解决的是真实问题而非想象中的问题。

**评估驱动的开发：**

1. **识别差距**：在没有技能的情况下在代表性任务上运行 Claude。记录具体的失败或缺失的上下文
2. **创建评估**：构建三个测试这些差距的场景
3. **建立基线**：在没有技能的情况下测量 Claude 的性能
4. **编写最小指令**：创建刚好足够的内容来解决差距并通过评估
5. **迭代**：执行评估，与基线比较，并改进

此方法确保你正在解决实际问题，而不是预测可能永远不会出现的需求。

**评估结构**：

```json  theme={null}
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using an appropriate PDF processing library or command-line tool",
    "Extracts text content from all pages in the document without missing any pages",
    "Saves the extracted text to a file named output.txt in a clear, readable format"
  ]
}
```

<Note>
  此示例演示了一个带有简单测试评分标准的数据驱动评估。我们目前不提供内置的方式来运行这些评估。用户可以创建自己的评估系统。评估是衡量技能有效性的真理之源。
</Note>

### 与 Claude 迭代开发技能

最有效的技能开发过程涉及 Claude 本身。与一个 Claude 实例（"Claude A"）合作创建一个将被其他实例（"Claude B"）使用的技能。Claude A 帮助您设计和改进指令，而 Claude B 在真实任务中测试它们。这有效是因为 Claude 模型既理解如何编写有效的智能体指令，又理解智能体需要什么信息。

**创建新技能：**

1. **在没有技能的情况下完成任务**：使用正常提示与 Claude A 一起完成问题。在工作时，你自然会提供上下文、解释偏好并分享程序性知识。注意到你重复提供的信息。

2. **识别可重用模式**：完成任务后，确定你提供的哪些上下文对类似未来任务有用。

   **示例**：如果你完成了 BigQuery 分析，你可能提供了表名、字段定义、过滤规则（如"始终排除测试账户"）和常见查询模式。

3. **要求 Claude A 创建技能**："创建一个捕获我们刚使用的 BigQuery 分析模式的技能。包括表 schema、命名约定和过滤测试账户的规则。"

   <Tip>
     Claude 模型原生理解技能格式和结构。你不需要特殊的系统提示或"编写技能"技能来让 Claude 帮助创建技能。只需要求 Claude 创建技能，它就会生成结构正确的 SKILL.md 内容，包含适当的 frontmatter 和正文。
   </Tip>

4. **审查简洁性**：检查 Claude A 没有添加不必要的解释。问："删除关于什么是胜率的解释 - Claude 已经知道了。"

5. **改进信息架构**：要求 Claude A 更有效地组织内容。例如："组织一下，将表 schema 放在单独的参考文件中。我们以后可能添加更多表。"

6. **在类似任务上测试**：在新实例（加载了技能的 Claude B）上对相关用例使用该技能。观察 Claude B 是否找到正确信息、正确应用规则并成功处理任务。

7. **根据观察迭代**：如果 Claude B 遇到困难或遗漏了什么，带着具体信息返回 Claude A："当 Claude 使用此技能时，它忘记按 Q4 过滤日期。我们应该添加一个关于日期过滤模式的部分吗？"

**迭代现有技能：**

相同的层次结构在改进技能时继续。你在以下之间交替：

* **与 Claude A 合作**（帮助改进技能的专家）
* **使用 Claude B 测试**（使用技能执行真实工作的智能体）
* **观察 Claude B 的行为**并将洞察带回 Claude A

1. **在真实工作流中使用技能**：给 Claude B（加载了技能）实际任务，而非测试场景

2. **观察 Claude B 的行为**：注意它在何处挣扎、成功或做出意外选择

   **观察示例**："当我要求 Claude B 给出区域销售报告时，它写了查询但忘记过滤掉测试账户，即使技能提到了此规则。"

3. **返回 Claude A 寻求改进**：分享当前的 SKILL.md 并描述你观察到的内容。问："我注意到当我要求区域报告时 Claude B 忘记过滤测试账户。技能提到了过滤，但也许它不够突出？"

4. **审查 Claude A 的建议**：Claude A 可能建议重新组织以使规则更突出，使用更强的语言如 "MUST filter" 而不是 "always filter"，或重构工作流部分。

5. **应用并测试更改**：使用 Claude A 的改进更新技能，然后在类似请求上用 Claude B 重新测试

6. **根据使用情况重复**：当遇到新场景时，继续这种观察-改进-测试循环。每次迭代都基于实际智能体行为而非假设来改进技能。

**收集团队反馈：**

1. 与队友分享技能并观察他们的使用情况
2. 问：技能是否在预期时激活？指令是否清晰？缺少什么？
3. 纳入反馈以解决你自己使用模式中的盲点

**为何此方法有效**：Claude A 理解智能体需求，你提供领域专业知识，Claude B 通过真实使用揭示差距，迭代改进基于观察到的行为而非假设来改进技能。

### 观察 Claude 如何浏览技能

当你在技能上迭代时，注意 Claude 实际上如何在实践中使用它们。注意以下情况：

* **意外的探索路径**：Claude 是否按你未预料的顺序读取文件？这可能表明你的结构不像你想的那样直观
* **遗漏的连接**：Claude 是否未能遵循对重要文件的引用？你的链接可能需要更明确或更突出
* **过度依赖某些部分**：如果 Claude 重复读取同一文件，请考虑该内容是否应放在主 SKILL.md 中
* **被忽略的内容**：如果 Claude 从不访问捆绑文件，它可能是不必要的或在主要指令中信号不足

根据这些观察而非假设进行迭代。技能元数据中的 'name' 和 'description' 特别关键。Claude 在决定是否针对当前任务触发技能时使用这些。确保它们清楚地描述技能做什么以及何时应使用。

## 应避免的反模式

### 避免 Windows 风格的路径

始终在文件路径中使用正斜杠，即使在 Windows 上：

* ✓ **好**：`scripts/helper.py`、`reference/guide.md`
* ✗ **避免**：`scripts\helper.py`、`reference\guide.md`

Unix 风格的路径适用于所有平台，而 Windows 风格的路径在 Unix 系统上会导致错误。

### 避免提供太多选项

除非必要，不要提供多种方法：

````markdown  theme={null}
**Bad example: Too many choices** (confusing):
"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."

**Good example: Provide a default** (with escape hatch):
"Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."
````

## 进阶：带可执行代码的技能

以下部分侧重于包含可执行脚本的技能。如果你的技能仅使用 markdown 指令，请跳到 [有效技能清单](#checklist-for-effective-skills)。

### 解决问题，不要推诿

在为技能编写脚本时，处理错误情况而非将问题推给 Claude。

**好示例：明确处理错误**：

```python  theme={null}
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # Create file with default content instead of failing
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
    except PermissionError:
        # Provide alternative instead of failing
        print(f"Cannot access {path}, using default")
        return ''
```

**坏示例：推诿给 Claude**：

```python  theme={null}
def process_file(path):
    # Just fail and let Claude figure it out
    return open(path).read()
```

配置参数也应合理并记录在案以避免"玄学常量"（Ousterhout 法则）。如果你不知道正确的值，Claude 怎么能确定？

**好示例：自我说明**：

```python  theme={null}
# HTTP requests typically complete within 30 seconds
# Longer timeout accounts for slow connections
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed
# Most intermittent failures resolve by the second retry
MAX_RETRIES = 3
```

**坏示例：魔法数字**：

```python  theme={null}
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```

### 提供实用脚本

即使 Claude 可以编写脚本，预制脚本也有优势：

**实用脚本的好处**：

* 比生成的代码更可靠
* 节省 token（不需要将代码包含在上下文中）
* 节省时间（无需生成代码）
* 确保跨使用的一致性

<img src="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=4bbc45f2c2e0bee9f2f0d5da669bad00" alt="Bundling executable scripts alongside instruction files" data-og-width="2048" width="2048" data-og-height="1154" height="1154" data-path="images/agent-skills-executable-scripts.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=280&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=9a04e6535a8467bfeea492e517de389f 280w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=560&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=e49333ad90141af17c0d7651cca7216b 560w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=840&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=954265a5df52223d6572b6214168c428 840w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1100&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=2ff7a2d8f2a83ee8af132b29f10150fd 1100w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=1650&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=48ab96245e04077f4d15e9170e081cfb 1650w, https://mintcdn.com/anthropic-claude-docs/4Bny2bjzuGBK7o00/images/agent-skills-executable-scripts.png?w=2500&fit=max&auto=format&n=4Bny2bjzuGBK7o00&q=85&s=0301a6c8b3ee879497cc5b5483177c90 2500w" />

上面的图示展示了可执行脚本如何与指令文件一起工作。指令文件（forms.md）引用脚本，Claude 可以执行它而无需将其内容加载到上下文中。

**重要区别**：在你的指令中明确说明 Claude 应该：

* **执行脚本**（最常见）："运行 `analyze_form.py` 来提取字段"
* **作为参考读取**（用于复杂逻辑）："参见 `analyze_form.py` 了解字段提取算法"

对于大多数实用脚本，优先选择执行，因为它更可靠且高效。有关脚本执行如何工作的详细信息，请参见下面的 [运行时环境](#runtime-environment) 部分。

**示例**：

````markdown  theme={null}
## Utility scripts

**analyze_form.py**: Extract all form fields from PDF

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

Output format:
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

**validate_boxes.py**: Check for overlapping bounding boxes

```bash
python scripts/validate_boxes.py fields.json
# Returns: "OK" or lists conflicts
```

**fill_form.py**: Apply field values to PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
````

### 使用视觉分析

当输入可以渲染为图像时，让 Claude 分析它们：

````markdown  theme={null}
## Form layout analysis

1. Convert PDF to images:
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. Analyze each page image to identify form fields
3. Claude can see field locations and types visually
````

<Note>
  在此示例中，你需要编写 `pdf_to_images.py` 脚本。
</Note>

Claude 的视觉能力有助于理解布局和结构。

### 创建可验证的中间输出

当 Claude 执行复杂的开放式任务时，它可能会出错。"计划-验证-执行"模式通过让 Claude 首先以结构化格式创建计划，然后在使用脚本验证该计划之后再执行，从而尽早捕获错误。

**示例**：想象一下让 Claude 根据电子表格更新 PDF 中的 50 个表单字段。如果没有验证，Claude 可能会引用不存在的字段、创建冲突值、遗漏必填字段或不正确地应用更新。

**解决方案**：使用上面展示的工作流模式（PDF 表单填写），但添加一个中间的 `changes.json` 文件，在应用更改之前进行验证。工作流变为：分析 → **创建计划文件** → **验证计划** → 执行 → 验证。

**此模式为何有效：**

* **尽早捕获错误**：验证在应用更改之前发现问题
* **机器可验证**：脚本提供客观验证
* **可逆的规划**：Claude 可以在不触及原始文件的情况下迭代计划
* **清晰的调试**：错误消息指向具体问题

**使用时机**：批量操作、破坏性更改、复杂验证规则、高风险操作。

**实施提示**：使验证脚本详细且带有具体错误消息，例如"找不到 'signature\_date' 字段。可用字段：customer\_name, order\_total, signature\_date\_signed"，以帮助 Claude 修复问题。

### 打包依赖

技能在具有平台特定限制的代码执行环境中运行：

* **claude.ai**：可以从 npm 和 PyPI 安装包并从 GitHub 仓库拉取
* **Anthropic API**：没有网络访问和运行时包安装

在 SKILL.md 中列出必需的包，并验证它们在 [代码执行工具文档](/en/docs/agents-and-tools/tool-use/code-execution-tool) 中可用。

### 运行时环境

技能在具有文件系统访问、bash 命令和代码执行能力的代码执行环境中运行。有关此架构的概念性解释，请参见概览中的 [技能架构](/en/docs/agents-and-tools/agent-skills/overview#the-skills-architecture)。

**这如何影响你的编写：**

**Claude 如何访问技能：**

1. **预加载元数据**：启动时，所有技能 YAML frontmatter 中的名称和描述被加载到系统提示中
2. **按需读取文件**：Claude 在需要时使用 bash Read 工具从文件系统访问 SKILL.md 和其他文件
3. **高效执行脚本**：实用脚本可以通过 bash 执行而无需将其完整内容加载到上下文中。只有脚本的输出消耗 token
4. **大文件无上下文损失**：参考文件、数据或文档在实际读取之前不消耗上下文 token

* **文件路径很重要**：Claude 像文件系统一样浏览你的技能目录。使用正斜杠（`reference/guide.md`），而不是反斜杠
* **描述性命名文件**：使用指示内容的名称：`form_validation_rules.md`，而不是 `doc2.md`
* **组织以便发现**：按领域或功能组织目录
  * 好：`reference/finance.md`、`reference/sales.md`
  * 坏：`docs/file1.md`、`docs/file2.md`
* **捆绑综合资源**：包括完整的 API 文档、大量示例、大型数据集；在访问之前没有上下文损失
* **对确定性操作优先选择脚本**：编写 `validate_form.py` 而不是要求 Claude 生成验证代码
* **明确执行意图**：
  * "运行 `analyze_form.py` 来提取字段"（执行）
  * "参见 `analyze_form.py` 了解提取算法"（作为参考读取）
* **测试文件访问模式**：通过真实请求测试来验证 Claude 能够浏览你的目录结构

**示例：**

```
bigquery-skill/
├── SKILL.md (overview, points to reference files)
└── reference/
    ├── finance.md (revenue metrics)
    ├── sales.md (pipeline data)
    └── product.md (usage analytics)
```

当用户询问收入时，Claude 读取 SKILL.md，看到对 `reference/finance.md` 的引用，并调用 bash 仅读取该文件。sales.md 和 product.md 文件保留在文件系统中，在需要之前消耗零上下文 token。这种基于文件系统的模型是实现渐进披露的原因。Claude 可以导航并选择性地加载每个任务所需的内容。

有关技术架构的完整详细信息，请参见 Skills 概览中的 [技能如何工作](/en/docs/agents-and-tools/agent-skills/overview#how-skills-work)。

### MCP 工具引用

如果你的技能使用 MCP（Model Context Protocol）工具，始终使用完全限定的工具名称以避免"工具未找到"错误。

**格式**：`ServerName:tool_name`

**示例**：

```markdown  theme={null}
Use the BigQuery:bigquery_schema tool to retrieve table schemas.
Use the GitHub:create_issue tool to create issues.
```

其中：

* `BigQuery` 和 `GitHub` 是 MCP 服务器名称
* `bigquery_schema` 和 `create_issue` 是这些服务器内的工具名称

没有服务器前缀，Claude 可能无法定位工具，尤其是在有多个 MCP 服务器可用时。

### 不要假设工具已安装

不要假设包可用：

````markdown  theme={null}
**Bad example: Assumes installation**:
"Use the pdf library to process the file."

**Good example: Explicit about dependencies**:
"Install required package: `pip install pypdf`

Then use it:
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```"
````

## 技术说明

### YAML frontmatter 要求

SKILL.md frontmatter 仅包含 `name`（最多 64 个字符）和 `description`（最多 1024 个字符）字段。有关完整的结构详情，请参见 [Skills 概览](/en/docs/agents-and-tools/agent-skills/overview#skill-structure)。

### Token 预算

将 SKILL.md 正文保持在 500 行以下以获得最佳性能。如果你的内容超过此限制，请使用前面描述的渐进披露模式将其拆分为单独文件。有关架构详情，请参见 [Skills 概览](/en/docs/agents-and-tools/agent-skills/overview#how-skills-work)。

## 有效技能清单

在分享技能之前，验证：

### 核心质量

* [ ] 描述具体并包含关键术语
* [ ] 描述同时包含技能做什么以及何时使用
* [ ] SKILL.md 正文少于 500 行
* [ ] 其他详情在单独文件中（如需要）
* [ ] 没有时间敏感信息（或在 "old patterns" 部分中）
* [ ] 整个文档中术语一致
* [ ] 示例具体而非抽象
* [ ] 文件引用一层深
* [ ] 适当地使用了渐进披露
* [ ] 工作流有清晰的步骤

### 代码和脚本

* [ ] 脚本解决问题而非推诿给 Claude
* [ ] 错误处理明确且有帮助
* [ ] 没有"玄学常量"（所有值都有理由）
* [ ] 必需包在指令中列出并验证可用
* [ ] 脚本有清晰的文档
* [ ] 没有 Windows 风格的路径（全部使用正斜杠）
* [ ] 关键操作有验证/验证步骤
* [ ] 质量关键任务包含反馈循环

### 测试

* [ ] 至少创建了三个评估
* [ ] 使用 Haiku、Sonnet 和 Opus 进行了测试
* [ ] 用真实使用场景测试
* [ ] 已纳入团队反馈（如适用）

## 下一步

<CardGroup cols={2}>
  <Card title="开始使用 Agent Skills" icon="rocket" href="/en/docs/agents-and-tools/agent-skills/quickstart">
    Create your first Skill
  </Card>

  <Card title="在 Claude Code 中使用技能" icon="terminal" href="/en/docs/claude-code/skills">
    Create and manage Skills in Claude Code
  </Card>

  <Card title="通过 API 使用技能" icon="code" href="/en/api/skills-guide">
    Upload and use Skills programmatically
  </Card>
</CardGroup>
