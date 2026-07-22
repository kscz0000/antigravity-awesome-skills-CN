# Instagram 账号类型 — Business vs Creator

## 对比

| 功能 | Personal | Creator | Business |
|---------|----------|---------|----------|
| Graph API | 无访问权限 | 完全访问 | 完全访问 |
| 通过 API 发布 | 禁止 | 支持 | 支持 |
| 媒体洞察 | 禁止 | 支持 | 支持 |
| 账号洞察 | 禁止 | 支持 | 支持 |
| 通过 API 发私信 | 禁止 | 支持 | 支持 |
| 通过 API 管理评论 | 禁止 | 支持 | 支持 |
| API 原生定时发布 | 禁止 | 有限支持 | 支持 |
| 话题标签搜索 | 禁止 | 支持 | 支持 |
| Shopping/目录 | 禁止 | 禁止 | 支持 |
| Facebook 主页关联 | 不需要 | 可选 | 必需 |

## 何时使用各类型

### Business
推荐用于：
- 企业、商店、品牌
- 需要通过 API 原生定时发布
- 想使用 Shopping/目录
- 已有企业 Facebook 主页

### Creator
推荐用于：
- 网红、艺术家、内容创作者
- 想要分析数据的个人
- 不想强制关联 Facebook 主页

### Personal
**Graph API 不支持。** 需要迁移。

## 迁移：Personal → Business/Creator

### 前提条件
1. 活跃的 Instagram 账号
2. 对于 Business：关联的 Facebook 主页（可创建新的）
3. 对于 Creator：不需要主页（可选）

### 步骤（在 Instagram 应用中）

#### 迁移到 Business：
1. 打开 Instagram → 设置
2. 账号 → 切换为专业账号
3. 选择"企业"
4. 选择业务类别
5. 关联 Facebook 主页（或创建新的）
6. 确认

#### 迁移到 Creator：
1. 打开 Instagram → 设置
2. 账号 → 切换为专业账号
3. 选择"创作者"
4. 选择类别
5. 确认

### 迁移后会发生什么
- **保留：** 帖子、粉丝、关注、私信、简介
- **新增：** 洞察、联系按钮、类别
- **变化：** 个人资料公开（如果是私密账号，将被转换）

### 回退
可以回退到 Personal，但：
- 立即失去 API 访问权限
- 失去洞察历史
- 帖子和粉丝保留

## 迁移：Business → Creator

也可以在 Business 和 Creator 之间切换：
1. 设置 → 账号 → 切换账号类型
2. 选择另一个专业类型
3. 洞察历史可能重置

## 自动检测（account_setup.py）

脚本 `account_setup.py --check` 通过以下方式检测类型：
```
GET /me?fields=account_type
```

可能的值：`BUSINESS`, `MEDIA_CREATOR`, `PERSONAL`

如果是 `PERSONAL`，使用 `--guide` 引导用户完成迁移。

## 与 Facebook 主页关联

### 为什么需要（Business）
- Graph API 通过 Facebook Pages API 访问 Instagram
- OAuth 令牌授权主页，主页提供关联 IG 账号的访问权限
- 没有关联主页 → 无法访问 API

### 发现流程（auth.py）
```
1. GET /me/accounts → 列出用户的 Facebook 主页
2. 对每个主页：GET /{page-id}?fields=instagram_business_account
3. 返回关联的 IG 用户 ID
```

### 无主页的 Creator 账号
Creator 账号可以在没有主页的情况下工作，但 OAuth 流程仍需要至少一个主页。建议：创建一个基本主页（不需要内容）仅用于关联。
