---
name: apify-ultimate-scraper
description: "AI驱动的数据提取工具，支持55+个Actor覆盖所有主流平台。此技能自动为您的任务选择最佳Actor。触发词：网页抓取、数据提取、Instagram爬虫、Facebook爬虫、TikTok爬虫、YouTube爬虫、Google Maps爬虫、社交媒体数据、评论抓取、用户画像、商业列表、评论分析、网红发现、品牌监控、竞品分析、趋势研究"
risk: unknown
source: community
---

# 通用网页抓取器

AI驱动的数据提取工具，支持55+个Actor覆盖所有主流平台。此技能自动为您的任务选择最佳Actor。

## 使用场景
- 用户需要网页数据提取但尚未选择特定的Apify Actor。
- 您需要一个通用的Apify入口点，将广泛的抓取目标映射到最合适的Actor。
- 任务跨多个平台，受益于统一的Actor选择、执行和总结工作流。

## 前置条件
（无需预先检查）

- 包含 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持原生 `--env-file`）
- `mcpc` CLI工具：`npm install -g @apify/mcpc`

## 工作流程

复制此检查清单并跟踪进度：

```
任务进度：
- [ ] 步骤1：理解用户目标并选择Actor
- [ ] 步骤2：通过mcpc获取Actor模式
- [ ] 步骤3：询问用户偏好（格式、文件名）
- [ ] 步骤4：运行抓取脚本
- [ ] 步骤5：总结结果并提供后续建议
```

### 步骤1：理解用户目标并选择Actor

首先，理解用户想要实现什么。然后从下方选项中选择最佳Actor。

#### Instagram Actors（12个）

| Actor ID | 最佳用途 |
|----------|----------|
| `apify/instagram-profile-scraper` | 个人资料数据、粉丝数、简介信息 |
| `apify/instagram-post-scraper` | 单条帖子详情、互动指标 |
| `apify/instagram-comment-scraper` | 评论提取、情感分析 |
| `apify/instagram-hashtag-scraper` | 话题标签内容、热门话题 |
| `apify/instagram-hashtag-stats` | 话题标签表现指标 |
| `apify/instagram-reel-scraper` | Reels内容和指标 |
| `apify/instagram-search-scraper` | 搜索用户、地点、话题标签 |
| `apify/instagram-tagged-scraper` | 标记特定账号的帖子 |
| `apify/instagram-followers-count-scraper` | 粉丝数追踪 |
| `apify/instagram-scraper` | 全面的Instagram数据 |
| `apify/instagram-api-scraper` | 基于API的Instagram访问 |
| `apify/export-instagram-comments-posts` | 批量评论/帖子导出 |

#### Facebook Actors（14个）

| Actor ID | 最佳用途 |
|----------|----------|
| `apify/facebook-pages-scraper` | 主页数据、指标、联系信息 |
| `apify/facebook-page-contact-information` | 主页中的邮箱、电话、地址 |
| `apify/facebook-posts-scraper` | 帖子内容和互动 |
| `apify/facebook-comments-scraper` | 评论提取 |
| `apify/facebook-likes-scraper` | 点赞反应分析 |
| `apify/facebook-reviews-scraper` | 主页评论 |
| `apify/facebook-groups-scraper` | 群组内容和成员 |
| `apify/facebook-events-scraper` | 活动数据 |
| `apify/facebook-ads-scraper` | 广告创意和定向 |
| `apify/facebook-search-scraper` | 搜索结果 |
| `apify/facebook-reels-scraper` | Reels内容 |
| `apify/facebook-photos-scraper` | 照片提取 |
| `apify/facebook-marketplace-scraper` | Marketplace列表 |
| `apify/facebook-followers-following-scraper` | 粉丝/关注列表 |

#### TikTok Actors（14个）

| Actor ID | 最佳用途 |
|----------|----------|
| `clockworks/tiktok-scraper` | 全面的TikTok数据 |
| `clockworks/free-tiktok-scraper` | 免费TikTok提取 |
| `clockworks/tiktok-profile-scraper` | 个人资料数据 |
| `clockworks/tiktok-video-scraper` | 视频详情和指标 |
| `clockworks/tiktok-comments-scraper` | 评论提取 |
| `clockworks/tiktok-followers-scraper` | 粉丝列表 |
| `clockworks/tiktok-user-search-scraper` | 按关键词查找用户 |
| `clockworks/tiktok-hashtag-scraper` | 话题标签内容 |
| `clockworks/tiktok-sound-scraper` | 热门音乐 |
| `clockworks/tiktok-ads-scraper` | 广告内容 |
| `clockworks/tiktok-discover-scraper` | 发现页内容 |
| `clockworks/tiktok-explore-scraper` | 探索内容 |
| `clockworks/tiktok-trends-scraper` | 热门内容 |
| `clockworks/tiktok-live-scraper` | 直播数据 |

#### YouTube Actors（5个）

