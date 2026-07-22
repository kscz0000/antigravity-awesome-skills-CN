---
name: playwright-java
description: "使用 Page Object Model、JUnit 5、Allure 报告和并行执行，搭建、编写、调试和增强企业级 Playwright E2E 测试。当用户要求搭建 Playwright Java 测试项目、编写 Page Object 类、配置跨浏览器测试或生成 Allure 报告时使用。"
category: test-automation
risk: safe
source: community
date_added: "2025-03-08"
author: amalsam18
tags: [playwright, java, e2e-testing, junit5, page-object-model, allure, selenium-alternative]
tools: [claude, cursor,antigravity]
---

# Playwright Java – 高级测试自动化

## 概述

本技能生成生产级、企业级的 Playwright Java 测试代码。强制使用 Page Object Model（POM）、严格的定位器策略、线程安全的并行执行以及完整的 Allure 报告集成。目标环境为 Java 17+ 和 Playwright 1.44+。

配套参考文件涵盖更深入的主题：

| 主题 | 文件 |
|-------|------|
| Maven POM、ConfigReader、Docker/CI 配置 | `references/config.md` |
| 组件模式、下拉框、上传、等待策略 | `references/page-objects.md` |
| 完整断言 API、软断言、视觉测试 | `references/assertions.md` |
| 夹具、测试数据工厂、认证状态、重试 | `references/fixtures.md` |
| 即用型基类模板 | `templates/BaseTest.java`、`templates/BasePage.java` |

---

## 何时使用本技能

- 从零搭建新的 Playwright Java 项目时使用
- 编写 Page Object 类或 JUnit 5 测试类时使用
- 用户询问跨浏览器测试、并行执行或 Allure 报告时使用
- 修复不稳定测试或用正确的等待策略替换 `Thread.sleep()` 时使用
- 在 CI/CD 流水线（GitHub Actions、Jenkins、Docker）中配置 Playwright 时使用
- 在单个测试中组合 API 调用和 UI 断言（混合测试）时使用
- 用户提到"POM 模式"、"BrowserContext"、"Playwright fixtures"或"traces"时使用

---

## 工作原理

### 第一步：确定方案

编写代码前，使用以下矩阵选择合适的模式：

| 用户需求 | 方案 |
|---|---|
| 从零创建新项目 | 完整脚手架 — 参见 `references/config.md` |
| 单功能测试 | POM 页面类 + JUnit5 测试类 |
| API + UI 混合 | `APIRequestContext` 配合 `Page` |
| 跨浏览器 | `@MethodSource` 按浏览器名称参数化 |
| 不稳定测试修复 | 用 `waitFor` / `waitForResponse` 替换 `sleep` |
| CI 集成 | 流水线中使用 `playwright install --with-deps` |
| 并行执行 | `junit-platform.properties` + `ThreadLocal` |
| 丰富报告 | Allure + Playwright trace + 视频录制 |

---

### 第二步：搭建项目结构

创建新项目时始终使用以下目录布局：

```
src/
├── test/
│   ├── java/com/company/tests/
│   │   ├── base/
│   │   │   ├── BaseTest.java        ← templates/BaseTest.java
│   │   │   └── BasePage.java        ← templates/BasePage.java
│   │   ├── pages/
│   │   │   └── LoginPage.java
│   │   ├── tests/
│   │   │   └── LoginTest.java
│   │   ├── utils/
│   │   │   ├── TestDataFactory.java
│   │   │   └── WaitUtils.java
│   │   └── config/
│   │       └── ConfigReader.java
│   └── resources/
│       ├── test.properties
│       ├── junit-platform.properties
│       └── testdata/users.json
pom.xml
```

---

### 第三步：配置线程安全的 BaseTest

```java
public class BaseTest {
    protected static ThreadLocal<Playwright>     playwrightTL = new ThreadLocal<>();
    protected static ThreadLocal<Browser>        browserTL    = new ThreadLocal<>();
    protected static ThreadLocal<BrowserContext> contextTL    = new ThreadLocal<>();
    protected static ThreadLocal<Page>           pageTL       = new ThreadLocal<>();

    protected Page page() { return pageTL.get(); }

    @BeforeEach
    void setUp() {
        Playwright playwright = Playwright.create();
        playwrightTL.set(playwright);

        Browser browser = resolveBrowser(playwright).launch(
            new BrowserType.LaunchOptions()
                .setHeadless(ConfigReader.isHeadless()));
        browserTL.set(browser);

        BrowserContext context = browser.newContext(new Browser.NewContextOptions()
            .setViewportSize(1920, 1080)
            .setRecordVideoDir(Paths.get("target/videos/"))
            .setLocale("en-US"));
        context.tracing().start(new Tracing.StartOptions()
            .setScreenshots(true).setSnapshots(true));
        contextTL.set(context);
        pageTL.set(context.newPage());
    }

    @AfterEach
    void tearDown(TestInfo testInfo) {
        String name = testInfo.getDisplayName().replaceAll("[^a-zA-Z0-9]", "_");
        contextTL.get().tracing().stop(new Tracing.StopOptions()
            .setPath(Paths.get("target/traces/" + name + ".zip")));
        pageTL.get().close();
        contextTL.get().close();
        browserTL.get().close();
        playwrightTL.get().close();
    }

    private BrowserType resolveBrowser(Playwright pw) {
        return switch (System.getProperty("browser", "chromium").toLowerCase()) {
            case "firefox" -> pw.firefox();
            case "webkit"  -> pw.webkit();
            default        -> pw.chromium();
        };
    }
}
```

