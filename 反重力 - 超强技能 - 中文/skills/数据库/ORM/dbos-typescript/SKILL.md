---
name: dbos-typescript
description: "使用 DBOS 持久化工作流构建可靠、容错 TypeScript 应用的指南。适用于向现有 TypeScript 代码添加 DBOS、创建工作流和步骤，或使用队列进行并发控制。"
risk: safe
source: "https://docs.dbos.dev/"
date_added: "2026-02-27"
---

# DBOS TypeScript 最佳实践

使用 DBOS 持久化工作流构建可靠、容错 TypeScript 应用的指南。

## 使用场景

在以下情况下参考这些指南：
- 向现有 TypeScript 代码添加 DBOS
- 创建工作流和步骤
- 使用队列进行并发控制
- 实现工作流通信（事件、消息、流）
- 配置和启动 DBOS 应用
- 从外部应用使用 DBOSClient
- 测试 DBOS 应用

## 规则分类（按优先级）

| 优先级 | 分类 | 影响 | 前缀 |
|--------|------|------|------|
| 1 | Lifecycle | CRITICAL | `lifecycle-` |
| 2 | Workflow | CRITICAL | `workflow-` |
| 3 | Step | HIGH | `step-` |
| 4 | Queue | HIGH | `queue-` |
| 5 | Communication | MEDIUM | `comm-` |
| 6 | Pattern | MEDIUM | `pattern-` |
| 7 | Testing | LOW-MEDIUM | `test-` |
| 8 | Client | MEDIUM | `client-` |
| 9 | Advanced | LOW | `advanced-` |

## 关键规则

### 安装

始终安装最新版本的 DBOS：

```bash
npm install @dbos-inc/dbos-sdk@latest
```

### DBOS 配置与启动

DBOS 应用必须在运行任何工作流之前配置并启动 DBOS：

```typescript
import { DBOS } from "@dbos-inc/dbos-sdk";

async function main() {
  DBOS.setConfig({
    name: "my-app",
    systemDatabaseUrl: process.env.DBOS_SYSTEM_DATABASE_URL,
  });
  await DBOS.launch();
  await myWorkflow();
}

main().catch(console.log);
```

### 工作流与步骤结构

工作流由步骤组成。任何执行复杂操作或访问外部服务的函数必须使用 `DBOS.runStep` 作为步骤运行：

```typescript
import { DBOS } from "@dbos-inc/dbos-sdk";

async function fetchData() {
  return await fetch("https://api.example.com").then(r => r.json());
}

async function myWorkflowFn() {
  const result = await DBOS.runStep(fetchData, { name: "fetchData" });
  return result;
}
const myWorkflow = DBOS.registerWorkflow(myWorkflowFn);
```

### 关键约束

- 不要在步骤内调用、启动或排队工作流
- 不要使用线程或不受控并发来启动工作流——使用 `DBOS.startWorkflow` 或队列
- 工作流必须是确定性的——非确定性操作放在步骤中
- 不要从工作流或步骤修改全局变量

## 使用方法

阅读各个规则文件以获取详细说明和示例：

```
references/lifecycle-config.md
references/workflow-determinism.md
references/queue-concurrency.md
```

## 参考资料

- https://docs.dbos.dev/
- https://github.com/dbos-inc/dbos-transact-ts

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
