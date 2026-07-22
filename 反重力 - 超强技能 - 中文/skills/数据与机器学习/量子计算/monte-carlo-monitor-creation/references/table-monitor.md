# 表监控器参考

构建 `createTableMonitorMac` 工具调用的详细参考。

## 适用场景

涉及以下需求时使用表监控器：

- 一次监控整个数据库或 Schema 中的多张表
- 追踪新鲜度（每张表上次更新是什么时候？）
- 检测 Schema 变更（列的添加、删除或类型变更）
- 监控大范围表的数据量变化（行数异常）
- 通过异常检测实现广泛覆盖（无需自定义阈值）

**以下场景不要使用表监控器：**

- 追踪单表的字段级指标（使用指标监控器）
- 应用自定义阈值或显式操作符如 GT/LT（使用指标监控器）
- 验证行级业务规则或引用完整性（使用验证监控器）

---

## 必需参数

| 参数 | 类型 | 说明 |
|-----------|------|------|
| `name` | string | 表监控器的唯一标识符。在同一命名空间中的所有表监控器中必须唯一。 |
| `description` | string | 监控器检查内容的人类可读描述（最多 512 字符）。 |
| `warehouse` | string | 仓库名称或 UUID。使用 `getTable` 或 `search` 查找。 |
| `asset_selection` | object | 定义要监控哪些表的资产选择配置（见下方资产选择）。 |

## 可选参数

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|------|
| `alert_conditions` | array of strings | `["last_updated_on", "schema", "total_row_count", "total_row_count_last_changed_on"]` | 要监控的指标名称（见下方告警条件）。 |
| `domain_id` | string (uuid) | 无 | 域 UUID（使用 `getDomains` 列出）。 |

---

## 前置步骤：验证仓库

创建表监控器前，解析仓库名称或 UUID。`warehouse` 参数是必需的，必须与 Monte Carlo 账户中的现有仓库匹配。

1. 如果用户提供了表名，调用 `getTable` 获取表详情——响应包含仓库名称和 UUID。
2. 如果用户提供了数据库或 Schema 名称但没有具体表，调用 `search` 加数据库或 Schema 名称查找资产并识别仓库。
3. 在 `warehouse` 参数中使用仓库名称或 UUID。

**绝不猜测仓库值。** 如果无法解析，询问用户。

---

## 资产选择

`asset_selection` 对象定义监控器覆盖哪些表。必须包含 `databases` 列表。

**使用数据库和 Schema 范围选择要监控的表。** 这是可靠的方式，覆盖大多数用例。

