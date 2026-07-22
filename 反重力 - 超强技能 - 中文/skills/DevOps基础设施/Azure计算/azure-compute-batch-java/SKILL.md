---
name: azure-compute-batch-java
description: Azure Batch Java SDK，用于运行大规模并行和 HPC 批处理作业。支持池、作业、任务和计算节点管理。触发词：Azure Batch、批处理、HPC、并行计算、Java SDK、计算节点、作业调度、任务管理、Batch SDK、池管理、autoscale、低优先级节点
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure Batch SDK for Java

用于在 Azure 中运行大规模并行和高性能计算（HPC）批处理作业的客户端库。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-compute-batch</artifactId>
    <version>1.0.0-beta.5</version>
</dependency>
```

## 前提条件

- Azure Batch 账户
- 已配置计算节点的池
- Azure 订阅

## 环境变量

```bash
AZURE_BATCH_ENDPOINT=https://<account>.<region>.batch.azure.com
AZURE_BATCH_ACCOUNT=<account-name>
AZURE_BATCH_ACCESS_KEY=<account-key>
```

## 创建客户端

### 使用 Microsoft Entra ID（推荐）

```java
import com.azure.compute.batch.BatchClient;
import com.azure.compute.batch.BatchClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

BatchClient batchClient = new BatchClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(System.getenv("AZURE_BATCH_ENDPOINT"))
    .buildClient();
```

### 异步客户端

```java
import com.azure.compute.batch.BatchAsyncClient;

BatchAsyncClient batchAsyncClient = new BatchClientBuilder()
    .credential(new DefaultAzureCredentialBuilder().build())
    .endpoint(System.getenv("AZURE_BATCH_ENDPOINT"))
    .buildAsyncClient();
```

### 使用共享密钥凭据

```java
import com.azure.core.credential.AzureNamedKeyCredential;

String accountName = System.getenv("AZURE_BATCH_ACCOUNT");
String accountKey = System.getenv("AZURE_BATCH_ACCESS_KEY");
AzureNamedKeyCredential sharedKeyCreds = new AzureNamedKeyCredential(accountName, accountKey);

BatchClient batchClient = new BatchClientBuilder()
    .credential(sharedKeyCreds)
    .endpoint(System.getenv("AZURE_BATCH_ENDPOINT"))
    .buildClient();
```

## 核心概念

| 概念 | 描述 |
|---------|-------------|
| Pool（池） | 运行任务的计算节点集合 |
| Job（作业） | 任务的逻辑分组 |
| Task（任务） | 计算单元（命令/脚本） |
| Node（节点） | 执行任务的虚拟机 |
| Job Schedule（作业计划） | 定期创建作业 |

## 池操作

### 创建池

```java
import com.azure.compute.batch.models.*;

batchClient.createPool(new BatchPoolCreateParameters("myPoolId", "STANDARD_DC2s_V2")
    .setVirtualMachineConfiguration(
        new VirtualMachineConfiguration(
            new BatchVmImageReference()
                .setPublisher("Canonical")
                .setOffer("UbuntuServer")
                .setSku("22_04-lts")
                .setVersion("latest"),
            "batch.node.ubuntu 22.04"))
    .setTargetDedicatedNodes(2)
    .setTargetLowPriorityNodes(0), null);
```

### 获取池

```java
BatchPool pool = batchClient.getPool("myPoolId");
System.out.println("Pool state: " + pool.getState());
System.out.println("Current dedicated nodes: " + pool.getCurrentDedicatedNodes());
```

### 列出池

```java
import com.azure.core.http.rest.PagedIterable;

PagedIterable<BatchPool> pools = batchClient.listPools();
for (BatchPool pool : pools) {
    System.out.println("Pool: " + pool.getId() + ", State: " + pool.getState());
}
```

### 调整池大小

```java
import com.azure.core.util.polling.SyncPoller;

BatchPoolResizeParameters resizeParams = new BatchPoolResizeParameters()
    .setTargetDedicatedNodes(4)
    .setTargetLowPriorityNodes(2);

