# Track 管理器实施手册

本文件包含该技能引用的详细模式、检查清单和代码示例。

## 预检步骤

1. 验证 Conductor 已初始化：
   - 检查 `conductor/product.md` 是否存在
   - 检查 `conductor/tracks.md` 是否存在
   - 检查 `conductor/tracks/` 目录是否存在
   - 若缺失：显示错误并建议先运行 `/conductor:setup`

2. 确保归档目录存在（用于归档/恢复操作）：
   - 检查 `conductor/tracks/_archive/` 是否存在
   - 在执行归档操作时按需创建

## 模式检测

解析参数以确定操作模式：

| 参数                   | 模式         | 描述                                             |
| ---------------------- | ------------ | ------------------------------------------------------- |
| `--list [filter]`      | 列表         | 显示所有 track（可选：active、completed、archived）       |
| `--archive <id>`       | 归档         | 将已完成的 track 移至归档                                    |
| `--archive --bulk`     | 批量归档     | 多选已完成的 track                            |
| `--restore <id>`       | 恢复         | 将已归档的 track 恢复为活跃                              |
| `--delete <id>`        | 删除         | 永久移除一个 track                            |
| `--rename <old> <new>` | 重命名       | 更改 track ID                            |
| `--cleanup`            | 清理         | 检测并修复孤立产物                       |
| (无)                   | 交互式       | 菜单驱动的操作选择                         |

---

## 交互模式（无参数）

无参数调用时，显示主菜单：

### 1. 收集快速统计

读取 `conductor/tracks.md` 并扫描目录：

- 统计活跃 track（状态 `[ ]` 或 `[~]`）
- 统计已完成 track（状态 `[x]`，未归档）
- 统计已归档 track（位于 `_archive/` 目录）

### 2. 显示主菜单

```
================================================================================
                          TRACK MANAGER
================================================================================

What would you like to do?

1. List all tracks
2. Archive a completed track
3. Restore an archived track
4. Delete a track permanently
5. Rename a track
6. Cleanup orphaned artifacts
7. Exit

Quick stats:
- {N} active tracks
- {M} completed (ready to archive)
- {P} archived

Select option:
```

### 3. 处理选择

- 选项 1：执行列表模式
- 选项 2：执行归档模式（无参数）
- 选项 3：执行恢复模式（无参数）
- 选项 4：执行删除模式（无参数）
- 选项 5：执行重命名模式（无参数）
- 选项 6：执行清理模式
- 选项 7：退出并显示 "Track management cancelled."

---

## 列表模式（`--list`）

显示全面的 track 概览，支持可选过滤。

### 1. 数据采集

**针对活跃 track：**

- 读取 `conductor/tracks.md`
- 对每个状态为 `[ ]` 或 `[~]` 的 track：
  - 读取 `conductor/tracks/{trackId}/metadata.json` 获取类型、日期
  - 读取 `conductor/tracks/{trackId}/plan.md` 获取任务计数
  - 计算进度百分比

**针对已完成的 track：**

- 查找状态为 `[x]` 且不在 `_archive/` 中的 track
- 读取元数据获取完成日期

**针对已归档的 track：**

- 扫描 `conductor/tracks/_archive/` 目录
- 读取每个 `metadata.json` 的归档原因和日期

### 2. 输出格式

**完整列表（无过滤）：**

```
================================================================================
                          TRACK MANAGER
================================================================================

ACTIVE TRACKS ({count})
| Status | Track ID           | Type    | Progress    | Updated    |
|--------|-------------------|---------|-------------|------------|
| [~]    | dashboard_20250112| feature | 7/15 (47%)  | 2025-01-15 |
| [ ]    | nav-fix_20250114  | bug     | 0/4 (0%)    | 2025-01-14 |

COMPLETED TRACKS ({count})
| Track ID           | Type    | Completed  | Duration |
|-------------------|---------|------------|----------|
| auth_20250110     | feature | 2025-01-12 | 2 days   |

ARCHIVED TRACKS ({count})
| Track ID              | Type    | Reason     | Archived   |
|-----------------------|---------|------------|------------|
| old-feature_20241201  | feature | Superseded | 2025-01-05 |

================================================================================
Commands: /conductor:manage --archive | --restore | --delete | --rename | --cleanup
================================================================================
```

