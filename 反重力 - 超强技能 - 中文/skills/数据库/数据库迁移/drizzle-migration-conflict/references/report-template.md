# 报告模板

本模板用于诊断与修复建议。报告应保持简短、基于证据。

## 结论取值

- `NO_CONFLICT_FOUND` — 根据现有证据，未发现迁移冲突或结构不一致。
- `SAFE_TO_REGENERATE` — 冲突已厘清，schema 源已解决，建议的下一步是丢弃已生成产物并重新生成迁移。
- `NEEDS_USER_CONFIRMATION` — 已存在修复路径，但破坏性步骤或分支侧决策需要用户确认。
- `BLOCKED_BY_AMBIGUITY` — 迁移结构、真源分支、schema 状态或迁移目录无法被安全地确定。

## 模板

````markdown
# Drizzle Migration Conflict Report

Conclusion: <NO_CONFLICT_FOUND | SAFE_TO_REGENERATE | NEEDS_USER_CONFIRMATION | BLOCKED_BY_AMBIGUITY>
Mode: <diagnose | repair | ci-hardening | explain>

## Detected Structure
- Migration directory: `<path>`
- Structure: <legacy | folder-based | mixed | unknown>
- Drizzle Kit version: <version or unable to verify>
- Git state: <clean | dirty | active merge | active rebase | unable to verify>

## Conflict State
- <confirmed conflict or inconsistency with file paths>
- <journal/snapshot/SQL mismatch, non-commutative check, or conflict marker evidence>

## Recommended Path
- <safe next step>
- <why this path preserves schema intent and migration history>

## Commands
```bash
# Read-only commands first.
<commands>

# Destructive commands only if confirmed by the user.
<commands requiring confirmation>
```

## Files At Risk
- `<path>` - <why it may be discarded or regenerated>

## Validation
- <drizzle-kit check or project script>
- <helper script command>
- <typecheck/test command if relevant>

## Unable To Verify
- <missing version, unavailable branch, unknown migration path, or external docs not refreshed>
````

## 报告规则

- 将破坏性命令放在明确标注的代码块中。
- 除非已确认合并/变基方向、真源分支和具体文件路径，否则不要输出 `--ours` 或 `--theirs` 命令。否则请使用 `BLOCKED_BY_AMBIGUITY`。
- 如果项目有多个 Drizzle 配置，请独立报告每个输出。
- 如果未发现冲突但工作区是脏的，请说明未对未提交文件进行修复。
- 不要包含与用户冲突无关的"检查清单"分类项。
- 对密钥做脱敏处理。报告中不得包含数据库 URL、密码、令牌或连接字符串。当某项配置或环境值有影响时，仅描述其是否指向类生产目标，并将该值记为 `<redacted>`。
