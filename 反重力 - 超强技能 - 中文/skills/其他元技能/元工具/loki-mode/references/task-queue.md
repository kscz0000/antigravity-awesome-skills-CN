# 任务队列参考

分布式任务队列系统、死信处理和熔断器。

---

## 任务模式

```json
{
  "id": "uuid",
  "idempotencyKey": "hash-of-task-content",
  "type": "eng-backend|eng-frontend|ops-devops|...",
  "priority": 1-10,
  "dependencies": ["task-id-1", "task-id-2"],
  "payload": {
    "action": "implement|test|deploy|...",
    "target": "file/path or resource",
    "params": {},
    "goal": "成功是什么样的（高层目标）",
    "constraints": ["无第三方依赖", "保持向后兼容"],
    "context": {
      "relatedFiles": ["file1.ts", "file2.ts"],
      "architectureDecisions": ["ADR-001: 使用 JWT 令牌"],
      "previousAttempts": "之前尝试了什么，为什么失败"
    }
  },
  "createdAt": "ISO",
  "claimedBy": null,
  "claimedAt": null,
  "timeout": 3600,
  "retries": 0,
  "maxRetries": 3,
  "backoffSeconds": 60,
  "lastError": null,
  "completedAt": null,
  "result": {
    "status": "success|failed",
    "output": "产生了什么",
    "decisionReport": { ... }
  }
}
```

**决策报告是已完成任务的必需项。** 没有适当决策文档的任务将被标记为不完整。

---

## 队列文件

```
.loki/queue/
+-- pending.json       # 等待领取的任务
+-- in-progress.json   # 当前执行中的任务
+-- completed.json     # 已完成任务
+-- dead-letter.json   # 失败任务待审查
+-- cancelled.json     # 已取消任务
```

---

## 队列操作

### 领取任务（带文件锁）

```python
def claim_task(agent_id, agent_capabilities):
    with file_lock(".loki/state/locks/queue.lock", timeout=10):
        pending = read_json(".loki/queue/pending.json")

        # 查找符合条件的任务
        for task in sorted(pending.tasks, key=lambda t: -t.priority):
            if task.type not in agent_capabilities:
                continue
            if task.claimedBy and not claim_expired(task):
                continue
            if not all_dependencies_completed(task.dependencies):
                continue
            if circuit_breaker_open(task.type):
                continue

            # 领取它
            task.claimedBy = agent_id
            task.claimedAt = now()
            move_task(task, "pending", "in-progress")
            return task

        return None
```

### 文件锁（Bash）

```bash
#!/bin/bash
# 使用 flock 进行原子任务领取

QUEUE_FILE=".loki/queue/pending.json"
LOCK_FILE=".loki/state/locks/queue.lock"

(
  flock -x -w 10 200 || exit 1

  # 原子读取、领取、写入
  TASK=$(jq -r '.tasks | map(select(.claimedBy == null)) | .[0]' "$QUEUE_FILE")
  if [ "$TASK" != "null" ]; then
    TASK_ID=$(echo "$TASK" | jq -r '.id')
    jq --arg id "$TASK_ID" --arg agent "$AGENT_ID" \
      '.tasks |= map(if .id == $id then .claimedBy = $agent | .claimedAt = now else . end)' \
      "$QUEUE_FILE" > "${QUEUE_FILE}.tmp" && mv "${QUEUE_FILE}.tmp" "$QUEUE_FILE"
    echo "$TASK_ID"
  fi

) 200>"$LOCK_FILE"
```

### 完成任务

```python
def complete_task(task_id, result, success=True):
    with file_lock(".loki/state/locks/queue.lock"):
        task = find_task(task_id, "in-progress")
        task.completedAt = now()
        task.result = result

        if success:
            move_task(task, "in-progress", "completed")
            reset_circuit_breaker(task.type)
            trigger_dependents(task_id)
        else:
            handle_failure(task)
```

---

## 失败处理

### 指数退避

```python
def handle_failure(task):
    task.retries += 1
    task.lastError = get_last_error()

    if task.retries >= task.maxRetries:
        # 移动到死信队列
        move_task(task, "in-progress", "dead-letter")
        increment_circuit_breaker(task.type)
        alert_orchestrator(f"Task {task.id} moved to dead letter queue")
    else:
        # 指数退避：60s, 120s, 240s, ...
        task.backoffSeconds = task.backoffSeconds * (2 ** (task.retries - 1))
        task.availableAt = now() + task.backoffSeconds
        move_task(task, "in-progress", "pending")
        log(f"Task {task.id} retry {task.retries}, backoff {task.backoffSeconds}s")
```

---

## 死信队列

死信队列中的任务需要人工审查：

### 审查流程

1. 读取 `.loki/queue/dead-letter.json`
2. 对每个任务：
   - 分析 `lastError` 和失败模式
   - 确定：
     - 任务无效 -> 删除
     - 智能体有 bug -> 修复智能体，重试
     - 外部依赖宕机 -> 等待，重试
     - 需要人工决策 -> 升级