**过滤列表（`--list active`、`--list completed`、`--list archived`）：**

仅显示请求的区段，格式相同。

### 3. 空状态

**完全没有 track：**

```
================================================================================
                          TRACK MANAGER
================================================================================

No tracks found.

To create your first track: /conductor:new-track

================================================================================
```

**过滤条件下无 track：**

```
================================================================================
                          TRACK MANAGER
================================================================================

No {filter} tracks found.

================================================================================
```

---

## 归档模式（`--archive`）

将已完成的 track 移至归档目录。

### 带参数（`--archive <track-id>`）

#### 1. 验证 track

- 检查 track 是否存在于 `conductor/tracks/{track-id}/`
- 若未找到，显示错误并附可用 track：

  ```
  ERROR: Track not found: {track-id}

  Available tracks:
  - auth_20250110 (completed)
  - dashboard_20250112 (in progress)

  Usage: /conductor:manage --archive <track-id>
  ```

- 检查 track 未被归档（不在 `_archive/` 中）
- 若已归档：

  ```
  ERROR: Track '{track-id}' is already archived.

  Archived: {archived_at}
  Reason:   {archive_reason}
  Location: conductor/tracks/_archive/{track-id}/

  To restore: /conductor:manage --restore {track-id}
  ```

#### 2. 验证完成状态

读取 `conductor/tracks/{track-id}/metadata.json` 和 `plan.md`：

- 若状态不是 `completed` 或 `[x]`：

  ```
  Track '{track-id}' is not marked as complete.

  Current status: {status}
  Tasks: {completed}/{total} complete

  Options:
  1. Archive anyway (not recommended)
  2. Cancel and complete the track first
  3. View track status

  Select option:
  ```

- 若选择选项 1，发出警告后继续
- 若选择选项 2 或 3，退出或显示状态

#### 3. 提示输入归档原因

```
Why are you archiving this track?

1. Completed - Work finished successfully
2. Superseded - Replaced by another track
3. Abandoned - No longer needed
4. Other (specify)

Select reason:
```

若选择 "Other"，提示输入自定义原因。

#### 4. 显示确认信息

```
================================================================================
                          ARCHIVE CONFIRMATION
================================================================================

Track:    {track-id} - {title}
Type:     {type}
Status:   {status}
Tasks:    {completed}/{total} complete
Reason:   {reason}

Actions:
- Move conductor/tracks/{track-id}/ to conductor/tracks/_archive/{track-id}/
- Update conductor/tracks.md (move to Archived Tracks section)
- Update metadata.json with archive info
- Create git commit: chore(conductor): Archive track '{title}'

================================================================================

Type 'YES' to proceed, or anything else to cancel:
```

**关键：要求显式输入 'YES' 确认。**

#### 5. 执行归档

1. 若 `conductor/tracks/_archive/` 不存在则创建：

   ```bash
   mkdir -p conductor/tracks/_archive
   ```

2. 移动 track 目录：

   ```bash
   mv conductor/tracks/{track-id} conductor/tracks/_archive/
   ```

3. 更新 `conductor/tracks/_archive/{track-id}/metadata.json`：

   ```json
   {
     "archived": true,
     "archived_at": "ISO_TIMESTAMP",
     "archive_reason": "{reason}",
     "status": "archived"
   }
   ```

4. 更新 `conductor/tracks.md`：
   - 从 Active Tracks 或 Completed Tracks 区段移除条目
   - 在 Archived Tracks 区段以如下格式添加条目：
     ```markdown
     ### {track-id}: {title}

     **Reason:** {reason}
     **Archived:** YYYY-MM-DD
     **Folder:** ./tracks/\_archive/{track-id}/
     ```

5. Git 提交：
   ```bash
   git add conductor/tracks/_archive/{track-id} conductor/tracks.md
   git commit -m "chore(conductor): Archive track '{title}'"
   ```

#### 6. 成功输出

```
================================================================================
                          ARCHIVE COMPLETE
================================================================================

Track archived: {track-id} - {title}

Location:  conductor/tracks/_archive/{track-id}/
Reason:    {reason}
Commit:    {sha}

To restore: /conductor:manage --restore {track-id}
To list:    /conductor:manage --list archived

================================================================================
```

### 不带参数（`--archive`）

#### 1. 查找可归档的 track

