---
name: conductor-manage
description: "管理 track 生命周期：归档、恢复、删除、重命名和清理"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Track 管理器

管理完整的 track 生命周期，包括归档、恢复、删除、重命名和清理孤立产物。

## 使用此技能的场景

- 归档、恢复、重命名或删除 Conductor track
- 列出 track 状态或清理孤立产物
- 管理跨活跃、已完成和已归档状态的 track 生命周期

## 不使用此技能的场景

- 仓库中未初始化 Conductor
- 缺少修改 track 元数据或文件的权限
- 任务与 Conductor track 管理无关

## 操作说明

- 执行前验证 `conductor/` 结构和所需文件。
- 从参数或交互式提示中确定操作模式。
- 应用破坏性操作（删除/清理）前进行确认。
- 一致地更新 `tracks.md` 和元数据。
- 如需详细步骤，打开 `resources/implementation-playbook.md`。

## 安全注意事项

- 删除操作前备份 track 数据。
- 未经明确批准，不要移除已归档的 track。

## 资源

- `resources/implementation-playbook.md` 包含详细的模式、提示词和工作流程。

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
