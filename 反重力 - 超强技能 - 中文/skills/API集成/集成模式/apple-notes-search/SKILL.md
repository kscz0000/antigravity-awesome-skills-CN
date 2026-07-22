---
name: apple-notes-search
description: "通过 apple-notes MCP 服务器，在用户自己的 Apple Notes 中执行语义+关键词搜索与关联发现。用户想从笔记中查找、回忆或综合信息，或挖掘隐性的桥梁/相关笔记时使用。macOS，本地运行。触发词：apple notes、笔记搜索、Apple Notes、mcp、语义搜索、关联发现、笔记查找、回忆笔记、笔记综合。"
risk: critical
source: community
source_repo: connerkward/mcp-apple-notes
source_type: community
date_added: "2026-06-16"
author: connerkward
tags: [apple-notes, search, mcp, macos, semantic-search, knowledge]
tools: [claude-code]
license: "MIT"
license_source: "https://github.com/connerkward/mcp-apple-notes/blob/main/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
  setup:
    type: manual
    summary: "需要第三方 MCP 配置与 macOS 完全磁盘访问权限；请勿纳入插件安全包。"
    docs: SKILL.md
---

# Apple Notes 搜索与关联发现

`apple-notes` 是一款 MCP 服务器，用于在用户自己的 Apple Notes 上执行语义搜索与关联发现——覆盖混合检索、Swanson-ABC 桥接、实体线程，以及对全部已写内容的引用式综合。Embedding、检索、BM25、聚类与桥接计算全部**在本地完成**；只有**综合生成**环节调用大模型（本地或云端均可，由用户自行选择）。

本技能涵盖：(1) 你必须引导用户完成的一次性配置；(2) 在服务器暴露的众多工具中，如何按场景选用。

## 何时使用本技能

- 用户希望从自己的 Apple Notes 中**查找、回忆或检索**某条信息（例如"在我的笔记里搜 X"、"我写过什么关于 X 的"、"我有没有记过 Y"）。
- 用户希望在笔记之间**发掘隐性关联**（例如"在我的笔记里找桥接/关联"、"X 和 Y 之间有什么联系"、"显示相关笔记"）。
- 用户希望基于笔记**综合出自己的观点**（例如"从我的笔记总结我对 X 的看法"、"汇总我在 X 主题下写过的所有内容"）。
- 也可用于"索引我的 Apple Notes"、按标签/文件夹查询，以及"什么东西与 X 相关"。
- **不要**用于创建提醒事项，也不适用于 Apple Notes 之外的其他笔记系统。

## 首先：MCP 是否已连接？

如果 `apple-notes` 工具不可用，说明服务器尚未注册——请先按下面的**配置**步骤操作。如果工具已就绪但搜索返回"未索引"或空结果，先运行 `index-notes`（参见排序注意事项）。

## 配置（引导用户完成——这是本技能的核心价值）

服务器直接读取 Apple Notes 的 SQLite 存储，因此 **bun** 可执行文件需要"完全磁盘访问"权限。按顺序执行：

1. **安装 bun**（若未安装）：`brew install oven-sh/bun/bun`
2. **克隆并安装依赖：**
   ```bash
   git clone https://github.com/connerkward/mcp-apple-notes
   cd mcp-apple-notes
   git checkout <reviewed-tag-or-commit>
   bun install
   ```
3. **为 bun 授予完全磁盘访问权限。** 先执行 `which bun`，再打开"系统设置" → "隐私与安全性" → "完全磁盘访问"，点击 `+`，将该 `bun` 二进制文件的绝对路径加入（通常位于 `/opt/homebrew/bin/bun` 或 `/usr/local/bin/bun`）。若未授予此权限，服务器无法读取 NoteStore.sqlite，所有调用都会因权限错误而失败。（`bun install` 的 postinstall 步骤会自动尝试打开该面板。）
4. **注册 MCP 服务器**（按用户使用的客户端选择）：
   - Claude Code：`claude mcp add apple-notes -- bun /absolute/path/to/mcp-apple-notes/index.ts --stdio`
   - Claude Desktop：在 `claude_desktop_config.json` 中添加：
     ```json
     { "mcpServers": { "apple-notes": {
         "command": "/Users/<you>/.bun/bin/bun",
         "args": ["/Users/<you>/mcp-apple-notes/index.ts", "--stdio"] } } }
     ```
   - 作为 Claude Code 插件（同时打包本技能）：`/plugin marketplace add connerkward/ckw-skills`，再执行 `/plugin install apple-notes@connerkward`。
5. **重启客户端**，告知用户输入**"Index my Apple Notes"**（或调用 `index-notes`）。首次索引约 1,800 条笔记只需几秒。

