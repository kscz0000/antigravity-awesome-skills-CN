---
name: apify-influencer-discovery
description: 发现和评估网红用于品牌合作，验证真实性，追踪Instagram、Facebook、YouTube和TikTok跨平台合作表现。触发词：网红发现、influencer discovery、网红搜索、KOL发现、网红评估、社媒网红、网红营销、网红分析、Instagram网红、TikTok网红、YouTube创作者、网红数据、网红合作
risk: unknown
source: community
---

# 网红发现

使用 Apify Actors 跨多平台发现和分析网红。

## 使用场景
- 需要发现创作者或网红用于外联、合作或营销活动规划。
- 任务是评估真实性、互动率、领域匹配度或跨社交平台的受众信号。
- 需要 Apify 驱动的数据提取，以及合适网红候选人的短名单或摘要。

## 前置条件
（无需提前检查）

- 包含 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持原生 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流程

复制此清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：确定发现来源（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor schema
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行发现脚本
- [ ] 步骤 5：汇总结果
```

### 步骤 1：确定发现来源

根据用户需求选择合适的 Actor：

| 用户需求 | Actor ID | 最适合场景 |
|-----------|----------|----------|
| 网红资料 | `apify/instagram-profile-scraper` | 资料指标、简介、粉丝数 |
| 按标签查找 | `apify/instagram-hashtag-scraper` | 发现使用特定标签的网红 |
| Reel 互动 | `apify/instagram-reel-scraper` | 分析 Reel 表现和互动 |
| 按领域发现 | `apify/instagram-search-scraper` | 按关键词/领域搜索网红 |
| 品牌提及 | `apify/instagram-tagged-scraper` | 追踪谁标记了品牌/产品 |
| 综合数据 | `apify/instagram-scraper` | 完整资料、帖子、评论分析 |
| API 驱动发现 | `apify/instagram-api-scraper` | 快速 API 数据提取 |
| 互动分析 | `apify/export-instagram-comments-posts` | 导出评论用于情感分析 |
| Facebook 内容 | `apify/facebook-posts-scraper` | 分析 Facebook 帖子表现 |
| 微型网红 | `apify/facebook-groups-scraper` | 在利基群组中发现网红 |
| 影响力页面 | `apify/facebook-search-scraper` | 搜索有影响力的页面 |
| YouTube 创作者 | `streamers/youtube-channel-scraper` | 频道指标和订阅者数据 |
| TikTok 网红 | `clockworks/tiktok-scraper` | 全面 TikTok 数据提取 |
| TikTok（免费） | `clockworks/free-tiktok-scraper` | 免费 TikTok 数据提取器 |
| 直播主播 | `clockworks/tiktok-live-scraper` | 发现直播网红 |

### 步骤 2：获取 Actor Schema

使用 mcpc 动态获取 Actor 的输入 schema 和详情：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为选定的 Actor（例如 `apify/instagram-profile-scraper`）。

这将返回：
- Actor 描述和 README
- 必需和可选输入参数
- 输出字段（如有）

### 步骤 3：询问用户偏好

运行前询问：
1. **输出格式**：
   - **快速回答** - 在聊天中显示前几条结果（不保存文件）
   - **CSV** - 包含所有字段的完整导出
   - **JSON** - JSON 格式的完整导出
2. **结果数量**：根据用例特点确定

### 步骤 4：运行脚本

**快速回答（在聊天中显示，无文件）：**
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
- 发现的网红数量
- 文件位置和名称
- 可用的关键指标（粉丝数、互动率等）
- 建议的后续步骤（筛选、外联、深入分析）

## 错误处理

`APIFY_TOKEN not found` - 请用户创建包含 `APIFY_TOKEN=your_token` 的 `.env` 文件
`mcpc not found` - 请用户安装 `npm install -g @apify/mcpc`
`Actor not found` - 检查 Actor ID 拼写
`Run FAILED` - 请用户检查错误输出中的 Apify 控制台链接
`Timeout` - 减少输入量或增加 `--timeout`

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
