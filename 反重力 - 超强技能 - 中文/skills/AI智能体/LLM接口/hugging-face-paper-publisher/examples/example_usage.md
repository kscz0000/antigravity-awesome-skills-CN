# 使用示例：HF 论文发布器技能

本文档演示了在 Hugging Face Hub 上发布研究论文的常见工作流。

## 示例 1：索引已有的 arXiv 论文

如果你已经在 arXiv 上发表了论文，并希望使其在 Hugging Face 上可被检索到：

```bash
# 检查论文是否存在
uv run scripts/paper_manager.py check --arxiv-id "2301.12345"

# 索引论文
uv run scripts/paper_manager.py index --arxiv-id "2301.12345"

# 获取论文信息
uv run scripts/paper_manager.py info --arxiv-id "2301.12345"
```

预期输出：
```json
{
  "exists": true,
  "url": "https://huggingface.co/papers/2301.12345",
  "arxiv_id": "2301.12345",
  "arxiv_url": "https://arxiv.org/abs/2301.12345"
}
```

## 示例 2：将论文关联到你的模型

索引论文后，将其关联到你的模型仓库：

```bash
# 关联单篇论文
uv run scripts/paper_manager.py link \
  --repo-id "username/my-awesome-model" \
  --repo-type "model" \
  --arxiv-id "2301.12345"

# 关联多篇论文
uv run scripts/paper_manager.py link \
  --repo-id "username/my-awesome-model" \
  --repo-type "model" \
  --arxiv-ids "2301.12345,2302.67890"
```

此操作将：
1. 下载模型的 README.md
2. 添加或更新 YAML 前言
3. 插入论文引用及链接
4. 上传更新后的 README
5. Hub 自动创建 `arxiv:2301.12345` 标签

## 示例 3：将论文关联到数据集

数据集的过程相同：

```bash
uv run scripts/paper_manager.py link \
  --repo-id "username/my-dataset" \
  --repo-type "dataset" \
  --arxiv-id "2301.12345" \
  --citation "$(cat citation.bib)"
```

## 示例 4：创建新的研究文章

从模板生成研究论文：

```bash
# 使用标准模板创建
uv run scripts/paper_manager.py create \
  --template "standard" \
  --title "Efficient Fine-Tuning of Large Language Models" \
  --authors "Jane Doe, John Smith" \
  --abstract "We propose a novel approach to fine-tuning..." \
  --output "paper.md"

# 使用现代模板创建
uv run scripts/paper_manager.py create \
  --template "modern" \
  --title "Vision Transformers for Medical Imaging" \
  --output "medical_vit_paper.md"

# 创建 ML 实验报告
uv run scripts/paper_manager.py create \
  --template "ml-report" \
  --title "BERT Fine-tuning Experiment Results" \
  --output "bert_experiment_report.md"
```

## 示例 5：生成引用

获取论文的格式化引用：

```bash
# BibTeX 格式
uv run scripts/paper_manager.py citation \
  --arxiv-id "2301.12345" \
  --format "bibtex"
```

输出：
```bibtex
@article{arxiv2301_12345,
  title={Efficient Fine-Tuning of Large Language Models},
  author={Doe, Jane and Smith, John},
  journal={arXiv preprint arXiv:2301.12345},
  year={2023}
}
```

## 示例 6：完整工作流 - 新论文

从论文创建到发布的完整工作流：

```bash
# 步骤 1：创建研究文章
uv run scripts/paper_manager.py create \
  --template "modern" \
  --title "Novel Architecture for Multimodal Learning" \
  --authors "Alice Chen, Bob Kumar" \
  --output "multimodal_paper.md"

# 步骤 2：编辑论文（使用你喜欢的编辑器）
# vim multimodal_paper.md

# 步骤 3：提交到 arXiv（外部流程）
# 上传到 arxiv.org，收到 arXiv ID：2312.99999

# 步骤 4：在 Hugging Face 上索引
uv run scripts/paper_manager.py index --arxiv-id "2312.99999"

# 步骤 5：关联到你的模型/数据集
uv run scripts/paper_manager.py link \
  --repo-id "alice/multimodal-model-v1" \
  --repo-type "model" \
  --arxiv-id "2312.99999"

uv run scripts/paper_manager.py link \
  --repo-id "alice/multimodal-dataset" \
  --repo-type "dataset" \
  --arxiv-id "2312.99999"

# 步骤 6：为 README 生成引用
uv run scripts/paper_manager.py citation \
  --arxiv-id "2312.99999" \
  --format "bibtex" > citation.bib
```

## 示例 7：批量关联论文

将多篇论文关联到多个仓库：

