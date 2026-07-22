---
name: pci-compliance
description: "精通 PCI DSS（支付卡行业数据安全标准）合规，用于安全支付处理和持卡人数据管理。当用户要求'PCI合规'或'支付安全'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# PCI 合规

精通 PCI DSS（支付卡行业数据安全标准）合规，用于安全支付处理和持卡人数据管理。

## 不适用场景

- 任务与 PCI 合规无关
- 需要本范围之外的其他领域或工具

## 指引

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可执行的步骤和验证方法
- 如需详细示例，请打开 `resources/implementation-playbook.md`

## 使用场景

- 构建支付处理系统
- 处理信用卡信息
- 实现安全支付流程
- 执行 PCI 合规审计
- 缩小 PCI 合规范围
- 实现 Token 化和加密
- 准备 PCI DSS 评估

## PCI DSS 要求（12 项核心要求）

### 构建和维护安全网络
1. 安装和维护防火墙配置
2. 不使用供应商默认密码

### 保护持卡人数据
3. 保护存储的持卡人数据
4. 加密公共网络上的持卡人数据传输

### 维护漏洞管理
5. 保护系统免受恶意软件侵害
6. 开发和维护安全的系统与应用

### 实施强访问控制
7. 按业务需要限制对持卡人数据的访问
8. 标识和验证对系统组件的访问
9. 限制对持卡人数据的物理访问

### 监控和测试网络
10. 跟踪和监控对网络资源和持卡人数据的所有访问
11. 定期测试安全系统和流程

### 维护信息安全策略
12. 维护涵盖信息安全的策略

## 合规等级

**等级 1**：> 600 万笔交易/年（需年度 ROC）
**等级 2**：100-600 万笔交易/年（年度 SAQ）
**等级 3**：2 万-100 万笔电商交易/年
**等级 4**：< 2 万笔电商交易或 < 100 万笔总交易

## 数据最小化（禁止存储）

```python
# NEVER STORE THESE
PROHIBITED_DATA = {
    'full_track_data': 'Magnetic stripe data',
    'cvv': 'Card verification code/value',
    'pin': 'PIN or PIN block'
}

# CAN STORE (if encrypted)
ALLOWED_DATA = {
    'pan': 'Primary Account Number (card number)',
    'cardholder_name': 'Name on card',
    'expiration_date': 'Card expiration',
    'service_code': 'Service code'
}

class PaymentData:
    """Safe payment data handling."""

    def __init__(self):
        self.prohibited_fields = ['cvv', 'cvv2', 'cvc', 'pin']

    def sanitize_log(self, data):
        """Remove sensitive data from logs."""
        sanitized = data.copy()

        # Mask PAN
        if 'card_number' in sanitized:
            card = sanitized['card_number']
            sanitized['card_number'] = f"{card[:6]}{'*' * (len(card) - 10)}{card[-4:]}"

        # Remove prohibited data
        for field in self.prohibited_fields:
            sanitized.pop(field, None)

        return sanitized

    def validate_no_prohibited_storage(self, data):
        """Ensure no prohibited data is being stored."""
        for field in self.prohibited_fields:
            if field in data:
                raise SecurityError(f"Attempting to store prohibited field: {field}")
```

## Token 化

