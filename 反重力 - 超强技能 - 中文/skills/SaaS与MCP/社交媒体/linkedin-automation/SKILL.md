---
name: linkedin-automation
description: "通过 Rube MCP (Composio) 自动化 LinkedIn 任务：创建帖子、管理个人资料、公司信息、评论和图片上传。务必先搜索工具获取最新 schema。当用户要求'自动化LinkedIn操作'、'LinkedIn发帖'、'管理LinkedIn'、'LinkedIn自动发布'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 LinkedIn 自动化

通过 Rube MCP 接入 Composio 的 LinkedIn 工具包，自动化 LinkedIn 操作。

## 前提条件

- Rube MCP 已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立 LinkedIn 活跃连接，toolkit 设为 `linkedin`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `linkedin`
3. 若连接状态非 ACTIVE，按返回的授权链接完成 LinkedIn OAuth
4. 确认连接状态为 ACTIVE 后再运行任何工作流

## 核心工作流

### 1. 创建 LinkedIn 帖子

**适用场景**：用户想在 LinkedIn 发布文本帖子

**工具调用顺序**：
1. `LINKEDIN_GET_MY_INFO` - 获取已认证用户的资料信息 [前置]
2. `LINKEDIN_REGISTER_IMAGE_UPLOAD` - 若帖子包含图片，注册图片上传 [可选]
3. `LINKEDIN_CREATE_LINKED_IN_POST` - 发布帖子 [必需]

**关键参数**：
- `text`：帖子内容文本
- `visibility`：'PUBLIC' 或 'CONNECTIONS'
- `media_title`：附件媒体的标题
- `media_description`：附件媒体的描述

**注意事项**：
- 创建帖子前必须通过 GET_MY_INFO 获取用户资料 URN
- 图片上传分两步：先注册上传，再在帖子中引用该资源
- 帖子文本受 LinkedIn API 字符数限制
- 可见性默认值可能不同，务必显式指定

### 2. 获取资料信息

**适用场景**：用户想查看自己的 LinkedIn 个人资料或公司详情

**工具调用顺序**：
1. `LINKEDIN_GET_MY_INFO` - 获取已认证用户的资料 [必需]
2. `LINKEDIN_GET_COMPANY_INFO` - 获取公司主页详情 [可选]

**关键参数**：
- GET_MY_INFO 无需参数（使用已认证用户）
- `organization_id`：GET_COMPANY_INFO 所需的公司/组织 ID

**注意事项**：
- GET_MY_INFO 仅返回已认证用户，无法查询其他用户
- 公司信息需要数字组织 ID，不支持公司名称或 vanity URL
- 部分资料字段可能因 OAuth 授权范围而受限

### 3. 管理帖子图片

**适用场景**：用户想上传图片并附加到 LinkedIn 帖子

**工具调用顺序**：
1. `LINKEDIN_REGISTER_IMAGE_UPLOAD` - 向 LinkedIn 注册图片上传 [必需]
2. 将图片二进制数据上传至返回的上传 URL [必需]
3. `LINKEDIN_GET_IMAGES` - 验证已上传图片的状态 [可选]
4. `LINKEDIN_CREATE_LINKED_IN_POST` - 使用图片资源创建帖子 [必需]

**关键参数**：
- `owner`：图片所有者的 URN（用户或组织）
- `image_id`：GET_IMAGES 所需的已上传图片 ID

**注意事项**：
- 上传分两阶段：注册后上传二进制数据
- 创建帖子时必须使用注册时返回的图片资源 URN
- 支持格式通常包括 JPG、PNG 和 GIF
- 大图片处理可能需要时间才能可用

### 4. 评论帖子

**适用场景**：用户想在已有 LinkedIn 帖子上发表评论

**工具调用顺序**：
1. `LINKEDIN_CREATE_COMMENT_ON_POST` - 在帖子上添加评论 [必需]

**关键参数**：
- `post_id`：待评论帖子的 URN 或 ID
- `text`：评论内容
- `actor`：评论者的 URN（用户或组织）

**注意事项**：
- 帖子 ID 必须为有效的 LinkedIn URN 格式
- actor URN 必须与已认证用户或所管理的组织一致
- 评论创建受速率限制，避免短时间内频繁评论

### 5. 删除帖子

**适用场景**：用户想删除已发布的 LinkedIn 帖子

**工具调用顺序**：
1. `LINKEDIN_DELETE_LINKED_IN_POST` - 删除指定帖子 [必需]

**关键参数**：
- `post_id`：待删除帖子的 URN 或 ID

**注意事项**：
- 删除不可逆，无法恢复
- 仅帖子作者或组织管理员可删除帖子
- post_id 必须是创建帖子时返回的完整 URN

## 常用模式

### ID 解析

**从资料获取用户 URN**：
```
1. Call LINKEDIN_GET_MY_INFO
2. Extract user URN (e.g., 'urn:li:person:XXXXXXXXXX')
3. Use URN as actor/owner in subsequent calls
```

**从公司获取组织 ID**：
```
1. Call LINKEDIN_GET_COMPANY_INFO with organization_id
2. Extract organization URN for posting as a company page
```

### 图片上传流程

- 调用 REGISTER_IMAGE_UPLOAD 获取上传 URL 和资源 URN
- 将图片二进制数据上传至提供的 URL
- 创建带媒体的帖子时使用该资源 URN
- 若上传状态不确定，用 GET_IMAGES 验证

## 已知注意事项

**认证**：
- LinkedIn OAuth 令牌作用域有限，确保已授予所需权限
- 令牌会过期，API 返回 401 错误时需重新认证

**URN 格式**：
- LinkedIn 使用 URN 标识符（如 'urn:li:person:ABC123'）
- 始终使用完整 URN 格式，不要只用字母数字 ID 部分
- 组织 URN 与个人 URN 格式不同

**速率限制**：
- LinkedIn API 对帖子创建和评论有严格的每日速率限制
- 批量操作需实现退避策略
- 监控 429 响应并遵守 Retry-After 头

**内容限制**：
- 帖子受 API 字符数限制
- 部分内容类型（投票、文档）可能需要额外的 API 功能
- 帖子文本不支持 HTML 标记

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 获取个人资料 | LINKEDIN_GET_MY_INFO | (无) |
| 创建帖子 | LINKEDIN_CREATE_LINKED_IN_POST | text, visibility |
| 获取公司信息 | LINKEDIN_GET_COMPANY_INFO | organization_id |
| 注册图片上传 | LINKEDIN_REGISTER_IMAGE_UPLOAD | owner |
| 获取已上传图片 | LINKEDIN_GET_IMAGES | image_id |
| 删除帖子 | LINKEDIN_DELETE_LINKED_IN_POST | post_id |
| 评论帖子 | LINKEDIN_CREATE_COMMENT_ON_POST | post_id, text, actor |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家审查
- 若缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清
