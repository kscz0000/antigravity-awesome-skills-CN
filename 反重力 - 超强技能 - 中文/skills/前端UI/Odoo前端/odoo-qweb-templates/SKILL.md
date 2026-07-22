---
name: odoo-qweb-templates
description: "Odoo QWeb 模板专家，适用于 PDF 报表、邮件模板和网站页面。涵盖 t-if、t-foreach、t-field 和报表操作。当用户要求'odoo-qweb-templates'时使用。"
risk: safe
source: "self"
---

# Odoo QWeb Templates

## 概述

QWeb 是 Odoo 的主要模板引擎，用于 PDF 报表、网站页面和邮件模板。本技能可生成结构正确、指令规范、支持翻译并绑定报表操作的 QWeb XML。

## 何时使用本技能

- 创建自定义 PDF 报表（发票、发货单、证书）。
- 构建由工作流操作触发的 QWeb 邮件模板。
- 设计包含动态内容的 Odoo 网站页面。
- 调试 QWeb 渲染错误（`t-if`、`t-foreach` 问题）。

## 使用方式

1. **激活**：提及 `@odoo-qweb-templates` 并描述所需的报表或模板。
2. **生成**：获得完整的 `ir.actions.report` 记录和 QWeb 模板。
3. **调试**：粘贴有问题的模板，定位并修复渲染问题。

## 示例

### 示例 1：自定义 PDF 报表

```xml
<!-- Report Action -->
<record id="action_report_patient_card" model="ir.actions.report">
    <field name="name">Patient Card</field>
    <field name="model">hospital.patient</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">hospital_management.report_patient_card</field>
    <field name="binding_model_id" ref="model_hospital_patient"/>
</record>

<!-- QWeb Template -->
<template id="report_patient_card">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc">
            <t t-call="web.external_layout">
                <div class="page">
                    <h2>Patient Card</h2>
                    <table class="table table-bordered">
                        <tr>
                            <td><strong>Name:</strong></td>
                            <td><t t-field="doc.name"/></td>
                        </tr>
                        <tr>
                            <td><strong>Doctor:</strong></td>
                            <td><t t-field="doc.doctor_id.name"/></td>
                        </tr>
                        <tr>
                            <td><strong>Status:</strong></td>
                            <td><t t-field="doc.state"/></td>
                        </tr>
                    </table>
                </div>
            </t>
        </t>
    </t>
</template>
```

### 示例 2：条件渲染

```xml
<!-- Show a warning block only if the patient is not confirmed -->
<t t-if="doc.state == 'draft'">
    <div class="alert alert-warning">
        <strong>Warning:</strong> This patient has not been confirmed yet.
    </div>
</t>
```

## 最佳实践

- ✅ **推荐：** 对模型字段使用 `t-field` — Odoo 会自动正确格式化日期、货币值和布尔值。
- ✅ **推荐：** 对非字段字符串的安全 HTML 输出使用 `t-out`（Odoo 15+）。仅在 Odoo 14 及以下版本使用 `t-esc`（它会对输出进行 HTML 转义）。
- ✅ **推荐：** PDF 报表调用 `web.external_layout`，自动包含公司页眉、页脚和 Logo。
- ✅ **推荐：** 在 Python 报表辅助函数中使用 `_lt()`（延迟翻译）处理可翻译的字符串字面量，而非内联 `t-esc`。
- ❌ **禁止：** 在 QWeb 中使用原始 Python 表达式 — 应在模型或报表 `_get_report_values()` 辅助函数中计算值。
- ❌ **禁止：** 使用 `t-foreach` 时遗漏 `t-as`；没有它就无法在循环体内访问当前记录。
- ❌ **禁止：** 在需要渲染 HTML 内容的地方使用 `t-esc` — 它会转义标签并以原始文本输出。

## 局限性

- 不涵盖动态 QWeb 页面的**网站控制器路由** — 那需要 Python `http.route` 的知识。
- **邮件模板** QWeb 的变量作用域与报表 QWeb 不同（`object` 对比 `docs`）— 本技能主要聚焦于 PDF 报表。
- QWeb JavaScript（用于看板/表单组件）是不同的引擎；本技能仅涵盖**服务端 QWeb**。
- 不涵盖 PDF 渲染问题的 **wkhtmltopdf 配置**（页面大小、边距、页眉页脚重叠）。