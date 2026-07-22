# 数据质量框架实施手册

本文件包含技能所引用的详细模式、检查清单和代码示例。

## 核心概念

### 1. 数据质量维度

| 维度 | 描述 | 示例检查 |
|-----------|-------------|---------------|
| **完整性（Completeness）** | 无缺失值 | `expect_column_values_to_not_be_null` |
| **唯一性（Uniqueness）** | 无重复 | `expect_column_values_to_be_unique` |
| **有效性（Validity）** | 值在预期范围内 | `expect_column_values_to_be_in_set` |
| **准确性（Accuracy）** | 数据与现实一致 | 交叉引用校验 |
| **一致性（Consistency）** | 无矛盾 | `expect_column_pair_values_A_to_be_greater_than_B` |
| **时效性（Timeliness）** | 数据是最新的 | `expect_column_max_to_be_between` |

### 2. 数据测试金字塔

```
          /\
         /  \     集成测试（跨表）
        /────\
       /      \   单元测试（单列）
      /────────\
     /          \ 模式测试（结构）
    /────────────\
```

## 快速开始

### Great Expectations 安装配置

```bash
# 安装
pip install great_expectations

# 初始化项目
great_expectations init

# 创建数据源
great_expectations datasource new
```

```python
# great_expectations/checkpoints/daily_validation.yml
import great_expectations as gx

# 创建上下文
context = gx.get_context()

# 创建期望套件
suite = context.add_expectation_suite("orders_suite")

# 添加期望
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeUnique(column="order_id")
)

# 验证
results = context.run_checkpoint(checkpoint_name="daily_orders")
```

## 模式

### 模式 1：Great Expectations 套件

```python
# expectations/orders_suite.py
import great_expectations as gx
from great_expectations.core import ExpectationSuite
from great_expectations.core.expectation_configuration import ExpectationConfiguration

def build_orders_suite() -> ExpectationSuite:
    """构建完整的订单期望套件"""

    suite = ExpectationSuite(expectation_suite_name="orders_suite")

    # 模式期望
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_table_columns_to_match_set",
        kwargs={
            "column_set": ["order_id", "customer_id", "amount", "status", "created_at"],
            "exact_match": False  # 允许其他列
        }
    ))

    # 主键
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "order_id"}
    ))
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_unique",
        kwargs={"column": "order_id"}
    ))

    # 外键
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_column_values_to_not_be_null",
        kwargs={"column": "customer_id"}
    ))

    # 枚举值
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_in_set",
        kwargs={
            "column": "status",
            "value_set": ["pending", "processing", "shipped", "delivered", "cancelled"]
        }
    ))

    # 数值范围
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_between",
        kwargs={
            "column": "amount",
            "min_value": 0,
            "max_value": 100000,
            "strict_min": True  # amount > 0
        }
    ))

    # 日期有效性
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_column_values_to_be_dateutil_parseable",
        kwargs={"column": "created_at"}
    ))

    # 时效性 —— 数据应是最近的
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_column_max_to_be_between",
        kwargs={
            "column": "created_at",
            "min_value": {"$PARAMETER": "now - timedelta(days=1)"},
            "max_value": {"$PARAMETER": "now"}
        }
    ))

    # 行数合理性
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_table_row_count_to_be_between",
        kwargs={
            "min_value": 1000,  # 期望至少 1000 行
            "max_value": 10000000
        }
    ))

    # 统计期望
    suite.add_expectation(ExpectationConfiguration(
        expectation_type="expect_column_mean_to_be_between",
        kwargs={
            "column": "amount",
            "min_value": 50,
            "max_value": 500
        }
    ))

    return suite
```

### 模式 2：Great Expectations 检查点

```yaml
# great_expectations/checkpoints/orders_checkpoint.yml
name: orders_checkpoint
config_version: 1.0
class_name: Checkpoint
run_name_template: "%Y%m%d-%H%M%S-orders-validation"

validations:
  - batch_request:
      datasource_name: warehouse
      data_connector_name: default_inferred_data_connector_name
      data_asset_name: orders
      data_connector_query:
        index: -1  # 最新批次
    expectation_suite_name: orders_suite

action_list:
  - name: store_validation_result
    action:
      class_name: StoreValidationResultAction

  - name: store_evaluation_parameters
    action:
      class_name: StoreEvaluationParametersAction

  - name: update_data_docs
    action:
      class_name: UpdateDataDocsAction

  # 失败时发送 Slack 通知
  - name: send_slack_notification
    action:
      class_name: SlackNotificationAction
      slack_webhook: ${SLACK_WEBHOOK}
      notify_on: failure
      renderer:
        module_name: great_expectations.render.renderer.slack_renderer
        class_name: SlackRenderer
```

