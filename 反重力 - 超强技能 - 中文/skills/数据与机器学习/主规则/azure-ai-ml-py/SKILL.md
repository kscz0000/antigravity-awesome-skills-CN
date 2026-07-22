---
name: azure-ai-ml-py
description: Azure Machine Learning SDK v2 Python 客户端库。用于管理工作区、作业、模型、数据集、计算资源和管道。触发词：Azure ML、机器学习、ML工作区、训练作业、模型注册、计算集群、ML管道、数据资产、AML SDK
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Machine Learning SDK v2 for Python

用于管理 Azure ML 资源的客户端库：工作区、作业、模型、数据和计算资源。

## 安装

```bash
pip install azure-ai-ml
```

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
AZURE_ML_WORKSPACE_NAME=<your-workspace-name>
```

## 身份验证

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    credential=DefaultAzureCredential(),
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"],
    resource_group_name=os.environ["AZURE_RESOURCE_GROUP"],
    workspace_name=os.environ["AZURE_ML_WORKSPACE_NAME"]
)
```

### 从配置文件

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

# 使用当前目录或父目录中的 config.json
ml_client = MLClient.from_config(
    credential=DefaultAzureCredential()
)
```

## 工作区管理

### 创建工作区

```python
from azure.ai.ml.entities import Workspace

ws = Workspace(
    name="my-workspace",
    location="eastus",
    display_name="My Workspace",
    description="ML workspace for experiments",
    tags={"purpose": "demo"}
)

ml_client.workspaces.begin_create(ws).result()
```

### 列出工作区

```python
for ws in ml_client.workspaces.list():
    print(f"{ws.name}: {ws.location}")
```

## 数据资产

### 注册数据

```python
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes

# 注册文件
my_data = Data(
    name="my-dataset",
    version="1",
    path="azureml://datastores/workspaceblobstore/paths/data/train.csv",
    type=AssetTypes.URI_FILE,
    description="Training data"
)

ml_client.data.create_or_update(my_data)
```

### 注册文件夹

```python
my_data = Data(
    name="my-folder-dataset",
    version="1",
    path="azureml://datastores/workspaceblobstore/paths/data/",
    type=AssetTypes.URI_FOLDER
)

ml_client.data.create_or_update(my_data)
```

## 模型注册表

### 注册模型

```python
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes

model = Model(
    name="my-model",
    version="1",
    path="./model/",
    type=AssetTypes.CUSTOM_MODEL,
    description="My trained model"
)

ml_client.models.create_or_update(model)
```

### 列出模型

```python
for model in ml_client.models.list(name="my-model"):
    print(f"{model.name} v{model.version}")
```

## 计算资源

### 创建计算集群

```python
from azure.ai.ml.entities import AmlCompute

cluster = AmlCompute(
    name="cpu-cluster",
    type="amlcompute",
    size="Standard_DS3_v2",
    min_instances=0,
    max_instances=4,
    idle_time_before_scale_down=120
)

ml_client.compute.begin_create_or_update(cluster).result()
```

### 列出计算资源

```python
for compute in ml_client.compute.list():
    print(f"{compute.name}: {compute.type}")
```

## 作业

### 命令作业

```python
from azure.ai.ml import command, Input

job = command(
    code="./src",
    command="python train.py --data ${{inputs.data}} --lr ${{inputs.learning_rate}}",
    inputs={
        "data": Input(type="uri_folder", path="azureml:my-dataset:1"),
        "learning_rate": 0.01
    },
    environment="AzureML-sklearn-1.0-ubuntu20.04-py38-cpu@latest",
    compute="cpu-cluster",
    display_name="training-job"
)

returned_job = ml_client.jobs.create_or_update(job)
print(f"Job URL: {returned_job.studio_url}")
```

### 监控作业

```python
ml_client.jobs.stream(returned_job.name)
```

## 管道

```python
from azure.ai.ml import dsl, Input, Output
from azure.ai.ml.entities import Pipeline

@dsl.pipeline(
    compute="cpu-cluster",
    description="Training pipeline"
)
def training_pipeline(data_input):
    prep_step = prep_component(data=data_input)
    train_step = train_component(
        data=prep_step.outputs.output_data,
        learning_rate=0.01
    )
    return {"model": train_step.outputs.model}

pipeline = training_pipeline(
    data_input=Input(type="uri_folder", path="azureml:my-dataset:1")
)

pipeline_job = ml_client.jobs.create_or_update(pipeline)
```

## 环境

### 创建自定义环境

```python
from azure.ai.ml.entities import Environment

env = Environment(
    name="my-env",
    version="1",
    image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04",
    conda_file="./environment.yml"
)

ml_client.environments.create_or_update(env)
```

## 数据存储

### 列出数据存储

```python
for ds in ml_client.datastores.list():
    print(f"{ds.name}: {ds.type}")
```

### 获取默认数据存储

```python
default_ds = ml_client.datastores.get_default()
print(f"Default: {default_ds.name}")
```

## MLClient 操作

| 属性 | 操作 |
|----------|------------|
| `workspaces` | create, get, list, delete |
| `jobs` | create_or_update, get, list, stream, cancel |
| `models` | create_or_update, get, list, archive |
| `data` | create_or_update, get, list |
| `compute` | begin_create_or_update, get, list, delete |
| `environments` | create_or_update, get, list |
| `datastores` | create_or_update, get, list, get_default |
| `components` | create_or_update, get, list |

## 最佳实践

1. **使用版本控制**管理数据、模型和环境
2. **配置空闲自动缩容**以降低计算成本
3. **使用环境**确保训练可复现
4. **流式传输作业日志**监控进度
5. **训练成功后注册模型**
6. **使用管道**处理多步骤工作流
7. **为资源添加标签**便于组织和成本追踪

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 输出内容不能替代环境特定的验证、测试或专家评审。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
