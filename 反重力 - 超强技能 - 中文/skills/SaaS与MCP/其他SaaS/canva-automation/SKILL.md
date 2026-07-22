---
name: canva-automation
description: "通过 Rube MCP (Composio) 自动化 Canva 任务：设计、导出、文件夹、品牌模板、自动填充。始终先搜索工具获取当前 schema。当用户要求'自动化 Canva 操作'、'Canva 设计自动化'、'批量导出 Canva 设计'、'Canva 模板自动填充'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 通过 Rube MCP 实现 Canva 自动化

通过 Composio 的 Canva 工具包和 Rube MCP 自动化 Canva 设计操作。

## 前置条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 建立活跃的 Canva 连接，toolkit 参数为 `canva`
- 始终先调用 `RUBE_SEARCH_TOOLS` 获取当前工具 schema

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——添加端点即可使用。


1. 确认 `RUBE_SEARCH_TOOLS` 有响应，验证 Rube MCP 可用
2. 调用 `RUBE_MANAGE_CONNECTIONS`，toolkit 参数为 `canva`
3. 如果连接状态不是 ACTIVE，按照返回的认证链接完成 Canva OAuth
4. 确认连接状态显示 ACTIVE 后再运行任何工作流

## 核心工作流

### 1. 列出和浏览设计

**适用场景**：用户想查找现有设计或浏览 Canva 资源库

**工具调用顺序**：
1. `CANVA_LIST_USER_DESIGNS` - 列出所有设计，支持可选过滤 [必需]

**关键参数**：
- `query`：按名称过滤设计的搜索词
- `continuation`：上一次响应返回的分页 token
- `ownership`：按所有权过滤，可选 'owned'、'shared' 或 'any'
- `sort_by`：排序字段（如 'modified_at'、'title'）

**注意事项**：
- 结果分页返回；持续跟踪 `continuation` token 直到不再出现
- 已删除的设计可能短暂显示；需检查设计状态
- 搜索基于子串匹配，不支持模糊匹配

### 2. 创建和设计

**适用场景**：用户想从零开始或基于模板创建新的 Canva 设计

**工具调用顺序**：
1. `CANVA_ACCESS_USER_SPECIFIC_BRAND_TEMPLATES_LIST` - 浏览可用的品牌模板 [可选]
2. `CANVA_CREATE_CANVA_DESIGN_WITH_OPTIONAL_ASSET` - 创建新设计 [必需]

**关键参数**：
- `design_type`：设计类型（如 'Presentation'、'Poster'、'SocialMedia'）
- `title`：新设计的名称
- `asset_id`：可选，要包含在设计中的素材
- `width` / `height`：自定义尺寸（像素）

**注意事项**：
- 设计类型必须完全匹配 Canva 预定义类型
- 自定义尺寸有最小和最大限制
- 素材必须先通过 CANVA_CREATE_ASSET_UPLOAD_JOB 上传后才能引用

### 3. 上传素材

**适用场景**：用户想将图片或文件上传到 Canva 用于设计

**工具调用顺序**：
1. `CANVA_CREATE_ASSET_UPLOAD_JOB` - 发起素材上传 [必需]
2. `CANVA_FETCH_ASSET_UPLOAD_JOB_STATUS` - 轮询直到上传完成 [必需]

**关键参数**：
- `name`：素材的显示名称
- `url`：要上传文件的公开 URL（用于基于 URL 的上传）
- `job_id`：步骤 1 返回的上传作业 ID（用于状态轮询）

**注意事项**：
- 上传是异步的；必须轮询作业状态直到完成
- 支持的格式包括 PNG、JPG、SVG、MP4、GIF
- 有文件大小限制；大文件处理时间更长
- CREATE 返回的 `job_id` 是状态轮询所需的 ID
- 状态值：'in_progress'、'success'、'failed'

### 4. 导出设计

**适用场景**：用户想将 Canva 设计下载或导出为 PDF、PNG 或其他格式

**工具调用顺序**：
1. `CANVA_LIST_USER_DESIGNS` - 找到要导出的设计 [前置步骤]
2. `CANVA_CREATE_CANVA_DESIGN_EXPORT_JOB` - 启动导出流程 [必需]
3. `CANVA_GET_DESIGN_EXPORT_JOB_RESULT` - 轮询直到导出完成并获取下载 URL [必需]

**关键参数**：
- `design_id`：要导出的设计 ID
- `format`：导出格式（'pdf'、'png'、'jpg'、'svg'、'mp4'、'gif'、'pptx'）
- `pages`：要导出的特定页码（数组）
- `quality`：导出质量（'regular'、'high'）
- `job_id`：用于轮询状态的导出作业 ID

