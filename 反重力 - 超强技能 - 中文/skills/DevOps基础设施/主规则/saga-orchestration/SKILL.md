---
name: saga-orchestration
description: "分布式事务和长时间运行业务流程的编排模式。触发词：saga orchestration、分布式事务、补偿事务、saga模式、编排模式、长事务、分布式工作流、订单履约、saga编排"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Saga 编排

分布式事务和长时间运行业务流程的编排模式。

## 不适用场景

- 任务与 Saga 编排无关
- 需要本范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 适用场景

- 协调跨多个服务的事务
- 实现补偿事务
- 管理长时间运行的业务工作流
- 处理分布式系统中的故障
- 构建订单履约流程
- 实现审批工作流

## 核心概念

### 1. Saga 类型

```
Choreography                    Orchestration
┌─────┐  ┌─────┐  ┌─────┐     ┌─────────────┐
│Svc A│─►│Svc B│─►│Svc C│     │ Orchestrator│
└─────┘  └─────┘  └─────┘     └──────┬──────┘
   │        │        │               │
   ▼        ▼        ▼         ┌─────┼─────┐
 Event    Event    Event       ▼     ▼     ▼
                            ┌────┐┌────┐┌────┐
                            │Svc1││Svc2││Svc3│
                            └────┘└────┘└────┘
```

### 2. Saga 执行状态

| 状态           | 说明                           |
| -------------- | ------------------------------ |
| **Started**    | Saga 已启动                    |
| **Pending**    | 等待步骤完成                   |
| **Compensating** | 因故障正在回滚               |
| **Completed**  | 所有步骤执行成功               |
| **Failed**     | 补偿完成后 Saga 失败           |

## 模板

### 模板 1：Saga 编排器基类

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

class SagaState(Enum):
    STARTED = "started"
    PENDING = "pending"
    COMPENSATING = "compensating"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class SagaStep:
    name: str
    action: str
    compensation: str
    status: str = "pending"
    result: Optional[Dict] = None
    error: Optional[str] = None
    executed_at: Optional[datetime] = None
    compensated_at: Optional[datetime] = None


@dataclass
class Saga:
    saga_id: str
    saga_type: str
    state: SagaState
    data: Dict[str, Any]
    steps: List[SagaStep]
    current_step: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class SagaOrchestrator(ABC):
    """Saga 编排器基类。"""

    def __init__(self, saga_store, event_publisher):
        self.saga_store = saga_store
        self.event_publisher = event_publisher

    @abstractmethod
    def define_steps(self, data: Dict) -> List[SagaStep]:
        """定义 Saga 步骤。"""
        pass

    @property
    @abstractmethod
    def saga_type(self) -> str:
        """唯一的 Saga 类型标识符。"""
        pass

    async def start(self, data: Dict) -> Saga:
        """启动一个新的 Saga。"""
        saga = Saga(
            saga_id=str(uuid.uuid4()),
            saga_type=self.saga_type,
            state=SagaState.STARTED,
            data=data,
            steps=self.define_steps(data)
        )
        await self.saga_store.save(saga)
        await self._execute_next_step(saga)
        return saga

    async def handle_step_completed(self, saga_id: str, step_name: str, result: Dict):
        """处理步骤成功完成。"""
        saga = await self.saga_store.get(saga_id)

        # 更新步骤状态
        for step in saga.steps:
            if step.name == step_name:
                step.status = "completed"
                step.result = result
                step.executed_at = datetime.utcnow()
                break

        saga.current_step += 1
        saga.updated_at = datetime.utcnow()

        # 检查 Saga 是否已完成
        if saga.current_step >= len(saga.steps):
            saga.state = SagaState.COMPLETED
            await self.saga_store.save(saga)
            await self._on_saga_completed(saga)
        else:
            saga.state = SagaState.PENDING
            await self.saga_store.save(saga)
            await self._execute_next_step(saga)

    async def handle_step_failed(self, saga_id: str, step_name: str, error: str):
        """处理步骤失败——启动补偿。"""
        saga = await self.saga_store.get(saga_id)

        # 标记步骤为失败
        for step in saga.steps:
            if step.name == step_name:
                step.status = "failed"
                step.error = error
                break

        saga.state = SagaState.COMPENSATING
        saga.updated_at = datetime.utcnow()
        await self.saga_store.save(saga)

        # 从当前步骤向前反向执行补偿
        await self._compensate(saga)

    async def _execute_next_step(self, saga: Saga):
        """执行 Saga 中的下一个步骤。"""
        if saga.current_step >= len(saga.steps):
            return

        step = saga.steps[saga.current_step]
        step.status = "executing"
        await self.saga_store.save(saga)

        # 发布命令以执行步骤
        await self.event_publisher.publish(
            step.action,
            {
                "saga_id": saga.saga_id,
                "step_name": step.name,
                **saga.data
            }
        )

    async def _compensate(self, saga: Saga):
        """对已完成的步骤执行补偿。"""
        # 按反向顺序补偿
        for i in range(saga.current_step - 1, -1, -1):
            step = saga.steps[i]
            if step.status == "completed":
                step.status = "compensating"
                await self.saga_store.save(saga)

                await self.event_publisher.publish(
                    step.compensation,
                    {
                        "saga_id": saga.saga_id,
                        "step_name": step.name,
                        "original_result": step.result,
                        **saga.data
                    }
                )

    async def handle_compensation_completed(self, saga_id: str, step_name: str):
        """处理补偿完成。"""
        saga = await self.saga_store.get(saga_id)

        for step in saga.steps:
            if step.name == step_name:
                step.status = "compensated"
                step.compensated_at = datetime.utcnow()
                break

        # 检查是否所有补偿已完成
        all_compensated = all(
            s.status in ("compensated", "pending", "failed")
            for s in saga.steps
        )

        if all_compensated:
            saga.state = SagaState.FAILED
            await self._on_saga_failed(saga)

        await self.saga_store.save(saga)

    async def _on_saga_completed(self, saga: Saga):
        """Saga 成功完成时调用。"""
        await self.event_publisher.publish(
            f"{self.saga_type}Completed",
            {"saga_id": saga.saga_id, **saga.data}
        )

    async def _on_saga_failed(self, saga: Saga):
        """Saga 在补偿后失败时调用。"""
        await self.event_publisher.publish(
            f"{self.saga_type}Failed",
            {"saga_id": saga.saga_id, "error": "Saga failed", **saga.data}
        )
