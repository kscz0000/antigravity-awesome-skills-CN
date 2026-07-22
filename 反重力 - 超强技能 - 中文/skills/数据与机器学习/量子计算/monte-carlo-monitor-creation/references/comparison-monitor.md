# 比较监控器参考

构建 `createComparisonMonitorMac` 工具调用的详细参考。

## 适用场景

涉及以下需求时使用比较监控器：

- 比较两张表之间的数据（如源表 vs 目标表、开发环境 vs 生产环境）
- 验证迁移或复制后的数据一致性
- 检查跨环境的行数对等性
- 比较表之间的字段级指标（空值计数、总和、分布）

---

## 前置步骤：验证两张表和字段

在构建告警条件前，必须验证两张表都存在且引用的字段是真实列。这是比较监控器失败的最常见原因。

1. **解析两个 MCON。** 使用 `search` 查找源表和目标表。如果用户提供了 `database:schema.table` 格式，分别搜索获取 MCON。
2. **获取完整 Schema。** 对源表和目标表都调用 `getTable` 并传入 `include_fields: true`。需要两边的列列表。
3. **对于字段级指标，验证字段在两侧都存在。** 确认 `sourceField` 存在于源表的列列表中，且 `targetField` 存在于目标表的列列表中。字段名在大多数仓库中区分大小写。
4. **检查字段类型兼容性。** 指标必须与两侧的列类型兼容。例如，`NUMERIC_MEAN` 要求源表和目标表都是数值列。如果源列是数值型但目标列是字符串，比较将失败。
5. 如果任何字段不存在或类型不兼容，停下来请用户澄清。不要猜测。

---

## 必需参数

| 参数 | 类型 | 说明 |
|-----------|------|------|
| `name` | string | 监控器的唯一标识符。使用描述性 slug（如 `orders_dev_prod_compare`）。 |
| `description` | string | 监控器检查内容的人类可读描述。 |
| `source_table` | string | 源表 MCON（首选）或 `database:schema.table` 格式。非 MCON 时需同时传入 `source_warehouse`。 |
| `target_table` | string | 目标表 MCON（首选）或 `database:schema.table` 格式。非 MCON 时需同时传入 `target_warehouse`。 |
| `alert_conditions` | array | 比较条件列表（见下方告警条件）。 |

## 可选参数

| 参数 | 类型 | 说明 |
|-----------|------|------|
| `source_warehouse` | string | 源表的仓库名称或 UUID。`source_table` 非 MCON 时必需。 |
| `target_warehouse` | string | 目标表的仓库名称或 UUID。`target_table` 非 MCON 时必需。 |
| `segment_fields` | array of string | 用于分段比较的字段。必须在两张表中都存在且名称相同。 |
| `domain_id` | string (uuid) | 域 UUID（使用 `getDomains` 列出）。每个监控器只能分配一个域。 |

---

## 跨仓库比较

当源表和目标表位于不同仓库时（如比较 Snowflake 的暂存表与 BigQuery 的生产表），必须显式提供 `source_warehouse` 和 `target_warehouse`。当表在不同环境中时，工具无法自动解析仓库。

即使两个表都是 MCON，如果它们属于不同仓库，也要传入两个仓库参数以确保安全。在跨仓库场景中省略它们会导致静默失败或不正确的结果。

常见跨仓库模式：
- **开发 vs 生产：** 同类型仓库，不同数据库或 Schema
- **迁移验证：** 源在旧仓库，目标在新仓库
- **复制检查：** 主仓库 vs 副本或下游仓库

---

## 告警条件

每个条件比较源表和目标表之间的一个指标。

| 字段 | 类型 | 必需 | 说明 |
|-------|------|----------|------|
| `metric` | string | 是 | 要比较的指标（见下方指标参考）。 |
| `sourceField` | string | 字段级指标必需 | 源表中的列。除 `ROW_COUNT` 外的所有指标都必需。 |
| `targetField` | string | 字段级指标必需 | 目标表中的列。除 `ROW_COUNT` 外的所有指标都必需。 |
| `thresholdValue` | number | 否 | 源和目标之间可接受差异的阈值。 |
| `isThresholdRelative` | boolean | 否 | `false` = 绝对差异（默认），`true` = 百分比差异。 |
| `customMetric` | object | 否 | 源和目标的自定义 SQL 表达式（见下方自定义指标）。 |

