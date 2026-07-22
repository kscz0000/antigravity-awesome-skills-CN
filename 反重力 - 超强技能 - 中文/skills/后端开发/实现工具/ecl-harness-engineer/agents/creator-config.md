# 配置与环境创建智能体

你正在创建或更新 harness 配置和环境文件。

## 输入

你将收到：
- 环境分析（来自 `harness/.analysis/environment.json`）
- 架构数据（来自 `harness/.analysis/architecture.json`）
- 现有状态（来自 `harness/.analysis/audit.json`）
- 要创建/更新的文件差异列表

## 你创建/更新的文件

### harness/config/environment.json

运行时生态系统契约。描述应用程序运行所需的内容。

**必需字段**（功能验证取决于这些）：
- `runtime.dev_command` — 如何以开发模式启动服务器
- `runtime.build_command` — 如何构建项目
- `test_environment.env_vars` — 测试模式的环境变量
- `functional_scenarios[]` — 验证场景列表

```json
{
  "runtime": {
    "language": "go",
    "version": "1.22",
    "build_command": "go build ./...",
    "dev_command": "go run main.go server -c config/server.toml",
    "test_command": "go test ./...",
    "binary_path": "./qts"
  },
  "databases": [
    {
      "type": "postgresql",
      "env_vars": {"DATABASE_URL": "postgres://..."},
      "docker": {"image": "postgres:16", "port": 5432},
      "test_alternative": "SQLite in-memory"
    }
  ],
  "services": [
    {"type": "redis", "env_vars": {"REDIS_URL": "redis://localhost:6379"}}
  ],
  "secrets": [
    {"name": "JWT_SECRET", "description": "JWT signing key", "test_value": "test-secret-do-not-use-in-prod"}
  ],
  "test_environment": {
    "env_vars": {
      "GIN_MODE": "release",
      "ENV_TAG": "test",
      "LOG_LEVEL": "error"
    }
  },
  "functional_scenarios": [
    {
      "name": "health_check",
      "description": "Verify server starts and health endpoint responds correctly",
      "prerequisites": ["postgresql", "redis"],
      "steps": [
        "Start server with runtime.dev_command",
        "Wait for server to be ready (GET /healthz returns 200)",
        "Verify health response contains status: up"
      ],
      "expected_outcome": "Server is healthy and all dependencies connected"
    },
    {
      "name": "basic_crud_flow",
      "description": "Create, read, update, delete a resource via API",
      "prerequisites": ["postgresql"],
      "steps": [
        "POST /api/v1/resources with valid payload -> 201",
        "GET /api/v1/resources/:id -> 200 with matching data",
        "PUT /api/v1/resources/:id -> 200",
        "DELETE /api/v1/resources/:id -> 204"
      ],
      "expected_outcome": "CRUD operations work correctly"
    }
  ],
  "scripts": {
    "setup": "harness/scripts/setup-env.sh",
    "start": "harness/scripts/start-server.sh",
    "teardown": "harness/scripts/teardown-env.sh"
  }
}
```

遵循 `references/environment-detection-guide.md` 获取检测策略。

### harness/scripts/setup-env.sh

启动外部依赖（DB、Redis 等）：

```bash
#!/bin/bash
set -euo pipefail

# Start PostgreSQL
docker run -d --name harness-postgres \
  -p 127.0.0.1:5432:5432 \
  -e POSTGRES_PASSWORD=testpass \
  postgres:16

# Wait for ready
until docker exec harness-postgres pg_isready; do sleep 1; done

echo "✓ Environment ready"
```

如果 `docker-compose.yml` 已存在，则改为创建一个薄包装。

### harness/scripts/start-server.sh

使用测试环境启动应用程序：

