---
name: odoo-xml-views-builder
description: "Odoo XML 视图构建专家：支持 Form、List、Kanban、Search、Calendar 和 Graph 视图。为 Odoo 14-17 生成符合正确可见性语法的 XML。当用户要求构建或审查 Odoo XML 视图时使用。"
risk: safe
source: "self"
---

# Odoo XML 视图构建器

## 概述

本技能用于生成和审查 Odoo XML 视图定义，涵盖 Kanban、Form、List、Search、Calendar 和 Graph 视图。它理解可见性修饰符、`groups`、`domain`、`context` 以及 widget 的用法，适用于 Odoo 14–17 各版本，包括从 `attrs`（v14–16）到内联表达式（v17+）的迁移。

## 使用场景

- 为自定义模型创建新的 form 或 list 视图。
- 向现有视图添加字段、选项卡或智能按钮。
- 构建带有颜色编码或进度条的 Kanban 视图。
- 创建带有筛选器和分组选项的搜索视图。

## 工作原理

1. **激活**：提及 `@odoo-xml-views-builder` 并描述你想要的视图。
2. **生成**：获取完整的、可直接粘贴的 XML 视图定义。
3. **审查**：粘贴现有 XML 并获取常见错误的修复建议。

## 示例

### 示例 1：带选项卡的 Form 视图

```xml
<record id="view_hospital_patient_form" model="ir.ui.view">
    <field name="name">hospital.patient.form</field>
    <field name="model">hospital.patient</field>
    <field name="arch" type="xml">
        <form string="Patient">
            <header>
                <button name="action_confirm" string="Confirm"
                    type="object" class="btn-primary"
                    invisible="state != 'draft'"/>
                <field name="state" widget="statusbar"
                    statusbar_visible="draft,confirmed,done"/>
            </header>
            <sheet>
                <div class="oe_title">
                    <h1><field name="name" placeholder="Patient Name"/></h1>
                </div>
                <notebook>
                    <page string="General Info">
                        <group>
                            <field name="birth_date"/>
                            <field name="doctor_id"/>
                        </group>
                    </page>
                </notebook>
            </sheet>
            <chatter/>
        </form>
    </field>
</record>
```

### 示例 2：Kanban 视图

```xml
<record id="view_hospital_patient_kanban" model="ir.ui.view">
    <field name="name">hospital.patient.kanban</field>
    <field name="model">hospital.patient</field>
    <field name="arch" type="xml">
        <kanban default_group_by="state" class="o_kanban_small_column">
            <field name="name"/>
            <field name="state"/>
            <field name="doctor_id"/>
            <templates>
                <t t-name="kanban-card">
                    <div class="oe_kanban_content">
                        <strong><field name="name"/></strong>
                        <div>Doctor: <field name="doctor_id"/></div>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

## 最佳实践

- ✅ **推荐：** 使用内联 `invisible="condition"`（Odoo 17+）代替 `attrs` 来实现显示/隐藏逻辑。
- ✅ **推荐：** 仅在目标为 Odoo 14–16 时使用 `attrs="{'invisible': [...]}"`——该写法在 v17 中已弃用。
- ✅ **推荐：** 始终为视图记录设置 `string` 属性，便于调试。
- ✅ **推荐：** 使用 `<chatter/>`（v17）或 `<div class="oe_chatter">` + 字段标签（v16 及以下）来实现活动跟踪。
- ❌ **禁止：** 在 Odoo 17 中使用 `attrs`——该写法已完全弃用，会在日志中产生警告。
- ❌ **禁止：** 在视图 XML 中放置业务逻辑——应将其保留在 Python 模型方法中。
- ❌ **禁止：** 在视图中使用硬编码的 `domain` 字符串，当模型上有 `domain` 字段可以动态使用时。

## 限制

- 不涵盖 **OWL JavaScript widgets** 或客户端组件开发。
- **搜索面板视图**（`<searchpanel>`）未完全涵盖——需要前端知识。
- 不涉及**网站 QWeb 视图**——请使用 `@odoo-qweb-templates`。
- **Cohort 和 Map 视图**（仅限企业版）不在本技能范围内。