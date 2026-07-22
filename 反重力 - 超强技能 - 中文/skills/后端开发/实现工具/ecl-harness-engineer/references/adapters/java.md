---
adapter:
  language: java
  display_name: "Java / Kotlin"
  version: "1.0"

  detection:
    files: [pom.xml, build.gradle, build.gradle.kts, settings.gradle, settings.gradle.kts]
    content_patterns:
      - file: "pom.xml"
        pattern: "<groupId>"
      - file: "build.gradle.kts"
        pattern: "plugins|dependencies"
    confidence: 0.90

  commands:
    build: null   # 从构建工具检测
    test: null    # 从构建工具检测
    lint: null    # 经常是 spotbugs、checkstyle 或 ktlint
    lint_arch: null
    format: null
    start: null
    dev: null

  package_manager:
    detection:
      - lockfile: "pom.xml"
        manager: "maven"
      - lockfile: "build.gradle"
        manager: "gradle"
      - lockfile: "build.gradle.kts"
        manager: "gradle"
    default: "maven"
    install_command: null  # 依赖在构建过程中解析

  route_detection:
    server_indicators:
      - pattern: '@RestController|@Controller|@RequestMapping'
        description: "Spring MVC/Boot controller"
        frameworks: ["spring"]
      - pattern: 'import io\.micronaut'
        description: "Micronaut framework"
        frameworks: ["micronaut"]
      - pattern: 'import io\.quarkus'
        description: "Quarkus framework"
        frameworks: ["quarkus"]
      - pattern: 'import io\.vertx'
        description: "Vert.x framework"
        frameworks: ["vertx"]
      - pattern: 'import io\.ktor'
        description: "Ktor framework (Kotlin)"
        frameworks: ["ktor"]
      - pattern: 'import io\.javalin'
        description: "Javalin web framework"
        frameworks: ["javalin"]

    cli_indicators:
      - pattern: 'import picocli|@CommandLine'
        description: "picocli CLI framework"
        frameworks: ["picocli"]
      - pattern: 'public static void main\(String'
        description: "Java main method (potential CLI)"
        frameworks: ["stdlib"]

    frontend_indicators: []

    patterns:
      # Spring MVC annotations
      - type: route
        regex: '@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping)\s*\(\s*(?:value\s*=\s*)?["\x27]([^"\x27]*)["\x27]'
        groups: [method, path]
        frameworks: ["spring"]
      # Spring RequestMapping
      - type: route
        regex: '@RequestMapping\s*\(.*(?:value|path)\s*=\s*["\x27]([^"\x27]+)["\x27].*method\s*=\s*RequestMethod\.(\w+)'
        groups: [path, method]
        frameworks: ["spring"]
      # Ktor (Kotlin)
      - type: route
        regex: '(get|post|put|delete|patch)\s*\(\s*["\x27]([^"\x27]+)["\x27]'
        groups: [method, path]
        frameworks: ["ktor"]
      # Javalin
      - type: route
        regex: 'app\.(get|post|put|delete|patch)\s*\(\s*["\x27]([^"\x27]+)["\x27]'
        groups: [method, path]
        frameworks: ["javalin"]

  import_analysis:
    list_packages: null
    import_pattern: "^import\\s+([\\w.]+)"
    source_extensions: [".java", ".kt"]
    module_root_file: "pom.xml"

  layer_conventions:
    patterns:
      - layer: 0
        paths: ["src/main/java/**/model", "src/main/java/**/entity", "src/main/java/**/dto"]
        description: "Domain models, entities, DTOs"
      - layer: 1
        paths: ["src/main/java/**/util", "src/main/java/**/common", "src/main/java/**/config"]
        description: "Utilities and configuration"
      - layer: 2
        paths: ["src/main/java/**/service", "src/main/java/**/repository", "src/main/java/**/dao"]
        description: "Service and data access layer"
      - layer: 3
        paths: ["src/main/java/**/controller", "src/main/java/**/api", "src/main/java/**/resource"]
        description: "REST controllers, API endpoints"
      - layer: 4
        paths: ["src/main/java/**/Application.java", "src/main/java/**/Main.java"]
        description: "Application entry point"

  dependency_detection:
    manifest_file: "pom.xml"
    databases:
      - pattern: "postgresql|postgres"
        type: "postgres"
        default_port: 5432
      - pattern: "mysql-connector"
        type: "mysql"
        default_port: 3306
      - pattern: "mongodb-driver|mongo-java-driver"
        type: "mongodb"
        default_port: 27017
      - pattern: "jedis|lettuce-core|spring-data-redis"
        type: "redis"
        default_port: 6379
      - pattern: "h2|sqlite-jdbc"
        type: "sqlite"
        default_port: 0
    services:
      - pattern: "kafka-clients|spring-kafka"
        type: "kafka"
        default_port: 9092
      - pattern: "amqp-client|spring-amqp|spring-rabbit"
        type: "rabbitmq"
        default_port: 5672
      - pattern: "elasticsearch-rest-client|spring-data-elasticsearch"
        type: "elasticsearch"
        default_port: 9200
    env_var_patterns:
      - pattern: 'System\.getenv\(\s*["\x27]([^"\x27]+)["\x27]\)'
      - pattern: '\\$\\{([A-Z_][A-Z0-9_]*)\\}'

  linter:
    template_section: "java-linter"
    script_extension: ".java"
    run_command: null  # 通常集成到构建工具中（spotbugs、checkstyle）

  naming:
    file_pattern: "^[A-Z][a-zA-Z0-9]*\\.java$"
    test_pattern: "^[A-Z][a-zA-Z0-9]*Test\\.java$"
    directory_style: "lowercase"

  ci:
    github_actions:
      image: null  # 使用 setup-java action
      setup_steps:
        - "uses: actions/setup-java@v4\n  with:\n    distribution: 'temurin'\n    java-version: '21'"
      cache_paths: ["~/.m2/repository", "~/.gradle/caches"]
