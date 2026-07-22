# Apache Airflow DAG 模式实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

## 核心概念

### 1. DAG 设计原则

| 原则 | 描述 |
|------|------|
| **幂等性** | 多次运行产生相同结果 |
| **原子性** | 任务要么完全成功，要么完全失败 |
| **增量处理** | 仅处理新增/变更的数据 |
| **可观测性** | 每个步骤都有日志、指标和告警 |

### 2. 任务依赖关系

```python
# 线性
task1 >> task2 >> task3

# 扇出
task1 >> [task2, task3, task4]

# 扇入
[task1, task2, task3] >> task4

# 复杂
task1 >> task2 >> task4
task1 >> task3 >> task4
```

## 快速开始

```python
# dags/example_dag.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(hours=1),
}

with DAG(
    dag_id='example_etl',
    default_args=default_args,
    description='Example ETL pipeline',
    schedule='0 6 * * *',  # 每天早上6点
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'example'],
    max_active_runs=1,
) as dag:

    start = EmptyOperator(task_id='start')

    def extract_data(**context):
        execution_date = context['ds']
        # 提取逻辑在此
        return {'records': 1000}

    extract = PythonOperator(
        task_id='extract',
        python_callable=extract_data,
    )

    end = EmptyOperator(task_id='end')

    start >> extract >> end
```

## 模式

### 模式 1: TaskFlow API (Airflow 2.0+)

```python
# dags/taskflow_example.py
from datetime import datetime
from airflow.decorators import dag, task
from airflow.models import Variable

@dag(
    dag_id='taskflow_etl',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'taskflow'],
)
def taskflow_etl():
    """使用 TaskFlow API 的 ETL 管道"""

    @task()
    def extract(source: str) -> dict:
        """从数据源提取数据"""
        import pandas as pd

        df = pd.read_csv(f's3://bucket/{source}/{{ ds }}.csv')
        return {'data': df.to_dict(), 'rows': len(df)}

    @task()
    def transform(extracted: dict) -> dict:
        """转换提取的数据"""
        import pandas as pd

        df = pd.DataFrame(extracted['data'])
        df['processed_at'] = datetime.now()
        df = df.dropna()
        return {'data': df.to_dict(), 'rows': len(df)}

    @task()
    def load(transformed: dict, target: str):
        """加载数据到目标位置"""
        import pandas as pd

        df = pd.DataFrame(transformed['data'])
        df.to_parquet(f's3://bucket/{target}/{{ ds }}.parquet')
        return transformed['rows']

    @task()
    def notify(rows_loaded: int):
        """发送通知"""
        print(f'已加载 {rows_loaded} 行数据')

    # 通过 XCom 传递定义依赖关系
    extracted = extract(source='raw_data')
    transformed = transform(extracted)
    loaded = load(transformed, target='processed_data')
    notify(loaded)

# 实例化 DAG
taskflow_etl()
```

### 模式 2: 动态 DAG 生成

```python
# dags/dynamic_dag_factory.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
import json

# 多个相似管道的配置
PIPELINE_CONFIGS = [
    {'name': 'customers', 'schedule': '@daily', 'source': 's3://raw/customers'},
    {'name': 'orders', 'schedule': '@hourly', 'source': 's3://raw/orders'},
    {'name': 'products', 'schedule': '@weekly', 'source': 's3://raw/products'},
]

def create_dag(config: dict) -> DAG:
    """从配置创建 DAG 的工厂函数"""

    dag_id = f"etl_{config['name']}"

    default_args = {
        'owner': 'data-team',
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
    }

    dag = DAG(
        dag_id=dag_id,
        default_args=default_args,
        schedule=config['schedule'],
        start_date=datetime(2024, 1, 1),
        catchup=False,
        tags=['etl', 'dynamic', config['name']],
    )

    with dag:
        def extract_fn(source, **context):
            print(f"从 {source} 提取数据，执行日期: {context['ds']}")

        def transform_fn(**context):
            print(f"转换数据，执行日期: {context['ds']}")

        def load_fn(table_name, **context):
            print(f"加载到 {table_name}，执行日期: {context['ds']}")

        extract = PythonOperator(
            task_id='extract',
            python_callable=extract_fn,
            op_kwargs={'source': config['source']},
        )

        transform = PythonOperator(
            task_id='transform',
            python_callable=transform_fn,
        )

        load = PythonOperator(
            task_id='load',
            python_callable=load_fn,
            op_kwargs={'table_name': config['name']},
        )

        extract >> transform >> load

    return dag

# 生成 DAG
for config in PIPELINE_CONFIGS:
    globals()[f"dag_{config['name']}"] = create_dag(config)
```

