---
name: postgres-best-practices
description: "Supabase 的 Postgres 性能优化与最佳实践。当用户编写、审查或优化 Postgres 查询、Schema 设计或数据库配置时使用。"
risk: safe
source: community
date_added: "2026-02-27"
---

# Supabase Postgres 最佳实践

由 Supabase 维护的 Postgres 性能优化完整指南。涵盖 8 个类别的规则，按影响程度排序，用于指导自动化查询优化和 Schema 设计。

## 适用场景

在以下情况参考本指南：
- 编写 SQL 查询或设计 Schema
- 创建索引或优化查询
- 排查数据库性能问题
- 配置连接池或扩展策略
- 针对 Postgres 特性进行优化
- 使用行级安全（RLS）

## 规则分类与优先级

| 优先级 | 分类 | 影响 | 前缀 |
|--------|------|------|------|
| 1 | 查询性能 | CRITICAL | `query-` |
| 2 | 连接管理 | CRITICAL | `conn-` |
| 3 | 安全与 RLS | CRITICAL | `security-` |
| 4 | Schema 设计 | HIGH | `schema-` |
| 5 | 并发与锁 | MEDIUM-HIGH | `lock-` |
| 6 | 数据访问模式 | MEDIUM | `data-` |
| 7 | 监控与诊断 | LOW-MEDIUM | `monitor-` |
| 8 | 高级特性 | LOW | `advanced-` |

## 使用方法

阅读各规则文件获取详细说明和 SQL 示例：

```
rules/query-missing-indexes.md
rules/schema-partial-indexes.md
rules/_sections.md
```

每个规则文件包含：
- 该规则为何重要的简要说明
- 错误的 SQL 示例及解释
- 正确的 SQL 示例及解释
- 可选的 EXPLAIN 输出或性能指标
- 补充上下文和参考资料
- Supabase 特定说明（如适用）

## 完整编译文档

包含所有规则展开的完整指南：`AGENTS.md`

## 适用场景

本技能适用于执行概览中描述的工作流或操作。

## 限制条件
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
