# 记忆系统参考

基于 2025 年研究（MIRIX、A-Mem、MemGPT、AriGraph）的增强记忆架构。

---

## 记忆层次结构概览

```
+------------------------------------------------------------------+
| 工作记忆 (CONTINUITY.md)                                          |
| - 当前会话状态                                                    |
| - 每次轮次更新                                                    |
| - 我现在正在做什么？                                              |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
| 情景记忆 (.loki/memory/episodic/)                                |
| - 具体交互痕迹                                                    |
| - 带时间戳的完整上下文                                            |
| - "当我尝试 X 时发生了什么？"                                     |
+------------------------------------------------------------------+
        |
        v (整合)
+------------------------------------------------------------------+
| 语义记忆 (.loki/memory/semantic/)                                |
| - 泛化的模式和事实                                                |
| - 上下文无关的知识                                                |
| - "X 通常如何工作？"                                              |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
| 程序记忆 (.loki/memory/skills/)                                  |
| - 学习到的动作序列                                                |
| - 可复用的技能模板                                                |
| - "如何成功做 X"                                                  |
+------------------------------------------------------------------+
```

---

## 目录结构

```
.loki/memory/
+-- episodic/
|   +-- 2026-01-06/
|   |   +-- task-001.json      # 任务执行的完整痕迹
|   |   +-- task-002.json
|   +-- index.json             # 用于检索的时间索引
|
+-- semantic/
|   +-- patterns.json          # 泛化的模式
|   +-- anti-patterns.json     # 不应该做什么
|   +-- facts.json             # 领域知识
|   +-- links.json             # Zettelkasten 风格连接
|
+-- skills/
|   +-- api-implementation.md  # 技能：如何实现 API
|   +-- test-writing.md        # 技能：如何编写测试
|   +-- debugging.md           # 技能：如何调试问题
|
+-- ledgers/                   # 智能体特定检查点
|   +-- eng-001.json
|   +-- qa-001.json
|
+-- handoffs/                  # 智能体间转移
|   +-- handoff-001.json
|
+-- learnings/                 # 从错误中提取
|   +-- 2026-01-06.json

# 相关：指标系统（与记忆分离）
# .loki/metrics/
# +-- efficiency/              # 任务成本追踪（时间、智能体、重试）
# +-- rewards/                 # 结果/效率/偏好信号
# +-- dashboard.json           # 滚动 7 天指标摘要
# 详见 references/tool-orchestration.md
```

---

## 情景记忆模式

每次任务执行创建一个情景痕迹：

```json
{
  "id": "ep-2026-01-06-001",
  "task_id": "task-042",
  "timestamp": "2026-01-06T10:30:00Z",
  "duration_seconds": 342,
  "agent": "eng-001-backend",
  "context": {
    "phase": "development",
    "goal": "实现 POST /api/todos 端点",
    "constraints": ["无第三方依赖", "< 200ms 响应"],
    "files_involved": ["src/routes/todos.ts", "src/db/todos.ts"]
  },
  "action_log": [
    {"t": 0, "action": "read_file", "target": "openapi.yaml"},
    {"t": 5, "action": "write_file", "target": "src/routes/todos.ts"},
    {"t": 120, "action": "run_test", "result": "fail", "error": "缺少返回类型"},
    {"t": 140, "action": "edit_file", "target": "src/routes/todos.ts"},
    {"t": 180, "action": "run_test", "result": "pass"}
  ],
  "outcome": "success",
  "errors_encountered": [
    {
      "type": "TypeScript 编译",
      "message": "缺少返回类型注解",
      "resolution": "为路由处理器添加显式的 :void"
    }
  ],
  "artifacts_produced": ["src/routes/todos.ts", "tests/todos.test.ts"],
  "git_commit": "abc123"
}
```

---

## 语义记忆模式

从情景记忆中提取的泛化模式：

