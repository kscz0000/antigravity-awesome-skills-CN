---
name: aws-agentic-ai
description: AWS Bedrock AgentCore 综合专家，专注于规模化部署与管理 AI 代理。在处理任意 AgentCore 服务（包括 Gateway、Runtime、Memory、Identity、Code Interpreter、Browser、Observability、Agent Registry 或 Evaluations）时使用本技能。覆盖代理部署、MCP 工具接入、凭证与身份管理、会话记忆、可观测性、Agent Registry 注册与发现、自动化评估等全链路场景。触发词：AWS Bedrock AgentCore、AgentCore、代理部署、Gateway、Runtime、Memory、Identity、Code Interpreter、Browser、Observability、Agent Registry、Evaluations、MCP。
risk: unknown
source: https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai
source_repo: zxkane/aws-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/zxkane/aws-skills/blob/main/LICENSE
---

# AWS Bedrock AgentCore

## 何时使用

当你需要借助 AWS Bedrock AgentCore 这一综合专家能力来规模化部署与管理 AI 代理时，请使用本技能。在处理任意 AgentCore 服务（包括 Gateway、Runtime、Memory、Identity、Code Interpreter、Browser、Observability、Agent Registry 或 Evaluations）时使用。覆盖代理部署、MCP 工具接入、跨服务集成等场景。

AWS Bedrock AgentCore 提供了一套完整的平台，借助九大核心服务完成 AI 代理的部署与横向扩展。本技能涵盖服务选型、部署模式以及基于 AWS CLI 的集成工作流。

**本技能的使用方法**：先在下表中识别用户需要的服务，然后阅读对应服务的 README 后再给出答复。对于跨服务模式（凭证、安全、注册表集成等），请查阅"跨服务资源"一节。回答前务必通过 MCP 文档工具核实 AWS 相关细节。

## AWS 文档要求

回答前务必通过 MCP 工具核实 AWS 相关事实。本技能依赖两种文档来源：

- **AgentCore 专属文档**（`mcp__acdocs__*`）—— 与本插件捆绑提供，提供 `search_agentcore_docs` 与 `fetch_agentcore_doc` 两个工具，用于检索 AgentCore 文档。
- **通用 AWS 文档**（`mcp__aws-mcp__*` 或 `mcp__*awsdocs*__*`）—— 通过 `aws-mcp-setup` 依赖加载，覆盖更广泛的 AWS 官方文档。

针对 AgentCore 专属问题，优先使用 AgentCore 文档 MCP。若 MCP 工具不可用，引导用户完成 `aws-mcp-setup` 技能的安装流程。

## 可用服务

| 服务 | 用途 | 文档 |
|---------|---------|-------------|
| **Gateway** | 将 REST API 转换为 MCP 工具 | [`services/gateway/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/gateway/README.md) |
| **Runtime** | 部署与横向扩展代理 | [`services/runtime/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/runtime/README.md) |
| **Memory** | 管理会话状态 | [`services/memory/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/memory/README.md) |
| **Identity** | 凭证与访问管理 | [`services/identity/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/identity/README.md) |
| **Code Interpreter** | 在沙箱中安全执行代码 | [`services/code-interpreter/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/code-interpreter/README.md) |
| **Browser** | Web 自动化与网页抓取 | [`services/browser/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/browser/README.md) |
| **Observability** | 链路追踪与监控 | [`services/observability/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/observability/README.md) |
| **Agent Registry** | 代理与工具的目录化、发现与治理（预览版） | [`services/registry/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/registry/README.md) |
| **Evaluations** | 自动化代理质量评估（LLM-as-a-Judge） | [`services/evaluations/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/evaluations/README.md) |

## 常见工作流

### 部署 Gateway 目标

实现前请先阅读 [`services/gateway/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/gateway/README.md) —— Gateway 的设置涉及部署策略、IAM 与认证选项，不同用例之间的差异较大。

1. 将 OpenAPI schema 上传至 S3。
2. *（仅 API Key 认证场景）* 创建凭证提供者并存储 API Key。
3. 创建 Gateway 目标，关联 schema（若使用 API Key 还需关联凭证）。
4. 验证目标状态并测试连通性。

> 凭证提供者仅在 API Key 认证场景下需要。Lambda 目标使用 IAM 角色，MCP 服务器则使用 OAuth。

### 管理凭证

请先阅读 [`cross-service/credential-management.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/cross-service/credential-management.md) —— 凭证模式在不同服务之间存在差异，配置错误会引发难以排查的认证故障。

1. 所有 API Key 均使用 Identity 服务的凭证提供者。
2. 通过 ARN 引用将凭证提供者链接到 Gateway 目标。
3. 每季度通过凭证提供者更新来轮换凭证。
4. 使用 CloudWatch 指标监控用量与异常。

### 发现代理与工具（Agent Registry）

请先阅读 [`services/registry/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/registry/README.md) —— 注册表包含治理工作流、MCP 端点选项与同步模式，决定了记录如何进入可发现状态。

1. 创建一个注册表，用于归类组织内部的 AI 资源。
2. 注册资源（MCP 服务器、代理、技能、自定义类型），并填写描述性元数据。
3. 提交记录以供审批（开发环境自动通过，生产环境需人工审批）。
4. 通过 CLI 或 MCP 端点检索并发现已批准的可用资源。

