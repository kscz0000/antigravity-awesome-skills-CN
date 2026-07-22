---
name: reddit-automation
description: "通过 Rube MCP (Composio) 自动化 Reddit 任务：搜索 subreddit、创建帖子、管理评论、浏览热门内容。务必先搜索工具获取最新 schema。"
risk: critical
source: community
date_added: "2026-02-27"
---

# Reddit Automation via Rube MCP

通过 Composio 的 Reddit 工具包和 Rube MCP 自动化 Reddit 操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 Reddit 连接，toolkit 为 `reddit`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 响应正常，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `reddit`
3. 若连接状态非 ACTIVE，按返回的授权链接完成 Reddit OAuth
4. 运行工作流前确认连接状态显示 ACTIVE

## 核心工作流

### 1. 搜索 Reddit

**使用场景**：用户想在各 subreddit 中搜索帖子

**工具调用顺序**：
1. `REDDIT_SEARCH_ACROSS_SUBREDDITS` - 搜索匹配查询的帖子 [必需]

**关键参数**：
- `query`：搜索关键词
- `subreddit`：限定在特定 subreddit 内搜索（可选）
- `sort`：排序方式，可选 'relevance'、'hot'、'top'、'new'、'comments'
- `time_filter`：时间范围，可选 'hour'、'day'、'week'、'month'、'year'、'all'
- `limit`：返回结果数量

**注意事项**：
- 由于索引延迟，搜索结果可能不包含最新帖子
- `time_filter` 参数仅在特定排序选项下生效
- 结果分页显示；使用 after/before token 获取后续页面
- NSFW 内容可能根据账户设置被过滤

### 2. 创建帖子

**使用场景**：用户想向 subreddit 提交新帖子

**工具调用顺序**：
1. `REDDIT_LIST_SUBREDDIT_POST_FLAIRS` - 获取可用的帖子标签 [可选]
2. `REDDIT_CREATE_REDDIT_POST` - 提交帖子 [必需]

**关键参数**：
- `subreddit`：目标 subreddit 名称（不含 'r/' 前缀）
- `title`：帖子标题
- `text`：帖子正文（用于文本帖子）
- `url`：链接 URL（用于链接帖子）
- `flair_id`：从 subreddit 标签列表中获取的标签 ID

**注意事项**：
- 部分 subreddit 要求必须选择标签；先调用 LIST_SUBREDDIT_POST_FLAIRS
- 各 subreddit 发帖规则差异较大；可能有 karma/账号年龄限制
- text 和 url 互斥；帖子只能是文本或链接其中之一
- 存在速率限制；避免快速连续发帖
- subreddit 名称不应包含 'r/' 前缀

### 3. 管理评论

**使用场景**：用户想对帖子发表评论或管理已有评论

**工具调用顺序**：
1. `REDDIT_RETRIEVE_POST_COMMENTS` - 获取帖子下的评论 [可选]
2. `REDDIT_POST_REDDIT_COMMENT` - 给帖子添加评论或回复评论 [必需]
3. `REDDIT_EDIT_REDDIT_COMMENT_OR_POST` - 编辑已有评论 [可选]
4. `REDDIT_DELETE_REDDIT_COMMENT` - 删除评论 [可选]

**关键参数**：
- `post_id`：帖子 ID（用于检索或评论）
- `parent_id`：父级全名（如帖子为 't3_abc123'，评论为 't1_xyz789'）
- `body`：评论文本内容
- `thing_id`：待编辑或删除项的全名

**注意事项**：
- Reddit 使用 'fullname' 格式：评论以 't1_' 为前缀，帖子以 't3_' 为前缀
- 编辑会替换整个评论内容；需包含所有想要保留的内容
- 已删除评论显示为 '[deleted]'，但树状结构保留
- 部分 subreddit 可能有评论层级限制

### 4. 浏览 Subreddit 内容

**使用场景**：用户想查看 subreddit 的热门或趋势内容

**工具调用顺序**：
1. `REDDIT_GET_R_TOP` - 获取 subreddit 的热门帖子 [必需]
2. `REDDIT_GET` - 从 subreddit 端点获取帖子 [替代方案]
3. `REDDIT_RETRIEVE_REDDIT_POST` - 获取特定帖子的完整详情 [可选]

**关键参数**：
- `subreddit`：Subreddit 名称
- `time_filter`：热门帖子的时间范围，可选 'hour'、'day'、'week'、'month'、'year'、'all'
- `limit`：获取的帖子数量
- `post_id`：特定帖子 ID，用于获取完整详情

