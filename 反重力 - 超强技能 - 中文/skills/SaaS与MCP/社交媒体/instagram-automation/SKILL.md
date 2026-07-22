---
name: instagram-automation
description: "通过 Rube MCP (Composio) 自动化 Instagram 任务：创建帖子、轮播图、管理媒体、获取洞察数据和发布限额。始终先搜索工具获取当前 schema。触发词：Instagram自动化、Instagram发布、轮播帖、媒体管理、Instagram洞察、发布限额、Rube MCP、Composio Instagram"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Instagram 自动化

通过 Rube MCP 下的 Composio Instagram 工具包自动化 Instagram 运营操作。

## 前置条件

- Rube MCP 必须已连接（`RUBE_SEARCH_TOOLS` 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 工具包 `instagram` 建立 Instagram 活跃连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema
- 需要 Instagram 商业账号或创作者账号（不支持个人账号）

## 配置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API 密钥——添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 可响应，验证 Rube MCP 可用
2. 使用工具包 `instagram` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按返回的授权链接完成 Instagram/Facebook OAuth 认证
4. 在运行任何工作流之前确认连接状态为 ACTIVE

## 核心工作流

### 1. 创建单图/视频帖子

**适用场景**：用户想向 Instagram 发布单张照片或视频

**工具调用顺序**：
1. `INSTAGRAM_GET_USER_INFO` - 获取 Instagram 用户 ID [前置步骤]
2. `INSTAGRAM_CREATE_MEDIA_CONTAINER` - 使用图片/视频 URL 创建媒体容器 [必需]
3. `INSTAGRAM_GET_POST_STATUS` - 检查媒体容器是否就绪 [可选]
4. `INSTAGRAM_CREATE_POST` 或 `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` - 发布容器 [必需]

**关键参数**：
- `image_url`：待发布图片的公开 URL
- `video_url`：待发布视频的公开 URL
- `caption`：帖子配文
- `ig_user_id`：Instagram 商业账号用户 ID

**注意事项**：
- 媒体 URL 必须可公开访问；私有/需认证的 URL 会失败
- 视频容器处理需要时间；发布前轮询 GET_POST_STATUS
- 配文支持话题标签和 @提及，但有 2200 字符限制
- 发布尚未完成处理的容器会返回错误

### 2. 创建轮播帖子

**适用场景**：用户想在一条轮播帖子中发布多张图片/视频

**工具调用顺序**：
1. `INSTAGRAM_CREATE_MEDIA_CONTAINER` - 为每个媒体项分别创建容器 [必需，每项重复一次]
2. `INSTAGRAM_CREATE_CAROUSEL_CONTAINER` - 创建引用所有媒体容器的轮播容器 [必需]
3. `INSTAGRAM_GET_POST_STATUS` - 检查轮播容器就绪状态 [可选]
4. `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` - 发布轮播 [必需]

**关键参数**：
- `children`：轮播的媒体容器 ID 数组
- `caption`：轮播帖子配文
- `ig_user_id`：Instagram 商业账号用户 ID

**注意事项**：
- 轮播需要 2-10 个媒体项；少于或多于都会失败
- 每个子容器必须在创建轮播容器之前单独创建
- 所有子容器必须完全处理完毕后才能创建轮播
- 轮播支持混合媒体（图片 + 视频）

### 3. 获取媒体和洞察数据

**适用场景**：用户想查看自己的帖子或分析帖子表现

**工具调用顺序**：
1. `INSTAGRAM_GET_IG_USER_MEDIA` 或 `INSTAGRAM_GET_USER_MEDIA` - 列出用户的媒体 [必需]
2. `INSTAGRAM_GET_IG_MEDIA` - 获取特定帖子的详情 [可选]
3. `INSTAGRAM_GET_POST_INSIGHTS` 或 `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` - 获取帖子指标 [可选]
4. `INSTAGRAM_GET_USER_INSIGHTS` - 获取账号级洞察数据 [可选]

**关键参数**：
- `ig_user_id`：Instagram 商业账号用户 ID
- `media_id`：特定媒体帖子的 ID
- `metric`：要获取的指标（如 impressions、reach、engagement）
- `period`：洞察数据的时间范围（如 day、week、lifetime）

