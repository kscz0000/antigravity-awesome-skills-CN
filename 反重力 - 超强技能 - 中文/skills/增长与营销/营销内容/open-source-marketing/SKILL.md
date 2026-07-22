---
name: open-source-marketing
description: 当用户想要以真诚方式推广开源项目时使用。触发词：开源营销、OSS营销、GitHub推广、推广我的库、增长Star、开源发布、开源增长、贡献者营销。
risk: unknown
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/open-source-marketing
source_repo: jonathimer/devmarketing-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/jonathimer/devmarketing-skills/blob/main/LICENSE
---

# 开源营销
## 何时使用

当用户想要以真诚方式推广开源项目时使用此技能。触发词：开源营销、OSS营销、GitHub推广、推广我的库、增长Star、开源发布、开源增长、贡献者营销。

本技能帮助你推广开源项目而不让人反感。涵盖 GitHub 优化、社区建设、贡献者体验、发布策略和可持续增长。

---

## 开始之前

**先加载你的受众上下文。** 阅读 `.agents/developer-audience-context.md` 以了解：

- 谁会使用这个项目（角色、技术栈、痛点）
- 他们在哪里发现工具（社区、社交媒体、搜索）
- 有哪些替代方案（为什么他们会切换？）
- 他们如何评估开源项目（Star、活跃度、文档、社区）

如果上下文文件不存在，先运行 `developer-audience-context` 技能。

---

## 开源营销思维

### 什么有效 vs. 什么无效

| 有效 | 无效 |
|------|------|
| 公开构建过程 | 到处刷"看看我的项目" |
| 解决真实问题 | 先有方案再找问题 |
| 真诚的社区互动 | 功利性的关注/取关 |
| 优秀的文档和开发者体验 | "代码本身就是文档" |
| 庆祝贡献者 | 独揽功劳 |
| 持续活跃 | 发布后消失 |

### 增长公式

```
Growth = (Real value) × (Discoverability) × (First-use experience)
```

任何一个因子为零，增长就为零。

---

## GitHub 优化

### README 优化

你的 README 就是你的落地页。把它优化好。

**结构：**

```markdown
# Project Name

[One-line description that explains what it does]

[Badges: build status, version, license, downloads]

[Screenshot or GIF showing it in action]

## Why [Project Name]?

- ✅ [Benefit 1 - specific, not fluffy]
- ✅ [Benefit 2]
- ✅ [Benefit 3]

## Quick Start

\`\`\`bash
npm install project-name
\`\`\`

\`\`\`javascript
// 5 lines that show immediate value
\`\`\`

## Installation

[Detailed installation for all platforms]

## Usage

[Core usage patterns with examples]

## Documentation

[Link to full docs]

## Contributing

We love contributions! See [CONTRIBUTING.md](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/open-source-marketing/CONTRIBUTING.md).

## License

[License type] - see [LICENSE](https://github.com/jonathimer/devmarketing-skills/tree/main/skills/open-source-marketing/LICENSE)
```

### README 检查清单

| 要素 | 为何重要 |
|------|----------|
| **清晰的名称** | 易记、可搜索、好拼写 |
| **一句话描述** | "一个面向[受众]的[类型]，能够[做什么]" |
| **徽章** | 社会证明、健康信号 |
| **视觉展示** | GIF > 截图 > 无 |
| **快速上手** | <5 行代码即可体验价值 |
| **为什么选它？** | 与替代方案的差异化 |
| **安装说明** | 覆盖所有平台，可直接复制 |
| **示例** | 真实用例，非人为构造 |
| **文档链接** | 提供更多细节 |
| **贡献指南** | 欢迎社区参与 |

### 仓库优化

| 要素 | 最佳实践 |
|------|----------|
| **描述** | 最多 100 字符，关键词丰富 |
| **Topics** | 5-10 个相关标签，提升可发现性 |
| **网站** | 链接到文档或落地页 |
| **Releases** | 语义化版本号、更新日志 |
| **Issues** | Bug/功能请求模板 |
| **Discussions** | 启用以支持社区问答 |
| **Sponsors** | 如需资金支持则启用 |

### Issue 和 PR 模板

**Bug 报告模板：**

```markdown
---
name: Bug Report
about: Report a bug to help us improve
---

## Bug Description
[Clear description]

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS:
- Node version:
- Package version:

## Additional Context
[Screenshots, logs, etc.]
```

**功能请求模板：**

