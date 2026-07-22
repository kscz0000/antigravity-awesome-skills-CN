---
name: trello-automation
description: "通过 Rube MCP（Composio）自动化 Trello 看板、卡片和工作流。支持创建卡片、管理列表、分配成员及跨看板搜索。触发词：Trello自动化、看板管理、卡片创建、工作流自动化"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Trello 自动化

通过 Composio 的 Rube MCP 集成，自动化 Trello 看板管理、卡片创建和团队协作工作流。

## 前置条件

- Rube MCP 已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立了 toolkit 为 `trello` 的活跃 Trello 连接
- 操作前务必先调用 `RUBE_SEARCH_TOOLS` 获取当前工具的 schema

## 配置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API Key，添加端点即可使用。

1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 设为 `trello`
3. 若连接状态非 ACTIVE，按返回的授权链接完成 Trello 认证
4. 运行任何工作流前，确认连接状态为 ACTIVE

## 核心工作流

### 1. 在看板上创建卡片

**适用场景**：向 Trello 看板添加新卡片或任务

**工具调用顺序**：
1. `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER` - 列出看板，获取目标看板 ID [前置]
2. `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD` - 获取看板上的列表，找到目标列表 ID [前置]
3. `TRELLO_ADD_CARDS` - 在目标列表上创建卡片 [必需]
4. `TRELLO_ADD_CARDS_CHECKLISTS_BY_ID_CARD` - 为卡片添加清单 [可选]
5. `TRELLO_ADD_CARDS_CHECKLIST_CHECK_ITEM_BY_ID_CARD_BY_ID_CHECKLIST` - 向清单添加条目 [可选]

**关键参数**：
- `idList`：24 位十六进制 ID（非列表名称）
- `name`：卡片标题
- `desc`：卡片描述（支持 Markdown）
- `pos`：位置（'top'/'bottom'）
- `due`：截止日期（ISO 8601 格式）

**注意事项**：
- 立即保存返回的 id（idCard），后续清单操作依赖此值
- 清单响应可能是嵌套结构（data.data），需从内层对象提取 idChecklist
- 每个清单条目需一次 API 调用，大量条目可能触发速率限制

### 2. 管理看板和列表

**适用场景**：查看、浏览或重组看板布局

**工具调用顺序**：
1. `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER` - 列出用户的所有看板 [必需]
2. `TRELLO_GET_BOARDS_BY_ID_BOARD` - 获取看板详情 [必需]
3. `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD` - 获取看板上的列表（列） [可选]
4. `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD` - 获取看板成员 [可选]
5. `TRELLO_GET_BOARDS_LABELS_BY_ID_BOARD` - 获取看板标签 [可选]

**关键参数**：
- `idMember`：当前认证用户使用 'me'
- `filter`：'open'、'starred' 或 'all'
- `idBoard`：24 位十六进制或 8 位 shortLink（非看板名称）

**注意事项**：
- 某些响应中看板位于 response.data.details[] 下，不要假设为顶层扁平数组
- 列表可能嵌套在 results[0].response.data.details 中，解析时需做防御性处理
- 带尾部 'Z' 的 ISO 8601 时间戳必须按带时区方式解析

### 3. 在列表间移动卡片

**适用场景**：将卡片移到另一个列表以变更状态

**工具调用顺序**：
1. `TRELLO_GET_SEARCH` - 按名称或关键词搜索卡片 [前置]
2. `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD` - 获取目标列表 ID [前置]
3. `TRELLO_UPDATE_CARDS_BY_ID_CARD` - 更新卡片的 idList 完成移动 [必需]

**关键参数**：
- `idCard`：搜索返回的卡片 ID
- `idList`：目标列表 ID
- `pos`：在新列表中的排序位置（可选）

**注意事项**：
- 搜索返回部分匹配结果，更新前核实卡片名称
- 移动不会自动更新在新列表中的位置，需要排序时手动设置 pos

### 4. 为卡片分配成员

**适用场景**：将团队成员分配到卡片

**工具调用顺序**：
1. `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD` - 获取看板成员 ID [前置]
2. `TRELLO_ADD_CARDS_ID_MEMBERS_BY_ID_CARD` - 将成员添加到卡片 [必需]

**关键参数**：
- `idCard`：目标卡片 ID
- `value`：要分配的成员 ID

**注意事项**：
- UPDATE_CARDS_ID_MEMBERS 会替换全部成员列表，追加请用 ADD_CARDS_ID_MEMBERS
- 成员必须拥有看板权限

