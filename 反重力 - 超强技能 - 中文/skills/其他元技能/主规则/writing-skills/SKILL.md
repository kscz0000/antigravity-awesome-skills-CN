---
name: writing-skills
description: "在创建、更新或改进智能体技能时使用。触发词：技能创建、技能更新、技能改进、agent skills"
category: meta
risk: unknown
source: community
date_added: "2026-02-27"
---

# 编写技能（卓越篇）

技能创建卓越性的调度器。使用下方决策树找到合适的模板与标准。

## ⚡ 快速决策树

### 你需要做什么？

1. **创建一个新技能：**
   - 是否简单（单文件，<200 行）？→ [Tier 1 架构](references/tier-1-simple/README.md)
   - 是否复杂（多概念，200-1000 行）？→ [Tier 2 架构](references/tier-2-expanded/README.md)
   - 是否为大型平台（10+ 产品，AWS、Convex）？→ [Tier 3 架构](references/tier-3-platform/README.md)

2. **改进现有技能：**
   - 修复"它太长了" -> [模块化（Tier 3）](references/templates/tier-3-platform.md)
   - 修复"AI 忽略规则" -> [反合理化](references/anti-rationalization/README.md)
   - 修复"用户找不到它" -> [CSO（搜索优化）](references/cso/README.md)

3. **验证合规性：**
   - 检查元数据/命名 -> [标准](references/standards/README.md)
   - 添加测试 -> [测试指南](references/testing/README.md)

## 📚 组件索引

| 组件 | 用途 |
|-----------|---------|
| **[CSO](references/cso/README.md)** | "面向 LLM 的 SEO"。如何编写能够触发的 description。 |
| **[标准](references/standards/README.md)** | 文件命名、YAML frontmatter、目录结构。 |
| **[反合理化](references/anti-rationalization/README.md)**| 如何编写智能体不会忽略的规则。 |
| **[测试](references/testing/README.md)** | 如何确保你的技能真正有效。 |

## 🛠️ 模板

- [技巧型技能](references/templates/technique.md)（How-to）
- [参考型技能](references/templates/reference.md)（文档）
- [纪律型技能](references/templates/discipline.md)（规则）
- [模式型技能](references/templates/pattern.md)（设计模式）

## 何时使用
- 从零创建一个新技能
- 改进智能体忽略的现有技能
- 调试某个技能为何未被触发
- 在团队内统一技能标准

## 工作原理

1. **确定目标** → 使用上方决策树
2. **选择模板** → 从 `references/templates/` 中选择
3. **应用 CSO** → 优化 description 以提升可发现性
4. **加入反合理化** → 针对纪律型技能
5. **测试** → RED-GREEN-REFACTOR 循环

## 快速示例

```yaml
---
name: my-technique
description: Use when [specific symptom occurs].
metadata:
  category: technique
  triggers: error-text, symptom, tool-name
---

# My Technique

## When to Use
- [Symptom A]
- [Error message]
```

## 常见错误

| 错误 | 修复方法 |
|---------|-----|
| description 概述了工作流 | 仅使用"Use when..."触发词 |
| 没有 `metadata.triggers` | 添加 3+ 关键词 |
| 通用名称（如 "helper"） | 使用动名词（如 `creating-skills`） |
| 单体的长 SKILL.md | 拆分到 `references/` |

更多内容见 [gotchas.md](gotchas.md)。

## ✅ 部署前检查清单

部署任何技能之前：

- [ ] `name` 字段与目录名完全一致
- [ ] `SKILL.md` 文件名全大写
- [ ] description 以 "Use when..." 开头
- [ ] `metadata.triggers` 包含 3+ 关键词
- [ ] 总行数 < 500（更多内容放入 `references/`）
- [ ] 交叉引用中不使用 `@` 强制加载
- [ ] 使用真实场景测试过

## 🔗 相关技能

- **opencode-expert**：用于 OpenCode 环境配置
- 使用 `/write-skill` 命令进行引导式技能创建

## 示例

**创建一个 Tier 1 技能：**
```bash
mkdir -p ~/.config/opencode/skills/my-technique
touch ~/.config/opencode/skills/my-technique/SKILL.md
```

**创建一个 Tier 2 技能：**
```bash
mkdir -p ~/.config/opencode/skills/my-skill/references/core
touch ~/.config/opencode/skills/my-skill/{SKILL.md,gotchas.md}
touch ~/.config/opencode/skills/my-skill/references/core/README.md
```

## 局限性
- 仅当任务明确匹配上述范围时才使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。
