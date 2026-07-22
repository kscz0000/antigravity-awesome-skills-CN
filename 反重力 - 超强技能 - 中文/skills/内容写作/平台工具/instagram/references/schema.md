# SQLite 数据库架构 — instagram.db

位置：`C:\Users\renat\skills\instagram\data\instagram.db`
模式：WAL（预写日志），启用外键。

## ER 图

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   accounts      │      │     posts       │      │   templates     │
├─────────────────┤      ├─────────────────┤      ├─────────────────┤
│ id (PK)         │──┐   │ id (PK)         │   ┌──│ id (PK)         │
│ ig_user_id      │  │   │ account_id(FK)  │───┘  │ name (UNIQUE)   │
│ username        │  │   │ media_type      │      │ caption_tpl     │
│ account_type    │  │   │ media_url       │      │ hashtag_set     │
│ access_token    │  │   │ local_path      │      │ default_time    │
│ token_exp       │  │   │ caption         │      │ created_at      │
│ fb_page_id      │  │   │ hashtags        │      └─────────────────┘
│ app_id          │  │   │ template_id(FK) │
│ app_secret      │  │   │ status          │
│ is_active       │  │   │ scheduled_at    │
│ created_at      │  │   │ published_at    │
└─────────────────┘  │   │ ig_media_id     │
                     │   │ ig_container    │
                     │   │ permalink       │
                     │   │ error_msg       │
                     │   │ created_at      │
                     │   └─────────────────┘
                     │
                     │   ┌─────────────────┐
                     ├───│   comments      │
                     │   ├─────────────────┤
                     │   │ id (PK)         │
                     │   │ account_id(FK)  │
                     │   │ ig_comment_id   │
                     │   │ ig_media_id     │
                     │   │ username        │
                     │   │ text            │
                     │   │ timestamp       │
                     │   │ replied         │
                     │   │ reply_text      │
                     │   │ hidden          │
                     │   └─────────────────┘
                     │
                     │   ┌─────────────────┐
                     ├───│   insights      │
                     │   ├─────────────────┤
                     │   │ id (PK)         │
                     │   │ account_id(FK)  │
                     │   │ ig_media_id     │
                     │   │ metric_name     │
                     │   │ metric_value    │
                     │   │ period          │
                     │   │ fetched_at      │
                     │   │ raw_json        │
                     │   └─────────────────┘
                     │
                     │   ┌─────────────────────┐
                     ├───│   user_insights     │
                     │   ├─────────────────────┤
                     │   │ id (PK)             │
                     │   │ account_id (FK)     │
                     │   │ metric_name         │
                     │   │ metric_value        │
                     │   │ period              │
                     │   │ end_time            │
                     │   │ fetched_at          │
                     │   └─────────────────────┘
                     │
                     │   ┌─────────────────────┐
                     ├───│ hashtag_searches    │
                     │   ├─────────────────────┤
                     │   │ id (PK)             │
                     │   │ account_id (FK)     │
                     │   │ hashtag             │
                     │   │ ig_hashtag_id       │
                     │   │ searched_at         │
                     │   └─────────────────────┘
                     │
                     │   ┌─────────────────┐
                     └───│   action_log    │
                         ├─────────────────┤
                         │ id (PK)         │
                         │ account_id      │
                         │ action          │
                         │ params (JSON)   │
                         │ result (JSON)   │
                         │ confirmed       │
                         │ rate_remain     │
                         │ created_at      │
                         └─────────────────┘
