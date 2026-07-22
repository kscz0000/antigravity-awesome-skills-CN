---
name: git-pushing
description: "暂存所有更改，创建规范化提交，并推送到远程分支。触发词：push this、commit and push、save to github、push to remote、推送、提交并推送、保存到远程、推送到远程、完成功能后分享。"
risk: critical
source: community
date_added: "2026-02-27"
---

# Git 推送工作流

暂存所有更改，创建规范化提交，并推送到远程分支。

## 使用时机

当用户满足以下条件时自动激活：

- 明确请求推送更改（"push this"、"commit and push"）
- 提及将工作保存到远程（"save to github"、"push to remote"）
- 完成功能并希望分享
- 说出类似 "let's push this up" 或 "commit these changes" 的短语

## 工作流程

**始终使用脚本** - 不要使用手动 git 命令：

```bash
bash skills/git-pushing/scripts/smart_commit.sh
```

使用自定义消息：

```bash
bash skills/git-pushing/scripts/smart_commit.sh "feat: add feature"
```

脚本处理：暂存、规范化提交消息、Claude 页脚、带 -u 标志推送。

## 限制

- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
