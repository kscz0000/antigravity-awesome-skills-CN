---
name: speckit-updater
description: SpecKit 安全更新工具，为 GitHub SpecKit 安装提供安全更新能力，在应用模板更新的同时保留自定义内容。触发词：SpecKit更新、安全更新、模板更新、版本更新、回滚
risk: unknown
source: community
---

# SpecKit 安全更新

本技能为 GitHub SpecKit 安装提供安全更新能力，在应用模板更新的同时保留自定义内容。

**安装方式**：可通过插件安装（`/plugin marketplace add NotMyself/claude-plugins` 然后 `/plugin install speckit-updater`）或手动 Git 克隆。详见 README.md。

## 使用场景
- 需要更新或安装 SpecKit 模板，同时保留项目自定义内容。
- 需要围绕更新、回滚或特定版本的 SpecKit 操作进行安全审批流程。
- 通过对话方式操作 SpecKit 更新器，而非盲目运行原始命令。

## 调用本技能时的操作指南

当用户调用 `/speckit-updater` 时，你需要：

1. **运行更新编排脚本**，不带任何参数（对话模式）：
   ```powershell
   pwsh -NoProfile -Command "& 'C:\Users\bobby\.claude\skills\speckit-updater\scripts\update-wrapper.ps1'"
   ```

2. **解析输出**中的标记：
   - **`[PROMPT_FOR_APPROVAL]`** — 更新场景（已有 SpecKit 安装）
   - **`[PROMPT_FOR_INSTALL]`** — 全新安装场景（无 .specify/ 目录）

3. **更新场景**（发现 `[PROMPT_FOR_APPROVAL]` 标记）：
   - **展示 Markdown 摘要**，包含：
     - 当前版本 vs. 可用版本
     - 需要更新/添加/删除的文件
     - 检测到的冲突（如有）
     - 保留的文件（已自定义）
     - 备份位置
     - 自定义命令
   - **请求用户批准**继续更新
   - **若批准**，使用 `-Proceed` 参数重新运行
   - **若拒绝**，告知用户更新已取消

4. **全新安装场景**（发现 `[PROMPT_FOR_INSTALL]` 标记）：
   - **以自然的方式向用户提出安装建议**，例如：
     - "当前项目尚未安装 SpecKit，是否需要安装？"
     - "我可以为你安装最新的 SpecKit 模板。这将创建 .specify/ 目录结构并从 GitHub 下载模板。"
   - **不要向用户提及 `-Proceed` 参数**（这是实现细节）
   - **若用户同意**（说"好"、"继续"、"安装吧"等），使用 `-Proceed` 参数重新运行
   - **若用户拒绝**，告知安装已取消

5. **执行已批准的操作**，使用 `-Proceed` 参数重新运行：
   ```powershell
   pwsh -NoProfile -Command "& 'C:\Users\bobby\.claude\skills\speckit-updater\scripts\update-wrapper.ps1' -Proceed"
   ```

**特殊情况：**
- 若用户请求 `-CheckOnly`：使用该参数运行并展示报告
- 若用户请求 `-Rollback`：使用该参数运行并确认恢复
- 若用户请求特定 `-Version`：包含该参数

## 命令

### /speckit-updater

更新 SpecKit 模板、命令和脚本，同时保留自定义内容。

**用法：**
- `/speckit-updater` — 交互式更新/安装，带对话审批工作流（推荐用于 Claude Code）
- `/speckit-updater -Proceed` — 用户确认后继续更新/安装（由 Claude 在用户确认后使用）
- `/speckit-updater -CheckOnly` — 仅检查更新，不应用
- `/speckit-updater -Version v0.0.72` — 更新到指定版本
- `/speckit-updater -Force` — 强制覆盖 SpecKit 文件（保留自定义命令）
- `/speckit-updater -Rollback` — 从之前的备份恢复
- `/speckit-updater -Auto` — 已弃用：请改用对话工作流（显示警告，映射到 -Proceed）

**全新安装（无 .specify/ 目录）：**
- 首次调用时显示带 `[PROMPT_FOR_INSTALL]` 标记的安装建议
- Claude Code 以自然方式向用户提问（如"是否需要安装 SpecKit？"）
- 用户通过对话回复确认（如"好"、"继续"、"安装吧"）
- Claude 自动使用 `-Proceed` 参数重新调用（实现细节对用户隐藏）
- 脚本创建 `.specify/` 结构、下载模板、创建清单
- 全程退出码为 0（等待审批不是错误）
- 与更新流程一致：两者都使用对话审批工作流

