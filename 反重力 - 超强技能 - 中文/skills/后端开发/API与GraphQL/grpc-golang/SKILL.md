---
name: grpc-golang
description: "使用 Go 构建生产级 gRPC 服务，支持 mTLS、流式传输和可观测性。触发词：gRPC Go、gRPC Golang、Protobuf Go、Buf、mTLS gRPC、流式 RPC、服务间通信、gRPC 服务开发、Go gRPC 最佳实践。"
risk: safe
source: self
date_added: "2026-02-27"
---

# gRPC Golang (gRPC-Go)

## 概述

在 Go 中设计和实现生产级 gRPC 服务的综合指南。涵盖使用 Buf 进行契约标准化、通过 mTLS 实现传输层安全，以及使用 OpenTelemetry 拦截器实现深度可观测性。

## 使用此技能的场景

- 在 Go 中设计微服务间 gRPC 通信。
- 使用 Protobuf 构建高性能内部 API。
- 实现流式工作负载（单向或双向）。
- 使用 Protobuf 和 Buf 标准化 API 契约。
- 为服务间认证配置 mTLS。

## 不适用场景

- 构建没有 gRPC 需求的纯 REST/HTTP 公共 API。
- 在无法引入新 API 版本（如 `api.v2`）或确保向后兼容性的情况下修改遗留 `.proto` 文件。
- 管理服务网格流量路由（如 Istio/Linkerd），这超出了应用代码范围。

## 分步指南

1. **确认技术上下文**：确定 Go 版本、gRPC-Go 版本，以及项目使用 Buf 还是原生 protoc。
2. **确认需求**：确定 mTLS 需求、负载模式（一元/流式）、SLO 和消息大小限制。
3. **规划 Schema**：定义包版本控制（如 `api.v1`）、资源类型和错误映射。
4. **安全设计**：为服务间认证实现 mTLS。
5. **可观测性**：配置拦截器用于追踪、指标和结构化日志。
6. **验证**：在最终确定代码生成之前，始终运行 `buf lint` 和破坏性变更检查。

详细模式、代码示例和反模式请参阅 `resources/implementation-playbook.md`。

## 示例

### 示例 1：定义服务和消息（v1 API）

```proto
syntax = "proto3";
package api.v1;
option go_package = "github.com/org/repo/gen/api/v1;apiv1";

service UserService {
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
}

message User {
  string id = 1;
  string name = 2;
}

message GetUserRequest {
  string id = 1;
}

message GetUserResponse {
  User user = 1;
}
```

## 最佳实践

- ✅ **应该**：使用 Buf 通过 `buf.yaml` 和 `buf.gen.yaml` 标准化工具链和 lint 检查。
- ✅ **应该**：始终在包路径中使用语义化版本控制（如 `package api.v1`）。
- ✅ **应该**：对所有内部服务间通信强制执行 mTLS。
- ✅ **应该**：在所有流式处理器中处理 `ctx.Done()` 以防止资源泄漏。
- ✅ **应该**：将领域错误映射到标准 gRPC 状态码（如 `codes.NotFound`）。
- ❌ **不应该**：向 gRPC 客户端返回原始内部错误字符串或堆栈跟踪。
- ❌ **不应该**：为每个请求创建新的 `grpc.ClientConn`；始终复用连接。

## 故障排除

- **错误：生成代码不一致**：如果生成的代码与 schema 不匹配，运行 `buf generate` 并验证 `go_package` 选项。
- **错误：上下文截止时间**：检查客户端超时设置，确保服务器没有在流式处理器中无限阻塞。
- **错误：mTLS 握手失败**：确保 CA 证书已正确添加到客户端和服务器端的 `x509.CertPool` 中。

## 局限性

- 不涵盖服务网格流量路由（Istio/Linkerd 配置）。
- 不涵盖 gRPC-Web 或基于浏览器的 gRPC 集成。
- 假设 Go 1.21+ 和 gRPC-Go v1.60+；旧版本可能有不同的 API（如 `grpc.Dial` vs `grpc.NewClient`）。
- 不涵盖 L7 gRPC 感知负载均衡器配置（如 Envoy、NGINX）。
- 不涉及 Protobuf schema 注册表或超出 Buf lint 范围的大规模 schema 治理。

## 资源

- `resources/implementation-playbook.md` 包含详细模式、代码示例和反模式。
- [Google API Design Guide](https://cloud.google.com/apis/design)
- [Buf Docs](https://buf.build/docs)
- [gRPC-Go Docs](https://grpc.io/docs/languages/go/)
- [OpenTelemetry Go Instrumentation](https://opentelemetry.io/docs/instrumentation/go/)

## 相关技能

- @golang-pro - gRPC 层之外的通用 Go 模式和性能优化。
- @go-concurrency-patterns - 流式处理器的高级 goroutine 生命周期管理。
- @api-design-principles - 编写 `.proto` 文件之前的资源命名和版本控制策略。
- @docker-expert - 容器化 gRPC 服务并通过 Docker secrets 配置 TLS 证书注入。
