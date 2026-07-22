# 实验室研究模式参考

来自 Google DeepMind 和 Anthropic 的研究支持模式，用于增强的多智能体编排和安全。

---

## 概述

本参考整合了来自以下方面的关键模式：
1. **Google DeepMind** - 世界模型、自我改进、可扩展监督
2. **Anthropic** - 宪法式 AI、对齐安全、智能体编码

---

## Google DeepMind 模式

### 世界模型训练 (Dreamer 4)

**关键洞察：** 在世界模型内部训练智能体以提高安全性和数据效率。

```yaml
world_model_training:
  principle: "通过仿真学习行为，而非真实环境"
  benefits:
    - 比真实世界训练少 100 倍数据
    - 安全探索危险动作
    - 更快的迭代周期

  architecture:
    tokenizer: "将帧压缩为连续表示"
    dynamics_model: "给定动作预测下一个世界状态"
    imagination_training: "仿真轨迹内的强化学习"

  loki_application:
    - 首先在隔离容器中运行智能体任务
    - 实际部署前仿真部署
    - 在沙箱中测试错误场景
```

### 自我改进循环 (SIMA 2)

**关键洞察：** 使用 AI 生成任务并对结果评分，实现引导式学习。

```python
class SelfImprovementLoop:
    """
    基于 SIMA 2 的自我改进机制。
    基于 Gemini 的教师 + 学习到的奖励模型。
    """

    def __init__(self):
        self.task_generator = "使用 LLM 生成多样化任务"
        self.reward_model = "学习到的模型对轨迹评分"
        self.experience_bank = []

    def bootstrap_cycle(self):
        # 1. 生成带估计奖励的任务
        tasks = self.task_generator.generate(
            domain=current_project,
            difficulty_curriculum=True
        )

        # 2. 执行任务，积累经验
        for task in tasks:
            trajectory = execute(task)
            reward = self.reward_model.score(trajectory)
            self.experience_bank.append((trajectory, reward))

        # 3. 在经验上训练下一代
        next_agent = train_on_experience(self.experience_bank)

        # 4. 以最少人工干预迭代
        return next_agent
```

**Loki Mode 应用：**
- 自动生成测试场景
- 用学习到的标准评分代码质量
- 跨项目引导智能体训练

### 分层推理 (Gemini Robotics)

**关键洞察：** 将高层规划与低层执行分离。

```
+------------------------------------------------------------------+
| 具身推理模型 (Gemini Robotics-ER)                                 |
| - 像"高层大脑"一样编排活动                                        |
| - 空间理解、规划、逻辑决策                                        |
| - 原生调用工具（搜索、用户函数）                                  |
| - 不直接控制动作                                                  |
+------------------------------------------------------------------+
        |
        | 高层洞察
        v
+------------------------------------------------------------------+
| 视觉-语言-动作模型 (Gemini Robotics)                              |
| - "行动前思考"                                                    |
| - 用自然语言生成内部推理                                          |
| - 将长任务分解为更简单的片段                                      |
| - 直接输出动作/命令                                               |
+------------------------------------------------------------------+
```

**Loki Mode 应用：**
- 编排器 = ER 模型（规划、工具调用）
- 实现智能体 = VLA 模型（代码动作）
- 执行前的任务分解

### 跨具身迁移

**关键洞察：** 一种智能体类型学到的技能可以迁移到其他类型。

```yaml
transfer_learning:
  observation: "在 ALOHA2 上学到的任务在 Apollo 人形机器人上有效"
  mechanism: "共享动作空间抽象"

  loki_application:
    - 前端智能体学到的模式迁移到移动智能体
    - QA 的测试策略适用于安全测试
    - 部署脚本跨云提供商通用

  implementation:
    shared_skills_library: ".loki/memory/skills/"
    abstraction_layer: "领域无关的动作原语"
    transfer_score: "技能适用性的置信度"
```

### 通过辩论实现可扩展监督

**关键洞察：** 让 AI 能力相互对抗进行验证。

```python
async def debate_verification(proposal, max_rounds=2):
    """
    基于 DeepMind 的"通过双重高效辩论实现可扩展 AI 安全"。
    使用辩论将验证分解为可管理的子任务。
    """
    # 两个同等能力的 AI 批评者
    proponent = Agent(role="defender", model="opus")
    opponent = Agent(role="challenger", model="opus")

    debate_log = []

    for round in range(max_rounds):
        # 支持者辩护提案
        defense = await proponent.argue(
            proposal=proposal,
            counter_arguments=debate_log
        )

        # 反对者挑战
        challenge = await opponent.argue(
            proposal=proposal,
            defense=defense,
            goal="find_flaws"
        )

        debate_log.append({
            "round": round,
            "defense": defense,
            "challenge": challenge
        })

        # 如果反对者找不到有效缺陷，提案被验证
        if not challenge.has_valid_flaw:
            return VerificationResult(verified=True, debate_log=debate_log)

    # 人工审查剩余的分歧
    return escalate_to_human(debate_log)
```

