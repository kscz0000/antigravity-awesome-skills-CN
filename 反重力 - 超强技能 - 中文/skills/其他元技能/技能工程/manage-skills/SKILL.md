---
name: manage-skills
description: 跨 11 种工具（Cursor、Claude、Agents、Windsurf、Copilot、Codex、Cline、Aider、Continue、Roo Code、Augment）发现、列出、创建、编辑、切换、复制、移动和删除 AI 智能体技能。当用户要求"管理技能""列出技能""创建技能""复制技能"等操作时使用。
risk: critical
source: community
source_repo: umutbozdag/agent-skills-manager
source_type: community
---

# 管理 AI 智能体技能

可直接在终端中管理所有主流 AI 编码工具的技能和规则。本技能介绍各工具的目录结构、文件格式和操作方式。

## 使用时机

用户需要查看、创建、编辑、启用、禁用、复制、移动或删除本地 AI 智能体技能或规则文件时使用。

## 支持的工具与路径

### 基于目录的工具（多技能）

每个技能位于独立子目录中，包含带 YAML frontmatter 的 `SKILL.md` 文件。

| 工具 | 全局路径 | 项目路径 |
|------|----------|----------|
| Agents | `~/.agents/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` |
| Cursor | `~/.cursor/skills/<name>/SKILL.md` | `.cursor/skills/<name>/SKILL.md` |
| Claude | `~/.claude/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` |
| Windsurf | `~/.windsurf/rules/<name>/<name>.md` | `.windsurf/rules/<name>/<name>.md` |
| Cline | `~/.cline/rules/<name>/<name>.md` | `.cline/rules/<name>/<name>.md` |
| Continue | `~/.continue/rules/<name>/<name>.md` | `.continue/rules/<name>/<name>.md` |
| Roo Code | `~/.roo/rules/<name>/<name>.md` | `.roo/rules/<name>/<name>.md` |

### 单文件工具（一个配置文件）

| 工具 | 全局路径 | 项目路径 |
|------|----------|----------|
| Copilot | `~/.github/copilot-instructions.md` | `.github/copilot-instructions.md` |
| Codex | `~/.codex/AGENTS.md` | `.codex/AGENTS.md` |
| Aider | `~/.aider.conf.yml` | `.aider.conf.yml` |
| Augment | `~/augment-guidelines.md` | `augment-guidelines.md` |

### Cursor 插件（只读）

插件技能缓存在 `~/.cursor/plugins/cache/<org>/<plugin>/<version>/skills/<name>/SKILL.md`，由 Cursor 管理，不应直接编辑。

## 技能文件格式

基于目录的工具（Agents、Cursor、Claude）使用 YAML frontmatter：

```markdown
---
name: skill-name
description: Brief description of what this skill does
---

# Skill Name

Skill instructions go here. The AI agent reads this content
when the skill is activated.
```

Windsurf、Cline、Continue 和 Roo Code 的技能为普通 `.md` 文件（frontmatter 可选）。

## 操作

### 列出所有技能

```bash
# List skills for a specific tool
ls ~/.agents/skills/
ls ~/.cursor/skills/
ls ~/.claude/skills/
ls ~/.windsurf/rules/
ls ~/.cline/rules/
ls ~/.continue/rules/
ls ~/.roo/rules/

# Count total skills across all tools
echo "Agents: $(ls ~/.agents/skills/ 2>/dev/null | wc -l | tr -d ' ')"
echo "Cursor: $(ls ~/.cursor/skills/ 2>/dev/null | wc -l | tr -d ' ')"
echo "Claude: $(ls ~/.claude/skills/ 2>/dev/null | wc -l | tr -d ' ')"
echo "Windsurf: $(ls ~/.windsurf/rules/ 2>/dev/null | wc -l | tr -d ' ')"
echo "Cline: $(ls ~/.cline/rules/ 2>/dev/null | wc -l | tr -d ' ')"
echo "Continue: $(ls ~/.continue/rules/ 2>/dev/null | wc -l | tr -d ' ')"
echo "Roo: $(ls ~/.roo/rules/ 2>/dev/null | wc -l | tr -d ' ')"

# Check single-file tools
test -f ~/.github/copilot-instructions.md && echo "Copilot: exists" || echo "Copilot: not found"
test -f ~/.codex/AGENTS.md && echo "Codex: exists" || echo "Codex: not found"
test -f ~/.aider.conf.yml && echo "Aider: exists" || echo "Aider: not found"
test -f ~/augment-guidelines.md && echo "Augment: exists" || echo "Augment: not found"
```

