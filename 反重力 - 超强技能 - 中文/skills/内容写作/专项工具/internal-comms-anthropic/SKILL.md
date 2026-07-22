---
name: internal-comms-anthropic
description: "撰写内部沟通文档时使用此技能，涵盖3P更新、公司简报、FAQ回复、状态报告、领导层更新、项目更新和事件报告。触发词：内部沟通、3P更新、公司简报、FAQ回复、状态报告、领导层更新、项目更新、事件报告、internal comms"
risk: unknown
source: community
date_added: "2026-02-27"
---

## 何时使用此技能
撰写内部沟通文档时，使用此技能处理：
- 3P 更新（Progress 进展、Plans 计划、Problems 问题）
- 公司简报
- FAQ 回复
- 状态报告
- 领导层更新
- 项目更新
- 事件报告

## 如何使用此技能

撰写任何内部沟通文档时：

1. **识别沟通类型**，根据用户请求判断
2. **加载对应的指南文件**，从 `examples/` 目录中选取：
    - `examples/3p-updates.md` - 用于 Progress/Plans/Problems 团队更新
    - `examples/company-newsletter.md` - 用于全公司简报
    - `examples/faq-answers.md` - 用于回答常见问题
    - `examples/general-comms.md` - 用于以上类别均不匹配的其他场景
3. **遵循该文件中的具体指引**，包括格式、语气和内容收集方式

如果沟通类型无法匹配任何现有指南，请请求澄清或获取更多关于期望格式的上下文。

## 关键词
3P updates, company newsletter, company comms, weekly update, faqs, common questions, updates, internal comms

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代针对具体环境的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
