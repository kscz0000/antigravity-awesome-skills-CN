---
name: hugging-face-evaluation
description: 在 Hugging Face 模型卡中添加和管理评估结果。支持从 README 内容提取评估表格、从 Artificial Analysis API 导入分数，以及使用 vLLM/lighteval 运行自定义模型评估。兼容 model-index 元数据格式。
risk: unknown
source: community
---

# 概述

本技能提供在 Hugging Face 模型卡中添加结构化评估结果的工具。支持多种添加评估数据的方法：
- 从 README 内容提取现有评估表格
- 从 Artificial Analysis 导入基准测试分数
- 使用 vLLM 或 accelerate 后端运行自定义模型评估（lighteval/inspect-ai）

## 适用场景

- 需要在 Hugging Face 模型卡中添加结构化评估结果
- 想要导入基准测试数据或使用 vLLM、lighteval、inspect-ai 运行自定义评估
- 正在为模型发布准备兼容排行榜的 `model-index` 元数据

## 与 HF 生态集成

- **模型卡**：更新 model-index 元数据以实现排行榜集成
- **Artificial Analysis**：直接 API 集成用于基准测试导入
- **Papers with Code**：兼容其 model-index 规范
- **Jobs**：通过 `uv` 集成在 Hugging Face Jobs 上直接运行评估
- **vLLM**：高效 GPU 推理用于自定义模型评估
- **lighteval**：HuggingFace 的评估库，支持 vLLM/accelerate 后端
- **inspect-ai**：英国 AI 安全研究所的评估框架

# 版本

1.3.0

# 依赖

## 核心依赖

- huggingface_hub>=0.26.0
- markdown-it-py>=3.0.0
- python-dotenv>=1.2.1
- pyyaml>=6.0.3
- requests>=2.32.5
- re (built-in)

## 推理提供商评估

- inspect-ai>=0.3.0
- inspect-evals
- openai

## vLLM 自定义模型评估（需要 GPU）

- lighteval[accelerate,vllm]>=0.6.0
- vllm>=0.4.0
- torch>=2.0.0
- transformers>=4.40.0
- accelerate>=0.30.0

注意：使用 `uv run` 时，vLLM 依赖会通过 PEP 723 脚本头自动安装。

# 重要：使用本技能

## ⚠️ 关键：创建 PR 前检查现有 PR

**在使用 `--create-pr` 创建任何拉取请求之前，必须检查现有的开放 PR：**

```bash
uv run scripts/evaluation_manager.py get-prs --repo-id "username/model-name"
```

**如果存在开放 PR：**
1. **不要创建新 PR** - 这会给维护者带来重复工作
2. **警告用户** 已存在开放 PR
3. **向用户展示** 现有 PR 的 URL 以便查看
4. 仅在用户明确确认要创建另一个 PR 时才继续

这可以防止向模型仓库发送重复的评估 PR。

---

> **所有路径均相对于包含此 SKILL.md 文件的目录。**
> 运行任何脚本前，先 `cd` 到该目录或使用完整路径。

**使用 `--help` 获取最新工作流指导。** 支持纯 Python 或 `uv run`：
```bash
uv run scripts/evaluation_manager.py --help
uv run scripts/evaluation_manager.py inspect-tables --help
uv run scripts/evaluation_manager.py extract-readme --help
```
关键工作流（与 CLI 帮助一致）：

1) `get-prs` → 首先检查现有开放 PR
2) `inspect-tables` → 查找表格编号/列
3) `extract-readme --table N` → 默认打印 YAML
4) 添加 `--apply`（推送）或 `--create-pr` 来写入更改

# 核心能力

## 1. 检查和提取 README 中的评估表格

- **检查表格**：使用 `inspect-tables` 查看 README 中所有表格的结构、列和示例行
- **解析 Markdown 表格**：使用 markdown-it-py 精确解析（忽略代码块和示例）
- **表格选择**：使用 `--table N` 从特定表格提取（存在多个表格时必需）
- **格式检测**：识别常见格式（基准测试作为行、列，或包含多个模型的对比表格）
- **列匹配**：自动识别模型列/行；优先使用 `--model-column-index`（从 inspect 输出的索引）。仅在使用精确列标题文本时使用 `--model-name-override`
- **YAML 生成**：将选定表格转换为 model-index YAML 格式
- **任务类型**：`--task-type` 设置 model-index 输出中的 `task.type` 字段（如 `text-generation`、`summarization`）

