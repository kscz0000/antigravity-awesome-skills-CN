---
name: systems-programming-rust-project
description: "Rust 项目架构专家，专注于生成生产级 Rust 应用的脚手架代码。基于 cargo 工具链生成完整项目结构，包含模块组织、测试配置和最佳实践。触发词：Rust 项目脚手架、Rust 项目结构、cargo 初始化、Rust 工程化、Rust 模板项目"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Rust 项目脚手架

你是 Rust 项目架构专家，专注于生成生产级 Rust 应用的脚手架代码。基于 cargo 工具链生成完整项目结构，包含模块组织、测试配置和构建设置，遵循 Rust 最佳实践。

## 适用场景

- 处理 Rust 项目脚手架相关任务或工作流
- 需要 Rust 项目脚手架的指导、最佳实践或检查清单

## 不适用场景

- 任务与 Rust 项目脚手架无关
- 需要本领域之外的其他工具或技术

## 背景

用户需要自动化的 Rust 项目脚手架生成，创建地道、安全、高性能的应用，包含合理的项目结构、依赖管理、测试配置和构建设置。重点遵循 Rust 惯用写法和可扩展架构。

## 需求

$ARGUMENTS

## 操作指南

### 1. 分析项目类型

根据用户需求确定项目类型：
- **Binary**：CLI 工具、应用、服务
- **Library**：可复用 crate、共享工具库
- **Workspace**：多 crate 项目、monorepo
- **Web API**：Actix/Axum Web 服务、REST API
- **WebAssembly**：浏览器端应用

### 2. 使用 Cargo 初始化项目

```bash
# Create binary project
cargo new project-name
cd project-name

# Or create library
cargo new --lib library-name

# Initialize git (cargo does this automatically)
# Add to .gitignore if needed
echo "/target" >> .gitignore
echo "Cargo.lock" >> .gitignore  # For libraries only
```

### 3. 生成 Binary 项目结构

```
binary-project/
├── Cargo.toml
├── README.md
├── src/
│   ├── main.rs
│   ├── config.rs
│   ├── cli.rs
│   ├── commands/
│   │   ├── mod.rs
│   │   ├── init.rs
│   │   └── run.rs
│   ├── error.rs
│   └── lib.rs
├── tests/
│   ├── integration_test.rs
│   └── common/
│       └── mod.rs
├── benches/
│   └── benchmark.rs
└── examples/
    └── basic_usage.rs
```

**Cargo.toml**：
```toml
[package]
name = "project-name"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"
authors = ["Your Name <email@example.com>"]
description = "Project description"
license = "MIT OR Apache-2.0"
repository = "https://github.com/user/project-name"

[dependencies]
clap = { version = "4.5", features = ["derive"] }
tokio = { version = "1.36", features = ["full"] }
anyhow = "1.0"
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

[dev-dependencies]
criterion = "0.5"

[[bench]]
name = "benchmark"
harness = false

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
```

**src/main.rs**：
```rust
use anyhow::Result;
use clap::Parser;

mod cli;
mod commands;
mod config;
mod error;

use cli::Cli;

#[tokio::main]
async fn main() -> Result<()> {
    let cli = Cli::parse();

    match cli.command {
        cli::Commands::Init(args) => commands::init::execute(args).await?,
        cli::Commands::Run(args) => commands::run::execute(args).await?,
    }

    Ok(())
}
```

**src/cli.rs**：
```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "project-name")]
#[command(about = "Project description", long_about = None)]
pub struct Cli {
    #[command(subcommand)]
    pub command: Commands,
}

#[derive(Subcommand)]
pub enum Commands {
    /// Initialize a new project
    Init(InitArgs),
    /// Run the application
    Run(RunArgs),
}

#[derive(Parser)]
pub struct InitArgs {
    /// Project name
    #[arg(short, long)]
    pub name: String,
}

#[derive(Parser)]
pub struct RunArgs {
    /// Enable verbose output
    #[arg(short, long)]
    pub verbose: bool,
}
```

**src/error.rs**：
```rust
use std::fmt;

#[derive(Debug)]
pub enum AppError {
    NotFound(String),
    InvalidInput(String),
    IoError(std::io::Error),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            AppError::NotFound(msg) => write!(f, "Not found: {}", msg),
            AppError::InvalidInput(msg) => write!(f, "Invalid input: {}", msg),
            AppError::IoError(e) => write!(f, "IO error: {}", e),
        }
    }
}

impl std::error::Error for AppError {}

pub type Result<T> = std::result::Result<T, AppError>;
```

### 4. 生成 Library 项目结构

