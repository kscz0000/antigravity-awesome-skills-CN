---
name: context-kit
description: "评估、改造并安全安装 Context Kit 的个人上下文工件，以用于 Claude Code 或相邻的智能体工作流。评估Context Kit、安全安装个人上下文、改造上下文模板、本地CRM规划、个人记忆系统"
category: productivity
risk: critical
source: community
source_repo: JDDavenport/context-kit
source_type: community
date_added: "2026-07-04"
author: JDDavenport
tags: [personal-context, claude-code, memory, knowledge-management, agent-workflows]
tools: [claude, codex, cursor, gemini]
---

# Context Kit（上下文工具包）

## 何时使用

当用户希望执行以下操作时，请使用本技能：

- 为 Claude Code 或其他编码智能体搭建持久的个人上下文文件
- 将 Context Kit 的“个人上下文工件（Personal Context Artifact）”模式与现有的记忆或项目笔记系统进行对比
- 改造上下文模板的结构，但不将私密细节粘贴到聊天中
- 在运行一键安装程序或下载的技能包之前，先审查其是否合适
- 为 CRM 笔记、悬而未决的事项、会话摘要或晨间简报制定更安全的、本地优先的方案

## 概览

Context Kit 是一个外部项目，它将个人上下文组织为 Markdown 工件以及配套的 Claude Code 技能。本技能帮助用户决定要采纳哪些内容、存放在何处，以及如何避免让一个有用的上下文系统变成一堆敏感数据。

默认将每一份个人上下文文件视为私密的。这些文件可能包含身份细节、家庭情况、工作履历、联系人笔记、心智模型、健康限制或人际关系信息。未经用户明确批准其所包含的精确子集，请勿将其粘贴到第三方工具、公开仓库、问题跟踪器或模型上下文中。

## 安全规则

1. 在用户看到具体命令、源仓库以及脚本将要写入的目标路径之前，不要运行远程安装脚本。
2. 在执行任何安装程序之前，优先克隆或下载仓库以供审查：
   ```bash
   git clone https://github.com/JDDavenport/context-kit.git
   cd context-kit
   sed -n '1,220p' scripts/install.sh
   ```
3. 切勿在个人上下文工件中存储密码、API 密钥、恢复码、私钥、会话令牌或支付信息。
4. 如果用户希望保存联系人笔记或 CRM 文件，请仅存储他们愿意以本地明文 Markdown 形式保存的信息。
5. 在将这些文件加入仓库之前，请确认 `.gitignore` 已排除所选的私有上下文目录。
6. 如果要将 Context Kit 改造用于团队或公司场景，请将个人上下文与公司机密或客户机密信息分离开来。

## 设置流程

1. 询问用户希望 Context Kit 改善什么：会话启动上下文、语气一致性、人际关系记忆、悬而未决的事项跟踪、每日简报，还是交接摘要。
2. 在运行任何操作之前，先检查上游项目和安装程序。
3. 选择存储位置：
   - Claude Code 默认：`~/.claude/context/` 和 `~/.claude/skills/`
   - 项目本地上下文：`.agent/context/` 或其他被忽略的目录
   - 便携式设置：带有明确同步规则的私有笔记仓库
4. 在填充全部内容之前，先创建一份最小的启动集合：
   - `pca-wiki.md`：用于持久身份与领域信息
   - `pca-mental-models.md`：用于决策规则
   - `pca-voice.md`：用于写作偏好
   - `pca-protocols.md`：用于硬性规则与边界
5. 仅添加足以让下一次智能体会话有用的细节。在有明确理由之前，请略去敏感的、推测性的或已过时的内容。
6. 建立定期审查的节奏。个人上下文很容易过时；在驱动决策时，过时的上下文比没有上下文更糟糕。

## 安装审查清单

在运行安装程序之前，请核实：

- 仓库 URL 与用户所指定的完全一致
- 脚本仅向预期的本地目录写入内容
- 脚本不会上传文件、发送遥测数据，或意外修改 shell 启动文件
- 目标目录不在公开仓库内
- 用户拥有回滚路径，例如能够删除已复制的模板和技能

如果有任何不清楚之处，请在审查阶段停下来，并向用户提供需要复核的确切行内容。

## 示例

### 示例：在安装之前先审查

```bash
git clone https://github.com/JDDavenport/context-kit.git
cd context-kit
sed -n '1,220p' scripts/install.sh
find templates skills -maxdepth 2 -type f | sort
```

审查完成后，汇总将要安装的文件，并在运行安装程序之前请求用户确认。

### 示例：创建私有的项目本地上下文目录

```bash
mkdir -p .agent/context
printf '.agent/context/\n' >> .gitignore
cp ~/Downloads/context-kit/templates/pca-wiki.md .agent/context/pca-wiki.md
```

然后，针对项目将模板裁剪到最小可用字段，而不是立即填满每一项个人内容。

## 最佳实践

- 保持上下文文件简短，以便智能体在会话开始时就能读取，而不会被过时的细节淹没。
- 将持久事实与临时状态分开。临时状态请使用项目工作计划或任务跟踪器。
- 标注假设和不确定的记忆，而不是将其当作事实呈现。
- 在重大的人生、角色、健康或项目变化之后，重新审视个人上下文。
- 尽可能将语气示例与反例与私人身份细节分开存储。

## 常见陷阱

- 在未先审查的情况下，直接通过 `curl` 运行 shell 安装程序
- 将个人上下文文件提交到公开仓库
- 以“智能体需要知道一切”为借口存储秘密信息
- 让人际关系或健康相关笔记过时，却仍将其当作现行信息使用
- 复制上游付费或许可证不清晰的内容，而不是链接到原文或撰写原创的本地笔记

## 局限性

- 本技能本身无法验证当前的上游许可证或安装程序行为；请在运行命令之前检查实时仓库。
- 它不能替代专用的密钥管理器、CRM、密码保险库或医疗记录系统。
- 它用于本地个人上下文的整理，而不是用于在没有正当理由的情况下收集他人的私人信息。