```json
{
  "id": "sem-001",
  "pattern": "Express 路由处理器在严格模式下需要显式返回类型",
  "category": "typescript",
  "conditions": [
    "使用 TypeScript 严格模式",
    "编写 Express 路由处理器",
    "处理器不返回值"
  ],
  "correct_approach": "在处理器签名中添加 `: void`：`(req, res): void =>`",
  "incorrect_approach": "省略返回类型注解",
  "confidence": 0.95,
  "source_episodes": ["ep-2026-01-06-001", "ep-2026-01-05-012"],
  "usage_count": 8,
  "last_used": "2026-01-06T14:00:00Z",
  "links": [
    {"to": "sem-005", "relation": "related_to"},
    {"to": "sem-012", "relation": "supersedes"}
  ]
}
```

---

## 情景到语义整合

**何时整合：** 任务完成后、空闲时间、阶段边界。

```python
def consolidate_episodic_to_semantic():
    """
    将具体经验转化为通用知识。
    基于 MemGPT 和 Voyager 研究。
    """
    # 1. 加载最近的情景记忆
    recent_episodes = load_episodes(since=hours_ago(24))

    # 2. 按相似性分组
    clusters = cluster_by_similarity(recent_episodes)

    for cluster in clusters:
        if len(cluster) >= 2:  # 模式出现多次
            # 3. 提取共同模式
            pattern = extract_common_pattern(cluster)

            # 4. 验证模式
            if pattern.confidence >= 0.8:
                # 5. 检查是否已存在
                existing = find_similar_semantic(pattern)
                if existing:
                    # 用新证据更新现有模式
                    existing.source_episodes.extend([e.id for e in cluster])
                    existing.confidence = recalculate_confidence(existing)
                    existing.usage_count += 1
                else:
                    # 创建新的语义记忆
                    save_semantic(pattern)

    # 6. 从错误中整合反模式
    error_episodes = [e for e in recent_episodes if e.errors_encountered]
    for episode in error_episodes:
        for error in episode.errors_encountered:
            anti_pattern = {
                "what_fails": error.type,
                "why": error.message,
                "prevention": error.resolution,
                "source": episode.id
            }
            save_anti_pattern(anti_pattern)
```

---

## Zettelkasten 风格链接

每个记忆笔记可以链接到相关笔记：

```json
{
  "links": [
    {"to": "sem-005", "relation": "derived_from"},
    {"to": "sem-012", "relation": "contradicts"},
    {"to": "sem-018", "relation": "elaborates"},
    {"to": "sem-023", "relation": "example_of"},
    {"to": "sem-031", "relation": "superseded_by"}
  ]
}
```

### 链接关系

| 关系 | 含义 |
|------|------|
| `derived_from` | 此模式从该情景中提取 |
| `related_to` | 概念相似，经常一起使用 |
| `contradicts` | 这些模式冲突 - 需要解决 |
| `elaborates` | 提供更多关于链接模式的细节 |
| `example_of` | 通用模式的具体实例 |
| `supersedes` | 此模式替换旧模式 |
| `superseded_by` | 此模式已过时，使用链接的模式 |

---

## 程序记忆（技能）

可复用的动作序列：

```markdown
# 技能：API 端点实现

## 前置条件
- OpenAPI 规范存在于 .loki/specs/openapi.yaml
- 数据库模式已定义

## 步骤
1. 从 openapi.yaml 读取端点规范
2. 在 src/routes/{resource}.ts 中创建路由处理器
3. 使用规范模式实现请求验证
4. 实现业务逻辑
5. 如需要添加数据库操作
6. 返回匹配规范模式的响应
7. 编写契约测试
8. 运行测试，验证通过

## 常见错误与修复
- 缺少返回类型：为处理器添加 `: void`
- 模式不匹配：从规范重新生成类型

## 退出标准
- 所有契约测试通过
- 响应匹配 OpenAPI 规范
- 无 TypeScript 错误
```

---

## 记忆检索

### 按相似性检索

