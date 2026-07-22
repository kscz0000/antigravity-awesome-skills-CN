---
name: stripe-integration
description: "Stripe 支付处理集成精通指南，涵盖结账、订阅、Webhook 和退款，构建健壮的 PCI 合规支付流程。触发词：Stripe集成、Stripe支付、支付处理、结账集成、订阅计费、Webhook处理、退款处理、Stripe Connect、SCA认证、3D Secure"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Stripe 集成

Stripe 支付处理集成精通指南，涵盖结账、订阅、Webhook 和退款，构建健壮的 PCI 合规支付流程。

## 不适用场景

- 任务与 Stripe 集成无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束条件和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 适用场景

- 在 Web/移动应用中实现支付处理
- 搭建订阅计费系统
- 处理一次性支付和周期性扣费
- 处理退款和争议
- 管理客户支付方式
- 为欧洲支付实现 SCA（强客户认证）
- 使用 Stripe Connect 构建市场支付流程

## 核心概念

### 1. 支付流程
**Checkout Session（托管式）**
- Stripe 托管的支付页面
- PCI 合规负担最小
- 实现速度最快
- 支持一次性支付和周期性支付

**Payment Intents（自定义 UI）**
- 完全控制支付 UI
- 需要 Stripe.js 以满足 PCI 合规
- 实现更复杂
- 更好的自定义选项

**Setup Intents（保存支付方式）**
- 收集支付方式而不扣款
- 用于订阅和未来支付
- 需要客户确认

### 2. Webhooks
**关键事件：**
- `payment_intent.succeeded`：支付完成
- `payment_intent.payment_failed`：支付失败
- `customer.subscription.updated`：订阅变更
- `customer.subscription.deleted`：订阅取消
- `charge.refunded`：退款已处理
- `invoice.payment_succeeded`：订阅支付成功

### 3. 订阅
**组件：**
- **Product（产品）**：你销售的内容
- **Price（价格）**：金额和频率
- **Subscription（订阅）**：客户的周期性支付
- **Invoice（发票）**：每个计费周期生成

### 4. 客户管理
- 创建和管理客户记录
- 存储多种支付方式
- 跟踪客户元数据
- 管理账单详情

## 快速开始

```python
import stripe

stripe.api_key = "sk_test_..."

# Create a checkout session
session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': 'Premium Subscription',
            },
            'unit_amount': 2000,  # .00
            'recurring': {
                'interval': 'month',
            },
        },
        'quantity': 1,
    }],
    mode='subscription',
    success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='https://yourdomain.com/cancel',
)

# Redirect user to session.url
print(session.url)
```

## 支付实现模式

### 模式 1：一次性支付（托管式结账）
```python
def create_checkout_session(amount, currency='usd'):
    """Create a one-time payment checkout session."""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Purchase',
                        'images': ['https://example.com/product.jpg'],
                    },
                    'unit_amount': amount,  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://yourdomain.com/cancel',
            metadata={
                'order_id': 'order_123',
                'user_id': 'user_456'
            }
        )
        return session
    except stripe.error.StripeError as e:
        # Handle error
        print(f"Stripe error: {e.user_message}")
        raise
```

### 模式 2：自定义 Payment Intent 流程
```python
def create_payment_intent(amount, currency='usd', customer_id=None):
    """Create a payment intent for custom checkout UI."""
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        customer=customer_id,
        automatic_payment_methods={
            'enabled': True,
        },
        metadata={
            'integration_check': 'accept_a_payment'
        }
    )
    return intent.client_secret  # Send to frontend

# Frontend (JavaScript)
"""
const stripe = Stripe('pk_test_...');
const elements = stripe.elements();
const cardElement = elements.create('card');
cardElement.mount('#card-element');

const {error, paymentIntent} = await stripe.confirmCardPayment(
    clientSecret,
    {
        payment_method: {
            card: cardElement,
            billing_details: {
                name: 'Customer Name'
            }
        }
    }
);

if (error) {
    // Handle error
} else if (paymentIntent.status === 'succeeded') {
    // Payment successful
}
"""
```

### 模式 3：创建订阅
```python
def create_subscription(customer_id, price_id):
    """Create a subscription for a customer."""
    try:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
        )

        return {
            'subscription_id': subscription.id,
            'client_secret': subscription.latest_invoice.payment_intent.client_secret
        }
    except stripe.error.StripeError as e:
        print(f"Subscription creation failed: {e}")
        raise
```

### 模式 4：客户门户
```python
def create_customer_portal_session(customer_id):
    """Create a portal session for customers to manage subscriptions."""
    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url='https://yourdomain.com/account',
    )
    return session.url  # Redirect customer here
```

## Webhook 处理

