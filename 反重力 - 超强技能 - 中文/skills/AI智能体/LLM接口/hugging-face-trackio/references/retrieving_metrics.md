# 使用 Trackio CLI 查询指标

`trackio` CLI 提供直接的终端访问，无需启动 MCP 服务器即可查询 Trackio 实验追踪数据。

## 命令速查

| 任务 | 命令 |
|------|------|
| 列出项目 | `trackio list projects` |
| 列出运行 | `trackio list runs --project <name>` |
| 列出指标 | `trackio list metrics --project <name> --run <name>` |
| 列出系统指标 | `trackio list system-metrics --project <name> --run <name>` |
| 列出告警 | `trackio list alerts --project <name> [--run <name>] [--level <level>] [--since <timestamp>]` |
| 获取项目摘要 | `trackio get project --project <name>` |
| 获取运行摘要 | `trackio get run --project <name> --run <name>` |
| 获取指标值 | `trackio get metric --project <name> --run <name> --metric <name>` |
| 获取指定步数的指标 | `trackio get metric ... --metric <name> --step <N>` |
| 获取步数附近的指标 | `trackio get metric ... --metric <name> --around <N> --window <W>` |
| 获取全部指标快照 | `trackio get snapshot --project <name> --run <name> --step <N>` |
| 获取系统指标 | `trackio get system-metric --project <name> --run <name>` |
| 启动仪表盘 | `trackio show [--project <name>]` |
| 同步到 Space | `trackio sync --project <name> --space-id <space_id>` |

## 核心命令

### 列表命令

```bash
trackio list projects                                    # List all projects
trackio list projects --json                            # JSON output

trackio list runs --project <name>                      # List runs in project
trackio list runs --project <name> --json               # JSON output

trackio list metrics --project <name> --run <name>      # List metrics for run
trackio list metrics --project <name> --run <name> --json

trackio list system-metrics --project <name> --run <name>  # List system metrics
trackio list system-metrics --project <name> --run <name> --json

trackio list alerts --project <name>                       # List alerts
trackio list alerts --project <name> --run <name> --json   # Filter by run
trackio list alerts --project <name> --level error --json  # Filter by level
trackio list alerts --project <name> --json --since <ts>   # Poll since timestamp
```

### 查询命令

```bash
trackio get project --project <name>                    # Project summary
trackio get project --project <name> --json             # JSON output

trackio get run --project <name> --run <name>           # Run summary
trackio get run --project <name> --run <name> --json

trackio get metric --project <name> --run <name> --metric <name>  # Metric values
trackio get metric --project <name> --run <name> --metric <name> --json
trackio get metric ... --metric <name> --step 200                 # At exact step
trackio get metric ... --metric <name> --around 200 --window 10   # ±10 steps
trackio get metric ... --metric <name> --at-time <ts> --window 60 # ±60 seconds

trackio get snapshot --project <name> --run <name> --step 200 --json       # All metrics at step
trackio get snapshot --project <name> --run <name> --around 200 --window 5 --json  # Window
trackio get snapshot --project <name> --run <name> --at-time <ts> --window 60 --json

trackio get system-metric --project <name> --run <name>           # All system metrics
trackio get system-metric --project <name> --run <name> --metric <name>  # Specific metric
trackio get system-metric --project <name> --run <name> --json
```

### 仪表盘命令

```bash
trackio show                                              # Launch dashboard
trackio show --project <name>                           # Load specific project
trackio show --theme <theme>                            # Custom theme
trackio show --mcp-server                                # Enable MCP server
trackio show --color-palette "#FF0000,#00FF00"         # Custom colors
```

### 同步命令

```bash
trackio sync --project <name> --space-id <space_id>     # Sync to HF Space
trackio sync --project <name> --space-id <space_id> --private  # Private space
trackio sync --project <name> --space-id <space_id> --force   # Overwrite
```

## 输出格式

所有 `list` 和 `get` 命令支持两种输出格式：

- **可读格式**（默认）：格式化文本，适合终端查看
- **JSON**（加 `--json` 标志）：结构化 JSON，适合程序化使用

## 常用模式

### 浏览项目和运行

```bash
# List all available projects
trackio list projects

# List runs in a project
trackio list runs --project my-project

# Get project overview
trackio get project --project my-project --json
```

