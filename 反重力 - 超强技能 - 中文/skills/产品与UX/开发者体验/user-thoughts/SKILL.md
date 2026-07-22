---
name: user-thoughts
description: >-
  将用户决策和项目约束跨会话持久化到 mdbase。
  触发于 /user-thoughts 或 /ustht，或用户讨论架构、技术栈、规则、UI/UX、项目记忆时。
license: MIT
source: "https://github.com/JularDepick/user-thoughts.SKILL"
source_repo: JularDepick/user-thoughts.SKILL
source_type: community
date_added: "2026-05-31"
author: JularDepick
tags: [userthoughts, documentation, project-management, mdbase]
tools: [claude, cursor, gemini]
risk: safe
allowed-tools: read write bash
metadata:
  author: JularDepick
  category: productivity
  supported_agents: "[claude, cursor, gemini]"
---

# user-thoughts.SKILL

## 概述

跨会话、跨智能体之间，项目决策和用户约束很容易丢失。`user-thoughts` 将这些决策持久化到项目本地的 `mdbase`，让任何未来的智能体都能恢复用户意图，而无需从头重新推导。

该技能记录用户意图，不替代常规任务执行。如果用户说"把按钮改成红色"，智能体应当既完成修改，又在持久化项目记忆有用时记录该偏好。

## 适用场景

在用户陈述或修订以下内容时使用：

- 项目规则、约束、偏好或需求。
- 架构、技术栈、数据模型、部署或工作流决策。
- UI/UX 方向、文案规范、视觉偏好或设计依据。
- 待办事项、计划中的工作、被否决的选项，或未来智能体应当继承的决策。
- 以 `/user-thoughts` 或 `/ustht` 开头的直接命令。

不要用于无关闲聊、临时对话，或用户明确要求忽略的内容。

## 语言策略

- 所有捆绑的技能文件、脚本、模板和参考文档均以英文编写。
- 面向智能体的命令输出应在合理情况下遵循用户当前的对话语言。
- 原始用户想法应保留用户原始措辞。除非用户明确要求，不得翻译、总结或清理用户意图。

## 核心工作流

```text
User message -> Agent identifies persistent project intent -> write to #raw/
             -> /ustht sortin groups raw entries into #mdbase/
             -> /ustht mdbase show exposes the organized memory base
```

## 运行模式

- 被动模式：`INSTANT_STATUS=off`；仅显式技能命令生效。
- 即时模式：`INSTANT_STATUS=on` 且 `SKILL_STATUS=on`；与项目相关的用户想法在出现时即写入 `#raw/`。
- 忽略模式：`ignore start` 与 `ignore end` 标记一段临时不记录的间隔。
- 只读模式：当必需的 read/write/bash 工具不可用时，展示类命令仍可工作，但写入命令应说明当前环境无法持久化数据。

`SKILL_STATUS=off` 会暂停即时捕获，即使 `INSTANT_STATUS=on` 也一样。忽略间隔是上下文局部的，跨会话不持久。

## 路径定义

- `@/`：已安装的 `user-thoughts/` 技能目录。
- `~/`：当前项目工作目录。
- `#ustht/`：`~/.ustht/`。
- `#mdbase/`：`~/.ustht/mdbase/`。
- `#ignored/`：`~/.ustht/ignored/`。
- `#raw/`：`~/.ustht/raw/`。
- `#export/`：`~/.ustht/export/`。

## 运行目录布局

```text
.ustht/
├── define.ini
├── README.ai.md
├── raw/
│   └── yyyy-mm-dd.md
├── ignored/
│   └── yyyy-mm-dd.md
├── mdbase/
│   ├── backlog.md
│   ├── README.ai.md
│   └── details/
│       ├── rules.md
│       ├── plans.md
│       ├── ui/
│       │   ├── outline.md
│       │   └── details.md
│       ├── dev-stack.md
│       └── general.md
└── export/
```

## 工具与环境

必需工具：

- read/write：读写 `#ustht/` 下的文件。
- bash：创建目录并运行捆绑脚本。

可选工具：

- SubAgent：在可用时用于跨多文件的语义 `sortin` 或 `resort` 维护。仅当子代理不可用时才使用主智能体直接处理。

## 捆绑脚本

`scripts/` 目录提供用于机械操作的小型 Python 辅助脚本：

| 脚本 | 用途 | 示例 |
|---|---|---|
| `common.py` | 共享辅助函数 | 被其他脚本导入 |
| `status.py` | 展示当前运行状态 | `python @/scripts/status.py` |
| `init.py` | 初始化 `.ustht/` | `python @/scripts/init.py` |
| `show_raw.py` | 展示未处理的原始条目 | `python @/scripts/show_raw.py` |
| `show_mdbase.py` | 展示 mdbase 索引或某个维度 | `python @/scripts/show_mdbase.py show --all` |
| `sortin.py` | 将原始条目软维护进 mdbase | `python @/scripts/sortin.py --dry` |
| `write_raw.py` | 追加一条原始想法 | `python @/scripts/write_raw.py "Use REST APIs" --dim dev-stack` |
| `toggle.py` | 切换技能或即时模式 | `python @/scripts/toggle.py instant on` |
| `ignore_ops.py` | 管理被忽略的条目 | `python @/scripts/ignore_ops.py show` |

