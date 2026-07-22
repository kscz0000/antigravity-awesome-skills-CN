---
name: hugging-face-datasets
description: 在 Hugging Face Hub 上创建和管理数据集。支持初始化仓库、定义配置/系统提示词、流式行更新以及基于 SQL 的数据集查询/转换。设计用于与 HF MCP 服务器配合，提供完整的数据集工作流。
risk: unknown
source: community
---

# 概述

本技能提供在 Hugging Face Hub 上管理数据集的工具，专注于创建、配置、内容管理和基于 SQL 的数据操作。它是对现有 Hugging Face MCP 服务器的补充，提供数据集编辑和查询能力。

## 适用场景

- 需要在 Hugging Face Hub 上创建、配置或更新数据集
- 需要对 Hub 数据集进行 SQL 风格的查询、转换或导出操作
- 直接管理数据集内容和元数据，而非仅搜索现有数据集

## 与 HF MCP 服务器的协作

- **HF MCP 服务器用于**：数据集发现、搜索和元数据检索
- **本技能用于**：数据集创建、内容编辑、SQL 查询、数据转换和结构化数据格式化

# 版本

2.1.0

# 依赖

# 本技能使用 PEP 723 脚本，支持内联依赖管理
# 脚本运行时自动安装依赖：uv run scripts/script_name.py

- uv（Python 包管理器）
- 入门指南：见下方"使用说明"了解 PEP 723 用法

# 核心能力

## 1. 数据集生命周期管理

- **初始化**：创建具有正确结构的新数据集仓库
- **配置**：存储详细配置，包括系统提示词和元数据
- **流式更新**：高效添加行数据，无需下载整个数据集

## 2. 基于 SQL 的数据集查询（新功能）

通过 `scripts/sql_manager.py` 使用 DuckDB SQL 查询任意 Hugging Face 数据集：

- **直接查询**：使用 `hf://` 协议对数据集运行 SQL
- **模式发现**：描述数据集结构和列类型
- **数据采样**：获取随机样本进行探索
- **聚合分析**：计数、直方图、唯一值分析
- **数据转换**：使用 SQL 进行过滤、连接、重塑
- **导出与推送**：保存结果到本地或推送到新的 Hub 仓库

## 3. 多格式数据集支持

通过模板系统支持多种数据集类型：

- **对话/聊天**：聊天模板、多轮对话、工具使用示例
- **文本分类**：情感分析、意图检测、主题分类
- **问答系统**：阅读理解、事实问答、知识库
- **文本补全**：语言建模、代码补全、创意写作
- **表格数据**：用于回归/分类任务的结构化数据
- **自定义格式**：为特定需求定义灵活的模式

## 4. 质量保证功能

- **JSON 验证**：确保上传过程中的数据完整性
- **批量处理**：高效处理大型数据集
- **错误恢复**：优雅处理上传失败和冲突

# 使用说明

本技能包含两个使用 PEP 723 内联依赖管理的 Python 脚本：

> **所有路径相对于包含此 SKILL.md 文件的目录。**
> 脚本运行方式：`uv run scripts/script_name.py [参数]`

- `scripts/dataset_manager.py` - 数据集创建和管理
- `scripts/sql_manager.py` - 基于 SQL 的数据集查询和转换

### 前置条件

- 已安装 `uv` 包管理器
- 必须设置 `HF_TOKEN` 环境变量，使用具有写入权限的令牌

---

# SQL 数据集查询 (sql_manager.py)

使用 DuckDB SQL 查询、转换和推送 Hugging Face 数据集。`hf://` 协议提供对任意公共数据集的直接访问（私有数据集需要令牌）。

## 快速开始

```bash
# 查询数据集
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject='nutrition' LIMIT 10"

# 获取数据集模式
uv run scripts/sql_manager.py describe --dataset "cais/mmlu"

# 随机采样
uv run scripts/sql_manager.py sample --dataset "cais/mmlu" --n 5

# 带条件计数
uv run scripts/sql_manager.py count --dataset "cais/mmlu" --where "subject='nutrition'"
```

## SQL 查询语法

在 SQL 中使用 `data` 作为表名——它会被替换为实际的 `hf://` 路径：