---

### 第四步：构建 Page Object 类

```java
public class LoginPage extends BasePage {

    // 所有定位器声明为字段 — 不要在操作方法中内联
    private final Locator emailInput;
    private final Locator passwordInput;
    private final Locator loginButton;
    private final Locator errorMessage;

    public LoginPage(Page page) {
        super(page);
        emailInput    = page.getByLabel("Email address");
        passwordInput = page.getByLabel("Password");
        loginButton   = page.getByRole(AriaRole.BUTTON,
                            new Page.GetByRoleOptions().setName("Sign in"));
        errorMessage  = page.getByTestId("login-error");
    }

    @Override protected String getUrl() { return "/login"; }

    // 导航方法返回下一个 Page Object — 支持流式链式调用
    public DashboardPage loginAs(String email, String password) {
        fill(emailInput, email);
        fill(passwordInput, password);
        clickAndWaitForNav(loginButton);
        return new DashboardPage(page);
    }

    public LoginPage loginExpectingError(String email, String password) {
        fill(emailInput, email);
        fill(passwordInput, password);
        loginButton.click();
        errorMessage.waitFor();
        return this;
    }

    public String getErrorMessage() { return errorMessage.textContent(); }
}
```

---

### 第五步：使用 Allure 注解编写测试

```java
@ExtendWith(AllureJunit5.class)
class LoginTest extends BaseTest {

    private LoginPage loginPage;

    @BeforeEach
    void openLoginPage() {
        loginPage = new LoginPage(page());
        loginPage.navigate();
    }

    @Test
    @Severity(SeverityLevel.BLOCKER)
    @DisplayName("Valid credentials redirect to dashboard")
    void shouldLoginWithValidCredentials() {
        User user = TestDataFactory.getDefaultUser();
        DashboardPage dash = loginPage.loginAs(user.email(), user.password());

        assertThat(page()).hasURL(Pattern.compile(".*/dashboard"));
        assertThat(dash.getWelcomeBanner()).containsText("Welcome, " + user.firstName());
    }

    @Test
    void shouldShowErrorOnInvalidCredentials() {
        loginPage.loginExpectingError("bad@test.com", "wrongpass");

        SoftAssertions softly = new SoftAssertions();
        softly.assertThat(loginPage.getErrorMessage()).contains("Invalid email or password");
        softly.assertThat(page()).hasURL(Pattern.compile(".*/login"));
        softly.assertAll();
    }

    @ParameterizedTest
    @MethodSource("provideInvalidCredentials")
    void shouldRejectInvalidCredentials(String email, String password, String expectedError) {
        loginPage.loginExpectingError(email, password);
        assertThat(loginPage.getErrorMessage()).containsText(expectedError);
    }

    static Stream<Arguments> provideInvalidCredentials() {
        return Stream.of(
            Arguments.of("", "password123", "Email is required"),
            Arguments.of("user@test.com", "", "Password is required"),
            Arguments.of("notanemail", "pass", "Invalid email format")
        );
    }
}
```

---

## 示例

### 示例 1：API + UI 混合测试

```java
@Test
void shouldDisplayNewlyCreatedOrder() {
    // 通过 API 准备数据 — 比通过 UI 导航更快
    APIRequestContext api = page().context().request();
    APIResponse response = api.post("/api/orders",
        RequestOptions.create()
            .setHeader("Authorization", "Bearer " + authToken)
            .setData(Map.of("productId", "SKU-001", "quantity", 2)));
    assertThat(response).isOK();

    String orderId = new JsonParser().parse(response.text())
        .getAsJsonObject().get("id").getAsString();

    OrdersPage orders = new OrdersPage(page());
    orders.navigate();
    assertThat(orders.getOrderRowById(orderId)).isVisible();
}
```

### 示例 2：网络 Mock

