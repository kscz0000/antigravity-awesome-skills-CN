---
name: odoo-migration-helper
description: "Odoo 自定义模块跨版本迁移的分步指南（v14→v15→v16→v17），涵盖 API 变更、废弃方法和视图迁移。当用户要求迁移 Odoo 模块、升级 Odoo 版本或修复版本兼容性问题时使用。"
risk: safe
source: "self"
---

# Odoo 迁移助手

## 概述

Odoo 模块跨大版本迁移需要谨慎处理 API 变更、废弃方法、字段重命名和新视图语法。本技能系统性地引导你完成迁移过程，覆盖版本间最常见的破坏性变更。

## 使用场景

- 将自定义模块从 Odoo 14/15/16 升级到更高版本
- 在运行 `odoo-upgrade` 前获取检查清单
- 修复版本升级后的废弃警告
- 了解两个特定 Odoo 版本之间的变更

## 工作流程

1. **激活**：提及 `@odoo-migration-helper`，指定源版本和目标版本，粘贴模块代码
2. **分析**：获取破坏性变更列表及修复前后的代码对比
3. **验证**：获得针对模块功能的迁移检查清单

## 各版本关键迁移变更

### Odoo 16 → 17

| 主题 | 旧版 (v16) | 新版 (v17) |
|---|---|---|
| 视图可见性 | `attrs="{'invisible': [...]}"` | `invisible="condition"` |
| Chatter | `<div class="oe_chatter">` | `<chatter/>` |
| 必填/只读 | `attrs="{'required': [...]}"` | `required="condition"` |
| Python 最低版本 | 3.10 | 3.10+ |
| JS 模块 | 旧版 `define(['web.core'])` | ES module `import` 语法 |

### Odoo 15 → 16

| 主题 | 旧版 (v15) | 新版 (v16) |
|---|---|---|
| 网站发布标志 | `website_published = True` | `is_published = True` |
| 邮件别名 | 公司上的 `alias_domain` | 迁移至 `mail.alias.domain` 模型 |
| 报表渲染 | `_render_qweb_pdf()` | `_render_qweb_pdf()`（相同，但签名已变更） |
| 会计分录 | `account.move.line` 分组 | 行聚合规则已更新 |
| 邮件线程 | `mail_thread_id` | 已废弃；使用 `message_ids` |

## 示例

### 示例 1：将 `attrs` 可见性迁移至 Odoo 17

```xml
<!-- v16 — 基于域的 attrs -->
<field name="discount" attrs="{'invisible': [('product_type', '!=', 'service')]}"/>
<field name="discount" attrs="{'required': [('state', '=', 'sale')]}"/>

<!-- v17 — 内联 Python 表达式 -->
<field name="discount" invisible="product_type != 'service'"/>
<field name="discount" required="state == 'sale'"/>
```

### 示例 2：迁移 Chatter 块

```xml
<!-- v16 -->
<div class="oe_chatter">
    <field name="message_follower_ids"/>
    <field name="activity_ids"/>
    <field name="message_ids"/>
</div>

<!-- v17 -->
<chatter/>
```

### 示例 3：迁移 website_published 标志（v15 → v16）

```python
# v15
record.website_published = True

# v16+
record.is_published = True
```

## 最佳实践

- ✅ **推荐**：每个版本推送生产前，用 `--update=your_module` 测试
- ✅ **推荐**：使用官方 [Odoo 升级指南](https://upgrade.odoo.com/) 获取自动预升级分析报告
- ✅ **推荐**：社区模块需检查 OCA 迁移说明和模块的 `HISTORY.rst`
- ✅ **推荐**：迁移后运行 `npm run validate`，尽早发现 manifest 或 frontmatter 问题
- ❌ **避免**：跳过中间版本——必须按 v14→v15→v16→v17 顺序，不可跳跃
- ❌ **避免**：忘记更新 `__manifest__.py` 中的 `version`（如 `17.0.1.0.0`）
- ❌ **避免**：假设 OCA 模块已就绪——需检查其 GitHub 分支是否支持目标版本

## 限制

- 仅覆盖 **v14 至 v17**——不涉及 v13 及更早版本（manifest 前时代的模块结构完全不同）
- **Odoo.sh 自动升级**路径有额外步骤，此处未覆盖；请参阅 Odoo.sh 文档
- **企业版专属模块**（如 `account_accountant`、`sign`）可能存在未记录的破坏性变更；需在预发环境使用企业版许可证测试
- JavaScript OWL 组件迁移（v15 Legacy → v16 OWL）是复杂话题，本技能未完全覆盖