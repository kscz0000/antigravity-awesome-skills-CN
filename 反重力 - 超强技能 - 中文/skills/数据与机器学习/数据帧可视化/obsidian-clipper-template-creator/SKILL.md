---
name: obsidian-clipper-template-creator
description: Obsidian Web Clipper 模板创建指南。当用户要求创建新的剪藏模板、了解可用变量或格式化剪藏内容时使用。
risk: safe
source: community
date_added: "2026-02-27"
---

# Obsidian Web Clipper 模板创建器

此技能帮助你为 Obsidian Web Clipper 创建可导入的 JSON 模板。

## 何时使用
- 你需要创建或优化一个可导入的 Obsidian Web Clipper 模板。
- 你需要将网站的真实 DOM、Schema 数据和选择器映射到有效的剪藏模板中。
- 你需要在将 JSON 交给用户之前进行选择器验证和模板逻辑指导。

## 工作流程

1. **识别用户意图：** 特定网站（YouTube）、特定类型（食谱），还是一般剪藏？
2. **检查现有 Base：** 用户可能已在 `Bases/` 中定义了 Base Schema。
    - **操作：** 读取 `Bases/*.base` 以找到匹配的类别（例如 `Recipes.base`）。
    - **操作：** 使用 Base 中定义的属性来构建 Clipper 模板属性。
    - 详见 [references/bases-workflow.md](references/bases-workflow.md)。
3. **获取并分析参考 URL：** 针对真实页面验证变量。
    - **操作：** 向用户请求要剪藏内容的示例 URL（如果未提供）。
    - **操作（必需）：** 使用 **WebFetch** 获取页面内容；如果 WebFetch 不可用，使用浏览器 DOM 快照。参见 [references/analysis-workflow.md](references/analysis-workflow.md)。
    - **操作：** 分析 HTML 中的 Schema.org JSON、Meta 标签和 CSS 选择器。
    - **操作（必需）：** 针对获取的内容验证每个选择器。不要猜测选择器。
    - 参见 [references/analysis-workflow.md](references/analysis-workflow.md) 了解分析技巧。
4. **起草 JSON：** 按照 Schema 创建有效的 JSON 对象。
    - 参见 [references/json-schema.md](references/json-schema.md)。
5. **考虑模板逻辑：** 对可选区块使用条件判断（例如仅在存在时显示营养信息），对列表数据使用循环，使用变量赋值避免重复表达式，对缺失变量使用回退值。仅在逻辑能改善模板时使用逻辑；保持简单模板的简洁性。参见 [references/logic.md](references/logic.md)。
6. **验证变量：** 确保所选变量（预设、Schema、选择器）存在于你的分析结果中。
    - **操作（必需）：** 如果选择器无法从获取的内容中验证，明确说明并请求另一个 URL。
    - 参见 [references/variables.md](references/variables.md)。

## 选择器验证规则

- **始终验证选择器**——在回复前针对实时页面内容进行验证。
- **绝不猜测选择器。** 如果无法访问 DOM 或元素缺失，请求另一个 URL 或截图。
- **优先使用稳定的选择器**（data 属性、语义角色、唯一 ID），而非脆弱的 class 链。
- **记录目标元素**——在推理过程中说明（例如"关于侧边栏段落"）以减少不匹配。

## 输出格式

**始终**将最终结果输出为用户可复制导入的 JSON 代码块。

Clipper 模板编辑器会验证模板语法。
如果使用模板逻辑（条件判断、循环、变量赋值），请确保遵循 [references/logic.md](references/logic.md) 和官方 [Logic](https://help.obsidian.md/web-clipper/logic) 文档中的语法，以便模板通过验证。

```json
{
  "schemaVersion": "0.1.0",
  "name": "My Template",
  ...
}
```

## 资源

- [references/variables.md](references/variables.md) - 可用数据变量。
- [references/filters.md](references/filters.md) - 格式化过滤器。
- [references/json-schema.md](references/json-schema.md) - JSON 结构文档。
- [references/logic.md](references/logic.md) - 模板逻辑。
- [references/bases-workflow.md](references/bases-workflow.md) - 如何将 Bases 映射到模板。
- [references/analysis-workflow.md](references/analysis-workflow.md) - 如何验证页面数据。

### 官方文档

- [Variables](https://help.obsidian.md/web-clipper/variables)
- [Filters](https://help.obsidian.md/web-clipper/filters)
- [Logic](https://help.obsidian.md/web-clipper/logic)
- [Templates](https://help.obsidian.md/web-clipper/templates)

## 示例

参见 [assets/](assets/) 中的 JSON 示例。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