扫描尚未归档的已完成 track：

- `tracks.md` 中状态为 `[x]`
- 不在 `_archive/` 目录中

#### 2. 显示选择菜单

```
================================================================================
                          ARCHIVE TRACKS
================================================================================

Completed tracks available for archiving:

1. [x] auth_20250110 - User Authentication (completed 2025-01-12)
2. [x] setup-ci_20250108 - CI Pipeline Setup (completed 2025-01-09)

Already archived: {N} tracks

--------------------------------------------------------------------------------

Options:
1-{N}. Select a track to archive
A.     Archive all completed tracks
C.     Cancel

Select option:
```

- 若为数字，进入单个归档流程
- 若为 'A'，进入批量归档
- 若为 'C'，退出

#### 3. 无可归档 track

```
================================================================================
                          ARCHIVE TRACKS
================================================================================

No completed tracks available for archiving.

Current tracks:
- [~] nav-fix_20250114 - In progress
- [ ] api-v2_20250115 - Pending

Already archived: {N} tracks (use --list archived to view)

================================================================================
```

### 批量归档（`--archive --bulk`）

#### 1. 显示多选界面

```
================================================================================
                       BULK ARCHIVE SELECTION
================================================================================

Select tracks to archive (comma-separated numbers, or 'all'):

Completed Tracks:
[ ] 1. auth_20250110 - User Authentication (completed 2025-01-12)
[ ] 2. setup-ci_20250108 - CI Pipeline Setup (completed 2025-01-09)
[ ] 3. docs-update_20250105 - Documentation Update (completed 2025-01-06)

Enter selection (e.g., "1,3" or "all"):
```

#### 2. 确认选择

```
================================================================================
                       BULK ARCHIVE CONFIRMATION
================================================================================

Tracks to archive:

1. auth_20250110 - User Authentication
2. setup-ci_20250108 - CI Pipeline Setup

Archive reason for all: Completed

Actions:
- Move 2 track directories to conductor/tracks/_archive/
- Update conductor/tracks.md
- Create git commit: chore(conductor): Archive 2 completed tracks

================================================================================

Type 'YES' to proceed, or anything else to cancel:
```

#### 3. 执行批量归档

- 按顺序归档每个 track
- 为全部 track 创建一个 git 提交：
  ```bash
  git add conductor/tracks/_archive/ conductor/tracks.md
  git commit -m "chore(conductor): Archive {N} completed tracks"
  ```

---

## 恢复模式（`--restore`）

将已归档的 track 恢复到活跃状态。

### 带参数（`--restore <track-id>`）

#### 1. 验证 track

- 检查 track 是否存在于 `conductor/tracks/_archive/{track-id}/`
- 若未找到：

  ```
  ERROR: Archived track not found: {track-id}

  Available archived tracks:
  - old-feature_20241201 (archived 2025-01-05)

  Usage: /conductor:manage --restore <track-id>
  ```

#### 2. 检查冲突

- 确认 `conductor/tracks/` 中不存在同 ID 的活跃 track
- 若有冲突：

  ```
  ERROR: Cannot restore '{track-id}' - a track with this ID already exists.

  Active track: conductor/tracks/{track-id}/

  Options:
  1. Delete existing track first
  2. Restore with different ID (will prompt for new ID)
  3. Cancel

  Select option:
  ```

#### 3. 显示确认信息

```
================================================================================
                          RESTORE CONFIRMATION
================================================================================

Restoring archived track:

Track:    {track-id} - {title}
Type:     {type}
Archived: {archived_at}
Reason:   {archive_reason}

Actions:
- Move conductor/tracks/_archive/{track-id}/ to conductor/tracks/{track-id}/
- Update conductor/tracks.md (move to Completed Tracks section)
- Update metadata.json
- Create git commit: chore(conductor): Restore track '{title}'

Note: Track will be restored with status 'completed'. Use /conductor:implement
to resume work if needed.

================================================================================

Type 'YES' to proceed, or anything else to cancel:
```

#### 4. 执行恢复

1. 移动 track 目录：

   ```bash
   mv conductor/tracks/_archive/{track-id} conductor/tracks/
   ```

2. 更新 `conductor/tracks/{track-id}/metadata.json`：

   ```json
   {
     "archived": false,
     "restored_at": "ISO_TIMESTAMP",
     "status": "completed"
   }
   ```

