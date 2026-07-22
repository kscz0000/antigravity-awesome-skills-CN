---
name: google-calendar-automation
description: "轻量级 Google 日历集成，独立 OAuth 认证，无需 MCP 服务器。触发词：Google日历、日历自动化、Calendar事件、日程管理、OAuth日历、创建日历事件、查找空闲时间、日历邀请回复"
license: Apache-2.0
risk: critical
source: community
metadata:
  author: sanjay3290
  version: "1.0"
---

# Google 日历

轻量级 Google 日历集成，独立 OAuth 认证，无需 MCP 服务器。

> **⚠️ 需要 Google Workspace 账号。** 不支持个人 Gmail 账号。

## 使用场景
- 需要从本地脚本列出、创建、查看或更新 Google 日历事件。
- 任务需要基于 OAuth 的日历自动化，但不想搭建 MCP 服务器。
- 需要在 Workspace 环境中快速操作日历、日程、参会者或事件详情。

## 首次设置

使用 Google 认证（会打开浏览器）：
```bash
python scripts/auth.py login
```

检查认证状态：
```bash
python scripts/auth.py status
```

需要时登出：
```bash
python scripts/auth.py logout
```

## 命令

所有操作通过 `scripts/gcal.py` 执行。首次使用时若未登录会自动认证。

### 列出日历
```bash
python scripts/gcal.py list-calendars
```

### 列出事件
```bash
# 列出主日历的事件（默认：未来30天）
python scripts/gcal.py list-events

# 列出指定时间范围的事件
python scripts/gcal.py list-events --time-min 2024-01-15T00:00:00Z --time-max 2024-01-31T23:59:59Z

# 列出指定日历的事件
python scripts/gcal.py list-events --calendar "work@example.com"

# 限制结果数量
python scripts/gcal.py list-events --max-results 10
```

### 获取事件详情
```bash
python scripts/gcal.py get-event EVENT_ID
python scripts/gcal.py get-event EVENT_ID --calendar "work@example.com"
```

### 创建事件
```bash
# 基本事件
python scripts/gcal.py create-event "Team Meeting" "2024-01-15T10:00:00Z" "2024-01-15T11:00:00Z"

# 带描述和地点的事件
python scripts/gcal.py create-event "Team Meeting" "2024-01-15T10:00:00Z" "2024-01-15T11:00:00Z" \
    --description "Weekly sync" --location "Conference Room A"

# 带参会者的事件
python scripts/gcal.py create-event "Team Meeting" "2024-01-15T10:00:00Z" "2024-01-15T11:00:00Z" \
    --attendees user1@example.com user2@example.com

# 在指定日历创建事件
python scripts/gcal.py create-event "Meeting" "2024-01-15T10:00:00Z" "2024-01-15T11:00:00Z" \
    --calendar "work@example.com"
```

### 更新事件
```bash
# 更新事件标题
python scripts/gcal.py update-event EVENT_ID --summary "New Title"

# 更新事件时间
python scripts/gcal.py update-event EVENT_ID --start "2024-01-15T14:00:00Z" --end "2024-01-15T15:00:00Z"

# 更新多个字段
python scripts/gcal.py update-event EVENT_ID \
    --summary "Updated Meeting" --description "New agenda" --location "Room B"

# 更新参会者
python scripts/gcal.py update-event EVENT_ID --attendees user1@example.com user3@example.com
```

### 删除事件
```bash
python scripts/gcal.py delete-event EVENT_ID
python scripts/gcal.py delete-event EVENT_ID --calendar "work@example.com"
```

### 查找空闲时间
查找指定参会者的第一个可用会议时段：
```bash
# 为自己查找30分钟空闲时段
python scripts/gcal.py find-free-time \
    --attendees me \
    --time-min "2024-01-15T09:00:00Z" \
    --time-max "2024-01-15T17:00:00Z" \
    --duration 30

# 为多位参会者查找60分钟空闲时段
python scripts/gcal.py find-free-time \
    --attendees me user1@example.com user2@example.com \
    --time-min "2024-01-15T09:00:00Z" \
    --time-max "2024-01-19T17:00:00Z" \
    --duration 60
```

### 回复事件邀请
```bash
# 接受邀请
python scripts/gcal.py respond-to-event EVENT_ID accepted

# 拒绝邀请
python scripts/gcal.py respond-to-event EVENT_ID declined

# 标记为暂定
python scripts/gcal.py respond-to-event EVENT_ID tentative

# 回复但不通知组织者
python scripts/gcal.py respond-to-event EVENT_ID accepted --no-notify
```

## 日期/时间格式

所有时间使用带时区的 ISO 8601 格式：
- UTC：`2024-01-15T10:30:00Z`
- 带偏移量：`2024-01-15T10:30:00-05:00`（EST）

## 日历 ID 格式

- 主日历：使用 `primary` 或省略 `--calendar` 参数
- 其他日历：使用 `list-calendars` 返回的日历 ID（通常是邮箱地址）

## 令牌管理

令牌使用系统密钥环安全存储：
- **macOS**：Keychain
- **Windows**：Windows Credential Locker
- **Linux**：Secret Service API（GNOME Keyring、KDE Wallet 等）

服务名称：`google-calendar-skill-oauth`

令牌过期时通过 Google 云函数自动刷新。

## 限制
- 仅当任务明确符合上述范围时才使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