```markdown
---
name: Feature Request
about: Suggest an idea for this project
---

## Problem
[What problem does this solve?]

## Proposed Solution
[How would you like it to work?]

## Alternatives Considered
[Other approaches you've thought about]

## Additional Context
[Examples, mockups, etc.]
```

---

## 社区建设

### 社区平台

| 平台 | 最适合 | 搭建成本 |
|------|--------|----------|
| **GitHub Discussions** | 问答、公告 | 低 |
| **Discord** | 实时聊天、社区氛围 | 中 |
| **Slack** | 企业社区 | 中 |
| **论坛（Discourse）** | 异步、可搜索的讨论 | 高 |

从 GitHub Discussions 开始。当活跃用户超过 50 人时再加 Discord。

### 社区原则

| 原则 | 实施方式 |
|------|----------|
| **及时响应** | 48 小时内回复 Issue（即使只是"正在查看"） |
| **庆祝贡献** | 公开感谢每位贡献者 |
| **保持透明** | 分享路线图，解释决策 |
| **设定期望** | 明确维护者响应 SLA |
| **欢迎新人** | "good first issue" 标签、导师制 |

### 贡献者漏斗

```
User → Star → Issue → PR → Regular Contributor → Maintainer
```

优化每个转化环节：

| 转化环节 | 如何改进 |
|----------|----------|
| 用户 → Star | 优秀的 README，价值可见 |
| Star → Issue | 清晰的 Issue 模板，友好的语气 |
| Issue → PR | "good first issue" 标签、CONTRIBUTING.md |
| PR → 常规贡献者 | 快速 Review，鼓励性反馈 |
| 常规贡献者 → 维护者 | 信任、共享所有权 |

---

## 贡献者体验

### CONTRIBUTING.md 要点

```markdown
# Contributing to [Project]

First off, thanks for considering contributing! ❤️

## Quick Start

1. Fork the repo
2. Clone your fork
3. Install dependencies: `npm install`
4. Create a branch: `git checkout -b my-feature`
5. Make your changes
6. Run tests: `npm test`
7. Commit: `git commit -m "Add my feature"`
8. Push: `git push origin my-feature`
9. Open a Pull Request

## Development Setup

[Detailed setup instructions]

## Code Style

- We use [Prettier/ESLint config]
- Run `npm run lint` before committing
- [Other conventions]

## Commit Messages

We follow [Conventional Commits](https://conventionalcommits.org/):
- `feat: add new feature`
- `fix: resolve bug`
- `docs: update readme`
- `chore: update dependencies`

## Pull Request Process

1. Update docs if needed
2. Add tests for new features
3. Ensure CI passes
4. Get one approval

## Good First Issues

Look for issues labeled `good first issue` — these are great starting points!

## Questions?

Open a Discussion or reach out on Discord.
```

### "Good First Issue" 策略

创建真正容易上手的问题：

| 好的 | 不好的 |
|------|--------|
| "为 X 函数添加 TypeScript 类型" | "重构整个代码库" |
| "修复 README 中的拼写错误" | "性能优化" |
| "为 Y 方法添加测试" | "调试间歇性 CI 故障" |
| "更新依赖 Z" | "根据 RFC 实现功能" |

每个 good first issue 应包含：
- 解释上下文及为何重要
- 链接到相关代码文件
- 描述预期结果
- 在评论中提供帮助

---

## 发布策略

### 发布前检查清单

| 任务 | 完成？ |
|------|--------|
| README 已打磨 | ☐ |
| 快速上手可用 | ☐ |
| 文档已就位 | ☐ |
| 3+ 个示例/演示 | ☐ |
| 测试通过 | ☐ |
| 已选择许可证 | ☐ |
| CONTRIBUTING.md | ☐ |
| Issue 模板 | ☐ |
| 社交预览图 | ☐ |
| 5-10 个 GitHub Topics | ☐ |

### 发布日行动手册

**时间线：**

| 时间 | 行动 |
|------|------|
| **前一天** | 最终审查 README，准备所有帖子 |
| **发布日上午** | 发 Hacker News 帖子（最佳：太平洋时间周二至周四 6-8am） |
| **+1 小时** | 发 Twitter 主题帖 |
| **+2 小时** | 在相关 Subreddit 发 Reddit 帖子 |
| **全天** | 回复所有评论/问题 |
| **日终** | 感谢所有人，分享数据 |

### 各平台策略