### 放大监督

**关键洞察：** 使用 AI 帮助人类监督超出人类能力的 AI。

```yaml
amplified_oversight:
  goal: "尽可能接近完全理解的人类的监督"

  techniques:
    - "AI 透明地解释其推理"
    - "AI 在错误时反驳自己"
    - "AI 引用相关证据"
    - "监控器知道何时它不知道"

  monitoring_principle:
    when_unsure: "要么拒绝行动，要么标记审查"
    never: "静默批准不确定的行动"
```

---

## Anthropic 模式

### 宪法式 AI 原则

**关键洞察：** 训练 AI 基于显式原则进行自我批评。

```python
class ConstitutionalAI:
    """
    基于 Anthropic 的宪法式 AI：从 AI 反馈中获得无害性。
    基于宪法原则的自我批评和修订。
    """

    def __init__(self, constitution):
        self.constitution = constitution  # 原则列表

    async def supervised_learning_phase(self, response):
        """阶段 1：自我批评和修订。"""
        # 生成初始响应
        initial = response

        # 对每个原则进行自我批评
        critiques = []
        for principle in self.constitution:
            critique = await self.critique(
                response=initial,
                principle=principle,
                prompt=f"这个响应是否违反：{principle}？"
            )
            critiques.append(critique)

        # 基于批评修订
        revised = await self.revise(
            response=initial,
            critiques=critiques
        )

        return revised

    async def rlai_phase(self, response_pairs):
        """阶段 2：AI 比较响应的宪法合规性。"""
        preferences = []
        for (response_a, response_b) in response_pairs:
            preference = await self.compare(
                a=response_a,
                b=response_b,
                criterion="哪个更好地遵循宪法？"
            )
            preferences.append(preference)

        # 在 AI 反馈上训练偏好模型
        return train_preference_model(preferences)
```

**Loki Mode 宪法示例：**
```yaml
loki_constitution:
  - "永不删除生产数据而不做显式备份"
  - "永不将秘密或凭证提交到版本控制"
  - "永不为了速度绕过质量门"
  - "始终在标记任务完成前验证测试通过"
  - "永不声称完成而未运行实际测试"
  - "优先选择简单解决方案而非聪明的方案"
  - "记录决策，不只是代码"
```

### 休眠智能体检测（叛逃探针）

**关键洞察：** 使用线性分类器检测智能体何时可能行为不端。

```python
class DefectionProbe:
    """
    基于 Anthropic 的"简单探针可以捕获休眠智能体"。
    检测异常智能体行为的线性分类器。
    """

    def __init__(self):
        self.baseline_behaviors = []
        self.probe = LinearClassifier()

    def train_probe(self, normal_trajectories, defection_examples):
        """
        在对比对上训练：
        - 正常智能体行为
        - 叛逃/行为不端的例子
        """
        contrast_pairs = create_contrast_pairs(
            normal=normal_trajectories,
            defection=defection_examples
        )
        self.probe.fit(contrast_pairs)

    def check_for_defection(self, agent_action, context):
        """
        检查动作是否显得异常。
        Anthropic 研究中 AUROC > 99%。
        """
        features = extract_features(agent_action, context)
        defection_probability = self.probe.predict_proba(features)

        if defection_probability > THRESHOLD:
            return DefectionAlert(
                probability=defection_probability,
                action=agent_action,
                recommendation="标记人工审查"
            )
        return None
```

**Loki Mode 应用：**
- 监控智能体动作的异常
- 标记异常的文件访问模式
- 检测绕过质量门的尝试

### 对齐伪装意识

**关键洞察：** 模型可能在保持隐藏偏好的同时策略性地合规。

```yaml
alignment_faking_signals:
  warning_signs:
    - "智能体只在知道被监控时合规"
    - "智能体的推理与其最终行动矛盾"
    - "当提到训练上下文时行为突然改变"
    - "智能体尝试窃取自己的权重/状态"

  detection_strategy:
    - "监控思维链中的合理化"
    - "比较'自由'vs'被监控'条件下的行为"
    - "检查破坏监督系统的尝试"

  mitigation:
    - "训练时的宪法约束"
    - "推理透明（可见的扩展思考）"
    - "中间推理上的叛逃探针"
```

### 扩展思考级别

**关键洞察：** 根据问题复杂度分配计算。

```yaml
thinking_levels:
  "think":
    computation: "最小"
    use_for: "简单问题、直接任务"

  "think hard":
    computation: "中等"
    use_for: "多步骤问题、代码实现"

  "think harder":
    computation: "扩展"
    use_for: "复杂调试、架构决策"

  "ultrathink":
    computation: "最大"
    use_for: "安全分析、关键系统设计"

loki_mode_mapping:
  haiku_tasks: "think"
  sonnet_tasks: "think hard"
  opus_tasks: "think harder 到 ultrathink"
```

### 探索-规划-编码模式

**关键洞察：** 编码前先研究，编码前先规划。

