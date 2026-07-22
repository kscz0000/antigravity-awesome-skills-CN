---
name: odoo-upgrade-advisor
description: "Odoo 版本升级分步顾问：升级前检查清单、社区版与企业版升级路径、OCA 模块兼容性检查，以及升级后验证。当用户要求'Odoo升级'、'Odoo版本迁移'、'OpenUpgrade'或'升级验证'时使用。"
risk: safe
source: "self"
---

# Odoo 升级顾问

## 概述

Odoo 主版本之间的升级（如 v15 → v16 → v17）需要仔细的准备、测试和验证。本技能提供结构化的升级前检查清单，引导你使用升级工具（Odoo Upgrade Service 和 OpenUpgrade），并给出升级后验证流程。

## 使用场景

- 规划 Odoo 主版本升级。
- 确定哪些自定义模块需要迁移。
- 在生产环境之前先在预发布环境运行升级。
- 升级后验证系统。

## 工作方式

1. **激活**：提及 `@odoo-upgrade-advisor`，说明当前版本和目标版本。
2. **规划**：获取完整的升级路线图和风险评估。
3. **执行**：获取逐步升级命令序列。

## 升级路径

| 从 | 到 | 是否支持 | 工具 |
|---|---|---|---|
| v16 | v17 | ✅ 直接升级 | Odoo Upgrade Service / OpenUpgrade |
| v15 | v16 | ✅ 直接升级 | Odoo Upgrade Service / OpenUpgrade |
| v14 | v15 | ✅ 直接升级 | Odoo Upgrade Service / OpenUpgrade |
| v14 | v17 | ⚠️ 多跳升级 | v14→v15→v16→v17（不可跳过） |
| v13 及更早 | 任意版本 | ❌ 不支持 | 需要手动迁移 |

## 示例

### 示例 1：升级前检查清单

```text
BEFORE YOU START:
  ☑ 1. List all installed modules (Settings → Technical → Modules)
        Export to CSV and review for custom/OCA modules
  ☑ 2. Check OCA compatibility matrix for each community module
        https://github.com/OCA/maintainer-tools/wiki/Migration-Status
  ☑ 3. Take a full backup (database + filestore) — your restore point
  ☑ 4. Clone production to a staging environment
  ☑ 5. Run the Odoo Upgrade pre-analysis:
        https://upgrade.odoo.com/ → Upload DB → Review breaking changes report
  ☑ 6. Review custom modules against migration notes
        (use @odoo-migration-helper for per-module analysis)
  ☑ 7. Upgrade and test in staging → Fix all errors → Re-test
  ☑ 8. Schedule a production maintenance window
  ☑ 9. Notify users of scheduled downtime
  ☑ 10. Perform production upgrade → Validate → Go/No-Go decision
```

### 示例 2：使用 OpenUpgrade 进行社区版升级

```bash
# Clone OpenUpgrade for the TARGET version (e.g., upgrading to v17)
git clone https://github.com/OCA/OpenUpgrade.git \
  --branch 17.0 \
  --single-branch \
  /opt/openupgrade

# Run the migration against your staging database
python3 /opt/openupgrade/odoo-bin \
  --update all \
  --database odoo_staging \
  --config /etc/odoo/odoo.conf \
  --stop-after-init \
  --load openupgrade_framework

# Review the log for errors before touching production
tail -200 /var/log/odoo/odoo.log | grep -E "ERROR|WARNING|Traceback"
```

### 示例 3：升级后验证检查清单

```text
After upgrading, validate these critical areas before going live:

Accounting:
  ☑ Trial Balance totals match the pre-upgrade snapshot
  ☑ Open invoices, bills, and payments are accessible
  ☑ Bank reconciliation can be performed on a test statement

Inventory:
  ☑ Stock valuation report matches pre-upgrade (run Inventory Valuation)
  ☑ Open Purchase Orders and Sale Orders are visible

HR / Payroll:
  ☑ All employee records are intact
  ☑ Payslips from the last 3 months are accessible and correct

Custom Modules:
  ☑ Every custom module loaded without ImportError or XML error
  ☑ Run the critical business workflows end-to-end:
      Create sale order → confirm → deliver → invoice → payment

Users & Security:
  ☑ User logins work correctly
  ☑ Access rights are preserved (spot-check 3-5 users)
```

## 最佳实践

- ✅ **推荐：** 始终在**生产环境的副本**（预发布环境）上先行升级——切勿直接在生产实例操作。
- ✅ **推荐：** 在新版本**完全验证并签字确认**之前，保持旧版本运行。
- ✅ **推荐：** 查看 OCA 的迁移状态页面：[OCA Migration Status](https://github.com/OCA/maintainer-tools/wiki/Migration-Status)
- ✅ **推荐：** 使用 [Odoo Upgrade Service](https://upgrade.odoo.com/) 的预分析报告，在**编写任何代码之前**获取破坏性变更列表。
- ❌ **禁止：** 跳过中间版本——Odoo 要求逐版升级（v14→v15→v16→v17）。
- ❌ **禁止：** 同时升级自定义模块和 Odoo 核心——先适配 Odoo 核心，再修复自定义模块。
- ❌ **禁止：** 直接对生产环境运行 OpenUpgrade——务必先在预发布副本上测试。

## 局限性

- 仅覆盖 **v14–v17**。v13 及更早版本的模块结构根本不同，需要手动迁移。
- **企业版专属模块变更**（如 `sign`、`account_accountant`）可能存在未记录的破坏性变更，OpenUpgrade 不包含这些内容。
- **Odoo.sh** 的自动升级路径有单独的工作流（通过 Odoo.sh 仪表板管理），本技能不涉及。
- OWL JavaScript 组件迁移（旧版 widget → OWL v16+）属于复杂的前端课题，超出本技能范围。
