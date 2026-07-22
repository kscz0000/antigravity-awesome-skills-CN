---
name: agents-md
description: 当用户要求"创建 AGENTS.md"、"更新 AGENTS.md"、"维护智能体文档"、"设置 CLAUDE.md"，或需要保持智能体指令简洁时使用此技能。强制执行基于研究的最小化、高信号智能体文档最佳实践。触发词：AGENTS.md、CLAUDE.md、智能体文档、智能体配置、agent文档、agent配置、创建AGENTS、更新AGENTS
risk: unknown
source: community
---

# 维护 AGENTS.md

AGENTS.md 是面向智能体的权威文档。保持精简——智能体能力足够，不需要手把手指导。目标控制在 60 行以内；绝不超过 100 行。指令遵循质量随文档长度增加而下降。

## 何时使用

- 用户要求创建、更新或审查 `AGENTS.md` 或 `CLAUDE.md`
- 项目需要从实际工具链和仓库结构中提取简洁、高信号的智能体指令
- 现有智能体文档过长、重复或偏离真实项目约定

## 文件设置

1. 在项目根目录创建 `AGENTS.md`
2. 创建符号链接：`ln -s AGENTS.md CLAUDE.md`

## 写入前准备

分析项目以理解文件应包含什么内容：

1. **包管理器** — 检查锁文件（`pnpm-lock.yaml`、`yarn.lock`、`package-lock.json`、`uv.lock`、`poetry.lock`）
2. **Linter/格式化配置** — 查找 `.eslintrc`、`biome.json`、`ruff.toml`、`.prettierrc` 等（不要在 AGENTS.md 中重复）
3. **CI/构建命令** — 检查 `Makefile`、`package.json` scripts、CI 配置获取权威命令
4. **Monorepo 标识** — 检查 `pnpm-workspace.yaml`、`nx.json`、Cargo workspace 或子目录 `package.json` 文件
5. **现有约定** — 检查现有 CONTRIBUTING.md、docs/ 或 README 模式

## 写入规则

- **标题 + 列表** — 不写段落
- **代码块** — 用于命令和模板
- **引用而非嵌入** — 指向现有文档："参见 `CONTRIBUTING.md` 了解配置"或"遵循 `src/api/routes/` 中的模式"
- **无填充内容** — 不要开场白、结论或客套话
- **信任能力** — 省略显而易见的上下文
- **优先文件级命令** — 使用单文件测试/lint/类型检查命令而非全项目构建
- **不重复 linter** — 代码风格存在于 linter 配置中，不在 AGENTS.md

## 必需章节

### 包管理器

仅说明工具和关键命令：
```markdown
## Package Manager
Use **pnpm**: `pnpm install`, `pnpm dev`, `pnpm test`
```

### 文件级命令

单文件命令比全项目构建更快更省。可用时务必包含：
```markdown
## File-Scoped Commands
| Task | Command |
|------|---------|
| Typecheck | `pnpm tsc --noEmit path/to/file.ts` |
| Lint | `pnpm eslint path/to/file.ts` |
| Test | `pnpm jest path/to/file.test.ts` |
```

### 提交署名

必须包含此章节。智能体应使用自己的身份：
```markdown
## Commit Attribution
AI commits MUST include:
```
Co-Authored-By: (the agent model's name and attribution byline)
```
Example: `Co-Authored-By: Claude Sonnet 4 <noreply@example.com>`
```

### 关键约定

智能体必须遵循的项目特定模式。保持简洁。

## 可选章节

仅在真正需要时添加：
- API 路由模式（展示模板，不要解释）
- CLI 命令（表格格式）
- 文件命名约定
- 项目结构提示（指向关键文件，标记需避免的遗留代码）
- Monorepo 覆盖规则（子目录 `AGENTS.md` 覆盖根目录）

## 反模式

省略以下内容：
- "欢迎使用..."或"本文档解释..."
- "你应该..."或"请记住..."
- 已在配置文件中的 linter/格式化规则（`.eslintrc`、`biome.json`、`ruff.toml`）
- 列出已安装的技能或插件（智能体会自动发现）
- 存在文件级替代方案时的全项目构建命令
- 显而易见的指令（"运行测试"、"写干净的代码"）
- 原因解释（只说做什么）
- 冗长的段落

## 示例结构

```markdown
# Agent Instructions

## Package Manager
Use **pnpm**: `pnpm install`, `pnpm dev`

## Commit Attribution
AI commits MUST include:
```
Co-Authored-By: (the agent model's name and attribution byline)
```

## File-Scoped Commands
| Task | Command |
|------|---------|
| Typecheck | `pnpm tsc --noEmit path/to/file.ts` |
| Lint | `pnpm eslint path/to/file.ts` |
| Test | `pnpm jest path/to/file.test.ts` |

## API Routes
[Template code block]

## CLI
| Command | Description |
|---------|-------------|
| `pnpm cli sync` | Sync data |
```

## 限制

- 仅当任务明确匹配上述范围时使用此技能
- 输出不能替代环境特定验证、测试或专家审查
- 如缺少必需输入、权限、安全边界或成功标准，请停止并请求澄清
