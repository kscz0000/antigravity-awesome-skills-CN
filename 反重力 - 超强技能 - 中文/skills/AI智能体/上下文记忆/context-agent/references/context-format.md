# 格式规范 — Context Agent

## session-NNN.md

每个会话文件遵循此格式：

```markdown
# 会话 NNN — YYYY-MM-DD
**Slug：** session-slug | **时长：** ~Xmin | **模型：** claude-opus-4-6

## 话题
- 讨论的主要议题
- 其他议题

## 决策
- 已做出的决策及理由

## 已完成任务
- [x] 已完成的任务

## 待办任务
- [ ] 遗留任务（优先级：高|中|低）

## 修改的文件
- `path/to/file.py` — edit|write

## 发现
- 重要的技术洞察

## 已解决的错误
- 遇到的错误描述

## 未解决的问题
- 尚未回答的问题

## 技术债
- 识别出的技术债项

## 指标
- Input tokens: N
- Output tokens: N
- Cache tokens: N
- 消息数: N
- Tool calls: N

---
*上一会话：[session-NNN-1](session-NNN-1.md)*
```

## ACTIVE_CONTEXT.md

最多 150 行。格式如下：

```markdown
# 活跃上下文 — 更新于 YYYY-MM-DD HH:MM

## 活跃项目
| 项目 | 状态 | 上一会话 | 下一步 |
|------|------|----------|--------|
| 名称 | 活跃 | session-NNN | 动作 |

## 待办任务
### 高优先级
- [ ] 任务（来自 session-NNN）
### 中优先级
- [ ] 任务
### 低优先级
- [ ] 任务

## 近期决策
- [session-NNN] 已做出的决策

## 当前阻塞项
- 阻塞项或"无"

## 已确立约定
- 采用的规范

## 最近会话
- session-NNN: 话题 1、话题 2
```

## PROJECT_REGISTRY.md

```markdown
# 项目注册表 — 更新于 YYYY-MM-DD HH:MM

| 项目 | 状态 | 最近交互 | 下一步动作 |
|------|------|----------|------------|
| 名称 | 活跃 | YYYY-MM-DD (session-NNN) | 动作1; 动作2 |
```

## MEMORY.md

`ACTIVE_CONTEXT.md` 的副本，附带头部说明：

```markdown
<!-- 由 context-agent 自动生成。详情请运行：
python C:\Users\renat\skills\context-agent\scripts\context_manager.py load -->

[与 ACTIVE_CONTEXT.md 内容一致]
```

## context.db (SQLite FTS5)

用于全文搜索的虚拟表：

```sql
CREATE VIRTUAL TABLE session_search USING fts5(
    session_number,    -- "001", "002", etc.
    date,              -- "2026-02-25"
    section,           -- "topics", "decisions", etc.
    content,           -- 区段全文
    tokenize='unicode61'
);
```
