---
name: runapi-cli
description: 使用 RunAPI CLI 从智能体生成 AI 图像、视频和音乐/音频。触发词：runapi、RunAPI CLI、AI图像生成、AI视频生成、AI音乐生成、模型调用、异步任务、runapi install、runapi auth
category: development
risk: critical
source: official
source_repo: runapi-ai/cli-skill
source_type: official
date_added: "2026-06-07"
author: runapi-ai
tags: [runapi, cli, models, automation, codex, claude, gemini]
tools: [claude, codex, gemini, cursor, antigravity]
license: "Apache-2.0"
license_source: "https://github.com/runapi-ai/cli-skill/blob/main/LICENSE"
---

# RunAPI 命令行工具

## 概述

`runapi` CLI 是 RunAPI 模型任务的执行层。当智能体需要生成 AI 图像、视频或音乐/音频、运行一次性模型任务、传递 JSON 请求体、等待异步任务完成，或在终端、服务器或 CI 作业中脚本化调用 RunAPI 时使用此工具。

源码仓库：[github.com/runapi-ai/cli-skill](https://github.com/runapi-ai/cli-skill)（Apache-2.0）

## 何时使用此技能

- 当用户要求从智能体运行 RunAPI 模型时使用。
- 当用户需要检查 RunAPI CLI 认证或账户状态时使用。
- 当用户需要向 RunAPI 服务传递 JSON 请求体时使用。
- 当用户需要提交异步 RunAPI 任务并等待完成时使用。
- 当用户希望在本地机器、服务器或 CI runner 上安装 RunAPI CLI 时使用。

## 安装

### macOS / Linux

```shell
brew install runapi-ai/tap/runapi
```

### 服务器 / CI

下载安装脚本，检查内容，然后在本地运行。

```shell
curl -fsSL https://runapi.ai/cli/install.sh -o runapi-install.sh
less runapi-install.sh
sh runapi-install.sh
```

锁定特定版本：

```shell
sh runapi-install.sh --version v0.1.0
```

安装脚本会自动检测操作系统和架构，从 `https://runapi.ai/cli/latest.json` 验证 SHA-256 校验和，如果验证失败则拒绝写入二进制文件。

## 认证

将 RunAPI 认证和生成操作视为安全敏感操作：命令可能调用远程服务、消耗额度并暴露账户状态。运行前先审查安装脚本，将 API 密钥保存在环境变量或 stdin 中，而非 shell 历史记录中。

先检查当前状态：

```shell
runapi auth status
```

| 来源 | 方式 |
|---|---|
| 环境变量 | 从环境读取 `RUNAPI_API_KEY` |
| 已保存配置 | `printf '%s' "$RUNAPI_API_KEY" \| runapi auth import-token --token -` |
| 浏览器登录 | 仅当用户明确要求浏览器认证时使用 `runapi login` |

`RUNAPI_BASE_URL` 可覆盖默认基础 URL。

避免在命令参数中直接传递密钥。优先使用 `RUNAPI_API_KEY` 或通过 `--token -` 从 stdin 导入令牌。

## 发现服务、命令和字段

CLI 以 JSON 为优先。每个服务公开类型化命令，每个命令通过 `--help` 文档化其请求字段。在构造请求前先查看命令帮助。

```shell
runapi --help
runapi suno --help
runapi suno text-to-music --help
```

## 运行模型

通过 `--input-file`、`--input` 或 stdin 以 JSON 格式传递请求体。默认流程为同步模式，会轮询直到任务完成。

```shell
runapi suno text-to-music --input-file request.json

runapi suno text-to-music --async --input-file request.json
runapi wait <task-id> --service suno --action text-to-music

runapi get <task-id> --service suno --action text-to-music
```

JSON 响应输出到 stdout；进度信息输出到 stderr。可管道传递给 `jq` 进行下游解析。

## 账户

```shell
runapi account info
runapi account balance
```

## 将技能安装到其他智能体运行时

```shell
runapi agent install-skill --target claude
runapi agent install-skill --target codex
runapi agent install-skill --target gemini
runapi agent install-skill --target openclaw
runapi agent list-targets
runapi agent install-skill --target-dir <path>
```

## 限制

- RunAPI 模型调用需要有效的 RunAPI 账户或 API 密钥。
- 部分模型任务运行时间较长，应使用 `--async` 加 `runapi wait`。
- 浏览器登录是交互式的，不应作为智能体的默认路径。
- 此技能不能替代模型特定的参数验证；构建请求 JSON 前请先查看命令帮助。

## 安全与注意事项

- 切勿将 API 密钥粘贴到示例命令或 PR 文本中。
- 优先使用 `RUNAPI_API_KEY` 或 stdin 令牌导入，而非命令行传递密钥。
- 不要默认从智能体运行交互式 `runapi login`。
- 在认定任务成功之前，务必检查 CLI 退出码。

## 参考资料

- RunAPI CLI 技能：https://github.com/runapi-ai/cli-skill
- RunAPI CLI 仓库：https://github.com/runapi-ai/cli
- RunAPI 模型目录：https://runapi.ai/models.md
