# gRPC Golang 实现手册

本文件包含技能引用的详细模式、检查清单和代码示例。

## Schema 设计标准

### Protobuf 定义

- **语法**：仅使用 proto3。
- **版本控制**：使用包版本控制（如 `api.v1`）。
- **分页**：列表操作使用 `page_token` 和 `page_size`。
- **时区**：服务器级别始终使用 UTC 值的 `google.protobuf.Timestamp`。
- **幂等性**：使用幂等键或设计无副作用方法以支持安全重试。
- **验证**：采用 schema 级验证方法（如 Buf 验证规则或 `protoc-gen-validate`），确保生成的代码在服务器端强制执行。

```proto
syntax = "proto3";
package api.v1;
option go_package = "github.com/org/repo/gen/api/v1;apiv1";

import "google/protobuf/timestamp.proto";

service UserService {
  rpc GetUser(GetUserRequest) returns (GetUserResponse);
  rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
  rpc WatchUsers(WatchUsersRequest) returns (stream UserEvent);
}

message User {
  string id = 1;
  string name = 2;
  string email = 3;
  google.protobuf.Timestamp created_at = 4;
}

message GetUserRequest {
  string id = 1;
}

message GetUserResponse {
  User user = 1;
}

message ListUsersRequest {
  int32 page_size = 1;
  string page_token = 2;
}

message ListUsersResponse {
  repeated User users = 1;
  string next_page_token = 2;
}

message WatchUsersRequest {
  // 空；从当前点流式传输所有用户事件。
}

message UserEvent {
  enum EventType {
    EVENT_TYPE_UNSPECIFIED = 0;
    EVENT_TYPE_CREATED = 1;
    EVENT_TYPE_UPDATED = 2;
    EVENT_TYPE_DELETED = 3;
  }
  EventType type = 1;
  User user = 2;
  google.protobuf.Timestamp occurred_at = 3;
}
```

## 代码生成

- **工具链**：使用 `google.golang.org/protobuf/cmd/protoc-gen-go` 和 `protoc-gen-go-grpc`。
- **管理**：使用 `buf.gen.yaml` 管理插件版本和生成参数。
- **兼容性**：确保插件使用 Protobuf Go v2 API（`google.golang.org/protobuf`）。不要与已弃用的 v1 API（`github.com/golang/protobuf`）混用。

### buf.gen.yaml 示例

```yaml
version: v2
plugins:
  - remote: buf.build/protocolbuffers/go
    out: gen
    opt: paths=source_relative
  - remote: buf.build/grpc/go
    out: gen
    opt: paths=source_relative
```

## 服务器实现

### 完整服务器设置（含优雅关闭）

```go
package main

import (
	"context"
	"log"
	"net"
	"os"
	"os/signal"
	"syscall"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/health"
	healthpb "google.golang.org/grpc/health/grpc_health_v1"
	"google.golang.org/grpc/keepalive"

	apiv1 "github.com/org/repo/gen/api/v1"
)

func main() {
	srv := grpc.NewServer(
		grpc.ChainUnaryInterceptor(
			recoveryInterceptor,
			loggingInterceptor,
			otelUnaryInterceptor,
		),
		grpc.KeepaliveParams(keepalive.ServerParameters{
			MaxConnectionIdle: 5 * time.Minute,
			Time:              1 * time.Minute,
			Timeout:           20 * time.Second,
		}),
		grpc.MaxRecvMsgSize(4<<20), // 4 MB
		grpc.MaxSendMsgSize(4<<20), // 4 MB
	)

	// 注册应用服务。
	apiv1.RegisterUserServiceServer(srv, newUserService())

	// 使用完全限定服务名注册健康检查。
	healthSrv := health.NewServer()
	healthpb.RegisterHealthServer(srv, healthSrv)
	healthSrv.SetServingStatus(
		"api.v1.UserService",
		healthpb.HealthCheckResponse_SERVING,
	)

	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("listen: %v", err)
	}

	// 优雅关闭：GracefulStop 带回退超时到 Stop。
	go func() {
		sigCh := make(chan os.Signal, 1)
		signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
		<-sigCh

		log.Println("shutting down gRPC server...")
		healthSrv.SetServingStatus(
			"api.v1.UserService",
			healthpb.HealthCheckResponse_NOT_SERVING,
		)

		ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
		defer cancel()

		stopped := make(chan struct{})
		go func() {
			srv.GracefulStop()
			close(stopped)
		}()

		select {
		case <-stopped:
			log.Println("server stopped gracefully")
		case <-ctx.Done():
			log.Println("graceful stop timed out, forcing stop")
			srv.Stop()
		}
	}()

	log.Printf("gRPC server listening on %s", lis.Addr())
	if err := srv.Serve(lis); err != nil {
		log.Fatalf("serve: %v", err)
	}
}
```

