# 修复：强制执行严格的 30 天日期过滤

## 概述

`/last30days` 技能返回超过 30 天的内容，违反了其核心承诺。分析显示：
- **Reddit**：仅 40% 的结果在 30 天内（15 个中有 9 个更旧，有些来自 2022 年！）
- **X**：100% 在 30 天内（工作正常）
- **WebSearch**：90% 日期未知（无法验证新鲜度）

## 问题陈述

技能名称是"last30days" - 用户期望仅过去 30 天的内容。目前：

1. **Reddit 搜索提示词**说"优先选择最近的帖子，但如果最近帖子稀缺，则包含较旧的相关帖子" - 这太宽松了
2. **X 搜索提示词**明确包含 `from_date` 和 `to_date` - 这就是它有效的原因
3. **WebSearch** 返回没有发布日期的页面 - 我们无法验证它们是最近的
4. **评分惩罚**（低日期置信度 -10）不能阻止旧内容出现

## 提议的解决方案

### 策略："硬过滤，而非软惩罚"

与其惩罚旧内容，不如**完全排除它**。如果不是过去 30 天的，就不应该出现。

| 来源 | 当前行为 | 新行为 |
|------|----------|--------|
| Reddit | 弱"优先最近" | 明确日期范围 + 硬过滤 |
| X | 明确日期范围（有效） | 无需更改 |
| WebSearch | 无日期感知 | 需要最近标记或排除 |

## 技术方法

### 阶段 1：修复 Reddit 日期过滤

**文件：`scripts/lib/openai_reddit.py`**

当前提示词（第 33 行）：
```
Find {min_items}-{max_items} relevant Reddit discussion threads.
Prefer recent threads, but include older relevant ones if recent ones are scarce.
```

新提示词：
```
Find {min_items}-{max_items} relevant Reddit discussion threads from {from_date} to {to_date}.

CRITICAL: Only include threads posted within the last 30 days (after {from_date}).
Do NOT include threads older than {from_date}, even if they seem relevant.
If you cannot find enough recent threads, return fewer results rather than older ones.
```

**需要的更改：**
1. 向 `search_reddit()` 函数添加 `from_date` 和 `to_date` 参数
2. 像 X 那样将日期注入 `REDDIT_SEARCH_PROMPT`
3. 更新 `last30days.py` 中的调用者以传递日期

### 阶段 2：添加硬日期过滤（后处理）

**文件：`scripts/lib/normalize.py`**

添加一个过滤步骤，删除 `from_date` 之前的日期项目：

```python
def filter_by_date_range(
    items: List[Union[RedditItem, XItem, WebSearchItem]],
    from_date: str,
    to_date: str,
    require_date: bool = False,
) -> List:
    """硬过滤：删除日期范围之外的项目。

    参数：
        items: 要过滤的项目列表
        from_date: 开始日期（YYYY-MM-DD）
        to_date: 结束日期（YYYY-MM-DD）
        require_date: 如果为 True，也删除没有日期的项目

    返回：
        仅包含范围内项目的过滤列表
    """
    result = []
    for item in items:
        if item.date is None:
            if not require_date:
                result.append(item)  # 保留未知日期（带惩罚）
            continue

        # 硬过滤：如果日期在 from_date 之前，排除
        if item.date < from_date:
            continue  # 删除 - 太旧

        if item.date > to_date:
            continue  # 删除 - 未来日期（可能是解析错误）

        result.append(item)

    return result
```

### 阶段 3：WebSearch 日期智能

WebSearch 可以找到最近的内容 - Medium 帖子有日期，GitHub 有提交时间戳，新闻网站有发布日期。我们应该**提取并优先考虑**这些信号。

**策略："日期侦探"**

1. **从 URL 提取日期**：许多网站在 URL 中嵌入日期
   - Medium：`medium.com/@author/title-abc123`（无日期）vs 新闻网站
   - GitHub：查找提交日期、片段中的发布日期
   - 新闻：`/2026/01/24/article-title`
   - 博客：`/blog/2026/01/title`

