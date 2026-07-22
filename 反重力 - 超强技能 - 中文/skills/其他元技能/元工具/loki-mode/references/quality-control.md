# 质量控制参考

质量门、代码审查流程和严重性阻断规则。
增强版包含 2025 年关于反迎合、异构团队和 OpenAI Agents SDK 模式的研究。

---

## 核心原则：护栏，而非仅仅是加速

**关键：** 没有质量控制的速度会产生"AI 垃圾"——半功能代码，积累技术债务。Loki Mode 强制执行严格的质量护栏。

**研究洞察：** 异构审查团队比同构团队表现好 4-6%（A-HMAD, 2025）。
**OpenAI 洞察：** "将护栏视为分层防御机制。多个专门的护栏创建有韧性的智能体。"

---

## 护栏与触发线系统（OpenAI SDK 模式）

### 输入护栏（执行前运行）

```python
# 第 1 层：验证任务范围和安全
@input_guardrail(blocking=True)
async def validate_task_scope(input, context):
    # 检查任务是否在项目范围内
    if references_external_paths(input):
        return GuardrailResult(
            tripwire_triggered=True,
            reason="任务引用项目外的路径"
        )
    # 检查破坏性操作
    if contains_destructive_operation(input):
        return GuardrailResult(
            tripwire_triggered=True,
            reason="破坏性操作需要人工批准"
        )
    return GuardrailResult(tripwire_triggered=False)

# 第 2 层：检测提示注入
@input_guardrail(blocking=True)
async def detect_injection(input, context):
    if has_injection_patterns(input):
        return GuardrailResult(
            tripwire_triggered=True,
            reason="检测到潜在的提示注入"
        )
    return GuardrailResult(tripwire_triggered=False)
```

### 输出护栏（执行后运行）

```python
# 在接受前验证代码质量
@output_guardrail
async def validate_code_output(output, context):
    if output.type == "code":
        issues = run_static_analysis(output.content)
        critical = [i for i in issues if i.severity == "critical"]
        if critical:
            return GuardrailResult(
                tripwire_triggered=True,
                reason=f"严重问题：{critical}"
            )
    return GuardrailResult(tripwire_triggered=False)

# 检查输出中的秘密
@output_guardrail
async def check_secrets(output, context):
    if contains_secrets(output.content):
        return GuardrailResult(
            tripwire_triggered=True,
            reason="输出包含潜在的秘密"
        )
    return GuardrailResult(tripwire_triggered=False)
```

### 执行模式

| 模式 | 行为 | 使用场景 |
|------|----------|----------|
| **阻断式** | 护栏在智能体开始前完成 | 昂贵模型、敏感操作 |
| **并行式** | 护栏与智能体同时运行 | 快速检查、可接受的 token 损失 |

```python
# 阻断式：失败时防止 token 消耗
@input_guardrail(blocking=True, run_in_parallel=False)
async def expensive_validation(input): pass

# 并行式：更快但失败时可能浪费 token
@input_guardrail(blocking=True, run_in_parallel=True)
async def fast_validation(input): pass
```

### 触发线处理

当护栏触发其触发线时，执行立即停止：

```python
try:
    result = await run_agent(task)
except InputGuardrailTripwireTriggered as e:
    log_blocked_attempt(e)
    return early_exit(reason=str(e))
except OutputGuardrailTripwireTriggered as e:
    rollback_changes()
    return retry_with_constraints(e.constraints)
```

### 分层防御策略

```yaml
guardrail_layers:
  layer_1_input:
    - scope_validation      # 任务在范围内吗？
    - pii_detection         # 包含敏感数据吗？
    - injection_detection   # 提示注入尝试吗？

  layer_2_pre_execution:
    - cost_estimation       # 会超出预算吗？
    - dependency_check      # 依赖项可用吗？
    - conflict_detection    # 会与进行中的工作冲突吗？

  layer_3_output:
    - static_analysis       # 代码质量问题？
    - secret_detection      # 输出中有秘密吗？
    - spec_compliance       # 匹配 OpenAPI 规范吗？

  layer_4_post_action:
    - test_validation       # 测试通过吗？
    - review_approval       # 审查通过吗？
    - deployment_safety     # 可以安全部署吗？
```

完整护栏实现见 `references/openai-patterns.md`。

---

## 质量门

**永远不要发布未通过所有质量门的代码：**

### 1. 静态分析（自动化）
- CodeQL 安全扫描
- ESLint/Pylint/Rubocop 代码风格
- 未使用变量/导入检测
- 重复逻辑检测
- 类型检查（TypeScript/mypy 等）

