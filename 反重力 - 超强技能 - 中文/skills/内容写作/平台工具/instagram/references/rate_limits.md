# 速率限制 — Instagram Graph API

## 主要限制

| 资源 | 限制 | 时间窗口 | 备注 |
|---------|--------|--------|-------|
| 通用 API 调用 | 200 次请求 | 1 小时 | 每用户/令牌 |
| 内容发布 | 25 条帖子 | 24 小时 | 每 IG 账号 |
| 话题标签搜索 | 30 个唯一标签 | 7 天（滚动） | 每 IG 账号 |
| 私信（发送） | 200 条消息 | 1 小时 | Human Agent messaging |
| Stories | 无官方限制 | — | 但建议 < 25/天 |

## 技能如何追踪

### 滑动窗口（SQLite）
`governance.py` 使用 `action_log` 表统计窗口内的操作：

```sql
-- 最近一小时的请求
SELECT COUNT(*) FROM action_log
WHERE account_id = ? AND created_at >= datetime('now', '-1 hour')

-- 最近 24 小时的发布
SELECT COUNT(*) FROM action_log
WHERE account_id = ? AND action IN ('publish_photo','publish_video',...)
AND created_at >= datetime('now', '-24 hours')

-- 最近一周的唯一话题标签
SELECT COUNT(DISTINCT hashtag) FROM hashtag_searches
WHERE account_id = ? AND searched_at >= datetime('now', '-7 days')
```

### 警告阈值
- **80%**: 信息日志 — "接近速率限制"
- **90%**: 警告 — "接近速率限制，请考虑放慢"
- **100%**: 阻止 — 返回错误并显示预计等待时间

## API 速率限制响应

### 错误代码 4（应用级别）
```json
{
  "error": {
    "message": "Application request limit reached",
    "type": "OAuthException",
    "code": 4
  }
}
```
**操作：** 退避 1 小时。`api_client.py` 检测并自动重试。

### 错误代码 17（用户级别）
```json
{
  "error": {
    "message": "(#17) User request limit reached",
    "type": "OAuthException",
    "code": 17
  }
}
```
**操作：** 每账号退避 1 小时。

### HTTP 429（请求过多）
某些端点返回 HTTP 429 而非 JSON 错误。
**操作：** 遵守 `Retry-After` 头（如存在），否则使用默认退避。

## 退避策略

### api_client.py — 指数退避
```
尝试 1: 等待 2s
尝试 2: 等待 4s
尝试 3: 等待 8s
3 次失败后: 放弃并报告
```

### 特定速率限制
```
代码 4/17: 等待 3600s（1 小时）
代码 190（令牌）: 立即失败（需要刷新）
代码 10/200（权限）: 立即失败
```

## 优化

### 批量请求
为减少请求计数，使用 fields 参数在一次调用中获取多个字段：
```
GET /me?fields=id,username,followers_count,media{id,caption,media_type,permalink}
```

### 本地缓存
`db.py` 将数据持久化到 SQLite — 避免对最近数据重复调用。

### 智能同步
`run_all.py` 按优先级处理：
1. Profile（1 次请求）
2. Media（1 次请求，批量）
3. Insights（N 次请求，每帖 1 次）
4. Comments（N 次请求，每帖 1 次）

使用 `--limit` 控制每次同步处理的帖子数量。

## 监控

```bash
# 查看剩余速率限制（基于日志估算）
python scripts/auth.py --status

# 查看审计日志中的最近操作
python scripts/export.py --type actions --format json
```
