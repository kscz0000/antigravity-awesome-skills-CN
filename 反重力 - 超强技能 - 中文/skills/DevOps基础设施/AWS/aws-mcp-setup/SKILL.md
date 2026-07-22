---
name: aws-mcp-setup
description: 为 AI 智能体配置 AWS MCP 服务器，提供文档搜索与 API 调用能力。当需要设置 AWS MCP、配置 AWS 文档工具、排查 MCP 连接问题时使用，或当用户提及 aws-mcp、awsdocs、uvx 安装、MCP 服务器配置时触发。同时覆盖完整版 AWS MCP 服务器（带身份认证）与免认证的 AWS 文档 MCP 服务器两种方案。触发词：AWS MCP、aws-mcp、awsdocs、uvx 安装、MCP 配置、AWS 文档搜索、API 调用。
risk: unknown
source: https://github.com/zxkane/aws-skills/tree/main/plugins/aws-common/skills/aws-mcp-setup
source_repo: zxkane/aws-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/zxkane/aws-skills/blob/main/LICENSE
---

# AWS MCP 服务器配置指南
## 适用场景

当你需要为 AI 智能体配置 AWS MCP 服务器以提供文档搜索和 API 调用能力时使用本技能。适用于设置 AWS MCP、配置 AWS 文档工具、排查 MCP 连接问题的场景，或当用户提及 aws-mcp、awsdocs、uvx 安装、MCP 服务器配置时触发。同时覆盖完整版 AWS MCP 服务器（带身份认证）与免认证的 AWS 文档 MCP 服务器两种方案。


## 概述

本指南帮助你为 AI 智能体配置 AWS MCP 工具。共有两种方案可选：

| 方案 | 前置要求 | 支持能力 |
|--------|--------------|--------------|
| **完整版 AWS MCP 服务器** | Python 3.10+、uvx、AWS 凭证 | 执行 AWS API 调用 + 文档搜索 |
| **AWS 文档 MCP** | 无 | 仅文档搜索 |

## 步骤 1：检查现有配置

配置前，先用以下任一方法确认 AWS MCP 工具是否已经可用：

### 方法 A：检查可用工具（推荐）

在你的智能体可用工具列表中查找以下工具名模式：
- `mcp__aws-mcp__*` 或 `mcp__aws__*` → 已配置完整版 AWS MCP 服务器
- `mcp__*awsdocs*__aws___*` → 已配置 AWS 文档 MCP

**如何检查**：运行 `/mcp` 命令列出所有当前激活的 MCP 服务器。

### 方法 B：检查配置文件

智能体工具采用分层配置（优先级：本地 → 项目 → 用户 → 企业）：

| 作用域 | 文件位置 | 用途 |
|-------|---------------|----------|
| Local | `.claude.json`（项目内） | 个人或试验用途 |
| Project | `.mcp.json`（项目根目录） | 团队共享 |
| User | `~/.claude.json` | 跨项目个人配置 |
| Enterprise | 系统管理目录 | 全组织统一 |

在这些文件中查找含有 `aws-mcp`、`aws` 或 `awsdocs` 键的 `mcpServers`：

```bash
# 检查项目配置
cat .mcp.json 2>/dev/null | grep -E '"(aws-mcp|aws|awsdocs)"'

# 检查用户配置
cat ~/.claude.json 2>/dev/null | grep -E '"(aws-mcp|aws|awsdocs)"'

# 或使用 Claude CLI
claude mcp list
```

若 AWS MCP 已经配置好，则无需重复配置。

## 步骤 2：选择配置方案

### 自动检测

运行以下命令判断应使用哪种方案：

```bash
# 检查 uvx（需 Python 3.10+）
which uvx || echo "uvx not available"

# 检查 AWS 凭证是否有效
aws sts get-caller-identity || echo "AWS credentials not configured"
```

### 方案 A：完整版 AWS MCP 服务器（推荐）

**适用条件**：uvx 可用 且 AWS 凭证有效

**前置条件**：
- Python 3.10+，并安装了 `uv` 包管理器
- 已配置 AWS 凭证（可通过 profile、环境变量或 IAM 角色）

**必需的 IAM 权限**：
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": [
      "aws-mcp:InvokeMCP",
      "aws-mcp:CallReadOnlyTool",
      "aws-mcp:CallReadWriteTool"
    ],
    "Resource": "*"
  }]
}
```

**配置项**（添加到你的 MCP 设置中）：
```json
{
  "mcpServers": {
    "aws-mcp": {
      "command": "uvx",
      "args": [
        "mcp-proxy-for-aws@latest",
        "https://aws-mcp.us-east-1.api.aws/mcp",
        "--metadata", "AWS_REGION=us-west-2"
      ]
    }
  }
}
```

**凭证配置选项**：

1. **AWS Profile**（推荐用于开发场景）：
   ```json
   "args": [
     "mcp-proxy-for-aws@latest",
     "https://aws-mcp.us-east-1.api.aws/mcp",
     "--profile", "my-profile",
     "--metadata", "AWS_REGION=us-west-2"
   ]
   ```

2. **环境变量**：
   ```json
   "env": {
     "AWS_ACCESS_KEY_ID": "...",
     "AWS_SECRET_ACCESS_KEY": "...",
     "AWS_REGION": "us-west-2"
   }
   ```

3. **IAM 角色**（适用于 EC2/ECS/Lambda）：无需额外配置，会自动使用实例元数据凭证

**附加选项**：
- `--region <region>`：覆盖 AWS 区域
- `--read-only`：限制为只读工具
- `--log-level <level>`：设置日志级别（debug、info、warning、error）

**参考链接**：https://github.com/aws/mcp-proxy-for-aws

### 方案 B：AWS 文档 MCP 服务器（免认证）

**适用条件**：
- 没有 Python/uvx 环境
- 没有 AWS 凭证
- 仅需要文档搜索（不需要执行 API）

**配置项**：
```json
{
  "mcpServers": {
    "awsdocs": {
      "type": "http",
      "url": "https://knowledge-mcp.global.api.aws"
    }
  }
}
```

## 步骤 3：验证

配置完成后，请验证工具是否可用：

**完整版 AWS MCP**：
- 查找工具：`mcp__aws-mcp__aws___search_documentation`、`mcp__aws-mcp__aws___call_aws`

**文档 MCP**：
- 查找工具：`mcp__awsdocs__aws___search_documentation`、`mcp__awsdocs__aws___read_documentation`

## 故障排除

| 问题 | 原因 | 解决方案 |
|-------|-------|----------|
| `uvx: command not found` | 未安装 uv | 用 `pip install uv` 安装，或改用方案 B |
| `AccessDenied` 错误 | 缺少 IAM 权限 | 在 IAM 策略中加入 aws-mcp:* 权限 |
| `InvalidSignatureException` | 凭证问题 | 运行 `aws sts get-caller-identity` 检查 |
| 工具未出现 | MCP 未启动 | 配置变更后重启智能体 |

## 使用限制

- 仅在任务需求与上游来源和本地项目上下文明确匹配时使用本技能。
- 在应用任何变更前，请先验证命令、生成的代码、依赖、凭证以及外部服务行为。
- 不要将示例直接当作特定环境下的测试、安全审查或破坏性/高成本操作的用户授权依据来使用。
