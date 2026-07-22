---
name: lambdatest-agent-skills
description: "面向 46 个框架的生产级测试自动化技能，覆盖 E2E、单元、移动端、BDD、视觉和云测试，支持 15+ 种编程语言。当用户要求编写测试自动化代码、搭建测试项目或使用 LambdaTest 云平台运行测试时使用。"
category: testing
risk: safe
source: community
source_repo: LambdaTest/agent-skills
source_type: community
date_added: "2026-04-16"
author: tanveer-farooq
tags: [testing, test-automation, e2e, unit-testing, mobile-testing, bdd, selenium, playwright, cypress, jest, pytest, appium, lambdatest]
tools: [claude, cursor, gemini, copilot]
license: "MIT"
license_source: "https://github.com/LambdaTest/agent-skills/blob/main/LICENSE"
---

# LambdaTest Agent Skills — 测试自动化注册表（46 个技能）

## 概述

本技能是一个精选索引，收录了来自 [LambdaTest/agent-skills](https://github.com/LambdaTest/agent-skills) 仓库的 46 个生产级测试自动化技能。它教会 AI 编码助手如何在每个主流框架和 15+ 编程语言中编写、组织和执行测试自动化代码。AI 不再生成泛泛的测试代码，而是成为一位资深 QA 自动化架构师——理解正确的项目结构、依赖版本、云端执行方式、CI/CD 集成，以及每个框架的常见调试模式。

本技能改编自外部 GitHub 仓库内容：
- `source_repo: LambdaTest/agent-skills`
- `source_type: community`

## 使用场景

- 需要为任何主流框架编写、搭建或审查测试自动化代码时使用
- 使用 Selenium、Playwright、Cypress、Jest、pytest、Appium 或其他 46 个支持的框架时使用
- 搭建新测试项目，需要正确的项目结构、配置文件和依赖时使用
- 将测试集成到 CI/CD 流水线（GitHub Actions、Jenkins、GitLab CI）时使用
- 在框架间迁移测试（如 Selenium → Playwright、Puppeteer → Cypress）时使用
- 在 LambdaTest / TestMu AI 等云基础设施上运行测试时使用
- 用户询问如何编写、调试或扩展自动化测试时使用

## 工作原理

### 第一步：确定框架和语言

判断用户使用的测试框架和编程语言，匹配下方 46 个支持技能中的一个。每个技能针对特定框架，提供对应语言的代码模式。

### 第二步：加载对应的技能上下文

从下方的注册表中加载相关框架技能。每个技能包含：项目搭建与依赖、核心代码模式、Page Object 或测试工具类、云端执行配置、CI/CD 集成、常见问题排查表、最佳实践清单。

### 第三步：生成生产级测试代码

利用已加载的技能上下文生成符合真实规范的测试代码——而非通用模板。正确应用各框架和语言对应的 import 路径、配置格式、断言库和运行命令。

### 第四步：配置本地或云端执行

若用户需要在本地运行，应用本地运行器配置。若在 LambdaTest / TestMu AI 云端运行，则配置 RemoteWebDriver capabilities 或对应的云 SDK，从环境变量读取 `LT_USERNAME` 和 `LT_ACCESS_KEY`——**绝不要将凭证硬编码**。

### 第五步：添加 CI/CD 集成

按需生成 GitHub Actions（或 Jenkins / GitLab CI）工作流，实现并行执行测试、上传报告、失败时捕获产物。

## 技能注册表

### 🌐 E2E / 浏览器测试（15 个技能）

| 技能 | 语言 | 说明 |
|---|---|---|
| `selenium-skill` | Java, Python, JS, C#, Ruby | Selenium WebDriver，支持跨浏览器和云端 |
| `playwright-skill` | JS, TS, Python, Java, C# | Playwright 浏览器自动化，含 API mock |
| `cypress-skill` | JS, TS | Cypress E2E 和组件测试 |
| `webdriverio-skill` | JS, TS | WebdriverIO，含 Page Object 和云端集成 |
| `puppeteer-skill` | JS, TS | Puppeteer Chrome 自动化 |
| `testcafe-skill` | JS, TS | TestCafe 跨浏览器测试 |
| `nightwatchjs-skill` | JS, TS | Nightwatch.js 浏览器自动化 |
| `capybara-skill` | Ruby | Capybara 验收测试 |
| `geb-skill` | Groovy | Geb Groovy 浏览器自动化 |
| `selenide-skill` | Java | Selenide 流式 Selenium 封装 |
| `nemojs-skill` | JS | Nemo.js PayPal 浏览器自动化 |
| `protractor-skill` | JS, TS | Protractor Angular E2E 测试 |
| `codeception-skill` | PHP | Codeception 全栈 PHP 测试 |
| `laravel-dusk-skill` | PHP | Laravel Dusk 浏览器测试 |
| `robot-framework-skill` | Python, Robot | Robot Framework 关键字驱动测试 |

### 🧪 单元测试（15 个技能）

| 技能 | 语言 | 说明 |
|---|---|---|
| `jest-skill` | JS, TS | Jest 单元和集成测试，含 mock |
| `junit-5-skill` | Java | JUnit 5，含参数化测试和扩展 |
| `pytest-skill` | Python | pytest，含 fixture、parametrize 和插件 |
| `testng-skill` | Java | TestNG，含 data provider 和并行执行 |
| `vitest-skill` | JS, TS | Vitest，专为 Vite 项目设计 |
| `mocha-skill` | JS, TS | Mocha 配合 Chai 断言 |
| `jasmine-skill` | JS, TS | Jasmine BDD 风格单元测试 |
| `karma-skill` | JS, TS | Karma 测试运行器 |
| `xunit-skill` | C# | xUnit.net for .NET |
| `nunit-skill` | C# | NUnit for .NET |
| `mstest-skill` | C# | MSTest for .NET |
| `rspec-skill` | Ruby | RSpec，含 shared examples |
| `phpunit-skill` | PHP | PHPUnit，含 data provider |
| `testunit-skill` | Ruby | Test::Unit Ruby 测试 |
| `unittest-skill` | Python | Python unittest，含 mock |

### 📱 移动端测试（5 个技能）

| 技能 | 语言 | 说明 |
|---|---|---|
| `appium-skill` | Java, Python, JS, Ruby, C# | Appium iOS 和 Android 移动端测试 |
| `espresso-skill` | Java, Kotlin | Espresso Android UI 测试 |
| `xcuitest-skill` | Swift, Obj-C | XCUITest iOS UI 测试 |
| `flutter-testing-skill` | Dart | Flutter widget 和集成测试 |
| `detox-skill` | JS, TS | Detox React Native E2E 测试 |

### 📋 BDD 测试（7 个技能）

| 技能 | 语言 | 说明 |
|---|---|---|
| `cucumber-skill` | Java, JS, Ruby, TS | Cucumber Gherkin BDD |
| `specflow-skill` | C# | SpecFlow .NET BDD（Gherkin） |
| `serenity-bdd-skill` | Java | Serenity BDD（Screenplay 模式） |
| `behave-skill` | Python | Behave Python BDD |
| `behat-skill` | PHP | Behat PHP BDD |
| `gauge-skill` | Java, Python, JS, Ruby, C# | Gauge 规约驱动测试 |
| `lettuce-skill` | Python | Lettuce Python BDD 测试 |

### 👁️ 视觉回归测试（1 个技能）

| 技能 | 语言 | 说明 |
|---|---|---|
| `smartui-skill` | JS, TS, Java | SmartUI 视觉回归测试 |

### ☁️ 云端测试（1 个技能）

| 技能 | 语言 | 说明 |
|---|---|---|
| `hyperexecute-skill` | YAML | HyperExecute 云端测试编排 |

### 🔄 框架迁移（1 个技能）

| 技能 | 语言 | 说明 |
|---|---|---|
| `test-framework-migration-skill` | JS, TS, Java, Python, C# | 在 Selenium、Playwright、Puppeteer、Cypress 之间转换测试 |

### 🔄 DevOps / CI/CD（1 个技能）

| 技能 | 语言 | 说明 |
|---|---|---|
| `cicd-pipeline-skill` | YAML | GitHub Actions、Jenkins、GitLab CI 的 CI/CD 流水线集成 |

## 示例

### 示例 1：用 TypeScript 搭建 Playwright 测试

```
"用 TypeScript 为登录页编写 Playwright 测试，并在 Chrome 和 Firefox 上运行"
```

技能会生成：正确的 `playwright.config.ts`、登录页的 typed Page Object、使用 `@playwright/test` 的测试文件，以及带并行执行的 GitHub Actions 工作流。

### 示例 2：在 LambdaTest 云端运行 Selenium 测试

```
"把我的 Selenium Java 测试跑在 LambdaTest 上，浏览器选 Chrome、Firefox 和 Safari，系统用 Windows 11 和 macOS Sonoma"
```

技能会配置带 LambdaTest capabilities 的 `RemoteWebDriver`，从环境变量读取 `LT_USERNAME` 和 `LT_ACCESS_KEY`，并搭建并行 TestNG 套件。

### 示例 3：将 Selenium 测试迁移到 Playwright

```
"把我现有的 Selenium Python 测试迁移到 Playwright"
```

技能调用 `test-framework-migration-skill`，将 Selenium 的定位符、等待和断言映射为 Playwright 等价写法，保留测试意图的同时更新语法。

### 示例 4：搭建带 fixture 的 pytest 测试套件

```
"为支付 API 创建一个 pytest 测试套件，要求包含 fixtures 和参数化测试用例"
```

技能会生成含共享 fixtures 的 `conftest.py`、使用 `@pytest.mark.parametrize` 的参数化测试用例，以及带覆盖率报告的 `pytest.ini` 配置。

## 最佳实践

- ✅ 云端凭证（`LT_USERNAME`、`LT_ACCESS_KEY`）始终使用环境变量——**绝不硬编码**
- ✅ 采用 Page Object Model（POM），将测试逻辑与 UI 选择器分离
- ✅ 所有框架中优先使用显式等待，避免固定 `sleep()` 调用
- ✅ 框架支持时尽量并行执行测试，缩短总耗时
- ✅ 测试失败时务必截图和记录日志，方便排查
- ✅ 依赖版本严格对齐各框架官方推荐值——避免混用大版本号
- ❌ 不要编写依赖测试执行顺序的测试
- ❌ 不要在测试文件中硬编码 URL、凭证或环境相关的值
- ❌ 不要跳过断言——没有断言的测试不算测试
- ❌ 不要放过 flaky 测试——应定位根因并修复，而非靠重试掩盖问题

## 局限性

- 本技能是索引和触发指南。各框架的完整实现细节存放在 [LambdaTest/agent-skills](https://github.com/LambdaTest/agent-skills) 的独立技能文件中。
- 本技能不能替代框架官方文档、环境搭建指南或专业 QA 审查。
- 云端执行示例假设你拥有有效的 LambdaTest / TestMu AI 账户。若凭证或目标环境不明确，请停下来询问用户的配置详情。
- 移动端测试技能（Appium、Espresso、XCUITest、Flutter、Detox）需要平台专属工具链（Android SDK、Xcode），需单独安装。

## 安全注意事项

- 生成的代码中**绝不允许**出现 `LT_USERNAME`、`LT_ACCESS_KEY`、API token 或任何凭证。必须通过环境变量引用。
- 生成 CI/CD 流水线时，机密信息存入 GitHub Actions Secrets 或等效机制——**禁止明文写入 YAML**。
- 安装命令（`npm install`、`pip install`、`mvn install`）仅应在本地开发环境或已授权的 CI 环境中执行。

## 常见陷阱

- **问题：** 本地通过但 CI 失败
  **解决：** 确保 CI 中启用了无头模式（headless），且本地与 CI 环境的浏览器版本一致。优先使用框架内置的 CI 检测能力。

- **问题：** 时序问题导致 flaky 测试
  **解决：** 用显式等待替换 `sleep()`——Playwright 用 `waitForSelector`，Selenium 用 `WebDriverWait`，Cypress 用 `cy.get().should()`。

- **问题：** 云端测试报认证错误
  **解决：** 核实 `LT_USERNAME` 和 `LT_ACCESS_KEY` 已作为环境变量正确设置，且与 LambdaTest 控制台上的凭证一致。

- **问题：** 云端执行的浏览器 capabilities 配置有误
  **解决：** 使用 LambdaTest Capabilities Generator（https://www.lambdatest.com/capabilities-generator/）获取目标浏览器和操作系统对应的正确 capability 对象。

- **问题：** 移动端测试报"device not found"
  **解决：** 本地运行时确认模拟器已启动，`adb devices`（Android）或 Simulator（iOS）处于活跃状态。云端运行时检查设备名称是否与 LambdaTest 支持的设备名完全匹配。

## 相关技能

- `@test-driven-development` — 需要先写测试再写实现代码时使用
- `@testing-patterns` — 通用测试设计模式和策略
- `@cicd-pipeline-skill` — 搭建端到端 CI/CD 流水线并集成测试自动化时使用
- `@debugging-strategies` — 诊断系统性测试失败时使用
