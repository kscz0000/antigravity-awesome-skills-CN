---
name: apify-brand-reputation-monitoring
description: "使用 Apify Actors 从多个平台抓取评论、评分和品牌提及。触发词：品牌声誉监控、评论抓取、评分监控、品牌提及、Apify Actor、声誉追踪、评论分析、社交监听、评价监控、品牌情感分析"
risk: unknown
source: community
---

# 品牌声誉监控

使用 Apify Actors 从多个平台抓取评论、评分和品牌提及。

## 何时使用

- 需要监控社交、旅游或地图平台上的评论、评分或品牌提及。
- 任务是选择并运行 Apify Actor 进行品牌情感或声誉追踪。
- 需要导出监控结果和声誉信号摘要。

## 前置条件
（无需提前检查）

- 包含 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持原生 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流程

复制此清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：确定数据源（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor schema
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行监控脚本
- [ ] 步骤 5：汇总结果
```

### 步骤 1：确定数据源

根据用户需求选择合适的 Actor：

| 用户需求 | Actor ID | 最适合 |
|----------|----------|--------|
| Google Maps 评论 | `compass/crawler-google-places` | 商家评论、评分 |
| Google Maps 评论导出 | `compass/Google-Maps-Reviews-Scraper` | 专用评论抓取 |
| Booking.com 酒店 | `voyager/booking-scraper` | 酒店数据、评分 |
| Booking.com 评论 | `voyager/booking-reviews-scraper` | 详细酒店评论 |
| TripAdvisor 评论 | `maxcopell/tripadvisor-reviews` | 景点/餐厅评论 |
| Facebook 评论 | `apify/facebook-reviews-scraper` | 主页评论 |
| Facebook 评论 | `apify/facebook-comments-scraper` | 帖子评论监控 |
| Facebook 主页指标 | `apify/facebook-pages-scraper` | 主页评分概览 |
| Facebook 反应 | `apify/facebook-likes-scraper` | 反应类型分析 |
| Instagram 评论 | `apify/instagram-comment-scraper` | 评论情感分析 |
| Instagram 话题标签 | `apify/instagram-hashtag-scraper` | 品牌标签监控 |
| Instagram 搜索 | `apify/instagram-search-scraper` | 品牌提及发现 |
| Instagram 标记帖子 | `apify/instagram-tagged-scraper` | 品牌标签追踪 |
| Instagram 导出 | `apify/export-instagram-comments-posts` | 批量评论导出 |
| Instagram 综合 | `apify/instagram-scraper` | 完整 Instagram 监控 |
| Instagram API | `apify/instagram-api-scraper` | 基于 API 的监控 |
| YouTube 评论 | `streamers/youtube-comments-scraper` | 视频评论情感 |
| TikTok 评论 | `clockworks/tiktok-comments-scraper` | TikTok 情感分析 |

### 步骤 2：获取 Actor Schema

使用 mcpc 动态获取 Actor 的输入 schema 和详情：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为选定的 Actor（例如 `compass/crawler-google-places`）。

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

### 步骤 5：汇总结果

完成后报告：
- 找到的评论/提及数量
- 文件位置和名称
- 可用的关键字段
- 建议的后续步骤（情感分析、筛选）

## 错误处理

`APIFY_TOKEN not found` - 请用户创建包含 `APIFY_TOKEN=your_token` 的 `.env` 文件
`mcpc not found` - 请用户安装 `npm install -g @apify/mcpc`
`Actor not found` - 检查 Actor ID 拼写
`Run FAILED` - 请用户查看错误输出中的 Apify 控制台链接
`Timeout` - 减少输入规模或增加 `--timeout`

## 限制

- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
