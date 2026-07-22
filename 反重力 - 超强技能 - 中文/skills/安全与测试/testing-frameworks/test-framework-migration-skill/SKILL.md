---
name: test-framework-migration-skill
description: 在 Selenium、Playwright、Puppeteer 和 Cypress 之间迁移并转换测试自动化脚本。当用户要求迁移、转换或将测试从一个框架移植到另一个框架时使用；在不同框架中重写测试时使用；或从 Selenium 切换到 Playwright、Playwright 切换到……时使用。触发词：迁移框架、转换框架、移植测试、迁移测试、Selenium 转 Playwright、Playwright 转 Selenium、Puppeteer 转 Playwright、Cypress 转 Playwright、test framework migration、测试框架迁移。
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# 测试框架迁移技能
## 使用场景

当你需要在 Selenium、Playwright、Puppeteer 和 Cypress 之间迁移和转换测试自动化脚本时使用此技能。当用户要求迁移、转换或将测试从一个框架移植到另一个框架时使用；在不同框架中重写测试时使用；或从 Selenium 切换到 Playwright、Playwright 切换到……时使用。

你是一名资深 QA 自动化架构师。你通过应用技能参考文档中的 API 映射、生命周期变更和模式转换，将测试自动化脚本从一个框架（Selenium、Playwright、Puppeteer、Cypress）迁移到另一个框架。

## 步骤 1 — 检测源框架

从用户消息或打开的文件中确定**源**框架：

| 消息或代码中的信号 | 源框架 |
|---------------------------|------------------|
| "Selenium"、"WebDriver"、"driver.findElement"、"By.id"、"ChromeDriver" | Selenium |
| "Playwright"、"page.getByRole"、"expect(locator).toBeVisible"、"@playwright/test" | Playwright |
| "Puppeteer"、"page.$"、"page.goto"、"puppeteer.launch" | Puppeteer |
| "Cypress"、"cy.get"、"cy.visit"、"cy.contains"、"cy.should" | Cypress |

如果存在歧义（例如用户说 "convert my tests" 但没有打开文件），请询问："你当前的测试使用的是哪个框架（Selenium、Playwright、Puppeteer 还是 Cypress）？"

## 步骤 2 — 检测目标框架

从用户消息中确定**目标**框架：

| 用户说…… | 目标 |
|--------------|--------|
| "to Playwright"、"to playwright" | Playwright |
| "to Selenium"、"to WebDriver" | Selenium |
| "to Puppeteer" | Puppeteer |
| "to Cypress" | Cypress |

如果用户只指定了源（例如 "convert my Selenium tests"），请询问："你想迁移到哪个框架（Playwright、Puppeteer、Cypress，或保留 Selenium 但换语言）？"

## 步骤 3 — 检测语言

| 源 → 目标 | 语言说明 |
|----------------|---------------|
| Selenium（Java/Python/C#）→ Playwright | Playwright 通常是 JS/TS；迁移通常意味着改写为 TypeScript 或 JavaScript。如果源是 Java/C#/Python，请明确说明这一点。 |
| Selenium（JS）→ Playwright | 可以使用相同语言（JS/TS）。 |
| Playwright/Puppeteer/Cypress → Selenium | 目标可以是 Java、Python、JS、C#。优先与项目一致，或询问用户。 |
| Playwright ↔ Puppeteer ↔ Cypress | 通常保持在 JS/TS。 |

有关语言矩阵详情（哪些框架支持哪些语言），请参阅 [reference/overview.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/overview.md)。

## 步骤 4 — 路由到参考

在生成迁移代码之前**务必先读取**匹配的参考文件：

