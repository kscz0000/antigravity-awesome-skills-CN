---
name: e2e-testing
description: "Playwright E2E 测试模式，涵盖页面对象模型、配置、CI/CD 集成、测试产物管理与不稳定测试处理策略。触发词：E2E测试、端到端测试、Playwright测试、页面对象模型、POM、CI/CD集成、不稳定测试、测试产物、自动化测试、浏览器测试、flaky test、e2e testing、Playwright e2e。"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# E2E 测试工作流

## 概述

使用 Playwright 进行端到端测试的专用工作流，包括浏览器自动化、视觉回归测试、跨浏览器测试和 CI/CD 集成。

## 何时使用此工作流

在以下情况下使用此工作流：
- 设置 E2E 测试
- 自动化浏览器测试
- 实现视觉回归
- 跨浏览器测试
- 将测试集成到 CI/CD

## 工作流阶段

### 阶段 1：测试设置

#### 要调用的技能
- `playwright-skill` - Playwright 设置
- `e2e-testing-patterns` - E2E 模式

#### 操作
1. 安装 Playwright
2. 配置测试框架
3. 设置测试目录
4. 配置浏览器
5. 创建基础测试设置

#### 复制粘贴提示词
```
Use @playwright-skill to set up Playwright testing
```

### 阶段 2：测试设计

#### 要调用的技能
- `e2e-testing-patterns` - 测试模式
- `test-automator` - 测试自动化

#### 操作
1. 识别关键流程
2. 设计测试场景
3. 规划测试数据
4. 创建页面对象
5. 设置 fixtures

#### 复制粘贴提示词
```
Use @e2e-testing-patterns to design E2E test strategy
```

### 阶段 3：测试实现

#### 要调用的技能
- `playwright-skill` - Playwright 测试
- `webapp-testing` - Web 应用测试

#### 操作
1. 编写测试脚本
2. 添加断言
3. 实现等待机制
4. 处理动态内容
5. 添加错误处理

#### 复制粘贴提示词
```
Use @playwright-skill to write E2E test scripts
```

### 阶段 4：浏览器自动化

#### 要调用的技能
- `browser-automation` - 浏览器自动化
- `playwright-skill` - Playwright 功能

#### 操作
1. 配置无头模式
2. 设置截图
3. 实现视频录制
4. 添加 trace 收集
5. 配置移动端模拟

#### 复制粘贴提示词
```
Use @browser-automation to automate browser interactions
```

### 阶段 5：视觉回归

#### 要调用的技能
- `playwright-skill` - 视觉测试
- `ui-visual-validator` - 视觉验证

#### 操作
1. 设置视觉测试
2. 创建基准图像
3. 添加视觉断言
4. 配置阈值
5. 审查差异

#### 复制粘贴提示词
```
Use @playwright-skill to implement visual regression testing
```

### 阶段 6：跨浏览器测试

#### 要调用的技能
- `playwright-skill` - 多浏览器
- `webapp-testing` - 浏览器测试

#### 操作
1. 配置 Chromium
2. 添加 Firefox 测试
3. 添加 WebKit 测试
4. 测试移动端浏览器
5. 比较结果

#### 复制粘贴提示词
```
Use @playwright-skill to run cross-browser tests
```

### 阶段 7：CI/CD 集成

#### 要调用的技能
- `github-actions-templates` - GitHub Actions
- `cicd-automation-workflow-automate` - CI/CD

#### 操作
1. 创建 CI 工作流
2. 配置并行执行
3. 设置产物
4. 添加报告
5. 配置通知

#### 复制粘贴提示词
```
Use @github-actions-templates to integrate E2E tests with CI
```

## 质量门控

- [ ] 测试通过
- [ ] 覆盖率充足
- [ ] 视觉测试稳定
- [ ] 跨浏览器验证完成
- [ ] CI 集成正常工作

## 相关工作流包

- `testing-qa` - 测试工作流
- `development` - 开发
- `web-performance-optimization` - 性能

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
