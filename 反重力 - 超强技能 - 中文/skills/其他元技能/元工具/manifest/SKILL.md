---
name: manifest
description: "为你的智能体安装和配置 Manifest 可观测性插件。当设置遥测、配置 API 密钥或排查插件问题时使用。触发词：Manifest 插件、可观测性插件、遥测配置、Manifest API 密钥、插件安装、Manifest 设置、observability plugin、telemetry setup"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Manifest 设置

按顺序执行以下步骤。不要跳过。

## 使用此技能的场景

- 用户想为智能体设置可观测性或遥测
- 用户想将智能体连接到 Manifest 进行监控
- 用户需要配置 Manifest API 密钥或自定义端点
- 用户正在排查 Manifest 插件连接问题
- 用户想验证 Manifest 插件是否正在运行

## 不使用此技能的场景

- 用户需要通用可观测性设计（改用 `observability-engineer`）
- 用户想构建自定义仪表盘或告警规则
- 用户未使用 Manifest 平台

## 操作说明

### 步骤 1 — 停止网关

首先停止网关以避免配置期间的热重载问题。

```bash
claude gateway stop
```

### 步骤 2 — 安装插件

```bash
claude plugins install manifest
```

如果失败，请检查 CLI 是否已安装并在 PATH 中可用。

### 步骤 3 — 获取 API 密钥

询问用户：

> 要连接你的智能体，需要一个 Manifest API 密钥。获取方法如下：
>
> 1. 访问 **https://app.manifest.build** 并创建账户（或登录）
> 2. 登录后，点击 **"Connect Agent"** 创建新智能体
> 3. 复制以 `mnfst_` 开头的 API 密钥
> 4. 将其粘贴到这里

等待以 `mnfst_` 开头的密钥。如果密钥格式不匹配，告诉用户格式看起来不正确并请其重试。

### 步骤 4 — 配置插件

```bash
claude config set plugins.entries.manifest.config.apiKey "USER_API_KEY"
```

将 `USER_API_KEY` 替换为用户提供的实际密钥。

询问用户是否有自定义端点。如果没有，将自动使用默认值（`https://app.manifest.build/api/v1/otlp`）。如果有：

```bash
claude config set plugins.entries.manifest.config.endpoint "USER_ENDPOINT"
```

### 步骤 5 — 启动网关

```bash
claude gateway install
```

### 步骤 6 — 验证

等待 3 秒让网关完全启动，然后检查日志：

```bash
grep "manifest" ~/.claude/logs/gateway.log | tail -5
```

查找：

```
[manifest] Observability pipeline active
```

如果出现此信息，告诉用户设置完成。如果没有，检查错误消息并进行排查。

## 安全注意事项

- 配置后切勿以明文记录或输出 API 密钥
- 写入配置前验证密钥格式（`mnfst_` 前缀）

## 故障排除

| 错误 | 解决方法 |
|-------|-----|
| Missing apiKey | 重新执行步骤 4 |
| Invalid apiKey format | 密钥必须以 `mnfst_` 开头 |
| Connection refused | 端点不可达。检查 URL 或询问是否自托管 |
| Duplicate OTel registration | 禁用冲突的内置插件：`claude plugins disable diagnostics-otel` |

## 示例

### 示例 1：基本设置

```
Use @manifest to set up observability for my agent.
```

### 示例 2：自定义端点

```
Use @manifest to connect my agent to my self-hosted Manifest instance at https://manifest.internal.company.com/api/v1/otlp
```

## 最佳实践

- 进行配置更改前始终停止网关
- 默认端点适用于大多数用户 — 仅在自托管时更改
- API 密钥始终以 `mnfst_` 开头 — 其他格式均无效
- 调试任何插件问题时首先检查网关日志

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
