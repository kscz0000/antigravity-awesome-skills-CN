---
name: apify-trend-analysis
description: 发现和追踪 Google Trends、Instagram、Facebook、YouTube 和 TikTok 等平台的新兴趋势，为内容策略提供依据。触发词：趋势分析、热门话题、内容趋势、社交媒体趋势、Google Trends、Instagram 话题标签、TikTok 热门、YouTube Shorts、趋势追踪、热门发现
risk: unknown
source: community
---

# 趋势分析

使用 Apify Actors 从多个平台提取数据，发现和追踪新兴趋势。

## 前提条件
（无需提前检查）

- 包含 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持原生 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流程

复制此清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：确定趋势类型（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor schema
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行分析脚本
- [ ] 步骤 5：总结发现
```

### 步骤 1：确定趋势类型

根据研究需求选择合适的 Actor：

| 用户需求 | Actor ID | 最佳用途 |
|----------|----------|----------|
| 搜索趋势 | `apify/google-trends-scraper` | Google Trends 数据 |
| 话题标签追踪 | `apify/instagram-hashtag-scraper` | 标签内容 |
| 标签指标 | `apify/instagram-hashtag-stats` | 性能统计 |
| 视觉趋势 | `apify/instagram-post-scraper` | 帖子分析 |
| 热门发现 | `apify/instagram-search-scraper` | 搜索趋势 |
| 全面追踪 | `apify/instagram-scraper` | 完整数据 |
| 基于 API 的趋势 | `apify/instagram-api-scraper` | API 访问 |
| 互动趋势 | `apify/export-instagram-comments-posts` | 评论追踪 |
| 产品趋势 | `apify/facebook-marketplace-scraper` | 市场数据 |
| 视觉分析 | `apify/facebook-photos-scraper` | 图片趋势 |
| 社区趋势 | `apify/facebook-groups-scraper` | 群组监控 |
| YouTube Shorts | `streamers/youtube-shorts-scraper` | 短视频趋势 |
| YouTube 标签 | `streamers/youtube-video-scraper-by-hashtag` | 标签视频 |
| TikTok 标签 | `clockworks/tiktok-hashtag-scraper` | 标签内容 |
| 热门音频 | `clockworks/tiktok-sound-scraper` | 音频趋势 |
| TikTok 广告 | `clockworks/tiktok-ads-scraper` | 广告趋势 |
| 发现页 | `clockworks/tiktok-discover-scraper` | 发现趋势 |
| 探索趋势 | `clockworks/tiktok-explore-scraper` | 探索内容 |
| 热门内容 | `clockworks/tiktok-trends-scraper` | 病毒式内容 |

### 步骤 2：获取 Actor Schema

使用 mcpc 动态获取 Actor 的输入 schema 和详情：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为选定的 Actor（例如 `apify/google-trends-scraper`）。

这将返回：
- Actor 描述和 README
- 必需和可选的输入参数
- 输出字段（如有）

### 步骤 3：询问用户偏好

运行前询问：
1. **输出格式**：
   - **快速回答** - 在聊天中显示前几条结果（不保存文件）
   - **CSV** - 导出所有字段的完整数据
   - **JSON** - JSON 格式的完整导出
2. **结果数量**：根据用例特点确定

### 步骤 4：运行脚本

**快速回答（在聊天中显示，不保存文件）：**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT'
```

**CSV：**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_OUTPUT_FILE.csv \
  --format csv
```

**JSON：**
```bash
node --env-file=.env ${CLAUDE_PLUGIN_ROOT}/reference/scripts/run_actor.js \
  --actor "ACTOR_ID" \
  --input 'JSON_INPUT' \
  --output YYYY-MM-DD_OUTPUT_FILE.json \
  --format json
```

### 步骤 5：总结发现

完成后报告：
- 发现的结果数量
- 文件位置和名称
- 关键趋势洞察
- 建议的后续步骤（深入分析、内容机会）


## 错误处理

`APIFY_TOKEN not found` - 请用户创建包含 `APIFY_TOKEN=your_token` 的 `.env` 文件
`mcpc not found` - 请用户安装 `npm install -g @apify/mcpc`
`Actor not found` - 检查 Actor ID 拼写
`Run FAILED` - 请用户检查错误输出中的 Apify 控制台链接
`Timeout` - 减少输入规模或增加 `--timeout`


## 使用时机
当处理与其主要领域或上述功能相关的任务时，使用此技能。

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
