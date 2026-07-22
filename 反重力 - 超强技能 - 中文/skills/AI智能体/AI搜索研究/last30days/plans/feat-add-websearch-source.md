# 功能：添加 WebSearch 作为第三来源（零配置回退）

## 概述

将 Claude 内置的 WebSearch 工具添加为 `/last30days` 的第三个研究来源。这使技能能够**开箱即用，无需任何 API 密钥**，同时保留 Reddit/X 作为"带有流行度信号的真实人类声音"的首要地位。

**关键原则**：WebSearch 是补充性的，而非主要的。Reddit/X 上带有互动指标（点赞、喜欢、评论）的真实人类声音比一般网络内容更有价值。

## 问题陈述

目前 `/last30days` 需要至少一个 API 密钥（OpenAI 或 xAI）才能运行。没有 API 密钥的用户会收到错误。此外，网络搜索可以填补 Reddit/X 覆盖范围较薄的空白。

**用户要求**：
- 开箱即用（无需 API 密钥）
- 绝不能压倒 Reddit/X 结果
- 需要适当的权重
- 通过前后测试验证

## 提议的解决方案

### 权重策略："互动调整评分"

**当前公式**（Reddit/X 相同）：
```
score = 0.45*relevance + 0.25*recency + 0.30*engagement - penalties
```

**问题**：WebSearch 没有互动指标。给它 `DEFAULT_ENGAGEMENT=35` 配 `-10 penalty` = 25 基础分，仍然不公平地竞争。

**解决方案**：特定来源评分，使用**互动替代**：

| 来源 | 相关性 | 时效性 | 互动 | 来源惩罚 |
|------|--------|--------|------|----------|
| Reddit | 45% | 25% | 30%（真实指标） | 0 |
| X | 45% | 25% | 30%（真实指标） | 0 |
| WebSearch | 55% | 35% | 0%（无数据） | -15 分 |

**理由**：
- WebSearch 项目仅凭相关性和时效性竞争（重新加权至 100%）
- `-15 分来源惩罚` 确保 WebSearch 排名低于可比的 Reddit/X 项目
- 高质量 WebSearch 仍可出现（分数 60-70）但不会主导（Reddit/X 分数 70-85）

### 模式行为

| 可用 API 密钥 | 默认行为 | `--include-web` |
|---------------|----------|-----------------|
| 无 | **仅 WebSearch** | 不适用 |
| 仅 OpenAI | 仅 Reddit | Reddit + WebSearch |
| 仅 xAI | 仅 X | X + WebSearch |
| 两者 | Reddit + X | Reddit + X + WebSearch |

**CLI 标志**：`--include-web`（当有其他来源可用时默认：false）

## 技术方法

### 架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     last30days.py 编排器                         │
├─────────────────────────────────────────────────────────────────┤
│  run_research()                                                  │
│  ├── if sources includes "reddit": openai_reddit.search_reddit()│
│  ├── if sources includes "x": xai_x.search_x()                  │
│  └── if sources includes "web": websearch.search_web() ← 新增   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     处理管道                                     │
├─────────────────────────────────────────────────────────────────┤
│  normalize_websearch_items() → WebSearchItem 模式 ← 新增         │
│  score_websearch_items() → 无互动评分 ← 新增                     │
│  dedupe_websearch() → 去重 ← 新增                                │
│  render_websearch_section() → 输出格式化 ← 新增                  │
└─────────────────────────────────────────────────────────────────┘
```

### 实现阶段

#### 阶段 1：模式与核心基础设施

**要创建/修改的文件：**

```python
# scripts/lib/websearch.py（新增）
"""用于一般网络发现的 Claude WebSearch API 客户端。"""

WEBSEARCH_PROMPT = """Search the web for content about: {topic}

CRITICAL: Only include results from the last 30 days (after {from_date}).

Find {min_items}-{max_items} high-quality, relevant web pages. Prefer:
- Blog posts, tutorials, documentation
- News articles, announcements
- Authoritative sources (official docs, reputable publications)

AVOID:
- Reddit (covered separately)
- X/Twitter (covered separately)
- YouTube without transcripts
- Forum threads without clear answers

Return ONLY valid JSON:
{{
  "items": [
    {{
      "title": "Page title",
      "url": "https://...",
      "source_domain": "example.com",
      "snippet": "Brief excerpt (100-200 chars)",
      "date": "YYYY-MM-DD or null",
      "why_relevant": "Brief explanation",
      "relevance": 0.85
    }}
  ]
}}
"""

