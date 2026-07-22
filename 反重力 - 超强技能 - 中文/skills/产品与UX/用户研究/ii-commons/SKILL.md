---
name: ii-commons
description: "跨 arXiv、PubMed/PMC 和美国政策语料库的确定性检索，支持每日新鲜度截止。触发词：ii-commons、arXiv检索、PubMed检索、政策文献检索、研究检索、语料库新鲜度、确定性搜索、科研检索"
category: research
risk: safe
source: community
source_repo: Intelligent-Internet/II-Commons-Skills
source_type: community
date_added: "2026-05-26"
author: Intelligent Internet
tags: [research, arxiv, pubmed, pmc, policy, retrieval, cli, codex]
tools: [claude, cursor, gemini, codex, antigravity]
license: "Apache-2.0"
license_source: "https://github.com/Intelligent-Internet/II-Commons-Skills/blob/main/LICENSE"
---

# II-Commons 确定性科研检索

## 概述

II-Commons 为研究智能体提供跨 arXiv、PubMed/PMC 及支持的美国政策语料库的确定性检索。当任务需要可复现的搜索、元数据查找、全文 Markdown 检索，或在回答最新证据前需要检查新鲜度时使用此技能。

上游项目以 `@intelligentinternet/ii-commons` 发布 Node.js CLI，并在 `skills/ii-commons/` 提供完整的智能体技能。

## 何时使用此技能

- 在 arXiv、PubMed/PMC 或支持的美国政策语料库中检索证据时使用。
- 用户要求最新或近期研究且语料库新鲜度重要时使用。
- 需要稳定标识符、元数据或全文 Markdown 用于下游分析时使用。
- 比较科学文献与政策文件中的证据时使用。

## 工作原理

### 步骤 1：检查语料库新鲜度

在涉及新鲜度的搜索前运行 `cutoff`：

```bash
npx @intelligentinternet/ii-commons cutoff
```

在解读近期结果之前，报告相关的截止日期。

### 步骤 2：搜索正确的语料库

使用以下参数格式。字面量示例可按原样输入，但当查询来自用户提示时，应通过 runner API 以参数数组方式传递，而非插值到 shell 字符串中。双引号无法防止生成的 shell 命令中的命令替换。

```bash
npx @intelligentinternet/ii-commons search arxiv "large language model inference" --max-results 10
npx @intelligentinternet/ii-commons search pubmed "type 2 diabetes review" --start 20240000 --max-results 10
npx @intelligentinternet/ii-commons search policy "state overtime rule for agricultural workers" --jurisdictions US-CA --max-results 10
```

```js
spawnSync("npx", [
  "@intelligentinternet/ii-commons",
  "search",
  "arxiv",
  userQuery,
  "--max-results",
  "10",
]);
```

预印本和技术研究选择 `arxiv`，生物医学和临床文献选择 `pubmed`，支持的美国政策语料库选择 `policy`。

### 步骤 3：检索元数据或 Markdown

使用搜索结果中的稳定标识符：

```bash
npx @intelligentinternet/ii-commons meta "arXiv:2402.03578"
npx @intelligentinternet/ii-commons markdown "PMCID:PMC11152602"
```

先从搜索结果构建摘要，在需要详细检查或全文锚定时再请求 Markdown。

## 安装

使用 `npx` 运行 CLI：

```bash
npx @intelligentinternet/ii-commons --help
```

或全局安装：

```bash
npm install -g @intelligentinternet/ii-commons
ii-commons cutoff
```

要安装完整的上游智能体技能，从以下位置安装 `skills/ii-commons/` 文件夹：

```text
https://github.com/Intelligent-Internet/II-Commons-Skills
```

## 最佳实践

- 优先使用服务端日期过滤器（如 `--start` 和 `--end`）进行有时间范围的 arXiv 和 PubMed 搜索。
- 保留规范标识符，如 `arXiv:<id>`、`PMID:<id>`、`PMCID:PMC<id>` 和 `policy:<jurisdiction>:<id>`。
- 使用 `cutoff` 作为每个语料库的权威新鲜度边界。
- 在初始搜索结果显示出正确范围之前，保持非时间过滤器保守。

## 局限性

- 需要 Node.js 18 或更新版本，以及到 `commons.ii.inc` 的出站网络访问。
- 基本使用无需认证；更高用量限制可能需要从 `https://commons.ii.inc/` 获取 API 令牌。
- 政策覆盖范围仅限于 II-Commons 提供的政策语料库。

## 安全与注意事项

- 不要打印或暴露 `II_COMMONS_API_KEY` 的值。
- 将输出视为检索证据，而非专家评审。对于医疗、法律或政策敏感工作，请引用来源并保留不确定性。
- 命令调用外部 API 服务；在运行前确认用户环境允许网络访问。

## 相关技能

- 当证据不在 arXiv、PubMed/PMC 或支持的政策语料库范围内时，使用更广泛的网页搜索或深度研究技能。
- 在 II-Commons 识别出稳定的来源记录后，使用引文管理技能。
