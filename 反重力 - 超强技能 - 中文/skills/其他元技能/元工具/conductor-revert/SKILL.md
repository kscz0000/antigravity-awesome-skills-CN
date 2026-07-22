---
name: conductor-revert
description: "按逻辑工作单元（track、phase 或 task）进行 Git 感知的撤销操作"
risk: critical
source: community
date_added: "2026-02-27"
---

# 回滚 Track

按逻辑工作单元回滚变更，具备完整的 git 感知能力。支持回滚整个 track、特定 phase 或单个 task。

## 使用此技能的场景

- 处理回滚 track 任务或工作流
- 需要回滚 track 的指导、最佳实践或检查清单

## 不使用此技能的场景

- 任务与回滚 track 无关
- 需要此范围之外的其他领域或工具

## 指令

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 预检检查

1. 验证 Conductor 已初始化：
   - 检查 `conductor/tracks.md` 是否存在
   - 若缺失：显示错误并建议先运行 `/conductor:setup`

2. 验证 git 仓库：
   - 运行 `git status` 确认 git 仓库
   - 检查是否有未提交的变更
   - 若存在未提交的变更：

     ```
     WARNING: Uncommitted changes detected

     Files with changes:
     {list of files}

     Options:
     1. Stash changes and continue
     2. Commit changes first
     3. Cancel revert
     ```

3. 验证 git 状态足够干净以执行回滚：
   - 无正在进行的合并
   - 无正在进行的变基
   - 若发现问题：停止并说明解决步骤

## 目标选择

### 若提供了参数：

解析参数格式：

**完整 track：** `{trackId}`

- 示例：`auth_20250115`
- 回滚整个 track 的所有提交

**特定 phase：** `{trackId}:phase{N}`

- 示例：`auth_20250115:phase2`
- 回滚 phase N 及其所有后续 phase 的提交

**特定 task：** `{trackId}:task{X.Y}`

- 示例：`auth_20250115:task2.3`
- 仅回滚 task X.Y 的提交

### 若无参数：

显示引导选择菜单：

```
What would you like to revert?

Currently In Progress:
1. [~] Task 2.3 in dashboard_20250112 (most recent)

Recently Completed:
2. [x] Task 2.2 in dashboard_20250112 (1 hour ago)
3. [x] Phase 1 in dashboard_20250112 (3 hours ago)
4. [x] Full track: auth_20250115 (yesterday)

Options:
5. Enter specific reference (track:phase or track:task)
6. Cancel

Select option:
```

## 提交发现

### Task 回滚

1. 在 git log 中搜索特定 task 的提交：

   ```bash
   git log --oneline --grep="{trackId}" --grep="Task {X.Y}" --all-match
   ```

2. 同时查找 plan.md 更新提交：

   ```bash
   git log --oneline --grep="mark task {X.Y} complete" --grep="{trackId}" --all-match
   ```

3. 收集所有匹配的提交 SHA

### Phase 回滚

1. 通过读取 plan.md 确定 phase 的 task 范围
2. 搜索该 phase 中所有 task 的提交：

   ```bash
   git log --oneline --grep="{trackId}" | grep -E "Task {N}\.[0-9]"
   ```

3. 查找 phase 验证提交（若存在）
4. 查找 phase task 的所有 plan.md 更新提交
5. 按时间顺序收集所有匹配的提交 SHA

### 完整 Track 回滚

1. 查找所有提及该 track 的提交：

   ```bash
   git log --oneline --grep="{trackId}"
   ```

2. 查找 track 创建提交：

   ```bash
   git log --oneline -- "conductor/tracks/{trackId}/"
   ```

3. 按时间顺序收集所有匹配的提交 SHA

## 执行计划展示

在执行任何回滚操作前，展示完整计划：

```
================================================================================
                           REVERT EXECUTION PLAN
================================================================================

Target: {description of what's being reverted}

Commits to revert (in reverse chronological order):
  1. abc1234 - feat: add chart rendering (dashboard_20250112)
  2. def5678 - chore: mark task 2.3 complete (dashboard_20250112)
  3. ghi9012 - feat: add data hooks (dashboard_20250112)
  4. jkl3456 - chore: mark task 2.2 complete (dashboard_20250112)

Files that will be affected:
  - src/components/Dashboard.tsx (modified)
  - src/hooks/useData.ts (will be deleted - was created in these commits)
  - conductor/tracks/dashboard_20250112/plan.md (modified)

Plan updates:
  - Task 2.2: [x] -> [ ]
  - Task 2.3: [~] -> [ ]

================================================================================
                              !! WARNING !!
================================================================================

This operation will:
- Create {N} revert commits
- Modify {M} files
- Reset {P} tasks to pending status

This CANNOT be easily undone without manual intervention.

================================================================================

Type 'YES' to proceed, or anything else to cancel:
```