> **已知限制：** MCP 工具支持 `filters` 和 `exclusions` 参数，但工具的 Schema 描述了错误的格式。在修复之前（[K2-269](https://linear.app/montecarlodata/issue/K2-269)），**不要传入 `filters` 或 `exclusions`**——它们会导致错误。改用数据库/Schema 范围来缩小被监控表的范围。如果用户需要正则或模式过滤，解释此限制并建议（a）使用 Schema 级别范围尽量接近，或（b）为特定表创建单独的指标监控器。

### 数据库级别选择

要监控整个数据库中的所有表，只指定数据库名称，不传 `schemas` 列表：

```json
{
  "databases": [
    {"name": "analytics"}
  ]
}
```

这监控 `analytics` 数据库中每个 Schema 的每张表。

### Schema 级别选择

要监控特定 Schema 中的所有表，包含 `schemas` 列表：

```json
{
  "databases": [
    {
      "name": "analytics",
      "schemas": ["core", "staging"]
    }
  ]
}
```

这监控 `analytics` 中 `core` 和 `staging` Schema 的每张表，但不监控其他 Schema 中的表。

### 多个数据库

可以在单个监控器中跨多个数据库监控表：

```json
{
  "databases": [
    {"name": "analytics", "schemas": ["core"]},
    {"name": "raw_data"},
    {"name": "reporting", "schemas": ["public", "internal"]}
  ]
}
```

---

## 告警条件

告警条件定义表监控器追踪哪些指标。操作符始终为 AUTO（异常检测）——表监控器不支持自定义阈值。

| 指标 | 说明 |
|--------|------|
| `last_updated_on` | 新鲜度监控。表未在其正常节奏内更新时告警。 |
| `schema` | 任何 Schema 变更。列被添加、删除或类型变更时告警。 |
| `schema_fields_added` | 检测到新列。仅当表中出现新列时告警。 |
| `schema_fields_removed` | 列被删除。仅当现有列从表中被移除时告警。 |
| `schema_fields_type_change` | 列类型变更。仅当列的数据类型变更时告警。 |
| `total_row_count` | 行数变化。总行数异常变化时告警。 |
| `total_row_count_last_changed_on` | 距上次数据量变化的时间。行数未变化的异常时长告警。 |

### 注意事项

- **所有操作符均为 AUTO（异常检测）。** 表监控器不支持 GT、LT 等自定义阈值。如果用户需要自定义阈值，改用指标监控器。
- **无 `schedule` 字段。** 表监控器不支持 MaC YAML 中的 `schedule` 字段。添加它会导致 `montecarlo monitors apply` 验证错误。表监控器的调度由 Monte Carlo 自动管理。不要在生成的 YAML 中添加调度块。
- 默认集合（`last_updated_on`、`schema`、`total_row_count`、`total_row_count_last_changed_on`）提供广泛覆盖，适用于大多数用例。仅当用户明确要求子集时才覆盖默认值。
- `schema` 是 `schema_fields_added`、`schema_fields_removed` 和 `schema_fields_type_change` 的超集。使用 `schema` 时无需再包含细粒度 Schema 指标。

---

## 示例

### 监控数据库中的所有表（最小配置）

```json
{
  "name": "analytics_db_monitor",
  "description": "Monitor all tables in the analytics database for freshness, schema changes, and volume",
  "warehouse": "production_warehouse",
  "asset_selection": {
    "databases": [
      {"name": "analytics"}
    ]
  }
}
```

使用默认告警条件（`last_updated_on`、`schema`、`total_row_count`、`total_row_count_last_changed_on`）。

### 监控特定 Schema（默认告警）

```json
{
  "name": "core_schemas_monitor",
  "description": "Monitor all tables in core and reporting schemas",
  "warehouse": "production_warehouse",
  "asset_selection": {
    "databases": [
      {
        "name": "analytics",
        "schemas": ["core", "reporting"]
      }
    ]
  }
}
```

监控 `core` 和 `reporting` Schema 中的每张表，其他 Schema 不受监控。

### 跨数据库监控多个 Schema

```json
{
  "name": "prod_tables_monitor",
  "description": "Monitor production tables across analytics and raw_data databases",
  "warehouse": "production_warehouse",
  "asset_selection": {
    "databases": [
      {
        "name": "analytics",
        "schemas": ["core", "reporting"]
      },
      {
        "name": "raw_data",
        "schemas": ["ingestion"]
      }
    ]
  }
}
```

监控特定生产 Schema 中的表，开发和暂存 Schema 不受监控。

### 仅 Schema 变更监控

```json
{
  "name": "warehouse_schema_watch",
  "description": "Track schema changes across the entire data warehouse",
  "warehouse": "production_warehouse",
  "asset_selection": {
    "databases": [
      {"name": "analytics"},
      {"name": "raw_data"}
    ]
  },
  "alert_conditions": [
    "schema_fields_added",
    "schema_fields_removed",
    "schema_fields_type_change"
  ]
}
```

仅监控跨多个数据库的 Schema 变更（不监控新鲜度或数据量）。使用细粒度 Schema 指标而非 `schema`，以便选择性启用/禁用每种类型。

---

## 表监控器 vs 指标监控器

| 方面 | 表监控器 | 指标监控器 |
|--------|---------------|----------------|
| **范围** | 多张表（数据库/Schema 级别） | 单表 |
| **指标** | 新鲜度、Schema 变更、行数 | 字段级指标（空值率、均值、总和等） |
| **操作符** | 仅 AUTO（异常检测） | AUTO 或显式阈值（GT、LT、EQ 等） |
| **资产选择** | 数据库/Schema，带过滤和排除 | 通过 MCON 或名称指定的单表 |
| **时间戳字段** | 不需要 | 必需（`aggregate_time_field`） |
| **分段** | 不可用 | 通过 `segment_fields` 可用 |
| **最佳用途** | 广泛覆盖、新鲜度、Schema 漂移 | 针对性的字段级数据质量检查 |

**经验法则：** 如果用户想监控特定表的特定字段并设定特定阈值，使用指标监控器。如果用户想跨多表进行广泛监控并自动异常检测，使用表监控器。
