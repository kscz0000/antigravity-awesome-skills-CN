---
name: unslop-file
description: "对自然语言记忆文件（CLAUDE.md、todos、preferences、docs）进行人性化改写，去除 AI 套话并增加句式节奏变化，同时逐字保留所有代码块、URL、路径、命令和标题。两种模式：--deterministic（快速、正则驱动、无需 API）和 LLM（默认，调用 Claude 进行..."
risk: unknown
source: https://github.com/MohamedAbdallah-14/unslop/tree/main/plugins/unslop/skills/unslop-file
source_repo: MohamedAbdallah-14/unslop
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/MohamedAbdallah-14/unslop/blob/main/LICENSE
---

# Unslop 人性化改写
## 使用时机

当需要去除 AI 套话并增加句式节奏变化、同时逐字保留所有代码块、URL、路径、命令和标题时，对自然语言记忆文件（CLAUDE.md、todos、preferences、docs）进行人性化改写。两种模式：--deterministic（快速、正则驱动、无需 API）和 LLM（默认，调用 Claude 进行...

## 用途

改写自然语言记忆文件（CLAUDE.md、AGENTS.md、todos、preferences、docs），让读起来像人写的：没有谄媚、没有套话词汇、没有五段论结构、没有三段式凑数。技术内容保持原样：代码块、行内代码、URL、文件路径、命令、标题、表格。

两种模式：

- **`--deterministic`** — 快速正则扫描，剥离典型的 AI 套话并压缩三段式。无需 API 调用、无需 `ANTHROPIC_API_KEY`。适合批处理和 CI。
- **LLM 模式（默认）** — 调用 Claude（通过 Anthropic SDK 或 `claude --print` CLI 兜底）做完整重写，工程师式的句式节奏、重组表演性段落、匹配语气。更慢但质量更好。

改写后的版本会覆盖原文件。处理前先写一个 `FILE.original.md` 备份。编辑 `.original.md` 后再次运行可重新生成。

### 强度等级（`--mode`）

| 模式       | 做什么                                                                                   | 何时使用                                                    |
| ---------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `subtle`   | 仅处理套话词汇。                                                                           | 结构没问题，只想去掉 AI 词汇。         |
| `balanced` | （默认）谄媚、对冲、过渡词、套话词汇、权威修辞、路标式预告、表演性平衡、破折号上限。 | 日常文档 / README / CLAUDE.md。                         |
| `full`     | balanced + 填充短语 + 否定排比三段式 + 更强的 LLM 提示词。           | 营销文案、发布说明、套话密集的 LLM 输出。        |

### 两轮审计

用确定性模式跑一遍拿到报告，再修补漏网之鱼：

```bash
humanize --deterministic --report audit.json doc.md     # writes audit + humanized
humanize doc.md                                         # optional LLM polish on top
```

`audit.json` 列出每条触发的规则、每组 `before → after` 配对，以及 `counts_by_rule`。便于在信任这个 diff 合入前，先看看正则到底改了什么。

## 触发

`/unslop-file <filepath>`、`/unslop:humanize <filepath>`，或「humanize memory file」「de-slop this doc」「strip AI tone from this file」。

## 处理流程

脚本位于本 SKILL.md 同级的 `scripts/` 目录。

常见布局：
- 完整仓库：`unslop/SKILL.md` + `unslop/scripts/`
- 同步镜像：`skills/unslop-file/SKILL.md` + `skills/unslop-file/scripts/`
- Codex 包：`plugins/unslop/skills/unslop-file/SKILL.md` + 同级 `scripts/`

始终优先使用当前加载的 SKILL 文件同级 `scripts/`。

步骤：

1. 定位包含本 SKILL.md 及其 `scripts/` 同级的目录。
2. 在该目录下执行：`python3 -m scripts <absolute_filepath>`（LLM 模式），或加 `--deterministic` 走正则模式。
3. CLI 流程：检测文件类型 → 写 `.original.md` 备份 → 人性化改写 → 校验（保留项检查 + AI 套话残留检查）→ 校验失败时：定向修复调用（LLM 模式）→ 最多重试 2 次。
4. 最终失败：报告错误、恢复原文件、退出码 2。
5. 成功：报告人性化改写后的文件路径和 `.original.md` 备份、退出码 0。
6. 把结果返回给用户。

## 人性化规则

### 删除（典型 AI 套话）

