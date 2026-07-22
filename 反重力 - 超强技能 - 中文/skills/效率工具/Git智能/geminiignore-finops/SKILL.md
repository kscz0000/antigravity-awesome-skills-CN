---
name: geminiignore-finops
description: "为 AI 上下文窗口效率和 token 成本降低（FinOps）配置与优化 .geminiignore 文件。触发词：geminiignore、FinOps、上下文优化、token 节省、忽略文件配置。"
category: context-optimization
risk: safe
source: community
source_repo: iradoweck/antigravity-awesome-skills
source_type: community
date_added: "2026-05-25"
author: iradoweck
tags: [finops, context-management, token-optimization, geminiignore]
tools: [gemini, claude, cursor]
license: "MIT"
license_source: "https://github.com/iradoweck/antigravity-awesome-skills/blob/main/LICENSE"
---

# GeminiIgnore FinOps 设置与优化

## 概述

本技能用于在不同技术栈下构建、优化并维护高性能的 `.geminiignore` 文件。通过过滤掉机器生成的代码、庞大的日志文件、包锁文件以及二进制资源，本技能可优化 AI 智能体的上下文窗口、提升处理速度，并降低 token 消耗成本（FinOps）。

## 何时使用本技能

- 在为新的代码仓库或工作空间初始化与 AI 智能体进行结对编程时使用。
- 当 AI 上下文窗口接近容量上限，或计费优化（FinOps）是优先事项时使用。
- 当 AI 智能体意外读取了构建产物、锁文件、数据库或二进制媒体文件时使用。

## 工作原理

### 步骤 1：分析工作空间的技术栈

检测项目中使用的语言、框架和依赖管理器（例如 Node.js、Python、PHP、Dart/Flutter、Rust）。

### 步骤 2：初始化或更新 `.geminiignore` 文件

在当前工作空间根目录创建 `.geminiignore` 文件。如果已存在，则审查现有内容，补充缺失的规则类别。

### 步骤 3：实施 7 条核心规则

按以下类别添加规则，在过滤掉不必要机器噪音的同时，保留人类编写的代码可见：

1. **系统与编辑器噪音**：屏蔽操作系统临时文件（`.DS_Store`、`Thumbs.db`）以及用户专属的 IDE 缓存（`.idea/`、`.vscode/*`、Xcode 用户数据）。
2. **依赖目录与锁文件**：忽略第三方包目录（`node_modules/`、`vendor/`）以及巨大的机器生成锁文件（`package-lock.json`、`yarn.lock`、`Cargo.lock`、`composer.lock`）。
3. **构建与目标产物**：屏蔽编译产物目录（`dist/`、`build/`、`.next/`、`.nuxt/`）。
4. **缓存与工具元数据**：屏蔽编译器缓存（`.tsbuildinfo`、`.vite/`、`.pytest_cache/`、`.eslintcache`）。
5. **二进制与富媒体资源**：屏蔽媒体类型（`*.png`、`*.pdf`、`*.mp4`、`*.woff2`），以避免触发高成本的视觉/多模态 token。
6. **本地数据库与日志**：屏蔽日志文件（`*.log`）以及 SQL 转储文件或本地 SQLite 数据库（`*.sqlite`、`*.db`）。
7. **编译产物与移动端构建**：屏蔽移动端安装包文件（`*.apk`、`*.ipa`）以及编译后的二进制文件（`*.class`、`*.pyc`、`*.dll`）。

### 步骤 4：校验排除规则

确认 AI 仍可看到关键配置蓝图（例如 `.env.example`、`package.json`、`composer.json`、`pyproject.toml`），但会忽略真实的 `.env` 文件以及编译产物。

## 示例

### 示例 1：通用标准 `.geminiignore` 模板

以下是面向多语言项目的推荐基线配置：

```ini
# ==============================================================================
# .geminiignore - BASELINE DE FINOPS E ARQUITETURA
# ==============================================================================

# 1. SISTEMA OPERACIONAL E IDEs
.DS_Store
Thumbs.db
Desktop.ini
$RECYCLE.BIN/
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
.idea/
*.iml
.gradle/
local.properties
.history/

# 2. DEPENDÊNCIAS (ECONOMIA DE TOKENS EM LOCK FILES)
node_modules/
package-lock.json
yarn.lock
pnpm-lock.yaml
vendor/
composer.lock
venv/
.venv/
env/
.env
.env.*
!.env.example
poetry.lock
Cargo.lock
pubspec.lock

# 3. BUILDS E EXPORTAÇÕES
dist/
build/
out/
target/
.next/
.nuxt/
.output/
bin/
obj/

# 4. CACHES DE FRAMEWORKS
.vite/
.parcel-cache/
.eslintcache
.babel-cache/
.tsbuildinfo
.turbo/
.pytest_cache/
.ruff_cache/
storage/framework/
storage/logs/

# 5. ASSETS BINÁRIOS E MULTIMÍDIA EXTREMOS
*.png
*.jpg
*.jpeg
*.gif
*.webp
*.svg
*.ico
*.psd
*.fig
*.pdf
*.zip
*.tar.gz
*.woff
*.woff2
*.ttf

# 6. BANCOS DE DADOS E LOGS
*.log
*.db
*.sqlite
*.sqlite3
*.sql
*.sql.gz

# 7. ARQUIVOS COMPILADOS
*.apk
*.aab
*.ipa
*.jar
*.class
*.pyc
__pycache__/
*.so
*.dylib
*.dll
*.exe
*.js.map
*.css.map
```

## 最佳实践

- ✅ **忽略依赖锁文件**：标准锁文件（如 `package-lock.json`、`yarn.lock`）包含数千行冗余的包解析树，忽略它们是单一最大的 FinOps 收益。
- ✅ **保持配置文件可见**：确保 `package.json`、`composer.json`、`Cargo.toml`、`pyproject.toml` 等清单文件**绝不**被忽略，因为 AI 需要它们来理解依赖关系。
- ✅ **白名单示例配置**：在 `.env` 忽略规则之外，配套使用 `!.env.example` 之类的规则，让 AI 理解配置结构而不会泄露凭据。
- ❌ **不要忽略源代码**：避免过于宽泛的目录模式（如 `lib/` 或 `app/`），如果其中包含主要源码。请保持精确（例如屏蔽 `vendor/bundle/`，而非屏蔽你自己的代码）。

## 局限性

- `.geminiignore` 文件仅影响解析工作空间的 AI 工具，不能替代 Git 仓库管理中的 `.gitignore`。
- 模式必须按 gitignore 风格的 glob 格式正确编写，避免意外忽略源文件。

## 相关技能

- `@context-optimization` — 上下文窗口管理的整体策略。
- `@clean-code` — 面向整洁、可读代码库的架构实践。