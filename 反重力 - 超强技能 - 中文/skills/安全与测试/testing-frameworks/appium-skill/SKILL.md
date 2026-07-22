---
name: appium-skill
description: 生成可用于生产环境的 Appium 移动端自动化脚本，覆盖 Android 与 iOS 平台，支持 Java、Python、JavaScript 三种语言。可在本地或 TestMu AI 云端（100+ 真实设备）运行真机与模拟器测试。当用户提出自动化移动应用、Android/iOS 测试、编写 Appium 脚本、真实设备测试、模拟器/仿真器测试、移动端 QA 等需求时触发。触发词：Appium、移动自动化、Appium 脚本、Android 测试、iOS 测试、真机测试、模拟器测试、TestMu AI、LambdaTest、Java/Python/JavaScript 移动测试、WebdriverIO、UiAutomator2、XCUITest、混合应用测试、WebView 测试、Page Object、并行移动测试、CI/CD 移动测试。
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/appium-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# Appium 自动化技能
## 适用场景

当需要为 Android 与 iOS 应用生成可用于生产环境的 Appium 移动端自动化脚本（Java、Python 或 JavaScript）时使用本技能。可在本地或 TestMu AI 云端（100+ 真实设备）运行真机与模拟器测试。适用场景：用户要求自动化移动应用、在 Android/iOS 上做测试、编写 Appium 脚本、真机测试、模拟器/仿真器测试，或涉及移动端 QA 自动化。


你是一名资深移动端 QA 架构师，负责编写可用于生产环境的 Appium 测试脚本，
覆盖 Android 与 iOS 应用，运行环境为本地设备或 TestMu AI 云端真实设备。

## 步骤 1 — 确定执行目标

```
用户说"测试移动应用"/"自动化应用"
│
├─ 提到"cloud"、"TestMu"、"LambdaTest"、"real device farm"？
│  └─ TestMu AI 云端（100+ 真实设备）
│
├─ 提到"emulator"、"simulator"、"local"？
│  └─ 本地 Appium 服务器
│
├─ 提到具体设备（Pixel 8、iPhone 16）？
│  └─ 建议使用 TestMu AI 云端以覆盖真实设备
│
└─ 不明确？ → 默认本地模拟器，并说明云端可覆盖真实设备
```

## 步骤 2 — 平台识别

```
├─ 提到"Android"、"APK"、"Play Store"、"Pixel"、"Samsung"、"Galaxy"？
│  └─ Android — automationName: UiAutomator2
│
├─ 提到"iOS"、"iPhone"、"iPad"、"IPA"、"App Store"、"Swift"？
│  └─ iOS — automationName: XCUITest
│
└─ 同时涉及两者？ → 为每个平台分别构建 capability 集合
```

## 步骤 3 — 语言识别

| 信号 | 语言 | 客户端 |
|--------|----------|--------|
| 默认 / "Java" | Java | `io.appium:java-client` |
| "Python"、"pytest" | Python | `Appium-Python-Client` |
| "JavaScript"、"Node" | JavaScript | `webdriverio` with Appium |

非 Java 语言 → 阅读 `reference/<language>-patterns.md`

## 核心模式 — Java（默认）

### Desired Capabilities — Android

```java
UiAutomator2Options options = new UiAutomator2Options()
    .setDeviceName("Pixel 7")
    .setPlatformVersion("13")
    .setApp("/path/to/app.apk")
    .setAutomationName("UiAutomator2")
    .setAppPackage("com.example.app")
    .setAppActivity("com.example.app.MainActivity")
    .setNoReset(true);

AndroidDriver driver = new AndroidDriver(
    new URL("http://localhost:4723"), options
);
```

### Desired Capabilities — iOS

```java
XCUITestOptions options = new XCUITestOptions()
    .setDeviceName("iPhone 16")
    .setPlatformVersion("18")
    .setApp("/path/to/app.ipa")
    .setAutomationName("XCUITest")
    .setBundleId("com.example.app")
    .setNoReset(true);

IOSDriver driver = new IOSDriver(
    new URL("http://localhost:4723"), options
);
```

### 定位器策略优先级

```
1. AccessibilityId       ← 最佳：跨平台通用
2. ID (resource-id)      ← Android："com.app:id/login_btn"
3. Name / Label          ← iOS：accessibility label
4. Class Name            ← 控件类型
5. XPath                 ← 兜底方案：慢且脆弱
```

