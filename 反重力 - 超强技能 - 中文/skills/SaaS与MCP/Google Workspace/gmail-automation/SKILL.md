---
name: gmail-automation
description: "轻量级 Gmail 集成，独立 OAuth 认证，无需 MCP 服务器。触发词：Gmail自动化、邮件搜索、发送邮件、Gmail集成、OAuth邮件、收件箱自动化"
license: Apache-2.0
risk: critical
source: community
metadata:
  author: sanjay3290
  version: "1.0"
---

# Gmail

轻量级 Gmail 集成，独立 OAuth 认证，无需 MCP 服务器。

> **⚠️ 需要 Google Workspace 账号。** 不支持个人 Gmail 账号。

## 何时使用
- 需要在命令行搜索、阅读或发送 Gmail 邮件，且无需 MCP 服务器。
- 正在为 Google Workspace 账号自动化收件箱工作流。
- 想要一个由独立 OAuth 脚本支撑的轻量级 Gmail 集成。

## 首次设置

使用 Google 认证（打开浏览器）：
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

所有操作通过 `scripts/gmail.py` 执行。首次使用时若未登录会自动认证。

### 搜索邮件

```bash
# 使用 Gmail 查询语法搜索
python scripts/gmail.py search "from:someone@example.com is:unread"

# 搜索最近邮件（不带查询条件返回全部）
python scripts/gmail.py search --limit 20

# 按标签筛选
python scripts/gmail.py search --label INBOX --limit 10

# 包含垃圾邮件和已删除邮件
python scripts/gmail.py search "subject:important" --include-spam-trash
```

### 读取邮件内容

```bash
# 获取完整邮件内容
python scripts/gmail.py get MESSAGE_ID

# 仅获取元数据（邮件头）
python scripts/gmail.py get MESSAGE_ID --format metadata

# 获取最小响应（仅 ID）
python scripts/gmail.py get MESSAGE_ID --format minimal
```

### 发送邮件

```bash
# 发送简单邮件
python scripts/gmail.py send --to "user@example.com" --subject "Hello" --body "Message body"

# 发送带抄送和密送的邮件
python scripts/gmail.py send --to "user@example.com" --cc "cc@example.com" --bcc "bcc@example.com" \
  --subject "Team Update" --body "Update message"

# 使用别名发送（必须在 Gmail 设置中配置）
python scripts/gmail.py send --to "user@example.com" --subject "Hello" --body "Message" \
  --from "Mile9 Accounts <accounts@mile9.io>"

# 发送 HTML 邮件
python scripts/gmail.py send --to "user@example.com" --subject "HTML Email" \
  --body "<h1>Hello</h1><p>HTML content</p>" --html
```

### 草稿管理

```bash
# 创建草稿
python scripts/gmail.py create-draft --to "user@example.com" --subject "Draft Subject" \
  --body "Draft content"

# 发送已有草稿
python scripts/gmail.py send-draft DRAFT_ID
```

### 修改邮件（标签）

```bash
# 标记为已读（移除 UNREAD 标签）
python scripts/gmail.py modify MESSAGE_ID --remove-label UNREAD

# 标记为未读
python scripts/gmail.py modify MESSAGE_ID --add-label UNREAD

# 归档（从收件箱移除）
python scripts/gmail.py modify MESSAGE_ID --remove-label INBOX

# 加星标
python scripts/gmail.py modify MESSAGE_ID --add-label STARRED

# 取消星标
python scripts/gmail.py modify MESSAGE_ID --remove-label STARRED

# 标记为重要
python scripts/gmail.py modify MESSAGE_ID --add-label IMPORTANT

# 同时修改多个标签
python scripts/gmail.py modify MESSAGE_ID --remove-label UNREAD --add-label STARRED
```

### 列出标签

```bash
# 列出所有 Gmail 标签（系统标签和用户创建的标签）
python scripts/gmail.py list-labels
```

## Gmail 查询语法

Gmail 支持强大的搜索运算符：

| 查询 | 说明 |
|-------|-------------|
| `from:user@example.com` | 来自特定发件人的邮件 |
| `to:user@example.com` | 发送给特定收件人的邮件 |
| `subject:meeting` | 主题包含"meeting"的邮件 |
| `is:unread` | 未读邮件 |
| `is:starred` | 已加星标邮件 |
| `is:important` | 重要邮件 |
| `has:attachment` | 包含附件的邮件 |
| `after:2024/01/01` | 某日期之后的邮件 |
| `before:2024/12/31` | 某日期之前的邮件 |
| `newer_than:7d` | 最近 7 天的邮件 |
| `older_than:1m` | 超过 1 个月的邮件 |
| `label:work` | 带有特定标签的邮件 |
| `in:inbox` | 收件箱中的邮件 |
| `in:sent` | 已发送邮件 |
| `in:trash` | 已删除邮件 |

使用 AND（空格）、OR 或 -（NOT）组合：
```bash
python scripts/gmail.py search "from:boss@company.com is:unread newer_than:1d"
python scripts/gmail.py search "subject:urgent OR subject:important"
python scripts/gmail.py search "from:newsletter@example.com -is:starred"
```

## 常用标签 ID

| 标签 | ID |
|-------|-----|
| 收件箱 | `INBOX` |
| 已发送 | `SENT` |
| 草稿 | `DRAFT` |
| 垃圾邮件 | `SPAM` |
| 已删除 | `TRASH` |
| 已加星标 | `STARRED` |
| 重要 | `IMPORTANT` |
| 未读 | `UNREAD` |

## 令牌管理

令牌使用系统密钥环安全存储：
- **macOS**: Keychain
- **Windows**: Windows Credential Locker
- **Linux**: Secret Service API（GNOME Keyring、KDE Wallet 等）

服务名称：`gmail-skill-oauth`

令牌过期时通过 Google 云函数自动刷新。

## 限制
- 仅当任务明确符合上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
