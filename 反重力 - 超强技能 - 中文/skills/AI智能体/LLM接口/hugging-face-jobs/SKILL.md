---
source: "https://github.com/huggingface/skills/tree/main/skills/huggingface-jobs"
name: hugging-face-jobs
description: 在 Hugging Face Jobs 上运行工作负载，支持托管式 CPU、GPU、TPU、密钥和 Hub 持久化。
license: 完整条款见 LICENSE.txt
risk: unknown
---

# 在 Hugging Face Jobs 上运行工作负载

## 概述

在完全托管的 Hugging Face 基础设施上运行任意工作负载。无需本地配置——任务在云端 CPU、GPU 或 TPU 上运行，可将结果持久化到 Hugging Face Hub。

**常见用途：**
- **数据处理** - 转换、过滤或分析大型数据集
- **批量推理** - 对数千个样本运行推理
- **实验与基准测试** - 可复现的机器学习实验
- **模型训练** - 微调模型（TRL 专项训练请参阅 `model-trainer` 技能）
- **合成数据生成** - 使用 LLM 生成数据集
- **开发与测试** - 无需本地 GPU 配置即可测试代码
- **定时任务** - 自动化周期性任务

**模型训练专项：** 请参阅 `model-trainer` 技能了解基于 TRL 的训练工作流。

## 适用场景

适用于以下需求：
- 在云基础设施上运行 Python 工作负载
- 无需本地 GPU/TPU 配置即可执行任务
- 大规模数据处理
- 运行批量推理或实验
- 调度周期性任务
- 使用 GPU/TPU 运行任意工作负载
- 将结果持久化到 Hugging Face Hub

## 核心指令

处理任务时：

1. **始终使用 `hf_jobs()` MCP 工具** - 通过 `hf_jobs("uv", {...})` 或 `hf_jobs("run", {...})` 提交任务。`script` 参数直接接收 Python 代码。除非用户明确要求，否则不要保存到本地文件。将脚本内容作为字符串传递给 `hf_jobs()`。

2. **始终处理认证** - 与 Hub 交互的任务需要通过 secrets 传入 `HF_TOKEN`。详见下文 Token 使用章节。

3. **提交后提供任务详情** - 提交后，提供任务 ID、监控 URL、预估时间，并告知用户可随时请求状态检查。

4. **设置合理的超时时间** - 默认 30 分钟对长时间运行的任务可能不足。

## 前置条件检查清单

启动任何任务前，请验证：

