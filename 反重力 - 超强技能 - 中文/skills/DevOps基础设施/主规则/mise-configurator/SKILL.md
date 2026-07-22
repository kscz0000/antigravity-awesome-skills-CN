---
name: mise-configurator
description: "生成生产级 mise.toml 配置，用于本地开发、CI/CD 流水线和工具链标准化。当用户要求'配置 mise'、'生成 mise.toml'、'统一运行时版本'或'迁移 asdf/nvm/pyenv'时使用。"
category: devops
risk: safe
source: self
source_type: self
date_added: "2026-04-16"
author: community
tags: [mise, devops, ci-cd, toolchain, runtimes, automation]
tools: [claude, cursor, gemini]
---
# Mise Configurator

## 概述

本技能生成简洁、生产级的 `mise.toml` 配置，适用于本地开发环境和 CI/CD 流水线。

它能统一运行时版本、简化项目上手流程、替代 `asdf`/`nvm`/`pyenv` 等旧版版本管理器，并以最小配置成本创建可复现的多语言环境。

## 适用场景

- 需要创建或更新 `mise.toml` 时
- 使用 Node.js、Python、Go、Rust、Java、Bun、Terraform 或混合技术栈时
- 涉及用 mise 配置 CI/CD 运行时时
- 从 `.tool-versions`、`asdf`、`nvm` 或 `pyenv` 迁移时
- 需要在团队或 monorepo 中统一工具版本时

## 工作流程

### 步骤 1：检测项目上下文

检查仓库中已有的配置文件：

- `package.json`
- `pnpm-lock.yaml`
- `pyproject.toml`
- `requirements.txt`
- `go.mod`
- `Cargo.toml`
- `.tool-versions`
- `Dockerfile`
- GitHub Actions 或其他 CI 配置文件

据此推断语言、包管理器和已锁定的版本。

### 步骤 2：生成 `mise.toml`

生成最小化、合法、可直接复制使用的配置，遵循以下原则：

- 优先使用仓库中已有的锁定版本
- 未找到时采用用户明确指定的目标版本
- 提供实用的开发者默认值
- 共享生产配置中使用具体的锁定版本号

### 步骤 3：添加引导命令

提供初始化命令：

```bash
mise trust
mise install
```

### 步骤 4：生成 CI/CD 集成

按需生成带缓存和运行时安装的流水线示例。

## 示例

### 示例 1：Node.js + pnpm 项目

```toml
[tools]
node = "22.11.0"
pnpm = "9.15.0"
```

### 示例 2：Python + GitHub Actions

```toml
[tools]
python = "3.12.7"
poetry = "1.8.4"
```

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: jdx/mise-action@v2
  - run: poetry install
  - run: pytest
```

## 最佳实践

- ✅ 尊重仓库中已有的锁定版本

- ✅ 保持配置最小化且可读

- ✅ 优先选择稳定版运行时

- ✅ 生成的 CI 示例应包含缓存

- ✅ 仓库未声明版本时，先询问目标版本再锁定

- ❌ 共享生产配置中不使用浮动的 `latest` 或 `lts` 别名（除非明确要求）

- ❌ 不添加不必要的工具条目

- ❌ 不忽略已有的 lockfile 或版本文件


## 局限性

- 本技能不能替代针对具体环境的验证、测试或专家评审。

- 缺少必要输入、权限或安全边界时，停下来询问确认。

- 运行时可用性可能因操作系统、Shell 或 CI 平台而异。

- 部分插件或小众工具可能需要手动调整。


## 安全注意事项

- 执行前先审查生成的 Shell 命令。

- 修改流水线前确认 CI/CD 权限。

- 根据生产需求验证运行时版本。

- 仅在授权的仓库和环境中使用。


## 常见问题

- **问题：** 选择了错误的运行时版本
    **解决：** 先检查仓库的 lockfile 和锁定版本。

- **问题：** CI 安装速度慢
    **解决：** 启用缓存层，复用 mise 缓存目录。

- **问题：** 工具不在注册表中
    **解决：** 确认插件支持情况，或手动安装。


## 相关技能

- `@docker-expert` - 构建容器化开发环境时使用

- `@github-actions-templates` - 高级工作流自动化时使用

- `@monorepo-architect` - 大型多包仓库时使用
