---
name: microsoft-azure-webjobs-extensions-authentication-events-dotnet
description: Microsoft Entra 身份验证事件 .NET SDK，提供 Azure Functions 自定义身份验证扩展触发器。当用户要求'Entra认证事件'、'自定义认证扩展'、'Token签发事件'、'属性收集事件'、'OTP自定义发送'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents (.NET)

Azure Functions 扩展，用于处理 Microsoft Entra ID 自定义身份验证事件。

## 安装

```bash
dotnet add package Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents
```

**当前版本**：v1.1.0（稳定版）

## 支持的事件

| 事件 | 用途 |
|------|------|
| `OnTokenIssuanceStart` | 在签发阶段向令牌添加自定义声明 |
| `OnAttributeCollectionStart` | 在展示前自定义属性收集界面 |
| `OnAttributeCollectionSubmit` | 用户提交后验证/修改属性 |
| `OnOtpSend` | 自定义 OTP 投递（短信、邮件等） |

## 核心工作流

### 1. 令牌增强（添加自定义声明）

登录时向访问令牌或 ID 令牌添加自定义声明。

```csharp
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents;
using Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents.TokenIssuanceStart;
using Microsoft.Extensions.Logging;

public static class TokenEnrichmentFunction
{
    [FunctionName("OnTokenIssuanceStart")]
    public static WebJobsAuthenticationEventResponse Run(
        [WebJobsAuthenticationEventsTrigger] WebJobsTokenIssuanceStartRequest request,
        ILogger log)
    {
        log.LogInformation("Token issuance event for user: {UserId}", 
            request.Data?.AuthenticationContext?.User?.Id);

        // Create response with custom claims
        var response = new WebJobsTokenIssuanceStartResponse();
        
        // Add claims to the token
        response.Actions.Add(new WebJobsProvideClaimsForToken
        {
            Claims = new Dictionary<string, string>
            {
                { "customClaim1", "customValue1" },
                { "department", "Engineering" },
                { "costCenter", "CC-12345" },
                { "apiVersion", "v2" }
            }
        });

        return response;
    }
}
```

### 2. 结合外部数据的令牌增强

从外部系统（数据库、API）获取声明。

```csharp
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents;
using Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents.TokenIssuanceStart;
using Microsoft.Extensions.Logging;
using System.Net.Http;
using System.Text.Json;

public static class TokenEnrichmentWithExternalData
{
    private static readonly HttpClient _httpClient = new();

    [FunctionName("OnTokenIssuanceStartExternal")]
    public static async Task<WebJobsAuthenticationEventResponse> Run(
        [WebJobsAuthenticationEventsTrigger] WebJobsTokenIssuanceStartRequest request,
        ILogger log)
    {
        string? userId = request.Data?.AuthenticationContext?.User?.Id;
        
        if (string.IsNullOrEmpty(userId))
        {
            log.LogWarning("No user ID in request");
            return new WebJobsTokenIssuanceStartResponse();
        }

        // Fetch user data from external API
        var userProfile = await GetUserProfileAsync(userId);
        
        var response = new WebJobsTokenIssuanceStartResponse();
        response.Actions.Add(new WebJobsProvideClaimsForToken
        {
            Claims = new Dictionary<string, string>
            {
                { "employeeId", userProfile.EmployeeId },
                { "department", userProfile.Department },
                { "roles", string.Join(",", userProfile.Roles) }
            }
        });

        return response;
    }

    private static async Task<UserProfile> GetUserProfileAsync(string userId)
    {
        var response = await _httpClient.GetAsync($"https://api.example.com/users/{userId}");
        response.EnsureSuccessStatusCode();
        var json = await response.Content.ReadAsStringAsync();
        return JsonSerializer.Deserialize<UserProfile>(json)!;
    }
}

public record UserProfile(string EmployeeId, string Department, string[] Roles);
```

### 3. 属性收集 — 自定义界面（Start 事件）

在属性收集页面展示前进行自定义。

