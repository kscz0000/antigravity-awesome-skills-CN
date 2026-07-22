---
name: windows-shell-reliability
description: "在 Windows 上可靠地执行命令：路径、编码以及常见二进制工具的陷阱。"
risk: safe
source: community
date_added: "2026-03-19"
---

# Windows Shell 可靠性模式

> 通过 PowerShell 和 CMD 在 Windows 上运行命令的最佳实践。

## 使用场景
在开发或调试运行于 Windows 系统的脚本与自动化任务时使用本技能，尤其是涉及文件路径、字符编码或标准 CLI 工具的场景。

---

## 1. 编码与重定向

### 关键：不同 PowerShell 版本的输出重定向差异
旧版 Windows PowerShell 在重定向原生命令的输出时可能会改写字节流，从而破坏后续处理。PowerShell 7.4+ 在重定向 stdout 时会保留原始字节流，因此只有当你面对的是旧版 shell 的行为，或者日志文件已经不可读时，才需要使用 UTF-8 转换这种变通方案。

| 问题 | 表现 | 解决方案 |
|---------|---------|----------|
| `dotnet > log.txt` | 在旧版 Windows PowerShell 中 `view_file` 失败 | `Get-Content log.txt \| Set-Content -Encoding utf8 log_utf8.txt` |
| `npm run > log.txt` | 需要一份包含错误信息的 UTF-8 文本日志 | `npm run ... 2>&1 \| Out-File -Encoding UTF8 log.txt` |

**规则：** 在 PowerShell 7.4+ 上优先直接使用原生重定向；只有当旧版 Windows PowerShell 的重定向产生不可读的日志时，才使用显式的 UTF-8 转换。

---

## 2. 处理路径与空格

### 关键：引号
Windows 路径经常包含空格。

| ❌ 错误 | ✅ 正确 |
|----------|-----------|
| `dotnet build src/my project/file.fsproj` | `dotnet build "src/my project/file.fsproj"` |
| `& C:\Path With Spaces\bin.exe` | `& "C:\Path With Spaces\bin.exe"` |

**规则：** 对可能包含空格的绝对路径和相对路径始终加上引号。

### 调用运算符（&）
在 PowerShell 中，如果可执行文件路径以引号开头，你必须使用 `&` 运算符。

**模式：**
```powershell
& "C:\Program Files\dotnet\dotnet.exe" build ...
```

---

## 3. 常见二进制与 Cmdlet 陷阱

| 操作 | ❌ CMD 风格 | ✅ PowerShell 选择 |
|--------|-------------|---------------------|
| 删除 | `del /f /q file` | `Remove-Item -Force file` |
| 复制 | `copy a b` | `Copy-Item a b` |
| 移动 | `move a b` | `Move-Item a b` |
| 建目录 | `mkdir folder` | `New-Item -ItemType Directory -Path folder` |

**提示：** 在 PowerShell 中使用 `ls`、`cat`、`cp` 等 CLI 别名通常没问题，但在脚本中使用完整的 cmdlet 更加健壮。

---

## 4. Dotnet CLI 可靠性

### 构建速度与一致性
| 场景 | 命令 | 原因 |
|---------|---------|-----|
| 快速迭代 | `dotnet build --no-restore` | 跳过冗余的 nuget restore。 |
| 全新构建 | `dotnet build --no-incremental` | 避免使用过期的构建产物。 |
| 后台运行 | `Start-Process dotnet -ArgumentList 'run' -RedirectStandardOutput output.txt -RedirectStandardError error.txt` | 启动应用且不阻塞 shell，同时保留日志。 |

---

## 5. 环境变量

| Shell | 语法 |
|-------|--------|
| PowerShell | `$env:VARIABLE_NAME` |
| CMD | `%VARIABLE_NAME%` |

---

## 6. 长路径
Windows 默认存在 260 字符的路径长度限制。

**修复方法：** 如果遇到长路径错误，请使用扩展路径前缀：
`\\?\C:\Very\Long\Path\...`

---

## 7. Shell 错误排查

| 错误 | 可能原因 | 修复方法 |
|-------|-------------|-----|
| `The term 'xxx' is not recognized` | 路径不在 $env:PATH 中 | 使用绝对路径或修复 PATH。 |
| `Access to the path is denied` | 文件被占用或权限不足 | 停止相关进程或以管理员身份运行。 |
| `Encoding mismatch` | 旧版 shell 重定向了输出 | 将文件以 UTF-8 重新导出，或使用 `2>&1 \| Out-File -Encoding UTF8` 捕获。 |

---

## 限制
- 仅当任务明确匹配上述使用范围时才使用本技能。
- 不要将本技能的输出视为针对特定环境的验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来并请求澄清。
