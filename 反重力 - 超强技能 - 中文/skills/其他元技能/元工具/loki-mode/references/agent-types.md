# 智能体类型参考

所有 37 种专业智能体类型的完整定义和能力。

---

## 概述

Loki Mode 有 37 种预定义智能体类型，组织成 7 个专业群。编排器仅为您的项目生成所需的智能体 - 简单应用可能使用 5-10 个智能体，而复杂初创公司可能生成 100+ 个并行工作的智能体。

---

## 工程群（8 种类型）

| 智能体 | 能力 |
|-------|-------------|
| `eng-frontend` | React/Vue/Svelte、TypeScript、Tailwind、无障碍、响应式设计、状态管理 |
| `eng-backend` | Node/Python/Go、REST/GraphQL、认证、业务逻辑、中间件、验证 |
| `eng-database` | PostgreSQL/MySQL/MongoDB、迁移、查询优化、索引、备份 |
| `eng-mobile` | React Native/Flutter/Swift/Kotlin、离线优先、推送通知、应用商店准备 |
| `eng-api` | OpenAPI 规格、SDK 生成、版本控制、webhook、速率限制、文档 |
| `eng-qa` | 单元/集成/E2E 测试、覆盖率、自动化、测试数据管理 |
| `eng-perf` | 性能分析、基准测试、优化、缓存、负载测试、内存分析 |
| `eng-infra` | Docker、K8s 清单、IaC 审查、网络、安全加固 |

---

## 运维群（8 种类型）

| 智能体 | 能力 |
|-------|-------------|
| `ops-devops` | CI/CD 管道、GitHub Actions、GitLab CI、Jenkins、构建优化 |
| `ops-sre` | 可靠性、SLO/SLI、容量规划、值班、运维手册 |
| `ops-security` | SAST/DAST、渗透测试、漏洞管理、安全审查 |
| `ops-monitor` | 可观测性、Datadog/Grafana、告警、仪表板、日志聚合 |
| `ops-incident` | 事故响应、运维手册、RCA、事后分析、沟通 |
| `ops-release` | 版本控制、变更日志、蓝绿、金丝雀、回滚、功能开关 |
| `ops-cost` | 云成本优化、合理配置、FinOps、预留实例 |
| `ops-compliance` | SOC2、GDPR、HIPAA、PCI-DSS、审计准备、策略执行 |

---

## 业务群（8 种类型）

| 智能体 | 能力 |
|-------|-------------|
| `biz-marketing` | 落地页、SEO、内容、邮件活动、社交媒体 |
| `biz-sales` | CRM 设置、外联、演示、提案、管道管理 |
| `biz-finance` | 计费（Stripe）、开票、指标、跑道、定价策略 |
| `biz-legal` | ToS、隐私政策、合同、IP 保护、合规文档 |
| `biz-support` | 帮助文档、FAQ、工单系统、聊天机器人、知识库 |
| `biz-hr` | 职位发布、招聘、入职、文化文档、团队结构 |
| `biz-investor` | 路演文稿、投资人更新、数据室、股权表管理 |
| `biz-partnerships` | BD 外联、集成合作、联合营销、API 合作 |

---

## 数据群（3 种类型）

| 智能体 | 能力 |
|-------|-------------|
| `data-ml` | 模型训练、MLOps、特征工程、推理、模型监控 |
| `data-eng` | ETL 管道、数据仓库、dbt、Airflow、数据质量 |
| `data-analytics` | 产品分析、A/B 测试、仪表板、洞察、报告 |

---

## 产品群（3 种类型）

| 智能体 | 能力 |
|-------|-------------|
| `prod-pm` | 积压梳理、优先级、路线图、规格、利益相关者管理 |
| `prod-design` | 设计系统、Figma、UX 模式、原型、用户研究 |
| `prod-techwriter` | API 文档、指南、教程、发布说明、开发者体验 |

---

## 增长群（4 种类型）

