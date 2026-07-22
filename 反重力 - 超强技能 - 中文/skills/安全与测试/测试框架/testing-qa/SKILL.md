---
name: testing-qa
description: "全面的测试和质量保证工作流，涵盖单元测试、集成测试、E2E测试、浏览器自动化和质量保证。当用户需要设置测试基础设施、编写单元测试、实施E2E测试、自动化浏览器测试、建立质量门控或进行代码审查时使用。"
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# 测试/QA 工作流包

## 概述

全面的测试和质量保证工作流，涵盖单元测试、集成测试、E2E测试、浏览器自动化以及面向生产就绪软件的质量门控。

## 何时使用此工作流

在以下情况下使用此工作流：
- 设置测试基础设施
- 编写单元测试和集成测试
- 实施 E2E 测试
- 自动化浏览器测试
- 建立质量门控
- 执行代码审查

## 工作流阶段

### 阶段 1：测试策略

#### 要调用的技能
- `test-automator` - 测试自动化
- `test-driven-development` - TDD

#### 操作
1. 定义测试策略
2. 选择测试框架
3. 规划测试覆盖率
4. 设置测试基础设施
5. 配置 CI 集成

#### 复制粘贴提示词
```
Use @test-automator to design testing strategy
```

```
Use @test-driven-development to implement TDD workflow
```

### 阶段 2：单元测试

#### 要调用的技能
- `javascript-testing-patterns` - Jest/Vitest
- `python-testing-patterns` - pytest
- `unit-testing-test-generate` - 测试生成
- `tdd-orchestrator` - TDD 编排

#### 操作
1. 编写单元测试
2. 设置测试固件
3. 配置模拟
4. 测量覆盖率
5. 集成到 CI

#### 复制粘贴提示词
```
Use @javascript-testing-patterns to write Jest tests
```

```
Use @python-testing-patterns to write pytest tests
```

```
Use @unit-testing-test-generate to generate unit tests
```

### 阶段 3：集成测试

#### 要调用的技能
- `api-testing-observability-api-mock` - API 测试
- `e2e-testing-patterns` - 集成模式

#### 操作
1. 设计集成测试
2. 设置测试数据库
3. 配置 API 模拟
4. 测试服务交互
5. 验证数据流

#### 复制粘贴提示词
```
Use @api-testing-observability-api-mock to test APIs
```

### 阶段 4：E2E 测试

#### 要调用的技能
- `playwright-skill` - Playwright 测试
- `e2e-testing-patterns` - E2E 模式
- `webapp-testing` - Web 应用测试

#### 操作
1. 设计 E2E 场景
2. 编写测试脚本
3. 配置测试数据
4. 设置并行执行
5. 实施视觉回归

#### 复制粘贴提示词
```
Use @playwright-skill to create E2E tests
```

```
Use @e2e-testing-patterns to design E2E strategy
```

### 阶段 5：浏览器自动化

#### 要调用的技能
- `browser-automation` - 浏览器自动化
- `webapp-testing` - 浏览器测试
- `screenshots` - 截图自动化

#### 操作
1. 设置浏览器自动化
2. 配置无头测试
3. 实施视觉测试
4. 捕获截图
5. 测试响应式设计

#### 复制粘贴提示词
```
Use @browser-automation to automate browser tasks
```

```
Use @screenshots to capture marketing screenshots
```

### 阶段 6：性能测试

#### 要调用的技能
- `performance-engineer` - 性能工程
- `performance-profiling` - 性能分析
- `web-performance-optimization` - Web 性能

#### 操作
1. 设计性能测试
2. 设置负载测试
3. 测量响应时间
4. 识别瓶颈
5. 优化性能

#### 复制粘贴提示词
```
Use @performance-engineer to test application performance
```

### 阶段 7：代码审查

#### 要调用的技能
- `code-reviewer` - AI 代码审查
- `code-review-excellence` - 审查最佳实践
- `find-bugs` - Bug 检测
- `security-scanning-security-sast` - 安全扫描

#### 操作
1. 配置审查工具
2. 运行自动化审查
3. 检查 Bug
4. 验证安全性
5. 批准变更

#### 复制粘贴提示词
```
Use @code-reviewer to review pull requests
```

```
Use @find-bugs to detect bugs in code
```

### 阶段 8：质量门控

#### 要调用的技能
- `lint-and-validate` - Linting
- `verification-before-completion` - 验证

#### 操作
1. 配置 linter
2. 设置格式化工具
3. 定义质量指标
4. 实施门控
5. 监控合规性

#### 复制粘贴提示词
```
Use @lint-and-validate to check code quality
```

```
Use @verification-before-completion to verify changes
```

## 测试金字塔

```
        /       /  \    E2E 测试 (10%)
      /----     /      \  集成测试 (20%)
    /--------   /          \ 单元测试 (70%)
  /------------```

## 质量门控检查清单

- [ ] 单元测试覆盖率 > 80%
- [ ] 所有测试通过
- [ ] 关键路径有 E2E 测试
- [ ] 性能基准达标
- [ ] 安全扫描通过
- [ ] 代码审查批准
- [ ] Linting 干净

## 相关工作流包

- `development` - 开发工作流
- `security-audit` - 安全测试
- `cloud-devops` - CI/CD 集成
- `ai-ml` - AI 测试

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
