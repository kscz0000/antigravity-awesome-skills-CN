---
name: busybox-on-windows
description: "如何在 Windows 上使用 BusyBox 的 Win32 构建版来运行许多标准 UNIX 命令行工具。当用户要求在 Windows 上使用 BusyBox、运行 UNIX 命令、或需要 busybox.exe 时使用。"
risk: safe
source: community
date_added: "2026-02-27"
---

BusyBox 是一个单一二进制文件，实现了许多常见的 Unix 工具。

此技能仅在 Windows 上使用。如果你在 UNIX 系统上，请到此为止。

仅当在此文档所在目录下找不到 `busybox.exe` 文件时，才执行以下步骤。
这些是 PowerShell 命令，如果你使用的是传统 `cmd.exe` 终端，则必须使用 `powershell -Command "..."` 来运行它们。
1. 打印 CPU 类型：`Get-CimInstance -ClassName Win32_Processor | Select-Object Name, NumberOfCores, MaxClockSpeed`
2. 打印操作系统版本：`Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion" | Select-Object ProductName, DisplayVersion, CurrentBuild`
3. 运行以下 PowerShell 命令之一来下载适合的 BusyBox 构建版：
   - 32 位 x86 (ANSI)：`$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://frippery.org/files/busybox/busybox.exe -OutFile busybox.exe`
   - 64 位 x86 (ANSI)：`$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://frippery.org/files/busybox/busybox64.exe -OutFile busybox.exe`
   - 64 位 x86 (Unicode)：`$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://frippery.org/files/busybox/busybox64u.exe -OutFile busybox.exe`
   - 64 位 ARM (Unicode)：`$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://frippery.org/files/busybox/busybox64a.exe -OutFile busybox.exe`

常用命令：
- 帮助：`busybox.exe --list`
- 可用的 UNIX 命令：`busybox.exe --list`

用法：在 UNIX 命令前加上 `busybox.exe` 前缀，例如：`busybox.exe ls -1`

如果需要在其他工作目录下运行 UNIX 命令，请使用 `busybox.exe` 的绝对路径。

文档：https://frippery.org/busybox/
BusyBox 原项目：https://busybox.net/

## 何时使用
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
