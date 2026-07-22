---
name: latex-paper-conversion
description: "当用户要求将 LaTeX 学术论文从一种格式（如 Springer、IPOL）转换为另一种格式（如 MDPI、IEEE、Nature）时使用。自动完成内容提取、注入、格式修复和编译。"
risk: safe
source: community
date_added: "2026-03-14"
---

# LaTeX 论文格式转换

## 概述

本技能自动化了将 LaTeX 学术论文从一个出版商模板转换到另一个的繁琐重复流程。不同期刊（如 Springer、MDPI、IEEE）的结构要求、文档类、页边距设置和参考文献风格差异巨大。本技能通过执行结构化的多阶段工作流——提取内容、映射到新模板、解决常见编译错误——来简化这些转换。

## 何时使用本技能

- 用户要求将现有 LaTeX 论文迁移到新期刊格式时使用。
- 用户提供了现有 `.tex` 文件和新模板目录时使用。
- 用户提到从格式 A（如 IPOL/Neural Processing）转换为格式 B（如 MDPI）时使用。

## 工作原理

### 第 1 步：前置条件与评估
识别**源 LaTeX 文件**，并向用户索取**目标模板目录**。理解核心排版映射关系（单栏 vs 双栏、参考文献风格）。

### 第 2 步：提取与注入脚本生成
创建 Python 脚本（如 `convert_format.py`）来解析源 LaTeX 文件。使用正则表达式提取核心文本块。将新模板的 `preamble`、提取出的 `body` 和 `backmatter` 合并，写入输出目录中的新文件。

### 第 3 步：系统性修复
在写入最终文件之前，或在后续调用中，对提取的正文执行通用修复：
- 转换数学环境大小写（如 `\begin{theorem}` 改为 `\begin{Theorem}`）。
- 调整激进的浮动体位置参数（如 `[!t]` 或 `[h!]`）为模板支持的选项。除非显式加载了 `float` 宏包，否则不要强制使用 `[H]`。
- 确保 `\includegraphics` 路径相对于新 `.tex` 文件的位置。
- 若转为双栏布局，将 `\begin{tabular}` 转为 `\begin{tabularx}{\textwidth}` 或使用 `\resizebox`。

### 第 4 步：编译与调试
运行构建周期（`pdflatex` -> `bibtex` -> `pdflatex`）。使用 `grep` 或 `rg` 检查 `.log` 文件，系统性地修复宏包冲突、未定义命令或编译中断。

## 示例

### 示例 1：IPOL 转 MDPI
\```
USER: "我需要把论文 'SAHQR_Paper.tex' 转换为 'MDPI_template_ACS' 文件夹中的 MDPI 格式。"
AGENT: *触发 latex-paper-conversion 技能*
1. 分析源 `.tex` 和目标 `template.tex`。
2. 创建 Python 脚本提取 Introduction 到 Conclusion 的内容。
3. 将内容注入 MDPI 模板。
4. 更新图片路径和表格浮动参数 `[h!]` 为 `[H]`。
5. 通过 pdflatex 和 bibtex 编译，确认零错误。
\```

## 最佳实践

- ✅ 始终编写 Python 提取脚本；**不要**手动复制粘贴数千行 LaTeX。
- ✅ 始终运行 `pdflatex` 并检查 `.log` 文件，确保最终输出能编译通过。
- ✅ 源文件和目标模板差异较大时（如需要合并摘要和关键词），主动向用户确认结构映射。
- ❌ 不要假设所有数学宏包在新模板中都自动存在（如缺少则添加 `\usepackage{amsmath}`）。

## 常见陷阱

- **问题**：从单栏转为双栏时表格出现 Overfull hbox。
  **解决**：检测 `\begin{tabular}` 并自动用 `\resizebox{\columnwidth}{!}{...}` 包裹，或建议调整格式。
- **问题**：编译时出现 Undefined control sequence 错误。
  **解决**：搜索 `Paper.log`，在转换后的模板中补充缺失的 `\usepackage{}`。

## 其他资源

- [Overleaf LaTeX 文档](https://www.overleaf.com/learn)

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 输出结果不能替代针对具体环境的验证、测试或专家审校。
- 缺少必要输入、权限、安全边界或成功标准时，停下来向用户确认。
