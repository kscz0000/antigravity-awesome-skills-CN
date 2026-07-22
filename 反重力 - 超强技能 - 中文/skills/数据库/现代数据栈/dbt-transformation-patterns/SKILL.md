---
name: dbt-transformation-patterns
description: "dbt (data build tool) 的生产级模式，包括模型组织、测试策略、文档和增量处理。"
risk: none
source: community
date_added: "2026-02-27"
---

# dbt Transformation Patterns

dbt (data build tool) 的生产级模式，包括模型组织、测试策略、文档和增量处理。

## 使用此技能的场景

- 使用 dbt 构建数据转换管道
- 将模型组织为 staging、intermediate 和 marts 层
- 实施数据质量测试和文档
- 为大数据集创建增量模型
- 设置 dbt 项目结构和约定

## 不使用此技能的场景

- 项目未使用 dbt 或仓库支持的工作流
- 仅需要临时 SQL 查询
- 无法访问源数据或 schema

## 指令

- 定义模型层、命名和所有权。
- 实施测试、文档和新鲜度检查。
- 选择物化方式和增量策略。
- 使用选择器和 CI 工作流优化运行。
- 如需详细模式，打开 `resources/implementation-playbook.md`。

## 资源

- `resources/implementation-playbook.md` 提供详细的 dbt 模式和示例。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
