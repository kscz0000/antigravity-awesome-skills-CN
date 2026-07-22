---
name: airflow-dag-patterns
description: "构建生产级 Apache Airflow DAG，涵盖 operators、sensors、测试和部署最佳实践。触发词：Airflow DAG、数据管道编排、工作流编排、批处理调度、DAG设计、Airflow operators、Airflow sensors、DAG测试、Airflow生产部署、DAG调试"
risk: safe
source: community
date_added: "2026-02-27"
---

# Apache Airflow DAG 模式

Apache Airflow 生产级模式，涵盖 DAG 设计、operators、sensors、测试和部署策略。

## 使用此技能的场景

- 使用 Airflow 创建数据管道编排
- 设计 DAG 结构和依赖关系
- 实现自定义 operators 和 sensors
- 在本地测试 Airflow DAG
- 在生产环境中部署 Airflow
- 调试失败的 DAG 运行

## 不使用此技能的场景

- 只需要简单的 cron 作业或 shell 脚本
- Airflow 不在技术栈中
- 任务与工作流编排无关

## 指导说明

1. 识别数据源、调度计划和依赖关系。
2. 设计具有明确所有权和重试机制的幂等任务。
3. 实现 DAG，包含可观测性和告警钩子。
4. 在预发布环境中验证，并编写运维手册。

详细模式、检查清单和模板请参考 `resources/implementation-playbook.md`。

## 安全注意事项

- 未经批准，避免更改生产 DAG 的调度计划。
- 仔细测试回填和重试操作，防止数据重复。

## 资源

- `resources/implementation-playbook.md` 包含详细模式、检查清单和模板。

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代针对特定环境的验证、测试或专家评审。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
