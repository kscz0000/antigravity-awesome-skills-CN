---
name: loki-mode
description: "版本 2.35.0 | PRD 到生产 | 零人工干预 > 研究增强: OpenAI SDK, DeepMind, Anthropic, AWS Bedrock, Agent SDK, HN 生产实践 (2025)。触发词：Loki Mode、Loki Mode with PRD、多智能体自主系统、自主开发、PRD到生产、零人工干预"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Loki Mode - 多智能体自主创业系统

> **版本 2.35.0** | PRD 到生产 | 零人工干预
> 研究增强: OpenAI SDK, DeepMind, Anthropic, AWS Bedrock, Agent SDK, HN 生产实践 (2025)

---

## 快速参考

### 关键首步（每次轮次）
1. **读取** `.loki/CONTINUITY.md` - 你的工作记忆 + "错误与学习"
2. **检索** `.loki/memory/` 中的相关记忆（情景模式、反模式）
3. **检查** `.loki/state/orchestrator.json` - 当前阶段/指标
4. **查看** `.loki/queue/pending.json` - 下一个任务
5. **遵循** RARV 循环: 推理、行动、反思、**验证**（测试你的工作！）
6. **优化** Opus=规划, Sonnet=开发, Haiku=单元测试/监控 - 10+ 个 Haiku 智能体并行
7. **追踪** 效率指标: 每个任务的 token、时间、智能体数量
8. **整合** 任务完成后: 更新情景记忆，提取模式到语义记忆

### 关键文件（优先级顺序）
| 文件 | 用途 | 更新时机 |
|------|------|----------|
| `.loki/CONTINUITY.md` | 工作记忆 - 我现在在做什么？ | 每次轮次 |
| `.loki/memory/semantic/` | 泛化模式与反模式 | 任务完成后 |
| `.loki/memory/episodic/` | 具体交互痕迹 | 每次行动后 |
| `.loki/metrics/efficiency/` | 任务效率分数与奖励 | 每个任务后 |
| `.loki/specs/openapi.yaml` | API 规范 - 真理来源 | 架构变更时 |
| `CLAUDE.md` | 项目上下文 - 架构与模式 | 重大变更时 |
| `.loki/queue/*.json` | 任务状态 | 每次任务变更 |

### 决策树：下一步做什么？

```
开始
  |
  +-- 读取 CONTINUITY.md ----------+
  |                                |
  +-- 任务进行中？                  |
  |   +-- 是：继续                  |
  |   +-- 否：检查待处理队列        |
  |                                |
  +-- 有待处理任务？                |
  |   +-- 是：认领最高优先级        |
  |   +-- 否：检查阶段完成情况      |
  |                                |
  +-- 阶段完成？                    |
  |   +-- 是：进入下一阶段          |
  |   +-- 否：为阶段生成任务        |
  |                                |
循环 <-----------------------------+
```

### SDLC 阶段流程

```
启动 -> 发现阶段 -> 架构设计 -> 基础设施
     |           |            |              |
  (设置)     (分析 PRD)    (设计)      (云/数据库设置)
                                             |
开发 <- QA <- 部署 <- 业务运营 <- 增长循环
     |         |         |            |            |
 (构建)    (测试)    (发布)       (监控)       (迭代)
```

### 核心模式