```

## 详细表结构

### accounts
存储配置的 Instagram 账号。从一开始就支持多账号。

| 字段 | 类型 | 约束 | 描述 |
|-------|------|------------|-----------|
| id | INTEGER | PK | 自增 |
| ig_user_id | TEXT | UNIQUE NOT NULL | Graph API 中的 IG 用户 ID |
| username | TEXT | | @用户名 |
| account_type | TEXT | | BUSINESS, MEDIA_CREATOR |
| access_token | TEXT | NOT NULL | 长期令牌（60 天） |
| token_expires_at | TEXT | | ISO 8601 日期时间 |
| facebook_page_id | TEXT | | 关联的 Facebook 主页 ID |
| app_id | TEXT | | Meta App ID |
| app_secret | TEXT | | Meta App Secret |
| is_active | INTEGER | DEFAULT 1 | 活跃账号（1）或停用（0） |
| created_at | TEXT | DEFAULT now | 创建时间戳 |

### posts
带有状态机的内容管道。

| 字段 | 类型 | 约束 | 描述 |
|-------|------|------------|-----------|
| id | INTEGER | PK | 自增 |
| account_id | INTEGER | FK → accounts | 关联账号 |
| media_type | TEXT | | PHOTO, VIDEO, CAROUSEL, REEL, STORY |
| media_url | TEXT | | 公开 URL（Imgur 上传后） |
| local_path | TEXT | | 原始本地路径 |
| caption | TEXT | | 帖子文字 |
| hashtags | TEXT | | 话题标签 JSON 数组 |
| template_id | INTEGER | FK → templates | 使用的模板（可选） |
| status | TEXT | DEFAULT 'draft' | draft, approved, scheduled, container_created, published, failed |
| scheduled_at | TEXT | | 计划日期时间（ISO 8601） |
| published_at | TEXT | | 实际发布日期时间 |
| ig_media_id | TEXT | | 发布后 API 返回的 ID |
| ig_container_id | TEXT | | 用于两步发布恢复的容器 ID |
| permalink | TEXT | | Instagram 帖子 URL |
| error_msg | TEXT | | 失败时的错误消息 |
| created_at | TEXT | DEFAULT now | 创建时间戳 |

**索引：** `idx_posts_status`, `idx_posts_account`, `idx_posts_ig_media`

### comments
帖子评论，带回复追踪。

| 字段 | 类型 | 约束 | 描述 |
|-------|------|------------|-----------|
| id | INTEGER | PK | 自增 |
| account_id | INTEGER | FK → accounts | 关联账号 |
| ig_comment_id | TEXT | UNIQUE | Graph API 中的评论 ID |
| ig_media_id | TEXT | | 相关媒体 ID |
| username | TEXT | | 作者 @用户名 |
| text | TEXT | | 评论内容 |
| timestamp | TEXT | | ISO 8601 日期时间 |
| replied | INTEGER | DEFAULT 0 | 是否已回复（0/1） |
| reply_text | TEXT | | 回复内容 |
| hidden | INTEGER | DEFAULT 0 | 是否隐藏（0/1） |

### insights
每条媒体的单独指标。

| 字段 | 类型 | 约束 | 描述 |
|-------|------|------------|-----------|
| id | INTEGER | PK | 自增 |
| account_id | INTEGER | FK → accounts | 关联账号 |
| ig_media_id | TEXT | | 媒体 ID |
| metric_name | TEXT | | impressions, reach, engagement, saved, video_views |
| metric_value | REAL | | 指标数值 |
| period | TEXT | | lifetime, day, week, days_28 |
| fetched_at | TEXT | DEFAULT now | 获取时间 |
| raw_json | TEXT | | API 完整响应（保留） |

**索引：** `idx_insights_media`

### user_insights
账号聚合指标（非单条媒体）。

| 字段 | 类型 | 约束 | 描述 |
|-------|------|------------|-----------|
| id | INTEGER | PK | 自增 |
| account_id | INTEGER | FK → accounts | 关联账号 |
| metric_name | TEXT | | follower_count, reach, impressions, profile_views |
| metric_value | REAL | | 指标数值 |
| period | TEXT | | day, week, days_28 |
| end_time | TEXT | | 周期结束时间 ISO 8601 |
| fetched_at | TEXT | DEFAULT now | 获取时间 |

### templates
可复用的标题和话题标签模板。

| 字段 | 类型 | 约束 | 描述 |
|-------|------|------------|-----------|
| id | INTEGER | PK | 自增 |
| name | TEXT | UNIQUE NOT NULL | 模板名称（如："promo"） |
| caption_template | TEXT | | 带 {变量} 的模板 |
| hashtag_set | TEXT | | 话题标签 JSON 数组 |
| default_schedule_time | TEXT | | 默认时间（HH:MM） |
| created_at | TEXT | DEFAULT now | 创建时间戳 |

### hashtag_searches
话题标签搜索追踪（用于遵守每周 30 个的限制）。

| 字段 | 类型 | 约束 | 描述 |
|-------|------|------------|-----------|
| id | INTEGER | PK | 自增 |
| account_id | INTEGER | FK → accounts | 关联账号 |
| hashtag | TEXT | | 搜索的话题标签 |
| ig_hashtag_id | TEXT | | API 返回的 ID |
| searched_at | TEXT | DEFAULT now | 搜索时间戳 |

### action_log
所有修改数据操作的审计日志。

| 字段 | 类型 | 约束 | 描述 |
|-------|------|------------|-----------|
| id | INTEGER | PK | 自增 |
| account_id | INTEGER | | 关联账号（可为 NULL） |
| action | TEXT | NOT NULL | 操作名称（publish_photo, delete_comment 等） |
| params | TEXT | | 操作参数 JSON |
| result | TEXT | | 结果 JSON |
| confirmed | INTEGER | | 用户是否确认（0/1/NULL） |
| rate_remaining | TEXT | | 剩余速率限制 JSON |
| created_at | TEXT | DEFAULT now | 操作时间戳 |

**索引：** `idx_action_log_created`

## 常用查询

### 统计今日发布数
```sql
SELECT COUNT(*) FROM action_log
WHERE action LIKE 'publish_%' AND created_at >= date('now')
```

### 准备处理的未发布帖子
```sql
SELECT * FROM posts
WHERE status IN ('approved', 'scheduled', 'container_created')
AND (scheduled_at IS NULL OR scheduled_at <= datetime('now'))
ORDER BY created_at
```

### 按媒体类型的平均互动
```sql
SELECT p.media_type,
       AVG(i.metric_value) as avg_engagement
FROM posts p
JOIN insights i ON i.ig_media_id = p.ig_media_id
WHERE i.metric_name = 'engagement'
GROUP BY p.media_type
```

### 未回复的评论
```sql
SELECT c.*, p.permalink
FROM comments c
JOIN posts p ON p.ig_media_id = c.ig_media_id
WHERE c.replied = 0
ORDER BY c.timestamp DESC
```

### 本周使用的话题标签
```sql
SELECT DISTINCT hashtag, COUNT(*) as searches
FROM hashtag_searches
WHERE searched_at >= datetime('now', '-7 days')
GROUP BY hashtag
ORDER BY searches DESC
```
