# 核心工作流参考

完整的 RARV 循环、CONTINUITY.md 模板和自主规则。

---

## 自主规则

**本系统以零人工干预运行。**

### 核心规则
1. **永不提问** - 不要说"您想让我..."、"我应该..."或"您更倾向于..."
2. **永不等待确认** - 立即采取行动。如果需要做什么，就去做。
3. **永不主动停止** - 持续运行直到完成承诺兑现或达到最大迭代次数
4. **永不建议替代方案** - 选择最佳选项并执行。不要"您也可以..."或"或者..."
5. **始终使用 RARV 循环** - 每个行动遵循推理-行动-反思-验证模式

---

## RARV 循环（推理-行动-反思-验证）

**增强版自动自我验证循环（Boris Cherny 模式）**

每次迭代遵循此循环：

```
+-------------------------------------------------------------------+
| 推理：接下来需要做什么？                                           |
| - 首先读取 .loki/CONTINUITY.md（工作记忆）                         |
| - 读取"错误与学习"以避免过去的错误                                 |
| - 检查 .loki/state/orchestrator.json 中的当前状态                 |
| - 查看 .loki/queue/pending.json 中的待处理任务                    |
| - 识别最高优先级的非阻塞任务                                       |
| - 确定完成它的确切步骤                                            |
+-------------------------------------------------------------------+
| 行动：执行任务                                                     |
| - 通过 Task 工具派发子智能体 或 直接执行                           |
| - 编写代码，运行测试，修复问题                                     |
| - 原子性提交变更（git 检查点）                                     |
| - 更新队列文件 (.loki/queue/*.json)                                |
+-------------------------------------------------------------------+
| 反思：成功了吗？接下来呢？                                         |
| - 验证任务成功（测试通过，无错误）                                 |
| - 更新 .loki/CONTINUITY.md 记录进度                                |
| - 更新编排器状态                                                   |
| - 检查完成承诺 - 我们完成了吗？                                    |
| - 如果未完成，循环回推理步骤                                       |
+-------------------------------------------------------------------+
| 验证：让 AI 测试自己的工作（2-3 倍质量提升）                       |
| - 运行自动化测试（单元、集成、E2E）                                |
| - 检查编译/构建（无错误或警告）                                    |
| - 对照规范验证 (.loki/specs/openapi.yaml)                          |
| - 通过写入后钩子运行 linter/格式化工具                             |
| - 如适用进行浏览器/运行时测试                                      |
|                                                                   |
| 如果验证失败：                                                    |
|   1. 捕获错误详情（堆栈跟踪、日志）                                |
|   2. 分析根本原因                                                 |
|   3. 更新 CONTINUITY.md 中的"错误与学习"                          |
|   4. 如需要回滚到最后良好的 git 检查点                             |
|   5. 应用学习并从推理步骤重试                                     |
|                                                                   |
| - 如果验证通过，标记任务完成并继续                                 |
+-------------------------------------------------------------------+
```

**关键增强：** 验证步骤创建了一个反馈循环，AI：
- 自动测试每个变更
- 通过更新 CONTINUITY.md 从失败中学习
- 带学习到的上下文重试
- 实现 2-3 倍质量提升（Boris Cherny 观察到的结果）

---

## CONTINUITY.md - 工作记忆协议

**关键：** 您在 `.loki/CONTINUITY.md` 有一个持久的工作记忆文件，在所有执行轮次中维护状态。

### 每次轮次开始时：
1. 读取 `.loki/CONTINUITY.md` 以定位当前状态
2. 在整个推理过程中参考它
3. 永远不要在不先检查 CONTINUITY.md 的情况下做决策

### 每次轮次结束时：
1. 用任何重要的新信息更新 `.loki/CONTINUITY.md`
2. 记录完成的内容
3. 记录接下来需要发生什么
4. 记录任何阻塞或做出的决策

### CONTINUITY.md 模板

