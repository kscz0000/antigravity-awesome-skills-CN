---
name: powershell-windows
description: "PowerShell Windows 模式。涵盖关键陷阱、运算符语法和错误处理。当用户要求编写、调试或审查 PowerShell 脚本时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# PowerShell Windows 模式

> Windows PowerShell 的关键模式与常见陷阱。

---

## 1. 运算符语法规则

### 关键：必须使用括号

| ❌ 错误写法 | ✅ 正确写法 |
|----------|-----------|
| `if (Test-Path "a" -or Test-Path "b")` | `if ((Test-Path "a") -or (Test-Path "b"))` |
| `if (Get-Item $x -and $y -eq 5)` | `if ((Get-Item $x) -and ($y -eq 5))` |

**规则：** 使用逻辑运算符时，每个 cmdlet 调用必须用括号包裹。

---

## 2. Unicode/Emoji 限制

### 关键：脚本中禁止使用 Unicode

| 用途 | ❌ 不要使用 | ✅ 使用 |
|---------|-------------|--------|
| 成功 | ✅ ✓ | [OK] [+] |
| 错误 | ❌ ✗ 🔴 | [!] [X] |
| 警告 | ⚠️ 🟡 | [*] [WARN] |
| 信息 | ℹ️ 🔵 | [i] [INFO] |
| 进度 | ⏳ | [...] |

**规则：** PowerShell 脚本中仅使用 ASCII 字符。

---

## 3. 空值检查模式

### 访问前必须先检查

| ❌ 错误写法 | ✅ 正确写法 |
|----------|-----------|
| `$array.Count -gt 0` | `$array -and $array.Count -gt 0` |
| `$text.Length` | `if ($text) { $text.Length }` |

---

## 4. 字符串插值

### 复杂表达式

| ❌ 错误写法 | ✅ 正确写法 |
|----------|-----------|
| `"Value: $($obj.prop.sub)"` | 先存入变量再引用 |

**模式：**
```
$value = $obj.prop.sub
Write-Output "Value: $value"
```

---

## 5. 错误处理

### ErrorActionPreference

| 值 | 适用场景 |
|-------|-----|
| Stop | 开发阶段（快速失败） |
| Continue | 生产脚本 |
| SilentlyContinue | 预期会有错误时 |

### Try/Catch 模式

- 不要在 try 块内 return
- 使用 finally 做清理工作
- 在 try/catch 之后再 return

---

## 6. 文件路径

### Windows 路径规则

| 模式 | 用法 |
|---------|-----|
| 字面路径 | `C:\Users\User\file.txt` |
| 变量路径 | `Join-Path $env:USERPROFILE "file.txt"` |
| 相对路径 | `Join-Path $ScriptDir "data"` |

**规则：** 使用 Join-Path 确保跨平台兼容性。

---

## 7. 数组操作

### 正确模式

| 操作 | 语法 |
|-----------|--------|
| 空数组 | `$array = @()` |
| 添加元素 | `$array += $item` |
| ArrayList 添加 | `$list.Add($item) | Out-Null` |

---

## 8. JSON 操作

### 关键：Depth 参数

| ❌ 错误写法 | ✅ 正确写法 |
|----------|-----------|
| `ConvertTo-Json` | `ConvertTo-Json -Depth 10` |

**规则：** 处理嵌套对象时必须指定 `-Depth`。

### 文件操作

| 操作 | 模式 |
|-----------|---------|
| 读取 | `Get-Content "file.json" -Raw | ConvertFrom-Json` |
| 写入 | `$data | ConvertTo-Json -Depth 10 | Out-File "file.json" -Encoding UTF8` |

---

## 9. 常见错误

| 错误信息 | 原因 | 修复方法 |
|---------------|-------|-----|
| "parameter 'or'" | 缺少括号 | 用括号包裹 cmdlet |
| "Unexpected token" | Unicode 字符 | 仅使用 ASCII |
| "Cannot find property" | 空对象 | 先检查空值 |
| "Cannot convert" | 类型不匹配 | 使用 .ToString() |

---

## 10. 脚本模板

```powershell
# Strict mode
Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

# Paths
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Main
try {
    # Logic here
    Write-Output "[OK] Done"
    exit 0
}
catch {
    Write-Warning "Error: $_"
    exit 1
}
```

---

> **记住：** PowerShell 有独特的语法规则。括号包裹、仅用 ASCII、空值检查是不可妥协的基本要求。

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，应停下来请求澄清。
