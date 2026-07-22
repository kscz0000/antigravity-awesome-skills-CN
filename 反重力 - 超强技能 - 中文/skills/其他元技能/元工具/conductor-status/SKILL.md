---
name: conductor-status
description: "显示项目状态、活跃轨道和下一步操作"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Conductor Status

显示 Conductor 项目的当前状态，包括整体进度、活跃轨道和下一步操作。

## 使用此技能的时机

- 处理 conductor status 相关任务或工作流时
- 需要 conductor status 相关的指导、最佳实践或检查清单时

## 不使用此技能的时机

- 任务与 conductor status 无关时
- 需要此范围之外的其他领域或工具时

## 操作说明

- 明确目标、约束条件和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 预检查

1. 验证 Conductor 已初始化：
   - 检查 `conductor/product.md` 是否存在
   - 检查 `conductor/tracks.md` 是否存在
   - 如缺失：显示错误并建议先运行 `/conductor:setup`

2. 检查是否存在轨道：
   - 读取 `conductor/tracks.md`
   - 如无已注册轨道：显示设置完成消息并建议创建第一个轨道

## 数据收集

### 1. 项目信息

读取 `conductor/product.md` 并提取：

- 项目名称
- 项目描述

### 2. 轨道概览

读取 `conductor/tracks.md` 并解析：

- 轨道总数
- 已完成轨道（标记为 `[x]`）
- 进行中轨道（标记为 `[~]`）
- 待处理轨道（标记为 `[ ]`）

### 3. 详细轨道分析

对于 `conductor/tracks/` 中的每个轨道：

读取 `conductor/tracks/{trackId}/plan.md`：

- 统计总任务数（匹配 `- [x]`、`- [~]`、`- [ ]` 且带有 Task 前缀的行）
- 统计已完成任务（`[x]`）
- 统计进行中任务（`[~]`）
- 统计待处理任务（`[ ]`）
- 识别当前阶段（第一个有未完成任务的阶段）
- 识别下一个待处理任务

读取 `conductor/tracks/{trackId}/metadata.json`：

- 轨道类型（feature、bug、chore、refactor）
- 创建日期
- 最后更新日期
- 状态

读取 `conductor/tracks/{trackId}/spec.md`：

- 检查是否有记录的阻塞项或依赖项

### 4. 阻塞项检测

扫描潜在阻塞项：

- 带有 `BLOCKED:` 前缀标记的任务
- 依赖于未完成轨道的任务
- 验证失败的任务

## 输出格式

### 完整项目状态（无参数）

```
================================================================================
                        PROJECT STATUS: {Project Name}
================================================================================
Last Updated: {current timestamp}

--------------------------------------------------------------------------------
                              OVERALL PROGRESS
--------------------------------------------------------------------------------

Tracks:     {completed}/{total} completed ({percentage}%)
Tasks:      {completed}/{total} completed ({percentage}%)

Progress:   [##########..........] {percentage}%

--------------------------------------------------------------------------------
                              TRACK SUMMARY
--------------------------------------------------------------------------------

| Status | Track ID          | Type    | Tasks      | Last Updated |
|--------|-------------------|---------|------------|--------------|
| [x]    | auth_20250110     | feature | 12/12 (100%)| 2025-01-12  |
| [~]    | dashboard_20250112| feature | 7/15 (47%) | 2025-01-15  |
| [ ]    | nav-fix_20250114  | bug     | 0/4 (0%)   | 2025-01-14  |

--------------------------------------------------------------------------------
                              CURRENT FOCUS
--------------------------------------------------------------------------------

Active Track:  dashboard_20250112 - Dashboard Feature
Current Phase: Phase 2: Core Components
Current Task:  [~] Task 2.3: Implement chart rendering

Progress in Phase:
  - [x] Task 2.1: Create dashboard layout
  - [x] Task 2.2: Add data fetching hooks
  - [~] Task 2.3: Implement chart rendering
  - [ ] Task 2.4: Add filter controls

--------------------------------------------------------------------------------
                              NEXT ACTIONS
--------------------------------------------------------------------------------

1. Complete: Task 2.3 - Implement chart rendering (dashboard_20250112)
2. Then: Task 2.4 - Add filter controls (dashboard_20250112)
3. After Phase 2: Phase verification checkpoint

--------------------------------------------------------------------------------
                               BLOCKERS
--------------------------------------------------------------------------------

{If blockers found:}
! BLOCKED: Task 3.1 in dashboard_20250112 depends on api_20250111 (incomplete)

{If no blockers:}
No blockers identified.

================================================================================
Commands: /conductor:implement {trackId} | /conductor:new-track | /conductor:revert
================================================================================
```

