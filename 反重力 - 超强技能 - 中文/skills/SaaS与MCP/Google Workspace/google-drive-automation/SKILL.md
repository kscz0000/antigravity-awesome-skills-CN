---
name: google-drive-automation
description: "轻量级 Google Drive 集成，独立 OAuth 认证，无需 MCP 服务器，完整读写权限。触发词：Google Drive 自动化、云端硬盘操作、Drive 文件管理、Drive 上传下载、Drive 搜索、Drive 文件夹"
license: Apache-2.0
risk: critical
source: community
metadata:
  author: sanjay3290
  version: "1.0"
---

# Google Drive

轻量级 Google Drive 集成，独立 OAuth 认证，无需 MCP 服务器，完整读写权限。

> **需要 Google Workspace 账号。** 不支持个人 Gmail 账号。

## 适用场景
- 需要搜索、列出、上传、下载、移动或整理 Google Drive 文件和文件夹。
- 任务需要通过本地脚本在 Workspace 账号中进行直接的 Drive 读写自动化。
- 需要文件级 Drive 操作，但不想引入 MCP 服务器依赖。

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

## 读取命令

所有操作通过 `scripts/drive.py` 执行。首次使用时若未登录会自动认证。

```bash
# 搜索文件（全文搜索）
python scripts/drive.py search "quarterly report"

# 仅按标题搜索
python scripts/drive.py search "title:budget"

# 使用 Google Drive URL 搜索（自动提取 ID）
python scripts/drive.py search "https://drive.google.com/drive/folders/1ABC123..."

# 搜索共享给你的文件
python scripts/drive.py search --shared-with-me

# 分页搜索
python scripts/drive.py search "report" --limit 5 --page-token "..."

# 按精确名称查找文件夹
python scripts/drive.py find-folder "Project Documents"

# 列出 Drive 根目录文件
python scripts/drive.py list

# 列出指定文件夹中的文件
python scripts/drive.py list 1ABC123xyz --limit 20

# 下载文件
python scripts/drive.py download 1ABC123xyz ./downloads/report.pdf
```

## 写入命令

```bash
# 上传文件到 Drive 根目录
python scripts/drive.py upload ~/Documents/report.pdf

# 上传到指定文件夹
python scripts/drive.py upload ~/Documents/report.pdf --folder 1ABC123xyz

# 上传并自定义文件名
python scripts/drive.py upload ~/Documents/report.pdf --name "Q4 Report.pdf"

# 创建新文件夹
python scripts/drive.py create-folder "Project Documents"

# 在另一个文件夹内创建文件夹
python scripts/drive.py create-folder "Attachments" --parent 1ABC123xyz

# 将文件移动到其他文件夹
python scripts/drive.py move FILE_ID DESTINATION_FOLDER_ID

# 复制文件
python scripts/drive.py copy FILE_ID
python scripts/drive.py copy FILE_ID --name "Report Copy" --folder 1ABC123xyz

# 重命名文件或文件夹
python scripts/drive.py rename FILE_ID "New Name.pdf"

# 将文件移至回收站
python scripts/drive.py trash FILE_ID
```

## 搜索查询格式

搜索命令支持多种查询格式：

| 格式 | 示例 | 说明 |
|------|------|------|
| 全文搜索 | `"quarterly report"` | 搜索文件内容和名称 |
| 标题搜索 | `"title:budget"` | 仅搜索文件名称 |
| URL | `https://drive.google.com/...` | 自动提取并使用文件/文件夹 ID |
| 文件夹 ID | `1ABC123...` | 列出文件夹内容（25+ 字符 ID） |
| 原生查询 | `mimeType='application/pdf'` | 透传 Drive 查询语法 |

## 文件 ID 格式

Google Drive 使用长 ID，如 `1ABC123xyz_-abc123`。可从以下途径获取 ID：
- `search` 结果
- `find-folder` 结果
- `list` 结果
- Google Drive URL

## 下载限制

- 常规文件（PDF、图片等）可直接下载
- Google 文档/表格/幻灯片无法通过此工具下载
- 对于 Google Workspace 文件，请使用导出功能或专用工具

## 令牌管理

令牌使用系统密钥环安全存储：
- **macOS**：Keychain
- **Windows**：Windows Credential Locker
- **Linux**：Secret Service API（GNOME Keyring、KDE Wallet 等）

服务名称：`google-drive-skill-oauth`

使用 Google 云函数自动刷新过期令牌。

## 限制
- 仅在任务明确符合上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 若缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
