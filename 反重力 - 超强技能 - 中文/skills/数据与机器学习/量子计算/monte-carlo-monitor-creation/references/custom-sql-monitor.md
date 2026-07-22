# 自定义 SQL 监控器参考

构建 `createCustomSqlMonitorMac` 工具调用的详细参考。

## 适用场景

涉及以下需求时使用自定义 SQL 监控器：

- 运行特定 SQL 查询并对其结果告警
- 实现跨表逻辑（JOIN、子查询、CTE）
- 应用无法映射到单一指标的业务特定聚合或计算
- 监控跨多列或多表的条件
- 使用已有的 SQL 查询

---

## 通用兜底方案

自定义 SQL 是兜底监控器类型。当其他监控器类型无法表达用户需求时使用：

- **验证监控器不适用**，因为列尚不存在，或逻辑需要跨表 JOIN。
- **指标监控器无法表达业务逻辑**——例如两列之间的比率、条件聚合或跨多表的计算。
- **需要跨表 JOIN**——指标和验证监控器只能操作单表。如果检查需要两张或更多表的数据，自定义 SQL 是唯一选择。
- **用户已有 SQL 查询**——不要强行套入其他监控器类型。用自定义 SQL 监控器包装即可。

如果发现自己在扭曲其他监控器类型来适应用户意图，停下来改用自定义 SQL。

---

## 必需参数

| 参数 | 类型 | 说明 |
|-----------|------|------|
| `name` | string | 监控器的唯一标识符。使用描述性 slug（如 `orphan_orders_check`）。 |
| `description` | string | 监控器检查内容的人类可读描述。 |
| `warehouse` | string | 执行 SQL 查询的仓库名称或 UUID。 |
| `sql` | string | 返回**单个数值**（一行一列）的 SQL 查询。 |
| `alert_conditions` | array | 阈值条件列表（见下方告警条件）。 |

## 可选参数

| 参数 | 类型 | 说明 |
|-----------|------|------|
| `domain_id` | string (uuid) | 域 UUID（使用 `getDomains` 列出）。每个监控器只能分配一个域。 |

---

## 告警条件

每个告警条件将查询结果与阈值比较。

| 字段 | 类型 | 必需 | 说明 |
|-------|------|----------|------|
| `operator` | string | 是 | `"GT"`、`"LT"`、`"EQ"`、`"GTE"`、`"LTE"`、`"NE"` |
| `thresholdValue` | number | 是 | 用于比较查询结果的数值阈值。 |

### 不支持 AUTO

自定义 SQL 监控器**不支持** `AUTO`（异常检测）。每个告警条件必须指定显式操作符和阈值。这是常见错误——如果用户需要异常检测，引导他们使用指标监控器，它支持 `AUTO`。

如果用户不确定设什么阈值，帮助他们推理："什么值表示有问题？如果查询返回 X，是否应该触发告警？"

---

## SQL 查询要求

SQL 查询必须返回恰好**一行一列的数值**。这是不可协商的——监控器将该单个值与告警条件比较。

### 规则

- 使用聚合函数：`COUNT(*)`、`SUM()`、`AVG()`、`MAX()`、`MIN()` 或类似函数。
- 可以引用仓库中可访问的任何表、视图或物化视图。
- 可以使用 JOIN、子查询、CTE、窗口函数——任何有效 SQL。
- **不要**包含末尾分号。
- **不要**包含注释（`--` 或 `/* */`）——某些仓库会不一致地剥离它们。

### SQL 验证要点

这些是导致自定义 SQL 监控器失败或产生误导结果的最常见错误：

1. **用 COALESCE 处理 NULL。** 如果聚合可能返回 NULL（如空结果集上的 `SUM(amount)`），包装它：`SELECT COALESCE(SUM(amount), 0) FROM ...`。NULL 结果无法与阈值比较，不会触发告警。

2. **确保恰好一行一列。** 如果查询可能返回零行（如无 `GROUP BY` 的过滤 `SELECT`），用外层聚合包装：`SELECT COUNT(*) FROM (SELECT ...) sub`。如果返回多列，只选择需要的那个。

3. **在脑中测试查询。** 最终确定前问自己："如果这个查询返回 5，告警条件会正确触发吗？"用具体数字走一遍逻辑。

4. **对于时间窗口检查，使用适当的日期函数。** 日期运算的 SQL 语法因仓库而异（见下方仓库特定 SQL 说明）。始终限定时间窗口以避免扫描整个表历史。

