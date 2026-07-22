---
name: lint-and-validate
description: "强制要求：每次代码变更后必须运行相应的验证工具。代码无错前不得结束任务。当用户要求'lint检查'、'代码验证'、'运行lint'、'检查代码质量'、'类型检查'、'代码规范检查'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Lint 与验证技能

> **强制要求：** 每次代码变更后必须运行相应的验证工具。代码无错前不得结束任务。

### 按生态系统的操作流程

#### Node.js / TypeScript
1. **Lint/修复：** `npm run lint` 或 `npx eslint "path" --fix`
2. **类型检查：** `npx tsc --noEmit`
3. **安全审计：** `npm audit --audit-level=high`

#### Python
1. **Linter (Ruff)：** `ruff check "path" --fix`（快速且现代）
2. **安全检查 (Bandit)：** `bandit -r "path" -ll`
3. **类型检查 (MyPy)：** `mypy "path"`

## 质量循环
1. **编写/编辑代码**
2. **运行审计：** `npm run lint && npx tsc --noEmit`
3. **分析报告：** 检查"FINAL AUDIT REPORT"部分。
4. **修复并重复：** 不允许提交存在"FINAL AUDIT"失败的代码。

## 错误处理
- `lint` 失败时：立即修复样式或语法问题。
- `tsc` 失败时：在继续之前纠正类型不匹配。
- 未配置工具时：检查项目根目录的 `.eslintrc`、`tsconfig.json`、`pyproject.toml`，并建议创建。

---
**严格规则：** 未通过这些检查的代码不得提交或报告为"完成"。

---

## 脚本

| 脚本 | 用途 | 命令 |
|------|------|------|
| `scripts/lint_runner.py` | 统一 lint 检查 | `python scripts/lint_runner.py <project_path>` |
| `scripts/type_coverage.py` | 类型覆盖率分析 | `python scripts/type_coverage.py <project_path>` |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不能替代针对具体环境的验证、测试或专家审查。
- 缺少必要输入、权限、安全边界或成功标准时，停下来请求澄清。