3. 更新 `conductor/tracks.md`：
   - 从 Archived Tracks 区段移除条目
   - 在 Completed Tracks 区段添加条目

4. Git 提交：
   ```bash
   git add conductor/tracks/{track-id} conductor/tracks.md
   git commit -m "chore(conductor): Restore track '{title}'"
   ```

#### 5. 成功输出

```
================================================================================
                          RESTORE COMPLETE
================================================================================

Track restored: {track-id} - {title}

Location:  conductor/tracks/{track-id}/
Status:    completed

Next steps:
- Run /conductor:status {track-id} to see track details
- Run /conductor:implement {track-id} to resume work (if needed)

================================================================================
```

### 不带参数（`--restore`）

显示已归档 track 的菜单供选择：

```
================================================================================
                          RESTORE TRACKS
================================================================================

Archived tracks available for restoration:

1. old-feature_20241201 - Old Feature (archived 2025-01-05, reason: Superseded)
2. cleanup-api_20241215 - API Cleanup (archived 2025-01-10, reason: Completed)

--------------------------------------------------------------------------------

Options:
1-{N}. Select a track to restore
C.     Cancel

Select option:
```

---

## 删除模式（`--delete`）

永久删除 track，并附带安全确认。

### 带参数（`--delete <track-id>`）

#### 1. 查找 track

在以下位置搜索 track：

1. `conductor/tracks/{track-id}/`（活跃/已完成）
2. `conductor/tracks/_archive/{track-id}/`（已归档）

若未找到：

```
ERROR: Track not found: {track-id}

Available tracks:
Active:
- dashboard_20250112

Archived:
- old-feature_20241201

Usage: /conductor:manage --delete <track-id>
```

#### 2. 检查进行中状态

若 track 状态为 `[~]`（进行中）：

```
================================================================================
                          !! WARNING !!
================================================================================

Track '{track-id}' is currently IN PROGRESS.

Current task: Task 2.3 - {description}
Progress:     7/15 tasks (47%)

Deleting an in-progress track may result in lost work.

Options:
1. Delete anyway (use --force to skip this warning)
2. Archive instead (recommended)
3. Cancel

Select option:
```

未使用 `--force` 标志时，要求显式选择。

#### 3. 显示完整警告

```
================================================================================
                     !! PERMANENT DELETION WARNING !!
================================================================================

Track:    {track-id} - {title}
Type:     {type}
Status:   {status}
Location: conductor/tracks/{track-id}/ (or _archive/)
Created:  {created_date}
Files:    {count} (spec.md, plan.md, metadata.json, index.md)
Commits:  {count} related commits (will NOT be deleted)

This action CANNOT be undone. The track directory and all contents
will be permanently removed.

Consider archiving instead: /conductor:manage --archive {track-id}

================================================================================

Type 'DELETE' to permanently remove, or anything else to cancel:
```

**关键：要求完全输入 'DELETE' 字符串，而不是 'yes' 或 'y'。**

#### 4. 执行删除

1. 移除 track 目录：

   ```bash
   rm -rf conductor/tracks/{track-id}
   # or
   rm -rf conductor/tracks/_archive/{track-id}
   ```

2. 更新 `conductor/tracks.md`：
   - 从相应区段（Active、Completed 或 Archived）移除条目

3. Git 提交：
   ```bash
   git add conductor/tracks.md
   git commit -m "chore(conductor): Delete track '{title}'"
   ```

注：git 提交会记录删除操作，但不会删除历史提交。

#### 5. 成功输出

```
================================================================================
                          DELETE COMPLETE
================================================================================

Track permanently deleted: {track-id} - {title}

Note: Git history still contains commits referencing this track.
      The track directory and registry entry have been removed.

================================================================================
```

### 不带参数（`--delete`）

显示所有 track 的菜单供选择：

```
================================================================================
                          DELETE TRACKS
================================================================================

!! This will PERMANENTLY delete a track !!

Select a track to delete:

Active/Completed:
1. [ ] nav-fix_20250114 - Navigation Bug Fix
2. [x] auth_20250110 - User Authentication

Archived:
3. old-feature_20241201 - Old Feature

--------------------------------------------------------------------------------

Options:
1-{N}. Select a track to delete
C.     Cancel

Select option:
```

---

