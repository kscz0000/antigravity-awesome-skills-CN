---
name: skill-writer
description: 按照 Agent Skills 规范创建和改进智能体技能。适用于被要求创建、编写或更新技能时。触发词：创建技能、编写技能、更新技能、create skill、write skill、update skill、技能编写
risk: unknown
source: community
---

# 技能编写器

将此作为技能创建和改进的唯一规范工作流。
首要成功条件：在编写前最大化高价值输入覆盖，使最终技能的盲区最小化。

仅加载任务所需的路径：

| 任务 | 读取 |
|------|------|
| 设置技能类别和必需维度 | `references/mode-selection.md` |
| 应用深度与简洁的写作约束 | `references/design-principles.md` |
| 为此技能选择结构模式 | `references/skill-patterns.md` |
| 为流程密集型技能选择工作流编排模式 | `references/workflow-patterns.md` |
| 为确定性质量选择输出格式模式 | `references/output-patterns.md` |
| 选择工作流路径和必需输出 | `references/mode-selection.md` |
| 按技能类型加载代表性综合示例 | `references/examples/*.md` |
| 使用深度门控综合外部/本地来源 | `references/synthesis-path.md` |
| 编写或更新 SKILL.md 及支持文件 | `references/authoring-path.md` |
| 优化技能描述和触发精度 | `references/description-optimization.md` |
| 使用正面/负面/修复示例进行迭代 | `references/iteration-path.md` |
| 评估行为并比较基线与使用技能后的效果（可选量化） | `references/evaluation-path.md` |
| 注册和验证技能变更 | `references/registration-validation.md` |

## 步骤 1：确定目标和路径

1. 确定目标技能路径和预期操作（`create`、`update`、`synthesize`、`iterate`）。
2. 读取 `references/mode-selection.md` 并选择所需路径。
3. 对技能分类（`workflow-process`、`integration-documentation`、`security-review`、`skill-authoring`、`generic`）。
4. 如果类别或深度需求不明确，提出一个直接问题；否则说明明确的假设。

## 步骤 2：需要时运行综合

读取 `references/synthesis-path.md`。

1. 收集并评分相关来源，附带出处。
2. 摄取外部内容时应用信任和安全规则。
3. 产出有来源支持的决策和覆盖/缺口状态。
4. 技能为混合类型时，从 `references/examples/*.md` 加载一个或多个配置文件。
5. 对技能编写工作流强制执行基线来源包。
6. 在进入编写前强制执行深度门控。

## 步骤 3：从结果/示例改进时先运行迭代

当选定路径包含 `iteration` 时（例如操作为 `iterate`），先读取 `references/iteration-path.md`。

1. 捕获并匿名化示例，附带出处。
2. 对工作集和留出集重新评估技能行为。
3. 基于正面/负面/证据提出改进建议。
4. 将具体的行为差异带入编写阶段。

当选定路径不包含 `iteration` 时跳过此步骤。

## 步骤 4：编写或更新技能制品

读取 `references/authoring-path.md`。

1. 以祈使语气编写或更新 `SKILL.md`，描述应富含触发词。
2. 仅在有充分理由时创建聚焦的参考文件和脚本。
3. 遵循 `references/skill-patterns.md`、`references/workflow-patterns.md` 和
   `references/output-patterns.md` 以确保结构和输出确定性。
4. 对于编写/生成器技能，在参考文件中包含转换后的示例：
   - 正常路径
   - 安全/健壮变体
   - 反模式 + 修正版本

## 步骤 5：优化描述质量

读取 `references/description-optimization.md`。

1. 验证应触发和不应触发的查询集。
2. 通过针对性的描述编辑减少误触发和漏触发。
3. 保持触发语言在 Codex 和 Claude 之间通用。

## 步骤 6：评估结果

读取 `references/evaluation-path.md`。

1. 默认运行轻量级定性检查（推荐）。
2. 对于集成/文档和技能编写技能，包含 `references/evaluation-path.md` 中的简洁深度评分标准。
3. 仅在请求或风险需要时运行更深入的评估方案和量化基线对比。
4. 记录结果和未解决的风险。

## 步骤 7：注册和验证

读取 `references/registration-validation.md`。

1. 应用仓库注册步骤。
2. 使用严格深度门控运行快速验证。
3. 拒绝未通过深度门控或必需制品检查的浅层输出。

## 输出格式

返回：

1. `总结`
2. `已做的变更`
3. `验证结果`
4. `未解决的缺口`

## 使用场景
当处理与上述主要领域或功能相关的任务时使用此技能。

## 局限性
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
