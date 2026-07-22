# 硬件选择指南

选择合适的硬件（flavor）对成本效益高的工作负载至关重要。

> **参考：** [HF Jobs 硬件文档](https://huggingface.co/docs/hub/en/spaces-config-reference)（2025年7月更新）

## 可用硬件

### CPU 规格

| 规格 | 描述 | 适用场景 |
|--------|-------------|----------|
| `cpu-basic` | 基础 CPU 实例 | 测试、轻量级脚本 |
| `cpu-upgrade` | 增强型 CPU 实例 | 数据处理、并行工作负载 |

**适用场景：** 数据处理、测试脚本、轻量级工作负载
**不建议用于：** 模型训练、GPU 加速工作负载

### GPU 规格

| 规格 | GPU | 显存 | 适用场景 |
|--------|-----|------|----------|
| `t4-small` | NVIDIA T4 | 16GB | <1B 模型、演示、快速测试 |
| `t4-medium` | NVIDIA T4 | 16GB | 1-3B 模型、开发 |
| `l4x1` | NVIDIA L4 | 24GB | 3-7B 模型、高效工作负载 |
| `l4x4` | 4x NVIDIA L4 | 96GB | 多 GPU、并行工作负载 |
| `a10g-small` | NVIDIA A10G | 24GB | 3-7B 模型、生产环境 |
| `a10g-large` | NVIDIA A10G | 24GB | 7-13B 模型、批量推理 |
| `a10g-largex2` | 2x NVIDIA A10G | 48GB | 多 GPU、大模型 |
| `a10g-largex4` | 4x NVIDIA A10G | 96GB | 多 GPU、超大模型 |
| `a100-large` | NVIDIA A100 | 40GB | 13B+ 模型、最快 GPU 选项 |

### TPU 规格

| 规格 | 配置 | 适用场景 |
|--------|---------------|----------|
| `v5e-1x1` | TPU v5e (1x1) | 小型 TPU 工作负载 |
| `v5e-2x2` | TPU v5e (2x2) | 中型 TPU 工作负载 |
| `v5e-2x4` | TPU v5e (2x4) | 大型 TPU 工作负载 |

**TPU 适用场景：**
- JAX/Flax 模型训练
- 大规模推理
- TPU 优化工作负载

## 选择指南

### 按工作负载类型

**数据处理**
- **推荐：** `cpu-upgrade` 或 `l4x1`
- **适用场景：** 转换、过滤、分析数据集
- **批处理大小：** 取决于数据量
- **时间：** 因数据集大小而异

**批量推理**
- **推荐：** `a10g-large` 或 `a100-large`
- **适用场景：** 对数千个样本运行推理
- **批处理大小：** 8-32 视模型而定
- **时间：** 取决于样本数量

**实验与基准测试**
- **推荐：** `a10g-small` 或 `a10g-large`
- **适用场景：** 可复现的机器学习实验
- **批处理大小：** 不定
- **时间：** 取决于实验复杂度

**模型训练**（详见 `model-trainer` 技能）
- **推荐：** 参阅 model-trainer 技能
- **适用场景：** 微调模型
- **批处理大小：** 取决于模型大小
- **时间：** 数小时至数天

**合成数据生成**
- **推荐：** `a10g-large` 或 `a100-large`
- **适用场景：** 使用 LLM 生成数据集
- **批处理大小：** 取决于生成方法
- **时间：** 大型数据集需要数小时

### 按预算

**极小预算（<$5 总额）**
- 使用 `cpu-basic` 或 `t4-small`
- 处理小数据集
- 快速测试和演示

**小预算（$5-20）**
- 使用 `t4-medium` 或 `a10g-small`
- 处理中等数据集
- 运行实验

**中等预算（$20-50）**
- 使用 `a10g-small` 或 `a10g-large`
- 处理大型数据集
- 生产工作负载

**大预算（$50-200）**
- 使用 `a10g-large` 或 `a100-large`
- 大规模处理
- 多个实验

### 按模型大小（用于推理/处理）

**微型模型（<1B 参数）**
- **推荐：** `t4-small`
- **示例：** Qwen2.5-0.5B、TinyLlama
- **批处理大小：** 8-16

**小型模型（1-3B 参数）**
- **推荐：** `t4-medium` 或 `a10g-small`
- **示例：** Qwen2.5-1.5B、Phi-2
- **批处理大小：** 4-8

**中型模型（3-7B 参数）**
- **推荐：** `a10g-small` 或 `a10g-large`
- **示例：** Qwen2.5-7B、Mistral-7B
- **批处理大小：** 2-4

**大型模型（7-13B 参数）**
- **推荐：** `a10g-large` 或 `a100-large`
- **示例：** Llama-3-8B
- **批处理大小：** 1-2

**超大型模型（13B+ 参数）**
- **推荐：** `a100-large`
- **示例：** Llama-3-13B、Llama-3-70B
- **批处理大小：** 1

## 内存考虑

### 估算内存需求

**推理：**
```
内存 (GB) ≈ (模型参数数量，单位为十亿) × 2-4
```

**训练：**
```
内存 (GB) ≈ (模型参数数量，单位为十亿) × 20（全量）或 × 4（LoRA）
```

**示例：**
- Qwen2.5-0.5B 推理：~1-2GB ✅ 适合 t4-small
- Qwen2.5-7B 推理：~14-28GB ✅ 适合 a10g-large
- Qwen2.5-7B 训练：~140GB ❌ 不使用 LoRA 不可行

### 内存优化

如果遇到内存限制：

1. **减小批处理大小**
   ```python
   batch_size = 1
   ```

2. **分块处理**
   ```python
   for chunk in chunks:
       process(chunk)
   ```

3. **使用更小的模型**
   - 使用量化模型
   - 使用 LoRA 适配器

4. **升级硬件**
   - cpu → t4 → a10g → a100

## 成本估算

### 公式

```
总成本 = (运行小时数) × (每小时成本)
```

### 示例计算

**数据处理：**
- 硬件：cpu-upgrade（$0.50/小时）
- 时间：1 小时
- 成本：$0.50

**批量推理：**
- 硬件：a10g-large（$5/小时）
- 时间：2 小时
- 成本：$10.00

**实验：**
- 硬件：a10g-small（$3.50/小时）
- 时间：4 小时
- 成本：$14.00

### 成本优化建议

1. **从小规模开始：** 在 cpu-basic 或 t4-small 上测试
2. **监控运行时间：** 设置合理的超时
3. **优化代码：** 减少不必要的计算
4. **选择合适的硬件：** 不要过度配置
5. **使用检查点：** 任务失败时可恢复
6. **监控成本：** 定期检查运行中的任务

## 多 GPU 工作负载

多 GPU 规格会自动分配工作负载：

**多 GPU 规格：**
- `l4x4` - 4x L4 GPU（总显存 96GB）
- `a10g-largex2` - 2x A10G GPU（总显存 48GB）
- `a10g-largex4` - 4x A10G GPU（总显存 96GB）

**使用场景：**
- 大模型（>13B 参数）
- 需要更快处理（线性加速）
- 大型数据集（>100K 样本）
- 并行工作负载
- 推理时的张量并行

**MCP 工具示例：**
```python
hf_jobs("uv", {
    "script": "process.py",
    "flavor": "a10g-largex2",  # 2 个 GPU
    "timeout": "4h",
    "secrets": {"HF_TOKEN": "$HF_TOKEN"}
})
```

**CLI 等效：**
```bash
hf jobs uv run process.py --flavor a10g-largex2 --timeout 4h
```

## 在选项间抉择

### CPU vs GPU

**选择 CPU 的情况：**
- 不需要 GPU 加速
- 仅数据处理
- 预算受限
- 简单工作负载

**选择 GPU 的情况：**
- 模型推理/训练
- GPU 加速库
- 需要更快处理
- 大模型

### a10g vs a100

**选择 a10g 的情况：**
- 模型 <13B 参数
- 注重预算
- 处理时间不关键

**选择 a100 的情况：**
- 模型 13B+ 参数
- 需要最快处理
- 内存需求高
- 预算允许

### 单 GPU vs 多 GPU

**选择单 GPU 的情况：**
- 模型 <7B 参数
- 预算受限
- 调试更简单

**选择多 GPU 的情况：**
- 模型 >13B 参数
- 需要更快处理
- 需要大批处理大小
- 对大型任务具有成本效益

## 快速参考

### 所有可用规格

```python
# 官方规格列表（2025年7月更新）
FLAVORS = {
    # CPU
    "cpu-basic",      # 测试、轻量级
    "cpu-upgrade",    # 数据处理

    # GPU - 单卡
    "t4-small",       # 16GB - <1B 模型
    "t4-medium",      # 16GB - 1-3B 模型
    "l4x1",           # 24GB - 3-7B 模型
    "a10g-small",     # 24GB - 3-7B 生产
    "a10g-large",     # 24GB - 7-13B 模型
    "a100-large",     # 40GB - 13B+ 模型

    # GPU - 多卡
    "l4x4",           # 4x L4（总 96GB）
    "a10g-largex2",   # 2x A10G（总 48GB）
    "a10g-largex4",   # 4x A10G（总 96GB）

    # TPU
    "v5e-1x1",        # TPU v5e 1x1
    "v5e-2x2",        # TPU v5e 2x2
    "v5e-2x4",        # TPU v5e 2x4
}
```

### 工作负载 → 硬件映射

```python
HARDWARE_MAP = {
    "data_processing": "cpu-upgrade",
    "batch_inference_small": "t4-small",
    "batch_inference_medium": "a10g-large",
    "batch_inference_large": "a100-large",
    "experiments": "a10g-small",
    "tpu_workloads": "v5e-1x1",
    "training": "see model-trainer skill"
}
```

### CLI 示例

```bash
# CPU 任务
hf jobs run python:3.12 python script.py

# GPU 任务
hf jobs run --flavor a10g-large pytorch/pytorch:2.6.0-cuda12.4-cudnn9-devel python script.py

# TPU 任务
hf jobs run --flavor v5e-1x1 your-tpu-image python script.py

# 带 GPU 的 UV 脚本
hf jobs uv run --flavor a10g-small my_script.py
```
