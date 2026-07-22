---
name: instagram
description: 通过 Graph API 完整集成 Instagram。发布、分析、评论、私信、话题标签、定时发布、模板以及 Business/Creator 账号管理。
risk: critical
source: community
date_added: '2026-03-06'
author: renat
tags:
- social-media
- instagram
- graph-api
- content
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# Skill: Instagram 集成

## 概述

通过 Graph API 完整集成 Instagram。发布、分析、评论、私信、话题标签、定时发布、模板以及 Business/Creator 账号管理。

## 何时使用此技能

- 当用户提到"instagram"或相关话题时
- 当用户提到"ig"或相关话题时
- 当用户提到"post instagram"或相关话题时
- 当用户提到"publicar instagram"或相关话题时
- 当用户提到"reels instagram"或相关话题时
- 当用户提到"stories instagram"或相关话题时

## 何时不使用此技能

- 任务与 instagram 无关时
- 有更简单、更具体的工具可以处理请求时
- 用户需要的是无领域专业知识的通用帮助时

## 工作原理

通过 Graph API 完全控制 Instagram 账号。发布、社区、分析、私信、话题标签、模板和仪表板——全部通过治理机制管理（速率限制、审计日志、公开操作前确认）。

## 快速概览

| 领域 | 脚本 | 功能 |
|------|---------|-----------|
| **设置** | `account_setup.py`, `auth.py` | 配置账号、OAuth、令牌 |
| **发布** | `publish.py`, `schedule.py` | 发布照片/视频/Reel/Story/轮播图，定时发布 |
| **社区** | `comments.py`, `messages.py` | 评论、私信、提及 |
| **分析** | `insights.py`, `analyze.py` | 指标、最佳时间、热门帖子 |
| **话题标签** | `hashtags.py` | 搜索和追踪 |
| **智能** | `templates.py`, `analyze.py` | 内容模板、趋势 |
| **基础设施** | `export.py`, `serve_api.py`, `run_all.py` | 导出、仪表板、同步 |
| **读取** | `profile.py`, `media.py` | 个人资料、列出媒体 |

## 文件位置

```
C:\Users\renat\skills\instagram\
├── SKILL.md
├── scripts/
│   ├── requirements.txt
│   │  # ── 核心模块 ──
│   ├── config.py                     # 路径、常量、媒体规格
│   ├── db.py                         # SQLite：账号、帖子、评论、洞察
│   ├── auth.py                       # OAuth 2.0，令牌存储/刷新
│   ├── api_client.py                 # Instagram Graph API 封装 + 重试
│   ├── governance.py                 # 速率限制、审计日志、确认
│   │  # ── 功能模块 ──
│   ├── account_setup.py              # 账号检测、迁移、验证
│   ├── publish.py                    # 发布 + 通过 Imgur 本地上传
│   ├── schedule.py                   # 编排器：已批准 → 已发布
│   ├── comments.py                   # 读取/回复/删除评论
│   ├── messages.py                   # 私信（发送/接收/列出）
│   ├── insights.py                   # 获取 + 存储指标
│   ├── hashtags.py                   # 搜索 + 追踪
│   ├── profile.py                    # 查看/更新个人资料
│   ├── media.py                      # 列出媒体、详情
│   │  # ── 智能模块 ──
│   ├── templates.py                  # 标题/话题标签模板
│   ├── analyze.py                    # 最佳时间、热门帖子
│   │  # ── 基础设施 ──
│   ├── export.py                     # 导出 JSON/CSV/JSONL
│   ├── serve_api.py                  # FastAPI + 仪表板
│   └── run_all.py                    # 完整同步
├── references/
│   ├── graph_api.md                  # 端点和参数
│   ├── permissions.md                # 各功能的 OAuth 权限范围
│   ├── rate_limits.md                # 2025 年限制
│   ├── account_types.md              # Business 与 Creator 对比
│   ├── publishing_guide.md           # 媒体规格
│   ├── setup_walkthrough.md          # Meta 应用指南
│   └── schema.md                     # ER 图
├── static/
│   └── dashboard.html                # Chart.js 仪表板
└── data/
    

## 安装（一次性）

```bash
pip install -r C:\Users\renat\skills\instagram\scripts\requirements.txt
```

## 初始配置

```bash

## 1. 验证 Instagram 账号类型

python C:\Users\renat\skills\instagram\scripts\account_setup.py --check

## 2. 配置 OAuth（打开浏览器进行授权）

