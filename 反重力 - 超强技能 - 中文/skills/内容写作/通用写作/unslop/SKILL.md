---
name: unslop
description: "通过 unslop CLI 后处理 AI 生成的文本，在发布前剥离 AI 写作模式。触发词：AI写作模式、文本后处理、unslop、AI文本清理、发布前处理、去除AI痕迹、文本质量"
category: writing
risk: safe
source: community
source_repo: MohamedAbdallah-14/unslop
source_type: community
date_added: "2026-04-25"
author: MohamedAbdallah-14
tags: [writing, content-quality, ai-writing, text-processing, cli, publishing]
tools: [claude-code, cursor, gemini-cli, codex-cli, antigravity]
license: "MIT"
license_source: "https://github.com/MohamedAbdallah-14/unslop/blob/main/LICENSE"
---

# unslop — 通过 CLI 剥离 AI 写作模式

## 概述

unslop 是一个 CLI 工具，通过后处理以编程方式移除 AI 写作模式。与要求智能体避免 AI 式表达的技能不同，unslop 作为确定性的流水线步骤运行：管道输入文本，输出干净文本。在提交文档、发布帖子或将任何 AI 生成内容发送到生产环境之前，将其用作最终处理步骤。

`--deterministic` 标志使输出可复现——相同输入始终产生相同输出。`--stdin` 标志从标准输入读取，支持 shell 管道组合。

## 何时使用此技能

- 当你有准备发布的 AI 生成文本，需要最终清理步骤时
- 在 shell 管道中需要自动强制文本质量时
- 编写提交钩子或 CI 步骤，在内容发布前验证时
- 需要跨多次运行的可复现文本标准化时

## 安装

一次性安装：

```bash
pipx install unslop
# 或
uv tool install unslop
```

验证：

```bash
unslop --version
```

## 工作原理

### 步骤 1：通过 unslop 管道传输文本

标准清理（运行间可能略有不同）：

```bash
echo "This leverages cutting-edge AI to deliver robust solutions." | unslop --stdin
```

确定性清理（相同输入 → 每次运行相同输出）：

```bash
echo "This leverages cutting-edge AI to deliver robust solutions." | unslop --stdin --deterministic
```

### 步骤 2：在 Shell 管道中使用

将任何命令的输出通过 unslop 管道传输：

```bash
cat draft.md | unslop --stdin --deterministic > clean.md
```

或与其他工具链接：

```bash
cat draft.md | unslop --stdin --deterministic | pbcopy   # macOS: 将干净文本复制到剪贴板
```

### 步骤 3：集成到提交钩子或 CI

添加到 pre-commit 钩子或 CI 步骤，在任何生成内容发布前强制质量门控：

```bash
# 在 .git/hooks/pre-commit 或 CI 脚本中
CONTENT=$(cat docs/changelog.md)
CLEANED=$(echo "$CONTENT" | unslop --stdin --deterministic)
if [ "$CONTENT" != "$CLEANED" ]; then
  echo "Changelog contains AI writing patterns. Run: cat docs/changelog.md | unslop --stdin --deterministic > docs/changelog.md"
  exit 1
fi
```

## 示例

### 示例 1：清理草稿文档

```bash
cat blog-post-draft.md | unslop --stdin --deterministic > blog-post-final.md
```

### 示例 2：写作时内联清理

```bash
# 写入内容，通过 unslop 管道传输，将结果写回
cat README.md | unslop --stdin > README.clean.md && mv README.clean.md README.md
```

### 示例 3：提交 PR 前验证

```bash
# 检查是否有生成的文档需要清理
for f in docs/*.md; do
  ORIGINAL=$(cat "$f")
  CLEANED=$(echo "$ORIGINAL" | unslop --stdin --deterministic)
  [ "$ORIGINAL" != "$CLEANED" ] && echo "Needs cleanup: $f"
done
```

## 最佳实践

- ✅ 在 CI 和自动化中使用 `--deterministic` 确保可复现输出
- ✅ 在最终稿上运行，而非中间迭代版本
- ✅ 与 `avoid-ai-writing` 技能结合使用，同时获得生成时指导和后处理
- ❌ 不要在代码文件上运行——unslop 针对散文，而非源代码
- ❌ 不要在 unslop 后跳过审查：自动清理偶尔会改变含义；请阅读输出

## 局限性

- 仅处理散文——不处理代码、JSON 或结构化数据
- 不捕获事实错误或实质性写作问题
- 某些替换可能不适用于每个上下文；发布前审查输出
- 需要 Python 工具如 `pipx` 或 `uv` 进行独立 CLI 安装

## 安全与安全说明

- unslop 从标准输入读取并写入标准输出——默认无文件系统副作用
- `--deterministic` 模式是本地的，不进行 LLM API 调用
- 默认 LLM 模式可能使用 `ANTHROPIC_API_KEY` 或 Claude CLI；对敏感本地文件和 CI 门控使用 `--deterministic`
- 固定到确定性模式时，可安全在 CI 管道和提交钩子中运行
