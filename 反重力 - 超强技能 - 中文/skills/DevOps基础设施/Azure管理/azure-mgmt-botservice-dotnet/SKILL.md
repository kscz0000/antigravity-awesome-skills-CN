---
name: azure-mgmt-botservice-dotnet
description: Azure Resource Manager SDK for Bot Service in .NET. 管理平面操作，用于创建和管理 Azure Bot 资源、通道（Teams、DirectLine、Slack）及连接设置。当用户要求'管理Azure Bot资源'、'配置Bot Service通道'、'创建Azure机器人'、'Azure Bot Service .NET SDK'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure.ResourceManager.BotService (.NET)

通过 Azure Resource Manager 预配和管理 Azure Bot Service 资源的管理平面 SDK。

## 安装

```bash
dotnet add package Azure.ResourceManager.BotService
dotnet add package Azure.Identity
```

**当前版本**：稳定版 v1.1.1，预览版 v1.1.0-beta.1

## 环境变量

```bash
AZURE_SUBSCRIPTION_ID=<your-subscription-id>
# For service principal auth (optional)
AZURE_TENANT_ID=<tenant-id>
AZURE_CLIENT_ID=<client-id>
AZURE_CLIENT_SECRET=<client-secret>
```

## 身份验证

```csharp
using Azure.Identity;
using Azure.ResourceManager;
using Azure.ResourceManager.BotService;

// Authenticate using DefaultAzureCredential
var credential = new DefaultAzureCredential();
ArmClient armClient = new ArmClient(credential);

// Get subscription and resource group
SubscriptionResource subscription = await armClient.GetDefaultSubscriptionAsync();
ResourceGroupResource resourceGroup = await subscription.GetResourceGroups().GetAsync("myResourceGroup");

// Access bot collection
BotCollection botCollection = resourceGroup.GetBots();
```

## 资源层级

```
ArmClient
└── SubscriptionResource
    └── ResourceGroupResource
        └── BotResource
            ├── BotChannelResource (DirectLine, Teams, Slack, etc.)
            ├── BotConnectionSettingResource (OAuth connections)
            └── BotServicePrivateEndpointConnectionResource
```

## 核心工作流

### 1. 创建 Bot 资源

```csharp
using Azure.ResourceManager.BotService;
using Azure.ResourceManager.BotService.Models;

// Create bot data
var botData = new BotData(AzureLocation.WestUS2)
{
    Kind = BotServiceKind.Azurebot,
    Sku = new BotServiceSku(BotServiceSkuName.F0),
    Properties = new BotProperties(
        displayName: "MyBot",
        endpoint: new Uri("https://mybot.azurewebsites.net/api/messages"),
        msaAppId: "<your-msa-app-id>")
    {
        Description = "My Azure Bot",
        MsaAppType = BotMsaAppType.MultiTenant
    }
};

// Create or update the bot
ArmOperation<BotResource> operation = await botCollection.CreateOrUpdateAsync(
    WaitUntil.Completed, 
    "myBotName", 
    botData);
    
BotResource bot = operation.Value;
Console.WriteLine($"Bot created: {bot.Data.Name}");
```

### 2. 配置 DirectLine 通道

```csharp
// Get the bot
BotResource bot = await resourceGroup.GetBots().GetAsync("myBotName");

// Get channel collection
BotChannelCollection channels = bot.GetBotChannels();

// Create DirectLine channel configuration
var channelData = new BotChannelData(AzureLocation.WestUS2)
{
    Properties = new DirectLineChannel()
    {
        Properties = new DirectLineChannelProperties()
        {
            Sites = 
            {
                new DirectLineSite("Default Site")
                {
                    IsEnabled = true,
                    IsV1Enabled = false,
                    IsV3Enabled = true,
                    IsSecureSiteEnabled = true
                }
            }
        }
    }
};

// Create or update the channel
ArmOperation<BotChannelResource> channelOp = await channels.CreateOrUpdateAsync(
    WaitUntil.Completed,
    BotChannelName.DirectLineChannel,
    channelData);

Console.WriteLine("DirectLine channel configured");
```

### 3. 配置 Microsoft Teams 通道

```csharp
var teamsChannelData = new BotChannelData(AzureLocation.WestUS2)
{
    Properties = new MsTeamsChannel()
    {
        Properties = new MsTeamsChannelProperties()
        {
            IsEnabled = true,
            EnableCalling = false
        }
    }
};

await channels.CreateOrUpdateAsync(
    WaitUntil.Completed,
    BotChannelName.MsTeamsChannel,
    teamsChannelData);
```

### 4. 配置 Web Chat 通道

```csharp
var webChatChannelData = new BotChannelData(AzureLocation.WestUS2)
{
    Properties = new WebChatChannel()
    {
        Properties = new WebChatChannelProperties()
        {
            Sites =
            {
                new WebChatSite("Default Site")
                {
                    IsEnabled = true
                }
            }
        }
    }
};

await channels.CreateOrUpdateAsync(
    WaitUntil.Completed,
    BotChannelName.WebChatChannel,
    webChatChannelData);
```

### 5. 获取 Bot 及列出通道

```csharp
// Get bot
BotResource bot = await botCollection.GetAsync("myBotName");
Console.WriteLine($"Bot: {bot.Data.Properties.DisplayName}");
Console.WriteLine($"Endpoint: {bot.Data.Properties.Endpoint}");

// List channels
await foreach (BotChannelResource channel in bot.GetBotChannels().GetAllAsync())
{
    Console.WriteLine($"Channel: {channel.Data.Name}");
}
```

