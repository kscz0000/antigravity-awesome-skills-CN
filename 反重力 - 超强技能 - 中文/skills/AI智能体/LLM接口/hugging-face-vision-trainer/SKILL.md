---
source: "https://github.com/huggingface/skills/tree/main/skills/huggingface-vision-trainer"
name: hugging-face-vision-trainer
description: 在 Hugging Face Jobs 上训练或微调视觉模型，支持目标检测、图像分类和 SAM/SAM2 分割。当用户要求'训练视觉模型'、'微调目标检测模型'、'图像分类训练'、'SAM分割微调'、'在HF Jobs上训练'时使用。
risk: unknown
---

# Hugging Face Jobs 上的视觉模型训练

在托管云 GPU 上训练目标检测、图像分类和 SAM/SAM2 分割模型。无需本地 GPU 环境——训练结果自动保存到 Hugging Face Hub。

## 何时使用此技能

当用户需要以下操作时使用：
- 在云 GPU 或本地微调目标检测模型（D-FINE、RT-DETR v2、DETR、YOLOS）
- 在云 GPU 或本地微调图像分类模型（timm: MobileNetV3、MobileViT、ResNet、ViT/DINOv3 或任何 Transformers 分类器）
- 使用 bbox 或 point 提示微调 SAM 或 SAM2 模型进行分割/图像抠图
- 在自定义数据集上训练边界框检测器
- 在自定义数据集上训练图像分类器
- 使用提示在自定义掩码数据集上训练分割模型
- 在 Hugging Face Jobs 基础设施上运行视觉训练任务
- 确保训练后的视觉模型永久保存到 Hub

## 相关技能

- **`hugging-face-jobs`** — 通用 HF Jobs 基础设施：token 认证、硬件规格、超时管理、成本估算、密钥、环境变量、定时任务和结果持久化。**任何非训练相关的 Jobs 问题请参考此技能**（例如"密钥怎么用？"、"有哪些硬件？"、"如何传递 token？"）。
- **`hugging-face-model-trainer`** — 基于 TRL 的语言模型训练（SFT、DPO、GRPO）。文本/语言模型微调请使用该技能。

## 本地脚本执行

辅助脚本使用 PEP 723 内联依赖。用 `uv run` 运行：
```bash
uv run scripts/dataset_inspector.py --dataset username/dataset-name --split train
uv run scripts/estimate_cost.py --help
```

## 前置条件清单

启动任何训练任务前，请确认：

