# 章节定义

本文件定义 DBOS Python 最佳实践的规则分类。规则会根据文件名前缀自动归入对应章节。

---

## 1. Lifecycle（lifecycle）
**影响等级：** CRITICAL
**说明：** DBOS 配置、初始化和启动模式。是所有 DBOS 应用的基石。

## 2. Workflow（workflow）
**影响等级：** CRITICAL
**说明：** 工作流的创建、确定性要求、后台执行以及工作流 ID。

## 3. Step（step）
**影响等级：** HIGH
**说明：** 步骤的创建、重试、事务，以及何时使用步骤、何时使用工作流。

## 4. Queue（queue）
**影响等级：** HIGH
**说明：** 队列的创建、并发限制、速率限制、分区和优先级。

## 5. Communication（comm）
**影响等级：** MEDIUM
**说明：** 工作流事件、消息和流，用于工作流之间的通信。

## 6. Pattern（pattern）
**影响等级：** MEDIUM
**说明：** 常用模式，包括幂等性、定时工作流、防抖和类。

## 7. Testing（test）
**影响等级：** LOW-MEDIUM
**说明：** 使用 pytest、fixtures 和最佳实践测试 DBOS 应用。

## 8. Client（client）
**影响等级：** MEDIUM
**说明：** DBOSClient，用于从外部应用与 DBOS 交互。

## 9. Advanced（advanced）
**影响等级：** LOW
**说明：** 异步工作流、工作流版本管理、补丁和代码升级。