### 查看运行详情

```bash
# Get run summary with all metrics
trackio get run --project my-project --run my-run --json

# List available metrics
trackio list metrics --project my-project --run my-run

# Get specific metric values
trackio get metric --project my-project --run my-run --metric loss --json
```

### 查询系统指标

```bash
# List system metrics (GPU, etc.)
trackio list system-metrics --project my-project --run my-run

# Get all system metric data
trackio get system-metric --project my-project --run my-run --json

# Get specific system metric
trackio get system-metric --project my-project --run my-run --metric gpu_utilization --json
```

### 自动化脚本

```bash
# Extract latest metric value
LATEST_LOSS=$(trackio get metric --project my-project --run my-run --metric loss --json | jq -r '.values[-1].value')

# Export run summary to file
trackio get run --project my-project --run my-run --json > run_summary.json

# Filter runs with jq
trackio list runs --project my-project --json | jq '.runs[] | select(startswith("train"))'
```

### LLM Agent 工作流

```bash
# 1. Discover available projects
trackio list projects --json

# 2. Explore project structure
trackio get project --project my-project --json

# 3. Inspect specific run
trackio get run --project my-project --run my-run --json

# 4. Query metric values
trackio get metric --project my-project --run my-run --metric accuracy --json

# 5. Poll for alerts (use --since for efficient incremental polling)
trackio list alerts --project my-project --json --since "2025-06-01T00:00:00"

# 6. When an alert fires at step N, get all metrics around that point
trackio get snapshot --project my-project --run my-run --around 200 --window 5 --json
```

## 错误处理

命令会验证输入并返回清晰的错误信息：

- 项目不存在：`Error: Project '<name>' not found.`
- 运行不存在：`Error: Run '<name>' not found in project '<project>'.`
- 指标不存在：`Error: Metric '<name>' not found in run '<run>' of project '<project>'.`

所有错误以非零退出码返回，输出到 stderr。

## 关键选项

- `--project`：项目名称（多数命令必需）
- `--run`：运行名称（运行相关命令必需）
- `--metric`：指标名称（指标相关命令必需）
- `--json`：输出 JSON 格式而非可读格式
- `--step`：精确步数筛选（用于 `get metric`、`get snapshot`）
- `--around`：窗口中心步数（用于 `get metric`、`get snapshot`）
- `--at-time`：窗口中心 ISO 时间戳（用于 `get metric`、`get snapshot`）
- `--window`：窗口大小：`--around` 为 ±步数，`--at-time` 为 ±秒数（默认：10）
- `--level`：告警级别筛选（`info`、`warn`、`error`）（用于 `list alerts`）
- `--since`：ISO 时间戳，筛选该时间之后的告警（用于 `list alerts`）
- `--theme`：仪表盘主题（用于 `show` 命令）
- `--mcp-server`：启用 MCP 服务器模式（用于 `show` 命令）
- `--color-palette`：逗号分隔的十六进制颜色（用于 `show` 命令）
- `--private`：创建私有 Space（用于 `sync` 命令）
- `--force`：覆盖已有数据库（用于 `sync` 命令）

## JSON 输出结构

### 列出项目
```json
{"projects": ["project1", "project2"]}
```

### 列出运行
```json
{"project": "my-project", "runs": ["run1", "run2"]}
```

### 项目摘要
```json
{
  "project": "my-project",
  "num_runs": 3,
  "runs": ["run1", "run2", "run3"],
  "last_activity": 100
}
```

### 运行摘要
```json
{
  "project": "my-project",
  "run": "my-run",
  "num_logs": 50,
  "metrics": ["loss", "accuracy"],
  "config": {"learning_rate": 0.001},
  "last_step": 49
}
```

### 指标值
```json
{
  "project": "my-project",
  "run": "my-run",
  "metric": "loss",
  "values": [
    {"step": 0, "timestamp": "2024-01-01T00:00:00", "value": 0.5},
    {"step": 1, "timestamp": "2024-01-01T00:01:00", "value": 0.4}
  ]
}
```

## 参考

- **完整 CLI 文档**：参见 [docs/source/cli_commands.md](docs/source/cli_commands.md)
- **API 与 MCP 服务器**：参见 [docs/source/api_mcp_server.md](docs/source/api_mcp_server.md)