### 使用支付处理器 Token
```python
import stripe

class TokenizedPayment:
    """Handle payments using tokens (no card data on server)."""

    @staticmethod
    def create_payment_method_token(card_details):
        """Create token from card details (client-side only)."""
        # THIS SHOULD ONLY BE DONE CLIENT-SIDE WITH STRIPE.JS
        # NEVER send card details to your server

        """
        // Frontend JavaScript
        const stripe = Stripe('pk_...');

        const {token, error} = await stripe.createToken({
            card: {
                number: '4242424242424242',
                exp_month: 12,
                exp_year: 2024,
                cvc: '123'
            }
        });

        // Send token.id to server (NOT card details)
        """
        pass

    @staticmethod
    def charge_with_token(token_id, amount):
        """Charge using token (server-side)."""
        # Your server only sees the token, never the card number
        stripe.api_key = "sk_..."

        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token_id,  # Token instead of card details
            description="Payment"
        )

        return charge

    @staticmethod
    def store_payment_method(customer_id, payment_method_token):
        """Store payment method as token for future use."""
        stripe.Customer.modify(
            customer_id,
            source=payment_method_token
        )

        # Store only customer_id and payment_method_id in your database
        # NEVER store actual card details
        return {
            'customer_id': customer_id,
            'has_payment_method': True
            # DO NOT store: card number, CVV, etc.
        }
```

### 自定义 Token 化（高级）
```python
import secrets
from cryptography.fernet import Fernet

class TokenVault:
    """Secure token vault for card data (if you must store it)."""

    def __init__(self, encryption_key):
        self.cipher = Fernet(encryption_key)
        self.vault = {}  # In production: use encrypted database

    def tokenize(self, card_data):
        """Convert card data to token."""
        # Generate secure random token
        token = secrets.token_urlsafe(32)

        # Encrypt card data
        encrypted = self.cipher.encrypt(json.dumps(card_data).encode())

        # Store token -> encrypted data mapping
        self.vault[token] = encrypted

        return token

    def detokenize(self, token):
        """Retrieve card data from token."""
        encrypted = self.vault.get(token)
        if not encrypted:
            raise ValueError("Token not found")

        # Decrypt
        decrypted = self.cipher.decrypt(encrypted)
        return json.loads(decrypted.decode())

    def delete_token(self, token):
        """Remove token from vault."""
        self.vault.pop(token, None)
```

## 加密

### 静态数据
```python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class EncryptedStorage:
    """Encrypt data at rest using AES-256-GCM."""

    def __init__(self, encryption_key):
        """Initialize with 256-bit key."""
        self.key = encryption_key  # Must be 32 bytes

    def encrypt(self, plaintext):
        """Encrypt data."""
        # Generate random nonce
        nonce = os.urandom(12)

        # Encrypt
        aesgcm = AESGCM(self.key)
        ciphertext = aesgcm.encrypt(nonce, plaintext.encode(), None)

        # Return nonce + ciphertext
        return nonce + ciphertext

    def decrypt(self, encrypted_data):
        """Decrypt data."""
        # Extract nonce and ciphertext
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]

        # Decrypt
        aesgcm = AESGCM(self.key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

        return plaintext.decode()

# Usage
storage = EncryptedStorage(os.urandom(32))
encrypted_pan = storage.encrypt("4242424242424242")
# Store encrypted_pan in database
```

### 传输数据
```python
# Always use TLS 1.2 or higher
# Flask/Django example
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# Enforce HTTPS
from flask_talisman import Talisman
Talisman(app, force_https=True)
```

## 访问控制

```python
from functools import wraps
from flask import session

def require_pci_access(f):
    """Decorator to restrict access to cardholder data."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get('user')

        # Check if user has PCI access role
        if not user or 'pci_access' not in user.get('roles', []):
            return {'error': 'Unauthorized access to cardholder data'}, 403

        # Log access attempt
        audit_log(
            user=user['id'],
            action='access_cardholder_data',
            resource=f.__name__
        )

        return f(*args, **kwargs)

    return decorated_function

@app.route('/api/payment-methods')
@require_pci_access
def get_payment_methods():
    """Retrieve payment methods (restricted access)."""
    # Only accessible to users with pci_access role
    pass
```

## 审计日志

