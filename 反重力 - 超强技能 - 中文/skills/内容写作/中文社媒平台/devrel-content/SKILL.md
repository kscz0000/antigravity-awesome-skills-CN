---
name: devrel-content
description: 当用户希望为开发者创作技术内容（包括博客文章、教程和文档）时使用本技能。触发短语包括"写一篇博客文章"、"技术文章"、"开发者内容"、"教程"、"DevRel 内容"、"开发者博客"、"技术写作"或"开发者内容..."。触发词：写博客文章、技术文章、开发者内容、教程、devrel 内容、开发者博客、技术写作、开发者内容创作、技术博客、开发者文档。
risk: unknown
source: https://github.com/jonathimer/devmarketing-skills/tree/main/skills/devrel-content
source_repo: jonathimer/devmarketing-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/jonathimer/devmarketing-skills/blob/main/LICENSE
---

# DevRel 内容
## 适用场景

当用户希望为开发者创作技术内容（包括博客文章、教程和文档）时使用本技能。触发短语包括"写一篇博客文章"、"技术文章"、"开发者内容"、"教程"、"DevRel 内容"、"开发者博客"、"技术写作"或"开发者内容..."。


本技能帮助你创作开发者真正愿意阅读的技术内容：博客文章、教程、文档以及能够建立信任并推动采用的思想领导类内容。

---

## 开始之前

**首先加载受众上下文。** 阅读 `.agents/developer-audience-context.md` 以了解：

- 你在为谁写作（角色、资历、技术栈）
- 他们的痛点（哪些问题能引发共鸣）
- 他们的原话（他们如何描述事物）
- 语气与基调（需要多正式或多技术）

如果上下文文件不存在，请先运行 `developer-audience-context` 技能。

---

## DevRel 内容框架

### 阶段 1：研究与验证

在动手写作之前，先验证这个主题值得写。

| 研究类型 | 怎么做 |
|--------------|------------|
| **搜索意图** | 在 Google 上搜索你的主题。当前已有哪些内容排名靠前？还缺什么？ |
| **社区信号** | 搜索 Reddit、Hacker News、Stack Overflow。开发者在讨论这个话题吗？ |
| **竞品空白** | 竞品已经写过什么？哪些角度还没覆盖？ |
| **内部数据** | 关于该主题的支持工单、Discord 提问、GitHub Issue |
| **关键词研究** | 使用 Ahrefs/SEMrush 查询技术术语的搜索量 |

**危险信号** — 出现下列情况时不要写：

- 你是唯一关心这个话题的人
- 已经有 10 篇类似的文章
- 主题过于宽泛（例如"JavaScript 入门"）
- 主题过于狭窄（没有搜索量，也没有社区关注）

### 阶段 2：内容类型选择

根据目标选择合适的格式：

| 内容类型 | 最适合 | 结构 |
|-------------|----------|-----------|
| **教程（Tutorial）** | 教授某项具体技能 | 步骤化、代码密集 |
| **指南（Guide）** | 全面覆盖某个主题 | 分章节、参考型 |
| **对比（Comparison）** | 帮助做决策 | 表格形式、优缺点 |
| **公告（Announcement）** | 发布功能/产品 | 新闻导语、是什么/为什么/怎么做 |
| **思想领导（Thought leadership）** | 建立权威性 | 观点、预测、立场 |
| **案例研究（Case study）** | 社会认同 | 问题 → 方案 → 成果 |
| **排错（Troubleshooting）** | 解决具体错误 | 错误 → 原因 → 修复 |

### 阶段 3：提纲结构

使用以下提纲模板：

```markdown
# [承诺具体价值的标题]

## 开场钩子（2-3 句话）
- 点出问题或机会
- 建立可信度（例如"我们迁移了 10,000 个仓库……"）
- 承诺读者将学到什么

## 背景（可选）
- 必要时给出简要背景
- 链接到前置知识

## 主体内容
### 第 1 节：[第一个核心概念]
- 解释说明
- 代码示例
- 常见陷阱

### 第 2 节：[第二个核心概念]
- 解释说明
- 代码示例
- 实际应用

### 第 3 节：[第三个核心概念]
- 解释说明
- 代码示例
- 高阶技巧

## 整合落地
- 完整示例
- 可运行代码

## 下一步
- 链接到更深入的内容
- 行动号召（试用产品、加入 Discord 等）
```

---

## 编写代码示例

代码就是内容本身，必须写对。

### 复制粘贴测试

每个代码示例都必须满足：