```bash
#!/bin/bash

# 论文列表
PAPERS=("2301.12345" "2302.67890" "2303.11111")

# 模型列表
MODELS=("username/model-a" "username/model-b" "username/model-c")

# 将每篇论文关联到每个模型
for paper in "${PAPERS[@]}"; do
  for model in "${MODELS[@]}"; do
    echo "正在将 $paper 关联到 $model..."
    uv run scripts/paper_manager.py link \
      --repo-id "$model" \
      --repo-type "model" \
      --arxiv-id "$paper"
  done
done
```

## 示例 8：使用论文信息更新模型卡片

获取论文信息并手动更新模型卡片：

```bash
# 获取论文信息
uv run scripts/paper_manager.py info \
  --arxiv-id "2301.12345" \
  --format "text" > paper_info.txt

# 查看信息
cat paper_info.txt

# 手动合并到你的模型卡片，或使用 link 命令
```

## 示例 9：搜索与发现论文

```bash
# 搜索论文（打开浏览器）
uv run scripts/paper_manager.py search \
  --query "transformer attention mechanism"
```

## 示例 10：使用 tfrere 的模板

本技能与 [tfrere 的研究文章模板](https://huggingface.co/spaces/tfrere/research-article-template) 互补：

```bash
# 1. 使用 tfrere 的 Space 创建精美的网页版论文
# 访问：https://huggingface.co/spaces/tfrere/research-article-template

# 2. 将你的论文内容导出为 Markdown

# 3. 提交到 arXiv

# 4. 使用本技能进行索引和关联
uv run scripts/paper_manager.py index --arxiv-id "YOUR_ARXIV_ID"
uv run scripts/paper_manager.py link \
  --repo-id "your-username/your-model" \
  --arxiv-id "YOUR_ARXIV_ID"
```

## 示例 11：错误处理

```bash
# 关联前检查论文是否存在
if uv run scripts/paper_manager.py check --arxiv-id "2301.12345" | grep -q '"exists": true'; then
  echo "论文存在，正在进行关联..."
  uv run scripts/paper_manager.py link \
    --repo-id "username/model" \
    --arxiv-id "2301.12345"
else
  echo "论文不存在，先进行索引..."
  uv run scripts/paper_manager.py index --arxiv-id "2301.12345"
  uv run scripts/paper_manager.py link \
    --repo-id "username/model" \
    --arxiv-id "2301.12345"
fi
```

## 示例 12：CI/CD 集成

添加到你的 `.github/workflows/update-paper.yml`：

```yaml
name: Update Paper Links

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up uv
        uses: astral-sh/setup-uv@v5

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Link paper to model
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          uv run scripts/paper_manager.py link \
            --repo-id "${{ github.repository_owner }}/model-name" \
            --repo-type "model" \
            --arxiv-id "2301.12345"
```

## 技巧与最佳实践

1. **始终先检查论文是否存在**，以避免不必要的操作
2. **使用有意义的提交信息** 当将论文关联到仓库时
3. **在模型卡片中包含完整引用** 以便正确归属
4. **将论文关联到所有相关制品**（模型、数据集、spaces）
5. **生成 BibTeX 引用** 方便他人参考
6. **在你的 HF 个人资料设置中保持论文可见性更新**
7. **在你的研究组内一致使用模板**
8. **与代码一起对论文进行版本控制**

## 故障排除

### 索引后未找到论文

```bash
# 直接访问 URL 触发索引
open "https://huggingface.co/papers/2301.12345"

# 等待几秒钟，然后再次检查
uv run scripts/paper_manager.py check --arxiv-id "2301.12345"
```

### 关联时权限被拒绝

```bash
# 验证你的令牌具有写权限
echo $HF_TOKEN

# 如果缺失则设置令牌
export HF_TOKEN="your_token_here"

# 或使用 .env 文件
echo "HF_TOKEN=your_token_here" > .env
```

### arXiv ID 格式问题

```bash
# 脚本处理各种格式：
uv run scripts/paper_manager.py check --arxiv-id "2301.12345"
uv run scripts/paper_manager.py check --arxiv-id "arxiv:2301.12345"
uv run scripts/paper_manager.py check --arxiv-id "https://arxiv.org/abs/2301.12345"

# 它们都等价且会被规范化
```

## 下一步

- 浏览 [论文页面文档](https://huggingface.co/docs/hub/en/paper-pages)
- 查看 [tfrere 的研究模板](https://huggingface.co/spaces/tfrere/research-article-template)
- 在 HF 上浏览 [论文列表](https://huggingface.co/papers)
- 了解 [模型卡片](https://huggingface.co/docs/hub/en/model-cards)
