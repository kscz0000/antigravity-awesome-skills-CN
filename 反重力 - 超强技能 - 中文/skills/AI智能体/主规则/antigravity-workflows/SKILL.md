---
name: antigravity-workflows
description: "通过引导式工作流编排多个 Antigravity 技能，用于 SaaS MVP 交付、安全审计、AI 智能体构建和浏览器 QA。触发词：antigravity工作流、技能编排、SaaS MVP交付、安全审计工作流、AI智能体构建、浏览器自动化QA、DDD领域设计、多技能编排"
risk: none
source: self
date_added: "2026-02-27"
---

# Antigravity Workflows

使用此技能将复杂目标转化为引导式的技能调用序列。

## 何时使用此技能

在以下情况下使用此技能：
- 用户希望组合多个技能，而无需手动选择每一个。
- 目标是多阶段的（例如：规划、构建、测试、发布）。
- 用户请求常见场景的最佳实践执行，例如：
  - 发布 SaaS MVP
  - 运行 Web 安全审计
  - 构建 AI 智能体系统
  - 实现浏览器自动化和 E2E QA

## 工作流真实来源

按以下顺序读取工作流：
1. `docs/WORKFLOWS.md` 用于人类可读的操作手册。
2. `data/workflows.json` 用于机器可读的工作流元数据。

## 如何运行此技能

1. 识别用户的具体目标。
2. 提出 1-2 个最匹配的工作流。
3. 请用户选择一个。
4. 逐步执行：
   - 宣布当前步骤和预期产物。
   - 调用该步骤推荐的技能。
   - 在进入下一步之前验证完成标准。
5. 最后提供：
   - 完成的产物
   - 验证证据
   - 剩余风险和后续行动

## 默认工作流路由

- 产品交付请求 -> `ship-saas-mvp`
- 安全审查请求 -> `security-audit-web-app`
- 智能体/LLM 产品请求 -> `build-ai-agent-system`
- E2E/浏览器测试请求 -> `qa-browser-automation`
- 领域驱动设计请求 -> `design-ddd-core-domain`

## 复制粘贴提示词

```text
使用 @antigravity-workflows 为我的项目创意运行"发布 SaaS MVP"工作流。
```

```text
使用 @antigravity-workflows 执行完整的"Web 应用安全审计"工作流。
```

```text
使用 @antigravity-workflows 通过检查点引导我完成"构建 AI 智能体系统"。
```

```text
使用 @antigravity-workflows 执行"QA 和浏览器自动化"工作流并稳定不稳定测试。
```

```text
使用 @antigravity-workflows 为我的新服务执行"设计 DDD 核心领域"工作流。
```

## 限制

- 此技能负责编排；它不替代专业技能。
- 它依赖于被引用技能的本地可用性。
- 如果没有环境访问权限、凭证或所需基础设施，它无法保证成功。
- 对于 Go 中的特定技术栈浏览器自动化，`go-playwright` 可能需要相应的技能存在于您的本地技能库中。

## 相关技能

- `concise-planning`
- `brainstorming`
- `workflow-automation`
- `verification-before-completion`