### 安全的 Webhook 端点
```python
from flask import Flask, request
import stripe

app = Flask(__name__)

endpoint_secret = 'whsec_...'

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_failed_payment(payment_intent)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_canceled(subscription)

    return 'Success', 200

def handle_successful_payment(payment_intent):
    """Process successful payment."""
    customer_id = payment_intent.get('customer')
    amount = payment_intent['amount']
    metadata = payment_intent.get('metadata', {})

    # Update your database
    # Send confirmation email
    # Fulfill order
    print(f"Payment succeeded: {payment_intent['id']}")

def handle_failed_payment(payment_intent):
    """Handle failed payment."""
    error = payment_intent.get('last_payment_error', {})
    print(f"Payment failed: {error.get('message')}")
    # Notify customer
    # Update order status

def handle_subscription_canceled(subscription):
    """Handle subscription cancellation."""
    customer_id = subscription['customer']
    # Update user access
    # Send cancellation email
    print(f"Subscription canceled: {subscription['id']}")
```

### Webhook 最佳实践
```python
import hashlib
import hmac

def verify_webhook_signature(payload, signature, secret):
    """Manually verify webhook signature."""
    expected_sig = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_sig)

def handle_webhook_idempotently(event_id, handler):
    """Ensure webhook is processed exactly once."""
    # Check if event already processed
    if is_event_processed(event_id):
        return

    # Process event
    try:
        handler()
        mark_event_processed(event_id)
    except Exception as e:
        log_error(e)
        # Stripe will retry failed webhooks
        raise
```

## 客户管理

```python
def create_customer(email, name, payment_method_id=None):
    """Create a Stripe customer."""
    customer = stripe.Customer.create(
        email=email,
        name=name,
        payment_method=payment_method_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        } if payment_method_id else None,
        metadata={
            'user_id': '12345'
        }
    )
    return customer

def attach_payment_method(customer_id, payment_method_id):
    """Attach a payment method to a customer."""
    stripe.PaymentMethod.attach(
        payment_method_id,
        customer=customer_id
    )

    # Set as default
    stripe.Customer.modify(
        customer_id,
        invoice_settings={
            'default_payment_method': payment_method_id
        }
    )

def list_customer_payment_methods(customer_id):
    """List all payment methods for a customer."""
    payment_methods = stripe.PaymentMethod.list(
        customer=customer_id,
        type='card'
    )
    return payment_methods.data
```

## 退款处理

```python
def create_refund(payment_intent_id, amount=None, reason=None):
    """Create a refund."""
    refund_params = {
        'payment_intent': payment_intent_id
    }

    if amount:
        refund_params['amount'] = amount  # Partial refund

    if reason:
        refund_params['reason'] = reason  # 'duplicate', 'fraudulent', 'requested_by_customer'

    refund = stripe.Refund.create(**refund_params)
    return refund

def handle_dispute(charge_id, evidence):
    """Update dispute with evidence."""
    stripe.Dispute.modify(
        charge_id,
        evidence={
            'customer_name': evidence.get('customer_name'),
            'customer_email_address': evidence.get('customer_email'),
            'shipping_documentation': evidence.get('shipping_proof'),
            'customer_communication': evidence.get('communication'),
        }
    )
```

## 测试

```python
# Use test mode keys
stripe.api_key = "sk_test_..."

# Test card numbers
TEST_CARDS = {
    'success': '4242424242424242',
    'declined': '4000000000000002',
    '3d_secure': '4000002500003155',
    'insufficient_funds': '4000000000009995'
}

def test_payment_flow():
    """Test complete payment flow."""
    # Create test customer
    customer = stripe.Customer.create(
        email="test@example.com"
    )

    # Create payment intent
    intent = stripe.PaymentIntent.create(
        amount=1000,
        currency='usd',
        customer=customer.id,
        payment_method_types=['card']
    )

    # Confirm with test card
    confirmed = stripe.PaymentIntent.confirm(
        intent.id,
        payment_method='pm_card_visa'  # Test payment method
    )

    assert confirmed.status == 'succeeded'
```

## 资源

- **references/checkout-flows.md**：详细结账实现
- **references/webhook-handling.md**：Webhook 安全与处理
- **references/subscription-management.md**：订阅生命周期
- **references/customer-management.md**：客户和支付方式管理
- **references/invoice-generation.md**：开票与计费
- **assets/stripe-client.py**：生产就绪的 Stripe 客户端封装
- **assets/webhook-handler.py**：完整的 Webhook 处理器
- **assets/checkout-config.json**：结账配置模板

## 最佳实践

1. **始终使用 Webhook**：不要仅依赖客户端确认
2. **幂等性**：以幂等方式处理 Webhook 事件
3. **错误处理**：优雅地处理所有 Stripe 错误
4. **测试模式**：上线前用测试密钥充分测试
5. **元数据**：使用元数据将 Stripe 对象关联到你的数据库
6. **监控**：跟踪支付成功率和错误
7. **PCI 合规**：永远不要在你的服务器上处理原始卡号数据
8. **SCA 就绪**：为欧洲支付实现 3D Secure

## 常见陷阱

- **不验证 Webhook**：始终验证 Webhook 签名
- **遗漏 Webhook 事件**：处理所有相关的 Webhook 事件
- **硬编码金额**：使用分/最小货币单位
- **无重试逻辑**：为 API 调用实现重试
- **忽略测试模式**：用测试卡号测试所有边界情况

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
