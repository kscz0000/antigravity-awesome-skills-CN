---
name: cucumber-skill
description: '生成 Cucumber BDD 测试，包含 Gherkin feature 文件以及 Java、JavaScript 或 Ruby 语言的步骤定义。涉及 Cucumber、Gherkin、Feature/Scenario、Given/When/Then、BDD 等关键词时触发。触发词：Cucumber、Gherkin、BDD、Feature 文件、Given/When/Then、step...'
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/cucumber-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# Cucumber BDD 技能
## 适用场景

需要生成 Cucumber BDD 测试，使用 Gherkin feature 文件并以 Java、JavaScript 或 Ruby 编写步骤定义时调用此技能。涉及 Cucumber、Gherkin、Feature/Scenario、Given/When/Then、BDD 等关键词时触发。触发词：Cucumber、Gherkin、BDD、Feature 文件、Given/When/Then、step...


## 核心模式

### Feature 文件（Gherkin）

```gherkin
Feature: User Login
  As a registered user
  I want to log into the application
  So that I can access my dashboard

  Background:
    Given I am on the login page

  Scenario: Successful login
    When I enter "user@test.com" in the email field
    And I enter "password123" in the password field
    And I click the login button
    Then I should be redirected to the dashboard
    And I should see "Welcome" on the page

  Scenario: Invalid credentials
    When I enter "wrong@test.com" in the email field
    And I enter "wrongpass" in the password field
    And I click the login button
    Then I should see an error message "Invalid credentials"

  Scenario Outline: Login with various users
    When I enter "<email>" in the email field
    And I enter "<password>" in the password field
    And I click the login button
    Then I should see "<result>"

    Examples:
      | email           | password    | result     |
      | admin@test.com  | admin123    | Dashboard  |
      | user@test.com   | password    | Dashboard  |
      | bad@test.com    | wrong       | Error      |
```

### 步骤定义 —— Java

```java
import io.cucumber.java.en.*;
import static org.junit.jupiter.api.Assertions.*;

public class LoginSteps {
    private LoginPage loginPage;
    private DashboardPage dashboardPage;

    @Given("I am on the login page")
    public void iAmOnTheLoginPage() {
        loginPage = new LoginPage(driver);
        loginPage.navigate();
    }

    @When("I enter {string} in the email field")
    public void iEnterEmail(String email) {
        loginPage.enterEmail(email);
    }

    @When("I enter {string} in the password field")
    public void iEnterPassword(String password) {
        loginPage.enterPassword(password);
    }

    @When("I click the login button")
    public void iClickLogin() {
        dashboardPage = loginPage.clickLogin();
    }

    @Then("I should be redirected to the dashboard")
    public void iShouldBeOnDashboard() {
        assertTrue(driver.getCurrentUrl().contains("/dashboard"));
    }

    @Then("I should see {string} on the page")
    public void iShouldSeeText(String text) {
        assertTrue(dashboardPage.getPageSource().contains(text));
    }
}
```

### 步骤定义 —— JavaScript

```javascript
const { Given, When, Then } = require('@cucumber/cucumber');
const { expect } = require('chai');

Given('I am on the login page', async function() {
  await this.page.goto('/login');
});

When('I enter {string} in the email field', async function(email) {
  await this.page.fill('#email', email);
});

When('I click the login button', async function() {
  await this.page.click('button[type="submit"]');
});

Then('I should see {string} on the page', async function(text) {
  const content = await this.page.textContent('body');
  expect(content).to.include(text);
});
```

### Hooks

```java
import io.cucumber.java.*;

public class Hooks {
    @Before
    public void setUp(Scenario scenario) {
        driver = new ChromeDriver();
    }

    @After
    public void tearDown(Scenario scenario) {
        if (scenario.isFailed()) {
            byte[] screenshot = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
            scenario.attach(screenshot, "image/png", "failure-screenshot");
        }
        driver.quit();
    }
}
```

### 标签

```gherkin
@smoke
Feature: Login
  @critical @fast
  Scenario: Quick login
    ...

  @slow @regression
  Scenario: Full login flow
    ...
```

```bash
# Run by tag
mvn test -Dcucumber.filter.tags="@smoke"
mvn test -Dcucumber.filter.tags="@smoke and not @slow"
```

### 反模式

| 错误 | 正确 | 原因 |
|-----|------|-----|
| Gherkin 中混入 UI 细节 | 业务语言 | 可读性 |
| 一个步骤对应一行代码 | 业务上有意义的步骤 | 抽象 |
| 共有步骤不使用 Background | 使用 Background | DRY |
| 命令式步骤 | 声明式步骤 | 可维护 |


### 在 TestMu AI 上执行

设置环境变量：`LT_USERNAME`、`LT_ACCESS_KEY`

**Java：**
```java
// CucumberHooks.java
ChromeOptions browserOptions = new ChromeOptions();
HashMap<String, Object> ltOptions = new HashMap<>();
ltOptions.put("user", System.getenv("LT_USERNAME"));
ltOptions.put("accessKey", System.getenv("LT_ACCESS_KEY"));
ltOptions.put("build", "Cucumber Build");
ltOptions.put("name", scenario.getName());
ltOptions.put("platformName", "Windows 11");
ltOptions.put("video", true);
browserOptions.setCapability("LT:Options", ltOptions);
driver = new RemoteWebDriver(new URL("https://hub.lambdatest.com/wd/hub"), browserOptions);
```

**JavaScript：**
```javascript
const driver = new Builder()
  .usingServer(`https://${process.env.LT_USERNAME}:${process.env.LT_ACCESS_KEY}@hub.lambdatest.com/wd/hub`)
  .withCapabilities({ browserName: 'chrome', 'LT:Options': {
    user: process.env.LT_USERNAME, accessKey: process.env.LT_ACCESS_KEY,
    build: 'Cucumber Build', platformName: 'Windows 11', video: true
  }}).build();
```
## 速查表

| 任务 | 命令 |
|------|---------|
| 运行全部（Java） | `mvn test` 配合 cucumber-junit-platform-engine |
| 运行全部（JS） | `npx cucumber-js` |
| 按标签运行 | `--tags "@smoke"` |
| 演练 | `--dry-run` |
| 生成代码片段 | 运行未定义的步骤 |

## 进阶模式 → `reference/playbook.md`

| § | 章节 | 行数 |
|---|---------|-------|
| 1 | 项目搭建与配置 | Maven、runner、rerun |
| 2 | Feature 编写模式 | Background、outlines、DataTable |
| 3 | 步骤定义 | 类型化步骤、DI 注入 |
| 4 | 依赖注入与共享状态 | PicoContainer、ScenarioContext |
| 5 | Hooks（生命周期管理） | Before/After 顺序、截图 |
| 6 | 自定义参数类型 | Transformers、DocString |
| 7 | 并行执行 | 线程安全、TestNG 并行 |
| 8 | 报告 | Allure、masterthought、JSON |
| 9 | CI/CD 集成 | GitHub Actions、tag 矩阵 |
| 10 | 调试速查 | 10 个常见问题 |
| 11 | 最佳实践清单 | 13 项 |

## 局限性

- 仅在任务与上游源及本地项目上下文明确匹配时使用本技能。
- 在应用更改前，验证命令、生成的代码、依赖、凭证及外部服务行为。
- 不要把示例当作环境专属测试、安全审查或对破坏性或高成本操作的用户审批的替代。
