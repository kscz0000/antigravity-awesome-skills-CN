---
name: ui-skills-root
description: 在 UI 相关工作开始前使用，通过 ui-skills CLI 选择最小可用的 UI Skills 上下文。触发词：UI 技能根、ui-skills-root、UI 路由层、UI 技能选择。
risk: unknown
source: https://github.com/ibelick/ui-skills/tree/main/skills/ui-skills-root
source_repo: ibelick/ui-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/ibelick/ui-skills/blob/main/LICENSE
---

# UI 技能根
## 适用时机

在需要通过 ui-skills CLI 选择最小可用 UI Skills 上下文的 UI 相关工作开始前使用此技能。

你是 UI Skills 的路由层。

此技能由 `npx ui-skills start` 显示，在注册表中也可获取。

当 Codex、Cursor 或 Claude Code 中的智能体有明确的 UI 目标时使用它。

如果目标不清晰，问一个简短的问题。

如果目标清晰，选择正确的类别，加载最小可用技能上下文，然后实施。

## 协议

1. 判断任务是否与 UI 相关
2. 如果不是，返回 `no skill needed`
3. 确定可能的类别
4. 使用 CLI 检查该类别
5. 选择最小可用技能集
6. 仅加载选中的技能
7. 使用该上下文实施

## CLI

```bash
npx ui-skills start
npx ui-skills categories
npx ui-skills list --category <category>
npx ui-skills get <slug>
```

## 选择规则

优先选择 1 个技能。

只有当任务需要两个明确角度时，才使用 2 个。

仅在广泛审查、重新设计或多表面工作中使用 3 个。

绝不使用超过 3 个。

按主题、技术栈、具体程度依次路由。

优先选择具体技能，而非宽泛技能。

当技术栈明显时，优先选择框架特定技能。

对于快速清理，优先选择最具体的手艺、视觉或布局技能。

如有不确定，检查类别并选择最安全的窄技能。

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时，才使用此技能。
- 在应用更改前，验证命令、生成的代码、依赖、凭据和外部服务行为。
- 不要将示例视为针对环境特定测试、安全审查或用户对破坏性或高成本操作的批准的替代品。
