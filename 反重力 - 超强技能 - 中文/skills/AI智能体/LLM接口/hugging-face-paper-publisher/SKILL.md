---
source: "https://github.com/huggingface/skills/tree/main/skills/huggingface-paper-publisher"
name: hugging-face-paper-publisher
description: 在 Hugging Face Hub 发布和管理研究论文。支持创建论文页面、将论文关联到模型/数据集、认领作者身份，以及生成专业的基于 Markdown 的研究文章。
risk: unknown
---

# 概述

## 适用场景
适用于用户希望在 Hugging Face Hub 发布、关联、索引或管理研究论文的场景。
本技能为 AI 工程师和研究人员提供在 Hugging Face Hub 发布、管理和关联研究论文的完整工具集。它简化了从论文创建到发布的完整流程，包括与 arXiv 集成、模型/数据集关联和作者身份管理。

## 与 HF 生态集成
- **论文页面**：在 Hugging Face Hub 索引和发现论文
- **arXiv 集成**：从 arXiv ID 自动索引论文
- **模型/数据集关联**：通过元数据将论文关联到相关资源
- **作者身份验证**：认领和验证论文作者身份
- **研究文章模板**：生成专业、现代的科学论文

# 版本
1.0.0

# 依赖
内置脚本使用 PEP 723 内联依赖。推荐使用 `uv run` 而非手动配置环境。

- huggingface_hub>=0.26.0
- pyyaml>=6.0.3
- requests>=2.32.5
- markdown>=3.5.0
- python-dotenv>=1.2.1

# 核心能力

## 1. 论文页面管理
- **索引论文**：从 arXiv 添加论文到 Hugging Face
- **认领作者身份**：验证并认领已发布论文的作者身份
- **管理可见性**：控制哪些论文显示在个人主页
- **论文发现**：在 HF 生态中查找和探索论文

## 2. 论文关联到资源
- **模型卡片**：向模型元数据添加论文引用
- **数据集卡片**：通过 README 将论文关联到数据集
- **自动标签**：Hub 自动生成 arxiv:<PAPER_ID> 标签
- **引用管理**：维护正确的归属和参考文献

## 3. 研究文章创建
- **Markdown 模板**：生成专业的论文格式
- **现代设计**：简洁、易读的研究文章布局
- **动态目录**：自动生成目录
- **章节结构**：标准科学论文组织方式
- **LaTeX 数学**：支持公式和技术符号

## 4. 元数据管理
- **YAML 前言**：正确的模型/数据集卡片元数据
- **引用追踪**：跨仓库维护论文引用
- **版本控制**：追踪论文更新和修订
- **多论文支持**：将多篇论文关联到单个资源

# 使用说明

本技能在 `scripts/` 目录中包含用于论文发布操作的 Python 脚本。

### 前置条件
- 使用 `uv run` 运行脚本（依赖从脚本头部解析）
- 设置 `HF_TOKEN` 环境变量，使用具有写入权限的令牌

> **所有路径相对于包含此 SKILL.md 文件的目录。**
> 运行任何脚本前，先 `cd` 到该目录或使用完整路径。


### 方法 1：从 arXiv 索引论文

从 arXiv 添加论文到 Hugging Face 论文页面。

**基本用法：**
```bash
uv run scripts/paper_manager.py index \
  --arxiv-id "2301.12345"
```

**检查论文是否存在：**
```bash
uv run scripts/paper_manager.py check \
  --arxiv-id "2301.12345"
```

**直接 URL 访问：**
也可以直接访问 `https://huggingface.co/papers/{arxiv-id}` 来索引论文。

### 方法 2：将论文关联到模型/数据集

向模型或数据集 README 添加论文引用及正确的 YAML 元数据。

**添加到模型卡片：**
```bash
uv run scripts/paper_manager.py link \
  --repo-id "username/model-name" \
  --repo-type "model" \
  --arxiv-id "2301.12345"
```

**添加到数据集卡片：**
```bash
uv run scripts/paper_manager.py link \
  --repo-id "username/dataset-name" \
  --repo-type "dataset" \
  --arxiv-id "2301.12345"
```

**添加多篇论文：**
```bash
uv run scripts/paper_manager.py link \
  --repo-id "username/model-name" \
  --repo-type "model" \
  --arxiv-ids "2301.12345,2302.67890,2303.11111"
```

**使用自定义引用：**
```bash
uv run scripts/paper_manager.py link \
  --repo-id "username/model-name" \
  --repo-type "model" \
  --arxiv-id "2301.12345" \
  --citation "$(cat citation.txt)"
```

