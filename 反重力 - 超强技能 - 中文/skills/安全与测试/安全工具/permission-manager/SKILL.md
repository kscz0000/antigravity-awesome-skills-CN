---
name: permission-manager
version: 1.0.0
description: "管理 opencode 权限：审查始终允许列表、建议安全的只读命令、配置权限模式"
risk: critical
source: community
source_type: community
source_repo: mskadu/opencode-agent-skills
license: MIT
license_source: "https://github.com/mskadu/opencode-agent-skills/blob/main/LICENSE"
date_added: "2026-06-05"
---

## 我做什么
- 审查并总结当前始终允许的命令
- 建议可自动批准的安全只读命令
- 在 opencode.json 中添加或移除允许列表中的命令
- 配置技能级权限（allow/deny/ask），支持通配符模式
- 审计权限配置的安全性和可用性

## 何时使用
在优化 opencode 的权限设置、审查允许的命令或配置技能访问控制时使用。

## 工作流步骤

1. **读取当前配置**：加载 `~/.config/opencode/opencode.json` 或项目级 `opencode.json`
2. **总结权限**：识别当前允许的命令和技能权限
3. **建议新增项**：推荐可自动允许的安全只读命令（参见下方推荐列表）
4. **应用变更**：编辑配置以添加/移除权限条目
5. **验证**：确保变更后 JSON 有效

通过审计当前配置并在对话中推荐调整，补充 opencode 内置的 allow/deny/ask 权限机制。

## 核心规则
- 绝不允许修改文件、提交、推送或更改系统状态的命令
- 优先使用精确的命令条目，如 `git status --short`、`git diff --stat` 和 `ls -la`
- 避免尾部通配符如 `git status*`，除非该扩展命令族已通过人工审查确认为只读
- 修改权限配置前需与用户确认
- 区分 bash 命令权限和技能权限
- 保持配置整洁：将相关命令分组排列

## 局限性

- 本技能仅限于 opencode 权限配置，不应修改其他 agent host 的权限存储。
- 将所有具备写入能力的命令权限视为高风险；即使模式看起来范围狭窄，也应人工审查。

## 如何触发我

使用 Task 工具，指定 `permission-manager` 子代理类型：

```
/permissions
```

或用自然语言要求 opencode "管理 opencode 权限"或"审查允许的命令"。