```csharp
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents;
using Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents.Framework;
using Microsoft.Extensions.Logging;

public static class AttributeCollectionStartFunction
{
    [FunctionName("OnAttributeCollectionStart")]
    public static WebJobsAuthenticationEventResponse Run(
        [WebJobsAuthenticationEventsTrigger] WebJobsAttributeCollectionStartRequest request,
        ILogger log)
    {
        log.LogInformation("Attribute collection start for correlation: {CorrelationId}",
            request.Data?.AuthenticationContext?.CorrelationId);

        var response = new WebJobsAttributeCollectionStartResponse();

        // Option 1: Continue with default behavior
        response.Actions.Add(new WebJobsContinueWithDefaultBehavior());

        // Option 2: Prefill attributes
        // response.Actions.Add(new WebJobsSetPrefillValues
        // {
        //     Attributes = new Dictionary<string, string>
        //     {
        //         { "city", "Seattle" },
        //         { "country", "USA" }
        //     }
        // });

        // Option 3: Show blocking page (prevent sign-up)
        // response.Actions.Add(new WebJobsShowBlockPage
        // {
        //     Message = "Sign-up is currently disabled."
        // });

        return response;
    }
}
```

### 4. 属性收集 — 验证提交（Submit 事件）

用户提交后验证并修改属性。

```csharp
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents;
using Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents.Framework;
using Microsoft.Extensions.Logging;

public static class AttributeCollectionSubmitFunction
{
    [FunctionName("OnAttributeCollectionSubmit")]
    public static WebJobsAuthenticationEventResponse Run(
        [WebJobsAuthenticationEventsTrigger] WebJobsAttributeCollectionSubmitRequest request,
        ILogger log)
    {
        var response = new WebJobsAttributeCollectionSubmitResponse();

        // Access submitted attributes
        var attributes = request.Data?.UserSignUpInfo?.Attributes;
        
        string? email = attributes?["email"]?.ToString();
        string? displayName = attributes?["displayName"]?.ToString();

        // Validation example: block certain email domains
        if (email?.EndsWith("@blocked.com") == true)
        {
            response.Actions.Add(new WebJobsShowBlockPage
            {
                Message = "Sign-up from this email domain is not allowed."
            });
            return response;
        }

        // Validation example: show validation error
        if (string.IsNullOrEmpty(displayName) || displayName.Length < 3)
        {
            response.Actions.Add(new WebJobsShowValidationError
            {
                Message = "Display name must be at least 3 characters.",
                AttributeErrors = new Dictionary<string, string>
                {
                    { "displayName", "Name is too short" }
                }
            });
            return response;
        }

        // Modify attributes before saving
        response.Actions.Add(new WebJobsModifyAttributeValues
        {
            Attributes = new Dictionary<string, string>
            {
                { "displayName", displayName.Trim() },
                { "city", attributes?["city"]?.ToString()?.ToUpperInvariant() ?? "" }
            }
        });

        return response;
    }
}
```

### 5. 自定义 OTP 投递

通过自定义渠道（短信、邮件、推送通知）发送一次性密码。

```csharp
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents;
using Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents.Framework;
using Microsoft.Extensions.Logging;

public static class CustomOtpFunction
{
    [FunctionName("OnOtpSend")]
    public static async Task<WebJobsAuthenticationEventResponse> Run(
        [WebJobsAuthenticationEventsTrigger] WebJobsOnOtpSendRequest request,
        ILogger log)
    {
        var response = new WebJobsOnOtpSendResponse();

        string? phoneNumber = request.Data?.OtpContext?.Identifier;
        string? otp = request.Data?.OtpContext?.OneTimeCode;

        if (string.IsNullOrEmpty(phoneNumber) || string.IsNullOrEmpty(otp))
        {
            log.LogError("Missing phone number or OTP");
            response.Actions.Add(new WebJobsOnOtpSendFailed
            {
                Error = "Missing required data"
            });
            return response;
        }

        try
        {
            // Send OTP via your SMS provider
            await SendSmsAsync(phoneNumber, $"Your verification code is: {otp}");
            
            response.Actions.Add(new WebJobsOnOtpSendSuccess());
            log.LogInformation("OTP sent successfully to {PhoneNumber}", phoneNumber);
        }
        catch (Exception ex)
        {
            log.LogError(ex, "Failed to send OTP");
            response.Actions.Add(new WebJobsOnOtpSendFailed
            {
                Error = "Failed to send verification code"
            });
        }

        return response;
    }

    private static async Task SendSmsAsync(string phoneNumber, string message)
    {
        // Implement your SMS provider integration (Twilio, Azure Communication Services, etc.)
        await Task.CompletedTask;
    }
}
```

### 6. Function App 配置

为身份验证事件配置 Function App。

```csharp
// Program.cs (Isolated worker model)
using Microsoft.Extensions.Hosting;

var host = new HostBuilder()
    .ConfigureFunctionsWorkerDefaults()
    .Build();

host.Run();
```

```json
// host.json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true
      }
    }
  },
  "extensions": {
    "http": {
      "routePrefix": ""
    }
  }
}
```

