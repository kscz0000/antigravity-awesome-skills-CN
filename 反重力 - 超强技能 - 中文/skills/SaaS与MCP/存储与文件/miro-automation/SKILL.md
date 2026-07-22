---
name: miro-automation
description: "通过 Rube MCP (Composio) 自动化 Miro 任务：画板、元素、便签、框架、分享、连接器。始终先搜索工具获取最新 schema。当用户要求'自动化 Miro'、'操作 Miro 画板'、'创建便签'、'分享画板'、'连接 Miro 元素'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 自动化 Miro

通过 Composio 的 Miro 工具包和 Rube MCP 自动化 Miro 白板操作。

## 前提条件

- Rube MCP 已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 激活 Miro 连接，toolkit 设为 `miro`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中将 `https://rube.app/mcp` 添加为 MCP 服务器。无需 API Key——添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `miro`
3. 若连接状态非 ACTIVE，按返回的授权链接完成 Miro OAuth
4. 运行任何工作流前确认连接状态为 ACTIVE

## 核心工作流

### 1. 列出和浏览画板

**适用场景**：查找画板或获取画板详情

**工具调用顺序**：
1. `MIRO_GET_BOARDS2` - 列出所有可访问的画板 [必需]
2. `MIRO_GET_BOARD` - 获取特定画板的详细信息 [可选]

**关键参数**：
- `query`：按名称筛选画板的搜索词
- `sort`：排序方式，可选 'default'、'last_modified'、'last_opened'、'last_created'、'alphabetically'
- `limit`：每页结果数（最大 50）
- `offset`：分页偏移量
- `board_id`：用于详细检索的特定画板 ID

**注意事项**：
- 分页采用 offset 方式，非 cursor 方式
- 每页最多 50 个画板；需用 offset 迭代获取完整列表
- 画板 ID 为长字母数字串；始终先通过搜索解析

### 2. 创建画板和元素

**适用场景**：创建新画板或向已有画板添加元素

**工具调用顺序**：
1. `MIRO_CREATE_BOARD` - 创建空白画板 [可选]
2. `MIRO_CREATE_STICKY_NOTE_ITEM` - 向画板添加便签 [可选]
3. `MIRO_CREATE_FRAME_ITEM2` - 添加框架来组织内容 [可选]
4. `MIRO_CREATE_ITEMS_IN_BULK` - 批量添加元素 [可选]

**关键参数**：
- `name` / `description`：画板名称和描述（用于 CREATE_BOARD）
- `board_id`：目标画板 ID（所有元素创建操作必需）
- `data`：内容对象，含 `content` 字段用于便签文本
- `style`：样式对象，含 `fillColor` 用于便签颜色
- `position`：含 `x` 和 `y` 坐标的对象
- `geometry`：含 `width` 和 `height` 的对象

**注意事项**：
- `board_id` 是所有元素操作的必需参数；先通过 GET_BOARDS2 解析
- 便签颜色在 `fillColor` 字段使用十六进制代码（如 '#FF0000'）
- 位置坐标使用画板坐标系（原点在中心）
- 批量创建有单次请求元素上限；查看当前 schema 确认
- 框架元素必须提供含 width 和 height 的 `geometry`

### 3. 浏览和管理画板元素

**适用场景**：查看、查找或组织画板上的元素

**工具调用顺序**：
1. `MIRO_GET_BOARD_ITEMS` - 列出画板上所有元素 [必需]
2. `MIRO_GET_CONNECTORS2` - 列出元素间的连接 [可选]

**关键参数**：
- `board_id`：目标画板 ID（必需）
- `type`：按元素类型筛选（'sticky_note'、'shape'、'text'、'frame'、'image'、'card'）
- `limit`：每页元素数
- `cursor`：上一次响应的分页游标

**注意事项**：
- 结果分页返回；持续跟踪 `cursor` 直到其消失即为完整列表
- 元素类型必须严格匹配 Miro 预定义类型
- 大型画板可能有数千个元素；用类型筛选缩小范围
- 连接器与元素分开管理；用 GET_CONNECTORS2 获取关系数据

### 4. 分享和协作画板

**适用场景**：与团队成员分享画板或管理访问权限

