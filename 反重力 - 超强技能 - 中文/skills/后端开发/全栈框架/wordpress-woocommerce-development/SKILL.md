---
name: wordpress-woocommerce-development
description: "WooCommerce 商城开发工作流，涵盖商城搭建、支付集成、物流配置、定制开发以及 WordPress 7.0 新特性：AI 连接器、DataViews 和协作工具。触发词：WooCommerce开发、WordPress商城、WooCommerce定制、WordPress 7.0、商城开发、支付集成、物流配置、AI商品描述、欺诈检测。"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# WordPress WooCommerce 开发工作流

## 概述

用于构建 WooCommerce 商城的工作流，涵盖商城搭建、支付网关集成、物流配置、自定义商品类型、商城优化以及 WordPress 7.0 增强功能。

## WordPress 7.0 + WooCommerce 特性

1. **AI 集成**
   - 自动生成商品描述
   - AI 驱动的客服回复
   - 商品摘要生成
   - 营销文案辅助

2. **订单 DataViews**
   - 现代化的订单管理界面
   - 增强的筛选与排序
   - 用于订单历史的活动布局

3. **实时协作**
   - 协同编辑订单
   - 团队备注与沟通
   - 实时库存更新

4. **后台界面焕新**
   - 一致的 WooCommerce 后台样式
   - 屏幕之间的视图过渡

5. **Abilities API**
   - AI 驱动的订单处理
   - 自动化库存管理
   - 智能物流推荐

## 何时使用此工作流

在以下场景使用此工作流：
- 搭建 WooCommerce 商城
- 集成支付网关
- 配置物流方式
- 创建自定义商品类型
- 构建订阅类商品
- 实现 AI 驱动的功能（WP 7.0）

## 工作流阶段

### 阶段 1：商城搭建

#### 调用的技能
- `app-builder` - 项目脚手架
- `wordpress-penetration-testing` - WordPress 模式

#### 行动
1. 安装 WooCommerce
2. 运行安装向导
3. 配置商城设置
4. 设置税务规则
5. 配置货币
6. 使用 WordPress 7.0 后台进行测试

#### WordPress 7.0 + WooCommerce 配置
```php
// Minimum requirements for WP 7.0 + WooCommerce
// Add to wp-config.php for collaboration settings
define('WP_COLLABORATION_MAX_USERS', 10);

// AI features are enabled by installing a provider plugin
// Install OpenAI, Anthropic, or Gemini connector from WordPress.org
// Then configure via Settings > Connectors in admin panel
```

#### 可复制粘贴的提示词
```
Use @app-builder to set up WooCommerce store
```

### 阶段 2：商品配置

#### 调用的技能
- `wordpress-penetration-testing` - WooCommerce 模式

#### 行动
1. 创建商品分类
2. 添加商品属性
3. 配置商品类型
4. 设置可变商品
5. 添加商品图片

#### AI 驱动的商品描述（WP 7.0）
```php
// Auto-generate product descriptions with AI
add_action('woocommerce_new_product', 'generate_ai_description', 10, 2);

function generate_ai_product_description($product_id, $product) {
    if ($product->get_description()) {
        return; // Skip if description exists
    }
    
    // Check if AI client is available
    if (!function_exists('wp_ai_client_prompt')) {
        return;
    }
    
    $title = $product->get_name();
    $short_description = $product->get_short_description();
    
    $prompt = sprintf(
        'Write a compelling WooCommerce product description for "%s" that highlights key features and benefits. Make it SEO-friendly and persuasive.',
        $title
    );
    
    if ($short_description) {
        $prompt .= "\n\nShort description: " . $short_description;
    }
    
    $result = wp_ai_client_prompt($prompt);
    
    if (is_wp_error($result)) {
        return;
    }
    
    // Use temperature for consistent output
    $result->using_temperature(0.3);
    $description = $result->generate_text();
    
    if ($description && !is_wp_error($description)) {
        $product->set_description($description);
        $product->save();
    }
}
```

#### 可复制粘贴的提示词
```
Use @wordpress-penetration-testing to configure WooCommerce products
```

### 阶段 3：支付集成

#### 调用的技能
- `payment-integration` - 支付处理
- `stripe-integration` - Stripe
- `paypal-integration` - PayPal

#### 行动
1. 选择支付网关
2. 配置 Stripe
3. 设置 PayPal
4. 添加线下支付
5. 测试支付流程

