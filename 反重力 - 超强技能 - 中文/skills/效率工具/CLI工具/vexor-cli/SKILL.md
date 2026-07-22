---
name: vexor-cli
description: 通过 `vexor` 进行语义文件发现。用于在中型或大型仓库中定位某物的实现/加载/定义位置，或文件位置不明确时。优先使用此工具而非手动浏览。触发词：vexor、语义文件搜索、文件发现、代码定位、意图搜索、文件查找、语义发现
risk: unknown
source: community
---

# Vexor CLI 技能

## 何时使用
- 需要按意图而非精确文件名或文本匹配来定位文件。
- 仓库足够大，手动浏览或简单的 grep 太慢或模糊。
- 希望语义发现某物的实现、加载、定义或文档位置。

## 目标

按意图（它们做什么）查找文件，而非精确文本。

## 使用方法

- 首先使用 `vexor` 进行基于意图的文件发现。
- 如果缺少 `vexor`，请遵循 references/install-vexor.md。

## 命令

```bash
vexor "<QUERY>" [--path <ROOT>] [--mode <MODE>] [--ext .py,.md] [--exclude-pattern <PATTERN>] [--top 5] [--format rich|porcelain|porcelain-z]
```

## 常用标志

- `--path/-p`: 根目录（默认：当前目录）
- `--mode/-m`: 索引/搜索策略
- `--ext/-e`: 限制文件扩展名（例如 `.py,.md`）
- `--exclude-pattern`: 按 gitignore 风格模式排除路径（可重复；`.js` → `**/*.js`）
- `--top/-k`: 结果数量
- `--include-hidden`: 包含点文件
- `--no-respect-gitignore`: 包含被忽略的文件
- `--no-recursive`: 仅顶层目录
- `--format`: `rich`（默认）或 `porcelain`/`porcelain-z` 用于脚本
- `--no-cache`: 仅内存，不读/写索引缓存

## 模式（选择最便宜且有效的）

- `auto`: 按文件类型路由（默认）
- `name`: 仅文件名（最快）
- `head`: 仅前几行（快）
- `brief`: 关键词摘要（适合 PRD）
- `code`: 代码感知分块，用于 `.py/.js/.ts`（代码库的最佳默认值）
- `outline`: Markdown 标题/章节（最适合文档）
- `full`: 分块完整文件内容（最慢，召回率最高）

## 故障排除

- 需要被忽略或隐藏的文件：添加 `--include-hidden` 和/或 `--no-respect-gitignore`。
- 可脚本化输出：使用 `--format porcelain`（TSV）或 `--format porcelain-z`（NUL 分隔）。
- 获取详细帮助：`vexor search --help`。
- 配置问题：`vexor doctor` 或 `vexor config --show` 诊断 API、缓存和连接性（告诉用户进行设置）。

## 示例

```bash
# 查找 CLI 入口点 / 命令
vexor search "typer app commands" --top 5
```

```bash
# 按标题/章节搜索文档
vexor search "user authentication flow" --path docs --mode outline --ext .md --format porcelain
```

```bash
# 定位配置加载/验证逻辑
vexor search "config loader" --path . --mode code --ext .py
```

```bash
# 排除测试和 JavaScript 文件
vexor search "config loader" --path . --exclude-pattern tests/** --exclude-pattern .js
```

## 提示

- 首次搜索会索引文件（可能需要一分钟）。后续搜索很快。如需要可使用更长的超时时间。
- 结果返回相似度排名、精确文件位置、行号和匹配片段预览。
- 结合 `--ext` 与 `--exclude-pattern` 聚焦于子集（排除规则在此基础上应用）。

## 局限性
- 仅当任务明显符合上述描述的范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
