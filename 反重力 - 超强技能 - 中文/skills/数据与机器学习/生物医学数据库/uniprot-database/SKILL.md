---
name: uniprot-database
description: 通过 REST API 直接访问 UniProt。支持蛋白质检索、FASTA 序列获取、ID 映射、Swiss-Prot/TrEMBL 数据查询。涉及多数据库的 Python 工作流建议使用 bioservices（40+ 服务的统一接口）。适用于直接 HTTP/REST 调用或 UniProt 专项控制。触发词：UniProt、蛋白质检索、FASTA、ID 映射、Swiss-Prot、TrEMBL、蛋白质序列、UniProt API、蛋白查询、基因映射。
license: Unknown
metadata:
    skill-author: K-Dense Inc.
risk: safe
source: community
---

# UniProt 数据库

## 概述

UniProt 是全球领先的蛋白质序列与功能信息综合资源。支持按名称、基因或登录号检索蛋白质，获取 FASTA 格式序列，执行跨数据库 ID 映射，通过 REST API 访问 Swiss-Prot/TrEMBL 注释信息进行蛋白质分析。

## 使用场景

适用于以下场景：
- 按名称、基因符号、登录号或物种检索蛋白质条目
- 获取 FASTA 或其他格式的蛋白质序列
- 在 UniProt 与外部数据库（Ensembl、RefSeq、PDB 等）之间进行标识符映射
- 访问蛋白质注释信息，包括 GO 术语、结构域和功能描述
- 高效批量获取多个蛋白质条目
- 查询已审核（Swiss-Prot）与未审核（TrEMBL）蛋白质数据
- 流式获取大规模蛋白质数据集
- 使用字段特定搜索语法构建自定义查询

## 核心功能

### 1. 蛋白质检索

使用自然语言查询或结构化搜索语法检索 UniProt。

**常用搜索模式：**
```python
# Search by protein name
query = "insulin AND organism_name:\"Homo sapiens\""

# Search by gene name
query = "gene:BRCA1 AND reviewed:true"

# Search by accession
query = "accession:P12345"

# Search by sequence length
query = "length:[100 TO 500]"

# Search by taxonomy
query = "taxonomy_id:9606"  # Human proteins

# Search by GO term
query = "go:0005515"  # Protein binding
```

使用 API 搜索端点：`https://rest.uniprot.org/uniprotkb/search?query={query}&format={format}`

**支持格式：** JSON、TSV、Excel、XML、FASTA、RDF、TXT

### 2. 获取单个蛋白质条目

通过登录号获取特定蛋白质条目。

**登录号格式：**
- 经典格式：P12345、Q1AAA9、O15530（6个字符：字母 + 5位字母数字）
- 扩展格式：A0A022YWF9（新条目使用10个字符）

**获取端点：** `https://rest.uniprot.org/uniprotkb/{accession}.{format}`

示例：`https://rest.uniprot.org/uniprotkb/P12345.fasta`

### 3. 批量获取与 ID 映射

在不同数据库系统之间映射蛋白质标识符，高效获取多个条目。

**ID 映射工作流：**
1. 提交映射任务至：`https://rest.uniprot.org/idmapping/run`
2. 检查任务状态：`https://rest.uniprot.org/idmapping/status/{jobId}`
3. 获取结果：`https://rest.uniprot.org/idmapping/results/{jobId}`

**支持的映射数据库：**
- UniProtKB AC/ID
- Gene names
- Ensembl、RefSeq、EMBL
- PDB、AlphaFoldDB
- KEGG、GO terms
- 更多数据库详见 `/references/id_mapping_databases.md`

**限制：**
- 每次任务最多 100,000 个 ID
- 结果保留 7 天

### 4. 流式获取大规模结果集

对于超出分页限制的大型查询，使用流式端点：

`https://rest.uniprot.org/uniprotkb/stream?query={query}&format={format}`

流式端点返回所有结果，无分页限制，适合下载完整数据集。

### 5. 自定义检索字段

精确指定需要获取的字段，提升数据传输效率。

**常用字段：**
- `accession` - UniProt 登录号
- `id` - 条目名称
- `gene_names` - 基因名称
- `organism_name` - 物种名称
- `protein_name` - 蛋白质名称
- `sequence` - 氨基酸序列
- `length` - 序列长度
- `go_*` - 基因本体注释
- `cc_*` - 注释字段（功能、相互作用等）
- `ft_*` - 特征注释（结构域、位点等）

**示例：** `https://rest.uniprot.org/uniprotkb/search?query=insulin&fields=accession,gene_names,organism_name,length,sequence&format=tsv`

完整字段列表详见 `/references/api_fields.md`。

## Python 实现

编程访问请使用提供的辅助脚本 `scripts/uniprot_client.py`，包含以下功能：

- `search_proteins(query, format)` - 使用任意查询检索 UniProt
- `get_protein(accession, format)` - 获取单个蛋白质条目
- `map_ids(ids, from_db, to_db)` - 在标识符类型之间进行映射
- `batch_retrieve(accessions, format)` - 批量获取多个条目
- `stream_results(query, format)` - 流式获取大规模结果集

**替代 Python 包：**
- **Unipressed**：现代、类型化的 UniProt REST API Python 客户端
- **bioservices**：综合生物信息学 Web 服务客户端

## 查询语法示例

**布尔运算符：**
```
kinase AND organism_name:human
(diabetes OR insulin) AND reviewed:true
cancer NOT lung
```

**字段特定搜索：**
```
gene:BRCA1
accession:P12345
organism_id:9606
taxonomy_name:"Homo sapiens"
annotation:(type:signal)
```

**范围查询：**
```
length:[100 TO 500]
mass:[50000 TO 100000]
```

**通配符：**
```
gene:BRCA*
protein_name:kinase*
```

完整语法文档详见 `/references/query_syntax.md`。

## 最佳实践

1. **优先使用已审核条目**：使用 `reviewed:true` 筛选 Swiss-Prot（人工审核）条目
2. **明确指定格式**：选择最适合的格式（FASTA 用于序列、TSV 用于表格数据、JSON 用于编程解析）
3. **使用字段筛选**：仅请求所需字段，减少带宽和处理时间
4. **处理分页**：对大型结果集实施分页或使用流式端点
5. **缓存结果**：将常用数据本地存储，减少 API 调用次数
6. **速率限制**：尊重 API 资源，大批量操作时加入延时
7. **检查数据质量**：TrEMBL 条目为计算预测结果；Swiss-Prot 条目为人工审核结果

## 资源

### scripts/
`uniprot_client.py` - Python 客户端，提供常用 UniProt 操作的辅助函数，包括检索、获取、ID 映射和流式传输。

### references/
- `api_fields.md` - 自定义查询的完整可用字段列表
- `id_mapping_databases.md` - ID 映射操作支持的数据库
- `query_syntax.md` - 完整查询语法及高级示例
- `api_examples.md` - 多语言代码示例（Python、curl、R）

## 更多资源

- **API 文档**：https://www.uniprot.org/help/api
- **交互式 API 浏览器**：https://www.uniprot.org/api-documentation
- **REST 教程**：https://www.uniprot.org/help/uniprot_rest_tutorial
- **查询语法帮助**：https://www.uniprot.org/help/query-fields
- **SPARQL 端点**：https://sparql.uniprot.org/（高级图查询）

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不可将输出视为环境特定验证、测试或专家评审的替代品。
- 若缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