## 2. 从 Artificial Analysis 导入

- **API 集成**：直接从 Artificial Analysis 获取基准测试分数
- **自动格式化**：将 API 响应转换为 model-index 格式
- **元数据保留**：维护来源归属和 URL
- **PR 创建**：自动创建包含评估更新的拉取请求

## 3. Model-Index 管理

- **YAML 生成**：创建格式正确的 model-index 条目
- **合并支持**：在不覆盖的情况下向现有模型卡添加评估
- **验证**：确保符合 Papers with Code 规范
- **批量操作**：高效处理多个模型

## 4. 在 HF Jobs 上运行评估（推理提供商）

- **Inspect-AI 集成**：使用 `inspect-ai` 库运行标准评估
- **UV 集成**：在 HF 基础设施上无缝运行带有临时依赖的 Python 脚本
- **零配置**：无需 Dockerfile 或 Space 管理
- **硬件选择**：为评估作业配置 CPU 或 GPU 硬件
- **安全执行**：通过 CLI 传递的 secrets 安全处理 API 令牌

## 5. 使用 vLLM 运行自定义模型评估（新增）

⚠️ **重要：** 此方法仅适用于安装了 `uv` 且具有足够 GPU 内存的设备。
**优势：** 无需使用 `hf_jobs()` MCP 工具，可直接在终端运行脚本
**适用场景：** 用户在本地设备上工作且 GPU 可用

### 运行脚本前

- 检查脚本路径
- 检查 uv 是否已安装
- 使用 `nvidia-smi` 检查 GPU 是否可用

### 运行脚本

```bash
uv run scripts/train_sft_example.py
```

### 特性

- **vLLM 后端**：高性能 GPU 推理（比标准 HF 方法快 5-10 倍）
- **lighteval 框架**：HuggingFace 的评估库，支持 Open LLM Leaderboard 任务
- **inspect-ai 框架**：英国 AI 安全研究所的评估库
- **独立或 Jobs**：本地运行或提交到 HF Jobs 基础设施

# 使用说明

本技能在 `scripts/` 目录中包含执行操作的 Python 脚本。

### 前置条件

- 推荐：使用 `uv run`（PEP 723 头自动安装依赖）
- 或手动安装：`pip install huggingface-hub markdown-it-py python-dotenv pyyaml requests`
- 使用具有写入权限的令牌设置 `HF_TOKEN` 环境变量
- 对于 Artificial Analysis：设置 `AA_API_KEY` 环境变量
- 如果安装了 `python-dotenv`，会自动加载 `.env`

### 方法 1：从 README 提取（CLI 工作流）

推荐流程（与 `--help` 一致）：
```bash
# 1) 检查表格以获取表格编号和列提示
uv run scripts/evaluation_manager.py inspect-tables --repo-id "username/model"

# 2) 提取特定表格（默认打印 YAML）
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "username/model" \
  --table 1 \
  [--model-column-index <inspect-tables 显示的列索引>] \
  [--model-name-override "<列标题/模型名称>"]  # 如果无法使用索引，请使用精确标题文本

# 3) 应用更改（推送或 PR）
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "username/model" \
  --table 1 \
  --apply       # 直接推送
# 或
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "username/model" \
  --table 1 \
  --create-pr   # 打开 PR
```

验证清单：
- 默认打印 YAML；应用前与 README 表格对比
- 优先使用 `--model-column-index`；如果使用 `--model-name-override`，列标题文本必须精确
- 对于转置表格（模型作为行），确保只提取一行

### 方法 2：从 Artificial Analysis 导入

从 Artificial Analysis API 获取基准测试分数并添加到模型卡。

**基本用法：**
```bash
AA_API_KEY="your-api-key" uv run scripts/evaluation_manager.py import-aa \
  --creator-slug "anthropic" \
  --model-name "claude-sonnet-4" \
  --repo-id "username/model-name"
```