```sql
-- 基本查询
SELECT * FROM data LIMIT 10

-- 过滤
SELECT * FROM data WHERE subject='nutrition'

-- 聚合
SELECT subject, COUNT(*) as cnt FROM data GROUP BY subject ORDER BY cnt DESC

-- 列选择和转换
SELECT question, choices[answer] AS correct_answer FROM data

-- 正则匹配
SELECT * FROM data WHERE regexp_matches(question, 'nutrition|diet')

-- 字符串函数
SELECT regexp_replace(question, '\n', '') AS cleaned FROM data
```

## 常用操作

### 1. 探索数据集结构

```bash
# 获取模式
uv run scripts/sql_manager.py describe --dataset "cais/mmlu"

# 获取列中的唯一值
uv run scripts/sql_manager.py unique --dataset "cais/mmlu" --column "subject"

# 获取值分布
uv run scripts/sql_manager.py histogram --dataset "cais/mmlu" --column "subject" --bins 20
```

### 2. 过滤和转换

```bash
# 使用 SQL 进行复杂过滤
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --sql "SELECT subject, COUNT(*) as cnt FROM data GROUP BY subject HAVING cnt > 100"

# 使用 transform 命令
uv run scripts/sql_manager.py transform \
  --dataset "cais/mmlu" \
  --select "subject, COUNT(*) as cnt" \
  --group-by "subject" \
  --order-by "cnt DESC" \
  --limit 10
```

### 3. 创建子集并推送到 Hub

```bash
# 查询并推送到新数据集
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject='nutrition'" \
  --push-to "username/mmlu-nutrition-subset" \
  --private

# 转换并推送
uv run scripts/sql_manager.py transform \
  --dataset "ibm/duorc" \
  --config "ParaphraseRC" \
  --select "question, answers" \
  --where "LENGTH(question) > 50" \
  --push-to "username/duorc-long-questions"
```

### 4. 导出到本地文件

```bash
# 导出为 Parquet
uv run scripts/sql_manager.py export \
  --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject='nutrition'" \
  --output "nutrition.parquet" \
  --format parquet

# 导出为 JSONL
uv run scripts/sql_manager.py export \
  --dataset "cais/mmlu" \
  --sql "SELECT * FROM data LIMIT 100" \
  --output "sample.jsonl" \
  --format jsonl
```

### 5. 使用数据集配置/分割

```bash
# 指定配置（子集）
uv run scripts/sql_manager.py query \
  --dataset "ibm/duorc" \
  --config "ParaphraseRC" \
  --sql "SELECT * FROM data LIMIT 5"

# 指定分割
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --split "test" \
  --sql "SELECT COUNT(*) FROM data"

# 查询所有分割
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --split "*" \
  --sql "SELECT * FROM data LIMIT 10"
```

### 6. 使用完整路径的原始 SQL

用于复杂查询或连接数据集：

```bash
uv run scripts/sql_manager.py raw --sql "
  SELECT a.*, b.* 
  FROM 'hf://datasets/dataset1@~parquet/default/train/*.parquet' a
  JOIN 'hf://datasets/dataset2@~parquet/default/train/*.parquet' b
  ON a.id = b.id
  LIMIT 100
"
```

## Python API 用法

```python
from sql_manager import HFDatasetSQL

sql = HFDatasetSQL()

# 查询
results = sql.query("cais/mmlu", "SELECT * FROM data WHERE subject='nutrition' LIMIT 10")

# 获取模式
schema = sql.describe("cais/mmlu")

# 采样
samples = sql.sample("cais/mmlu", n=5, seed=42)

# 计数
count = sql.count("cais/mmlu", where="subject='nutrition'")

# 直方图
dist = sql.histogram("cais/mmlu", "subject")

# 过滤和转换
results = sql.filter_and_transform(
    "cais/mmlu",
    select="subject, COUNT(*) as cnt",
    group_by="subject",
    order_by="cnt DESC",
    limit=10
)

# 推送到 Hub
url = sql.push_to_hub(
    "cais/mmlu",
    "username/nutrition-subset",
    sql="SELECT * FROM data WHERE subject='nutrition'",
    private=True
)

# 导出到本地
sql.export_to_parquet("cais/mmlu", "output.parquet", sql="SELECT * FROM data LIMIT 100")

sql.close()
```

## HF 路径格式

DuckDB 使用 `hf://` 协议访问数据集：

```
hf://datasets/{dataset_id}@{revision}/{config}/{split}/*.parquet
```

示例：

