---
name: google-docs-automation
description: "轻量级 Google Docs 集成，独立 OAuth 认证，无需 MCP 服务器。适用于 Google Docs 自动化、操作 Google 文档、创建/编辑/搜索 Google Docs 等场景。"
license: Apache-2.0
risk: critical
source: community
metadata:
  author: sanjay3290
  version: "1.0"
---

# Google Docs

轻量级 Google Docs 集成，独立 OAuth 认证，无需 MCP 服务器。

> **⚠️ 需要 Google Workspace 账户。** 不支持个人 Gmail 账户。

## 适用场景
- 需要从本地自动化脚本创建、搜索、读取或编辑 Google Docs。
- 任务涉及文档文本提取、追加/插入操作或 Workspace 文档内容替换。
- 需要直接操作 Docs，无需依赖 MCP 服务器。

## 首次设置

Google 认证（将打开浏览器）：
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

所有操作通过 `scripts/docs.py` 执行。首次使用时若未登录会自动认证。

```bash
# 创建新文档
python scripts/docs.py create "Meeting Notes"

# 创建带初始内容的文档
python scripts/docs.py create "Project Plan" --content "# Overview\n\nThis is the project plan."

# 按标题查找文档
python scripts/docs.py find "meeting" --limit 10

# 获取文档文本内容
python scripts/docs.py get-text 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms

# 使用完整 URL 获取文本
python scripts/docs.py get-text "https://docs.google.com/document/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit"

# 在文档末尾追加文本
python scripts/docs.py append-text 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms "New paragraph at the end."

# 在文档开头插入文本
python scripts/docs.py insert-text 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms "Text at the beginning.\n\n"

# 替换文档中的文本
python scripts/docs.py replace-text 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms "old text" "new text"
```

## 文档 ID 格式

Google Docs 使用类似 `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms` 的文档 ID。你可以：
- 使用完整 URL（ID 会自动提取）
- 直接使用文档 ID
- 从 `find` 命令结果获取文档 ID

## Token 管理

Token 使用系统密钥环安全存储：
- **macOS**: Keychain
- **Windows**: Windows Credential Locker
- **Linux**: Secret Service API (GNOME Keyring, KDE Wallet 等)

服务名称：`google-docs-skill-oauth`

访问令牌过期时会通过 Google 云函数自动刷新。

## 限制
- 仅在任务明确符合上述范围时使用此技能。
- 输出内容不能替代特定环境的验证、测试或专家审查。
- 若缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