#### 关联工作原理

当你在模型或数据集 README 中添加 arXiv 论文链接时：
1. Hub 从链接中提取 arXiv ID
2. 自动为仓库添加 `arxiv:<PAPER_ID>` 标签
3. 用户可点击标签查看论文页面
4. 论文页面显示所有引用该论文的模型/数据集
5. 论文可通过过滤器和搜索被发现

### 方法 3：认领作者身份

在 Hugging Face 上发布的论文中验证你的作者身份。

**启动认领流程：**
```bash
uv run scripts/paper_manager.py claim \
  --arxiv-id "2301.12345" \
  --email "your.email@institution.edu"
```

**手动流程：**
1. 访问你的论文页面：`https://huggingface.co/papers/{arxiv-id}`
2. 在作者列表中找到你的名字
3. 点击你的名字并选择"Claim authorship"
4. 等待管理员团队验证

**检查作者身份状态：**
```bash
uv run scripts/paper_manager.py check-authorship \
  --arxiv-id "2301.12345"
```

### 方法 4：管理论文可见性

控制哪些已验证论文显示在公开主页。

**列出你的论文：**
```bash
uv run scripts/paper_manager.py list-my-papers
```

**切换可见性：**
```bash
uv run scripts/paper_manager.py toggle-visibility \
  --arxiv-id "2301.12345" \
  --show true
```

**在设置中管理：**
访问账户设置 → 论文部分，为每篇论文切换"显示在主页"。

### 方法 5：创建研究文章

使用现代模板生成专业的基于 Markdown 的研究论文。

**从模板创建：**
```bash
uv run scripts/paper_manager.py create \
  --template "standard" \
  --title "Your Paper Title" \
  --output "paper.md"
```

**可用模板：**
- `standard` - 传统科学论文结构
- `modern` - 简洁、适合网页的格式，灵感来自 Distill
- `arxiv` - arXiv 风格格式
- `ml-report` - 机器学习实验报告

**生成完整论文：**
```bash
uv run scripts/paper_manager.py create \
  --template "modern" \
  --title "Fine-Tuning Large Language Models with LoRA" \
  --authors "Jane Doe, John Smith" \
  --abstract "$(cat abstract.txt)" \
  --output "paper.md"
```

**转换为 HTML：**
```bash
uv run scripts/paper_manager.py convert \
  --input "paper.md" \
  --output "paper.html" \
  --style "modern"
```

### 论文模板结构

**标准研究论文章节：**
```markdown
---
title: Your Paper Title
authors: Jane Doe, John Smith
affiliations: University X, Lab Y
date: 2025-01-15
arxiv: 2301.12345
tags: [machine-learning, nlp, fine-tuning]
---

# Abstract
Brief summary of the paper...

# 1. Introduction
Background and motivation...

# 2. Related Work
Previous research and context...

# 3. Methodology
Approach and implementation...

# 4. Experiments
Setup, datasets, and procedures...

# 5. Results
Findings and analysis...

# 6. Discussion
Interpretation and implications...

# 7. Conclusion
Summary and future work...

# References
```

**现代模板特性：**
- 动态目录
- 响应式网页设计
- 代码语法高亮
- 交互式图表
- 数学公式渲染（LaTeX）
- 引用管理
- 作者机构链接

### 命令参考

**索引论文：**
```bash
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"
```

**关联到仓库：**
```bash
uv run scripts/paper_manager.py link \
  --repo-id "username/repo-name" \
  --repo-type "model|dataset|space" \
  --arxiv-id "2301.12345" \
  [--citation "Full citation text"] \
  [--create-pr]
```

**认领作者身份：**
```bash
uv run scripts/paper_manager.py claim \
  --arxiv-id "2301.12345" \
  --email "your.email@edu"
```

**管理可见性：**
```bash
uv run scripts/paper_manager.py toggle-visibility \
  --arxiv-id "2301.12345" \
  --show true|false
```

**创建研究文章：**
```bash
uv run scripts/paper_manager.py create \
  --template "standard|modern|arxiv|ml-report" \
  --title "Paper Title" \
  [--authors "Author1, Author2"] \
  [--abstract "Abstract text"] \
  [--output "filename.md"]
```

**转换 Markdown 为 HTML：**
```bash
uv run scripts/paper_manager.py convert \
  --input "paper.md" \
  --output "paper.html" \
  [--style "modern|classic"]
```