---

# Java / Kotlin 适配器

## 构建工具检测

| 文件 | 构建工具 | 构建命令 | 测试命令 |
|------|-----------|---------------|--------------|
| `pom.xml` | Maven | `mvn package -DskipTests` | `mvn test` |
| `build.gradle` | Gradle (Groovy) | `./gradlew build -x test` | `./gradlew test` |
| `build.gradle.kts` | Gradle (Kotlin DSL) | `./gradlew build -x test` | `./gradlew test` |

如果存在 `mvnw` 或 `gradlew` wrapper，则优先使用 wrapper 而不是系统安装的工具。

## 服务器启动命令推断

1. 现有的 `harness/config/environment.json` 启动命令（如果存在）
2. Spring Boot → `./gradlew bootRun` 或 `mvn spring-boot:run`
3. 存在 Fat JAR → `java -jar target/*.jar` 或 `java -jar build/libs/*.jar`
4. 使用 `@SpringBootApplication` 注解的主类 → 从 pom.xml/build.gradle 推断

## 框架特定说明

### Spring Boot
- 通过注解路由：`@GetMapping("/path")`、`@PostMapping("/path")`
- 控制器前缀：类上的 `@RequestMapping("/api/v1")`
- 自动配置：`application.properties` 或 `application.yml`
- 默认端口：8080（可通过 `server.port` 配置）
- Actuator 健康：`/actuator/health`

### Micronaut
- 与 Spring 类似的注解风格：`@Get("/path")`、`@Post("/path")`
- 编译时 DI（无反射）
- 默认端口：8080

### Ktor (Kotlin)
- 基于 DSL 的路由：`routing { get("/path") { ... } }`
- 通过 `application.conf` (HOCON) 或 `application.yaml` 配置

## 测试模式

- JUnit 5 是标准：`@Test`、`@ParameterizedTest`
- Kotlin：相同的 JUnit 5 + kotest 作为替代
- 集成测试通常使用 `@SpringBootTest` + Testcontainers
- 测试目录：`src/test/java/` 或 `src/test/kotlin/`