**使用环境文件：**
```bash
# 创建 .env 文件
echo "AA_API_KEY=your-api-key" >> .env
echo "HF_TOKEN=your-hf-token" >> .env

# 运行导入
uv run scripts/evaluation_manager.py import-aa \
  --creator-slug "anthropic" \
  --model-name "claude-sonnet-4" \
  --repo-id "username/model-name"
```

**创建拉取请求：**
```bash
uv run scripts/evaluation_manager.py import-aa \
  --creator-slug "anthropic" \
  --model-name "claude-sonnet-4" \
  --repo-id "username/model-name" \
  --create-pr
```

### 方法 3：运行评估作业

使用 `hf jobs uv run` CLI 在 Hugging Face 基础设施上提交评估作业。

**直接 CLI 用法：**
```bash
HF_TOKEN=$HF_TOKEN \
hf jobs uv run hf-evaluation/scripts/inspect_eval_uv.py \
  --flavor cpu-basic \
  --secret HF_TOKEN=$HF_TOKEN \
  -- --model "meta-llama/Llama-2-7b-hf" \
     --task "mmlu"
```

**GPU 示例（A10G）：**
```bash
HF_TOKEN=$HF_TOKEN \
hf jobs uv run hf-evaluation/scripts/inspect_eval_uv.py \
  --flavor a10g-small \
  --secret HF_TOKEN=$HF_TOKEN \
  -- --model "meta-llama/Llama-2-7b-hf" \
     --task "gsm8k"
```

**Python 辅助脚本（可选）：**
```bash
uv run scripts/run_eval_job.py \
  --model "meta-llama/Llama-2-7b-hf" \
  --task "mmlu" \
  --hardware "t4-small"
```

### 方法 4：使用 vLLM 运行自定义模型评估

使用 vLLM 或 accelerate 后端直接在 GPU 上评估自定义 HuggingFace 模型。这些脚本**独立于推理提供商脚本**，在作业硬件上本地运行模型。

#### vLLM 评估适用场景（对比推理提供商）

| 特性 | vLLM 脚本 | 推理提供商脚本 |
|------|----------|---------------|
| 模型访问 | 任意 HF 模型 | 具有 API 端点的模型 |
| 硬件 | 您的 GPU（或 HF Jobs GPU） | 提供商的基础设施 |
| 成本 | HF Jobs 计算成本 | API 使用费 |
| 速度 | vLLM 优化 | 取决于提供商 |
| 离线 | 是（下载后） | 否 |

#### 选项 A：使用 vLLM 后端的 lighteval

lighteval 是 HuggingFace 的评估库，支持 Open LLM Leaderboard 任务。

**独立运行（本地 GPU）：**
```bash
# 使用 vLLM 运行 MMLU 5-shot
uv run scripts/lighteval_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --tasks "leaderboard|mmlu|5"

# 运行多个任务
uv run scripts/lighteval_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --tasks "leaderboard|mmlu|5,leaderboard|gsm8k|5"

# 使用 accelerate 后端而非 vLLM
uv run scripts/lighteval_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --tasks "leaderboard|mmlu|5" \
  --backend accelerate

# 聊天/指令微调模型
uv run scripts/lighteval_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B-Instruct \
  --tasks "leaderboard|mmlu|5" \
  --use-chat-template
```

**通过 HF Jobs：**
```bash
hf jobs uv run scripts/lighteval_vllm_uv.py \
  --flavor a10g-small \
  --secrets HF_TOKEN=$HF_TOKEN \
  -- --model meta-llama/Llama-3.2-1B \
     --tasks "leaderboard|mmlu|5"
```

**lighteval 任务格式：**
任务使用 `suite|task|num_fewshot` 格式：
- `leaderboard|mmlu|5` - MMLU 5-shot
- `leaderboard|gsm8k|5` - GSM8K 5-shot
- `lighteval|hellaswag|0` - HellaSwag zero-shot
- `leaderboard|arc_challenge|25` - ARC-Challenge 25-shot

