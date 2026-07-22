---
name: security-checklist
description: >
  monopoly 安全加固清单参考文档。涵盖网络安全、认证授权、API 安全、数据安全、
  密钥管理、供应链与依赖、事件响应和合规（GDPR、PCI-DSS、HIPAA、SOC 2）。
risk: safe
reports-to: monopoly
---

# MONOPOLY — 安全加固清单

## 网络安全
- [ ] 所有服务在私有 VPC 内；仅 LB/API 网关对外暴露
- [ ] 安全组遵循最小权限原则（默认拒绝，按需开放端口/CIDR）
- [ ] NACL 作为第二道防线
- [ ] 启用 WAF，使用 OWASP Top 10 规则集
- [ ] DDoS 防护（至少 Cloudflare / AWS Shield Standard）
- [ ] 多区域服务间通信使用 VPN 或 Private Link

## 认证与授权
- [ ] JWT 令牌短有效期（15 分钟访问令牌，7 天刷新令牌）
- [ ] 第三方认证使用 OAuth 2.0 / OIDC
- [ ] 管理员账户强制 MFA
- [ ] 授权使用 RBAC 或 ABAC
- [ ] JWT 负载中不含敏感信息（使用不透明引用）
- [ ] 令牌撤销策略（Redis 黑名单或短 TTL）

## API 安全
- [ ] API 网关处限流（按用户、按 IP、按端点）
- [ ] 所有端点做输入校验和净化
- [ ] SQL 注入防护（参数化查询、ORM）
- [ ] XSS 防护（输出编码、CSP 头）
- [ ] CSRF 防护（SameSite Cookie、CSRF 令牌）
- [ ] CORS 策略锁定（不用通配符 `*`）
- [ ] HTTP 安全头（HSTS、X-Frame-Options、X-Content-Type-Options）

## 数据安全
- [ ] 传输加密（全面使用 TLS 1.2+，推荐 TLS 1.3）
- [ ] 静态加密（数据库 AES-256，S3 SSE）
- [ ] PII 数据已识别、最小化，必要时字段级加密
- [ ] 数据库备份已加密
- [ ] 日志中不含敏感数据（PII、密码、令牌、卡号）

## 密钥管理
- [ ] 代码或环境变量中不存放明文密钥
- [ ] 使用密钥管理器（HashiCorp Vault、AWS Secrets Manager、GCP Secret Manager）
- [ ] 密钥轮换自动化
- [ ] 服务间认证使用 IAM 角色（而非静态凭证）

## 供应链与依赖
- [ ] 依赖扫描（Snyk、Dependabot、npm audit）
- [ ] 容器镜像扫描（Trivy、ECR 扫描）
- [ ] 生产环境锁定依赖版本
- [ ] 生成 SBOM（软件物料清单）用于合规

## 事件响应
- [ ] 所有管理员操作和数据访问有审计日志
- [ ] 异常访问模式告警
- [ ] 事件响应手册已文档化
- [ ] 数据泄露通知流程已定义（GDPR 72 小时规则）
- [ ] 定期渗透测试已排期

## 合规（按适用情况）
- [ ] GDPR：数据驻留、删除权、同意追踪
- [ ] PCI-DSS：如处理卡数据 — 绝不存储原始 PAN
- [ ] HIPAA：如处理健康数据 — 加密、审计日志、与供应商签 BAA
- [ ] SOC 2 Type II：访问控制、可用性、机密性证据


## 局限性
- 本文档为参考性质，可能未覆盖所有边界情况。在生产环境前务必验证架构方案。
