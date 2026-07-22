---
name: vscode-extension-guide-en
description: "VS Code 扩展开发全流程指南，涵盖脚手架搭建到 Marketplace 发布。触发词：VS Code 扩展、扩展开发、Marketplace 发布、TreeView、Webview、CSP 安全、扩展打包、扩展激活"
category: core-dev
risk: safe
source: community
source_repo: lewiswigmore/agent-skills
source_type: community
date_added: "2026-04-12"
author: lewiswigmore
tags: [vscode, extension, ide, typescript, marketplace]
tools: [claude, cursor, copilot, codex, gemini]
---

# VS Code 扩展开发指南（英文）

## 概述

本指南为英文版本，介绍如何构建 VS Code 扩展，涵盖从脚手架搭建到 Marketplace 发布的完整生命周期。包含 Webview 模式、CSP 安全、TreeView、测试、打包与故障排查的参考资料。基于 VS Code 1.74+ API 更新。

改编自 aktsmm/agent-skills（CC BY-NC-SA 4.0），翻译为英文并针对当前 VS Code API 进行了修正。

## 何时使用本技能

- 从零开始创建新的 VS Code 扩展时
- 为扩展添加命令、快捷键或设置时
- 在扩展中构建 TreeView 或 Webview UI 时
- 将扩展发布到 VS Code Marketplace 时
- 排查扩展激活或打包问题时

## 工作原理

### 快速开始

```bash
npm install -g yo generator-code
yo code
```

### 项目结构

```
my-extension/
├── package.json          # Extension manifest
├── src/extension.ts      # Entry point
├── out/                  # Compiled JS
├── images/icon.png       # 128x128 PNG for Marketplace
└── .vscodeignore         # Exclude files from VSIX
```

### 构建与打包

```bash
npm run compile           # Build once
npm run watch             # Watch mode (F5 to launch debug)
npx @vscode/vsce package  # Creates .vsix
```

## 参考主题

完整技能包含以下详细参考文档：

- **Webview 模式**：CSP 安全与消息传递
- **TreeView**：数据提供者与拖放支持
- **测试**：基于 @vscode/test-electron 的测试设置
- **发布**：发布到 VS Code Marketplace
- **AI 定制**：针对扩展项目的 AI 定制
- **代码审查提示词**：针对扩展代码的审查
- **故障排查**：常见扩展问题排查

## 安装完整技能

如需获取包含所有参考文档的完整指南：

```bash
npx skills add lewiswigmore/agent-skills --skill vscode-extension-guide-en
```

## 最佳实践

- 发布前统一 package 名称、设置键、命令 ID 与视图 ID
- 使用 `.vscodeignore` 将包体积控制在 5MB 以内
- 自 VS Code 1.74 起，`activationEvents` 可针对已贡献的命令和视图自动检测
- 打包前始终使用 Extension Development Host（F5）进行测试

## 常见陷阱

- **问题：** 扩展无法加载
  **解决方案：** 检查 `activationEvents`。自 VS Code 1.74 起，针对已贡献的命令/视图可自动检测。

- **问题：** 找不到命令
  **解决方案：** 确保 package.json 与代码中的命令 ID 完全一致。

- **问题：** Webview 内容无法显示
  **解决方案：** 检查 Content Security Policy，使用 webview 的 `cspSource` 属性。

## 相关技能

- `@test-driven-development` - 在实现扩展功能前先编写测试
- `@debugging-strategies` - 对扩展问题进行系统性故障排查

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 请勿将输出结果替代针对特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