**注意事项**：
- 导出是异步的；必须轮询作业结果直到完成
- 完成导出后的下载 URL 会在有限时间后过期
- 页面较多的大型设计导出时间更长
- 并非所有格式都支持所有设计类型（如 MP4 仅用于动画）
- 轮询间隔：状态检查之间等待 2-3 秒

### 5. 用文件夹组织

**适用场景**：用户想创建文件夹或将设计整理到文件夹中

**工具调用顺序**：
1. `CANVA_POST_FOLDERS` - 创建新文件夹 [必需]
2. `CANVA_MOVE_ITEM_TO_SPECIFIED_FOLDER` - 将设计移入文件夹 [可选]

**关键参数**：
- `name`：文件夹名称
- `parent_folder_id`：父文件夹，用于嵌套组织
- `item_id`：要移动的设计或素材 ID
- `folder_id`：目标文件夹 ID

**注意事项**：
- 同一父文件夹内的文件夹名称必须唯一
- 在文件夹之间移动项目会立即更新其位置
- 根级文件夹没有 parent_folder_id

### 6. 品牌模板自动填充

**适用场景**：用户想通过填充品牌模板占位符来生成设计

**工具调用顺序**：
1. `CANVA_ACCESS_USER_SPECIFIC_BRAND_TEMPLATES_LIST` - 列出可用的品牌模板 [必需]
2. `CANVA_INITIATE_CANVA_DESIGN_AUTOFILL_JOB` - 用数据启动自动填充 [必需]

**关键参数**：
- `brand_template_id`：要使用的品牌模板 ID
- `title`：生成设计的标题
- `data`：占位符名称到替换值的键值映射

**注意事项**：
- 模板占位符必须完全匹配（区分大小写）
- 自动填充是异步的；需轮询等待完成
- 只有品牌模板支持自动填充，普通设计不支持
- 数据值必须匹配每个占位符的预期类型（文本、图片 URL）

## 常用模式

### 异步作业模式

许多 Canva 操作是异步的：
```
1. Initiate job (upload, export, autofill) -> get job_id
2. Poll status endpoint with job_id every 2-3 seconds
3. Check for 'success' or 'failed' status
4. On success, extract result (asset_id, download_url, design_id)
```

### ID 解析

**设计名称 → 设计 ID**：
```
1. Call CANVA_LIST_USER_DESIGNS with query=design_name
2. Find matching design in results
3. Extract id field
```

**品牌模板名称 → 模板 ID**：
```
1. Call CANVA_ACCESS_USER_SPECIFIC_BRAND_TEMPLATES_LIST
2. Find template by name
3. Extract brand_template_id
```

### 分页

- 检查响应中的 `continuation` token
- 在下一次请求的 `continuation` 参数中传入该 token
- 持续执行直到 `continuation` 不存在或为空

## 已知陷阱

**异步操作**：
- 上传、导出和自动填充都是异步的
- 始终轮询作业状态；不要假设立即完成
- 导出的下载 URL 会过期；及时使用

**素材管理**：
- 素材必须先上传才能在设计中使用
- 上传作业必须达到 'success' 状态后 asset_id 才有效
- 支持的格式各异；查阅 Canva 文档了解当前限制

**速率限制**：
- Canva API 每个端点都有速率限制
- 批量操作时实现指数退避
- 尽可能批量处理操作以减少 API 调用

**响应解析**：
- 响应数据可能嵌套在 `data` 键下
- 作业状态响应根据完成状态包含不同字段
- 防御性解析，为可选字段提供回退

## 快速参考

| 任务 | 工具标识 | 关键参数 |
|------|----------|----------|
| 列出设计 | CANVA_LIST_USER_DESIGNS | query, continuation |
| 创建设计 | CANVA_CREATE_CANVA_DESIGN_WITH_OPTIONAL_ASSET | design_type, title |
| 上传素材 | CANVA_CREATE_ASSET_UPLOAD_JOB | name, url |
| 检查上传 | CANVA_FETCH_ASSET_UPLOAD_JOB_STATUS | job_id |
| 导出设计 | CANVA_CREATE_CANVA_DESIGN_EXPORT_JOB | design_id, format |
| 获取导出 | CANVA_GET_DESIGN_EXPORT_JOB_RESULT | job_id |
| 创建文件夹 | CANVA_POST_FOLDERS | name, parent_folder_id |
| 移入文件夹 | CANVA_MOVE_ITEM_TO_SPECIFIED_FOLDER | item_id, folder_id |
| 列出模板 | CANVA_ACCESS_USER_SPECIFIC_BRAND_TEMPLATES_LIST | (无) |
| 模板填充 | CANVA_INITIATE_CANVA_DESIGN_AUTOFILL_JOB | brand_template_id, data |

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
