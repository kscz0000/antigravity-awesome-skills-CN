# 工作流模式

## 顺序工作流

对于复杂任务，将操作分解为清晰、顺序的步骤。通常在 SKILL.md 的开头给 Claude 一个过程概述会很有帮助：

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

## 条件工作流

对于具有分支逻辑的任务，引导 Claude 完成决策点：

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```