**注意事项**：
- time_filter='all' 返回历史全部热门内容
- 帖子详情包含正文，但评论需单独调用获取
- 部分帖子可能因 subreddit 规则被移除或隐藏
- 除非在账户级别过滤，否则 NSFW 帖子会包含在结果中

### 5. 管理帖子

**使用场景**：用户想编辑或删除自己的帖子

**工具调用顺序**：
1. `REDDIT_EDIT_REDDIT_COMMENT_OR_POST` - 编辑帖子文本内容 [可选]
2. `REDDIT_DELETE_REDDIT_POST` - 删除帖子 [可选]
3. `REDDIT_GET_USER_FLAIR` - 获取用户在 subreddit 中的标签 [可选]

**关键参数**：
- `thing_id`：帖子全名（如 't3_abc123'）
- `body`：新的文本内容（用于编辑）
- `subreddit`：Subreddit 名称（用于获取标签）

**注意事项**：
- 只有文本帖子可以编辑正文；链接帖子无法修改
- 帖子标题提交后不可编辑
- 删除不可恢复；已删除帖子显示为 '[deleted]'
- 用户标签按 subreddit 区分，可能受限

## 常用模式

### Reddit Fullname 格式

**前缀说明**：
```
t1_ = Comment (e.g., 't1_abc123')
t2_ = Account (e.g., 't2_xyz789')
t3_ = Post/Link (e.g., 't3_def456')
t4_ = Message
t5_ = Subreddit
```

**使用方法**：
```
1. Retrieve a post to get its fullname (t3_XXXXX)
2. Use fullname as parent_id when commenting
3. Use fullname as thing_id when editing/deleting
```

### 分页

- Reddit 使用基于游标的分页，通过 'after' 和 'before' token 实现
- 设置 `limit` 指定每页条目数（最大 100）
- 检查响应中的 `after` token
- 后续请求中传入 `after` 值获取下一页

### 标签解析

```
1. Call REDDIT_LIST_SUBREDDIT_POST_FLAIRS with subreddit name
2. Find matching flair by text or category
3. Extract flair_id
4. Include flair_id when creating the post
```

## 已知陷阱

**速率限制**：
- Reddit 按账户和 OAuth 应用实施速率限制
- 新账户发帖限制约为每 10 分钟 1 条
- 评论限制类似但相对宽松
- 429 错误应触发指数退避

**内容规则**：
- 每个 subreddit 有自己的发帖规则和要求
- 部分 subreddit 为受限或私有
- Karma 要求可能阻止在某些 subreddit 发帖
- Auto-moderator 规则可能移除匹配特定模式的帖子

**ID 格式**：
- parent_id 和 thing_id 始终使用 fullname 格式（带前缀）
- 不带前缀的原始 ID 会导致 'Invalid ID' 错误
- 搜索结果中的帖子 ID 可能需要添加 't3_' 前缀

**文本格式**：
- Reddit 使用 Markdown 格式化帖子和评论
- 支持代码块、表格和标题
- 链接使用 `text` 格式
- 提及用户用 `u/username`，提及 subreddit 用 `r/subreddit`

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 搜索 Reddit | REDDIT_SEARCH_ACROSS_SUBREDDITS | query, subreddit, sort, time_filter |
| 创建帖子 | REDDIT_CREATE_REDDIT_POST | subreddit, title, text/url |
| 获取帖子评论 | REDDIT_RETRIEVE_POST_COMMENTS | post_id |
| 添加评论 | REDDIT_POST_REDDIT_COMMENT | parent_id, body |
| 编辑评论/帖子 | REDDIT_EDIT_REDDIT_COMMENT_OR_POST | thing_id, body |
| 删除评论 | REDDIT_DELETE_REDDIT_COMMENT | thing_id |
| 删除帖子 | REDDIT_DELETE_REDDIT_POST | thing_id |
| 获取热门帖子 | REDDIT_GET_R_TOP | subreddit, time_filter, limit |
| 浏览 subreddit | REDDIT_GET | subreddit |
| 获取帖子详情 | REDDIT_RETRIEVE_REDDIT_POST | post_id |
| 获取特定评论 | REDDIT_RETRIEVE_SPECIFIC_COMMENT | comment_id |
| 列出帖子标签 | REDDIT_LIST_SUBREDDIT_POST_FLAIRS | subreddit |
| 获取用户标签 | REDDIT_GET_USER_FLAIR | subreddit |

## 使用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，停下来请求澄清。