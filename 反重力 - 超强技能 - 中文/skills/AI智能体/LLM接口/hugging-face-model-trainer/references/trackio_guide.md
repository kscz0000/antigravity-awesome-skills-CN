# TRL 训练的 Trackio 集成

**Trackio** 是一个实验跟踪库，为 Hugging Face Jobs 基础设施上的远程训练提供实时指标可视化。

⚠️ **重要**：对于 Jobs 训练（远程云 GPU）：
- 训练在临时云运行器上进行（不是你的本地机器）
- Trackio 将指标同步到 Hugging Face Space 以进行实时监控
- 没有 Space，任务完成时指标将丢失
- Space 仪表盘永久保存你的训练指标

## 为 Jobs 设置 Trackio

**步骤 1：添加 trackio 依赖**
```python
# /// script
# dependencies = [
#     "trl>=0.12.0",
#     "trackio",  # 必需！
# ]
# ///
```

**步骤 2：创建 Trackio Space（一次性设置）**

**选项 A：让 Trackio 自动创建（推荐）**
向 `trackio.init()` 传递 `space_id`，如果 Space 不存在，Trackio 将自动创建。

**选项 B：手动创建**
- 通过 Hub UI 在 https://huggingface.co/new-space 创建 Space
- 选择 Gradio SDK
- 或使用命令：`hf repos create my-trackio-dashboard --type space --space-sdk gradio`

**步骤 3：使用 space_id 初始化 Trackio**
```python
import trackio

trackio.init(
    project="my-training",
    space_id="username/trackio",  # 对 Jobs 至关重要！将 'username' 替换为你的 HF 用户名
    config={
        "model": "Qwen/Qwen2.5-0.5B",
        "dataset": "trl-lib/Capybara",
        "learning_rate": 2e-5,
    }
)
```

**步骤 4：配置 TRL 使用 Trackio**
```python
SFTConfig(
    report_to="trackio",
    # ... 其他配置
)
```

**步骤 5：完成跟踪**
```python
trainer.train()
trackio.finish()  # 确保最终指标已同步
```

## Trackio 跟踪的内容

Trackio 自动记录：
- ✅ 训练损失
- ✅ 学习率
- ✅ GPU 利用率
- ✅ 内存使用
- ✅ 训练吞吐量
- ✅ 自定义指标

## 与 Jobs 的协作方式

1. **运行训练** → 指标记录到本地 SQLite 数据库
2. **每 5 分钟** → Trackio 将数据库同步到 HF Dataset（Parquet）
3. **Space 仪表盘** → 从 Dataset 读取，实时显示指标
4. **任务完成** → 最终同步确保所有指标持久化

## 默认配置模式

**除非用户另有要求，否则使用合理的 trackio 默认配置。**

### 推荐默认值

```python
import trackio

trackio.init(
    project="qwen-capybara-sft",
    name="baseline-run",             # 用户可识别的描述性名称
    space_id="username/trackio",     # 默认 space: {username}/trackio
    config={
        # 保持 config 最小 - 仅包含超参数和模型/数据集信息
        "model": "Qwen/Qwen2.5-0.5B",
        "dataset": "trl-lib/Capybara",
        "learning_rate": 2e-5,
        "num_epochs": 3,
    }
)
```

**关键原则：**
- **Space ID**：使用 `{username}/trackio`，"trackio" 作为默认 space 名称
- **运行命名**：除非另有说明，以用户可识别的方式命名运行
- **配置**：保持最小 - 除非要求，不要自动捕获任务元数据
- **分组**：可选 - 仅在用户要求组织相关实验时使用

## 分组运行（可选）

`group` 参数有助于在仪表盘侧边栏中组织相关运行。这在用户运行多个不同配置的实验但希望将它们一起比较时很有用：

```python
# 示例：按实验类型分组运行
trackio.init(project="my-project", run_name="baseline-run-1", group="baseline")
trackio.init(project="my-project", run_name="augmented-run-1", group="augmented")
trackio.init(project="my-project", run_name="tuned-run-1", group="tuned")
```

具有相同组名的运行可以在侧边栏中分组，从而更轻松地比较相关实验。你可以按任何配置参数分组：

```python
# 超参数扫描 - 按学习率分组
trackio.init(project="hyperparam-sweep", run_name="lr-0.001-run", group="lr_0.001")
trackio.init(project="hyperparam-sweep", run_name="lr-0.01-run", group="lr_0.01")
```

## Jobs 的环境变量

你可以使用环境变量配置 trackio，而非向 `trackio.init()` 传递参数。这对于跨多个任务管理配置很有用。



**`HF_TOKEN`**
创建 Space 和写入数据集所必需（通过 `secrets` 传递）：
```python
hf_jobs("uv", {
    "script": "...",
    "secrets": {
        "HF_TOKEN": "$HF_TOKEN"  # 启用 Space 创建和 Hub 推送
    }
})
```

### 使用环境变量的示例

```python
hf_jobs("uv", {
    "script": """
# 训练脚本 - trackio 配置来自环境
import trackio
from datetime import datetime

# 自动生成运行名称
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
run_name = f"sft_qwen25_{timestamp}"

# project 和 space_id 可以来自环境变量
trackio.init(run_name=run_name, group="SFT")

# ... 训练代码 ...
trackio.finish()
""",
    "flavor": "a10g-large",
    "timeout": "2h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

**何时使用环境变量：**
- 管理具有相同配置的多个任务
- 保持训练脚本跨项目可移植
- 将配置与代码分离

**何时使用直接参数：**
- 具有特定配置的单个任务
- 当代码中清晰度优先时
- 当每个任务有不同的 project/space 时

## 查看仪表盘

开始训练后：
1. 导航到 Space：`https://huggingface.co/spaces/username/trackio`
2. Gradio 仪表盘显示所有跟踪的实验
3. 按 project 过滤、比较运行、查看带平滑的图表

## 推荐

- **Trackio**：最适合长时间训练运行期间的实时监控
- **Weights & Biases**：最适合团队协作，需要账户