| Actor ID | 最佳用途 |
|----------|----------|
| `streamers/youtube-scraper` | 视频数据和指标 |
| `streamers/youtube-channel-scraper` | 频道信息 |
| `streamers/youtube-comments-scraper` | 评论提取 |
| `streamers/youtube-shorts-scraper` | Shorts内容 |
| `streamers/youtube-video-scraper-by-hashtag` | 按话题标签查找视频 |

#### Google Maps Actors（4个）

| Actor ID | 最佳用途 |
|----------|----------|
| `compass/crawler-google-places` | 商家列表、评分、联系信息 |
| `compass/google-maps-extractor` | 详细商家数据 |
| `compass/Google-Maps-Reviews-Scraper` | 评论提取 |
| `poidata/google-maps-email-extractor` | 从列表中发现邮箱 |

#### 其他Actors（6个）

| Actor ID | 最佳用途 |
|----------|----------|
| `apify/google-search-scraper` | Google搜索结果 |
| `apify/google-trends-scraper` | Google Trends数据 |
| `voyager/booking-scraper` | Booking.com酒店数据 |
| `voyager/booking-reviews-scraper` | Booking.com评论 |
| `maxcopell/tripadvisor-reviews` | TripAdvisor评论 |
| `vdrmota/contact-info-scraper` | 从URL提取联系信息 |

---

#### 按用例选择Actor

| 用例 | 主要Actors |
|------|------------|
| **潜在客户开发** | `compass/crawler-google-places`, `poidata/google-maps-email-extractor`, `vdrmota/contact-info-scraper` |
| **网红发现** | `apify/instagram-profile-scraper`, `clockworks/tiktok-profile-scraper`, `streamers/youtube-channel-scraper` |
| **品牌监控** | `apify/instagram-tagged-scraper`, `apify/instagram-hashtag-scraper`, `compass/Google-Maps-Reviews-Scraper` |
| **竞品分析** | `apify/facebook-pages-scraper`, `apify/facebook-ads-scraper`, `apify/instagram-profile-scraper` |
| **内容分析** | `apify/instagram-post-scraper`, `clockworks/tiktok-scraper`, `streamers/youtube-scraper` |
| **趋势研究** | `apify/google-trends-scraper`, `clockworks/tiktok-trends-scraper`, `apify/instagram-hashtag-stats` |
| **评论分析** | `compass/Google-Maps-Reviews-Scraper`, `voyager/booking-reviews-scraper`, `maxcopell/tripadvisor-reviews` |
| **受众分析** | `apify/instagram-followers-count-scraper`, `clockworks/tiktok-followers-scraper`, `apify/facebook-followers-following-scraper` |

---

#### 多Actor工作流

对于复杂任务，可串联多个Actor：

| 工作流 | 步骤1 | 步骤2 |
|--------|-------|-------|
| **潜在客户丰富** | `compass/crawler-google-places` → | `vdrmota/contact-info-scraper` |
| **网红背调** | `apify/instagram-profile-scraper` → | `apify/instagram-comment-scraper` |
| **竞品深度分析** | `apify/facebook-pages-scraper` → | `apify/facebook-posts-scraper` |
| **本地商家分析** | `compass/crawler-google-places` → | `compass/Google-Maps-Reviews-Scraper` |

#### 找不到合适的Actor？

如果上方Actors均不匹配用户请求，可直接搜索Apify Store：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call search-actors keywords:="SEARCH_KEYWORDS" limit:=10 offset:=0 category:="" | jq -r '.content[0].text'
```

将 `SEARCH_KEYWORDS` 替换为1-3个简单术语（例如 "LinkedIn profiles", "Amazon products", "Twitter"）。

### 步骤2：获取Actor模式

使用mcpc动态获取Actor的输入模式和详情：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为选定的Actor（例如 `compass/crawler-google-places`）。

这将返回：
- Actor描述和README
- 必需和可选的输入参数
- 输出字段（如有）

### 步骤3：询问用户偏好

运行前，询问：
1. **输出格式**：
   - **快速回答** - 在聊天中显示前几条结果（不保存文件）
   - **CSV** - 导出所有字段
   - **JSON** - 以JSON格式导出
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

### 步骤5：总结结果并提供后续建议

完成后，报告：
- 找到的结果数量
- 文件位置和名称
- 可用的关键字段
- **基于结果建议的后续工作流**：

| 如果用户获取了 | 建议下一步 |
|----------------|------------|
| 商家列表 | 使用 `vdrmota/contact-info-scraper` 丰富信息或获取评论 |
| 网红资料 | 使用评论抓取器分析互动情况 |
| 竞品主页 | 使用帖子/广告抓取器深入分析 |
| 趋势数据 | 使用平台特定的话题标签抓取器验证 |

## 错误处理

`APIFY_TOKEN not found` - 请用户创建包含 `APIFY_TOKEN=your_token` 的 `.env` 文件
`mcpc not found` - 请用户安装 `npm install -g @apify/mcpc`
`Actor not found` - 检查Actor ID拼写
`Run FAILED` - 请用户查看错误输出中的Apify控制台链接
`Timeout` - 减少输入规模或增加 `--timeout`

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