- `hf://datasets/cais/mmlu@~parquet/default/train/*.parquet`
- `hf://datasets/ibm/duorc@~parquet/ParaphraseRC/test/*.parquet`

`@~parquet` 修订版为任意数据集格式提供自动转换的 Parquet 文件。

## 实用 DuckDB SQL 函数

```sql
-- 字符串函数
LENGTH(column)                    -- 字符串长度
regexp_replace(col, '\n', '')     -- 正则替换
regexp_matches(col, 'pattern')    -- 正则匹配
LOWER(col), UPPER(col)           -- 大小写转换

-- 数组函数  
choices[0]                        -- 数组索引（从 0 开始）
array_length(choices)             -- 数组长度
unnest(choices)                   -- 将数组展开为行

-- 聚合函数
COUNT(*), SUM(col), AVG(col)
GROUP BY col HAVING condition

-- 采样
USING SAMPLE 10                   -- 随机采样
USING SAMPLE 10 (RESERVOIR, 42)   -- 可复现采样

-- 窗口函数
ROW_NUMBER() OVER (PARTITION BY col ORDER BY col2)
```

---

# 数据集创建 (dataset_manager.py)

### 推荐工作流

**1. 发现（使用 HF MCP 服务器）：**

```python
# 使用 HF MCP 工具查找现有数据集
search_datasets("conversational AI training")
get_dataset_details("username/dataset-name")
```

**2. 创建（使用本技能）：**

```bash
# 初始化新数据集
uv run scripts/dataset_manager.py init --repo_id "your-username/dataset-name" [--private]

# 配置详细的系统提示词
uv run scripts/dataset_manager.py config --repo_id "your-username/dataset-name" --system_prompt "$(cat system_prompt.txt)"
```

**3. 内容管理（使用本技能）：**

```bash
# 使用任意模板快速设置
uv run scripts/dataset_manager.py quick_setup \
  --repo_id "your-username/dataset-name" \
  --template classification

# 使用模板验证添加数据
uv run scripts/dataset_manager.py add_rows \
  --repo_id "your-username/dataset-name" \
  --template qa \
  --rows_json "$(cat your_qa_data.json)"
```

### 基于模板的数据结构

**1. 聊天模板 (`--template chat`)**

```json
{
  "messages": [
    {"role": "user", "content": "自然用户请求"},
    {"role": "assistant", "content": "带工具使用的响应"},
    {"role": "tool", "content": "工具响应", "tool_call_id": "call_123"}
  ],
  "scenario": "用例描述",
  "complexity": "simple|intermediate|advanced"
}
```

**2. 分类模板 (`--template classification`)**

```json
{
  "text": "待分类的输入文本",
  "label": "分类标签",
  "confidence": 0.95,
  "metadata": {"domain": "technology", "language": "en"}
}
```

**3. 问答模板 (`--template qa`)**

```json
{
  "question": "问题内容是什么？",
  "answer": "完整答案",
  "context": "额外上下文（如需要）",
  "answer_type": "factual|explanatory|opinion",
  "difficulty": "easy|medium|hard"
}
```

**4. 补全模板 (`--template completion`)**

```json
{
  "prompt": "起始文本或上下文",
  "completion": "预期的续写内容",
  "domain": "code|creative|technical|conversational",
  "style": "写作风格描述"
}
```

**5. 表格模板 (`--template tabular`)**

```json
{
  "columns": [
    {"name": "feature1", "type": "numeric", "description": "第一个特征"},
    {"name": "target", "type": "categorical", "description": "目标变量"}
  ],
  "data": [
    {"feature1": 123, "target": "class_a"},
    {"feature1": 456, "target": "class_b"}
  ]
}
```

### 高级系统提示词模板

用于生成高质量训练数据：

```text
你是一个擅长有效使用 MCP 工具的 AI 助手。

## MCP 服务器定义
[定义可用的服务器和工具]

## 训练示例结构
[指定聊天模板的确切 JSON 模式]

## 质量指南
[详细说明真实场景、渐进复杂度、正确工具使用的要求]

## 示例类别
[列出开发工作流、调试场景、数据管理任务]
```

### 示例类别与模板

本技能包含超越 MCP 使用的多样化训练示例：

**可用示例集：**

