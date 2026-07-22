---
name: conductor-implement
description: "按照 TDD 工作流执行轨道实现计划中的任务"
risk: critical
source: community
date_added: "2026-02-27"
---

# 实现轨道

执行轨道实现计划中的任务，遵循 `conductor/workflow.md` 中定义的工作流规则。

## 使用此技能的场景

- 处理实现轨道任务或工作流
- 需要实现轨道的指导、最佳实践或检查清单

## 不使用此技能的场景

- 任务与实现轨道无关
- 需要此范围之外的其他领域或工具

## 指导说明

- 明确目标、约束条件和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如果需要详细示例，请打开 `resources/implementation-playbook.md`。

## 预检查

1. 验证 Conductor 已初始化：
   - 检查 `conductor/product.md` 是否存在
   - 检查 `conductor/workflow.md` 是否存在
   - 检查 `conductor/tracks.md` 是否存在
   - 如果缺失：显示错误并建议先运行 `/conductor:setup`

2. 加载工作流配置：
   - 读取 `conductor/workflow.md`
   - 解析 TDD 严格级别
   - 解析提交策略
   - 解析验证检查点规则

## 轨道选择

### 如果提供了参数：

- 验证轨道是否存在：`conductor/tracks/{argument}/plan.md`
- 如果未找到：搜索部分匹配项，建议修正

### 如果没有参数：

1. 读取 `conductor/tracks.md`
2. 解析未完成的轨道（状态 `[ ]` 或 `[~]`）
3. 显示选择菜单：

   ```
   选择要实现的轨道：

   进行中：
   1. [~] auth_20250115 - 用户认证（阶段 2，任务 3）

   待处理：
   2. [ ] nav-fix_20250114 - 导航 Bug 修复
   3. [ ] dashboard_20250113 - 仪表盘功能

   输入编号或轨道 ID：
   ```

## 上下文加载

加载实现所需的所有相关上下文：

1. 轨道文档：
   - `conductor/tracks/{trackId}/spec.md` - 需求
   - `conductor/tracks/{trackId}/plan.md` - 任务列表
   - `conductor/tracks/{trackId}/metadata.json` - 进度状态

2. 项目上下文：
   - `conductor/product.md` - 产品理解
   - `conductor/tech-stack.md` - 技术约束
   - `conductor/workflow.md` - 流程规则

3. 代码风格（如果存在）：
   - `conductor/code_styleguides/{language}.md`

## 轨道状态更新

将轨道更新为进行中：

1. 在 `conductor/tracks.md` 中：
   - 将此轨道的 `[ ]` 改为 `[~]`

2. 在 `conductor/tracks/{trackId}/metadata.json` 中：
   - 设置 `status: "in_progress"`
   - 更新 `updated` 时间戳

## 任务执行循环

对于 plan.md 中的每个未完成任务（标记为 `[ ]`）：

### 1. 任务识别

解析 plan.md 找到下一个未完成任务：

- 查找匹配 `- [ ] Task X.Y: {description}` 的行
- 从结构中追踪当前阶段

### 2. 任务开始

将任务标记为进行中：

- 更新 plan.md：将当前任务的 `[ ]` 改为 `[~]`
- 宣布："开始任务 X.Y：{description}"

### 3. TDD 工作流（如果在 workflow.md 中启用了 TDD）

**红灯阶段 - 编写失败的测试：**

```
正在为任务 X.Y 执行 TDD 工作流...

步骤 1：编写失败的测试
```

- 如需要则创建测试文件
- 为任务功能编写测试
- 运行测试确认它们失败
- 如果测试意外通过：停止，调查原因

**绿灯阶段 - 实现：**

```
步骤 2：实现最小代码以通过测试
```

- 编写使测试通过的最小代码
- 运行测试确认它们通过
- 如果测试失败：调试并修复

**重构阶段：**

```
步骤 3：重构代码，同时保持测试通过
```

- 清理代码
- 运行测试确保仍然通过

### 4. 非 TDD 工作流（如果 TDD 不严格）

- 直接实现任务
- 运行任何现有测试
- 根据需要进行手动验证

### 5. 任务完成

**提交更改**（遵循 workflow.md 中的提交策略）：

```bash
git add -A
git commit -m "{commit_prefix}: {任务描述} ({trackId})"
```

**更新 plan.md：**

- 将已完成任务的 `[~]` 改为 `[x]`
- 提交计划更新：

```bash
git add conductor/tracks/{trackId}/plan.md
git commit -m "chore: 标记任务 X.Y 完成 ({trackId})"
```

**更新 metadata.json：**

- 递增 `tasks.completed`
- 更新 `updated` 时间戳

### 6. 阶段完成检查