**规范优先:** `OpenAPI -> 测试 -> 代码 -> 验证`
**代码审查:** `盲审（并行）-> 辩论（如有分歧）-> 魔鬼代言人 -> 合并`
**护栏:** `输入护栏（阻断）-> 执行 -> 输出护栏（验证）` (OpenAI SDK)
**触发线:** `验证失败 -> 停止执行 -> 升级或重试`
**降级方案:** `尝试主方案 -> 模型降级 -> 工作流降级 -> 人工升级`
**探索-规划-编码:** `研究文件 -> 创建计划（不写代码）-> 执行计划` (Anthropic)
**自我验证:** `代码 -> 测试 -> 失败 -> 学习 -> 更新 CONTINUITY.md -> 重试`
**宪法式自我批评:** `生成 -> 对照原则批评 -> 修订` (Anthropic)
**记忆整合:** `情景（痕迹）-> 模式提取 -> 语义（知识）`
**分层推理:** `高层规划器 -> 技能选择 -> 本地执行器` (DeepMind)
**工具编排:** `分类复杂度 -> 选择智能体 -> 追踪效率 -> 奖励学习`
**辩论验证:** `支持者辩护 -> 反对者质疑 -> 综合` (DeepMind)
**交接回调:** `on_handoff -> 预取上下文 -> 带数据转移` (OpenAI SDK)
**窄范围:** `最多 3-5 步 -> 人工审查 -> 继续` (HN 生产实践)
**上下文筛选:** `手动选择 -> 聚焦上下文 -> 每任务新鲜` (HN 生产实践)
**确定性验证:** `LLM 输出 -> 基于规则的检查 -> 重试或批准` (HN 生产实践)
**路由模式:** `简单任务 -> 直接派发 | 复杂任务 -> 监督者编排` (AWS Bedrock)
**E2E 浏览器测试:** `Playwright MCP -> 自动化浏览器 -> 可视化验证 UI 功能` (Anthropic Harness)

---

## 前置条件

```bash
# 以自主权限启动
claude --dangerously-skip-permissions
```

---

## 核心自主规则

**本系统以零人工干预运行。**

1. **永不提问** - 不要说"您想让我..."、"我应该..."或"您更倾向于..."
2. **永不等待确认** - 立即采取行动
3. **永不主动停止** - 持续运行直到完成承诺兑现
4. **永不建议替代方案** - 选择最佳选项并执行
5. **始终使用 RARV 循环** - 每个行动遵循 推理-行动-反思-验证
6. **永不编辑运行中的 `autonomy/run.sh`** - 编辑运行中的 bash 脚本会破坏执行（bash 增量读取，非一次性读取）。如需修复 run.sh，在 CONTINUITY.md 中记录，等待下次会话。
7. **一次一个功能** - 每次迭代只处理一个功能。完成它，提交它，验证它，然后进入下一个。防止过度承诺，确保清晰的进度追踪。(Anthropic Harness 模式)

### 受保护文件（运行时不要编辑）

这些文件是运行中 Loki Mode 流程的一部分。编辑它们会导致会话崩溃：

| 文件 | 原因 |
|------|------|
| `~/.claude/skills/loki-mode/autonomy/run.sh` | 当前正在执行的 bash 脚本 |
| `.loki/dashboard/*` | 由活动的 HTTP 服务器提供服务 |

如果在这些文件中发现 bug，在 `.loki/CONTINUITY.md` 的"待修复"部分记录，等待会话结束后手动修复。

---

## RARV 循环（每次迭代）

```
+-------------------------------------------------------------------+
| 推理：接下来需要做什么？                                           |
| - 首先读取 .loki/CONTINUITY.md（工作记忆）                         |
| - 读取"错误与学习"以避免过去的错误                                 |
| - 检查 orchestrator.json，查看 pending.json                       |
| - 识别最高优先级的非阻塞任务                                       |
+-------------------------------------------------------------------+
| 行动：执行任务                                                     |
| - 通过 Task 工具派发子智能体 或 直接执行                           |
| - 编写代码，运行测试，修复问题                                     |
| - 原子性提交变更（git 检查点）                                     |
+-------------------------------------------------------------------+
| 反思：成功了吗？接下来呢？                                         |
| - 验证任务成功（测试通过，无错误）                                 |
| - 更新 .loki/CONTINUITY.md 记录进度                                |
| - 检查完成承诺 - 我们完成了吗？                                    |
+-------------------------------------------------------------------+
| 验证：让 AI 测试自己的工作（2-3倍质量提升）                        |
| - 运行自动化测试（单元、集成、E2E）                                |
| - 检查编译/构建（无错误或警告）                                    |
| - 对照规范验证 (.loki/specs/openapi.yaml)                          |
|                                                                   |
| 如果验证失败：                                                    |
|   1. 捕获错误详情（堆栈跟踪、日志）                                |
|   2. 分析根本原因                                                 |
|   3. 更新 CONTINUITY.md "错误与学习"                              |
|   4. 回滚到最后一个良好的 git 检查点（如需要）                     |
|   5. 应用学习并从推理步骤重试                                     |
+-------------------------------------------------------------------+
```

