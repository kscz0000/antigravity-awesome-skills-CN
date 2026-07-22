---
name: debug-buttercup
description: "所有 Pod 都运行在 crs 命名空间中。当 crs 命名空间中的 Pod 处于 CrashLoopBackOff、OOMKilled 或正在重启时，多个服务同时重启（级联故障），或 Redis 无响应或显示 AOF 警告时使用。"
risk: unknown
source: community
---

# Debug Buttercup

## 何时使用
- `crs` 命名空间中的 Pod 处于 CrashLoopBackOff、OOMKilled 或正在重启
- 多个服务同时重启（级联故障）
- Redis 无响应或显示 AOF 警告
- 队列持续增长但任务未推进
- 节点显示 DiskPressure、MemoryPressure 或 PID 压力
- Build-bot 无法连接 Docker 守护进程（DinD 故障）
- Scheduler 卡住且任务状态未推进
- 健康检查探针意外失败
- 部署的 Helm values 与实际 Pod 配置不匹配

## 何时不使用

- 部署或升级 Buttercup（使用 Helm 和部署指南）
- 调试 `crs` Kubernetes 命名空间之外的问题
- 不涉及故障症状的性能调优

## 命名空间和服务

所有 Pod 都运行在命名空间 `crs` 中。关键服务：

| 层级 | 服务 |
|-------|----------|
| 基础设施 | redis, dind, litellm, registry-cache |
| 编排 | scheduler, task-server, task-downloader, scratch-cleaner |
| 模糊测试 | build-bot, fuzzer-bot, coverage-bot, tracer-bot, merger-bot |
| 分析 | patcher, seed-gen, program-model, pov-reproducer |
| 接口 | competition-api, ui |

## 分诊工作流

始终从分诊开始。首先运行这三条命令：

```bash
# 1. Pod 状态 - 查看重启、CrashLoopBackOff、OOMKilled
kubectl get pods -n crs -o wide

# 2. 事件 - 出错的时间线
kubectl get events -n crs --sort-by='.lastTimestamp'

# 3. 仅警告 - 过滤噪音
kubectl get events -n crs --field-selector type=Warning --sort-by='.lastTimestamp'
```

然后缩小范围：

```bash
# 为什么特定 Pod 重启？检查 Last State Reason（OOMKilled、Error、Completed）
kubectl describe pod -n crs <pod-name> | grep -A8 'Last State:'

# 检查实际资源限制与预期值
kubectl get pod -n crs <pod-name> -o jsonpath='{.spec.containers[0].resources}'

# 崩溃容器的日志（--previous = 已死亡的容器）
kubectl logs -n crs <pod-name> --previous --tail=200

# 当前日志
kubectl logs -n crs <pod-name> --tail=200
```

### 历史问题与正在发生的问题

高重启次数不一定意味着问题正在持续——重启会在 Pod 生命周期内累积。始终区分：
- `--tail` 显示日志缓冲区的末尾，可能包含旧消息。使用 `--since=300s` 确认问题是否正在发生。
- 日志输出中的 `--timestamps` 有助于关联跨服务的事件。
- 在 `describe pod` 中检查 `Last State` 时间戳，查看最近一次崩溃实际发生的时间。

### 级联检测

当许多 Pod 大约在同一时间重启时，在调查单个 Pod 之前检查共享依赖故障。最常见的级联：Redis 宕机 -> 每个服务都出现 `ConnectionError`/`ConnectionRefusedError` -> 大规模重启。在多个 `--previous` 日志中查找相同错误——如果它们都显示 `redis.exceptions.ConnectionError`，则调试 Redis，而非单个服务。

## 日志分析

```bash
# 一次查看服务的所有副本
kubectl logs -n crs -l app=fuzzer-bot --tail=100 --prefix

# 实时流式输出
kubectl logs -n crs -l app.kubernetes.io/name=redis -f

# 收集所有日志到磁盘（现有脚本）
bash deployment/collect-logs.sh
```

## 资源压力

```bash
# 每个 Pod 的 CPU/内存
kubectl top pods -n crs

# 节点级别
kubectl top nodes

# 节点条件（磁盘压力、内存压力、PID 压力）
kubectl describe node <node> | grep -A5 Conditions

# Pod 内部磁盘使用情况
kubectl exec -n crs <pod> -- df -h

# 什么在占用磁盘
kubectl exec -n crs <pod> -- sh -c 'du -sh /corpus/* 2>/dev/null'
kubectl exec -n crs <pod> -- sh -c 'du -sh /scratch/* 2>/dev/null'
```

## Redis 调试

Redis 是核心骨干。当它宕机时，一切都会级联故障。

```bash
# Redis Pod 状态
kubectl get pods -n crs -l app.kubernetes.io/name=redis

# Redis 日志（AOF 警告、OOM、连接问题）
kubectl logs -n crs -l app.kubernetes.io/name=redis --tail=200

# 连接 Redis CLI
kubectl exec -n crs <redis-pod> -- redis-cli

# redis-cli 内部：关键诊断命令
INFO memory          # used_memory_human, maxmemory
INFO persistence     # aof_enabled, aof_last_bgrewrite_status, aof_delayed_fsync
INFO clients         # connected_clients, blocked_clients
INFO stats           # total_connections_received, rejected_connections
CLIENT LIST          # 查看连接的客户端
DBSIZE               # 键总数

# AOF 配置
CONFIG GET appendonly     # AOF 是否启用？
CONFIG GET appendfsync   # fsync 策略：everysec、always 或 no

# /data 挂载在哪里？（磁盘 vs tmpfs 对 AOF 性能有影响）
```

