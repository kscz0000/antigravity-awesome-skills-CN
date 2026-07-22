---
adapter:
  language: rust
  display_name: "Rust"
  version: "1.0"

  detection:
    files: [Cargo.toml, Cargo.lock]
    content_patterns:
      - file: "Cargo.toml"
        pattern: '\\[package\\]'
    confidence: 0.95

  commands:
    build: "cargo build"
    test: "cargo test"
    lint: "cargo clippy -- -D warnings"
    lint_arch: null  # Rust 模块系统自然强制架构
    format: "cargo fmt"
    start: "cargo run"
    dev: "cargo watch -x run"

  package_manager:
    detection: []  # Cargo 内置
    default: "cargo"
    install_command: "cargo build"

  route_detection:
    server_indicators:
      - pattern: 'use actix_web|actix_web::'
        description: "Actix-web framework"
        frameworks: ["actix-web"]
      - pattern: 'use axum|axum::'
        description: "Axum web framework"
        frameworks: ["axum"]
      - pattern: 'use rocket|#\[rocket::main\]'
        description: "Rocket web framework"
        frameworks: ["rocket"]
      - pattern: 'use warp|warp::'
        description: "Warp web framework"
        frameworks: ["warp"]
      - pattern: 'use hyper|hyper::'
        description: "Hyper HTTP library"
        frameworks: ["hyper"]
      - pattern: 'use tide|tide::'
        description: "Tide web framework"
        frameworks: ["tide"]

    cli_indicators:
      - pattern: 'use clap|clap::'
        description: "Clap CLI framework"
        frameworks: ["clap"]
      - pattern: 'use structopt|structopt::'
        description: "StructOpt CLI (legacy clap)"
        frameworks: ["structopt"]
      - pattern: 'std::env::args'
        description: "Standard library args parsing"
        frameworks: ["stdlib"]

    frontend_indicators:
      - pattern: 'use leptos|leptos::'
        description: "Leptos WASM framework"
        frameworks: ["leptos"]
      - pattern: 'use yew|yew::'
        description: "Yew WASM framework"
        frameworks: ["yew"]
      - pattern: 'use dioxus|dioxus::'
        description: "Dioxus UI framework"
        frameworks: ["dioxus"]

    patterns:
      # Actix-web
      - type: route
        regex: '#\[(?:web::)?(get|post|put|delete|patch)\s*\(\s*"([^"]+)"'
        groups: [method, path]
        frameworks: ["actix-web"]
      # Axum
      - type: route
        regex: '\.(get|post|put|delete|patch)\s*\(\s*"([^"]+)"'
        groups: [method, path]
        frameworks: ["axum"]
      # Rocket
      - type: route
        regex: '#\[(get|post|put|delete|patch)\s*\(\s*"([^"]+)"'
        groups: [method, path]
        frameworks: ["rocket"]
      # Clap derive
      - type: command
        regex: '#\[command\s*\(.*name\s*=\s*"([^"]+)"'
        groups: [command_name]
        frameworks: ["clap"]
      # Clap builder
      - type: command
        regex: 'Command::new\s*\(\s*"([^"]+)"'
        groups: [command_name]
        frameworks: ["clap"]

  import_analysis:
    list_packages: "cargo metadata --format-version 1"
    import_pattern: "use\\s+([\\w:]+)"
    source_extensions: [".rs"]
    module_root_file: "Cargo.toml"

  layer_conventions:
    patterns:
      - layer: 0
        paths: ["src/models", "src/types", "src/domain"]
        description: "Domain types and models"
      - layer: 1
        paths: ["src/utils", "src/common", "src/lib.rs"]
        description: "Shared utilities"
      - layer: 2
        paths: ["src/services", "src/core", "src/repository"]
        description: "Business logic"
      - layer: 3
        paths: ["src/handlers", "src/routes", "src/api"]
        description: "HTTP/API handlers"
      - layer: 4
        paths: ["src/main.rs", "src/bin"]
        description: "Entry points"

  dependency_detection:
    manifest_file: "Cargo.toml"
    databases:
      - pattern: 'sqlx.*postgres|tokio-postgres|diesel.*postgres'
        type: "postgres"
        default_port: 5432
      - pattern: 'sqlx.*mysql|diesel.*mysql'
        type: "mysql"
        default_port: 3306
      - pattern: 'mongodb'
        type: "mongodb"
        default_port: 27017
      - pattern: 'redis|deadpool-redis'
        type: "redis"
        default_port: 6379
      - pattern: 'rusqlite|sqlx.*sqlite'
        type: "sqlite"
        default_port: 0
    services:
      - pattern: 'rdkafka|kafka'
        type: "kafka"
        default_port: 9092
      - pattern: 'lapin|amqp'
        type: "rabbitmq"
        default_port: 5672
      - pattern: 'elasticsearch'
        type: "elasticsearch"
        default_port: 9200
    env_var_patterns:
      - pattern: 'std::env::var\(\s*"([^"]+)"'
      - pattern: 'env::var\(\s*"([^"]+)"'
      - pattern: 'dotenv::var\(\s*"([^"]+)"'

  linter:
    template_section: "rust-linter"
    script_extension: ".rs"
    run_command: "cargo clippy"

  naming:
    file_pattern: "^[a-z][a-z0-9_]*\\.rs$"
    test_pattern: "^[a-z][a-z0-9_]*\\.rs$"  # Rust 中的测试是内联的
    directory_style: "snake_case"

  ci:
    github_actions:
      image: null
      setup_steps:
        - "uses: dtolnay/rust-toolchain@stable\n  with:\n    components: clippy, rustfmt"
      cache_paths: ["~/.cargo/registry", "~/.cargo/git", "target"]
---

# Rust 适配器

## 架构说明

Rust 的模块系统（`mod`、`pub`、`pub(crate)`）自然强制封装。
`lint_arch` 命令是 `null`，因为 Rust 的编译器已在编译时阻止许多
依赖违规。但是，自定义架构 linter 对于强制执行更高级的层级边界仍然有价值。

## 服务器启动命令推断

1. 现有的 `harness/config/environment.json` 启动命令（如果存在）
2. `Cargo.toml` 具有 `[[bin]]` 部分 → `cargo run --bin <name>`
3. 默认 → `cargo run`

对于发布构建：`cargo build --release && ./target/release/<name>`

## 框架特定说明

### Axum
- 基于路由器的：`Router::new().route("/path", get(handler))`
- 用于请求解析的提取器：`Json<T>`、`Path<T>`、`Query<T>`
- 通过 `Extension` 或 `State` 共享状态
- 默认：在 `0.0.0.0:3000` 上运行

### Actix-web
- 属性宏：`#[get("/path")]`、`#[post("/path")]`
- 应用工厂模式：`App::new().service(handler)`
- 默认：`HttpServer::new(...).bind("127.0.0.1:8080")`

### Rocket
- 属性宏：`#[get("/path")]`、`#[post("/path")]`
- 用于中间件的 Fairings
- 通过 `Rocket.toml` 配置

## 测试模式

- 单元测试：同一文件中的内联 `#[cfg(test)] mod tests { ... }`
- 集成测试：crate 根目录下的 `tests/` 目录
- `cargo test` 运行两者
- 有用的标志：`cargo test -- --nocapture`（显示 println 输出）

## Workspace 支持

如果根 `Cargo.toml` 中有 `[workspace]`：
- 每个成员 crate 可以有自己的层级约定
- 构建：`cargo build --workspace`
- 测试：`cargo test --workspace`