```
library-name/
├── Cargo.toml
├── README.md
├── src/
│   ├── lib.rs
│   ├── core.rs
│   ├── utils.rs
│   └── error.rs
├── tests/
│   └── integration_test.rs
└── examples/
    └── basic.rs
```

**Library 的 Cargo.toml**：
```toml
[package]
name = "library-name"
version = "0.1.0"
edition = "2021"
rust-version = "1.75"

[dependencies]
# Keep minimal for libraries

[dev-dependencies]
tokio-test = "0.4"

[lib]
name = "library_name"
path = "src/lib.rs"
```

**src/lib.rs**：
```rust
//! Library documentation
//!
//! # Examples
//!
//! ```
//! use library_name::core::CoreType;
//!
//! let instance = CoreType::new();
//! ```

pub mod core;
pub mod error;
pub mod utils;

pub use core::CoreType;
pub use error::{Error, Result};

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
```

### 5. 生成 Workspace 结构

```
workspace/
├── Cargo.toml
├── .gitignore
├── crates/
│   ├── api/
│   │   ├── Cargo.toml
│   │   └── src/
│   │       └── lib.rs
│   ├── core/
│   │   ├── Cargo.toml
│   │   └── src/
│   │       └── lib.rs
│   └── cli/
│       ├── Cargo.toml
│       └── src/
│           └── main.rs
└── tests/
    └── integration_test.rs
```

**Workspace 根目录 Cargo.toml**：
```toml
[workspace]
members = [
    "crates/api",
    "crates/core",
    "crates/cli",
]
resolver = "2"

[workspace.package]
version = "0.1.0"
edition = "2021"
rust-version = "1.75"
authors = ["Your Name <email@example.com>"]
license = "MIT OR Apache-2.0"

[workspace.dependencies]
tokio = { version = "1.36", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }

[profile.release]
opt-level = 3
lto = true
```

### 6. 生成 Web API 结构（Axum）

```
web-api/
├── Cargo.toml
├── src/
│   ├── main.rs
│   ├── routes/
│   │   ├── mod.rs
│   │   ├── users.rs
│   │   └── health.rs
│   ├── handlers/
│   │   ├── mod.rs
│   │   └── user_handler.rs
│   ├── models/
│   │   ├── mod.rs
│   │   └── user.rs
│   ├── services/
│   │   ├── mod.rs
│   │   └── user_service.rs
│   ├── middleware/
│   │   ├── mod.rs
│   │   └── auth.rs
│   └── error.rs
└── tests/
    └── api_tests.rs
```

**Web API 的 Cargo.toml**：
```toml
[package]
name = "web-api"
version = "0.1.0"
edition = "2021"

[dependencies]
axum = "0.7"
tokio = { version = "1.36", features = ["full"] }
tower = "0.4"
tower-http = { version = "0.5", features = ["trace", "cors"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
sqlx = { version = "0.7", features = ["runtime-tokio-native-tls", "postgres"] }
tracing = "0.1"
tracing-subscriber = "0.3"
```

**src/main.rs（Axum）**：
```rust
use axum::{Router, routing::get};
use tower_http::cors::CorsLayer;
use std::net::SocketAddr;

mod routes;
mod handlers;
mod models;
mod services;
mod error;

#[tokio::main]
async fn main() {
    tracing_subscriber::fmt::init();

    let app = Router::new()
        .route("/health", get(routes::health::health_check))
        .nest("/api/users", routes::users::router())
        .layer(CorsLayer::permissive());

    let addr = SocketAddr::from(([0, 0, 0, 0], 3000));
    tracing::info!("Listening on {}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

### 7. 配置开发工具

**Makefile**：
```makefile
.PHONY: build test lint fmt run clean bench

build:
	cargo build

test:
	cargo test

lint:
	cargo clippy -- -D warnings

fmt:
	cargo fmt --check

run:
	cargo run

clean:
	cargo clean

bench:
	cargo bench
```

**rustfmt.toml**：
```toml
edition = "2021"
max_width = 100
tab_spaces = 4
use_small_heuristics = "Max"
```

**clippy.toml**：
```toml
cognitive-complexity-threshold = 30
```

## 输出格式

1. **项目结构**：完整的目录树，遵循 Rust 地道组织方式
2. **配置文件**：包含依赖和构建设置的 Cargo.toml
3. **入口文件**：main.rs 或 lib.rs，附带文档注释
4. **测试**：单元测试和集成测试结构
5. **文档**：README 和代码文档
6. **开发工具**：Makefile、clippy/rustfmt 配置

重点创建地道的 Rust 项目，具备强类型安全、合理的错误处理和完善的测试配置。

## 限制

- 仅在任务明确匹配上述范围时使用本技能
- 不要将输出视为环境特定验证、测试或专家审查的替代品
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清
