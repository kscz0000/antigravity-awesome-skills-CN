---
name: mmx-cli
description: "使用 mmx 通过 MiniMax AI 平台生成文本、图像、视频、语音和音乐。当用户想要创建媒体内容、与 MiniMax 模型对话、执行网络搜索或从终端管理 MiniMax API 资源时使用。触发词：mmx、MiniMax CLI、MiniMax 命令行、生成图像、生成视频、语音合成、生成音乐、文本生成、MiniMax API"
risk: safe
source: "https://github.com/MiniMax-AI/cli"
date_added: "2026-04-14"
---

# MiniMax CLI — 智能体技能指南

使用 `mmx` 通过 MiniMax AI 平台生成文本、图像、视频、语音、音乐，并执行网络搜索。

## 何时使用

当用户想要通过 `mmx` 终端 CLI 生成或检查文本、图像、视频、语音、音乐、网络搜索结果或 MiniMax API 资源时使用此技能。

## 前置条件

```bash
# 安装
npm install -g mmx-cli

# 认证（OAuth 持久化到 ~/.mmx/credentials.json，API key 持久化到 ~/.mmx/config.json）
mmx auth login --api-key sk-xxxxx

# 验证当前认证来源
mmx auth status

# 或每次调用时传入
mmx text chat --api-key sk-xxxxx --message "Hello"
```

区域自动检测。可通过 `--region global` 或 `--region cn` 覆盖。

---

## 智能体标志

在非交互式（智能体/CI）环境中始终使用以下标志：

| 标志 | 用途 |
|---|---|
| `--non-interactive` | 缺少参数时快速失败，而非提示输入 |
| `--quiet` | 抑制旋转器/进度条；stdout 为纯数据 |
| `--output json` | 机器可读的 JSON 输出 |
| `--async` | 立即返回任务 ID（视频生成） |
| `--dry-run` | 预览 API 请求而不执行 |
| `--yes` | 跳过确认提示 |

---

## 命令

### text chat

聊天补全。默认模型：`MiniMax-M2.7`。

```bash
mmx text chat --message <text> [flags]
```

```bash
# 单条消息
mmx text chat --message "user:What is MiniMax?" --output json --quiet

# 多轮对话带系统提示
mmx text chat \
  --system "You are a coding assistant." \
  --message "user:Write fizzbuzz in Python" \
  --output json

# 从文件读取
cat conversation.json | mmx text chat --messages-file - --output json
```

---

### image generate

生成图像。模型：`image-01`。

```bash
mmx image generate --prompt <text> [flags]
```

```bash
mmx image generate --prompt "A cat in a spacesuit" --output json --quiet
mmx image generate --prompt "Logo" --n 3 --out-dir ./gen/ --quiet
```

---

### video generate

生成视频。默认模型：`MiniMax-Hailuo-2.3`。异步任务 — 默认轮询直到完成。

```bash
mmx video generate --prompt <text> [flags]
```

```bash
# 非阻塞：获取任务 ID
mmx video generate --prompt "A robot." --async --quiet

# 阻塞：等待并保存文件
mmx video generate --prompt "Ocean waves." --download ocean.mp4 --quiet
```

---

### speech synthesize

文本转语音。默认模型：`speech-2.8-hd`。最大 1 万字符。

```bash
mmx speech synthesize --text <text> [flags]
```

```bash
mmx speech synthesize --text "Hello world" --out hello.mp3 --quiet
echo "Breaking news." | mmx speech synthesize --text-file - --out news.mp3
```

---

### music generate

生成音乐。模型：`music-2.6-free`。

```bash
mmx music generate --prompt <text> [--lyrics <text>] [flags]
```

```bash
# 纯音乐
mmx music generate --prompt "Cinematic orchestral, building tension" --instrumental --out bgm.mp3 --quiet

# 带自动生成歌词
mmx music generate --prompt "Upbeat pop about summer" --lyrics-optimizer --out summer.mp3 --quiet
```

---

### search query

通过 MiniMax 进行网络搜索。

```bash
mmx search query --q "MiniMax AI" --output json --quiet
```

---

### vision describe

通过 VLM 进行图像理解。

```bash
mmx vision describe --image photo.jpg --prompt "What breed?" --output json
```

---

## 管道模式

```bash
# 链式：生成图像 → 描述它
URL=$(mmx image generate --prompt "A sunset" --quiet)
mmx vision describe --image "$URL" --quiet

# 异步视频工作流
TASK=$(mmx video generate --prompt "A robot" --async --quiet | jq -r '.taskId')
mmx video task get --task-id "$TASK" --output json
mmx video download --task-id "$TASK" --out robot.mp4
```

---

## 退出码

| 代码 | 含义 |
|---|---|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 用法错误 |
| 3 | 认证错误 |
| 4 | 配额超限 |
| 5 | 超时 |
| 10 | 内容过滤触发 |

---

## 限制

- 需要配置 MiniMax 账户和有效认证，任何 API 支持的命令才能工作。
- 媒体生成任务可能是异步的、配额限制的或区域受限的；智能体应显式处理延迟完成和提供商侧失败。
- 本技能仅记录 CLI 用法，不替代提供商策略审查、内容安全检查或下游文件验证。