SyncPoller<BatchPool, BatchPool> poller = batchClient.beginResizePool("myPoolId", resizeParams);
poller.waitForCompletion();
BatchPool resizedPool = poller.getFinalResult();
```

### 启用自动缩放

```java
BatchPoolEnableAutoScaleParameters autoScaleParams = new BatchPoolEnableAutoScaleParameters()
    .setAutoScaleEvaluationInterval(Duration.ofMinutes(5))
    .setAutoScaleFormula("$TargetDedicatedNodes = min(10, $PendingTasks.GetSample(TimeInterval_Minute * 5));");

batchClient.enablePoolAutoScale("myPoolId", autoScaleParams);
```

### 删除池

```java
SyncPoller<BatchPool, Void> deletePoller = batchClient.beginDeletePool("myPoolId");
deletePoller.waitForCompletion();
```

## 作业操作

### 创建作业

```java
batchClient.createJob(
    new BatchJobCreateParameters("myJobId", new BatchPoolInfo().setPoolId("myPoolId"))
        .setPriority(100)
        .setConstraints(new BatchJobConstraints()
            .setMaxWallClockTime(Duration.ofHours(24))
            .setMaxTaskRetryCount(3)),
    null);
```

### 获取作业

```java
BatchJob job = batchClient.getJob("myJobId", null, null);
System.out.println("Job state: " + job.getState());
```

### 列出作业

```java
PagedIterable<BatchJob> jobs = batchClient.listJobs(new BatchJobsListOptions());
for (BatchJob job : jobs) {
    System.out.println("Job: " + job.getId() + ", State: " + job.getState());
}
```

### 获取任务计数

```java
BatchTaskCountsResult counts = batchClient.getJobTaskCounts("myJobId");
System.out.println("Active: " + counts.getTaskCounts().getActive());
System.out.println("Running: " + counts.getTaskCounts().getRunning());
System.out.println("Completed: " + counts.getTaskCounts().getCompleted());
```

### 终止作业

```java
BatchJobTerminateParameters terminateParams = new BatchJobTerminateParameters()
    .setTerminationReason("Manual termination");
BatchJobTerminateOptions options = new BatchJobTerminateOptions().setParameters(terminateParams);

SyncPoller<BatchJob, BatchJob> poller = batchClient.beginTerminateJob("myJobId", options, null);
poller.waitForCompletion();
```

### 删除作业

```java
SyncPoller<BatchJob, Void> deletePoller = batchClient.beginDeleteJob("myJobId");
deletePoller.waitForCompletion();
```

## 任务操作

### 创建单个任务

```java
BatchTaskCreateParameters task = new BatchTaskCreateParameters("task1", "echo 'Hello World'");
batchClient.createTask("myJobId", task);
```

### 创建带退出条件的任务

```java
batchClient.createTask("myJobId", new BatchTaskCreateParameters("task2", "cmd /c exit 3")
    .setExitConditions(new ExitConditions()
        .setExitCodeRanges(Arrays.asList(
            new ExitCodeRangeMapping(2, 4, 
                new ExitOptions().setJobAction(BatchJobActionKind.TERMINATE)))))
    .setUserIdentity(new UserIdentity()
        .setAutoUser(new AutoUserSpecification()
            .setScope(AutoUserScope.TASK)
            .setElevationLevel(ElevationLevel.NON_ADMIN))),
    null);
```

### 创建任务集合（最多100个）

```java
List<BatchTaskCreateParameters> taskList = Arrays.asList(
    new BatchTaskCreateParameters("task1", "echo Task 1"),
    new BatchTaskCreateParameters("task2", "echo Task 2"),
    new BatchTaskCreateParameters("task3", "echo Task 3")
);
BatchTaskGroup taskGroup = new BatchTaskGroup(taskList);
BatchCreateTaskCollectionResult result = batchClient.createTaskCollection("myJobId", taskGroup);
```

### 创建大量任务（无限制）

```java
List<BatchTaskCreateParameters> tasks = new ArrayList<>();
for (int i = 0; i < 1000; i++) {
    tasks.add(new BatchTaskCreateParameters("task" + i, "echo Task " + i));
}
batchClient.createTasks("myJobId", tasks);
```

### 获取任务

```java
BatchTask task = batchClient.getTask("myJobId", "task1");
System.out.println("Task state: " + task.getState());
System.out.println("Exit code: " + task.getExecutionInfo().getExitCode());
```

### 列出任务

```java
PagedIterable<BatchTask> tasks = batchClient.listTasks("myJobId");
for (BatchTask task : tasks) {
    System.out.println("Task: " + task.getId() + ", State: " + task.getState());
}
```

### 获取任务输出

```java
import com.azure.core.util.BinaryData;
import java.nio.charset.StandardCharsets;