**工具调用顺序**：
1. `MIRO_GET_BOARDS2` - 找到要分享的画板 [前置]
2. `MIRO_SHARE_BOARD` - 分享画板给用户 [必需]
3. `MIRO_GET_BOARD_MEMBERS` - 验证当前画板成员 [可选]

**关键参数**：
- `board_id`：要分享的画板（必需）
- `emails`：邀请的邮箱地址数组
- `role`：访问级别（'viewer'、'commenter'、'editor'）
- `message`：可选的邀请消息

**注意事项**：
- 邮箱地址必须有效；无效邮箱会导致整个请求失败
- 角色必须是预定义值之一；区分大小写
- 与组织外用户分享可能需要管理员审批
- GET_BOARD_MEMBERS 返回所有成员，包括所有者

### 5. 创建可视化连接

**适用场景**：用线条或箭头连接画板上的元素

**工具调用顺序**：
1. `MIRO_GET_BOARD_ITEMS` - 找到要连接的元素 [前置]
2. `MIRO_GET_CONNECTORS2` - 查看已有连接 [可选]

**关键参数**：
- `board_id`：目标画板 ID
- `startItem`：含源元素 `id` 的对象
- `endItem`：含目标元素 `id` 的对象
- `style`：连接器样式（线型、颜色、箭头）

**注意事项**：
- 起始和终止元素必须在同一画板上
- 创建连接需要元素 ID；先通过 GET_BOARD_ITEMS 解析
- 连接器样式多样；查看 schema 中的可用选项
- 不允许自引用连接（起始和终止相同）

## 常用模式

### ID 解析

**画板名称 → 画板 ID**：
```
1. Call MIRO_GET_BOARDS2 with query=board_name
2. Find board by name in results
3. Extract id field
```

**画板上查找元素**：
```
1. Call MIRO_GET_BOARD_ITEMS with board_id and optional type filter
2. Find item by content or position
3. Extract item id for further operations
```

### 分页

- 画板：使用 `offset` 和 `limit`（基于偏移）
- 画板元素：使用 `cursor` 和 `limit`（基于游标）
- 持续请求直到无更多结果或 cursor 消失
- 各端点默认页大小不同

### 坐标系

- 画板原点 (0,0) 在中心
- X 正方向为右，Y 正方向为下
- 元素按中心点定位
- 使用 `position: {x: 0, y: 0}` 放置在画板中心
- 框架定义有界区域；内部元素继承框架位置

## 已知注意事项

**画板 ID**：
- 几乎所有操作都需要画板 ID
- 始终先通过 GET_BOARDS2 将画板名称解析为 ID
- 不要硬编码画板 ID；不同账户 ID 不同

**元素创建**：
- 每种元素类型的必填字段不同
- 便签需要 `data.content` 来设置文本
- 框架需要 `geometry.width` 和 `geometry.height`
- 未指定位置时默认 (0,0)；元素可能重叠

**速率限制**：
- Miro API 按 token 有速率限制
- 批量操作优于逐个创建元素
- 多个元素时使用 MIRO_CREATE_ITEMS_IN_BULK

**响应解析**：
- 响应数据可能嵌套在 `data` 键下
- 元素类型决定响应中包含哪些字段
- 防御性解析；可选字段可能缺失

## 速查表

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出画板 | MIRO_GET_BOARDS2 | query, sort, limit, offset |
| 获取画板详情 | MIRO_GET_BOARD | board_id |
| 创建画板 | MIRO_CREATE_BOARD | name, description |
| 添加便签 | MIRO_CREATE_STICKY_NOTE_ITEM | board_id, data, style, position |
| 添加框架 | MIRO_CREATE_FRAME_ITEM2 | board_id, data, geometry, position |
| 批量添加元素 | MIRO_CREATE_ITEMS_IN_BULK | board_id, items |
| 获取画板元素 | MIRO_GET_BOARD_ITEMS | board_id, type, cursor |
| 分享画板 | MIRO_SHARE_BOARD | board_id, emails, role |
| 获取成员 | MIRO_GET_BOARD_MEMBERS | board_id |
| 获取连接器 | MIRO_GET_CONNECTORS2 | board_id |

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家审查
- 若缺少必需的输入、权限、安全边界或成功标准，应停下来请求澄清
