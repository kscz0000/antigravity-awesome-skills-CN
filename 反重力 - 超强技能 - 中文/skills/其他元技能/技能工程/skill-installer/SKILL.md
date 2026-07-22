---
name: skill-installer
description: 在生态系统中安装、验证、注册和检查新技能。包含 10 项安全检查、复制、编排器注册和安装后验证。触发词：安装技能、注册技能、新技能、install skill、registrar skill、instalar skill、技能管理
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- skill-management
- deployment
- validation
- installation
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# 技能安装器 v3.0

## 概述

在生态系统中安装、验证、注册和检查新技能。包含 10 项安全检查、复制、编排器注册和安装后验证。

## 使用场景

- 用户提到"安装技能"或相关话题时
- 用户提到"install skill"或相关话题时
- 用户提到"注册技能"或相关话题时
- 用户提到"新技能"或相关话题时
- 用户提到"new skill"或相关话题时
- 用户提到"将技能添加到生态系统"或相关话题时

## 不适用场景

- 任务与技能安装器无关
- 有更简单、更具体的工具可以处理该请求
- 用户需要不涉及领域专业知识的通用帮助

## 工作原理

企业级安装智能体，确保通过 skill-creator 或手动创建的每个技能都能被正确安装、注册和验证。包含自动修复、回滚、试运行、仪表盘和高级诊断。

## 原则：最大冗余

六层验证确保没有技能被错误安装：

| 层级 | 脚本 | 验证内容 |
|------|------|----------|
| 1 | detect_skills.py | SKILL.md 存在且包含 frontmatter |
| 2 | validate_skill.py | 10 项深度检查 |
| 3 | install_skill.py（前置） | 冲突、权限、空间、版本 |
| 4 | install_skill.py（后置） | 文件已正确复制 |
| 5 | scan_registry.py | 技能出现在注册表中（含去重） |
| 6 | package_skill.py | 有效的 ZIP，无反斜杠，非空，完整性检查 |

---

## 目录结构

```
C:\Users\renat\skills\skill-installer\
├── SKILL.md              <- 本文件
├── scripts/
│   ├── install_skill.py  <- 主安装器（11 步）+ 所有命令
│   ├── detect_skills.py  <- 未安装技能扫描器
│   ├── validate_skill.py <- 深度验证（10 项检查）
│   ├── package_skill.py  <- ZIP 打包器 + 完整性验证器
│   └── requirements.txt
├── references/
│   └── known-locations.md
└── data/
    ├── install_log.json  <- 操作日志（自动生成，带轮转）
    ├── backups/          <- 覆盖前的备份
    └── staging/          <- 安全复制的临时区域
```

---

## 主工作流

当此技能被激活时，按以下顺序执行：

## 场景 1：skill-creator 完成后

skill-creator 刚在某个目录中创建了技能。执行：

```bash
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --source "<创建的技能路径>" --force
```

将 `<创建的技能路径>` 替换为 skill-creator 保存技能的目录。

## 场景 2：用户请求安装特定技能

```bash
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --source "<路径>" [--name "名称覆盖"] [--force]
```

## 场景 3：模拟安装但不实际执行（试运行）

```bash
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --source "<路径>" --dry-run
```

精确显示 11 个步骤中每一步会做什么，但不修改任何文件。

## 场景 4：检测并安装待处理技能

```bash
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --detect
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --detect --auto
```

扫描已知位置（桌面、下载、临时目录、工作区），展示带有时间戳和大小的候选项。使用 `--auto` 可自动安装所有候选项。

## 场景 5：卸载技能

```bash
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --uninstall "技能名称"
```

从 `skills/`、`.claude/skills/` 中移除，更新注册表并删除桌面上的 ZIP。移除前会自动备份。

## 场景 6：健康检查 + 自动修复

```bash
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --health
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --health --repair
```

`--health` 检查所有技能：frontmatter、注册、注册表、重复项。
`--health --repair` 发现问题并自动修复：
- 未注册的技能 → 注册
- 注册表中缺失的技能 → 更新
- 重复项 → 移除

## 场景 7：回滚（从备份恢复）

```bash
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --rollback "技能名称"
```

查找该技能的最新备份并恢复到之前的状态。自动重新注册并更新注册表。

## 场景 8：重新安装所有技能

```bash
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --reinstall-all
```

重新注册 `.claude/skills/` 中的所有技能，重新打包所有 ZIP，并更新注册表。适用于批量更改或迁移后。

## 场景 9：状态仪表盘

```bash
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --status
```

显示丰富的仪表盘：每个技能的名称、版本、健康状态、注册状态、备份情况，以及操作统计（安装、卸载、回滚）。

## 场景 10：查看操作历史

```bash
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --log
python C:\Users\renat\skills\skill-installer\scripts\install_skill.py --log 50
```

显示最近 N 条操作记录，包含时间戳、类型、技能和结果。

---

## 验证技能

```bash
python C:\Users\renat\skills\skill-installer\scripts\validate_skill.py "C:\路径\到\技能"
python C:\Users\renat\skills\skill-installer\scripts\validate_skill.py "C:\路径\到\技能" --strict
```

