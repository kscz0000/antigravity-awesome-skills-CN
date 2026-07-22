---
name: azure-communication-callautomation-java
description: "构建服务端呼叫自动化工作流，包括IVR系统、呼叫路由、录音和AI驱动的交互。触发词：呼叫自动化Java、IVR Java、交互式语音响应、呼叫录音Java、DTMF识别Java、文本转语音呼叫、语音识别呼叫、接听来电、转接呼叫Java、Azure Communication Services呼叫自动化"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Azure Communication Call Automation (Java)

构建服务端呼叫自动化工作流，包括IVR系统、呼叫路由、录音和AI驱动的交互。

## 安装

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-communication-callautomation</artifactId>
    <version>1.6.0</version>
</dependency>
```

## 创建客户端

```java
import com.azure.communication.callautomation.CallAutomationClient;
import com.azure.communication.callautomation.CallAutomationClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;

// 使用 DefaultAzureCredential
CallAutomationClient client = new CallAutomationClientBuilder()
    .endpoint("https://<resource>.communication.azure.com")
    .credential(new DefaultAzureCredentialBuilder().build())
    .buildClient();

// 使用连接字符串
CallAutomationClient client = new CallAutomationClientBuilder()
    .connectionString("<connection-string>")
    .buildClient();
```

## 核心概念

| 类 | 用途 |
|-------|---------|
| `CallAutomationClient` | 发起呼叫、接听/拒绝来电、重定向呼叫 |
| `CallConnection` | 已建立呼叫中的操作（添加参与者、终止） |
| `CallMedia` | 媒体操作（播放音频、识别DTMF/语音） |
| `CallRecording` | 开始/停止/暂停录音 |
| `CallAutomationEventParser` | 解析来自ACS的webhook事件 |

## 发起外呼

```java
import com.azure.communication.callautomation.models.*;
import com.azure.communication.common.CommunicationUserIdentifier;
import com.azure.communication.common.PhoneNumberIdentifier;

// 呼叫PSTN号码
PhoneNumberIdentifier target = new PhoneNumberIdentifier("+14255551234");
PhoneNumberIdentifier caller = new PhoneNumberIdentifier("+14255550100");

CreateCallOptions options = new CreateCallOptions(
    new CommunicationUserIdentifier("<user-id>"),  // 来源
    List.of(target))                                // 目标
    .setSourceCallerId(caller)
    .setCallbackUrl("https://your-app.com/api/callbacks");

CreateCallResult result = client.createCall(options);
String callConnectionId = result.getCallConnectionProperties().getCallConnectionId();
```

## 接听来电

```java
// 来自Event Grid webhook - IncomingCall事件
String incomingCallContext = "<incoming-call-context-from-event>";

AnswerCallOptions options = new AnswerCallOptions(
    incomingCallContext,
    "https://your-app.com/api/callbacks");

AnswerCallResult result = client.answerCall(options);
CallConnection callConnection = result.getCallConnection();
```

## 播放音频（文本转语音）

```java
CallConnection callConnection = client.getCallConnection(callConnectionId);
CallMedia callMedia = callConnection.getCallMedia();

// 播放文本转语音
TextSource textSource = new TextSource()
    .setText("Welcome to Contoso. Press 1 for sales, 2 for support.")
    .setVoiceName("en-US-JennyNeural");

PlayOptions playOptions = new PlayOptions(
    List.of(textSource),
    List.of(new CommunicationUserIdentifier("<target-user>")));

callMedia.play(playOptions);

// 播放音频文件
FileSource fileSource = new FileSource()
    .setUrl("https://storage.blob.core.windows.net/audio/greeting.wav");

callMedia.play(new PlayOptions(List.of(fileSource), List.of(target)));
```

## 识别DTMF输入

```java
// 识别DTMF音调
DtmfTone stopTones = DtmfTone.POUND;

CallMediaRecognizeDtmfOptions recognizeOptions = new CallMediaRecognizeDtmfOptions(
    new CommunicationUserIdentifier("<target-user>"),
    5)  // 最大收集音调数
    .setInterToneTimeout(Duration.ofSeconds(5))
    .setStopTones(List.of(stopTones))
    .setInitialSilenceTimeout(Duration.ofSeconds(15))
    .setPlayPrompt(new TextSource().setText("Enter your account number followed by pound."));