**流程：**
1. 验证前置条件（Git 已安装、Git 状态干净、有写入权限）
2. 加载或创建清单（.specify/manifest.json）
3. 从 GitHub Releases API 获取目标版本
4. 比较文件哈希以识别自定义内容
5. 创建带时间戳的备份
6. 应用选择性更新，保留已自定义的文件
7. 对冲突打开 VSCode 合并编辑器（流程 A：逐个处理）
8. 自动调用 /speckit.constitution 进行配置更新
9. 更新清单中的版本信息
10. 管理备份保留（保留最近 5 个）

**调用此命令时，我会：**
1. 执行 update-orchestrator.ps1 脚本
2. 解析输出中的标记（更新用 `[PROMPT_FOR_APPROVAL]`，全新安装用 `[PROMPT_FOR_INSTALL]`）
3. **更新场景**：展示变更摘要的 Markdown
4. **安装场景**：自然地询问是否安装 SpecKit（不提及 `-Proceed` 参数）
5. 通过对话等待你的批准
6. 批准后：自动使用 `-Proceed` 参数重新调用执行
7. 引导你逐个文件解决冲突（仅更新场景）
8. 根据需要打开 VSCode 差异/合并工具（仅更新场景）
9. 展示详细的结果摘要

**对话工作流：** 本技能使用两步审批流程：
- **第一步**：输出摘要 → 脚本退出 → 等待审批
- **第二步**：审批后，Claude 使用 `-Proceed` 重新调用 → 应用更新

**要求：**
- Git 已安装且在 PATH 中
- 需要网络连接以从 GitHub 获取更新
- 对 .specify/ 和 .claude/ 目录有写入权限
- Git 工作目录干净或已暂存

**脚本位置：** `{skill_path}/scripts/update-wrapper.ps1`（入口点）和 `{skill_path}/scripts/update-orchestrator.ps1`（主逻辑）

**入口点命令：**
```powershell
pwsh -NoProfile -Command "& '{skill_path}/scripts/update-wrapper.ps1' [parameters]"
```

**注意：** 包装脚本同时支持 PowerShell 风格（`-CheckOnly`）和 Linux 风格（`--check-only`）的参数。

## 功能特性

- **自定义内容保留**：使用规范化文件哈希自动检测并保留用户自定义内容
- **智能冲突解决**：逐个引导处理冲突，提供 4 种选项：合并编辑器、保留我的、使用新的、跳过
- **版本追踪**：维护 `.specify/manifest.json`，记录文件哈希、版本信息和备份历史
- **自动备份**：在 `.specify/backups/` 中创建带时间戳的备份，自动管理保留数量
- **快速失败与回滚**：任何错误时自动回滚，恢复到更新前的状态
- **模拟运行模式**：`--check-only` 精确展示将要变更的内容而不实际应用
- **配置集成**：当配置模板有更新时通知（运行 `/speckit.constitution`）
- **自定义命令安全**：用户创建的命令永远不会被覆盖，即使使用 `--force`

## 架构

### 模块
- **HashUtils**：规范化哈希（处理行尾符、尾部空白、BOM）
- **VSCodeIntegration**：上下文检测、快速选择、差异/合并编辑器集成
- **GitHubApiClient**：GitHub Releases API 交互（未认证，60 次请求/小时）
- **ManifestManager**：清单的增删改查操作，带缓存
- **BackupManager**：备份创建、恢复和保留管理
- **ConflictDetector**：文件状态分析和冲突检测

### 工作流
1. 前置条件验证（关键检查必须通过，警告允许继续）
2. 清单加载/创建（安全默认值：若无清单则假设所有文件已自定义）
3. 查询 GitHub API 获取目标版本
4. 文件状态分析（6 种操作：添加/删除/合并/保留/更新/跳过）
5. 用户确认变更预览
6. 创建备份（带时间戳，排除 backups 目录）
7. 选择性文件更新（快速失败并自动回滚）
8. 冲突解决（流程 A：逐个处理，VSCode 合并编辑器）
9. 清单更新（版本、文件哈希、自定义标记）
10. 备份清理（保留最近 5 个，需确认）
11. 展示详细摘要

## 退出码

| 代码 | 含义 |
|------|------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 前置条件不满足 |
| 3 | 网络/API 错误 |
| 4 | Git 错误 |
| 5 | 用户取消 |
| 6 | 需要回滚（自动执行） |

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