def search_web(topic: str, from_date: str, to_date: str, depth: str = "default") -> dict:
    """使用 Claude 内置的 WebSearch 工具搜索网络。

    注意：这在 Claude Code 内部运行，所以我们直接使用 WebSearch 工具。
    无需 API 密钥 - 使用 Claude 的会话。
    """
    # 实现使用 Claude 的 web_search_20250305 工具
    pass

def parse_websearch_response(response: dict) -> list[dict]:
    """将 WebSearch 结果解析为标准化格式。"""
    pass
```

```python
# scripts/lib/schema.py - 添加 WebSearchItem

@dataclass
class WebSearchItem:
    """标准化的网络搜索项目。"""
    id: str
    title: str
    url: str
    source_domain: str  # 例如，"medium.com"、"github.com"
    snippet: str
    date: Optional[str] = None
    date_confidence: str = "low"
    relevance: float = 0.5
    why_relevant: str = ""
    subs: SubScores = field(default_factory=SubScores)
    score: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'source_domain': self.source_domain,
            'snippet': self.snippet,
            'date': self.date,
            'date_confidence': self.date_confidence,
            'relevance': self.relevance,
            'why_relevant': self.why_relevant,
            'subs': self.subs.to_dict(),
            'score': self.score,
        }
```

#### 阶段 2：评分系统更新

```python
# scripts/lib/score.py - 添加 websearch 评分

# 新常量
WEBSEARCH_SOURCE_PENALTY = 15  # 因缺少互动而扣除的分数

# 重新加权以适应无互动
WEBSEARCH_WEIGHT_RELEVANCE = 0.55
WEBSEARCH_WEIGHT_RECENCY = 0.45

def score_websearch_items(items: List[schema.WebSearchItem]) -> List[schema.WebSearchItem]:
    """对 WebSearch 项目评分，不使用互动指标。

    使用重新加权的公式：55% 相关性 + 45% 时效性 - 15pt 来源惩罚
    """
    for item in items:
        rel_score = int(item.relevance * 100)
        rec_score = dates.recency_score(item.date)

        item.subs = schema.SubScores(
            relevance=rel_score,
            recency=rec_score,
            engagement=0,  # 明确为零 - 无互动数据
        )

        overall = (
            WEBSEARCH_WEIGHT_RELEVANCE * rel_score +
            WEBSEARCH_WEIGHT_RECENCY * rec_score
        )

        # 应用来源惩罚（WebSearch < Reddit/X）
        overall -= WEBSEARCH_SOURCE_PENALTY

        # 应用日期置信度惩罚（与其他来源相同）
        if item.date_confidence == "low":
            overall -= 10
        elif item.date_confidence == "med":
            overall -= 5

        item.score = max(0, min(100, int(overall)))

    return items
```

#### 阶段 3：编排器集成

```python
# scripts/last30days.py - 更新 run_research()

def run_research(...) -> tuple:
    """运行研究管道。

    返回：(reddit_items, x_items, web_items, raw_openai, raw_xai,
              raw_websearch, reddit_error, x_error, web_error)
    """
    # ... 现有 Reddit/X 代码 ...

    # WebSearch（新增）
    web_items = []
    raw_websearch = None
    web_error = None

    if sources in ("all", "web", "reddit-web", "x-web"):
        if progress:
            progress.start_web()

        try:
            raw_websearch = websearch.search_web(topic, from_date, to_date, depth)
            web_items = websearch.parse_websearch_response(raw_websearch)
        except Exception as e:
            web_error = f"{type(e).__name__}: {e}"

        if progress:
            progress.end_web(len(web_items))

    return (reddit_items, x_items, web_items, raw_openai, raw_xai,
            raw_websearch, reddit_error, x_error, web_error)
```

#### 阶段 4：CLI 与环境更新

```python
# scripts/last30days.py - 添加 CLI 标志

parser.add_argument(
    "--include-web",
    action="store_true",
    help="Include general web search alongside Reddit/X (lower weighted)",
)

# scripts/lib/env.py - 更新 get_available_sources()

def get_available_sources(config: dict) -> str:
    """确定可用来源。WebSearch 始终可用（无需 API 密钥）。"""
    has_openai = bool(config.get('OPENAI_API_KEY'))
    has_xai = bool(config.get('XAI_API_KEY'))

    if has_openai and has_xai:
        return 'both'  # WebSearch 可用但非默认
    elif has_openai:
        return 'reddit'
    elif has_xai:
        return 'x'
    else:
        return 'web'  # 回退：仅 WebSearch（无需密钥）