### 模式 3: 分支和条件逻辑

```python
# dags/branching_example.py
from airflow.decorators import dag, task
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule

@dag(
    dag_id='branching_pipeline',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
)
def branching_pipeline():

    @task()
    def check_data_quality() -> dict:
        """检查数据质量并返回指标"""
        quality_score = 0.95  # 模拟值
        return {'score': quality_score, 'rows': 10000}

    def choose_branch(**context) -> str:
        """决定执行哪个分支"""
        ti = context['ti']
        metrics = ti.xcom_pull(task_ids='check_data_quality')

        if metrics['score'] >= 0.9:
            return 'high_quality_path'
        elif metrics['score'] >= 0.7:
            return 'medium_quality_path'
        else:
            return 'low_quality_path'

    quality_check = check_data_quality()

    branch = BranchPythonOperator(
        task_id='branch',
        python_callable=choose_branch,
    )

    high_quality = EmptyOperator(task_id='high_quality_path')
    medium_quality = EmptyOperator(task_id='medium_quality_path')
    low_quality = EmptyOperator(task_id='low_quality_path')

    # 汇合点 - 任一分支完成后运行
    join = EmptyOperator(
        task_id='join',
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    quality_check >> branch >> [high_quality, medium_quality, low_quality] >> join

branching_pipeline()
```

### 模式 4: Sensors 和外部依赖

```python
# dags/sensor_patterns.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.operators.python import PythonOperator

with DAG(
    dag_id='sensor_example',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # 等待 S3 文件
    wait_for_file = S3KeySensor(
        task_id='wait_for_s3_file',
        bucket_name='data-lake',
        bucket_key='raw/{{ ds }}/data.parquet',
        aws_conn_id='aws_default',
        timeout=60 * 60 * 2,  # 2小时
        poke_interval=60 * 5,  # 每5分钟检查一次
        mode='reschedule',  # 等待时释放 worker 插槽
    )

    # 等待另一个 DAG 完成
    wait_for_upstream = ExternalTaskSensor(
        task_id='wait_for_upstream_dag',
        external_dag_id='upstream_etl',
        external_task_id='final_task',
        execution_date_fn=lambda dt: dt,  # 相同执行日期
        timeout=60 * 60 * 3,
        mode='reschedule',
    )

    # 使用 @task.sensor 装饰器的自定义 sensor
    @task.sensor(poke_interval=60, timeout=3600, mode='reschedule')
    def wait_for_api() -> PokeReturnValue:
        """自定义 sensor 检查 API 可用性"""
        import requests

        response = requests.get('https://api.example.com/health')
        is_done = response.status_code == 200

        return PokeReturnValue(is_done=is_done, xcom_value=response.json())

    api_ready = wait_for_api()

    def process_data(**context):
        api_result = context['ti'].xcom_pull(task_ids='wait_for_api')
        print(f"API 返回: {api_result}")

    process = PythonOperator(
        task_id='process',
        python_callable=process_data,
    )

    [wait_for_file, wait_for_upstream, api_ready] >> process
```

### 模式 5: 错误处理和告警