```

### 模板 2：订单履约 Saga

```python
class OrderFulfillmentSaga(SagaOrchestrator):
    """编排跨服务的订单履约流程。"""

    @property
    def saga_type(self) -> str:
        return "OrderFulfillment"

    def define_steps(self, data: Dict) -> List[SagaStep]:
        return [
            SagaStep(
                name="reserve_inventory",
                action="InventoryService.ReserveItems",
                compensation="InventoryService.ReleaseReservation"
            ),
            SagaStep(
                name="process_payment",
                action="PaymentService.ProcessPayment",
                compensation="PaymentService.RefundPayment"
            ),
            SagaStep(
                name="create_shipment",
                action="ShippingService.CreateShipment",
                compensation="ShippingService.CancelShipment"
            ),
            SagaStep(
                name="send_confirmation",
                action="NotificationService.SendOrderConfirmation",
                compensation="NotificationService.SendCancellationNotice"
            )
        ]


# 用法示例
async def create_order(order_data: Dict):
    saga = OrderFulfillmentSaga(saga_store, event_publisher)
    return await saga.start({
        "order_id": order_data["order_id"],
        "customer_id": order_data["customer_id"],
        "items": order_data["items"],
        "payment_method": order_data["payment_method"],
        "shipping_address": order_data["shipping_address"]
    })


# 各服务中的事件处理器
class InventoryService:
    async def handle_reserve_items(self, command: Dict):
        try:
            # 预留库存
            reservation = await self.reserve(
                command["items"],
                command["order_id"]
            )
            # 上报成功
            await self.event_publisher.publish(
                "SagaStepCompleted",
                {
                    "saga_id": command["saga_id"],
                    "step_name": "reserve_inventory",
                    "result": {"reservation_id": reservation.id}
                }
            )
        except InsufficientInventoryError as e:
            await self.event_publisher.publish(
                "SagaStepFailed",
                {
                    "saga_id": command["saga_id"],
                    "step_name": "reserve_inventory",
                    "error": str(e)
                }
            )

    async def handle_release_reservation(self, command: Dict):
        # 补偿操作
        await self.release_reservation(
            command["original_result"]["reservation_id"]
        )
        await self.event_publisher.publish(
            "SagaCompensationCompleted",
            {
                "saga_id": command["saga_id"],
                "step_name": "reserve_inventory"
            }
        )
```

### 模板 3：基于编舞的 Saga

```python
from dataclasses import dataclass
from typing import Dict, Any
import asyncio

@dataclass
class SagaContext:
    """在编舞式 Saga 事件间传递的上下文。"""
    saga_id: str
    step: int
    data: Dict[str, Any]
    completed_steps: list


