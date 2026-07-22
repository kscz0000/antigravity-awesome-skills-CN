---
name: web-security-testing
description: "面向 OWASP Top 10 漏洞的 Web 应用安全测试工作流，覆盖注入、XSS、认证缺陷与访问控制问题。触发词：Web 安全测试、OWASP Top 10、XSS 测试、SQL 注入、IDOR、渗透测试、安全审计、漏洞评估、安全头检测、认证测试。"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Web 安全测试工作流

## 概述

针对 Web 应用的 OWASP Top 10 漏洞进行测试的专项工作流，覆盖注入攻击、XSS、认证缺陷与访问控制问题。

## 何时使用本工作流

在以下场景使用本工作流：
- 测试 Web 应用安全性
- 执行 OWASP Top 10 评估
- 开展渗透测试
- 验证安全控制措施
- 漏洞赏金狩猎

## 工作流阶段

### 阶段一：信息收集

#### 调用的技能
- `scanning-tools` - 安全扫描
- `top-web-vulnerabilities` - OWASP 知识

#### 操作
1. 绘制应用攻击面
2. 识别技术栈
3. 发现端点
4. 查找子域名
5. 记录发现

#### 可复制粘贴的提示词
```
Use @scanning-tools to perform web application reconnaissance
```

### 阶段二：注入测试

#### 调用的技能
- `sql-injection-testing` - SQL 注入
- `sqlmap-database-pentesting` - SQLMap

#### 操作
1. 测试 SQL 注入
2. 测试 NoSQL 注入
3. 测试命令注入
4. 测试 LDAP 注入
5. 记录漏洞

#### 可复制粘贴的提示词
```
Use @sql-injection-testing to test for SQL injection
```

```
Use @sqlmap-database-pentesting to automate SQL injection testing
```

### 阶段三：XSS 测试

#### 调用的技能
- `xss-html-injection` - XSS 测试
- `html-injection-testing` - HTML 注入

#### 操作
1. 测试反射型 XSS
2. 测试存储型 XSS
3. 测试基于 DOM 的 XSS
4. 测试 XSS 过滤器
5. 记录发现

#### 可复制粘贴的提示词
```
Use @xss-html-injection to test for cross-site scripting
```

### 阶段四：认证测试

#### 调用的技能
- `broken-authentication` - 认证测试

#### 操作
1. 测试撞库攻击
2. 测试暴力破解防护
3. 测试会话管理
4. 测试密码策略
5. 测试 MFA 实现

#### 可复制粘贴的提示词
```
Use @broken-authentication to test authentication security
```

### 阶段五：访问控制测试

#### 调用的技能
- `idor-testing` - IDOR 测试
- `file-path-traversal` - 路径穿越

#### 操作
1. 测试垂直权限提升
2. 测试水平权限提升
3. 测试 IDOR 漏洞
4. 测试目录穿越
5. 测试未授权访问

#### 可复制粘贴的提示词
```
Use @idor-testing to test for insecure direct object references
```

```
Use @file-path-traversal to test for path traversal
```

### 阶段六：安全头检测

#### 调用的技能
- `api-security-best-practices` - 安全头

#### 操作
1. 检查 CSP 实现
2. 验证 HSTS 配置
3. 测试 X-Frame-Options
4. 检查 X-Content-Type-Options
5. 验证 referrer 策略

#### 可复制粘贴的提示词
```
Use @api-security-best-practices to audit security headers
```

### 阶段七：报告

#### 调用的技能
- `reporting-standards` - 安全报告

#### 操作
1. 记录漏洞
2. 评估风险等级
3. 提供修复建议
4. 创建概念验证
5. 生成报告

#### 可复制粘贴的提示词
```
Use @reporting-standards to create security report
```

## OWASP Top 10 检查清单

- [ ] A01: 访问控制失效
- [ ] A02: 加密失败
- [ ] A03: 注入
- [ ] A04: 不安全设计
- [ ] A05: 安全配置错误
- [ ] A06: 易受攻击和过时的组件
- [ ] A07: 认证失败
- [ ] A08: 软件与数据完整性失效
- [ ] A09: 安全日志与监控失效
- [ ] A10: SSRF（服务端请求伪造）

## 质量门

- [ ] 所有 OWASP Top 10 项目均已测试
- [ ] 漏洞已记录
- [ ] 已捕获概念验证
- [ ] 已提供修复建议
- [ ] 已生成报告

## 相关工作流包

- `security-audit` - 安全审计
- `api-security-testing` - API 安全
- `wordpress-security` - WordPress 安全

## 局限性
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来询问澄清。