## mTLS 设置

```go
package main

import (
	"crypto/tls"
	"crypto/x509"
	"fmt"
	"log"
	"os"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
)

// loadServerTLS 为服务器端配置 mTLS。
func loadServerTLS() grpc.ServerOption {
	tlsCert, err := tls.LoadX509KeyPair("server.crt", "server.key")
	if err != nil {
		log.Fatalf("load server cert: %v", err)
	}

	caCert, err := os.ReadFile("ca.crt")
	if err != nil {
		log.Fatalf("read CA cert: %v", err)
	}

	caPool := x509.NewCertPool()
	if !caPool.AppendCertsFromPEM(caCert) {
		log.Fatal("failed to append CA cert")
	}

	tlsCfg := &tls.Config{
		Certificates: []tls.Certificate{tlsCert},
		ClientCAs:    caPool,
		ClientAuth:   tls.RequireAndVerifyClientCert,
		MinVersion:   tls.VersionTLS13,
	}
	return grpc.Creds(credentials.NewTLS(tlsCfg))
}

// dialWithMTLS 使用 mTLS 创建客户端连接。
func dialWithMTLS(target string) (*grpc.ClientConn, error) {
	clientCert, err := tls.LoadX509KeyPair("client.crt", "client.key")
	if err != nil {
		return nil, fmt.Errorf("load client cert: %w", err)
	}

	caCert, err := os.ReadFile("ca.crt")
	if err != nil {
		return nil, fmt.Errorf("read CA cert: %w", err)
	}

	caPool := x509.NewCertPool()
	if !caPool.AppendCertsFromPEM(caCert) {
		return nil, fmt.Errorf("failed to append CA cert")
	}

	creds := credentials.NewTLS(&tls.Config{
		Certificates: []tls.Certificate{clientCert},
		RootCAs:      caPool,
		MinVersion:   tls.VersionTLS13,
	})

	// 注意：对于 gRPC-Go v1.63+，推荐使用 grpc.NewClient 替代。
	conn, err := grpc.Dial(target, grpc.WithTransportCredentials(creds))
	if err != nil {
		return nil, fmt.Errorf("dial %s: %w", target, err)
	}
	return conn, nil
}
```

## 客户端最佳实践

### 连接复用

```go
package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"

	apiv1 "github.com/org/repo/gen/api/v1"
)

// 启动时初始化一次；在应用生命周期内复用。
var userConn *grpc.ClientConn

func initClients(creds credentials.TransportCredentials) {
	var err error
	// 注意：对于 gRPC-Go v1.63+，使用 grpc.NewClient 替代。
	userConn, err = grpc.Dial(
		os.Getenv("USER_SVC_ADDR"),
		grpc.WithTransportCredentials(creds),
	)
	if err != nil {
		log.Fatalf("dial user-svc: %v", err)
	}
}

func callListUsers(ctx context.Context) (*apiv1.ListUsersResponse, error) {
	// 始终为每次调用设置截止时间，而非为连接设置。
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	client := apiv1.NewUserServiceClient(userConn)
	resp, err := client.ListUsers(ctx, &apiv1.ListUsersRequest{PageSize: 20})
	if err != nil {
		return nil, fmt.Errorf("list users: %w", err)
	}
	return resp, nil
}
```

