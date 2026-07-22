---
name: skill-suggester
version: 1.0.0
description: "扫描提示词历史中的重复模式与未满足需求，然后提议新技能或命令模板"
risk: safe
source: community
source_type: community
source_repo: mskadu/opencode-agent-skills
license: MIT
license_source: "https://github.com/mskadu/opencode-agent-skills/blob/main/LICENSE"
date_added: "2026-06-05"
---

## skill-suggester

读取你的 opencode 提示词历史，发现重复的多步工作流，并推荐值得封装为技能的候选项。让你不必再重复同一段对话。

## 何时使用

当用户想从 opencode 提示词历史中挖掘重复工作流、反复出现的未满足需求，或寻找可复用的新技能候选时，使用此技能。

## 如何调用

运行 `/skill skill-suggester` 扫描完整历史。可选传入 `--since <日期>`（例如 `--since 2026-05-01`）限定时间窗口。

## 分析方法

1. 定位提示词历史文件 `~/.local/state/opencode/prompt-history*.jsonl`
2. 解析每条记录的消息内容
3. 从以下维度评分，判断技能潜力：
   - **重复性**：类似措辞或主题出现 3 次以上（"扫描所有仓库"、"检查收件箱"）
   - **多步序列**：完成一次请求需要 5 次以上工具调用
   - **未支持请求**：你曾请求过但没有专属技能的事情
   - **变通模式**：每次都要手动给出的指令，而非一条命令搞定
4. 对每个候选项记录：
   - 该模式出现的次数
   - 消耗的工具调用数
   - 如果封装为技能，预计节省的时间

## 输出格式

```
## Skill Candidates (last N entries)

### 1. "<candidate name>" (PRIORITY)
- **Pattern**: <what you keep asking for>
- **Frequency**: X times in history
- **Avg complexity**: Y tool calls per instance
- **Estimated savings**: ~Z minutes/week
- **Evidence**:
  - "[excerpt from prompt history]"
  - "[another excerpt]"
- **Recommendation**: <create as skill | add as command template | not worth it>

### 2. ...
```

## 关键规则

- 只标记出现两次以上的模式。一次性的不算技能。
- 包含你过去提示词的直接引用作为证据。
- 为每个候选评级：`high`（明显有回报，每周使用）、`medium`（有了更好）、`low`（少见但值得记录）。
- 如果没有符合条件的，如实说明原因。
- 展示候选后，询问你是否要创建其中任何一个。

## 局限性

- 提示词历史可能包含敏感的本地上下文；总结模式时不要暴露不必要的隐私摘录。
- 建议仅供参考，创建或发布新技能前仍需人工审核。
