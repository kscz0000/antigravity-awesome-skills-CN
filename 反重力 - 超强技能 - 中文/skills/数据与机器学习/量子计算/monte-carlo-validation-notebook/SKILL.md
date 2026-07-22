---
name: monte-carlo-validation-notebook
description: "为 dbt PR 变更生成 SQL 验证 Notebook，包含前后对比查询。当用户要求'为 dbt 变更生成验证 Notebook'或'验证 dbt 模型变更'时使用。"
category: data
risk: safe
source: community
source_repo: monte-carlo-data/mc-agent-toolkit
source_type: community
date_added: "2026-04-08"
author: monte-carlo-data
tags: [data-observability, validation, dbt, monte-carlo, sql-notebook]
tools: [claude, cursor, codex]
---

> **提示：** 此技能与 Sonnet 配合良好。调用前运行 `/model sonnet` 可加快生成速度。

生成包含 dbt 变更验证查询的 SQL Notebook。

**参数：** $ARGUMENTS

## 使用场景

当用户希望通过 Monte Carlo SQL Notebook 查询来验证 dbt 模型或快照变更时使用此技能，无论是来自 GitHub PR 还是本地 dbt 仓库。

解析参数：
- **Target**（必需）：第一个参数 — GitHub PR URL 或本地 dbt 仓库路径
- **MC Base URL**（可选）：`--mc-base-url <URL>` — 默认值为 `https://getmontecarlo.com`
- **Models**（可选）：`--models <model1,model2,...>` — 逗号分隔的模型文件名列表（不带 `.sql` 扩展名），仅生成这些模型的查询。默认情况下，包含所有已变更的模型，最多 10 个。

---

# 设置

**前置条件：**
- **`gh`**（GitHub CLI）— PR 模式必需。必须已认证（`gh auth status`）。
- **`python3`** — 辅助脚本必需。
- **`pyyaml`** — 通过 `pip3 install pyyaml` 安装（或 `pip install pyyaml`、`uv pip install pyyaml` 等）

**注意：** 生成的 SQL 使用 ANSI 兼容语法，可在 Snowflake、BigQuery、Redshift 和 Athena 上运行。针对特定数据仓库的差异可能需要微调。

此技能在 `${CLAUDE_PLUGIN_ROOT}/skills/monte-carlo-validation-notebook/scripts/` 中包含两个辅助脚本：

- **`resolve_dbt_schema.py`** - 从 `dbt_project.yml` 路由规则和模型配置覆盖中解析 dbt 模型输出 schema。
- **`generate_notebook_url.py`** - 将 notebook YAML 编码为 base64 导入 URL 并在浏览器中打开。

# 模式检测

根据 target 参数自动检测模式：
- 如果 target 看起来像 URL（包含 `://` 或 `github.com`）-> **PR 模式**
- 如果 target 是路径（`.`、`/path/to/repo`、相对路径）-> **本地模式**

---

# 上下文

此命令生成包含 dbt 变更验证查询的 SQL Notebook。Notebook 可在 MC Bridge SQL Notebook 界面中打开进行交互式验证。

输出是一个可直接在 notebook 界面中打开的导入 URL：
```
<MC_BASE_URL>/notebooks/import#<base64-encoded-yaml>
```

**核心特性：**
- **数据库参数**：两个 `text` 参数（`prod_db` 和 `dev_db`）用于选择数据库
- **Schema 推断**：自动从 `dbt_project.yml` 和模型配置中推断每个模型的 schema
- **单表查询**：使用 `{{prod_db}}.<SCHEMA>.<TABLE>` 的基础验证查询
- **对比查询**：比较 `{{prod_db}}` 与 `{{dev_db}}` 的前后对比查询
- **灵活使用**：用户可将两个参数设置为同一数据库以进行单库分析

# Notebook YAML 规范参考

