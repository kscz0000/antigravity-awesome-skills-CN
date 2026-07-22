# Playwright Java – 夹具、钩子与测试数据

## JUnit 5 Playwright 扩展（自定义夹具）

将浏览器生命周期封装为可复用的 JUnit 5 扩展：

```java
package com.company.tests.base;

import com.microsoft.playwright.*;
import org.junit.jupiter.api.extension.*;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public class PlaywrightExtension
        implements BeforeEachCallback, AfterEachCallback, ParameterResolver {

    private static final Map<String, Page> pageMap = new ConcurrentHashMap<>();

    @Override
    public void beforeEach(ExtensionContext ctx) {
        Playwright pw = Playwright.create();
        Browser browser = pw.chromium().launch(new BrowserType.LaunchOptions().setHeadless(true));
        BrowserContext context = browser.newContext();
        Page page = context.newPage();
        pageMap.put(ctx.getUniqueId(), page);

        ctx.getStore(ExtensionContext.Namespace.GLOBAL).put("playwright", pw);
        ctx.getStore(ExtensionContext.Namespace.GLOBAL).put("browser", browser);
        ctx.getStore(ExtensionContext.Namespace.GLOBAL).put("context", context);
    }

    @Override
    public void afterEach(ExtensionContext ctx) {
        pageMap.remove(ctx.getUniqueId());
        closeIfNotNull(ctx.getStore(ExtensionContext.Namespace.GLOBAL).remove("context", BrowserContext.class));
        closeIfNotNull(ctx.getStore(ExtensionContext.Namespace.GLOBAL).remove("browser", Browser.class));
        closeIfNotNull(ctx.getStore(ExtensionContext.Namespace.GLOBAL).remove("playwright", Playwright.class));
    }

    @Override
    public boolean supportsParameter(ParameterContext param, ExtensionContext ext) {
        return param.getParameter().getType() == Page.class;
    }

    @Override
    public Object resolveParameter(ParameterContext param, ExtensionContext ext) {
        return pageMap.get(ext.getUniqueId());
    }

    private void closeIfNotNull(AutoCloseable obj) {
        if (obj != null) try { obj.close(); } catch (Exception ignored) {}
    }
}

// 使用方式：
@ExtendWith(PlaywrightExtension.class)
class CheckoutTest {
    @Test
    void shouldCompleteCheckout(Page page) {
        // Page 通过依赖注入自动提供
        new LoginPage(page).navigate().loginAs("user@test.com", "pass");
    }
}
```

---

## 测试数据工厂

```java
package com.company.tests.utils;

import com.fasterxml.jackson.databind.ObjectMapper;
import net.datafaker.Faker;

import java.io.InputStream;
import java.util.List;

public final class TestDataFactory {
    private static final Faker faker = new Faker();
    private static final ObjectMapper mapper = new ObjectMapper();

    // --- 从 JSON 加载静态测试数据 ---
    public static User getDefaultUser() {
        return loadUsers().stream()
                .filter(u -> u.role().equals("default"))
                .findFirst()
                .orElseThrow(() -> new RuntimeException("No default user in testdata/users.json"));
    }

    public static User getAdminUser() {
        return loadUsers().stream()
                .filter(u -> u.role().equals("admin"))
                .findFirst()
                .orElseThrow();
    }

    @SuppressWarnings("unchecked")
    private static List<User> loadUsers() {
        try (InputStream in = TestDataFactory.class
                .getClassLoader().getResourceAsStream("testdata/users.json")) {
            return mapper.readValue(in, mapper.getTypeFactory()
                    .constructCollectionType(List.class, User.class));
        } catch (Exception e) {
            throw new RuntimeException("Failed to load users.json", e);
        }
    }

    // --- 动态数据生成 ---
    public static User generateRandomUser() {
        return new User(
            faker.internet().emailAddress(),
            faker.internet().password(12, 20, true, true, true),
            faker.name().firstName(),
            faker.name().lastName(),
            "default"
        );
    }

    public static String randomPhone() {
        return faker.phoneNumber().cellPhone();
    }

    public static String randomPostalCode() {
        return faker.address().zipCode();
    }
}
```