**查找可用任务：**
完整的 lighteval 任务列表可在以下位置找到：
https://github.com/huggingface/lighteval/blob/main/examples/tasks/all_tasks.txt

此文件包含所有支持的任务，格式为 `suite|task|num_fewshot|0`（末尾的 `0` 是版本标志，可忽略）。常见套件包括：
- `leaderboard` - Open LLM Leaderboard 任务（MMLU、GSM8K、ARC、HellaSwag 等）
- `lighteval` - 其他 lighteval 任务
- `bigbench` - BigBench 任务
- `original` - 原始基准测试任务

要使用列表中的任务，提取 `suite|task|num_fewshot` 部分（不含末尾的 `0`）并传递给 `--tasks` 参数。例如：
- 文件中：`leaderboard|mmlu|0` → 使用：`leaderboard|mmlu|0`（或改为 `5` 进行 5-shot）
- 文件中：`bigbench|abstract_narrative_understanding|0` → 使用：`bigbench|abstract_narrative_understanding|0`
- 文件中：`lighteval|wmt14:hi-en|0` → 使用：`lighteval|wmt14:hi-en|0`

多个任务可用逗号分隔：`--tasks "leaderboard|mmlu|5,leaderboard|gsm8k|5"`

#### 选项 B：使用 vLLM 后端的 inspect-ai

inspect-ai 是英国 AI 安全研究所的评估框架。

**独立运行（本地 GPU）：**
```bash
# 使用 vLLM 运行 MMLU
uv run scripts/inspect_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --task mmlu

# 使用 HuggingFace Transformers 后端
uv run scripts/inspect_vllm_uv.py \
  --model meta-llama/Llama-3.2-1B \
  --task mmlu \
  --backend hf

# 多 GPU 张量并行
uv run scripts/inspect_vllm_uv.py \
  --model meta-llama/Llama-3.2-70B \
  --task mmlu \
  --tensor-parallel-size 4
```

**通过 HF Jobs：**
```bash
hf jobs uv run scripts/inspect_vllm_uv.py \
  --flavor a10g-small \
  --secrets HF_TOKEN=$HF_TOKEN \
  -- --model meta-llama/Llama-3.2-1B \
     --task mmlu
```

**可用的 inspect-ai 任务：**
- `mmlu` - 大规模多任务语言理解
- `gsm8k` - 小学数学
- `hellaswag` - 常识推理
- `arc_challenge` - AI2 推理挑战
- `truthfulqa` - TruthfulQA 基准测试
- `winogrande` - Winograd 模式挑战
- `humaneval` - 代码生成

#### 选项 C：Python 辅助脚本

辅助脚本自动选择硬件并简化作业提交：

```bash
# 根据模型大小自动检测硬件
uv run scripts/run_vllm_eval_job.py \
  --model meta-llama/Llama-3.2-1B \
  --task "leaderboard|mmlu|5" \
  --framework lighteval

# 显式选择硬件
uv run scripts/run_vllm_eval_job.py \
  --model meta-llama/Llama-3.2-70B \
  --task mmlu \
  --framework inspect \
  --hardware a100-large \
  --tensor-parallel-size 4

# 使用 HF Transformers 后端
uv run scripts/run_vllm_eval_job.py \
  --model microsoft/phi-2 \
  --task mmlu \
  --framework inspect \
  --backend hf
```

**硬件推荐：**
| 模型大小 | 推荐硬件 |
|---------|---------|
| < 3B 参数 | `t4-small` |
| 3B - 13B | `a10g-small` |
| 13B - 34B | `a10g-large` |
| 34B+ | `a100-large` |

### 命令参考

**顶级帮助和版本：**
```bash
uv run scripts/evaluation_manager.py --help
uv run scripts/evaluation_manager.py --version
```

**检查表格（从这里开始）：**
```bash
uv run scripts/evaluation_manager.py inspect-tables --repo-id "username/model-name"
```

**从 README 提取：**
```bash
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "username/model-name" \
  --table N \
  [--model-column-index N] \
  [--model-name-override "精确列标题或模型名称"] \
  [--task-type "text-generation"] \
  [--dataset-name "自定义基准测试"] \
  [--apply | --create-pr]
```

