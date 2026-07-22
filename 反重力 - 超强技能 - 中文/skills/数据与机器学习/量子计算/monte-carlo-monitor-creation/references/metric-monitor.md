# 指标监控器参考

构建 `createMetricMonitorMac` 工具调用的详细参考。

## 适用场景

涉及以下需求时使用指标监控器：

- 追踪行数随时间的变化
- 监控特定字段的空值率、唯一计数或其他统计指标
- 检测数值分布中的异常（均值、最大值、最小值、百分位数）
- 监控数据新鲜度（距上次行数变化的时间）
- 按维度分段指标（如按国家、状态）

---

## 必需参数

| 参数 | 类型 | 说明 |
|-----------|------|------|
| `name` | string | 监控器的唯一标识符。使用描述性 slug（如 `orders_null_check`）。 |
| `description` | string | 监控器检查内容的人类可读描述。 |
| `table` | string | 表 MCON（首选）或 `database:schema.table` 格式。非 MCON 时需同时传入 `warehouse`。 |
| `aggregate_time_field` | string | **必须是表中的真实时间戳/日期时间列。** 绝不猜测此值。 |
| `alert_conditions` | array | 告警条件对象列表（见下方告警条件）。 |

## 可选参数

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|------|
| `warehouse` | string | 自动解析 | 仓库名称或 UUID。`table` 非 MCON 时必需。 |
| `segment_fields` | array of string | 无 | 用于分组/分段指标的字段（如 `["country", "status"]`）。 |
| `aggregate_by` | string | `"day"` | 时间间隔：`"hour"`、`"day"`、`"week"`、`"month"`。 |
| `where_condition` | string | 无 | SQL WHERE 子句（不含 `WHERE` 关键字），用于在计算指标前过滤行。 |
| `interval_minutes` | int | 自动 | 调度间隔（分钟）。必须与 `aggregate_by` 兼容（见下方说明）。未指定时，工具默认为所选 `aggregate_by` 的最小有效间隔。 |
| `domain_id` | string (uuid) | 无 | 域 UUID（使用 `getDomains` 列出）。 |

---

## 调度与聚合兼容性

调度间隔必须与 `aggregate_by` 兼容。日聚合要求间隔为 1440 分钟（24 小时）的倍数，周聚合要求 10080 的倍数，以此类推。传入 `interval_minutes` 时确保满足此约束。省略时工具会选取合理默认值。

| `aggregate_by` | 最小 `interval_minutes` | 省略时默认值 |
|---|---|---|
| `hour` | 60 | 60 |
| `day` | 1440 | 1440 |
| `week` | 10080 | 10080 |
| `month` | 43200 | 43200 |

例如，要每隔一天运行日聚合监控器，传入 `aggregate_by: "day"` 和 `interval_minutes: 2880`。

---

## 选择时间戳字段

`aggregate_time_field` 是最关键的参数。它必须是表中包含时间戳或日期时间值的真实列。这是监控器创建失败的头号原因。

### 如何选择

1. 你应该已从 `getTable`（含 `include_fields: true`）获取了列名（在主技能步骤 2 中完成）。
2. 寻找名称暗示时间戳的列：`created_at`、`updated_at`、`modified_at`、`timestamp`、`event_timestamp`，或带 `_ts`、`_dt`、`_time` 后缀的列，以及 `date`、`datetime`。
3. 如果用户指定了某个字段，验证它是否存在于列列表中。
4. 如果恰好有一个明显候选项，建议使用它。
5. 如果有多个候选项，展示给用户选择。
6. 如果没有明显的时间戳列，建议改用自定义 SQL 监控器（不需要时间戳字段）。

**绝不**在未确认时间戳字段存在于表 Schema 中的情况下继续。

### 时间戳字段常见错误

- **使用 DATE 列（而非 TIMESTAMP）：** 可能可行，但聚合粒度受限。例如，在 DATE 列上使用 `aggregate_by: "hour"` 没有意义，因为时间部分始终是午夜。提醒用户并默认使用 `aggregate_by: "day"` 或更粗粒度。
- **使用包含大量空值的字段：** 如果时间戳列有大量空值，空时间戳的行会被排除在聚合窗口之外，产生不可靠或误导性结果。从 `getTable` 字段统计中检查列的空值率（如有），空值率高时提醒用户。
- **猜测不存在的字段名：** 始终对照 `getTable` 输出验证列名。拼写错误或假设的名称（如实际列是 `created_at` 却用了 `created_date`）会导致监控器创建静默失败或报错。

---

## 字段类型与指标兼容性矩阵

**选择指标前，从 `getTable` 结果检查列的数据类型。** 传入与列类型不兼容的指标是时间戳问题之后最常见的创建失败原因。

