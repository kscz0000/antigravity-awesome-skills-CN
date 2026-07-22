# skill-creator

**自动化 CLI 技能创建，内置最佳实践。**

## 功能概述

skill-creator 自动化了为 GitHub Copilot CLI 和 Claude Code 创建新 CLI 技能的整个工作流程。它引导您进行头脑风暴，应用标准化模板，验证内容质量，并处理安装——所有这些都遵循 Anthropic 的官方最佳实践。

## 主要特性

- **🎯 交互式头脑风暴** - 协作会话，定义技能目的和范围
- **✨ 模板自动化** - 自动生成文件，零手动配置
- **🔍 质量验证** - 内置 YAML、内容质量和写作风格检查
- **📦 灵活安装** - 选择仅仓库、全局或混合安装
- **📊 可视化进度条** - 实时进度指示器，显示完成状态（例如 `[████████████░░░░░░] 60% - Step 3/5`）
- **🔗 提示词工程师集成** - 可选使用 prompt-engineer 技能进行增强

## 何时使用

在以下情况下使用此技能：
- 按照官方标准创建新的 CLI 技能
- 使用自定义功能扩展 CLI 功能
- 将领域知识打包成可重用的技能格式
- 使用自定义技能自动化重复性 CLI 任务
- 在系统范围内本地或全局安装技能

## 安装

### 前置条件

此技能是 `cli-ai-skills` 仓库的一部分。要使用它：

```bash
# 克隆仓库
git clone https://github.com/yourusername/cli-ai-skills.git
cd cli-ai-skills
```

### 全局安装（推荐）

通过符号链接安装，使技能在任何地方可用：

```bash
# 对于 GitHub Copilot CLI
ln -sf "$(pwd)/.github/skills/skill-creator" ~/.copilot/skills/skill-creator

# 对于 Claude Code
ln -sf "$(pwd)/.claude/skills/skill-creator" ~/.claude/skills/skill-creator
```

**全局安装的优势：**
- 在任何目录中工作
- 当您 `git pull` 仓库时自动更新
- 无需配置文件

### 仅仓库安装

如果您希望仅在此仓库中使用该技能，则无需安装。在 `cli-ai-skills` 目录中工作时，该技能将可用。

## 使用方法

### 基本技能创建

只需请求 CLI 创建新技能：

```bash
# GitHub Copilot CLI
gh copilot "create a new skill for debugging Python errors"

# Claude Code
claude "create a skill that helps with git workflows"
```

该技能将通过可视化进度跟踪引导您完成：
1. **头脑风暴** (20%) - 定义目的、触发条件和类型
2. **提示词增强** (40%, 可选) - 使用 prompt-engineer 技能进行增强
3. **文件生成** (60%) - 从模板创建文件
4. **验证** (80%) - 检查质量和标准
5. **安装** (100%) - 选择本地、全局或两者

每个阶段都会显示进度条：
```
[████████████░░░░░░] 60% - Step 3/5: File Generation
```

### 高级用法

#### 创建代码生成技能

```bash
"Create a code skill that generates React components from descriptions"
```

该技能将：
- 使用专门的 `code-skill-template.md`
- 询问特定框架（React、Vue 等）
- 在 `examples/` 文件夹中包含代码示例

#### 创建文档技能

```bash
"Build a skill that writes API documentation from code"
```

该技能将：
- 使用 `documentation-skill-template.md`
- 询问文档格式
- 设置风格指南的参考

#### 为特定平台安装

```bash
"Create a skill for Copilot only that analyzes TypeScript errors"
```

该技能将：
- 仅在 `.github/skills/` 中生成文件
- 跳过 Claude 特定的安装
- 根据 Copilot 要求进行验证

## 示例演练

以下是创建技能的过程：

