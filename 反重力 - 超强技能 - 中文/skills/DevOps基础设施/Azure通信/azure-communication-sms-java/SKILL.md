---
name: azure-communication-sms-java
description: "使用 Azure Communication Services SMS Java SDK 发送短信消息。适用于实现短信通知、警报、OTP 送达、批量消息或送达报告。触发词：发送短信Java、短信通知、OTP短信、批量短信、Azure短信服务、SMS Java、短信SDK"
risk: safe
source: community
date_added: "2026-02-27"
---

# Azure Communication SMS (Java)

向单个或多个收件人发送短信消息，并支持送达报告。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-communication-sms</artifactId>
    <version>1.2.0</version>
</dependency>
```

## 创建客户端

```java
import com.azure.communication.sms.SmsClient;
import com.azure.communication.sms.SmsClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

// 使用 DefaultAzureCredential（推荐）
SmsClient smsClient = new SmsClientBuilder()
    .endpoint("https://<resource>.communication.azure.com")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();

// 使用连接字符串
SmsClient smsClient = new SmsClientBuilder()
    .connectionString("<connection-string>")
    .buildClient();

// 使用 AzureKeyCredential
import com.azure.core.credential.AzureKeyCredential;

SmsClient smsClient = new SmsClientBuilder()
    .endpoint("https://<resource>.communication.azure.com")
    .credential(new AzureKeyCredential("<access-key>"))
    .buildClient();

// 异步客户端
SmsAsyncClient smsAsyncClient = new SmsClientBuilder()
    .connectionString("<connection-string>")
    .buildAsyncClient();
```

## 向单个收件人发送短信

```java
import com.azure.communication.sms.models.SmsSendResult;

// 简单发送
SmsSendResult result = smsClient.send(
    "+14255550100",      // 发送方（您的 ACS 电话号码）
    "+14255551234",      // 接收方
    "您的验证码是 123456");

System.out.println("消息 ID: " + result.getMessageId());
System.out.println("接收方: " + result.getTo());
System.out.println("成功: " + result.isSuccessful());

if (!result.isSuccessful()) {
    System.out.println("错误: " + result.getErrorMessage());
    System.out.println("状态: " + result.getHttpStatusCode());
}
```

## 向多个收件人发送短信

```java
import com.azure.communication.sms.models.SmsSendOptions;
import java.util.Arrays;
import java.util.List;

List<String> recipients = Arrays.asList(
    "+14255551111",
    "+14255552222",
    "+14255553333"
);

// 带选项
SmsSendOptions options = new SmsSendOptions()
    .setDeliveryReportEnabled(true)
    .setTag("marketing-campaign-001");

Iterable<SmsSendResult> results = smsClient.sendWithResponse(
    "+14255550100",      // 发送方
    recipients,          // 接收方列表
    "限时特惠！今日全场5折。",
    options,
    Context.NONE
).getValue();

for (SmsSendResult result : results) {
    if (result.isSuccessful()) {
        System.out.println("已发送至 " + result.getTo() + ": " + result.getMessageId());
    } else {
        System.out.println("发送失败 " + result.getTo() + ": " + result.getErrorMessage());
    }
}
```

## 发送选项

```java
SmsSendOptions options = new SmsSendOptions();

// 启用送达报告（通过 Event Grid 发送）
options.setDeliveryReportEnabled(true);

// 添加自定义标签用于追踪
options.setTag("order-confirmation-12345");
```

## 响应处理

```java
import com.azure.core.http.rest.Response;

Response<Iterable<SmsSendResult>> response = smsClient.sendWithResponse(
    "+14255550100",
    Arrays.asList("+14255551234"),
    "您好！",
    new SmsSendOptions().setDeliveryReportEnabled(true),
    Context.NONE
);

// 检查 HTTP 响应
System.out.println("状态码: " + response.getStatusCode());
System.out.println("响应头: " + response.getHeaders());

// 处理结果
for (SmsSendResult result : response.getValue()) {
    System.out.println("消息 ID: " + result.getMessageId());
    System.out.println("是否成功: " + result.isSuccessful());
    
    if (!result.isSuccessful()) {
        System.out.println("HTTP 状态: " + result.getHttpStatusCode());
        System.out.println("错误: " + result.getErrorMessage());
    }
}
```

## 异步操作

```java
import reactor.core.publisher.Mono;

