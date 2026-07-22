# 验证监控器参考

构建 `createValidationMonitorMac` 工具调用的详细参考。

## 适用场景

涉及以下需求时使用验证监控器：

- 检查特定字段是否不为空
- 验证值在允许集合内（如状态为 'active'、'pending'、'inactive'）
- 实施引用完整性（字段值存在于另一张表中）
- 应用行级业务规则（如"金额必须为正"）
- 使用 AND/OR 逻辑组合多个条件

---

## 搞对逻辑：条件匹配无效数据

这是验证监控器中最容易混淆的方面，也是错误的首要来源。**条件描述的是无效数据的样子——你希望被提醒的数据。** 它们不描述有效数据的样子。

可以这样理解：监控器扫描行，找到匹配条件的行时触发告警。所以条件必须匹配"坏"行。

| 用户想要 | 条件应匹配 | 常见错误 |
|------------|----------------------|----------------|
| "id 不应为空" | id IS NULL（发现空值时告警） | id IS NOT NULL（会对每个有效行告警） |
| "状态必须在 [active, pending] 中" | status NOT IN [active, pending]（对意外值告警） | status IN [active, pending]（会对有效行告警） |
| "金额必须为正" | amount IS NEGATIVE（对坏值告警） | amount > 0（会对有效行告警） |
| "email 不能为空" | email IS NULL **或** email = ''（对缺失值告警） | email IS NOT NULL（会对有效行告警） |

**构建任何条件前，问自己："如果一行匹配此条件，这行是无效的吗？"如果答案是否，逻辑就反了。**

---

## 前置步骤：验证字段存在

构建 `alert_condition` 前，验证你计划引用的每个字段名都存在于表的列列表中。这是验证监控器失败的第二大原因——引用不存在或拼写错误的列。

1. 你应该已从 `getTable`（含 `include_fields: true`）获取了列列表（在主技能步骤 2 中完成）。
2. 对于计划条件中的每个字段名，确认它完全按拼写出现在列列表中（字段名在大多数仓库中区分大小写）。
3. 如果字段不存在，停下来请用户澄清正确的列名。不要猜测。

---

## 必需参数

| 参数 | 类型 | 说明 |
|-----------|------|------|
| `name` | string | 监控器的唯一标识符。使用描述性 slug（如 `orders_not_null_check`）。 |
| `description` | string | 监控器检查内容的人类可读描述。 |
| `table` | string | 表 MCON（首选）或 `database:schema.table` 格式。非 MCON 时需同时传入 `warehouse`。 |
| `alert_condition` | object | 定义何时告警的条件树（见下方告警条件结构）。 |

## 可选参数

| 参数 | 类型 | 说明 |
|-----------|------|------|
| `warehouse` | string | 仓库名称或 UUID。`table` 非 MCON 时必需。 |
| `domain_id` | string (uuid) | 域 UUID（使用 `getDomains` 列出）。 |

---

## 告警条件结构

`alert_condition` 的顶层必须始终是 GROUP 节点。该 GROUP 包含一个或多个用 AND 或 OR 逻辑组合的条件。

```json
{
  "type": "GROUP",
  "operator": "AND",
  "conditions": [...]
}
```

### 条件类型

有四种条件类型：UNARY、BINARY、SQL 和 GROUP。

#### UNARY（单值检查）

用于对单个字段无比较值的谓词。

```json
{
  "type": "UNARY",
  "predicate": {"name": "null", "negated": false},
  "value": [{"type": "FIELD", "field": "column_name"}]
}
```

- `predicate.name` —— 要应用的谓词（见下方谓词参考）。
- `predicate.negated` —— 设为 `true` 反转谓词（如 `null` 加 `negated: true` 表示"不为空"）。
- `value` —— 包含单个值描述符的数组（通常是 FIELD 引用）。

#### BINARY（比较检查）

用于将字段与值比较的谓词。

```json
{
  "type": "BINARY",
  "predicate": {"name": "greater_than", "negated": false},
  "left": [{"type": "FIELD", "field": "column_name"}],
  "right": [{"type": "LITERAL", "literal": "0"}]
}
```

- `left` —— 比较的左侧（通常是 FIELD 引用）。
- `right` —— 比较的右侧（通常是 LITERAL 值、SQL 表达式或 FIELD 引用）。
- `left` 和 `right` 都是值描述符数组。

#### SQL（自定义 SQL 表达式）

用于难以用 UNARY/BINARY 节点表达的复杂条件。SQL 表达式对无效行应求值为 true。

```json
{
  "type": "SQL",
  "sql": "amount > 0 AND amount < 1000000"
}
```

#### GROUP（嵌套条件）

用于用 AND 或 OR 逻辑组合多个条件。GROUP 可以嵌套。

```json
{
  "type": "GROUP",
  "operator": "OR",
  "conditions": [
    {"type": "UNARY", "...": "..."},
    {"type": "BINARY", "...": "..."}
  ]
}
```

