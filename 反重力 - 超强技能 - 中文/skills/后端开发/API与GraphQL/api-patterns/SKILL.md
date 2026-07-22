---
name: api-patterns
description: "API 设计原则与决策框架。REST 与 GraphQL 与 tRPC 选择、响应格式、版本控制、分页。触发词：API设计、REST API、GraphQL、tRPC、API版本控制、API分页、API认证、API限流、API文档、API安全测试"
risk: unknown
source: community
date_added: "2026-02-27"
---

# API 模式

> 2025 年 API 设计原则与决策框架。
> **学会思考，而非照搬固定模式。**

## 🎯 选择性阅读规则

**仅阅读与请求相关的文件！** 查看内容地图，找到你需要的内容。

---

## 📑 内容地图

| 文件 | 描述 | 何时阅读 |
|------|------|----------|
| `api-style.md` | REST 与 GraphQL 与 tRPC 决策树 | 选择 API 类型时 |
| `rest.md` | 资源命名、HTTP 方法、状态码 | 设计 REST API 时 |
| `response.md` | 封装模式、错误格式、分页 | 响应结构设计 |
| `graphql.md` | Schema 设计、使用时机、安全性 | 考虑 GraphQL 时 |
| `trpc.md` | TypeScript monorepo、类型安全 | TS 全栈项目 |
| `versioning.md` | URI/Header/Query 版本控制 | API 演进规划 |
| `auth.md` | JWT、OAuth、Passkey、API Keys | 认证模式选择 |
| `rate-limiting.md` | 令牌桶、滑动窗口 | API 保护 |
| `documentation.md` | OpenAPI/Swagger 最佳实践 | 文档编写 |
| `security-testing.md` | OWASP API Top 10、认证/授权测试 | 安全审计 |

---

## 🔗 相关技能

| 需求 | 技能 |
|------|------|
| API 实现 | `@[skills/backend-development]` |
| 数据结构 | `@[skills/database-design]` |
| 安全细节 | `@[skills/security-hardening]` |

---

## ✅ 决策检查清单

设计 API 之前：

- [ ] **询问用户 API 消费者是谁？**
- [ ] **为此上下文选择 API 风格？**（REST/GraphQL/tRPC）
- [ ] **定义一致的响应格式？**
- [ ] **规划版本控制策略？**
- [ ] **考虑认证需求？**
- [ ] **规划限流？**
- [ ] **确定文档方法？**

---

## ❌ 反模式

**禁止：**
- 默认对所有场景使用 REST
- 在 REST 端点中使用动词（/getUsers）
- 返回不一致的响应格式
- 向客户端暴露内部错误
- 跳过限流

**应该：**
- 根据上下文选择 API 风格
- 询问客户端需求
- 详细记录
- 使用适当的状态码

---

## 脚本

| 脚本 | 用途 | 命令 |
|------|------|------|
| `scripts/api_validator.py` | API 端点验证 | `python scripts/api_validator.py <project_path>` |

## 使用时机

当任务明确匹配上述范围时，可使用此技能执行工作流或操作描述。

## 限制

- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如所需输入、权限、安全边界或成功标准缺失，请停止并请求澄清。
