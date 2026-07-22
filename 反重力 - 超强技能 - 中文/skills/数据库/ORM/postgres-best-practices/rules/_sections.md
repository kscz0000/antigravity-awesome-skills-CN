# 分类定义

本文件定义 Postgres 最佳实践的规则分类。规则根据文件名前缀自动归入对应分类。

以下示例仅供参考，请替换为实际的 Postgres 最佳实践规则分类。

---

## 1. 查询性能（query）
**影响：** CRITICAL
**描述：** 慢查询、缺失索引、低效查询计划。Postgres 性能问题最常见的来源。

## 2. 连接管理（conn）
**影响：** CRITICAL
**描述：** 连接池、连接限制和 Serverless 策略。对高并发或 Serverless 部署的应用至关重要。

## 3. 安全与 RLS（security）
**影响：** CRITICAL
**描述：** 行级安全策略、权限管理和认证模式。

## 4. Schema 设计（schema）
**影响：** HIGH
**描述：** 表设计、索引策略、分区和数据类型选择。长期性能的基础。

## 5. 并发与锁（lock）
**影响：** MEDIUM-HIGH
**描述：** 事务管理、隔离级别、死锁预防和锁竞争模式。

## 6. 数据访问模式（data）
**影响：** MEDIUM
**描述：** 消除 N+1 查询、批量操作、游标分页和高效数据获取。

## 7. 监控与诊断（monitor）
**影响：** LOW-MEDIUM
**描述：** 使用 pg_stat_statements、EXPLAIN ANALYZE、指标收集和性能诊断。

## 8. 高级特性（advanced）
**影响：** LOW
**描述：** 全文搜索、JSONB 优化、PostGIS、扩展和高级 Postgres 特性。
