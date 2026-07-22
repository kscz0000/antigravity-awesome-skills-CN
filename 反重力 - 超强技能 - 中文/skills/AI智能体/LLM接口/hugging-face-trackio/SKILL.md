---
source: "https://github.com/huggingface/skills/tree/main/skills/huggingface-trackio"
name: hugging-face-trackio
description: 使用 Trackio 进行 ML 实验追踪，支持 Python 日志记录、告警和 CLI 指标查询。当用户要求'Trackio 实验追踪'、'ML 训练指标记录'、'训练告警'、'Trackio CLI 查询指标'时使用。
risk: unknown
---

# Trackio - ML 训练实验追踪

Trackio 是一个实验追踪库，用于记录和可视化 ML 训练指标。它同步到 Hugging Face Spaces，提供实时监控仪表盘。

## 三种接口

| 任务 | 接口 | 参考 |
|------|------|------|
| 训练中**记录指标** | Python API | [references/logging_metrics.md](references/logging_metrics.md) |
| 训练诊断**触发告警** | Python API | [references/alerts.md](references/alerts.md) |
| 训练中/后**查询指标与告警** | CLI | [references/retrieving_metrics.md](references/retrieving_metrics.md) |

## 各接口适用场景

### Python API → 记录指标

在训练脚本中使用 `import trackio` 记录指标：

- 用 `trackio.init()` 初始化追踪
- 用 `trackio.log()` 记录指标，或使用 TRL 的 `report_to="trackio"`
- 用 `trackio.finish()` 结束运行

**核心概念**：远程/云端训练时，传入 `space_id`——指标会同步到 Space 仪表盘，实例终止后数据依然保留。

→ 详见 [references/logging_metrics.md](references/logging_metrics.md)，包含初始化配置、TRL 集成和配置选项。

### Python API → 告警

在训练代码中插入 `trackio.alert()` 调用来标记重要事件——类似于插入 print 语句调试，但结构化且可查询：

- `trackio.alert(title="...", level=trackio.AlertLevel.WARN)` — 触发告警
- 三个严重级别：`INFO`、`WARN`、`ERROR`
- 告警会打印到终端、存入数据库、显示在仪表盘，还可发送到 webhook（Slack/Discord）

**LLM Agent 核心概念**：告警是自主实验迭代的主要机制。Agent 应在训练代码中插入告警来诊断异常情况（loss 飙升、NaN 梯度、准确率过低、训练停滞）。由于告警会打印到终端，监控训练脚本输出的 Agent 能自动看到它们。后台或分离运行时，Agent 可通过 CLI 轮询。

→ 详见 [references/alerts.md](references/alerts.md)，包含完整告警 API、webhook 配置和自主 Agent 工作流。

### CLI → 查询

使用 `trackio` 命令查询已记录的指标和告警：

- `trackio list projects/runs/metrics` — 浏览可用数据
- `trackio get project/run/metric` — 获取摘要和数值
- `trackio list alerts --project <name> --json` — 查询告警
- `trackio show` — 启动仪表盘
- `trackio sync` — 同步到 HF Space

**核心概念**：加 `--json` 获取结构化输出，适合自动化和 LLM Agent 使用。

→ 详见 [references/retrieving_metrics.md](references/retrieving_metrics.md)，包含全部命令、工作流和 JSON 输出格式。

## 最简记录配置

```python
import trackio

trackio.init(project="my-project", space_id="username/trackio")
trackio.log({"loss": 0.1, "accuracy": 0.9})
trackio.log({"loss": 0.09, "accuracy": 0.91})
trackio.finish()
```

### 最简查询

```bash
trackio list projects --json
trackio get metric --project my-project --run my-run --metric loss --json
```

## 自主 ML 实验工作流

以 LLM Agent 身份自主运行实验时，推荐工作流：

1. **设置训练并插入告警** — 在诊断条件处插入 `trackio.alert()` 调用
2. **启动训练** — 后台运行脚本
3. **轮询告警** — 使用 `trackio list alerts --project <name> --json --since <timestamp>` 检查新告警
4. **读取指标** — 使用 `trackio get metric ...` 查看具体数值
5. **迭代** — 根据告警和指标，停止运行、调整超参数、启动新运行

```python
import trackio

trackio.init(project="my-project", config={"lr": 1e-4})

for step in range(num_steps):
    loss = train_step()
    trackio.log({"loss": loss, "step": step})

    if step > 100 and loss > 5.0:
        trackio.alert(
            title="Loss divergence",
            text=f"Loss {loss:.4f} still high after {step} steps",
            level=trackio.AlertLevel.ERROR,
        )
    if step > 0 and abs(loss) < 1e-8:
        trackio.alert(
            title="Vanishing loss",
            text="Loss near zero — possible gradient collapse",
            level=trackio.AlertLevel.WARN,
        )

trackio.finish()
```

然后在另一个终端/进程中轮询：

```bash
trackio list alerts --project my-project --json --since "2025-01-01T00:00:00"
```

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不能替代环境验证、测试或专家审查。
- 缺少必要输入、权限、安全边界或成功标准时，停下来确认。