**关键：必须要求显式的 'YES' 确认。不接受 'y'、'yes' 或回车。**

## 回滚执行

按逆时间顺序执行回滚（最新的优先）：

```
Executing revert plan...

[1/4] Reverting abc1234...
      git revert --no-edit abc1234
      ✓ Success

[2/4] Reverting def5678...
      git revert --no-edit def5678
      ✓ Success

[3/4] Reverting ghi9012...
      git revert --no-edit ghi9012
      ✓ Success

[4/4] Reverting jkl3456...
      git revert --no-edit jkl3456
      ✓ Success
```

### 合并冲突处理

若任何回滚产生合并冲突：

```
================================================================================
                           MERGE CONFLICT DETECTED
================================================================================

Conflict occurred while reverting: {sha} - {message}

Conflicted files:
  - src/components/Dashboard.tsx

Options:
1. Show conflict details
2. Abort revert sequence (keeps completed reverts)
3. Open manual resolution guide

IMPORTANT: Reverts 1-{N} have been completed. You may need to manually
resolve this conflict before continuing or fully undo the revert sequence.

Select option:
```

**遇到任何冲突立即停止。不要尝试自动解决。**

## Plan.md 更新

成功执行 git 回滚后，更新 plan.md：

1. 读取当前 plan.md
2. 对于每个被回滚的 task，更改标记：
   - `[x]` -> `[ ]`
   - `[~]` -> `[ ]`
3. 写入更新后的 plan.md
4. 更新 metadata.json：
   - 递减 `tasks.completed`
   - 按需更新 `status`
   - 更新 `updated` 时间戳

**不要提交 plan.md 变更** — 它们是回滚操作的一部分

## Track 状态更新

### 若回滚整个 track：

- 在 tracks.md 中：将 `[x]` 或 `[~]` 改为 `[ ]`
- 考虑提供完全删除 track 目录的选项

### 若回滚至未完成状态：

- 在 tracks.md 中：若部分完成则标记为 `[~]`，若完全回滚则标记为 `[ ]`

## 验证

回滚完成后：

```
================================================================================
                           REVERT COMPLETE
================================================================================

Summary:
  - Reverted {N} commits
  - Reset {P} tasks to pending
  - {M} files affected

Git log now shows:
  {recent commit history}

Plan.md status:
  - Task 2.2: [ ] Pending
  - Task 2.3: [ ] Pending

================================================================================

Verify the revert was successful:
  1. Run tests: {test command}
  2. Check application: {relevant check}

If issues are found, you may need to:
  - Fix conflicts manually
  - Re-implement the reverted tasks
  - Use 'git revert HEAD~{N}..HEAD' to undo the reverts

================================================================================
```

## 安全规则

1. **绝不使用 `git reset --hard`** — 只使用 `git revert`
2. **绝不使用 `git push --force`** — 只使用安全的 push 操作
3. **绝不自动解决冲突** — 总是停止等待人工干预
4. **总是展示完整计划** — 用户必须看到将要发生的具体操作
5. **要求显式的 'YES'** — 不是 'y'，不是回车，只能是 'YES'
6. **遇到任何错误立即停止** — 不要尝试在失败后继续
7. **保留历史** — 回滚提交优于重写历史

## 边缘情况

### Track 从未提交

```
No commits found for track: {trackId}

The track exists but has no associated commits. This may mean:
- Implementation never started
- Commits used different format

Options:
1. Delete track directory only
2. Cancel
```

### 提交已被回滚

```
Some commits appear to already be reverted:
  - abc1234 was reverted by xyz9876

Options:
1. Skip already-reverted commits
2. Cancel and investigate
```

### 已推送到远程

```
WARNING: Some commits have been pushed to remote

Commits on remote:
  - abc1234 (origin/main)
  - def5678 (origin/main)

Reverting will create new revert commits that you'll need to push.
This is the safe approach (no force push required).

Continue with revert? (YES/no):
```

## 撤销回滚

若用户需要撤销回滚操作本身：

```
To undo this revert operation:

  git revert HEAD~{N}..HEAD

This will create new commits that restore the reverted changes.

Alternatively, if not yet pushed:
  git reset --soft HEAD~{N}
  git checkout -- .

(Use with caution - this discards the revert commits)
```

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 若缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