```python
# 运行检查点
import great_expectations as gx

context = gx.get_context()
result = context.run_checkpoint(checkpoint_name="orders_checkpoint")

if not result.success:
    failed_expectations = [
        r for r in result.run_results.values()
        if not r.success
    ]
    raise ValueError(f"数据质量检查失败：{failed_expectations}")
```

### 模式 3：dbt 数据测试

```yaml
# models/marts/core/_core__models.yml
version: 2

models:
  - name: fct_orders
    description: 订单事实表
    tests:
      # 表级测试
      - dbt_utils.recency:
          datepart: day
          field: created_at
          interval: 1
      - dbt_utils.at_least_one
      - dbt_utils.expression_is_true:
          expression: "total_amount >= 0"

    columns:
      - name: order_id
        description: 主键
        tests:
          - unique
          - not_null

      - name: customer_id
        description: 指向 dim_customers 的外键
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id

      - name: order_status
        tests:
          - accepted_values:
              values: ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

      - name: total_amount
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: ">= 0"

      - name: created_at
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: "<= current_timestamp"

  - name: dim_customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null

      - name: email
        tests:
          - unique
          - not_null
          # 自定义正则测试
          - dbt_utils.expression_is_true:
              expression: "email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'"
```

### 模式 4：自定义 dbt 测试

```sql
-- tests/generic/test_row_count_in_range.sql
{% test row_count_in_range(model, min_count, max_count) %}

with row_count as (
    select count(*) as cnt from {{ model }}
)

select cnt
from row_count
where cnt < {{ min_count }} or cnt > {{ max_count }}

{% endtest %}

-- 在 schema.yml 中的用法：
-- tests:
--   - row_count_in_range:
--       min_count: 1000
--       max_count: 10000000
```

```sql
-- tests/generic/test_sequential_values.sql
{% test sequential_values(model, column_name, interval=1) %}

with lagged as (
    select
        {{ column_name }},
        lag({{ column_name }}) over (order by {{ column_name }}) as prev_value
    from {{ model }}
)

select *
from lagged
where {{ column_name }} - prev_value != {{ interval }}
  and prev_value is not null

{% endtest %}
```

```sql
-- tests/singular/assert_orders_customers_match.sql
-- 单一测试：特定业务规则

with orders_customers as (
    select distinct customer_id from {{ ref('fct_orders') }}
),

dim_customers as (
    select customer_id from {{ ref('dim_customers') }}
),

orphaned_orders as (
    select o.customer_id
    from orders_customers o
    left join dim_customers c using (customer_id)
    where c.customer_id is null
)

select * from orphaned_orders
-- 若返回 0 行则测试通过
```

### 模式 5：数据契约

```yaml
# contracts/orders_contract.yaml
apiVersion: datacontract.com/v1.0.0
kind: DataContract
metadata:
  name: orders
  version: 1.0.0
  owner: data-platform-team
  contact: data-team@company.com

info:
  title: 订单数据契约
  description: 来自电商平台的订单事件数据契约
  purpose: 分析、报表与机器学习特征

servers:
  production:
    type: snowflake
    account: company.us-east-1
    database: ANALYTICS
    schema: CORE

terms:
  usage: 仅限内部分析使用
  limitations: 下游数据集市不得暴露 PII
  billing: 按扫描查询的 TB 数计费

schema:
  type: object
  properties:
    order_id:
      type: string
      format: uuid
      description: 唯一订单标识
      required: true
      unique: true
      pii: false

    customer_id:
      type: string
      format: uuid
      description: 客户标识
      required: true
      pii: true
      piiClassification: indirect

    total_amount:
      type: number
      minimum: 0
      maximum: 100000
      description: 订单总额（美元）

    created_at:
      type: string
      format: date-time
      description: 订单创建时间戳
      required: true

    status:
      type: string
      enum: [pending, processing, shipped, delivered, cancelled]
      description: 当前订单状态

quality:
  type: SodaCL
  specification:
    checks for orders:
      - row_count > 0
      - missing_count(order_id) = 0
      - duplicate_count(order_id) = 0
      - invalid_count(status) = 0:
          valid values: [pending, processing, shipped, delivered, cancelled]
      - freshness(created_at) < 24h

sla:
  availability: 99.9%
  freshness: 1 小时
  latency: 5 分钟
```