class OrderChoreographySaga:
    """基于编舞模式的 Saga，使用事件驱动。"""

    def __init__(self, event_bus):
        self.event_bus = event_bus
        self._register_handlers()

    def _register_handlers(self):
        self.event_bus.subscribe("OrderCreated", self._on_order_created)
        self.event_bus.subscribe("InventoryReserved", self._on_inventory_reserved)
        self.event_bus.subscribe("PaymentProcessed", self._on_payment_processed)
        self.event_bus.subscribe("ShipmentCreated", self._on_shipment_created)

        # 补偿处理器
        self.event_bus.subscribe("PaymentFailed", self._on_payment_failed)
        self.event_bus.subscribe("ShipmentFailed", self._on_shipment_failed)

    async def _on_order_created(self, event: Dict):
        """步骤 1：订单已创建，预留库存。"""
        await self.event_bus.publish("ReserveInventory", {
            "saga_id": event["order_id"],
            "order_id": event["order_id"],
            "items": event["items"]
        })

    async def _on_inventory_reserved(self, event: Dict):
        """步骤 2：库存已预留，处理支付。"""
        await self.event_bus.publish("ProcessPayment", {
            "saga_id": event["saga_id"],
            "order_id": event["order_id"],
            "amount": event["total_amount"],
            "reservation_id": event["reservation_id"]
        })

    async def _on_payment_processed(self, event: Dict):
        """步骤 3：支付完成，创建发货单。"""
        await self.event_bus.publish("CreateShipment", {
            "saga_id": event["saga_id"],
            "order_id": event["order_id"],
            "payment_id": event["payment_id"]
        })

    async def _on_shipment_created(self, event: Dict):
        """步骤 4：完成——发送确认通知。"""
        await self.event_bus.publish("OrderFulfilled", {
            "saga_id": event["saga_id"],
            "order_id": event["order_id"],
            "tracking_number": event["tracking_number"]
        })

    # 补偿处理器
    async def _on_payment_failed(self, event: Dict):
        """支付失败——释放库存。"""
        await self.event_bus.publish("ReleaseInventory", {
            "saga_id": event["saga_id"],
            "reservation_id": event["reservation_id"]
        })
        await self.event_bus.publish("OrderFailed", {
            "order_id": event["order_id"],
            "reason": "Payment failed"
        })

    async def _on_shipment_failed(self, event: Dict):
        """发货失败——退款并释放库存。"""
        await self.event_bus.publish("RefundPayment", {
            "saga_id": event["saga_id"],
            "payment_id": event["payment_id"]
        })
        await self.event_bus.publish("ReleaseInventory", {
            "saga_id": event["saga_id"],
            "reservation_id": event["reservation_id"]
        })
```

### 模板 4：带超时的 Saga

```python
class TimeoutSagaOrchestrator(SagaOrchestrator):
    """带步骤超时的 Saga 编排器。"""

    def __init__(self, saga_store, event_publisher, scheduler):
        super().__init__(saga_store, event_publisher)
        self.scheduler = scheduler

    async def _execute_next_step(self, saga: Saga):
        if saga.current_step >= len(saga.steps):
            return

        step = saga.steps[saga.current_step]
        step.status = "executing"
        step.timeout_at = datetime.utcnow() + timedelta(minutes=5)
        await self.saga_store.save(saga)

        # 调度超时检查
        await self.scheduler.schedule(
            f"saga_timeout_{saga.saga_id}_{step.name}",
            self._check_timeout,
            {"saga_id": saga.saga_id, "step_name": step.name},
            run_at=step.timeout_at
        )

        await self.event_publisher.publish(
            step.action,
            {"saga_id": saga.saga_id, "step_name": step.name, **saga.data}
        )

    async def _check_timeout(self, data: Dict):
        """检查步骤是否已超时。"""
        saga = await self.saga_store.get(data["saga_id"])
        step = next(s for s in saga.steps if s.name == data["step_name"])

        if step.status == "executing":
            # 步骤已超时——标记为失败
            await self.handle_step_failed(
                data["saga_id"],
                data["step_name"],
                "Step timed out"
            )
```

## 持久执行替代方案

上述模板从零构建 Saga 基础设施——Saga 存储、事件发布器、补偿追踪。**持久执行框架**（如 DBOS）消除了大量此类样板代码：工作流运行时自动将状态持久化到数据库，重试失败的步骤，并在崩溃后从最近的检查点恢复。你无需构建 `SagaOrchestrator` 基类，只需编写一个带步骤的工作流函数——框架会处理持久化、崩溃恢复和精确一次执行语义。当你需要类 Saga 的可靠性而不想自己管理协调基础设施时，可以考虑使用持久执行框架。

## 最佳实践

### 推荐做法

- **步骤幂等化** — 确保可安全重试
- **精心设计补偿逻辑** — 补偿必须能正确执行
- **使用关联 ID** — 用于跨服务追踪
- **实现超时机制** — 不要无限等待
- **记录一切** — 便于排查故障

### 避免做法

- **不要假设即时完成** — Saga 需要时间
- **不要跳过补偿测试** — 这是最关键的部分
- **不要耦合服务** — 使用异步消息
- **不要忽略部分失败** — 优雅地处理

## 相关技能

配合使用效果更佳：`event-sourcing-architect`、`workflow-automation`、`dbos-*`

## 参考资源

- [Saga Pattern](https://microservices.io/patterns/data/saga.html)
- [Designing Data-Intensive Applications](https://dataintensive.net/)

## 使用限制

- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定的验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