python C:\Users\renat\skills\instagram\scripts\auth.py --setup

## 3. 验证一切是否正常

python C:\Users\renat\skills\instagram\scripts\profile.py --view
```

如果账号是个人账号，脚本 `account_setup.py --guide` 会提供迁移到 Business 或 Creator 的指引。

## 照片（支持本地文件 — 通过 Imgur 自动上传）

python C:\Users\renat\skills\instagram\scripts\publish.py --type photo --image caminho/foto.jpg --caption "Texto do post"

## 视频

python C:\Users\renat\skills\instagram\scripts\publish.py --type video --video caminho/video.mp4 --caption "Meu vídeo"

## Reel

python C:\Users\renat\skills\instagram\scripts\publish.py --type reel --video caminho/reel.mp4 --caption "Novo reel!"

## Story

python C:\Users\renat\skills\instagram\scripts\publish.py --type story --image caminho/story.jpg

## 轮播图（2-10 张图片）

python C:\Users\renat\skills\instagram\scripts\publish.py --type carousel --images img1.jpg img2.jpg img3.jpg --caption "Carrossel"

## 创建为草稿（不立即发布）

python C:\Users\renat\skills\instagram\scripts\publish.py --type photo --image foto.jpg --caption "Texto" --draft

## 批准草稿进行发布

python C:\Users\renat\skills\instagram\scripts\publish.py --approve --id 5
```

## 安排未来发布

python C:\Users\renat\skills\instagram\scripts\schedule.py --type photo --image foto.jpg --caption "Post agendado" --at "2026-03-01T10:00"

## 列出已安排的帖子

python C:\Users\renat\skills\instagram\scripts\schedule.py --list

## 处理待发布的帖子

python C:\Users\renat\skills\instagram\scripts\schedule.py --process

## 取消安排

python C:\Users\renat\skills\instagram\scripts\schedule.py --cancel --id 5
```

## 列出帖子的评论

python C:\Users\renat\skills\instagram\scripts\comments.py --list --media-id 12345

## 回复评论

python C:\Users\renat\skills\instagram\scripts\comments.py --reply --comment-id 67890 --text "Obrigado!"

## 删除评论

python C:\Users\renat\skills\instagram\scripts\comments.py --delete --comment-id 67890

## 查看提及

python C:\Users\renat\skills\instagram\scripts\comments.py --mentions

## 未回复的评论

python C:\Users\renat\skills\instagram\scripts\comments.py --unreplied
```

## 发送私信

python C:\Users\renat\skills\instagram\scripts\messages.py --send --user-id 12345 --text "Olá!"

## 列出对话

python C:\Users\renat\skills\instagram\scripts\messages.py --conversations

## 查看对话消息

python C:\Users\renat\skills\instagram\scripts\messages.py --thread --conversation-id 12345
```

## 特定帖子的指标

python C:\Users\renat\skills\instagram\scripts\insights.py --media --media-id 12345

## 账号指标（最近 7 天）

python C:\Users\renat\skills\instagram\scripts\insights.py --user --period day --since 7

## 获取并保存所有近期帖子的洞察数据

python C:\Users\renat\skills\instagram\scripts\insights.py --fetch-all --limit 20
```

## 最佳发帖时间（基于你的数据）

python C:\Users\renat\skills\instagram\scripts\analyze.py --best-times

## 按互动排名的热门帖子

python C:\Users\renat\skills\instagram\scripts\analyze.py --top-posts --limit 10

## 增长趋势

python C:\Users\renat\skills\instagram\scripts\analyze.py --growth --period 30
```

## 搜索带有话题标签的近期帖子

python C:\Users\renat\skills\instagram\scripts\hashtags.py --search "artificialintelligence" --limit 25

## 话题标签的热门帖子

python C:\Users\renat\skills\instagram\scripts\hashtags.py --top "tecnologia"

## 话题标签信息（帖子数量）

python C:\Users\renat\skills\instagram\scripts\hashtags.py --info "marketing"
```

## 创建模板

python C:\Users\renat\skills\instagram\scripts\templates.py --create --name "promo" --caption "Nova promoção: {produto}! {desconto}% OFF" --hashtags "#oferta,#desconto,#promoção"

## 列出模板

python C:\Users\renat\skills\instagram\scripts\templates.py --list

## 在帖子中使用模板