```java
@Test
void shouldHandleApiFailureGracefully() {
    page().route("**/api/products", route -> route.fulfill(
        new Route.FulfillOptions()
            .setStatus(503)
            .setBody("{\"error\":\"Service Unavailable\"}")
            .setContentType("application/json")));

    ProductsPage products = new ProductsPage(page());
    products.navigate();

    assertThat(products.getErrorBanner())
        .hasText("We're having trouble loading products. Please try again.");
}
```

### 示例 3：并行跨浏览器测试

```java
@ParameterizedTest
@MethodSource("browsers")
void shouldRenderCheckoutOnAllBrowsers(String browserName) {
    System.setProperty("browser", browserName);
    new CheckoutPage(page()).navigate();
    assertThat(page().locator(".checkout-form")).isVisible();
}

static Stream<String> browsers() {
    return Stream.of("chromium", "firefox", "webkit");
}
```

### 示例 4：并行执行配置

```properties
# src/test/resources/junit-platform.properties
junit.jupiter.execution.parallel.enabled=true
junit.jupiter.execution.parallel.mode.default=concurrent
junit.jupiter.execution.parallel.config.strategy=fixed
junit.jupiter.execution.parallel.config.fixed.parallelism=4
```

### 示例 5：GitHub Actions CI 流水线

```yaml
- name: Install Playwright browsers
  run: mvn exec:java -e -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.args="install --with-deps"

- name: Run tests
  run: mvn test -Dbrowser=${{ matrix.browser }} -Dheadless=true

- name: Upload traces on failure
  uses: actions/upload-artifact@v4
  if: failure()
  with:
    name: playwright-traces
    path: target/traces/

- name: Upload Allure results
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: allure-results
    path: target/allure-results/
```

---

## 最佳实践

- ✅ 每个并行安全的测试套件使用 `ThreadLocal<Page>`
- ✅ 在 Page Object 类顶部声明所有 `Locator` 字段
- ✅ 导航方法返回下一个 Page Object（流式链式调用）
- ✅ 使用 `assertThat(locator)` — 自动重试直到超时
- ✅ 优先使用 `getByRole`、`getByLabel`、`getByTestId` 作为定位器
- ✅ 在 `@BeforeEach` 中启动 tracing，在 `@AfterEach` 中指定文件路径停止
- ✅ 验证单页面多个字段时使用 `SoftAssertions`
- ✅ 配置已保存的认证状态（`storageState`）以跳过跨测试类的登录
- ❌ 永远不要使用 `Thread.sleep()` — 替换为 `waitFor()` 或 `waitForResponse()`
- ❌ 永远不要硬编码基础 URL — 始终使用 `ConfigReader.getBaseUrl()`
- ❌ 永远不要在 Page Object 内创建 `Playwright` 实例
- ❌ 永远不要对动态或频繁变化的元素使用 XPath

---

## 常见陷阱

- **问题：** 并行模式下测试随机失败
  **解决方案：** 确保每个测试通过 `ThreadLocal` 创建自己的 `Playwright → Browser → BrowserContext → Page` 链。永远不要跨线程共享 `Page`。

- **问题：** `assertThat(locator).isVisible()` 超时，即使元素已经显示
  **解决方案：** 使用 `.setTimeout(10_000)` 增加超时时间，或在 `BaseTest` 中提高 `context.setDefaultTimeout()`。

- **问题：** 添加了 `Thread.sleep(2000)` 但测试仍然不稳定
  **解决方案：** 替换为 `page.waitForResponse("**/api/endpoint", () -> action())` 或 `assertThat(locator).hasText("Done")` 进行自动轮询。

- **问题：** Playwright trace zip 文件为空或缺失
  **解决方案：** 确保在测试操作之前调用 `tracing().start()`，且 `tracing().stop()` 在 `@AfterEach` 中 — 不是 `@AfterAll`。

- **问题：** Allure 报告为空或缺少步骤
  **解决方案：** 将 AspectJ agent 添加到 `pom.xml` 中 `maven-surefire-plugin` 的 `<argLine>` — 参见 `references/config.md` 中的完整代码片段。

- **问题：** `storageState` 认证文件过期，测试重定向到登录页
  **解决方案：** 在套件执行前重新运行 `AuthSetup` 以重新生成 `target/auth/user-state.json`，或添加一个 `@BeforeAll` 条件刷新它。

---

## 相关技能

- `@rest-assured-java` — 用于无 UI 交互的纯 API 测试套件
- `@selenium-java` — 遗留替代方案；所有新项目优先选择 Playwright
- `@allure-reporting` — 深入了解 Allure 注解、分类和历史趋势
- `@testcontainers-java` — 测试需要实时数据库或服务时配合本技能使用
- `@github-actions-ci` — 用于构建完整的多浏览器矩阵 CI 流水线

## 限制

- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并要求澄清。
