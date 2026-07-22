# SDLC 阶段参考

所有阶段的详细工作流和测试流程。

---

## 阶段概述

```
Bootstrap -> Discovery -> Architecture -> Infrastructure
     |           |            |              |
  (设置)    (分析 PRD)   (设计)      (云/数据库设置)
                                             |
Development <- QA <- Deployment <- Business Ops <- Growth Loop
     |         |         |            |            |
  (构建)    (测试)    (发布)       (监控)       (迭代)
```

---

## 阶段 0：Bootstrap

**目的：** 初始化 Loki Mode 环境

### 操作：
1. 创建 `.loki/` 目录结构
2. 在 `.loki/state/orchestrator.json` 中初始化编排器状态
3. 验证 PRD 存在且可读
4. 生成初始智能体池（3-5 个智能体）
5. 创建 CONTINUITY.md

### 创建的目录结构：
```
.loki/
+-- CONTINUITY.md
+-- state/
|   +-- orchestrator.json
|   +-- agents/
|   +-- circuit-breakers/
+-- queue/
|   +-- pending.json
|   +-- in-progress.json
|   +-- completed.json
|   +-- dead-letter.json
+-- specs/
+-- memory/
+-- artifacts/
```

---

## 阶段 1：Discovery

**目的：** 理解需求和市场背景

### 操作：
1. 解析 PRD，提取需求
2. 生成 `biz-analytics` 智能体进行竞争研究
3. 网络搜索竞争对手，提取功能、评论
4. 识别市场空白和机会
5. 生成带优先级和依赖关系的任务积压

### 输出：
- 需求文档
- 竞争分析
- `.loki/queue/pending.json` 中的初始任务积压

---

## 阶段 2：Architecture

**目的：** 设计系统架构并生成规格

### 规格优先工作流

**步骤 1：从 PRD 提取 API 需求**
- 解析 PRD 中的用户故事和功能
- 映射到 REST/GraphQL 操作
- 文档化数据模型和关系

**步骤 2：生成 OpenAPI 3.1 规格**

```yaml
openapi: 3.1.0
info:
  title: Product API
  version: 1.0.0
paths:
  /auth/login:
    post:
      summary: 认证用户并返回 JWT
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email: { type: string, format: email }
                password: { type: string, minLength: 8 }
      responses:
        200:
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  token: { type: string }
                  expiresAt: { type: string, format: date-time }
        401:
          description: 凭证无效
```

**步骤 3：验证规格**
```bash
npm install -g @stoplight/spectral-cli
spectral lint .loki/specs/openapi.yaml
swagger-cli validate .loki/specs/openapi.yaml
```

**步骤 4：从规格生成产物**
```bash
# TypeScript 类型
npx openapi-typescript .loki/specs/openapi.yaml --output src/types/api.ts

# 客户端 SDK
npx openapi-generator-cli generate \
  -i .loki/specs/openapi.yaml \
  -g typescript-axios \
  -o src/clients/api

# 服务端存根
npx openapi-generator-cli generate \
  -i .loki/specs/openapi.yaml \
  -g nodejs-express-server \
  -o backend/generated

# 文档
npx redoc-cli bundle .loki/specs/openapi.yaml -o docs/api.html
```

**步骤 5：选择技术栈**
- 生成 `eng-backend` + `eng-frontend` 架构师
- 两个智能体审查规格并提议技术栈
- 需要共识（两者必须同意）
- 带证据的自我反思检查点

**步骤 6：创建项目脚手架**
- 用技术栈初始化项目
- 安装依赖
- 配置 linter
- 设置契约测试框架

---

## 阶段 3：Infrastructure

**目的：** 配置云资源和 CI/CD

### 操作：
1. 生成 `ops-devops` 智能体
2. 配置云资源（见 `references/deployment.md`）
3. 设置 CI/CD 管道
4. 配置监控和告警
5. 创建 staging 和生产环境

### CI/CD 管道：
```yaml
name: CI/CD Pipeline
on: [push, pull_request]
jobs:
  test:
    - Lint
    - Type check
    - Unit tests
    - Contract tests
    - Security scan
  deploy-staging:
    needs: test
    - Deploy to staging
    - Smoke tests
  deploy-production:
    needs: deploy-staging
    - Blue-green deploy
    - Health checks
    - Auto-rollback on errors
```

---

## 阶段 4：Development

**目的：** 带质量门实现功能

### 每任务工作流：

```
1. 调度实现子智能体（Task 工具，模型：sonnet）
2. 子智能体用 TDD 实现，提交，报告
3. 并行调度 3 个审查者（单消息，3 个 Task 调用）：
   - code-reviewer (opus)
   - business-logic-reviewer (opus)
   - security-reviewer (opus)
4. 按严重程度聚合发现
5. 若发现 Critical/High/Medium：
   - 调度修复子智能体
   - 重新运行所有 3 个审查者
   - 循环直到全部通过
6. 为 Low 问题添加 TODO 注释
7. 为 Cosmetic 问题添加 FIXME 注释
8. 用 git 检查点标记任务完成
```

