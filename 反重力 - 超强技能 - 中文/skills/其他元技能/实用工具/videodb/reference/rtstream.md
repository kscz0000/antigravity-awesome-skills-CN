# RTStream 指南

## 概述

RTStream 支持实时摄取直播视频流（RTSP/RTMP）和桌面捕获会话。连接后，你可以从直播源录制、索引、搜索和导出内容。

代码级详细信息（SDK 方法、参数、示例），请参阅 [rtstream-reference.md](rtstream-reference.md)。

## 使用场景

- **安防监控**：连接 RTSP 摄像头，检测事件，触发告警
- **直播推流**：摄取 RTMP 流，实时索引，支持即时搜索
- **会议录制**：捕获桌面屏幕和音频，实时转录，导出录制
- **事件处理**：监控直播源，运行 AI 分析，响应检测到的内容

## 快速开始

1. **连接直播流**（RTSP/RTMP URL）或从捕获会话获取 RTStream

2. **开始摄取**以录制直播内容

3. **启动 AI 管道**进行实时索引（音频、视觉、转录）

4. **监控事件**通过 WebSocket 获取实时 AI 结果和告警

5. **停止摄取**完成时

6. **导出为视频**用于永久存储和后续处理

7. **搜索录制**查找特定时刻

## RTStream 来源

### 从 RTSP/RTMP 流

直接连接到直播视频源：

```python
rtstream = coll.connect_rtstream(
    url="rtmp://your-stream-server/live/stream-key",
    name="My Live Stream",
)
```

### 从捕获会话

从桌面捕获获取 RTStream（麦克风、屏幕、系统音频）：

```python
session = conn.get_capture_session(session_id)

mics = session.get_rtstream("mic")
displays = session.get_rtstream("screen")
system_audios = session.get_rtstream("system_audio")
```

捕获会话工作流，请参阅 [capture.md](capture.md)。

---

## 脚本

| 脚本 | 描述 |
|------|------|
| `scripts/ws_listener.py` | WebSocket 事件监听器，用于实时 AI 结果 |
