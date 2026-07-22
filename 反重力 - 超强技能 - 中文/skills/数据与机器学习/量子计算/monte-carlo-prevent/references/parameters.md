# MCP 参数说明

Monte Carlo MCP 工具的重要参数详情。调用 API 时参考以避免常见错误。

---

## `getAlerts` — 使用 snake_case 参数

MCP 工具使用 Python snake_case，**而非** MC Web UI 中的 camelCase 参数：

```
✓ created_after    （不是 createdTime.after）
✓ created_before   （不是 createdTime.before）
✓ order_by         （不是 orderBy）
✓ table_mcons      （不是 tableMcons）
```

始终提供 `created_after` 和 `created_before`。最大时间窗口为 60 天。
需要时使用 `getCurrentTime()` 获取当前 ISO 时间戳。

---

## `search` — 查找正确的表标识符

MC 使用 MCON（Monte Carlo Object Names）作为表标识符。调用 `getTable`、`getAssetLineage` 或 `getAlerts` 前，始终先使用 `search` 将表名解析为 MCON。

```
search(query="orders_status") → 返回 mcon、full_table_id、warehouse
```
