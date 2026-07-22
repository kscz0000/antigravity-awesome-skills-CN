---
name: web-design-guidelines
description: "审查文件是否符合 Web 界面指南。触发词：Web 界面指南、UI 审查、可访问性审计、设计审查、checklist、web guidelines、UI 设计、界面设计、最佳实践、设计系统"
risk: safe
source: community
date_added: "2026-02-27"
---

# Web 界面指南

审查文件是否符合 Web 界面指南。

## 工作原理

1. 从下方源 URL 获取最新指南
2. 读取指定的文件（或提示用户提供文件/模式）
3. 对照获取指南中的所有规则进行检查
4. 以简洁的 `file:line` 格式输出发现的问题

## 指南来源

每次审查前获取最新指南：

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

使用 WebFetch 检索最新规则。获取的内容包含所有规则和输出格式说明。

## 使用方法

当用户提供文件或模式参数时：
1. 从上方源 URL 获取指南
2. 读取指定的文件
3. 应用获取指南中的所有规则
4. 使用指南中指定的格式输出发现的问题

如果未指定文件，询问用户要审查哪些文件。

## 使用时机
本技能适用于执行上述概述中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
