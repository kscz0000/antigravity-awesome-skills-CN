# AWS Terraform 模块模式

## VPC 模块
- 带公有/私有子网的 VPC
- Internet Gateway 和 NAT Gateway
- 路由表及关联
- Network ACL
- VPC Flow Logs

## EKS 模块
- 带托管节点组的 EKS 集群
- IRSA（IAM Roles for Service Accounts）
- 集群自动伸缩器
- VPC CNI 配置
- 集群日志

## RDS 模块
- RDS 实例或集群
- 自动备份
- 只读副本
- 参数组
- 子网组
- 安全组

## S3 模块
- 带版本控制的 S3 存储桶
- 静态加密
- 存储桶策略
- 生命周期规则
- 跨区域复制配置

## ALB 模块
- Application Load Balancer
- 目标组
- 监听规则
- SSL/TLS 证书
- 访问日志

## Lambda 模块
- Lambda 函数
- IAM 执行角色
- CloudWatch Logs
- 环境变量
- VPC 配置（可选）

## 安全组模块
- 可复用的安全组规则
- 入站/出站规则
- 动态规则创建
- 规则描述

## 最佳实践

1. 使用 AWS provider 版本 ~> 5.0
2. 默认启用加密
3. 使用最小权限 IAM
4. 为所有资源统一添加标签
5. 启用日志和监控
6. 使用 KMS 进行加密
7. 实施备份策略
8. 尽可能使用 PrivateLink
9. 启用 GuardDuty/SecurityHub
10. 遵循 AWS Well-Architected Framework
