---
name: ingest-youtube
description: "将 YouTube 视频字幕拉取到可查询的 Markdown 知识库，支持 yt-dlp 字幕发现、VTT 清洗、元数据 frontmatter 和捕获种子存根。触发词：YouTube字幕提取、视频转录、拉取字幕、ingest-youtube、YouTube导入"
risk: safe
source: community
source_repo: adelaidasofia/ai-brain-starter
source_type: community
date_added: "2026-05-09"
license: MIT
license_source: "https://github.com/adelaidasofia/ai-brain-starter/blob/main/LICENSE"
upstream: "https://github.com/adelaidasofia/ai-brain-starter/tree/main/skills/ingest-youtube"
plugin:
  setup:
    type: manual
    summary: "运行 ingest.py 前需本地安装 yt-dlp；脚本仅接受 http(s) YouTube 视频 URL，并将 Markdown 写入选定知识库。"
    docs: "SKILL.md"
---

# ingest-youtube — YouTube 到知识库的连接器

将 YouTube 字幕拉取到 Markdown 知识库，作为可查询的类型化记忆条目，供下游技能（知识图谱提取、声纹训练、内容再利用、行动项提取）使用。

与 ingest-slack、ingest-whatsapp、ingest-notion、ingest-linear、ingest-github、ingest-gmail 采用相同模式。添加 YouTube 意味着新增一个规范化器，而非新架构。

## 何时使用

- 用户粘贴 YouTube URL 并要求获取字幕或摘要
- 用户输入 `/ingest-youtube <url>` 处理单个视频
- 用户要求捕获、同步、导入、转录或将演讲/播客/主题演讲拉取到知识库

不要用于：
- 下载实际视频文件（请直接使用 `yt-dlp` 并加 `-f best`）
- 频道级批量导入或 `--days` 时间窗口；本脚本每次仅处理一个视频 URL
- 直播流（字幕不稳定）
- 非 YouTube 来源（Vimeo、Twitch、Twitter Spaces 有各自的连接器）
- 用户不需要知识库文件的一次性字幕读取（请直接运行 `yt-dlp --write-auto-sub` 并输出到 stdout）

## 工作原理

1. 将输入解析为一个 YouTube 视频 URL。
2. 验证 `yt-dlp` 已安装。若未安装，脚本退出并给出安装指引：`brew install yt-dlp`（macOS）或 `pip3 install --user yt-dlp`。
3. 将 URL 验证为单个 http(s) YouTube 视频，调用 `yt-dlp --ignore-config --list-subs -- <url>` 枚举可用字幕。
4. 字幕优先级：手动字幕 > 自动生成字幕。手动字幕保留创作者提供的标点和说话人标签；自动生成的字幕为大写且无标点。
5. 通过 `yt-dlp --write-sub --sub-lang <lang> --skip-download` 下载最高优先级字幕为 VTT 格式。默认语言偏好：`en,es`（英语优先，西班牙语次之）。
6. 剥离 VTT 时间标记，合并为干净的散文段落。对重复行去重（自动生成的 VTT 会有行重复）。若源内容含说话人标签则保留。
7. 通过 `yt-dlp --print-json --skip-download` 拉取视频元数据（标题、频道、上传日期、时长、video_id、URL）。
8. 对频道名和视频标题做 slugify 处理。写入 `External Inputs/YouTube/<channel-slug>/<YYYY-MM-DD>-<video-slug>.md`。
9. 扫描字幕中的触发关键词（decision、framework、model、principle、"the lesson is"、playbook、anti-pattern、case study）。每个匹配项在 `Meta/Captures/<YYYY-MM-DD>-youtube-<channel-slug>-<video-id>.md` 创建写作种子存根，使种子进入捕获聚合器。
10. 打印摘要：文件路径、字幕字数、语言、检测到的种子数。

## 调用方式

```bash
python3 ingest.py <youtube-url> [--vault <path>] [--lang <code>]
```

默认值：
- `--vault`：`$VAULT_ROOT` 环境变量或当前目录
- `--lang`：`en,es`（英语优先，西班牙语次之；匹配常见的双语默认设置）
- `--whisper`：作为未来的回退标志被接受，但本版本在无字幕可用时写入存根

## 输出契约

知识库文件位于 `External Inputs/YouTube/<channel-slug>/<YYYY-MM-DD>-<video-slug>.md`，包含以下 frontmatter：

```yaml
---
type: external-input
source: youtube
video_id: <11-char ID>
url: https://www.youtube.com/watch?v=<id>
channel: <channel-name>
channel_url: https://www.youtube.com/<handle>
title: <video title>
upload_date: <YYYY-MM-DD>
duration_seconds: <int>
language: <ISO code>
subtitle_source: manual | auto | whisper
word_count: <int>
ingested_at: <ISO 8601 timestamp>
---
```

正文为清洗后的字幕，以段落散文形式呈现。若源内容含说话人标签，每轮格式为 `**<speaker>:** <text>`。

## 幂等性

重复导入同一视频 URL 会覆盖同一知识库文件。种子存根文件名对 video_id 做哈希，因此同一源视频在不同运行中产生相同的存根文件名。重新运行是刷新，不是重复。

## 字幕缺失

若 `yt-dlp --list-subs` 未返回手动或自动字幕，脚本会写入一个包含视频元数据和源 URL 的存根知识库笔记，而非静默失败。`--whisper` 标志保留用于未来的本地转录回退，当前报告该回退未实现。

如需手动回退，可用 `yt-dlp` 下载音频，用本地 Whisper 工作流转录，再添加字幕或文本后重新运行导入。

## 限制

- 每次运行仅导入一个 YouTube 视频 URL；频道句柄、播放列表和 `--days` 时间窗口不在范围内。
- 依赖 `yt-dlp` 返回的字幕；无字幕的视频仅生成元数据存根，而非转录文本。
- 本版本不下载视频文件，也不执行内置 Whisper 转录。
- 网络可用性、YouTube 字幕访问权限和本地 `yt-dlp` 行为决定导入是否成功。

## 验收测试

使用有史以来第一个上传的 YouTube 视频进行测试：

```bash
python3 ingest.py "https://www.youtube.com/watch?v=jNQXAC9IVRw" --vault /tmp/test
```

预期输出：
```
Wrote 39 words to /tmp/test/External Inputs/YouTube/jawed/2005-04-24-me-at-the-zoo.md. Language: en. Subtitle source: manual.
```

输出文件包含有效的 frontmatter 和干净的散文正文。

## 依赖

- `yt-dlp`（必需）：通过 `brew install yt-dlp` 或 `pip3 install --user yt-dlp` 安装
- `whisper-cpp`（可选，用于本脚本之外的手动回退）

## 来源

捆绑于 [adelaidasofia/ai-brain-starter](https://github.com/adelaidasofia/ai-brain-starter)，一个围绕 AI 智能体的验证框架，使记忆不断积累而非损坏。本技能是 ingest-* 系列知识库连接器的一部分。