---

## 值类型

值描述符出现在 UNARY 和 BINARY 条件的 `value`、`left` 和 `right` 数组中。

| 类型 | 字段 | 说明 | 示例 |
|------|-------|------|---------|
| `FIELD` | `"field": "column_name"` | 引用表中的列。 | `{"type": "FIELD", "field": "user_id"}` |
| `LITERAL` | `"literal": "value"` | 静态值（始终为字符串，即使是数字）。 | `{"type": "LITERAL", "literal": "100"}` |
| `SQL` | `"sql": "SELECT ..."` | SQL 表达式或子查询。 | `{"type": "SQL", "sql": "SELECT MAX(id) FROM ref_table"}` |

---

## 谓词参考

构建条件前，调用 `getValidationPredicates` 获取已连接仓库支持的完整谓词列表。以下列表涵盖常见谓词但可能不完全。

### 一元谓词

这些谓词不需要比较值——它们检查字段本身的属性。

| 谓词 | 说明 | 使用示例 |
|-----------|-------------|-------------|
| `null` | 字段值为空。 | 对空 id 告警。 |
| `is_negative` | 字段值为负。 | 对负金额告警。 |
| `is_between_0_and_1` | 字段值在 0 和 1 之间（含）。 | 对应为百分比（0-100）的比率告警。 |
| `is_future_date` | 字段值为未来的日期/时间戳。 | 对未来日期的记录告警。 |
| `is_uuid` | 字段值匹配 UUID 格式。 | 对 UUID 字段中的非 UUID 值告警（配合 `negated: true` 使用）。 |

### 二元谓词

这些谓词将字段与值比较。

| 谓词 | 右侧 | 说明 | 使用示例 |
|-----------|----------------|-------------|-------------|
| `equal` | 单个 LITERAL | 字段等于给定值。 | `status` 等于 `'deleted'` 时告警。 |
| `greater_than` | 单个 LITERAL | 字段大于给定值。 | `discount_pct` 超过 100 时告警。 |
| `less_than` | 单个 LITERAL | 字段小于给定值。 | `quantity` 低于 0 时告警。 |
| `in_set` | 多个 LITERAL | 字段值在给定集合中。 | `status` 在无效集合中时告警（见下方示例）。 |
| `contains` | 单个 LITERAL | 字段值包含给定子串。 | `email` 包含 `'test@'` 时告警。 |
| `starts_with` | 单个 LITERAL | 字段值以给定前缀开头。 | `phone` 以 `'000'` 开头时告警。 |
| `between` | 两个 LITERAL | 字段值在两个给定值之间（含）。 | `score` 在 0 和 10 之间时告警（如果该范围无效）。 |

### 使用 `negated` 反转谓词

任何谓词都可以通过在谓词对象中设置 `"negated": true` 来反转。这对"必须在集合中"的验证至关重要：

- **"状态必须在 [active, pending] 中"** 变为 `in_set`，值为 `["active", "pending"]` 并设 `negated: true`——意为"状态不在 [active, pending] 中时告警"。
- **"id 不能为空"** 变为 `null` 并设 `negated: false`——意为"id 为空时告警"（无需反转，因为条件已经匹配无效数据）。

---

## 示例

### id 为空时告警

继续前验证 `id` 存在于 `getTable` 返回的表 Schema 中。

```json
{
  "name": "orders_id_not_null",
  "description": "Alert when order id is null",
  "table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++analytics:core.orders",
  "alert_condition": {
    "type": "GROUP",
    "operator": "AND",
    "conditions": [
      {
        "type": "UNARY",
        "predicate": {"name": "null", "negated": false},
        "value": [{"type": "FIELD", "field": "id"}]
      }
    ]
  }
}
```

条件匹配 `id` IS NULL 的行——这些是我们希望被提醒的无效行。

### 状态不在允许集合中时告警

继续前验证 `status` 存在于 `getTable` 返回的表 Schema 中。

```json
{
  "name": "orders_status_allowed_values",
  "description": "Alert when order status is outside the allowed set",
  "table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++analytics:core.orders",
  "alert_condition": {
    "type": "GROUP",
    "operator": "AND",
    "conditions": [
      {
        "type": "BINARY",
        "predicate": {"name": "in_set", "negated": true},
        "left": [{"type": "FIELD", "field": "status"}],
        "right": [
          {"type": "LITERAL", "literal": "active"},
          {"type": "LITERAL", "literal": "pending"},
          {"type": "LITERAL", "literal": "inactive"}
        ]
      }
    ]
  }
}
```

注意 `negated: true`——谓词是 `in_set`，但我们想在值不在集合中时告警。这能捕获任何意外的状态值。

### 金额为负时告警

继续前验证 `amount` 存在于 `getTable` 返回的表 Schema 中。