| 列类型 | 兼容指标 |
|-------------|-------------------|
| **数值型**（int、float、decimal、bigint） | `NUMERIC_MEAN`、`NUMERIC_MEDIAN`、`NUMERIC_MIN`、`NUMERIC_MAX`、`NUMERIC_STDDEV`、`SUM`、`ZERO_COUNT`、`ZERO_RATE`、`NEGATIVE_COUNT`、`NEGATIVE_RATE`、`NULL_COUNT`、`NULL_RATE`、`UNIQUE_COUNT`、`UNIQUE_RATE`、`DUPLICATE_COUNT` |
| **字符串/文本**（varchar、char、text） | `TEXT_MAX_LENGTH`、`TEXT_MIN_LENGTH`、`TEXT_MEAN_LENGTH`、`TEXT_INT_RATE`、`TEXT_NUMBER_RATE`、`TEXT_UUID_RATE`、`TEXT_EMAIL_ADDRESS_RATE`、`EMPTY_STRING_COUNT`、`EMPTY_STRING_RATE`、`NULL_COUNT`、`NULL_RATE`、`UNIQUE_COUNT`、`UNIQUE_RATE`、`DUPLICATE_COUNT` |
| **布尔型** | `TRUE_COUNT`、`FALSE_COUNT`、`NULL_COUNT`、`NULL_RATE` |
| **时间戳/日期** | `FUTURE_TIMESTAMP_COUNT`、`PAST_TIMESTAMP_COUNT`、`UNIX_ZERO_TIMESTAMP_COUNT`、`NULL_COUNT`、`NULL_RATE`、`UNIQUE_COUNT`、`UNIQUE_RATE` |
| **任意类型** | `NULL_COUNT`、`NULL_RATE`、`UNIQUE_COUNT`、`UNIQUE_RATE`、`DUPLICATE_COUNT` |

### 规则

- **绝不**对字符串、布尔或时间戳列应用 `NUMERIC_*`、`SUM`、`ZERO_*` 或 `NEGATIVE_*` 指标。
- **绝不**对数值、布尔或时间戳列应用 `TEXT_*` 或 `EMPTY_STRING_*` 指标。
- **绝不**对非布尔列应用 `TRUE_COUNT` 或 `FALSE_COUNT`。
- **绝不**对非时间戳列应用 `FUTURE_TIMESTAMP_COUNT`、`PAST_TIMESTAMP_COUNT` 或 `UNIX_ZERO_TIMESTAMP_COUNT`。
- 不确定时，`NULL_COUNT`、`NULL_RATE`、`UNIQUE_COUNT` 和 `UNIQUE_RATE` 对任何列类型都安全。

---

## 告警条件

每个告警条件包含：

| 字段 | 类型 | 必需 | 说明 |
|-------|------|----------|------|
| `metric` | string | 是 | 要监控的指标（见下方指标参考）。 |
| `operator` | string | 是 | `"AUTO"`（异常检测）、`"GT"`、`"LT"`、`"EQ"`、`"GTE"`、`"LTE"`、`"NE"`。 |
| `threshold` | number | 显式操作符时 | 阈值。使用 `GT`、`LT`、`EQ`、`GTE`、`LTE` 或 `NE` 时必需。`AUTO` 时不使用。 |
| `fields` | array of string | 视情况 | 应用指标的列名。字段级指标必需。表级指标不需要。 |

---

## 操作符指南

### 何时使用 `AUTO`（异常检测）

- 不了解值的预期范围，希望 Monte Carlo 的 ML 学习正常模式并对偏差告警时最佳。
- 适用于自然波动的指标（行数、演进数据的空值率、数值分布）。
- 某些指标**要求**使用 `AUTO`——见下表。

### 何时使用显式阈值（`GT`、`LT`、`EQ`、`GTE`、`LTE`、`NE`）

- 存在已知业务规则或数据契约时使用（如"`email` 的空值率绝不应超过 5%"、"订单金额必须始终大于 0"）。
- 提供确定性告警——无需训练期，条件满足时立即触发。
- 告警条件中需要 `threshold` 值。

### 指标的操作符限制

| 指标 | 允许的操作符 | 说明 |
|--------|-------------------|-------|
| `ROW_COUNT_CHANGE` | 仅 `AUTO` | 行数增量的异常检测。 |
| `TIME_SINCE_LAST_ROW_COUNT_CHANGE` | 仅 `AUTO` | 停滞时长的异常检测。 |
| `RELATIVE_ROW_COUNT` | 仅 `AUTO` | 分段分布的异常检测。需要 `segment_fields`。 |
| 所有其他指标 | `AUTO`、`GT`、`LT`、`EQ`、`GTE`、`LTE`、`NE` | 任何操作符都有效。 |

---

## 指标参考

### 表级指标（不需要 `fields`）

| 指标 | 操作符 | 说明 |
|--------|----------|------|
| `ROW_COUNT_CHANGE` | 必须使用 `AUTO` | 总行数异常变化告警。 |
| `TIME_SINCE_LAST_ROW_COUNT_CHANGE` | 必须使用 `AUTO` | 表未更新异常时长告警。 |

### 字段级指标（必须指定 `fields`）

