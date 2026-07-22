---
name: azure-communication-common-java
description: "Azure Communication Services Java 通用工具库。用于处理 CommunicationTokenCredential、用户标识符、令牌刷新或跨 ACS 服务的共享认证。触发词：ACS认证、通信令牌凭证、用户访问令牌、令牌刷新、CommunicationUserIdentifier、PhoneNumberIdentifier、Azure Communication Services 认证"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Communication Common (Java)

Azure Communication Services 的共享认证工具和数据结构。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-communication-common</artifactId>
    <version>1.4.0</version>
</dependency>
```

## 核心概念

| 类 | 用途 |
|-------|---------|
| `CommunicationTokenCredential` | 使用 ACS 服务对用户进行认证 |
| `CommunicationTokenRefreshOptions` | 配置自动令牌刷新 |
| `CommunicationUserIdentifier` | 标识 ACS 用户 |
| `PhoneNumberIdentifier` | 标识 PSTN 电话号码 |
| `MicrosoftTeamsUserIdentifier` | 标识 Teams 用户 |
| `UnknownIdentifier` | 未知类型的通用标识符 |

## CommunicationTokenCredential

### 静态令牌（短期客户端）

```java
import com.azure.communication.common.CommunicationTokenCredential;

// 简单静态令牌 - 无刷新
String userToken = "<user-access-token>";
CommunicationTokenCredential credential = new CommunicationTokenCredential(userToken);

// 用于 Chat、Calling 等
ChatClient chatClient = new ChatClientBuilder()
    .endpoint("https://<resource>.communication.azure.com")
    .credential(credential)
    .buildClient();
```

### 主动令牌刷新（长期客户端）

```java
import com.azure.communication.common.CommunicationTokenRefreshOptions;
import java.util.concurrent.Callable;

// 令牌刷新回调 - 当令牌即将过期时调用
Callable<String> tokenRefresher = () -> {
    // 调用你的服务器获取新令牌
    return fetchNewTokenFromServer();
};

// 启用主动刷新
CommunicationTokenRefreshOptions refreshOptions = new CommunicationTokenRefreshOptions(tokenRefresher)
    .setRefreshProactively(true)      // 过期前刷新
    .setInitialToken(currentToken);    // 可选的初始令牌

CommunicationTokenCredential credential = new CommunicationTokenCredential(refreshOptions);
```

### 异步令牌刷新

```java
import java.util.concurrent.CompletableFuture;

// 异步令牌获取器
Callable<String> asyncRefresher = () -> {
    CompletableFuture<String> future = fetchTokenAsync();
    return future.get();  // 阻塞直到令牌可用
};

CommunicationTokenRefreshOptions options = new CommunicationTokenRefreshOptions(asyncRefresher)
    .setRefreshProactively(true);

CommunicationTokenCredential credential = new CommunicationTokenCredential(options);
```

## Entra ID (Azure AD) 认证

```java
import com.azure.identity.InteractiveBrowserCredentialBuilder;
import com.azure.communication.common.EntraCommunicationTokenCredentialOptions;
import java.util.Arrays;
import java.util.List;

// 用于 Teams Phone Extensibility
InteractiveBrowserCredential entraCredential = new InteractiveBrowserCredentialBuilder()
    .clientId("<your-client-id>")
    .tenantId("<your-tenant-id>")
    .redirectUrl("<your-redirect-uri>")
    .build();

String resourceEndpoint = "https://<resource>.communication.azure.com";
List<String> scopes = Arrays.asList(
    "https://auth.msft.communication.azure.com/TeamsExtension.ManageCalls"
);

EntraCommunicationTokenCredentialOptions entraOptions = 
    new EntraCommunicationTokenCredentialOptions(entraCredential, resourceEndpoint)
        .setScopes(scopes);

CommunicationTokenCredential credential = new CommunicationTokenCredential(entraOptions);
```

## 通信标识符

### CommunicationUserIdentifier

```java
import com.azure.communication.common.CommunicationUserIdentifier;

// 为 ACS 用户创建标识符
CommunicationUserIdentifier user = new CommunicationUserIdentifier("8:acs:resource-id_user-id");

// 获取原始 ID
String rawId = user.getId();
```

### PhoneNumberIdentifier

```java
import com.azure.communication.common.PhoneNumberIdentifier;

// E.164 格式电话号码
PhoneNumberIdentifier phone = new PhoneNumberIdentifier("+14255551234");

String phoneNumber = phone.getPhoneNumber();  // "+14255551234"
String rawId = phone.getRawId();              // "4:+14255551234"
```

### MicrosoftTeamsUserIdentifier

```java
import com.azure.communication.common.MicrosoftTeamsUserIdentifier;

// Teams 用户标识符
MicrosoftTeamsUserIdentifier teamsUser = new MicrosoftTeamsUserIdentifier("<teams-user-id>")
    .setCloudEnvironment(CommunicationCloudEnvironment.PUBLIC);

// 匿名 Teams 用户
MicrosoftTeamsUserIdentifier anonymousTeamsUser = new MicrosoftTeamsUserIdentifier("<teams-user-id>")
    .setAnonymous(true);
