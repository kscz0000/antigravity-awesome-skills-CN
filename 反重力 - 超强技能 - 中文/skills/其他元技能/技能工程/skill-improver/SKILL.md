---
name: skill-improver
description: "使用 skill-reviewer 智能体迭代改进 Claude Code 技能，直到达到质量标准。适用于修复存在多个质量问题的技能、迭代新技能直到达标、或用自动化修复-审查循环替代手动编辑。触发词：改进技能、修复技能质量、迭代技能、技能审查、技能改进、improve skill、fix skill、iterate skill"
risk: unknown
source: community
---

# 技能改进方法论

使用 skill-reviewer 智能体迭代改进 Claude Code 技能，直到达到质量标准。

## 前置条件

需要 `plugin-dev` 插件，该插件提供 `skill-reviewer` 智能体。

验证是否已启用：运行 `/plugins` — `plugin-dev` 应出现在列表中。如果缺失，请从 Trail of Bits 插件仓库安装。

## 核心循环

1. **审查** - 对目标技能调用 skill-reviewer
2. **分类** - 按严重程度解析问题
3. **修复** - 处理关键和主要问题
4. **评估** - 修复前先检查次要问题的有效性
5. **重复** - 持续直到达到质量标准

## 使用场景
- 修复存在多个质量问题的技能
- 迭代新技能直到达标
- 用自动化修复-审查循环替代手动编辑
- 跨技能的一致性质量管控

## 不适用场景

- **一次性审查**：直接使用 `/skill-reviewer`
- **快速单点修复**：直接编辑文件
- **非技能文件**：仅适用于 SKILL.md 文件
- **实验性技能**：手动迭代在探索阶段更有控制力

## 问题分类

### 关键问题（必须立即修复）

这些问题会阻塞技能加载或导致运行时故障：

- 缺少必需的 frontmatter 字段（name、description）— Claude 无法索引或触发该技能
- YAML frontmatter 语法无效 — 解析失败，技能无法加载
- 引用的文件不存在 — Claude 跟踪链接时会产生运行时错误
- 文件路径损坏 — 同上，会导致工具故障

### 主要问题（必须修复）

这些问题会显著降低技能效果：

- 触发描述薄弱或模糊 — Claude 可能无法识别何时使用该技能
- 写作视角错误（使用第二人称"你"而非祈使语气）— 与 Claude 的执行模型不一致
- SKILL.md 超过 500 行且未使用 references/ — 过载上下文，降低理解度
- 缺少"使用场景"或"不适用场景"章节 — 项目质量标准要求
- 描述未指明触发条件 — 技能可能永远不会被选中

### 次要问题（修复前需评估）

这些是打磨项，可能改善也可能不改善技能：

- 主观风格偏好 — 审查者的品味可能与作者不同
- 可选增强 — 可能增加复杂度但收益不对等
- "锦上添花"的改进 — 实施前考虑成本收益
- 格式建议 — 通常有效但影响较小

## 次要问题评估

在实施任何次要问题修复前，先评估：

1. **这是否真正的改进？** - 是增加实际价值还是仅仅满足偏好？
2. **这是否可能是误报？** - 审查者是否误解了上下文？**
3. **这是否真的能帮助 Claude 使用该技能？** - 聚焦于功能性改进

只实施明显有益的次要修复。skill-reviewer 可能产生误报。

## 调用 skill-reviewer

使用 plugin-dev 插件中的 skill-reviewer 智能体。请求审查时请 Claude 执行：

> 使用 plugin-dev:skill-reviewer 智能体审查 [SKILL_PATH] 处的技能。提供详细的按严重程度分类的质量评估报告。

将 `[SKILL_PATH]` 替换为技能目录的绝对路径（例如 `/path/to/plugins/my-plugin/skills/my-skill`）。

## 修复循环示例

**第 1 轮 — skill-reviewer 输出：**
```text
Critical: SKILL.md:1 - Missing required 'name' field in frontmatter
Major: SKILL.md:3 - Description uses second person ("you should use")
Major: Missing "When NOT to Use" section
Minor: Line 45 is verbose
```

**已应用修复：**
- 在 frontmatter 中添加了 name 字段
- 将描述改写为第三人称
- 添加了"不适用场景"章节

**第 2 轮 — 再次运行 skill-reviewer 验证修复：**
```text
Minor: Line 45 is verbose
```

**次要问题评估：**
第 45 行当前表述已经足够清晰。冗长部分提供了有用的上下文。跳过。

**所有关键/主要问题已解决。输出完成标记：**
```
<skill-improvement-complete>
```

注意：标记必须出现在输出中。类似"quality bar met"或"looks good"的表述不会停止循环。

## 完成标准

**关键**：停止钩子仅检查下方的显式标记。没有其他信号会终止循环。

完成时输出此标记：

```
<skill-improvement-complete>
```

**何时输出标记：**

1. **skill-reviewer 报告"Pass"** 或 **未发现问题** → 立即输出标记
2. **所有关键和主要问题已修复** 且你已验证修复有效 → 输出标记
3. **剩余问题仅为次要问题** 且你已评估为误报或不值得修复 → 输出标记

**何时不输出标记：**

- 任何关键问题未修复
- 任何主要问题未修复
- 你尚未运行 skill-reviewer 验证修复是否有效

标记是完成循环的唯一方式。类似"looks good"或"quality bar met"的自然语言不会停止循环。

## 需要拒绝的借口

- "我先标记完成，以后再回来修" - 现在就修复问题
- "这个次要问题看起来不对，我要全部跳过" - 逐一评估每个问题
- "审查者太严格了" - 质量标准存在是有原因的
- "已经够好了" - 如果还有主要问题，就不够好

## 局限性
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
