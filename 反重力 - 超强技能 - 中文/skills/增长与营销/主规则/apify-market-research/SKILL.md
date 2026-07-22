---
name: apify-market-research
description: 使用 Apify Actors 从 Google Maps、Facebook、Instagram、Booking.com 和 TripAdvisor 提取数据，分析市场状况、地理机会、定价、消费者行为和产品验证。触发词：市场研究、市场分析、竞品调研、地理分析、定价分析、消费者行为、产品验证、Google Maps 数据、Facebook 数据、Instagram 数据、TripAdvisor 评论、Booking 数据、市场密度、区域需求、趋势分析
risk: unknown
source: community
---

# 市场研究

使用 Apify Actors 从多个平台提取数据进行市场研究。

## 使用场景
- 需要市场规模、区域需求、定价、趋势或消费者行为数据。
- 任务是从地图、旅游、Facebook、Instagram 或趋势来源通过 Apify 收集研究数据。
- 需要结构化的市场数据以及综合的机会或风险分析视图。

## 前置条件
（无需提前检查）

- 包含 `APIFY_TOKEN` 的 `.env` 文件
- Node.js 20.6+（支持原生 `--env-file`）
- `mcpc` CLI 工具：`npm install -g @apify/mcpc`

## 工作流程

复制此清单并跟踪进度：

```
任务进度：
- [ ] 步骤 1：确定市场研究类型（选择 Actor）
- [ ] 步骤 2：通过 mcpc 获取 Actor schema
- [ ] 步骤 3：询问用户偏好（格式、文件名）
- [ ] 步骤 4：运行分析脚本
- [ ] 步骤 5：总结发现
```

### 步骤 1：确定市场研究类型

根据研究需求选择合适的 Actor：

| 用户需求 | Actor ID | 最佳用途 |
|----------|----------|----------|
| 市场密度 | `compass/crawler-google-places` | 位置分析 |
| 地理空间分析 | `compass/google-maps-extractor` | 商业地图 |
| 区域兴趣 | `apify/google-trends-scraper` | 趋势数据 |
| 定价和需求 | `apify/facebook-marketplace-scraper` | 市场定价 |
| 活动市场 | `apify/facebook-events-scraper` | 活动分析 |
| 消费者需求 | `apify/facebook-groups-scraper` | 群组研究 |
| 市场格局 | `apify/facebook-pages-scraper` | 商业主页 |
| 商业密度 | `apify/facebook-page-contact-information` | 联系数据 |
| 文化洞察 | `apify/facebook-photos-scraper` | 视觉研究 |
| 细分定位 | `apify/instagram-hashtag-scraper` | 话题标签研究 |
| 标签统计 | `apify/instagram-hashtag-stats` | 市场规模 |
| 市场活动 | `apify/instagram-reel-scraper` | 活动分析 |
| 市场情报 | `apify/instagram-scraper` | 完整数据 |
| 产品发布研究 | `apify/instagram-api-scraper` | API 访问 |
| 酒店市场 | `voyager/booking-scraper` | 酒店数据 |
| 旅游洞察 | `maxcopell/tripadvisor-reviews` | 评论分析 |

### 步骤 2：获取 Actor Schema

使用 mcpc 动态获取 Actor 的输入 schema 和详细信息：

```bash
export $(grep APIFY_TOKEN .env | xargs) && mcpc --json mcp.apify.com --header "Authorization: Bearer $APIFY_TOKEN" tools-call fetch-actor-details actor:="ACTOR_ID" | jq -r ".content"
```

将 `ACTOR_ID` 替换为选定的 Actor（例如 `compass/crawler-google-places`）。

这将返回：
- Actor 描述和 README
- 必需和可选的输入参数
- 输出字段（如果有）

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
- 找到的结果数量
- 文件位置和名称
- 关键市场洞察
- 建议的后续步骤（深入分析、验证）

## 错误处理

`APIFY_TOKEN not found` - 请用户创建包含 `APIFY_TOKEN=your_token` 的 `.env` 文件
`mcpc not found` - 请用户安装 `npm install -g @apify/mcpc`
`Actor not found` - 检查 Actor ID 拼写
`Run FAILED` - 请用户查看错误输出中的 Apify 控制台链接
`Timeout` - 减少输入大小或增加 `--timeout`

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出不能替代针对特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
