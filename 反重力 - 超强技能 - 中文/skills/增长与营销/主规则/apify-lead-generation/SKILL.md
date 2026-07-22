---
name: apify-lead-generation
description: "使用 Apify Actors 从多个平台抓取潜在客户线索。触发词：潜在客户挖掘、线索抓取、lead generation、Apify、Instagram抓取、TikTok抓取、Google Maps商家、联系人抓取、商业线索、创作者发现"
risk: unknown
source: community
---

# 潜在客户挖掘

使用 Apify Actors 从多个平台抓取潜在客户线索。

## 何时使用

- 您需要从地图、搜索、社交或视频平台获取企业、创作者或联系人线索。
- 任务涉及选择 Apify Actor 来发现潜在客户并提取外联数据。
- 您需要导出的线索数据以及线索质量或细分的简要总结。

## 前置条件
（无需提前检查）

- 包含 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持原生 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流程

复制此清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：确定线索来源（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor schema
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行线索查找脚本
- [ ] 步骤 5：总结结果
```

### 步骤 1：确定线索来源

根据用户需求选择合适的 Actor：

| 用户需求 | Actor ID | 最适合场景 |
|-----------|----------|----------|
| 本地商家 | `compass/crawler-google-places` | 餐厅、健身房、商店 |
| 联系人丰富 | `vdrmota/contact-info-scraper` | 从 URL 提取邮箱、电话 |
| Instagram 个人资料 | `apify/instagram-profile-scraper` | 网红发现 |
| Instagram 帖子/评论 | `apify/instagram-scraper` | 帖子、评论、话题标签、地点 |
| Instagram 搜索 | `apify/instagram-search-scraper` | 地点、用户、话题标签发现 |
| TikTok 视频/话题标签 | `clockworks/tiktok-scraper` | 全面的 TikTok 数据提取 |
| TikTok 话题标签/个人资料 | `clockworks/free-tiktok-scraper` | 免费 TikTok 数据提取器 |
| TikTok 用户搜索 | `clockworks/tiktok-user-search-scraper` | 按关键词查找用户 |
| TikTok 个人资料 | `clockworks/tiktok-profile-scraper` | 创作者外联 |
| TikTok 粉丝/关注 | `clockworks/tiktok-followers-scraper` | 受众分析、细分 |
| Facebook 主页 | `apify/facebook-pages-scraper` | 商业联系人 |
| Facebook 主页联系人 | `apify/facebook-page-contact-information` | 提取邮箱、电话、地址 |
| Facebook 群组 | `apify/facebook-groups-scraper` | 购买意向信号 |
| Facebook 活动 | `apify/facebook-events-scraper` | 活动社交、合作 |
| Google 搜索 | `apify/google-search-scraper` | 广泛线索发现 |
| YouTube 频道 | `streamers/youtube-scraper` | 创作者合作 |
| Google Maps 邮箱 | `poidata/google-maps-email-extractor` | 直接邮箱提取 |

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
   - **JSON** - 以 JSON 格式导出完整数据
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

### 步骤 5：总结结果

完成后报告：
- 找到的线索数量
- 文件位置和名称
- 可用的关键字段
- 建议的下一步（筛选、丰富）

## 错误处理

`APIFY_TOKEN not found` - 请用户创建包含 `APIFY_TOKEN=your_token` 的 `.env` 文件
`mcpc not found` - 请用户安装 `npm install -g @apify/mcpc`
`Actor not found` - 检查 Actor ID 拼写
`Run FAILED` - 请用户检查错误输出中的 Apify 控制台链接
`Timeout` - 减少输入大小或增加 `--timeout`

## 限制

- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