**检查论文状态：**
```bash
uv run scripts/paper_manager.py check --arxiv-id "2301.12345"
```

**列出你的论文：**
```bash
uv run scripts/paper_manager.py list-my-papers
```

**搜索论文：**
```bash
uv run scripts/paper_manager.py search --query "transformer attention"
```

### YAML 元数据格式

将论文关联到模型或数据集时，需要正确的 YAML 前言：

**模型卡片示例：**
```yaml
---
language:
  - en
license: apache-2.0
tags:
  - text-generation
  - transformers
  - llm
library_name: transformers
---

# Model Name

This model is based on the approach described in [Our Paper](https://arxiv.org/abs/2301.12345).

## Citation

```bibtex
@article{doe2023paper,
  title={Your Paper Title},
  author={Doe, Jane and Smith, John},
  journal={arXiv preprint arXiv:2301.12345},
  year={2023}
}
```
```

**数据集卡片示例：**
```yaml
---
language:
  - en
license: cc-by-4.0
task_categories:
  - text-generation
  - question-answering
size_categories:
  - 10K<n<100K
---

# Dataset Name

Dataset introduced in [Our Paper](https://arxiv.org/abs/2301.12345).

For more details, see the [paper page](https://huggingface.co/papers/2301.12345).
```

Hub 会自动从这些链接中提取 arXiv ID 并创建 `arxiv:2301.12345` 标签。

### 集成示例

**工作流 1：发布新研究**
```bash
# 1. 创建研究文章
uv run scripts/paper_manager.py create \
  --template "modern" \
  --title "Novel Fine-Tuning Approach" \
  --output "paper.md"

# 2. 编辑 paper.md 填入内容

# 3. 提交到 arXiv（外部流程）
# 上传到 arxiv.org，获取 arXiv ID

# 4. 在 Hugging Face 索引
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"

# 5. 关联到你的模型
uv run scripts/paper_manager.py link \
  --repo-id "your-username/your-model" \
  --repo-type "model" \
  --arxiv-id "2301.12345"

# 6. 认领作者身份
uv run scripts/paper_manager.py claim \
  --arxiv-id "2301.12345" \
  --email "your.email@edu"
```

**工作流 2：关联已有论文**
```bash
# 1. 检查论文是否存在
uv run scripts/paper_manager.py check --arxiv-id "2301.12345"

# 2. 如需则索引
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"

# 3. 关联到多个仓库
uv run scripts/paper_manager.py link \
  --repo-id "username/model-v1" \
  --repo-type "model" \
  --arxiv-id "2301.12345"

uv run scripts/paper_manager.py link \
  --repo-id "username/training-data" \
  --repo-type "dataset" \
  --arxiv-id "2301.12345"

uv run scripts/paper_manager.py link \
  --repo-id "username/demo-space" \
  --repo-type "space" \
  --arxiv-id "2301.12345"
```

**工作流 3：为模型添加论文引用**
```bash
# 1. 获取当前 README
hf download username/model-name README.md

# 2. 添加论文链接
uv run scripts/paper_manager.py link \
  --repo-id "username/model-name" \
  --repo-type "model" \
  --arxiv-id "2301.12345" \
  --citation "Full citation for the paper"

# 脚本会：
# - 如缺失则添加 YAML 元数据
# - 在 README 中插入 arXiv 链接
# - 添加格式化的引用
# - 保留现有内容
```

### 最佳实践

1. **论文索引**
   - 论文在 arXiv 发布后尽快索引
   - 在模型/数据集卡片中包含完整的引用信息
   - 在相关仓库中使用一致的论文引用

2. **元数据管理**
   - 为所有模型/数据集卡片添加 YAML 前言
   - 包含正确的许可证信息
   - 标记相关的任务类别和领域

3. **作者身份**
   - 认领你作为作者列出的论文
   - 使用机构邮箱进行验证
   - 保持论文可见性设置更新

4. **仓库关联**
   - 将论文关联到所有相关的模型、数据集和 Spaces
   - 在 README 描述中包含论文背景
   - 添加 BibTeX 引用以方便参考

5. **研究文章**
   - 在项目中一致使用模板
   - 在论文中包含代码和数据链接
   - 生成适合网页分享的 HTML 版本

### 高级用法

**批量关联论文：**
```bash
# 将多篇论文关联到一个仓库
for arxiv_id in "2301.12345" "2302.67890" "2303.11111"; do
  uv run scripts/paper_manager.py link \
    --repo-id "username/model-name" \
    --repo-type "model" \
    --arxiv-id "$arxiv_id"
done
```