### ✅ **账户与认证**
- 拥有 [Pro](https://hf.co/pro)、[Team](https://hf.co/enterprise) 或 [Enterprise](https://hf.co/enterprise) 计划的 Hugging Face 账户（Jobs 需要付费计划）
- 已认证登录：使用 `hf_whoami()` 检查
- **Hub 访问用的 HF_TOKEN** ⚠️ 关键 - 任何 Hub 操作（推送模型/数据集、下载私有仓库等）都需要
- Token 必须具有适当权限（下载用读取权限，上传用写入权限）

### ✅ **Token 使用**（详见 Token 使用章节）

**何时需要 Token：**
- 推送模型/数据集到 Hub
- 访问私有仓库
- 在脚本中使用 Hub API
- 任何需要认证的 Hub 操作

**如何提供 Token：**
```python
# hf_jobs MCP 工具 — $HF_TOKEN 会自动替换为真实 Token：
{"secrets": {"HF_TOKEN": "$HF_TOKEN"}}

# HfApi().run_uv_job() — 必须传入实际 Token：
from huggingface_hub import get_token
secrets={"HF_TOKEN": get_token()}
```

**⚠️ 关键：** `$HF_TOKEN` 占位符仅被 `hf_jobs` MCP 工具自动替换。使用 `HfApi().run_uv_job()` 时，必须通过 `get_token()` 传入真实 Token。传入字面字符串 `"$HF_TOKEN"` 会导致 9 字符无效 Token 和 401 错误。

## Token 使用指南

### 理解 Token

**什么是 HF Token？**
- Hugging Face Hub 的认证凭证
- 认证操作（推送、私有仓库、API 访问）必需
- 在 `hf auth login` 后安全存储在本地

**Token 类型：**
- **读取 Token** - 可下载模型/数据集，读取私有仓库
- **写入 Token** - 可推送模型/数据集，创建仓库，修改内容
- **组织 Token** - 可代表组织执行操作

### 何时需要 Token

**始终需要：**
- 推送模型/数据集到 Hub
- 访问私有仓库
- 创建新仓库
- 修改现有仓库
- 编程方式使用 Hub API

**不需要：**
- 下载公开模型/数据集
- 运行不与 Hub 交互的任务
- 读取公开仓库信息

### 如何向任务提供 Token

#### 方法一：自动 Token（推荐）

```python
hf_jobs("uv", {
    "script": "your_script.py",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ 自动替换
})
```

**工作原理：**
- `$HF_TOKEN` 是占位符，会被替换为实际 Token
- 使用登录会话中的 Token（`hf auth login`）
- 最安全便捷的方式
- Token 作为 secret 传递时在服务端加密

**优点：**
- 代码中不暴露 Token
- 使用当前登录会话
- 重新登录后自动更新
- 与 MCP 工具无缝配合

#### 方法二：显式 Token（不推荐）

```python
hf_jobs("uv", {
    "script": "your_script.py",
    "secrets": {"HF_TOKEN": "hf_abc123..."}  # ⚠️ 硬编码 Token
})
```

**适用场景：**
- 仅当自动 Token 不工作时
- 使用特定 Token 测试
- 组织 Token（谨慎使用）

**安全隐患：**
- Token 在代码/日志中可见
- Token 轮换时需手动更新
- Token 泄露风险

#### 方法三：环境变量（安全性较低）

```python
hf_jobs("uv", {
    "script": "your_script.py",
    "env": {"HF_TOKEN": "hf_abc123..."}  # ⚠️ 比 secrets 安全性低
})
```

**与 secrets 的区别：**
- `env` 变量在任务日志中可见
- `secrets` 在服务端加密
- Token 始终优先使用 `secrets`

### 在脚本中使用 Token

**在 Python 脚本中，Token 作为环境变量可用：**

```python
# /// script
# dependencies = ["huggingface-hub"]
# ///

import os
from huggingface_hub import HfApi

# 如果通过 secrets 传入，Token 自动可用
token = os.environ.get("HF_TOKEN")

# 配合 Hub API 使用
api = HfApi(token=token)

# 或让 huggingface_hub 自动检测
api = HfApi()  # 自动使用 HF_TOKEN 环境变量
```

**最佳实践：**
- 不要在脚本中硬编码 Token
- 使用 `os.environ.get("HF_TOKEN")` 访问
- 尽可能让 `huggingface_hub` 自动检测
- Hub 操作前验证 Token 存在

### Token 验证

**检查是否已登录：**
```python
from huggingface_hub import whoami
user_info = whoami()  # 已认证时返回用户名
```

**验证任务中的 Token：**
```python
import os
assert "HF_TOKEN" in os.environ, "未找到 HF_TOKEN！"
token = os.environ["HF_TOKEN"]
print(f"Token 前缀: {token[:7]}...")  # 应以 "hf_" 开头
```

### 常见 Token 问题

**错误：401 Unauthorized**
- **原因：** Token 缺失或无效
- **解决：** 在任务配置中添加 `secrets={"HF_TOKEN": "$HF_TOKEN"}`
- **验证：** 检查本地 `hf_whoami()` 是否正常

**错误：403 Forbidden**
- **原因：** Token 缺少必要权限
- **解决：** 确保推送操作使用具有写入权限的 Token
- **检查：** 在 https://huggingface.co/settings/tokens 查看 Token 类型

**错误：环境中未找到 Token**
- **原因：** 未传递 `secrets` 或键名错误
- **解决：** 使用 `secrets={"HF_TOKEN": "$HF_TOKEN"}`（不是 `env`）
- **验证：** 脚本检查 `os.environ.get("HF_TOKEN")`

**错误：仓库访问被拒绝**
- **原因：** Token 无权访问私有仓库
- **解决：** 使用具有访问权限的账户 Token
- **检查：** 验证仓库可见性和您的权限

### Token 安全最佳实践

1. **永不提交 Token** - 使用 `$HF_TOKEN` 占位符或环境变量
2. **使用 secrets 而非 env** - secrets 在服务端加密
3. **定期轮换 Token** - 周期性生成新 Token
4. **使用最小权限** - 仅创建所需权限的 Token
5. **不共享 Token** - 每个用户应使用自己的 Token
6. **监控 Token 使用** - 在 Hub 设置中检查 Token 活动

### 完整 Token 示例

```python
# 示例：推送结果到 Hub
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["huggingface-hub", "datasets"]
# ///

import os
from huggingface_hub import HfApi
from datasets import Dataset

# 验证 Token 可用
assert "HF_TOKEN" in os.environ, "需要 HF_TOKEN！"

# 使用 Token 进行 Hub 操作
api = HfApi(token=os.environ["HF_TOKEN"])

# 创建并推送数据集
data = {"text": ["Hello", "World"]}
dataset = Dataset.from_dict(data)
dataset.push_to_hub("username/my-dataset", token=os.environ["HF_TOKEN"])

print("✅ 数据集推送成功！")
""",
    "flavor": "cpu-basic",
    "timeout": "30m",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}  # ✅ 安全提供 Token
})
```

## 快速入门：两种方式

### 方式一：UV 脚本（推荐）

UV 脚本使用 PEP 723 内联依赖，实现整洁、自包含的工作负载。

**MCP 工具：**
```python
hf_jobs("uv", {
    "script": """
# /// script
# dependencies = ["transformers", "torch"]
# ///

from transformers import pipeline
import torch

# 您的工作负载
classifier = pipeline("sentiment-analysis")
result = classifier("I love Hugging Face!")
print(result)
""",
    "flavor": "cpu-basic",
    "timeout": "30m"
})
```

**CLI 等效：**
```bash
hf jobs uv run my_script.py --flavor cpu-basic --timeout 30m
```

**Python API：**
```python
from huggingface_hub import run_uv_job
run_uv_job("my_script.py", flavor="cpu-basic", timeout="30m")
```

**优点：** 直接使用 MCP 工具，代码整洁，依赖内联声明，无需保存文件

**适用场景：** 所有工作负载的默认选择，自定义逻辑，任何需要 `hf_jobs()` 的场景

#### UV 脚本的自定义 Docker 镜像

默认情况下，UV 脚本使用 `ghcr.io/astral-sh/uv:python3.12-bookworm-slim`。对于依赖复杂的机器学习工作负载，使用预构建镜像：

```python
hf_jobs("uv", {
    "script": "inference.py",
    "image": "vllm/vllm-openai:latest",  # 预装 vLLM 的镜像
    "flavor": "a10g-large"
})
```

**CLI：**
```bash
hf jobs uv run --image vllm/vllm-openai:latest --flavor a10g-large inference.py
```

**优点：** 启动更快，依赖预装，针对特定框架优化

#### Python 版本

默认情况下，UV 脚本使用 Python 3.12。指定其他版本：

```python
hf_jobs("uv", {
    "script": "my_script.py",
    "python": "3.11",  # 使用 Python 3.11
    "flavor": "cpu-basic"
})
```

**Python API：**
```python
from huggingface_hub import run_uv_job
run_uv_job("my_script.py", python="3.11")
```

#### 脚本处理

⚠️ **重要：** 根据您运行 Jobs 的方式，有两种"脚本路径"处理方式：

- **使用 `hf_jobs()` MCP 工具（本仓库推荐）**：`script` 值必须是**内联代码**（字符串）或 **URL**。本地文件系统路径（如 `"./scripts/foo.py"`）在远程容器中不存在。
- **使用 `hf jobs uv run` CLI**：本地文件路径**可用**（CLI 会上传您的脚本）。

**`hf_jobs()` MCP 工具的常见错误：**

```python
# ❌ 会失败（远程容器无法看到您的本地路径）
hf_jobs("uv", {"script": "./scripts/foo.py"})
```

**`hf_jobs()` MCP 工具的正确模式：**

```python
# ✅ 内联：读取本地脚本文件并传递其*内容*
from pathlib import Path
script = Path("hf-jobs/scripts/foo.py").read_text()
hf_jobs("uv", {"script": script})

# ✅ URL：将脚本托管在可访问的位置
hf_jobs("uv", {"script": "https://huggingface.co/datasets/uv-scripts/.../raw/main/foo.py"})

# ✅ 来自 GitHub 的 URL
hf_jobs("uv", {"script": "https://raw.githubusercontent.com/huggingface/trl/main/trl/scripts/sft.py"})
```

**CLI 等效（支持本地路径）：**

```bash
hf jobs uv run ./scripts/foo.py -- --your --args
```

#### 运行时添加依赖

添加超出 PEP 723 头部的额外依赖：

```python
hf_jobs("uv", {
    "script": "inference.py",
    "dependencies": ["transformers", "torch>=2.0"],  # 额外依赖
    "flavor": "a10g-small"
})
```

**Python API：**
```python
from huggingface_hub import run_uv_job
run_uv_job("inference.py", dependencies=["transformers", "torch>=2.0"])
```

### 方式二：基于 Docker 的任务

使用自定义 Docker 镜像和命令运行任务。

**MCP 工具：**
```python
hf_jobs("run", {
    "image": "python:3.12",
    "command": ["python", "-c", "print('Hello from HF Jobs!')"],
    "flavor": "cpu-basic",
    "timeout": "30m"
})
```

**CLI 等效：**
```bash
hf jobs run python:3.12 python -c "print('Hello from HF Jobs!')"
```

**Python API：**
```python
from huggingface_hub import run_job
run_job(image="python:3.12", command=["python", "-c", "print('Hello!')"], flavor="cpu-basic")
```

**优点：** 完全 Docker 控制，使用预构建镜像，运行任意命令
**适用场景：** 需要特定 Docker 镜像，非 Python 工作负载，复杂环境

**GPU 示例：**
```python
hf_jobs("run", {
    "image": "pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel",
    "command": ["python", "-c", "import torch; print(torch.cuda.get_device_name())"],
    "flavor": "a10g-small",
    "timeout": "1h"
})
```

**使用 Hugging Face Spaces 作为镜像：**

可以使用 HF Spaces 的 Docker 镜像：
```python
hf_jobs("run", {
    "image": "hf.co/spaces/lhoestq/duckdb",  # Space 作为 Docker 镜像
    "command": ["duckdb", "-c", "SELECT 'Hello from DuckDB!'"],
    "flavor": "cpu-basic"
})
```

**CLI：**
```bash
hf jobs run hf.co/spaces/lhoestq/duckdb duckdb -c "SELECT 'Hello!'"
```

### 在 Hub上查找更多 UV 脚本

`uv-scripts` 组织提供存储在 Hugging Face Hub 数据集中的现成 UV 脚本：

```python
# 发现可用的 UV 脚本集合
dataset_search({"author": "uv-scripts", "sort": "downloads", "limit": 20})

# 探索特定集合
hub_repo_details(["uv-scripts/classification"], repo_type="dataset", include_readme=True)
```

**热门集合：** OCR、分类、合成数据、vLLM、数据集创建

## 硬件选择

> **参考：** [HF Jobs 硬件文档](https://huggingface.co/docs/hub/en/spaces-config-reference)（2025年7月更新）

| 工作负载类型 | 推荐硬件 | 适用场景 |
|---------------|---------------------|----------|
| 数据处理、测试 | `cpu-basic`, `cpu-upgrade` | 轻量级任务 |
| 小模型、演示 | `t4-small` | <1B 模型，快速测试 |
| 中等模型 | `t4-medium`, `l4x1` | 1-7B 模型 |
| 大模型、生产环境 | `a10g-small`, `a10g-large` | 7-13B 模型 |
| 超大模型 | `a100-large` | 13B+ 模型 |
| 批量推理 | `a10g-large`, `a100-large` | 高吞吐量 |
| 多 GPU 工作负载 | `l4x4`, `a10g-largex2`, `a10g-largex4` | 并行/大模型 |
| TPU 工作负载 | `v5e-1x1`, `v5e-2x2`, `v5e-2x4` | JAX/Flax，TPU 优化 |

**所有可用规格：**
- **CPU：** `cpu-basic`, `cpu-upgrade`
- **GPU：** `t4-small`, `t4-medium`, `l4x1`, `l4x4`, `a10g-small`, `a10g-large`, `a10g-largex2`, `a10g-largex4`, `a100-large`
- **TPU：** `v5e-1x1`, `v5e-2x2`, `v5e-2x4`

**指南：**
- 测试时从小规格硬件开始
- 根据实际需求扩展
- 并行工作负载或大模型使用多 GPU
- JAX/Flax 工作负载使用 TPU
- 详见 `references/hardware_guide.md` 获取详细规格

## 关键：保存结果

**⚠️ 临时环境—必须持久化结果**

Jobs 环境是临时的。任务结束时所有文件都会删除。如果不持久化结果，**所有工作将丢失**。

### 持久化选项

**1. 推送到 Hugging Face Hub（推荐）**

```python
# 推送模型
model.push_to_hub("username/model-name", token=os.environ["HF_TOKEN"])

# 推送数据集
dataset.push_to_hub("username/dataset-name", token=os.environ["HF_TOKEN"])

# 推送产物
api.upload_file(
    path_or_fileobj="results.json",
    path_in_repo="results.json",
    repo_id="username/results",
    token=os.environ["HF_TOKEN"]
)
```

**2. 使用外部存储**

```python
# 上传到 S3、GCS 等
import boto3
s3 = boto3.client('s3')
s3.upload_file('results.json', 'my-bucket', 'results.json')
```

**3. 通过 API 发送结果**

```python
# POST 结果到您的 API
import requests
requests.post("https://your-api.com/results", json=results)
```

### Hub 推送所需配置

**在任务提交中：**
```python
# hf_jobs MCP 工具：
{"secrets": {"HF_TOKEN": "$HF_TOKEN"}}  # 自动替换

# HfApi().run_uv_job()：
from huggingface_hub import get_token
secrets={"HF_TOKEN": get_token()}  # 必须传入真实 Token
```

**在脚本中：**
```python
import os
from huggingface_hub import HfApi

# Token 从 secrets 自动可用
api = HfApi(token=os.environ.get("HF_TOKEN"))

# 推送您的结果
api.upload_file(...)
```

### 验证检查清单

提交前：
- [ ] 已选择结果持久化方式
- [ ] 使用 Hub 时 Token 在 secrets 中（MCP：`"$HF_TOKEN"`，Python API：`get_token()`）
- [ ] 脚本优雅处理缺失 Token
- [ ] 测试持久化路径可行

**参阅：** `references/hub_saving.md` 获取详细的 Hub 持久化指南

## 超时管理

**⚠️ 默认：30 分钟**

任务在超时后自动停止。对于训练等长时间运行的任务，始终设置自定义超时。

### 设置超时

**MCP 工具：**
```python
{
    "timeout": "2h"   # 2 小时
}
```

**支持的格式：**
- 整数/浮点数：秒（如 `300` = 5 分钟）
- 带后缀字符串：`"5m"`（分钟）、`"2h"`（小时）、`"1d"`（天）
- 示例：`"90m"`、`"2h"`、`"1.5h"`、`300`、`"1d"`

**Python API：**
```python
from huggingface_hub import run_job, run_uv_job

run_job(image="python:3.12", command=[...], timeout="2h")
run_uv_job("script.py", timeout=7200)  # 2 小时（秒）
```

### 超时指南

| 场景 | 推荐值 | 说明 |
|----------|-------------|-------|
| 快速测试 | 10-30 分钟 | 验证配置 |
| 数据处理 | 1-2 小时 | 取决于数据量 |
| 批量推理 | 2-4 小时 | 大批次 |
| 实验 | 4-8 小时 | 多次运行 |
| 长时间运行 | 8-24 小时 | 生产工作负载 |

**始终添加 20-30% 缓冲** 用于设置、网络延迟和清理。

**超时时：** 任务立即终止，所有未保存进度丢失

## 成本估算

**通用指南：**

```
总成本 = (运行小时数) × (每小时成本)
```

**示例计算：**

**快速测试：**
- 硬件：cpu-basic（$0.10/小时）
- 时间：15 分钟（0.25 小时）
- 成本：$0.03

**数据处理：**
- 硬件：l4x1（$2.50/小时）
- 时间：2 小时
- 成本：$5.00

**批量推理：**
- 硬件：a10g-large（$5/小时）
- 时间：4 小时
- 成本：$20.00

**成本优化建议：**
1. 从小规格开始 - 在 cpu-basic 或 t4-small 上测试
2. 监控运行时间 - 设置合理的超时
3. 使用检查点 - 任务失败时可恢复
4. 优化代码 - 减少不必要的计算
5. 选择合适的硬件 - 不要过度配置

## 监控与追踪

### 检查任务状态

**MCP 工具：**
```python
# 列出所有任务
hf_jobs("ps")

# 检查特定任务
hf_jobs("inspect", {"job_id": "your-job-id"})

# 查看日志
hf_jobs("logs", {"job_id": "your-job-id"})

# 取消任务
hf_jobs("cancel", {"job_id": "your-job-id"})
```

**Python API：**
```python
from huggingface_hub import list_jobs, inspect_job, fetch_job_logs, cancel_job

# 列出您的任务
jobs = list_jobs()

# 仅列出运行中的任务
running = [j for j in list_jobs() if j.status.stage == "RUNNING"]

# 检查特定任务
job_info = inspect_job(job_id="your-job-id")

# 查看日志
for log in fetch_job_logs(job_id="your-job-id"):
    print(log)

# 取消任务
cancel_job(job_id="your-job-id")
```

**CLI：**
```bash
hf jobs ps                    # 列出任务
hf jobs logs <job-id>         # 查看日志
hf jobs cancel <job-id>       # 取消任务
```

**注意：** 等待用户请求状态检查。避免重复轮询。

### 任务 URL

提交后，任务有监控 URL：
```
https://huggingface.co/jobs/username/job-id
```

在浏览器中查看日志、状态和详情。

### 等待多个任务

```python
import time
from huggingface_hub import inspect_job, run_job

# 运行多个任务
jobs = [run_job(image=img, command=cmd) for img, cmd in workloads]

# 等待全部完成
for job in jobs:
    while inspect_job(job_id=job.id).status.stage not in ("COMPLETED", "ERROR"):
        time.sleep(10)
```

## 定时任务

使用 CRON 表达式或预定义计划按计划运行任务。

**MCP 工具：**
```python
# 调度每小时运行的 UV 脚本
hf_jobs("scheduled uv", {
    "script": "your_script.py",
    "schedule": "@hourly",
    "flavor": "cpu-basic"
})

# 使用 CRON 语法调度
hf_jobs("scheduled uv", {
    "script": "your_script.py",
    "schedule": "0 9 * * 1",  # 每周一上午 9 点
    "flavor": "cpu-basic"
})

# 调度基于 Docker 的任务
hf_jobs("scheduled run", {
    "image": "python:3.12",
    "command": ["python", "-c", "print('Scheduled!')"],
    "schedule": "@daily",
    "flavor": "cpu-basic"
})
```

**Python API：**
```python
from huggingface_hub import create_scheduled_job, create_scheduled_uv_job

# 调度 Docker 任务
create_scheduled_job(
    image="python:3.12",
    command=["python", "-c", "print('Running on schedule!')"],
    schedule="@hourly"
)

# 调度 UV 脚本
create_scheduled_uv_job("my_script.py", schedule="@daily", flavor="cpu-basic")

# 使用 GPU 调度
create_scheduled_uv_job(
    "ml_inference.py",
    schedule="0 */6 * * *",  # 每 6 小时
    flavor="a10g-small"
)
```

**可用计划：**
- `@annually`, `@yearly` - 每年一次
- `@monthly` - 每月一次
- `@weekly` - 每周一次
- `@daily` - 每天一次
- `@hourly` - 每小时一次
- CRON 表达式 - 自定义计划（如 `"*/5 * * * *"` 表示每 5 分钟）

**管理定时任务：**
```python
# MCP 工具
hf_jobs("scheduled ps")                              # 列出定时任务
hf_jobs("scheduled inspect", {"job_id": "..."})     # 查看详情
hf_jobs("scheduled suspend", {"job_id": "..."})     # 暂停
hf_jobs("scheduled resume", {"job_id": "..."})      # 恢复
hf_jobs("scheduled delete", {"job_id": "..."})      # 删除
```

**Python API 管理：**
```python
from huggingface_hub import (
    list_scheduled_jobs,
    inspect_scheduled_job,
    suspend_scheduled_job,
    resume_scheduled_job,
    delete_scheduled_job
)

# 列出所有定时任务
scheduled = list_scheduled_jobs()

# 检查定时任务
info = inspect_scheduled_job(scheduled_job_id)

# 暂停定时任务
suspend_scheduled_job(scheduled_job_id)

# 恢复定时任务
resume_scheduled_job(scheduled_job_id)

# 删除定时任务
delete_scheduled_job(scheduled_job_id)
```

## Webhooks：事件触发任务

当 Hugging Face 仓库发生变化时自动触发任务。

**Python API：**
```python
from huggingface_hub import create_webhook

# 创建 webhook，当仓库变化时触发任务
webhook = create_webhook(
    job_id=job.id,
    watched=[
        {"type": "user", "name": "your-username"},
        {"type": "org", "name": "your-org-name"}
    ],
    domains=["repo", "discussion"],
    secret="your-secret"
)
```

**工作原理：**
1. Webhook 监听被监视仓库的变化
2. 触发时，任务运行并带有 `WEBHOOK_PAYLOAD` 环境变量
3. 您的脚本可解析负载了解发生了什么变化

**用途：**
- 上传新数据集时自动处理
- 模型更新时触发推理
- 代码变化时运行测试
- 生成仓库活动报告

**在脚本中访问 webhook 负载：**
```python
import os
import json

payload = json.loads(os.environ.get("WEBHOOK_PAYLOAD", "{}"))
print(f"事件类型: {payload.get('event', {}).get('action')}")
```

详见 [Webhooks 文档](https://huggingface.co/docs/huggingface_hub/guides/webhooks)。

## 常见工作负载模式

本仓库在 `hf-jobs/scripts/` 中提供现成的 UV 脚本。优先使用它们而非创建新模板。

### 模式一：数据集 → 模型响应（vLLM）— `scripts/generate-responses.py`

**功能：** 加载 Hub 数据集（聊天 `messages` 或 `prompt` 列），应用模型聊天模板，使用 vLLM 生成响应，并将输出数据集 + 数据集卡片**推送**回 Hub。

**需要：** GPU + **写入** Token（会推送数据集）。

```python
from pathlib import Path

script = Path("hf-jobs/scripts/generate-responses.py").read_text()
hf_jobs("uv", {
    "script": script,
    "script_args": [
        "username/input-dataset",
        "username/output-dataset",
        "--messages-column", "messages",
        "--model-id", "Qwen/Qwen3-30B-A3B-Instruct-2507",
        "--temperature", "0.7",
        "--top-p", "0.8",
        "--max-tokens", "2048",
    ],
    "flavor": "a10g-large",
    "timeout": "4h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"},
})
```

### 模式二：CoT Self-Instruct 合成数据 — `scripts/cot-self-instruct.py`

**功能：** 通过 CoT Self-Instruct 生成合成提示/答案，可选过滤输出（答案一致性 / RIP），然后将生成的数据集 + 数据集卡片**推送**到 Hub。

**需要：** GPU + **写入** Token（会推送数据集）。

```python
from pathlib import Path

script = Path("hf-jobs/scripts/cot-self-instruct.py").read_text()
hf_jobs("uv", {
    "script": script,
    "script_args": [
        "--seed-dataset", "davanstrien/s1k-reasoning",
        "--output-dataset", "username/synthetic-math",
        "--task-type", "reasoning",
        "--num-samples", "5000",
        "--filter-method", "answer-consistency",
    ],
    "flavor": "l4x4",
    "timeout": "8h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"},
})
```

### 模式三：流式数据集统计（Polars + HF Hub）— `scripts/finepdfs-stats.py`

**功能：** 直接从 Hub 扫描 parquet（无需下载 300GB），计算时间统计，并（可选）上传结果到 Hub 数据集仓库。

**需要：** CPU 通常足够；仅当传递 `--output-repo`（上传）时需要 Token。

```python
from pathlib import Path

script = Path("hf-jobs/scripts/finepdfs-stats.py").read_text()
hf_jobs("uv", {
    "script": script,
    "script_args": [
        "--limit", "10000",
        "--show-plan",
        "--output-repo", "username/finepdfs-temporal-stats",
    ],
    "flavor": "cpu-upgrade",
    "timeout": "2h",
    "env": {"HF_XET_HIGH_PERFORMANCE": "1"},
    "secrets": {"HF_TOKEN": "$HF_TOKEN"},
})
```

## 常见失败模式

### 内存不足（OOM）

**解决：**
1. 减小批次大小或数据块大小
2. 分批处理数据
3. 升级硬件：cpu → t4 → a10g → a100

### 任务超时

**解决：**
1. 检查日志了解实际运行时间
2. 增加超时并添加缓冲：`"timeout": "3h"`
3. 优化代码加快执行
4. 分块处理数据

### Hub 推送失败

**解决：**
1. 在 secrets 中添加 Token：MCP 使用 `"$HF_TOKEN"`（自动替换），Python API 使用 `get_token()`（必须传入真实 Token）
2. 在脚本中验证 Token：`assert "HF_TOKEN" in os.environ`
3. 检查 Token 权限
4. 验证仓库存在或可创建

### 缺少依赖

**解决：**
添加到 PEP 723 头部：
```python
# /// script
# dependencies = ["package1", "package2>=1.0.0"]
# ///
```

### 认证错误

**解决：**
1. 检查本地 `hf_whoami()` 是否正常
2. 验证 secrets 中的 Token — MCP：`"$HF_TOKEN"`，Python API：`get_token()`（不是 `"$HF_TOKEN"`）
3. 重新登录：`hf auth login`
4. 检查 Token 是否具有所需权限

## 故障排除

**常见问题：**
- 任务超时 → 增加超时，优化代码
- 结果未保存 → 检查持久化方式，验证 HF_TOKEN
- 内存不足 → 减小批次大小，升级硬件
- 导入错误 → 在 PEP 723 头部添加依赖
- 认证错误 → 检查 Token，验证 secrets 参数

**参阅：** `references/troubleshooting.md` 获取完整故障排除指南

## 资源

### 参考资料（本技能内）
- `references/token_usage.md` - 完整 Token 使用指南
- `references/hardware_guide.md` - 硬件规格与选择
- `references/hub_saving.md` - Hub 持久化指南
- `references/troubleshooting.md` - 常见问题与解决方案

### 脚本（本技能内）
- `scripts/generate-responses.py` - vLLM 批量生成：数据集 → 响应 → 推送到 Hub
- `scripts/cot-self-instruct.py` - CoT Self-Instruct 合成数据生成 + 过滤 → 推送到 Hub
- `scripts/finepdfs-stats.py` - Polars 流式统计 Hub 上的 `finepdfs-edu` parquet（可选推送）

### 外部链接

**官方文档：**
- [HF Jobs 指南](https://huggingface.co/docs/huggingface_hub/guides/jobs) - 主要文档
- [HF Jobs CLI 参考](https://huggingface.co/docs/huggingface_hub/guides/cli#hf-jobs) - 命令行界面
- [HF Jobs API 参考](https://huggingface.co/docs/huggingface_hub/package_reference/hf_api) - Python API 详情
- [硬件规格参考](https://huggingface.co/docs/hub/en/spaces-config-reference) - 可用硬件

**相关工具：**
- [UV 脚本指南](https://docs.astral.sh/uv/guides/scripts/) - PEP 723 内联依赖
- [UV 脚本组织](https://huggingface.co/uv-scripts) - 社区 UV 脚本集合
- [HF Hub 认证](https://huggingface.co/docs/huggingface_hub/quick-start#authentication) - Token 设置
- [Webhooks 文档](https://huggingface.co/docs/huggingface_hub/guides/webhooks) - 事件触发器

## 核心要点

1. **内联提交脚本** - `script` 参数直接接收 Python 代码；除非用户要求否则无需保存文件
2. **任务是异步的** - 不要等待/轮询；让用户在需要时检查
3. **始终设置超时** - 默认 30 分钟可能不足；设置合理的超时
4. **始终持久化结果** - 环境是临时的；不持久化则工作丢失
5. **安全使用 Token** - MCP：`secrets={"HF_TOKEN": "$HF_TOKEN"}`，Python API：`secrets={"HF_TOKEN": get_token()}` — `"$HF_TOKEN"` 仅适用于 MCP 工具
6. **选择合适的硬件** - 从小规格开始，根据需求扩展（见硬件指南）
7. **使用 UV 脚本** - Python 工作负载默认使用 `hf_jobs("uv", {...})` 配合内联脚本
8. **处理认证** - Hub 操作前验证 Token 可用
9. **监控任务** - 提供任务 URL 和状态检查命令
10. **优化成本** - 选择合适硬件，设置合理超时

## 快速参考：MCP 工具 vs CLI vs Python API

| 操作 | MCP 工具 | CLI | Python API |
|-----------|----------|-----|------------|
| 运行 UV 脚本 | `hf_jobs("uv", {...})` | `hf jobs uv run script.py` | `run_uv_job("script.py")` |
| 运行 Docker 任务 | `hf_jobs("run", {...})` | `hf jobs run image cmd` | `run_job(image, command)` |
| 列出任务 | `hf_jobs("ps")` | `hf jobs ps` | `list_jobs()` |
| 查看日志 | `hf_jobs("logs", {...})` | `hf jobs logs <id>` | `fetch_job_logs(job_id)` |
| 取消任务 | `hf_jobs("cancel", {...})` | `hf jobs cancel <id>` | `cancel_job(job_id)` |
| 调度 UV | `hf_jobs("scheduled uv", {...})` | `hf jobs scheduled uv run SCHEDULE script.py` | `create_scheduled_uv_job()` |
| 调度 Docker | `hf_jobs("scheduled run", {...})` | `hf jobs scheduled run SCHEDULE image cmd` | `create_scheduled_job()` |
| 列出定时任务 | `hf_jobs("scheduled ps")` | `hf jobs scheduled ps` | `list_scheduled_jobs()` |
| 删除定时任务 | `hf_jobs("scheduled delete", {...})` | `hf jobs scheduled delete <id>` | `delete_scheduled_job()` |

## 限制
- 仅当任务明确符合上述描述的范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
