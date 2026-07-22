# 📔 统一日记系统（智能体上下文保留日志记录器）v4.1

![Version](https://img.shields.io/badge/version-v4.1-blue)
![AI Agent](https://img.shields.io/badge/AI-Agent_Driven-orange)
![Sync](https://img.shields.io/badge/Sync-Notion%20%7C%20Obsidian-lightgrey)

**统一日记系统**是一个完全自动化、防污染的 AI 日志记录与同步工作流，专为多项目开发者和创作者设计。通过利用 AI 智能体的连续工具调用，一条自然语言命令即可自动执行 4 步流水线：**本地项目日志 ➔ 全局上下文融合 ➔ 云端双向同步 ➔ 经验提取**，实现真正的"单次"无缝记录。

---

## ✨ 核心特性

* ⚡ **智能体单次执行**：一旦触发，AI 将不间断完成整个技术流程，仅在最后一步暂停请求人工验证提取的"经验教训"。
* 🛡️ **上下文防火墙**：严格分离"项目本地日记"与"全局主日记"。从根本上解决了 AI 在每日总结时产生幻觉、混淆项目 A 和项目 B 进度的严重"上下文污染/标签漂移"问题。
* 🧠 **自动化经验总结**：不仅是事件时间线，AI 会主动从你今天遇到的 bug 或发现中提取"新规则"或"优化建议"，提炼到你的知识库。
* 🔄 **无缝跨平台同步**：内置脚本，只需一个 `--sync-only` 标志即可将最终全局日记直接推送到 Notion 和/或 Obsidian。

---

## 🏗️ 5 步工作流架构

当开发者在*任意*项目目录中输入 `:{Write a diary entry using the diary skill}` 时，系统将严格执行以下原子操作：

### 步骤 1：本地项目归档（AI 执行）
1. **自动定位**：AI 调用终端命令（如 `pwd`）识别当前工作目录，确定"项目名称"。
2. **精确写入**：以"追加模式"将今日的 Git 提交、代码变更和问题解决方案写入该项目本地目录：`diary/YYYY/MM/YYYY-MM-DD-<Project_Name>.md`。

### 步骤 1.5：刷新项目上下文（自动化脚本）
* **自动执行**：AI 调用 `prepare_context.py` 扫描项目的最新目录结构、技术栈和基于日记的行动项，在项目根目录生成/更新 `AGENT_CONTEXT.md`。

### 步骤 2：提取全局与项目素材（自动化脚本）
* **素材获取**：AI 自动执行 `fetch_diaries.py`，精确拉取"刚写入的本地项目日记"和今日的"全局日记（如存在）"，将两者打印到终端供 AI 读取。

### 步骤 3：AI 智能融合与全局归档（AI 执行）
* **无缝融合**：AI 在心智中将步骤 2 的两组素材缝合在一起，将合并结果写入全局日记库：`.../global_skills/auto-skill/diary/YYYY/MM/YYYY-MM-DD.md`。
* **严格分区**：使用 `### 📁 <Project Name>` 标签确保现有项目进度被保留，新项目进度安全追加——绝对不覆盖。

### 步骤 4：云端同步与经验提取（脚本 + 人工）
1. **一键推送**：AI 调用 `master_diary_sync.py --sync-only` 将数据推送到 Notion/Obsidian。
2. **人工授权**：AI 提取今日的 `📌 新规则` 或 `🔄 经验优化` 并呈现给开发者。授权后，这些内容被写入本地知识库并嵌入（如通过 `qmd embed`）。

---

## 📂 目录结构

本系统采用"分布式记录、集中管理"架构：

```text
📦 你的计算机环境
 ┣ 📂 项目 A（如：auto-video-editor）
 ┃ ┗ 📂 diary/YYYY/MM/
 ┃    ┗ 📜 2026-02-24-auto-video-editor.md  <-- 步骤 1 写入此处（干净、隔离的历史）
 ┣ 📂 项目 B（如：GSS）
 ┃ ┗ 📂 diary/YYYY/MM/
 ┃    ┗ 📜 2026-02-24-GSS.md                
 ┃
 ┗ 📂 全局技能与日记中心（本仓库）
    ┣ 📂 scripts/
    ┃  ┣ 📜 fetch_diaries.py                <-- 步骤 2：素材运输器
    ┃  ┣ 📜 prepare_context.py              <-- 步骤 1.5：上下文刷新器
    ┃  ┗ 📜 master_diary_sync.py            <-- 步骤 4：Notion/Obsidian 同步
    ┣ 📂 knowledge-base/                    <-- 步骤 4：AI 提取的经验
    ┗ 📂 diary/YYYY/MM/
       ┗ 📜 2026-02-24.md                   <-- 步骤 3：最终融合的全局日志
```

---

## 🚀 如何使用

在 `.env` 中配置好 Notion 令牌后，只需在项目工作中于 CLI/IDE 聊天中输入：

```bash
:{Write a diary entry using the diary skill} 今天我完成了 Google Colab Python 脚本的初步集成，并修复了包版本冲突。
```

系统将接管并自动处理所有归档、合并和同步工作。

---

## 🛠️ 设置与前提条件

1. **配置**：将 `.env.example` 重命名为 `.env` 并填写你的 `NOTION_TOKEN`、`NOTION_DIARY_DB`，并设置全局日记根目录的存储位置。
2. **依赖**：`pip install -r requirements.txt`
3. **AI 智能体**：需要具备函数调用/连续工具调用能力的 AI 助手（如 Cursor、Claude Code 或 Gemini CLI 框架）。

---

> **💡 设计理念：**
> 为什么不让 AI 直接写入全局日记？因为我们发现，当 AI 缺乏"隔离的本地项目上下文"时，它经常遭受**标签漂移**（将项目 A 的进度写在项目 B 的标题下）。通过这种高度结构化的"本地优先、全局其次"的 4 步架构，我们彻底消除了 AI 自动日志记录中的上下文污染痛点。