```bash
#!/bin/bash
set -euo pipefail

export PORT=8081
export ENV=test
export DATABASE_URL="postgres://postgres:testpass@localhost:5432/testdb?sslmode=disable"

# Start server
go run cmd/api/main.go &
SERVER_PID=$!

# Wait for ready
for i in $(seq 1 30); do
  if curl -s http://localhost:$PORT/health > /dev/null 2>&1; then
    echo "✓ Server ready (PID: $SERVER_PID)"
    exit 0
  fi
  sleep 1
done

echo "✗ Server failed to start"
exit 1
```

### harness/scripts/teardown-env.sh

停止并清理：

```bash
#!/bin/bash
docker stop harness-postgres 2>/dev/null || true
docker rm harness-postgres 2>/dev/null || true
echo "✓ Cleaned up"
```

### Makefile 目标

确保这些目标存在：

```makefile
.PHONY: lint-arch lint-ecl lint-encoding verify-harness build test setup-env start-server teardown-env

lint-arch:
	./scripts/lint-deps
	./scripts/lint-quality

lint-ecl:
	{ecl_lint_command}

lint-encoding:
	{encoding_lint_command}

verify-harness: lint-ecl lint-encoding lint-arch

build:
	{appropriate build command}

test:
	{appropriate test command}

setup-env:
	./harness/scripts/setup-env.sh

start-server:
	./harness/scripts/start-server.sh

teardown-env:
	./harness/scripts/teardown-env.sh
```

### .github/workflows/ci.yml

运行 build、lint 和 test 的基础 CI：

```yaml
name: CI
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-{lang}@v5
        with:
          {lang}-version: '{version}'
      - run: make build
      - run: make lint-arch
      - run: make test
```

CI 默认必须严格。包括项目的正常业务闸门（`lint`、
`typecheck`、`test`、`build`，以及检测到的嵌套包构建）加上 harness 检查。
不要因为基线已经为红色而移除或跳过业务闸门；而是在最终交接中将其报告为
预先存在的项目债。仅当用户明确请求此权衡时，才生成分阶段或宽松的 CI。

对于 TypeScript/Node.js 项目，优先使用包管理器脚本和 Node 设置，而不是仅 Makefile 的
CI。使用 `references/adapters/typescript.md` 中的适配器来检测 npm/pnpm/yarn/bun 并生成
诸如 `npm run lint:harness`、`npm run lint:arch`、`npm run typecheck`、`npm test`、
`npm run build` 和检测到的嵌套包构建步骤之类的命令。

### Harness 目录结构

创建默认核心 harness 目录树：

```
harness/
├── config/
│   └── environment.json
├── changes/
│   ├── active/
│   ├── parking/
│   ├── archive/
│   └── INDEX.json
├── evolution/
│   ├── state.json
│   ├── results.tsv
│   └── proposals/
├── templates/
│   └── change/
│       ├── summary.md
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       └── reviews/
│           └── review.md
├── scripts/
│   ├── setup-env.sh
│   ├── start-server.sh
│   └── teardown-env.sh
```

初始化 `harness/evolution/state.json`：

```json
{
  "enabled": true,
  "threshold": 5,
  "window": 10,
  "last_evolved_archive_count": 0,
  "last_evolved_change_id": null,
  "last_score": null,
  "last_run_at": null,
  "pending": false
}
```

使用以下头部初始化 `harness/evolution/results.tsv`：

```tsv
timestamp	change_id	old_score	new_score	status	dimension	note	eval_mode
```

允许的状态值为 `keep`、`revert`、`rejected` 和 `noop`。允许的 eval 模式为
`independent_review`、`dry_run` 和 `full_test`。当没有独立审计/子智能体
可用时使用 `dry_run`；在该模式下不要自动应用 harness 差异。

默认情况下不要创建空的高级目录。

仅当确认的范围或用户请求明确要求该能力时，才创建可选的高级目录：

```
harness/
├── eval/          # Agent evaluation datasets and runner inputs
├── trace/         # Agent execution traces
├── state/         # Runtime state for external executors
├── checkpoints/   # Resumable execution checkpoints
├── memory/        # Long-term agent memory experiments
│   ├── episodes/
│   ├── knowledge/
│   └── procedures/
└── metrics/       # Execution, quality, and cost metrics
```