| 源 → 目标 | 参考文件 |
|----------------|----------------|
| Selenium → Playwright | [reference/selenium-to-playwright.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/selenium-to-playwright.md) |
| Playwright → Selenium | [reference/playwright-to-selenium.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/playwright-to-selenium.md) |
| Selenium → Puppeteer | [reference/selenium-to-puppeteer.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/selenium-to-puppeteer.md) |
| Puppeteer → Selenium | [reference/puppeteer-to-selenium.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/puppeteer-to-selenium.md) |
| Puppeteer → Playwright | [reference/puppeteer-to-playwright.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/puppeteer-to-playwright.md) |
| Playwright → Puppeteer | [reference/playwright-to-puppeteer.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/playwright-to-puppeteer.md) |
| Cypress → Playwright | [reference/cypress-to-playwright.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/cypress-to-playwright.md) |
| Playwright → Cypress | [reference/playwright-to-cypress.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/playwright-to-cypress.md) |
| Selenium → Cypress | [reference/selenium-to-cypress.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/selenium-to-cypress.md) |
| Cypress → Selenium | [reference/cypress-to-selenium.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/cypress-to-selenium.md) |

如果该组合不在表中，请说明并建议最接近的支持的迁移（例如稍后可增加 WebDriverIO 作为新的参考文件）。

## 步骤 5 — 应用映射

使用参考文档：

1. **定位器** — 使用 API 映射表进行转换（例如 `By.id("x")` → `page.getByRole(...)` 或 `page.locator('#x')`）。
2. **等待** — 转换等待策略（显式等待 / 自动等待 / cy.should）。
3. **动作** — 映射 click、type、select 等。
4. **断言** — 映射为目标框架的断言风格。
5. **生命周期** — 调整 setup/teardown（driver vs page，launch vs connect）。
6. **云（TestMu）** — 如果用户在云上运行，迁移后指向目标框架的云文档。

生成迁移代码后，根据参考文档的 "Gotchas" 部分进行验证，以避免常见陷阱。

## 深度模式的交叉参考

| 需求 | 查看位置 |
|------|----------------|
| 完整的 Playwright 模式、POM、云 | `playwright-skill` 和 [playwright-skill/reference/cloud-integration.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/../playwright-skill/reference/cloud-integration.md) |
| 完整的 Selenium 模式、POM、云 | `selenium-skill` 和 [selenium-skill/reference/cloud-integration.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/../selenium-skill/reference/cloud-integration.md) |
| 完整的 Puppeteer 模式、云 | `puppeteer-skill` 和 [puppeteer-skill/reference/cloud-integration.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/../puppeteer-skill/reference/cloud-integration.md) |
| 完整的 Cypress 模式、云 | `cypress-skill` 和 [cypress-skill/reference/cloud-integration.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/../cypress-skill/reference/cloud-integration.md) |
| TestMu 能力（所有框架） | [shared/testmu-cloud-reference.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/../shared/testmu-cloud-reference.md) |

## 验证流程

生成迁移代码后：

1. 确保每个定位器/动作/断言都使用参考映射进行了转换（没有残留的源 API）。
2. 确保生命周期（setup/teardown）与目标框架匹配。
3. 如果目标是 Playwright：使用自动等待断言（`expect(locator).toBeVisible()`），不要使用原始的 `waitForTimeout`。
4. 如果目标是 Cypress：`cy` 命令不要使用 async/await；使用链式风格。
5. 如果目标是 Selenium：使用显式的 `WebDriverWait`，永远不要使用 `Thread.sleep`。

## 参考文件汇总

| 文件 | 何时读取 |
|------|--------------|
| [reference/overview.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/overview.md) | 框架对比、语言矩阵、何时迁移 |
| [reference/playbook.md](https://github.com/LambdaTest/agent-skills/tree/main/test-framework-migration-skill/reference/playbook.md) | 完整的迁移工作流、调试表、CI/CD 检查清单、最佳实践 |
| `reference/<source>-to-<target>.md` | 在转换该组合的任何脚本之前 |

## 局限性

- 仅当任务明确匹配其上游源和本地项目上下文时，才使用此技能。
- 在应用更改之前，请验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例视为环境特定测试、安全审查或用户对破坏性或高成本操作的批准的替代品。
