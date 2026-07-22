---
name: apify-audience-analysis
description: 分析 Facebook、Instagram、YouTube 和 TikTok 跨平台的受众人口统计、偏好、行为模式和互动质量。触发词：受众分析、观众分析、粉丝画像、用户画像、受众统计、社媒受众、粉丝行为、互动分析、audience analysis、follower demographics、engagement patterns
risk: unknown
source: community
---

# 受众分析

使用 Apify Actor 从多个平台提取粉丝人口统计、互动模式和行为数据，分析和理解你的受众。

## 使用场景
- 需要从社交平台获取受众人口统计、互动模式或粉丝行为数据。
- 任务是选择并运行 Apify Actor 进行 Facebook、Instagram、YouTube 或 TikTok 的受众分析。
- 需要结构化提取以及受众发现的总结解读。

## 前置条件
（无需预先检查）

- 包含 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持原生 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流程

复制此清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：确定受众分析类型（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor schema
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行分析脚本
- [ ] 步骤 5：总结发现
```

### 步骤 1：确定受众分析类型

根据分析需求选择合适的 Actor：

| 用户需求 | Actor ID | 最佳用途 |
|---------|----------|---------|
| Facebook 粉丝人口统计 | `apify/facebook-followers-following-scraper` | FB 粉丝/关注列表 |
| Facebook 互动行为 | `apify/facebook-likes-scraper` | FB 帖子点赞分析 |
| Facebook 视频受众 | `apify/facebook-reels-scraper` | FB Reels 观看者 |
| Facebook 评论分析 | `apify/facebook-comments-scraper` | FB 帖子/视频评论 |
| Facebook 内容互动 | `apify/facebook-posts-scraper` | FB 帖子互动指标 |
| Instagram 受众规模 | `apify/instagram-profile-scraper` | IG 档案人口统计 |
| Instagram 基于位置 | `apify/instagram-search-scraper` | IG 地理标记受众 |
| Instagram 标签网络 | `apify/instagram-tagged-scraper` | IG 标签网络分析 |
| Instagram 全面分析 | `apify/instagram-scraper` | 完整 IG 受众数据 |
| Instagram API 方式 | `apify/instagram-api-scraper` | IG API 访问 |
| Instagram 粉丝计数 | `apify/instagram-followers-count-scraper` | IG 粉丝追踪 |
| Instagram 评论导出 | `apify/export-instagram-comments-posts` | IG 评论批量导出 |
| Instagram 评论分析 | `apify/instagram-comment-scraper` | IG 评论情感分析 |
| YouTube 观看者反馈 | `streamers/youtube-comments-scraper` | YT 评论分析 |
| YouTube 频道受众 | `streamers/youtube-channel-scraper` | YT 频道订阅者 |
| TikTok 粉丝人口统计 | `clockworks/tiktok-followers-scraper` | TT 粉丝列表 |
| TikTok 档案分析 | `clockworks/tiktok-profile-scraper` | TT 档案人口统计 |
| TikTok 评论分析 | `clockworks/tiktok-comments-scraper` | TT 评论互动 |

### 步骤 2：获取 Actor Schema

使用 mcpc 动态获取 Actor 的输入 schema 和详情：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为选定的 Actor（例如 `apify/facebook-followers-following-scraper`）。

这将返回：
- Actor 描述和 README
- 必需和可选的输入参数
- 输出字段（如有）

### 步骤 3：询问用户偏好

运行前，询问：
1. **输出格式**：
   - **快速回答** - 在聊天中显示前几条结果（不保存文件）
   - **CSV** - 包含所有字段的完整导出
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

完成后，报告：
- 分析的受众成员/档案数量
- 文件位置和名称
- 关键人口统计洞察
- 建议的下一步（深入分析、细分）

## 错误处理

`APIFY_TOKEN not found` - 请用户创建包含 `APIFY_TOKEN=your_token` 的 `.env` 文件
`mcpc not found` - 请用户安装 `npm install -g @apify/mcpc`
`Actor not found` - 检查 Actor ID 拼写
`Run FAILED` - 请用户查看错误输出中的 Apify 控制台链接
`Timeout` - 减少输入大小或增加 `--timeout`

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