**注意事项**：
- 洞察数据仅对商业/创作者账号可用
- 部分指标有最低粉丝数要求
- 洞察数据可能存在最长 48 小时的延迟
- `period` 参数必须与指标类型匹配

### 4. 检查发布限额

**适用场景**：用户想在发帖前确认是否还有发布配额

**工具调用顺序**：
1. `INSTAGRAM_GET_IG_USER_CONTENT_PUBLISHING_LIMIT` - 检查剩余发布配额 [必需]

**关键参数**：
- `ig_user_id`：Instagram 商业账号用户 ID

**注意事项**：
- Instagram 强制执行每 24 小时滚动窗口 25 条帖子的限额
- 发布限额按滚动方式重置，而非午夜归零
- 批量发帖前务必检查限额以避免失败

### 5. 获取媒体评论和子项

**适用场景**：用户想查看帖子的评论或轮播帖的子项

**工具调用顺序**：
1. `INSTAGRAM_GET_IG_MEDIA_COMMENTS` - 列出媒体帖子的评论 [必需]
2. `INSTAGRAM_GET_IG_MEDIA_CHILDREN` - 列出轮播帖子的子项 [可选]

**关键参数**：
- `media_id`：媒体帖子的 ID
- `ig_media_id`：备选媒体 ID 参数

**注意事项**：
- 评论可能分页返回；需跟随分页游标获取完整结果
- 轮播子项以独立媒体对象的形式返回
- 账号的评论审核设置会影响返回内容

## 常用模式

### ID 解析

**Instagram 用户 ID**：
```
1. Call INSTAGRAM_GET_USER_INFO
2. Extract ig_user_id from response
3. Use in all subsequent API calls
```

**媒体容器状态检查**：
```
1. Call INSTAGRAM_CREATE_MEDIA_CONTAINER
2. Extract container_id from response
3. Poll INSTAGRAM_GET_POST_STATUS with container_id
4. Wait until status is 'FINISHED' before publishing
```

### 两阶段发布

- 阶段 1：使用内容 URL 创建媒体容器
- 阶段 2：容器处理完成后发布
- 对于视频内容，两个阶段之间务必检查容器状态
- 对于轮播，所有子项必须完成阶段 1 后才能创建轮播容器

## 已知陷阱

**媒体 URL**：
- 所有图片/视频 URL 必须是可公开访问的 HTTPS URL
- 需要认证、CDN 限制或需要 Cookie 的 URL 会失败
- 临时 URL（如预签名 S3 等）可能在处理完成前过期

**速率限制**：
- 每 24 小时滚动窗口 25 条帖子
- API 速率限制与发布限额独立计算
- 对 429 响应实施指数退避重试

**账号要求**：
- 仅支持 Instagram 商业账号或创作者账号
- 个人账号无法使用 Instagram Graph API
- 账号必须关联 Facebook 主页

**响应解析**：
- 媒体 ID 为数字字符串
- 洞察数据可能嵌套在不同的响应键下
- 分页使用基于游标的 token

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 获取用户信息 | INSTAGRAM_GET_USER_INFO | (无) |
| 创建媒体容器 | INSTAGRAM_CREATE_MEDIA_CONTAINER | image_url/video_url, caption |
| 创建轮播 | INSTAGRAM_CREATE_CAROUSEL_CONTAINER | children, caption |
| 发布帖子 | INSTAGRAM_CREATE_POST | ig_user_id, creation_id |
| 发布媒体 | INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH | ig_user_id, creation_id |
| 检查帖子状态 | INSTAGRAM_GET_POST_STATUS | ig_container_id |
| 列出用户媒体 | INSTAGRAM_GET_IG_USER_MEDIA | ig_user_id |
| 获取媒体详情 | INSTAGRAM_GET_IG_MEDIA | ig_media_id |
| 获取帖子洞察 | INSTAGRAM_GET_POST_INSIGHTS | media_id, metric |
| 获取用户洞察 | INSTAGRAM_GET_USER_INSIGHTS | ig_user_id, metric, period |
| 获取发布限额 | INSTAGRAM_GET_IG_USER_CONTENT_PUBLISHING_LIMIT | ig_user_id |
| 获取媒体评论 | INSTAGRAM_GET_IG_MEDIA_COMMENTS | ig_media_id |
| 获取轮播子项 | INSTAGRAM_GET_IG_MEDIA_CHILDREN | ig_media_id |

## 何时使用
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