### 6. 重新生成 DirectLine 密钥

```csharp
var regenerateRequest = new BotChannelRegenerateKeysContent(BotChannelName.DirectLineChannel)
{
    SiteName = "Default Site"
};

BotChannelResource channelWithKeys = await bot.GetBotChannelWithRegenerateKeysAsync(regenerateRequest);
```

### 7. 更新 Bot

```csharp
BotResource bot = await botCollection.GetAsync("myBotName");

// Update using patch
var updateData = new BotData(bot.Data.Location)
{
    Properties = new BotProperties(
        displayName: "Updated Bot Name",
        endpoint: bot.Data.Properties.Endpoint,
        msaAppId: bot.Data.Properties.MsaAppId)
    {
        Description = "Updated description"
    }
};

await bot.UpdateAsync(updateData);
```

### 8. 删除 Bot

```csharp
BotResource bot = await botCollection.GetAsync("myBotName");
await bot.DeleteAsync(WaitUntil.Completed);
```

## 支持的通道类型

| 通道 | 常量 | 类 |
|------|------|-----|
| Direct Line | `BotChannelName.DirectLineChannel` | `DirectLineChannel` |
| Direct Line Speech | `BotChannelName.DirectLineSpeechChannel` | `DirectLineSpeechChannel` |
| Microsoft Teams | `BotChannelName.MsTeamsChannel` | `MsTeamsChannel` |
| Web Chat | `BotChannelName.WebChatChannel` | `WebChatChannel` |
| Slack | `BotChannelName.SlackChannel` | `SlackChannel` |
| Facebook | `BotChannelName.FacebookChannel` | `FacebookChannel` |
| Email | `BotChannelName.EmailChannel` | `EmailChannel` |
| Telegram | `BotChannelName.TelegramChannel` | `TelegramChannel` |
| Telephony | `BotChannelName.TelephonyChannel` | `TelephonyChannel` |

## 关键类型参考

| 类型 | 用途 |
|------|------|
| `ArmClient` | 所有 ARM 操作的入口点 |
| `BotResource` | 表示 Azure Bot 资源 |
| `BotCollection` | Bot CRUD 操作集合 |
| `BotData` | Bot 资源定义 |
| `BotProperties` | Bot 配置属性 |
| `BotChannelResource` | 通道配置 |
| `BotChannelCollection` | 通道集合 |
| `BotChannelData` | 通道配置数据 |
| `BotConnectionSettingResource` | OAuth 连接设置 |

## BotServiceKind 值

| 值 | 说明 |
|----|------|
| `BotServiceKind.Azurebot` | Azure Bot（推荐） |
| `BotServiceKind.Bot` | 旧版 Bot Framework bot |
| `BotServiceKind.Designer` | Composer bot |
| `BotServiceKind.Function` | Function bot |
| `BotServiceKind.Sdk` | SDK bot |

## BotServiceSkuName 值

| 值 | 说明 |
|----|------|
| `BotServiceSkuName.F0` | 免费层 |
| `BotServiceSkuName.S1` | 标准层 |

## BotMsaAppType 值

| 值 | 说明 |
|----|------|
| `BotMsaAppType.MultiTenant` | 多租户应用 |
| `BotMsaAppType.SingleTenant` | 单租户应用 |
| `BotMsaAppType.UserAssignedMSI` | 用户分配的托管标识 |

## 最佳实践

1. **始终使用 `DefaultAzureCredential`** — 支持多种身份验证方式
2. **对同步操作使用 `WaitUntil.Completed`**
3. **处理 `RequestFailedException`** 以应对 API 错误
4. **对所有操作使用异步方法**（`*Async`）
5. **安全存储 MSA App 凭据** — 使用 Key Vault 保管密钥
6. **生产环境 Bot 使用托管标识**（`BotMsaAppType.UserAssignedMSI`）
7. **生产环境中为 DirectLine 通道启用安全站点**

## 错误处理

```csharp
using Azure;

try
{
    var operation = await botCollection.CreateOrUpdateAsync(
        WaitUntil.Completed, 
        botName, 
        botData);
}
catch (RequestFailedException ex) when (ex.Status == 409)
{
    Console.WriteLine("Bot already exists");
}
catch (RequestFailedException ex)
{
    Console.WriteLine($"ARM Error: {ex.Status} - {ex.ErrorCode}: {ex.Message}");
}
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Azure.ResourceManager.BotService` | Bot 管理（本 SDK） | `dotnet add package Azure.ResourceManager.BotService` |
| `Microsoft.Bot.Builder` | Bot Framework SDK | `dotnet add package Microsoft.Bot.Builder` |
| `Microsoft.Bot.Builder.Integration.AspNet.Core` | ASP.NET Core 集成 | `dotnet add package Microsoft.Bot.Builder.Integration.AspNet.Core` |

## 参考链接

| 资源 | URL |
|------|-----|
| NuGet 包 | https://www.nuget.org/packages/Azure.ResourceManager.BotService |
| API 参考 | https://learn.microsoft.com/dotnet/api/azure.resourcemanager.botservice |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/botservice/Azure.ResourceManager.BotService |
| Azure Bot Service 文档 | https://learn.microsoft.com/azure/bot-service/ |

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