## 重命名模式（`--rename`）

更改 track ID 并完整更新引用。

### 带参数（`--rename <old-id> <new-id>`）

#### 1. 验证旧 track 存在

检查 track 是否存在于：

- `conductor/tracks/{old-id}/`
- `conductor/tracks/_archive/{old-id}/`

若未找到：

```
ERROR: Track not found: {old-id}

Available tracks:
- auth_20250110
- dashboard_20250112

Usage: /conductor:manage --rename <old-id> <new-id>
```

#### 2. 验证新 ID

**检查格式**（必须匹配 `{shortname}_{YYYYMMDD}`）：

```
ERROR: Invalid track ID format: {new-id}

Track IDs must follow the pattern: {shortname}_{YYYYMMDD}
Examples:
- user-auth_20250115
- fix-login_20250114
- api-v2_20250110
```

**检查无冲突：**

```
ERROR: Track '{new-id}' already exists.

Choose a different ID or delete the existing track first.
```

#### 3. 显示确认信息

```
================================================================================
                          RENAME TRACK
================================================================================

Current:  {old-id} - {title}
New ID:   {new-id}

Changes:
- Rename conductor/tracks/{old-id}/ to {new-id}/
- Update tracks.md entry
- Update metadata.json id field
- Update plan.md track ID header

Note: Git commit history will retain original track ID references.
      Related commits cannot be renamed.

================================================================================

Type 'YES' to proceed, or anything else to cancel:
```

#### 4. 执行重命名

1. 重命名目录：

   ```bash
   mv conductor/tracks/{old-id} conductor/tracks/{new-id}
   # or for archived:
   mv conductor/tracks/_archive/{old-id} conductor/tracks/_archive/{new-id}
   ```

2. 更新 `conductor/tracks/{new-id}/metadata.json`：

   ```json
   {
     "id": "{new-id}",
     "previous_ids": ["{old-id}"],
     "renamed_at": "ISO_TIMESTAMP"
   }
   ```

   若 `previous_ids` 已存在，则追加旧 ID。

3. 更新 `conductor/tracks/{new-id}/plan.md`：
   - 更改 header 行中的 track ID

4. 更新 `conductor/tracks.md`：
   - 更新相应区段中的 track ID
   - 更新文件夹链接路径

5. Git 提交：
   ```bash
   git add conductor/tracks/{new-id} conductor/tracks.md
   git commit -m "chore(conductor): Rename track '{old-id}' to '{new-id}'"
   ```

#### 5. 成功输出

```
================================================================================
                          RENAME COMPLETE
================================================================================

Track renamed: {old-id} → {new-id}

New location: conductor/tracks/{new-id}/

Note: Historical git commits still reference '{old-id}'.

================================================================================
```

### 不带参数（`--rename`）

交互模式：

```
================================================================================
                          RENAME TRACK
================================================================================

Select a track to rename:

1. auth_20250110 - User Authentication
2. dashboard_20250112 - Dashboard Feature
3. nav-fix_20250114 - Navigation Bug Fix

--------------------------------------------------------------------------------

Options:
1-{N}. Select a track
C.     Cancel

Select option:
```

选择后：

```
Enter new track ID for '{old-id}':

Format: {shortname}_{YYYYMMDD}
Current: {old-id}

New ID:
```

---

## 清理模式（`--cleanup`）

检测并修复孤立的 track 产物。

### 1. 扫描问题

**孤立目录：**

- 扫描 `conductor/tracks/` 中的目录
- 逐一检查其是否在 tracks.md 中
- 标记未在注册表中的目录

**注册表孤立项：**

- 解析 tracks.md 中的所有 track 条目
- 检查每个条目是否都有对应目录
- 标记没有目录的条目

**不完整 track：**

- 对每个 track 目录，验证必需文件是否存在：
  - `spec.md`
  - `plan.md`
  - `metadata.json`
- 标记缺少必需文件的 track

**陈旧的进行中 track：**

- 查找状态为 `[~]` 的 track
- 检查 `metadata.json` 中的 `updated` 时间戳
- 若超过 7 天未触碰则标记

### 2. 显示结果

