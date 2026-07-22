---
name: data-quality-frameworks
description: "使用 Great Expectations、dbt 测试和数据契约实现数据质量验证。适用于构建数据质量管道、实现验证规则或建立数据契约。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Data Quality Frameworks

使用 Great Expectations、dbt 测试和数据契约实现数据质量的生产级模式，确保数据管道可靠。

## Use this skill when

- Implementing data quality checks in pipelines
- Setting up Great Expectations validation
- Building comprehensive dbt test suites
- Establishing data contracts between teams
- Monitoring data quality metrics
- Automating data validation in CI/CD

## Do not use this skill when

- The data sources are undefined or unavailable
- You cannot modify validation rules or schemas
- The task is unrelated to data quality or contracts

## Instructions

- 识别关键数据集和质量维度
- 定义期望/测试和契约规则
- 在 CI/CD 中自动化验证并安排定期检查
- 设置告警、责任归属和修复步骤
- 如需详细模式，打开 `resources/implementation-playbook.md`

## Safety

- 避免在没有回退方案的情况下阻塞关键管道
- 在验证输出中安全处理敏感数据

## Resources

- `resources/implementation-playbook.md` 包含详细的框架、模板和示例

## Limitations
- 仅当任务明确符合上述范围时使用此技能
- 不要将输出替代特定环境的验证、测试或专家审查
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清
