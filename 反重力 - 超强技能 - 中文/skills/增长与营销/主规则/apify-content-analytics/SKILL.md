---
name: apify-content-analytics
description: 跨平台内容分析工具，追踪Instagram、Facebook、YouTube和TikTok的互动指标、衡量营销活动ROI并分析内容表现。触发词：内容分析、互动指标、营销ROI、社媒数据、帖子表现、视频分析、评论分析、标签追踪、粉丝增长、广告效果、内容表现追踪、Apify Actor
risk: unknown
source: community
---

# 内容分析

使用 Apify Actor 从多个平台提取互动指标，追踪和分析内容表现。

## 使用场景
- 需要获取帖子、Reels、视频、广告或标签的互动、增长或ROI指标。
- 任务是使用 Apify Actor 收集跨平台内容表现数据。
- 需要导出分析结果并解读哪些内容表现最佳。

## 前置条件
（无需提前检查）

- 包含 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持原生 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流程

复制此清单并追踪进度：

```
任务进度：
- [ ] 步骤1：确定内容分析类型（选择 Actor）
- [ ] 步骤2：通过 mcpc 获取 Actor schema
- [ ] 步骤3：询问用户偏好（格式、文件名）
- [ ] 步骤4：运行分析脚本
- [ ] 步骤5：总结发现
```

### 步骤1：确定内容分析类型

根据分析需求选择合适的 Actor：

| 用户需求 | Actor ID | 最佳用途 |
|---------|----------|---------|
| 帖子互动指标 | `apify/instagram-post-scraper` | 帖子表现 |
| Reel 表现 | `apify/instagram-reel-scraper` | Reel 分析 |
| 粉丝增长追踪 | `apify/instagram-followers-count-scraper` | 增长指标 |
| 评论互动 | `apify/instagram-comment-scraper` | 评论分析 |
| 标签表现 | `apify/instagram-hashtag-scraper` | 品牌标签 |
| 提及追踪 | `apify/instagram-tagged-scraper` | 标签追踪 |
| 综合指标 | `apify/instagram-scraper` | 完整数据 |
| 基于API的分析 | `apify/instagram-api-scraper` | API 访问 |
| Facebook帖子表现 | `apify/facebook-posts-scraper` | 帖子指标 |
| 反应分析 | `apify/facebook-likes-scraper` | 互动类型 |
| Facebook Reels指标 | `apify/facebook-reels-scraper` | Reels表现 |
| 广告效果追踪 | `apify/facebook-ads-scraper` | 广告分析 |
| Facebook评论分析 | `apify/facebook-comments-scraper` | 评论互动 |
| 主页表现审计 | `apify/facebook-pages-scraper` | 主页指标 |
| YouTube视频指标 | `streamers/youtube-scraper` | 视频表现 |
| YouTube Shorts分析 | `streamers/youtube-shorts-scraper` | Shorts表现 |
| TikTok内容指标 | `clockworks/tiktok-scraper` | TikTok分析 |

### 步骤2：获取 Actor Schema

使用 mcpc 动态获取 Actor 的输入 schema 和详情：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为选定的 Actor（例如 `apify/instagram-post-scraper`）。

这将返回：
- Actor 描述和 README
- 必需和可选的输入参数
- 输出字段（如有）

### 步骤3：询问用户偏好

运行前，询问：
1. **输出格式**：
   - **快速回答** - 在聊天中显示前几条结果（不保存文件）
   - **CSV** - 导出所有字段的完整数据
   - **JSON** - JSON 格式的完整导出
2. **结果数量**：根据用例特点确定

### 步骤4：运行脚本

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

### 步骤5：总结发现

完成后，报告：
- 分析的内容数量
- 文件位置和名称
- 关键表现洞察
- 建议的后续步骤（深入分析、内容优化）

## 错误处理

`APIFY_TOKEN not found` - 请用户创建包含 `APIFY_TOKEN=your_token` 的 `.env` 文件
`mcpc not found` - 请用户安装 `npm install -g @apify/mcpc`
`Actor not found` - 检查 Actor ID 拼写
`Run FAILED` - 请用户检查错误输出中的 Apify 控制台链接
`Timeout` - 减少输入大小或增加 `--timeout`

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
