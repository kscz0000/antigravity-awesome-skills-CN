---
name: using-neon
description: "Neon 是一个无服务器 Postgres 平台，将计算和存储分离，提供自动扩缩容、分支、即时恢复和缩容至零。它完全兼容 Postgres，适用于任何支持 Postgres 的语言、框架或 ORM。触发词：Neon、无服务器Postgres、Neon数据库、Postgres分支、自动扩缩容、serverless postgres"
risk: safe
source: "https://github.com/neondatabase/agent-skills/tree/main/skills/neon-postgres"
date_added: "2026-02-27"
---

# Neon 无服务器 Postgres

Neon 是一个无服务器 Postgres 平台，将计算和存储分离，提供自动扩缩容、分支、即时恢复和缩容至零。它完全兼容 Postgres，适用于任何支持 Postgres 的语言、框架或 ORM。

## 何时使用此技能

在以下情况下使用此技能：
- 使用 Neon 无服务器 Postgres
- 设置 Neon 数据库
- 为 Neon 选择连接方式
- 使用 Neon 功能如分支或自动扩缩容
- 使用 Neon 认证或 API
- 关于 Neon 最佳实践的问题

## Neon 文档

在做出与 Neon 相关的声明之前，请始终参考 Neon 文档。文档是所有 Neon 相关信息的真实来源。

下面你将找到按关注领域组织的资源列表。这旨在帮助你找到正确的文档页面以获取，并提供一些额外上下文。

你可以使用 `curl` 命令以 markdown 格式获取文档页面：

**文档：**

```bash
# 获取所有 Neon 文档列表
curl https://neon.com/llms.txt

# 以 markdown 格式获取任意文档页面
curl -H "Accept: text/markdown" https://neon.com/docs/<path>
```

不要猜测文档页面。使用 `llms.txt` 索引查找相关 URL 或跟随下方资源中的链接。

## 资源概览

根据用户需求参考相应的资源文件：

### 核心指南

| 领域               | 资源                               | 何时使用                                         |
| ------------------ | ---------------------------------- | ------------------------------------------------ |
| Neon 是什么        | `references/what-is-neon.md`       | 理解 Neon 概念、架构、核心资源                   |
| 参考文档           | `references/referencing-docs.md`   | 查阅官方文档、验证信息                           |
| 功能               | `references/features.md`           | 分支、自动扩缩容、缩容至零、即时恢复             |
| 快速入门           | `references/getting-started.md`    | 设置项目、连接字符串、依赖项、模式              |
| 连接方式           | `references/connection-methods.md` | 根据平台和运行时选择驱动                         |
| 开发者工具         | `references/devtools.md`           | VSCode 扩展、MCP 服务器、Neon CLI (`neon init`)  |

### 数据库驱动与 ORM

用于无服务器/边缘函数的 HTTP/WebSocket 查询。

| 领域              | 资源                              | 何时使用                                         |
| ----------------- | --------------------------------- | ------------------------------------------------ |
| 无服务器驱动      | `references/neon-serverless.md`   | `@neondatabase/serverless` - HTTP/WebSocket 查询 |
| Drizzle ORM       | `references/neon-drizzle.md`      | Drizzle ORM 与 Neon 集成                         |

### 认证与数据 API SDK

Neon 的认证和 PostgREST 风格数据 API。

| 领域        | 资源                        | 何时使用                                                     |
| ----------- | --------------------------- | ------------------------------------------------------------ |
| Neon Auth   | `references/neon-auth.md`   | `@neondatabase/auth` - 仅认证                                |
| Neon JS SDK | `references/neon-js.md`     | `@neondatabase/neon-js` - 认证 + 数据 API（PostgREST 风格查询）|

### Neon 平台 API 与 CLI

通过 REST API、SDK 或 CLI 以编程方式管理 Neon 资源。

| 领域                  | 资源                                | 何时使用                               |
| --------------------- | ----------------------------------- | -------------------------------------- |
| 平台 API 概览         | `references/neon-platform-api.md`   | 通过 REST API 管理 Neon 资源           |
| Neon CLI              | `references/neon-cli.md`            | 终端工作流、脚本、CI/CD 管道          |
| TypeScript SDK        | `references/neon-typescript-sdk.md` | `@neondatabase/api-client`             |
| Python SDK            | `references/neon-python-sdk.md`     | `neon-api` 包                          |

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
