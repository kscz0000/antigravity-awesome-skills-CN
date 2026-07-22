---
name: m365-agents-dotnet
description: Microsoft 365 Agents SDK for .NET，用于构建面向 Teams/M365/Copilot Studio 的多通道智能体，支持 ASP.NET Core 托管、AgentApplication 路由和基于 MSAL 的认证。当用户要求'构建 Microsoft 365 智能体'、'开发 Teams Bot'、'集成 Copilot Studio'、'使用 .NET 开发 M365 Agent'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Microsoft 365 Agents SDK (.NET)

## 概述

使用 Microsoft.Agents SDK 构建 Microsoft 365、Teams 和 Copilot Studio 的企业级智能体，支持 ASP.NET Core 托管、智能体路由和基于 MSAL 的认证。

## 实现前准备

- 使用 microsoft-docs MCP 验证 AddAgent、AgentApplication 和认证选项的最新 API。
- 在 NuGet 上确认你计划使用的 Microsoft.Agents.* 包的版本。

## 安装

```bash
dotnet add package Microsoft.Agents.Hosting.AspNetCore
dotnet add package Microsoft.Agents.Authentication.Msal
dotnet add package Microsoft.Agents.Storage
dotnet add package Microsoft.Agents.CopilotStudio.Client
dotnet add package Microsoft.Identity.Client.Extensions.Msal
```

## 配置 (appsettings.json)

```json
{
  "TokenValidation": {
    "Enabled": true,
    "Audiences": [
      "{{ClientId}}"
    ],
    "TenantId": "{{TenantId}}"
  },
  "AgentApplication": {
    "StartTypingTimer": false,
    "RemoveRecipientMention": false,
    "NormalizeMentions": false
  },
  "Connections": {
    "ServiceConnection": {
      "Settings": {
        "AuthType": "ClientSecret",
        "ClientId": "{{ClientId}}",
        "ClientSecret": "{{ClientSecret}}",
        "AuthorityEndpoint": "https://login.microsoftonline.com/{{TenantId}}",
        "Scopes": [
          "https://api.botframework.com/.default"
        ]
      }
    }
  },
  "ConnectionsMap": [
    {
      "ServiceUrl": "*",
      "Connection": "ServiceConnection"
    }
  ],
  "CopilotStudioClientSettings": {
    "DirectConnectUrl": "",
    "EnvironmentId": "",
    "SchemaName": "",
    "TenantId": "",
    "AppClientId": "",
    "AppClientSecret": ""
  }
}
```

## 核心工作流：ASP.NET Core 智能体托管

```csharp
using Microsoft.Agents.Builder;
using Microsoft.Agents.Hosting.AspNetCore;
using Microsoft.Agents.Storage;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpClient();
builder.AddAgentApplicationOptions();
builder.AddAgent<MyAgent>();
builder.Services.AddSingleton<IStorage, MemoryStorage>();

builder.Services.AddControllers();
builder.Services.AddAgentAspNetAuthentication(builder.Configuration);

WebApplication app = builder.Build();

app.UseAuthentication();
app.UseAuthorization();

app.MapGet("/", () => "Microsoft Agents SDK Sample");

var incomingRoute = app.MapPost("/api/messages",
    async (HttpRequest request, HttpResponse response, IAgentHttpAdapter adapter, IAgent agent, CancellationToken ct) =>
    {
        await adapter.ProcessAsync(request, response, agent, ct);
    });

if (!app.Environment.IsDevelopment())
{
    incomingRoute.RequireAuthorization();
}
else
{
    app.Urls.Add("http://localhost:3978");
}

app.Run();
```

## AgentApplication 路由

```csharp
using Microsoft.Agents.Builder;
using Microsoft.Agents.Builder.App;
using Microsoft.Agents.Builder.State;
using Microsoft.Agents.Core.Models;
using System;
using System.Threading;
using System.Threading.Tasks;

public sealed class MyAgent : AgentApplication
{
    public MyAgent(AgentApplicationOptions options) : base(options)
    {
        OnConversationUpdate(ConversationUpdateEvents.MembersAdded, WelcomeAsync);
        OnActivity(ActivityTypes.Message, OnMessageAsync, rank: RouteRank.Last);
        OnTurnError(OnTurnErrorAsync);
    }

    private static async Task WelcomeAsync(ITurnContext turnContext, ITurnState turnState, CancellationToken ct)
    {
        foreach (ChannelAccount member in turnContext.Activity.MembersAdded)
        {
            if (member.Id != turnContext.Activity.Recipient.Id)
            {
                await turnContext.SendActivityAsync(
                    MessageFactory.Text("Welcome to the agent."),
                    ct);
            }
        }
    }

    private static async Task OnMessageAsync(ITurnContext turnContext, ITurnState turnState, CancellationToken ct)
    {
        await turnContext.SendActivityAsync(
            MessageFactory.Text($"You said: {turnContext.Activity.Text}"),
            ct);
    }

    private static async Task OnTurnErrorAsync(
        ITurnContext turnContext,
        ITurnState turnState,
        Exception exception,
        CancellationToken ct)
    {
        await turnState.Conversation.DeleteStateAsync(turnContext, ct);

        var endOfConversation = Activity.CreateEndOfConversationActivity();
        endOfConversation.Code = EndOfConversationCodes.Error;
        endOfConversation.Text = exception.Message;
        await turnContext.SendActivityAsync(endOfConversation, ct);
    }
}
```