---

## ROW_COUNT 与字段：关键规则

> **使用 `ROW_COUNT` 指标时绝不要传入 `sourceField` 或 `targetField`。**

`ROW_COUNT` 是表级指标——它计算表中的所有行数，而非列中的值。传入字段名会导致 API 调用失败或产生意外行为。

这是比较监控器中最常见的错误。在提交任何包含 `ROW_COUNT` 的告警条件前，验证 `sourceField` 和 `targetField` 都不在条件对象中。

| 指标 | 需要字段？ | 传入字段会怎样？ |
|--------|---------------|----------------------------------|
| `ROW_COUNT` | **否——绝不传入字段** | API 错误或未定义行为 |
| 所有其他指标 | **是——始终传入两个字段** | 比较工作所必需 |

---

## 指标参考

### 表级指标（不需要字段）

| 指标 | 说明 |
|--------|------|
| `ROW_COUNT` | 比较源和目标的总行数。 |

### 字段级指标（需要 `sourceField` 和 `targetField`）

#### 唯一性和重复

| 指标 | 说明 |
|--------|------|
| `UNIQUE_COUNT` | 不同值的计数。 |
| `DUPLICATE_COUNT` | 重复（非唯一）值的计数。 |
| `APPROX_DISTINCT_COUNT` | 近似不同值计数（大表上更快）。 |

#### 空值和空字符串检查

| 指标 | 说明 |
|--------|------|
| `NULL_COUNT` | 空值计数。 |
| `NON_NULL_COUNT` | 非空值计数。 |
| `EMPTY_STRING_COUNT` | 空字符串值计数。 |
| `TEXT_ALL_SPACES_COUNT` | 全为空白字符的值计数。 |
| `NAN_COUNT` | NaN 值计数。 |
| `TEXT_NULL_KEYWORD_COUNT` | 包含类空值关键词（如"NULL"、"None"）的值计数。 |

#### 数值统计

| 指标 | 说明 |
|--------|------|
| `NUMERIC_MEAN` | 数值字段的均值。 |
| `NUMERIC_MEDIAN` | 数值字段的中位数。 |
| `NUMERIC_MIN` | 最小值。 |
| `NUMERIC_MAX` | 最大值。 |
| `NUMERIC_STDDEV` | 标准差。 |
| `SUM` | 数值字段的总和。 |
| `ZERO_COUNT` | 零值计数。 |
| `NEGATIVE_COUNT` | 负值计数。 |

#### 百分位数

| 指标 | 说明 |
|--------|------|
| `PERCENTILE_20` | 第 20 百分位值。 |
| `PERCENTILE_40` | 第 40 百分位值。 |
| `PERCENTILE_60` | 第 60 百分位值。 |
| `PERCENTILE_80` | 第 80 百分位值。 |

#### 文本统计

| 指标 | 说明 |
|--------|------|
| `TEXT_MAX_LENGTH` | 最大字符串长度。 |
| `TEXT_MIN_LENGTH` | 最小字符串长度。 |
| `TEXT_MEAN_LENGTH` | 平均字符串长度。 |
| `TEXT_STD_LENGTH` | 字符串长度的标准差。 |

#### 文本格式检查

| 指标 | 说明 |
|--------|------|
| `TEXT_NOT_INT_COUNT` | 无法解析为整数的值计数。 |
| `TEXT_NOT_NUMBER_COUNT` | 无法解析为数字的值计数。 |
| `TEXT_NOT_UUID_COUNT` | 不匹配 UUID 格式的值计数。 |
| `TEXT_NOT_SSN_COUNT` | 不匹配 SSN 格式的值计数。 |
| `TEXT_NOT_US_PHONE_COUNT` | 不匹配美国电话格式的值计数。 |
| `TEXT_NOT_US_STATE_CODE_COUNT` | 不匹配美国州代码的值计数。 |
| `TEXT_NOT_US_ZIP_CODE_COUNT` | 不匹配美国邮编的值计数。 |
| `TEXT_NOT_EMAIL_ADDRESS_COUNT` | 不匹配邮箱格式的值计数。 |
| `TEXT_NOT_TIMESTAMP_COUNT` | 无法解析为时间戳的值计数。 |

#### 布尔值