```

### UnknownIdentifier

```java
import com.azure.communication.common.UnknownIdentifier;

// 用于未知类型的标识符
UnknownIdentifier unknown = new UnknownIdentifier("some-raw-id");
```

## 标识符解析

```java
import com.azure.communication.common.CommunicationIdentifier;
import com.azure.communication.common.CommunicationIdentifierModel;

// 将原始 ID 解析为相应类型
public CommunicationIdentifier parseIdentifier(String rawId) {
    if (rawId.startsWith("8:acs:")) {
        return new CommunicationUserIdentifier(rawId);
    } else if (rawId.startsWith("4:")) {
        String phone = rawId.substring(2);
        return new PhoneNumberIdentifier(phone);
    } else if (rawId.startsWith("8:orgid:")) {
        String teamsId = rawId.substring(8);
        return new MicrosoftTeamsUserIdentifier(teamsId);
    } else {
        return new UnknownIdentifier(rawId);
    }
}
```

## 标识符类型检查

```java
import com.azure.communication.common.CommunicationIdentifier;

public void processIdentifier(CommunicationIdentifier identifier) {
    if (identifier instanceof CommunicationUserIdentifier) {
        CommunicationUserIdentifier user = (CommunicationUserIdentifier) identifier;
        System.out.println("ACS User: " + user.getId());
        
    } else if (identifier instanceof PhoneNumberIdentifier) {
        PhoneNumberIdentifier phone = (PhoneNumberIdentifier) identifier;
        System.out.println("Phone: " + phone.getPhoneNumber());
        
    } else if (identifier instanceof MicrosoftTeamsUserIdentifier) {
        MicrosoftTeamsUserIdentifier teams = (MicrosoftTeamsUserIdentifier) identifier;
        System.out.println("Teams User: " + teams.getUserId());
        System.out.println("Anonymous: " + teams.isAnonymous());
        
    } else if (identifier instanceof UnknownIdentifier) {
        UnknownIdentifier unknown = (UnknownIdentifier) identifier;
        System.out.println("Unknown: " + unknown.getId());
    }
}
```

## 令牌访问

```java
import com.azure.core.credential.AccessToken;

// 获取当前令牌（用于调试/日志 - 不要暴露！）
CommunicationTokenCredential credential = new CommunicationTokenCredential(token);

// 同步访问
AccessToken accessToken = credential.getToken();
System.out.println("Token expires: " + accessToken.getExpiresAt());

// 异步访问
credential.getTokenAsync()
    .subscribe(token -> {
        System.out.println("Token: " + token.getToken().substring(0, 20) + "...");
        System.out.println("Expires: " + token.getExpiresAt());
    });
```

## 销毁凭证

```java
// 完成后清理
credential.close();

// 或使用 try-with-resources
try (CommunicationTokenCredential cred = new CommunicationTokenCredential(options)) {
    // 使用凭证
    chatClient.doSomething();
}
```

## 云环境

```java
import com.azure.communication.common.CommunicationCloudEnvironment;

// 可用环境
CommunicationCloudEnvironment publicCloud = CommunicationCloudEnvironment.PUBLIC;
CommunicationCloudEnvironment govCloud = CommunicationCloudEnvironment.GCCH;
CommunicationCloudEnvironment dodCloud = CommunicationCloudEnvironment.DOD;

// 在 Teams 标识符上设置
MicrosoftTeamsUserIdentifier teamsUser = new MicrosoftTeamsUserIdentifier("<user-id>")
    .setCloudEnvironment(CommunicationCloudEnvironment.GCCH);
```

## 环境变量

```bash
AZURE_COMMUNICATION_ENDPOINT=https://<resource>.communication.azure.com
AZURE_COMMUNICATION_USER_TOKEN=<user-access-token>
```

## 最佳实践

1. **主动刷新** - 对于长期客户端，始终使用 `setRefreshProactively(true)`
2. **令牌安全** - 永远不要记录或暴露完整令牌
3. **关闭凭证** - 不再需要时销毁凭证
4. **错误处理** - 优雅地处理令牌刷新失败
5. **标识符类型** - 使用具体的标识符类型，而非原始字符串

## 常用模式

```java
// 模式：为 Chat/Calling 客户端创建凭证
public ChatClient createChatClient(String token, String endpoint) {
    CommunicationTokenRefreshOptions refreshOptions = 
        new CommunicationTokenRefreshOptions(this::refreshToken)
            .setRefreshProactively(true)
            .setInitialToken(token);
    
    CommunicationTokenCredential credential = 
        new CommunicationTokenCredential(refreshOptions);
    
    return new ChatClientBuilder()
        .endpoint(endpoint)
        .credential(credential)
        .buildClient();
}

private String refreshToken() {
    // 调用你的令牌端点
    return tokenService.getNewToken();
}
```

## 触发词

- "ACS 认证"、"通信令牌凭证"
- "用户访问令牌"、"令牌刷新"
- "CommunicationUserIdentifier"、"PhoneNumberIdentifier"
- "Azure Communication Services 认证"

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 输出不应替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