| 指标 | 列类型 | 说明 |
|--------|-------------|------|
| `NULL_COUNT` | 任意 | 空值计数。 |
| `NULL_RATE` | 任意 | 空值率（0.0 到 1.0）。 |
| `UNIQUE_COUNT` | 任意 | 不同值计数。 |
| `UNIQUE_RATE` | 任意 | 不同值率（0.0 到 1.0）。 |
| `DUPLICATE_COUNT` | 任意 | 重复（非唯一）值计数。 |
| `EMPTY_STRING_COUNT` | 字符串/文本 | 空字符串值计数。 |
| `EMPTY_STRING_RATE` | 字符串/文本 | 空字符串值率。 |
| `NUMERIC_MEAN` | 数值 | 数值字段的均值。 |
| `NUMERIC_MEDIAN` | 数值 | 数值字段的中位数。 |
| `NUMERIC_MIN` | 数值 | 数值字段的最小值。 |
| `NUMERIC_MAX` | 数值 | 数值字段的最大值。 |
| `NUMERIC_STDDEV` | 数值 | 数值字段的标准差。 |
| `SUM` | 数值 | 数值字段的总和。 |
| `ZERO_COUNT` | 数值 | 零值计数。 |
| `ZERO_RATE` | 数值 | 零值率。 |
| `NEGATIVE_COUNT` | 数值 | 负值计数。 |
| `NEGATIVE_RATE` | 数值 | 负值率。 |
| `TRUE_COUNT` | 布尔 | true 值计数。 |
| `FALSE_COUNT` | 布尔 | false 值计数。 |
| `TEXT_MAX_LENGTH` | 字符串/文本 | 最大字符串长度。 |
| `TEXT_MIN_LENGTH` | 字符串/文本 | 最小字符串长度。 |
| `TEXT_MEAN_LENGTH` | 字符串/文本 | 平均字符串长度。 |
| `TEXT_INT_RATE` | 字符串/文本 | 可解析为整数的值比率。 |
| `TEXT_NUMBER_RATE` | 字符串/文本 | 可解析为数字的值比率。 |
| `TEXT_UUID_RATE` | 字符串/文本 | 匹配 UUID 格式的值比率。 |
| `TEXT_EMAIL_ADDRESS_RATE` | 字符串/文本 | 匹配邮箱格式的值比率。 |
| `FUTURE_TIMESTAMP_COUNT` | 时间戳/日期 | 未来时间戳计数。 |
| `PAST_TIMESTAMP_COUNT` | 时间戳/日期 | 过于久远的过去时间戳计数。 |
| `UNIX_ZERO_TIMESTAMP_COUNT` | 时间戳/日期 | 等于 Unix 纪元零点（1970-01-01）的时间戳计数。 |

### 分段指标

| 指标 | 操作符 | 说明 |
|--------|----------|------|
| `RELATIVE_ROW_COUNT` | 必须使用 `AUTO` | 跨分段分布异常变化告警。必须使用 `segment_fields`。 |

---

## 示例

### 行数异常检测

```json
{
  "name": "orders_row_count",
  "description": "Detect anomalous changes in daily order volume",
  "table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++analytics:core.orders",
  "aggregate_time_field": "created_at",
  "aggregate_by": "day",
  "alert_conditions": [
    {
      "metric": "ROW_COUNT_CHANGE",
      "operator": "AUTO"
    }
  ]
}
```

### 特定字段的空值监控

```json
{
  "name": "orders_null_check",
  "description": "Alert when email or user_id nulls exceed 50 per day",
  "table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++analytics:core.orders",
  "aggregate_time_field": "created_at",
  "aggregate_by": "day",
  "alert_conditions": [
    {
      "metric": "NULL_COUNT",
      "operator": "GT",
      "threshold": 50,
      "fields": ["email", "user_id"]
    }
  ]
}
```

### 分段监控

```json
{
  "name": "orders_by_country_distribution",
  "description": "Detect anomalous shifts in order distribution across countries",
  "table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++analytics:core.orders",
  "aggregate_time_field": "created_at",
  "aggregate_by": "day",
  "segment_fields": ["country"],
  "alert_conditions": [
    {
      "metric": "RELATIVE_ROW_COUNT",
      "operator": "AUTO"
    }
  ]
}
```

### 带过滤的数值范围监控

```json
{
  "name": "completed_orders_amount_check",
  "description": "Detect anomalous max order amounts for completed orders",
  "table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++analytics:core.orders",
  "aggregate_time_field": "created_at",
  "aggregate_by": "day",
  "where_condition": "status = 'completed'",
  "alert_conditions": [
    {
      "metric": "NUMERIC_MAX",
      "operator": "AUTO",
      "fields": ["amount"]
    }
  ]
}
```

### 单监控器多告警条件

```json
{
  "name": "payments_quality_check",
  "description": "Monitor payment amount stats and null rate on transaction_id",
  "table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++warehouse:billing.payments",
  "aggregate_time_field": "processed_at",
  "aggregate_by": "day",
  "domain_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "alert_conditions": [
    {
      "metric": "NUMERIC_MEAN",
      "operator": "AUTO",
      "fields": ["amount"]
    },
    {
      "metric": "NULL_RATE",
      "operator": "GT",
      "threshold": 0.01,
      "fields": ["transaction_id"]
    }
  ]
}
```
