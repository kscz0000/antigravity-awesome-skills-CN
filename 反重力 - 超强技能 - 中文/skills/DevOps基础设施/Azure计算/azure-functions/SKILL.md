---
name: azure-functions
description: Azure Functions 开发专家模式，包括独立工作器模型、Durable Functions 编排、冷启动优化和生产模式。涵盖 .NET、Python 和 Node.js 编程模型。当用户要求'Azure Functions 开发'、'Durable Functions 编排'、'Azure 无服务器'、'函数应用'时使用。
risk: none
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# Azure Functions

Azure Functions 开发专家模式，包括独立工作器模型、Durable Functions 编排、冷启动优化和生产模式。涵盖 .NET、Python 和 Node.js 编程模型。

## 模式

### 独立工作器模型 (.NET)

具有进程隔离的现代 .NET 执行模型

**何时使用**：构建新的 .NET Azure Functions 应用

### 模板

// Program.cs - Isolated Worker Model
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var host = new HostBuilder()
    .ConfigureFunctionsWorkerDefaults()
    .ConfigureServices(services =>
    {
        // Add Application Insights
        services.AddApplicationInsightsTelemetryWorkerService();
        services.ConfigureFunctionsApplicationInsights();

        // Add HttpClientFactory (prevents socket exhaustion)
        services.AddHttpClient();

        // Add your services
        services.AddSingleton<IMyService, MyService>();
    })
    .Build();

host.Run();

// HttpTriggerFunction.cs
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Extensions.Logging;

public class HttpTriggerFunction
{
    private readonly ILogger<HttpTriggerFunction> _logger;
    private readonly IMyService _service;

    public HttpTriggerFunction(
        ILogger<HttpTriggerFunction> logger,
        IMyService service)
    {
        _logger = logger;
        _service = service;
    }

    [Function("HttpTrigger")]
    public async Task<HttpResponseData> Run(
        [HttpTrigger(AuthorizationLevel.Function, "get", "post")] HttpRequestData req)
    {
        _logger.LogInformation("Processing request");

        try
        {
            var result = await _service.ProcessAsync(req);

            var response = req.CreateResponse(HttpStatusCode.OK);
            await response.WriteAsJsonAsync(result);
            return response;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error processing request");
            var response = req.CreateResponse(HttpStatusCode.InternalServerError);
            await response.WriteAsJsonAsync(new { error = "Internal server error" });
            return response;
        }
    }
}

### 注意事项

- 进程内模型已于 2026 年 11 月弃用
- 独立工作器支持 .NET 8、9、10 和 .NET Framework
- 完整的依赖注入支持
- 自定义中间件支持

### Node.js v4 编程模型

面向 TypeScript/JavaScript 的现代代码优先方法

**何时使用**：构建 Node.js Azure Functions

### 模板

// src/functions/httpTrigger.ts
import { app, HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";

export async function httpTrigger(
  request: HttpRequest,
  context: InvocationContext
): Promise<HttpResponseInit> {
  context.log(`Http function processed request for url "${request.url}"`);

  try {
    const name = request.query.get("name") || (await request.text()) || "world";

    return {
      status: 200,
      jsonBody: { message: `Hello, ${name}!` }
    };
  } catch (error) {
    context.error("Error processing request:", error);
    return {
      status: 500,
      jsonBody: { error: "Internal server error" }
    };
  }
}

// Register function with app object
app.http("httpTrigger", {
  methods: ["GET", "POST"],
  authLevel: "function",
  handler: httpTrigger
});

// Timer trigger example
app.timer("timerTrigger", {
  schedule: "0 */5 * * * *",  // Every 5 minutes
  handler: async (myTimer, context) => {
    context.log("Timer function executed at:", new Date().toISOString());
  }
});

// Blob trigger example
app.storageBlob("blobTrigger", {
  path: "samples-workitems/{name}",
  connection: "AzureWebJobsStorage",
  handler: async (blob, context) => {
    context.log(`Blob trigger processing: ${context.triggerMetadata.name}`);
    context.log(`Blob size: ${blob.length} bytes`);
  }
});

### 注意事项

- v4 模型以代码为中心，无需 function.json 文件
- 使用类似 Express.js 的 app 对象
- TypeScript 一等公民支持
- 所有触发器在代码中注册

### Python v2 编程模型

基于装饰器的 Python 函数方法

**何时使用**：构建 Python Azure Functions

### 模板

# function_app.py
import azure.functions as func
import logging
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="hello", methods=["GET", "POST"])
async def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    try:
        name = req.params.get("name")
        if not name:
            try:
                req_body = req.get_json()
                name = req_body.get("name")
            except ValueError:
                pass

        if name:
            return func.HttpResponse(
                json.dumps({"message": f"Hello, {name}!"}),
                mimetype="application/json"
            )
        else:
            return func.HttpResponse(
                json.dumps({"message": "Hello, World!"}),
                mimetype="application/json"
            )
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )

@app.timer_trigger(schedule="0 */5 * * * *", arg_name="myTimer")
def timer_trigger(myTimer: func.TimerRequest) -> None:
    logging.info("Timer trigger executed")

@app.blob_trigger(arg_name="myblob", path="samples-workitems/{name}",
                  connection="AzureWebJobsStorage")
def blob_trigger(myblob: func.InputStream):
    logging.info(f"Blob trigger: {myblob.name}, Size: {myblob.length} bytes")

@app.queue_trigger(arg_name="msg", queue_name="myqueue",
                   connection="AzureWebJobsStorage")
def queue_trigger(msg: func.QueueMessage) -> None:
    logging.info(f"Queue message: {msg.get_body().decode('utf-8')}")

### 注意事项

- v2 模型使用装饰器，无需 function.json 文件
- Python 始终以进程外方式运行（始终隔离）
- Python 需要 Linux 托管
- 支持异步函数

### Durable Functions - 函数链式调用

具有状态持久化的顺序执行

**何时使用**：需要带自动重试的顺序工作流

### 模板

// C# Isolated Worker - Function Chaining
using Microsoft.Azure.Functions.Worker;
using Microsoft.DurableTask;
using Microsoft.DurableTask.Client;

public class OrderWorkflow
{
    [Function("OrderOrchestrator")]
    public static async Task<OrderResult> RunOrchestrator(
        [OrchestrationTrigger] TaskOrchestrationContext context)
    {
        var order = context.GetInput<Order>();

        // Functions execute sequentially, state persisted between each
        var validated = await context.CallActivityAsync<ValidatedOrder>(
            "ValidateOrder", order);

        var payment = await context.CallActivityAsync<PaymentResult>(
            "ProcessPayment", validated);

        var shipped = await context.CallActivityAsync<ShippingResult>(
            "ShipOrder", new ShipRequest { Order = validated, Payment = payment });

        var notification = await context.CallActivityAsync<bool>(
            "SendNotification", shipped);

        return new OrderResult
        {
            OrderId = order.Id,
            Status = "Completed",
            TrackingNumber = shipped.TrackingNumber
        };
    }

    [Function("ValidateOrder")]
    public static async Task<ValidatedOrder> ValidateOrder(
        [ActivityTrigger] Order order, FunctionContext context)
    {
        var logger = context.GetLogger<OrderWorkflow>();
        logger.LogInformation("Validating order {OrderId}", order.Id);

        // Validation logic...
        return new ValidatedOrder { /* ... */ };
    }

    [Function("ProcessPayment")]
    public static async Task<PaymentResult> ProcessPayment(
        [ActivityTrigger] ValidatedOrder order, FunctionContext context)
    {
        // Payment processing with built-in retry...
        return new PaymentResult { /* ... */ };
    }

    [Function("OrderWorkflow_HttpStart")]
    public static async Task<HttpResponseData> HttpStart(
        [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequestData req,
        [DurableClient] DurableTaskClient client,
        FunctionContext context)
    {
        var order = await req.ReadFromJsonAsync<Order>();
        string instanceId = await client.ScheduleNewOrchestrationInstanceAsync(
            "OrderOrchestrator", order);

        return client.CreateCheckStatusResponse(req, instanceId);
    }
}

### 注意事项

- 活动之间状态自动持久化
- 瞬态故障自动重试
- 可在进程重启后存活
- 内置状态端点用于监控

### Durable Functions - 扇出/扇入

并行执行与结果聚合

**何时使用**：并行处理多个项目

### 模板

// C# Isolated Worker - Fan-Out/Fan-In
using Microsoft.Azure.Functions.Worker;
using Microsoft.DurableTask;

public class ParallelProcessing
{
    [Function("ProcessImagesOrchestrator")]
    public static async Task<ProcessingResult> RunOrchestrator(
        [OrchestrationTrigger] TaskOrchestrationContext context)
    {
        var images = context.GetInput<List<string>>();

        // Fan-out: Start all tasks in parallel
        var tasks = images.Select(image =>
            context.CallActivityAsync<ImageResult>("ProcessImage", image));

        // Fan-in: Wait for all tasks to complete
        var results = await Task.WhenAll(tasks);

        // Aggregate results
        var successful = results.Count(r => r.Success);
        var failed = results.Count(r => !r.Success);

        return new ProcessingResult
        {
            TotalProcessed = results.Length,
            Successful = successful,
            Failed = failed,
            Results = results.ToList()
        };
    }

