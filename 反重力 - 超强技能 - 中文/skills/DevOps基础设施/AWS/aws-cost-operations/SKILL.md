---
name: aws-cost-operations
description: AWS 成本优化、监控和卓越运营专家。用于分析 AWS 账单、估算成本、设置 CloudWatch 告警、查询日志、审计 CloudTrail 活动或评估安全态势。当用户提及 AWS 成本、支出、计费时必不可少。触发词：AWS 成本优化、AWS 计费分析、CloudWatch 告警、CloudTrail 审计、安全态势评估、成本估算。
risk: unknown
source: https://github.com/zxkane/aws-skills/tree/main/plugins/aws-cost-ops/skills/aws-cost-operations
source_repo: zxkane/aws-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/zxkane/aws-skills/blob/main/LICENSE
---

# AWS 成本与运营

本技能通过集成 MCP 服务器，为 AWS 成本优化、监控、可观测性和卓越运营提供全面的指导。

## AWS 文档要求

回答前务必使用 MCP 工具（`mcp__aws-mcp__*` 或 `mcp__*awsdocs*__*`）验证 AWS 事实。`aws-mcp-setup` 依赖项会自动加载——如果 MCP 工具不可用，请引导用户完成该技能的设置流程。

## 集成的 MCP 服务器

本插件提供 3 个 MCP 服务器：

### 内置服务器

#### 1. AWS Pricing MCP 服务器（`pricing`）
**用途**：部署前的成本估算和优化
- 在部署资源前估算成本
- 比较不同区域的定价
- 计算总体拥有成本（TCO）
- 评估不同服务选项的成本效益

#### 2. AWS Cost Explorer MCP 服务器（`costexp`）
**用途**：详细的成本分析和报告
- 分析历史支出模式
- 识别成本异常和趋势
- 预测未来成本
- 按服务、区域或标签分析成本

#### 3. Amazon CloudWatch MCP 服务器（`cw`）
**用途**：指标、告警和日志分析
- 查询 CloudWatch 指标和日志
- 创建和管理 CloudWatch 告警
- 排查运营问题
- 监控资源利用率

> **注意**：以下服务器通过完整 AWS MCP 服务器单独提供（参见 `aws-mcp-setup` 技能），不包含在本插件中：
> - AWS 计费和成本管理 MCP——实时计费详情
> - CloudWatch Application Signals MCP——APM 和 SLO
> - AWS Managed Prometheus MCP——容器的 PromQL 查询
> - AWS CloudTrail MCP——API 活动审计
> - AWS Well-Architected 安全评估 MCP——安全态势评估

## 何时使用本技能

在以下场景使用本技能：
- 优化 AWS 成本并减少支出
- 在部署前估算成本
- 监控应用程序和基础设施性能
- 设置可观测性和告警
- 分析支出模式和趋势
- 调查运营问题
- 审计 AWS 活动和变更
- 评估安全态势
- 实施卓越运营

## 成本优化最佳实践

### 部署前的成本估算

**始终在部署前估算成本**：
1. 使用 **AWS Pricing MCP** 估算资源成本
2. 比较不同区域的定价
3. 评估替代服务选项
4. 计算预期月度成本
5. 为扩展和增长做规划

**工作流示例**：
```
"估算在 us-east-1 区域运行一个 Lambda 函数（100 万次调用、512MB 内存、3 秒执行时长）的月度成本"
```

### 成本分析与优化

**定期成本审查**：
1. 使用 **Cost Explorer MCP** 分析支出趋势
2. 识别成本异常和意外费用
3. 按服务、区域和环境审查成本
4. 比较实际成本与预算成本
5. 生成成本优化建议

**成本优化策略**：
- 调整过度配置资源的规模
- 使用合适的存储类（S3、EBS）
- 为动态工作负载实施自动伸缩
- 利用 Savings Plans 和 Reserved Instances
- 删除未使用的资源和快照
- 有效使用成本分配标签

### 预算监控

**对照预算跟踪支出**：
1. 使用 **Billing and Cost Management MCP** 监控预算
2. 为阈值突破设置预算告警
3. 定期审查预算利用率
4. 根据趋势调整预算
5. 实施成本控制和治理

## 监控与可观测性最佳实践

### CloudWatch 指标与告警

**实施全面监控**：
1. 使用 **CloudWatch MCP** 查询指标和日志
2. 为关键指标设置告警：
   - CPU 和内存利用率
   - 错误率和延迟
   - 队列深度和处理时间
   - API 网关限流
   - Lambda 错误和超时