| 指标 | 说明 |
|--------|------|
| `TRUE_COUNT` | true 值计数。 |
| `FALSE_COUNT` | false 值计数。 |

#### 时间戳

| 指标 | 说明 |
|--------|------|
| `FUTURE_TIMESTAMP_COUNT` | 未来时间戳计数。 |
| `PAST_TIMESTAMP_COUNT` | 过于久远的过去时间戳计数。 |
| `UNIX_ZERO_COUNT` | 等于 Unix 纪元零点（1970-01-01）的时间戳计数。 |

---

## 选择正确的指标

| 用户意图 | 正确指标 | 需要字段？ |
|-------------|---------------|----------------|
| 行数对等 | `ROW_COUNT` | **否**——绝不传入字段 |
| 列中的不同值 | `UNIQUE_COUNT` | 是 |
| 列中的空值 | `NULL_COUNT` | 是 |
| 总和、平均值、最小值、最大值 | `SUM`、`NUMERIC_MEAN`、`NUMERIC_MIN`、`NUMERIC_MAX` | 是 |
| 数据完整性 | `NON_NULL_COUNT` | 是 |
| 字符串格式验证 | `TEXT_NOT_EMAIL_ADDRESS_COUNT`、`TEXT_NOT_UUID_COUNT` 等 | 是 |
| 自定义计算表达式 | 使用 `customMetric` 而非 `metric` | 否（由 SQL 处理） |

---

## 自定义指标

以下情况使用自定义指标：

- **列名不同**，需要计算表达式（而非直接字段比较）。
- **需要派生计算**，如 `SUM(quantity * unit_price)` 而非简单列指标。
- **标准指标无法覆盖比较**（如比较比率、条件聚合或窗口计算）。

如果列只是名称不同但想使用标准指标（如比较源表的 `revenue` SUM 与目标表的 `total_revenue`），不需要自定义指标——只需使用标准指标并设置不同的 `sourceField` 和 `targetField` 值。

自定义指标结构：

```json
{
  "customMetric": {
    "displayName": "Revenue Sum",
    "sourceSqlExpression": "SUM(revenue)",
    "targetSqlExpression": "SUM(total_revenue)"
  }
}
```

| 字段 | 类型 | 必需 | 说明 |
|-------|------|----------|------|
| `displayName` | string | 是 | 告警和仪表板中指标的人类可读名称。 |
| `sourceSqlExpression` | string | 是 | 对源表求值的 SQL 表达式。 |
| `targetSqlExpression` | string | 是 | 对目标表求值的 SQL 表达式。 |

使用 `customMetric` 时，不要在同一告警条件中同时传入 `metric`、`sourceField` 或 `targetField`。自定义指标替代了所有这些。

---

## 阈值指南

### 绝对阈值（`isThresholdRelative: false` 或省略）

`thresholdValue` 是源和目标指标值之间可接受的最大绝对差异。

- `thresholdValue: 0` —— 源和目标必须完全匹配。
- `thresholdValue: 100` —— 最多 100 个单位的差异可接受。

### 相对（百分比）阈值（`isThresholdRelative: true`）

`thresholdValue` 是可接受的最大百分比差异。

- `thresholdValue: 5` —— 最多 5% 的差异可接受。
- `thresholdValue: 0.1` —— 最多 0.1% 的差异可接受。

### 何时使用哪种

| 场景 | 推荐阈值类型 |
|----------|---------------------------|
| 精确复制（行数必须匹配） | 绝对，`thresholdValue: 0` |
| 近实时同步（有小延迟） | 绝对，小值（如 10-100） |
| 不同规模的表 | 相对，百分比 |
| 聚合指标（总和、均值） | 相对，处理浮点差异 |

---

## 示例

### 行数对等（绝对阈值）

比较开发和生产的行数，差异超过 100 行时告警。

```json
{
  "name": "orders_dev_prod_row_count",
  "description": "Verify dev and prod orders tables have similar row counts",
  "source_table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++dev_warehouse:core.orders",
  "target_table": "MCON++b2c3d4e5-f6a7-8901-bcde-f12345678901++1++1++prod_warehouse:core.orders",
  "alert_conditions": [
    {
      "metric": "ROW_COUNT",
      "thresholdValue": 100,
      "isThresholdRelative": false
    }
  ]
}
```

