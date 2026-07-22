---
name: linear-claude-skill
description: "管理 Linear issue、项目和团队。当用户要求'管理 Linear'、'创建 issue'、'更新项目状态'、'Linear 工单'时使用。"
risk: safe
source: "https://github.com/wrsmith108/linear-claude-skill"
date_added: "2026-02-27"
---

## 何时使用此技能

管理 Linear issue、项目和团队

当需要管理 Linear issue、项目和团队时使用此技能。
# Linear

管理 Linear 中 issue、项目和团队的工具与工作流。

---

## ⚠️ 工具可用性（先读此节）

**此技能支持多种工具后端，按可用性选择：**

1. **MCP 工具 (mcp__linear)** — 如可用则优先使用
2. **Linear CLI（`linear` 命令）** — 始终可通过 Bash 使用
3. **辅助脚本** — 用于复杂操作

**如 MCP 工具不可用**，通过 Bash 使用 Linear CLI：

```bash
# View an issue
linear issues view ENG-123

# Create an issue
linear issues create --title "Issue title" --description "Description"

# Update issue status (get state IDs first)
linear issues update ENG-123 -s "STATE_ID"

# Add a comment
linear issues comment add ENG-123 -m "Comment text"

# List issues
linear issues list
```

**不要将"MCP 工具不可用"报告为阻碍** — 改用 CLI。

---


## 何时使用此技能

管理 Linear issue、项目和团队

当需要管理 Linear issue、项目和团队时使用此技能。
## 🔐 安全：Varlock 集成

**关键**：绝不在终端输出或 Claude 上下文中暴露 API 密钥。

### 安全命令（始终使用）

```bash
# Validate LINEAR_API_KEY is set (masked output)
varlock load 2>&1 | grep LINEAR

# Run commands with secrets injected
varlock run -- npx tsx scripts/query.ts "query { viewer { name } }"

# Check schema (safe - no values)
cat .env.schema | grep LINEAR
```

### 危险命令（禁止使用）

```bash
# ❌ NEVER - exposes key to Claude's context
linear config show
echo 
printenv | grep LINEAR
cat .env
```

### 新项目配置

1. 创建 `.env.schema` 并添加 `@sensitive` 标注：
   ```bash
   # @type=string(startsWith=lin_api_) @required @sensitive
   LINEAR_API_KEY=
   ```

2. 将 `LINEAR_API_KEY` 添加到 `.env`（切勿提交此文件）

3. 配置 MCP 使用环境变量：
   ```json
   {
     "mcpServers": {
       "linear": {
         "env": { "LINEAR_API_KEY": "" }
       }
     }
   }
   ```

4. 操作前用 `varlock load` 验证

---

## 快速入门（首次使用）

### 1. 检查配置

运行配置检查以验证环境：

```bash
npx tsx ~/.claude/skills/linear/scripts/setup.ts
```

检查内容：
- LINEAR_API_KEY 已设置且有效
- @linear/sdk 已安装
- Linear CLI 可用性（可选）
- MCP 配置（可选）

### 2. 获取 API 密钥（如需）

如配置检查提示缺少 API 密钥：

