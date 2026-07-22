---
source: "https://github.com/huggingface/skills/tree/main/skills/huggingface-papers"
name: hugging-face-papers
description: 读取和分析 Hugging Face 论文页面或 arXiv 论文，支持 markdown 格式和 papers API 元数据。当用户要求'查看论文'、'分析论文'、'Hugging Face 论文'、'arXiv 论文'、'论文摘要'时使用。
risk: unknown
---

# Hugging Face 论文页面

Hugging Face 论文页面（hf.co/papers）是基于 arXiv（arxiv.org）构建的平台，专注于人工智能（AI）和计算机科学领域的研究论文。Hugging Face 用户可在 hf.co/papers/submit 提交论文，论文会展示在每日论文信息流（hf.co/papers）中。每天用户可以对论文投票和评论。每个论文页面允许作者：
- 认领自己的论文（点击 `authors` 字段中的姓名），论文页面会出现在其 Hugging Face 个人主页上
- 关联相关的模型检查点、数据集和 Spaces，只需在模型卡片、数据集卡片或 Space 的 README 中包含 HF 论文或 arXiv URL
- 关联 GitHub 仓库和/或项目页面 URL
- 关联 HF 组织，论文页面也会出现在该 Hugging Face 组织页面上

当有人在模型卡片、数据集卡片或 Space 仓库的 README 中提及 HF 论文或 arXiv 摘要/PDF URL 时，该论文会被自动索引。注意，并非所有在 Hugging Face 上索引的论文都会提交到每日论文。后者更多是一种推广研究论文的方式。论文只能在 arXiv 发布后 14 天内提交到每日论文。

Hugging Face 团队提供了易用的 API 来与论文页面交互。论文内容可以 markdown 格式获取，也可以返回结构化元数据，如作者姓名、关联的模型/数据集/Spaces、关联的 GitHub 仓库和项目页面。

## 何时使用
- 用户分享了 Hugging Face 论文页面 URL（如 `https://huggingface.co/papers/2602.08025`）
- 用户分享了 Hugging Face markdown 论文页面 URL（如 `https://huggingface.co/papers/2602.08025.md`）
- 用户分享了 arXiv URL（如 `https://arxiv.org/abs/2602.08025` 或 `https://arxiv.org/pdf/2602.08025`）
- 用户提到了 arXiv ID（如 `2602.08025`）
- 用户要求总结、解释或分析一篇 AI 研究论文

## 解析论文 ID

建议从用户提供的输入中解析论文 ID（arXiv ID）：

| 输入 | 论文 ID |
| --- | --- |
| `https://huggingface.co/papers/2602.08025` | `2602.08025` |
| `https://huggingface.co/papers/2602.08025.md` | `2602.08025` |
| `https://arxiv.org/abs/2602.08025` | `2602.08025` |
| `https://arxiv.org/pdf/2602.08025` | `2602.08025` |
| `2602.08025v1` | `2602.08025v1` |
| `2602.08025` | `2602.08025` |

解析后可将论文 ID 用于下方提到的任何 Hub API 端点。

### 以 markdown 格式获取论文页面

论文内容可以 markdown 格式获取：

```bash
curl -s "https://huggingface.co/papers/{PAPER_ID}.md"
```

这会返回 Hugging Face 论文页面的 markdown 内容，依赖 https://arxiv.org/html/{PAPER_ID} 上的论文 HTML 版本。