SmsAsyncClient asyncClient = new SmsClientBuilder()
    .connectionString("<connection-string>")
    .buildAsyncClient();

// 发送单条消息
asyncClient.send("+14255550100", "+14255551234", "异步消息！")
    .subscribe(
        result -> System.out.println("已发送: " + result.getMessageId()),
        error -> System.out.println("错误: " + error.getMessage())
    );

// 带选项发送给多个收件人
SmsSendOptions options = new SmsSendOptions()
    .setDeliveryReportEnabled(true);

asyncClient.sendWithResponse(
    "+14255550100",
    Arrays.asList("+14255551111", "+14255552222"),
    "批量异步消息",
    options)
    .subscribe(response -> {
        for (SmsSendResult result : response.getValue()) {
            System.out.println("结果: " + result.getTo() + " - " + result.isSuccessful());
        }
    });
```

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;

try {
    SmsSendResult result = smsClient.send(
        "+14255550100",
        "+14255551234",
        "测试消息"
    );
    
    // 单条消息错误不会抛出异常
    if (!result.isSuccessful()) {
        handleMessageError(result);
    }
    
} catch (HttpResponseException e) {
    // 请求级别失败（认证、网络等）
    System.out.println("请求失败: " + e.getMessage());
    System.out.println("状态: " + e.getResponse().getStatusCode());
} catch (RuntimeException e) {
    System.out.println("意外错误: " + e.getMessage());
}

private void handleMessageError(SmsSendResult result) {
    int status = result.getHttpStatusCode();
    String error = result.getErrorMessage();
    
    if (status == 400) {
        System.out.println("无效电话号码: " + result.getTo());
    } else if (status == 429) {
        System.out.println("频率限制 - 请稍后重试");
    } else {
        System.out.println("错误 " + status + ": " + error);
    }
}
```

## 送达报告

送达报告通过 Azure Event Grid 发送。为您的 ACS 资源配置 Event Grid 订阅。

```java
// Event Grid webhook 处理器（在您的端点中）
public void handleDeliveryReport(String eventJson) {
    // 解析 Event Grid 事件
    // 事件类型: Microsoft.Communication.SMSDeliveryReportReceived
    
    // 事件数据包含:
    // - messageId: 对应 SmsSendResult.getMessageId()
    // - from: 发送方号码
    // - to: 接收方号码
    // - deliveryStatus: "Delivered"、"Failed" 等
    // - deliveryStatusDetails: 详细状态
    // - receivedTimestamp: 状态接收时间
    // - tag: 您在 SmsSendOptions 中设置的自定义标签
}
```

## SmsSendResult 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `getMessageId()` | String | 唯一消息标识符 |
| `getTo()` | String | 接收方电话号码 |
| `isSuccessful()` | boolean | 发送是否成功 |
| `getHttpStatusCode()` | int | 该接收方的 HTTP 状态码 |
| `getErrorMessage()` | String | 失败时的错误详情 |
| `getRepeatabilityResult()` | RepeatabilityResult | 幂等性结果 |

## 环境变量

```bash
AZURE_COMMUNICATION_ENDPOINT=https://<resource>.communication.azure.com
AZURE_COMMUNICATION_CONNECTION_STRING=endpoint=https://...;accesskey=...
SMS_FROM_NUMBER=+14255550100
```

## 最佳实践

1. **电话号码格式** - 使用 E.164 格式：`+[国家代码][号码]`
2. **送达报告** - 为关键消息（OTP、警报）启用送达报告
3. **标签** - 使用标签将消息与业务上下文关联
4. **错误处理** - 单独检查每个收件人的 `isSuccessful()`
5. **频率限制** - 对 429 响应实现带退避的重试机制
6. **批量发送** - 对多个收件人使用批量发送（更高效）

## 触发词

- "发送短信 Java"、"短信消息 Java"
- "短信通知"、"OTP 短信"、"批量短信"
- "送达报告 短信"、"Azure Communication Services 短信"

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出内容不应替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
