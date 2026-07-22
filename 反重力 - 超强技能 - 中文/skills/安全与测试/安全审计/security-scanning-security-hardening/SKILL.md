---
name: security-scanning-security-hardening
description: "协调跨应用、基础设施和合规控制的多层安全扫描与加固。触发词：安全扫描、安全加固、多层安全、安全协调、安全控制、安全合规、安全评估、安全监控"
risk: unknown
source: community
date_added: "2026-02-27"
---

通过协调的多智能体编排，实施综合安全加固和纵深防御策略：

[扩展思考：此工作流在所有应用层实施纵深防御安全策略。它协调专业安全智能体执行综合评估、实施分层安全控制，并建立持续安全监控。该方法遵循现代 DevSecOps 原则，包括左移安全、自动化扫描和合规验证。每个阶段都基于先前发现，构建能够应对当前漏洞和未来威胁的弹性安全态势。]

## 使用场景

- 运行协调的安全加固计划
- 在应用、基础设施和 CI/CD 间建立纵深防御控制
- 优先处理扫描和威胁建模中的修复工作

## 不适用场景

- 只需要快速扫描而不需要修复工作
- 缺乏安全测试或变更的授权
- 环境无法容忍侵入性安全控制

## 使用说明

1. 执行阶段 1 建立安全基线。
2. 应用阶段 2 修复高风险问题。
3. 实施阶段 3 控制并验证防御。
4. 完成阶段 4 验证和合规检查。

## 安全注意事项

- 未经批准，避免在生产环境进行侵入性测试。
- 确保在加固变更前存在回滚计划。

## 阶段 1：综合安全评估

### 1. 初始漏洞扫描
- 使用 Task 工具，subagent_type="security-auditor"
- 提示："对 $ARGUMENTS 执行综合安全评估。使用 Semgrep/SonarQube 进行 SAST 分析，使用 OWASP ZAP 进行 DAST 扫描，使用 Snyk/Trivy 进行依赖审计，使用 GitLeaks/TruffleHog 进行密钥检测。生成 SBOM 用于供应链分析。识别 OWASP Top 10 漏洞、CWE 弱点和 CVE 风险。"
- 输出：详细漏洞报告，包含 CVSS 评分、可利用性分析、攻击面映射、密钥暴露报告、SBOM 清单
- 上下文：所有修复工作的初始基线

### 2. 威胁建模与风险分析
- 使用 Task 工具，subagent_type="security-auditor"
- 提示："对 $ARGUMENTS 使用 STRIDE 方法进行威胁建模。分析攻击向量，创建攻击树，评估已识别漏洞的业务影响。将威胁映射到 MITRE ATT&CK 框架。基于可能性和影响优先排序风险。"
- 输出：威胁模型图、风险矩阵（含优先排序的漏洞）、攻击场景文档、业务影响分析
- 上下文：使用漏洞扫描结果为威胁优先级提供信息

### 3. 架构安全审查
- 使用 Task 工具，subagent_type="backend-api-security::backend-architect"
- 提示："审查 $ARGUMENTS 中的安全弱点架构。评估服务边界、数据流安全、认证/授权架构、加密实现、网络分段。设计零信任架构模式。参考威胁模型和漏洞发现。"
- 输出：安全架构评估、零信任设计建议、服务网格安全要求、数据分类矩阵
- 上下文：结合威胁模型解决架构漏洞

## 阶段 2：漏洞修复

### 4. 关键漏洞修复
- 使用 Task 工具，subagent_type="security-auditor"
- 提示："协调 $ARGUMENTS 中关键漏洞（CVSS 7+）的即时修复。使用参数化查询修复 SQL 注入，使用输出编码修复 XSS，使用安全会话管理修复认证绕过，使用输入验证修复不安全的反序列化。为 CVE 应用安全补丁。"
- 输出：已修补的代码（含漏洞修复）、安全补丁文档、回归测试要求
- 上下文：解决漏洞评估中的高优先级项目

### 5. 后端安全加固
- 使用 Task 工具，subagent_type="backend-api-security::backend-security-coder"
- 提示："为 $ARGUMENTS 实施综合后端安全控制。使用 OWASP ESAPI 添加输入验证，实施速率限制和 DDoS 防护，使用 OAuth2/JWT 验证保护 API 端点，使用 AES-256/TLS 1.3 为静态/传输数据添加加密。实施安全日志记录而不暴露 PII。"
- 输出：加固的 API 端点、验证中间件、加密实现、安全配置模板
- 上下文：基于漏洞修复构建预防性控制

### 6. 前端安全实施
- 使用 Task 工具，subagent_type="frontend-mobile-security::frontend-security-coder"
- 提示："为 $ARGUMENTS 实施前端安全措施。配置基于 nonce 的 CSP 头，使用 DOMPurify 实现 XSS 防护，使用 PKCE OAuth2 保护认证流程，为外部资源添加 SRI，使用 SameSite/HttpOnly/Secure 标志实现安全 Cookie 处理。"
- 输出：安全的前端组件、CSP 策略配置、认证流程实现、安全头配置
- 上下文：通过客户端保护补充后端安全