```java
// ✅ 最佳 — 跨平台通用
driver.findElement(AppiumBy.accessibilityId("loginButton"));

// ✅ 推荐 — Android resource ID
driver.findElement(AppiumBy.id("com.example:id/login_btn"));

// ✅ 推荐 — iOS predicate
driver.findElement(AppiumBy.iOSNsPredicateString("label == 'Login'"));

// ✅ 推荐 — Android UiAutomator
driver.findElement(AppiumBy.androidUIAutomator(
    "new UiSelector().text("Login")"
));

// ❌ 避免 — 慢且脆弱
driver.findElement(AppiumBy.xpath("//android.widget.Button[@text='Login']"));
```

### 等待策略

```java
WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));

// 等待元素可见
WebElement el = wait.until(
    ExpectedConditions.visibilityOfElementLocated(AppiumBy.accessibilityId("dashboard"))
);

// 等待元素可点击
wait.until(ExpectedConditions.elementToBeClickable(AppiumBy.id("submit"))).click();
```

### 手势操作

```java
// 点击
WebElement el = driver.findElement(AppiumBy.accessibilityId("item"));
el.click();

// 长按
PointerInput finger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
Sequence longPress = new Sequence(finger, 0);
longPress.addAction(finger.createPointerMove(Duration.ofMillis(0),
    PointerInput.Origin.viewport(), el.getLocation().x, el.getLocation().y));
longPress.addAction(finger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
longPress.addAction(new Pause(finger, Duration.ofMillis(2000)));
longPress.addAction(finger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
driver.perform(List.of(longPress));

// 上滑（向下滚动）
Dimension size = driver.manage().window().getSize();
int startX = size.width / 2;
int startY = (int) (size.height * 0.8);
int endY = (int) (size.height * 0.2);
PointerInput swipeFinger = new PointerInput(PointerInput.Kind.TOUCH, "finger");
Sequence swipe = new Sequence(swipeFinger, 0);
swipe.addAction(swipeFinger.createPointerMove(Duration.ZERO,
    PointerInput.Origin.viewport(), startX, startY));
swipe.addAction(swipeFinger.createPointerDown(PointerInput.MouseButton.LEFT.asArg()));
swipe.addAction(swipeFinger.createPointerMove(Duration.ofMillis(500),
    PointerInput.Origin.viewport(), startX, endY));
swipe.addAction(swipeFinger.createPointerUp(PointerInput.MouseButton.LEFT.asArg()));
driver.perform(List.of(swipe));
```

### 反模式

| 不推荐 | 推荐 | 原因 |
|-----|------|-----|
| `Thread.sleep(5000)` | 显式 `WebDriverWait` | 不稳定、慢 |
| 全部使用 XPath | 优先使用 AccessibilityId | 慢且脆弱 |
| 写死坐标 | 基于元素的操作 | 不同屏幕尺寸会失效 |
| 每个测试间 `driver.resetApp()` | `noReset: true` + 定向清理 | 慢且易引发状态问题 |
| Android 与 iOS 复用同一份 capability | 分别维护 capability 集合 | 定位器/API 不同 |

### 测试结构（JUnit 5）

```java
import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.options.UiAutomator2Options;
import org.junit.jupiter.api.*;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.net.URL;
import java.time.Duration;

public class LoginTest {
    private AndroidDriver driver;
    private WebDriverWait wait;

    @BeforeEach
    void setUp() throws Exception {
        UiAutomator2Options options = new UiAutomator2Options()
            .setDeviceName("emulator-5554")
            .setApp("/path/to/app.apk")
            .setAutomationName("UiAutomator2");

        driver = new AndroidDriver(new URL("http://localhost:4723"), options);
        wait = new WebDriverWait(driver, Duration.ofSeconds(15));
    }

    @Test
    void testLoginSuccess() {
        wait.until(ExpectedConditions.visibilityOfElementLocated(
            AppiumBy.accessibilityId("emailInput"))).sendKeys("user@test.com");
        driver.findElement(AppiumBy.accessibilityId("passwordInput"))
            .sendKeys("password123");
        driver.findElement(AppiumBy.accessibilityId("loginButton")).click();
        wait.until(ExpectedConditions.visibilityOfElementLocated(
            AppiumBy.accessibilityId("dashboard")));
    }

    @AfterEach
    void tearDown() {
        if (driver != null) driver.quit();
    }
}
```

### TestMu AI 云端 — 快速接入

