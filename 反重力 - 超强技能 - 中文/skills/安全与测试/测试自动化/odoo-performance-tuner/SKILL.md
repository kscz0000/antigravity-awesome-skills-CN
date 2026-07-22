---
name: odoo-performance-tuner
description: "Odoo 性能诊断与优化专家指南：慢查询、Worker 配置、内存限制、PostgreSQL 调优及性能分析工具。当用户要求优化 Odoo 性能、排查慢查询、配置 Worker、调优 PostgreSQL 或使用性能分析工具时使用。"
risk: safe
source: "self"
---

# Odoo Performance Tuner

## 概述

本技能帮助诊断和解决 Odoo 性能问题——从页面加载缓慢、数据库瓶颈，到 Worker 配置不当和内存膨胀。涵盖 PostgreSQL 查询调优、Odoo Worker 设置和内置性能分析工具。

## 使用场景

- 生产环境 Odoo 响应慢（页面加载慢、超时）
- 日志中出现 `MemoryError` 或 `Worker timeout` 错误
- 使用 Odoo 的性能分析器诊断慢查询
- 针对特定服务器配置调优 `odoo.conf`

## 工作流程

1. **激活**：提及 `@odoo-performance-tuner` 并描述你的性能问题
2. **诊断**：分享相关日志或配置，获取根因分析
3. **修复**：获得具体的配置变更方案及解释

## 示例

### 示例 1：推荐的 Worker 配置

```ini
# odoo.conf — tuned for a 4-core, 8GB RAM server

workers = 9                   # (CPU_cores × 2) + 1 — never set to 0 in production
max_cron_threads = 2          # background cron jobs; keep ≤ 2 to preserve user-facing capacity
limit_memory_soft = 1610612736  # 1.5 GB — worker is recycled gracefully after this
limit_memory_hard = 2147483648  # 2.0 GB — worker is killed immediately; prevents OOM crashes
limit_time_cpu = 600          # max CPU seconds per request
limit_time_real = 1200        # max wall-clock seconds per request
limit_request = 8192          # max requests before worker recycles (prevents memory leaks)
```

### 示例 2：使用 PostgreSQL 查找慢查询

```sql
-- Step 1: Enable pg_stat_statements extension (run once as postgres superuser)
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Step 2: Also add to postgresql.conf and reload:
-- shared_preload_libraries = 'pg_stat_statements'
-- log_min_duration_statement = 1000   -- log queries taking > 1 second

-- Step 3: Find the top 10 slowest average queries
SELECT
    LEFT(query, 100) AS query_snippet,
    round(mean_exec_time::numeric, 2) AS avg_ms,
    calls,
    round(total_exec_time::numeric, 2) AS total_ms
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Step 4: Check for missing indexes causing full table scans
SELECT schemaname, tablename, attname, n_distinct, correlation
FROM pg_stats
WHERE tablename = 'sale_order_line'
  AND correlation < 0.5   -- low correlation = poor index efficiency
ORDER BY n_distinct DESC;
```

### 示例 3：使用 Odoo 内置性能分析器

```text
Prerequisites: Run Odoo with ?debug=1 in the URL to enable debug mode.

Menu: Settings → Technical → Profiling

Steps:
  1. Click "Enable Profiling" — set a duration (e.g., 60 seconds)
  2. Navigate to and reproduce the slow action
  3. Return to Settings → Technical → Profiling → View Results

What to look for:
  - Total SQL queries > 100 on a single page  → N+1 query problem
  - Single queries taking > 100ms             → missing DB index
  - Same query repeated many times            → missing cache, use @ormcache
  - Python time high but SQL low             → compute field inefficiency
```

## 最佳实践

- ✅ **推荐：** 在内存中的记录集上使用 `mapped()`、`filtered()` 和 `sorted()` — 它们不会触发额外的 SQL 查询。
- ✅ **推荐：** 在 domain 过滤器常用字段上添加 PostgreSQL B-tree 索引（`partner_id`、`state`、`date_order`）。
- ✅ **推荐：** 为静态资源启用 Odoo 的 HTTP 缓存，并在网站前端部署 CDN（Cloudflare、AWS CloudFront）。
- ✅ **推荐：** 对使用相同参数反复调用的方法使用 `@tools.ormcache` 装饰器。
- ❌ **禁止：** 生产环境设置 `workers = 0` — 单线程模式会串行处理所有请求，任何慢操作都会阻塞全部用户。
- ❌ **禁止：** 忽略 `limit_memory_soft` — 超出限制的 Worker 会在请求间隙被回收；没有此限制则内存无限增长直至崩溃。
- ❌ **禁止：** 直接操作记录集的 `prefetch_ids` — 依赖 Odoo 的自动批量预取机制（默认启用）。

## 限制

- PostgreSQL 调优（`shared_buffers`、`work_mem`、`effective_cache_size`）因服务器配置而异，本文不做深入讨论 — 以 [PGTune](https://pgtune.leopard.in.ua/) 作为初始基准。
- Odoo 内置性能分析器仅捕获 **Python + SQL** 追踪；JavaScript 渲染性能需使用浏览器开发者工具。
- **Odoo.sh** 托管服务限制了对 PostgreSQL 和 `odoo.conf` 的直接访问 — 部分调优选项不可用。
- 不涵盖 **Redis 会话存储** 或 **Celery 任务队列** 优化，这些是面向超高流量实例的高级方案。