#### WordPress 7.0 AI 在支付中的应用
```php
// AI-powered fraud detection
// Note: This is a demonstration - implement proper fraud detection with multiple signals

// Use AI to analyze order for fraud indicators
function ai_check_order_fraud($order_id) {
    // Check if AI client is available
    if (!function_exists('wp_ai_client_prompt')) {
        return false; // Default to no suspicion if AI unavailable
    }
    
    $order = wc_get_order($order_id);
    if (!$order) {
        return false;
    }
    
    $prompt = sprintf(
        'Analyze this order for potential fraud. Order total: $%s. Shipping address: %s, %s. Billing: %s. Is this suspicious? Return only "suspicious" or "clean" without explanation.',
        $order->get_total(),
        $order->get_shipping_address_1(),
        $order->get_shipping_city(),
        $order->get_billing_email()
    );
    
    $result = wp_ai_client_prompt($prompt);
    
    if (is_wp_error($result)) {
        return false;
    }
    
    $result->using_temperature(0.1); // Low temp for consistent classification
    $analysis = $result->generate_text();
    
    return (strpos($analysis, 'suspicious') !== false);
}
```

#### 可复制粘贴的提示词
```
Use @stripe-integration to integrate Stripe payments
```

```
Use @paypal-integration to integrate PayPal
```

### 阶段 4：物流配置

#### 调用的技能
- `wordpress-penetration-testing` - WooCommerce 物流

#### 行动
1. 设置物流区域
2. 配置物流方式
3. 添加统一运费
4. 设置免运费
5. 集成承运商

#### AI 物流推荐（WP 7.0）
```php
// AI-powered shipping recommendations
add_action('woocommerce_after_checkout_form', 'ai_shipping_recommendations');

function ai_shipping_recommendations($checkout) {
    // Check if AI client is available
    if (!function_exists('wp_ai_client_prompt')) {
        return;
    }
    
    $cart = WC()->cart;
    if ($cart->is_empty() || !$cart->get_cart_contents_weight()) {
        return;
    }
    
    $prompt = sprintf(
        'Based on this cart (total weight: %d kg, destination: %s), recommend the best shipping method from: free shipping (orders over $100), flat rate ($9.99), or express ($24.99). Consider delivery time and cost efficiency. Respond with just the recommended method name.',
        $cart->get_cart_contents_weight(),
        WC()->customer->get_shipping_country()
    );
    
    $result = wp_ai_client_prompt($prompt);
    
    if (is_wp_error($result)) {
        return;
    }
    
    $result->using_temperature(0.1); // Low temp for consistent recommendation
    $recommendation = $result->generate_text();
    
    if (strpos($recommendation, 'express') !== false) {
        wc_add_notice(esc_html__('AI Recommendation: Consider Express shipping for faster delivery!', 'woocommerce'), 'info');
    }
}
```

#### 可复制粘贴的提示词
```
Use @wordpress-penetration-testing to configure shipping
```

### 阶段 5：商城定制

#### 调用的技能
- `frontend-developer` - 商城定制
- `frontend-design` - 商城设计

#### 行动
1. 定制商品页
2. 修改购物车页
3. 美化结账流程
4. 创建自定义模板
5. 添加自定义字段

