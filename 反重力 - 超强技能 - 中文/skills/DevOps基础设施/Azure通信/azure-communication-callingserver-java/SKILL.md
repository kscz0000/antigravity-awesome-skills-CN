---
name: azure-communication-callingserver-java
description: "⚠️ 已弃用：此 SDK 已更名为 Call Automation。新项目请使用 azure-communication-callautomation。此技能仅用于维护遗留代码。触发词：callingserver legacy、deprecated calling SDK、migrate callingserver to callautomation、迁移 callingserver、遗留通话 SDK"
risk: safe
source: community
date_added: "2026-02-27"
---

# Azure Communication CallingServer (Java) - 已弃用

> **⚠️ 已弃用**：此 SDK 已更名为 **Call Automation**。新项目请使用 `azure-communication-callautomation` 代替。此技能仅用于维护遗留代码。

## 迁移到 Call Automation

```xml
<!-- 旧版（已弃用） -->
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-communication-callingserver</artifactId>
    <version>1.0.0-beta.5</version>
</dependency>

<!-- 新版（请使用此版本） -->
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-communication-callautomation</artifactId>
    <version>1.6.0</version>
</dependency>
```

## 类名变更

| CallingServer（旧版） | Call Automation（新版） |
|----------------------|------------------------|
| `CallingServerClient` | `CallAutomationClient` |
| `CallingServerClientBuilder` | `CallAutomationClientBuilder` |
| `CallConnection` | `CallConnection`（相同） |
| `ServerCall` | 已移除 - 使用 `CallConnection` |

## 遗留客户端创建

```java
// 旧方式（已弃用）
import com.azure.communication.callingserver.CallingServerClient;
import com.azure.communication.callingserver.CallingServerClientBuilder;

CallingServerClient client = new CallingServerClientBuilder()
    .connectionString("<connection-string>")
    .buildClient();

// 新方式
import com.azure.communication.callautomation.CallAutomationClient;
import com.azure.communication.callautomation.CallAutomationClientBuilder;

CallAutomationClient client = new CallAutomationClientBuilder()
    .connectionString("<connection-string>")
    .buildClient();
```

## 遗留录音功能

```java
// 旧方式
StartRecordingOptions options = new StartRecordingOptions(serverCallId)
    .setRecordingStateCallbackUri(callbackUri);

StartCallRecordingResult result = client.startRecording(options);
String recordingId = result.getRecordingId();

client.pauseRecording(recordingId);
client.resumeRecording(recordingId);
client.stopRecording(recordingId);

// 新方式 - 请参阅 azure-communication-callautomation 技能
```

## 新开发注意事项

**新项目请勿使用此 SDK。**

请参阅 `azure-communication-callautomation-java` 技能了解：
- 发起外呼
- 接听来电
- 通话录音
- DTMF 识别
- 文本转语音 / 语音转文本
- 添加/移除参与者
- 通话转接

## 触发词

- "callingserver legacy"、"deprecated calling SDK"
- "migrate callingserver to callautomation"

## 使用时机
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时才使用此技能。
- 输出内容不能替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
