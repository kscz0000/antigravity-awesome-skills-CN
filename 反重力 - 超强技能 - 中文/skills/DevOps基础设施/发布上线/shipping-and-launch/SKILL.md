---
name: shipping-and-launch
description: 准备生产环境发布。当准备部署到生产环境时使用。当需要发布前检查清单、设置监控、规划分阶段发布或需要回滚策略时使用。
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/shipping-and-launch
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# Shipping and Launch

## 概述

自信地发布。目标不仅仅是部署——而是安全地部署，监控到位、回滚方案就绪、对成功的定义清晰明确。每次发布都应该是可逆的、可观测的、渐进的。

## 适用场景

- 首次将功能部署到生产环境
- 向用户发布重大变更
- 迁移数据或基础设施
- 开放测试版或抢先体验计划
- 任何有风险的部署（实际上所有部署都有风险）

## 发布前检查清单

### 代码质量

- [ ] 所有测试通过（单元测试、集成测试、端到端测试）
- [ ] 构建成功且无警告
- [ ] Lint 和类型检查通过
- [ ] 代码已审查并批准
- [ ] 没有应在发布前解决的 TODO 注释
- [ ] 生产代码中没有 `console.log` 调试语句
- [ ] 错误处理覆盖了预期的故障模式

### 安全

- [ ] 代码和版本控制中没有密钥
- [ ] `npm audit` 没有严重或高危漏洞
- [ ] 所有面向用户的端点都有输入验证
- [ ] 认证和授权检查已就位
- [ ] 安全头已配置（CSP、HSTS 等）
- [ ] 认证端点已设置速率限制
- [ ] CORS 已配置为特定来源（非通配符）

### 性能

- [ ] Core Web Vitals 在"良好"阈值范围内
- [ ] 关键路径中没有 N+1 查询
- [ ] 图片已优化（压缩、响应式尺寸、懒加载）
- [ ] 包体积在预算范围内
- [ ] 数据库查询有合适的索引
- [ ] 静态资源和重复查询已配置缓存

### 无障碍

- [ ] 所有交互元素都支持键盘导航
- [ ] 屏幕阅读器能够传达页面内容和结构
- [ ] 颜色对比度满足 WCAG 2.1 AA 标准（文本 4.5:1）
- [ ] 模态框和动态内容的焦点管理正确
- [ ] 错误信息具有描述性并与表单字段关联
- [ ] axe-core 或 Lighthouse 中没有无障碍警告

### 基础设施

- [ ] 生产环境的环境变量已设置
- [ ] 数据库迁移已应用（或已准备好应用）
- [ ] DNS 和 SSL 已配置
- [ ] CDN 已为静态资源配置
- [ ] 日志和错误报告已配置
- [ ] 健康检查端点存在且正常响应

### 文档

- [ ] README 已更新（如有新的配置要求）
- [ ] API 文档是最新的
- [ ] 架构决策已编写 ADR
- [ ] 变更日志已更新
- [ ] 面向用户的文档已更新（如适用）

## 功能开关策略

在功能开关之后发布，将部署与发布解耦：

```typescript
// Feature flag check
const flags = await getFeatureFlags(userId);

if (flags.taskSharing) {
  // New feature: task sharing
  return <TaskSharingPanel task={task} />;
}

// Default: existing behavior
return null;
```

**功能开发生命周期：**

```
1. DEPLOY with flag OFF     → Code is in production but inactive
2. ENABLE for team/beta     → Internal testing in production environment
3. GRADUAL ROLLOUT          → 5% → 25% → 50% → 100% of users
4. MONITOR at each stage    → Watch error rates, performance, user feedback
5. CLEAN UP                 → Remove flag and dead code path after full rollout
```

**规则：**
- 每个功能开关都有负责人和过期日期
- 全面发布后 2 周内清理开关
- 不要嵌套功能开关（会产生指数级组合）
- 在 CI 中测试开关的两种状态（开和关）

## 分阶段发布

### 发布序列

```
1. DEPLOY to staging
   └── Full test suite in staging environment
   └── Manual smoke test of critical flows

2. DEPLOY to production (feature flag OFF)
   └── Verify deployment succeeded (health check)
   └── Check error monitoring (no new errors)

3. ENABLE for team (flag ON for internal users)
   └── Team uses the feature in production
   └── 24-hour monitoring window

4. CANARY rollout (flag ON for 5% of users)
   └── Monitor error rates, latency, user behavior
   └── Compare metrics: canary vs. baseline
   └── 24-48 hour monitoring window
   └── Advance only if all thresholds pass (see table below)

5. GRADUAL increase (25% -> 50% -> 100%)
   └── Same monitoring at each step
   └── Ability to roll back to previous percentage at any point

6. FULL rollout (flag ON for all users)
   └── Monitor for 1 week
   └── Clean up feature flag
```

### 发布决策阈值

使用以下阈值决定在每个阶段是推进、暂停还是回滚：

