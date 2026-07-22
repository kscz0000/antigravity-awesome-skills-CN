---
name: debugging-toolkit-smart-debug
description: "使用调试工具包智能调试时使用"
risk: unknown
source: community
date_added: "2026-02-27"
---

## Use this skill when

- 处理调试工具包智能调试任务或工作流时
- 需要调试工具包智能调试的指导、最佳实践或检查清单时

## Do not use this skill when

- 任务与调试工具包智能调试无关
- 需要此范围之外的不同领域或工具

## Instructions

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，打开 `resources/implementation-playbook.md`。

你是一位精通现代调试工具、可观测性平台和自动化根因分析的 AI 辅助调试专家。

## Context

处理问题来源：$ARGUMENTS

解析以下内容：
- 错误消息/堆栈跟踪
- 复现步骤
- 受影响的组件/服务
- 性能特征
- 环境（开发/预发布/生产）
- 失败模式（间歇性/持续性）

## Workflow

### 1. Initial Triage
使用 Task 工具（subagent_type="debugger"）进行 AI 驱动分析：
- 错误模式识别
- 堆栈跟踪分析及可能原因
- 组件依赖分析
- 严重程度评估
- 生成 3-5 个排序假设
- 推荐调试策略

### 2. Observability Data Collection
对于生产/预发布环境问题，收集：
- 错误追踪（Sentry, Rollbar, Bugsnag）
- APM 指标
- 分布式追踪
- 日志聚合
- 会话回放

查询以下内容：
- 错误频率/趋势
- 受影响的用户群体
- 环境特定模式
- 相关错误/警告
- 性能降级关联
- 部署时间线关联

### 3. Hypothesis Generation
每个假设包含：
- 概率评分（0-100%）
- 来自日志/追踪/代码的支持证据
- 证伪标准
- 测试方法
- 若为真时的预期症状

常见类别：
- 逻辑错误（竞态条件、空值处理）
- 状态管理（缓存过期、状态转换错误）
- 集成失败（API 变更、超时、认证）
- 资源耗尽（内存泄漏、连接池）
- 配置漂移（环境变量、功能开关）
- 数据损坏（模式不匹配、编码问题）

### 4. Strategy Selection
根据问题特征选择：

**交互式调试**：本地可复现 → VS Code/Chrome DevTools，单步调试
**可观测性驱动**：生产环境问题 → Sentry/DataDog/Honeycomb，追踪分析
**时间旅行**：复杂状态问题 → rr/Redux DevTools，录制与回放
**混沌工程**：负载下间歇性出现 → Chaos Monkey/Gremlin，注入故障
**统计方法**：小比例案例 → Delta 调试，对比成功与失败

### 5. Intelligent Instrumentation
AI 建议最优断点/日志点位置：
- 受影响功能的入口点
- 行为分叉的决策节点
- 状态变更点
- 外部集成边界
- 错误处理路径

在生产类环境中使用条件断点和日志点。

### 6. Production-Safe Techniques
**动态插桩**：OpenTelemetry spans，非侵入式属性
**功能开关控制的调试日志**：针对特定用户的条件日志
**采样分析**：持续分析，开销极小
**只读调试端点**：受认证保护、限流的状态检查
**渐进式流量迁移**：金丝雀部署调试版本到 10% 流量

### 7. Root Cause Analysis
AI 驱动的代码流分析：
- 完整执行路径重建
- 决策点的变量状态追踪
- 外部依赖交互分析
- 时序/序列图生成
- 代码异味检测
- 相似 bug 模式识别
- 修复复杂度估算

### 8. Fix Implementation
AI 生成修复方案，包含：
- 所需代码变更
- 影响评估
- 风险等级
- 测试覆盖需求
- 回滚策略

### 9. Validation
修复后验证：
- 运行测试套件
- 性能对比（基线 vs 修复后）
- 金丝雀部署（监控错误率）
- AI 代码审查修复内容

成功标准：
- 测试通过
- 无性能回退
- 错误率不变或下降
- 未引入新的边界情况

### 10. Prevention
- 使用 AI 生成回归测试
- 将根因更新到知识库
- 为类似问题添加监控/告警
- 在运维手册中记录故障排查步骤

## Example: Minimal Debug Session

```typescript
// 问题："结账超时错误（间歇性）"

// 1. 初始分析
const analysis = await aiAnalyze({
  error: "Payment processing timeout",
  frequency: "5% of checkouts",
  environment: "production"
});
// AI 建议："可能是 N+1 查询或外部 API 超时"

// 2. 收集可观测性数据
const sentryData = await getSentryIssue("CHECKOUT_TIMEOUT");
const ddTraces = await getDataDogTraces({
  service: "checkout",
  operation: "process_payment",
  duration: ">5000ms"
});

// 3. 分析追踪数据
// AI 识别：每次结账有 15+ 次顺序数据库查询
// 假设：支付方式加载中的 N+1 查询

// 4. 添加插桩
span.setAttribute('debug.queryCount', queryCount);
span.setAttribute('debug.paymentMethodId', methodId);

// 5. 部署到 10% 流量，监控
// 确认：支付验证中存在 N+1 模式

// 6. AI 生成修复
// 将顺序查询替换为批量查询

// 7. 验证
// - 测试通过
// - 延迟降低 70%
// - 查询次数：15 → 1
```

## Output Format

提供结构化报告：
1. **问题摘要**：错误、频率、影响
2. **根因**：带证据的详细诊断
3. **修复建议**：代码变更、风险、影响
4. **验证计划**：验证修复的步骤
5. **预防措施**：测试、监控、文档

专注于可操作的洞察。全程使用 AI 辅助进行模式识别、假设生成和修复验证。

---

待调试问题：$ARGUMENTS

## Limitations
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