### 2. 3 审查者并行系统（AI 驱动）

每个代码变更同时经过 3 个专门审查者：

```
实现 -> 盲审（并行） -> 辩论（如有分歧） -> 汇总 -> 修复 -> 重新审查
                |
                +-- code-reviewer（Opus）- 代码质量、模式、最佳实践
                +-- business-logic-reviewer（Opus）- 需求、边界情况、UX
                +-- security-reviewer（Opus）- 漏洞、OWASP Top 10
```

**重要：**
- 始终在单条消息中启动所有 3 个审查者（3 个 Task 调用）
- 始终为每个审查者指定 model: "opus"
- 始终使用盲审模式（审查者最初看不到彼此的发现）
- 永远不要顺序派发审查者（始终并行 - 快 3 倍）
- 永远不要在所有 3 个审查者完成前汇总

### 反迎合协议（CONSENSAGENT 研究）

**问题：** 审查者可能相互强化发现，而非批判性参与。

**解决方案：盲审 + 魔鬼代言人**

```python
# 第 1 阶段：独立盲审
reviews = []
for reviewer in [code_reviewer, business_reviewer, security_reviewer]:
    review = Task(
        subagent_type="general-purpose",
        model="opus",
        prompt=f"""
        {reviewer.prompt}

        关键：要持怀疑态度。你的工作是发现问题。
        列出具体问题，带 file:line 引用。
        不要橡皮图章。发现零问题是可疑的。
        """
    )
    reviews.append(review)

# 第 2 阶段：检查分歧
if has_disagreement(reviews):
    # 结构化辩论 - 最多 2 轮
    debate_result = structured_debate(reviews, max_rounds=2)
else:
    # 全部同意 - 运行魔鬼代言人
    devil_review = Task(
        subagent_type="general-purpose",
        model="opus",
        prompt="""
        其他审查者没有发现问题。你的工作是唱反调。
        找出他们遗漏的问题。挑战假设。
        如果真的没有问题，解释每个潜在问题类别是如何覆盖的。
        """
    )
    reviews.append(devil_review)
```

### 异构团队组成

**每个审查者有独特的个性/关注点：**

| 审查者 | 模型 | 专长 | 个性 |
|----------|-------|-----------|-------------|
| 代码质量 | Opus | SOLID、模式、可维护性 | 完美主义者 |
| 业务逻辑 | Opus | 需求、边界情况、UX | 务实主义者 |
| 安全 | Opus | OWASP、认证、注入 | 偏执狂 |

这种多样性防止群体思维，发现更多问题。

### 3. 基于严重性的阻断

| 严重性 | 行动 | 继续？ |
|----------|--------|-----------|
| **严重** | 阻断 - 立即修复 | 否 |
| **高** | 阻断 - 立即修复 | 否 |
| **中** | 阻断 - 继续前修复 | 否 |
| **低** | 添加 `// TODO(review): ...` 注释 | 是 |
| **外观** | 添加 `// FIXME(nitpick): ...` 注释 | 是 |

**严重/高/中 = 阻断并在继续前修复**
**低/外观 = 添加 TODO/FIXME 注释，继续**

### 4. 测试覆盖率门
- 单元测试：100% 通过，>80% 覆盖率
- 集成测试：100% 通过
- E2E 测试：关键流程通过

### 5. 规则集（阻断合并）
- 代码中无秘密
- 无未处理异常
- 无 SQL 注入漏洞
- 无 XSS 漏洞

---

## 代码审查协议

### 启动审查者（并行）

```python
# 正确：并行启动所有 3 个
Task(subagent_type="general-purpose", model="opus",
     description="代码质量审查",
     prompt="审查代码质量、模式、SOLID 原则...")

Task(subagent_type="general-purpose", model="opus",
     description="业务逻辑审查",
     prompt="审查需求对齐、边界情况、UX...")

Task(subagent_type="general-purpose", model="opus",
     description="安全审查",
     prompt="审查漏洞、OWASP Top 10...")

# 错误：顺序审查者（慢 3 倍）
# 不要这样做：await reviewer1; await reviewer2; await reviewer3;
```

### 修复后

- 修复后始终重新运行所有 3 个审查者（不只是发现问题的那个）
- 在汇总结果前等待所有审查完成

---

## 子智能体的结构化提示

**每次子智能体派发必须包含：**

