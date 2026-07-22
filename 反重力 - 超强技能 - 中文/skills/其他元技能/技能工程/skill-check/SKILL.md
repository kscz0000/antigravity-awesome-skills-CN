---
name: skill-check
description: "根据 agentskills 规范验证 Claude Code 技能。在用户发现问题之前捕获结构、语义和命名问题。当用户说'检查技能'、'skillcheck'、'验证 SKILL.md'、'技能验证'、'技能检查'时使用。"
category: development
risk: safe
source: https://github.com/olgasafonova/SkillCheck-Free
date_added: "2026-03-11"
author: olgasafonova
tags: [validation, linter, agentskills, skill-authoring, code-quality]
tools: [claude, cursor, windsurf, codex-cli]
license: MIT
allowed-tools: Read Glob
compatibility: claude-code
---

# SkillCheck

## 概述

根据 [agentskills 规范](https://agentskills.io)和 Anthropic 最佳实践验证 SKILL.md 文件。通过单次只读扫描捕获结构错误、语义矛盾、命名反模式和质量缺陷。

## 何时使用此技能

- 当用户说"检查技能"、"skillcheck"或"验证 SKILL.md"时使用
- 在发布技能到市场前审查时使用
- 调试技能为何无法正确触发时使用
- 团队入门技能编写标准时使用
- 不要用于反垃圾检测、安全扫描或 token 分析；这些功能需要使用 [SkillCheck Pro](https://getskillcheck.com)

## 工作原理

### 步骤 1：解析

读取目标 SKILL.md 文件并提取 YAML frontmatter。

### 步骤 2：验证

按顺序应用所有免费层级检查：

| 类别 | 检查项 | 捕获内容 |
|------|--------|----------|
| 结构 (1.x) | 名称格式、description 的 WHAT+WHEN、allowed-tools、categories、XML 注入 | 格式错误的 frontmatter、缺失字段 |
| 正文 (2.x) | 行数、硬编码路径、过期日期、空白章节、废弃语法、MCP 工具资格 | 内容质量问题 |
| 命名 (3.x) | 模糊术语、单词名称、动名词建议 | 可发现性差 |
| 语义 (4.x) | 矛盾、歧义术语、缺失输出格式、空泛建议/陈词滥调、触发器位置错误 | 逻辑不一致 |
| 质量 (8.x) | 示例、错误处理、触发器、输出格式、前置条件、负面触发器 | 优势（正向模式） |

### 步骤 3：评分

计算总分（0-100）。扣分规则：严重 = -20，警告 = -5，建议 = -1。

### 步骤 4：报告

返回结构化结果：分数、等级（优秀/良好/需改进/差）、包含检查 ID、行号、消息和修复建议的问题列表。

## 示例

### 示例 1：验证技能

```
用户：检查我的技能 ~/.claude/skills/weekly-report/SKILL.md

SkillCheck 输出：
## weekly-report 检查结果 [免费版]

分数：85/100（良好）

### 警告 (2)
  - 1.2-desc-when (第 3 行)：Description 缺少 WHEN 子句
  - 4.5-desc-no-triggers (第 3 行)：Description 缺少触发条件

### 建议 (1)
  - 3.4-gerund-naming (第 2 行)：技能名称可使用动名词形式

### 通过检查：28
```

### 示例 2：干净的技能通过所有检查

```
用户：skillcheck ~/.claude/skills/processing-pdfs/SKILL.md

分数：100/100（优秀）
全部 31 项检查通过。未发现问题。
```

## 限制

- 只读：不修改任何文件
- 免费层级仅覆盖结构、语义和命名检查
- 反垃圾、安全、WCAG、token、企业和工作流检查需要 [SkillCheck Pro](https://getskillcheck.com)
- 语义检查（矛盾检测、空泛建议/陈词滥调）为启发式，约有 5% 误报率
- 不验证引用的文件或脚本；仅检查 SKILL.md 内容
- 单文件验证；不会与同目录下的其他技能交叉检查

## 最佳实践

- 在提交技能到任何市场前运行 SkillCheck
- 修复所有严重和警告问题；建议为可选
- 使用检查 ID（如 `1.2-desc-when`）在技能正文中查找确切规则
- 修复后重新运行以确认分数提升

## 常见陷阱

- **问题：** 由于许多建议导致分数看起来很低
  **解决方案：** 建议最多扣 15 分。优先关注警告和严重问题。

- **问题：** 代码块内的歧义术语出现误报
  **解决方案：** SkillCheck 跳过代码块和行内代码。如果仍有误报，用反引号包裹该术语。

- **问题：** 空泛建议/陈词滥调检查标记了合理指令
  **解决方案：** 将泛泛建议（"记住测试很重要"）改写为具体指令（"提交前运行测试"）。
