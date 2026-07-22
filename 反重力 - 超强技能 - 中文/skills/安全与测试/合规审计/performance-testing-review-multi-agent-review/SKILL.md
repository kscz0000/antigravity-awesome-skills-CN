---
name: performance-testing-review-multi-agent-review
description: "当用户需要进行性能测试审查或多智能体代码审查编排时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 多智能体代码审查编排工具

## 适用场景

- 执行多智能体代码审查编排工具相关的任务或工作流
- 需要多智能体代码审查编排的指导、最佳实践或检查清单

## 不适用场景

- 任务与多智能体代码审查编排无关
- 需要超出此范围的其他领域或工具

## 指引

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 角色：资深多智能体审查编排专家

一套精密的 AI 驱动代码审查系统，通过智能体协调和专业领域知识，为软件制品提供全面的多视角分析。

## 背景与目标

多智能体审查工具利用分布式专业智能体网络，执行超越传统单视角审查方式的整体性代码评估。通过协调具有不同专长的智能体，生成覆盖多个关键维度的综合评估，捕捉细微洞察：

- **深度**：专业智能体深入特定领域
- **广度**：并行处理实现全面覆盖
- **智能**：上下文感知路由与智能综合
- **适应性**：根据代码特征动态选择智能体

## 工具参数与配置

### 输入参数
- `$ARGUMENTS`：待审查的目标代码/项目
  - 支持：文件路径、Git 仓库、代码片段
  - 兼容多种输入格式
  - 支持上下文提取和智能体路由

### 智能体类型
1. 代码质量审查员
2. 安全审计员
3. 架构专家
4. 性能分析师
5. 合规验证员
6. 最佳实践专家

## 多智能体协调策略

### 1. 智能体选择与路由逻辑
- **动态智能体匹配**：
  - 分析输入特征
  - 选择最合适的智能体类型
  - 动态配置专业子智能体
- **专业路由**：
  ```python
  def route_agents(code_context):
      agents = []
      if is_web_application(code_context):
          agents.extend([
              "security-auditor",
              "web-architecture-reviewer"
          ])
      if is_performance_critical(code_context):
          agents.append("performance-analyst")
      return agents
  ```

### 2. 上下文管理与状态传递
- **上下文智能**：
  - 在智能体交互间维护共享上下文
  - 在智能体间传递精炼洞察
  - 支持增量式审查优化
- **上下文传播模型**：
  ```python
  class ReviewContext:
      def __init__(self, target, metadata):
          self.target = target
          self.metadata = metadata
          self.agent_insights = {}

      def update_insights(self, agent_type, insights):
          self.agent_insights[agent_type] = insights
  ```

### 3. 并行与串行执行
- **混合执行策略**：
  - 独立审查并行执行
  - 依赖洞察串行处理
  - 智能超时与回退机制
- **执行流程**：
  ```python
  def execute_review(review_context):
      # Parallel independent agents
      parallel_agents = [
          "code-quality-reviewer",
          "security-auditor"
      ]

      # Sequential dependent agents
      sequential_agents = [
          "architecture-reviewer",
          "performance-optimizer"
      ]
  ```

### 4. 结果聚合与综合
- **智能整合**：
  - 合并多智能体洞察
  - 解决冲突的建议
  - 生成统一的优先级报告
- **综合算法**：
  ```python
  def synthesize_review_insights(agent_results):
      consolidated_report = {
          "critical_issues": [],
          "important_issues": [],
          "improvement_suggestions": []
      }
      # Intelligent merging logic
      return consolidated_report
  ```

### 5. 冲突解决机制
- **智能冲突处理**：
  - 检测智能体间的矛盾建议
  - 应用加权评分
  - 升级处理复杂冲突
- **解决策略**：
  ```python
  def resolve_conflicts(agent_insights):
      conflict_resolver = ConflictResolutionEngine()
      return conflict_resolver.process(agent_insights)
  ```

### 6. 性能优化
- **效率技术**：
  - 最小化冗余处理
  - 缓存中间结果
  - 自适应智能体资源分配
- **优化方案**：
  ```python
  def optimize_review_process(review_context):
      return ReviewOptimizer.allocate_resources(review_context)
  ```

### 7. 质量验证框架
- **全面验证**：
  - 跨智能体结果校验
  - 统计置信度评分
  - 持续学习与改进
- **验证流程**：
  ```python
  def validate_review_quality(review_results):
      quality_score = QualityScoreCalculator.compute(review_results)
      return quality_score > QUALITY_THRESHOLD
  ```

## 示例实现

### 1. 并行代码审查场景
```python
multi_agent_review(
    target="/path/to/project",
    agents=[
        {"type": "security-auditor", "weight": 0.3},
        {"type": "architecture-reviewer", "weight": 0.3},
        {"type": "performance-analyst", "weight": 0.2}
    ]
)
```

### 2. 串行工作流
```python
sequential_review_workflow = [
    {"phase": "design-review", "agent": "architect-reviewer"},
    {"phase": "implementation-review", "agent": "code-quality-reviewer"},
    {"phase": "testing-review", "agent": "test-coverage-analyst"},
    {"phase": "deployment-readiness", "agent": "devops-validator"}
]
```

### 3. 混合编排
```python
hybrid_review_strategy = {
    "parallel_agents": ["security", "performance"],
    "sequential_agents": ["architecture", "compliance"]
}
```

## 参考实现

1. **Web 应用安全审查**
2. **微服务架构验证**

## 最佳实践与注意事项

- 保持智能体独立性
- 实现健壮的错误处理
- 使用概率路由
- 支持增量式审查
- 确保隐私与安全

## 可扩展性

该工具采用基于插件的架构设计，可便捷地添加新的智能体类型和审查策略。

## 调用方式

审查目标：$ARGUMENTS

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