    [Function("ProcessImage")]
    public static async Task<ImageResult> ProcessImage(
        [ActivityTrigger] string imageUrl, FunctionContext context)
    {
        var logger = context.GetLogger<ParallelProcessing>();
        logger.LogInformation("Processing image: {Url}", imageUrl);

        try
        {
            // Image processing logic...
            await Task.Delay(1000); // Simulated work

            return new ImageResult
            {
                Url = imageUrl,
                Success = true,
                ProcessedUrl = $"processed-{imageUrl}"
            };
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Failed to process {Url}", imageUrl);
            return new ImageResult { Url = imageUrl, Success = false };
        }
    }

    // Python equivalent
    // @app.orchestration_trigger(context_name="context")
    // def process_images_orchestrator(context: df.DurableOrchestrationContext):
    //     images = context.get_input()
    //
    //     # Fan-out: Create parallel tasks
    //     tasks = [context.call_activity("ProcessImage", img) for img in images]
    //
    //     # Fan-in: Wait for all
    //     results = yield context.task_all(tasks)
    //
    //     return {"processed": len(results), "results": results}
}

### 注意事项

- 独立任务并行执行
- 全部完成后聚合结果
- 内存高效 - 仅存储任务 ID
- 支持数千个并行活动

### 冷启动优化

最小化生产环境中的冷启动延迟

**何时使用**：需要生产环境中的快速响应时间

### 模板

// 1. Use Premium Plan with pre-warmed instances
// host.json
{
  "version": "2.0",
  "extensions": {
    "durableTask": {
      "hubName": "MyTaskHub"
    }
  },
  "functionTimeout": "00:30:00"
}

// 2. Add warmup trigger (Premium Plan)
[Function("Warmup")]
public static void Warmup(
    [WarmupTrigger] object warmupContext,
    FunctionContext context)
{
    var logger = context.GetLogger("Warmup");
    logger.LogInformation("Warmup trigger executed - initializing dependencies");

    // Pre-initialize expensive resources
    // Database connections, HttpClients, etc.
}

// 3. Use static/singleton clients with DI
public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        // HttpClientFactory prevents socket exhaustion
        services.AddHttpClient<IMyApiClient, MyApiClient>(client =>
        {
            client.BaseAddress = new Uri("https://api.example.com");
            client.Timeout = TimeSpan.FromSeconds(30);
        });

        // Singleton for expensive initialization
        services.AddSingleton<IExpensiveService>(sp =>
        {
            // Initialize once, reuse across invocations
            return new ExpensiveService();
        });
    }
}

// 4. Reduce package size
// .csproj - exclude unnecessary dependencies
<PropertyGroup>
  <PublishTrimmed>true</PublishTrimmed>
  <TrimMode>partial</TrimMode>
</PropertyGroup>

// 5. Run from package deployment
// Azure CLI
// az functionapp deployment source config-zip \
//   --resource-group myResourceGroup \
//   --name myFunctionApp \
//   --src myapp.zip \
//   --build-remote true

### 注意事项

- 所有区域/语言的冷启动改善约 53%
- 高级计划提供预预热实例
- 预热触发器在流量到达前初始化
- 包部署可减少冷启动

### 队列触发器与错误处理

带毒队列的可靠消息处理

**何时使用**：从 Azure Storage Queue 处理消息

### 模板

// C# Isolated Worker - Queue Trigger
using Microsoft.Azure.Functions.Worker;

public class QueueProcessor
{
    private readonly ILogger<QueueProcessor> _logger;
    private readonly IMyService _service;

