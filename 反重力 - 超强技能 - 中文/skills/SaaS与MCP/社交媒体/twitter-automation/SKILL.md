---
name: twitter-automation
description: "通过 Rube MCP (Composio) 自动化 Twitter/X 操作：发帖、搜索、用户管理、书签、列表、媒体。始终先搜索工具以获取当前 schema。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Twitter/X 自动化

通过 Composio 的 Twitter 工具包（经 Rube MCP）自动化 Twitter/X 操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS`（toolkit 为 `twitter`）建立活跃的 Twitter 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 以获取当前工具 schema

## 配置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API Key ——添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`（toolkit 为 `twitter`）
3. 若连接状态非 ACTIVE，按返回的授权链接完成 Twitter OAuth
4. 确认连接状态为 ACTIVE 后再执行任何工作流

## 核心工作流

### 1. 创建和管理帖子

**适用场景**：用户要创建、删除或查找推文/帖子

**工具调用顺序**：
1. `TWITTER_USER_LOOKUP_ME` - 获取已认证用户信息 [前置]
2. `TWITTER_UPLOAD_MEDIA` / `TWITTER_UPLOAD_LARGE_MEDIA` - 上传媒体 [可选]
3. `TWITTER_CREATION_OF_A_POST` - 创建新帖子 [必需]
4. `TWITTER_POST_LOOKUP_BY_POST_ID` - 查找特定帖子 [可选]
5. `TWITTER_POST_DELETE_BY_POST_ID` - 删除帖子 [可选]

**关键参数**：
- `text`：帖子文本内容（最多 280 个加权字符）
- `media__media_ids`：媒体 ID 字符串数组，用于附件
- `reply__in_reply_to_tweet_id`：要回复的推文 ID
- `quote_tweet_id`：要引用的推文 ID
- `id`：用于查找/删除的帖子 ID

**注意事项**：
- 帖子文本限制为 280 个加权字符；部分 Unicode 字符计为多个
- 发帖操作不具备幂等性；超时重试会产生重复帖子
- 媒体 ID 必须为数字字符串，不能是整数
- UPLOAD_LARGE_MEDIA 用于视频/GIF；UPLOAD_MEDIA 用于图片
- 始终先调用 USER_LOOKUP_ME 获取已认证用户的 ID

### 2. 搜索帖子

**适用场景**：用户要查找符合特定条件的推文

**工具调用顺序**：
1. `TWITTER_RECENT_SEARCH` - 搜索最近 7 天的推文 [必需]
2. `TWITTER_FULL_ARCHIVE_SEARCH` - 搜索完整归档（需学术访问权限）[可选]
3. `TWITTER_RECENT_SEARCH_COUNTS` - 获取匹配查询的推文计数 [可选]

**关键参数**：
- `query`：使用 Twitter 搜索运算符的查询语句
- `max_results`：每页结果数（10-100）
- `next_token`：分页令牌
- `start_time`/`end_time`：ISO 8601 时间范围
- `tweet__fields`：要返回的字段，逗号分隔
- `expansions`：要展开的关联对象

**注意事项**：
- RECENT_SEARCH 仅覆盖最近 7 天；更早的推文需用 FULL_ARCHIVE_SEARCH
- FULL_ARCHIVE_SEARCH 需要学术研究或企业级访问权限
- 查询运算符：`from:username`、`to:username`、`is:retweet`、`has:media`、`-is:retweet`
- 无结果时返回 `meta.result_count: 0`，无 `data` 字段
- 速率限制因端点和访问级别而异；检查响应头

### 3. 查找用户

**适用场景**：用户要查找或查看 Twitter 用户资料

**工具调用顺序**：
1. `TWITTER_USER_LOOKUP_ME` - 获取已认证用户 [可选]
2. `TWITTER_USER_LOOKUP_BY_USERNAME` - 按用户名查找 [可选]
3. `TWITTER_USER_LOOKUP_BY_ID` - 按用户 ID 查找 [可选]
4. `TWITTER_USER_LOOKUP_BY_IDS` - 批量查找多个用户 [可选]

**关键参数**：
- `username`：Twitter 用户名（不含 @ 前缀）
- `id`：数字用户 ID 字符串
- `ids`：逗号分隔的用户 ID，用于批量查找
- `user__fields`：要返回的字段（description、public_metrics 等）

**注意事项**：
- 用户名不区分大小写，但不能包含 @ 前缀
- 用户 ID 为数字字符串，不是整数
- 被封禁或已删除的账户会返回错误，而非空结果
- LOOKUP_BY_IDS 每次请求最多接受 100 个 ID

### 4. 管理书签

**适用场景**：用户要保存、查看或移除书签推文

**工具调用顺序**：
1. `TWITTER_USER_LOOKUP_ME` - 获取已认证用户 ID [前置]
2. `TWITTER_BOOKMARKS_BY_USER` - 列出已收藏的帖子 [必需]
3. `TWITTER_ADD_POST_TO_BOOKMARKS` - 收藏帖子 [可选]
4. `TWITTER_REMOVE_A_BOOKMARKED_POST` - 移除收藏 [可选]

**关键参数**：
- `id`：用户 ID（来自 USER_LOOKUP_ME），用于列出书签
- `tweet_id`：要收藏或取消收藏的推文 ID
- `max_results`：每页结果数
- `pagination_token`：下一页的分页令牌

**注意事项**：
- 书签操作需要已认证用户的 ID，而非用户名
- 书签为私有数据；只有已认证用户本人可见
- 分页使用 `pagination_token`，而非 `next_token`

