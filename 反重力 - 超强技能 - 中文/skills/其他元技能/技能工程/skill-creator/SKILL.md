---
name: skill-creator
description: "按照Anthropic官方最佳实践创建新的CLI技能，无需手动配置。此技能自动化头脑风暴、模板应用、验证和安装过程，同时保持渐进式披露模式和写作风格标准。触发词：创建技能、新建技能、技能生成、技能创建、skill创建、CLI技能"
category: meta
risk: safe
source: community
tags: "[automation, scaffolding, skill-creation, meta-skill]"
date_added: "2026-02-27"
---

# skill-creator

## 用途

按照Anthropic官方最佳实践创建新的CLI技能，无需手动配置。此技能自动化头脑风暴、模板应用、验证和安装过程，同时保持渐进式披露模式和写作风格标准。

## 使用场景

此技能适用于以下情况：
- 用户想要用自定义功能扩展CLI
- 用户需要按照官方标准创建技能
- 用户想要用可重用技能自动化重复的CLI任务
- 用户需要将领域知识打包成技能格式
- 用户想要本地和全局技能安装选项

## 核心能力

1. **交互式头脑风暴** - 协作会议定义技能用途和范围
2. **提示词增强** - 可选集成prompt-engineer技能进行优化
3. **模板应用** - 从标准化模板自动生成文件
4. **验证** - 针对Anthropic标准的YAML、内容和样式检查
5. **安装** - 本地仓库或带符号链接的全局安装
6. **进度跟踪** - 每个步骤的可视化完成状态指示器

## 步骤 0：发现

在开始技能创建之前，收集运行时信息：

```bash
# 检测可用平台
COPILOT_INSTALLED=false
CLAUDE_INSTALLED=false
CODEX_INSTALLED=false

if command -v gh &>/dev/null && gh copilot --version &>/dev/null 2>&1; then
    COPILOT_INSTALLED=true
fi

if [[ -d "$HOME/.claude" ]]; then
    CLAUDE_INSTALLED=true
fi

if [[ -d "$HOME/.codex" ]]; then
    CODEX_INSTALLED=true
fi

# 确定工作目录
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
SKILLS_REPO="$REPO_ROOT"

# 检查是否在cli-ai-skills仓库中
if [[ ! -d "$SKILLS_REPO/.github/skills" ]]; then
    echo "⚠️  Not in cli-ai-skills repository. Creating standalone skill."
    STANDALONE=true
fi

# 从git配置获取用户信息
AUTHOR=$(git config user.name || echo "Unknown")
EMAIL=$(git config user.email || echo "")
```

**关键信息：**
- 目标平台（Copilot、Claude、Codex或全部三个）
- 安装偏好（本地、全局或两者）
- 技能名称和用途
- 技能类型（通用、代码、文档、分析）

## 主要工作流程

### 进度跟踪指南

在整个工作流程中，在每个阶段开始前显示可视化进度条，让用户保持知情。进度条格式为：

```
[████████████░░░░░░] 60% - 步骤 3/5: 创建 SKILL.md
```

**格式规范：**
- 20个字符宽（使用 █ 表示已填充，░ 表示空）
- 百分比基于当前步骤（步骤1=20%，步骤2=40%，步骤3=60%，步骤4=80%，步骤5=100%）
- 步骤计数器显示当前/总数（例如"步骤 3/5"）
- 当前阶段的简短描述

**使用以下命令显示进度条：**
```bash
echo "[████░░░░░░░░░░░░░░] 20% - 步骤 1/5: 头脑风暴与规划"
```

### 阶段 1：头脑风暴与规划

**进度：** 在开始此阶段前显示：
```bash
echo "[████░░░░░░░░░░░░░░] 20% - 步骤 1/5: 头脑风暴与规划"
```

