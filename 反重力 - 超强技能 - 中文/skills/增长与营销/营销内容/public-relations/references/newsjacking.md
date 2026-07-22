# 新闻搭车 —— 反应式公关工作流

将你的观点注入已经在流行的故事。做得好：搭上注意力浪潮的免费传播。做得差：轻则尴尬，重则品牌受损。

## 目录
- 新闻搭车何时有效（何时不适用）
- 检测 → 评分 → 角度 → 推介 循环
- 新闻价值评分标准
- 故事角度库
- 速度：唯一重要的事
- 信息源与工具
- 失败模式

---

## 新闻搭车何时有效

- **你领域的科技/监管新闻** —— 新法规、新平台上线、竞争对手转型、重大收购
- **行业数据发布** —— 重大报告发布，你有更犀利的观点或矛盾数据
- **公共讨论** —— 你的专长真正相关的辩论或争议
- **季节性/周期性时刻** —— 财报季、年终回顾、会议周

## 该跳过的时机

- **悲剧、事故、死亡** —— 没有例外。不要碰。
- **政治敏感故事**，除非你的品牌明确持政治立场
- **你在该领域没有真正的专长**
- **窗口已关闭** —— 如果故事已超过 48 小时且你不是第一个，你就迟了
- **角度是"我们有个产品解决这个问题"** —— 那是营销，不是新闻

---

## 循环

一个可重复的工作流，Claude 可按需或每日运行。

