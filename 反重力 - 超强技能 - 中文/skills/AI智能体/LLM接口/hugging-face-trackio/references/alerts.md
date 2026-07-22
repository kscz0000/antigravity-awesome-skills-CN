# Trackio 告警

告警让你直接从代码中标记重要的训练事件。它是 LLM Agent 诊断运行状态、自主迭代 ML 实验的主要机制。

告警会打印到终端、存入数据库、显示在仪表盘，还可发送到 webhook（Slack/Discord）。

## 核心 API

### trackio.alert()

```python
trackio.alert(
    title="Loss divergence",                    # Short title (required)
    text="Loss 5.2 still high after 200 steps", # Detailed description (optional)
    level=trackio.AlertLevel.WARN,               # INFO, WARN, or ERROR (default: WARN)
    webhook_url="https://hooks.slack.com/...",   # Per-alert webhook override (optional)
)
```

### 告警级别

| 级别 | 用途 |
|------|------|
| `trackio.AlertLevel.INFO` | 信息性里程碑（检查点已保存、评估完成） |
| `trackio.AlertLevel.WARN` | 潜在问题（loss 停滞、准确率偏低、梯度范数过大） |
| `trackio.AlertLevel.ERROR` | 严重故障（NaN loss、发散、OOM） |

### Webhook 支持

通过 `trackio.init()` 或 `TRACKIO_WEBHOOK_URL` 环境变量设置全局 webhook URL。告警会自动格式化为 Slack 和 Discord 格式。

```python
trackio.init(
    project="my-project",
    webhook_url="https://hooks.slack.com/services/...",
    webhook_min_level=trackio.AlertLevel.WARN,  # Only send WARN+ to webhook
)
```

单条告警覆盖：

```python
trackio.alert(
    title="Critical failure",
    level=trackio.AlertLevel.ERROR,
    webhook_url="https://hooks.slack.com/services/...",  # Overrides global URL
)
```

环境变量：
- `TRACKIO_WEBHOOK_URL` — 全局 webhook URL
- `TRACKIO_WEBHOOK_MIN_LEVEL` — webhook 发送的最低级别（`info`、`warn`、`error`）

## 查询告警（CLI）

```bash
# List all alerts for a project
trackio list alerts --project my-project --json

# Filter by run or level
trackio list alerts --project my-project --run my-run --level error --json

# Poll for new alerts since a timestamp (efficient for agents)
trackio list alerts --project my-project --json --since "2025-06-01T12:00:00"
```

### JSON 输出结构

```json
{
  "project": "my-project",
  "run": null,
  "level": null,
  "since": "2025-06-01T12:00:00",
  "alerts": [
    {
      "run": "run-name",
      "title": "Loss divergence",
      "text": "Loss 5.2 still high after 200 steps",
      "level": "warn",
      "step": 200,
      "timestamp": "2025-06-01T12:05:30"
    }
  ]
}
```

## 自主 Agent 工作流

LLM Agent 运行 ML 实验的推荐模式：

### 1. 在训练代码中插入告警

添加诊断性的 `trackio.alert()` 调用，用于 Agent 需要响应的条件：

```python
import trackio

trackio.init(project="hyperparam-sweep", config={"lr": lr, "batch_size": bs})

for step in range(num_steps):
    loss = train_step()
    trackio.log({"loss": loss, "step": step})

    if step > 200 and loss > 5.0:
        trackio.alert(
            title="Loss divergence",
            text=f"Loss {loss:.4f} still above 5.0 after {step} steps — learning rate may be too high",
            level=trackio.AlertLevel.ERROR,
        )

    if step > 500 and loss_delta < 0.001:
        trackio.alert(
            title="Training stall",
            text=f"Loss barely changed over last 100 steps (delta={loss_delta:.6f})",
            level=trackio.AlertLevel.WARN,
        )

    if math.isnan(loss):
        trackio.alert(
            title="NaN loss",
            text="Loss became NaN — training is broken",
            level=trackio.AlertLevel.ERROR,
        )
        break

trackio.finish()
```

### 2. 监控告警

告警触发时会自动打印到终端。如果 Agent 在监控训练脚本的输出（例如前台运行或跟踪日志），它能立即看到告警——无需轮询。

后台或分离运行时，通过 CLI 轮询告警：

```bash
# Poll for alerts (run periodically)
trackio list alerts --project hyperparam-sweep --json --since "2025-06-01T00:00:00"
```

### 3. 查看告警附近的指标

告警触发时，用 `trackio get snapshot` 查看该时刻的所有指标：

```bash
# Alert fired at step 200 — get all metrics in a ±5 step window
trackio get snapshot --project hyperparam-sweep --run run-1 --around 200 --window 5 --json

# Or inspect a single metric around the alert's timestamp
trackio get metric --project hyperparam-sweep --run run-1 --metric loss --around 200 --window 10 --json
```

### 4. 响应并迭代

根据告警类型采取行动：
- **ERROR 告警** → 停止运行、调整超参数、重新启动
- **WARN 告警** → 用 `trackio get snapshot ...` 检查指标，决定是否干预
- **INFO 告警** → 记录进度，继续监控

### 5. 跨运行比较

```bash
# Check metrics from previous runs
trackio get run --project hyperparam-sweep --run run-1 --json
trackio get metric --project hyperparam-sweep --run run-1 --metric loss --json

# Launch new run with adjusted config
python train.py --lr 5e-5
```

## 在 Transformers / TRL 中使用告警

使用 `report_to="trackio"` 时，你无法直接控制训练循环。用 `TrainerCallback` 来触发告警：

```python
from transformers import TrainerCallback

class AlertCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if "trackio" not in args.report_to:
            return
        if logs and "loss" in logs:
            if logs["loss"] > 5.0 and state.global_step > 100:
                trackio.alert(
                    title="High loss",
                    text=f"Loss {logs['loss']:.4f} at step {state.global_step}",
                    level=trackio.AlertLevel.ERROR,
                )

trainer = SFTTrainer(
    model=model,
    args=SFTConfig(output_dir="./out", report_to="trackio"),
    callbacks=[AlertCallback()],
    ...
)
```
