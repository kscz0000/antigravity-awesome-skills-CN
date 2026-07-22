---
name: odoo-automated-tests
description: "使用 TransactionCase、HttpCase 和浏览器 tour 测试编写和运行 Odoo 自动化测试。涵盖测试数据设置、mock 和 CI 集成。当用户要求编写或运行 Odoo 自动化测试时使用。"
risk: safe
source: "self"
---

# Odoo 自动化测试

## 概述

Odoo 内置了基于 Python `unittest` 的测试框架。本技能帮助你编写 `TransactionCase` 单元测试、`HttpCase` 集成测试以及 JavaScript tour 测试，同时涵盖在 CI 流水线中运行测试的方法。

## 使用场景

- 为自定义模型的业务逻辑编写单元测试。
- 创建 HTTP 测试以验证 controller 端点。
- 在 CI 流水线中调试测试失败。
- 使用 `--test-enable` 设置自动化测试执行。

## 工作原理

1. **激活**：提及 `@odoo-automated-tests` 并描述要测试的功能。
2. **生成**：获取包含 setup、teardown 和断言的完整测试类代码。
3. **运行**：获取执行测试的精确 `odoo` CLI 命令。

## 示例

### 示例 1：TransactionCase 单元测试（Odoo 15+ 模式）

```python
# tests/test_hospital_patient.py
from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.exceptions import ValidationError

@tagged('post_install', '-at_install')
class TestHospitalPatient(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # Use setUpClass for performance — runs once per class, not per test
        super().setUpClass()
        cls.Patient = cls.env['hospital.patient']
        cls.doctor = cls.env['res.users'].browse(cls.env.uid)

    def test_create_patient(self):
        patient = self.Patient.create({
            'name': 'John Doe',
            'doctor_id': self.doctor.id,
        })
        self.assertEqual(patient.state, 'draft')
        self.assertEqual(patient.name, 'John Doe')

    def test_confirm_patient(self):
        patient = self.Patient.create({'name': 'Jane Smith'})
        patient.action_confirm()
        self.assertEqual(patient.state, 'confirmed')

    def test_empty_name_raises_error(self):
        with self.assertRaises(ValidationError):
            self.Patient.create({'name': ''})

    def test_access_denied_for_other_user(self):
        # Test security rules by running as a different user
        other_user = self.env.ref('base.user_demo')
        with self.assertRaises(Exception):
            self.Patient.with_user(other_user).create({'name': 'Test'})
```

> **`setUpClass` 与 `setUp` 的区别：** 使用 `setUpClass`（Odoo 15+）来创建共享测试数据。它每个类只运行一次，比每个测试方法都重新初始化的 `setUp` 快得多。

### 示例 2：通过 CLI 运行测试

```bash
# Run all tests for a specific module
./odoo-bin --test-enable --stop-after-init -d my_database -u hospital_management

# Run only tests tagged with a specific tag
./odoo-bin --test-enable --stop-after-init -d my_database \
  --test-tags hospital_management

# Run a specific test class
./odoo-bin --test-enable --stop-after-init -d my_database \
  --test-tags /hospital_management:TestHospitalPatient
```

### 示例 3：HttpCase controller 测试

```python
from odoo.tests.common import HttpCase
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestPatientController(HttpCase):

    def test_patient_page_authenticated(self):
        # Authenticate as a user, not with hardcoded password
        self.authenticate(self.env.user.login, self.env.user.login)
        resp = self.url_open('/hospital/patients')
        self.assertEqual(resp.status_code, 200)

    def test_patient_page_redirects_unauthenticated(self):
        # No authenticate() call = public/anonymous user
        resp = self.url_open('/hospital/patients', allow_redirects=False)
        self.assertIn(resp.status_code, [301, 302, 403])
```

## 最佳实践

- ✅ **推荐：** 使用 `setUpClass()` 配合 `cls.env` 而非 `setUp()`——对大型测试套件来说性能提升显著。
- ✅ **推荐：** 使用 `@tagged('post_install', '-at_install')` 使测试在所有模块安装完成后运行。
- ✅ **推荐：** 同时测试正常路径和错误条件（`ValidationError`、`AccessError`、`UserError`）。
- ✅ **推荐：** 使用 `self.with_user(user)` 测试访问控制，无需调用 `sudo()`。
- ❌ **避免：** 使用生产数据库进行测试——始终使用专用测试数据库。
- ❌ **避免：** 依赖测试执行顺序——每个 `TransactionCase` 测试都在隔离的事务中回滚。
- ❌ **避免：** 在 `HttpCase.authenticate()` 中硬编码密码——使用 `self.env.user.login` 或 fixture 用户。

## 局限性

- **JavaScript tour 测试** 需要运行中的浏览器（通过 `phantomjs` 或 `Chrome headless`）和活跃的 Odoo 服务器——此处不做深入介绍。
- `HttpCase` 测试比 `TransactionCase` 慢得多——仅在需要验证 controller/路由时使用。
- 不涵盖**模拟外部服务**（例如在测试中 mock SMTP 服务器或支付网关）。
- 测试隔离在**事务级别**而非数据库级别——提交数据的测试（例如通过 `cr.commit()`）可能在测试间泄漏状态。