核心结构：
```yaml
version: 1
metadata:
  id: string           # kebab-case + random suffix
  name: string         # display name
  created_at: string   # ISO 8601
  updated_at: string   # ISO 8601
default_context:       # optional database/schema context
  database: string
  schema: string
cells:
  - id: string
    type: sql | markdown | parameter
    content: string    # SQL, markdown, or parameter config (JSON)
    display_type: table | bar | timeseries
```

## 参数单元格规范

参数单元格允许定义在 SQL 中通过 `{{param_name}}` 语法引用的变量：

```yaml
- id: param-prod-db
  type: parameter
  content:
    name: prod_db              # variable name
    config:
      type: text                   # free-form text input
      default_value: "ANALYTICS"
      placeholder: "Prod database"
  display_type: table
```

参数类型：
- `text`：自由文本输入（用于数据库名称）
- `schema_selector`：两个下拉框（database -> schema），值存储为 `DATABASE.SCHEMA`
- `dropdown`：从预定义选项中选择

# 任务

根据模式和目标生成包含验证查询的 SQL Notebook。

## 阶段 1：获取变更文件

根据模式采用不同方式：

### PR 模式（GitHub PR）：

1. 从目标 URL 中提取 PR 编号和仓库。
   - 示例：`https://github.com/monte-carlo-data/dbt/pull/3386` -> owner=`monte-carlo-data`, repo=`dbt`, PR=`3386`

2. 使用 `gh` 获取 PR 元数据：
```bash
gh pr view <PR#> --repo <owner>/<repo> --json number,title,author,mergedAt,headRefOid
```

3. 获取变更文件列表：
```bash
gh pr view <PR#> --repo <owner>/<repo> --json files --jq '.files[].path'
```

4. 获取 diff：
```bash
gh pr diff <PR#> --repo <owner>/<repo>
```

5. 将变更文件列表过滤为仅 `models/` 或 `snapshots/` 目录下的 `.sql` 文件（任意深度 — 例如 `models/`、`analytics/models/`、`dbt/models/`）。这些是要分析的 dbt 模型。如果没有模型 SQL 文件被变更，报告该情况并停止。

6. 对于每个变更的模型文件，获取 head SHA 处的完整文件内容：
```bash
gh api repos/<owner>/<repo>/contents/<file_path>?ref=<head_sha> --jq '.content' | python3 -c "import sys,base64; sys.stdout.write(base64.b64decode(sys.stdin.read()).decode())"
```

7. **获取 dbt_project.yml** 用于 schema 解析。通过查看变更文件路径检测 dbt 项目根目录 — 找到包含 `dbt_project.yml` 的公共父目录。按以下顺序尝试路径直到成功：
```bash
gh api repos/<owner>/<repo>/contents/<dbt_root>/dbt_project.yml?ref=<head_sha> --jq '.content' | python3 -c "import sys,base64; sys.stdout.write(base64.b64decode(sys.stdin.read()).decode())"
```
常见的 `<dbt_root>` 位置：`analytics`、`.`（仓库根目录）、`dbt`、`transform`。逐一尝试直到找到。

将 `dbt_project.yml` 保存到 `/tmp/validation_notebook_working/<PR#>/dbt_project.yml`。

### 本地模式（本地目录）：

1. 切换到目标目录。

2. 获取当前分支信息：
```bash
git rev-parse --abbrev-ref HEAD
```

3. 检测基础分支 — 按顺序尝试 `main`、`master`、`develop`，或使用上游跟踪分支。

4. 获取与基础分支相比的变更 SQL 文件列表：
```bash
git diff --name-only <base_branch>...HEAD -- '*.sql'
```

5. 过滤为仅 `models/` 或 `snapshots/` 目录下的 `.sql` 文件（任意深度 — 例如 `models/`、`analytics/models/`、`dbt/models/`）。如果没有模型 SQL 文件被变更，报告该情况并停止。

6. 获取每个变更文件的 diff：
```bash
git diff <base_branch>...HEAD -- <file_path>
```

7. 直接从文件系统读取模型文件。

