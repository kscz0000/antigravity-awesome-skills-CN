# last30days 技能规格

## 概述

`last30days` 是一个 Claude Code 技能，使用 OpenAI Responses API 和 xAI Responses API 分别研究 Reddit 和 X (Twitter) 上的给定主题。它强制执行严格的 30 天时效窗口、流行度感知排名，并产生可操作的输出，包括最佳实践、提示词包和可重用的上下文片段。

技能根据可用的 API 密钥以三种模式运行：**仅 reddit**（OpenAI 密钥）、**仅 x**（xAI 密钥）或**两者**（完整交叉验证）。它使用自动模型选择以保持与两个提供商的最新模型同步，并可选固定以提高稳定性。

## 架构

编排器（`last30days.py`）协调发现、丰富、标准化、评分、去重和渲染。每个关注点都隔离在 `scripts/lib/` 中：

- **env.py**：从 `~/.config/last30days/.env` 加载和验证 API 密钥
- **dates.py**：日期范围计算和置信度评分
- **cache.py**：以主题 + 日期范围为键的 24 小时 TTL 缓存
- **http.py**：仅使用标准库的 HTTP 客户端，带重试逻辑
- **models.py**：OpenAI/xAI 模型的自动选择
- **openai_reddit.py**：OpenAI Responses API + web_search 用于 Reddit
- **xai_x.py**：xAI Responses API + x_search 用于 X
- **reddit_enrich.py**：获取 Reddit 帖子 JSON 以获取真实互动指标
- **normalize.py**：将原始 API 响应转换为规范模式
- **score.py**：计算流行度感知分数（相关性 + 时效性 + 互动）
- **dedupe.py**：通过文本相似度进行近重复检测
- **render.py**：生成 markdown 和 JSON 输出
- **schema.py**：类型定义和验证

## 嵌入其他技能

其他技能可以通过多种方式导入研究上下文：

### 内联上下文注入
```markdown
## 最近研究上下文
!python3 ~/.claude/skills/last30days/scripts/last30days.py "your topic" --emit=context
```

### 从文件读取
```markdown
## 研究上下文
!cat ~/.local/share/last30days/out/last30days.context.md
```

### 获取路径以动态加载
```bash
CONTEXT_PATH=$(python3 ~/.claude/skills/last30days/scripts/last30days.py "topic" --emit=path)
cat "$CONTEXT_PATH"
```

### JSON 用于程序化使用
```bash
python3 ~/.claude/skills/last30days/scripts/last30days.py "topic" --emit=json > research.json
```

## CLI 参考

```
python3 ~/.claude/skills/last30days/scripts/last30days.py <topic> [options]

选项：
  --refresh           绕过缓存并获取新数据
  --mock              使用固定数据而非真实 API 调用
  --emit=MODE         输出模式：compact|json|md|context|path（默认：compact）
  --sources=MODE      来源选择：auto|reddit|x|both（默认：auto）
```

## 输出文件

所有输出都写入 `~/.local/share/last30days/out/`：

- `report.md` - 人类可读的完整报告
- `report.json` - 带分数的标准化数据
- `last30days.context.md` - 用于其他技能的紧凑可重用片段
- `raw_openai.json` - 原始 OpenAI API 响应
- `raw_xai.json` - 原始 xAI API 响应
- `raw_reddit_threads_enriched.json` - 丰富的 Reddit 帖子数据
