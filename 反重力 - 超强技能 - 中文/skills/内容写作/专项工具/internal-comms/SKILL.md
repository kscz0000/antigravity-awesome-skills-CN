---
name: internal-comms
description: "使用可复用的内部格式撰写内部沟通文档，如状态报告、管理层动态、3P更新、新闻简报、FAQ、事件报告和项目进展。触发词：内部沟通、状态报告、3P更新、公司简报、FAQ回复、事件报告、项目更新"
risk: unknown
source: "https://github.com/anthropics/skills"
date_added: "2026-03-21"
license: Complete terms in LICENSE.txt
---

## 何时使用此技能

撰写内部沟通文档时，此技能适用于：
- 3P 更新（Progress 进展、Plans 计划、Problems 问题）
- 公司新闻简报
- FAQ 回复
- 状态报告
- 管理层动态
- 项目进展
- 事件报告

## 如何使用此技能

撰写任何内部沟通文档时：

1. **识别沟通类型**，根据请求判断
2. **加载对应的指南文件**，从 `examples/` 目录中选取：
    - `examples/3p-updates.md` - 用于 Progress/Plans/Problems 团队更新
    - `examples/company-newsletter.md` - 用于公司全员简报
    - `examples/faq-answers.md` - 用于回答常见问题
    - `examples/general-comms.md` - 用于以上类型均不匹配的其他情况
3. **遵循文件中的具体指引**，包括格式、语气和内容收集方式

如果沟通类型不匹配任何现有指南，请请求澄清或获取更多关于期望格式的上下文。

## 关键词
3P updates, company newsletter, company comms, weekly update, faqs, common questions, updates, internal comms

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出不可替代针对具体环境的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
