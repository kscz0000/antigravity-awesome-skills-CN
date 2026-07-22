# Playwright Java – 断言参考

## Import 声明

```java
import static com.microsoft.playwright.assertions.PlaywrightAssertions.assertThat;
import org.assertj.core.api.SoftAssertions;
```

---

## 定位器断言（自动重试）

Playwright 的 `assertThat(locator)` 自动轮询（最多等待 `defaultTimeout`）。**始终优先使用这些断言，而不是 `locator.isVisible()` + `assertTrue`。**

```java
// 可见性
assertThat(locator).isVisible();
assertThat(locator).isHidden();

// 启用 / 禁用
assertThat(locator).isEnabled();
assertThat(locator).isDisabled();

// 文本内容（精确或部分匹配）
assertThat(locator).hasText("Exact text");
assertThat(locator).containsText("partial");
assertThat(locator).hasText(Pattern.compile("Order #\\d+"));

// 多元素
assertThat(locator).hasCount(5);
assertThat(locator).hasText(new String[]{"Item A", "Item B", "Item C"});

// 属性
assertThat(locator).hasAttribute("aria-expanded", "true");
assertThat(locator).hasAttribute("href", Pattern.compile(".*\\/dashboard"));

// CSS 类
assertThat(locator).hasClass("active");
assertThat(locator).hasClass(Pattern.compile("btn-.*"));

// 输入值
assertThat(locator).hasValue("expected input value");
assertThat(locator).hasValue(Pattern.compile("\\d{4}-\\d{2}-\\d{2}")); // 日期模式

// 选中状态（复选框/单选框）
assertThat(locator).isChecked();
assertThat(locator).not().isChecked();

// 聚焦状态
assertThat(locator).isFocused();

// 可编辑状态
assertThat(locator).isEditable();
```

---

## 页面断言

```java
// URL
assertThat(page).hasURL("https://example.com/dashboard");
assertThat(page).hasURL(Pattern.compile(".*/dashboard"));

// 标题
assertThat(page).hasTitle("Dashboard – MyApp");
assertThat(page).hasTitle(Pattern.compile(".*Dashboard.*"));
```

---

## 取反

```java
// 添加 .not() 进行反向断言
assertThat(locator).not().isVisible();
assertThat(locator).not().hasText("Error");
assertThat(page).not().hasURL(Pattern.compile(".*/login"));
```

---

## 断言自定义超时

```java
assertThat(locator)
    .hasText("Loaded", new LocatorAssertions.HasTextOptions().setTimeout(10_000));
```

---

## 软断言（AssertJ）

在报告前收集所有失败 — 对表单验证测试至关重要：

```java
@Test
void shouldDisplayAllProfileFields() {
    ProfilePage profile = new ProfilePage(page());
    profile.navigate();

    SoftAssertions soft = new SoftAssertions();
    soft.assertThat(profile.getNameField().inputValue()).isEqualTo("Amal");
    soft.assertThat(profile.getEmailField().inputValue()).contains("@");
    soft.assertThat(profile.getRoleLabel().textContent()).isEqualTo("Engineer");
    soft.assertAll(); // 结束时抛出异常，列出所有失败项
}
```

---

## 响应断言

```java
APIResponse response = page().context().request().get("/api/health");
assertThat(response).isOK();                         // 状态码 200-299
assertThat(response).hasStatus(201);
assertThat(response).hasHeader("content-type", "application/json");
assertThat(response).hasJSON("{\"status\":\"UP\"}"); // 精确 JSON 匹配
```

---

## 截图对比（视觉测试）

```java
// 全页截图
assertThat(page).hasScreenshot(new PageAssertions.HasScreenshotOptions()
    .setName("dashboard.png")
    .setFullPage(true)
    .setThreshold(0.2));

// 定位器截图
assertThat(page.locator(".chart-container"))
    .hasScreenshot(new LocatorAssertions.HasScreenshotOptions()
        .setName("revenue-chart.png"));
```

更新基准文件：使用 `PLAYWRIGHT_UPDATE_SNAPSHOTS=true mvn test` 运行

---

## 常见反模式（应避免）

```java
// ❌ 错误 — 无自动重试，容易断裂
assertTrue(page.locator(".spinner").isHidden());
Thread.sleep(2000);

// ✅ 正确 — 自动重试直到超时
assertThat(page.locator(".spinner")).isHidden();

// ❌ 错误 — getText() 可能返回过期值
String text = locator.textContent();
assertEquals("Done", text);

// ✅ 正确 — 断言重试直到文本匹配
assertThat(locator).hasText("Done");

// ❌ 错误 — 无等待的计数检查
assertEquals(5, page.locator("li").count());

// ✅ 正确 — 等待计数稳定
assertThat(page.locator("li")).hasCount(5);
```
