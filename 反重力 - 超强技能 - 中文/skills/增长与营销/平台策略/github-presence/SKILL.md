---
name: github-presence
description: 当用户希望优化他们的 GitHub 个人资料、README 或项目可发现性时使用。触发短语包括"GitHub README"、"README 优化"、"GitHub 个人资料"、"GitHub stars"、"GitHub 可发现性"、"awesome 列表"或"GitHub 营销"。
risk: unknown
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/github-presence
source_repo: jonathimer/devmarketing-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/jonathimer/devmarketing-skills/blob/main/LICENSE
---

# GitHub 影响力
## 何时使用

当用户希望优化他们的 GitHub 个人资料、README 或项目可发现性时使用此技能。触发短语包括"GitHub README"、"README 优化"、"GitHub 个人资料"、"GitHub stars"、"GitHub 可发现性"、"awesome 列表"或"GitHub 营销"。


GitHub 是开发者在试用你的项目之前评估它的地方。本技能涵盖 README 优化、个人资料 README、通过 Topics 和 awesome 列表提升可发现性，以及利用 GitHub 功能进行营销。

---

## 开始之前

1. 若存在则阅读 `.agents/developer-audience-context.md`
2. 审计你当前的 GitHub 影响力（个人资料、置顶仓库、README）
3. 理解：GitHub 通常是第一次技术评估——请相应优化

---

## README 结构

### 优秀 README 的结构

| 章节 | 用途 | 是否必需 |
|---------|---------|-----------|
| **Logo/Banner** | 品牌识别、视觉吸引力 | 推荐 |
| **Badges** | 快速信任信号、状态 | 推荐 |
| **One-liner** | 一句话讲清楚它是干什么的 | 必需 |
| **Hero example** | 立即展示"长什么样" | 强烈推荐 |
| **Features** | 相比替代品的优势 | 必需 |
| **Quick start** | 在 2 分钟内跑起来 | 必需 |
| **Installation** | 所有安装方式 | 必需 |
| **Usage** | 核心用法示例 | 必需 |
| **Documentation** | 指向完整文档的链接 | 必需 |
| **Contributing** | 如何贡献 | 推荐 |
| **License** | 法律说明 | 必需 |

### README 模板

```markdown
<div align="center">
  <img src="logo.svg" alt="Project Name" width="200">
  <h1>Project Name</h1>
  <p><strong>One compelling sentence explaining what this does.</strong></p>

  <!-- Badges -->
  <a href="https://github.com/org/repo/actions"><img src="https://github.com/org/repo/workflows/CI/badge.svg" alt="CI"></a>
  <a href="https://www.npmjs.com/package/name"><img src="https://img.shields.io/npm/v/name.svg" alt="npm version"></a>
  <a href="https://github.com/org/repo/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <a href="https://discord.gg/invite"><img src="https://img.shields.io/discord/123456789" alt="Discord"></a>

  <br>
  <br>

  <a href="https://docs.example.com">Documentation</a> •
  <a href="https://example.com">Website</a> •
  <a href="https://discord.gg/invite">Discord</a>
</div>

---

## Why Project Name?

- **Feature 1** — Brief explanation
- **Feature 2** — Brief explanation
- **Feature 3** — Brief explanation

## Quick Start

```bash
npm install project-name
```

```javascript
import { thing } from 'project-name';

const result = thing.doSomething();
console.log(result);
```

## Installation

### npm
```bash
npm install project-name
```

### yarn
```bash
yarn add project-name
```

### pnpm
```bash
pnpm add project-name
```

## Usage

### Basic Example

```javascript
// Code example with comments
```

### Advanced Example

```javascript
// More complex example
```

## Documentation

Full documentation available at [docs.example.com](https://docs.example.com)

- [Getting Started](https://docs.example.com/getting-started)
- [API Reference](https://docs.example.com/api)
- [Examples](https://docs.example.com/examples)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/github-presence/CONTRIBUTING.md) for details.

## License

MIT © [Your Name](https://yoursite.com)
```

---

## 真正重要的 Badges

### 信任信号类 Badges

| Badge | 含义 | 使用时机 |
|-------|--------------|-------------|
| CI/Build status | 代码质量 | 始终 |
| Version | 最新发布版本 | 包类项目始终 |
| License | 法律说明 | 始终 |
| Downloads/installs | 采用度 | 数据亮眼时 |
| Coverage | 测试质量 | 覆盖率 > 70% 时 |
| Security | 审计状态 | 有安全审计时 |

### 社区类 Badges

| Badge | 来源 | 用途 |
|-------|--------|---------|
| Discord members | shields.io | 展示活跃社区 |
| GitHub stars | shields.io | 社会认同 |
| Contributors | shields.io | 开源健康度 |
| Last commit | shields.io | 项目活跃度 |