**提取论文信息：**
```bash
# 从 arXiv 获取论文元数据
uv run scripts/paper_manager.py info \
  --arxiv-id "2301.12345" \
  --format "json"
```

**生成引用：**
```bash
# 创建 BibTeX 引用
uv run scripts/paper_manager.py citation \
  --arxiv-id "2301.12345" \
  --format "bibtex"
```

**验证链接：**
```bash
# 检查仓库中的所有论文链接
uv run scripts/paper_manager.py validate \
  --repo-id "username/model-name" \
  --repo-type "model"
```

### 错误处理

- **论文未找到**：arXiv ID 不存在或尚未索引
- **权限拒绝**：HF_TOKEN 缺少仓库写入权限
- **无效 YAML**：README 前言元数据格式错误
- **作者身份验证失败**：邮箱与论文作者记录不匹配
- **已被认领**：其他用户已认领作者身份
- **速率限制**：短时间内 API 请求过多

### 故障排除

**问题**："Paper not found on Hugging Face"
- **解决方案**：访问 `hf.co/papers/{arxiv-id}` 触发索引

**问题**："Authorship claim not verified"
- **解决方案**：等待管理员审核或联系 HF 支持并提供证明

**问题**："arXiv tag not appearing"
- **解决方案**：确保 README 包含正确的 arXiv URL 格式

**问题**："Cannot link to repository"
- **解决方案**：验证 HF_TOKEN 具有写入权限

**问题**："Template rendering errors"
- **解决方案**：检查 markdown 语法和 YAML 前言格式

### 资源和参考

- **Hugging Face 论文页面**：[hf.co/papers](https://huggingface.co/papers)
- **模型卡片指南**：[hf.co/docs/hub/model-cards](https://huggingface.co/docs/hub/en/model-cards)
- **数据集卡片指南**：[hf.co/docs/hub/datasets-cards](https://huggingface.co/docs/hub/en/datasets-cards)
- **研究文章模板**：[tfrere/research-article-template](https://huggingface.co/spaces/tfrere/research-article-template)
- **arXiv 格式指南**：[arxiv.org/help/submit](https://arxiv.org/help/submit)

### 与 tfrere 研究模板集成

本技能与 [tfrere 的研究文章模板](https://huggingface.co/spaces/tfrere/research-article-template) 互补，提供：

- 自动化论文索引工作流
- 仓库关联能力
- 元数据管理工具
- 引用生成工具

你可以使用 tfrere 的模板进行写作，然后使用本技能在 Hugging Face Hub 发布和关联论文。

### 常见模式

**模式 1：新论文发布**
```bash
# 写作 → 发布 → 索引 → 关联
uv run scripts/paper_manager.py create --template modern --output paper.md
# (提交到 arXiv)
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"
uv run scripts/paper_manager.py link --repo-id "user/model" --arxiv-id "2301.12345"
```

**模式 2：已有论文发现**
```bash
# 搜索 → 检查 → 关联
uv run scripts/paper_manager.py search --query "transformers"
uv run scripts/paper_manager.py check --arxiv-id "2301.12345"
uv run scripts/paper_manager.py link --repo-id "user/model" --arxiv-id "2301.12345"
```

**模式 3：作者作品集管理**
```bash
# 认领 → 验证 → 组织
uv run scripts/paper_manager.py claim --arxiv-id "2301.12345"
uv run scripts/paper_manager.py list-my-papers
uv run scripts/paper_manager.py toggle-visibility --arxiv-id "2301.12345" --show true
```

### API 集成

**Python 脚本示例：**
```python
from scripts.paper_manager import PaperManager

pm = PaperManager(hf_token="your_token")

# 索引论文
pm.index_paper("2301.12345")

# 关联到模型
pm.link_paper(
    repo_id="username/model",
    repo_type="model",
    arxiv_id="2301.12345",
    citation="Full citation text"
)

# 检查状态
status = pm.check_paper("2301.12345")
print(status)
```

### 未来增强

计划在未来版本中添加的功能：
- 支持非 arXiv 论文（会议论文集、期刊）
- 从 DOI 自动格式化引用
- 论文比较和版本控制工具
- 协作论文写作功能
- 与 LaTeX 工作流集成
- 自动图表提取
- 论文指标和影响力追踪

## 限制
- 仅在任务明确符合上述范围时使用本技能。
- 输出不能替代特定环境的验证、测试或专家评审。
- 如缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
