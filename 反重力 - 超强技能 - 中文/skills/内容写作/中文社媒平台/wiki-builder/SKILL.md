---
name: wiki-builder
description: "创建并维护可复用的研究型维基，支持来源溯源、可配置结构、本地 Markdown 输出。涉及维基、知识库、研究笔记、来源整理、概念页、索引页、wiki.config 时使用。"
category: "knowledge-management"
risk: "safe"
source: "official"
source_repo: "dair-ai/dair-academy-plugins"
source_type: "official"
date_added: "2026-06-19"
author: "DAIR.AI"
license: "MIT"
license_source: "https://github.com/dair-ai/dair-academy-plugins/blob/main/README.md#license"
tags:
  - dair-academy
  - ai
  - workflow
tools:
  - claude-code
  - codex-cli
  - cursor
---

# 维基构建器

_来源：[dair-ai/dair-academy-plugins](https://github.com/dair-ai/dair-academy-plugins)（MIT 许可证）。_

## 用途

创建并维护可配置的研究型维基。每个维基是一个独立目录，包含自己的来源、编译后的页面、衍生产物、提示词与本地配置。

默认情况下，维基位于 `~/dair-wikis/`。可通过环境变量 `WIKI_ROOT` 或 `init_wiki.sh` 的 `--root` 参数覆盖该路径。

本技能刻意保持通用。不要把所有维基硬塞进 AI 论文的结构。每个维基的 `wiki.config.md` 都是用途、受众、页面类型、风格规范与更新流程的唯一真相源。

## 适用场景

涉及以下需求时使用本技能：

- 启动一个新维基或知识库。
- 为研究笔记、论文、产品、人物、组织、领域、项目、活动建立维基。
- 把源材料导入已存在的维基。
- 生成维基页、来源页、概念页、关系图、时间线、摘要或索引。
- 向维基提问并把答案归档回维基。
- 重构或演进一个维基的结构、需求或风格。
- 维护维基的来源、来源说明与更新日志。

## 默认维基位置

除非用户明确给出其他路径，否则将维基存放在此处：

```bash
${WIKI_ROOT:-$HOME/dair-wikis}/<wiki-slug>
```

使用小写 kebab-case 形式的 slug，例如 `agent-memory`、`ai-evals`、`open-source-models`、`company-research`。

## 核心结构

新维基应从以下结构起步：

```text
<wiki-slug>/
├── wiki.config.md
├── raw/
├── wiki/
│   └── index.md
├── derived/
├── prompts/
│   ├── compile-index.md
│   ├── compile-source-page.md
│   ├── compile-concept-page.md
│   ├── query-and-file.md
│   └── lint-wiki.md
├── logs/
│   └── maintenance-log.md
└── sources.md
```

仅在维基的 `wiki.config.md` 确实需要时才新增目录。常见的扩展包括 `wiki/papers`、`wiki/concepts`、`wiki/people`、`wiki/products`、`wiki/organizations`、`wiki/timelines`、`wiki/questions`、`wiki/maps`、`assets`。

## 启动一个新维基

对新维基，使用随技能附带的脚本（通过插件安装位置解析其路径，通常为 `${CLAUDE_PLUGIN_ROOT}/skills/wiki-builder/scripts/init_wiki.sh`）：

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/wiki-builder/scripts/init_wiki.sh" <slug> --title "Readable Title" --flavor research
```

传入 `--root /custom/path` 可把维基放到 `~/dair-wikis/` 之外的位置。

默认支持的风格包括 `research`、`paper`、`domain`、`product`、`person`、`organization`、`project`。拿不准时使用 `research`。

脚手架搭建完成后：

1. 编辑 `wiki.config.md`，使其匹配用户的真实目标。
2. 把复制或下载的源材料放进 `raw/`。
3. 在 `sources.md` 中登记来源溯源。
4. 在 `wiki/` 下生成页面。
5. 在 `logs/maintenance-log.md` 中记录重大维护动作。

## 运维工作流

### 1. 确认任务

先明确用户是要启动、导入、编译、查询、重构、检查还是导出。若请求中指向已存在的维基，先查看其 `wiki.config.md` 再做修改。

### 2. 使用本地配置

每个维基的规则可能不同。在生成或修改页面之前，先阅读：

- `wiki.config.md`
- 当来源溯源重要时阅读 `sources.md`
- 当维基有自定义提示词时，阅读 `prompts/` 下相关文件

本地配置优先于本技能的通用默认值。

### 3. 保留溯源

不要把无来源的笼统说法当作维基事实。当使用网页、论文、转写稿、笔记或仓库文件时，登记足够溯源信息，使未来的智能体能够再次定位原始来源。

至少，`sources.md` 条目应包含标题、来源路径或 URL、添加日期，以及一段简短说明该来源的贡献点。

### 4. 编译页面

优先考虑持久的维基页面，而不是一次性摘要。优质页面通常包含：

- 简明的概览
- 有来源支撑的要点
- 到相关维基页面的链接
- 悬而未决的问题或不确定性
- 在相关时附上更新说明

保持页面结构与维基的 `wiki.config.md` 及风格一致。

### 5. 维护维基

当新增或改动大量页面时，更新 `wiki/index.md`、相关关系图与 `logs/maintenance-log.md`。若用户请求改变了维基的用途或结构，先更新 `wiki.config.md`。

## 风格

在选择或适配维基类型时阅读 `references/wiki-flavors.md`。该参考文档给出了 research、paper、domain、product、person、organization、project 等维基的建议页面类型与结构。

## 质量基线

- 让第一页立即有用。
- 优先使用显式文件名与稳定 slug。
- 把原始材料与编译后的解读分开。
- 互相关联相关维基页面。
- 明确标注推测与未知项。
- 避免在不同地方重复改写同一来源摘要。
- 让生成的页面在未来对智能体与人都易于浏览。

## 局限性

- 当工作流指定了上游工具、账号、API 密钥或本地配置时，需具备这些条件。
- 未经用户明确批准，不得执行破坏性、生产级、付费或对外发送消息的操作。
- 在把生成的产物或建议当作最终结果前，请用用户的真实来源进行校验。