**从 Artificial Analysis 导入：**
```bash
AA_API_KEY=... uv run scripts/evaluation_manager.py import-aa \
  --creator-slug "creator-name" \
  --model-name "model-slug" \
  --repo-id "username/model-name" \
  [--create-pr]
```

**查看/验证：**
```bash
uv run scripts/evaluation_manager.py show --repo-id "username/model-name"
uv run scripts/evaluation_manager.py validate --repo-id "username/model-name"
```

**检查开放 PR（使用 --create-pr 前务必运行）：**
```bash
uv run scripts/evaluation_manager.py get-prs --repo-id "username/model-name"
```
列出模型仓库的所有开放拉取请求。显示 PR 编号、标题、作者、日期和 URL。

**运行评估作业（推理提供商）：**
```bash
hf jobs uv run scripts/inspect_eval_uv.py \
  --flavor "cpu-basic|t4-small|..." \
  --secret HF_TOKEN=$HF_TOKEN \
  -- --model "model-id" \
     --task "task-name"
```

或使用 Python 辅助脚本：

```bash
uv run scripts/run_eval_job.py \
  --model "model-id" \
  --task "task-name" \
  --hardware "cpu-basic|t4-small|..."
```

**运行 vLLM 评估（自定义模型）：**
```bash
# 使用 vLLM 的 lighteval
hf jobs uv run scripts/lighteval_vllm_uv.py \
  --flavor "a10g-small" \
  --secrets HF_TOKEN=$HF_TOKEN \
  -- --model "model-id" \
     --tasks "leaderboard|mmlu|5"

# 使用 vLLM 的 inspect-ai
hf jobs uv run scripts/inspect_vllm_uv.py \
  --flavor "a10g-small" \
  --secrets HF_TOKEN=$HF_TOKEN \
  -- --model "model-id" \
     --task "mmlu"

# 辅助脚本（自动硬件选择）
uv run scripts/run_vllm_eval_job.py \
  --model "model-id" \
  --task "leaderboard|mmlu|5" \
  --framework lighteval
```

### Model-Index 格式

生成的 model-index 遵循以下结构：

```yaml
model-index:
  - name: Model Name
    results:
      - task:
          type: text-generation
        dataset:
          name: Benchmark Dataset
          type: benchmark_type
        metrics:
          - name: MMLU
            type: mmlu
            value: 85.2
          - name: HumanEval
            type: humaneval
            value: 72.5
        source:
          name: Source Name
          url: https://source-url.com
```

警告：不要在模型名称中使用 markdown 格式。使用表格中的确切名称。仅在 source.url 字段中使用 url。

### 错误处理

- **未找到表格**：脚本会报告是否未检测到评估表格
- **格式无效**：为格式错误的表格提供清晰的错误消息
- **API 错误**：针对 Artificial Analysis API 临时故障的重试逻辑
- **令牌问题**：尝试更新前进行验证
- **合并冲突**：添加新条目时保留现有 model-index 条目
- **Space 创建**：优雅处理命名冲突和硬件请求失败

### 最佳实践

1. **首先检查现有 PR**：创建任何新 PR 前运行 `get-prs` 以避免重复
2. **始终从 `inspect-tables` 开始**：查看表格结构并获取正确的提取命令
3. **使用 `--help` 获取指导**：运行 `inspect-tables --help` 查看完整工作流
4. **先预览**：默认行为打印 YAML；使用 `--apply` 或 `--create-pr` 前先查看
5. **验证提取的值**：手动将 YAML 输出与 README 表格对比
6. **对多表格 README 使用 `--table N`**：存在多个评估表格时必需
7. **对对比表格使用 `--model-name-override`**：从 `inspect-tables` 输出复制精确列标题
8. **为他人的模型创建 PR**：更新不属于自己的模型时使用 `--create-pr`
9. **每个仓库一个模型**：仅将主模型的结果添加到 model-index
10. **YAML 名称中不使用 markdown**：YAML 中的模型名称字段应为纯文本

### 模型名称匹配

提取包含多个模型的评估表格（作为列或行）时，脚本使用**精确规范化令牌匹配**：