```
You: "create a skill for database schema migrations"

[████░░░░░░░░░░░░░░] 20% - Step 1/5: Brainstorming & Planning

What should this skill do?
> Helps users create and manage database schema migrations safely

When should it trigger? (3-5 phrases)
> "create migration", "generate schema change", "migrate database"

What type of skill?
> [×] General purpose

Which platforms?
> [×] Both (Copilot + Claude)

[... continues through all phases ...]

🎉 Skill created successfully!

📦 Skill Name: database-migration
📁 Location: .github/skills/database-migration/
🔗 Installed: Global (Copilot + Claude)
```

## 文件结构

当您创建技能时，会生成以下结构：

```
.github/skills/your-skill-name/
├── SKILL.md              # 主要技能说明（1.5-2k 词）
├── README.md             # 面向用户的文档（此文件）
├── references/           # 详细指南（每个 2k-5k 词）
│   └── （空，准备用于扩展文档）
├── examples/             # 可运行的代码示例
│   └── （空，准备用于示例）
└── scripts/              # 可执行工具
    └── （空，准备用于自动化）
```

## 配置

**无需配置！** 此技能使用运行时发现来：
- 检测已安装的平台（Copilot CLI、Claude Code）
- 自动查找仓库根目录
- 从 git 配置中提取作者信息
- 确定最佳文件位置

## 验证

创建的每个技能都会自动验证：
- ✅ **YAML Frontmatter** - 必需字段和格式
- ✅ **描述格式** - 第三人称、触发短语
- ✅ **字数统计** - 理想 1,500-2,000 词，最多 5,000 词
- ✅ **写作风格** - 祈使句形式，无第二人称
- ✅ **渐进式披露** - 正确的内容组织

## 使用的框架

此技能利用了几个已建立的方法论：

- **渐进式披露** - 3 级内容层次结构（元数据 → SKILL.md → 捆绑资源）
- **捆绑资源模式** - 参考、示例和脚本作为单独文件
- **Anthropic 最佳实践** - 官方技能开发标准
- **零配置设计** - 运行时发现，无硬编码值
- **模板驱动生成** - 所有技能的一致结构

## 故障排除

### "Template not found" 错误

确保您在 `cli-ai-skills` 仓库中或已克隆它：

```bash
git clone https://github.com/yourusername/cli-ai-skills.git
cd cli-ai-skills
```

### "Platform not detected" 警告

如果未检测到平台：
1. 选择"仅仓库"安装
2. 在设置期间手动指定平台
3. 使用提供的命令稍后全局安装

### 验证失败

如果验证发现问题：
- 查看输出中的建议
- 为常见问题选择自动修复
- 为复杂问题手动编辑文件
- 重新运行验证：`scripts/validate-skill-yaml.sh .github/skills/your-skill`

## 高级功能

### 提示词工程师集成

使用 AI 增强您的技能描述：
1. 在第 2 阶段（提示词优化）启用
2. 技能将自动调用 `prompt-engineer`
3. 继续之前查看增强的输出

### 捆绑资源

对于复杂技能，使用捆绑资源：
- **references/** - 详细文档（无字数限制）
- **examples/** - 用户可以运行的代码示例
- **scripts/** - 按需加载的自动化工具

### 版本管理

更新现有技能：
```bash
scripts/update-skill-version.sh your-skill-name 1.1.0
```

## 贡献

创建了有用的技能？分享它：
1. 确保验证通过
2. 添加使用示例
3. 更新主 README.md
4. 提交拉取请求

## 资源

- **写作风格指南：** `resources/templates/writing-style-guide.md`
- **Anthropic 官方指南：** https://github.com/anthropics/claude-plugins-official
- **模板目录：** `resources/templates/`
- **验证脚本：** `scripts/validate-*.sh`

## 支持

如有问题或疑问：
- 查看 `.github/skills/` 中的现有技能作为示例
- 查看 `resources/skills-development.md` 了解方法论
- 在仓库中提交问题

---

**版本：** 1.1.0  
**平台：** GitHub Copilot CLI, Claude Code  
**作者：** Eric Andrade  
**最后更新：** 2026-02-01