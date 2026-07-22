---
name: kubestellar-console
description: "多集群 Kubernetes 仪表盘，通过 MCP server 提供 AI 驱动运维能力，内置 10+ agent 技能。当用户要求管理多集群 Kubernetes、使用 KubeStellar Console、AI 辅助 Kubernetes 运维、多集群仪表盘操作时使用。"
category: devops
risk: critical
source: community
source_repo: kubestellar/console
source_type: community
date_added: "2026-04-27"
author: kubestellar
tags: [kubernetes, multi-cluster, mcp, dashboard, cncf, devops, observability]
tools: [claude, cursor, gemini, codex]
license: "Apache-2.0"
license_source: "https://github.com/kubestellar/console/blob/main/LICENSE"
plugin:
  setup:
    type: manual
    summary: "需要 kc-agent 二进制文件（brew tap kubestellar/tap && brew install kc-agent）"
    docs: "https://github.com/kubestellar/console#quick-start"
---

# KubeStellar Console

## 概览

KubeStellar Console 是一个开源的多集群 Kubernetes 仪表盘（CNCF 项目），支持 AI 驱动运维。它内置 `kc-agent`——一个将编码智能体与 kubeconfig 及 Kubernetes API 连接的 MCP server，以及 10+ 内置 agent 技能，覆盖开发、测试和运维场景。

## 适用场景

- 管理跨边缘和云端的多个 Kubernetes 集群时使用
- 需要 AI 辅助的 Kubernetes 排障和调试时使用
- 在 Kubernetes 仪表盘上执行性能测试、缓存合规检查或 CI 调试时使用
- 与 CNCF 项目（Argo、Kyverno、Istio 等 20+ 项目）集成时使用

## 工作原理

### 第一步：安装 kc-agent

```bash
brew tap kubestellar/tap && brew install kc-agent
```

### 第二步：启动 MCP server

```bash
kc-agent
```

这会将你的 kubeconfig 桥接到任何兼容 MCP 的编码智能体。

### 第三步：使用内置 agent 技能

项目内置的 agent 技能可通过 `CLAUDE.md` 和 `AGENTS.md` 访问：

- **@perf-test** — 仪表盘性能测试和 TTFI 分析
- **@cache-test** — 卡片缓存合规测试（IndexedDB 热返回）
- **@nav-test** — 导航性能测试
- **@ui-compliance-test** — 卡片加载合规检查（8 项标准，150+ 卡片）
- **@ci-status** — CI 流水线监控和状态检查
- **@rca** — CI/测试失败的根因分析
- **@tdd** — 测试驱动开发工作流
- **@k8s-debug** — Kubernetes 调试与排障

## 核心特性

- 跨边缘和云端的多集群管理
- 实时流式可观测性
- 20+ CNCF 项目集成（Argo、Kyverno、Istio 等）
- GitHub OAuth 认证
- 供应链安全（SBOM、SLSA）
- SQLite WASM 缓存，采用 stale-while-revalidate 策略
- 15+ 主题，支持深色/浅色模式

## 安全说明

- **严重风险：**`kc-agent` 将你的 kubeconfig 桥接到兼容 MCP 的智能体。如果你的 kubeconfig 携带 cluster-admin 或写入权限，智能体将继承这些能力。务必使用最小权限 RBAC 上下文。
- **建议：** 在与智能体配合使用前，先将 `kc-agent` 绑定到最小权限只读 RBAC：
  ```bash
  kubectl create clusterrole kc-agent-readonly --verb=get,list,watch --resource='*'
  kubectl create clusterrolebinding kc-agent-readonly --clusterrole=kc-agent-readonly --serviceaccount=default:kc-agent
  ```
- 不要在未配置认证的情况下将 `kc-agent` 暴露在公网。
- 查看 [SECURITY-AI.md](https://github.com/kubestellar/console/blob/main/docs/security/SECURITY-AI.md) 了解提示词注入和智能体漂移的缓解措施。

## 局限性

- 本技能需要单独通过 Homebrew 安装外部二进制文件（`kc-agent`）。
- 不要把智能体输出当作环境特定验证或专家评审的替代品。
- 如果所需权限或安全边界不明确，应停下来先确认。

## 相关链接

- [GitHub](https://github.com/kubestellar/console)
- [官网](https://console.kubestellar.io)
- [CLAUDE.md](https://github.com/kubestellar/console/blob/main/CLAUDE.md)
- [AGENTS.md](https://github.com/kubestellar/console/blob/main/AGENTS.md)