### Badge 服务

| 服务 | URL | 最适合 |
|---------|-----|----------|
| Shields.io | shields.io | 大多数 badges |
| Badgen | badgen.net | 快速、极简 |
| GitHub badges | Native | Actions、issues |

### Badge 示例

```markdown
<!-- Build status -->
![CI](https://github.com/org/repo/workflows/CI/badge.svg)

<!-- npm version -->
[![npm](https://img.shields.io/npm/v/package-name.svg)](https://www.npmjs.com/package/package-name)

<!-- Downloads -->
[![Downloads](https://img.shields.io/npm/dm/package-name.svg)](https://www.npmjs.com/package/package-name)

<!-- License -->
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

<!-- Discord -->
[![Discord](https://img.shields.io/discord/SERVER_ID?color=7289da&logo=discord&logoColor=white)](https://discord.gg/invite)

<!-- Stars -->
[![GitHub stars](https://img.shields.io/github/stars/org/repo?style=social)](https://github.com/org/repo)
```

---

## 个人资料 README

### 设置个人资料 README

1. 创建一个与你用户名同名的仓库（例如 `github.com/yourname/yourname`）
2. 添加 `README.md` 文件
3. 该文件会展示在你的个人资料页

### 个人资料 README 结构

```markdown
# Hi, I'm [Name] 👋

[One sentence about what you do]

## What I'm Working On

- 🔭 Building [project] — [brief description]
- 🌱 Learning [technology]
- 💬 Ask me about [expertise areas]

## Projects

| Project | Description | Stars |
|---------|-------------|-------|
| [Project 1](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/github-presence/link) | Brief description | ![Stars](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/github-presence/badge) |
| [Project 2](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/github-presence/link) | Brief description | ![Stars](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/github-presence/badge) |

## Recent Blog Posts

<!-- BLOG-POST-LIST:START -->
<!-- Automated with GitHub Actions -->
<!-- BLOG-POST-LIST:END -->

## Connect

[![Twitter](https://img.shields.io/badge/-Twitter-1DA1F2?style=flat&logo=twitter&logoColor=white)](https://twitter.com/handle)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/handle)

## GitHub Stats

![Your GitHub stats](https://github-readme-stats.vercel.app/api?username=yourusername&show_icons=true)
```

### 个人资料 README 最佳实践

| 应该做 | 不要做 |
|----|-------|
| 保持易扫读 | 写大段文字 |
| 展示你最好的项目 | 列举所有项目 |
| 包含当前的工作 | 让它过时 |
| 添加联系方式 | 让人难以联系到你 |
| 展现个性 | 千篇一律 |

---

## 可发现性

### GitHub Topics

Topics 是别人找到你的仓库的方式。针对搜索进行优化。

| Topic 策略 | 示例 |
|----------------|---------|
| 技术 | `javascript`、`rust`、`python` |
| 框架 | `react`、`nextjs`、`django` |
| 用途 | `cli`、`api`、`testing` |
| 类别 | `developer-tools`、`devops` |
| 问题域 | `authentication`、`caching` |

**添加 topics**：仓库设置 → Topics（最多 20 个）

### 搜索优化

GitHub 搜索会考虑以下因素：
1. **仓库名称** — 包含主要关键词
2. **描述** — 350 字符，富含关键词
3. **README 内容** — 全文被索引
4. **Topics** — 类目匹配
5. **语言** — 自动检测

### Awesome 列表

进入 awesome 列表会带来流量和信誉。

| 步骤 | 操作 |
|------|--------|
| 1 | 找到相关的 awesome 列表（搜索 "awesome + [主题]"） |
| 2 | 查看列表的要求（质量、活跃度、文档） |
| 3 | 确保你的项目符合标准 |
| 4 | 按列表规范提交 PR |
| 5 | 保持耐心——策展需要时间 |

**面向开发者工具的热门 awesome 列表**：
- `awesome-cli-apps`
- `awesome-selfhosted`
- `awesome-nodejs`
- `awesome-python`
- `awesome-go`
- `awesome-rust`
- `awesome-devops`

---

## 用于营销的 GitHub Actions

### 自动更新 README

```yaml
# .github/workflows/readme-update.yml
name: Update README

on:
  schedule:
    - cron: '0 0 * * *'  # Daily
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Example: Update blog post list
      - uses: gautamkrishnar/blog-post-workflow@master
        with:
          feed_list: "https://yourblog.com/feed"

      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git diff --quiet && git diff --staged --quiet || git commit -m "Update README"
          git push
```

### 指标与统计

