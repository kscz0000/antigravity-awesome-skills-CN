# 使用 Trackio 记录指标

**Trackio** 是 Hugging Face 出品的轻量级免费实验追踪库。提供与 wandb 兼容的 API，采用本地优先设计记录指标。

- **GitHub**: [gradio-app/trackio](https://github.com/gradio-app/trackio)
- **文档**: [huggingface.co/docs/trackio](https://huggingface.co/docs/trackio/index)

## 安装

```bash
pip install trackio
# or
uv pip install trackio
```

## 核心 API

### 基本用法

```python
import trackio

# Initialize a run
trackio.init(
    project="my-project",
    config={"learning_rate": 0.001, "epochs": 10}
)

# Log metrics during training
for epoch in range(10):
    loss = train_epoch()
    trackio.log({"loss": loss, "epoch": epoch})

# Finalize the run
trackio.finish()
```

### 关键函数

| 函数 | 用途 |
|------|------|
| `trackio.init(...)` | 启动新的追踪运行 |
| `trackio.log(dict)` | 记录指标（训练中反复调用） |
| `trackio.finish()` | 结束运行，确保所有指标已保存 |
| `trackio.show()` | 启动本地仪表盘 |
| `trackio.sync(...)` | 将本地项目同步到 HF Space |

## trackio.init() 参数

```python
trackio.init(
    project="my-project",           # Project name (groups runs together)
    name="run-name",                # Optional: name for this specific run
    config={...},                   # Hyperparameters and config to log
    space_id="username/trackio",    # Optional: sync to HF Space for remote dashboard
    group="experiment-group",       # Optional: group related runs
)
```

## 本地与远程仪表盘

### 本地（默认）

默认情况下，trackio 将指标存储在本地 SQLite 数据库中，并在本地运行仪表盘：

```python
trackio.init(project="my-project")
# ... training ...
trackio.finish()

# Launch local dashboard
trackio.show()
```

或从终端启动：
```bash
trackio show --project my-project
```

### 远程（HF Space）

传入 `space_id` 将指标同步到 Hugging Face Space，获得持久化、可分享的仪表盘：

```python
trackio.init(
    project="my-project",
    space_id="username/trackio"  # Auto-creates Space if it doesn't exist
)
```

⚠️ **远程训练**（云端 GPU、HF Jobs 等）：务必使用 `space_id`，因为实例终止后本地存储会丢失。

### 本地同步到远程

将已有本地项目同步到 Space：

```python
trackio.sync(project="my-project", space_id="username/my-experiments")
```

## wandb 兼容性

Trackio 的 API 与 wandb 兼容，可直接替换：

```python
import trackio as wandb

wandb.init(project="my-project")
wandb.log({"loss": 0.5})
wandb.finish()
```

## TRL 集成

使用 TRL 训练器时，设置 `report_to="trackio"` 即可自动记录指标：

```python
from trl import SFTConfig, SFTTrainer
import trackio

trackio.init(
    project="sft-training",
    space_id="username/trackio",
    config={"model": "Qwen/Qwen2.5-0.5B", "dataset": "trl-lib/Capybara"}
)

config = SFTConfig(
    output_dir="./output",
    report_to="trackio",  # Automatic metric logging
    # ... other config
)

trainer = SFTTrainer(model=model, args=config, ...)
trainer.train()
trackio.finish()
```

## 自动记录的内容

通过 TRL/Transformers 集成，trackio 自动捕获：
- 训练 loss
- 学习率
- 评估指标
- 训练吞吐量

手动记录时，可记录任意数值指标：

```python
trackio.log({
    "train_loss": 0.5,
    "train_accuracy": 0.85,
    "val_loss": 0.4,
    "val_accuracy": 0.88,
    "epoch": 1
})
```

## 运行分组

使用 `group` 在仪表盘侧边栏中组织相关实验：

```python
# Group by experiment type
trackio.init(project="my-project", name="baseline-v1", group="baseline")
trackio.init(project="my-project", name="augmented-v1", group="augmented")

# Group by hyperparameter
trackio.init(project="hyperparam-sweep", name="lr-0.001", group="lr_0.001")
trackio.init(project="hyperparam-sweep", name="lr-0.01", group="lr_0.01")
```

## 配置最佳实践

保持 config 精简——只记录对比较运行有用的内容：

```python
trackio.init(
    project="qwen-sft-capybara",
    name="baseline-lr2e5",
    config={
        "model": "Qwen/Qwen2.5-0.5B",
        "dataset": "trl-lib/Capybara",
        "learning_rate": 2e-5,
        "num_epochs": 3,
        "batch_size": 8,
    }
)
```

## 嵌入仪表盘

通过查询参数将 Space 仪表盘嵌入网页：

```html
<iframe 
  src="https://username-trackio.hf.space/?project=my-project&metrics=train_loss,val_loss&sidebar=hidden" 
  style="width:1600px; height:500px; border:0;">
</iframe>
```

查询参数：
- `project`：筛选指定项目
- `metrics`：逗号分隔的指标名称
- `sidebar`：`hidden` 或 `collapsed`
- `smoothing`：0-20（平滑滑块值）
- `xmin`、`xmax`：X 轴范围