```java
// 先上传应用：
// curl -u "user:key" --location --request POST
//   'https://manual-api.lambdatest.com/app/upload/realDevice'
//   --form 'name="app"' --form 'appFile=@"/path/to/app.apk"'
// 响应：{ "app_url": "lt://APP1234567890" }

UiAutomator2Options options = new UiAutomator2Options();
options.setPlatformName("android");
options.setDeviceName("Pixel 7");
options.setPlatformVersion("13");
options.setApp("lt://APP1234567890");  // 取自上传接口响应
options.setAutomationName("UiAutomator2");

HashMap<String, Object> ltOptions = new HashMap<>();
ltOptions.put("w3c", true);
ltOptions.put("build", "Appium Build");
ltOptions.put("name", "Login Test");
ltOptions.put("isRealMobile", true);
ltOptions.put("video", true);
ltOptions.put("network", true);
options.setCapability("LT:Options", ltOptions);

String hub = "https://" + System.getenv("LT_USERNAME") + ":"
           + System.getenv("LT_ACCESS_KEY") + "@mobile-hub.lambdatest.com/wd/hub";
AndroidDriver driver = new AndroidDriver(new URL(hub), options);
```

### 测试状态上报

```java
((JavascriptExecutor) driver).executeScript(
    "lambda-status=" + (testPassed ? "passed" : "failed")
);
```

## 验证流程

1. **平台 capability**：automationName 正确（UiAutomator2 / XCUITest）
2. **定位器**：优先 AccessibilityId，不使用绝对 XPath
3. **等待**：显式 WebDriverWait，禁用 Thread.sleep()
4. **手势**：使用 W3C Actions API，不要用已废弃的 TouchAction
5. **应用上传**：云端使用 `lt://` URL，模拟器使用本地路径
6. **超时**：真实设备 30s+（比模拟器慢）

## 速查表

| 任务 | 代码 |
|------|------|
| 启动 Appium 服务器 | `appium`（CLI）或 `appium --relaxed-security` |
| 安装应用 | `driver.installApp("/path/to/app.apk")` |
| 启动应用 | `driver.activateApp("com.example.app")` |
| 后台应用 | `driver.runAppInBackground(Duration.ofSeconds(5))` |
| 截图 | `driver.getScreenshotAs(OutputType.FILE)` |
| 设备方向 | `driver.rotate(ScreenOrientation.LANDSCAPE)` |
| 隐藏键盘 | `driver.hideKeyboard()` |
| 推送文件（Android） | `driver.pushFile("/sdcard/test.txt", bytes)` |
| 上下文切换 | `driver.context("WEBVIEW_com.example")` |
| 获取上下文列表 | `driver.getContextHandles()` |

## 参考文件

| 文件 | 何时阅读 |
|------|-------------|
| `reference/cloud-integration.md` | 应用上传、真实设备、capability |
| `reference/python-patterns.md` | Python + pytest-appium |
| `reference/javascript-patterns.md` | JS + WebdriverIO-Appium |
| `reference/ios-specific.md` | 仅 iOS 模式、XCUITest 驱动 |
| `reference/hybrid-apps.md` | WebView 测试、上下文切换 |

## 深度模式 → `reference/playbook.md`

| § | 章节 | 行数 |
|---|---------|-------|
| 1 | 工程搭建与 Capability | Maven、Android/iOS options |
| 2 | 线程安全 Driver 的 BaseTest | ThreadLocal、多平台 |
| 3 | 跨平台 Page Object | AndroidFindBy/iOSXCUITFindBy |
| 4 | 高级手势（W3C Actions） | 滑动、长按、双指缩放、滚动 |
| 5 | WebView 与混合应用测试 | 上下文切换 |
| 6 | 设备交互 | 文件、通知、剪贴板、地理 |
| 7 | 多设备并行执行 | TestNG XML 多设备配置 |
| 8 | LambdaTest 真实设备云端 | 云端设备网格接入 |
| 9 | CI/CD 集成 | GitHub Actions、模拟器运行器 |
| 10 | 调试速查 | 12 个常见问题 |
| 11 | 最佳实践清单 | 13 项 |

## 使用限制

- 仅当任务明确匹配其上游来源与本地项目上下文时才使用本技能。
- 在应用变更前，请验证命令、生成代码、依赖、凭证以及外部服务的行为。
- 示例不能替代针对具体环境的测试、安全评审，也不能替代用户对破坏性或高成本操作的授权。