### 5. 搜索和筛选卡片

**适用场景**：跨看板查找特定卡片

**工具调用顺序**：
1. `TRELLO_GET_SEARCH` - 按查询字符串搜索 [必需]

**关键参数**：
- `query`：搜索字符串（支持 board:、list:、label:、is:open/archived 操作符）
- `modelTypes`：设为 'cards'
- `partial`：设为 'true' 启用前缀匹配

**注意事项**：
- 搜索索引有延迟，新创建的卡片可能数分钟后才可搜到
- 精确名称匹配请用 TRELLO_GET_BOARDS_CARDS_BY_ID_BOARD 在本地过滤
- 查询使用分词处理，常见词可能被当作停用词忽略

### 6. 添加评论和附件

**适用场景**：为已有卡片补充上下文信息

**工具调用顺序**：
1. `TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD` - 在卡片上发布评论 [必需]
2. `TRELLO_ADD_CARDS_ATTACHMENTS_BY_ID_CARD` - 附加文件或 URL [可选]

**关键参数**：
- `text`：评论文本（1-16384 字符，支持 Markdown 和 @提及）
- `url` 或 `file`：附件来源（二选一）
- `name`：附件显示名称
- `mimeType`：文件 MIME 类型

**注意事项**：
- 评论不支持文件附件，需单独使用附件工具
- 附件删除不可恢复

## 常用模式

### ID 解析
操作前必须将显示名称解析为 ID：
- **看板名称 → 看板 ID**：用 `TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER`，idMember='me'
- **列表名称 → 列表 ID**：用 `TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD`，传入已解析的看板 ID
- **卡片名称 → 卡片 ID**：用 `TRELLO_GET_SEARCH`，传入查询字符串
- **成员名称 → 成员 ID**：用 `TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD`

### 分页
大多数列表端点返回全部数据。对于超过 1000 张卡片的看板，在卡片列表端点使用 `limit` 和 `before` 参数分页。

### 速率限制
每 Token 每 10 秒 300 次请求。批量读取使用 `TRELLO_GET_BATCH` 以控制请求量。

## 已知陷阱

- **ID 要求**：几乎所有工具都需要 ID 而非显示名称，操作前务必先解析名称到 ID
- **看板 ID 格式**：看板 ID 必须是 24 位十六进制或 8 位 shortLink，'my-board' 这类 URL slug 不是合法 ID
- **搜索延迟**：搜索索引有延迟，新创建或更新的卡片不会立即出现
- **嵌套响应**：响应数据常为嵌套结构（data.data 或 data.details[]），需防御性解析
- **速率限制**：每 Token 每 10 秒 300 次请求，批量读取请用 TRELLO_GET_BATCH

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|-----------|------------|
| 列出用户看板 | TRELLO_GET_MEMBERS_BOARDS_BY_ID_MEMBER | idMember='me', filter='open' |
| 获取看板详情 | TRELLO_GET_BOARDS_BY_ID_BOARD | idBoard（24 位十六进制） |
| 列出看板列表 | TRELLO_GET_BOARDS_LISTS_BY_ID_BOARD | idBoard |
| 创建卡片 | TRELLO_ADD_CARDS | idList, name, desc, pos, due |
| 更新卡片 | TRELLO_UPDATE_CARDS_BY_ID_CARD | idCard, idList（用于移动） |
| 搜索卡片 | TRELLO_GET_SEARCH | query, modelTypes='cards' |
| 添加清单 | TRELLO_ADD_CARDS_CHECKLISTS_BY_ID_CARD | idCard, name |
| 添加评论 | TRELLO_ADD_CARDS_ACTIONS_COMMENTS_BY_ID_CARD | idCard, text |
| 分配成员 | TRELLO_ADD_CARDS_ID_MEMBERS_BY_ID_CARD | idCard, value（成员 ID） |
| 附加文件/URL | TRELLO_ADD_CARDS_ATTACHMENTS_BY_ID_CARD | idCard, url 或 file |
| 获取看板成员 | TRELLO_GET_BOARDS_MEMBERS_BY_ID_BOARD | idBoard |
| 批量读取 | TRELLO_GET_BATCH | urls（逗号分隔路径） |

## 适用场景
本技能适用于执行上述概览中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能
- 输出结果不能替代针对特定环境的验证、测试或专家审查
- 缺少必要输入、权限、安全边界或成功标准时，应停下来请求澄清