显示进度：
```
╔══════════════════════════════════════════════════════════════╗
║     🛠️  技能创建器 - 创建新技能                              ║
╠══════════════════════════════════════════════════════════════╣
║ → 阶段 1: 头脑风暴                     [10%]               ║
║ ○ 阶段 2: 提示词优化                                       ║
║ ○ 阶段 3: 文件生成                                         ║
║ ○ 阶段 4: 验证                                            ║
║ ○ 阶段 5: 安装                                            ║
╠══════════════════════════════════════════════════════════════╣
║ 进度: ███░░░░░░░░░░░░░░░░░░░░░░░░░░░  10%              ║
╚══════════════════════════════════════════════════════════════╝
```

**询问用户：**

1. **这个技能应该做什么？**（自由描述）
   - 示例："通过分析堆栈跟踪帮助用户调试Python代码"
   
2. **何时应该触发？**（提供3-5个触发短语）
   - 示例："调试Python错误"、"分析堆栈跟踪"、"修复Python异常"

3. **这是什么类型的技能？**
   - [ ] 通用（默认模板）
   - [ ] 代码生成/修改
   - [ ] 文档创建/维护
   - [ ] 分析/调查

4. **应支持哪些平台？**
   - [ ] GitHub Copilot CLI
   - [ ] Claude Code
    - [ ] Codex
    - [ ] 全部三个（推荐）

5. **提供一句话描述**（将出现在元数据中）
   - 示例："分析Python堆栈跟踪并建议修复方案"

**捕获响应并准备下一阶段。**

### 阶段 2：提示词增强（可选）

**进度：** 在开始此阶段前显示：
```bash
echo "[████████░░░░░░░░░░] 40% - 步骤 2/5: 提示词增强"
```

更新进度：
```
╔══════════════════════════════════════════════════════════════╗
║ ✓ 阶段 1: 头脑风暴                                          ║
║ → 阶段 2: 提示词优化                 [30%]               ║
╠══════════════════════════════════════════════════════════════╣
║ 进度: █████████░░░░░░░░░░░░░░░░░░░░░  30%              ║
╚══════════════════════════════════════════════════════════════╝
```

**询问用户：**
"是否想使用prompt-engineer技能优化技能描述？"
- [ ] 是 - 使用prompt-engineer增强清晰度和结构
- [ ] 否 - 使用当前描述继续

如果选**是**：
1. 检查prompt-engineer技能是否可用
2. 以当前描述作为输入调用
3. 与用户一起审查增强输出
4. 询问："接受增强版还是保留原版？"

如果选**否**或prompt-engineer不可用：
- 使用原始用户输入继续

### 阶段 3：文件生成

**进度：** 在开始此阶段前显示：
```bash
echo "[████████████░░░░░░] 60% - 步骤 3/5: 文件生成"
```

更新进度：
```
╔══════════════════════════════════════════════════════════════╗
║ ✓ 阶段 1: 头脑风暴                                          ║
║ ✓ 阶段 2: 提示词优化                                        ║
║ → 阶段 3: 文件生成                   [50%]               ║
╠══════════════════════════════════════════════════════════════╣
║ 进度: ███████████████░░░░░░░░░░░░░░░  50%              ║
╚══════════════════════════════════════════════════════════════╝
```

**生成技能结构：**

```bash
# 将技能名称转换为kebab-case
SKILL_NAME=$(echo "$USER_INPUT" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

# 创建目录
if [[ "$PLATFORM" =~ "copilot" ]]; then
    mkdir -p ".github/skills/$SKILL_NAME"/{references,examples,scripts}
fi

if [[ "$PLATFORM" =~ "claude" ]]; then
    mkdir -p ".claude/skills/$SKILL_NAME"/{references,examples,scripts}
fi

if [[ "$PLATFORM" =~ "codex" ]]; then
    mkdir -p ".codex/skills/$SKILL_NAME"/{references,examples,scripts}
fi
```

**应用模板：**

1. **SKILL.md** - 使用相应模板：
   - `skill-template-copilot.md`、`skill-template-claude.md` 或 `skill-template-codex.md`
   - 替换占位符：
     - `{{SKILL_NAME}}` → kebab-case名称
     - `{{DESCRIPTION}}` → 一行描述
     - `{{TRIGGERS}}` → 逗号分隔的触发短语
     - `{{PURPOSE}}` → 头脑风暴中的详细用途
     - `{{AUTHOR}}` → 来自git配置
     - `{{DATE}}` → 当前日期（YYYY-MM-DD）
     - `{{VERSION}}` → "1.0.0"

