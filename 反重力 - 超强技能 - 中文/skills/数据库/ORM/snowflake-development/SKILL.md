---
name: snowflake-development
description: "全面的 Snowflake 开发助手，涵盖 SQL 最佳实践、数据管道设计（Dynamic Tables、Streams、Tasks、Snowpipe）、Cortex AI 函数、Cortex Agents、Snowpark Python、dbt 集成、性能调优和安全加固。触发词：Snowflake开发、Snowflake SQL、数据管道、Dynamic Tables、Cortex AI、Snowpark Python、dbt on Snowflake、性能调优"
category: data-engineering
risk: safe
source: community
date_added: "2026-03-24"
---

# Snowflake 开发

你是一名 Snowflake 开发专家。在编写 SQL、构建数据管道、使用 Cortex AI 或在 Snowflake 上使用 Snowpark Python 时，应用以下规则。

## 使用场景
- 当用户需要 Snowflake SQL、数据管道、Cortex AI 或 Snowpark Python 方面的帮助时。
- 当你需要 Snowflake 专用的 dbt、性能调优或安全加固指导时。

## SQL 最佳实践

### 命名与风格

- 所有标识符使用 `snake_case`。避免使用双引号标识符——它们会创建需要持续加引号的区分大小写名称。
- 使用 CTE（`WITH` 子句）而非嵌套子查询。
- 使用 `CREATE OR REPLACE` 实现幂等 DDL。
- 使用显式列列表——生产环境中绝不使用 `SELECT *`（Snowflake 的列式存储仅扫描引用的列）。

### 存储过程——冒号前缀规则

在 SQL 存储过程（BEGIN...END 块）中，变量和参数在 SQL 语句内部**必须**使用冒号 `:` 前缀。不使用的话，Snowflake 会报"invalid identifier"错误。

错误写法：
```sql
CREATE PROCEDURE my_proc(p_id INT) RETURNS STRING LANGUAGE SQL AS
BEGIN
    LET result STRING;
    SELECT name INTO result FROM users WHERE id = p_id;
    RETURN result;
END;
```

正确写法：
```sql
CREATE PROCEDURE my_proc(p_id INT) RETURNS STRING LANGUAGE SQL AS
BEGIN
    LET result STRING;
    SELECT name INTO :result FROM users WHERE id = :p_id;
    RETURN result;
END;
```

### 半结构化数据

- VARIANT、OBJECT、ARRAY 用于 JSON/Avro/Parquet/ORC。
- 访问嵌套字段：`src:customer.name::STRING`。始终强制转换：`src:price::NUMBER(10,2)`。
- VARIANT null 与 SQL NULL：JSON 的 `null` 存储为 `"null"`。加载时使用 `STRIP_NULL_VALUE = TRUE`。
- 展平数组：`SELECT f.value:name::STRING FROM my_table, LATERAL FLATTEN(input => src:items) f;`

### MERGE 实现 Upsert

```sql
MERGE INTO target t USING source s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET t.name = s.name, t.updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN INSERT (id, name, updated_at) VALUES (s.id, s.name, CURRENT_TIMESTAMP());
```

## 数据管道

### 选择方案

| 方案 | 使用场景 |
|------|----------|
| Dynamic Tables | 声明式转换。**默认选择。** 定义查询，Snowflake 负责刷新。 |
| Streams + Tasks | 命令式 CDC。用于过程逻辑、存储过程调用。 |
| Snowpipe | 从 S3/GCS/Azure 持续加载文件。 |

### Dynamic Tables

```sql
CREATE OR REPLACE DYNAMIC TABLE cleaned_events
    TARGET_LAG = '5 minutes'
    WAREHOUSE = transform_wh
    AS
    SELECT event_id, event_type, user_id, event_timestamp
    FROM raw_events
    WHERE event_type IS NOT NULL;
```

关键规则：
- 逐级设置 `TARGET_LAG`：顶层更紧密，底层更宽松。
- 增量 DT **不能**依赖全量刷新 DT。
- `SELECT *` 在 schema 变更时会出错——使用显式列列表。
- 基表必须保持变更追踪启用。
- 视图不能位于两个 Dynamic Table 之间。

### Streams 和 Tasks

```sql
CREATE OR REPLACE STREAM raw_stream ON TABLE raw_events;

CREATE OR REPLACE TASK process_events
    WAREHOUSE = transform_wh
    SCHEDULE = 'USING CRON 0 */1 * * * America/Los_Angeles'
    WHEN SYSTEM$STREAM_HAS_DATA('raw_stream')
    AS INSERT INTO cleaned_events SELECT ... FROM raw_stream;

-- Tasks 默认处于 SUSPENDED 状态——必须手动恢复
ALTER TASK process_events RESUME;
```

## Cortex AI

### 函数参考

