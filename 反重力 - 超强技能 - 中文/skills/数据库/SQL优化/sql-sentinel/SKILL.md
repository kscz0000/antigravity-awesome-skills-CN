---
name: sql-sentinel
description: "审计 SQL 中消耗数仓额度的成本与性能反模式。对数仓健康度评分 0-100，并输出按优先级排序的降本方案，适用于 BigQuery、Snowflake、Redshift 和 Postgres。"
category: data
risk: critical
source: community
source_repo: takeaseatventure/sql-sentinel
source_type: community
date_added: "2026-06-26"
author: takeaseat
tags: [sql, bigquery, snowflake, redshift, postgres, data-warehouse, cost-optimization, performance, audit, finops]
tools: [claude, cursor, codex, gemini]
plugin:
  targets:
    codex: blocked
    claude: blocked
  setup:
    type: manual
    summary: "仅在固定或审查完确切 commit 后，才克隆上游分析器并运行。"
    docs: SKILL.md
license: "MIT"
license_source: "https://github.com/takeaseatventure/sql-sentinel/blob/main/LICENSE"
---

# sql-sentinel

## 概述

一款静态分析技能，用于审计 SQL 中占据数仓账单大头的成本与性能反模式——`SELECT *`、全表扫描、非 SARGable 谓词、笛卡尔连接、`NOT IN` 的 NULL 陷阱等共 20 条规则。它对数仓查询健康度评分 0-100（A-F），并输出按优先级排序的降本方案，每条发现都包含原因、具体修复建议和预估节省。

面向分析工程师（dbt、Looker）、运行 FinOps /"降低云支出"项目的数据平台团队，以及任何在 SQL 上线前做代码审查的人。支持 BigQuery、Snowflake、Redshift 和 Postgres。零依赖，MIT 许可。

可执行引擎和完整规则集位于源仓库：https://github.com/takeaseatventure/sql-sentinel。请将该仓库视为第三方可执行代码。

## 何时使用此技能

- 用户为 BigQuery、Snowflake、Redshift、Postgres 或 Spark SQL 编写或审查查询时。
- 用户问"为什么这个查询这么慢？"或"为什么我的数仓账单这么高？"时。
- 用户即将将仪表盘查询或 dbt 模型发布到生产环境时。
- 数据工程师在代码审查或成本优化巡检前需要第二双眼睛时。
- 团队正在开展"降低云支出"或 FinOps 专项行动时。

## 工作原理

引擎将 SQL 脚本按语句拆分（正确处理引号和注释），对每条语句运行 20 条规则，按严重程度加权评分（critical 25、high 12、medium 5、low 1）得出 0-100 健康分，并返回按优先级排序的降本方案。

### 步骤 1：运行审计

仅在选定已审查的 commit、tag 或 release 之后，才安装或克隆源仓库。不要仅因本技能链接了该仓库就直接从可变的默认分支运行代码：

```bash
git clone https://github.com/takeaseatventure/sql-sentinel.git
cd sql-sentinel
git checkout <reviewed-commit-or-tag>
node scripts/sql-sentinel.js path/to/query.sql
```

或以编程方式调用：

```javascript
const { auditSql } = require('./scripts/sql-sentinel');
const report = auditSql(yourSqlString, { dialect: 'bigquery' });
console.log(report.healthScore);      // 0-100
console.log(report.grade);            // 'A' | 'B' | 'C' | 'D' | 'E' | 'F'
console.log(report.prioritizedPlan);  // array, worst findings first
```

### 步骤 2：阅读优先级方案

输出以严重发现开头（笛卡尔连接、批量 DELETE），逐级递减到低严重度的风格问题。每条发现解释它*为什么*烧钱以及*如何*修复。

## 示例

### 示例 1：一个杂乱的仪表盘查询

```sql
SELECT DISTINCT *
FROM user_events, raw_logs
WHERE LOWER(event_name) LIKE '%signup%'
  AND user_id NOT IN (SELECT id FROM deleted_users)
ORDER BY created_at;
```

审计评分为 17/100（等级 F），标记 7 条发现：
- CRITICAL：逗号连接产生笛卡尔积（可能将 $0.02 的查询变成 $200 的查询）
- HIGH：`SELECT *` 强制全列扫描（宽表上浪费 30-90% 字节）
- HIGH：前导通配符 `LIKE '%signup%'` 使索引失效
- HIGH：`LOWER(event_name)` 使索引失效（非 SARGable）
- HIGH：`NOT IN (SELECT ...)` — NULL 语义陷阱
- MEDIUM：`SELECT DISTINCT` 去重开销
- MEDIUM：`ORDER BY` 无 `LIMIT` 对全量结果排序

### 示例 2：一个干净、SARGable 的查询

```sql
-- This scores 90+/100 (grade A) — no findings
SELECT id, email, created_at
FROM users
WHERE created_at >= TIMESTAMP '2026-01-01'
  AND created_at <  TIMESTAMP '2026-02-01'
ORDER BY id
LIMIT 100;
```

## 20 条规则（规则集 v1.0.0）

| 规则 | 严重程度 | 捕获内容 |
|---|---|---|
| SQL001 | high | `SELECT *` 全列扫描 |
| SQL002 | critical | 无 `WHERE` → 全表扫描 |
| SQL003 | high | `LIKE '%term'` 非 SARGable |
| SQL004 | high | 列上使用函数导致索引失效 |
| SQL005 | critical | `CROSS JOIN` / 逗号连接 |
| SQL006 | medium | `SELECT DISTINCT` 去重开销 |
| SQL007 | medium | `ORDER BY` 无 `LIMIT` |
| SQL008 | high | `NOT IN (SELECT ...)` NULL 陷阱 |
| SQL009 | medium | 隐式类型转换 |
| SQL010 | low | 多个 `OR`（应使用 `IN`/`UNION`） |
| SQL011 | medium | 大规模 `COUNT(DISTINCT)`（应使用 HLL） |
| SQL012 | low | `LIMIT` 无 `ORDER BY` |
| SQL013 | medium | `SELECT` 中的标量子查询 |
| SQL014 | medium | 5 个以上 JOIN 的广播/溢出风险 |
| SQL015 | high | 事实表无分区过滤 |
| SQL017 | low | `SELECT` 中的字符串拼接 |
| SQL018 | medium | 窗口函数 `OVER ()` 无 `PARTITION` |
| SQL020 | critical | `DELETE`/`UPDATE` 无 `WHERE` |
| SQL021 | low | `EXISTS`/`IN` 中的 `SELECT *` |
| SQL022 | medium | `UNION` 与 `UNION ALL` 的区别 |

运行测试套件以验证每条规则对真实 SQL 是否触发：

```bash
cd scripts && node test.js   # 26 tests, zero dependencies
```

## 局限性

- 这是一个**静态**分析器。它检测的是 SQL *文本*中的反模式，不会读取查询计划、行数或账单。一条被标记的查询在 100 行的表上很便宜；同样的查询在十亿行的表上才是这些规则要防止的问题。
- 事实表启发式规则（SQL015）依据表*名*（`*_events`、`*_log`）判断，仅供参考，并非确定性结论。
- 它不会执行 SQL——在任何 `.sql` 文件上运行都是安全的。