**Hacker News：**
- 标题：描述性的，不夸大（"Show HN: X — a Y for Z"）
- 首条评论：解释动机和技术决策
- 保持在线数小时以回应
- 不要求赞（必死无疑）

**Reddit：**
- 找 2-3 个相关 Subreddit（不只是 r/programming）
- 先读规则
- 做社区成员，不做营销者
- 分享真正有用的上下文

**Twitter/X：**
- 主题帖格式：问题 → 方案 → 演示 → 链接
- 附上 GIF/视频
- 标记相关账号（框架作者等）
- 分享公开构建的历程

**Dev.to / Hashnode：**
- 写一篇"我为什么做了这个"文章
- 技术深度，个人故事
- 从你的博客交叉发布

### 发布后

| 周次 | 重点 |
|------|------|
| **第 1 周** | 回复所有反馈，修复 Bug |
| **第 2 周** | 博客文章："发布中学到了什么" |
| **第 3 周** | 开始定期更新，发布新功能 |
| **第 1 个月** | 社区建设，贡献者文档 |
| **持续** | 稳定活跃，定期发布 |

---

## 可持续增长

### 增长策略

| 策略 | 投入 | 影响 | 周期 |
|------|------|------|------|
| **SEO 优化文档** | 中 | 高 | 3-6 个月 |
| **集成教程** | 中 | 高 | 1-2 个月 |
| **会议演讲** | 高 | 中 | 3-6 个月 |
| **对比内容** | 低 | 中 | 1-2 个月 |
| **客座博客** | 中 | 中 | 1-2 个月 |
| **Newsletter 推荐** | 低 | 低-中 | 2-4 周 |
| **Twitter 运营** | 中 | 中 | 持续 |

### 开源内容策略

| 内容类型 | 目的 |
|----------|------|
| **"我们为什么做了 X"** | 发布故事、动机 |
| **"X vs Y vs Z"** | 捕获对比搜索流量 |
| **"从 Y 迁移到 X"** | 转化竞品用户 |
| **"X + [热门工具]"** | 捕获集成搜索流量 |
| **"我们在 [公司] 如何使用 X"** | 社会证明、真实用例 |
| **"X 性能基准测试"** | 技术可信度 |

### 避免倦怠

| 风险 | 缓解措施 |
|------|----------|
| **Issue 压力过大** | 设定响应 SLA 预期 |
| **功能需求过多** | 公开路线图、RFC 流程 |
| **独自维护** | 积极招募共同维护者 |
| **全天候压力** | 安排固定"办公时间"而非 24/7 |
| **负面反馈** | 行为准则、适度管理 |

---

## 关键指标

### 虚荣指标 vs. 价值指标

| 虚荣指标 | 价值指标 |
|----------|----------|
| Star 数 | 活跃 Issue + PR 数 |
| Fork 数 | 回归贡献者数 |
| 下载量 | 周活跃用户数 |
| Twitter 粉丝 | 社区互动度 |

### 追踪什么

| 指标 | 去哪看 |
|------|--------|
| **Star 增长趋势** | GitHub Insights、Star History |
| **克隆数** | GitHub Traffic |
| **来源引荐** | GitHub Traffic |
| **npm 下载量** | npm-stat.com |
| **社区规模** | Discord/Slack 成员数 |
| **贡献者数量** | GitHub Insights |
| **Issue 响应时间** | 手动追踪 |

---

## 工具

| 工具 | 用途 |
|------|------|
| **[Octolens](https://octolens.com)** | 监控你的项目在 GitHub、HN、Reddit、Twitter 和 Stack Overflow 上的提及。追踪竞品项目。发现提问的贡献者。 |
| **Star History** | 追踪 Star 增长趋势 |
| **npm-stat** | 下载统计 |
| **GitHub Traffic** | 访问量、克隆数、引荐来源 |
| **Shield.io** | 动态徽章 |
| **All Contributors** | 认可所有贡献者 |
| **Probot** | 自动化 GitHub 工作流 |

---

## 相关技能

- `developer-audience-context` — 了解你的用户
- `community-building` — 建立 Discord/Slack 社区
- `devrel-content` — 创建配套内容
- `developer-advocacy` — 会议演讲、播客
- `hacker-news-strategy` — 在 HN 上发布和互动

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用变更前，验证命令、生成的代码、依赖、凭证和外部服务行为。
- 不要将示例替代针对特定环境的测试、安全审查，或用户对破坏性/高成本操作的审批。