#### WordPress 7.0 模板定制
```php
// Custom product template with WP 7.0 blocks
add_action('woocommerce_after_main_content', 'add_product_ai_chat');

function add_product_ai_chat() {
    if (!is_product()) return;
    
    global $product;
    ?>
    <div class="product-ai-assistant">
        <h3>AI Shopping Assistant</h3>
        <button id="ai-chat-toggle" type="button">Ask about this product</button>
        <div id="ai-chat-panel" style="display:none;">
            <div id="ai-chat-messages"></div>
            <input type="text" id="ai-chat-input" placeholder="Ask about sizing, materials, etc.">
        </div>
    </div>
    <script>
    document.getElementById('ai-chat-toggle').addEventListener('click', function() {
        const panel = document.getElementById('ai-chat-panel');
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    });
    </script>
    <?php
}

// AI-powered product Q&A
add_action('wp_ajax_ai_product_question', 'handle_ai_product_question');
add_action('wp_ajax_nopriv_ai_product_question', 'handle_ai_product_question');

function handle_ai_product_question() {
    // Verify nonce for security
    if (!check_ajax_referer('ai_product_question_nonce', 'nonce', false)) {
        wp_send_json_error(['message' => 'Security check failed']);
    }
    
    $question = isset($_POST['question']) ? sanitize_text_field($_POST['question']) : '';
    $product_id = isset($_POST['product_id']) ? intval($_POST['product_id']) : 0;
    
    if (empty($question) || empty($product_id)) {
        wp_send_json_error(['message' => 'Missing required fields']);
    }
    
    $product = wc_get_product($product_id);
    if (!$product) {
        wp_send_json_error(['message' => 'Product not found']);
    }
    
    // Check if AI client is available
    if (!function_exists('wp_ai_client_prompt')) {
        wp_send_json_error(['message' => 'AI service unavailable']);
    }
    
    $prompt = sprintf(
        'Customer question about "%s": %s\n\nProduct details:
- Price: $%s
- SKU: %s
- Stock: %s

Answer helpfully, accurately, and concisely:',
        $product->get_name(),
        $question,
        $product->get_price(),
        $product->get_sku(),
        $product->get_stock_status()
    );
    
    $result = wp_ai_client_prompt($prompt);
    
    if (is_wp_error($result)) {
        wp_send_json_error(['message' => $result->get_error_message()]);
    }
    
    $result->using_temperature(0.4); // Slightly higher for more varied responses
    $answer = $result->generate_text();
    
    if (is_wp_error($answer)) {
        wp_send_json_error(['message' => 'Failed to generate response']);
    }
    
    wp_send_json_success(['answer' => $answer]);
}
```

#### 可复制粘贴的提示词
```
Use @frontend-developer to customize WooCommerce templates
```

### 阶段 6：扩展

#### 调用的技能
- `wordpress-penetration-testing` - WooCommerce 扩展

#### 行动
1. 安装所需扩展
2. 配置订阅
3. 设置预订
4. 添加会员
5. 集成市场

#### WooCommerce 的 Abilities API（WP 7.0）
```php
// Register ability categories first
add_action('wp_abilities_api_categories_init', function() {
    wp_register_ability_category('ecommerce', [
        'label' => __('E-Commerce', 'woocommerce'),
        'description' => __('WooCommerce store management and operations', 'woocommerce'),
    ]);
});

// Register abilities
add_action('wp_abilities_api_init', function() {
    // Register ability to update inventory
    wp_register_ability('woocommerce/update-inventory', [
        'label' => __('Update Inventory', 'woocommerce'),
        'description' => __('Update product stock quantity', 'woocommerce'),
        'category' => 'ecommerce',
        'input_schema' => [
            'type' => 'object',
            'properties' => [
                'product_id' => ['type' => 'integer', 'description' => 'Product ID to update'],
                'quantity' => ['type' => 'integer', 'description' => 'New stock quantity']
            ],
            'required' => ['product_id', 'quantity']
        ],
        'output_schema' => [
            'type' => 'object',
            'properties' => [
                'success' => ['type' => 'boolean'],
                'new_quantity' => ['type' => 'integer']
            ]
        ],
        'execute_callback' => 'woocommerce_update_inventory_handler',
        'permission_callback' => function() {
            return current_user_can('manage_woocommerce');
        }
    ]);
    
    // Register ability to process orders
    wp_register_ability('woocommerce/process-order', [
        'label' => __('Process Order', 'woocommerce'),
        'description' => __('Mark order as processing and trigger fulfillment', 'woocommerce'),
        'category' => 'ecommerce',
        'input_schema' => [
            'type' => 'object',
            'properties' => [
                'order_id' => ['type' => 'integer', 'description' => 'Order ID to process']
            ],
            'required' => ['order_id']
        ],
        'output_schema' => [
            'type' => 'object',
            'properties' => [
                'success' => ['type' => 'boolean'],
                'status' => ['type' => 'string']
            ]
        ],
        'execute_callback' => 'woocommerce_process_order_handler',
        'permission_callback' => function() {
            return current_user_can('manage_woocommerce');
        }
    ]);
});

// Handler for inventory update
function woocommerce_update_inventory_handler($input) {
    $product_id = isset($input['product_id']) ? absint($input['product_id']) : 0;
    $quantity = isset($input['quantity']) ? absint($input['quantity']) : 0;
    
    $product = wc_get_product($product_id);
    if (!$product) {
        return new WP_Error('invalid_product', 'Product not found');
    }
    
    // Update stock
    wc_update_product_stock($product, $quantity);
    
    return [
        'success' => true,
        'new_quantity' => $product->get_stock_quantity()
    ];
}

// Handler for order processing
function woocommerce_process_order_handler($input) {
    $order_id = isset($input['order_id']) ? absint($input['order_id']) : 0;
    
    $order = wc_get_order($order_id);
    if (!$order) {
        return new WP_Error('invalid_order', 'Order not found');
    }
    
    $order->update_status('processing');
    
    return [
        'success' => true,
        'status' => 'processing'
    ];
}
```