callMedia.startRecognizing(recognizeOptions);
```

## 识别语音

```java
// AI语音识别
CallMediaRecognizeSpeechOptions speechOptions = new CallMediaRecognizeSpeechOptions(
    new CommunicationUserIdentifier("<target-user>"))
    .setEndSilenceTimeout(Duration.ofSeconds(2))
    .setSpeechLanguage("en-US")
    .setPlayPrompt(new TextSource().setText("How can I help you today?"));

callMedia.startRecognizing(speechOptions);
```

## 呼叫录音

```java
CallRecording callRecording = client.getCallRecording();

// 开始录音
StartRecordingOptions recordingOptions = new StartRecordingOptions(
    new ServerCallLocator("<server-call-id>"))
    .setRecordingChannel(RecordingChannel.MIXED)
    .setRecordingContent(RecordingContent.AUDIO_VIDEO)
    .setRecordingFormat(RecordingFormat.MP4);

RecordingStateResult recordingResult = callRecording.start(recordingOptions);
String recordingId = recordingResult.getRecordingId();

// 暂停/恢复/停止
callRecording.pause(recordingId);
callRecording.resume(recordingId);
callRecording.stop(recordingId);

// 下载录音（在RecordingFileStatusUpdated事件之后）
callRecording.downloadTo(recordingUrl, Paths.get("recording.mp4"));
```

## 添加参与者到呼叫

```java
CallConnection callConnection = client.getCallConnection(callConnectionId);

CommunicationUserIdentifier participant = new CommunicationUserIdentifier("<user-id>");
AddParticipantOptions addOptions = new AddParticipantOptions(participant)
    .setInvitationTimeout(Duration.ofSeconds(30));

AddParticipantResult result = callConnection.addParticipant(addOptions);
```

## 转接呼叫

```java
// 盲转接
PhoneNumberIdentifier transferTarget = new PhoneNumberIdentifier("+14255559999");
TransferCallToParticipantResult result = callConnection.transferCallToParticipant(transferTarget);
```

## 处理事件（Webhook）

```java
import com.azure.communication.callautomation.CallAutomationEventParser;
import com.azure.communication.callautomation.models.events.*;

// 在你的webhook端点中
public void handleCallback(String requestBody) {
    List<CallAutomationEventBase> events = CallAutomationEventParser.parseEvents(requestBody);
    
    for (CallAutomationEventBase event : events) {
        if (event instanceof CallConnected) {
            CallConnected connected = (CallConnected) event;
            System.out.println("Call connected: " + connected.getCallConnectionId());
        } else if (event instanceof RecognizeCompleted) {
            RecognizeCompleted recognized = (RecognizeCompleted) event;
            // 处理DTMF或语音识别结果
            DtmfResult dtmfResult = (DtmfResult) recognized.getRecognizeResult();
            String tones = dtmfResult.getTones().stream()
                .map(DtmfTone::toString)
                .collect(Collectors.joining());
            System.out.println("DTMF received: " + tones);
        } else if (event instanceof PlayCompleted) {
            System.out.println("Audio playback completed");
        } else if (event instanceof CallDisconnected) {
            System.out.println("Call ended");
        }
    }
}
```

## 挂断呼叫

```java
// 为所有参与者挂断
callConnection.hangUp(true);

// 仅挂断当前分支
callConnection.hangUp(false);
```

## 错误处理

```java
import com.azure.core.exception.HttpResponseException;

try {
    client.answerCall(options);
} catch (HttpResponseException e) {
    if (e.getResponse().getStatusCode() == 404) {
        System.out.println("Call not found or already ended");
    } else if (e.getResponse().getStatusCode() == 400) {
        System.out.println("Invalid request: " + e.getMessage());
    }
}
```

## 环境变量

```bash
AZURE_COMMUNICATION_ENDPOINT=https://<resource>.communication.azure.com
AZURE_COMMUNICATION_CONNECTION_STRING=endpoint=https://...;accesskey=...
CALLBACK_BASE_URL=https://your-app.com/api/callbacks
```

## 触发词

- "call automation Java", "IVR Java", "interactive voice response"
- "call recording Java", "DTMF recognition Java"
- "text to speech call", "speech recognition call"
- "answer incoming call", "transfer call Java"
- "Azure Communication Services call automation"

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
