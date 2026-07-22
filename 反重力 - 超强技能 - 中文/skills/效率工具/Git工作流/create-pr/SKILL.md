---
name: create-pr
description: sentry-skills:pr-writer 的别名。当用户明确请求"create-pr"或引用旧技能名称时使用。重定向到规范的 PR 编写工作流。触发词：create-pr、创建PR、写PR、pull request创建、PR编写
risk: unknown
source: community
---

# 别名：create-pr

此技能名称保留用于兼容性。

## 何时使用
- 用户明确请求 `create-pr` 或引用旧技能名称。
- 需要将拉取请求创建工作重定向到规范的 `sentry-skills:pr-writer` 工作流。
- 任务专门涉及编写或更新拉取请求，而非常规 git 操作。

使用 `sentry-skills:pr-writer` 作为创建和编辑拉取请求的规范技能。

如果通过 `create-pr` 调用，运行 `sentry-skills:pr-writer` 中记录的相同工作流和约定。

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