```
================================================================================
                          TRACK CLEANUP
================================================================================

Scanning for issues...

ORPHANED DIRECTORIES (not in tracks.md):
  1. conductor/tracks/test-feature_20241201/
  2. conductor/tracks/experiment_20241220/

REGISTRY ORPHANS (no matching folder):
  3. broken-track_20250101 (listed in tracks.md)

INCOMPLETE TRACKS (missing files):
  4. partial_20250105/ - missing: metadata.json, index.md

STALE IN-PROGRESS (untouched >7 days):
  5. old-work_20250101 - last updated: 2025-01-02

================================================================================

Found {N} issues.

Actions:
1. Add orphaned directories to tracks.md
2. Remove registry orphans from tracks.md
3. Create missing files from templates
4. Archive stale tracks
A. Fix all issues automatically
S. Skip and review manually
C. Cancel

Select action:
```

### 3. 处理无问题情况

```
================================================================================
                          TRACK CLEANUP
================================================================================

Scanning for issues...

No issues found.

All tracks are properly registered and complete.

================================================================================
```

### 4. 执行修复

**针对孤立目录（操作 1）：**

```
Adding orphaned directories to tracks.md...

For each directory:
- Read metadata.json if exists for track info
- If no metadata, prompt for track details:

  Found: conductor/tracks/test-feature_20241201/

  Enter track title (or 'skip' to ignore):
  Enter track type (feature/bug/chore/refactor):

- Add entry to appropriate section in tracks.md
- Create metadata.json if missing
```

**针对注册表孤立项（操作 2）：**

```
Removing registry orphans from tracks.md...

Removed entries:
- broken-track_20250101

Note: No files were deleted, only tracks.md was updated.
```

**针对不完整 track（操作 3）：**

```
Creating missing files from templates...

partial_20250105/:
- Created metadata.json from template
- Created index.md from template

Note: You may need to populate these files with actual content.
```

**针对陈旧的进行中 track（操作 4）：**

```
Archiving stale tracks...

old-work_20250101:
- Archived with reason: Stale (untouched since 2025-01-02)
```

**针对所有问题（操作 A）：**

按顺序执行所有适用的修复，然后：

```bash
git add conductor/
git commit -m "chore(conductor): Clean up {N} orphaned track artifacts"
```

### 5. 完成输出

```
================================================================================
                          CLEANUP COMPLETE
================================================================================

Fixed {N} issues:
- Added {X} orphaned directories to tracks.md
- Removed {Y} registry orphans
- Created missing files for {Z} incomplete tracks
- Archived {W} stale tracks

Commit: {sha}

================================================================================
```

---

## 错误处理

### Git 操作失败

```
GIT ERROR: {error message}

The operation partially completed:
- Directory moved: Yes/No
- tracks.md updated: Yes/No
- Commit created: No

You may need to manually:
1. Complete the git commit
2. Restore files from their current locations

Current state:
- Track location: {path}
- tracks.md: {status}

To retry the commit:
  git add conductor/tracks.md conductor/tracks/{track-id}
  git commit -m "{intended message}"
```

### 文件系统错误

```
ERROR: Failed to {operation}: {error}

Possible causes:
- Permission denied
- Disk full
- File in use

No changes were made. Please resolve the issue and try again.
```

### 无效参数

```
ERROR: Invalid argument: {argument}

Usage: /conductor:manage [--archive | --restore | --delete | --rename | --list | --cleanup]

Examples:
  /conductor:manage                     # Interactive mode
  /conductor:manage --list              # List all tracks
  /conductor:manage --list archived     # List archived tracks only
  /conductor:manage --archive track-id  # Archive specific track
  /conductor:manage --restore track-id  # Restore archived track
  /conductor:manage --delete track-id   # Delete track permanently
  /conductor:manage --rename old new    # Rename track ID
  /conductor:manage --cleanup           # Fix orphaned artifacts
```

---

## 关键规则

1. **任何操作前务必验证 track 存在**
2. **破坏性操作需显式确认**：
   - 归档、恢复、重命名需输入 'YES'
   - 永久删除需输入 'DELETE'
3. **遇错即停** - 不要尝试在失败后继续
4. **更新 tracks.md** - 保持注册表与文件系统同步
5. **提交变更** - 创建 git 提交以保证可追溯
6. **保留历史** - 永远不要修改或删除 git 提交
7. **进行中警告** - 修改活跃工作时需格外谨慎
8. **提供替代方案** - 在删除前建议归档
