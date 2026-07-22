## 故障排查

### MCP 连接失败：
```bash
# 验证服务器是否可达
curl -s -o /dev/null -w "%{http_code}" https://integrations.getmontecarlo.com/mcp/
```

**若使用插件（OAuth）：** 在 Claude Code 中运行 `/mcp`，选择 `monte-carlo` 服务器，重新认证。若浏览器流程未完成，从浏览器地址栏复制回调 URL 粘贴到 Claude Code 中出现的 URL 提示中。

**传统方式（基于 header 的认证，适用于无 HTTP 传输的 MCP 客户端）：** 检查 MCP 配置中 `x-mcd-id` 和 `x-mcd-token` 是否正确设置。密钥格式为 `<KEY_ID>:<KEY_SECRET>` — 它们分别放在两个独立的 header 中。


### 监控器创建错误：

**`montecarlo monitors apply` 失败并提示 "Unknown field"：**
监控器定义文件必须以 `montecarlo:` 作为根键 — 不要直接复制 MCP 工具输出的 `validation:` 或 `custom_sql:` 内容。按工作流 2 中展示的 `montecarlo: > custom_sql:` 结构重新格式化。

**`montecarlo monitors apply` 失败并提示 "Not a Monte Carlo project"：**
确保工作目录中存在 `montecarlo.yml`（项目配置文件）。此文件仅包含 `version`、`namespace` 和 `default_resource` — 不包含监控器定义。

**`createValidationMonitorMac` 失败并出现 Snowflake 错误：**
此工具会针对实际表验证条件 SQL。若列尚不存在（例如在部署模型变更前编写监控器），改用 `createCustomSqlMonitorMac` 并提供显式 SQL 查询。
