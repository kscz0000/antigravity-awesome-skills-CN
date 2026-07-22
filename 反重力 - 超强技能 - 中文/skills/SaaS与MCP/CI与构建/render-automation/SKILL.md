---
name: render-automation
description: "通过 Rube MCP (Composio) 自动化 Render 任务：服务、部署、项目。始终先搜索工具获取当前 schema。触发词：Render自动化、Render部署、Render服务管理、Render项目、Rube MCP、Composio"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Render

通过 Composio 的 Render 工具包，借助 Rube MCP 实现 Render 云平台操作的自动化。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用工具包 `render` 建立活跃的 Render 连接
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 配置

**获取 Rube MCP**：将 `https://rube.app/mcp` 作为 MCP 服务器添加到客户端配置中。无需 API Key——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 使用工具包 `render` 调用 `RUBE_MANAGE_CONNECTIONS`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Render 认证
4. 确认连接状态显示 ACTIVE 后再运行任何工作流

## 核心工作流

### 1. 列出和浏览服务

**使用场景**：用户想查找或检查 Render 服务（Web 服务、静态站点、Worker、定时任务）

**工具调用顺序**：
1. `RENDER_LIST_SERVICES` - 列出所有服务，支持可选过滤器 [必需]

**关键参数**：
- `name`：按名称子串过滤服务
- `type`：按服务类型过滤（'web_service'、'static_site'、'private_service'、'background_worker'、'cron_job'）
- `limit`：每页最大结果数（默认 20，最大 100）
- `cursor`：来自上一次响应的分页游标

**注意事项**：
- 服务类型必须匹配精确的枚举值：'web_service'、'static_site'、'private_service'、'background_worker'、'cron_job'
- 分页采用游标方式；跟随 `cursor` 直到其消失
- 名称过滤基于子串匹配，不是精确匹配
- 服务 ID 格式为 'srv-xxxxxxxxxxxx'
- 默认 limit 为 20；如需完整列表请设置更高值

### 2. 触发部署

**使用场景**：用户想手动部署或重新部署某个服务

**工具调用顺序**：
1. `RENDER_LIST_SERVICES` - 找到要部署的服务 [前置条件]
2. `RENDER_TRIGGER_DEPLOY` - 触发新部署 [必需]
3. `RENDER_RETRIEVE_DEPLOY` - 监控部署进度 [可选]

**关键参数**：
- TRIGGER_DEPLOY 参数：
  - `serviceId`：要部署的服务 ID（必填，格式：'srv-xxxxxxxxxxxx'）
  - `clearCache`：设为 `true` 在部署前清除构建缓存
- RETRIEVE_DEPLOY 参数：
  - `serviceId`：服务 ID
  - `deployId`：来自触发响应的部署 ID（格式：'dep-xxxxxxxxxxxx'）

**注意事项**：
- `serviceId` 为必填项；先通过 LIST_SERVICES 解析
- 服务 ID 以 'srv-' 前缀开头
- 部署 ID 以 'dep-' 前缀开头
- `clearCache: true` 强制执行干净构建；耗时更长但能解决缓存相关问题
- 部署是异步的；使用 RETRIEVE_DEPLOY 轮询状态
- 在另一个部署进行中触发新部署可能会排队

### 3. 监控部署状态

**使用场景**：用户想检查部署的进度或结果

**工具调用顺序**：
1. `RENDER_RETRIEVE_DEPLOY` - 获取部署详情和状态 [必需]

**关键参数**：
- `serviceId`：服务 ID（必填）
- `deployId`：部署 ID（必填）
- 响应包含 `status`、`createdAt`、`updatedAt`、`finishedAt`、`commit`

**注意事项**：
- `serviceId` 和 `deployId` 都是必填项
- 部署状态包括：'created'、'build_in_progress'、'update_in_progress'、'live'、'deactivated'、'build_failed'、'update_failed'、'canceled'
- 'live' 表示部署成功
- 'build_failed' 或 'update_failed' 表示部署出错
- 以合理间隔轮询（10-30 秒）以避免触发速率限制

### 4. 管理项目

**使用场景**：用户想列出和组织 Render 项目

**工具调用顺序**：
1. `RENDER_LIST_PROJECTS` - 列出所有项目 [必需]

**关键参数**：
- `limit`：每页最大结果数（最大 100）
- `cursor`：来自上一次响应的分页游标

**注意事项**：
- 项目将相关服务分组在一起
- 分页采用游标方式
- 项目 ID 用于组织管理
- 并非所有服务都归属于某个项目

## 常用模式

### ID 解析

**服务名称 -> 服务 ID**：
```
1. Call RENDER_LIST_SERVICES with name=service_name
2. Find service by name in results
3. Extract id (format: 'srv-xxxxxxxxxxxx')
```

**部署查询**：
```
1. Store deployId from RENDER_TRIGGER_DEPLOY response
2. Call RENDER_RETRIEVE_DEPLOY with serviceId and deployId
3. Check status for completion
```

### 部署并监控模式

```
1. RENDER_LIST_SERVICES -> find service by name -> get serviceId
2. RENDER_TRIGGER_DEPLOY with serviceId -> get deployId
3. Loop: RENDER_RETRIEVE_DEPLOY with serviceId + deployId
4. Check status: 'live' = success, 'build_failed'/'update_failed' = error
5. Continue polling until terminal state reached
```

### 分页

- 使用响应中的 `cursor` 获取下一页
- 持续翻页直到 `cursor` 消失或结果为空
- LIST_SERVICES 和 LIST_PROJECTS 都使用游标分页
- 将 `limit` 设为最大值（100）以减少分页轮次

## 已知陷阱

**服务 ID**：
- 始终以 'srv-' 为前缀（如 'srv-abcd1234efgh'）
- 部署 ID 以 'dep-' 为前缀（如 'dep-d2mqkf9r0fns73bham1g'）
- 始终通过 LIST_SERVICES 将服务名称解析为 ID

**服务类型**：
- 过滤时必须使用精确的枚举值
- 可用类型：web_service、static_site、private_service、background_worker、cron_job
- 不同服务类型有不同的部署行为

**部署行为**：
- 部署是异步的；始终轮询等待完成
- 清除缓存的部署耗时更长，但能解决过期缓存问题
- 失败的部署不会自动回滚；前一个版本保持在线
- 并发触发的部署可能会排队

**速率限制**：
- Render API 有速率限制
- 避免频繁轮询；使用 10-30 秒间隔
- 批量操作应进行限流

**响应解析**：
- 响应数据可能嵌套在 `data` 键下
- 时间戳使用 ISO 8601 格式
- 对可选字段进行防御性解析并提供回退值

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 列出服务 | RENDER_LIST_SERVICES | name, type, limit, cursor |
| 触发部署 | RENDER_TRIGGER_DEPLOY | serviceId, clearCache |
| 获取部署状态 | RENDER_RETRIEVE_DEPLOY | serviceId, deployId |
| 列出项目 | RENDER_LIST_PROJECTS | limit, cursor |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出作为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