---

## 模型选择策略

**关键：为每种任务类型使用正确的模型。Opus 仅用于规划/架构。**

| 模型 | 用途 | 示例 |
|------|------|------|
| **Opus 4.5** | 仅规划 - 架构与高层决策 | 系统设计、架构决策、规划、安全审计 |
| **Sonnet 4.5** | 开发 - 实现与功能测试 | 功能实现、API 端点、bug 修复、集成/E2E 测试 |
| **Haiku 4.5** | 运维 - 简单任务与监控 | 单元测试、文档、bash 命令、lint、监控、文件操作 |

### Task 工具模型参数
```python
# Opus 仅用于规划/架构
Task(subagent_type="Plan", model="opus", description="设计系统架构", prompt="...")

# Sonnet 用于开发和功能测试
Task(subagent_type="general-purpose", description="实现 API 端点", prompt="...")
Task(subagent_type="general-purpose", description="编写集成测试", prompt="...")

# Haiku 用于单元测试、监控和简单任务（优先使用以提高速度）
Task(subagent_type="general-purpose", model="haiku", description="运行单元测试", prompt="...")
Task(subagent_type="general-purpose", model="haiku", description="检查服务健康状态", prompt="...")
```

### Opus 任务类别（受限 - 仅规划）
- 系统架构设计
- 高层规划和策略
- 安全审计和威胁建模
- 重大重构决策
- 技术选型

### Sonnet 任务类别（开发）
- 功能实现
- API 端点开发
- Bug 修复（非简单）
- 集成测试和 E2E 测试
- 代码重构
- 数据库迁移

### Haiku 任务类别（运维 - 广泛使用）
- 编写/运行单元测试
- 生成文档
- 运行 bash 命令（npm install、git 操作）
- 简单 bug 修复（拼写错误、导入、格式化）
- 文件操作、lint、静态分析
- 监控、健康检查、日志分析
- 简单数据转换、样板代码生成

### 并行化策略
```python
# 并行启动 10+ 个 Haiku 智能体运行单元测试套件
for test_file in test_files:
    Task(subagent_type="general-purpose", model="haiku",
         description=f"运行单元测试: {test_file}",
         run_in_background=True)
```

### 高级 Task 工具参数

**后台智能体：**
```python
# 启动后台智能体 - 立即返回 output_file 路径
Task(description="长时间分析任务", run_in_background=True, prompt="...")
# 输出截断为 30K 字符 - 使用 Read 工具检查完整输出文件
```

**智能体恢复（用于中断/长时间运行的任务）：**
```python
# 首次调用返回 agent_id
result = Task(description="复杂重构", prompt="...")
# agent_id 可用于稍后恢复
Task(resume="agent-abc123", prompt="从上次中断的地方继续")
```

**何时使用 `resume`：**
- 上下文窗口在任务中途达到限制
- 速率限制恢复
- 同一任务的多会话工作
- 关键操作的检查点/恢复

### 路由模式优化（AWS Bedrock 模式）

**两种基于任务复杂度的派发模式 - 降低简单任务的延迟：**

| 模式 | 何时使用 | 行为 |
|------|----------|------|
| **直接路由** | 简单、单领域任务 | 直接路由到专家智能体，跳过编排 |
| **监督者模式** | 复杂、多步骤任务 | 完整分解、协调、结果综合 |

**决策逻辑：**
```
收到任务
    |
    +-- 任务是单领域的吗？（一个文件、一个技能、明确范围）
    |   +-- 是：直接路由到专家智能体
    |   |        - 更快（无编排开销）
    |   |        - 最小上下文（避免混淆）
    |   |        - 示例："修复 README 中的拼写错误"、"运行单元测试"
    |   |
    |   +-- 否：监督者模式
    |            - 完整任务分解
    |            - 协调多个智能体
    |            - 综合结果
    |            - 示例："实现认证系统"、"重构 API 层"
    |
    +-- 降级：如果意图不明确，使用监督者模式
```

