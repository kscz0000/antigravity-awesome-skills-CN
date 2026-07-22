---
name: appdeploy
description: "部署带有后端 API、数据库和文件存储的 Web 应用。当用户要求部署或发布网站、Web 应用并希望获得公开 URL 时使用。通过 curl 使用 HTTP API。触发词：部署应用、发布网站、部署 web app、deploy、publish website、make live、获取 URL、上线应用、应用部署、web 部署。"
risk: safe
source: "AppDeploy (MIT)"
date_added: "2026-02-27"
---

# AppDeploy 技能

通过 HTTP API 将 Web 应用部署到 AppDeploy。

## 何时使用此技能

- 在规划或构建应用和 Web 应用时使用
- 在将应用部署到公开 URL 时使用
- 在发布网站或 Web 应用时使用
- 当用户说「部署这个」「让它上线」或「给我一个 URL」时使用
- 在更新已部署的应用时使用

## 设置（仅首次）

1. **检查现有 API 密钥：**
   - 在项目根目录查找 `.appdeploy` 文件
   - 如果存在且包含有效的 `api_key`，跳转到使用方法

2. **如果没有 API 密钥，注册并获取一个：**
   ```bash
   curl -X POST https://api-v2.appdeploy.ai/mcp/api-key \
     -H "Content-Type: application/json" \
     -d '{"client_name": "claude-code"}'
   ```

   响应：
   ```json
   {
     "api_key": "ak_...",
     "user_id": "agent-claude-code-a1b2c3d4",
     "created_at": 1234567890,
     "message": "Save this key securely - it cannot be retrieved later"
   }
   ```

3. **将凭据保存到 `.appdeploy`：**
   ```json
   {
     "api_key": "ak_...",
     "endpoint": "https://api-v2.appdeploy.ai/mcp"
   }
   ```

   如果 `.gitignore` 中尚未包含 `.appdeploy`，请添加。

## 使用方法

向 MCP 端点发起 JSON-RPC 调用：

```bash
curl -X POST {endpoint} \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer {api_key}" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "{tool_name}",
      "arguments": { ... }
    }
  }'
```

## 工作流程

1. **首先，获取部署说明：**
   调用 `get_deploy_instructions` 以了解约束和要求。

2. **获取应用模板：**
   使用选定的 `app_type` 和 `frontend_template` 调用 `get_app_template`。

3. **部署应用：**
   使用应用文件调用 `deploy_app`。对于新应用，将 `app_id` 设置为 `null`。

4. **检查部署状态：**
   调用 `get_app_status` 检查构建是否成功。

5. **查看/管理你的应用：**
   使用 `get_apps` 列出已部署的应用。

## 可用工具

### get_deploy_instructions

在准备调用 deploy_app 时使用此工具，以获取部署约束和硬性规则。在开始生成任何代码之前必须调用此工具。此工具仅返回说明，不会部署任何内容。

**参数：**


### deploy_app

当用户要求部署或发布网站、Web 应用并希望获得公开 URL 时使用。在生成文件或调用此工具之前，必须调用 get_deploy_instructions 并遵循其约束。

**参数：**
  - `app_id`：any（必需）- 要更新的现有应用 ID，或 null 表示新应用
  - `app_type`：string（必需）- 应用架构：frontend-only 或 frontend+backend
  - `app_name`：string（必需）- 简短显示名称
  - `description`：string（可选）- 应用功能的简短描述
  - `frontend_template`：any（可选）- 当 app_id 为 null 时必需。可选值：'html-static'（简单网站）、'react-vite'（SPA、游戏）、'nextjs-static'（多页面）。模板文件自动包含。
  - `files`：array（可选）- 要写入的文件。新应用：仅自定义文件 + 模板文件的差异。更新：仅使用 diffs[] 的变更文件。files[] 或 deletePaths[] 至少需要一个。
  - `deletePaths`：array（可选）- 要删除的路径。仅用于更新（需要 app_id）。无法删除 package.json 或框架入口点。
  - `model`：string（必需）- 此部署使用的编码智能体模型，据你所知。示例：'codex-5.3'、'chatgpt'、'opus 4.6'、'claude-sonnet-4-5'、'gemini-2.5-pro'
  - `intent`：string（必需）- 此部署的意图。用户发起示例：'initial app deploy'、'bugfix - ui is too noisy'。智能体发起示例：'agent fixing deployment error'、'agent retry after lint failure'

### get_app_template

