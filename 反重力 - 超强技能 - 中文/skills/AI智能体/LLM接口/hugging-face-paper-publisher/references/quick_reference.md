# 快速参考指南

## 常用命令

### 论文索引
```bash
# 从 arXiv 索引
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"

# 检查论文是否存在
uv run scripts/paper_manager.py check --arxiv-id "2301.12345"
```

### 关联论文
```bash
# 关联到模型
uv run scripts/paper_manager.py link \
  --repo-id "username/model" \
  --repo-type "model" \
  --arxiv-id "2301.12345"

# 关联到数据集
uv run scripts/paper_manager.py link \
  --repo-id "username/dataset" \
  --repo-type "dataset" \
  --arxiv-id "2301.12345"

# 关联多篇论文
uv run scripts/paper_manager.py link \
  --repo-id "username/model" \
  --repo-type "model" \
  --arxiv-ids "2301.12345,2302.67890"
```

### 创建论文
```bash
# 标准模板
uv run scripts/paper_manager.py create \
  --template "standard" \
  --title "Paper Title" \
  --output "paper.md"

# 现代模板
uv run scripts/paper_manager.py create \
  --template "modern" \
  --title "Paper Title" \
  --authors "Author1, Author2" \
  --abstract "Abstract text" \
  --output "paper.md"

# ML 报告
uv run scripts/paper_manager.py create \
  --template "ml-report" \
  --title "Experiment Report" \
  --output "report.md"

# arXiv 风格
uv run scripts/paper_manager.py create \
  --template "arxiv" \
  --title "Paper Title" \
  --output "paper.md"
```

### 引用
```bash
# 生成 BibTeX
uv run scripts/paper_manager.py citation \
  --arxiv-id "2301.12345" \
  --format "bibtex"
```

### 论文信息
```bash
# JSON 格式
uv run scripts/paper_manager.py info \
  --arxiv-id "2301.12345" \
  --format "json"

# 文本格式
uv run scripts/paper_manager.py info \
  --arxiv-id "2301.12345" \
  --format "text"
```

## URL 格式

### Hugging Face 论文页面
- 查看论文：`https://huggingface.co/papers/{arxiv-id}`
- 示例：`https://huggingface.co/papers/2301.12345`

### arXiv
- 摘要：`https://arxiv.org/abs/{arxiv-id}`
- PDF：`https://arxiv.org/pdf/{arxiv-id}.pdf`
- 示例：`https://arxiv.org/abs/2301.12345`

## YAML 元数据格式

### 模型卡片
```yaml
---
language:
  - en
license: apache-2.0
tags:
  - text-generation
  - transformers
library_name: transformers
---
```

### 数据集卡片
```yaml
---
language:
  - en
license: cc-by-4.0
task_categories:
  - text-generation
size_categories:
  - 10K<n<100K
---
```

## arXiv ID 格式

以下格式均有效：
- `2301.12345`
- `arxiv:2301.12345`
- `https://arxiv.org/abs/2301.12345`
- `https://arxiv.org/pdf/2301.12345.pdf`

## 环境设置

### 设置令牌
```bash
export HF_TOKEN="your_token"
```

### 或使用 .env 文件
```bash
echo "HF_TOKEN=your_token" > .env
```

## 常用工作流

### 1. 索引与关联
```bash
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"
uv run scripts/paper_manager.py link --repo-id "user/model" --arxiv-id "2301.12345"
```

### 2. 创建与发布
```bash
uv run scripts/paper_manager.py create --template "modern" --title "Title" --output "paper.md"
# 编辑 paper.md
# 提交到 arXiv → 获取 ID
uv run scripts/paper_manager.py index --arxiv-id "NEW_ID"
uv run scripts/paper_manager.py link --repo-id "user/model" --arxiv-id "NEW_ID"
```

### 3. 批量关联
```bash
for id in "2301.12345" "2302.67890"; do
  uv run scripts/paper_manager.py link --repo-id "user/model" --arxiv-id "$id"
done
```

## 故障排除

### 论文未找到

访问 `https://huggingface.co/papers/{arxiv-id}` 触发索引

### 权限被拒绝

检查 `HF_TOKEN` 是否已设置且具有写权限

### arXiv API 错误

稍等片刻后重试——arXiv 有速率限制

## 使用技巧

1. 关联前始终先检查论文是否存在
2. 使用模板保持一致性
3. 在模型卡片中包含完整引用
4. 将论文关联到所有相关制品
5. 保持引用信息最新

## 可用模板

- `standard` - 传统学术论文
- `modern` - 适合网页的格式（Distill 风格）
- `arxiv` - arXiv 期刊格式
- `ml-report` - ML 实验文档

## 文件位置

- 脚本：`scripts/paper_manager.py`
- 模板：`templates/*.md`
- 示例：`examples/example_usage.md`
- 本指南：`references/quick_reference.md`

## 获取帮助

```bash
# 命令帮助
uv run scripts/paper_manager.py --help

# 子命令帮助
uv run scripts/paper_manager.py link --help
```

## 其他资源

- [完整文档](../SKILL.md)
- [使用示例](../examples/example_usage.md)
- [HF 论文页面](https://huggingface.co/papers)
- [tfrere 的模板](https://huggingface.co/spaces/tfrere/research-article-template)
