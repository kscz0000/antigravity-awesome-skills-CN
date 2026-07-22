# 发布前审查报告模板

使用此模板生成最终报告。可在必要时将标题翻译为用户语言，但保持相同的章节、优先级标签、结论值和发现字段。

## 优先级定义

- `P0` — 阻塞发布。生产部署可能失败、损坏数据、泄露密钥、破坏兼容性或缺少必需的手动操作。
- `P1` — 高风险，发布前必须确认。证据表明存在生产依赖、迁移、配置、缓存、队列、资源或服务顺序风险。
- `P2` — 中等风险或模糊缺口。不确定是否阻塞，但 diff 引入了不确定性，发布前应检查。
- `P3` — 低风险备注。除非用户要求完整审计日志，否则不在主报告中包含 P3。

## 结论值

- `BLOCKED` — 存在至少一个 P0 发现。
- `NEEDS_CONFIRMATION` — 未发现 P0，但有一个或多个 P1/P2 项需要确认。
- `NO_BLOCKER_FOUND` — 从可用证据中未发现 P0-P2 发现或发布确认项。中性验证限制可单独列出。

## 发现与无法验证的区分

- 将与 diff 关联的生产风险放入"发现"。例如：新增环境变量但生产值无法验证、schema 变更且迁移执行状态不明、新队列的基础设施未确认。
- 任何 P1 或 P2 发现意味着结论为 `NEEDS_CONFIRMATION`，除非 P0 使其变为 `BLOCKED`。
- 仅将中性工具或访问限制放入"无法验证"。例如：远程 PR 访问不可用、部署平台访问不可用或负责人推断失败但无特定发布关键变更。
- 若访问/工具限制阻碍了发布关键 diff 变更的确认，将其提升为 P1/P2 发现而非仅留在"无法验证"中。

## 负责人推断

- 优先对变更行使用 `git blame` 确定文件和行。
- 若 blame 不可用或具有误导性，使用 `git log --format="%h %an %s" -- <path>`。
- 若多个 commit 贡献了同一发布风险，列出所有相关作者名。
- 将负责人标记为"推断"，不暴露邮箱地址。
- 若无法推断负责人，写 `Unknown (not inferable from local git evidence)`。

## 密钥脱敏

- 绝不打印密钥值（即使部分打印），除非值已是无害占位符如 `example`、`changeme` 或 `REDACTED`。
- 报告密钥时包含：路径、行号、变量/key 名称、类型和脱敏提示。
- 示例：`config/prod.env:12` - `PAYMENT_API_KEY`，疑似 API key，值已脱敏。
- 不将 PEM 块、JWT、cookie、session ID、私钥、密码、证书或云凭据粘贴到报告中。

## 最终报告格式

```markdown
# Production Release Readiness Review

## Scope
- Range: <base>..<head> | PR <number> | latest 5 commits fallback
- Current branch: <branch>
- Head commit: <hash>
- Compared from: <tag/hash/pr-base>
- Commit count: <count>
- Dirty worktree: <yes/no and short note>
- Commands used: <short list of read-only commands>

## Conclusion
`BLOCKED` | `NEEDS_CONFIRMATION` | `NO_BLOCKER_FOUND`

## Findings
| Priority | Module | Finding | Evidence | Inferred owner | Risk | Recommended action |
| --- | --- | --- | --- | --- | --- | --- |
| P0/P1/P2 | <area/service> | <short issue> | <file:line or commit/range> | <name(s) or unknown> | <why it matters> | <release action> |

## Deployment Order / Release Actions
- <Only include when relevant. State service order, migrations, queue/cache/resource actions, and compatibility constraints.>

## Unable To Verify
- <Tooling, auth, remote, production-config, or repository limits that prevent confirmation.>
```

## 发现编写规则

- 每个发现保持可操作且简短。
- 仅包含 P0-P2 或明确需要确认的风险。
- 不包含正常通过的类别，如"数据库 OK"或"安全 OK"。
- 使用证据驱动的措辞："schema 变更但无对应迁移文件"优于"可能缺少迁移"。
- 若风险模糊，明确说明发布前必须确认什么。
- 若无发现，省略"发现"表格并写：
  `No P0-P2 release blockers or confirmation items were found from the available repository evidence.`