### 重试策略

仅对幂等调用启用重试。使用指数退避。

```go
import "google.golang.org/grpc"

// 幂等方法的服务配置重试策略。
const retryPolicy = `{
  "methodConfig": [{
    "name": [{"service": "api.v1.UserService", "method": "GetUser"}],
    "retryPolicy": {
      "maxAttempts": 3,
      "initialBackoff": "0.1s",
      "maxBackoff": "1s",
      "backoffMultiplier": 2,
      "retryableStatusCodes": ["UNAVAILABLE", "DEADLINE_EXCEEDED"]
    }
  }]
}`

// 注意：对于 gRPC-Go v1.63+，使用 grpc.NewClient 替代 grpc.Dial。
conn, err := grpc.Dial(
	target,
	grpc.WithTransportCredentials(creds),
	grpc.WithDefaultServiceConfig(retryPolicy),
)
```

## 可观测性

### 拦截器标签

- **日志**：包含 `grpc.method`、`grpc.service`、`grpc.code`、`latency_ms` 和 `trace_id`。
- **指标**：导出请求计数、延迟直方图和进行中的流计数。

### OpenTelemetry 集成

```go
import (
	"go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc"
	"google.golang.org/grpc"
)

srv := grpc.NewServer(
	grpc.StatsHandler(otelgrpc.NewServerHandler()),
)

// 注意：对于 gRPC-Go v1.63+，使用 grpc.NewClient 替代 grpc.Dial。
conn, err := grpc.Dial(
	target,
	grpc.WithStatsHandler(otelgrpc.NewClientHandler()),
)
```

## 测试

### bufconn 进程内测试

```go
package service_test

import (
	"context"
	"net"
	"testing"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	"google.golang.org/grpc/status"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/test/bufconn"

	apiv1 "github.com/org/repo/gen/api/v1"
)

func TestListUsers(t *testing.T) {
	lis := bufconn.Listen(1 << 20)
	srv := grpc.NewServer()
	apiv1.RegisterUserServiceServer(srv, &fakeUserSvc{})
	go func() {
		if err := srv.Serve(lis); err != nil {
			t.Logf("server exited: %v", err)
		}
	}()
	t.Cleanup(srv.GracefulStop)

	// 注意：对于 gRPC-Go v1.63+，使用 grpc.NewClient 替代 grpc.DialContext。
	conn, err := grpc.DialContext(context.Background(),
		"bufnet",
		grpc.WithContextDialer(func(ctx context.Context, _ string) (net.Conn, error) {
			return lis.DialContext(ctx)
		}),
		grpc.WithTransportCredentials(insecure.NewCredentials()),
	)
	if err != nil {
		t.Fatalf("dial bufnet: %v", err)
	}
	t.Cleanup(func() { conn.Close() })

	client := apiv1.NewUserServiceClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	resp, err := client.ListUsers(ctx, &apiv1.ListUsersRequest{PageSize: 10})
	if code := status.Code(err); code != codes.OK {
		t.Fatalf("expected OK, got %v: %v", code, err)
	}
	if resp == nil {
		t.Fatal("expected non-nil response")
	}
}
```

## 流式处理器模式

始终在流式循环中检查 `ctx.Done()`。切勿向客户端暴露原始内部错误。

```go
func (s *userService) WatchUsers(
	req *apiv1.WatchUsersRequest,
	stream apiv1.UserService_WatchUsersServer,
) error {
	ctx := stream.Context()

	events := s.subscribeUserEvents()
	defer s.unsubscribe(events)

	for {
		select {
		case <-ctx.Done():
			// 客户端断开或截止时间超限；干净退出。
			return status.Error(codes.Canceled, "client disconnected")

		case event, ok := <-events:
			if !ok {
				// 通道关闭；服务器正在关闭。
				return status.Error(codes.Unavailable, "service shutting down")
			}

			if err := stream.Send(event); err != nil {
				// 在服务器端记录原始错误用于诊断。
				log.Printf("stream send failed: %v", err)
				// 向客户端返回通用消息；绝不泄露原始错误。
				return status.Error(codes.Internal, "failed to send event")
			}
		}
	}
}
```