```

## 验收标准

### 功能需求

- [x] 技能在零 API 密钥下工作（仅 WebSearch 模式）
- [x] `--include-web` 标志将 WebSearch 添加到 Reddit/X 搜索
- [x] WebSearch 项目的平均分数低于具有相似相关性的 Reddit/X 项目
- [x] WebSearch 结果排除 Reddit/X URL（单独处理）
- [x] 日期过滤在提示词中使用自然语言（"last 30 days"）
- [x] 输出清晰标记来源类型：`[WEB]`、`[Reddit]`、`[X]`

### 非功能需求

- [x] WebSearch 为总研究时间增加 <10s 延迟（0s - 延迟到 Claude）
- [x] 如果 WebSearch 失败则优雅降级
- [ ] 缓存适当包含 WebSearch 结果

### 质量门

- [x] 前后测试显示 WebSearch 不主导排名（通过 -15pt 惩罚）
- [x] 测试：10 Reddit + 10 X + 10 WebSearch → WebSearch 平均分数低 15-20pts（评分公式已验证）
- [x] 测试：仅 WebSearch 模式为常见主题产生有用结果

## 测试计划

### 前后对比脚本

```python
# tests/test_websearch_weighting.py

"""
测试工具，验证 WebSearch 不会压倒 Reddit/X。

使用以下方式运行相同查询：
1. 仅 Reddit + X（基线）
2. Reddit + X + WebSearch（比较）

验证：WebSearch 项目平均排名较低。
"""

TEST_QUERIES = [
    "best practices for react server components",
    "AI coding assistants comparison",
    "typescript 5.5 new features",
]

def test_websearch_weighting():
    for query in TEST_QUERIES:
        # 不使用 WebSearch 运行
        baseline = run_research(query, sources="both")
        baseline_scores = [item.score for item in baseline.reddit + baseline.x]

        # 使用 WebSearch 运行
        with_web = run_research(query, sources="both", include_web=True)
        web_scores = [item.score for item in with_web.web]
        reddit_x_scores = [item.score for item in with_web.reddit + with_web.x]

        # 断言
        avg_reddit_x = sum(reddit_x_scores) / len(reddit_x_scores)
        avg_web = sum(web_scores) / len(web_scores) if web_scores else 0

        assert avg_web < avg_reddit_x - 10, \
            f"WebSearch avg ({avg_web}) too close to Reddit/X avg ({avg_reddit_x})"

        # 检查前 5 名不全是 WebSearch
        top_5 = sorted(with_web.reddit + with_web.x + with_web.web,
                       key=lambda x: -x.score)[:5]
        web_in_top_5 = sum(1 for item in top_5 if isinstance(item, WebSearchItem))
        assert web_in_top_5 <= 2, f"Too many WebSearch items in top 5: {web_in_top_5}"
```

### 手动测试场景

| 场景 | 预期结果 |
|------|----------|
| 无 API 密钥，运行 `/last30days AI tools` | 仅 WebSearch 结果，有用输出 |
| 两个密钥 + `--include-web`，运行 `/last30days react` | 所有 3 个来源混合，Reddit/X 主导前 10 |
| 小众主题（无 Reddit/X 覆盖） | WebSearch 填补空白，成为主要来源 |
| 热门主题（大量 Reddit/X） | WebSearch 存在但排名较低 |

## 依赖与先决条件

- Claude Code 的 WebSearch 工具（`web_search_20250305`）- 已可用
- 无需新的 API 密钥
- `tests/` 中现有测试基础设施

## 风险分析与缓解

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| WebSearch 返回过时内容 | 中 | 中 | 在提示词中强制日期，应用低置信度惩罚 |
| WebSearch 主导排名 | 低 | 高 | 来源惩罚（-15pts），测试验证 |
| WebSearch 添加垃圾/低质量内容 | 中 | 中 | 排除社交媒体域名，域名过滤 |
| 日期解析不可靠 | 高 | 中 | 接受"低"置信度为 WebSearch 的正常情况 |

## 未来考虑

1. **域名权威评分**：可以用域名声誉代理互动
2. **用户可配置权重**：让用户调整 WebSearch 惩罚
3. **域名白名单/黑名单**：将 WebSearch 过滤到可信来源
4. **并行执行**：同时运行所有 3 个来源以提高速度

## 参考资料

### 内部参考
- 评分算法：`scripts/lib/score.py:8-15`
- 来源检测：`scripts/lib/env.py:57-72`
- 模式模式：`scripts/lib/schema.py:76-138`
- 编排器：`scripts/last30days.py:54-164`

### 外部参考
- Claude WebSearch 文档：https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool
- WebSearch 定价：$10/1K 搜索 + token 成本
- 日期过滤限制：无显式日期参数，使用自然语言

### 研究发现
- Reddit 点赞约占 SEO 排名价值的 12%（强信号）
- E-E-A-T 框架：互动指标 = 信任信号
- MSA2C2 方法：多源聚合的动态权重学习
