# 基于多智能体编排的智能问题排查与修复 — 实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

# 基于多智能体编排的智能问题排查与修复

[Extended thinking: This workflow implements a sophisticated debugging and resolution pipeline that leverages AI-assisted debugging tools and observability platforms to systematically diagnose and resolve production issues. The intelligent debugging strategy combines automated root cause analysis with human expertise, using modern 2024/2025 practices including AI code assistants (GitHub Copilot, Claude Code), observability platforms (Sentry, DataDog, OpenTelemetry), git bisect automation for regression tracking, and production-safe debugging techniques like distributed tracing and structured logging. The process follows a rigorous four-phase approach: (1) Issue Analysis Phase - error-detective and debugger agents analyze error traces, logs, reproduction steps, and observability data to understand the full context of the failure including upstream/downstream impacts, (2) Root Cause Investigation Phase - debugger and code-reviewer agents perform deep code analysis, automated git bisect to identify introducing commit, dependency compatibility checks, and state inspection to isolate the exact failure mechanism, (3) Fix Implementation Phase - domain-specific agents (python-pro, typescript-pro, rust-expert, etc.) implement minimal fixes with comprehensive test coverage including unit, integration, and edge case tests while following production-safe practices, (4) Verification Phase - test-automator and performance-engineer agents run regression suites, performance benchmarks, security scans, and verify no new issues are introduced. Complex issues spanning multiple systems require orchestrated coordination between specialist agents (database-optimizer → performance-engineer → devops-troubleshooter) with explicit context passing and state sharing. The workflow emphasizes understanding root causes over treating symptoms, implementing lasting architectural improvements, automating detection through enhanced monitoring and alerting, and preventing future occurrences through ty[... 241 chars omitted ...]

## 阶段1：问题分析 — 错误检测与上下文收集

使用 Task 工具，先后调用 subagent_type="error-debugging::error-detective" 和 subagent_type="error-debugging::debugger"：

**第一步：错误侦探分析**

**提示词：**
```
Analyze error traces, logs, and observability data for: $ARGUMENTS

Deliverables:
1. Error signature analysis: exception type, message patterns, frequency, first occurrence
2. Stack trace deep dive: failure location, call chain, involved components
3. Reproduction steps: minimal test case, environment requirements, data fixtures needed
4. Observability context:
   - Sentry/DataDog error groups and trends
   - Distributed traces showing request flow (OpenTelemetry/Jaeger)
   - Structured logs (JSON logs with correlation IDs)
   - APM metrics: latency spikes, error rates, resource usage
5. User impact assessment: affected user segments, error rate, business metrics impact
6. Timeline analysis: when did it start, correlation with deployments/config changes
7. Related symptoms: similar errors, cascading failures, upstream/downstream impacts

Modern debugging techniques to employ:
- AI-assisted log analysis (pattern detection, anomaly identification)
- Distributed trace correlation across microservices
- Production-safe debugging (no code changes, use observability data)
- Error fingerprinting for deduplication and tracking
```

**预期输出：**
```
ERROR_SIGNATURE: {exception type + key message pattern}
FREQUENCY: {count, rate, trend}
FIRST_SEEN: {timestamp or git commit}
STACK_TRACE: {formatted trace with key frames highlighted}
REPRODUCTION: {minimal steps + sample data}
OBSERVABILITY_LINKS: [Sentry URL, DataDog dashboard, trace IDs]
USER_IMPACT: {affected users, severity, business impact}
TIMELINE: {when started, correlation with changes}
RELATED_ISSUES: [similar errors, cascading failures]
```

**第二步：调试器根因定位**

**提示词：**
```
Perform root cause investigation using error-detective output:

Context from Error-Detective:
- Error signature: {ERROR_SIGNATURE}
- Stack trace: {STACK_TRACE}
- Reproduction: {REPRODUCTION}
- Observability: {OBSERVABILITY_LINKS}

Deliverables:
1. Root cause hypothesis with supporting evidence
2. Code-level analysis: variable states, control flow, timing issues
3. Git bisect analysis: identify introducing commit (automate with git bisect run)
4. Dependency analysis: version conflicts, API changes, configuration drift
5. State inspection: database state, cache state, external API responses
6. Failure mechanism: why does the code fail under these specific conditions
7. Fix strategy options with tradeoffs (quick fix vs proper fix)

Context needed for next phase:
- Exact file paths and line numbers requiring changes
- Data structures or API contracts affected
- Dependencies that may need updates
- Test scenarios to verify the fix
- Performance characteristics to maintain
```

**预期输出：**
```
ROOT_CAUSE: {technical explanation with evidence}
INTRODUCING_COMMIT: {git SHA + summary if found via bisect}
AFFECTED_FILES: [file paths with specific line numbers]
FAILURE_MECHANISM: {why it fails - race condition, null check, type mismatch, etc}
DEPENDENCIES: [related systems, libraries, external APIs]
FIX_STRATEGY: {recommended approach with reasoning}
QUICK_FIX_OPTION: {temporary mitigation if applicable}
PROPER_FIX_OPTION: {long-term solution}
TESTING_REQUIREMENTS: [scenarios that must be covered]
```

## 阶段2：根因调查 — 深度代码分析

使用 Task 工具，调用 subagent_type="error-debugging::debugger" 和 subagent_type="comprehensive-review::code-reviewer" 进行系统性调查：

**第一步：调试器代码分析**

**提示词：**
```
Perform deep code analysis and bisect investigation:

Context from Phase 1:
- Root cause: {ROOT_CAUSE}
- Affected files: {AFFECTED_FILES}
- Failure mechanism: {FAILURE_MECHANISM}
- Introducing commit: {INTRODUCING_COMMIT}

Deliverables:
1. Code path analysis: trace execution from entry point to failure
2. Variable state tracking: values at key decision points
3. Control flow analysis: branches taken, loops, async operations
4. Git bisect automation: create bisect script to identify exact breaking commit
   ```bash
   git bisect start HEAD v1.2.3
   git bisect run ./test_reproduction.sh
   ```
5. Dependency compatibility matrix: version combinations that work/fail
6. Configuration analysis: environment variables, feature flags, deployment configs
7. Timing and race condition analysis: async operations, event ordering, locks
8. Memory and resource analysis: leaks, exhaustion, contention

Modern investigation techniques:
- AI-assisted code explanation (Claude/Copilot to understand complex logic)
- Automated git bisect with reproduction test
- Dependency graph analysis (npm ls, go mod graph, pip show)
- Configuration drift detection (compare staging vs production)
- Time-travel debugging using production traces
```

**预期输出：**
```
CODE_PATH: {entry → ... → failure location with key variables}
STATE_AT_FAILURE: {variable values, object states, database state}
BISECT_RESULT: {exact commit that introduced bug + diff}
DEPENDENCY_ISSUES: [version conflicts, breaking changes, CVEs]
CONFIGURATION_DRIFT: {differences between environments}
RACE_CONDITIONS: {async issues, event ordering problems}
ISOLATION_VERIFICATION: {confirmed single root cause vs multiple issues}
```

**第二步：代码审查员深度审查**

**提示词：**
```
Review code logic and identify design issues:

Context from Debugger:
- Code path: {CODE_PATH}
- State at failure: {STATE_AT_FAILURE}
- Bisect result: {BISECT_RESULT}

Deliverables:
1. Logic flaw analysis: incorrect assumptions, missing edge cases, wrong algorithms
2. Type safety gaps: where stronger types could prevent the issue
3. Error handling review: missing try-catch, unhandled promises, panic scenarios
4. Contract validation: input validation gaps, output guarantees not met
5. Architectural issues: tight coupling, missing abstractions, layering violations
6. Similar patterns: other code locations with same vulnerability
7. Fix design: minimal change vs refactoring vs architectural improvement

Review checklist:
- Are null/undefined values handled correctly?
- Are async operations properly awaited/chained?
- Are error cases explicitly handled?
- Are type assertions safe?
- Are API contracts respected?
- Are side effects isolated?
```

**预期输出：**
```
LOGIC_FLAWS: [specific incorrect assumptions or algorithms]
TYPE_SAFETY_GAPS: [where types could prevent issues]
ERROR_HANDLING_GAPS: [unhandled error paths]
SIMILAR_VULNERABILITIES: [other code with same pattern]
FIX_DESIGN: {minimal change approach}
REFACTORING_OPPORTUNITIES: {if larger improvements warranted}
ARCHITECTURAL_CONCERNS: {if systemic issues exist}
```

## 阶段3：修复实施 — 领域专用智能体执行

根据阶段2的输出，使用 Task 工具路由到对应的领域智能体：

**路由逻辑：**
- Python 问题 → subagent_type="python-development::python-pro"
- TypeScript/JavaScript → subagent_type="javascript-typescript::typescript-pro"
- Go → subagent_type="systems-programming::golang-pro"
- Rust → subagent_type="systems-programming::rust-pro"
- SQL/数据库 → subagent_type="database-cloud-optimization::database-optimizer"
- 性能 → subagent_type="application-performance::performance-engineer"
- 安全 → subagent_type="security-scanning::security-auditor"

**提示词模板（按语言适配）：**
```
Implement production-safe fix with comprehensive test coverage:

Context from Phase 2:
- Root cause: {ROOT_CAUSE}
- Logic flaws: {LOGIC_FLAWS}
- Fix design: {FIX_DESIGN}
- Type safety gaps: {TYPE_SAFETY_GAPS}
- Similar vulnerabilities: {SIMILAR_VULNERABILITIES}

Deliverables:
1. Minimal fix implementation addressing root cause (not symptoms)
2. Unit tests:
   - Specific failure case reproduction
   - Edge cases (boundary values, null/empty, overflow)
   - Error path coverage
3. Integration tests:
   - End-to-end scenarios with real dependencies
   - External API mocking where appropriate
   - Database state verification
4. Regression tests:
   - Tests for similar vulnerabilities
   - Tests covering related code paths
5. Performance validation:
   - Benchmarks showing no degradation
   - Load tests if applicable
6. Production-safe practices:
   - Feature flags for gradual rollout
   - Graceful degradation if fix fails
   - Monitoring hooks for fix verification
   - Structured logging for debugging

Modern implementation techniques (2024/2025):
- AI pair programming (GitHub Copilot, Claude Code) for test generation
- Type-driven development (leverage TypeScript, mypy, clippy)
- Contract-first APIs (OpenAPI, gRPC schemas)
- Observability-first (structured logs, metrics, traces)
- Defensive programming (explicit error handling, validation)

Implementation requirements:
- Follow existing code patterns and conventions
- Add strategic debug logging (JSON structured logs)
- Include comprehensive type annotations
- Update error messages to be actionable (include context, suggestions)
- Maintain backward compatibility (version APIs if breaking)
- Add OpenTelemetry spans for distributed tracing
- Include metric counters for monitoring (success/failure rates)
```

**预期输出：**
```
FIX_SUMMARY: {what changed and why - root cause vs symptom}
CHANGED_FILES: [
  {path: "...", changes: "...", reasoning: "..."}
]
NEW_FILES: [{path: "...", purpose: "..."}]
TEST_COVERAGE: {
  unit: "X scenarios",
  integration: "Y scenarios",
  edge_cases: "Z scenarios",
  regression: "W scenarios"
}
TEST_RESULTS: {all_passed: true/false, details: "..."}
BREAKING_CHANGES: {none | API changes with migration path}
OBSERVABILITY_ADDITIONS: [
  {type: "log", location: "...", purpose: "..."},
  {type: "metric", name: "...", purpose: "..."},
  {type: "trace", span: "...", purpose: "..."}
]
FEATURE_FLAGS: [{flag: "...", rollout_strategy: "..."}]
BACKWARD_COMPATIBILITY: {maintained | breaking with mitigation}
```

## 阶段4：验证 — 自动化测试与性能验证

使用 Task 工具，调用 subagent_type="unit-testing::test-automator" 和 subagent_type="application-performance::performance-engineer"：

**第一步：测试自动化器回归套件**

**提示词：**
```
Run comprehensive regression testing and verify fix quality:

Context from Phase 3:
- Fix summary: {FIX_SUMMARY}
- Changed files: {CHANGED_FILES}
- Test coverage: {TEST_COVERAGE}
- Test results: {TEST_RESULTS}

Deliverables:
1. Full test suite execution:
   - Unit tests (all existing + new)
   - Integration tests
   - End-to-end tests
   - Contract tests (if microservices)
2. Regression detection:
   - Compare test results before/after fix
   - Identify any new failures
   - Verify all edge cases covered
3. Test quality assessment:
   - Code coverage metrics (line, branch, condition)
   - Mutation testing if applicable
   - Test determinism (run multiple times)
4. Cross-environment testing:
   - Test in staging/QA environments
   - Test with production-like data volumes
   - Test with realistic network conditions
5. Security testing:
   - Authentication/authorization checks
   - Input validation testing
   - SQL injection, XSS prevention
   - Dependency vulnerability scan
6. Automated regression test generation:
   - Use AI to generate additional edge case tests
   - Property-based testing for complex logic
   - Fuzzing for input validation

Modern testing practices (2024/2025):
- AI-generated test cases (GitHub Copilot, Claude Code)
- Snapshot testing for UI/API contracts
- Visual regression testing for frontend
- Chaos engineering for resilience testing
- Production traffic replay for load testing
```

**预期输出：**
```
TEST_RESULTS: {
  total: N,
  passed: X,
  failed: Y,
  skipped: Z,
  new_failures: [list if any],
  flaky_tests: [list if any]
}
CODE_COVERAGE: {
  line: "X%",
  branch: "Y%",
  function: "Z%",
  delta: "+/-W%"
}
REGRESSION_DETECTED: {yes/no + details if yes}
CROSS_ENV_RESULTS: {staging: "...", qa: "..."}
SECURITY_SCAN: {
  vulnerabilities: [list or "none"],
  static_analysis: "...",
  dependency_audit: "..."
}
TEST_QUALITY: {deterministic: true/false, coverage_adequate: true/false}
```

**第二步：性能工程师验证**

**提示词：**
```
Measure performance impact and validate no regressions:

Context from Test-Automator:
- Test results: {TEST_RESULTS}
- Code coverage: {CODE_COVERAGE}
- Fix summary: {FIX_SUMMARY}

Deliverables:
1. Performance benchmarks:
   - Response time (p50, p95, p99)
   - Throughput (requests/second)
   - Resource utilization (CPU, memory, I/O)
   - Database query performance
2. Comparison with baseline:
   - Before/after metrics
   - Acceptable degradation thresholds
   - Performance improvement opportunities
3. Load testing:
   - Stress test under peak load
   - Soak test for memory leaks
   - Spike test for burst handling
4. APM analysis:
   - Distributed trace analysis
   - Slow query detection
   - N+1 query patterns
5. Resource profiling:
   - CPU flame graphs
   - Memory allocation tracking
   - Goroutine/thread leaks
6. Production readiness:
   - Capacity planning impact
   - Scaling characteristics
   - Cost implications (cloud resources)

Modern performance practices:
- OpenTelemetry instrumentation
- Continuous profiling (Pyroscope, pprof)
- Real User Monitoring (RUM)
- Synthetic monitoring
```

**预期输出：**
```
PERFORMANCE_BASELINE: {
  response_time_p95: "Xms",
  throughput: "Y req/s",
  cpu_usage: "Z%",
  memory_usage: "W MB"
}
PERFORMANCE_AFTER_FIX: {
  response_time_p95: "Xms (delta)",
  throughput: "Y req/s (delta)",
  cpu_usage: "Z% (delta)",
  memory_usage: "W MB (delta)"
}
PERFORMANCE_IMPACT: {
  verdict: "improved|neutral|degraded",
  acceptable: true/false,
  reasoning: "..."
}
LOAD_TEST_RESULTS: {
  max_throughput: "...",
  breaking_point: "...",
  memory_leaks: "none|detected"
}
APM_INSIGHTS: [slow queries, N+1 patterns, bottlenecks]
PRODUCTION_READY: {yes/no + blockers if no}
```

**第三步：代码审查员最终审批**

**提示词：**
```
Perform final code review and approve for deployment:

Context from Testing:
- Test results: {TEST_RESULTS}
- Regression detected: {REGRESSION_DETECTED}
- Performance impact: {PERFORMANCE_IMPACT}
- Security scan: {SECURITY_SCAN}

Deliverables:
1. Code quality review:
   - Follows project conventions
   - No code smells or anti-patterns
   - Proper error handling
   - Adequate logging and observability
2. Architecture review:
   - Maintains system boundaries
   - No tight coupling introduced
   - Scalability considerations
3. Security review:
   - No security vulnerabilities
   - Proper input validation
   - Authentication/authorization correct
4. Documentation review:
   - Code comments where needed
   - API documentation updated
   - Runbook updated if operational impact
5. Deployment readiness:
   - Rollback plan documented
   - Feature flag strategy defined
   - Monitoring/alerting configured
6. Risk assessment:
   - Blast radius estimation
   - Rollout strategy recommendation
   - Success metrics defined

Review checklist:
- All tests pass
- No performance regressions
- Security vulnerabilities addressed
- Breaking changes documented
- Backward compatibility maintained
- Observability adequate
- Deployment plan clear
```

**预期输出：**
```
REVIEW_STATUS: {APPROVED|NEEDS_REVISION|BLOCKED}
CODE_QUALITY: {score/assessment}
ARCHITECTURE_CONCERNS: [list or "none"]
SECURITY_CONCERNS: [list or "none"]
DEPLOYMENT_RISK: {low|medium|high}
ROLLBACK_PLAN: {
  steps: ["..."],
  estimated_time: "X minutes",
  data_recovery: "..."
}
ROLLOUT_STRATEGY: {
  approach: "canary|blue-green|rolling|big-bang",
  phases: ["..."],
  success_metrics: ["..."],
  abort_criteria: ["..."]
}
MONITORING_REQUIREMENTS: [
  {metric: "...", threshold: "...", action: "..."}
]
FINAL_VERDICT: {
  approved: true/false,
  blockers: [list if not approved],
  recommendations: ["..."]
}
```

## 阶段5：文档与预防 — 长期韧性

使用 Task 工具，调用 subagent_type="comprehensive-review::code-reviewer" 制定预防策略：

**提示词：**
```
Document fix and implement prevention strategies to avoid recurrence:

Context from Phase 4:
- Final verdict: {FINAL_VERDICT}
- Review status: {REVIEW_STATUS}
- Root cause: {ROOT_CAUSE}
- Rollback plan: {ROLLBACK_PLAN}
- Monitoring requirements: {MONITORING_REQUIREMENTS}

Deliverables:
1. Code documentation:
   - Inline comments for non-obvious logic (minimal)
   - Function/class documentation updates
   - API contract documentation
2. Operational documentation:
   - CHANGELOG entry with fix description and version
   - Release notes for stakeholders
   - Runbook entry for on-call engineers
   - Postmortem document (if high-severity incident)
3. Prevention through static analysis:
   - Add linting rules (eslint, ruff, golangci-lint)
   - Configure stricter compiler/type checker settings
   - Add custom lint rules for domain-specific patterns
   - Update pre-commit hooks
4. Type system enhancements:
   - Add exhaustiveness checking
   - Use discriminated unions/sum types
   - Add const/readonly modifiers
   - Leverage branded types for validation
5. Monitoring and alerting:
   - Create error rate alerts (Sentry, DataDog)
   - Add custom metrics for business logic
   - Set up synthetic monitors (Pingdom, Checkly)
   - Configure SLO/SLI dashboards
6. Architectural improvements:
   - Identify similar vulnerability patterns
   - Propose refactoring for better isolation
   - Document design decisions
   - Update architecture diagrams if needed
7. Testing improvements:
   - Add property-based tests
   - Expand integration test scenarios
   - Add chaos engineering tests
   - Document testing strategy gaps

Modern prevention practices (2024/2025):
- AI-assisted code review rules (GitHub Copilot, Claude Code)
- Continuous security scanning (Snyk, Dependabot)
- Infrastructure as Code validation (Terraform validate, CloudFormation Linter)
- Contract testing for APIs (Pact, OpenAPI validation)
- Observability-driven development (instrument before deploying)
```

**预期输出：**
```
DOCUMENTATION_UPDATES: [
  {file: "CHANGELOG.md", summary: "..."},
  {file: "docs/runbook.md", summary: "..."},
  {file: "docs/architecture.md", summary: "..."}
]
PREVENTION_MEASURES: {
  static_analysis: [
    {tool: "eslint", rule: "...", reason: "..."},
    {tool: "ruff", rule: "...", reason: "..."}
  ],
  type_system: [
    {enhancement: "...", location: "...", benefit: "..."}
  ],
  pre_commit_hooks: [
    {hook: "...", purpose: "..."}
  ]
}
MONITORING_ADDED: {
  alerts: [
    {name: "...", threshold: "...", channel: "..."}
  ],
  dashboards: [
    {name: "...", metrics: [...], url: "..."}
  ],
  slos: [
    {service: "...", sli: "...", target: "...", window: "..."}
  ]
}
ARCHITECTURAL_IMPROVEMENTS: [
  {improvement: "...", reasoning: "...", effort: "small|medium|large"}
]
SIMILAR_VULNERABILITIES: {
  found: N,
  locations: [...],
  remediation_plan: "..."
}
FOLLOW_UP_TASKS: [
  {task: "...", priority: "high|medium|low", owner: "..."}
]
POSTMORTEM: {
  created: true/false,
  location: "...",
  incident_severity: "SEV1|SEV2|SEV3|SEV4"
}
KNOWLEDGE_BASE_UPDATES: [
  {article: "...", summary: "..."}
]
```

## 跨领域协调处理复杂问题

对于跨多个领域的问题，按顺序编排专业智能体并显式传递上下文：

**示例1：数据库性能问题导致应用超时**

**执行序列：**
1. **阶段1-2**：error-detective + debugger 识别慢查询
2. **阶段3a**：Task(subagent_type="database-cloud-optimization::database-optimizer")
   - 通过合适的索引优化查询
   - 上下文："查询执行耗时5秒，user_id列缺少索引，检测到N+1查询模式"
3. **阶段3b**：Task(subagent_type="application-performance::performance-engineer")
   - 为频繁访问的数据添加缓存层
   - 上下文："通过在user_id列添加索引，数据库查询从5秒优化到50毫秒。但由于N+1查询模式每次请求加载100+条用户记录，应用响应时间仍有2秒。为用户资料添加Redis缓存，TTL为5分钟。"
4. **阶段3c**：Task(subagent_type="incident-response::devops-troubleshooter")
   - 配置查询性能和缓存命中率的监控
   - 上下文："已添加Redis缓存层。需要监控：查询p95延迟（阈值：100ms）、缓存命中率（阈值：>80%）、缓存内存使用（80%时告警）。"

**示例2：生产环境前端JavaScript错误**

**执行序列：**
1. **阶段1**：error-detective 分析Sentry错误报告
   - 上下文："TypeError: Cannot read property 'map' of undefined，过去1小时500+次，影响iOS 14上的Safari用户"
2. **阶段2**：debugger + code-reviewer 调查
   - 上下文："API响应在无结果时有时返回null而非空数组。前端假设为数组。"
3. **阶段3a**：Task(subagent_type="javascript-typescript::typescript-pro")
   - 修复前端的null检查
   - 添加类型守卫
   - 上下文："后端API /api/users端点在无结果时返回null而非[]。修复前端以处理两种情况。添加TypeScript严格null检查。"
4. **阶段3b**：Task(subagent_type="backend-development::backend-architect")
   - 修复后端使其始终返回数组
   - 更新API契约
   - 上下文："前端现在可以处理null，但API应遵循契约返回[]而非null。更新OpenAPI规范以记录此行为。"
5. **阶段4**：test-automator 运行跨浏览器测试
6. **阶段5**：code-reviewer 记录API契约变更

**示例3：认证中的安全漏洞**

**执行序列：**
1. **阶段1**：error-detective 审查安全扫描报告
   - 上下文："登录端点存在SQL注入漏洞，Snyk严重级别：HIGH"
2. **阶段2**：debugger + security-auditor 调查
   - 上下文："SQL WHERE子句中用户输入未过滤，允许认证绕过"
3. **阶段3**：Task(subagent_type="security-scanning::security-auditor")
   - 实现参数化查询
   - 添加输入验证
   - 添加速率限制
   - 上下文："将字符串拼接替换为预编译语句。添加邮箱格式输入验证。实现速率限制（15分钟内5次尝试）。"
4. **阶段4a**：test-automator 添加安全测试
   - SQL注入尝试
   - 暴力破解场景
5. **阶段4b**：security-auditor 执行渗透测试
6. **阶段5**：code-reviewer 记录安全改进并创建事后总结

**上下文传递模板：**
```
Context for {next_agent}:

Completed by {previous_agent}:
- {summary_of_work}
- {key_findings}
- {changes_made}

Remaining work:
- {specific_tasks_for_next_agent}
- {files_to_modify}
- {constraints_to_follow}

Dependencies:
- {systems_or_components_affected}
- {data_needed}
- {integration_points}

Success criteria:
- {measurable_outcomes}
- {verification_steps}
```

## 配置选项

通过在调用时设置优先级来自定义工作流行为：

**VERIFICATION_LEVEL**：控制测试和验证的深度
- **minimal**：快速修复加基础测试，跳过性能基准
  - 适用场景：低风险bug、界面问题、文档修复
  - 涉及阶段：1-2-3（跳过详细的阶段4）
  - 预计时间：约30分钟
- **standard**：完整测试覆盖 + 代码审查（默认）
  - 适用场景：大多数生产bug、功能问题、数据问题
  - 涉及阶段：1-2-3-4（全部验证）
  - 预计时间：约2-4小时
- **comprehensive**：标准 + 安全审计 + 性能基准 + 混沌测试
  - 适用场景：安全问题、性能问题、数据损坏、高流量系统
  - 涉及阶段：1-2-3-4-5（包含长期预防）
  - 预计时间：约1-2天

**PREVENTION_FOCUS**：控制对未来预防的投入程度
- **none**：仅修复，不做预防工作
  - 适用场景：一次性问题、即将废弃的遗留代码、外部库bug
  - 输出：仅代码修复 + 测试
- **immediate**：添加测试和基础lint规则（默认）
  - 适用场景：常见bug、反复出现的模式、团队代码库
  - 输出：修复 + 测试 + lint规则 + 最小监控
- **comprehensive**：完整预防套件，包含监控和架构改进
  - 适用场景：高严重性事件、系统性问题、架构问题
  - 输出：修复 + 测试 + lint + 监控 + 架构文档 + 事后总结

**ROLLOUT_STRATEGY**：控制部署方式
- **immediate**：直接部署到生产环境（用于热修复、低风险变更）
- **canary**：逐步向部分流量推出（中等风险的默认方式）
- **blue-green**：完整环境切换，支持即时回滚
- **feature-flag**：部署代码但通过功能开关控制激活（高风险变更）

**OBSERVABILITY_LEVEL**：控制可观测性埋点深度
- **minimal**：仅基础错误日志
- **standard**：结构化日志 + 关键指标（默认）
- **comprehensive**：完整分布式追踪 + 自定义仪表盘 + SLO

**调用示例：**
```
Issue: Users experiencing timeout errors on checkout page (500+ errors/hour)

Config:
- VERIFICATION_LEVEL: comprehensive (affects revenue)
- PREVENTION_FOCUS: comprehensive (high business impact)
- ROLLOUT_STRATEGY: canary (test on 5% traffic first)
- OBSERVABILITY_LEVEL: comprehensive (need detailed monitoring)
```

## 现代调试工具集成

本工作流利用2024/2025年的现代工具：

**可观测性平台：**
- Sentry（错误追踪、发布追踪、性能监控）
- DataDog（APM、日志、追踪、基础设施监控）
- OpenTelemetry（厂商中立的分布式追踪）
- Honeycomb（复杂分布式系统的可观测性）
- New Relic（APM、合成监控）

**AI辅助调试：**
- GitHub Copilot（代码建议、测试生成、bug模式识别）
- Claude Code（全面代码分析、架构审查）
- Sourcegraph Cody（代码库搜索和理解）
- Tabnine（代码补全与bug预防）

**Git与版本控制：**
- 自动化git bisect配合复现脚本
- GitHub Actions在bisect提交上自动测试
- Git blame分析识别代码归属
- 提交消息分析理解变更意图

**测试框架：**
- Jest/Vitest（JavaScript/TypeScript单元/集成测试）
- pytest（Python测试，支持fixtures和参数化）
- Go testing + testify（Go单元测试和表驱动测试）
- Playwright/Cypress（端到端浏览器测试）
- k6/Locust（负载和性能测试）

**静态分析：**
- ESLint/Prettier（JavaScript/TypeScript lint和格式化）
- Ruff/mypy（Python lint和类型检查）
- golangci-lint（Go综合lint）
- Clippy（Rust lint和最佳实践）
- SonarQube（企业级代码质量和安全）

**性能分析：**
- Chrome DevTools（前端性能）
- pprof（Go性能分析）
- py-spy（Python性能分析）
- Pyroscope（持续性能分析）
- 火焰图用于CPU/内存分析

**安全扫描：**
- Snyk（依赖漏洞扫描）
- Dependabot（自动依赖更新）
- OWASP ZAP（安全测试）
- Semgrep（自定义安全规则）
- npm audit / pip-audit / cargo audit

## 成功标准

修复被认为完成需要满足以下所有条件：

**根因理解：**
- 根因已识别并有证据支撑
- 故障机制已清晰记录
- 引入提交已识别（如适用，通过git bisect）
- 相似漏洞已编目

**修复质量：**
- 修复针对根因而非症状
- 代码变更最小化（避免过度工程）
- 遵循项目约定和模式
- 未引入代码异味或反模式
- 向后兼容性已保持（或破坏性变更已记录）

**测试验证：**
- 所有现有测试通过（零回归）
- 新测试覆盖了具体的bug复现
- 边界情况和错误路径已测试
- 集成测试验证端到端行为
- 测试覆盖率提升（或维持在高位）

**性能与安全：**
- 无性能退化（p95延迟在基线的5%以内）
- 未引入安全漏洞
- 资源使用可接受（内存、CPU、I/O）
- 高流量变更通过负载测试

**部署就绪：**
- 代码审查已由领域专家批准
- 回滚计划已记录并测试
- 功能开关已配置（如适用）
- 监控和告警已配置
- 运维手册已更新排障步骤

**预防措施：**
- 静态分析规则已添加（如适用）
- 类型系统改进已实施（如适用）
- 文档已更新（代码、API、运维手册）
- 事后总结已创建（高严重性事件）
- 知识库文章已创建（新型问题）

**指标：**
- 平均恢复时间（MTTR）：SEV2+ < 4小时
- Bug复发率：0%（同一根因不应再次发生）
- 测试覆盖率：不下降，理想情况上升
- 部署成功率：> 95%（回滚率 < 5%）

待解决问题：$ARGUMENTS
