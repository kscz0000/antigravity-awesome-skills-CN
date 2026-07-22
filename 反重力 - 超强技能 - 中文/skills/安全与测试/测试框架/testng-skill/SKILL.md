---
name: testng-skill
description: '生成 Java TestNG 测试用例，包含分组、数据源、并行执行、XML 套件配置与监听器。在用户提及 "TestNG"、"@DataProvider"、"testng.xml"、"groups" 时使用。触发词："TestNG"、"@DataProvider"、"testng.xml"、"TestNG suite"、"parallel tests Java"。'
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/testng-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# TestNG 测试技能
## 使用时机

当你需要在 Java 中生成 TestNG 测试用例（包含分组、数据源、并行执行、XML 套件配置与监听器）时使用本技能。在用户提及 "TestNG"、"@DataProvider"、"testng.xml"、"groups" 时使用。触发词："TestNG"、"@DataProvider"、"testng.xml"、"TestNG suite"、"parallel tests Java"。


## 核心模式

### 带分组的基础测试

```java
import org.testng.annotations.*;
import org.testng.Assert;

public class LoginTest {
    @BeforeMethod
    public void setUp() { /* setup */ }

    @Test(groups = "smoke")
    public void testLoginSuccess() {
        Assert.assertTrue(loginService.login("user@test.com", "password123"));
    }

    @Test(groups = "regression", dependsOnMethods = "testLoginSuccess")
    public void testAccessDashboard() {
        Assert.assertNotNull(dashboard.getContent());
    }

    @Test(expectedExceptions = AuthenticationException.class)
    public void testLoginInvalidPassword() {
        loginService.login("user@test.com", "wrong");
    }

    @AfterMethod
    public void tearDown() { /* cleanup */ }
}
```

### 数据源

```java
@DataProvider(name = "loginData")
public Object[][] loginData() {
    return new Object[][] {
        {"admin@test.com", "admin123", true},
        {"user@test.com", "password", true},
        {"invalid@test.com", "wrong", false},
    };
}

@Test(dataProvider = "loginData")
public void testLogin(String email, String password, boolean expected) {
    Assert.assertEquals(loginService.login(email, password), expected);
}
```

### TestNG XML 套件

```xml
<!DOCTYPE suite SYSTEM "https://testng.org/testng-1.0.dtd">
<suite name="Regression" parallel="tests" thread-count="5">
  <test name="Smoke">
    <groups><run><include name="smoke"/></run></groups>
    <classes><class name="tests.LoginTest"/></classes>
  </test>
  <test name="Full">
    <groups><run><include name="regression"/><exclude name="flaky"/></run></groups>
    <packages><package name="tests.*"/></packages>
  </test>
</suite>
```

### 并行执行

```xml
<suite parallel="methods" thread-count="5">   <!-- Method level -->
<suite parallel="classes" thread-count="5">    <!-- Class level -->
<suite parallel="tests" thread-count="5">      <!-- Test level -->
```

### 软断言

```java
SoftAssert soft = new SoftAssert();
soft.assertEquals(user.getName(), "Alice");
soft.assertEquals(user.getAge(), 25);
soft.assertTrue(user.isActive());
soft.assertAll();  // Reports all failures at once
```

### 监听器

```java
public class TestListener implements ITestListener {
    @Override public void onTestFailure(ITestResult result) {
        System.out.println("Failed: " + result.getName());
        // Take screenshot, log, etc.
    }
}

@Listeners(TestListener.class)
public class LoginTest { /* ... */ }
```

### 生命周期注解

```
@BeforeSuite → @BeforeTest → @BeforeClass → @BeforeMethod → @Test → @AfterMethod → @AfterClass → @AfterTest → @AfterSuite
```

### 反模式

| 不好 | 良好 | 原因 |
|-----|------|-----|
| 到处使用 `dependsOnMethods` | 独立的测试 | 级联失败 |
| 不使用分组 | `@Test(groups = "smoke")` | 无法运行子集 |
| 硬编码测试数据 | `@DataProvider` | 可复用 |
| 按优先级排序 | 独立的测试 | 脆弱 |

## 速查表

| 任务 | 命令 |
|------|---------|
| 运行套件 | `mvn test -DsuiteXmlFile=testng.xml` |
| 运行分组 | `mvn test -Dgroups=smoke` |
| 运行类 | `mvn test -Dtest=LoginTest` |
| 报告 | `test-output/index.html` |

## 进阶模式 → `reference/playbook.md`

| § | 章节 | 行数 |
|---|---------|-------|
| 1 | 项目搭建与配置 | Maven + Surefire 配置 |
| 2 | 套件 XML 配置 | 多环境、并行、分组 |
| 3 | BaseTest 与线程安全驱动 | ThreadLocal、ConfigReader |
| 4 | 数据源（进阶） | Excel、JSON、CSV、并行、跨类 |
| 5 | 工厂模式 | 跨浏览器矩阵 |
| 6 | 监听器（生产套件） | 重试、截图、计时 |
| 7 | 软断言与依赖 | 分组、方法依赖 |
| 8 | Page Object 集成 | PageFactory、流畅式 PO |
| 9 | 并行执行策略 | 方法/类/测试/混合 |
| 10 | 报告集成 | Allure、ExtentReports |
| 11 | CI/CD 集成 | GitHub Actions、Jenkins |
| 12 | 调试速查 | 12 个常见问题 |
| 13 | 最佳实践清单 | 14 项 |

## 局限性

- 仅当任务明确匹配其上游来源与本地项目上下文时使用本技能。
- 在应用更改前，请校验命令、生成的代码、依赖、凭证以及外部服务行为。
- 切勿把示例当作环境特定测试、安全审查或用户对破坏性/高成本操作的批准替代品。