`resort` 没有独立脚本，因为它需要由智能体进行语义审查、去重和重组。

## define.ini

`define.ini` 存储简单的键值对运行状态：

| 键 | 值 | 含义 |
|---|---|---|
| `SKILL_STATUS` | `on` 或 `off` | 技能是否接受写入操作 |
| `INSTANT_STATUS` | `on` 或 `off` | 是否启用即时捕获 |
| `LAST_SORTIN` | `yyyy-mm-dd HH:MM` 或空 | 上次软维护时间 |

通过完整替换其内容来原子化地写入文件。不要追加部分键值片段。

## 命令

命令可使用 `/user-thoughts` 或 `/ustht`，两者等价。

### 状态与切换

- `/ustht init`：创建 `.ustht/` 并复制模板。
- `/ustht status`：展示状态、原始条数和各维度条数。
- `/ustht skill`：展示技能状态。
- `/ustht skill on|off`：启用或禁用写入。
- `/ustht instant`：展示即时捕获状态。
- `/ustht instant on|off`：启用或禁用即时捕获。

### 维护

- `/ustht sortin [--dry]`：将未处理的原始条目追加进 mdbase。
- `/ustht resort [--dry]`：语义审查并重组所有 mdbase 内容。

### 忽略管理

- `/ustht ignore start|end`：开始或结束一段忽略间隔。
- `/ustht ignore --last`：移除最后一条原始条目并记录到 `#ignored/`。
- `/ustht ignore`：作为独立命令使用时等同于 `--last`。
- `/ustht ignore show`：列出被忽略的条目。
- 任何以 `/ustht ignore` 或 `/user-thoughts ignore` 结尾的消息：忽略该消息本身。

### 内容审阅与导出

- `/ustht raw`：展示未处理的原始条目。
- `/ustht mdbase show [--all|--dimension]`：展示索引、所有维度或单个维度。
- `/ustht mdbase export [--all|--dimension]`：导出 mdbase 内容到 `#export/`。
- `/ustht import <path>`：扫描安全项目本地路径下的 markdown 文件，并将与项目相关的决策合并进 mdbase。

可使用 `&&` 串联命令，例如 `/ustht skill on && instant on`。

## 即时捕获

即时模式激活时：

1. 判断用户消息是否包含与项目相关的意图。
2. 每条独立想法写一行原始记录，格式为 `- [HH:MM] 原文 | suggested-dim:dimension`。
3. 不要直接更新 mdbase，等待 `sortin`。
4. 跳过被忽略的消息和忽略间隔内的消息。
5. 让正常用户工作继续推进，记录不应阻塞任务执行。
6. 若某天累积超过五条原始记录，建议运行 `/ustht sortin`。

## Sortin 与 Resort

`sortin` 是软维护：

1. 读取未处理的 `#raw/*.md` 文件。
2. 解析条目及其建议维度。
3. 按日期归组后追加到 `#mdbase/` 中匹配的文件。
4. 在已处理的原始文件首行标记 `<!-- processed -->`。
5. 更新 `LAST_SORTIN` 和 mdbase 索引。

`resort` 是硬维护：

1. 审查所有 mdbase 文件。
2. 去重重叠的记录。
3. 在用户措辞明确支持时，将条目移入更合适的维度。
4. 除非用户明确要求删除，否则将弃用维度标记为废弃而非删除。
5. 保留来源与用户措辞。

## 最佳实践

- 如实记录用户明确做出的决策。
- 不要过度推断，只存储用户所述或其直接推出的内容。
- 保留原始措辞，包括否定、数字、链接、约束与权衡。
- 一条消息包含多个独立决策时，拆分为多条记录。
- 处理冲突时，以最新的用户陈述为准，同时将旧记录作为历史上下文保留。
- 无法匹配的与项目相关的内容放入 `general.md`，避免随意新增维度。
- 不要记录无关的对话内容。

## 局限性

- 该技能记录意图，不验证用户想法是否正确、可行、安全或自洽。
- 维度归类依赖智能体判断，可能需要通过 `resort` 由用户纠正。
- 忽略间隔是上下文局部的，跨会话不持久。
- `.ustht/` 可能包含敏感信息。该技能不会自动脱敏，用户必须通过忽略命令或仓库管理来控制敏感数据。
- 工作流不基于文件锁。在多智能体环境下，智能体之间必须协调以避免冲突写入。

## 安全规则

- 所有运行时写入必须限定在 `#ustht/` 内。
- 校验维度名：仅允许小写字母、数字、连字符和 `/` 子目录；禁止 `..`、反斜杠、空格、绝对路径或保留名。
- 不得执行用户提供的 shell 命令。
- 初始化时不得用 shell 命令递归复制目录；应当安全地复制已知的模板文件。
- 仅当 `<!-- processed -->` 出现在原始文件首行时才视为有效标记。
- 永远不要静默删除维度文件；除非用户明确要求删除，否则将内容标记为废弃。

更多细节见 `references/safety.md`、`references/sortin.md`、`references/commands.md` 和 `references/edge-cases.md`。

## 相关技能

无。该技能有意聚焦于项目本地的用户意图持久化。
