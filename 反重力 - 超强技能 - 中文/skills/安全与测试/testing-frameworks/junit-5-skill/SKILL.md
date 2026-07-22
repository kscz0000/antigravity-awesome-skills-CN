---
name: junit-5-skill
description: 生成生产级 JUnit 5 单元测试和集成测试（Java）。涵盖断言、参数化测试、生命周期钩子、Mockito 模拟和嵌套测试。当用户提到 "JUnit"、"JUnit 5"、"@Test"、"assertEquals"、"Assertions"、"Java 单元测试" 时使用。触发词：JUnit、JUnit 5、@Test、assertEquals、断言、Java 单元测试、参数化测试、Mockito、嵌套测试
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/junit-5-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# JUnit 5 测试技能
## 何时使用

当你需要生成生产级 JUnit 5 单元测试和集成测试时使用此技能。涵盖断言、参数化测试、生命周期钩子、Mockito 模拟和嵌套测试。当用户提到 "JUnit"、"JUnit 5"、"@Test"、"assertEquals"、"Assertions"、"Java 单元测试" 时使用。触发词：...


你是一名专注于 JUnit 5 测试的高级 Java 开发者。

## 步骤 1 — 测试类型

```
├─ "unit test", "assert" → Standard unit test
├─ "parameterized", "multiple inputs" → @ParameterizedTest
├─ "mock", "Mockito" → Unit test with Mockito
├─ "integration test", "Spring" → Read reference/spring-integration.md
└─ Default → Standard unit test
```

## 核心模式

### 基础测试

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculatorTest {
    private Calculator calculator;

    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }

    @Test
    @DisplayName("Addition of two positive numbers")
    void addPositiveNumbers() {
        assertEquals(5, calculator.add(2, 3));
    }

    @Test
    void divideByZero_throwsException() {
        assertThrows(ArithmeticException.class, () -> calculator.divide(10, 0));
    }

    @Test
    void multipleAssertions() {
        assertAll("calculator operations",
            () -> assertEquals(4, calculator.add(2, 2)),
            () -> assertEquals(0, calculator.subtract(2, 2)),
            () -> assertEquals(6, calculator.multiply(2, 3))
        );
    }
}
```

### 断言参考

```java
assertEquals(expected, actual);
assertNotEquals(unexpected, actual);
assertTrue(condition);
assertFalse(condition);
assertNull(object);
assertNotNull(object);
assertThrows(IllegalArgumentException.class, () -> service.process(null));
assertTimeout(Duration.ofSeconds(2), () -> service.longRunningOp());
assertAll("group",
    () -> assertNotNull(user.getName()),
    () -> assertTrue(user.getAge() > 0)
);
assertIterableEquals(List.of(1, 2, 3), actualList);
```

### 参数化测试

```java
@ParameterizedTest
@ValueSource(strings = {"hello", "world", "junit"})
void stringIsNotEmpty(String value) {
    assertFalse(value.isEmpty());
}

@ParameterizedTest
@CsvSource({"1,1,2", "2,3,5", "10,-5,5"})
void addNumbers(int a, int b, int expected) {
    assertEquals(expected, calculator.add(a, b));
}

@ParameterizedTest
@MethodSource("provideUsers")
void validateUser(String name, int age, boolean expected) {
    assertEquals(expected, validator.isValid(name, age));
}

static Stream<Arguments> provideUsers() {
    return Stream.of(
        Arguments.of("Alice", 25, true),
        Arguments.of("", 25, false),
        Arguments.of("Bob", -1, false)
    );
}

@ParameterizedTest
@NullAndEmptySource
@ValueSource(strings = {"  ", "\t"})
void blankStringsAreInvalid(String input) {
    assertFalse(validator.isValid(input));
}
```

### 使用 Mockito 模拟

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock private UserRepository userRepo;
    @Mock private EmailService emailService;
    @InjectMocks private UserService userService;

    @Test
    void createUser_savesAndSendsEmail() {
        User user = new User("alice@test.com", "Alice");
        when(userRepo.save(any(User.class))).thenReturn(user);

        User result = userService.createUser("alice@test.com", "Alice");

        assertNotNull(result);
        verify(userRepo).save(any(User.class));
        verify(emailService).sendWelcomeEmail("alice@test.com");
    }

    @Test
    void getUser_notFound_throwsException() {
        when(userRepo.findById(99L)).thenReturn(Optional.empty());
        assertThrows(UserNotFoundException.class, () -> userService.getUser(99L));
    }
}
```

### 嵌套测试

```java
@DisplayName("UserService")
class UserServiceTest {
    @Nested
    @DisplayName("when creating a user")
    class CreateUser {
        @Test void withValidData_succeeds() { }
        @Test void withDuplicateEmail_throwsException() { }
    }

    @Nested
    @DisplayName("when deleting a user")
    class DeleteUser {
        @Test void existingUser_removesFromDb() { }
        @Test void nonExistentUser_throwsException() { }
    }
}
```

### 反模式

| 反模式 | 推荐做法 | 原因 |
|-----|------|-----|
| `@Test public void test1()` | `@Test void shouldCalculateSum()` | 命名应具描述性 |
| 测试私有方法 | 通过公共 API 测试 | 实现细节不应直接测试 |
| 不加 @DisplayName | 始终添加显示名称 | 报告更清晰 |
| `assertEquals(true, x)` | `assertTrue(x)` | 可读性更好 |

## Maven 依赖

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.11.0</version>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-junit-jupiter</artifactId>
    <version>5.14.0</version>
    <scope>test</scope>
</dependency>
```

## 快速参考

| 任务 | 命令 |
|------|---------|
| 运行全部 | `mvn test` or `./gradlew test` |
| 运行单个类 | `mvn test -Dtest=UserServiceTest` |
| 运行单个方法 | `mvn test -Dtest=UserServiceTest#createUser_succeeds` |
| 运行标签筛选 | `@Tag("slow")` + `mvn test -Dgroups="slow"` |
| 禁用测试 | `@Disabled("Reason")` |
| 条件执行 | `@EnabledOnOs(OS.LINUX)` |
| 超时控制 | `@Timeout(value = 5, unit = TimeUnit.SECONDS)` |
| 重复测试 | `@RepeatedTest(5)` |
| 执行顺序 | `@TestMethodOrder(MethodOrderer.OrderAnnotation.class)` |

## 深度模式

生产级模式详见 `reference/playbook.md`：

| 章节 | 内容 |
|---------|--------------|
| §1 项目设置 | Maven 依赖、并行配置、surefire |
| §2 测试生命周期 | BeforeAll/Each、排序、标签 |
| §3 参数化 | CsvSource、MethodSource、EnumSource、ValueSource |
| §4 Mockito | @Mock/@InjectMocks、captor、验证顺序 |
| §5 嵌套与动态 | @Nested 分组、@TestFactory |
| §6 AssertJ | 流式断言、提取、集合检查 |
| §7 条件执行 | @EnabledOnOs、假设、@EnabledIf |
| §8 自定义扩展 | 计时、重试、BeforeTestExecution |
| §9 CI/CD | GitHub Actions 与测试报告 |
| §10 调试表 | 8 个常见问题及修复方案 |
| §11 最佳实践 | 12 条生产检查清单 |

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用变更前，验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例替代环境特定的测试、安全审查或用户对破坏性/高成本操作的审批。