5. **避免非确定性结果。** 使用不带 `ORDER BY` 的 `LIMIT`，或 `RANDOM()`，会产生不可预测的结果，使告警不可靠。

---

## 仓库特定 SQL 说明

日期运算和函数的 SQL 语法因仓库而异。编写时间窗口查询时，使用用户仓库的正确语法：

| 操作 | Snowflake | BigQuery | Redshift |
|-----------|-----------|----------|----------|
| 当前时间减 1 天 | `DATEADD(day, -1, CURRENT_TIMESTAMP())` | `DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)` | `DATEADD(day, -1, GETDATE())` |
| 当前时间减 1 小时 | `DATEADD(hour, -1, CURRENT_TIMESTAMP())` | `TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)` | `DATEADD(hour, -1, GETDATE())` |
| 当前时间戳 | `CURRENT_TIMESTAMP()` | `CURRENT_TIMESTAMP()` | `GETDATE()` |
| 日期截断 | `DATE_TRUNC('day', col)` | `DATE_TRUNC(col, DAY)` | `DATE_TRUNC('day', col)` |

不确定用户使用哪个仓库时，直接询问。语法错误会导致监控器在每次调度运行时失败。

---

## 示例

### 孤立记录（GT 0）

订单引用了不存在的客户时告警。

```json
{
  "name": "orphan_orders_check",
  "description": "Detect orders referencing non-existent customers",
  "warehouse": "production_snowflake",
  "sql": "SELECT COUNT(*) FROM analytics.core.orders o LEFT JOIN analytics.core.customers c ON o.customer_id = c.id WHERE c.id IS NULL",
  "alert_conditions": [
    {
      "operator": "GT",
      "thresholdValue": 0
    }
  ]
}
```

### 每日收入下限（LT 阈值）

过去 24 小时总收入低于最低值时告警。

```json
{
  "name": "daily_revenue_floor",
  "description": "Alert when daily revenue falls below $10,000",
  "warehouse": "production_snowflake",
  "sql": "SELECT COALESCE(SUM(amount), 0) FROM analytics.billing.transactions WHERE created_at >= DATEADD(day, -1, CURRENT_TIMESTAMP())",
  "alert_conditions": [
    {
      "operator": "LT",
      "thresholdValue": 10000
    }
  ]
}
```

### 重复率超阈值

关键字段重复率超过 1% 时告警。

```json
{
  "name": "order_id_duplicate_rate",
  "description": "Alert when order_id duplicate rate exceeds 1%",
  "warehouse": "production_snowflake",
  "sql": "SELECT COALESCE(1.0 - (COUNT(DISTINCT order_id) * 1.0 / NULLIF(COUNT(*), 0)), 0) FROM analytics.core.orders WHERE created_at >= DATEADD(day, -1, CURRENT_TIMESTAMP())",
  "alert_conditions": [
    {
      "operator": "GT",
      "thresholdValue": 0.01
    }
  ]
}
```

### 多阈值条件（范围检查）

值超出可接受范围时告警。多个条件作为独立检查——每个评估为 true 的条件触发各自的告警。

```json
{
  "name": "avg_order_amount_range",
  "description": "Alert when average order amount is outside the $20-$500 range",
  "warehouse": "production_snowflake",
  "sql": "SELECT COALESCE(AVG(amount), 0) FROM analytics.core.orders WHERE created_at >= DATEADD(day, -1, CURRENT_TIMESTAMP()) AND status = 'completed'",
  "alert_conditions": [
    {
      "operator": "LT",
      "thresholdValue": 20
    },
    {
      "operator": "GT",
      "thresholdValue": 500
    }
  ]
}
```

### 跨表新鲜度检查（BigQuery 语法）

下游表最新行落后源表超过 2 小时时告警。

```json
{
  "name": "pipeline_lag_check",
  "description": "Alert when downstream table lags source by more than 2 hours",
  "warehouse": "production_bigquery",
  "sql": "SELECT COALESCE(TIMESTAMP_DIFF(s.max_ts, t.max_ts, MINUTE), 9999) FROM (SELECT MAX(event_timestamp) AS max_ts FROM project.raw.events) s CROSS JOIN (SELECT MAX(processed_at) AS max_ts FROM project.analytics.events_processed) t",
  "alert_conditions": [
    {
      "operator": "GT",
      "thresholdValue": 120
    }
  ]
}
```