    public QueueProcessor(ILogger<QueueProcessor> logger, IMyService service)
    {
        _logger = logger;
        _service = service;
    }

    [Function("ProcessQueueMessage")]
    public async Task Run(
        [QueueTrigger("myqueue-items", Connection = "AzureWebJobsStorage")]
        QueueMessage message)
    {
        _logger.LogInformation("Processing message: {Id}", message.MessageId);

        try
        {
            var payload = JsonSerializer.Deserialize<MyPayload>(message.Body);
            await _service.ProcessAsync(payload);

            _logger.LogInformation("Message processed successfully: {Id}", message.MessageId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error processing message: {Id}", message.MessageId);

            // Message will be retried up to maxDequeueCount (default 5)
            // Then moved to poison queue: myqueue-items-poison
            throw;
        }
    }

    // Optional: Monitor poison queue
    [Function("ProcessPoisonQueue")]
    public async Task ProcessPoison(
        [QueueTrigger("myqueue-items-poison", Connection = "AzureWebJobsStorage")]
        QueueMessage message)
    {
        _logger.LogWarning("Processing poison message: {Id}", message.MessageId);

        // Log to monitoring, alert, or store for manual review
        await _service.HandlePoisonMessageAsync(message);
    }
}

// host.json - Queue configuration
// {
//   "version": "2.0",
//   "extensions": {
//     "queues": {
//       "maxPollingInterval": "00:00:02",
//       "visibilityTimeout": "00:00:30",
//       "batchSize": 16,
//       "maxDequeueCount": 5,
//       "newBatchThreshold": 8
//     }
//   }
// }

### 注意事项

- 消息重试最多 maxDequeueCount 次
- 失败消息移至毒队列
- 配置 visibilityTimeout 以适应处理时间
- batchSize 控制并行处理数量

### HTTP 触发器与长时间运行模式

处理超过 230 秒 HTTP 限制的工作

**何时使用**：HTTP 请求触发长时间运行的工作

### 模板

// Async HTTP pattern - return immediately, poll for status
[Function("StartLongRunning")]
public static async Task<HttpResponseData> StartLongRunning(
    [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequestData req,
    [DurableClient] DurableTaskClient client,
    FunctionContext context)
{
    var input = await req.ReadFromJsonAsync<WorkRequest>();

    // Start orchestration (returns immediately)
    string instanceId = await client.ScheduleNewOrchestrationInstanceAsync(
        "LongRunningOrchestrator", input);

    // Return status URLs for polling
    return client.CreateCheckStatusResponse(req, instanceId);
}

// Response includes:
// {
//   "id": "abc123",
//   "statusQueryGetUri": "https://.../instances/abc123",
//   "sendEventPostUri": "https://.../instances/abc123/raiseEvent/{eventName}",
//   "terminatePostUri": "https://.../instances/abc123/terminate"
// }

// Alternative: Queue-based pattern without Durable Functions
[Function("StartWork")]
[QueueOutput("work-queue")]
public static async Task<WorkItem> StartWork(
    [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequestData req,
    FunctionContext context)
{
    var input = await req.ReadFromJsonAsync<WorkRequest>();
    var workId = Guid.NewGuid().ToString();

    // Queue the work, return immediately
    var workItem = new WorkItem
    {
        Id = workId,
        Request = input
    };

    // Return work ID for status checking
    var response = req.CreateResponse(HttpStatusCode.Accepted);
    await response.WriteAsJsonAsync(new
    {
        workId = workId,
        statusUrl = $"/api/status/{workId}"
    });

    return workItem;
}

[Function("ProcessWork")]
public static async Task ProcessWork(
    [QueueTrigger("work-queue")] WorkItem work,
    FunctionContext context)
{
    // Long-running processing here
    // Update status in storage for polling
}

### 注意事项

- HTTP 超时为 230 秒，与计划无关
- 使用 Durable Functions 实现异步模式
- 立即返回并提供状态端点
- 客户端轮询等待完成

## 常见陷阱

### HTTP 超时为 230 秒，与计划无关

严重程度：高

场景：具有长处理时间的 HTTP 触发函数

症状：
约 4 分钟后出现 504 网关超时。
请求在函数完成前终止。
即使函数继续运行，客户端也会收到超时。
host.json 超时设置对 HTTP 无效。

为何会出问题：
Azure 负载均衡器对 HTTP 请求有硬编码的 230 秒空闲超时。
这适用于你的函数应用超时设置，无论怎样设置都一样。

即使你在 host.json 中将 functionTimeout 设为 30 分钟，HTTP 触发器
从客户端角度来看仍会在 230 秒后超时。

函数可能在超时后继续运行，但客户端不会收到响应。

推荐修复方案：

## 使用 Durable Functions 的异步模式

```csharp
[Function("StartLongProcess")]
public static async Task<HttpResponseData> Start(
    [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequestData req,
    [DurableClient] DurableTaskClient client)
{
    var input = await req.ReadFromJsonAsync<WorkRequest>();

    // Start orchestration, returns immediately
    string instanceId = await client.ScheduleNewOrchestrationInstanceAsync(
        "LongRunningOrchestrator", input);

    // Returns status URLs for polling
    return client.CreateCheckStatusResponse(req, instanceId);
}

// Client polls statusQueryGetUri until complete
```

## 使用基于队列的异步模式

```csharp
[Function("StartWork")]
public static async Task<HttpResponseData> StartWork(
    [HttpTrigger(AuthorizationLevel.Function, "post")] HttpRequestData req,
    [QueueOutput("work-queue")] out WorkItem workItem)
{
    var workId = Guid.NewGuid().ToString();

    workItem = new WorkItem { Id = workId, /* ... */ };

    var response = req.CreateResponse(HttpStatusCode.Accepted);
    await response.WriteAsJsonAsync(new {
        id = workId,
        statusUrl = $"/api/status/{workId}"
    });
    return response;
}
```

## 使用 Webhook 回调模式

```csharp
// Client provides callback URL
// Function queues work, returns 202 Accepted
// When done, POST result to callback URL
```

### HttpClient 实例化导致套接字耗尽

严重程度：高

场景：在函数代码中创建 HttpClient 实例

症状：
SocketException："Unable to connect to remote server"
"An attempt was made to access a socket in a way forbidden"
负载下出现间歇性连接失败。
本地正常但生产环境失败。

为何会出问题：
为每个请求创建新的 HttpClient 会创建新的套接字连接。
套接字关闭后在 TIME_WAIT 状态下会停留 240 秒。

在高吞吐量的无服务器环境中，你会快速耗尽可用套接字。
这影响所有网络客户端，不仅仅是 HttpClient。

Azure Functions 在多个客户之间共享网络资源，
使得这个问题更加严重。

推荐修复方案：

## 使用 IHttpClientFactory（推荐）

```csharp
// Program.cs
var host = new HostBuilder()
    .ConfigureFunctionsWorkerDefaults()
    .ConfigureServices(services =>
    {
        services.AddHttpClient<IMyApiClient, MyApiClient>(client =>
        {
            client.BaseAddress = new Uri("https://api.example.com");
            client.Timeout = TimeSpan.FromSeconds(30);
        });
    })
    .Build();

// MyApiClient.cs
public class MyApiClient : IMyApiClient
{
    private readonly HttpClient _client;

    public MyApiClient(HttpClient client)
    {
        _client = client;  // Injected, managed by factory
    }

    public async Task<string> GetDataAsync()
    {
        return await _client.GetStringAsync("/data");
    }
}
```

## 使用静态客户端（替代方案）

```csharp
public static class MyFunction
{
    // Static HttpClient, reused across invocations
    private static readonly HttpClient _httpClient = new HttpClient
    {
        Timeout = TimeSpan.FromSeconds(30)
    };

    [Function("MyFunction")]
    public static async Task Run(...)
    {
        var result = await _httpClient.GetAsync("...");
    }
}
```

## Azure SDK 客户端同样适用此模式

```csharp
// Also applies to:
// - BlobServiceClient
// - CosmosClient
// - ServiceBusClient
// Use DI or static instances
```

### 阻塞异步调用导致线程饥饿

严重程度：高

场景：在异步代码中使用 .Result、.Wait() 或 Thread.Sleep

症状：
负载下出现死锁。
请求无限挂起。
"A task was canceled" 异常。
低并发正常，高并发失败。

为何会出问题：
Azure Functions 线程池有限。阻塞调用（.Result、.Wait()）
在等待时占用线程，阻止其他工作。

Thread.Sleep 阻塞了本可处理其他请求的线程。

在多个并发执行下，你会快速耗尽线程，
导致死锁和超时。

推荐修复方案：

## 始终使用 async/await

```csharp
// BAD - blocks thread
var result = httpClient.GetAsync(url).Result;
someTask.Wait();
Thread.Sleep(5000);

// GOOD - yields thread
var result = await httpClient.GetAsync(url);
await someTask;
await Task.Delay(5000);
```

## 修复同步方法调用

```csharp
// BAD - sync over async
public void ProcessData()
{
    var data = GetDataAsync().Result;  // Blocks!
}

// GOOD - async all the way
public async Task ProcessDataAsync()
{
    var data = await GetDataAsync();
}
```

## 在控制台/启动中配置异步

```csharp
// If you must call async from sync context
public static void Main(string[] args)
{
    // Use GetAwaiter().GetResult() at entry point only
    MainAsync(args).GetAwaiter().GetResult();
}

private static async Task MainAsync(string[] args)
{
    // Async code here
}
```

### 消耗计划 10 分钟超时限制

严重程度：中

场景：在消耗计划上运行长时间进程

症状：
函数在 10 分钟后终止。
日志中出现"Function timed out"。
处理未完成但未捕获错误。
开发环境正常（超时更长）但生产环境失败。

为何会出问题：
消耗计划有 10 分钟执行时间的硬性限制。
如未配置，默认为 5 分钟。

消耗计划上无法增加到超过 10 分钟。
长时间运行的工作需要高级计划或不同的架构。

推荐修复方案：

## 配置最大超时（消耗计划）

```json
// host.json
{
  "version": "2.0",
  "functionTimeout": "00:10:00"  // Max for Consumption
}
```

## 升级到高级计划以获得更长超时

```json
// Premium plan - 30 min default, unbounded available
{
  "version": "2.0",
  "functionTimeout": "00:30:00"  // Or remove for unbounded
}
```

## 使用 Durable Functions 处理长时间工作流

```csharp
[Function("LongWorkflowOrchestrator")]
public static async Task<string> RunOrchestrator(
    [OrchestrationTrigger] TaskOrchestrationContext context)
{
    // Each activity has its own timeout
    // Workflow can run for days
    await context.CallActivityAsync("Step1", input);
    await context.CallActivityAsync("Step2", input);
    await context.CallActivityAsync("Step3", input);
    return "Complete";
}
```

## 将工作拆分为更小的块

```csharp
// Queue-based chunking
[Function("ProcessChunk")]
[QueueOutput("work-queue")]
public static IEnumerable<WorkChunk> ProcessChunk(
    [QueueTrigger("work-queue")] WorkChunk chunk)
{
    var results = Process(chunk);

    // Queue next chunks if more work
    if (chunk.HasMore)
    {
        yield return chunk.Next();
    }
}
```

### .NET 进程内模型已于 2026 年 11 月弃用

严重程度：高

场景：创建新的 .NET 函数或维护现有函数

症状：
在新项目中使用进程内模型。
与宿主运行时的依赖冲突。
无法使用最新 .NET 版本。
未来迁移负担。

为何会出问题：
进程内模型将你的代码运行在与 Azure Functions 宿主相同的进程中。这会导致：
- 程序集版本冲突
- 仅限于 LTS .NET 版本
- 无法使用最新 .NET 特性
- 与宿主运行时紧密耦合

支持将于 2026 年 11 月 10 日结束。此后，进程内应用
可能停止工作或不再接收安全更新。

推荐修复方案：

## 新项目使用独立工作器

```bash
# Create new isolated worker project
func init MyFunctionApp --worker-runtime dotnet-isolated

# Or with .NET 8
dotnet new func --name MyFunctionApp --framework net8.0
```

## 将现有进程内模型迁移到独立工作器

```csharp
// OLD - In-process (FunctionName attribute)
public class InProcessFunction
{
    [FunctionName("MyFunction")]
    public async Task<IActionResult> Run(
        [HttpTrigger] HttpRequest req,
        ILogger log)
    {
        log.LogInformation("Processing");
        return new OkResult();
    }
}

// NEW - Isolated worker (Function attribute)
public class IsolatedFunction
{
    private readonly ILogger<IsolatedFunction> _logger;

    public IsolatedFunction(ILogger<IsolatedFunction> logger)
    {
        _logger = logger;
    }

    [Function("MyFunction")]
    public async Task<HttpResponseData> Run(
        [HttpTrigger(AuthorizationLevel.Function, "get")]
        HttpRequestData req)
    {
        _logger.LogInformation("Processing");
        return req.CreateResponse(HttpStatusCode.OK);
    }
}
```

## 关键迁移变更
- FunctionName → Function 特性
- HttpRequest → HttpRequestData
- IActionResult → HttpResponseData
- ILogger 注入 → 构造函数注入
- 添加带 HostBuilder 的 Program.cs

### ILogger 未输出到控制台或 AppInsights

严重程度：中

场景：在独立工作器中使用依赖注入的 ILogger

症状：
日志未出现在本地控制台。
日志未出现在 Application Insights。
使用 context.GetLogger() 日志正常，但注入的 ILogger 不行。
必须通过所有方法调用传递日志器。

为何会出问题：
在独立工作器模型中，依赖注入的 ILogger 可能未正确
连接到 Azure Functions 日志管道。

本地开发尤其受影响 - 日志可能无处输出。
Application Insights 需要显式配置。

来自 FunctionContext 的 ILogger 与注入的 ILogger<T> 工作方式不同。

推荐修复方案：

## 正确配置 Application Insights

```csharp
// Program.cs
var host = new HostBuilder()
    .ConfigureFunctionsWorkerDefaults()
    .ConfigureServices(services =>
    {
        // Add App Insights telemetry
        services.AddApplicationInsightsTelemetryWorkerService();
        services.ConfigureFunctionsApplicationInsights();
    })
    .Build();
```

## 配置日志级别

```json
// host.json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      }
    },
    "logLevel": {
      "default": "Information",
      "Host.Results": "Error",
      "Function": "Information",
      "Host.Aggregator": "Trace"
    }
  }
}
```

## 使用 context.GetLogger 确保可靠性

```csharp
[Function("MyFunction")]
public async Task Run(
    [HttpTrigger] HttpRequestData req,
    FunctionContext context)
{
    // This logger always works
    var logger = context.GetLogger<MyFunction>();
    logger.LogInformation("Processing request");
}
```

## 本地开发 - 检查 local.settings.json

```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "dotnet-isolated",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "APPLICATIONINSIGHTS_CONNECTION_STRING": "InstrumentationKey=..."
  }
}
```

### 缺少扩展包导致静默失败

严重程度：中

场景：使用触发器/绑定但未安装扩展

症状：
函数未在事件上触发。
"No job functions found" 警告。
配置正确但绑定不工作。
添加扩展包后正常工作。

为何会出问题：
Azure Functions v2+ 使用扩展包来处理触发器和绑定。
如果扩展未正确配置或包未安装，
函数宿主无法识别绑定。

在独立工作器中，需要显式 NuGet 包。
在进程内模型中，需要 Microsoft.Azure.WebJobs.Extensions.*。

推荐修复方案：

## 检查扩展包（最常见）

```json
// host.json - Extension bundles handle most cases
{
  "version": "2.0",
  "extensionBundle": {
    "id": "Microsoft.Azure.Functions.ExtensionBundle",
    "version": "[4.*, 5.0.0)"
  }
}
```

## 为独立工作器安装显式包

```xml
<!-- .csproj - Isolated worker packages -->
<PackageReference Include="Microsoft.Azure.Functions.Worker" Version="1.20.0" />
<PackageReference Include="Microsoft.Azure.Functions.Worker.Sdk" Version="1.16.0" />

<!-- Storage triggers/bindings -->
<PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.Storage" Version="6.2.0" />

<!-- Service Bus -->
<PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.ServiceBus" Version="5.14.0" />

<!-- Cosmos DB -->
<PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.CosmosDB" Version="4.6.0" />

<!-- Durable Functions -->
<PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.DurableTask" Version="1.1.0" />
```

## 验证函数注册

```bash
# Check registered functions
func host start --verbose

# Look for:
# "Found the following functions:"
# If empty, check extensions and attributes
```

### 高级计划在新实例上仍有冷启动

严重程度：中

场景：使用高级计划期望零冷启动

症状：
尽管使用高级计划仍出现冷启动。
新实例的首个请求较慢。
扩展事件期间的延迟峰值。
预预热实例未被使用。

为何会出问题：
高级计划提供预预热实例，但：
- 默认只有一个预预热实例
- 快速扩展仍会创建冷实例
- 预预热实例仍需运行你的代码初始化
- 预热触发器运行了，但你的代码可能仍然较慢

预预热意味着运行时已就绪，而非你的应用程序已就绪。

推荐修复方案：

## 添加预热触发器以初始化代码

```csharp
[Function("Warmup")]
public void Warmup(
    [WarmupTrigger] object warmupContext,
    FunctionContext context)
{
    var logger = context.GetLogger("Warmup");
    logger.LogInformation("Warmup trigger fired");

    // Initialize expensive resources
    _cosmosClient.GetContainer("db", "container");
    _httpClient.GetAsync("https://api.example.com/health").Wait();
}
```

## 配置预预热实例数量

```bash
# Increase pre-warmed instances (costs more)
az functionapp config set \
  --name <app-name> \
  --resource-group <rg> \
  --prewarmed-instance-count 3
```

## 优化应用初始化

```csharp
// Lazy initialize heavy resources
private static readonly Lazy<ExpensiveClient> _client =
    new Lazy<ExpensiveClient>(() => new ExpensiveClient());

// Connection pooling
services.AddDbContext<MyDbContext>(options =>
    options.UseSqlServer(connectionString, sql =>
        sql.MinPoolSize(5)));
```

## 使用始终就绪实例（最昂贵）

```bash
# Instances always running, no cold start
az functionapp config set \
  --name <app-name> \
  --resource-group <rg> \
  --minimum-elastic-instance-count 2
```

## 验证检查

### 硬编码连接字符串

严重程度：错误

连接字符串绝不能硬编码

消息：硬编码的连接字符串。请使用 Key Vault 或应用设置。

### 代码中硬编码 API 密钥

严重程度：错误

API 密钥应使用 Key Vault 或应用设置

消息：硬编码的 API 密钥。请使用 Key Vault 或环境变量。

### 生产环境中的匿名授权级别

严重程度：警告

匿名端点应通过其他方式保护

消息：匿名授权。确保通过 API 管理或其他认证方式保护。

### 阻塞式 .Result 调用

严重程度：错误

使用 .Result 会阻塞线程并导致死锁

消息：阻塞式 .Result 调用。请改用 await。

### 阻塞式 .Wait() 调用

严重程度：错误

使用 .Wait() 会阻塞线程

消息：阻塞式 .Wait() 调用。请改用 await。

### Thread.Sleep 使用

严重程度：错误

Thread.Sleep 会阻塞线程

消息：Thread.Sleep 阻塞线程。请改用 await Task.Delay()。

### 新建 HttpClient 实例

严重程度：警告

每次请求创建 HttpClient 会导致套接字耗尽

消息：每次请求新建 HttpClient。请使用 IHttpClientFactory 或静态客户端。

### using 语句中的 HttpClient

严重程度：警告

释放 HttpClient 会导致套接字耗尽

消息：using 语句中的 HttpClient。请使用 IHttpClientFactory 进行正确的生命周期管理。

### 进程内 FunctionName 特性

严重程度：信息

进程内模型已于 2026 年 11 月弃用

消息：进程内 FunctionName 特性。请考虑迁移到独立工作器。

### 缺少 Function 特性

严重程度：警告

独立工作器需要 [Function] 特性

消息：HttpTrigger 缺少 [Function] 特性（独立工作器需要它）。

## 协作

### 委派触发器

- 用户需要 AWS 无服务器 -> aws-serverless（Lambda、API Gateway、SAM）
- 用户需要 GCP 无服务器 -> gcp-cloud-run（Cloud Run、Cloud Functions）
- 用户需要基于容器的部署 -> gcp-cloud-run（Azure Container Apps 或 Cloud Run）
- 用户需要数据库设计 -> postgres-wizard（Azure SQL、Cosmos DB 数据建模）
- 用户需要认证 -> auth-specialist（Azure AD、Easy Auth、托管标识）
- 用户需要复杂编排 -> workflow-automation（Logic Apps、Power Automate）

## 何时使用
- 用户提及或暗示：azure function
- 用户提及或暗示：azure functions
- 用户提及或暗示：durable functions
- 用户提及或暗示：azure serverless
- 用户提及或暗示：function app

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
