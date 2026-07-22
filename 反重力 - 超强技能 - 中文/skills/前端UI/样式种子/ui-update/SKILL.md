---
name: ui-update
description: 更新项目中的 StyleSeed 引擎 —— 分析过时的内容并安全地执行更新。触发词：更新 StyleSeed、StyleSeed 升级、升级 StyleSeed 引擎、ui-update、SS 更新、StyleSeed 引擎更新、迁移到最新 StyleSeed、ss-update
risk: unknown
source: https://github.com/bitjaru/styleseed/tree/main/engine/.claude/skills/ss-update
source_repo: bitjaru/styleseed
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/bitjaru/styleseed/blob/main/LICENSE
---

# StyleSeed 更新助手
## 何时使用

当你需要更新项目中的 StyleSeed 引擎时使用本技能 —— 它会分析过时的内容并安全地执行更新。


## 何时不要使用

- 首次安装设置 → 使用 `/ss-setup`
- 只需要新增一个组件或皮肤 —— 手动复制该文件即可
- 项目与上游已经严重偏离 —— 先手动做差异审查
- 更新用户代码或组件 —— 本技能只更新引擎文件，不更新你的自定义 UI

自动检测并更新当前项目中的 StyleSeed 文件。

## 先让用户安心

更新是 **安全且可逆的**。更新是累加式的 —— 新的规则、组件、皮肤和技能会被添加进去；你的 `theme.css`、你的组件以及你的应用代码永远不会被覆盖；设计规则也只会新增（不会以破坏性的方式变更）。大版本号跳跃看似改动很多，但实际上几乎全是新增。**不要警告用户构建会出问题**，除非你真的发现了变更的组件或导入 API。告诉用户：先提交代码，复制新的规则和技能，跑一次构建，如果有异常就执行 `git reset --hard` —— 他们不会永久性地搞坏项目。

## 操作步骤

### 步骤 1：检测当前安装情况

扫描项目以定位 StyleSeed 文件的位置：

```bash
# Find DESIGN-LANGUAGE.md
find . -name "DESIGN-LANGUAGE.md" -not -path "*/node_modules/*"

# Find CLAUDE.md
find . -name "CLAUDE.md" -not -path "*/node_modules/*"

# Find skills (ss-* is current; ui-*/ux-* are legacy names to migrate from)
find . -path "*/.claude/skills/ss-*" -o -path "*/.claude/skills/ui-*" -o -path "*/.claude/skills/ux-*" | head -20

# Find theme.css
find . -name "theme.css" -not -path "*/node_modules/*"

# Find .cursorrules
find . -name ".cursorrules"
```

报告扫描到了什么以及它们的位置。

### 步骤 2：检查 StyleSeed 版本

**先做快速检查** —— 在不克隆仓库的情况下对比本地版本与已发布版本：
```bash
# local marker (may be absent on older installs)
cat engine/VERSION 2>/dev/null || cat VERSION 2>/dev/null || echo "unknown"
# latest published version + what's new
curl -s https://styleseed-demo.vercel.app/version.json
```
如果本地版本已经和 `version.json` 中的 `version` 一致，告诉用户他们已是最新版本并停止。否则报告 `whatsNew` 的内容并继续。

然后通过克隆或拉取来真正对比文件：
```bash
if [ -d "/tmp/styleseed" ]; then
  cd /tmp/styleseed && git pull
else
  git clone https://github.com/bitjaru/styleseed.git /tmp/styleseed
fi
```

对比以下内容：
- `engine/VERSION`（或 `version.json`）与本地副本 —— 这是唯一权威来源
- DESIGN-LANGUAGE.md 的规则数量与目录结构
- `.claude/skills/` 中已存在的技能与上游的差异（不要硬编码数量 —— 列出差异清单）
- 是否存在 `CLAUDE.md`、`AGENTS.md`、`.cursorrules`（三者要齐备）
- 新的引擎文档（VISUAL-CRAFT.md、APP-PLAYBOOKS.md、PAGE-TYPES.md）

### 步骤 3：报告并询问

向用户展示需要更新的内容：

```
StyleSeed Update Report:

Current state:
- DESIGN-LANGUAGE.md: [location] — [old/current version indicator]
- Skills: [count] found (latest: 12)
- Golden Rules: [yes/no]
- .cursorrules: [yes/no]

Recommended updates:
1. ✅ [safe] Update skills (X → 12)
2. ✅ [safe] Add .cursorrules
3. ⚠️ [review] Update DESIGN-LANGUAGE.md ([old line count] → [new line count])
4. ⚠️ [merge] Add Golden Rules to CLAUDE.md (won't overwrite existing content)

Shall I proceed? (I'll ask before each ⚠️ item)
```

### 步骤 4：执行更新

按顺序处理每一项更新：

**始终安全的操作（无需询问直接执行）：**
- 复制技能：`cp -r /tmp/styleseed/engine/.claude/skills/ .claude/skills/`
- 复制 .cursorrules（如不存在）：`cp /tmp/styleseed/engine/.cursorrules .cursorrules`

**执行前需询问：**

对于 DESIGN-LANGUAGE.md：
- 展示差异摘要：新增了多少条规则，新增了哪些章节
- 询问："是否更新 DESIGN-LANGUAGE md？（Y/N）"
- 确认后：复制到检测到的位置

对于 CLAUDE.md（Golden Rules）：
- 检查是否已存在 Golden Rules 章节
- 如果没有：询问 "是否向你的 CLAUDE.md 添加 Golden Rules 章节？这会在文件顶部新增 10 行。你已有的内容保持不变。"
- 如果已有：将 Golden Rules 插入到第一个标题之后

**绝对不要触碰：**
- theme.css —— 提示用户 "你的 theme.css（皮肤）未做任何改动。"
- components/ —— 提示用户 "你的组件未做任何改动。运行 `/ss-lint` 检查是否符合规范。"

### 步骤 5：总结

```
Update complete!

✅ Skills: 12 (added X new)
✅ .cursorrules: added
✅ DESIGN-LANGUAGE.md: updated to latest
✅ Golden Rules: added to CLAUDE.md

Not touched:
- theme.css (your skin)
- components/ (your code)

Next: run /ss-lint on your pages to check for rule violations.
```

## 重要提示

- 永远不要覆盖 theme.css
- 永远不要覆盖项目专属的 CLAUDE.md —— 只能合并 Golden Rules 章节
- 未经用户明确同意，永远不要覆盖组件
- 在做出改动前始终展示将发生哪些变化
- 不确定时，请向用户询问

## 局限性

- 仅当任务与上游源和本地项目上下文明确匹配时才使用本技能。
- 在应用任何变更前，请验证命令、生成的代码、依赖、凭据以及外部服务的行为。
- 不要把示例当作环境专属测试、安全审查或针对破坏性/高成本操作的审批的替代品。