3. 创建 CloudWatch 仪表板进行可视化
4. 使用日志洞察进行故障排查

**告警场景示例**：
- Lambda 错误率 > 1%
- EC2 CPU 利用率 > 80%
- API Gateway 4xx/5xx 错误激增
- DynamoDB 请求被限流
- ECS 任务失败

### 应用程序性能监控

**监控应用程序健康状况**：
1. 使用 **CloudWatch Application Signals MCP** 进行 APM
2. 跟踪服务级别目标（SLO）
3. 监控应用程序依赖项
4. 识别性能瓶颈
5. 设置分布式追踪

### 容器和 Kubernetes 监控

**针对容器化工作负载**：
1. 使用 **AWS Managed Prometheus MCP** 获取指标
2. 监控容器资源利用率
3. 跟踪 Pod 和节点健康状况
4. 创建 PromQL 查询用于自定义指标
5. 为容器异常设置告警

## 审计与安全最佳实践

### CloudTrail 活动分析

**审计 AWS 活动**：
1. 使用 **CloudTrail MCP** 分析 API 活动
2. 跟踪谁对资源做了变更
3. 调查安全事件
4. 监控可疑活动模式
5. 审计对策略的合规性

**常见审计场景**：
- "谁删除了这个 S3 存储桶？"
- "显示过去 24 小时内所有的 IAM 角色变更"
- "列出失败的登录尝试"
- "查找某个特定用户的所有操作"
- "跟踪安全组的修改"

### 安全评估

**定期安全审查**：
1. 使用 **Well-Architected Security Assessment MCP**
2. 根据最佳实践评估安全态势
3. 识别安全漏洞和薄弱环节
4. 实施推荐的安全改进措施
5. 记录安全合规情况

**安全评估领域**：
- 身份和访问管理（IAM）
- 检测性控制和监控
- 基础设施保护
- 数据保护和加密
- 事件响应准备

## 有效使用 MCP 服务器

### 成本分析工作流

1. **部署前**：使用 Pricing MCP 估算成本
2. **部署后**：使用 Billing MCP 跟踪实际支出
3. **分析**：使用 Cost Explorer MCP 进行详细成本分析
4. **优化**：实施 Cost Explorer 的建议

### 监控工作流

1. **设置**：配置 CloudWatch 指标和告警
2. **监控**：使用 CloudWatch MCP 跟踪关键指标
3. **分析**：使用 Application Signals 获取 APM 洞察
4. **排查**：查询 CloudWatch Logs 解决问题

### 安全工作流

1. **审计**：使用 CloudTrail MCP 审查活动
2. **评估**：使用 Well-Architected 安全评估
3. **修复**：实施安全建议
4. **监控**：通过 CloudWatch 跟踪安全事件

### MCP 使用最佳实践

1. **成本意识**：在部署资源前检查定价
2. **主动监控**：为关键指标设置告警
3. **定期审查**：每周分析成本和性能
4. **审计轨迹**：审查 CloudTrail 日志确保合规
5. **安全第一**：定期运行安全评估
6. **持续优化**：根据成本和性能建议采取行动

## 卓越运营指南

### 成本优化

- **全面打标**：使用一致的成本分配标签
- **月度审查**：分析支出趋势和异常
- **合理配置**：使资源匹配实际使用情况
- **自动化**：使用自动伸缩和调度
- **预算监控**：为成本超支设置告警

### 监控与告警

- **关键指标**：针对业务关键指标进行告警
- **减少噪音**：微调阈值以减少误报
- **可操作的告警**：确保告警具有明确的修复步骤
- **仪表板可见性**：为关键利益相关者创建仪表板
- **日志保留**：平衡成本和合规需求

### 安全与合规

- **最小权限**：授予所需的最低权限
- **定期审计**：审查 CloudTrail 日志中的异常
- **加密数据**：使用静态和传输中加密
- **持续评估**：频繁运行安全评估
- **事件响应**：制定安全事件的处理流程

## 其他资源

如需详细的运营模式和最佳实践，请参阅综合参考：

**文件**：`references/operations-patterns.md`

该参考包括：
- 成本优化策略
- 监控和告警模式
- 可观测性最佳实践
- 安全和合规指南
- 故障排查工作流

## CloudWatch 告警参考

**文件**：`references/cloudwatch-alarms.md`

常见告警配置适用于：
- Lambda 函数
- EC2 实例
- RDS 数据库
- DynamoDB 表
- API Gateway
- ECS 服务
- 应用程序负载均衡器

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例视为环境特定测试、安全审查或用户对破坏性或高成本操作的批准的替代品。