- 移除 markdown 格式（粗体 `**`、链接 `[]()`）
- 规范化名称（小写，用空格替换 `-` 和 `_`）
- 比较令牌集：`"OLMo-3-32B"` → `{"olmo", "3", "32b"}` 匹配 `"**Olmo 3 32B**"` 或 `"Olmo-3-32B`
- 仅在令牌完全匹配时提取（处理不同的词序和分隔符）
- 如果未找到精确匹配则失败（而不是从相似名称猜测）

**对于基于列的表格**（基准测试作为行，模型作为列）：
- 查找匹配模型名称的列标题
- 仅从该列提取分数

**对于转置表格**（模型作为行，基准测试作为列）：
- 在第一列查找匹配模型名称的行
- 仅从该行提取所有基准测试分数

这确保只提取正确模型的分数，不会提取不相关的模型或训练检查点。

### 常见模式

**更新自己的模型：**
```bash
# 从 README 提取并直接推送
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "your-username/your-model" \
  --task-type "text-generation"
```

**更新他人的模型（完整工作流）：**
```bash
# 步骤 1：始终先检查现有 PR
uv run scripts/evaluation_manager.py get-prs \
  --repo-id "other-username/their-model"

# 步骤 2：如果不存在开放 PR，继续创建
uv run scripts/evaluation_manager.py extract-readme \
  --repo-id "other-username/their-model" \
  --create-pr

# 如果存在开放 PR：
# - 警告用户存在现有 PR
# - 向用户展示 PR URL
# - 除非用户明确确认，否则不要创建新 PR
```

**导入最新基准测试：**
```bash
# 步骤 1：检查现有 PR
uv run scripts/evaluation_manager.py get-prs \
  --repo-id "anthropic/claude-sonnet-4"

# 步骤 2：如果没有 PR，从 Artificial Analysis 导入
AA_API_KEY=... uv run scripts/evaluation_manager.py import-aa \
  --creator-slug "anthropic" \
  --model-name "claude-sonnet-4" \
  --repo-id "anthropic/claude-sonnet-4" \
  --create-pr
```

### 故障排除

**问题**："No evaluation tables found in README"
- **解决方案**：检查 README 是否包含带数字分数的 markdown 表格

**问题**："Could not find model 'X' in transposed table"
- **解决方案**：脚本会显示可用模型。使用列表中的确切名称配合 `--model-name-override`
- **示例**：`--model-name-override "**Olmo 3-32B**"`

**问题**："AA_API_KEY not set"
- **解决方案**：设置环境变量或添加到 .env 文件

**问题**："Token does not have write access"
- **解决方案**：确保 HF_TOKEN 对仓库具有写入权限

**问题**："Model not found in Artificial Analysis"
- **解决方案**：验证 creator-slug 和 model-name 与 API 值匹配

**问题**："Payment required for hardware"
- **解决方案**：在 Hugging Face 账户中添加付款方式以使用非 CPU 硬件

**问题**："vLLM out of memory" 或 CUDA OOM
- **解决方案**：使用更大的硬件规格，降低 `--gpu-memory-utilization`，或使用 `--tensor-parallel-size` 进行多 GPU

**问题**："Model architecture not supported by vLLM"
- **解决方案**：对 HuggingFace Transformers 使用 `--backend hf`（inspect-ai）或 `--backend accelerate`（lighteval）

**问题**："Trust remote code required"
- **解决方案**：对具有自定义代码的模型添加 `--trust-remote-code` 标志（如 Phi-2、Qwen）

**问题**："Chat template not found"
- **解决方案**：仅对包含聊天模板的指令微调模型使用 `--use-chat-template`

### 集成示例

**Python 脚本集成：**
```python
import subprocess
import os

def update_model_evaluations(repo_id, readme_content):
    """使用 README 中的评估更新模型卡。"""
    result = subprocess.run([
        "python", "scripts/evaluation_manager.py",
        "extract-readme",
        "--repo-id", repo_id,
        "--create-pr"
    ], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"Successfully updated {repo_id}")
    else:
        print(f"Error: {result.stderr}")
```

## 局限性

- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