#### 可复制粘贴的提示词
```
Use @wordpress-penetration-testing to configure WooCommerce extensions
```

### 阶段 7：优化

#### 调用的技能
- `web-performance-optimization` - 性能
- `database-optimizer` - 数据库优化

#### 行动
1. 优化商品图片
2. 启用缓存
3. 优化数据库
4. 配置 CDN
5. 设置懒加载

#### WordPress 7.0 性能
- 客户端媒体处理
- 启用字体库
- 响应式网格区块
- 用于感知性能的视图过渡

#### 可复制粘贴的提示词
```
Use @web-performance-optimization to optimize WooCommerce store
```

### 阶段 8：测试

#### 调用的技能
- `playwright-skill` - 端到端测试
- `test-automator` - 测试自动化

#### 行动
1. 测试结账流程
2. 验证支付处理
3. 测试邮件通知
4. 检查移动端体验
5. 性能测试

#### WordPress 7.0 测试
- 使用新后台界面进行测试
- 验证 AI 功能可用
- 测试订单的 DataViews
- 验证协作功能

#### AI 驱动的商城测试
```php
// Automated AI testing for fraud detection during checkout
add_action('woocommerce_after_checkout_validation', 'ai_validate_order', 20);

function ai_validate_order($fields, $errors) {
    // Skip if AI is not available
    if (!function_exists('wp_ai_client_prompt')) {
        return;
    }
    
    // Skip for logged-in users (assumed trusted)
    if (is_user_logged_in()) {
        return;
    }
    
    $order_data = [
        'email' => isset($fields['billing_email']) ? $fields['billing_email'] : '',
        'phone' => isset($fields['billing_phone']) ? $fields['billing_phone'] : '',
        'address' => isset($fields['billing_address_1']) ? $fields['billing_address_1'] : '',
    ];
    
    // Skip if insufficient data
    if (empty($order_data['email'])) {
        return;
    }
    
    $prompt = sprintf(
        'This is a checkout validation. Check if these details seem legitimate: email=%s, phone=%s, address=%s. Return only "valid" or "suspicious" without additional text.',
        sanitize_email($order_data['email']),
        sanitize_text_field($order_data['phone']),
        sanitize_text_field($order_data['address'])
    );
    
    $result = wp_ai_client_prompt($prompt);
    
    if (is_wp_error($result)) {
        // Don't block checkout on AI errors
        return;
    }
    
    $result->using_temperature(0.1); // Low temp for consistent classification
    $response = $result->generate_text();
    
    if (is_wp_error($response)) {
        return;
    }
    
    if (strpos($response, 'suspicious') !== false) {
        $errors->add('validation', __('Additional verification may be needed for this order. We will contact you if needed.', 'woocommerce'));
    }
}
```

#### 可复制粘贴的提示词
```
Use @playwright-skill to test WooCommerce checkout flow
```

## WooCommerce + WordPress 7.0 AI 应用场景

1. **商品描述**
   - 基于商品属性自动生成
   - 翻译描述
   - SEO 优化

2. **客户服务**
   - 用于常见问题的 AI 聊天机器人
   - 订单状态查询
   - 退货处理

3. **库存管理**
   - 需求预测
   - 缺货预警
   - 补货建议

4. **营销**
   - 个性化邮件
   - 商品推荐
   - 弃单挽回

5. **订单处理**
   - 欺诈检测
   - 物流优化
   - 发票生成

## 质量门控

- [ ] 商品展示正确
- [ ] 结账流程正常
- [ ] 支付处理正常
- [ ] 物流计算正确
- [ ] 邮件正常发送
- [ ] 移动端响应式
- [ ] AI 功能已测试（WP 7.0）
- [ ] DataViews 工作正常（WP 7.0）

## 相关工作流包

- `wordpress` - WordPress 开发
- `wordpress-theme-development` - 主题开发
- `wordpress-plugin-development` - 插件开发
- `payment-integration` - 支付处理

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将此输出视为可替代环境特定验证、测试或专家审查的内容。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