| 要求 | 为什么重要 |
|------------|----------------|
| **可直接运行，无需修改** | 开发者会直接复制粘贴。如果运行失败，你就失去了信任。 |
| **包含 import** | 不要假设他们知道要引入哪些库。 |
| **展示输出** | 成功运行时他们应该看到什么？ |
| **处理错误** | 真实代码都有错误处理，展示出来。 |
| **使用真实值** | 不要使用 `foo`、`bar`、`example.com`，除非确有必要。 |

### 代码示例结构

```markdown
首先，安装依赖：

\`\`\`bash
npm install your-library axios
\`\`\`

接下来创建一个名为 `fetch-data.js` 的文件：

\`\`\`javascript
// fetch-data.js
import { Client } from 'your-library';
import axios from 'axios';

const client = new Client({
  apiKey: process.env.YOUR_API_KEY // 使用环境变量
});

async function fetchUserData(userId) {
  try {
    const user = await client.users.get(userId);
    console.log(`Fetched user: ${user.name}`);
    return user;
  } catch (error) {
    console.error(`Failed to fetch user: ${error.message}`);
    throw error;
  }
}

// 使用示例
fetchUserData('user_123')
  .then(user => console.log(user))
  .catch(err => process.exit(1));
\`\`\`

运行它：

\`\`\`bash
YOUR_API_KEY=sk_test_xxx node fetch-data.js
\`\`\`

预期输出：

\`\`\`
Fetched user: Jane Developer
{ id: 'user_123', name: 'Jane Developer', email: 'jane@example.dev' }
\`\`\`
```

### 各语言约定

| 语言 | 代码块标识 | 包安装命令 | 环境变量 |
|----------|-----------|-----------------|----------|
| JavaScript/Node | `javascript` 或 `js` | `npm install` | `process.env.VAR` |
| TypeScript | `typescript` 或 `ts` | `npm install` | `process.env.VAR` |
| Python | `python` 或 `py` | `pip install` | `os.environ['VAR']` |
| Go | `go` | `go get` | `os.Getenv("VAR")` |
| Rust | `rust` | `cargo add` | `std::env::var("VAR")` |
| Shell | `bash` 或 `shell` | N/A | `$VAR` |

---

## 技术准确性检查清单

发布前请逐项过一遍：

| 检查项 | 如何验证 |
|-------|---------------|
| **代码可运行** | 复制粘贴每个代码片段并执行 |
| **版本匹配** | 是否使用了最新的库版本？ |
| **链接有效** | 逐一点击每个链接 |
| **命令可执行** | 运行每个 CLI 命令 |
| **截图保持最新** | UI 截图是否与当前产品一致？ |
| **未使用已废弃 API** | 检查所用 API 是否已被废弃 |
| **安全审查** | 不包含硬编码密钥、SQL 注入等 |
| **同行评审** | 请一位工程师通读以确保准确性 |

---

## 面向开发者内容的 SEO

开发者使用 Google 的方式与普通消费者不同。

### 开发者的搜索模式

| 模式 | 搜索示例 |
|---------|----------------|
| **错误信息** | "TypeError: Cannot read property 'map' of undefined" |
| **How to** | "how to deploy next.js to vercel" |
| **对比** | "prisma vs typeorm 2024" |
| **最佳实践** | "typescript project structure best practices" |
| **替代方案** | "alternatives to firebase" |
| **搭配使用** | "react with typescript tutorial" |

### 技术 SEO 检查清单

| 元素 | 最佳实践 |
|---------|--------------|
| **标题（Title）** | 包含主关键词、框架名称、相关年份 |
| **Meta 描述** | 150 字以内，包含关键词，承诺具体成果 |
| **H1** | 与标题一致或高度接近 |
| **H2** | 包含次级关键词，便于扫读 |
| **代码块** | 使用正确的语法高亮（有助于获得精选摘要） |
| **内链** | 链接到相关文档、教程、API 参考 |
| **外链** | 链接到所提及工具的官方文档 |
| **URL slug** | 小写、连字符、包含关键词 |

### 优化标题示例

| 不佳 | 良好 |
|-----|------|
| "Using Our API" | "How to Authenticate with the YourProduct API (Node.js)" |
| "Database Guide" | "PostgreSQL Connection Pooling: Complete Guide with pgBouncer" |
| "Getting Started" | "Getting Started with YourProduct: Your First API Call in 5 Minutes" |

---

## 内容质量信号

优秀 DevRel 内容与平庸内容的区别在于：

### 应当这样做