返回包含 `valid`（布尔值）、`checks`、`warnings`、`errors` 的 JSON。

## 检测未安装的技能

```bash
python C:\Users\renat\skills\skill-installer\scripts\detect_skills.py
python C:\Users\renat\skills\skill-installer\scripts\detect_skills.py --path "C:\指定目录"
python C:\Users\renat\skills\skill-installer\scripts\detect_skills.py --all
```

返回包含候选项的 JSON，包括：`name`、`source_path`、`already_installed`、`valid_frontmatter`、`last_modified`、`size_kb`、`file_count`。

## 打包 ZIP 用于 Claude.ai

```bash
python C:\Users\renat\skills\skill-installer\scripts\package_skill.py --source "C:\路径"
python C:\Users\renat\skills\skill-installer\scripts\package_skill.py --all
python C:\Users\renat\skills\skill-installer\scripts\package_skill.py --all --output "C:\Users\renat\Desktop"
```

## 验证现有 ZIP 的完整性

```bash
python C:\Users\renat\skills\skill-installer\scripts\package_skill.py --verify
python C:\Users\renat\skills\skill-installer\scripts\package_skill.py --verify --output "C:\Users\renat\Desktop"
```

---

## install_skill.py 命令

| 命令 | 说明 |
|------|------|
| `--source <路径>` | 从路径安装技能 |
| `--source <路径> --force` | 存在时覆盖 |
| `--source <路径> --name <名称>` | 自定义名称 |
| `--source <路径> --dry-run` | 模拟安装，不做实际修改 |
| `--detect` | 自动检测待处理技能 |
| `--detect --auto` | 检测并自动安装 |
| `--uninstall <名称>` | 卸载（带备份） |
| `--rollback <名称>` | 从最近备份恢复 |
| `--reinstall-all` | 重新注册 + 重新打包所有技能 |
| `--health` | 所有技能健康检查 |
| `--health --repair` | 健康检查 + 自动修复 |
| `--status` | 包含版本、健康状态、备份的丰富仪表盘 |
| `--log [N]` | 最近 N 条操作（默认：20） |
| `--json` | 输出 JSON 而非格式化文本 |

---

## 安装器执行流程（11 步）

1. **解析来源** - 识别技能目录
2. **验证** - 对 SKILL.md 和结构运行 10 项检查
3. **确定名称** - 从 frontmatter 提取或使用 --name，比较版本
4. **检查冲突** - 检查目标位置是否已存在
5. **备份** - 如需覆盖，创建带时间戳的备份（排除 backups/ 和 staging/）
6. **通过暂存区复制** - 先复制到临时区域，验证哈希，然后移动
7. **注册到 Claude Code CLI** - 将 SKILL.md 复制到 .claude/skills/<名称>/
8. **更新注册表** - 运行 scan_registry.py --force（按名称去重）
9. **验证安装** - 确认文件、注册表、注册记录（5 项检查）
10. **打包 ZIP** - 创建用于 Claude.ai 网页/桌面上传的 ZIP（已验证）
11. **记录操作** - 追加到 install_log.json（带自动轮转）

**重要提示**：Claude Code（CLI）和 Claude.ai（网页/桌面）中的技能是分开的。安装器自动覆盖两个平台。

---

## 安全特性

- **自动备份**：任何覆盖前，先备份到 `data/backups/<名称>_<时间戳>/`
- **暂存区域**：先复制到临时目录，验证哈希，然后移动（最小化损坏风险）
- **幂等性**：对同一来源运行 2 次会检测到相同哈希，不会重复
- **禁止文件**：发现 .env、*.key、*.pem、credentials.* 时阻止安装
- **轮转日志**：所有操作均有日志；保留最近 500 条记录
- **备份限制**：每个技能保留最近 5 个备份，自动清理
- **防递归**：备份和暂存排除其自身的子目录
- **注册表去重**：scan_registry.py 按名称去重（不区分大小写）
- **ZIP 验证**：检查无反斜杠、内容非空、完整性
- **试运行**：模拟完整安装但不修改任何文件
- **回滚**：从备份恢复并自动重新注册
- **版本比较**：覆盖前检测升级/降级/相同版本
- **哈希规范化**：md5_dir 使用正斜杠并排除系统目录

---

## 与编排器的集成

此技能由 `scan_registry.py` 自动检测，并在用户提到安装相关关键词时由 `match_skills.py` 匹配。无需手动配置。

此外，全局 CLAUDE.md 包含在 skill-creator 完成技能后自动运行安装器的指令。

## 最佳实践

- 提供关于项目和需求的清晰、具体的上下文
- 将建议应用到生产代码前先审查所有建议
- 结合其他互补技能进行综合分析

## 常见陷阱

- 将此技能用于超出其领域专业范围的任务
- 在不了解具体上下文的情况下应用建议
- 未提供足够的项目上下文导致分析不准确

## 相关技能

- `skill-sentinel` - 互补技能，用于增强分析

## 局限性
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