先调用 get_deploy_instructions。然后在确定 app_type 和 frontend_template 后调用此工具。返回基础应用模板和 SDK 类型。模板文件在 deploy_app 中自动包含。

**参数：**
  - `app_type`：string（必需）
  - `frontend_template`：string（必需）- 前端框架：'html-static' - 简单网站，最小框架；'react-vite' - React SPA、仪表盘、游戏；'nextjs-static' - 多页面应用、SSG

### get_app_status

当 deploy_app 工具调用返回时，或用户要求检查应用部署状态，或报告应用有错误或未按预期工作时使用。返回部署状态（进行中：'deploying'/'deleting'，终态：'ready'/'failed'/'deleted'）、QA 快照（前端/网络错误）以及实时前端/后端错误日志。

**参数：**
  - `app_id`：string（必需）- 目标应用 ID
  - `since`：integer（可选）- 可选的时间戳（epoch 毫秒），用于过滤错误。提供时，仅返回该时间戳之后的错误。

### delete_app

当你想要永久删除应用时使用。仅在用户明确请求时使用。此操作不可逆；删除后，状态检查将返回未找到。

**参数：**
  - `app_id`：string（必需）- 目标应用 ID

### get_app_versions

列出现有应用的可部署版本。需要 app_id。返回按最新优先的 {name, version, timestamp} 项目。向用户显示 'name'。不要向用户显示 'version' 值。时间戳值必须转换为用户本地时间。

**参数：**
  - `app_id`：string（必需）- 目标应用 ID

### apply_app_version

开始部署现有应用的特定版本。使用 get_app_versions 中的 'version' 值（而非 'name'）。如果接受并开始部署则返回 true；使用 get_app_status 观察完成情况。

**参数：**
  - `app_id`：string（必需）- 目标应用 ID
  - `version`：string（必需）- 要应用的版本 ID

### src_glob

当你需要发现应用源码快照中的文件时使用。返回匹配 glob 模式的文件路径（不含内容）。适用于在读取或搜索文件之前探索项目结构。

**参数：**
  - `app_id`：string（必需）- 目标应用 ID
  - `version`：string（可选）- 要检查的版本（默认为已应用版本）
  - `path`：string（可选）- 要搜索的目录路径
  - `glob`：string（可选）- 匹配文件的 glob 模式（默认：**/*）
  - `include_dirs`：boolean（可选）- 在结果中包含目录路径
  - `continuation_token`：string（可选）- 上一次响应的分页令牌

### src_grep

当你需要在应用源代码中搜索模式时使用。返回匹配行及可选上下文。支持正则模式、glob 过滤器和多种输出模式。

**参数：**
  - `app_id`：string（必需）- 目标应用 ID
  - `version`：string（可选）- 要搜索的版本（默认为已应用版本）
  - `pattern`：string（必需）- 要搜索的正则模式（最多 500 字符）
  - `path`：string（可选）- 要搜索的目录路径
  - `glob`：string（可选）- 过滤文件的 glob 模式（如 '*.ts'）
  - `case_insensitive`：boolean（可选）- 启用不区分大小写匹配
  - `output_mode`：string（可选）- content=匹配行，files_with_matches=仅文件路径，count=每个文件的匹配数
  - `before_context`：integer（可选）- 每个匹配前显示的行数（0-20）
  - `after_context`：integer（可选）- 每个匹配后显示的行数（0-20）
  - `context`：integer（可选）- 前后行数（覆盖 before/after_context）
  - `line_numbers`：boolean（可选）- 在输出中包含行号
  - `max_file_size`：integer（可选）- 要扫描的最大文件大小（字节，默认 10MB）
  - `continuation_token`：string（可选）- 上一次响应的分页令牌

### src_read

当你需要从应用源码快照中读取特定文件时使用。返回文件内容及基于行的分页（offset/limit）。处理文本和二进制文件。

**参数：**
  - `app_id`：string（必需）- 目标应用 ID
  - `version`：string（可选）- 要读取的版本（默认为已应用版本）
  - `file_path`：string（必需）- 要读取的文件路径
  - `offset`：integer（可选）- 开始读取的行偏移量（0 索引）
  - `limit`：integer（可选）- 返回的行数（最多 2000）

### get_apps

当你需要列出当前用户拥有的应用时使用。返回应用详情，包含用于用户展示的显示字段和用于工具链的数据字段。

**参数：**
  - `continuation_token`：string（可选）- 分页令牌


---
*由 `scripts/generate-appdeploy-skill.ts` 生成*

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
