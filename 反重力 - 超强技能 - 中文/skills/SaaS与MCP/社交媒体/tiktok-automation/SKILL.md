---
name: tiktok-automation
description: "通过 Rube MCP（Composio）自动化 TikTok 任务：上传/发布视频、发布图文、管理内容、查看用户主页和数据统计。务必先搜索工具获取当前 schema。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 TikTok 自动化

通过 Composio 的 TikTok 工具包（经由 Rube MCP），自动化 TikTok 内容创作和主页管理操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 连接 toolkit `tiktok`，且状态为 Active
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取最新的工具 schema

## 配置步骤

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API Key——添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `tiktok`
3. 若连接状态不是 ACTIVE，按返回的授权链接完成 TikTok OAuth
4. 运行任何工作流前，确认连接状态为 ACTIVE

## 核心工作流

### 1. 上传并发布视频

**适用场景**：用户想上传视频并发布到 TikTok

**工具调用顺序**：
1. `TIKTOK_UPLOAD_VIDEO` 或 `TIKTOK_UPLOAD_VIDEOS` - 上传视频文件 [必需]
2. `TIKTOK_FETCH_PUBLISH_STATUS` - 检查上传/处理状态 [必需]
3. `TIKTOK_PUBLISH_VIDEO` - 发布已上传的视频 [必需]

**上传关键参数**：
- `video`：视频文件对象，包含 `s3key`、`mimetype`、`name`
- `title`：视频标题/描述

**发布关键参数**：
- `publish_id`：上传步骤返回的 ID
- `title`：视频描述文本
- `privacy_level`：'PUBLIC_TO_EVERYONE'、'MUTUAL_FOLLOW_FRIENDS'、'FOLLOWER_OF_CREATOR'、'SELF_ONLY'
- `disable_duet`：禁用合拍功能
- `disable_stitch`：禁用拼接功能
- `disable_comment`：禁用评论

**注意事项**：
- 视频上传和发布是两个独立步骤，先上传后发布
- 上传后需轮询 FETCH_PUBLISH_STATUS，等处理完成后再发布
- 视频须符合 TikTok 要求：MP4/WebM 格式，最长 10 分钟，最大 4GB
- 描述/标题有字数限制，参考 TikTok 当前规范
- privacy_level 字符串区分大小写，必须完全匹配
- 处理时间视视频大小而定，通常 30-120 秒

### 2. 发布图文

**适用场景**：用户想发布图文到 TikTok

**工具调用顺序**：
1. `TIKTOK_POST_PHOTO` - 上传并发布图文 [必需]
2. `TIKTOK_FETCH_PUBLISH_STATUS` - 检查处理状态 [可选]

**关键参数**：
- `photo`：图片文件对象，包含 `s3key`、`mimetype`、`name`
- `title`：图文描述文本
- `privacy_level`：帖子隐私设置

**注意事项**：
- 图文发布是 TikTok 较新的功能，可用性因账号类型而异
- 支持格式：JPEG、PNG、WebP
- 图片大小和尺寸有限制，参考 TikTok 当前规范

### 3. 查看和管理视频列表

**适用场景**：用户想查看已发布的视频

**工具调用顺序**：
1. `TIKTOK_LIST_VIDEOS` - 列出用户已发布的视频 [必需]

**关键参数**：
- `max_count`：每页返回的视频数量
- `cursor`：用于翻页的分页游标

**注意事项**：
- 仅返回当前认证用户自己的视频
- 响应包含视频元数据：id、title、create_time、share_url、duration 等
- 分页采用游标模式，检查响应中的 `has_more` 和 `cursor`
- 刚发布的视频可能不会立即出现在列表中

### 4. 查看用户主页和数据统计

**适用场景**：用户想查看 TikTok 主页信息或账号统计数据

**工具调用顺序**：
1. `TIKTOK_GET_USER_PROFILE` - 获取完整主页信息 [必需]
2. `TIKTOK_GET_USER_STATS` - 获取账号统计数据 [可选]
3. `TIKTOK_GET_USER_BASIC_INFO` - 获取基本用户信息 [备选]

**关键参数**：（无必需参数；返回当前认证用户的数据）

**注意事项**：
- 主页数据仅限当前认证用户，无法查看其他用户主页
- 统计数据包括粉丝数、关注数、视频数、获赞数
- `GET_USER_PROFILE` 返回的信息比 `GET_USER_BASIC_INFO` 更详细
- 统计数据可能有轻微延迟，非实时

### 5. 检查发布状态

**适用场景**：用户想检查内容上传或发布操作的状态

**工具调用顺序**：
1. `TIKTOK_FETCH_PUBLISH_STATUS` - 轮询状态更新 [必需]

**关键参数**：
- `publish_id`：之前上传/发布操作返回的发布 ID

**注意事项**：
- 状态值包括处理中、成功和失败
- 以合理间隔轮询（5-10 秒），避免触发频率限制
- 发布失败时，响应中会包含错误详情
- 内容审核可能导致处理后延迟或被拒绝

## 通用模式

### 视频发布流程

```
1. Upload video via TIKTOK_UPLOAD_VIDEO -> get publish_id
2. Poll TIKTOK_FETCH_PUBLISH_STATUS with publish_id until complete
3. If status is ready, call TIKTOK_PUBLISH_VIDEO with final settings
4. Optionally poll status again to confirm publication
```

### 分页

- 使用上一次响应中的 `cursor` 获取下一页
- 检查 `has_more` 布尔值判断是否还有更多结果
- `max_count` 控制每页大小

## 已知陷阱

**内容要求**：
- 视频：MP4/WebM，最大 4GB，最长 10 分钟
- 图片：JPEG/PNG/WebP
- 描述：字数限制因地区而异
- 内容须符合 TikTok 社区规范

**认证**：
- OAuth Token 有作用域，确保 video.upload 和 video.publish 已授权
- Token 会过期，操作返回 401 时需重新认证

**频率限制**：
- TikTok API 对每个应用有严格的频率限制
- 遇到 429 响应时实施指数退避
- 上传操作有每日次数限制

**响应解析**：
- 响应数据可能嵌套在 `data` 或 `data.data` 下
- 解析时做防御性处理，设置回退方案
- publish_id 是字符串类型，按原样使用

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 上传视频 | TIKTOK_UPLOAD_VIDEO | video, title |
| 批量上传视频 | TIKTOK_UPLOAD_VIDEOS | videos |
| 发布视频 | TIKTOK_PUBLISH_VIDEO | publish_id, title, privacy_level |
| 发布图文 | TIKTOK_POST_PHOTO | photo, title, privacy_level |
| 查看视频列表 | TIKTOK_LIST_VIDEOS | max_count, cursor |
| 获取主页信息 | TIKTOK_GET_USER_PROFILE | （无） |
| 获取用户统计 | TIKTOK_GET_USER_STATS | （无） |
| 获取基本信息 | TIKTOK_GET_USER_BASIC_INFO | （无） |
| 检查发布状态 | TIKTOK_FETCH_PUBLISH_STATUS | publish_id |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不可将输出替代特定环境的验证、测试或专家审查。
- 若缺少必需的输入、权限、安全边界或成功标准，应停下来请求澄清。