## Copilot Studio 直连引擎客户端

### 用于令牌获取的 DelegatingHandler（交互式流程）

```csharp
using System.Net.Http.Headers;
using Microsoft.Agents.CopilotStudio.Client;
using Microsoft.Identity.Client;

internal sealed class AddTokenHandler : DelegatingHandler
{
    private readonly SampleConnectionSettings _settings;

    public AddTokenHandler(SampleConnectionSettings settings) : base(new HttpClientHandler())
    {
        _settings = settings;
    }

    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request,
        CancellationToken cancellationToken)
    {
        if (request.Headers.Authorization is null)
        {
            string[] scopes = [CopilotClient.ScopeFromSettings(_settings)];

            IPublicClientApplication app = PublicClientApplicationBuilder
                .Create(_settings.AppClientId)
                .WithAuthority(AadAuthorityAudience.AzureAdMyOrg)
                .WithTenantId(_settings.TenantId)
                .WithRedirectUri("http://localhost")
                .Build();

            AuthenticationResult authResponse;
            try
            {
                var account = (await app.GetAccountsAsync()).FirstOrDefault();
                authResponse = await app.AcquireTokenSilent(scopes, account).ExecuteAsync(cancellationToken);
            }
            catch (MsalUiRequiredException)
            {
                authResponse = await app.AcquireTokenInteractive(scopes).ExecuteAsync(cancellationToken);
            }

            request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", authResponse.AccessToken);
        }

        return await base.SendAsync(request, cancellationToken);
    }
}
```

### 使用 CopilotClient 的控制台托管

```csharp
using Microsoft.Agents.CopilotStudio.Client;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

HostApplicationBuilder builder = Host.CreateApplicationBuilder(args);

var settings = new SampleConnectionSettings(
    builder.Configuration.GetSection("CopilotStudioClientSettings"));

builder.Services.AddHttpClient("mcs").ConfigurePrimaryHttpMessageHandler(() =>
{
    return new AddTokenHandler(settings);
});

builder.Services
    .AddSingleton(settings)
    .AddTransient<CopilotClient>(sp =>
    {
        var logger = sp.GetRequiredService<ILoggerFactory>().CreateLogger<CopilotClient>();
        return new CopilotClient(settings, sp.GetRequiredService<IHttpClientFactory>(), logger, "mcs");
    });

IHost host = builder.Build();
var client = host.Services.GetRequiredService<CopilotClient>();

await foreach (var activity in client.StartConversationAsync(emitStartConversationEvent: true))
{
    Console.WriteLine(activity.Type);
}

await foreach (var activity in client.AskQuestionAsync("Hello!", null))
{
    Console.WriteLine(activity.Type);
}
```

## 最佳实践

1. 使用 AgentApplication 子类集中管理路由和错误处理。
2. MemoryStorage 仅用于开发环境；生产环境请使用持久化存储。
3. 生产环境中启用 TokenValidation，并在 /api/messages 上要求授权。
4. 将认证密钥保存在配置提供程序中（Key Vault、托管标识、环境变量）。
5. 通过 IHttpClientFactory 复用 HttpClient，并缓存 MSAL 令牌。
6. 优先使用异步处理程序，并将 CancellationToken 传递给 SDK 调用。

## 参考文件

| 文件 | 内容 |
| --- | --- |
| references/acceptance-criteria.md | 导入路径、托管管道、Copilot Studio 客户端模式、反模式 |

## 参考链接

| 资源 | URL |
| --- | --- |
| Microsoft 365 Agents SDK | https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/ |
| AddAgent API | https://learn.microsoft.com/en-us/dotnet/api/microsoft.agents.hosting.aspnetcore.servicecollectionextensions.addagent?view=m365-agents-sdk |
| AgentApplication API | https://learn.microsoft.com/en-us/dotnet/api/microsoft.agents.builder.app.agentapplication?view=m365-agents-sdk |
| 认证配置选项 | https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/microsoft-authentication-library-configuration-options |
| Copilot Studio 集成 | https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/integrate-with-mcs |
| GitHub 示例 | https://github.com/microsoft/agents |

## 使用时机

本技能适用于执行概述中描述的工作流或操作。

## 限制

- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