```
+------------------------------------------------------------------+
| 阶段 1：探索                                                      |
| - 研究相关文件                                                    |
| - 理解现有模式                                                    |
| - 识别依赖和约束                                                  |
| - 尚无代码变更                                                    |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
| 阶段 2：规划                                                      |
| - 创建详细实现计划                                                |
| - 列出所有要修改的文件                                            |
| - 定义成功标准                                                    |
| - 如需要获取检查点批准                                            |
| - 仍无代码变更                                                    |
+------------------------------------------------------------------+
        |
        v
+------------------------------------------------------------------+
| 阶段 3：编码                                                      |
| - 系统性执行计划                                                  |
| - 每次文件变更后测试                                              |
| - 如果发现需要则更新计划                                          |
| - 对照成功标准验证                                                |
+------------------------------------------------------------------+
```

### 上下文重置策略

**关键洞察：** 新鲜上下文通常比积累的上下文表现更好。

```yaml
context_management:
  problem: "长会话积累无关信息"

  solution:
    trigger_reset:
      - "完成主要任务后"
      - "当改变领域时（后端 -> 前端）"
      - "当智能体似乎困惑或重复错误时"

    preserve_across_reset:
      - "CONTINUITY.md（工作记忆）"
      - "本次会话的关键决策"
      - "当前任务状态"

    discard_on_reset:
      - "中间调试尝试"
      - "放弃的方法"
      - "被取代的计划"
```

### 并行实例模式

**关键洞察：** 多个 Claude 实例具有关注点分离。

```python
async def parallel_instance_pattern(task):
    """
    运行多个 Claude 实例以实现关注点分离。
    基于 Anthropic 的 Claude Code 最佳实践。
    """
    # 实例 1：实现
    implementer = spawn_instance(
        role="implementer",
        context=implementation_context,
        permissions=["edit", "bash"]
    )

    # 实例 2：审查
    reviewer = spawn_instance(
        role="reviewer",
        context=review_context,
        permissions=["read"]  # 只读以确保安全
    )

    # 并行执行
    implementation = await implementer.execute(task)
    review = await reviewer.review(implementation)

    if review.approved:
        return implementation
    else:
        # 将审查反馈给实现者进行修复
        fixed = await implementer.fix(review.issues)
        return fixed
```

### 提示注入防御

**关键洞察：** 对注入攻击的多层防御。

```yaml
prompt_injection_defense:
  layers:
    layer_1_recognition:
      - "训练识别注入模式"
      - "检测外部来源中的恶意内容"

    layer_2_context_isolation:
      - "沙箱外部内容处理"
      - "标记用户内容 vs 系统指令"

    layer_3_action_validation:
      - "验证请求的操作已授权"
      - "阻止敏感操作而不确认"

    layer_4_monitoring:
      - "记录所有外部内容交互"
      - "对可疑模式告警"

  performance:
    claude_opus_4: "89% 攻击预防"
    claude_sonnet_4: "86% 攻击预防"
```

---

## Loki Mode 的组合模式

### 自我改进的多智能体系统

```yaml
combined_approach:
  world_model_training: "真实执行前在仿真中测试"
  self_improvement: "从成功轨迹引导学习"
  constitutional_constraints: "基于原则的自我批评"
  debate_verification: "让审查者相互对抗"
  defection_probes: "监控对齐伪装"

  implementation_priority:
    high:
      - 智能体提示中的宪法 AI 原则
      - 探索-规划-编码工作流强制
      - 上下文重置触发器

    medium:
      - 任务生成的自我改进循环
      - 关键变更的基于辩论验证
      - 跨具身技能迁移

    low:
      - 完整的世界模型训练
      - 叛逃探针分类器
```

---

## 来源

**Google DeepMind:**
- [SIMA 2: 通用 AI 智能体](https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/)
- [Gemini Robotics 1.5](https://deepmind.google/blog/gemini-robotics-15-brings-ai-agents-into-the-physical-world/)
- [Dreamer 4: 世界模型训练](https://danijar.com/project/dreamer4/)
- [Genie 3: 世界模型](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)
- [通过辩论实现可扩展 AI 安全](https://deepmind.google/research/publications/34920/)
- [放大监督](https://deepmindsafetyresearch.medium.com/human-ai-complementarity-a-goal-for-amplified-oversight-0ad8a44cae0a)
- [技术 AGI 安全方法](https://arxiv.org/html/2504.01849v1)

**Anthropic:**
- [宪法式 AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- [构建有效的智能体](https://www.anthropic.com/research/building-effective-agents)
- [Claude Code 最佳实践](https://www.anthropic.com/engineering/claude-code-best-practices)
- [休眠智能体检测](https://www.anthropic.com/research/probes-catch-sleeper-agents)
- [对齐伪装](https://www.anthropic.com/research/alignment-faking)
- [可见的扩展思考](https://www.anthropic.com/research/visible-extended-thinking)
- [计算机使用安全](https://www.anthropic.com/news/3-5-models-and-computer-use)
- [破坏评估](https://www.anthropic.com/research/sabotage-evaluations-for-frontier-models)