### 账户与认证
- 拥有 [Pro](https://hf.co/pro)、[Team](https://hf.co/enterprise) 或 [Enterprise](https://hf.co/enterprise) 计划的 Hugging Face 账户（Jobs 需要付费计划）
- 已认证登录：用 `hf_whoami()`（工具）或 `hf auth whoami`（终端）检查
- Token 具有**写入**权限
- **必须在 job secrets 中传递 token** — 语法见下方指令 #3（MCP 工具 vs Python API）

### 数据集要求 — 目标检测
- 数据集必须存在于 Hub
- 标注必须使用 `objects` 列，包含 `bbox`、`category`（可选 `area`）子字段
- Bbox 可以是 **xywh (COCO)** 或 **xyxy (Pascal VOC)** 格式 — 自动检测并转换
- 类别可以是**整数或字符串** — 字符串自动重映射为整数 ID
- `image_id` 列**可选** — 缺失时自动生成
- **务必在 GPU 训练前验证未知数据集**（见数据集验证章节）

### 数据集要求 — 图像分类
- 数据集必须存在于 Hub
- 必须有 **`image` 列**（PIL 图像）和 **`label` 列**（整数类 ID 或字符串）
- label 列可以是 `ClassLabel` 类型（带名称）或纯整数/字符串 — 字符串自动重映射
- 常见列名自动检测：`label`、`labels`、`class`、`fine_label`
- **务必在 GPU 训练前验证未知数据集**（见数据集验证章节）

### 数据集要求 — SAM/SAM2 分割
- 数据集必须存在于 Hub
- 必须有 **`image` 列**（PIL 图像）和 **`mask` 列**（二值真值分割掩码）
- 必须有**提示** — 以下任一：
  - **`prompt` 列**，包含 JSON 格式的 `{"bbox": [x0,y0,x1,y1]}` 或 `{"point": [x,y]}`
  - 或专用 **`bbox`** 列，包含 `[x0,y0,x1,y1]` 值
  - 或专用 **`point`** 列，包含 `[x,y]` 或 `[[x,y],...]` 值
- Bbox 应为 **xyxy** 格式（绝对像素坐标）
- 示例数据集：`merve/MicroMat-mini`（带 bbox 提示的图像抠图）
- **务必在 GPU 训练前验证未知数据集**（见数据集验证章节）

### 关键设置
- **超时时间必须超过预期训练时间** — 默认 30 分钟太短。推荐值见指令 #6。
- **必须启用 Hub 推送** — `push_to_hub=True`，`hub_model_id="username/model-name"`，token 放在 `secrets` 中

## 数据集验证

**在启动 GPU 训练前验证数据集格式，防止训练失败的首要原因：格式不匹配。**

**必须验证**未知/自定义数据集或任何之前未训练过的数据集。`cppe-5`（训练脚本默认数据集）**可跳过**。

### 运行检查器

**方式一：通过 HF Jobs（推荐 — 避免本地 SSL/依赖问题）：**
```python
hf_jobs("uv", {
    "script": "path/to/dataset_inspector.py",
    "script_args": ["--dataset", "username/dataset-name", "--split", "train"]
})
```

**方式二：本地运行：**
```bash
uv run scripts/dataset_inspector.py --dataset username/dataset-name --split train
```

**方式三：通过 `HfApi().run_uv_job()`（hf_jobs MCP 不可用时）：**
```python
from huggingface_hub import HfApi
api = HfApi()
api.run_uv_job(
    script="scripts/dataset_inspector.py",
    script_args=["--dataset", "username/dataset-name", "--split", "train"],
    flavor="cpu-basic",
    timeout=300,
)
```

### 读取结果

- **`✓ READY`** — 数据集兼容，可直接使用
- **`✗ NEEDS FORMATTING`** — 需要预处理（输出中会提供映射代码）

## 自动 Bbox 预处理

目标检测训练脚本（`scripts/object_detection_training.py`）自动处理 bbox 格式检测（xyxy→xywh 转换）、bbox 裁剪、`image_id` 生成、字符串类别→整数重映射和数据集截断。**无需手动预处理** — 只需确保数据集有 `objects.bbox` 和 `objects.category` 列。

## 训练工作流

复制此清单并跟踪进度：

```
训练进度：
- [ ] 步骤 1：验证前置条件（账户、token、数据集）
- [ ] 步骤 2：验证数据集格式（运行 dataset_inspector.py）
- [ ] 步骤 3：询问用户数据集大小和验证集划分
- [ ] 步骤 4：准备训练脚本（OD: scripts/object_detection_training.py, IC: scripts/image_classification_training.py, SAM: scripts/sam_segmentation_training.py）
- [ ] 步骤 5：本地保存脚本，提交任务，报告详情
```

**步骤 1：验证前置条件**

按照上方前置条件清单操作。

**步骤 2：验证数据集**

在消耗 GPU 时间前运行数据集检查器。见上方"数据集验证"章节。

**步骤 3：询问用户偏好**

始终使用 AskUserQuestion 工具，以选项格式呈现：

```python
AskUserQuestion({
    "questions": [
        {
            "question": "是否先用数据子集做快速测试？",
            "header": "数据集大小",
            "options": [
                {"label": "快速测试（10% 数据）", "description": "更快、更便宜（约30-60分钟，约$2-5），验证流程"},
                {"label": "完整数据集（推荐）", "description": "完整训练，获得最佳模型质量"}
            ],
            "multiSelect": false
        },
        {
            "question": "是否从训练数据中创建验证集划分？",
            "header": "划分数据",
            "options": [
                {"label": "是（推荐）", "description": "自动划分 15% 训练数据用于验证"},
                {"label": "否", "description": "使用数据集现有的验证集划分"}
            ],
            "multiSelect": false
        },
        {
            "question": "选择哪种 GPU 硬件？",
            "header": "硬件规格",
            "options": [
                {"label": "t4-small ($0.40/小时)", "description": "1x T4, 16 GB VRAM — 足够所有 100M 参数以下的 OD 模型"},
                {"label": "l4x1 ($0.80/小时)", "description": "1x L4, 24 GB VRAM — 更大图像或批量尺寸的余量"},
                {"label": "a10g-large ($1.50/小时)", "description": "1x A10G, 24 GB VRAM — 更快训练，更多 CPU/RAM"},
                {"label": "a100-large ($2.50/小时)", "description": "1x A100, 80 GB VRAM — 最快，适合超大数据集或图像尺寸"}
            ],
            "multiSelect": false
        }
    ]
})
```

**步骤 4：准备训练脚本**

目标检测使用 [scripts/object_detection_training.py](scripts/object_detection_training.py) 作为生产就绪模板。图像分类使用 [scripts/image_classification_training.py](scripts/image_classification_training.py)。SAM/SAM2 分割使用 [scripts/sam_segmentation_training.py](scripts/sam_segmentation_training.py)。所有脚本使用 `HfArgumentParser` — 所有配置通过 `script_args` 中的 CLI 参数传递，不通过编辑 Python 变量。timm 模型详情见 [references/timm_trainer.md](references/timm_trainer.md)。SAM2 训练详情见 [references/finetune_sam2_trainer.md](references/finetune_sam2_trainer.md)。

**步骤 5：保存脚本，提交任务，报告**

1. **本地保存脚本**到工作区根目录的 `submitted_jobs/`（不存在则创建），使用描述性名称如 `training_<dataset>_<YYYYMMDD_HHMMSS>.py`。告知用户路径。
2. **提交**使用 `hf_jobs` MCP 工具（首选）或 `HfApi().run_uv_job()` — 两种方法见指令 #1。所有配置通过 `script_args` 传递。
3. **报告**任务 ID（`.id` 属性）、监控 URL、Trackio 仪表盘（`https://huggingface.co/spaces/{username}/trackio`）、预计时间和估算成本。
4. **等待用户**请求状态检查 — 不要自动轮询。训练任务异步运行，可能需要数小时。

## 关键指令

这些规则防止常见故障。请严格遵守。

### 1. 任务提交：`hf_jobs` MCP 工具 vs Python API

**`hf_jobs()` 是 MCP 工具，不是 Python 函数。** 不要尝试从 `huggingface_hub` 导入它。作为工具调用：

```
hf_jobs("uv", {"script": training_script_content, "flavor": "a10g-large", "timeout": "4h", "secrets": {"HF_TOKEN": "$HF_TOKEN"}})
```

**如果 `hf_jobs` MCP 工具不可用**，直接使用 Python API：

```python
from huggingface_hub import HfApi, get_token
api = HfApi()
job_info = api.run_uv_job(
    script="path/to/training_script.py",  # 文件路径，不是内容
    script_args=["--dataset_name", "cppe-5", ...],
    flavor="a10g-large",
    timeout=14400,  # 秒（4小时）
    env={"PYTHONUNBUFFERED": "1"},
    secrets={"HF_TOKEN": get_token()},  # 必须用 get_token()，不是 "$HF_TOKEN"
)
print(f"Job ID: {job_info.id}")
```

**两种方法的关键差异：**

| | `hf_jobs` MCP 工具 | `HfApi().run_uv_job()` |
|---|---|---|
| `script` 参数 | Python 代码字符串或 URL（不是本地路径） | `.py` 文件路径（不是内容） |
| secrets 中的 token | `"$HF_TOKEN"`（自动替换） | `get_token()`（实际 token 值） |
| 超时格式 | 字符串（`"4h"`） | 秒（`14400`） |

**两种方法的共同规则：**
- 训练脚本必须包含 PEP 723 内联元数据和依赖
- 不要使用 `image` 或 `command` 参数（它们属于 `run_job()`，不属于 `run_uv_job()`）

### 2. 通过 job secrets 认证 + 显式 hub_token 注入

**Job 配置**必须在 secrets 中包含 token — 语法取决于提交方式（见上表）。

**训练脚本要求：** Transformers 的 `Trainer` 在 `push_to_hub=True` 时于 `__init__()` 中调用 `create_repo(token=self.args.hub_token)`。训练脚本必须在解析参数之后、创建 `Trainer` 之前将 `HF_TOKEN` 注入到 `training_args.hub_token`。模板 `scripts/object_detection_training.py` 已包含此逻辑：

```python
hf_token = os.environ.get("HF_TOKEN")
if training_args.push_to_hub and not training_args.hub_token:
    if hf_token:
        training_args.hub_token = hf_token
```

如果编写自定义脚本，必须在 `Trainer(...)` 调用前包含此 token 注入。

- 不要在自定义脚本中调用 `login()`，除非完全复制 `scripts/object_detection_training.py` 的模式
- 不要依赖隐式 token 解析（`hub_token=None`）— 在 Jobs 中不可靠
- 完整详情见 `hugging-face-jobs` 技能 → *Token 使用指南*

### 3. JobInfo 属性

使用 `.id` 访问任务标识符（不是 `.job_id` 或 `.name` — 这些属性不存在）：

```python
job_info = api.run_uv_job(...)  # 或 hf_jobs("uv", {...})
job_id = job_info.id  # 正确 — 返回字符串如 "687fb701029421ae5549d998"
```

### 4. 必需训练标志和 HfArgumentParser 布尔语法

`scripts/object_detection_training.py` 使用 `HfArgumentParser` — 所有配置通过 `script_args` 传递。布尔参数有两种语法：

- **`bool` 字段**（如 `push_to_hub`、`do_train`）：作为裸标志使用（`--push_to_hub`）或用 `--no_` 前缀取反（`--no_remove_unused_columns`）
- **`Optional[bool]` 字段**（如 `greater_is_better`）：必须传递显式值（`--greater_is_better True`）。裸 `--greater_is_better` 会导致 `error: expected one argument`

目标检测必需标志：

```
--no_remove_unused_columns          # 必须：保留 image 列用于 pixel_values
--no_eval_do_concat_batches         # 必须：图像有不同数量的目标框
--push_to_hub                       # 必须：环境是临时的
--hub_model_id username/model-name
--metric_for_best_model eval_map
--greater_is_better True            # 必须显式传 "True"（Optional[bool]）
--do_train
--do_eval
```

图像分类必需标志：

```
--no_remove_unused_columns          # 必须：保留 image 列用于 pixel_values
--push_to_hub                       # 必须：环境是临时的
--hub_model_id username/model-name
--metric_for_best_model eval_accuracy
--greater_is_better True            # 必须显式传 "True"（Optional[bool]）
--do_train
--do_eval
```

SAM/SAM2 分割必需标志：

```
--remove_unused_columns False       # 必须：保留 input_boxes/input_points
--push_to_hub                       # 必须：环境是临时的
--hub_model_id username/model-name
--do_train
--prompt_type bbox                  # 或 "point"
--dataloader_pin_memory False       # 必须：避免自定义 collator 的 pin_memory 问题
```

### 5. 超时管理

默认 30 分钟对目标检测来说太短。至少设置 2-4 小时。额外加 30% 缓冲用于模型加载、预处理和 Hub 推送。

| 场景 | 超时 |
|------|------|
| 快速测试（100-200 张图像，5-10 个 epoch） | 1h |
| 开发（500-1K 张图像，15-20 个 epoch） | 2-3h |
| 生产（1K-5K 张图像，30 个 epoch） | 4-6h |
| 大数据集（5K+ 张图像） | 6-12h |

### 6. Trackio 监控

Trackio 在目标检测训练脚本中**始终启用** — 自动调用 `trackio.init()` 和 `trackio.finish()`。无需传递 `--report_to trackio`。项目名取自 `--output_dir`，运行名取自 `--run_name`。图像分类需在 `TrainingArguments` 中传递 `--report_to trackio`。

仪表盘地址：`https://huggingface.co/spaces/{username}/trackio`

## 模型与硬件选择

### 推荐目标检测模型

| 模型 | 参数量 | 适用场景 |
|------|--------|----------|
| `ustc-community/dfine-small-coco` | 10.4M | 最佳起点 — 快速、便宜、SOTA 质量 |
| `PekingU/rtdetr_v2_r18vd` | 20.2M | 轻量级实时检测器 |
| `ustc-community/dfine-large-coco` | 31.4M | 更高精度，仍然高效 |
| `PekingU/rtdetr_v2_r50vd` | 43M | 强实时基线 |
| `ustc-community/dfine-xlarge-obj365` | 63.5M | 最佳精度（在 Objects365 上预训练） |
| `PekingU/rtdetr_v2_r101vd` | 76M | 最大 RT-DETR v2 变体 |

快速迭代用 `ustc-community/dfine-small-coco`。需要更好精度时换用 D-FINE Large 或 RT-DETR v2 R50。

### 推荐图像分类模型

所有 `timm/` 模型通过 `AutoModelForImageClassification`（加载为 `TimmWrapperForImageClassification`）开箱即用。详情见 [references/timm_trainer.md](references/timm_trainer.md)。

| 模型 | 参数量 | 适用场景 |
|------|--------|----------|
| `timm/mobilenetv3_small_100.lamb_in1k` | 2.5M | 超轻量 — 移动/边缘端，训练最快 |
| `timm/mobilevit_s.cvnets_in1k` | 5.6M | 移动端 transformer — 精度/速度平衡好 |
| `timm/resnet50.a1_in1k` | 25.6M | 强 CNN 基线 — 稳定可靠、研究充分 |
| `timm/vit_base_patch16_dinov3.lvd1689m` | 86.6M | 最佳精度 — DINOv3 自监督 ViT |

快速迭代用 `timm/mobilenetv3_small_100.lamb_in1k`。需要更好精度时换用 `timm/resnet50.a1_in1k` 或 `timm/vit_base_patch16_dinov3.lvd1689m`。

### 推荐 SAM/SAM2 分割模型

| 模型 | 参数量 | 适用场景 |
|------|--------|----------|
| `facebook/sam2.1-hiera-tiny` | 38.9M | 最快 SAM2 — 适合快速实验 |
| `facebook/sam2.1-hiera-small` | 46.0M | 最佳起点 — 质量/速度平衡好 |
| `facebook/sam2.1-hiera-base-plus` | 80.8M | 更高容量，适合复杂分割 |
| `facebook/sam2.1-hiera-large` | 224.4M | 最佳 SAM2 精度 — 需要更多 VRAM |
| `facebook/sam-vit-base` | 93.7M | 原版 SAM — ViT-B 骨干 |
| `facebook/sam-vit-large` | 312.3M | 原版 SAM — ViT-L 骨干 |
| `facebook/sam-vit-huge` | 641.1M | 原版 SAM — ViT-H，SAM v1 最佳精度 |

快速迭代用 `facebook/sam2.1-hiera-small`。SAM2 模型在相近质量下通常比 SAM v1 更高效。默认只训练 mask decoder（vision 和 prompt encoder 冻结）。

### 硬件推荐

所有推荐的 OD 和 IC 模型都在 100M 参数以下 — **`t4-small`（16 GB VRAM，$0.40/小时）足够运行所有模型。** 图像分类模型通常比目标检测模型更小更快 — `t4-small` 甚至能轻松处理 ViT-Base。SAM2 模型到 `hiera-base-plus` 为止，`t4-small` 足够（因为只训练 mask decoder）。`sam2.1-hiera-large` 或 SAM v1 模型请使用 `l4x1` 或 `a10g-large`。只有在大批量导致 OOM 时才升级 — 先减小批量再换硬件。常见升级路径：`t4-small` → `l4x1`（$0.80/小时，24 GB）→ `a10g-large`（$1.50/小时，24 GB）。

完整硬件规格列表：参考 `hugging-face-jobs` 技能。成本估算：运行 `scripts/estimate_cost.py`。

## 快速开始 — 目标检测

以下 `script_args` 对两种提交方式通用。关键差异见指令 #1。

```python
OD_SCRIPT_ARGS = [
    "--model_name_or_path", "ustc-community/dfine-small-coco",
    "--dataset_name", "cppe-5",
    "--image_square_size", "640",
    "--output_dir", "dfine_finetuned",
    "--num_train_epochs", "30",
    "--per_device_train_batch_size", "8",
    "--learning_rate", "5e-5",
    "--eval_strategy", "epoch",
    "--save_strategy", "epoch",
    "--save_total_limit", "2",
    "--load_best_model_at_end",
    "--metric_for_best_model", "eval_map",
    "--greater_is_better", "True",
    "--no_remove_unused_columns",
    "--no_eval_do_concat_batches",
    "--push_to_hub",
    "--hub_model_id", "username/model-name",
    "--do_train",
    "--do_eval",
]
```

```python
from huggingface_hub import HfApi, get_token
api = HfApi()
job_info = api.run_uv_job(
    script="scripts/object_detection_training.py",
    script_args=OD_SCRIPT_ARGS,
    flavor="t4-small",
    timeout=14400,
    env={"PYTHONUNBUFFERED": "1"},
    secrets={"HF_TOKEN": get_token()},
)
print(f"Job ID: {job_info.id}")
```

### 关键 OD `script_args`

- `--model_name_or_path` — 推荐：`"ustc-community/dfine-small-coco"`（见上方模型表）
- `--dataset_name` — Hub 数据集 ID
- `--image_square_size` — 480（快速迭代）或 800（更好精度）
- `--hub_model_id` — `"username/model-name"` 用于 Hub 持久化
- `--num_train_epochs` — 30 为典型收敛值
- `--train_val_split` — 验证集划分比例（默认 0.15），数据集缺少验证集时设置
- `--max_train_samples` — 截断训练集（适合快速测试，如 `"785"` 约为 7.8K 数据集的 10%）
- `--max_eval_samples` — 截断评估集

## 快速开始 — 图像分类

```python
IC_SCRIPT_ARGS = [
    "--model_name_or_path", "timm/mobilenetv3_small_100.lamb_in1k",
    "--dataset_name", "ethz/food101",
    "--output_dir", "food101_classifier",
    "--num_train_epochs", "5",
    "--per_device_train_batch_size", "32",
    "--per_device_eval_batch_size", "32",
    "--learning_rate", "5e-5",
    "--eval_strategy", "epoch",
    "--save_strategy", "epoch",
    "--save_total_limit", "2",
    "--load_best_model_at_end",
    "--metric_for_best_model", "eval_accuracy",
    "--greater_is_better", "True",
    "--no_remove_unused_columns",
    "--push_to_hub",
    "--hub_model_id", "username/food101-classifier",
    "--do_train",
    "--do_eval",
]
```

```python
from huggingface_hub import HfApi, get_token
api = HfApi()
job_info = api.run_uv_job(
    script="scripts/image_classification_training.py",
    script_args=IC_SCRIPT_ARGS,
    flavor="t4-small",
    timeout=7200,
    env={"PYTHONUNBUFFERED": "1"},
    secrets={"HF_TOKEN": get_token()},
)
print(f"Job ID: {job_info.id}")
```

### 关键 IC `script_args`

- `--model_name_or_path` — 任何 `timm/` 模型或 Transformers 分类模型（见上方模型表）
- `--dataset_name` — Hub 数据集 ID
- `--image_column_name` — 包含 PIL 图像的列（默认：`"image"`）
- `--label_column_name` — 包含类标签的列（默认：`"label"`）
- `--hub_model_id` — `"username/model-name"` 用于 Hub 持久化
- `--num_train_epochs` — 分类通常 3-5（比 OD 少）
- `--per_device_train_batch_size` — 16-64（分类模型比 OD 用更少内存）
- `--train_val_split` — 验证集划分比例（默认 0.15），数据集缺少验证集时设置
- `--max_train_samples` / `--max_eval_samples` — 快速测试时截断

## 快速开始 — SAM/SAM2 分割

```python
SAM_SCRIPT_ARGS = [
    "--model_name_or_path", "facebook/sam2.1-hiera-small",
    "--dataset_name", "merve/MicroMat-mini",
    "--prompt_type", "bbox",
    "--prompt_column_name", "prompt",
    "--output_dir", "sam2-finetuned",
    "--num_train_epochs", "30",
    "--per_device_train_batch_size", "4",
    "--learning_rate", "1e-5",
    "--logging_steps", "1",
    "--save_strategy", "epoch",
    "--save_total_limit", "2",
    "--remove_unused_columns", "False",
    "--dataloader_pin_memory", "False",
    "--push_to_hub",
    "--hub_model_id", "username/sam2-finetuned",
    "--do_train",
    "--report_to", "trackio",
]
```

```python
from huggingface_hub import HfApi, get_token
api = HfApi()
job_info = api.run_uv_job(
    script="scripts/sam_segmentation_training.py",
    script_args=SAM_SCRIPT_ARGS,
    flavor="t4-small",
    timeout=7200,
    env={"PYTHONUNBUFFERED": "1"},
    secrets={"HF_TOKEN": get_token()},
)
print(f"Job ID: {job_info.id}")
```

### 关键 SAM `script_args`

- `--model_name_or_path` — SAM 或 SAM2 模型（见上方模型表）；自动检测 SAM vs SAM2
- `--dataset_name` — Hub 数据集 ID（如 `"merve/MicroMat-mini"`）
- `--prompt_type` — `"bbox"` 或 `"point"` — 数据集中的提示类型
- `--prompt_column_name` — 包含 JSON 编码提示的列（默认：`"prompt"`）
- `--bbox_column_name` — 专用 bbox 列（JSON 提示列的替代）
- `--point_column_name` — 专用 point 列（JSON 提示列的替代）
- `--mask_column_name` — 包含真值掩码的列（默认：`"mask"`）
- `--hub_model_id` — `"username/model-name"` 用于 Hub 持久化
- `--num_train_epochs` — SAM 微调通常 20-30
- `--per_device_train_batch_size` — 2-4（SAM 模型占用大量内存）
- `--freeze_vision_encoder` / `--freeze_prompt_encoder` — 冻结编码器权重（默认：两者都冻结，只训练 mask decoder）
- `--train_val_split` — 验证集划分比例（默认 0.1）

## 检查任务状态

**MCP 工具（如可用）：**
```
hf_jobs("ps")                                   # 列出所有任务
hf_jobs("logs", {"job_id": "your-job-id"})      # 查看日志
hf_jobs("inspect", {"job_id": "your-job-id"})   # 任务详情
```

**Python API 备选：**
```python
from huggingface_hub import HfApi
api = HfApi()
api.list_jobs()                                  # 列出所有任务
api.get_job_logs(job_id="your-job-id")           # 查看日志
api.get_job(job_id="your-job-id")                # 任务详情
```

## 常见故障模式

### OOM（CUDA 内存不足）
减小 `per_device_train_batch_size`（尝试 4，再试 2），减小 `IMAGE_SIZE`，或升级硬件。

### 数据集格式错误
先运行 `scripts/dataset_inspector.py`。训练脚本自动检测 xyxy vs xywh，将字符串类别转换为整数 ID，缺失时添加 `image_id`。确保 `objects.bbox` 包含绝对像素的四值坐标列表，`objects.category` 包含整数 ID 或字符串标签。

### Hub 推送失败（401）
验证：(1) job secrets 包含 token（见指令 #2），(2) 脚本在创建 `Trainer` 前设置 `training_args.hub_token`，(3) `push_to_hub=True` 已设置，(4) `hub_model_id` 正确，(5) token 有写入权限。

### 任务超时
增加超时（见指令 #5 表格），减少 epoch/数据集，或使用 `hub_strategy="every_save"` 的检查点策略。

### KeyError: 'test'（缺少测试集划分）
目标检测训练脚本会优雅处理 — 回退到 `validation` 划分。确保使用最新的 `scripts/object_detection_training.py`。

### 单类数据集："iteration over a 0-d tensor"
`torchmetrics.MeanAveragePrecision` 在只有一个类时为每类指标返回标量（0-d）张量。模板 `scripts/object_detection_training.py` 通过对这些张量调用 `.unsqueeze(0)` 处理此问题。确保使用最新模板。

### 检测性能差（mAP < 0.15）
增加 epoch（30-50），确保 500+ 张图像，检查各类别 mAP 是否不平衡，尝试不同学习率（1e-5 到 1e-4），增大图像尺寸。

完整故障排查：见 [references/reliability_principles.md](references/reliability_principles.md)

## 参考文件

- [scripts/object_detection_training.py](scripts/object_detection_training.py) — 生产就绪的目标检测训练脚本
- [scripts/image_classification_training.py](scripts/image_classification_training.py) — 生产就绪的图像分类训练脚本（支持 timm 模型）
- [scripts/sam_segmentation_training.py](scripts/sam_segmentation_training.py) — 生产就绪的 SAM/SAM2 分割训练脚本（bbox 和 point 提示）
- [scripts/dataset_inspector.py](scripts/dataset_inspector.py) — 验证 OD、分类和 SAM 分割的数据集格式
- [scripts/estimate_cost.py](scripts/estimate_cost.py) — 估算任何视觉模型的训练成本（含 SAM/SAM2）
- [references/object_detection_training_notebook.md](references/object_detection_training_notebook.md) — 目标检测训练工作流、数据增强策略和训练模式
- [references/image_classification_training_notebook.md](references/image_classification_training_notebook.md) — 图像分类训练工作流，含 ViT、预处理和评估
- [references/finetune_sam2_trainer.md](references/finetune_sam2_trainer.md) — SAM2 微调演练，使用 MicroMat 数据集、DiceCE 损失和 Trainer 集成
- [references/timm_trainer.md](references/timm_trainer.md) — 在 HF Trainer 中使用 timm 模型（TimmWrapper、transforms、完整示例）
- [references/hub_saving.md](references/hub_saving.md) — 详细的 Hub 持久化指南和验证清单
- [references/reliability_principles.md](references/reliability_principles.md) — 来自生产经验的故障预防原则

## 外部链接

- [Transformers 目标检测指南](https://huggingface.co/docs/transformers/tasks/object_detection)
- [Transformers 图像分类指南](https://huggingface.co/docs/transformers/tasks/image_classification)
- [DETR 模型文档](https://huggingface.co/docs/transformers/model_doc/detr)
- [ViT 模型文档](https://huggingface.co/docs/transformers/model_doc/vit)
- [HF Jobs 指南](https://huggingface.co/docs/huggingface_hub/guides/jobs) — 主要 Jobs 文档
- [HF Jobs 配置](https://huggingface.co/docs/hub/en/jobs-configuration) — 硬件、密钥、超时、命名空间
- [HF Jobs CLI 参考](https://huggingface.co/docs/huggingface_hub/guides/cli#hf-jobs) — 命令行界面
- [目标检测模型](https://huggingface.co/models?pipeline_tag=object-detection)
- [图像分类模型](https://huggingface.co/models?pipeline_tag=image-classification)
- [SAM2 模型文档](https://huggingface.co/docs/transformers/model_doc/sam2)
- [SAM 模型文档](https://huggingface.co/docs/transformers/model_doc/sam)
- [目标检测数据集](https://huggingface.co/datasets?task_categories=task_categories:object-detection)
- [图像分类数据集](https://huggingface.co/datasets?task_categories=task_categories:image-classification)

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如果缺少必要输入、权限、安全边界或成功标准，停下来请求澄清。
