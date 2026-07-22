---
name: google-slides-automation
description: "轻量级 Google Slides 集成，独立 OAuth 认证，无需 MCP 服务器，完整读写权限。当用户要求'操作 Google 幻灯片'、'创建演示文稿'、'读取幻灯片内容'、'批量更新幻灯片'时使用。"
license: Apache-2.0
risk: critical
source: community
metadata:
  author: sanjay3290
  version: "1.0"
---

# Google Slides

轻量级 Google Slides 集成，独立 OAuth 认证，无需 MCP 服务器，完整读写权限。

> **需要 Google Workspace 账户。** 不支持个人 Gmail 账户。

## 使用场景
- 需要通过本地自动化创建、检查或修改 Google Slides 演示文稿
- 任务涉及读取幻灯片文本、添加/删除幻灯片或批量更新演示文稿内容
- 希望在不使用 MCP 服务器的情况下实现 Workspace 文档的 Slides 自动化

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

## 读取命令

所有操作通过 `scripts/slides.py` 执行。首次使用时若未登录会自动认证。

```bash
# 获取演示文稿中的所有文本内容
python scripts/slides.py get-text "1abc123xyz789"
python scripts/slides.py get-text "https://docs.google.com/presentation/d/1abc123xyz789/edit"

# 通过搜索查询查找演示文稿
python scripts/slides.py find "quarterly report"
python scripts/slides.py find "project proposal" --limit 5

# 获取演示文稿元数据（标题、幻灯片数量、幻灯片对象 ID）
python scripts/slides.py get-metadata "1abc123xyz789"
```

## 写入命令

```bash
# 创建新的空白演示文稿
python scripts/slides.py create "Q4 Sales Report"

# 在末尾添加空白幻灯片
python scripts/slides.py add-slide "1abc123xyz789"

# 使用指定布局添加幻灯片
python scripts/slides.py add-slide "1abc123xyz789" --layout TITLE_AND_BODY

# 在指定位置添加幻灯片（从 0 开始计数）
python scripts/slides.py add-slide "1abc123xyz789" --layout TITLE --at 0

# 在所有幻灯片中查找并替换文本
python scripts/slides.py replace-text "1abc123xyz789" "old text" "new text"
python scripts/slides.py replace-text "1abc123xyz789" "Draft" "Final" --match-case

# 通过对象 ID 删除幻灯片（使用 get-metadata 查找 ID）
python scripts/slides.py delete-slide "1abc123xyz789" "g123abc456"

# 批量更新（高级功能 - 用于格式化、插入形状、图片等）
python scripts/slides.py batch-update "1abc123xyz789" '[{"replaceAllText":{"containsText":{"text":"foo"},"replaceText":"bar"}}]'
```

## 幻灯片布局

`add-slide --layout` 可用的布局：
- `BLANK` - 空白幻灯片（默认）
- `TITLE` - 标题幻灯片
- `TITLE_AND_BODY` - 标题加正文
- `TITLE_AND_TWO_COLUMNS` - 标题加双栏文本
- `TITLE_ONLY` - 仅标题栏
- `SECTION_HEADER` - 章节分隔页
- `ONE_COLUMN_TEXT` - 单栏文本
- `MAIN_POINT` - 主要观点高亮
- `BIG_NUMBER` - 大数字展示

## 演示文稿 ID 格式

可以使用以下任一格式：
- 直接使用演示文稿 ID：`1abc123xyz789`
- 完整 Google Slides URL：`https://docs.google.com/presentation/d/1abc123xyz789/edit`

脚本会自动从 URL 中提取 ID。

## 输出格式

### get-text
返回从所有幻灯片中提取的文本，包括：
- 演示文稿标题
- 每张幻灯片上形状/文本框中的文本
- 表格数据及单元格内容

### find
返回匹配的演示文稿列表：
```json
{
  "presentations": [
    {"id": "1abc...", "name": "Q4 Report", "modifiedTime": "2024-01-15T..."}
  ],
  "nextPageToken": "..."
}
```

### get-metadata
返回演示文稿详情：
```json
{
  "presentationId": "1abc...",
  "title": "My Presentation",
  "slideCount": 15,
  "pageSize": {"width": {...}, "height": {...}},
  "hasMasters": true,
  "hasLayouts": true
}
```

## Token 管理

Token 使用系统密钥环安全存储：
- **macOS**: Keychain
- **Windows**: Windows Credential Locker
- **Linux**: Secret Service API（GNOME Keyring、KDE Wallet 等）

服务名称：`google-slides-skill-oauth`

使用 Google 云函数自动刷新过期的 token。

## 限制
- 仅在任务明确符合上述范围时使用此技能
- 输出不能替代环境特定的验证、测试或专家审查
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清