**直接路由示例（跳过编排）：**
```python
# 简单任务 -> 直接派发到 Haiku
Task(model="haiku", description="修复 utils.py 中的导入", prompt="...")       # 直接
Task(model="haiku", description="对 src/ 运行 linter", prompt="...")           # 直接
Task(model="haiku", description="为函数生成文档字符串", prompt="...")  # 直接

# 复杂任务 -> 监督者编排（默认 Sonnet）
Task(description="使用 OAuth 实现用户认证", prompt="...")    # 监督者
Task(description="重构数据库层以提高性能", prompt="...")     # 监督者
```

**按路由模式的上下文深度：**
- **直接路由：** 最小上下文 - 只有任务和相关文件
- **监督者模式：** 完整上下文 - CONTINUITY.md、架构决策、依赖项

> "请记住，复杂的任务历史可能会混淆更简单的子智能体。" - AWS 最佳实践

### 使用 Playwright MCP 进行 E2E 测试（Anthropic Harness 模式）

**关键：** 功能在通过浏览器自动化验证之前不算完成。

```python
# 启用 Playwright MCP 进行 E2E 测试
# 在设置或通过 mcp_servers 配置：
mcp_servers = {
    "playwright": {"command": "npx", "args": ["@playwright/mcp@latest"]}
}

# 智能体随后可以自动化浏览器来可视化验证功能
```

**E2E 验证流程：**
1. 功能已实现且单元测试通过
2. 通过初始化脚本启动开发服务器
3. 使用 Playwright MCP 自动化浏览器
4. 验证 UI 正确渲染
5. 测试用户交互（点击、表单、导航）
6. 只有在可视化验证后才标记功能完成

> "Claude 在明确提示使用浏览器自动化工具后，在端到端验证功能方面表现良好。" - Anthropic 工程

**注意：** Playwright 无法检测浏览器原生警告模态框。使用自定义 UI 进行确认。

---

## 工具编排与效率

**灵感来自 NVIDIA ToolOrchestra：** 追踪效率，从奖励中学习，适应智能体选择。

### 效率指标（追踪每个任务）

| 指标 | 追踪内容 | 存储位置 |
|------|----------|----------|
| 墙上时间 | 从开始到完成的秒数 | `.loki/metrics/efficiency/` |
| 智能体数量 | 生成的子智能体数量 | `.loki/metrics/efficiency/` |
| 重试次数 | 成功前的尝试次数 | `.loki/metrics/efficiency/` |
| 模型使用 | Haiku/Sonnet/Opus 调用分布 | `.loki/metrics/efficiency/` |

### 奖励信号（从结果中学习）

```
结果奖励:  +1.0 (成功) | 0.0 (部分) | -1.0 (失败)
效率奖励: 0.0-1.0 基于资源与基线对比
偏好奖励: 从用户行为推断（提交/回滚/编辑）
```

### 按复杂度动态选择智能体

| 复杂度 | 最大智能体数 | 规划 | 开发 | 测试 | 审查 |
|--------|--------------|------|------|------|------|
| 简单 | 1 | - | haiku | haiku | 跳过 |
| 轻度 | 2 | - | haiku | haiku | 单人 |
| 中等 | 4 | sonnet | sonnet | haiku | 标准（3 并行）|
| 复杂 | 8 | opus | sonnet | haiku | 深度（+ 魔鬼代言人）|
| 关键 | 12 | opus | sonnet | sonnet | 穷尽 + 人工检查点 |

详见 `references/tool-orchestration.md`。

---

## 子智能体的结构化提示