python C:\Users\renat\skills\instagram\scripts\publish.py --type photo --image foto.jpg --template promo --vars produto="Tênis" desconto=30
```

## 查看个人资料

python C:\Users\renat\skills\instagram\scripts\profile.py --view

## 列出近期帖子

python C:\Users\renat\skills\instagram\scripts\media.py --list --limit 10

## 帖子详情

python C:\Users\renat\skills\instagram\scripts\media.py --details --media-id 12345
```

## 导出分析数据为 CSV

python C:\Users\renat\skills\instagram\scripts\export.py --type insights --format csv

## 导出评论

python C:\Users\renat\skills\instagram\scripts\export.py --type comments --format json

## 导出全部

python C:\Users\renat\skills\instagram\scripts\export.py --type all --format csv

## 启动 Web 仪表板

python C:\Users\renat\skills\instagram\scripts\serve_api.py

## 访问：http://localhost:8000/dashboard

```

## 身份验证状态

python C:\Users\renat\skills\instagram\scripts\auth.py --status

## 完整同步（获取个人资料 + 媒体 + 洞察 + 评论）

python C:\Users\renat\skills\instagram\scripts\run_all.py

## 部分同步

python C:\Users\renat\skills\instagram\scripts\run_all.py --only media insights
```

## 速率限制

此技能会自动追踪 API 的速率限制：
- **200 次请求/小时** 每账号
- **25 次发布/天** 每账号
- **30 个唯一话题标签/周** 每账号
- **200 条私信/小时** 每账号

当达到限制的 90% 时，技能会发出警告。如果超出限制，会阻止操作并告知需要等待多长时间。

## 确认机制

影响公开内容的操作需要确认：
- **PUBLISH**：发布照片/视频/Reel/Story/轮播图
- **DELETE**：删除评论
- **MESSAGE**：发送私信
- **ENGAGE**：回复评论、隐藏评论

脚本会返回操作详情并在执行前请求确认。

## 审计日志

所有修改数据的操作都会记录到 SQLite 数据库中（`action_log` 表）：
- 时间戳、操作、参数、结果、确认状态
- 查询方式：`python C:\Users\renat\skills\instagram\scripts\db.py`

## Token 自动刷新

OAuth 令牌（60 天有效期）会在到期前 7 天自动续期。无需手动干预。

## API 限制

Instagram Graph API **不允许**的操作：
- 删除已发布的帖子
- 发布后编辑标题
- 通过 API 应用滤镜
- 从个人账号发帖（仅限 Business/Creator）
- 24 小时窗口外的私信（用户需要先有过互动）
- 非 JPEG 格式的照片（脚本会自动转换）

## "我想发布一张照片"

```bash
python C:\Users\renat\skills\instagram\scripts\publish.py --type photo --image foto.jpg --caption "Texto"
```

## "给我看看我的分析数据"

```bash
python C:\Users\renat\skills\instagram\scripts\run_all.py --only insights
python C:\Users\renat\skills\instagram\scripts\analyze.py --summary
```

## "最佳发帖时间是什么？"

```bash
python C:\Users\renat\skills\instagram\scripts\analyze.py --best-times
```

## "回复这条评论"

```bash
python C:\Users\renat\skills\instagram\scripts\comments.py --reply --comment-id ID --text "Resposta"
```

## "同步所有数据"

```bash
python C:\Users\renat\skills\instagram\scripts\run_all.py
```

## "打开仪表板"

```bash
python C:\Users\renat\skills\instagram\scripts\serve_api.py
```

## 参考资料

需要详细信息时请查阅：
- `references/graph_api.md` — API 端点、参数和响应
- `references/publishing_guide.md` — 媒体规格（尺寸、格式、大小）
- `references/rate_limits.md` — 详细的速率限制和策略
- `references/account_types.md` — Business 与 Creator 的区别、迁移
- `references/permissions.md` — 各功能所需的 OAuth 权限范围
- `references/setup_walkthrough.md` — Meta 应用设置的分步指南
- `references/schema.md` — SQLite 数据库 Schema（ER 图、字段、索引、查询）

## 最佳实践

- 提供清晰、具体的项目背景和需求
- 在将建议应用到生产代码之前进行审查
- 结合其他互补技能进行全面分析

## 常见陷阱

- 将此技能用于其专业领域之外的任务
- 在不了解具体背景的情况下应用建议
- 没有提供足够的项目背景以获得准确分析

## 相关技能

- `social-orchestrator` - 互补技能，用于增强分析
- `telegram` - 互补技能，用于增强分析
- `whatsapp-cloud-api` - 互补技能，用于增强分析

## 限制
- 仅当任务明确匹配上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
