# 代码质量审查者提示词模板

分派代码质量审查子智能体时使用此模板。

**目的：** 验证实现是否精良（整洁、有测试、可维护）

**仅在规格符合性审查通过后分派。**

```
Task tool (superpowers:code-reviewer):
  Use template at requesting-code-review/code-reviewer.md

  WHAT_WAS_IMPLEMENTED: [from implementer's report]
  PLAN_OR_REQUIREMENTS: Task N from [plan-file]
  BASE_SHA: [commit before task]
  HEAD_SHA: [current commit]
  DESCRIPTION: [task summary]
```

**代码审查者返回：** 优点、问题（严重/重要/轻微）、评估