| 智能体 | 能力 |
|-------|-------------|
| `growth-hacker` | 增长实验、病毒循环、推荐计划、获客 |
| `growth-community` | 社区建设、Discord/Slack、大使计划、活动 |
| `growth-success` | 客户成功、健康评分、流失预防、扩展 |
| `growth-lifecycle` | 邮件生命周期、应用内消息、重新激活、入门 |

---

## 审查群（3 种类型）

| 智能体 | 能力 |
|-------|-------------|
| `review-code` | 代码质量、设计模式、SOLID、可维护性、最佳实践 |
| `review-business` | 需求对齐、业务逻辑、边界情况、UX 流程 |
| `review-security` | 漏洞、认证/授权、OWASP Top 10、数据保护 |

---

## 智能体执行模型

**Claude Code 不支持后台进程。** 智能体通过以下方式执行：

1. **角色切换（推荐）：** 编排器维护智能体队列，按任务切换角色
2. **顺序：** 逐个执行智能体（简单、可靠）
3. **通过 tmux 并行：** 多个 Claude Code 会话（复杂、更快）

```bash
# 选项 1：顺序（简单、可靠）
for agent in frontend backend database; do
  claude -p "Act as $agent agent..." --dangerously-skip-permissions
done

# 选项 2：通过 tmux 并行（复杂、更快）
tmux new-session -d -s loki-pool
for i in {1..5}; do
  tmux new-window -t loki-pool -n "agent-$i" \
    "claude --dangerously-skip-permissions -p '$(cat .loki/prompts/agent-$i.md)'"
done

# 选项 3：角色切换（推荐）
# 编排器维护智能体队列，按任务切换角色
```

---

## 按智能体类型的模型选择

| 任务类型 | 模型 | 原因 |
|-----------|-------|--------|
| 实现 | Sonnet | 快速，编码足够好 |
| 代码审查 | Opus | 深度分析，捕捉细微问题 |
| 安全审查 | Opus | 关键，需要彻底性 |
| 业务逻辑审查 | Opus | 需要深入理解需求 |
| 文档 | Sonnet | 直接的写作 |
| 快速修复 | Haiku | 快速迭代 |

---

## 智能体生命周期

```
SPAWN -> INITIALIZE -> POLL_QUEUE -> CLAIM_TASK -> EXECUTE -> REPORT -> POLL_QUEUE
           |              |                        |          |
           |         circuit open?             timeout?    success?
           |              |                        |          |
           v              v                        v          v
     Create state    WAIT_BACKOFF              RELEASE    UPDATE_STATE
                          |                    + RETRY         |
                     exponential                              |
                       backoff                                v
                                                    NO_TASKS --> IDLE (5min)
                                                                    |
                                                             idle > 30min?
                                                                    |
                                                                    v
                                                               TERMINATE
```

---

## 动态扩展规则

| 条件 | 操作 | 冷却 |
|-----------|--------|----------|
| 队列深度 > 20 | 生成 2 个瓶颈类型智能体 | 5min |
| 队列深度 > 50 | 生成 5 个智能体，告警编排器 | 2min |
| 智能体空闲 > 30min | 终止智能体 | - |
| 智能体连续失败 3 次 | 终止，打开熔断器 | 5min |
| 关键任务等待 > 10min | 生成优先智能体 | 1min |
| 熔断器半开 | 生成 1 个测试智能体 | - |
| 该类型所有智能体失败 | HALT，请求人工干预 | - |

---

## 智能体上下文保存

### 血统规则
1. **不可变继承：** 智能体不能修改继承的上下文
2. **决策日志：** 所有决策必须记录到智能体上下文文件
3. **血统引用：** 所有提交必须引用父智能体 ID
4. **上下文交接：** 智能体完成时，上下文被归档但血统保留

### 防止上下文漂移
1. 生成前读取 `.agent/sub-agents/${parent_id}.json`
2. 继承不可变上下文（技术栈、约束、决策）
3. 将所有新决策记录到自己的上下文文件
4. 在所有提交中引用血统
5. 定期上下文同步：检查继承的上下文是否在上游更新