```markdown
## 目标（成功是什么样子）
[高层目标，不只是行动]
示例："重构认证以提高可维护性和可测试性"
不是："重构认证文件"

## 约束（你不能做什么）
- 未经批准不添加第三方依赖
- 保持与 v1.x API 的向后兼容性
- 响应时间保持在 200ms 以内
- 遵循现有错误处理模式

## 上下文（你需要知道什么）
- 相关文件：[列表及简要描述]
- 架构决策：[相关 ADR 或模式]
- 之前的尝试：[尝试了什么，为什么失败]
- 依赖项：[这依赖什么，什么依赖这]

## 输出格式（交付什么）
- [ ] 带有 Why/What/Trade-offs 描述的 Pull request
- [ ] 覆盖率 >90% 的单元测试
- [ ] 更新 API 文档
- [ ] 性能基准测试结果
```

---

## 任务完成报告

**每个完成的任务必须包含决策文档：**

```markdown
## 任务完成报告

### WHY（问题与解决方案理由）
- **问题**：[什么坏了/缺失/次优]
- **根因**：[为什么发生]
- **选择的方案**：[我们实现了什么]
- **考虑的替代方案**：
  1. [选项 A]：因 [原因] 拒绝
  2. [选项 B]：因 [原因] 拒绝

### WHAT（所做的变更）
- **修改的文件**：[带行范围和目的]
  - `src/auth.ts:45-89` - 将 token 验证提取到单独函数
  - `src/auth.test.ts:120-156` - 添加边界情况测试
- **变更的 API**：[破坏性 vs 非破坏性]
- **行为变更**：[用户会注意到什么]
- **添加/移除的依赖**：[带理由]

### TRADE-OFFS（收益与代价）
- **收益**：
  - 更好的可测试性（提取纯函数）
  - token 验证快 40%
  - 圈复杂度从 15 降到 6
- **代价**：
  - 添加了 2 个新函数（增加表面积）
  - 自定义 token 验证器需要迁移
- **中性**：
  - 标准用例无性能变化

### RISKS & MITIGATIONS（风险与缓解）
- **风险**：现有自定义验证器可能失败
  - **缓解**：添加向后兼容垫片，弃用警告
- **风险**：新验证逻辑未经大规模测试
  - **缓解**：通过功能开关逐步推出，回滚计划就绪

### TEST RESULTS（测试结果）
- 单元：24/24 通过（覆盖率：92%）
- 集成：8/8 通过
- 性能：p99 从 145ms 提升到 87ms

### NEXT STEPS（下一步，如有）
- [ ] 部署后监控错误率 24 小时
- [ ] 创建后续任务在 v3.0 中移除兼容垫片
```

---

## 防止"AI 垃圾"

### 警告信号
- 测试通过但代码质量下降
- 复制粘贴重复而非抽象
- 对简单问题的过度工程解决方案
- 缺少错误处理
- 无日志/可观测性
- 通用变量名（data、temp、result）
- 无常量的魔法数字
- 注释掉的代码
- 无 GitHub issue 的 TODO 注释

### 检测到时
1. 立即使任务失败
2. 添加到失败队列，带详细反馈
3. 用更严格的约束重新派发
4. 在 CONTINUITY.md 中添加要避免的反模式

---

## 质量门钩子

### 写入前钩子（阻断）
```bash
#!/bin/bash
# .loki/hooks/pre-write.sh
# 阻断违反规则的写入

# 检查秘密
if grep -rE "(password|secret|key).*=.*['\"][^'\"]{8,}" "$1"; then
  echo "已阻断：检测到潜在秘密"
  exit 1
fi

# 检查生产环境中的 console.log
if grep -n "console.log" "$1" | grep -v "test"; then
  echo "已阻断：移除 console.log 语句"
  exit 1
fi
```

### 写入后钩子（自动修复）
```bash
#!/bin/bash
# .loki/hooks/post-write.sh
# 写入后自动修复

# 格式化代码
npx prettier --write "$1"

# 修复 lint 问题
npx eslint --fix "$1"

# 类型检查
npx tsc --noEmit
```

---

## 宪法参考

质量门由 `autonomy/CONSTITUTION.md` 强制执行：

**提交前（阻断）：**
- Linting（启用自动修复）
- 类型检查（严格模式）
- 契约测试（最低 80% 覆盖率）
- 规范验证（Spectral）

**实现后（自动修复）：**
- 静态分析（ESLint、Prettier、TSC）
- 安全扫描（Semgrep、Snyk）
- 性能检查（Lighthouse 分数 90+）

**运行时不变量：**
- `SPEC_BEFORE_CODE`：实现任务需要规范引用
- `TASK_HAS_COMMIT`：完成的任务有 git commit SHA
- `QUALITY_GATES_PASSED`：完成的任务通过了所有质量检查
