# shadcn MCP 服务器

CLI 包含一个 MCP 服务器，让 AI 助手可以搜索、浏览、查看和安装注册表中的组件。

---

## 设置

```bash
shadcn mcp        # 启动 MCP 服务器（stdio）
shadcn mcp init   # 为编辑器写入配置
```

编辑器配置文件：

| 编辑器 | 配置文件 |
|--------|------------|
| Claude Code | `.mcp.json` |
| Cursor | `.cursor/mcp.json` |
| VS Code | `.vscode/mcp.json` |
| OpenCode | `opencode.json` |
| Codex | `~/.codex/config.toml`（手动） |

---

## 工具

> **提示：** MCP 工具处理注册表操作（搜索、查看、安装）。对于项目配置（别名、框架、Tailwind 版本），使用 `npx shadcn@latest info` —— 没有 MCP 等效功能。

### `shadcn:get_project_registries`

从 `components.json` 返回注册表名称。如果不存在 `components.json` 则报错。

**输入：** 无

### `shadcn:list_items_in_registries`

列出一个或多个注册表中的所有项目。

**输入：** `registries`（string[]）、`limit`（number，可选）、`offset`（number，可选）

### `shadcn:search_items_in_registries`

跨注册表模糊搜索。

**输入：** `registries`（string[]）、`query`（string）、`limit`（number，可选）、`offset`（number，可选）

### `shadcn:view_items_in_registries`

查看项目详情包括完整文件内容。

**输入：** `items`（string[]）—— 如 `["@shadcn/button", "@shadcn/card"]`

### `shadcn:get_item_examples_from_registries`

查找使用示例和演示及源代码。

**输入：** `registries`（string[]）、`query`（string）—— 如 `"accordion-demo"`、`"button example"`

### `shadcn:get_add_command_for_items`

返回 CLI 安装命令。

**输入：** `items`（string[]）—— 如 `["@shadcn/button"]`

### `shadcn:get_audit_checklist`

返回验证组件的检查清单（导入、依赖、lint、TypeScript）。

**输入：** 无

---

## 配置注册表

注册表在 `components.json` 中设置。`@shadcn` 注册表始终内置。

```json
{
  "registries": {
    "@acme": "https://acme.com/r/{name}.json",
    "@private": {
      "url": "https://private.com/r/{name}.json",
      "headers": { "Authorization": "Bearer ${MY_TOKEN}" }
    }
  }
}
```

- 名称必须以 `@` 开头。
- URL 必须包含 `{name}`。
- `${VAR}` 引用从环境变量解析。

社区注册表索引：`https://ui.shadcn.com/r/registries.json`