3. 重试：将任务移回 pending 并重置重试次数
4. 在 `.loki/logs/decisions/dlq-review-{date}.md` 中记录决策

---

## 幂等性

```python
def enqueue_task(task):
    # 从内容生成幂等键
    task.idempotencyKey = hash(json.dumps(task.payload, sort_keys=True))

    # 检查是否已存在
    for queue in ["pending", "in-progress", "completed"]:
        existing = find_by_idempotency_key(task.idempotencyKey, queue)
        if existing:
            log(f"Duplicate task detected: {task.idempotencyKey}")
            return existing.id  # 返回已存在的，不创建重复

    # 可以安全创建
    save_task(task, "pending")
    return task.id
```

---

## 任务取消

```python
def cancel_task(task_id, reason):
    with file_lock(".loki/state/locks/queue.lock"):
        for queue in ["pending", "in-progress"]:
            task = find_task(task_id, queue)
            if task:
                task.cancelledAt = now()
                task.cancelReason = reason
                move_task(task, queue, "cancelled")

                # 同时取消依赖任务
                for dep_task in find_tasks_depending_on(task_id):
                    cancel_task(dep_task.id, f"Parent {task_id} cancelled")

                return True
        return False
```

---

## 熔断器

### 状态模式

```json
{
  "circuitBreakers": {
    "eng-backend": {
      "state": "closed",
      "failures": 0,
      "lastFailure": null,
      "openedAt": null,
      "halfOpenAt": null
    }
  }
}
```

### 状态

| 状态 | 描述 | 行为 |
|-------|-------------|----------|
| **closed** | 正常运行 | 任务正常流动 |
| **open** | 失败过多 | 阻止此类型的所有任务 |
| **half-open** | 测试恢复 | 允许 1 个测试任务 |

### 配置

```yaml
# .loki/config/circuit-breakers.yaml
defaults:
  failureThreshold: 5
  cooldownSeconds: 300
  halfOpenAfter: 60

overrides:
  ops-security:
    failureThreshold: 3  # 安全更敏感
  biz-marketing:
    failureThreshold: 10  # 非关键更宽容
```

### 实现

```python
def check_circuit_breaker(agent_type):
    cb = load_circuit_breaker(agent_type)

    if cb.state == "closed":
        return True  # 继续

    if cb.state == "open":
        if now() > cb.openedAt + config.halfOpenAfter:
            cb.state = "half-open"
            save_circuit_breaker(cb)
            return True  # 允许测试任务
        return False  # 仍在阻止

    if cb.state == "half-open":
        return False  # 已在测试，等待

def on_task_success(agent_type):
    cb = load_circuit_breaker(agent_type)
    if cb.state == "half-open":
        cb.state = "closed"
        cb.failures = 0
    save_circuit_breaker(cb)

def on_task_failure(agent_type):
    cb = load_circuit_breaker(agent_type)
    cb.failures += 1
    cb.lastFailure = now()

    if cb.state == "half-open" or cb.failures >= config.failureThreshold:
        cb.state = "open"
        cb.openedAt = now()
        alert_orchestrator(f"Circuit breaker OPEN for {agent_type}")

    save_circuit_breaker(cb)
```

---

## 速率限制处理

### 检测

```python
def detect_rate_limit(error):
    indicators = [
        "rate limit",
        "429",
        "too many requests",
        "quota exceeded",
        "retry-after"
    ]
    return any(ind in str(error).lower() for ind in indicators)
```

### 响应协议

```python
def handle_rate_limit(agent_id, error):
    # 1. 保存状态检查点
    checkpoint_state(agent_id)

    # 2. 计算退避
    retry_after = parse_retry_after(error) or calculate_exponential_backoff()

    # 3. 记录并等待
    log(f"Rate limit hit for {agent_id}, waiting {retry_after}s")

    # 4. 通知其他智能体减速
    broadcast_signal("SLOWDOWN", {"wait": retry_after / 2})

    # 5. 退避后恢复
    schedule_resume(agent_id, retry_after)
```

### 指数退避

```python
def calculate_exponential_backoff(attempt=1, base=60, max_wait=3600):
    wait = min(base * (2 ** (attempt - 1)), max_wait)
    jitter = random.uniform(0, wait * 0.1)
    return wait + jitter
```

---

## 优先级系统

| 优先级 | 用例 | 示例 |
|----------|----------|---------|
| 10 | 关键阻塞 | 安全漏洞修复 |
| 8-9 | 高优先级 | 核心功能实现 |
| 5-7 | 正常 | 标准任务 |
| 3-4 | 低优先级 | 文档、清理 |
| 1-2 | 后台 | 锦上添花的改进 |

任务始终按优先级顺序在其类型内处理。