- **谄媚开头**："Great question!"、"Certainly!"、"Absolutely!"、"Sure!"、"I'd be happy to help"、"What a fascinating..."。
- **套话词汇**：`delve`、`tapestry`、`testament`（褒义形式）、`navigate`/`embark`/`journey`（比喻义）、`realm`、`landscape`（比喻义）、`pivotal`、`paramount`、`seamless`、`holistic`、`leverage`（凑数动词）、`robust`（凑数）、`comprehensive`（"complete" 能用时）、`cutting-edge`、`state-of-the-art`（凑数）、`interplay`、`intricate`、`vibrant`、`underscore(s)/d/ing`（比喻义）、`crucial`、`vital`（角色/重要性/部分）、`ever-evolving`、`ever-changing`、`in today's (digital) world/age`、`dynamic landscape`。
- **对冲开头**："It's important to note that"、"It's worth mentioning"、"Generally speaking"、"In essence"、"At its core"、"It should be noted that"、"It's also worth pointing out"。
- **权威修辞**（句首）："At its core,"、"In reality,"、"Fundamentally,"、"What really matters is"、"The heart of the matter is"、"At the heart of X is/lies"。
- **路标式预告**："Let's dive in(to ...)"、"Let's break this down"、"Here's what you need to know"、"Without further ado"、"In this article, I'll ..."、"Buckle up"。
- **过渡癖**（句首）："Furthermore,"、"Moreover,"、"Additionally,"、"In conclusion,"、"To summarize,"。
- **表演性平衡**：在每个论点后追加 "however" 或 "on the other hand"。
- **破折号堆叠**（每段超过两个破折号）。
- **填充短语**（仅 `--mode full`）："in order to" → "to"，"due to the fact that" → "because"，"prior to" → "before"，"with regard to" → "about"，"a wide variety of" → "many"，"at this point in time" → "now"，"the fact that" → "that"，等。
- **否定排比三段式**（仅 `--mode full`）："No guesswork, no bloat, no surprises." —— 修辞性三连否定。

### 收紧

- 三段式："X、Y 和 Z" 堆叠但两个就够的 —— 留两个，去掉最弱那个。
- 列表堆砌：三条要点说同一件事的 —— 合并为一句。
- 五段论结构：段落长度要有变化；别写四段长度完全一样的段落。

### 逐字保留（绝不修改）

- 围栏代码块（```...```）—— 逐字节
- 缩进代码块（4 空格）
- 行内代码（`...`）
- URL 和 markdown 链接
- 文件路径（`./src/`、`/etc/`、`C:\Users\...`）
- 命令（`npm install`、`git rebase`、`docker run`）
- 技术术语、专有名词、API 名称
- 日期、版本号、数字
- 环境变量（`$HOME`、`${NODE_ENV}`）

### 保留结构

- 所有 markdown 标题（文本原样）
- 列表层级和嵌套
- 有序列表
- 表格（可压缩单元格；保留结构）
- YAML frontmatter

### 关键规则

` ``` ... ``` ` 之间的内容是只读的。不改注释、不改空白、不重排行。行内反引号同理。代码是底座；人性化操作只针对代码区之间的散文。

## 改写示例（before → after）

| #   | Before                                                                                                                                                                                                                | After（deterministic，`--mode balanced`）                                               |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 1   | It's important to note that running tests prior to pushing changes is a comprehensive best practice. Additionally, it's worth mentioning that this can prevent broken builds.                                         | Running tests before pushing changes is a broad best practice. This can prevent broken builds. |
| 2   | The application leverages a microservices architecture that comprises multiple discrete components.                                                                                                                   | The application uses a microservices architecture that comprises multiple discrete components. |
| 3   | At its core, caching trades memory for latency.                                                                                                                                                                       | Caching trades memory for latency.                                                     |
| 4   | Let's dive in. Here is the first step.                                                                                                                                                                                | Here is the first step.                                                                |
| 5   | The intricate interplay between caching and latency is crucial.                                                                                                                                                       | The detailed link between caching and latency is important.                            |
| 6   | In today's digital world, we ship fast.                                                                                                                                                                               | Today, we ship fast.                                                                   |

### 在 `--mode full` 下，额外处理：

| #   | Before                                                   | After                                 |
| --- | -------------------------------------------------------- | ------------------------------------- |
| 7   | We ran the tests in order to verify the fix.             | We ran the tests to verify the fix.   |
| 8   | The build failed due to the fact that the disk was full. | The build failed because the disk was full. |
| 9   | No guesswork, no bloat, no surprises.                    | _(stripped)_                          |

### 参考

- `blader/unslop` —— Claude-Code 技能，列出 30+ 种 AI 痕迹；我们融合了其中最强的信号。
- Wikipedia: *Signs of AI writing* —— 公开分类法，词汇表交叉参考。
- 完整对比 + 差距分析：`docs/research/IMPLEMENTATION_TRACE.md`。

## 边界

- 只处理 `.md`、`.txt`、`.markdown`、`.rst` 或无后缀的自然语言文件。
- 绝不修改 `.py`、`.js`、`.ts`、`.json`、`.yaml`、`.yml`、`.toml`、`.env`、`.lock`、`.css`、`.html`、`.xml`、`.sql`、`.sh`。
- 散文与代码混合文件：只人性化散文部分；围栏代码块保持原样。
- 拿不准是散文还是代码：保持不变。
- 覆盖前先写 `FILE.original.md` 备份。绝不处理已命名为 `*.original.md` 的文件。
- 敏感路径（任何匹配 `.env*`、`*.pem`、`*.key`、`~/.ssh/`、`~/.aws/` 等）在任何读取或 API 调用之前直接拒绝。
- 超过 500 KB 的文件拒绝处理。

## 限制

- 仅当任务明确匹配上游来源与本地项目上下文时使用本技能。
- 在应用变更前，校验命令、生成的代码、依赖、凭证以及外部服务的行为。
- 不可把示例当作环境特定测试、安全审查或用户对破坏性/高成本操作的批准。