```yaml
# Auto-update GitHub stats image
- uses: lowlighter/metrics@latest
  with:
    token: ${{ secrets.METRICS_TOKEN }}
    filename: github-metrics.svg
```

### 发布公告

```yaml
# Tweet on new release
name: Release Announcement
on:
  release:
    types: [published]

jobs:
  announce:
    runs-on: ubuntu-latest
    steps:
      - name: Tweet
        uses: ethomson/send-tweet-action@v1
        with:
          status: "🚀 ${{ github.repository }} ${{ github.event.release.tag_name }} released! ${{ github.event.release.html_url }}"
          consumer-key: ${{ secrets.TWITTER_CONSUMER_KEY }}
          # ... other secrets
```

---

## GitHub Sponsors

### 启用 Sponsors

1. 加入 GitHub Sponsors（github.com/sponsors）
2. 撰写有吸引力的赞助档位说明
3. 在仓库中设置 funding.yml

**funding.yml 示例**：
```yaml
github: [yourusername]
patreon: yourpatreon
open_collective: yourproject
ko_fi: yourkofi
custom: ["https://buymeacoffee.com/you"]
```

### 真正有效的赞助档位

| 档位 | 价格 | 内容 |
|------|-------|-------|
| **支持者** | $5/月 | 致谢 + 在 README 中署名 |
| **赞助者** | $15/月 | README 中展示 Logo + Discord 角色 |
| **主赞助** | $50/月 | 优先支持 + 功能投票权 |
| **企业赞助** | $200+/月 | 专属支持 + 咨询 |

---

## 平台特定的是与非

### 应该做

1. **做**优化 README，给用户留下良好第一印象
2. **做**使用 badges 提供快速信任信号
3. **做**添加相关 topics（最多 20 个）
4. **做**保持个人资料 README 与时俱进
5. **做**及时响应 issues 和 PR
6. **做**置顶你最好的仓库
7. **做**提供清晰的安装说明
8. **做**向相关的 awesome 列表提交

### 不要做

1. **不要**忽视 README——它是你的落地页
2. **不要**使用过多 badges（显得杂乱）
3. **不要**让 issues 堆积不回复
4. **不要**忘记 license 文件
5. **不要**使用低质量或失效的图片
6. **不要**写没有结构的大段文字
7. **不要**忽视贡献指南

---

## 衡量成功

### 需要跟踪的 GitHub 指标

| 指标 | 含义 | 目标 |
|--------|-------------------|------|
| Stars | 兴趣/收藏 | 持续增长 |
| Forks | 实际使用 | 重质不重量 |
| Clones | 正在尝试的人 | 安装前的兴趣 |
| Traffic | 个人资料/仓库访问量 | 知名度 |
| Referrers | 流量来源 | 渠道有效性 |
| Contributors | 社区健康度 | 可持续的项目 |

### 流量洞察

访问方式：仓库 → Insights → Traffic

- 浏览量与独立访客数
- 热门内容（哪些文件）
- 引荐站点
- Clone 活动

---

## 工具

| 工具 | 用途 |
|------|----------|
| **[Octolens](https://octolens.com)** | 监控 GitHub 上对你的项目、竞品以及相关讨论的提及。在有人讨论你所解决的问题时获得提醒。 |
| **Shields.io** | 生成状态 badges |
| **GitHub Readme Stats** | 个人资料的动态统计 |
| **Carbon** | 精美的代码截图 |
| **readme.so** | README 生成器 |
| **Metrics** | 高级个人资料统计 |

---

## README 审计清单

- [ ] 名称和描述清晰、富含关键词
- [ ] Badges 展示 CI 状态、版本、License
- [ ] 一句话说明它是干什么的
- [ ] 快速入门让用户在 2 分钟内跑起来
- [ ] 代码示例可直接复制粘贴
- [ ] 所有链接有效且为 HTTPS
- [ ] 图片带有 alt 文本
- [ ] 在移动端可读
- [ ] 有 License 文件
- [ ] 有贡献指南
- [ ] 设置了 Topics（最多 20 个）
- [ ] 上传了社交预览图

---

## 相关技能

- `developer-audience-context` — 了解谁会评估你的仓库
- `hacker-news-strategy` — HN 用户在点赞前会先看 GitHub
- `reddit-engagement` — Reddit 用户通过 GitHub 评估
- `dev-to-hashnode` — 从 README 链接到内容

## 局限

- 仅当任务明确匹配其上游来源与本地项目上下文时才使用此技能。
- 在应用任何变更前，请验证命令、生成的代码、依赖、凭据以及外部服务的行为。
- 不要把示例当作环境特定测试、安全审查，或对破坏性/高成本操作的用户授权的替代。