2. **从片段提取日期**：查找日期标记
   - "January 24, 2026"、"Jan 2026"、"yesterday"、"this week"
   - "Published:"、"Posted:"、"Updated:"
   - 相对标记："2 days ago"、"last week"

3. **优先考虑有可验证日期的结果**：
   - 有最近日期的结果（30 天内）：全分
   - 有旧日期的结果：排除
   - 无日期信号的结果：重惩罚（-20）但保留作为补充

**文件：`scripts/lib/websearch.py`**

添加日期提取函数：

```python
import re
from datetime import datetime, timedelta

# 日期提取模式
URL_DATE_PATTERNS = [
    r'/(\d{4})/(\d{2})/(\d{2})/',  # /2026/01/24/
    r'/(\d{4})-(\d{2})-(\d{2})/',  # /2026-01-24/
    r'/(\d{4})(\d{2})(\d{2})/',    # /20260124/
]

SNIPPET_DATE_PATTERNS = [
    r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (\d{1,2}),? (\d{4})',
    r'(\d{1,2}) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (\d{4})',
    r'(\d{4})-(\d{2})-(\d{2})',
    r'Published:?\s*(\d{4}-\d{2}-\d{2})',
    r'(\d{1,2}) (days?|hours?|minutes?) ago',  # 相对日期
]

def extract_date_from_url(url: str) -> Optional[str]:
    """尝试从 URL 路径提取日期。"""
    for pattern in URL_DATE_PATTERNS:
        match = re.search(pattern, url)
        if match:
            # 解析并返回 YYYY-MM-DD 格式
            ...
    return None

def extract_date_from_snippet(snippet: str) -> Optional[str]:
    """尝试从文本片段提取日期。"""
    for pattern in SNIPPET_DATE_PATTERNS:
        match = re.search(pattern, snippet, re.IGNORECASE)
        if match:
            # 解析并返回 YYYY-MM-DD 格式
            ...
    return None

def extract_date_signals(url: str, snippet: str, title: str) -> tuple[Optional[str], str]:
    """从任何可用信号提取日期。

    返回：(date_string, confidence)
    - 来自 URL 的日期：'high' 置信度
    - 来自片段的日期：'med' 置信度
    - 未找到日期：None, 'low' 置信度
    """
    # 首先尝试 URL（最可靠）
    url_date = extract_date_from_url(url)
    if url_date:
        return url_date, 'high'

    # 尝试片段
    snippet_date = extract_date_from_snippet(snippet)
    if snippet_date:
        return snippet_date, 'med'

    # 尝试标题
    title_date = extract_date_from_snippet(title)
    if title_date:
        return title_date, 'med'

    return None, 'low'
```

**更新 WebSearch 解析以使用日期提取：**

```python
def parse_websearch_results(results, topic, from_date, to_date):
    items = []
    for result in results:
        url = result.get('url', '')
        snippet = result.get('snippet', '')
        title = result.get('title', '')

        # 提取日期信号
        extracted_date, confidence = extract_date_signals(url, snippet, title)

        # 硬过滤：如果我们找到日期且太旧，跳过
        if extracted_date and extracted_date < from_date:
            continue  # 删除 - 已验证的旧内容

        item = {
            'date': extracted_date,
            'date_confidence': confidence,
            ...
        }
        items.append(item)

    return items
```

**文件：`scripts/lib/score.py`**

更新 WebSearch 评分以奖励日期验证的结果：

```python
# WebSearch 日期置信度调整
WEBSEARCH_NO_DATE_PENALTY = 20  # 无日期的重惩罚（原为 10）
WEBSEARCH_VERIFIED_BONUS = 10   # URL 验证的最近日期的奖励

def score_websearch_items(items):
    for item in items:
        ...
        # 日期置信度调整
        if item.date_confidence == 'high':
            overall += WEBSEARCH_VERIFIED_BONUS  # 奖励验证日期
        elif item.date_confidence == 'low':
            overall -= WEBSEARCH_NO_DATE_PENALTY  # 未知的重惩罚
        ...
```