### 读取技能

```bash
cat ~/.cursor/skills/my-skill/SKILL.md
```

### 创建新技能

```bash
# For Agents/Cursor/Claude (SKILL.md format)
mkdir -p ~/.agents/skills/my-new-skill
cat > ~/.agents/skills/my-new-skill/SKILL.md << 'EOF'
---
name: my-new-skill
description: What this skill does
---

# My New Skill

Instructions for the agent go here.
EOF

# For Windsurf/Cline/Continue/Roo (plain .md format)
mkdir -p ~/.windsurf/rules/my-new-rule
cat > ~/.windsurf/rules/my-new-rule/my-new-rule.md << 'EOF'
# My New Rule

Instructions go here.
EOF

# For single-file tools
cat > .github/copilot-instructions.md << 'EOF'
Instructions for Copilot go here.
EOF
```

### 启用 / 禁用技能

禁用时会将文件重命名为 `.disabled`，工具会忽略它但内容保留：

```bash
# Disable
mv ~/.cursor/skills/my-skill/SKILL.md ~/.cursor/skills/my-skill/SKILL.md.disabled

# Enable
mv ~/.cursor/skills/my-skill/SKILL.md.disabled ~/.cursor/skills/my-skill/SKILL.md
```

### 在工具间复制技能

```bash
# Copy from Cursor to Claude
cp -r ~/.cursor/skills/my-skill ~/.claude/skills/my-skill

# Copy from Agents to Windsurf (adapt format)
mkdir -p ~/.windsurf/rules/my-skill
cp ~/.agents/skills/my-skill/SKILL.md ~/.windsurf/rules/my-skill/my-skill.md
```

### 移动技能

```bash
mv ~/.cursor/skills/my-skill ~/.agents/skills/my-skill
```

### 删除技能

```bash
rm -rf ~/.cursor/skills/my-skill
```

### 从全局复制到项目作用域

```bash
cp -r ~/.cursor/skills/my-skill .cursor/skills/my-skill
```

### 跨工具搜索技能

```bash
# Search by name
find ~/.agents/skills ~/.cursor/skills ~/.claude/skills ~/.windsurf/rules ~/.cline/rules ~/.continue/rules ~/.roo/rules -maxdepth 1 -type d 2>/dev/null | sort

# Search by content
grep -rl "search term" ~/.agents/skills/ ~/.cursor/skills/ ~/.claude/skills/ 2>/dev/null
```

### 查找已禁用的技能

```bash
find ~/.agents/skills ~/.cursor/skills ~/.claude/skills -name "*.disabled" 2>/dev/null
```

## 使用规范

- 用户要求"管理技能""列出技能""创建技能""复制技能到 X"等操作时，按上述路径和格式执行。
- 删除技能前必须确认。
- 在格式不同的工具间复制时（如 Cursor 的 SKILL.md 到 Windsurf 的普通 .md），需调整文件命名。
- 项目级技能覆盖同名全局技能。
- 单文件工具（Copilot、Codex、Aider、Augment）的编辑即替换整个文件内容。
- 创建技能时，目录名使用 kebab-case（如 `my-new-skill`）。

## 限制
- 仅在任务明确符合上述范围时使用本技能。
- 输出不能替代环境验证、测试或专家审查。
- 缺少必要输入、权限、安全边界或成功标准时，停下来询问确认。
