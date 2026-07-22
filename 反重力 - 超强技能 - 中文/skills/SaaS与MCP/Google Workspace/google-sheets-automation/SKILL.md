---
name: google-sheets-automation
description: "轻量级 Google Sheets 集成，独立 OAuth 认证。无需 MCP 服务器。完整读写权限。当用户要求'Google Sheets 自动化'、'操作电子表格'、'读写 Google Sheets'时使用。"
risk: critical
source: community
license: Apache-2.0
metadata:
  author: sanjay3290
  version: "1.0"
---

# Google Sheets

轻量级 Google Sheets 集成，独立 OAuth 认证。无需 MCP 服务器。完整读写权限。

> **需要 Google Workspace 账户。** 不支持个人 Gmail 账户。

## 首次设置

通过 Google 认证（打开浏览器）：
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

所有操作通过 `scripts/sheets.py` 执行。首次使用时若未登录会自动认证。

```bash
# 获取电子表格内容为纯文本（默认）
python scripts/sheets.py get-text SPREADSHEET_ID

# 获取电子表格内容为 CSV
python scripts/sheets.py get-text SPREADSHEET_ID --format csv

# 获取电子表格内容为 JSON
python scripts/sheets.py get-text SPREADSHEET_ID --format json

# 获取指定范围的值（A1 表示法）
python scripts/sheets.py get-range SPREADSHEET_ID "Sheet1!A1:D10"
python scripts/sheets.py get-range SPREADSHEET_ID "A1:C5"

# 通过搜索查询查找电子表格
python scripts/sheets.py find "budget 2024"
python scripts/sheets.py find "sales report" --limit 5

# 获取电子表格元数据（工作表、维度等）
python scripts/sheets.py get-metadata SPREADSHEET_ID
```

## 写入命令

```bash
# 用值更新单元格范围（JSON 二维数组）
python scripts/sheets.py update-range SPREADSHEET_ID "Sheet1!A1:B2" '[["Hello","World"],["Foo","Bar"]]'

# 使用 RAW 输入更新（不解析公式，将所有内容视为字面文本）
python scripts/sheets.py update-range SPREADSHEET_ID "Sheet1!A1:B1" '[["=SUM(A1:A5)","text"]]' --raw

# 在最后一行数据后追加行
python scripts/sheets.py append-rows SPREADSHEET_ID "Sheet1!A:Z" '[["New Row Col A","New Row Col B"]]'

# 清除范围内的值（保留格式）
python scripts/sheets.py clear-range SPREADSHEET_ID "Sheet1!A1:B10"

# 批量更新（高级 - 用于格式化、合并等）
python scripts/sheets.py batch-update SPREADSHEET_ID '[{"updateCells":{"range":{"sheetId":0},"fields":"userEnteredValue"}}]'
```

## 电子表格 ID

可以使用：
- 电子表格 ID：`1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`
- 完整 URL：`https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit`

脚本会自动从 URL 中提取 ID。

## 输出格式

### 文本（默认）
人类可读格式，使用管道符分隔：
```
Spreadsheet Title: Sales Data
Sheet Name: Q1
Name | Revenue | Units
Product A | 10000 | 50
Product B | 15000 | 75
```

### CSV
标准 CSV 格式，适合后续处理：
```
Name,Revenue,Units
Product A,10000,50
Product B,15000,75
```

### JSON
结构化数据格式：
```json
{
  "Q1": [
    ["Name", "Revenue", "Units"],
    ["Product A", "10000", "50"]
  ]
}
```

## A1 表示法示例

- `Sheet1!A1:B10` - Sheet1 上 A1 到 B10 的范围
- `Sheet1!A:A` - Sheet1 上 A 列的全部
- `Sheet1!1:1` - Sheet1 上第 1 行的全部
- `A1:C5` - 第一个工作表上的范围

## 值输入选项

- **USER_ENTERED**（默认）：值被解析为用户输入。数字、日期和公式会被解释。
- **RAW**（`--raw` 标志）：值完全按提供的方式存储。不解析公式或数字格式。

## Token 管理

Token 使用系统密钥环安全存储：
- **macOS**：Keychain
- **Windows**：Windows Credential Locker
- **Linux**：Secret Service API（GNOME Keyring、KDE Wallet 等）

服务名称：`google-sheets-skill-oauth`

Token 过期时使用 Google 云函数自动刷新。


## 使用时机
当处理与上述主要领域或功能相关的任务时使用此技能。

## 限制
- 仅在任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
