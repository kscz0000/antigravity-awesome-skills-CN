---
name: api-security-testing
description: "REST 和 GraphQL API 安全测试工作流，涵盖认证、授权、速率限制、输入验证和安全最佳实践。触发词：API安全测试、接口安全、API渗透测试、GraphQL安全、API认证测试、API授权测试、速率限制测试、输入验证测试、API漏洞扫描、接口漏洞检测"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# API 安全测试工作流

## 概述

专门用于测试 REST 和 GraphQL API 安全的工作流，包括认证、授权、速率限制、输入验证和 API 特定漏洞。

## 何时使用此工作流

在以下情况下使用此工作流：
- 测试 REST API 安全
- 评估 GraphQL 端点
- 验证 API 认证
- 测试 API 速率限制
- 漏洞赏金 API 测试

## 工作流阶段

### 阶段 1：API 发现

#### 调用的技能
- `api-fuzzing-bug-bounty` - API 模糊测试
- `scanning-tools` - API 扫描

#### 操作
1. 枚举端点
2. 记录 API 方法
3. 识别参数
4. 映射数据流
5. 审查文档

#### 复制粘贴提示词
```
Use @api-fuzzing-bug-bounty to discover API endpoints
```

### 阶段 2：认证测试

#### 调用的技能
- `broken-authentication` - 认证测试
- `api-security-best-practices` - API 认证

#### 操作
1. 测试 API 密钥验证
2. 测试 JWT 令牌
3. 测试 OAuth2 流程
4. 测试令牌过期
5. 测试刷新令牌

#### 复制粘贴提示词
```
Use @broken-authentication to test API authentication
```

### 阶段 3：授权测试

#### 调用的技能
- `idor-testing` - IDOR 测试

#### 操作
1. 测试对象级授权
2. 测试功能级授权
3. 测试基于角色的访问
4. 测试权限提升
5. 测试多租户隔离

#### 复制粘贴提示词
```
Use @idor-testing to test API authorization
```

### 阶段 4：输入验证

#### 调用的技能
- `api-fuzzing-bug-bounty` - API 模糊测试
- `sql-injection-testing` - 注入测试

#### 操作
1. 测试参数验证
2. 测试 SQL 注入
3. 测试 NoSQL 注入
4. 测试命令注入
5. 测试 XXE 注入

#### 复制粘贴提示词
```
Use @api-fuzzing-bug-bounty to fuzz API parameters
```

### 阶段 5：速率限制

#### 调用的技能
- `api-security-best-practices` - 速率限制

#### 操作
1. 测试速率限制头
2. 测试暴力破解防护
3. 测试资源耗尽
4. 测试绕过技术
5. 记录限制

#### 复制粘贴提示词
```
Use @api-security-best-practices to test rate limiting
```

### 阶段 6：GraphQL 测试

#### 调用的技能
- `api-fuzzing-bug-bounty` - GraphQL 模糊测试

#### 操作
1. 测试内省
2. 测试查询深度
3. 测试查询复杂度
4. 测试批量查询
5. 测试字段建议

#### 复制粘贴提示词
```
Use @api-fuzzing-bug-bounty to test GraphQL security
```

### 阶段 7：错误处理

#### 调用的技能
- `api-security-best-practices` - 错误处理

#### 操作
1. 测试错误消息
2. 检查信息泄露
3. 测试堆栈跟踪
4. 验证日志记录
5. 记录发现

#### 复制粘贴提示词
```
Use @api-security-best-practices to audit API error handling
```

## API 安全检查清单

- [ ] 认证正常工作
- [ ] 授权已强制执行
- [ ] 输入已验证
- [ ] 速率限制已激活
- [ ] 错误已净化
- [ ] 日志已启用
- [ ] CORS 已配置
- [ ] HTTPS 已强制

## 质量门控

- [ ] 所有端点已测试
- [ ] 漏洞已记录
- [ ] 已提供修复建议
- [ ] 报告已生成

## 相关工作流包

- `security-audit` - 安全审计
- `web-security-testing` - Web 安全
- `api-development` - API 开发

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