| 指标 | 推进（绿色） | 暂停调查（黄色） | 回滚（红色） |
|--------|-----------------|-------------------------------|-----------------|
| 错误率 | 在基线的 10% 以内 | 高于基线 10-100% | 超过基线 2 倍 |
| P95 延迟 | 在基线的 20% 以内 | 高于基线 20-50% | 超过基线 50% |
| 客户端 JS 错误 | 无新错误类型 | 新错误占比 <0.1% 会话 | 新错误占比 >0.1% 会话 |
| 业务指标 | 中性或正向 | 下降 <5%（可能是噪声） | 下降 >5% |

### 何时回滚

在以下情况立即回滚：
- 错误率超过基线 2 倍以上
- P95 延迟超过基线 50% 以上
- 用户报告的问题激增
- 检测到数据完整性问题
- 发现安全漏洞

## 监控与可观测性

### 监控内容

```
Application metrics:
├── Error rate (total and by endpoint)
├── Response time (p50, p95, p99)
├── Request volume
├── Active users
└── Key business metrics (conversion, engagement)

Infrastructure metrics:
├── CPU and memory utilization
├── Database connection pool usage
├── Disk space
├── Network latency
└── Queue depth (if applicable)

Client metrics:
├── Core Web Vitals (LCP, INP, CLS)
├── JavaScript errors
├── API error rates from client perspective
└── Page load time
```

### 错误报告

```typescript
// Set up error boundary with reporting
class ErrorBoundary extends React.Component {
  componentDidCatch(error: Error, info: React.ErrorInfo) {
    // Report to error tracking service
    reportError(error, {
      componentStack: info.componentStack,
      userId: getCurrentUser()?.id,
      page: window.location.pathname,
    });
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback onRetry={() => this.setState({ hasError: false })} />;
    }
    return this.props.children;
  }
}

// Server-side error reporting
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  reportError(err, {
    method: req.method,
    url: req.url,
    userId: req.user?.id,
  });

  // Don't expose internals to users
  res.status(500).json({
    error: { code: 'INTERNAL_ERROR', message: 'Something went wrong' },
  });
});
```

### 发布后验证

发布后的第一个小时内：

```
1. Check health endpoint returns 200
2. Check error monitoring dashboard (no new error types)
3. Check latency dashboard (no regression)
4. Test the critical user flow manually
5. Verify logs are flowing and readable
6. Confirm rollback mechanism works (dry run if possible)
```

## 回滚策略

每次部署在发生之前都需要回滚方案：

```markdown
## Rollback Plan for [Feature/Release]

### Trigger Conditions
- Error rate > 2x baseline
- P95 latency > [X]ms
- User reports of [specific issue]

### Rollback Steps
1. Disable feature flag (if applicable)
   OR
1. Deploy previous version: `git revert <commit> && git push`
2. Verify rollback: health check, error monitoring
3. Communicate: notify team of rollback

### Database Considerations
- Migration [X] has a rollback: `npx prisma migrate rollback`
- Data inserted by new feature: [preserved / cleaned up]

### Time to Rollback
- Feature flag: < 1 minute
- Redeploy previous version: < 5 minutes
- Database rollback: < 15 minutes
```
## 另见

- 关于每次变更必须通过的项目级完成定义（在应用本检查清单之前），参见 `references/definition-of-done.md`
- 安全发布前检查，参见 `references/security-checklist.md`
- 性能发布前检查清单，参见 `references/performance-checklist.md`
- 发布前无障碍验证，参见 `references/accessibility-checklist.md`

## 常见自我辩解

| 自我辩解 | 现实 |
|---|---|
| "在测试环境能用，在生产环境也能用" | 生产环境有不同的数据、流量模式和边界情况。部署后要监控。 |
| "这个功能不需要功能开关" | 每个功能都受益于紧急开关。即使"简单"的变更也可能出问题。 |
| "监控是额外开销" | 没有监控意味着你从用户投诉而不是仪表盘发现问题。 |
| "监控以后再加" | 在发布前加上。你看不到的问题就无法调试。 |
| "回滚等于承认失败" | 回滚是负责任的工程实践。发布有问题的功能才是失败。 |

## 危险信号

- 没有回滚方案就部署
- 生产环境没有监控或错误报告
- 一次性大发布（所有内容一起上，没有分阶段）
- 功能开关没有过期日期或负责人
- 部署后的第一个小时没有人监控
- 生产环境配置靠记忆而不是代码
- "周五下午了，直接发吧"

## 验证

部署前：

- [ ] 发布前检查清单已完成（所有部分为绿色）
- [ ] 功能开关已配置（如适用）
- [ ] 回滚方案已记录
- [ ] 监控仪表盘已设置
- [ ] 团队已被告知部署计划

部署后：

- [ ] 健康检查返回 200
- [ ] 错误率正常
- [ ] 延迟正常
- [ ] 关键用户流程正常
- [ ] 日志正常流动
- [ ] 回滚机制已测试或确认就绪

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用变更之前，请验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代特定环境的测试、安全审查或用户对破坏性或高成本操作的批准。
