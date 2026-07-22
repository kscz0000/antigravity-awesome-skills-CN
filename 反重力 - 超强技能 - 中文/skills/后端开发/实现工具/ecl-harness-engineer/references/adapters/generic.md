---
adapter:
  language: generic
  display_name: "Generic (Auto-Discovery)"
  version: "1.0"

  detection:
    files: []  # 始终作为回退匹配
    confidence: 0.10

  commands:
    build: null   # 从 Makefile / README 发现
    test: null    # 从 Makefile / README 发现
    lint: null
    lint_arch: null
    format: null
    start: null
    dev: null

  package_manager:
    detection: []
    default: null
    install_command: null

  route_detection:
    server_indicators:
      - pattern: 'listen|serve|http|server'
        description: "Generic HTTP server indicator"
        frameworks: []
    cli_indicators:
      - pattern: 'argv|args|argparse|getopt|flag'
        description: "Generic CLI argument parsing"
        frameworks: []
    frontend_indicators:
      - pattern: 'index\\.html|<!DOCTYPE html>'
        description: "HTML file presence"
        frameworks: []
    patterns: []

  import_analysis:
    list_packages: null
    import_pattern: null
    source_extensions: []
    module_root_file: null

  layer_conventions:
    patterns:
      - layer: 0
        paths: ["types", "models", "domain", "entities"]
        description: "Core types (generic convention)"
      - layer: 1
        paths: ["utils", "lib", "common", "helpers", "shared"]
        description: "Shared utilities (generic convention)"
      - layer: 2
        paths: ["services", "core", "business", "logic"]
        description: "Business logic (generic convention)"
      - layer: 3
        paths: ["handlers", "controllers", "api", "routes", "endpoints"]
        description: "API layer (generic convention)"
      - layer: 4
        paths: ["main", "cmd", "bin", "app", "src/index", "src/main"]
        description: "Entry points (generic convention)"

  dependency_detection:
    manifest_file: null
    databases: []
    services: []
    env_var_patterns: []

  linter:
    template_section: null
    script_extension: null
    run_command: null

  naming:
    file_pattern: null
    test_pattern: null
    directory_style: null

  ci:
    github_actions:
      image: "ubuntu-latest"
      setup_steps: []
      cache_paths: []
---

# 通用适配器（自动发现回退）

当没有语言特定适配器匹配时，此适配器激活。它不是
假设特定语言（之前的行为：默认为 Go），而是从项目约定中发现
命令。

## 发现策略

### 1. Makefile 发现

如果存在 `Makefile`，解析目标：

```bash
# 提取 make 目标
grep -E '^[a-zA-Z_-]+:' Makefile | sed 's/:.*//'
```

常见目标映射：
| 目标模式 | 映射命令 |
|---------------|---------------|
| `build`、`compile` | `commands.build` |
| `test`、`check` | `commands.test` |
| `lint`、`lint-arch` | `commands.lint`、`commands.lint_arch` |
| `fmt`、`format` | `commands.format` |
| `run`、`start`、`serve` | `commands.start` |
| `dev`、`watch` | `commands.dev` |

### 2. README 发现

如果没有 Makefile，扫描 `README.md` 中的常见命令代码块：

```bash
# 查找带有 build/test 命令的围栏代码块
grep -A 2 '```' README.md
```

### 3. package.json 脚本发现（非 Node 项目）

一些非 Node 项目使用 `package.json` 作为脚本别名：

```bash
# 检查 package.json 脚本是否存在
cat package.json | python3 -c "import sys,json; [print(k,v) for k,v in json.load(sys.stdin).get('scripts',{}).items()]"
```

### 4. docker-compose.yml 发现

如果存在 `docker-compose.yml`，则提取用于环境设置的服务定义。

## 何时通用适配器激活

通用适配器是**最后手段**。它仅在以下情况下激活：
1. 不存在 `go.mod`、`package.json`、`pyproject.toml`、`pom.xml`、`Cargo.toml`
2. 或当用户明确请求通用模式时

## 与语言特定适配器的行为差异

| 方面 | 语言适配器 | 通用适配器 |
|--------|-----------------|-----------------|
| Build 命令 | 硬编码默认值 | 从 Makefile/README 发现 |
| 路由检测 | 框架特定正则表达式 | 仅通用 HTTP 模式 |
| 层级约定 | 语言惯用路径 | 常见目录名称 |
| Linter | 语言特定模板 | 无（依赖现有工具） |
| CI 模板 | 语言特定镜像 | Ubuntu 与自定义步骤 |

## 扩展到新语言

如果你发现自己对特定语言反复使用通用适配器，
那是创建适当的语言适配器的信号。有关要遵循的 schema，请参阅 `adapter-schema.md`。