BinaryData stdout = batchClient.getTaskFile("myJobId", "task1", "stdout.txt");
System.out.println(new String(stdout.toBytes(), StandardCharsets.UTF_8));
```

### 终止任务

```java
batchClient.terminateTask("myJobId", "task1", null, null);
```

## 节点操作

### 列出节点

```java
PagedIterable<BatchNode> nodes = batchClient.listNodes("myPoolId", new BatchNodesListOptions());
for (BatchNode node : nodes) {
    System.out.println("Node: " + node.getId() + ", State: " + node.getState());
}
```

### 重启节点

```java
SyncPoller<BatchNode, BatchNode> rebootPoller = batchClient.beginRebootNode("myPoolId", "nodeId");
rebootPoller.waitForCompletion();
```

### 获取远程登录设置

```java
BatchNodeRemoteLoginSettings settings = batchClient.getNodeRemoteLoginSettings("myPoolId", "nodeId");
System.out.println("IP: " + settings.getRemoteLoginIpAddress());
System.out.println("Port: " + settings.getRemoteLoginPort());
```

## 作业计划操作

### 创建作业计划

```java
batchClient.createJobSchedule(new BatchJobScheduleCreateParameters("myScheduleId",
    new BatchJobScheduleConfiguration()
        .setRecurrenceInterval(Duration.ofHours(6))
        .setDoNotRunUntil(OffsetDateTime.now().plusDays(1)),
    new BatchJobSpecification(new BatchPoolInfo().setPoolId("myPoolId"))
        .setPriority(50)),
    null);
```

### 获取作业计划

```java
BatchJobSchedule schedule = batchClient.getJobSchedule("myScheduleId");
System.out.println("Schedule state: " + schedule.getState());
```

## 错误处理

```java
import com.azure.compute.batch.models.BatchErrorException;
import com.azure.compute.batch.models.BatchError;

try {
    batchClient.getPool("nonexistent-pool");
} catch (BatchErrorException e) {
    BatchError error = e.getValue();
    System.err.println("Error code: " + error.getCode());
    System.err.println("Message: " + error.getMessage().getValue());
    
    if ("PoolNotFound".equals(error.getCode())) {
        System.err.println("The specified pool does not exist.");
    }
}
```

## 最佳实践

1. **使用 Entra ID** — 认证时优先选择而非共享密钥
2. **使用管理 SDK 管理池** — `azure-resourcemanager-batch` 支持托管标识
3. **批量创建任务** — 创建多个任务时使用 `createTaskCollection` 或 `createTasks`
4. **正确处理长时间运行操作** — 池调整大小、删除操作是长时间运行的
5. **监控任务计数** — 使用 `getJobTaskCounts` 跟踪进度
6. **设置约束** — 配置 `maxWallClockTime` 和 `maxTaskRetryCount`
7. **使用低优先级节点** — 为容错工作负载节省成本
8. **启用自动缩放** — 根据工作负载动态调整池大小

## 参考链接

| 资源 | URL |
|----------|-----|
| Maven 包 | https://central.sonatype.com/artifact/com.azure/azure-compute-batch |
| GitHub | https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/batch/azure-compute-batch |
| API 文档 | https://learn.microsoft.com/java/api/com.azure.compute.batch |
| 产品文档 | https://learn.microsoft.com/azure/batch/ |
| REST API | https://learn.microsoft.com/rest/api/batchservice/ |
| 示例 | https://github.com/azure/azure-batch-samples |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