```python
def retrieve_relevant_memory(current_context):
    """
    检索与当前任务相关的记忆。
    使用语义相似性 + 时间新近度。
    """
    query_embedding = embed(current_context.goal)

    # 1. 首先搜索语义记忆
    semantic_matches = vector_search(
        collection="semantic",
        query=query_embedding,
        top_k=5
    )

    # 2. 搜索情景记忆中的相似情况
    episodic_matches = vector_search(
        collection="episodic",
        query=query_embedding,
        top_k=3,
        filters={"outcome": "success"}  # 优先成功的情景
    )

    # 3. 搜索技能
    skill_matches = keyword_search(
        collection="skills",
        keywords=extract_keywords(current_context)
    )

    # 4. 合并并排名
    combined = merge_and_rank(
        semantic_matches,
        episodic_matches,
        skill_matches,
        weights={"semantic": 0.5, "episodic": 0.3, "skills": 0.2}
    )

    return combined[:5]  # 返回前 5 个最相关的
```

### 任务执行前检索

**关键：** 在执行任何任务之前，检索相关记忆：

```python
def before_task_execution(task):
    """
    将相关记忆注入任务上下文。
    """
    # 1. 检索相关记忆
    memories = retrieve_relevant_memory(task)

    # 2. 检查反模式
    anti_patterns = search_anti_patterns(task.action_type)

    # 3. 注入到提示词
    task.context["relevant_patterns"] = [m.summary for m in memories]
    task.context["avoid_these"] = [a.summary for a in anti_patterns]
    task.context["applicable_skills"] = find_skills(task.type)

    return task
```

---

## 账本系统（智能体检查点）

每个智能体维护自己的账本：

```json
{
  "agent_id": "eng-001-backend",
  "last_checkpoint": "2026-01-06T10:00:00Z",
  "tasks_completed": 12,
  "current_task": "task-042",
  "state": {
    "files_modified": ["src/routes/todos.ts"],
    "uncommitted_changes": true,
    "last_git_commit": "abc123"
  },
  "context": {
    "tech_stack": ["express", "typescript", "sqlite"],
    "patterns_learned": ["sem-001", "sem-005"],
    "current_goal": "实现 todos 的 CRUD"
  }
}
```

---

## 交接协议

在智能体之间切换时：

```json
{
  "id": "handoff-001",
  "from_agent": "eng-001-backend",
  "to_agent": "qa-001-testing",
  "timestamp": "2026-01-06T11:00:00Z",
  "context": {
    "what_was_done": "实现了 POST /api/todos 端点",
    "artifacts": ["src/routes/todos.ts"],
    "git_state": "commit abc123",
    "needs_testing": ["验证的单元测试", "契约测试"],
    "known_issues": [],
    "relevant_patterns": ["sem-001"]
  }
}
```

---

## 记忆维护

### 修剪旧的情景记忆

```python
def prune_episodic_memories():
    """
    保留以下时间段的情景记忆：
    - 最近 7 天（完整细节）
    - 最近 30 天（摘要）
    - 更旧：仅当被语义记忆引用时
    """
    now = datetime.now()

    for episode in load_all_episodes():
        age_days = (now - episode.timestamp).days

        if age_days > 30:
            if not is_referenced_by_semantic(episode):
                archive_episode(episode)
        elif age_days > 7:
            summarize_episode(episode)
```

### 合并重复模式

```python
def merge_duplicate_semantics():
    """
    查找并合并语义相似的模式。
    """
    all_patterns = load_semantic_patterns()

    clusters = cluster_by_embedding_similarity(all_patterns, threshold=0.9)

    for cluster in clusters:
        if len(cluster) > 1:
            # 保留最高置信度，合并来源
            primary = max(cluster, key=lambda p: p.confidence)
            for other in cluster:
                if other != primary:
                    primary.source_episodes.extend(other.source_episodes)
                    primary.usage_count += other.usage_count
                    create_link(other, primary, "superseded_by")
            save_semantic(primary)
```

---

## 与 CONTINUITY.md 集成

CONTINUITY.md 是工作记忆 - 它引用但不重复长期记忆：

```markdown
## 相关记忆（自动检索）
- [sem-001] Express 处理器需要显式返回类型
- [ep-2026-01-05-012] 类似的端点实现成功
- [skill: api-implementation] 标准 API 实现流程

## 要避免的错误（来自学习）
- 不要忘记返回类型注解
- 在标记完成前运行契约测试
```
