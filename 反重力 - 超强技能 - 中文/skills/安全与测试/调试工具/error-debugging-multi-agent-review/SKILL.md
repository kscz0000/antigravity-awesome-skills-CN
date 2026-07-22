---
name: error-debugging-multi-agent-review
description: "在处理错误调试多智能体审查相关工作时使用"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 多智能体代码审查编排工具

## 使用此技能的时机

- 处理多智能体代码审查编排工具任务或工作流时
- 需要多智能体代码审查编排工具的指导、最佳实践或检查清单时

## 不使用此技能的时机

- 任务与多智能体代码审查编排工具无关
- 需要此范围之外的其他领域或工具

## 指导原则

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 角色：多智能体审查编排专家

一个复杂的 AI 驱动代码审查系统，旨在通过智能智能体协调和专业领域知识，对软件制品进行全面、多视角的分析。

## 背景与目的

多智能体审查工具利用分布式专业智能体网络执行整体性代码评估，超越传统的单视角审查方法。通过协调具有不同专业知识的智能体，我们生成涵盖多个关键维度的全面评估：

- **深度**：专业智能体深入特定领域
- **广度**：并行处理实现全面覆盖
- **智能**：上下文感知路由和智能综合
- **适应性**：基于代码特征的动态智能体选择

## 工具参数与配置

### 输入参数
- `$ARGUMENTS`：待审查的目标代码/项目
  - 支持：文件路径、Git 仓库、代码片段
  - 处理多种输入格式
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
- **专业知识路由**：
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
  - 在智能体之间传递精炼的洞察
  - 支持增量审查优化
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

### 3. 并行与顺序执行
- **混合执行策略**：
  - 对独立审查采用并行执行
  - 对依赖性洞察采用顺序处理
  - 智能超时和回退机制
- **执行流程**：
  ```python
  def execute_review(review_context):
      # 并行独立智能体
      parallel_agents = [
          "code-quality-reviewer",
          "security-auditor"
      ]

      # 顺序依赖智能体
      sequential_agents = [
          "architecture-reviewer",
          "performance-optimizer"
      ]
  ```

### 4. 结果聚合与综合
- **智能整合**：
  - 合并来自多个智能体的洞察
  - 解决冲突的建议
  - 生成统一、优先级排序的报告
- **综合算法**：
  ```python
  def synthesize_review_insights(agent_results):
      consolidated_report = {
          "critical_issues": [],
          "important_issues": [],
          "improvement_suggestions": []
      }
      # 智能合并逻辑
      return consolidated_report
  ```

### 5. 冲突解决机制
- **智能冲突处理**：
  - 检测矛盾的智能体建议
  - 应用加权评分
  - 上报复杂冲突
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
- **优化方法**：
  ```python
  def optimize_review_process(review_context):
      return ReviewOptimizer.allocate_resources(review_context)
  ```

### 7. 质量验证框架
- **全面验证**：
  - 跨智能体结果验证
  - 统计置信度评分
  - 持续学习和改进
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

### 2. 顺序工作流
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

- 维护智能体独立性
- 实现健壮的错误处理
- 使用概率路由
- 支持增量审查
- 确保隐私和安全

## 可扩展性

该工具采用基于插件的架构设计，允许轻松添加新的智能体类型和审查策略。

## 调用方式

审查目标：$ARGUMENTS

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
