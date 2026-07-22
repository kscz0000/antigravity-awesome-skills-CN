---
name: azure-mgmt-fabric-py
description: Azure Fabric 管理 SDK for Python，用于管理 Microsoft Fabric 容量和资源。当用户要求'管理 Microsoft Fabric 容量和资源'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Fabric Management SDK for Python

以编程方式管理 Microsoft Fabric 容量和资源。

## 安装

```bash
pip install azure-mgmt-fabric
pip install azure-identity
```

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
AZURE_RESOURCE_GROUP=<your-resource-group>
```

## 身份验证

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.fabric import FabricMgmtClient
import os

credential = DefaultAzureCredential()
client = FabricMgmtClient(
    credential=credential,
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"]
)
```

## 创建 Fabric 容量

```python
from azure.mgmt.fabric import FabricMgmtClient
from azure.mgmt.fabric.models import FabricCapacity, FabricCapacityProperties, CapacitySku
from azure.identity import DefaultAzureCredential
import os

credential = DefaultAzureCredential()
client = FabricMgmtClient(
    credential=credential,
    subscription_id=os.environ["AZURE_SUBSCRIPTION_ID"]
)

resource_group = os.environ["AZURE_RESOURCE_GROUP"]
capacity_name = "myfabriccapacity"

capacity = client.fabric_capacities.begin_create_or_update(
    resource_group_name=resource_group,
    capacity_name=capacity_name,
    resource=FabricCapacity(
        location="eastus",
        sku=CapacitySku(
            name="F2",  # Fabric SKU
            tier="Fabric"
        ),
        properties=FabricCapacityProperties(
            administration=FabricCapacityAdministration(
                members=["user@contoso.com"]
            )
        )
    )
).result()

print(f"Capacity created: {capacity.name}")
```

## 获取容量详情

```python
capacity = client.fabric_capacities.get(
    resource_group_name=resource_group,
    capacity_name=capacity_name
)

print(f"Capacity: {capacity.name}")
print(f"SKU: {capacity.sku.name}")
print(f"State: {capacity.properties.state}")
print(f"Location: {capacity.location}")
```

## 列出资源组中的容量

```python
capacities = client.fabric_capacities.list_by_resource_group(
    resource_group_name=resource_group
)

for capacity in capacities:
    print(f"Capacity: {capacity.name} - SKU: {capacity.sku.name}")
```

## 列出订阅中的所有容量

```python
all_capacities = client.fabric_capacities.list_by_subscription()

for capacity in all_capacities:
    print(f"Capacity: {capacity.name} in {capacity.location}")
```

## 更新容量

```python
from azure.mgmt.fabric.models import FabricCapacityUpdate, CapacitySku

updated = client.fabric_capacities.begin_update(
    resource_group_name=resource_group,
    capacity_name=capacity_name,
    properties=FabricCapacityUpdate(
        sku=CapacitySku(
            name="F4",  # Scale up
            tier="Fabric"
        ),
        tags={"environment": "production"}
    )
).result()

print(f"Updated SKU: {updated.sku.name}")
```

## 暂停容量

暂停容量以停止计费：

```python
client.fabric_capacities.begin_suspend(
    resource_group_name=resource_group,
    capacity_name=capacity_name
).result()

print("Capacity suspended")
```

## 恢复容量

恢复已暂停的容量：

```python
client.fabric_capacities.begin_resume(
    resource_group_name=resource_group,
    capacity_name=capacity_name
).result()

print("Capacity resumed")
```

## 删除容量

```python
client.fabric_capacities.begin_delete(
    resource_group_name=resource_group,
    capacity_name=capacity_name
).result()

print("Capacity deleted")
```

## 检查名称可用性

```python
from azure.mgmt.fabric.models import CheckNameAvailabilityRequest

result = client.fabric_capacities.check_name_availability(
    location="eastus",
    body=CheckNameAvailabilityRequest(
        name="my-new-capacity",
        type="Microsoft.Fabric/capacities"
    )
)

if result.name_available:
    print("Name is available")
else:
    print(f"Name not available: {result.reason}")
```

## 列出可用 SKU

```python
skus = client.fabric_capacities.list_skus(
    resource_group_name=resource_group,
    capacity_name=capacity_name
)

for sku in skus:
    print(f"SKU: {sku.name} - Tier: {sku.tier}")
```

## 客户端操作

| 操作 | 方法 |
|------|------|
| `client.fabric_capacities` | 容量 CRUD 操作 |
| `client.operations` | 列出可用操作 |

## Fabric SKU

| SKU | 描述 | 容量单位 |
|-----|------|----------|
| `F2` | 入门级 | 2 Capacity Units |
| `F4` | 小型 | 4 Capacity Units |
| `F8` | 中型 | 8 Capacity Units |
| `F16` | 大型 | 16 Capacity Units |
| `F32` | 超大型 | 32 Capacity Units |
| `F64` | 2倍超大型 | 64 Capacity Units |
| `F128` | 4倍超大型 | 128 Capacity Units |
| `F256` | 8倍超大型 | 256 Capacity Units |
| `F512` | 16倍超大型 | 512 Capacity Units |
| `F1024` | 32倍超大型 | 1024 Capacity Units |
| `F2048` | 64倍超大型 | 2048 Capacity Units |

## 容量状态

| 状态 | 描述 |
|------|------|
| `Active` | 容量正在运行 |
| `Paused` | 容量已暂停（不计费） |
| `Provisioning` | 正在创建 |
| `Updating` | 正在修改 |
| `Deleting` | 正在删除 |
| `Failed` | 操作失败 |

## 长时间运行的操作

所有变更操作均为长时间运行操作（LRO）。使用 `.result()` 等待完成：

```python
# Synchronous wait
capacity = client.fabric_capacities.begin_create_or_update(...).result()

# Or poll manually
poller = client.fabric_capacities.begin_create_or_update(...)
while not poller.done():
    print(f"Status: {poller.status()}")
    time.sleep(5)
capacity = poller.result()
```

## 最佳实践

1. **使用 DefaultAzureCredential** 进行身份验证
2. **暂停未使用的容量** 以降低成本
3. **从较小的 SKU 开始** 并根据需要扩展
4. **使用标签** 进行成本追踪和组织管理
5. **创建容量前检查名称可用性**
6. **正确处理 LRO** — 不要假设操作立即完成
7. **设置容量管理员** — 指定可以管理工作区的用户
8. **通过 Azure Monitor 指标监控容量使用情况**

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