### 模式 6：自动化质量流水线

```python
# quality_pipeline.py
from dataclasses import dataclass
from typing import List, Dict, Any
import great_expectations as gx
from datetime import datetime

@dataclass
class QualityResult:
    table: str
    passed: bool
    total_expectations: int
    failed_expectations: int
    details: List[Dict[str, Any]]
    timestamp: datetime

class DataQualityPipeline:
    """跨表编排数据质量检查"""

    def __init__(self, context: gx.DataContext):
        self.context = context
        self.results: List[QualityResult] = []

    def validate_table(self, table: str, suite: str) -> QualityResult:
        """对单表按期望套件进行验证"""

        checkpoint_config = {
            "name": f"{table}_validation",
            "config_version": 1.0,
            "class_name": "Checkpoint",
            "validations": [{
                "batch_request": {
                    "datasource_name": "warehouse",
                    "data_asset_name": table,
                },
                "expectation_suite_name": suite,
            }],
        }

        result = self.context.run_checkpoint(**checkpoint_config)

        # 解析结果
        validation_result = list(result.run_results.values())[0]
        results = validation_result.results

        failed = [r for r in results if not r.success]

        return QualityResult(
            table=table,
            passed=result.success,
            total_expectations=len(results),
            failed_expectations=len(failed),
            details=[{
                "expectation": r.expectation_config.expectation_type,
                "success": r.success,
                "observed_value": r.result.get("observed_value"),
            } for r in results],
            timestamp=datetime.now()
        )

    def run_all(self, tables: Dict[str, str]) -> Dict[str, QualityResult]:
        """对所有表运行验证"""
        results = {}

        for table, suite in tables.items():
            print(f"正在验证 {table}...")
            results[table] = self.validate_table(table, suite)

        return results

    def generate_report(self, results: Dict[str, QualityResult]) -> str:
        """生成质量报告"""
        report = ["# 数据质量报告", f"生成时间：{datetime.now()}", ""]

        total_passed = sum(1 for r in results.values() if r.passed)
        total_tables = len(results)

        report.append(f"## 概览：{total_passed}/{total_tables} 张表通过")
        report.append("")

        for table, result in results.items():
            status = "✅" if result.passed else "❌"
            report.append(f"### {status} {table}")
            report.append(f"- 期望总数：{result.total_expectations}")
            report.append(f"- 失败数：{result.failed_expectations}")

            if not result.passed:
                report.append("- 失败检查：")
                for detail in result.details:
                    if not detail["success"]:
                        report.append(f"  - {detail['expectation']}：{detail['observed_value']}")
            report.append("")

        return "\n".join(report)

# 用法
context = gx.get_context()
pipeline = DataQualityPipeline(context)

tables_to_validate = {
    "orders": "orders_suite",
    "customers": "customers_suite",
    "products": "products_suite",
}

results = pipeline.run_all(tables_to_validate)
report = pipeline.generate_report(results)

# 若任一表失败则中断流水线
if not all(r.passed for r in results.values()):
    print(report)
    raise ValueError("数据质量检查失败！")
```

## 最佳实践

### 推荐做法
- **尽早测试** —— 在转换前验证源数据
- **渐进式测试** —— 边发现问题边补充测试
- **记录期望** —— 为每个测试写清描述
- **失败告警** —— 与监控系统集成
- **版本化契约** —— 跟踪模式变更

### 避免做法
- **不要全量测试** —— 聚焦关键列
- **不要忽视警告** —— 警告往往先于失败出现
- **不要跳过时效性** —— 过期的数据就是坏数据
- **不要硬编码阈值** —— 使用动态基线
- **不要孤立测试** —— 也要测试关联关系

## 资源

- [Great Expectations 文档](https://docs.greatexpectations.io/)
- [dbt 测试文档](https://docs.getdbt.com/docs/build/tests)
- [数据契约规范](https://datacontract.com/)
- [Soda Core](https://docs.soda.io/soda-core/overview.html)