```bash
kubectl exec -n crs <redis-pod> -- mount | grep /data
kubectl exec -n crs <redis-pod> -- du -sh /data/
```

### 队列检查

Buttercup 使用带消费者组的 Redis 流。队列名称：

| 队列 | 流键名 |
|-------|-----------|
| Build | fuzzer_build_queue |
| Build Output | fuzzer_build_output_queue |
| Crash | fuzzer_crash_queue |
| Confirmed Vulns | confirmed_vulnerabilities_queue |
| Download Tasks | orchestrator_download_tasks_queue |
| Ready Tasks | tasks_ready_queue |
| Patches | patches_queue |
| Index | index_queue |
| Index Output | index_output_queue |
| Traced Vulns | traced_vulnerabilities_queue |
| POV Requests | pov_reproducer_requests_queue |
| POV Responses | pov_reproducer_responses_queue |
| Delete Task | orchestrator_delete_task_queue |

```bash
# 检查流长度（待处理消息数）
kubectl exec -n crs <redis-pod> -- redis-cli XLEN fuzzer_build_queue

# 检查消费者组延迟
kubectl exec -n crs <redis-pod> -- redis-cli XINFO GROUPS fuzzer_build_queue

# 检查每个消费者的待处理消息
kubectl exec -n crs <redis-pod> -- redis-cli XPENDING fuzzer_build_queue build_bot_consumers - + 10

# 任务注册表大小
kubectl exec -n crs <redis-pod> -- redis-cli HLEN tasks_registry

# 任务状态计数
kubectl exec -n crs <redis-pod> -- redis-cli SCARD cancelled_tasks
kubectl exec -n crs <redis-pod> -- redis-cli SCARD succeeded_tasks
kubectl exec -n crs <redis-pod> -- redis-cli SCARD errored_tasks
```

消费者组：`build_bot_consumers`、`orchestrator_group`、`patcher_group`、`index_group`、`tracer_bot_group`。

## 健康检查

Pod 将时间戳写入 `/tmp/health_check_alive`。存活探针检查文件的新鲜度。

```bash
# 检查健康检查文件的新鲜度
kubectl exec -n crs <pod> -- stat /tmp/health_check_alive
kubectl exec -n crs <pod> -- cat /tmp/health_check_alive
```

如果 Pod 处于重启循环，健康检查文件很可能已过期，因为主进程被阻塞（例如等待 Redis、卡在 I/O 上）。

## 遥测（OpenTelemetry / Signoz）

所有服务通过 OpenTelemetry 导出追踪和指标。如果部署了 Signoz（`global.signoz.deployed: true`），使用其 UI 进行跨服务的分布式追踪。

```bash
# 检查 OTEL 是否配置
kubectl exec -n crs <pod> -- env | grep OTEL

# 验证 Signoz Pod 是否运行（如果已部署）
kubectl get pods -n platform -l app.kubernetes.io/name=signoz
```

追踪对于诊断慢任务处理、识别管道中哪个服务是瓶颈、以及关联 scheduler -> build-bot -> fuzzer-bot 链中的事件特别有用。

## 卷和存储

```bash
# PVC 状态
kubectl get pvc -n crs

# 检查 corpus tmpfs 是否挂载、其大小和后备类型
kubectl exec -n crs <pod> -- mount | grep corpus_tmpfs
kubectl exec -n crs <pod> -- df -h /corpus_tmpfs 2>/dev/null

# 检查 CORPUS_TMPFS_PATH 是否设置
kubectl exec -n crs <pod> -- env | grep CORPUS

# 完整磁盘布局 - 真实磁盘 vs tmpfs 上有什么
kubectl exec -n crs <pod> -- df -h
```

当 `global.volumes.corpusTmpfs.enabled: true` 时设置 `CORPUS_TMPFS_PATH`。这会影响 fuzzer-bot、coverage-bot、seed-gen 和 merger-bot。

### 部署配置验证

当行为与预期不符时，验证 Helm values 是否实际生效：

```bash
# 检查 Pod 的实际资源限制
kubectl get pod -n crs <pod-name> -o jsonpath='{.spec.containers[0].resources}'

# 检查 Pod 的实际卷定义
kubectl get pod -n crs <pod-name> -o jsonpath='{.spec.volumes}'
```

Helm values 模板中的拼写错误（例如键名错误）会静默回退到 chart 默认值。如果部署的资源与 values 模板不匹配，请检查键名是否匹配。

## 服务特定调试

有关每个服务的详细症状、根本原因和修复方法，请参阅 references/failure-patterns.md。

快速参考：

- **DinD**: `kubectl logs -n crs -l app=dind --tail=100` -- 查看 docker 守护进程崩溃、存储驱动错误
- **Build-bot**: 检查构建队列深度、DinD 连接性、编译期间的 OOM
- **Fuzzer-bot**: corpus 磁盘使用、CPU 限流、崩溃队列积压
- **Patcher**: LiteLLM 连接性、LLM 超时、补丁队列深度
- **Scheduler**: 中央大脑 -- `kubectl logs -n crs -l app=scheduler --tail=-1 --prefix | grep "WAIT_PATCH_PASS\|ERROR\|SUBMIT"`

## 诊断脚本

运行自动分诊快照：

```bash
bash {baseDir}/scripts/diagnose.sh
```

传递 `--full` 以同时转储所有 Pod 的最近日志：

```bash
bash {baseDir}/scripts/diagnose.sh --full
```

这会一次性收集 Pod 状态、事件、资源使用、Redis 健康状况和队列深度。

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