高级目录必须附带读/写协议和验证命令。如果没有定义协议，则将该能力排除在生成的 harness 之外。

## 脚本必须

- `chmod +x` — 可执行
- 自包含 — 除 Docker 外无外部依赖
- 幂等 — 安全运行多次
- 带错误处理 — `set -euo pipefail`

## ECL 变更管理脚本

从 `references/ecl-harness.md` 为所选命令界面创建 ECL 脚本。
PowerShell、Bash、Node 和 Python 是等效的 profiles，只要它们实现相同的命令
和不变量。如果项目拒绝 `.ps1`，则不要将 PowerShell 作为唯一的入口点。
对于使用 Bash 的 Windows 项目，记录 Git Bash、WSL、MSYS2 或 CI Linux shell 作为先决条件。
根据项目证据自动选择 profile；仅当证据冲突或无法推断受支持的命令界面时才询问用户。

- `scripts/harness-change.{ps1|sh|mjs|py}`：实现 `new`、`status`、`validate`、`park`、`resume`、`close`、`search`、`context` 和 `reindex`。
- `scripts/harness-evolve.{ps1|sh|mjs|py}`：为默认的自动演化阈值检查实现 `check`、`collect` 和 `mark-complete`。
- `scripts/lint-ecl.{ps1|sh|mjs|py}`：验证激活变更结构、`docs/STATUS.md` 存在性、`plan.md`、已完成的验证、待办任务一致性、规范澄清闸门、计划审查闸门、任务 id 格式以及生成的索引新鲜度。
- `scripts/lint-encoding.{ps1|sh|mjs|py}`：扫描源/文档中的乱码标记和 UTF-8 风险。

规则：
- `INDEX.json` 源自 `parking/*/summary.md` 和 `archive/*/summary.md`；智能体不得手动编辑它。
- `park`、`close`、`resume` 和 `reindex` 必须重建 `INDEX.json`。
- `close` 和 `reindex` 必须运行 `harness-evolve check`；演化脚本可以创建
  `harness/evolution/pending.md`，但不得重写 docs、脚本、STATUS 或变更文件。
- 钩子/CI 集成可以运行验证，但不得自动写入文档、更新 `docs/STATUS.md` 或移动变更。
- `harness-change context` 应该在存在时列出激活变更文件；如果没有激活变更
  存在，则在存在待演化时在 `docs/STATUS.md` 之前列出 `harness/evolution/pending.md`。它不得打印或加载所有归档文件。
- 自动演化是核心轻量级基础设施。除非用户明确请求那些高级能力，否则不得创建 `harness/eval`、
  `harness/trace`、`harness/state`、`harness/checkpoints`、`harness/memory` 或
  `harness/metrics`。
- 将 Makefile/package 脚本/CI 连接到所选入口点，例如
  `bash scripts/lint-ecl.sh` 用于 Bash 或 `{pkg_manager} run lint:harness` 用于 package 脚本。
- 如果选择了 PowerShell profile，请在记录或连接命令之前检测 `pwsh` 是否可用。
  如果 `pwsh` 不可用，请使用 `powershell -NoProfile -ExecutionPolicy Bypass`。
- 保持 PowerShell profile 脚本与 Windows PowerShell 5.1 兼容。避免像
  `TrimStart(".\")` 这样的歧义重载；使用类型化参数，例如 `[char[]]@(".", "\")`。
- 避免在 PowerShell 模板中使用非 ASCII 乱码标记字面量。使用 Unicode 码点或其他
  PowerShell 5.1 安全表示，以便脚本仍能在旧版 Windows 代码页上解析。

## 验证配置规则

`harness/config/environment.json` 是由 ecl-harness-engineer 创建的静态运行时契约。
不要创建 `harness/config/verify.json` 或 `harness/config/validate.json`；任务特定的
验证计划稍后由执行器/运行时从 `environment.json` 加上
激活变更上下文生成。