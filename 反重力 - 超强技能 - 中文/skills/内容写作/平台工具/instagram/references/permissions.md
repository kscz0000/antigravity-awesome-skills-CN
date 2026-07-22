# OAuth 权限 — 各功能的权限范围

## 所需权限范围

| 权限范围 | 描述 | 功能 |
|-------|-----------|----------|
| `instagram_basic` | 读取个人资料和媒体 | 个人资料、列出帖子、媒体 |
| `instagram_content_publish` | 发布内容 | 发布照片、视频、reels、stories、轮播 |
| `instagram_manage_comments` | 管理评论 | 读取、回复、删除、隐藏评论 |
| `instagram_manage_insights` | 读取洞察 | 媒体和账号洞察 |
| `instagram_manage_messages` | 管理私信 | 发送、接收、列出消息 |
| `pages_show_list` | 列出 Facebook 主页 | 发现关联 IG 账号所需 |
| `pages_read_engagement` | 读取主页互动 | 某些指标所需 |

## 功能 → 权限范围映射

### 读取（基础）
```
查看个人资料        → instagram_basic, pages_show_list
列出媒体            → instagram_basic
查看评论            → instagram_basic
```

### 发布
```
发布照片/视频       → instagram_content_publish, instagram_basic
发布 reel           → instagram_content_publish, instagram_basic
发布 story          → instagram_content_publish, instagram_basic
发布轮播            → instagram_content_publish, instagram_basic
定时帖子            → instagram_content_publish, instagram_basic
```

### 社区
```
回复评论            → instagram_manage_comments
删除评论            → instagram_manage_comments
隐藏评论            → instagram_manage_comments
查看提及            → instagram_basic
```

### 消息
```
列出对话            → instagram_manage_messages
读取消息            → instagram_manage_messages
发送消息            → instagram_manage_messages
```

### 分析
```
媒体洞察            → instagram_manage_insights
账号洞察            → instagram_manage_insights
话题标签搜索        → instagram_basic
```

## 审批流程

### 开发（测试模式）
- 在 Meta App 中配置最多 5 个测试用户
- 所有权限范围无需审批即可使用
- 测试令牌正常工作

### 生产（App Review）
超出测试用户范围使用时，每个权限范围都需要审批：

1. **instagram_basic** — 简单审批（基本使用）
2. **instagram_content_publish** — 需要使用理由
3. **instagram_manage_comments** — 需要使用理由
4. **instagram_manage_insights** — 需要使用理由
5. **instagram_manage_messages** — 更严格的审批（隐私相关）

### App Review 技巧
- 录制展示使用场景的视频
- 清楚解释为什么需要每个权限
- 证明数据使用方式负责任
- 对于个人使用（1 个账号），测试模式足够

## auth.py 权限范围清单

`config.py` 定义默认权限范围：
```python
OAUTH_SCOPES = [
    "instagram_basic",
    "instagram_content_publish",
    "instagram_manage_comments",
    "instagram_manage_insights",
    "instagram_manage_messages",
    "pages_show_list",
    "pages_read_engagement",
]
```

如果不需要所有功能，可以在设置时减少权限范围。