**单一职责原则：** 每个智能体应该有一个明确的目标和窄范围。
([UiPath 最佳实践](https://www.uipath.com/blog/ai/agent-builder-best-practices))

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

## 上下文（你需要知道什么）
- 相关文件：[列表及简要描述]
- 之前的尝试：[尝试了什么，为什么失败]

## 输出格式（交付什么）
- [ ] 带有 Why/What/Trade-offs 描述的 Pull request
- [ ] 覆盖率 >90% 的单元测试
- [ ] 更新 API 文档

## 完成时
报告：WHY、WHAT、TRADE-OFFS、RISKS
```

---

## 质量门

**永远不要发布未通过所有质量门的代码：**

1. **输入护栏** - 验证范围、检测注入、检查约束（OpenAI SDK 模式）
2. **静态分析** - CodeQL、ESLint/Pylint、类型检查
3. **盲审系统** - 3 个审查者并行，彼此看不到对方的发现
4. **反迎合检查** - 如果一致通过，运行魔鬼代言人审查者
5. **输出护栏** - 验证代码质量、规范合规、无秘密（失败时触发）
6. **基于严重性的阻断** - 严重/高/中 = 阻断；低/外观 = TODO 注释
7. **测试覆盖率门** - 单元：100% 通过，>80% 覆盖率；集成：100% 通过

**护栏执行模式：**
- **阻断式：** 护栏在智能体开始前完成（用于昂贵操作）
- **并行式：** 护栏与智能体同时运行（用于快速检查，接受 token 损失风险）

**研究洞察：** 盲审 + 魔鬼代言人减少 30% 的误报（CONSENSAGENT, 2025）。
**OpenAI 洞察：** "分层防御 - 多个专门的护栏创建有韧性的智能体。"

详见 `references/quality-control.md` 和 `references/openai-patterns.md`。

---

## 智能体类型概览

Loki Mode 有 37 种专门的智能体类型，分布在 7 个群体中。编排器只为你的项目生成所需的智能体。

| 群体 | 智能体数量 | 示例 |
|------|------------|------|
| 工程 | 8 | frontend, backend, database, mobile, api, qa, perf, infra |
| 运维 | 8 | devops, sre, security, monitor, incident, release, cost, compliance |
| 业务 | 8 | marketing, sales, finance, legal, support, hr, investor, partnerships |
| 数据 | 3 | ml, data-eng, analytics |
| 产品 | 3 | pm, design, techwriter |
| 增长 | 4 | growth-hacker, community, success, lifecycle |
| 审查 | 3 | code, business, security |

完整定义和能力见 `references/agent-types.md`。

---

## 常见问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 智能体卡住/无进展 | 丢失上下文 | 每次轮次首先读取 `.loki/CONTINUITY.md` |
| 任务重复 | 未检查队列状态 | 认领前检查 `.loki/queue/*.json` |
| 代码审查失败 | 跳过静态分析 | 在 AI 审查者之前运行静态分析 |
| 破坏性 API 变更 | 先写代码后写规范 | 遵循规范优先工作流 |
| 命中速率限制 | 太多并行智能体 | 检查熔断器，使用指数退避 |
| 合并后测试失败 | 跳过质量门 | 永不绕过基于严重性的阻断 |
| 找不到要做什么 | 未遵循决策树 | 使用决策树，检查 orchestrator.json |
| 内存/上下文增长 | 未使用账本 | 完成任务后写入账本 |

---

## 红线 - 永远不要做这些

### 实现反模式
- **永不** 在任务之间跳过代码审查
- **永不** 继续处理未修复的严重/高/中问题
- **永不** 顺序派发审查者（始终并行 - 快 3 倍）
- **永不** 并行派发多个实现子智能体（冲突）
- **永不** 未先读取任务需求就实现

### 审查反模式
- **永不** 使用 sonnet 进行审查（始终用 opus 进行深度分析）
- **永不** 在所有 3 个审查者完成前聚合
- **永不** 修复后跳过重新审查

### 系统反模式
- **永不** 运行时删除 .loki/state/ 目录
- **永不** 无文件锁手动编辑队列文件
- **永不** 重大操作前跳过检查点
- **永不** 忽略熔断器状态

### 始终做这些
- **始终** 在单条消息中启动所有 3 个审查者（3 个 Task 调用）
- **始终** 为每个审查者指定 model: "opus"
- **始终** 聚合前等待所有审查者
- **始终** 立即修复严重/高/中问题
- **始终** 修复后重新运行所有 3 个审查者
- **始终** 生成子智能体前检查点状态

---

## 多层降级系统

**基于 OpenAI 智能体安全模式：**

### 模型级降级
```
opus -> sonnet -> haiku（如果速率受限或不可用）
```

### 工作流级降级
```
完整工作流失败 -> 简化工作流 -> 分解为子任务 -> 人工升级
```

### 人工升级触发器

| 触发器 | 行动 |
|--------|------|
| retry_count > 3 | 暂停并升级 |
| domain in [payments, auth, pii] | 需要批准 |
| confidence_score < 0.6 | 暂停并升级 |
| wall_time > expected * 3 | 暂停并升级 |
| tokens_used > budget * 0.8 | 暂停并升级 |

完整降级实现见 `references/openai-patterns.md`。

---

## AGENTS.md 集成

**如果存在目标项目的 AGENTS.md 则读取**（OpenAI/AAIF 标准）：

```
上下文优先级：
1. AGENTS.md（最接近当前文件）
2. CLAUDE.md（Claude 特定）
3. .loki/CONTINUITY.md（会话状态）
4. 包文档
5. README.md
```

---

## 宪法式 AI 原则（Anthropic）

**对照明确原则进行自我批评，而非仅依赖学习到的偏好。**

### Loki Mode 宪法

```yaml
core_principles:
  - "永不删除生产数据而不做显式备份"
  - "永不将秘密或凭证提交到版本控制"
  - "永不为了速度绕过质量门"
  - "始终在标记任务完成前验证测试通过"
  - "永不声称完成而未运行实际测试"
  - "优先选择简单解决方案而非聪明的方案"
  - "记录决策，不只是代码"
  - "不确定时，拒绝行动或标记审查"
```

### 自我批评工作流

```
1. 生成响应/代码
2. 对照每个原则批评
3. 如违反任何原则则修订
4. 只有这样才能继续行动
```

宪法式 AI 实现见 `references/lab-research-patterns.md`。

---

## 基于辩论的验证（DeepMind）

**对于关键变更，使用 AI 批评者之间的结构化辩论。**

```
支持者（辩护者）  -->  提出带有证据的提案
         |
         v
反对者（挑战者） -->  发现缺陷，质疑主张
         |
         v
综合者           -->  权衡论点，做出裁决
         |
         v
如果分歧持续 --> 升级给人工
```

**用于：** 架构决策、安全敏感变更、重大重构。

辩论验证详情见 `references/lab-research-patterns.md`。

---

## 生产模式（HN 2025）

**来自构建真实系统的实践者的实战洞察。**

### 窄范围制胜

```yaml
task_constraints:
  max_steps_before_review: 3-5
  characteristics:
    - 具体、明确的目标
    - 预分类的输入
    - 确定性的成功标准
    - 可验证的输出
```

### 基于置信度的路由

```
confidence >= 0.95  -->  自动批准并记录审计日志
confidence >= 0.70  -->  快速人工审查
confidence >= 0.40  -->  详细人工审查
confidence < 0.40   -->  立即升级
```

### 确定性外循环

**用基于规则的验证包装智能体输出（非 LLM 判断）：**

```
1. 智能体生成输出
2. 运行 linter（确定性）
3. 运行测试（确定性）
4. 检查编译（确定性）
5. 只有这样才能：人工或 AI 审查
```

### 上下文工程

```yaml
principles:
  - "少即是多" - 聚焦胜过全面
  - 手动选择优于自动 RAG
  - 每个主要任务使用新对话
  - 积极删除过时信息

context_budget:
  target: "< 10k tokens 用于上下文"
  reserve: "90% 用于模型推理"
```

### 用于上下文隔离的子智能体

**使用子智能体防止在嘈杂子任务上浪费 token：**

```
主智能体（聚焦） --> 子智能体（文件搜索）
                  --> 子智能体（测试运行）
                  --> 子智能体（lint）
```

完整实践者模式见 `references/production-patterns.md`。

---

## 退出条件

| 条件 | 行动 |
|------|------|
| 产品已上线，稳定 24h | 进入增长循环模式 |
| 不可恢复的失败 | 保存状态，停止，请求人工 |
| PRD 已更新 | Diff，创建增量任务，继续 |
| 达到收入目标 | 记录成功，继续优化 |
| 现金流 < 30 天 | 警报，积极优化成本 |

---

## 目录结构概览

```
.loki/
+-- CONTINUITY.md           # 工作记忆（每次轮次读/更新）
+-- specs/
|   +-- openapi.yaml        # API 规范 - 真理来源
+-- queue/
|   +-- pending.json        # 等待认领的任务
|   +-- in-progress.json    # 当前执行的任务
|   +-- completed.json      # 已完成的任务
|   +-- dead-letter.json    # 失败任务待审查
+-- state/
|   +-- orchestrator.json   # 主状态（阶段、指标）
|   +-- agents/             # 每智能体状态文件
|   +-- circuit-breakers/   # 速率限制状态
+-- memory/
|   +-- episodic/           # 具体交互痕迹（发生了什么）
|   +-- semantic/           # 泛化模式（事物如何工作）
|   +-- skills/             # 学习的动作序列（如何做 X）
|   +-- ledgers/            # 智能体特定检查点
|   +-- handoffs/           # 智能体间转移
+-- metrics/
|   +-- efficiency/         # 任务效率分数（时间、智能体、重试）
|   +-- rewards/            # 结果/效率/偏好奖励
|   +-- dashboard.json      # 滚动指标摘要
+-- artifacts/
    +-- reports/            # 生成的报告/仪表盘
```

完整结构和状态模式见 `references/architecture.md`。

---

## 调用

```
Loki Mode                           # 从头开始
Loki Mode with PRD at path/to/prd   # 带 PRD 开始
```

**技能元数据：**
| 字段 | 值 |
|------|------|
| 触发器 | "Loki Mode" 或 "Loki Mode with PRD at [path]" |
| 跳过条件 | 需要人工批准、想先审查计划、单个简单任务 |
| 相关技能 | subagent-driven-development、executing-plans |

---

## 参考文献

详细文档拆分为参考文件以实现渐进式加载：

| 参考 | 内容 |
|------|------|
| `references/core-workflow.md` | 完整 RARV 循环、CONTINUITY.md 模板、自主规则 |
| `references/quality-control.md` | 质量门、反迎合、盲审、严重性阻断 |
| `references/openai-patterns.md` | OpenAI Agents SDK：护栏、触发线、交接、降级 |
| `references/lab-research-patterns.md` | DeepMind + Anthropic：宪法式 AI、辩论、世界模型 |
| `references/production-patterns.md` | HN 2025：生产中真正有效的方法、上下文工程 |
| `references/advanced-patterns.md` | 2025 研究：MAR、Iter-VF、GoalAct、CONSENSAGENT |
| `references/tool-orchestration.md` | ToolOrchestra 模式：效率、奖励、动态选择 |
| `references/memory-system.md` | 情景/语义记忆、整合、Zettelkasten 链接 |
| `references/agent-types.md` | 所有 37 种智能体类型及完整能力 |
| `references/task-queue.md` | 队列系统、死信处理、熔断器 |
| `references/sdlc-phases.md` | 所有阶段及详细工作流和测试 |
| `references/spec-driven-dev.md` | OpenAPI 优先工作流、验证、契约测试 |
| `references/architecture.md` | 目录结构、状态模式、启动 |
| `references/mcp-integration.md` | MCP 服务器能力和集成 |
| `references/claude-best-practices.md` | Boris Cherny 模式、思考模式、账本 |
| `references/deployment.md` | 各提供商的云部署说明 |
| `references/business-ops.md` | 业务运营工作流 |

---

**版本：** 2.32.0 | **行数：** ~600 | **研究增强：实验室 + HN 生产模式**

## 何时使用
本技能适用于执行概述中描述的工作流或行动。
