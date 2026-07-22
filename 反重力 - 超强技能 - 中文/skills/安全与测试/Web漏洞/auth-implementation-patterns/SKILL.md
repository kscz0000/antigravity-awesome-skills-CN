---
name: auth-implementation-patterns
description: "使用行业标准模式和现代最佳实践构建安全、可扩展的身份认证与授权系统。触发词：身份认证、授权系统、JWT、OAuth2、SSO、RBAC、会话管理、登录系统、权限控制、认证实现、auth implementation、authentication、authorization"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 身份认证与授权实现模式

使用行业标准模式和现代最佳实践构建安全、可扩展的身份认证与授权系统。

## 使用此技能的场景

- 实现用户身份认证系统
- 保护 REST 或 GraphQL API
- 添加 OAuth2/社交登录或 SSO
- 设计会话管理或 RBAC
- 调试身份认证或授权问题

## 不使用此技能的场景

- 仅需要 UI 文案或登录页面样式
- 任务仅涉及基础设施，不涉及身份问题
- 无法更改认证策略或凭证存储

## 指导说明

- 定义用户、租户、流程和威胁模型约束。
- 选择认证策略（会话、JWT、OIDC）和令牌生命周期。
- 设计授权模型和策略执行点。
- 规划密钥存储、轮换、日志记录和审计要求。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 安全注意事项

- 切勿记录密钥、令牌或凭证。
- 强制执行最小权限原则，确保密钥安全存储。

## 资源

- `resources/implementation-playbook.md` 包含详细模式和示例。

## 局限性
- 仅当任务明确符合上述描述范围时使用此技能。
- 输出内容不能替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