8. **查找 dbt_project.yml**：
```bash
find . -name "dbt_project.yml" -type f | head -1
```

9. 本地模式的 notebook 元数据使用：
   - **ID**：`local-<branch-name>-<timestamp>`
   - **Title**：`Local: <branch-name>`
   - **Author**：`git config user.name` 的输出
   - **Merged**："N/A (local)"

### 模型选择（适用于两种模式）

过滤为 `models/` 或 `snapshots/` 下的 `.sql` 文件后：

1. **如果指定了 `--models`：** 将变更文件列表过滤为仅包含文件名（不带 `.sql` 扩展名，不区分大小写）与指定模型名称之一匹配的模型。如果任何指定模型未在变更文件中找到，警告用户但继续处理找到的模型。如果没有匹配，报告该情况并停止。

2. **模型上限：** 如果过滤后剩余超过 10 个模型，选择前 10 个（按文件路径顺序）并警告用户：
   ```
   ⚠️ <total_count> models changed — generating validation queries for the first 10 only.
   To generate for specific models, re-run with: --models <model1,model2,...>
   Skipped models: <list of skipped model filenames>
   ```

## 阶段 2：解析变更的模型

对于每个变更的 dbt 模型 `.sql` 文件，解析并提取：

### 2a. 模型元数据

**输出表名** -- 从文件名派生：
- `<any_path>/models/<subdir>/<model_name>.sql` -> 表名为 `<MODEL_NAME>`（大写，取自文件名）

**输出 schema** -- 使用 schema 解析脚本：

1. **设置**：将 `dbt_project.yml` 和模型文件保存到 `/tmp/validation_notebook_working/<id>/` 并保留路径：
   ```
   /tmp/validation_notebook_working/<id>/
   +-- dbt_project.yml
   +-- models/
       +-- <path>/<model>.sql
   ```

2. **运行脚本** 对每个模型：
   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/skills/monte-carlo-validation-notebook/scripts/resolve_dbt_schema.py /tmp/validation_notebook_working/<id>/dbt_project.yml /tmp/validation_notebook_working/<id>/models/<path>/<model>.sql
   ```

3. **错误处理**：如果脚本失败，**立即停止**并报告错误。如果 schema 解析失败，不要继续生成 notebook。

4. **输出**：脚本打印解析后的 schema（例如 `PROD`、`PROD_STAGE`、`PROD_LINEAGE`）

**注意**：不要手动解析 dbt_project.yml 或模型配置来获取 schema — 始终使用脚本。它处理模型配置覆盖、dbt_project.yml 路由规则、自定义 schema 的 PROD_ 前缀，并默认为 `PROD`。

**配置块** -- 查找 `{{ config(...) }}` 并提取：
- `materialized` -- 'table'、'view'、'incremental'、'ephemeral'
- `unique_key` -- 去重键（可能是字符串或列表）
- `cluster_by` -- 聚类字段（可能包含时间轴）

**核心分段字段** -- 扫描整个模型 SQL 查找可能是业务键的字段：
- 名为 `*_id` 的字段（例如 `account_id`、`resource_id`、`monitor_id`）出现在 JOIN ON、GROUP BY、PARTITION BY 或 `unique_key` 中
- 去重并按频率排序。取前 3 个。

**时间轴字段** -- 检测模型的时间维度（按优先级排序）：
1. `is_incremental()` 块：WHERE 比较中使用的字段
2. `cluster_by` 配置：timestamp/date 字段
3. 字段命名惯例：`ingest_ts`、`created_time`、`date_part`、`timestamp`、`run_start_time`、`export_ts`、`event_created_time`
4. QUALIFY/ROW_NUMBER 中的 ORDER BY DESC

如果未找到时间轴，跳过该模型的时间轴查询。

### 2b. Diff 分析

解析该文件的 diff 块。对每个变更行分类：

- **变更字段** -- SELECT 子句或 CTE 定义中添加/修改的行。提取输出列名。
- **变更过滤器** -- WHERE 子句中添加/修改的行。
- **变更连接** -- JOIN ON 条件中添加/修改的行。
- **变更 unique_key** -- 如果配置中的 `unique_key` 被修改，记录新旧值。
- **新增列** -- "after" SELECT 中出现在 "before" 中不存在的列（纯新增）。

### 2c. 模型分类

根据 diff 将每个模型分类为 **新增** 或 **修改**：
- 如果该文件的 diff 包含 `new file mode` → 分类为 **新增**
- 否则 → 分类为 **修改**

此分类决定在阶段 3 中生成哪些查询模式。

**注意：** 对于 **新增模型**，跳过阶段 2b 的 diff 分析（没有 "before" 可供比较）。阶段 2a 的元数据提取仍然适用。

## 阶段 3：生成验证查询

对于每个变更的模型，根据其分类（新增 vs 修改）生成适用的查询。

**关键：参数占位符语法**

使用 **双花括号** `{{...}}` 作为参数占位符。不要使用 `${...}` 或任何其他语法。

正确：`{{prod_db}}.PROD.AGENT_RUNS`
错误：`${prod_db}.PROD.AGENT_RUNS`

**表引用格式：**
- prod 查询使用 `{{prod_db}}.<SCHEMA>.<TABLE_NAME>`
- dev 查询使用 `{{dev_db}}.<SCHEMA>.<TABLE_NAME>`
- `<SCHEMA>` 使用 schema 解析脚本的输出**按模型硬编码**

---

### 新增模型的查询模式

对于新增模型，所有查询仅针对 `{{dev_db}}`。由于 prod 表不存在，不生成对比查询。

#### Pattern 7-new：总行数
**触发条件：** 始终。

```sql
SELECT COUNT(*) AS total_rows
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