```python
# dags/error_handling.py
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.models import Variable

def task_failure_callback(context):
    """任务失败时的回调函数"""
    task_instance = context['task_instance']
    exception = context.get('exception')

    # 发送到 Slack/PagerDuty 等
    message = f"""
    任务失败！
    DAG: {task_instance.dag_id}
    任务: {task_instance.task_id}
    执行日期: {context['ds']}
    错误: {exception}
    日志 URL: {task_instance.log_url}
    """
    # send_slack_alert(message)
    print(message)

def dag_failure_callback(context):
    """DAG 失败时的回调函数"""
    # 汇总失败信息，发送摘要
    pass

with DAG(
    dag_id='error_handling_example',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    on_failure_callback=dag_failure_callback,
    default_args={
        'on_failure_callback': task_failure_callback,
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
    },
) as dag:

    def might_fail(**context):
        import random
        if random.random() < 0.3:
            raise ValueError("随机失败！")
        return "成功"

    risky_task = PythonOperator(
        task_id='risky_task',
        python_callable=might_fail,
    )

    def cleanup(**context):
        """清理任务，无论上游是否失败都会运行"""
        print("正在清理...")

    cleanup_task = PythonOperator(
        task_id='cleanup',
        python_callable=cleanup,
        trigger_rule=TriggerRule.ALL_DONE,  # 即使上游失败也运行
    )

    def notify_success(**context):
        """仅当所有上游成功时运行"""
        print("所有任务成功！")

    success_notification = PythonOperator(
        task_id='notify_success',
        python_callable=notify_success,
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

    risky_task >> [cleanup_task, success_notification]
```

### 模式 6: 测试 DAG

```python
# tests/test_dags.py
import pytest
from datetime import datetime
from airflow.models import DagBag

@pytest.fixture
def dagbag():
    return DagBag(dag_folder='dags/', include_examples=False)

def test_dag_loaded(dagbag):
    """测试所有 DAG 无错误加载"""
    assert len(dagbag.import_errors) == 0, f"DAG 导入错误: {dagbag.import_errors}"

def test_dag_structure(dagbag):
    """测试特定 DAG 结构"""
    dag = dagbag.get_dag('example_etl')

    assert dag is not None
    assert len(dag.tasks) == 3
    assert dag.schedule_interval == '0 6 * * *'

def test_task_dependencies(dagbag):
    """测试任务依赖关系正确"""
    dag = dagbag.get_dag('example_etl')

    extract_task = dag.get_task('extract')
    assert 'start' in [t.task_id for t in extract_task.upstream_list]
    assert 'end' in [t.task_id for t in extract_task.downstream_list]

def test_dag_integrity(dagbag):
    """测试 DAG 无循环且有效"""
    for dag_id, dag in dagbag.dags.items():
        assert dag.test_cycle() is None, f"在 {dag_id} 中检测到循环"

# 测试单个任务逻辑
def test_extract_function():
    """extract 函数的单元测试"""
    from dags.example_dag import extract_data

    result = extract_data(ds='2024-01-01')
    assert 'records' in result
    assert isinstance(result['records'], int)
```

## 项目结构

```
airflow/
├── dags/
│   ├── __init__.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── operators.py    # 自定义 operators
│   │   ├── sensors.py      # 自定义 sensors
│   │   └── callbacks.py    # 告警回调
│   ├── etl/
│   │   ├── customers.py
│   │   └── orders.py
│   └── ml/
│       └── training.py
├── plugins/
│   └── custom_plugin.py
├── tests/
│   ├── __init__.py
│   ├── test_dags.py
│   └── test_operators.py
├── docker-compose.yml
└── requirements.txt
```

## 最佳实践

### 推荐做法
- **使用 TaskFlow API** - 代码更简洁，自动处理 XCom
- **设置超时** - 防止僵尸任务
- **使用 `mode='reschedule'`** - 对于 sensors，释放 worker 资源
- **测试 DAG** - 单元测试和集成测试
- **幂等任务** - 安全重试

### 避免做法
- **不要使用 `depends_on_past=True`** - 会造成瓶颈
- **不要硬编码日期** - 使用 `{{ ds }}` 宏
- **不要使用全局状态** - 任务应无状态
- **不要盲目跳过 catchup** - 理解其影响
- **不要在 DAG 文件中放置重逻辑** - 从模块导入

## 资源

- [Airflow 官方文档](https://airflow.apache.org/docs/)
- [Astronomer 指南](https://docs.astronomer.io/learn)
- [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html)