每个任务完成后，检查阶段是否完成：

- 解析 plan.md 的阶段结构
- 如果当前阶段的所有任务都是 `[x]`：

**运行阶段验证：**

```
阶段 {N} 完成。正在运行验证...
```

- 执行阶段列出的验证任务
- 运行完整测试套件：`npm test` / `pytest` 等

**报告并等待批准：**

```
阶段 {N} 验证结果：
- 所有阶段任务：已完成
- 测试：{通过/失败}
- 验证：{通过/失败}

批准继续进入阶段 {N+1} 吗？
1. 是，继续
2. 否，有问题需要修复
3. 暂停实现
```

**关键：在进入下一阶段前等待用户明确批准。**

## 实现过程中的错误处理

### 工具失败时

```
错误：{tool} 失败，原因：{错误消息}

选项：
1. 重试操作
2. 跳过此任务并继续
3. 暂停实现
4. 撤销当前任务更改
```

- 停止并展示选项
- 不要自动继续

### 测试失败时

```
任务 X.Y 后测试失败

失败的测试：
- {测试名称}：{失败原因}

选项：
1. 尝试修复
2. 回滚任务更改
3. 暂停等待手动干预
```

### Git 失败时

```
GIT 错误：{错误消息}

这可能表示：
- Conductor 之外有未提交的更改
- 合并冲突
- 权限问题

选项：
1. 显示 git status
2. 尝试解决
3. 暂停等待手动干预
```

## 轨道完成

当所有阶段和任务都完成时：

### 1. 最终验证

```
所有任务已完成。正在运行最终验证...
```

- 运行完整测试套件
- 检查 spec.md 中的所有验收标准
- 生成验证报告

### 2. 更新轨道状态

在 `conductor/tracks.md` 中：

- 将此轨道的 `[~]` 改为 `[x]`
- 更新 "Updated" 列

在 `conductor/tracks/{trackId}/metadata.json` 中：

- 设置 `status: "complete"`
- 设置 `phases.completed` 为总数
- 设置 `tasks.completed` 为总数
- 更新 `updated` 时间戳

在 `conductor/tracks/{trackId}/plan.md` 中：

- 将标题状态更新为 `[x] Complete`

### 3. 文档同步提示

```
轨道已完成！是否同步文档？

这将更新：
- conductor/product.md（如果添加了新功能）
- conductor/tech-stack.md（如果添加了新依赖）
- README.md（如果适用）

1. 是，同步文档
2. 否，跳过
```

### 4. 清理提示

```
轨道 {trackId} 已完成。

清理选项：
1. 归档 - 移动到 conductor/tracks/_archive/
2. 删除 - 移除轨道目录
3. 保留 - 保持原样
```

### 5. 完成摘要

```
轨道完成：{轨道标题}

摘要：
- 轨道 ID：{trackId}
- 完成阶段：{N}/{N}
- 完成任务：{M}/{M}
- 创建提交：{count}
- 测试：全部通过

下一步：
- 运行 /conductor:status 查看项目进度
- 运行 /conductor:new-track 开始下一个功能
```

## 进度追踪

在整个过程中维护 `metadata.json` 中的进度：

```json
{
  "id": "auth_20250115",
  "title": "User Authentication",
  "type": "feature",
  "status": "in_progress",
  "created": "2025-01-15T10:00:00Z",
  "updated": "2025-01-15T14:30:00Z",
  "current_phase": 2,
  "current_task": "2.3",
  "phases": {
    "total": 3,
    "completed": 1
  },
  "tasks": {
    "total": 12,
    "completed": 7
  },
  "commits": [
    "abc1234: feat: add login form (auth_20250115)",
    "def5678: feat: add password validation (auth_20250115)"
  ]
}
```

## 恢复

如果实现被暂停后恢复：

1. 加载 `metadata.json` 获取当前状态
2. 从 `current_task` 字段找到当前任务
3. 检查 plan.md 中任务是否为 `[~]`
4. 询问用户：

   ```
   正在恢复轨道：{title}

   上次进行中的任务：任务 {X.Y}：{description}

   选项：
   1. 从上次中断处继续
   2. 重新开始当前任务
   3. 先显示进度摘要
   ```

## 关键规则

1. **绝不要跳过验证检查点** - 阶段之间必须等待用户批准
2. **任何失败都要停止** - 不要尝试跳过错误继续
3. **严格遵循 workflow.md** - TDD、提交策略和验证规则是强制性的
4. **保持 plan.md 更新** - 任务状态必须反映实际进度
5. **频繁提交** - 每个任务完成都应该提交
6. **追踪所有提交** - 在 metadata.json 中记录提交哈希以便可能的回滚

## 局限性
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