### 7. 移动安全加固
- 使用 Task 工具，subagent_type="frontend-mobile-security::mobile-security-coder"
- 提示："为 $ARGUMENTS 实施移动应用安全。添加证书固定，实施生物识别认证，使用加密保护本地存储，使用 ProGuard/R8 进行代码混淆，实施防篡改和 Root/越狱检测，保护 IPC 通信。"
- 输出：加固的移动应用、安全配置文件、混淆规则、证书固定实现
- 上下文：将安全扩展到移动平台（如适用）

## 阶段 3：安全控制实施

### 8. 认证与授权增强
- 使用 Task 工具，subagent_type="security-auditor"
- 提示："为 $ARGUMENTS 实施现代认证系统。部署带 PKCE 的 OAuth2/OIDC，实施带 TOTP/WebAuthn/FIDO2 的 MFA，添加基于风险的认证，实施带最小权限原则的 RBAC/ABAC，添加带安全令牌轮换的会话管理。"
- 输出：认证服务配置、MFA 实现、授权策略、会话管理系统
- 上下文：基于架构审查加强访问控制

### 9. 基础设施安全控制
- 使用 Task 工具，subagent_type="deployment-strategies::deployment-engineer"
- 提示："为 $ARGUMENTS 部署基础设施安全控制。配置 WAF 规则以防护 OWASP，实施带微分段的网络分段，部署 IDS/IPS 系统，配置云安全组和 NACL，实施带速率限制和地理封锁的 DDoS 防护。"
- 输出：WAF 配置、网络安全策略、IDS/IPS 规则、云安全配置
- 上下文：实施网络级防御

### 10. 密钥管理实施
- 使用 Task 工具，subagent_type="deployment-strategies::deployment-engineer"
- 提示："为 $ARGUMENTS 实施企业密钥管理。部署 HashiCorp Vault 或 AWS Secrets Manager，实施密钥轮换策略，移除硬编码密钥，配置最小权限 IAM 角色，实施带 HSM 支持的加密密钥管理。"
- 输出：密钥管理配置、轮换策略、IAM 角色定义、密钥管理流程
- 上下文：消除密钥暴露漏洞

## 阶段 4：验证与合规

### 11. 渗透测试与验证
- 使用 Task 工具，subagent_type="security-auditor"
- 提示："为 $ARGUMENTS 执行综合渗透测试。执行已认证和未认证测试、API 安全测试、业务逻辑测试、权限提升尝试。使用 Burp Suite、Metasploit 和自定义漏洞利用。验证所有安全控制的有效性。"
- 输出：渗透测试报告、概念验证漏洞利用、修复验证、安全控制有效性指标
- 上下文：验证所有已实施的安全措施

### 12. 合规与标准验证
- 使用 Task 工具，subagent_type="security-auditor"
- 提示："验证 $ARGUMENTS 的安全框架合规性。验证 OWASP ASVS Level 2、CIS 基准、SOC2 Type II 要求、GDPR/CCPA 隐私控制、HIPAA/PCI-DSS（如适用）。生成合规证明报告。"
- 输出：合规评估报告、差距分析、修复要求、审计证据收集
- 上下文：确保法规和行业标准合规

### 13. 安全监控与 SIEM 集成
- 使用 Task 工具，subagent_type="incident-response::devops-troubleshooter"
- 提示："为 $ARGUMENTS 实施安全监控和 SIEM。部署 Splunk/ELK/Sentinel 集成，配置安全事件关联，实施行为分析以进行异常检测，设置自动化事件响应剧本，创建安全仪表板和告警。"
- 输出：SIEM 配置、关联规则、事件响应剧本、安全仪表板、告警定义
- 上下文：建立持续安全监控

## 配置选项
- scanning_depth: "quick" | "standard" | "comprehensive"（默认：comprehensive）
- compliance_frameworks: ["OWASP", "CIS", "SOC2", "GDPR", "HIPAA", "PCI-DSS"]
- remediation_priority: "cvss_score" | "exploitability" | "business_impact"
- monitoring_integration: "splunk" | "elastic" | "sentinel" | "custom"
- authentication_methods: ["oauth2", "saml", "mfa", "biometric", "passwordless"]

## 成功标准
- 所有关键漏洞（CVSS 7+）已修复
- OWASP Top 10 漏洞已解决
- 渗透测试中零高风险发现
- 安全框架验证通过
- 安全监控能够检测威胁并发出告警
- 关键告警的事件响应时间 < 15 分钟
- SBOM 已生成且漏洞已跟踪
- 所有密钥通过安全保险库管理
- 认证实施 MFA 和安全会话管理
- 安全测试已集成到 CI/CD 流水线

## 协调说明
- 每个阶段提供详细发现，为后续阶段提供信息
- 安全审计智能体与领域特定智能体协调修复
- 所有代码变更在实施前经过安全审查
- 评估与修复之间的持续反馈循环
- 安全发现在集中式漏洞管理系统中跟踪
- 实施后安排定期安全审查

安全加固目标：$ARGUMENTS

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。