## 错误映射

一致地将领域错误映射到 gRPC 状态码：

仅当 `err.Error()` 是安全的、面向用户的领域消息（而非内部错误字符串）时，才将其返回给客户端。

```go
package service

import (
	"errors"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

var (
	ErrNotFound       = errors.New("resource not found")
	ErrAlreadyExists  = errors.New("resource already exists")
	ErrInvalidInput   = errors.New("invalid input")
	ErrPermission     = errors.New("permission denied")
)

// toGRPCError 将领域错误映射到 gRPC 状态错误。
func toGRPCError(err error) error {
	if err == nil {
		return nil
	}
	switch {
	case errors.Is(err, ErrNotFound):
		return status.Error(codes.NotFound, err.Error())
	case errors.Is(err, ErrAlreadyExists):
		return status.Error(codes.AlreadyExists, err.Error())
	case errors.Is(err, ErrInvalidInput):
		return status.Error(codes.InvalidArgument, err.Error())
	case errors.Is(err, ErrPermission):
		return status.Error(codes.PermissionDenied, err.Error())
	default:
		return status.Error(codes.Internal, "internal error")
	}
}
```

## 项目布局

```
project/
  buf.gen.yaml
  buf.yaml
  proto/
    api/
      v1/
        user_service.proto
  gen/                          # 生成的代码（提交或 gitignore）
    api/
      v1/
        user_service.pb.go
        user_service_grpc.pb.go
  internal/
    service/
      user.go                  # 服务实现
      user_test.go             # bufconn 测试
    domain/
      errors.go                # 领域错误定义
  cmd/
    server/
      main.go                  # 带优雅关闭的服务器入口
  config/
    config.go                  # 基于环境的配置（超时、TLS 路径、限制）
```

## 安全检查清单

- 所有生产流量默认使用 TLS/mTLS。
- 强制执行限制（`MaxRecvMsgSize`、`MaxSendMsgSize`、元数据大小）以减少资源耗尽风险。
- 将客户端发送的元数据视为不可信；验证并白名单用于认证或租户路由的键。
- 在生产环境中禁用 gRPC 反射以避免暴露内部服务 schema。
- 在流式处理器的每次迭代中检查 `context.Done()` 以防止 goroutine 泄漏。

## 反模式

| 反模式 | 危害 | 修复方法 |
| ------ | ---- | -------- |
| 每个请求创建新的 `grpc.ClientConn` | 耗尽 OS 套接字并禁用 HTTP/2 多路复用，导致高延迟和资源泄漏 | 初始化一次，全局复用 |
| 混用 Protobuf v1 和 v2 库 | 导致静默序列化 bug；v1 和 v2 的 `proto.Marshal` 不可互换 | 全项目统一使用 `google.golang.org/protobuf`（v2） |
| 向客户端暴露原始内部错误字符串 | 泄露堆栈跟踪和内部服务名称；安全和用户体验风险 | 使用适当的 gRPC 状态码通过 `status.Errorf` 映射错误 |
| 在流式处理器中忽略 `context.Done()` | 客户端断开时导致 goroutine 和连接泄漏 | 在流式循环的每次迭代中检查 `ctx.Err()` |
| 使用 `_ =` 跳过错误处理 | 静默隐藏失败；生产故障无法诊断 | 始终显式检查和处理错误 |
| 使用不带健康检查的 `grpc.Dial` | 连接失败被延迟，可能在运行时才暴露为错误 | 使用健康检查并监控连接状态 |

> **迁移说明**：对于 gRPC-Go v1.63+（2024 年 1 月），`grpc.NewClient` 是 gRPC-Go 项目推荐用于新代码的更新 API。对于旧版本（或遵循现有代码库和官方 grpc.io 示例时），使用 `grpc.Dial` / `grpc.DialContext` 仍然常见。