有 2 个例外：
- 并非所有 arXiv 论文都有 HTML 版本。如果论文的 HTML 版本不存在，内容会回退到 Hugging Face 论文页面的 HTML。
- 如果返回 404，说明该论文尚未在 hf.co/papers 上索引。参见[错误处理](#error-handling)。

也可以从普通论文页面 URL 请求 markdown：

```bash
curl -s -H "Accept: text/markdown" "https://huggingface.co/papers/{PAPER_ID}"
```

### 论文页面 API 端点

所有端点使用基础 URL `https://huggingface.co`。

#### 获取结构化元数据

使用 Hugging Face REST API 获取论文元数据（JSON 格式）：

```bash
curl -s "https://huggingface.co/api/papers/{PAPER_ID}"
```

返回的结构化元数据可能包括：

- 作者（姓名和 Hugging Face 用户名，前提是已认领论文）
- 媒体 URL（提交论文到每日论文时上传）
- 摘要（abstract）和 AI 生成的摘要
- 项目页面和 GitHub 仓库
- 组织和互动元数据（投票数）

查找与论文关联的模型：

```bash
curl https://huggingface.co/api/models?filter=arxiv:{PAPER_ID}
```

查找与论文关联的数据集：

```bash
curl https://huggingface.co/api/datasets?filter=arxiv:{PAPER_ID}
```

查找与论文关联的 Spaces：

```bash
curl https://huggingface.co/api/spaces?filter=arxiv:{PAPER_ID}
```

#### 认领论文作者身份

为 Hugging Face 用户认领论文作者身份：

```bash
curl "https://huggingface.co/api/settings/papers/claim" \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer $HF_TOKEN" \
  --data '{
    "paperId": "{PAPER_ID}",
    "claimAuthorId": "{AUTHOR_ENTRY_ID}",
    "targetUserId": "{USER_ID}"
  }'
```

- 端点：`POST /api/settings/papers/claim`
- Body：
  - `paperId`（string，必填）：要认领的 arXiv 论文标识符
  - `claimAuthorId`（string）：要认领的论文作者条目，24 字符十六进制 ID
  - `targetUserId`（string）：接收认领的 HF 用户，24 字符十六进制 ID
- 响应：论文作者认领结果，包含已认领的论文 ID

#### 获取每日论文

获取每日论文信息流：

```bash
curl -s -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/daily_papers?p=0&limit=20&date=2017-07-21&sort=publishedAt"
```

- 端点：`GET /api/daily_papers`
- 查询参数：
  - `p`（integer）：页码
  - `limit`（integer）：结果数量，1 到 100 之间
  - `date`（string）：RFC 3339 完整日期，如 `2017-07-21`
  - `week`（string）：ISO 周，如 `2024-W03`
  - `month`（string）：月份值，如 `2024-01`
  - `submitter`（string）：按提交者筛选
  - `sort`（enum）：`publishedAt` 或 `trending`
- 响应：每日论文列表

#### 列出论文

按发布日期排序列出 arXiv 论文：

```bash
curl -s -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/papers?cursor={CURSOR}&limit=20"
```

- 端点：`GET /api/papers`
- 查询参数：
  - `cursor`（string）：分页游标
  - `limit`（integer）：结果数量，1 到 100 之间
- 响应：论文列表

#### 搜索论文

对论文执行混合语义和全文搜索：

```bash
curl -s -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/papers/search?q=vision+language&limit=20"
```

搜索范围涵盖论文标题、作者和内容。

- 端点：`GET /api/papers/search`
- 查询参数：
  - `q`（string）：搜索查询，最大长度 250
  - `limit`（integer）：结果数量，1 到 120 之间
- 响应：匹配的论文

#### 索引论文

通过 ID 从 arXiv 插入论文。如果论文已被索引，只有其作者可以重新索引：

```bash
curl "https://huggingface.co/api/papers/index" \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer $HF_TOKEN" \
  --data '{
    "arxivId": "{ARXIV_ID}"
  }'
```

- 端点：`POST /api/papers/index`
- Body：
  - `arxivId`（string，必填）：要索引的 arXiv ID，如 `2301.00001`
- 模式：`^\d{4}\.\d{4,5}$`
- 响应：成功时返回空 JSON 对象

#### 更新论文链接

更新论文的项目页面、GitHub 仓库或提交组织。请求者必须是论文作者、每日论文提交者或论文管理员：

```bash
curl "https://huggingface.co/api/papers/{PAPER_OBJECT_ID}/links" \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer $HF_TOKEN" \
  --data '{
    "projectPage": "https://example.com",
    "githubRepo": "https://github.com/org/repo",
    "organizationId": "{ORGANIZATION_ID}"
  }'
```

- 端点：`POST /api/papers/{paperId}/links`
- 路径参数：
  - `paperId`（string，必填）：Hugging Face 论文对象 ID
- Body：
  - `githubRepo`（string，可为空）：GitHub 仓库 URL
  - `organizationId`（string，可为空）：组织 ID，24 字符十六进制 ID
  - `projectPage`（string，可为空）：项目页面 URL
- 响应：成功时返回空 JSON 对象

## 错误处理

- **`https://huggingface.co/papers/{PAPER_ID}` 或 `md` 端点返回 404**：该论文尚未在 Hugging Face 论文页面上索引。
- **`/api/papers/{PAPER_ID}` 返回 404**：该论文可能尚未在 Hugging Face 论文页面上索引。
- **论文 ID 未找到**：验证提取的 arXiv ID，包括版本后缀

### 回退方案

如果 Hugging Face 论文页面的信息不足以回答用户的问题：

- 查看普通论文页面 `https://huggingface.co/papers/{PAPER_ID}`
- 回退到 arXiv 页面或 PDF 获取原始来源：
  - `https://arxiv.org/abs/{PAPER_ID}`
  - `https://arxiv.org/pdf/{PAPER_ID}`

## 注意事项

- 公开论文页面无需认证。
- 写入端点（如认领作者身份、索引论文、更新论文链接）需要 `Authorization: Bearer $HF_TOKEN`。
- 优先使用 `.md` 端点获取可靠的机器可读输出。
- 需要结构化 JSON 字段而非页面 markdown 时，优先使用 `/api/papers/{PAPER_ID}`。

## 局限性
- 仅在任务明确符合上述范围时使用本技能。
- 输出不能替代针对具体环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，应停下来请求澄清。
