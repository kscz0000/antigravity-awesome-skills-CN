---
name: odoo-module-developer
description: "Odoo 自定义模块开发专家指南。涵盖 __manifest__.py、模型继承、ORM 模式及模块结构最佳实践。当用户要求创建、开发或优化 Odoo 模块时使用。"
risk: safe
source: "self"
---

# Odoo 模块开发专家

## 概述

本技能将你的 AI 变为 Odoo 自定义模块开发专家。引导你完成模块脚手架搭建、模型定义、安全配置，并遵循 Community 和 Enterprise 版本的编码规范。

## 适用场景

- 从零创建新的 Odoo 自定义模块
- 扩展现有 Odoo 模型（例如为 `sale.order` 添加字段）
- 排查模块加载错误或 manifest 问题
- 正确实现 `onchange`、`compute` 和 `constraint` 方法

## 使用方式

1. **激活**：提及 `@odoo-module-developer` 并描述你要构建的模块
2. **脚手架**：获取完整的目录结构，包含 `__manifest__.py`、`__init__.py`、模型、视图和安全文件
3. **审查**：粘贴现有代码，按 Odoo 最佳实践进行评审

## 示例

### 示例 1：搭建新模块脚手架

**提示词：** `Create a module called "hospital_management" with a model for patients`

**生成结构：**

```text
hospital_management/
├── __manifest__.py
├── __init__.py
├── models/
│   ├── __init__.py
│   └── hospital_patient.py
├── views/
│   └── hospital_patient_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
└── data/
```

**`__manifest__.py`：**

```python
{
    'name': 'Hospital Management',
    'version': '17.0.1.0.0',
    'category': 'Healthcare',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/hospital_patient_views.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
```

**`models/hospital_patient.py`：**

```python
from odoo import models, fields, api

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Patient Name', required=True, tracking=True)
    birth_date = fields.Date(string='Birth Date')
    doctor_id = fields.Many2one('res.users', string='Assigned Doctor')
    state = fields.Selection([
        ('draft', 'New'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ], default='draft', tracking=True)
```

## 最佳实践

- ✅ **推荐**：模型 `_name` 必须带命名空间前缀（如 `hospital.patient`）
- ✅ **推荐**：使用 `_inherit = ['mail.thread']` 自动添加消息记录/日志
- ✅ **推荐**：manifest 中 `version` 格式为 `{odoo_version}.{major}.{minor}.{patch}`
- ✅ **推荐**：在 `__manifest__.py` 中设置 `'author'` 和 `'website'`，便于在应用列表中识别
- ❌ **禁止**：直接修改 Odoo 核心模型文件——始终使用 `_inherit`
- ❌ **禁止**：忘记在 `ir.model.access.csv` 中添加新模型，否则用户会遇到权限错误
- ❌ **禁止**：文件夹名称使用空格或大写——Odoo 要求模块名使用 snake_case

## 局限性

- 不涵盖 **OWL JavaScript 组件**或前端控件开发——视图 XML 请使用 `@odoo-xml-views-builder`
- **Odoo 13 及以下版本**模块结构不同（无 `__manifest__.py` 自动加载）——本技能面向 v14+
- 不涵盖**多公司**或**多网站**配置，这些需要额外的模型字段（`company_id`、`website_id`）
- 不生成自动化测试文件——请使用 `@odoo-automated-tests`