```python
import logging
from datetime import datetime

class PCIAuditLogger:
    """PCI-compliant audit logging."""

    def __init__(self):
        self.logger = logging.getLogger('pci_audit')
        # Configure to write to secure, append-only log

    def log_access(self, user_id, resource, action, result):
        """Log access to cardholder data."""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'resource': resource,
            'action': action,
            'result': result,
            'ip_address': request.remote_addr
        }

        self.logger.info(json.dumps(entry))

    def log_authentication(self, user_id, success, method):
        """Log authentication attempt."""
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'event': 'authentication',
            'success': success,
            'method': method,
            'ip_address': request.remote_addr
        }

        self.logger.info(json.dumps(entry))

# Usage
audit = PCIAuditLogger()
audit.log_access(user_id=123, resource='payment_methods', action='read', result='success')
```

## 安全最佳实践

### 输入验证
```python
import re

def validate_card_number(card_number):
    """Validate card number format (Luhn algorithm)."""
    # Remove spaces and dashes
    card_number = re.sub(r'[\s-]', '', card_number)

    # Check if all digits
    if not card_number.isdigit():
        return False

    # Luhn algorithm
    def luhn_checksum(card_num):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    return luhn_checksum(card_number) == 0

def sanitize_input(user_input):
    """Sanitize user input to prevent injection."""
    # Remove special characters
    # Validate against expected format
    # Escape for database queries
    pass
```

## PCI DSS SAQ（自评问卷）

### SAQ A（最少要求）
- 使用托管支付页面的电商
- 系统中无卡数据
- 约 20 个问题

### SAQ A-EP
- 使用嵌入式支付表单的电商
- 使用 JavaScript 处理卡数据
- 约 180 个问题

### SAQ D（最多要求）
- 存储、处理或传输卡数据
- 完整 PCI DSS 要求
- 约 300 个问题

## 合规检查清单

```python
PCI_COMPLIANCE_CHECKLIST = {
    'network_security': [
        'Firewall configured and maintained',
        'No vendor default passwords',
        'Network segmentation implemented'
    ],
    'data_protection': [
        'No storage of CVV, track data, or PIN',
        'PAN encrypted when stored',
        'PAN masked when displayed',
        'Encryption keys properly managed'
    ],
    'vulnerability_management': [
        'Anti-virus installed and updated',
        'Secure development practices',
        'Regular security patches',
        'Vulnerability scanning performed'
    ],
    'access_control': [
        'Access restricted by role',
        'Unique IDs for all users',
        'Multi-factor authentication',
        'Physical security measures'
    ],
    'monitoring': [
        'Audit logs enabled',
        'Log review process',
        'File integrity monitoring',
        'Regular security testing'
    ],
    'policy': [
        'Security policy documented',
        'Risk assessment performed',
        'Security awareness training',
        'Incident response plan'
    ]
}
```

## 参考资料

- **references/data-minimization.md**：禁止存储受限数据
- **references/tokenization.md**：Token 化策略
- **references/encryption.md**：加密要求
- **references/access-control.md**：基于角色的访问控制
- **references/audit-logging.md**：全面日志记录
- **assets/pci-compliance-checklist.md**：完整检查清单
- **assets/encrypted-storage.py**：加密工具
- **scripts/audit-payment-system.sh**：合规审计脚本

## 常见违规

1. **存储 CVV**：永远不要存储卡片验证码
2. **未加密 PAN**：卡号存储时必须加密
3. **弱加密**：使用 AES-256 或同等强度
4. **无访问控制**：限制谁可以访问持卡人数据
5. **缺少审计日志**：必须记录对支付数据的所有访问
6. **不安全传输**：始终使用 TLS 1.2+
7. **默认密码**：更改所有默认凭证
8. **无安全测试**：需要定期渗透测试

## 缩小 PCI 范围

1. **使用托管支付**：Stripe Checkout、PayPal 等
2. **Token 化**：用 Token 替代卡数据
3. **网络分段**：隔离持卡人数据环境
4. **外包**：使用 PCI 合规的支付处理器
5. **不存储**：永远不要存储完整卡信息

通过最小化接触卡数据的系统数量，可以显著降低合规负担。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