## 工具地图——按场景选工具

| 工具 | 适用场景 |
|------|----------|
| `index-notes` | 首次运行或强制重建。后台任务，带实时进度。 |
| `search-notes` | **默认检索。** 语义 + BM25 混合检索，结果经重排序。支持可选参数 `folder`、`modifiedAfter`、`modifiedBefore`。"我写过什么关于 X 的。" |
| `find-notes` | 精确子串匹配（类似 Apple Notes 自带搜索框）。用户要查字面字符串而非语义时使用。支持可选参数 `folder`、日期范围。 |
| `get-note` | 按标题（模糊兜底）获取单条笔记的完整内容。 |
| `list-notes` | 按时间倒序列出笔记。支持可选参数 `folder`、日期范围、`limit`。 |
| `list-folders` | 列出全部文件夹及笔记数量。 |
| `list-tags` / `search-by-tag` | 列出 `#hashtag` 清单 / 按指定标签筛选笔记。 |
| `related-notes` | 基于共享标签、`[[wikilinks]]` 与向量相似度，找出与目标笔记相关的笔记。"显示相关笔记。" |
| `bridge-notes` | **Swanson-ABC 桥接**——发现隐性关联：找到一对 (A, C)，它们彼此并不直接相似，但都强关联到同一个中间项 B。"在我的笔记里找隐性关联。"支持可选参数 `folder`、`limit`。不调用大模型。 |
| `feed` | 以 JSON 形式提供基于证据排名的关联流（桥接 + 抽象配对 + 实体线程）。支持可选参数 `limit`。 |
| `entity-notes` / `list-entities` | "我还在哪里提到过 Mercedes？"实体标签 → 按提及权重列出笔记。**需要可选的实体图数据库**（`~/.mcp-apple-notes/layered_graph.db`）；若不存在，工具会提示如何生成。 |
| `get-tables` | 从笔记中抽取竖线/制表符分隔的表格。 |
| `create-note` / `update-note` | 创建或编辑笔记。 |
| `check-changes` | 自上次索引后笔记是否有变更？（不触发重建索引） |
| `index-health` | 同步状态、最近索引时间、笔记数量。检索结果疑似陈旧时运行。 |

若要"综合我对 X 的看法"，综合能力由 **Web 应用**端点提供（运行 `bun index.ts` 后访问 `http://localhost:3741/` 的 `GET /api/synthesize?q=`），返回带有 `[n]` 行内引用、回链到源笔记的扎实答案。

## 排序注意事项（结果异常时请向用户说明）

- **首次检索前先建索引。** 没有索引会得到空结果或乱码；请先运行 `index-notes`。
- **自动重建索引：** 每次检索会执行约 1 毫秒的变更检测，并在笔记发生变更时触发**一个**后台增量索引——检索从当前索引立即返回，并在任务完成时补齐。若一条刚编辑的笔记未出现，属后台补齐延迟，再跑一次检索即可。
- **评分公式：** `score = RRF(vector, BM25) × title_boost × recency_factor`。
- **时间型查询**（`recent`、`latest`、`today`）会自动切换到 1 天半衰期、70% 权重的近因权重；普通查询以相关性为主（90 天半衰期，占 10%）。
- **综合生成是唯一可调用云端的环节。** 它需要一个大模型：可通过 LM Studio / Ollama 本地运行（`SYNTH_BASE_URL=http://localhost:1234/v1 SYNTH_MODEL=<model> OPENAI_API_KEY=local`，笔记保留在本地），或使用真实的 OpenAI 服务（需有额度的 `OPENAI_API_KEY`，默认 `gpt-4o-mini`）。其余所有环节——Embedding、检索、BM25、聚类、桥接、实体——全部在本地完成。

## 局限性

- 仅支持 macOS 与 Apple Notes；无法搜索 Obsidian、Notion、Google Docs 等其他笔记库。
- MCP 服务器需要本地文件系统权限以读取 Apple Notes 数据，因此配置无法仅通过远程 shell 完成。
- 检索质量依赖最新本地索引。最近编辑过的笔记可能需要 `check-changes`、`index-health`，或在后台索引补齐后重新检索。
- 实体工具依赖可选的图数据库；缺失时，请改用混合检索、精确检索、相关笔记或桥接。

## 致谢

Fork 自 [RafalWilinski/mcp-apple-notes](https://github.com/RafalWilinski/mcp-apple-notes)；
本 Fork 直接读取 SQLite + protobuf，并新增了桥接、实体、Feed 与综合生成能力。
作者：[Conner K Ward](https://github.com/connerkward)。License：MIT。