### 5. 管理列表

**适用场景**：用户要查看或管理 Twitter 列表

**工具调用顺序**：
1. `TWITTER_USER_LOOKUP_ME` - 获取已认证用户 ID [前置]
2. `TWITTER_GET_A_USER_S_OWNED_LISTS` - 列出拥有的列表 [可选]
3. `TWITTER_GET_A_USER_S_LIST_MEMBERSHIPS` - 列出加入的列表 [可选]
4. `TWITTER_GET_A_USER_S_PINNED_LISTS` - 获取置顶列表 [可选]
5. `TWITTER_GET_USER_S_FOLLOWED_LISTS` - 获取关注的列表 [可选]
6. `TWITTER_LIST_LOOKUP_BY_LIST_ID` - 获取列表详情 [可选]

**关键参数**：
- `id`：用户 ID，用于列出拥有的/加入的/关注的列表
- `list_id`：列表 ID，用于查询特定列表
- `max_results`：每页结果数（1-100）

**注意事项**：
- 列表 ID 和用户 ID 均为数字字符串
- 列表端点需要用户的数字 ID，而非用户名

### 6. 帖子互动

**适用场景**：用户要点赞、取消点赞或查看已点赞的帖子

**工具调用顺序**：
1. `TWITTER_USER_LOOKUP_ME` - 获取已认证用户 ID [前置]
2. `TWITTER_RETURNS_POST_OBJECTS_LIKED_BY_THE_PROVIDED_USER_ID` - 获取已点赞帖子 [可选]
3. `TWITTER_UNLIKE_POST` - 取消点赞 [可选]

**关键参数**：
- `id`：用户 ID，用于列出已点赞帖子
- `tweet_id`：要取消点赞的推文 ID

**注意事项**：
- 点赞/取消点赞端点需要来自 USER_LOOKUP_ME 的用户 ID
- 对于点赞数量较多的用户，已点赞帖子的分页可能较慢

## 常用模式

### 搜索查询语法

**运算符**：
- `from:username` - 该用户发布的帖子
- `to:username` - 回复该用户的帖子
- `@username` - 提及该用户
- `#hashtag` - 包含该话题标签
- `"exact phrase"` - 精确匹配
- `has:media` - 包含媒体
- `has:links` - 包含链接
- `is:retweet` / `-is:retweet` - 包含/排除转推
- `is:reply` / `-is:reply` - 包含/排除回复
- `lang:en` - 语言过滤

**组合运算**：
- 空格表示 AND
- `OR` 表示或
- `-` 前缀表示 NOT
- 括号用于分组

### 媒体上传流程

```
1. Upload media with TWITTER_UPLOAD_MEDIA (images) or TWITTER_UPLOAD_LARGE_MEDIA (video/GIF)
2. Get media_id from response
3. Pass media_id as string in media__media_ids array to TWITTER_CREATION_OF_A_POST
```

## 已知问题

**字符限制**：
- 标准帖子：280 个加权字符
- 部分 Unicode 字符计为多个
- URL 会被缩短并按固定长度计算（23 个字符）

**速率限制**：
- 不同访问层级差异显著（Free、Basic、Pro、Enterprise）
- Free 层级：限制较严（如每月 1,500 条帖子）
- 检查响应头中的 `x-rate-limit-remaining`

**幂等性**：
- 发帖操作不具备幂等性；重试会产生重复帖子
- 自动发帖场景需实现去重逻辑

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 创建帖子 | TWITTER_CREATION_OF_A_POST | text |
| 删除帖子 | TWITTER_POST_DELETE_BY_POST_ID | id |
| 查找帖子 | TWITTER_POST_LOOKUP_BY_POST_ID | id |
| 近期搜索 | TWITTER_RECENT_SEARCH | query |
| 归档搜索 | TWITTER_FULL_ARCHIVE_SEARCH | query |
| 搜索计数 | TWITTER_RECENT_SEARCH_COUNTS | query |
| 我的资料 | TWITTER_USER_LOOKUP_ME | (无) |
| 按名查用户 | TWITTER_USER_LOOKUP_BY_USERNAME | username |
| 按 ID 查用户 | TWITTER_USER_LOOKUP_BY_ID | id |
| 批量查用户 | TWITTER_USER_LOOKUP_BY_IDS | ids |
| 上传媒体 | TWITTER_UPLOAD_MEDIA | media |
| 上传视频 | TWITTER_UPLOAD_LARGE_MEDIA | media |
| 列出书签 | TWITTER_BOOKMARKS_BY_USER | id |
| 添加书签 | TWITTER_ADD_POST_TO_BOOKMARKS | tweet_id |
| 移除书签 | TWITTER_REMOVE_A_BOOKMARKED_POST | tweet_id |
| 取消点赞 | TWITTER_UNLIKE_POST | tweet_id |
| 已点赞帖子 | TWITTER_RETURNS_POST_OBJECTS_LIKED_BY_THE_PROVIDED_USER_ID | id |
| 拥有的列表 | TWITTER_GET_A_USER_S_OWNED_LISTS | id |
| 加入的列表 | TWITTER_GET_A_USER_S_LIST_MEMBERSHIPS | id |
| 置顶列表 | TWITTER_GET_A_USER_S_PINNED_LISTS | id |
| 关注的列表 | TWITTER_GET_USER_S_FOLLOWED_LISTS | id |
| 列表详情 | TWITTER_LIST_LOOKUP_BY_LIST_ID | list_id |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为替代特定环境的验证、测试或专家审查。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