**结果**：有可验证最近日期的 WebSearch 结果排名良好。无日期的结果受到重惩罚但仍作为补充上下文出现。已验证的旧内容完全被排除。

### 阶段 4：更新统计显示

仅在"过去 30 天"声明中计算 Reddit 和 X。WebSearch 应清晰标记为补充。

## 验收标准

### 功能需求

- [x] Reddit 搜索提示词包含明确的 `from_date` 和 `to_date`
- [x] `from_date` 之前日期的项目被排除，而非仅惩罚
- [x] X 搜索继续工作（无回归）
- [x] WebSearch 从 URL 提取日期（例如，`/2026/01/24/`）
- [x] WebSearch 从片段提取日期（例如，"January 24, 2026"）
- [x] 有验证最近日期的 WebSearch 获得 +10 奖励
- [x] 无日期信号的 WebSearch 获得 -20 惩罚（但仍出现）
- [x] 有验证旧日期的 WebSearch 被排除

### 非功能需求

- [ ] API 延迟无增加
- [ ] 当最近结果很少时的优雅处理（返回更少，而非更旧）
- [ ] 当结果因严格过滤而受限时的清晰用户消息

### 质量门

- [ ] 测试：Reddit 搜索返回 0% 超过 30 天的结果
- [ ] 测试：X 搜索继续返回 100% 最近结果
- [ ] 测试：WebSearch 在输出中清晰区分
- [ ] 测试：边缘情况 - 无最近内容的主题显示有帮助的消息

## 实现顺序

1. **阶段 1**：修复 Reddit 提示词（影响最大，简单更改）
2. **阶段 2**：在 normalize.py 中添加硬日期过滤（安全网）
3. **阶段 3**：添加 WebSearch 日期提取（URL + 片段解析）
4. **阶段 4**：更新 WebSearch 评分（验证奖励，未知重惩罚）
5. **阶段 5**：更新输出显示以显示日期置信度

## 测试计划

### 前后测试

修复前后运行相同查询：
```
/last30days remotion launch videos
```

**预期修复前：**
- Reddit：40% 在 30 天内

**预期修复后：**
- Reddit：100% 在 30 天内（如果最近内容不足则结果更少）

### 边缘情况测试

| 场景 | 预期行为 |
|------|----------|
| 无最近内容的主题 | 返回 0 结果 + 有帮助的消息 |
| 有 5 个最近结果的主题 | 返回 5 个结果（不用旧的填充） |
| 混合旧/新结果 | 仅返回新的 |

### WebSearch 日期提取测试

| URL/片段 | 预期日期 | 置信度 |
|----------|----------|--------|
| `medium.com/blog/2026/01/15/title` | 2026-01-15 | high |
| `github.com/repo` + "Released Jan 20, 2026" | 2026-01-20 | med |
| `docs.example.com/guide`（无日期信号） | None | low |
| `news.site.com/2024/05/old-article` | 2024-05-XX | 排除（太旧） |
| 片段："Updated 3 days ago" | 计算 | med |

## 风险分析

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| 小众主题结果更少 | 高 | 中 | 在输出中解释原因 |
| 用户对减少结果的困惑 | 中 | 低 | 清晰的消息传递 |
| 日期解析错误排除有效内容 | 低 | 中 | 保留未知日期的项目，仅清晰标记 |

## 参考资料

### 内部参考
- Reddit 搜索：`scripts/lib/openai_reddit.py:25-63`
- X 搜索（工作示例）：`scripts/lib/xai_x.py:26-55`
- 日期置信度：`scripts/lib/dates.py:62-90`
- 评分惩罚：`scripts/lib/score.py:149-153`
- 标准化：`scripts/lib/normalize.py:49,99`

### 外部参考
- OpenAI Responses API 缺乏原生日期过滤
- 必须依赖提示词工程 + 后处理
