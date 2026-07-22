---
name: efficient-web-research
risk: safe
description: >
  用于节省 token 的网络研究协议。当访问 URL、GitHub 仓库或运行搜索查询时使用。可防止整页抓取造成的浪费。
---

# 高效网络研究技能

一种以最节省 token、最准确、最结构化的方式访问网络内容的协议——
在合适的深度使用合适的工具，并在问题可回答时立即停止。

---

## 核心原则

> **抓取回答所需的最小信息。先略读，再深入。能回答时就停止。**

每次不必要的抓取都会浪费 token 并增加噪音。本技能强制采用分层方法，
仅当浅层失败时才升级抓取深度。

---

## 步骤 1 — 对输入进行分类

在抓取任何内容之前，先识别收到的输入类型：

| 输入类型 | 示例 | 跳转至 |
|---|---|---|
| GitHub 仓库 URL | `github.com/user/repo` | [GitHub 协议](#github-协议) |
| 具体页面 URL | `docs.python.org/3/library/os` | [URL 协议](#url-协议) |
| 主题 / 查询（无 URL） | "RAFT 一致性是如何工作的" | [搜索协议](#搜索协议) |
| 多个 URL | 链接列表 | [多 URL 协议](#多-url-协议) |
| PDF / 文件链接 | `.pdf`、`.txt`、`.md` URL | [文件协议](#文件协议) |

---

## GitHub 协议

当输入为 GitHub URL（仓库、文件、PR、Issue 等）时使用。

### 步骤 1 — 解析 URL

```
github.com/{owner}/{repo}                → 仓库根目录
github.com/{owner}/{repo}/tree/{branch}  → 目录
github.com/{owner}/{repo}/blob/{branch}/{path} → 单个文件
github.com/{owner}/{repo}/issues/{n}     → Issue
github.com/{owner}/{repo}/pull/{n}       → Pull Request
```

### 步骤 2 — 优先使用 GitHub API（优于爬取）

始终优先使用 GitHub API。它返回干净的 JSON——无需解析 HTML。

```
# 仓库元数据（名称、描述、语言、星标、主题）
GET https://api.github.com/repos/{owner}/{repo}

# 文件树（查看有哪些文件——非常便宜）
GET https://api.github.com/repos/{owner}/{repo}/git/trees/{ref}?recursive=1

# 单个文件内容（base64 编码）
GET https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}

# 仅 README（通常足以理解仓库）
GET https://api.github.com/repos/{owner}/{repo}/readme
```

### 步骤 3 — 仓库的分层抓取

```
第 1 层（始终先做）：
  → 抓取仓库元数据 + 仅 README
  → 现在能回答用户的问题吗？能 → 停止。不能 → 继续。

第 2 层（仅在需要时）：
  → 抓取文件树以了解结构
  → 根据问题识别最相关的 1-3 个文件
  → 现在能回答吗？能 → 停止。不能 → 继续。

第 3 层（最后手段）：
  → 仅抓取特定的相关文件（绝不抓取所有文件）
  → 优先级：主入口点、配置文件、关键模块
```

### GitHub 的 Token 规则

- 仅 README 就能回答约 70% 的"这个仓库是做什么的"类问题——始终先尝试
- 在单次研究回合中，绝不抓取超过 3 个文件
- 如果文件超过约 300 行，仅读取顶部（import + 类/函数签名）
- 在传入上下文之前解码 API 返回的 base64 内容

---

## URL 协议

当用户提供具体的非 GitHub URL（文档、文章、博客等）时使用。

### 步骤 1 — 评估 URL 类型

| 网站类型 | 适合使用 | 备注 |
|---|---|---|
| 静态文档 / MDN / ReadTheDocs | `read_url_content` | 快速、干净、便宜 |
| 新闻文章 / 博客 | `read_url_content` | 通常没问题 |
| SPA / React/Next.js 应用 | `browser_subagent` | JS 渲染 |
| 需要认证的页面 | `browser_subagent` | 需要登录 |
| 原始 GitHub 文件（raw.githubusercontent） | `read_url_content` | 直接文本 |

### 步骤 2 — 分层抓取

```
第 1 层 — 略读
  → 使用 read_url_content 抓取 URL
  → 仅读取标题（H1、H2、H3）和第一段
  → 该页面包含用户所需内容吗？不能 → 尝试其他 URL 或搜索。能 → 继续。

第 2 层 — 定向提取
  → 如果页面有锚链接（例如 /docs/page#section），使用锚点抓取
  → 仅提取相关部分（最多 200–500 tokens）
  → 能回答吗？能 → 停止。

第 3 层 — 完整抓取
  → 抓取完整页面，剥离样板内容（导航、页脚、广告、Cookie 横幅、侧边栏）
  → 上限 2000 tokens。在传入回答之前先进行摘要。

第 4 层 — 浏览器子代理（仅最后手段）
  → 仅当 read_url_content 返回空、混乱或 JS 占位内容时使用
  → 指示子代理："导航至 [URL]，等待内容加载，提取 [特定部分]"
  → 不要对静态页面使用 browser_subagent——它很昂贵
```

### 从抓取页面中剥离的内容

在使用抓取内容之前，始终删除：
- 导航菜单和面包屑
- Cookie 横幅和 GDPR 通知
- "相关文章" / "你可能还喜欢" 区块
- 页脚内容（版权、链接）
- 社交分享按钮
- 广告和赞助内容

提取并保留：
- 主要文章 / 文档正文
- 代码块
- 包含数据的表格
- 编号步骤或流程

---

## 搜索协议

当用户提供主题、问题或查询时使用——而不是具体 URL。

### 步骤 1 — 在搜索前先锐化查询

不要直接搜索用户的原始查询。先对其进行转换：

```
原始："how to deploy fastapi on aws"
锐化后："fastapi AWS deployment tutorial 2024"

原始："python async vs threads"
锐化后："Python asyncio vs threading performance comparison"

原始："best way to structure react project"
锐化后："React project folder structure best practices"
```

**查询锐化规则：**
- 增加具体性：版本号、技术名称、"tutorial" / "guide" / "comparison"
- 如果相关则增加时效性：当前年份
- 去除填充词："how do I"、"what is the"、"can you explain"
- 对于代码问题：明确添加语言 + 框架名称

### 步骤 2 — 搜索与选择

```
1. 使用锐化后的查询运行 search_web
2. 获取结果（标题 + 摘要）
3. 仅扫描标题 + 摘要——先不要抓取
4. 选择最相关的前 1-2 个结果（复杂情况下最多 3 个）
5. 跳过以下来源的结果：论坛（如果存在文档）、聚合博客、付费墙站点
6. 优先选择：官方文档、GitHub 仓库、知名技术博客、学术来源
```

### 步骤 3 — 抓取选定的结果

将 URL 协议（上述）应用于每个选定的 URL。
一次处理一个结果——只有当第一个 URL 未回答问题时才抓取第二个 URL。

### 搜索的 Token 规则

- 每个搜索查询绝不读取超过 3 个 URL
- 如果摘要已包含答案 → 不要抓取完整页面，使用摘要
- 对于事实性问题（日期、名称、简单事实）→ 摘要通常足够
- 对于流程性问题（如何做 X）→ 抓取 1 个相关页面，仅定向部分

---

## 多 URL 协议

当用户提供要比较或汇总的 URL 列表时使用。

```
1. 首先略读所有 URL（每个都进行第 1 层抓取）
2. 按与用户问题的相关性分组
3. 仅深度抓取最相关的 1-3 个 URL
4. 在合并之前，每个都先用 3-5 句话进行摘要
5. 绝不直接转储多个页面的原始内容——始终先按来源摘要
```

---

## 文件协议

当 URL 直接指向文件（PDF、.txt、.md、.csv 等）时使用

- `.md` / `.txt` / `.csv` → `read_url_content` 直接可用，读取完整内容
- `.pdf` → 使用 browser_subagent 或 PDF 提取工具；仅提取文本
- `.json` / `.yaml` → `read_url_content`，解析结构，摘要 schema + 关键值
- 大文件（>500 行）→ 读取前 100 行 + 后 20 行 + 搜索相关部分

---

## 反模式（绝不要这样做）

| 反模式 | 为什么不好 | 替代做法 |
|---|---|---|
| 为简单事实抓取完整页面 | 浪费数千 token | 使用摘要或定向锚点 |
| 对静态站点使用 browser_subagent | 非常昂贵 | 先使用 read_url_content |
| 使用原始用户查询进行搜索 | 结果模糊 | 先锐化查询 |
| 抓取 5 个以上搜索结果 | Token 爆炸 | 最多 3 个，回答后停止 |
| 将原始 HTML 转储到上下文中 | 嘈杂、浪费 | 始终剥离为 Markdown |
| "以防万一"地抓取 | 不必要的 token | 仅抓取回答所需的内容 |
| 重复抓取同一 URL | 冗余 | 在上下文中缓存结果，复用 |
| 抓取整个 GitHub 仓库 | 极其浪费 | 仅 README + 定向文件 |

---

## 决策流程图（快速参考）

```
接收到输入
│
├─ GitHub URL？
│   ├─ 通过 API 抓取 README + 元数据
│   ├─ 已回答？ → 停止
│   ├─ 需要更多？ → 抓取文件树，选择 1-3 个文件
│   └─ 仍需要更多？ → 仅抓取特定文件
│
├─ 具体 URL？
│   ├─ 尝试 read_url_content → 略读标题
│   ├─ 已回答？ → 停止
│   ├─ 需要更多？ → 定向部分抓取
│   ├─ 仍需要更多？ → 完整抓取，剥离
│   └─ JS 渲染 / 损坏？ → browser_subagent（最后手段）
│
├─ 主题/查询？
│   ├─ 锐化查询
│   ├─ search_web → 扫描摘要
│   ├─ 摘要足够？ → 从摘要回答，停止
│   ├─ 需要更多？ → 抓取前 1 个结果（定向）
│   └─ 仍需要更多？ → 抓取第 2 个结果（定向）
│
└─ URL 列表？
    ├─ 略读全部（每个第 1 层）
    ├─ 深度抓取最相关的 1-3 个
    └─ 按来源摘要，然后合并
```

---

## 输出格式规则

抓取后，按以下结构组织你的响应：

```
来源：[URL 或 "网络搜索：query"]
摘要：[2-5 句话的发现内容]
回答：[对用户问题的直接回答]
置信度：[高 / 中 / 低 — 基于来源质量]
```

对于多个来源：
```
来源 1：...
来源 2：...
综合回答：...
```

绝不输出：
- 原始 HTML 片段
- 完整页面转储
- 未注明来源的信息
- 超出回答问题所需的内容

---

## Token 预算指南

| 操作 | 大致 token 成本 | 使用时机 |
|---|---|---|
| GitHub README 抓取 | ~300–800 tokens | 始终首先用于仓库 |
| GitHub API 元数据 | ~200 tokens | 始终用于仓库 |
| 略读（仅标题） | ~100–200 tokens | 始终首先用于 URL |
| 定向部分抓取 | ~300–600 tokens | 当略读不够时 |
| 完整页面抓取（剥离后） | ~1000–2000 tokens | 仅当定向失败时 |
| browser_subagent | ~2000–5000 tokens | 仅最后手段 |
| 搜索摘要扫描 | ~300–500 tokens | 始终在抓取前 |

**经验法则：** 如果你打算在一次抓取上花费 >2000 tokens，先问问自己是否有更便宜的路径。

---

## 限制

- **JavaScript 依赖**：标准抓取可能无法完全渲染单页应用（SPA）。对于这些情况，必须回退到 `browser_subagent`，这会更慢且更昂贵。
- **付费墙与保护**：本技能无法绕过 CAPTCHA、机器人保护（例如严格的 Cloudflare 规则）或硬性付费墙。
- **GitHub API 限制**：未经认证的频繁 GitHub API 请求可能会触发速率限制。