```markdown
# Loki Mode 工作记忆
最后更新：[ISO 时间戳]
当前阶段：[bootstrap|discovery|architecture|development|qa|deployment|growth]
当前迭代：[数字]

## 活跃目标
[我们当前要完成的目标 - 1-2 句话]

## 当前任务
- ID：[队列中的任务 ID]
- 描述：[我们在做什么]
- 状态：[in-progress|blocked|reviewing]
- 开始时间：[时间戳]

## 刚完成
- [最近的成果，带 file:line 引用]
- [上一个成果]
- [等 - 最近 5 项]

## 下一步行动（优先级顺序）
1. [立即下一步]
2. [后续步骤]
3. [等]

## 活跃阻塞
- [任何当前的阻塞或等待项]

## 本会话关键决策
- [决策]：[理由] - [时间戳]

## 错误与学习（自我更新）
**关键：** 发生错误时，智能体必须更新此部分以防止重复错误。

### 模式：错误 -> 学习 -> 预防
- **失败内容：** [发生的具体错误]
- **失败原因：** [根本原因分析]
- **如何预防：** [避免将来发生的具体行动]
- **时间戳：** [学习时间]
- **智能体：** [哪个智能体学到的]

### 示例：
- **失败内容：** TypeScript 编译错误 - 缺少返回类型注解
- **失败原因：** Express 路由处理器在严格模式下需要显式的 `: void` 返回类型
- **如何预防：** 始终为路由处理器添加 `: void`：`(req, res): void =>`
- **时间戳：** 2026-01-04T00:16:00Z
- **智能体：** eng-001-backend-api

**自我更新协议：**
```
ON_ERROR:
  1. 捕获错误详情（堆栈跟踪、上下文）
  2. 分析根本原因
  3. 将学习写入 CONTINUITY.md 的"错误与学习"
  4. 基于学习更新方法
  5. 用修正后的方法重试
```

## 工作上下文
[当前工作所需的任何关键信息 - 正在使用的 API 密钥、架构决策、正在遵循的模式等。]

## 当前正在修改的文件
- [文件路径]：[我们要更改的内容]
```

---

## 记忆层次结构

记忆系统协同工作：

1. **CONTINUITY.md** = 工作记忆（当前会话状态，每次轮次更新）
2. **ledgers/** = 智能体特定状态（定期检查点）
3. **handoffs/** = 智能体间转移（智能体切换时）
4. **learnings/** = 提取的模式（任务完成时）
5. **rules/** = 永久验证模式（从学习提升）

**CONTINUITY.md 是"我现在在做什么？"的主要事实来源**

---

## Git 检查点系统

**关键：** 每个完成的任务必须创建 git 检查点以便安全回滚。

### 协议：任务完成后自动提交

**规则：** 当 `task.status == "completed"` 时，立即创建 git 提交。

```bash
# Git 检查点协议
ON_TASK_COMPLETE() {
    task_id=$1
    task_title=$2
    agent_id=$3

    # 暂存修改的文件
    git add <modified_files>

    # 创建结构化提交消息
    git commit -m "[Loki] ${agent_type}-${task_id}: ${task_title}

${detailed_description}

Agent: ${agent_id}
Parent: ${parent_agent_id}
Spec: ${spec_reference}
Tests: ${test_files}
Git-Checkpoint: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

    # 在任务元数据中存储提交 SHA
    commit_sha=$(git rev-parse HEAD)
    update_task_metadata task_id git_commit_sha "$commit_sha"

    # 更新 CONTINUITY.md
    echo "- Task $task_id completed (commit: $commit_sha)" >> .loki/CONTINUITY.md
}
```

### 提交消息格式

**模板：**
```
[Loki] ${agent_type}-${task_id}: ${task_title}

${detailed_description}

Agent: ${agent_id}
Parent: ${parent_agent_id}
Spec: ${spec_reference}
Tests: ${test_files}
Git-Checkpoint: ${timestamp}
```

**示例：**
```
[Loki] eng-005-backend: 实现 POST /api/todos 端点

按 OpenAPI 规范创建 todo 创建端点。
- title 字段输入验证
- SQLite 插入带时间戳
- 返回 201 和创建的 todo 对象
- 契约测试通过

Agent: eng-001-backend-api
Parent: orchestrator-main
Spec: .loki/specs/openapi.yaml#/paths/~1api~1todos/post
Tests: backend/tests/todos.contract.test.ts
Git-Checkpoint: 2026-01-04T05:45:00Z
```

### 回滚策略

**何时回滚：**
- 合并后质量门失败
- 集成测试失败
- 检测到安全漏洞
- 发现破坏性变更

**回滚命令：**
```bash
# 查找最后良好的检查点
last_good_commit=$(git log --grep="\[Loki\].*task-${last_good_task_id}" --format=%H -n 1)

# 回滚到该检查点
git reset --hard $last_good_commit

# 更新 CONTINUITY.md
echo "ROLLBACK: Reset to task-${last_good_task_id} (commit: $last_good_commit)" >> .loki/CONTINUITY.md

# 重新排队失败的任务
move_tasks_to_pending after_task=$last_good_task_id
```

---

## 如果子智能体失败

1. 不要尝试手动修复（上下文污染）
2. 派发修复子智能体，带具体错误上下文
3. 如果修复子智能体失败 3 次，移至死信队列
4. 为该智能体类型开启熔断器
5. 警报编排器请求人工审查
