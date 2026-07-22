---
name: conductor-validator
description: '验证 Conductor 项目产物的完整性、一致性和正确性。在设置完成后、诊断问题时或实现前验证项目上下文时使用。'
risk: safe
source: community
date_added: '2026-02-27'
---

# 检查 conductor 目录是否存在
ls -la conductor/

# 查找所有 track 目录
ls -la conductor/tracks/

# 检查必需文件
ls conductor/index.md conductor/product.md conductor/tech-stack.md conductor/workflow.md conductor/tracks.md
```

## 使用此技能的场景

- 处理检查 conductor 目录是否存在相关的任务或工作流
- 需要检查 conductor 目录是否存在的指导、最佳实践或检查清单

## 不使用此技能的场景

- 任务与检查 conductor 目录是否存在无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 模式匹配

**tracks.md 中的状态标记：**

```
- [ ] Track Name  # 未开始
- [~] Track Name  # 进行中
- [x] Track Name  # 已完成
```

**plan.md 中的任务标记：**

```
- [ ] Task description  # 待处理
- [~] Task description  # 进行中
- [x] Task description  # 已完成
```

**Track ID 模式：**

```
<type>_<name>_<YYYYMMDD>
示例: feature_user_auth_20250115
```

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