| 函数 | 用途 |
|------|------|
| `AI_COMPLETE` | LLM 补全（文本、图像、文档） |
| `AI_CLASSIFY` | 分类（最多 500 个标签） |
| `AI_FILTER` | 文本/图像的布尔过滤 |
| `AI_EXTRACT` | 从文本/图像/文档中结构化提取 |
| `AI_SENTIMENT` | 情感评分（-1 到 1） |
| `AI_PARSE_DOCUMENT` | OCR 或布局提取 |
| `AI_REDACT` | PII 脱敏 |

**已弃用（不要使用）：** `COMPLETE`、`CLASSIFY_TEXT`、`EXTRACT_ANSWER`、`PARSE_DOCUMENT`、`SUMMARIZE`、`TRANSLATE`、`SENTIMENT`、`EMBED_TEXT_768`。

### TO_FILE — 常见错误来源

Stage 路径和文件名是**分开的**参数：

```sql
-- 错误：TO_FILE('@stage/file.pdf')
-- 正确：
TO_FILE('@db.schema.mystage', 'invoice.pdf')
```

### 使用 AI_CLASSIFY 进行分类（而非 AI_COMPLETE）

```sql
SELECT AI_CLASSIFY(ticket_text,
    ['billing', 'technical', 'account']):labels[0]::VARCHAR AS category
FROM tickets;
```

### Cortex Agents

```sql
CREATE OR REPLACE AGENT my_db.my_schema.sales_agent
FROM SPECIFICATION $spec$
{
    "models": {"orchestration": "auto"},
    "instructions": {
        "orchestration": "You are SalesBot...",
        "response": "Be concise."
    },
    "tools": [{"tool_spec": {"type": "cortex_analyst_text_to_sql", "name": "Sales", "description": "Queries sales..."}}],
    "tool_resources": {"Sales": {"semantic_model_file": "@stage/model.yaml"}}
}
$spec$;
```

Agent 规则：
- 使用 `$spec$` 分隔符（而非 `$$`）。
- `models` 必须是对象，不能是数组。
- `tool_resources` 是独立的顶级对象，不能嵌套在 tools 内。
- 编辑规范中不要包含空值/null 值——会清空现有值。
- 工具描述是质量的第一要素。
- 不要直接修改生产环境的 Agent——先克隆。

## Snowpark Python

```python
from snowflake.snowpark import Session
import os

session = Session.builder.configs({
    "account": os.environ["SNOWFLAKE_ACCOUNT"],
    "user": os.environ["SNOWFLAKE_USER"],
    "password": os.environ["SNOWFLAKE_PASSWORD"],
    "role": "my_role", "warehouse": "my_wh",
    "database": "my_db", "schema": "my_schema"
}).create()
```

- 绝不硬编码凭据。
- DataFrame 是惰性的——在 `collect()`/`show()` 时执行。
- 不要在大型 DataFrame 上使用 `collect()`——在服务端处理。
- 批量/ML 工作负载使用**向量化 UDF**（比标量 UDF 快 10-100 倍）。

## dbt on Snowflake

Dynamic Table 物化（流式/近实时数据集市）：
```sql
{{ config(materialized='dynamic_table', snowflake_warehouse='transforming', target_lag='1 hour') }}
```

增量物化（大型事实表）：
```sql
{{ config(materialized='incremental', unique_key='event_id') }}
```

Snowflake 专用配置（可与任何物化方式组合）：
```sql
{{ config(transient=true, copy_grants=true, query_tag='team_daily') }}
```

- 不要在没有 `{% if is_incremental() %}` 保护的情况下使用 `{{ this }}`。
- 流式/近实时数据集市使用 `dynamic_table` 物化。

## 性能

- **Cluster keys**：仅用于多 TB 表，选择 WHERE/JOIN/GROUP BY 列。
- **Search Optimization**：`ALTER TABLE t ADD SEARCH OPTIMIZATION ON EQUALITY(col);`
- **Warehouse 规模**：从 X-Small 开始，按需扩展。`AUTO_SUSPEND = 60`，`AUTO_RESUME = TRUE`。
- **按工作负载分离 warehouse**。
- 先估算 AI 成本：`SELECT SUM(AI_COUNT_TOKENS('claude-4-sonnet', text)) FROM table;`

## 安全

- 遵循最小权限 RBAC。使用数据库角色进行对象级授权。
- 定期审计 ACCOUNTADMIN：`SHOW GRANTS OF ROLE ACCOUNTADMIN;`
- 使用网络策略进行 IP 白名单。
- 对 PII 列使用脱敏策略，对多租户隔离使用行访问策略。

## 常见错误模式

| 错误 | 原因 | 修复 |
|------|------|------|
| "Object does not exist" | 上下文错误或缺少授权 | 使用完整限定名称，检查授权 |
| 存储过程中"Invalid identifier" | 缺少冒号前缀 | 使用 `:variable_name` |
| "Numeric value not recognized" | VARIANT 未转换 | `src:field::NUMBER(10,2)` |
| Task 未运行 | 忘记恢复 | `ALTER TASK ... RESUME` |
| DT 刷新失败 | Schema 变更或追踪禁用 | 使用显式列，检查变更追踪 |

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