### 实现规则：
- 智能体仅实现规格中的内容
- 必须根据 openapi.yaml 模式验证
- 必须返回匹配规格的响应
- 性能目标来自 spec x-performance 扩展

---

## 阶段 5：Quality Assurance

**目的：** 全面测试和安全审计

### 测试阶段：

**单元阶段：**
```bash
npm run test:unit
# 或
pytest tests/unit/
```
- 覆盖率：>80% 要求
- 所有测试必须通过

**集成阶段：**
```bash
npm run test:integration
```
- 针对实际数据库测试 API 端点
- 测试外部服务集成
- 验证端到端数据流

**E2E 阶段：**
```bash
npx playwright test
# 或
npx cypress run
```
- 测试完整用户流程
- 跨浏览器测试
- 移动响应式测试

**契约阶段：**
```bash
npm run test:contract
```
- 验证实现匹配 OpenAPI 规格
- 测试请求/响应模式
- 破坏性变更检测

**安全阶段：**
```bash
npm audit
npx snyk test
semgrep --config=auto .
```
- OWASP Top 10 检查
- 依赖漏洞
- 静态分析

**性能阶段：**
```bash
npx k6 run tests/load.js
npx lighthouse http://localhost:3000
```
- 负载测试：100 并发用户持续 1 分钟
- 压力测试：500 并发用户持续 30 秒
- P95 响应时间 < 500ms 要求

**无障碍阶段：**
```bash
npx axe http://localhost:3000
```
- WCAG 2.1 AA 合规
- Alt 文本、ARIA 标签、颜色对比度
- 键盘导航、焦点指示器

**回归阶段：**
- 与前一版本比较行为
- 验证最近更改未破坏功能
- 测试 API 向后兼容性

**UAT 阶段：**
- 从 PRD 创建验收测试
- 演练完整用户旅程
- 验证业务逻辑匹配 PRD
- 文档化任何 UX 摩擦点

---

## 阶段 6：Deployment

**目的：** 发布到生产环境

### 操作：
1. 生成 `ops-release` 智能体
2. 生成语义版本、变更日志
3. 创建发布分支、标签
4. 部署到 staging，运行冒烟测试
5. 蓝绿部署到生产环境
6. 监控 30 分钟，错误激增时自动回滚

### 部署策略：

**蓝绿：**
```
1. 部署新版本到 "green" 环境
2. 运行冒烟测试
3. 将流量从 "blue" 切换到 "green"
4. 保留 "blue" 作为回滚目标
```

**金丝雀：**
```
1. 部署到 5% 流量
2. 监控错误率
3. 逐步增加到 25%、50%、100%
4. 若错误超过阈值则回滚
```

---

## 阶段 7：Business Operations

**目的：** 非技术业务设置

### 操作：
1. `biz-marketing`：创建落地页、SEO、内容
2. `biz-sales`：设置 CRM、外联模板
3. `biz-finance`：配置计费（Stripe）、开票
4. `biz-support`：创建帮助文档、聊天机器人
5. `biz-legal`：生成 ToS、隐私政策

---

## 阶段 8：Growth Loop

**目的：** 持续改进

### 循环：
```
MONITOR -> ANALYZE -> OPTIMIZE -> DEPLOY -> MONITOR
    |
客户反馈 -> 功能请求 -> 积压
    |
A/B 测试 -> 胜出者 -> 永久部署
    |
事故 -> RCA -> 预防 -> 部署修复
```

### 永不"完成"：
- 运行性能优化
- 添加缺失的测试覆盖
- 改进文档
- 重构代码异味
- 更新依赖
- 增强用户体验
- 实现 A/B 测试学习

---

## 最终审查（任何部署前）

```
1. 调度 3 个审查者审查整个实现：
   - code-reviewer：完整代码库质量
   - business-logic-reviewer：所有需求满足
   - security-reviewer：完整安全审计

2. 跨所有文件聚合发现
3. 修复 Critical/High/Medium 问题
4. 重新运行所有 3 个审查者直到全部通过
5. 在 .loki/artifacts/reports/final-review.md 生成最终报告
6. 仅在全部通过后进行部署
```

---

## 质量门总结

| 门 | 智能体 | 通过标准 |
|------|-------|---------------|
| 单元测试 | eng-qa | 100% 通过 |
| 集成测试 | eng-qa | 100% 通过 |
| E2E 测试 | eng-qa | 100% 通过 |
| 覆盖率 | eng-qa | > 80% |
| Linting | eng-qa | 0 错误 |
| 类型检查 | eng-qa | 0 错误 |
| 安全扫描 | ops-security | 0 高/严重 |
| 依赖审计 | ops-security | 0 漏洞 |
| 性能 | eng-qa | p99 < 200ms |
| 无障碍 | eng-frontend | WCAG 2.1 AA |
| 负载测试 | ops-devops | 处理 10x 预期流量 |
| 混沌测试 | ops-devops | 从故障中恢复 |
| 成本估算 | ops-cost | 预算内 |
| 法律审查 | biz-legal | 合规 |