1. 在浏览器中打开 [Linear](https://linear.app)
2. 进入 **Settings**（齿轮图标）-> **Security & access** -> **Personal API keys**
3. 点击 **Create key** 并复制密钥（以 `lin_api_` 开头）
4. 添加到环境：

```bash
# Option A: Add to shell profile (~/.zshrc or ~/.bashrc)
export LINEAR_API_KEY="lin_api_your_key_here"

# Option B: Add to Claude Code environment
echo 'LINEAR_API_KEY=lin_api_your_key_here' >> ~/.claude/.env

# Then reload your shell or restart Claude Code
```

### 3. 测试连接

验证一切正常：

```bash
npx tsx ~/.claude/skills/linear/scripts/query.ts "query { viewer { name } }"
```

应看到你在 Linear 中的用户名。

### 4. 常用操作

```bash
# Create issue in a project
npx tsx scripts/linear-ops.ts create-issue "Project" "Title" "Description"

# Update issue status
npx tsx scripts/linear-ops.ts status Done ENG-123 ENG-124

# Create sub-issue
npx tsx scripts/linear-ops.ts create-sub-issue ENG-100 "Sub-task" "Details"

# Update project status
npx tsx scripts/linear-ops.ts project-status "Phase 1" completed

# Show all commands
npx tsx scripts/linear-ops.ts help
```

完整参考见[项目管理命令](#project-management-commands)。

---


## 何时使用此技能

管理 Linear issue、项目和团队

当需要管理 Linear issue、项目和团队时使用此技能。
## 项目规划工作流

### 从一开始就在正确的项目中创建 issue

**最佳实践**：规划新阶段或新计划时，在同一次规划会话中一起创建项目及其 issue。避免先在临时项目中创建 issue 再后续移动。

#### 推荐工作流

1. **先创建项目**：
   ```bash
   npx tsx scripts/linear-ops.ts create-project "Phase X: Feature Name" "My Initiative"
   ```

2. **将项目状态设为 Planned**：
   ```bash
   npx tsx scripts/linear-ops.ts project-status "Phase X: Feature Name" planned
   ```

3. **直接在项目中创建 issue**：
   ```bash
   npx tsx scripts/linear-ops.ts create-issue "Phase X: Feature Name" "Parent task" "Description"
   npx tsx scripts/linear-ops.ts create-sub-issue ENG-XXX "Sub-task 1" "Description"
   npx tsx scripts/linear-ops.ts create-sub-issue ENG-XXX "Sub-task 2" "Description"
   ```

4. **工作开始时更新项目状态**：
   ```bash
   npx tsx scripts/linear-ops.ts project-status "Phase X: Feature Name" in-progress
   ```

#### 为什么这样做

- **可追溯性**：issue 从创建起就关联到项目
- **指标准确性**：项目进度追踪从第一天就准确
- **工作流效率**：无需在项目间移动 issue
- **组织性**：Linear 视图和筛选器正常工作

#### 应避免的反模式

❌ 在"暂存"项目中创建 issue 再后续移动：
```bash
# Don't do this
create-issue "Phase 6A" "New feature"  # Wrong project
# Later: manually move to Phase X      # Extra work
```

---

## 项目管理命令

### project-status

更新 Linear 中的项目状态。接受用户友好的术语，自动映射到 Linear API。

```bash
npx tsx scripts/linear-ops.ts project-status <project-name> <state>
```

**有效状态：**
| 输入 | 说明 | API 值 |
|-------|------|-----------|
| `backlog` | 尚未启动 | backlog |
| `planned` | 已排期 | planned |
| `in-progress` | 进行中 | started |
| `paused` | 暂时搁置 | paused |
| `completed` | 已完成 | completed |
| `canceled` | 已取消 | canceled |

**示例：**
```bash
# Start working on a project
npx tsx scripts/linear-ops.ts project-status "Phase 8: MCP Decision Engine" in-progress

# Mark project complete
npx tsx scripts/linear-ops.ts project-status "Phase 8" completed

# Partial name matching works
npx tsx scripts/linear-ops.ts project-status "Phase 8" paused
```

### link-initiative

将已有项目关联到计划。

```bash
npx tsx scripts/linear-ops.ts link-initiative <project-name> <initiative-name>
```

**示例：**
```bash
# Link a project to an initiative
npx tsx scripts/linear-ops.ts link-initiative "Phase 8: MCP Decision Engine" "Q1 Goals"

# Partial matching works
npx tsx scripts/linear-ops.ts link-initiative "Phase 8" "Q1 Goals"
```

### unlink-initiative

将项目从计划中移除。

```bash
npx tsx scripts/linear-ops.ts unlink-initiative <project-name> <initiative-name>
```

**示例：**
```bash
# Remove incorrect link
npx tsx scripts/linear-ops.ts unlink-initiative "Phase 8" "Linear Skill"

# Clean up test links
npx tsx scripts/linear-ops.ts unlink-initiative "Test Project" "Q1 Goals"
```

**错误处理：**
- 项目未关联到指定计划时返回错误
- 项目或计划未找到时返回错误

### 完整项目生命周期示例

```bash
# 1. Create project linked to initiative
npx tsx scripts/linear-ops.ts create-project "Phase 11: New Feature" "Q1 Goals"

# 2. Set state to planned
npx tsx scripts/linear-ops.ts project-status "Phase 11" planned

# 3. Create issues in the project
npx tsx scripts/linear-ops.ts create-issue "Phase 11" "Parent task" "Description"
npx tsx scripts/linear-ops.ts create-sub-issue ENG-XXX "Sub-task 1" "Details"

# 4. Start work - update to in-progress
npx tsx scripts/linear-ops.ts project-status "Phase 11" in-progress

# 5. Mark issues done
npx tsx scripts/linear-ops.ts status Done ENG-XXX ENG-YYY

# 6. Complete project
npx tsx scripts/linear-ops.ts project-status "Phase 11" completed

# 7. (Optional) Link to additional initiative
npx tsx scripts/linear-ops.ts link-initiative "Phase 11" "Q2 Goals"
```

---


## 何时使用此技能

管理 Linear issue、项目和团队

当需要管理 Linear issue、项目和团队时使用此技能。
## 工具选择

根据任务选择合适的工具：

| 工具 | 适用场景 |
|------|----------|
| **MCP（官方服务器）** | 大多数操作 — 首选 |
| **辅助脚本** | 批量操作，MCP 不可用时 |
| **SDK 脚本** | 复杂操作（循环、条件） |
| **GraphQL API** | MCP/SDK 不支持的操作 |

### MCP 服务器配置

**使用官方 Linear MCP 服务器** `mcp.linear.app`：

```json
{
  "mcpServers": {
    "linear": {
      "command": "npx",
      "args": ["mcp-remote", "https://mcp.linear.app/sse"],
      "env": { "LINEAR_API_KEY": "your_api_key" }
    }
  }
}
```

> **警告**：不要使用已弃用的社区服务器。详见 troubleshooting.md。

### MCP 可靠性（官方服务器）

| 操作 | 可靠性 | 备注 |
|------|--------|------|
| 创建 issue | ✅ 高 | 完全支持 |
| 更新状态 | ✅ 高 | 直接用 `state: "Done"` |
| 列出/搜索 issue | ✅ 高 | 支持筛选和查询 |
| 添加评论 | ✅ 高 | 支持 issue ID |

### 快速状态更新

```bash
# Via MCP - use human-readable state names
update_issue with id="issue-uuid", state="Done"

# Via helper script (bulk operations)
node scripts/linear-helpers.mjs update-status Done 123 124 125
```

### 辅助脚本参考

辅助脚本的详细用法见 **troubleshooting.md**。

### 并行智能体执行

批量操作或后台执行时，使用 `Linear-specialist` 子智能体：

```javascript
Task({
  description: "Update Linear issues",
  prompt: "Mark ENG-101, ENG-102, ENG-103 as Done",
  subagent_type: "Linear-specialist"
})
```

**何时使用 `Linear-specialist`（并行）：**
- 批量状态更新（3 个以上 issue）
- 项目状态变更
- 创建多个 issue
- 代码变更后的同步操作

**何时使用直接执行：**
- 单个 issue 查询
- 查看 issue 详情
- 快速状态检查
- 需要即时结果的操作

并行执行模式详见 **sync.md**。

## 关键要求

### Issue → 项目 → 计划

**每个 issue 必须关联到项目。每个项目必须关联到计划。**

| 实体 | 必须关联到 | 缺失后果 |
|------|-----------|----------|
| Issue | 项目 | 在项目看板中不可见 |
| 项目 | 计划 | 在路线图中不可见 |

完整的项目创建检查清单见 **projects.md**。

---

## 约定

### Issue 状态

- **已分配给我**：设为 `state: "Todo"`
- **未分配**：设为 `state: "Backlog"`

### 标签

使用**基于领域的标签分类体系**。详见 docs/labels.md。

**核心规则：**
- 一个类型标签：`feature`、`bug`、`refactor`、`chore`、`spike`
- 1-2 个领域标签：`security`、`backend`、`frontend` 等
- 适用时添加范围标签：`blocked`、`breaking-change`、`tech-debt`

```bash
# Validate labels
npx tsx scripts/linear-ops.ts labels validate "feature,security"

# Suggest labels for issue
npx tsx scripts/linear-ops.ts labels suggest "Fix XSS vulnerability"
```

## SDK 自动化脚本

**仅在 MCP 工具不够用时使用。** 涉及循环、映射或批量更新的复杂操作，用 `@linear/sdk` 编写 TypeScript 脚本。详见 `sdk.md`：

- 完整脚本模式和模板
- 常见自动化示例（批量更新、筛选、报表）
- 工具选择标准

脚本提供完整类型提示，多步操作比原生 GraphQL 更易调试。

## GraphQL API

**仅作后备。** 在 MCP 或 SDK 不支持的操作时使用。

完整文档见 **api.md**，包括：
- 认证与配置
- 查询和变更示例
- 超时处理模式
- MCP 超时替代方案
- Shell 脚本兼容性

**快速临时查询：**

```bash
npx tsx ~/.claude/skills/linear/scripts/query.ts "query { viewer { name } }"
```

## 项目与计划

高级项目和计划管理模式见 **projects.md**。

**快速参考** — 常用项目命令：

```bash
# Create project linked to initiative
npx tsx scripts/linear-ops.ts create-project "Phase X: Name" "My Initiative"

# Update project status
npx tsx scripts/linear-ops.ts project-status "Phase X" in-progress
npx tsx scripts/linear-ops.ts project-status "Phase X" completed

# Link/unlink projects to initiatives
npx tsx scripts/linear-ops.ts link-initiative "Phase X" "My Initiative"
npx tsx scripts/linear-ops.ts unlink-initiative "Phase X" "Old Initiative"
```

**projects.md 中的关键主题：**
- 项目创建检查清单（必填步骤）
- Content 与 Description 字段区别
- 创建前先发现
- 工作前验证代码库
- 子 issue 管理
- 项目状态更新
- 项目进展报告

---


## 何时使用此技能

管理 Linear issue、项目和团队

当需要管理 Linear issue、项目和团队时使用此技能。
## 同步模式（批量操作）

代码变更到 Linear 的批量同步见 **sync.md**。

**快速同步命令：**

```bash
# Bulk update issues to Done
npx tsx scripts/linear-ops.ts status Done ENG-101 ENG-102 ENG-103

# Update project status
npx tsx scripts/linear-ops.ts project-status "My Project" completed
```

---

## 参考

| 文档 | 用途 |
|------|------|
| api.md | GraphQL API 参考、超时处理 |
| sdk.md | SDK 自动化模式 |
| sync.md | 批量同步模式 |
| projects.md | 项目与计划管理 |
| troubleshooting.md | 常见问题、MCP 调试 |
| docs/labels.md | 标签分类体系 |

**外部链接：** [Linear MCP 文档](https://linear.app/docs/mcp.md)

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 输出不能替代环境特定的验证、测试或专家评审。
- 如缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清。