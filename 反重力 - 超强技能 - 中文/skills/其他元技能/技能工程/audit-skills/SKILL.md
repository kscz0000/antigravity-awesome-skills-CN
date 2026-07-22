---
name: audit-skills
description: "AI 技能与技能包的专家安全审计器。执行非侵入式静态分析，识别恶意模式、数据泄露、系统稳定性风险和混淆载荷，覆盖 Windows、macOS、Linux/Unix 和移动端（Android/iOS）。触发词：安全审计、技能审计、技能安全、安全扫描、恶意检测、跨平台安全、移动威胁检测"
category: security
risk: safe
source: community
date_added: "2026-03-07"
author: MAIOStudio
tags: [security, audit, skills, bundles, cross-platform]
tools: [claude, gemini, gpt, llama, mistral, etc]
---

<!-- security-allowlist: curl-pipe-bash -->

# Audit Skills（高级通用安全审计）

## 概述

AI 技能与技能包的专家安全审计器。执行非侵入式静态分析，识别恶意模式、数据泄露、系统稳定性风险和混淆载荷，覆盖 Windows、macOS、Linux/Unix 和移动端（Android/iOS）。
建议 2-4 句描述。

## 何时使用此技能

- 需要审计 AI 技能和技能包的安全漏洞时使用
- 进行跨平台安全分析时使用
- 用户询问验证技能合法性或执行安全审查时使用
- 扫描 AI 技能中的移动端威胁时使用

## 工作原理

### 步骤 1：静态分析

执行非侵入式静态分析，识别恶意模式、数据泄露、系统稳定性风险和混淆载荷。

### 步骤 2：平台特定威胁检测

分析跨 Windows、macOS、Linux/Unix 和移动端（Android/iOS）的平台特定安全问题。

#### 1. 权限、所有权与元数据篡改
- **提权访问**：`sudo`、`chown`、`chmod`、`TakeOwnership`、`icacls`、`Set-ExecutionPolicy`。
- **元数据篡改**：`touch -t`、`setfile`（macOS）、`attrib`（Windows）、`Set-ItemProperty`、`chflags`。
- **风险**：未授权访问、掩盖活动痕迹或使文件变为不可变。

#### 2. 文件/文件夹锁定与资源拒绝
- **模式**：`chmod 000`、`chattr +i`（不可变）、`attrib +r +s +h`、`icacls` 中的 `Deny` ACE。
- **全局操作**：锁定或隐藏 `%USERPROFILE%`、`/Users/` 或 `/etc/` 中的文件夹。
- **风险**：拒绝服务或数据锁定。

#### 3. 脚本执行与批处理调用
- **传统/批处理 Windows**：`.bat`、`.cmd`、`cmd.exe /c`、`vbs`、`cscript`、`wscript`。
- **Unix Shell**：`.sh`、`.bash`、`.zsh`、`chmod +x` 后执行。
- **PowerShell**：`.ps1`、`powershell -ExecutionPolicy Bypass -File ...`。
- **隐藏标志**：`-WindowStyle Hidden`、`-w hidden`、`-noprofile`。

#### 4. 危险安装/卸载与系统变更
- **Windows**：`msiexec /qn`、`choco uninstall`、`reg delete`。
- **Linux/Unix**：`apt-get purge`、`yum remove`、`rm -rf /usr/bin/...`。
- **macOS**：`brew uninstall`、从 `/Applications` 删除。
- **风险**：移除安全软件或创建不受监控的安装路径。

#### 5. 移动应用与操作系统安全（Android/iOS）
- **Android 工具**：`adb shell`、`pm install`、`am start`、`apktool`、`dex2jar`、`keytool`。
- **Android 文件**：篡改 `AndroidManifest.xml`（权限）、`classes.dex` 或 `strings.xml`。
- **iOS 工具**：`xcodebuild`、`codesign`、`security find-identity`、`fastlane`、`xcrun`。
- **iOS 文件**：篡改 `Info.plist`、`Entitlements.plist` 或 `Provisioning Profiles`。
- **移动端模式**：越狱/Root 检测绕过、移动源码中的硬编码 API 密钥、非移动技能中的敏感权限请求（相机、GPS、通讯录）。
- **风险**：恶意移动包注入、从移动构建中窃取凭证或通过 ADB 操控设备。

#### 6. 信息泄露与网络外泄
- **模式**：`curl`、`wget`、`Invoke-WebRequest`、`Invoke-RestMethod`、`scp`、`ftp`、`nc`、`socat`。
- **敏感数据**：`.env`、`.ssh`、`cookies.sqlite`、`Keychains`（macOS）、`Credentials`（Windows）、`keystore`（Android）。
- **内网**：扫描内部 IP 或映射本地服务。

#### 7. 服务、进程与稳定性操控
- **Windows**：`Stop-Service`、`taskkill /f`、`sc.exe delete`。
- **Unix/Mac**：`kill -9`、`pkill`、`systemctl disable/stop`、`launchctl unload`。
- **底层操作**：直接磁盘访问（`dd`）、固件/BIOS 调用、内核模块管理。

#### 8. 混淆与持久化
- **编码**：`Base64`、`Hex`、`XOR` 循环、`atob()`。
- **持久化**：`reg add`（Run 键）、`schtasks`、`crontab`、`launchctl`（macOS）、`systemd` 单元。
- **管道**：`curl ... | bash`、`iwr ... | iex`。

#### 9. 合法性与范围（通用）
- **注册表对齐**：与 `CATALOG.md` 交叉引用。
- **结构完整性**：是否遵循标准仓库布局？
- **健康范围**："UI 设计"技能需要 `adb shell` 或 `sudo` 吗？

### 步骤 3：报告生成

生成安全报告，包含评分（0-10）、平台目标识别、标记操作、威胁分析和缓解建议。

## 示例

### 示例 1：安全审查

```markdown
"对此技能包执行安全审计"
```

### 示例 2：跨平台威胁分析

```markdown
"扫描此 AI 技能中的移动端威胁"
```

## 最佳实践

- ✅ 执行非侵入式分析
- ✅ 检查提权模式
- ✅ 查找信息泄露漏洞
- ✅ 分析跨平台威胁
- ❌ 审计期间不要执行潜在恶意代码
- ❌ 不要修改被审计的代码
- ❌ 不要忽略移动端特定的安全问题

## 常见陷阱

- **问题**：审计期间执行代码
  **解决方案**：仅使用静态分析方法

- **问题**：遗漏跨平台威胁
  **解决方案**：检查所有支持平台上的平台特定安全问题

- **问题**：未能检测混淆载荷
  **解决方案**：查找编码模式，如 Base64、Hex、XOR 循环和 atob()

## 相关技能

- `@security-scanner` - 额外的安全扫描能力

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