注意：没有 `sourceField` 或 `targetField`——`ROW_COUNT` 是表级的。

### 行数对等（百分比阈值）

行数差异超过 5% 时告警。

```json
{
  "name": "orders_replication_check",
  "description": "Verify replicated orders table is within 5% of source row count",
  "source_table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++primary:sales.orders",
  "target_table": "MCON++b2c3d4e5-f6a7-8901-bcde-f12345678901++1++1++replica:sales.orders",
  "alert_conditions": [
    {
      "metric": "ROW_COUNT",
      "thresholdValue": 5,
      "isThresholdRelative": true
    }
  ]
}
```

### 字段级比较（不同列名）

比较源表的 `revenue` 总和与目标表的 `total_revenue`。

```json
{
  "name": "revenue_source_target_sum",
  "description": "Verify revenue sums match between staging and production",
  "source_table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++staging:finance.transactions",
  "target_table": "MCON++b2c3d4e5-f6a7-8901-bcde-f12345678901++1++1++production:finance.transactions",
  "alert_conditions": [
    {
      "metric": "SUM",
      "sourceField": "revenue",
      "targetField": "total_revenue",
      "thresholdValue": 1,
      "isThresholdRelative": true
    }
  ]
}
```

### 分段比较

比较源和目标之间 `email` 的空值计数，按 `country` 分段。`country` 字段必须在两张表中都存在。

```json
{
  "name": "email_nulls_by_country",
  "description": "Compare email null counts by country between ETL source and target",
  "source_table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++raw:crm.contacts",
  "target_table": "MCON++b2c3d4e5-f6a7-8901-bcde-f12345678901++1++1++analytics:crm.contacts",
  "segment_fields": ["country"],
  "alert_conditions": [
    {
      "metric": "NULL_COUNT",
      "sourceField": "email",
      "targetField": "email",
      "thresholdValue": 0,
      "isThresholdRelative": false
    }
  ]
}
```

### 跨仓库比较（显式仓库）

源和目标在不同仓库时，必须提供两个仓库参数。

```json
{
  "name": "migration_users_row_count",
  "description": "Validate user row counts match after Snowflake to BigQuery migration",
  "source_table": "snowflake_db:public.users",
  "source_warehouse": "snowflake-prod",
  "target_table": "bigquery_project:public.users",
  "target_warehouse": "bigquery-prod",
  "alert_conditions": [
    {
      "metric": "ROW_COUNT",
      "thresholdValue": 0,
      "isThresholdRelative": false
    }
  ]
}
```

### 自定义指标比较

当源和目标之间的 SQL 不同时，比较计算的收入表达式。

```json
{
  "name": "computed_revenue_compare",
  "description": "Compare total revenue computation between legacy and new schema",
  "source_table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++warehouse:legacy.orders",
  "target_table": "MCON++b2c3d4e5-f6a7-8901-bcde-f12345678901++1++1++warehouse:v2.orders",
  "alert_conditions": [
    {
      "customMetric": {
        "displayName": "Total Revenue",
        "sourceSqlExpression": "SUM(quantity * unit_price)",
        "targetSqlExpression": "SUM(total_amount)"
      },
      "thresholdValue": 0.01,
      "isThresholdRelative": true
    }
  ]
}
```

### 多个告警条件

在单个监控器中同时比较行数和字段级指标。

```json
{
  "name": "orders_full_comparison",
  "description": "Full comparison of orders between staging and production",
  "source_table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++staging:core.orders",
  "target_table": "MCON++b2c3d4e5-f6a7-8901-bcde-f12345678901++1++1++production:core.orders",
  "domain_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "alert_conditions": [
    {
      "metric": "ROW_COUNT",
      "thresholdValue": 0,
      "isThresholdRelative": false
    },
    {
      "metric": "NULL_COUNT",
      "sourceField": "customer_id",
      "targetField": "customer_id",
      "thresholdValue": 0,
      "isThresholdRelative": false
    },
    {
      "metric": "SUM",
      "sourceField": "amount",
      "targetField": "amount",
      "thresholdValue": 0.1,
      "isThresholdRelative": true
    }
  ]
}
```

注意：`ROW_COUNT` 条件没有字段，而字段级条件都指定了 `sourceField` 和 `targetField`。