> Agent Registry 处于预览阶段。可用区域：us-east-1、us-west-2、eu-west-1、ap-northeast-1、ap-southeast-2。

### 评估代理质量

请先阅读 [`services/evaluations/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/evaluations/README.md) —— 在线监控与按需测试两类场景下的评估器、评分模式与 IAM 配置有所不同。

1. 使用 OpenTelemetry（ADOT）为代理埋点，采集调用链路数据。
2. 创建评估器（可使用内置评估器如 `Builtin.Helpfulness`，也可创建自定义评估器）。
3. 配置在线评估，设置采样率与数据源。
4. 在 CloudWatch 仪表板中监控评分；针对低分会话进行调查。

### 监控代理

请阅读 [`services/observability/README.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/services/observability/README.md) 以获取完整的监控设置 —— 可观测性配置取决于 Runtime 协议与框架选型。

1. 为代理启用可观测性。
2. 配置 CloudWatch 仪表板以展示关键指标。
3. 为错误率与延迟配置告警。
4. 使用 X-Ray 进行分布式链路追踪。

## 深度参考资料

每个服务的 README（上表已列出链接）都包含入门指南、故障排查与进阶主题的子链接。建议先阅读对应服务的 README，再按其中的指引继续深入。

### 进阶 Runtime 与 OAuth 参考

针对 Runtime 内部机制、部署流程、OAuth 集成与通信协议的深度参考文档。在构建生产级 Runtime 部署或配置 OAuth 认证时阅读：

- **OAuth 集成**：[`references/agentcore-oauth-integration.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/references/agentcore-oauth-integration.md) - 三层 OAuth 架构（入站 JWT、出站凭证提供者、Gateway OAuth）、Cognito 配置、支持的 IdP、端到端 CDK 示例
- **Runtime 核心机制**：[`references/agentcore-runtime-core.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/references/agentcore-runtime-core.md) - 容器契约、MicroVM 会话模型、代理生命周期（按请求 vs 按会话）、工具集成（MCP/HTTP）、启动流程
- **Runtime 部署与运维**：[`references/agentcore-runtime-deploy.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/references/agentcore-runtime-deploy.md) - CDK 部署（L1/L2 构造）、多 Runtime 架构、安全模型、可观测性（OTel/CloudWatch）、BedrockAgentCoreApp 与 FastAPI 对比
- **Runtime 协议参考**：[`references/agentcore-runtime-protocols.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/references/agentcore-runtime-protocols.md) - HTTP、MCP、A2A、AG-UI 协议规范，附容器契约、端点规范与选型指南

### 可运行脚本模板

位于 [`scripts/`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/scripts/) 的生产就绪模板，覆盖常见部署模式：

| 脚本 | 协议 | 描述 |
|--------|----------|-------------|
| [`Dockerfile.runtime-template`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/scripts/Dockerfile.runtime-template) | — | 适用于 AgentCore Runtime 的 ARM64 多阶段 Docker 构建 |
| [`runtime-fastapi-template.py`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/scripts/runtime-fastapi-template.py) | HTTP | 基于 FastAPI 的 Runtime，支持 SSE 流式响应与 MCPClient |
| [`mcp-server-template.py`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/scripts/mcp-server-template.py) | MCP | 基于 Streamable HTTP 传输的 MCP 服务器 |
| [`a2a-server-template.py`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/scripts/a2a-server-template.py) | A2A | 支持 Agent Card 发现机制的 A2A 服务器 |
| [`agui-server-template.py`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/scripts/agui-server-template.py) | AG-UI | 提供标准 AG-UI 事件流的 AG-UI 服务器 |
| [`gateway-custom-resource-lambda.py`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/scripts/gateway-custom-resource-lambda.py) | — | 用于 Gateway 生命周期的 CDK Custom Resource Lambda |

## 跨服务资源

针对跨多个 AgentCore 服务的模式与最佳实践：

- **凭证管理**：[`cross-service/credential-management.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/cross-service/credential-management.md) - 统一的凭证模式、安全实践、轮换流程
- **注册表集成**：[`cross-service/registry-integration.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/cross-service/registry-integration.md) - 与 Gateway、Identity、Runtime 的跨服务模式
- **安全与资源策略**：[`cross-service/security-resource-policies.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/cross-service/security-resource-policies.md) - 基于资源的策略、跨账户访问、VPC/IP 限制
- **基于 S3 文件的代理部署**：[`cross-service/agent-persistence-patterns.md`](https://github.com/zxkane/aws-skills/tree/main/plugins/aws-agentic-ai/skills/aws-agentic-ai/cross-service/agent-persistence-patterns.md) - 在 AgentCore 上部署 Strands Agents、OpenClaw、Claude Agent SDK，配合 S3 文件与会话存储

## 其他资源

- **AWS 文档**：[Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- **API 参考**：[Bedrock AgentCore Control Plane API](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/)
- **AWS CLI 参考**：[bedrock-agentcore-control commands](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/bedrock-agentcore-control/index.html)

## 局限性

- 仅在任务明确匹配上游来源与本地项目上下文时使用本技能。
- 在应用变更前，请核实命令、生成的代码、依赖、凭证以及外部服务行为。
- 请勿将示例视为环境专属测试、安全审查或用户对破坏性/高成本操作授权的替代品。