1. **检测** —— 发掘你领域中的热门故事（见[信息源与工具](#信息源与工具)）
2. **评分** —— 应用[新闻价值评分标准](#新闻价值评分标准)；去掉低于阈值的
3. **角度** —— 使用[角度库](#故事角度库)为每个故事生成 2-3 个角度
4. **验证** —— 常识检查：你真的有支撑这个角度的专长/数据吗？
5. **推介** —— 向 3-5 位报道该领域的记者起草精简推介（见[journalist-pitching.md](journalist-pitching.md)）
6. **发布** —— 同时在你的博客、LinkedIn、X 上发布——这会建立记者在引用你之前会检查的痕迹

Claude 应生成的输出格式：

```
NEWSJACK CANDIDATE — 2026-06-10

Story: "EU passes AI Act amendment requiring agent registration"
Source: TechCrunch, 3h ago
Score: 8/10 (high relevance, fresh, you have proprietary data)

Angles:
1. Data hot take: "Our analysis of 12,000 agent deployments shows 73% would fail this requirement"
2. Contrarian: "Why the registration rule will hurt safety, not improve it"
3. Customer story: "How [customer] is preparing — interview offer"

Recommended: #1 (you have unique data, strongest hook)
Pitch draft: [see journalist-pitching.md for template]
Target journalists: [list with rationale]
```

---

## 新闻价值评分标准

对每个候选在五个维度上打 1-10 分，乘以权重，然后求和。最高可能分：80（10 × 8 倍权重总和）。

| 维度 | 衡量什么 | 权重 |
|------|----------|------|
| **时效性** | 故事 <24 小时？窗口仍然开放？ | 2x |
| **相关性** | 确实在你的专业领域？ | 2x |
| **角度独特性** | 你能说出别人说不了的话？ | 2x |
| **权威性** | 你有数据、客户或经验来支撑？ | 1x |
| **传播潜力** | 这个故事会继续增长还是已经见顶？ | 1x |

**阈值：** 加权总分 ≥ 50/80。低于此，跳过。

**自动淘汰条件：**
- 故事是关于悲剧性事件
- 你的角度只是"我不同意"但没有支撑
- 你并没有真正形成观点——只是想被引用

---

## 故事角度库

用这些模板快速生成角度。

### 1. 数据热点
*"我们在[事件]后分析了 [N] 个[事物]。以下是我们发现的。"*

当你有独家数据时最佳。记者得到一个数据，你得到引用。

### 2. 反共识
*"大家都在说[流行观点]。以下是为什么他们错了。"*

当你能用具体内容支撑立场时最佳。仅仅为博眼球而反对则很弱。

### 3. "我们预言了这件事"
*"六个月前我们写了[内容]——现在正在发生，接下来会怎样。"*

当你真的预言过时最佳。如果你没预言过，这会致命地损害你的信誉。

### 4. 客户影响
*"这里有一位直接受影响的[客户类型]。我们可以让你联系他们。"*

B2B 最适用。记者喜欢愿意发言的具名客户。

### 5. 内部人解读
*"这个故事很复杂。以下才是真正在发生的事。"*

当大多数报道缺少细节时最佳。你不是在争论——你在科普。

### 6. 趋势关联者
*"这不是孤立事件——它是我们在[模式]中看到的更大转变的一部分。"*

当你有多个数据点或例子可以串联时最佳。

### 7. 创始人观点
*"作为在这个领域构建了 [X 年]的人，大多数人在忽略的是这个。"*

观点文章/op-eds 最佳。作为简短推介则较弱。

---

## 速度：唯一重要的事

新闻搭车衰减很快。大致窗口：

| 故事类型 | 有效窗口 |
|----------|----------|
| 突发科技新闻 | 4-12 小时 |
| 重大监管/政策 | 24-48 小时 |
| 行业报告/数据发布 | 24-72 小时 |
| 会议公告 | 当天 |
| 收购/融资新闻 | 12-24 小时 |

**含义：** 如果你不能在窗口内起草并发送，就别费心了。设置好循环使检测 → 推介耗时 <2 小时。

---

## 信息源与工具

复用 `social` 技能监听工作流的工具。同样安装：`brew install jq`。

### Google News RSS（无需认证）

```bash
# Replace QUERY with topic (use + for spaces, %22 for quotes)
curl -s "https://news.google.com/rss/search?q=QUERY&hl=en-US&gl=US&ceid=US:en" \
  | xmllint --xpath "//item[position()<11]" - 2>/dev/null
```

### Hacker News（Algolia）—— 科技故事

```bash
SINCE=$(($(date +%s) - 86400))
curl -s "https://hn.algolia.com/api/v1/search_by_date?query=QUERY&tags=story&numericFilters=created_at_i>${SINCE}" \
  | jq '.hits[] | {title, url, points, num_comments, created_at, hn_url: ("https://news.ycombinator.com/item?id="+.objectID)}'
```

### Reddit（特定类别子版块）

```bash
curl -s -A "newsjack/1.0" \
  "https://www.reddit.com/r/SUBREDDIT/top.json?t=day&limit=15" \
  | jq '.data.children[].data | {title, url, score, num_comments, created_utc}'
```

### 记者研究（浏览器驱动）

寻找*哪些*记者正在报道该故事：
- **dev-browser** → Google News 搜索故事 → 点击文章 → 记录署名
- 然后去那些记者的 X / LinkedIn / Muck Rack 页面确认领域和近期报道

另见 [journalist-pitching.md](journalist-pitching.md) 了解完整的发现工作流。

### 信息源列表

对于可重复的监控，在 `.agents/listening-sources.md` 中添加"新闻搭车主题"部分（模板在 `social` 技能的 references 中）：

```markdown
## Newsjacking topics (Google News RSS)
- "AI agent regulation"
- "[your category] funding"
- "[your competitors] OR [adjacent competitors]"

## Industry data drops (RSS / manual)
- Pitchbook reports
- a16z state of [industry] reports
- [your category] benchmark reports
```

---

## 失败模式

这些事毁过职业生涯和品牌。

- **悲剧搭车** —— Oreo 2013 年超级碗推文成功了。此后大多数尝试没有。战争、灾难、死亡：不要碰。
- **强行关联** —— "这是我们关于[热门故事]的观点——它其实是关于[我们的产品]的。"记者一眼就看穿。
- **空洞观点** —— 推介"我们有观点"但没有具体内容。记者需要可引用的句子，不是"我们正在密切关注"。
- **有速度无判断** —— 用坏观点抢第一比用好观点赶晚更糟。30 分钟的"这是否符合品牌调性？"直觉检查存在是有原因的。
- **把同一角度推介给 50 位记者** —— 他们会交流。被抓到一次，关系就没了。
- **没有后续** —— 推介发出，记者 20 分钟内回复，创始人 6 小时后才回。故事已经过去了。

---

## 配套实践：公开痕迹

如果记者能找到你公开思考过这个话题的证据，每条新闻搭车推介都更强。推介之前：

1. 发布一篇短帖（博客、LinkedIn、X 话题串）表达你的观点
2. 在推介中引用（"更多思考见：[链接]"）
3. 这表明你不是投机取巧——你是该领域真正的声音

如果你没时间发布，你大概还没准备好推介。