2. **README.md** - 使用 `readme-template.md`：
   - 面向用户的文档（300-500字）
   - 包含安装说明
   - 添加使用示例

3. **References/**（可选但推荐）：
   - 创建 `detailed-guide.md` 用于扩展文档（2k-5k字）
   - 将冗长内容移到此处，保持SKILL.md在2k字以内

**文件创建命令：**

```bash
# 应用模板并替换
sed "s/{{SKILL_NAME}}/$SKILL_NAME/g; \
     s/{{DESCRIPTION}}/$DESCRIPTION/g; \
     s/{{AUTHOR}}/$AUTHOR/g; \
     s/{{DATE}}/$(date +%Y-%m-%d)/g" \
    resources/templates/skill-template-copilot.md \
    > ".github/skills/$SKILL_NAME/SKILL.md"

# 创建README
sed "s/{{SKILL_NAME}}/$SKILL_NAME/g" \
    resources/templates/readme-template.md \
    > ".github/skills/$SKILL_NAME/README.md"

# 如果选择了Codex，应用模板
if [[ "$PLATFORM" =~ "codex" ]]; then
    sed "s/{{SKILL_NAME}}/$SKILL_NAME/g; \
         s/{{DESCRIPTION}}/$DESCRIPTION/g; \
         s/{{AUTHOR}}/$AUTHOR/g; \
         s/{{DATE}}/$(date +%Y-%m-%d)/g" \
        resources/templates/skill-template-codex.md \
        > ".codex/skills/$SKILL_NAME/SKILL.md"
    
    sed "s/{{SKILL_NAME}}/$SKILL_NAME/g" \
        resources/templates/readme-template.md \
        > ".codex/skills/$SKILL_NAME/README.md"
fi
```

**显示创建的结构：**
```
✅ 已创建:
   .github/skills/your-skill-name/ (如果选择了Copilot)
   .claude/skills/your-skill-name/ (如果选择了Claude)
   .codex/skills/your-skill-name/ (如果选择了Codex)
   ├── SKILL.md (832 行)
   ├── README.md (347 行)
   ├── references/
   ├── examples/
   └── scripts/
```

### 阶段 4：验证

**进度：** 在开始此阶段前显示：
```bash
echo "[████████████████░░] 80% - 步骤 4/5: 验证"
```

更新进度：
```
╔══════════════════════════════════════════════════════════════╗
║ ✓ 阶段 3: 文件生成                                          ║
║ → 阶段 4: 验证                      [70%]               ║
╠══════════════════════════════════════════════════════════════╣
║ 进度: █████████████████████░░░░░░░░░  70%              ║
╚══════════════════════════════════════════════════════════════╝
```

**运行验证脚本：**

```bash
# 验证YAML前置元数据
scripts/validate-skill-yaml.sh ".github/skills/$SKILL_NAME"

# 验证内容质量
scripts/validate-skill-content.sh ".github/skills/$SKILL_NAME"
```

**预期输出：**
```
🔍 验证 YAML 前置元数据...
✅ YAML 前置元数据有效！

🔍 验证内容...
✅ 字数优秀: 1847 字
✅ 内容验证完成！
```

**如果验证失败：**
- 显示具体错误
- 提供自动修复选项（常见问题）
- 要求用户手动修正复杂问题

**常见自动修复：**
- 将第二人称转换为祈使形式
- 将描述重新格式化为第三人称
- 添加缺失的必填字段

### 阶段 5：安装

**进度：** 在开始此阶段前显示：
```bash
echo "[████████████████████] 100% - 步骤 5/5: 安装"
```

更新进度：
```
╔══════════════════════════════════════════════════════════════╗
║ ✓ 阶段 4: 验证                                              ║
║ → 阶段 5: 安装                      [90%]               ║
╠══════════════════════════════════════════════════════════════╣
║ 进度: ██████████████████████████░░░░░  90%              ║
╚══════════════════════════════════════════════════════════════╝
```

**询问用户：**
"你想如何安装此技能？"

- [ ] **仅仓库** - 文件创建在 `.github/skills/`（在仓库中时有效）
- [ ] **全局安装** - 在 `~/.copilot/skills/` 创建符号链接（处处有效）
- [ ] **两者** - 仓库 + 全局符号链接（推荐，git pull时自动更新）
- [ ] **跳过安装** - 仅创建文件

**如果选择全局安装：**

```bash
# 检测要安装的平台
INSTALL_TARGETS=()

if [[ "$COPILOT_INSTALLED" == "true" ]] && [[ "$PLATFORM" =~ "copilot" ]]; then
    INSTALL_TARGETS+=("copilot")
fi

if [[ "$CLAUDE_INSTALLED" == "true" ]] && [[ "$PLATFORM" =~ "claude" ]]; then
    INSTALL_TARGETS+=("claude")
fi

if [[ "$CODEX_INSTALLED" == "true" ]] && [[ "$PLATFORM" =~ "codex" ]]; then
    INSTALL_TARGETS+=("codex")
fi

# 要求用户确认检测到的平台
echo "检测到的平台: ${INSTALL_TARGETS[*]}"
echo "为这些平台安装？ [Y/n]"
```

**安装过程：**

```bash
# GitHub Copilot CLI
if [[ " ${INSTALL_TARGETS[*]} " =~ " copilot " ]]; then
    ln -sf "$SKILLS_REPO/.github/skills/$SKILL_NAME" \
           "$HOME/.copilot/skills/$SKILL_NAME"
    echo "✅ 已为 GitHub Copilot CLI 安装"
fi

# Claude Code
if [[ " ${INSTALL_TARGETS[*]} " =~ " claude " ]]; then
    ln -sf "$SKILLS_REPO/.claude/skills/$SKILL_NAME" \
           "$HOME/.claude/skills/$SKILL_NAME"
    echo "✅ 已为 Claude Code 安装"
fi

# Codex
if [[ " ${INSTALL_TARGETS[*]} " =~ " codex " ]]; then
    ln -sf "$SKILLS_REPO/.codex/skills/$SKILL_NAME" \
           "$HOME/.codex/skills/$SKILL_NAME"
    echo "✅ 已为 Codex 安装"
fi
```

**验证安装：**

```bash
# 检查符号链接
ls -la ~/.copilot/skills/$SKILL_NAME 2>/dev/null
ls -la ~/.claude/skills/$SKILL_NAME 2>/dev/null
ls -la ~/.codex/skills/$SKILL_NAME 2>/dev/null
```

### 阶段 6：完成

**进度：** 显示完成消息：
```bash
echo "[████████████████████] 100% - ✓ 技能创建成功！"
```

更新进度：
```
╔══════════════════════════════════════════════════════════════╗
║ ✓ 阶段 5: 安装                                              ║
║ ✅ 技能创建完成！                                           ║
╠══════════════════════════════════════════════════════════════╣
║ 进度: ██████████████████████████████  100%              ║
╚══════════════════════════════════════════════════════════════╝
```

**显示摘要：**

```
🎉 技能创建成功！

📦 技能名称: your-skill-name
📁 位置: .github/skills/your-skill-name/
🔗 已安装: 全局 (Copilot + Claude)

📋 创建的文件:
   ✅ SKILL.md (1,847 字)
   ✅ README.md (423 字)
   ✅ references/ (空，准备扩展文档)
   ✅ examples/ (空，准备代码示例)
   ✅ scripts/ (空，准备工具脚本)

🚀 后续步骤:
   1. 测试技能: 在CLI中尝试触发短语
   2. 添加示例: 在examples/中创建可工作的代码示例
   3. 扩展文档: 在references/中添加详细指南
   4. 提交变更: git add .github/skills/your-skill-name && git commit
   5. 分享: 推送到仓库供团队使用

💡 专业提示:
   - 保持SKILL.md在2,000字以内（当前: 1,847）
   - 将详细内容移到references/文件夹
   - 将可执行脚本添加到scripts/文件夹
   - 用真实使用示例更新README.md
   - 提交前运行验证: scripts/validate-skill-yaml.sh
```

## 错误处理

### 平台检测问题

如果无法检测平台：
```
⚠️  无法检测 GitHub Copilot CLI 或 Claude Code
    
是否：
1. 仅安装到仓库（在仓库中时有效）
2. 手动指定平台
3. 跳过安装
```

### 模板未找到

如果模板缺失：
```
❌ 错误: 在 resources/templates/ 未找到模板

此技能需要 cli-ai-skills 仓库结构。

选项:
1. 克隆 cli-ai-skills: git clone <repo-url>
2. 手动创建最小技能结构
3. 退出并先设置模板
```

### 验证失败

如果内容不符合标准：
```
⚠️  发现验证问题:

1. YAML: 描述未使用第三人称格式
   预期: "This skill should be used when..."
   发现: "Use this skill when..."
   
2. 内容: 字数过多 (5,342 字，最大 5,000)
   建议: 将详细部分移到 references/

自动修复？ [Y/n]
```

### 安装冲突

如果符号链接已存在：
```
⚠️  技能已安装在 ~/.copilot/skills/your-skill-name

选项:
1. 覆盖现有安装
2. 重命名新技能
3. 跳过安装
4. 安装到不同位置
```

## 捆绑资源

此技能在子目录中包含额外资源：

### references/

需要时加载的详细文档：
- `anthropic-best-practices.md` - Anthropic官方技能开发指南
- `writing-style-guide.md` - 写作标准和示例
- `progressive-disclosure.md` - 内容组织模式
- `validation-checklist.md` - 提交前质量检查

### examples/

演示技能使用的工作示例：
- `basic-skill-creation.md` - 简单技能创建演练
- `advanced-skill-bundled-resources.md` - 带references/的复杂技能
- `global-installation.md` - 系统范围安装技能

### scripts/

技能维护的可执行工具：
- `validate-all-skills.sh` - 批量验证仓库中的所有技能
- `update-skill-version.sh` - 升级版本并更新变更日志
- `generate-skill-index.sh` - 自动生成技能目录

## 技术实现说明

**模板替换：**
- 使用 `sed` 进行简单替换
- 精确保留YAML格式
- 使用正确转义处理多行描述

**符号链接策略：**
- 始终使用绝对路径: `ln -sf /full/path/to/source ~/.copilot/skills/name`
- 安装完成前验证符号链接
- 优势: 仓库拉取时自动更新

**验证集成：**
- 安装前运行验证
- 发现严重错误时阻止安装
- 警告仅供参考

**Git集成：**
- 从 `git config user.name` 提取作者
- 使用仓库根检测: `git rev-parse --show-toplevel`
- 遵循 `.gitignore` 模式

## 质量标准

**SKILL.md要求：**
- 1,500-2,000字（理想）
- 5,000字以内（最大）
- 第三人称描述格式
- 祈使/不定式写作风格
- 渐进式披露模式

**README.md要求：**
- 300-500字
- 面向用户的语言
- 清晰的安装说明
- 实用的使用示例

**验证检查：**
- YAML前置元数据完整性
- 描述格式（第三人称）
- 字数限制
- 写作风格（无第二人称）
- 必填字段存在

## 参考资料

- **Anthropic官方技能开发指南:** https://github.com/anthropics/claude-plugins-official/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md
- **仓库:** https://github.com/yourusername/cli-ai-skills
- **写作风格指南:** `resources/templates/writing-style-guide.md`
- **进度跟踪模板:** `resources/templates/progress-tracker.md`

## 限制
- 仅当任务明确匹配上述范围时使用此技能
- 不要将输出视为环境特定验证、测试或专家审查的替代品
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清