```json
// local.settings.json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "dotnet"
  }
}
```

## 核心类型参考

| 类型 | 用途 |
|------|------|
| `WebJobsAuthenticationEventsTriggerAttribute` | 函数触发器特性 |
| `WebJobsTokenIssuanceStartRequest` | 令牌签发事件请求 |
| `WebJobsTokenIssuanceStartResponse` | 令牌签发事件响应 |
| `WebJobsProvideClaimsForToken` | 添加声明的操作 |
| `WebJobsAttributeCollectionStartRequest` | 属性收集开始请求 |
| `WebJobsAttributeCollectionStartResponse` | 属性收集开始响应 |
| `WebJobsAttributeCollectionSubmitRequest` | 属性提交请求 |
| `WebJobsAttributeCollectionSubmitResponse` | 属性提交响应 |
| `WebJobsSetPrefillValues` | 预填表单值 |
| `WebJobsShowBlockPage` | 阻止用户并显示消息 |
| `WebJobsShowValidationError` | 显示验证错误 |
| `WebJobsModifyAttributeValues` | 修改已提交的值 |
| `WebJobsOnOtpSendRequest` | OTP 发送事件请求 |
| `WebJobsOnOtpSendResponse` | OTP 发送事件响应 |
| `WebJobsOnOtpSendSuccess` | OTP 发送成功 |
| `WebJobsOnOtpSendFailed` | OTP 发送失败 |
| `WebJobsContinueWithDefaultBehavior` | 继续默认流程 |

## Entra ID 配置

部署 Function App 后，在 Entra ID 中配置自定义扩展：

1. **注册 API** — Entra ID → 应用注册
2. **创建自定义身份验证扩展** — Entra ID → 外部标识 → 自定义身份验证扩展
3. **关联用户流** — Entra ID → 外部标识 → 用户流

### 应用注册必要设置

```
公开 API：
  - 应用程序 ID URI：api://<your-function-app-name>.azurewebsites.net
  - 范围：CustomAuthenticationExtension.Receive.Payload

API 权限：
  - Microsoft Graph：User.Read（委托）
```

## 最佳实践

1. **验证所有输入** — 不要信任请求数据，处理前先验证
2. **优雅处理错误** — 返回恰当的错误响应
3. **记录关联 ID** — 使用 `CorrelationId` 排查问题
4. **保持函数快速** — 身份验证事件有超时限制
5. **使用托管标识** — 安全访问 Azure 资源
6. **缓存外部数据** — 避免每次请求都做慢查询
7. **本地测试** — 使用 Azure Functions Core Tools 和示例负载
8. **用 App Insights 监控** — 追踪函数执行和错误

## 错误处理

```csharp
[FunctionName("OnTokenIssuanceStart")]
public static WebJobsAuthenticationEventResponse Run(
    [WebJobsAuthenticationEventsTrigger] WebJobsTokenIssuanceStartRequest request,
    ILogger log)
{
    try
    {
        // Your logic here
        var response = new WebJobsTokenIssuanceStartResponse();
        response.Actions.Add(new WebJobsProvideClaimsForToken
        {
            Claims = new Dictionary<string, string> { { "claim", "value" } }
        });
        return response;
    }
    catch (Exception ex)
    {
        log.LogError(ex, "Error processing token issuance event");
        
        // Return empty response - authentication continues without custom claims
        // Do NOT throw - this would fail the authentication
        return new WebJobsTokenIssuanceStartResponse();
    }
}
```

## 相关 SDK

| SDK | 用途 | 安装 |
|-----|------|------|
| `Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents` | 身份验证事件（本 SDK） | `dotnet add package Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents` |
| `Microsoft.Identity.Web` | Web 应用身份验证 | `dotnet add package Microsoft.Identity.Web` |
| `Azure.Identity` | Azure 身份验证 | `dotnet add package Azure.Identity` |

## 参考链接

| 资源 | URL |
|------|-----|
| NuGet 包 | https://www.nuget.org/packages/Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents |
| 自定义扩展概述 | https://learn.microsoft.com/entra/identity-platform/custom-extension-overview |
| 令牌签发事件 | https://learn.microsoft.com/entra/identity-platform/custom-extension-tokenissuancestart-setup |
| 属性收集事件 | https://learn.microsoft.com/entra/identity-platform/custom-extension-attribute-collection |
| GitHub 源码 | https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/entra/Microsoft.Azure.WebJobs.Extensions.AuthenticationEvents |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 输出内容不能替代针对具体环境的验证、测试或专家审查。
- 若缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清。