### 单个轨道状态（带 track-id 参数）

```
================================================================================
                    TRACK STATUS: {Track Title}
================================================================================
Track ID:    {trackId}
Type:        {feature|bug|chore|refactor}
Status:      {Pending|In Progress|Complete}
Created:     {date}
Updated:     {date}

--------------------------------------------------------------------------------
                              SPECIFICATION
--------------------------------------------------------------------------------

Summary: {brief summary from spec.md}

Acceptance Criteria:
  - [x] {Criterion 1}
  - [ ] {Criterion 2}
  - [ ] {Criterion 3}

--------------------------------------------------------------------------------
                              IMPLEMENTATION
--------------------------------------------------------------------------------

Overall:    {completed}/{total} tasks ({percentage}%)
Progress:   [##########..........] {percentage}%

## Phase 1: {Phase Name} [COMPLETE]
  - [x] Task 1.1: {description}
  - [x] Task 1.2: {description}
  - [x] Verification: {description}

## Phase 2: {Phase Name} [IN PROGRESS]
  - [x] Task 2.1: {description}
  - [~] Task 2.2: {description}  <-- CURRENT
  - [ ] Task 2.3: {description}
  - [ ] Verification: {description}

## Phase 3: {Phase Name} [PENDING]
  - [ ] Task 3.1: {description}
  - [ ] Task 3.2: {description}
  - [ ] Verification: {description}

--------------------------------------------------------------------------------
                              GIT HISTORY
--------------------------------------------------------------------------------

Related Commits:
  abc1234 - feat: add login form ({trackId})
  def5678 - feat: add password validation ({trackId})
  ghi9012 - chore: mark task 1.2 complete ({trackId})

--------------------------------------------------------------------------------
                              NEXT STEPS
--------------------------------------------------------------------------------

1. Current: Task 2.2 - {description}
2. Next: Task 2.3 - {description}
3. Phase 2 verification pending

================================================================================
Commands: /conductor:implement {trackId} | /conductor:revert {trackId}
================================================================================
```

## 状态标记图例

如有帮助可在底部显示：

```
Legend:
  [x] = Complete
  [~] = In Progress
  [ ] = Pending
  [!] = Blocked
```

## 错误状态

### 未找到轨道

```
================================================================================
                        PROJECT STATUS: {Project Name}
================================================================================

Conductor is set up but no tracks have been created yet.

To get started:
  /conductor:new-track "your feature description"

================================================================================
```

### Conductor 未初始化

```
ERROR: Conductor not initialized

Could not find conductor/product.md

Run /conductor:setup to initialize Conductor for this project.
```

### 轨道未找到（带参数）

```
ERROR: Track not found: {argument}

Available tracks:
  - auth_20250115
  - dashboard_20250112
  - nav-fix_20250114

Usage: /conductor:status [track-id]
```

## 计算逻辑

### 任务计数

```
For each plan.md:
  - Complete: count lines matching /^- \[x\] Task/
  - In Progress: count lines matching /^- \[~\] Task/
  - Pending: count lines matching /^- \[ \] Task/
  - Total: Complete + In Progress + Pending
```

### 阶段检测

```
Current phase = first phase header followed by any incomplete task ([ ] or [~])
```

### 进度条

```
filled = floor((completed / total) * 20)
empty = 20 - filled
bar = "[" + "#".repeat(filled) + ".".repeat(empty) + "]"
```

## 快速模式

如使用 `--quick` 或 `-q` 调用：

```
{Project Name}: {completed}/{total} tasks ({percentage}%)
Active: {trackId} - Task {X.Y}
```

## JSON 输出

如使用 `--json` 调用：

```json
{
  "project": "{name}",
  "timestamp": "ISO_TIMESTAMP",
  "tracks": {
    "total": N,
    "completed": X,
    "in_progress": Y,
    "pending": Z
  },
  "tasks": {
    "total": M,
    "completed": A,
    "in_progress": B,
    "pending": C
  },
  "current": {
    "track": "{trackId}",
    "phase": N,
    "task": "{X.Y}"
  },
  "blockers": []
}
```

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 输出不能替代特定环境的验证、测试或专家评审。
- 如缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