```json
{
  "name": "orders_positive_amount",
  "description": "Alert when order amount is negative",
  "table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++analytics:core.orders",
  "alert_condition": {
    "type": "GROUP",
    "operator": "AND",
    "conditions": [
      {
        "type": "UNARY",
        "predicate": {"name": "is_negative", "negated": false},
        "value": [{"type": "FIELD", "field": "amount"}]
      }
    ]
  }
}
```

条件匹配 `amount` 为负的行——这些是无效行。

### 组合条件：空值或负值

继续前验证 `amount` 和 `quantity` 都存在于 `getTable` 返回的表 Schema 中。

```json
{
  "name": "orders_amount_quality",
  "description": "Alert when amount is null or quantity is negative",
  "table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++analytics:core.orders",
  "alert_condition": {
    "type": "GROUP",
    "operator": "OR",
    "conditions": [
      {
        "type": "UNARY",
        "predicate": {"name": "null", "negated": false},
        "value": [{"type": "FIELD", "field": "amount"}]
      },
      {
        "type": "UNARY",
        "predicate": {"name": "is_negative", "negated": false},
        "value": [{"type": "FIELD", "field": "quantity"}]
      }
    ]
  }
}
```

OR 操作符意味着任一条件匹配就触发告警——行为空金额或数量为负。

### Between 检查与嵌套 AND/OR

继续前验证 `score` 和 `status` 都存在于 `getTable` 返回的表 Schema 中。

```json
{
  "name": "records_score_validation",
  "description": "Alert when score is outside 0-100 range for active records",
  "table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++warehouse:metrics.records",
  "alert_condition": {
    "type": "GROUP",
    "operator": "AND",
    "conditions": [
      {
        "type": "BINARY",
        "predicate": {"name": "equal", "negated": false},
        "left": [{"type": "FIELD", "field": "status"}],
        "right": [{"type": "LITERAL", "literal": "active"}]
      },
      {
        "type": "BINARY",
        "predicate": {"name": "between", "negated": true},
        "left": [{"type": "FIELD", "field": "score"}],
        "right": [
          {"type": "LITERAL", "literal": "0"},
          {"type": "LITERAL", "literal": "100"}
        ]
      }
    ]
  }
}
```

使用 `between` 加 `negated: true` 对 score 在 0-100 范围外的行告警，但仅针对 active 记录（AND 操作符要求两个条件都匹配）。

### 使用 SQL 子查询的引用完整性

继续前验证 `customer_id` 存在于 `getTable` 返回的表 Schema 中。

```json
{
  "name": "orders_valid_customer",
  "description": "Alert when customer_id does not exist in customers table",
  "table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++analytics:core.orders",
  "alert_condition": {
    "type": "GROUP",
    "operator": "AND",
    "conditions": [
      {
        "type": "SQL",
        "sql": "customer_id IS NOT NULL AND customer_id NOT IN (SELECT id FROM analytics.core.customers)"
      }
    ]
  }
}
```

SQL 条件类型适用于需要子查询的引用完整性检查。`customer_id IS NOT NULL` 守卫避免对空值告警（如需要，空值应由单独的空值检查捕获）。

### Contains 和 starts_with 检查

继续前验证 `email` 和 `phone` 都存在于 `getTable` 返回的表 Schema 中。

```json
{
  "name": "contacts_format_validation",
  "description": "Alert when email contains test data or phone has invalid prefix",
  "table": "MCON++a1b2c3d4-e5f6-7890-abcd-ef1234567890++1++1++warehouse:crm.contacts",
  "alert_condition": {
    "type": "GROUP",
    "operator": "OR",
    "conditions": [
      {
        "type": "BINARY",
        "predicate": {"name": "contains", "negated": false},
        "left": [{"type": "FIELD", "field": "email"}],
        "right": [{"type": "LITERAL", "literal": "@test.example.com"}]
      },
      {
        "type": "BINARY",
        "predicate": {"name": "starts_with", "negated": false},
        "left": [{"type": "FIELD", "field": "phone"}],
        "right": [{"type": "LITERAL", "literal": "000"}]
      }
    ]
  }
}
```

---

## 兜底：自定义 SQL 监控器

如果 `createValidationMonitorMac` 失败——例如因为引用的列在活表中尚不存在，或仓库不支持特定谓词——改用 `createCustomSqlMonitorMac` 加显式 SQL 查询。

自定义 SQL 监控器允许你将任何验证逻辑表达为返回行或计数的 SQL 查询。当结构化验证条件树无法表达你的需求或遇到 API 错误时，这始终可用作备选。

兜底时：

1. 将意图中的验证逻辑翻译为 SQL 查询。
2. SQL 应选择违反规则的行（遵循相同的"条件匹配无效数据"原则）。
3. 使用 `createCustomSqlMonitorMac` 加翻译后的查询。
4. 告知用户你使用了自定义 SQL 监控器作为兜底，并解释原因。
