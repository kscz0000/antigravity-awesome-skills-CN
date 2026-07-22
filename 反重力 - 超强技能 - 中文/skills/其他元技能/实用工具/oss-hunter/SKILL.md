---
name: oss-hunter
description: "自动发现热门仓库中的高影响力开源贡献机会。当用户要求查找开源issue、寻找贡献机会、发现help-wanted任务、生成贡献报告时使用。"
risk: safe
source: "https://github.com/jackjin1997/ClawForge"
date_added: "2026-02-27"
---

# OSS Hunter 🎯

精准技能，帮助智能体发现、分析并制定高影响力开源贡献策略。本技能帮助你成为顶级贡献者，通过识别热门仓库中最"可合并"且最具影响力的issue。

## 使用时机
- 用户要求查找可参与的开源issue时使用
- 在特定领域（如AI或Web3）搜索"help wanted"或"good first issue"任务时使用
- 为热门项目生成包含可执行策略的"贡献档案"时使用

## 快速开始

向你的智能体提问：
- "在热门AI仓库中找一些help-wanted的issue"
- "在langchain-ai/langchain中寻找适合快速PR的bug修复"
- "为GitHub上最新的热门项目生成贡献档案"

## 工作流程

寻找贡献机会时，智能体遵循以下多阶段协议：

### 阶段1：仓库发现
使用 `web_search` 或 `gh api` 查找热门仓库。
关注：
- Stars > 1000
- 近期活跃（24小时内有推送）
- 相关主题（AI、Agentic、Web3、工具）

### 阶段2：Issue提取
搜索特定标签：
- `help-wanted`
- `good-first-issue`
- `bug`
- `v1` / `roadmap`

```bash
gh issue list --repo owner/repo --label "help wanted" --limit 10
```

### 阶段3：可行性分析
分析issue：
1. **可复现性**：是否有代码片段可复现bug？
2. **影响力**：影响多少用户？
3. **可合并性**：检查近期PR历史。维护者是否快速合并社区PR？
4. **复杂度**：当前工具的智能体能否解决？

### 阶段4：档案生成
为用户生成结构化报告：
- **项目名称与Stars**
- **Issue链接与描述**
- **根因分析**（基于代码检查）
- **建议修复策略**
- **信心评分**（1-10）

## 限制

- 准确性取决于 `gh` CLI 或 `web_search` 工具的可用性。
- 读取大型仓库时受上下文窗口限制。
- 无法保证PR被接受（取决于维护者决定）。

---

## 为矩阵做贡献

通过向阶段3添加新启发式规则来构建更好的hunter。将你的改进提交到 [ClawForge](https://github.com/jackjin1997/ClawForge)。

*由 OpenClaw & ClawForge 驱动。*
