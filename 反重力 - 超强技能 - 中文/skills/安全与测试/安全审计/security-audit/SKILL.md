---
name: security-audit
description: "全面的安全审计工作流，涵盖Web应用测试、API安全、渗透测试、漏洞扫描和安全加固。触发词：安全审计、安全测试、渗透测试、漏洞扫描、安全加固"
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# 安全审计工作流套件

## 概述

针对Web应用、API和基础设施的全面安全审计工作流。该套件协调渗透测试、漏洞评估、安全扫描和修复相关的技能。

## 使用场景

在以下情况下使用此工作流：
- 对Web应用进行安全审计
- 测试API安全
- 执行渗透测试
- 扫描漏洞
- 加固应用安全
- 合规性安全评估

## 工作流阶段

### 阶段1：侦察

#### 调用技能
- `scanning-tools` - 安全扫描
- `shodan-reconnaissance` - Shodan搜索
- `top-web-vulnerabilities` - OWASP Top 10

#### 操作步骤
1. 确定目标范围
2. 收集情报
3. 绘制攻击面
4. 识别技术栈
5. 记录发现

#### 复制粘贴提示词
```
Use @scanning-tools to perform initial reconnaissance
```

```
Use @shodan-reconnaissance to find exposed services
```

### 阶段2：漏洞扫描

#### 调用技能
- `vulnerability-scanner` - 漏洞分析
- `security-scanning-security-sast` - 静态分析
- `security-scanning-security-dependencies` - 依赖扫描

#### 操作步骤
1. 运行自动化扫描器
2. 执行静态分析
3. 扫描依赖项
4. 识别配置错误
5. 记录漏洞

#### 复制粘贴提示词
```
Use @vulnerability-scanner to scan for OWASP Top 10 vulnerabilities
```

```
Use @security-scanning-security-dependencies to audit dependencies
```

### 阶段3：Web应用测试

#### 调用技能
- `top-web-vulnerabilities` - OWASP漏洞
- `sql-injection-testing` - SQL注入
- `xss-html-injection` - XSS测试
- `broken-authentication` - 认证测试
- `idor-testing` - IDOR测试
- `file-path-traversal` - 路径遍历
- `burp-suite-testing` - Burp Suite测试

#### 操作步骤
1. 测试注入漏洞
2. 测试认证机制
3. 测试会话管理
4. 测试访问控制
5. 测试输入验证
6. 测试安全头

#### 复制粘贴提示词
```
Use @sql-injection-testing to test for SQL injection vulnerabilities
```

```
Use @xss-html-injection to test for cross-site scripting
```

```
Use @broken-authentication to test authentication security
```

### 阶段4：API安全测试

#### 调用技能
- `api-fuzzing-bug-bounty` - API模糊测试
- `api-security-best-practices` - API安全最佳实践

#### 操作步骤
1. 枚举API端点
2. 测试认证/授权
3. 测试速率限制
4. 测试输入验证
5. 测试错误处理
6. 记录API漏洞

#### 复制粘贴提示词
```
Use @api-fuzzing-bug-bounty to fuzz API endpoints
```

### 阶段5：渗透测试

#### 调用技能
- `pentest-commands` - 渗透测试命令
- `pentest-checklist` - 渗透测试规划
- `ethical-hacking-methodology` - 道德黑客方法论
- `metasploit-framework` - Metasploit框架

#### 操作步骤
1. 规划渗透测试
2. 执行攻击场景
3. 利用漏洞
4. 记录概念验证
5. 评估影响

#### 复制粘贴提示词
```
Use @pentest-checklist to plan penetration test
```

```
Use @pentest-commands to execute penetration testing
```

### 阶段6：安全加固

#### 调用技能
- `security-scanning-security-hardening` - 安全加固
- `auth-implementation-patterns` - 认证实现模式
- `api-security-best-practices` - API安全最佳实践

#### 操作步骤
1. 实施安全控制
2. 配置安全头
3. 设置认证
4. 实施授权
5. 配置日志记录
6. 应用补丁

#### 复制粘贴提示词
```
Use @security-scanning-security-hardening to harden application security
```

### 阶段7：报告

#### 调用技能
- `reporting-standards` - 安全报告标准

#### 操作步骤
1. 记录发现
2. 评估风险等级
3. 提供修复步骤
4. 创建执行摘要
5. 生成技术报告

## 安全测试检查清单

### OWASP Top 10
- [ ] 注入漏洞（SQL、NoSQL、OS、LDAP）
- [ ] 身份验证失效
- [ ] 敏感数据泄露
- [ ] XML外部实体（XXE）
- [ ] 访问控制失效
- [ ] 安全配置错误
- [ ] 跨站脚本（XSS）
- [ ] 不安全的反序列化
- [ ] 使用含有已知漏洞的组件
- [ ] 日志记录和监控不足

### API安全
- [ ] 认证机制
- [ ] 授权检查
- [ ] 速率限制
- [ ] 输入验证
- [ ] 错误处理
- [ ] 安全头

## 质量门禁

- [ ] 所有计划测试已执行
- [ ] 漏洞已记录
- [ ] 概念验证已捕获
- [ ] 风险评估已完成
- [ ] 修复步骤已提供
- [ ] 报告已生成

## 相关工作流套件

- `development` - 安全开发实践
- `wordpress` - WordPress安全
- `cloud-devops` - 云安全
- `testing-qa` - 安全测试

## 限制条件
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。