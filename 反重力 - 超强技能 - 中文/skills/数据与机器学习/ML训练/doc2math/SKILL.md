---
name: doc2math
description: 将叙述性技术文档转换为基于原文的数学问题规范（MPS），包含变量、约束、目标与不确定性。将文档形式化为数学问题、从论文中提取数学结构、识别规范中缺失要素。触发词：doc2math、文档转数学、问题规范、MPS、数学形式化、变量提取、约束识别、目标提取、不确定性分析、形式化建模。
risk: safe
source: community
date_added: "2026-05-31"
---

# DOC2MATH — 文档到数学的问题规范转换

## 何时使用本技能

- "将这个问题的描述形式化为数学表达"
- "从这篇论文章节中提取数学结构"
- "这份规范中包含哪些变量、约束和目标？"
- "把这个应用题转换为结构化的 MPS"
- "找出该问题建模中缺失的部分"

## 零推断协议（强制要求）

1. **封闭世界** —— 文档中未陈述的内容，输出中也不得出现
2. **溯源规则** —— 每个元素必须引用准确的源文本片段（`"evidence"` 字段）
3. **禁止静默补全** —— 未知值使用 `null`；类型不明确时使用 `"ambiguous"`
4. **推断标注** —— 结构性的推断需打上 `"inferred": true` 并附 `"inference_basis"`
5. **MISSING 标记** —— 提及但定义不足的元素使用 `"status": "MISSING"` 并附 `"missing_reason"`
6. **禁止虚构数学** —— 不得引入源文本中没有的等式或数值

## 局限性

- 不会编造源文档中缺失的等式、定义域、数值或假设。
- 需要足够的源文本来为每个抽取的元素提供引用；对于内容稀疏的提示，应返回带有明确缺失信息标记的结果。
- 输出的是形式化规范，而非已求解的优化模型或证明。

## 工作原理

### 步骤 1 — 接收文档

接受文档文本、研究节选、问题描述或规范作为输入。

### 步骤 2 — 分类

识别 `problem_class`：`optimization | classification | simulation | proof | estimation | other`（优化 | 分类 | 仿真 | 证明 | 估计 | 其他）

### 步骤 3 — 提取 MPS 组件

**变量（Variables）** —— `id`、`name`、`symbol`、`type`、`domain`、`units`、`role`、`evidence`、`inferred`、`status`

**算子（Operators）** —— `id`、`name`、`symbol`、`arity`、`acts_on`、`produces`、`evidence`、`inferred`

**约束（Constraints）** —— `id`、`type`、`expression`、`variables_involved`、`evidence`、`hardness`、`inferred`、`status`

**目标（Objectives）** —— `id`、`direction`（minimize/maximize/satisfy/find/prove，即最小化/最大化/满足/寻找/证明）、`expression`、`variables_involved`、`evidence`、`inferred`

**不确定性（Uncertainty）** —— `id`、`type`（stochastic/epistemic/measurement/model/none_stated，即随机/认知/测量/模型/未声明）、`affects`、`characterization`、`evidence`、`status`

### 步骤 4 — 暴露缺失信息

识别文档暗示但未明确说明的内容：`missing_information[]`，包含 `element`、`needed_for`、`missing_reason`。

### 步骤 5 — 校验与评分

`validation_flags`：
- `has_complete_objectives`：true / false / partial
- `has_bounded_variables`：true / false / partial
- `has_evidence_for_all_elements`：true / false / partial
- `inference_count`：整数
- `missing_count`：整数
- `overall_formalizability`：HIGH / MEDIUM / LOW（高 / 中 / 低）

## 输出格式

将完整的 MPS 产出为 JSON 对象：

```json
{
  "mps_version": "1.0",
  "source_title": "...",
  "problem_class": "optimization",
  "variables": [...],
  "operators": [...],
  "constraints": [...],
  "objectives": [...],
  "uncertainty": [...],
  "missing_information": [...],
  "validation_flags": {
    "overall_formalizability": "HIGH"
  }
}
```

## 最佳实践

- ✅ 在输出任何元素前，先应用全部 6 条零推断协议规则
- ✅ 应暴露 MISSING 标记而非静默推断 —— 不完整的形式化也是有效输出
- ✅ 每个 `evidence` 字段都应准确引用源文本片段
- ❌ 不得引入源文本中无依据的数学关系

## 其他资源

- 仓库：[thebrierfox/doc2math-skill](https://github.com/thebrierfox/doc2math-skill)
- 完整 BYOK 工具：[ace-license-server-production.up.railway.app/byok/doc2math](https://ace-license-server-production.up.railway.app/byok/doc2math)
- 由 [IntuiTek¹](https://intuitek.ai) (~K¹) 构建 —— MIT 许可证
