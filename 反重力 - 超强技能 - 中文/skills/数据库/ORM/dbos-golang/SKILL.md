---
name: dbos-golang
description: "使用 DBOS 持久化工作流构建可靠、容错的 Go 应用程序指南。触发词：DBOS Go、持久化工作流、工作流步骤、队列并发控制、Go 容错应用。当在现有 Go 代码中添加 DBOS、创建工作流和步骤、使用队列进行并发控制时使用。"
risk: safe
source: "https://docs.dbos.dev/"
date_added: "2026-02-27"
---

# DBOS Go 最佳实践

使用 DBOS 持久化工作流构建可靠、容错的 Go 应用程序指南。

## 何时使用

在以下情况下参考这些指南：
- 在现有 Go 代码中添加 DBOS
- 创建工作流和步骤
- 使用队列进行并发控制
- 实现工作流通信（事件、消息、流）
- 配置和启动 DBOS 应用程序
- 从外部应用程序使用 DBOS Client
- 测试 DBOS 应用程序

## 按优先级分类的规则类别

| 优先级 | 类别 | 影响 | 前缀 |
|----------|----------|--------|--------|
| 1 | Lifecycle | 关键 | `lifecycle-` |
| 2 | Workflow | 关键 | `workflow-` |
| 3 | Step | 高 | `step-` |
| 4 | Queue | 高 | `queue-` |
| 5 | Communication | 中 | `comm-` |
| 6 | Pattern | 中 | `pattern-` |
| 7 | Testing | 低-中 | `test-` |
| 8 | Client | 中 | `client-` |
| 9 | Advanced | 低 | `advanced-` |

## 关键规则

### 安装

安装 DBOS Go 模块：

```bash
go get github.com/dbos-inc/dbos-transact-golang/dbos@latest
```

### DBOS 配置和启动

DBOS 应用程序必须创建上下文、注册工作流，并在运行任何工作流之前启动：

```go
package main

import (
	"context"
	"log"
	"os"
	"time"

	"github.com/dbos-inc/dbos-transact-golang/dbos"
)

func main() {
	ctx, err := dbos.NewDBOSContext(context.Background(), dbos.Config{
		AppName:     "my-app",
		DatabaseURL: os.Getenv("DBOS_SYSTEM_DATABASE_URL"),
	})
	if err != nil {
		log.Fatal(err)
	}
	defer dbos.Shutdown(ctx, 30*time.Second)

	dbos.RegisterWorkflow(ctx, myWorkflow)

	if err := dbos.Launch(ctx); err != nil {
		log.Fatal(err)
	}
}
```

### 工作流和步骤结构

工作流由步骤组成。任何执行复杂操作或访问外部服务的函数都必须使用 `dbos.RunAsStep` 作为步骤运行：

```go
func fetchData(ctx context.Context) (string, error) {
	resp, err := http.Get("https://api.example.com/data")
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return string(body), nil
}

func myWorkflow(ctx dbos.DBOSContext, input string) (string, error) {
	result, err := dbos.RunAsStep(ctx, fetchData, dbos.WithStepName("fetchData"))
	if err != nil {
		return "", err
	}
	return result, nil
}
```

### 关键约束

- 不要在步骤内启动或入队工作流
- 不要使用不受控制的 goroutine 启动工作流 - 使用带队列的 `dbos.RunWorkflow` 或 `dbos.Go`/`dbos.Select` 进行并发步骤
- 工作流必须是确定性的 - 非确定性操作放在步骤中
- 不要从工作流或步骤修改全局变量
- 所有工作流和队列必须在调用 `Launch()` 之前注册

## 如何使用

阅读单独的规则文件以获取详细说明和示例：

```
references/lifecycle-config.md
references/workflow-determinism.md
references/queue-concurrency.md
```

## 参考资料

- https://docs.dbos.dev/
- https://github.com/dbos-inc/dbos-transact-golang

## 限制
- 仅当任务明显符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