- `training_examples.json` - MCP 工具使用示例（调试、项目设置、数据库分析）
- `diverse_training_examples.json` - 更广泛的场景，包括：
  - **教育对话** - 解释编程概念、教程
  - **Git 工作流** - 功能分支、版本控制指导
  - **代码分析** - 性能优化、架构评审
  - **内容生成** - 专业写作、创意头脑风暴
  - **代码库导航** - 遗留代码探索、系统分析
  - **对话支持** - 问题解决、技术讨论

**使用不同示例集：**

```bash
# 添加 MCP 专注示例
uv run scripts/dataset_manager.py add_rows --repo_id "your-username/dataset-name" \
  --rows_json "$(cat examples/training_examples.json)"

# 添加多样化对话示例
uv run scripts/dataset_manager.py add_rows --repo_id "your-username/dataset-name" \
  --rows_json "$(cat examples/diverse_training_examples.json)"

# 混合两者以获得全面的训练数据
uv run scripts/dataset_manager.py add_rows --repo_id "your-username/dataset-name" \
  --rows_json "$(jq -s '.[0] + .[1]' examples/training_examples.json examples/diverse_training_examples.json)"
```

### 命令参考

**列出可用模板：**

```bash
uv run scripts/dataset_manager.py list_templates
```

**快速设置（推荐）：**

```bash
uv run scripts/dataset_manager.py quick_setup --repo_id "your-username/dataset-name" --template classification
```

**手动设置：**

```bash
# 初始化仓库
uv run scripts/dataset_manager.py init --repo_id "your-username/dataset-name" [--private]

# 配置系统提示词
uv run scripts/dataset_manager.py config --repo_id "your-username/dataset-name" --system_prompt "你的提示词"

# 带验证添加数据
uv run scripts/dataset_manager.py add_rows \
  --repo_id "your-username/dataset-name" \
  --template qa \
  --rows_json '[{"question": "什么是 AI？", "answer": "人工智能..."}]'
```

**查看数据集统计：**

```bash
uv run scripts/dataset_manager.py stats --repo_id "your-username/dataset-name"
```

### 错误处理

- **仓库已存在**：脚本会通知并继续配置
- **无效 JSON**：显示清晰的错误信息和解析详情
- **网络问题**：对临时故障自动重试
- **令牌权限**：操作开始前进行验证

---

# 组合工作流示例

## 示例 1：从现有数据集创建训练子集

```bash
# 1. 探索源数据集
uv run scripts/sql_manager.py describe --dataset "cais/mmlu"
uv run scripts/sql_manager.py histogram --dataset "cais/mmlu" --column "subject"

# 2. 查询并创建子集
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject IN ('nutrition', 'anatomy', 'clinical_knowledge')" \
  --push-to "username/mmlu-medical-subset" \
  --private
```

## 示例 2：转换和重塑数据

```bash
# 将 MMLU 转换为问答格式，提取正确答案
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --sql "SELECT question, choices[answer] as correct_answer, subject FROM data" \
  --push-to "username/mmlu-qa-format"
```

## 示例 3：合并多个数据集分割

```bash
# 导出多个分割并合并
uv run scripts/sql_manager.py export \
  --dataset "cais/mmlu" \
  --split "*" \
  --output "mmlu_all.parquet"
```

## 示例 4：质量过滤

```bash
# 过滤高质量示例
uv run scripts/sql_manager.py query \
  --dataset "squad" \
  --sql "SELECT * FROM data WHERE LENGTH(context) > 500 AND LENGTH(question) > 20" \
  --push-to "username/squad-filtered"
```

## 示例 5：创建自定义训练数据集

```bash
# 1. 查询源数据
uv run scripts/sql_manager.py export \
  --dataset "cais/mmlu" \
  --sql "SELECT question, subject FROM data WHERE subject='nutrition'" \
  --output "nutrition_source.jsonl" \
  --format jsonl

# 2. 使用你的流程处理（添加答案、格式化等）

# 3. 推送处理后的数据
uv run scripts/dataset_manager.py init --repo_id "username/nutrition-training"
uv run scripts/dataset_manager.py add_rows \
  --repo_id "username/nutrition-training" \
  --template qa \
  --rows_json "$(cat processed_data.json)"
```

## 限制

- 仅在任务明确匹配上述范围时使用本技能
- 输出不应替代特定环境的验证、测试或专家评审
- 如果缺少必要输入、权限、安全边界或成功标准，请停止并请求澄清