#### Pattern 9：样本数据预览
**触发条件：** 始终。

```sql
SELECT *
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
LIMIT 20
```

#### Pattern 2-new：核心分段计数
**触发条件：** 始终。

```sql
SELECT
    <segmentation_field>,
    COUNT(*) AS row_count
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
GROUP BY <segmentation_field>
ORDER BY row_count DESC
LIMIT 100
```

#### Pattern 5：唯一性检查
**触发条件：** 新增模型始终触发（从一开始就验证 unique_key 约束）。

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT <key_fields>) AS distinct_keys,
    COUNT(*) - COUNT(DISTINCT <key_fields>) AS duplicate_count
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

```sql
SELECT <key_fields>, COUNT(*) AS n
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
GROUP BY <key_fields>
HAVING COUNT(*) > 1
ORDER BY n DESC
LIMIT 100
```

#### Pattern 6-new：NULL 率检查（所有列）
**触发条件：** 始终。由于所有内容都是新增的，检查所有输出列。

```sql
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN <col1> IS NULL THEN 1 ELSE 0 END) AS <col1>_null_count,
    ROUND(100.0 * SUM(CASE WHEN <col1> IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS <col1>_null_pct,
    SUM(CASE WHEN <col2> IS NULL THEN 1 ELSE 0 END) AS <col2>_null_count,
    ROUND(100.0 * SUM(CASE WHEN <col2> IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS <col2>_null_pct
    -- repeat for each output column
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

#### Pattern 8：时间轴连续性
**触发条件：** 模型为 `materialized='incremental'` 或已识别时间轴字段。

```sql
SELECT
    CAST(<time_axis> AS DATE) AS day,
    COUNT(*) AS row_count
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
WHERE <time_axis> >= CURRENT_TIMESTAMP - INTERVAL '14' DAY
GROUP BY day
ORDER BY day DESC
LIMIT 30
```

---

### 修改模型的查询模式

对于修改模型，单表查询使用 `{{prod_db}}`，对比查询使用两者。

#### Pattern 7：总行数
**触发条件：** 始终。

```sql
SELECT COUNT(*) AS total_rows
FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
```

#### Pattern 9：样本数据预览
**触发条件：** 始终。

```sql
SELECT *
FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
LIMIT 20
```

#### Pattern 2：核心分段计数
**触发条件：** 始终。

```sql
SELECT
    <segmentation_field>,
    COUNT(*) AS row_count
FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
GROUP BY <segmentation_field>
ORDER BY row_count DESC
LIMIT 100
```

#### Pattern 1：变更字段分布
**触发条件：** 在阶段 2b 中发现变更字段。**排除新增列**（来自阶段 2b 的"新增列"）— 仅包含 prod 中存在的字段。

```sql
SELECT
    <changed_field>,
    COUNT(*) AS row_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct
FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
GROUP BY <changed_field>
ORDER BY row_count DESC
LIMIT 100
```

#### Pattern 5：唯一性检查
**触发条件：** JOIN 条件变更、`unique_key` 变更或模型为增量模型。

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT <key_fields>) AS distinct_keys,
    COUNT(*) - COUNT(DISTINCT <key_fields>) AS duplicate_count
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

```sql
SELECT <key_fields>, COUNT(*) AS n
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
GROUP BY <key_fields>
HAVING COUNT(*) > 1
ORDER BY n DESC
LIMIT 100
```

#### Pattern 6：NULL 率检查
**触发条件：** 新增列，或列被 COALESCE/NULLIF 包裹。

**重要：** 新增列（来自阶段 2b 的"新增列"）在 prod 中尚不存在。对于新增列，仅查询 `{{dev_db}}`。对于修改的列（COALESCE/NULLIF 变更），比较两个数据库。

**新增列**（仅 dev）：
```sql
SELECT
    COUNT(*) AS total_rows,
    SUM(CASE WHEN <column> IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN <column> IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS null_pct
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

**修改列**（prod vs dev）：
```sql
SELECT
    'prod' AS source,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN <column> IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN <column> IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS null_pct
FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
UNION ALL
SELECT
    'dev' AS source,
    COUNT(*) AS total_rows,
    SUM(CASE WHEN <column> IS NULL THEN 1 ELSE 0 END) AS null_count,
    ROUND(100.0 * SUM(CASE WHEN <column> IS NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS null_pct
FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

#### Pattern 8：时间轴连续性
**触发条件：** 模型为 `materialized='incremental'` 或已识别时间轴字段。

```sql
SELECT
    CAST(<time_axis> AS DATE) AS day,
    COUNT(*) AS row_count
FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
WHERE <time_axis> >= CURRENT_TIMESTAMP - INTERVAL '14' DAY
GROUP BY day
ORDER BY day DESC
LIMIT 30
```

#### Pattern 3：前后对比
**触发条件：** 始终（用于变更字段 + 顶部排序分段字段）。**仅限修改模型。**

**重要：** 从 `<group_fields>` 中排除新增列（来自阶段 2b 的"新增列"）。仅使用 prod 和 dev 中都存在的字段。新增列在 prod 中不存在，会导致查询错误。

```sql
WITH prod AS (
    SELECT <group_fields>, COUNT(*) AS cnt
    FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
    GROUP BY <group_fields>
),
dev AS (
    SELECT <group_fields>, COUNT(*) AS cnt
    FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
    GROUP BY <group_fields>
)
SELECT
    COALESCE(b.<field>, d.<field>) AS <field>,
    COALESCE(b.cnt, 0) AS cnt_prod,
    COALESCE(d.cnt, 0) AS cnt_dev,
    COALESCE(d.cnt, 0) - COALESCE(b.cnt, 0) AS diff
FROM prod b
FULL OUTER JOIN dev d ON b.<field> = d.<field>
ORDER BY ABS(diff) DESC
LIMIT 100
```

#### Pattern 7b：行数对比
**触发条件：** 始终。**仅限修改模型。**

```sql
SELECT 'prod' AS source, COUNT(*) AS row_count FROM {{prod_db}}.<SCHEMA>.<TABLE_NAME>
UNION ALL
SELECT 'dev' AS source, COUNT(*) AS row_count FROM {{dev_db}}.<SCHEMA>.<TABLE_NAME>
```

## 阶段 4：构建 Notebook YAML

### 4a. 元数据
```yaml
version: 1
metadata:
  id: validation-pr-<PR_NUMBER>-<random_suffix>
  name: "Validation: PR #<PR_NUMBER> - <PR_TITLE_TRUNCATED>"
  created_at: "<current_iso_timestamp>"
  updated_at: "<current_iso_timestamp>"
```

### 4b. 参数单元格

**仅在存在修改模型时包含 `prod_db`。** 如果所有模型都是新增的，仅包含 `dev_db`。

```yaml
# Include ONLY if there are modified models:
- id: param-prod-db
  type: parameter
  content:
    name: prod_db
    config:
      type: text
      default_value: "ANALYTICS"
      placeholder: "Prod database (e.g., ANALYTICS)"
  display_type: table

# Always include:
- id: param-dev-db
  type: parameter
  content:
    name: dev_db
    config:
      type: text
      default_value: "PERSONAL_<USER>"
      placeholder: "Dev database (e.g., PERSONAL_JSMITH)"
  display_type: table
```

### 4c. Markdown 摘要单元格
```yaml
- id: cell-summary
  type: markdown
  content: |
    # Validation Queries for <PR or Local Branch>
    ## Summary
    - **Title:** <title>
    - **Author:** <author>
    - **Source:** <PR URL or "Local branch: <branch>">
    - **Status:** <merge_timestamp or "Not yet merged" or "N/A (local)">
    ## Changes
    <brief description based on diff analysis>
    ## Changed Models
    - `<SCHEMA>.<TABLE_NAME>` (from `<file_path>`)
    ## How to Use
    1. Select your Snowflake connector above
    2. Set **dev_db** to your dev database (e.g., `PERSONAL_JSMITH`)
    3. If modified models are present, set **prod_db** to your prod database (e.g., `ANALYTICS`)
    4. Run single-table queries first, then comparison queries
  display_type: table
```

### 4d. SQL 单元格格式
```yaml
- id: cell-<pattern>-<model>-<index>
  type: sql
  content: |
    /*
    ========================================
    <Pattern Name (human-readable, e.g. "Total Row Count" — do NOT include pattern numbers like "Pattern 7:")>
    ========================================
    Model: <SCHEMA>.<TABLE_NAME>
    Triggered by: <why this pattern was generated>
    What to look for: <interpretation guidance>
    ----------------------------------------
    */
    <actual_sql_query>
  display_type: table
```

### 4e. 单元格组织

两种模型类型的单元格按以下顺序一致排列：

**新增模型：**
1. 摘要 markdown 单元格（注明模型为新增）
2. 参数单元格（仅 dev_db — 如果所有模型都是新增则不含 prod_db）
3. 总行数（Pattern 7-new）
4. 样本数据预览（Pattern 9）
5. 核心分段计数（Pattern 2-new）
6. 唯一性检查（Pattern 5）、NULL 率检查（Pattern 6-new）、时间轴连续性（Pattern 8）

**修改模型：**
1. 摘要 markdown 单元格
2. 参数单元格（prod_db、dev_db）
3. 总行数（Pattern 7）
4. 样本数据预览（Pattern 9）
5. 核心分段计数（Pattern 2）
6. 变更字段分布（Pattern 1）
7. 唯一性检查（Pattern 5）、NULL 率检查（Pattern 6）、时间轴连续性（Pattern 8）
8. 前后对比（Pattern 3）、行数对比（Pattern 7b）

## 阶段 5：生成导入 URL

1. 将 notebook YAML 写入 `/tmp/validation_notebook_working/<id>/notebook.yaml`
2. 运行 URL 生成脚本：
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/monte-carlo-validation-notebook/scripts/generate_notebook_url.py /tmp/validation_notebook_working/<id>/notebook.yaml --mc-base-url <MC_BASE_URL>
```
3. 脚本会验证 YAML 语法和 notebook schema（元数据和单元格的必填字段）。如果验证失败，仔细阅读错误信息，修复 YAML 以匹配阶段 4 中的规范，然后重新运行。

## 阶段 6：输出

展示：
```markdown
# Validation Notebook Generated
## Summary
- **Source:** PR #<number> - <title> OR Local: <branch>
- **Author:** <author>
- **Changed Models:** <count> models (of <total_count> changed)
- **Generated Queries:** <count> queries

> ⚠️ If models were capped: "Only the first 10 of <total_count> changed models were included. Re-run with `--models` to select specific models."

## Notebook Opened
The notebook has been opened directly in your browser.
Select your Snowflake connector in the notebook interface to begin running queries.
*Make sure MC Bridge is running. Let me know if you want tips on how to install this locally*
```

## 重要准则

1. **不要执行查询** -- 仅生成 notebook
2. **保持 SQL 可读** -- 格式规范且使用有意义的别名
3. **包含 LIMIT 100** — 用于可能返回大量行的查询
4. **使用双花括号** -- `{{prod_db}}` 而非 `${prod_db}`
5. **使用正确的表格式** -- `{{prod_db}}.<SCHEMA>.<TABLE>` 和 `{{dev_db}}.<SCHEMA>.<TABLE>`
6. **始终使用 schema 解析脚本** -- 不要手动解析 dbt_project.yml
7. **Schema 不是参数** -- 仅 `prod_db` 和 `dev_db` 是参数
8. **跳过 ephemeral 模型** -- 它们没有物理表
9. **截断 notebook 名称** -- 保持在 50 个字符以内
10. **生成唯一单元格 ID** -- 使用 `cell-p3-model-1` 之类的模式
11. **YAML 多行内容** -- 对包含注释的 SQL 使用 `|` 块标量
12. **仅 ASCII 的 YAML** -- 脚本在编码前会进行清理和验证

## 查询模式参考

| Pattern | 名称 | 触发条件 | 模型类型 | 数据库 | 顺序 |
|---------|------|---------|------------|----------|-------|
| 7 / 7-new | 总行数 | 始终 | 两者 | `{{prod_db}}`（修改）/ `{{dev_db}}`（新增） | 1 |
| 9 | 样本数据预览 | 始终 | 两者 | `{{prod_db}}`（修改）/ `{{dev_db}}`（新增） | 2 |
| 2 / 2-new | 核心分段计数 | 始终 | 两者 | `{{prod_db}}`（修改）/ `{{dev_db}}`（新增） | 3 |
| 1 | 变更字段分布 | diff 中列被修改（非新增） | 仅修改 | `{{prod_db}}` | 4 |
| 5 | 唯一性检查 | JOIN/unique_key 变更（修改）/ 始终（新增） | 两者 | `{{dev_db}}` | 5 |
| 6 / 6-new | NULL 率检查 | 新增列或 COALESCE（修改）/ 始终（新增） | 两者 | 新增列：仅 `{{dev_db}}`；COALESCE：两者（修改）/ `{{dev_db}}`（新增） | 5 |
| 8 | 时间轴连续性 | 增量模型或时间字段 | 两者 | `{{prod_db}}`（修改）/ `{{dev_db}}`（新增） | 5 |
| 3 | 前后对比 | 变更字段（非新增） | 仅修改 | 两者 | 6 |
| 7b | 行数对比 | 始终 | 仅修改 | 两者 | 6 |

## MC Bridge 设置帮助

如果用户询问如何安装或设置 MC Bridge，从 mc-bridge 仓库获取 README 并展示相关的快速入门/设置说明：

```bash
gh api repos/monte-carlo-data/mc-bridge/readme --jq '.content' | base64 --decode
```

重点关注：如何安装、配置连接和运行 MC Bridge。不要输出整个 README — 仅提取与设置相关的部分。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。