- **展示而非讲述** — 用代码代替大段文字
- **回应"为什么"** — 不仅是怎么做，还包括何时做、为何做
- **承认取舍** — 没有完美方案；开发者尊重诚实
- **引用来源** — 官方文档、RFC、相关文章
- **标注日期** — "更新于 2024 年 3 月"或带上版本号
- **渐进式披露** — 从简单入手，逐步增加复杂度
- **真实示例** — 生产场景，而非 hello world

### 不要这样做

- **一整面文字墙** — 用代码、标题、列表来打断节奏
- **营销腔** — "业界领先"、"无缝"、"颠覆性"
- **假设读者已具备知识** — 解释缩写，链接前置知识
- **过时内容** — 没有比一篇用着废弃 API 的 2019 年教程更糟糕的事了
- **埋没要点** — 先给答案，再做解释
- **没有代码** — 开发者来看代码，不是来看散文的

---

## 内容模板

### 博客文章模板

```markdown
# [具体、富含关键词的标题]

[2-3 句开场钩子：问题 + 承诺]

## 问题

[1 段说明痛点]

## 解决方案

[简要说明你的思路]

### 第 1 步：[动作]

[解释说明]

\`\`\`language
// Code
\`\`\`

### 第 2 步：[动作]

[解释说明]

\`\`\`language
// Code
\`\`\`

### 第 3 步：[动作]

[解释说明]

\`\`\`language
// Code
\`\`\`

## 完整示例

\`\`\`language
// 完整可运行代码
\`\`\`

## 排错

### [常见错误 1]
[解决方案]

### [常见错误 2]
[解决方案]

## 下一步

- [深入内容的链接]
- [相关教程的链接]
- [行动号召：亲自试一试]
```

### 对比文章模板

```markdown
# [工具 A] vs [工具 B]：[具体使用场景]（[年份]）

[1 段：本文适合谁，以及你将学到什么]

## 快速对比

| 特性 | 工具 A | 工具 B |
|---------|--------|--------|
| [特性 1] | | |
| [特性 2] | | |
| [特性 3] | | |

## 何时选择 [工具 A]

- [场景 1]
- [场景 2]
- [场景 3]

## 何时选择 [工具 B]

- [场景 1]
- [场景 2]
- [场景 3]

## 深度剖析：[具体方面]

### 工具 A 的做法
[解释说明 + 代码]

### 工具 B 的做法
[解释说明 + 代码]

## 我们的推荐

[基于使用场景的具体建议]
```

---

## 衡量内容效果

### 需要追踪的指标

| 指标 | 含义 |
|--------|------------------|
| **页面浏览量** | 触达范围（但脱离上下文就是虚荣指标） |
| **页面停留时间** | 参与度（他们真的在读吗？） |
| **滚动深度** | 是否读到了最后？ |
| **跳出率** | 是否找到了他们需要的内容？ |
| **搜索排名** | SEO 表现 |
| **反向链接** | 权威性与被引用价值 |
| **社交分享** | 共鸣度（尤其是 HN、Twitter、Reddit） |
| **转化事件** | 注册、安装、文档点击 |

### 内容 → 转化路径

追踪完整旅程：

1. 搜索/社交 → 博客文章
2. 博客文章 → 文档 / 快速上手
3. 文档 → 注册 / 安装
4. 注册 → 激活（首次成功）

---

## 工具

| 工具 | 用途 |
|------|----------|
| **[Octolens](https://octolens.com)** | 监控内容在 HN、Reddit、Twitter 的分享情况；追踪竞品内容表现；从开发者讨论中挖掘选题灵感。 |
| **Grammarly / Hemingway** | 可读性与语法检查 |
| **Carbon / Ray.so** | 美观的代码截图 |
| **Excalidraw** | 技术示意图 |
| **Loom** | 快速录屏讲解 |
| **Ahrefs / SEMrush** | 关键词研究与 SEO 追踪 |
| **Google Search Console** | 追踪搜索表现 |

---

## 相关技能

- `developer-audience-context` — 了解读者的基础
- `technical-tutorials` — 深入探讨步骤化内容
- `developer-newsletter` — 通过邮件分发内容
- `developer-seo` — 技术 SEO 优化
- `hacker-news-strategy` — 在 HN 上高效分享内容

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时才使用本技能。
- 在应用变更之前，请验证命令、生成的代码、依赖、凭证以及外部服务行为。
- 不要把示例当作针对特定环境的测试、安全审查，或用户对破坏性或高成本操作的审批的替代品。