---

## `testdata/users.json`

```json
[
  {
    "email": "admin@company.com",
    "password": "Admin@1234",
    "firstName": "Admin",
    "lastName": "User",
    "role": "admin"
  },
  {
    "email": "user@company.com",
    "password": "User@1234",
    "firstName": "Test",
    "lastName": "User",
    "role": "default"
  }
]
```

---

## 预认证上下文（复用认证状态）

保存一次登录状态，在多个测试中复用 — 大幅提升执行速度：

```java
// 在测试套件前运行一次（例如在 @BeforeAll 或初始化类中）
public class AuthSetup {
    public static void saveAuthState() {
        try (Playwright pw = Playwright.create()) {
            Browser browser = pw.chromium().launch();
            BrowserContext context = browser.newContext();
            Page page = context.newPage();

            page.navigate(ConfigReader.getBaseUrl() + "/login");
            page.getByLabel("Email").fill(TestDataFactory.getDefaultUser().email());
            page.getByLabel("Password").fill(TestDataFactory.getDefaultUser().password());
            page.getByRole(AriaRole.BUTTON, new Page.GetByRoleOptions().setName("Sign in")).click();
            page.waitForURL("**/dashboard");

            // 保存存储状态（cookies + localStorage）
            context.storageState(new BrowserContext.StorageStateOptions()
                .setPath(Paths.get("target/auth/user-state.json")));
        }
    }
}

// 在 BaseTest 中加载已保存的状态：
BrowserContext context = browser.newContext(new Browser.NewContextOptions()
    .setStorageStatePath(Paths.get("target/auth/user-state.json")));
```

---

## 测试失败时截图（Allure 附件）

```java
// 在 BaseTest 的 @AfterEach 中添加
@AfterEach
void captureOnFailure(TestInfo info) {
    // JUnit5 + Allure 中可通过 TestInfo 获取测试结果
    byte[] screenshot = page().screenshot(new Page.ScreenshotOptions().setFullPage(true));
    Allure.addAttachment("Screenshot on failure", "image/png",
        new ByteArrayInputStream(screenshot), "png");
}
```

---

## WaitUtils 辅助工具

```java
package com.company.tests.utils;

import com.microsoft.playwright.Page;

public final class WaitUtils {

    public static void waitForSpinnerToDisappear(Page page) {
        page.locator(".loading-spinner").waitFor(
            new Locator.WaitForOptions()
                .setState(WaitForSelectorState.HIDDEN)
                .setTimeout(15_000));
    }

    public static void waitForToastMessage(Page page, String message) {
        page.getByRole(AriaRole.ALERT)
            .filter(new Locator.FilterOptions().setHasText(message))
            .waitFor(new Locator.WaitForOptions()
                .setState(WaitForSelectorState.VISIBLE)
                .setTimeout(5_000));
    }

    public static void waitForApiResponse(Page page, String urlPattern) {
        page.waitForResponse(resp ->
            resp.url().contains(urlPattern) && resp.status() < 400,
            () -> {}
        );
    }
}
```

---

## 不稳定测试的重试逻辑

```java
// JUnit 5 内置重试扩展
// 添加到 pom.xml：
// <dependency>
//   <groupId>org.junit.jupiter</groupId>
//   <artifactId>junit-jupiter-engine</artifactId>
//   <version>5.10.2</version>
// </dependency>

@RepeatedTest(value = 3, failureThreshold = 1) // 最多重试 3 次
void flakySmokeTest() {
    // 测试体
}

// 基于 JUnit Extension 的自定义 @RetryTest 注解：
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@ExtendWith(RetryExtension.class)
public @interface RetryTest {
    int times() default 3;
}
```
