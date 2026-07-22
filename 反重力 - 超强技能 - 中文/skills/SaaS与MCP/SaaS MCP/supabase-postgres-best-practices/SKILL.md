---
name: supabase-postgres-best-practices
description: 基于 Supabase 的 Postgres 性能优化与最佳实践。在编写、审查或优化 Postgres 查询、模式设计或数据库配置时使用此技能。
risk: unknown
source: https://github.com/supabase/agent-skills/tree/main/skills/supabase-postgres-best-practices
source_repo: supabase/agent-skills
source_type: official
date_added: 2026-07-01
license: MIT
license_source: https://github.com/supabase/agent-skills/blob/main/LICENSE
---

# Supabase Postgres Best Practices
## 何时使用

当你需要基于 Supabase 的 Postgres 性能优化与最佳实践时使用此技能。在编写、审查或优化 Postgres 查询、模式设计或数据库配置时使用此技能。

由 Supabase 维护的 Postgres 综合性能优化指南。包含 8 个类别的规则，按影响优先级排列，用于指导自动化查询优化和模式设计。

## 适用场景

在以下场景参考这些指南：
- 编写 SQL 查询或设计模式
- 实现索引或查询优化
- 排查数据库性能问题
- 配置连接池或扩容
- 针对 Postgres 特性进行优化
- 使用行级安全（RLS）

## 规则类别（按优先级）

| 优先级 | 类别 | 影响 | 前缀 |
|----------|----------|--------|--------|
| 1 | 查询性能 | 关键 | `query-` |
| 2 | 连接管理 | 关键 | `conn-` |
| 3 | 安全与 RLS | 关键 | `security-` |
| 4 | 模式设计 | 高 | `schema-` |
| 5 | 并发与锁 | 中高 | `lock-` |
| 6 | 数据访问模式 | 中 | `data-` |
| 7 | 监控与诊断 | 中低 | `monitor-` |
| 8 | 高级特性 | 低 | `advanced-` |

## 使用方式

阅读各规则文件获取详细说明和 SQL 示例：

```
references/query-missing-indexes.md
references/query-partial-indexes.md
references/_sections.md
```

每条规则文件包含：
- 简要说明为什么重要
- 错误的 SQL 示例及解释
- 正确的 SQL 示例及解释
- 可选的 EXPLAIN 输出或指标
- 附加上下文和参考
- Supabase 特定说明（如适用）

## 参考资料

- https://www.postgresql.org/docs/current/
- https://supabase.com/docs
- https://wiki.postgresql.org/wiki/Performance_Optimization
- https://supabase.com/docs/guides/database/overview
- https://supabase.com/docs/guides/auth/row-level-security

## 限制

- 仅当任务明确匹配其上游产品或 API 范围时使用此技能。
- 在执行变更前，请对照当前官方文档验证命令、API 行为、定价、配额、凭证和部署效果。
- 不要将生成的示例替代环境特定的测试、安全审查或用户对破坏性或高成本操作的审批。
