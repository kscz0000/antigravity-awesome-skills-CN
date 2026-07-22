---
name: wordpress
description: "完整的 WordPress 开发工作流，涵盖主题开发、插件创建、WooCommerce 集成、性能优化和安全加固。包含 WordPress 7.0 功能：实时协作、AI 连接器、Abilities API、DataViews 和纯 PHP 区块。触发词：WordPress开发、主题开发、插件开发、WooCommerce、WordPress安全、WordPress性能、WordPress 7.0、RTC、AI Connector"
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# WordPress 开发工作流套件

## 概述

全面的 WordPress 开发工作流，涵盖主题开发、插件创建、WooCommerce 集成、性能优化和安全。此套件编排多个技能，用于构建生产就绪的 WordPress 站点和应用程序。

## WordPress 7.0 功能（向后兼容）

WordPress 7.0（2026年4月9日）引入了重要功能，同时保持向后兼容性：

### 实时协作 (RTC)
- 多用户可使用 Yjs CRDT 同时编辑
- HTTP 轮询提供程序（可通过 `WP_COLLABORATION_MAX_USERS` 配置）
- 通过 `sync.providers` 过滤器自定义传输
- **向后兼容性**：检测到旧版 meta box 时回退到文章锁定

### AI 连接器 API
- 核心中的提供商无关 AI 接口（`wp_ai_client_prompt()`）
- 设置 > 连接器，用于集中管理 API 凭证
- 官方提供商：OpenAI、Anthropic Claude、Google Gemini
- **向后兼容性**：通过插件支持 WordPress 6.9+

### Abilities API（7.0 稳定）
- 标准化能力声明系统
- REST API 端点：`/wp-json/abilities/v1/manifest`
- 用于 AI 代理集成的 MCP 适配器
- **向后兼容性**：可在 6.x 中作为 Composer 包使用

### DataViews 和 DataForm
- 在文章、页面、媒体屏幕上替换 WP_List_Table
- 新布局：表格、网格、列表、活动
- 客户端验证（pattern、minLength、maxLength、min、max）
- **向后兼容性**：使用旧钩子的插件仍可工作

### 纯 PHP 区块注册
- 完全通过 PHP 注册区块，无需 JavaScript
- 自动生成的检查器控件
- **向后兼容性**：现有 JS 区块继续工作

### Interactivity API 更新
- `watch()` 替换来自 @preact/signals 的 `effect`
- 状态导航变更
- **向后兼容性**：旧语法已弃用但仍可用

### 管理后台刷新
- 新默认配色方案
- 管理屏幕之间的视图过渡
- **向后兼容性**：CSS 级别变更，无破坏性变更

### 模式编辑
- 未同步模式默认使用 ContentOnly 模式
- `disableContentOnlyForUnsyncedPatterns` 设置
- **向后兼容性**：现有模式可正常工作

## 何时使用此工作流

在以下情况使用此工作流：
- 构建新的 WordPress 网站
- 创建自定义主题
- 开发 WordPress 插件
- 设置 WooCommerce 商店
- 优化 WordPress 性能
- 加固 WordPress 安全
- 实现 WordPress 7.0 功能（RTC、AI、DataViews）

## 工作流阶段

### 阶段 1：WordPress 设置

#### 要调用的技能
- `app-builder` - 项目脚手架
- `environment-setup-guide` - 开发环境

#### 操作
1. 设置本地开发环境（LocalWP、Docker 或 Valet）
2. 安装 WordPress（新项目推荐 7.0+）
3. 配置开发数据库
4. 设置版本控制
5. 为开发配置 wp-config.php

#### WordPress 7.0 配置
```php
// wp-config.php - 协作设置
define('WP_COLLABORATION_MAX_USERS', 5);

// AI 连接器通过安装提供商插件启用
// （例如 OpenAI、Anthropic Claude 或 Google Gemini 连接器）
// 不需要常量 - 通过管理后台设置 > 连接器配置
```

#### 复制粘贴提示词
```
Use @app-builder to scaffold a new WordPress project with modern tooling
```

### 阶段 2：主题开发

#### 要调用的技能
- `frontend-developer` - 组件开发
- `frontend-design` - UI 实现
- `tailwind-patterns` - 样式
- `web-performance-optimization` - 性能

#### 操作
1. 设计主题架构
2. 创建主题文件（style.css、functions.php、index.php）
3. 实现模板层次结构
4. 创建自定义页面模板
5. 添加自定义文章类型和分类法
6. 实现主题自定义选项
7. 添加响应式设计
8. 使用 WordPress 7.0 管理后台刷新测试

#### WordPress 7.0 主题注意事项
- 区块 API v3 现在引用模型
- theme.json 中的伪元素支持
- 全局样式自定义 CSS 遵守区块定义的选择器
- 管理导航的视图过渡

#### 主题结构
```
theme-name/
├── style.css
├── functions.php
├── index.php
├── header.php
├── footer.php
├── sidebar.php
├── single.php
├── page.php
├── archive.php
├── search.php
├── 404.php
├── template-parts/
├── inc/
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── languages/
```

#### 复制粘贴提示词
```
Use @frontend-developer to create a custom WordPress theme with React components
```

```
Use @tailwind-patterns to style WordPress theme with modern CSS
```

### 阶段 3：插件开发

#### 要调用的技能
- `backend-dev-guidelines` - 后端标准
- `api-design-principles` - API 设计
- `auth-implementation-patterns` - 身份验证

#### 操作
1. 设计插件架构
2. 创建插件样板
3. 实现钩子（动作和过滤器）
4. 创建管理界面
5. 添加自定义数据库表
6. 实现 REST API 端点
7. 添加设置和选项页面

#### WordPress 7.0 插件注意事项
- **RTC 兼容性**：使用 `show_in_rest => true` 注册文章 meta
- **AI 集成**：使用 `wp_ai_client_prompt()` 实现 AI 功能
- **DataViews**：考虑新的管理 UI 模式
- **Meta Box**：迁移到基于区块的 UI 以支持协作

#### RTC 兼容的文章 Meta 注册
```php
register_post_meta('post', 'custom_field', [
    'type' => 'string',
    'single' => true,
    'show_in_rest' => true,  // RTC 必需
    'sanitize_callback' => 'sanitize_text_field',
]);
```

#### AI 连接器示例
```php
// 使用 WordPress 7.0 AI 连接器
// 注意：需要安装并配置 AI 提供商插件（OpenAI、Claude 或 Gemini）

// 基本文本生成
$response = wp_ai_client_prompt('Summarize this content.')
    ->generate_text();

// 使用 temperature 进行确定性输出
$response = wp_ai_client_prompt('Summarize this content.')
    ->using_temperature(0.2)
    ->generate_text();

// 使用模型偏好（尝试列表中第一个可用的）
$response = wp_ai_client_prompt('Summarize this content.')
    ->using_model_preference('gpt-4', 'claude-3-opus', 'gemini-2-pro')
    ->generate_text();

// JSON 结构化输出
$schema = [
    'type' => 'object',
    'properties' => [
        'summary' => ['type' => 'string'],
        'keywords' => ['type' => 'array', 'items' => ['type' => 'string']]
    ],
    'required' => ['summary']
];
$response = wp_ai_client_prompt('Analyze this content and return JSON.')
    ->using_system_instruction('You are a content analyzer.')
    ->as_json_response($schema)
    ->generate_text();
```

#### 插件结构
```
plugin-name/
├── plugin-name.php
├── includes/
│   ├── class-plugin-activator.php
│   ├── class-plugin-deactivator.php
│   ├── class-plugin-loader.php
│   └── class-plugin.php
├── admin/
│   ├── class-plugin-admin.php
│   ├── css/
│   └── js/
├── public/
│   ├── class-plugin-public.php
│   ├── css/
│   └── js/
└── languages/
```

#### 复制粘贴提示词
```
Use @backend-dev-guidelines to create a WordPress plugin with proper architecture
```

### 阶段 4：WooCommerce 集成

#### 要调用的技能
- `payment-integration` - 支付处理
- `stripe-integration` - Stripe 支付
- `billing-automation` - 账单工作流

#### 操作
1. 安装并配置 WooCommerce
2. 创建自定义产品类型
3. 自定义结账流程
4. 集成支付网关
5. 设置配送方式
6. 创建自定义订单状态
7. 实现订阅产品
8. 添加自定义邮件模板

#### WordPress 7.0 + WooCommerce 注意事项
- 使用新管理界面测试结账
- AI 连接器用于产品描述
- DataViews 用于订单管理屏幕
- RTC 用于协作订单编辑

#### 复制粘贴提示词
```
Use @payment-integration to set up WooCommerce with Stripe
```

```
Use @billing-automation to create subscription products in WooCommerce
```

### 阶段 5：性能优化

#### 要调用的技能
- `web-performance-optimization` - 性能优化
- `database-optimizer` - 数据库优化

#### 操作
1. 实现缓存（对象、页面、浏览器）
2. 优化图像（懒加载、WebP）
3. 压缩和合并资源
4. 启用 CDN
5. 优化数据库查询
6. 实现懒加载
7. 配置 OPcache
8. 设置 Redis/Memcached

#### WordPress 7.0 性能
- 客户端媒体处理
- 所有主题启用字体库
- 响应式网格区块优化
- 视图过渡减少感知加载时间

#### 性能检查清单
- [ ] 页面加载时间 < 3 秒
- [ ] 首字节时间 < 200ms
- [ ] 最大内容绘制 < 2.5s
- [ ] 累积布局偏移 < 0.1
- [ ] 首次输入延迟 < 100ms

#### 复制粘贴提示词
```
Use @web-performance-optimization to audit and improve WordPress performance
```

### 阶段 6：安全加固

#### 要调用的技能
- `security-auditor` - 安全审计
- `wordpress-penetration-testing` - WordPress 安全测试
- `sast-configuration` - 静态分析

#### 操作
1. 更新 WordPress 核心、主题、插件
2. 实现安全头
3. 配置文件权限
4. 设置防火墙规则
5. 启用双因素身份验证
6. 实现速率限制
7. 配置安全日志
8. 设置恶意软件扫描

#### WordPress 7.0 安全注意事项
- PHP 7.4 最低要求（放弃 7.2/7.3 支持）
- 测试 Abilities API 权限边界
- 验证协作数据隔离
- AI 连接器凭证安全

#### 安全检查清单
- [ ] WordPress 核心已更新（推荐 7.0+）
- [ ] 所有插件/主题已更新
- [ ] 强制使用强密码
- [ ] 已启用双因素身份验证
- [ ] 已配置安全头
- [ ] 已禁用或保护 XML-RPC
- [ ] 已禁用文件编辑
- [ ] 已更改数据库前缀
- [ ] 已配置定期备份

#### 复制粘贴提示词
```
Use @wordpress-penetration-testing to audit WordPress security
```

```
Use @security-auditor to perform comprehensive security review
```

### 阶段 7：测试

#### 要调用的技能
- `test-automator` - 测试自动化
- `playwright-skill` - E2E 测试
- `webapp-testing` - Web 应用测试

#### 操作
1. 为自定义代码编写单元测试
2. 创建集成测试
3. 设置 E2E 测试
4. 测试跨浏览器兼容性
5. 测试响应式设计
6. 性能测试
7. 安全测试

#### WordPress 7.0 测试优先级
- 使用 iframe 文章编辑器测试
- 验证 DataViews 集成
- 测试协作 (RTC) 工作流
- 验证 AI 连接器功能
- 使用 watch() 测试 Interactivity API

#### 复制粘贴提示词
```
Use @playwright-skill to create E2E tests for WordPress site
```

### 阶段 8：部署

#### 要调用的技能
- `deployment-engineer` - 部署
- `cicd-automation-workflow-automate` - CI/CD
- `github-actions-templates` - GitHub Actions

#### 操作
1. 设置暂存环境
2. 配置部署管道
3. 设置数据库迁移
4. 配置环境变量
5. 部署期间启用维护模式
6. 部署到生产环境
7. 验证部署
8. 部署后监控

#### 复制粘贴提示词
```
Use @deployment-engineer to set up WordPress deployment pipeline
```

## WordPress 特定工作流

### 自定义文章类型开发（RTC 兼容）
```php
register_post_type('book', [
    'labels' => [...],
    'public' => true,
    'has_archive' => true,
    'supports' => ['title', 'editor', 'thumbnail', 'excerpt'],
    'menu_icon' => 'dashicons-book',
    'show_in_rest' => true,  // 为 RTC 启用
]);

// 为协作注册带有 REST API 的 meta
register_post_meta('book', 'isbn', [
    'type' => 'string',
    'single' => true,
    'show_in_rest' => true,
    'sanitize_callback' => 'sanitize_text_field',
]);
```

### 自定义 REST API 端点
```php
add_action('rest_api_init', function() {
    register_rest_route('myplugin/v1', '/books', [
        'methods' => 'GET',
        'callback' => 'get_books',
        'permission_callback' => '__return_true',
    ]);
});
```

### WordPress 7.0 AI 连接器使用
```php
// 使用 AI 自动生成文章摘要
add_action('save_post', function($post_id, $post) {
    if (wp_is_post_autosave($post_id) || wp_is_post_revision($post_id)) {
        return;
    }
    
    // 如果摘要已存在则跳过
    if (!empty($post->post_excerpt)) {
        return;
    }
    
    $content = strip_tags($post->post_content);
    if (empty($content)) {
        return;
    }
    
    // 检查 AI 客户端是否可用
    if (!function_exists('wp_ai_client_prompt')) {
        return;
    }
    
    // 使用输入构建提示词
    $result = wp_ai_client_prompt(
        'Create a brief 2-sentence summary of this content: ' . substr($content, 0, 1000)
    );
    
    if (is_wp_error($result)) {
        return; // 静默失败 - 不阻止文章保存
    }
    
    // 使用 temperature 获得一致的输出
    $result->using_temperature(0.3);
    $summary = $result->generate_text();
    
    if ($summary && !is_wp_error($summary)) {
        wp_update_post([
            'ID' => $post_id,
            'post_excerpt' => sanitize_textarea_field($summary)
        ]);
    }
}, 10, 2);
```

### 纯 PHP 区块注册（WordPress 7.0）
```php
// 完全在 PHP 中注册区块
register_block_type('my-plugin/hello-world', [
    'render_callback' => function($attributes, $content) {
        return '<p class="hello-world">Hello, World!</p>';
    },
    'attributes' => [
        'message' => ['type' => 'string', 'default' => 'Hello!']
    ],
]);
```

### Abilities API 注册
```php
// 在正确的钩子上注册能力类别
add_action('wp_abilities_api_categories_init', function() {
    wp_register_ability_category('content-creation', [
        'label' => __('Content Creation', 'my-plugin'),
        'description' => __('Abilities for generating and managing content', 'my-plugin'),
    ]);
});

// 在正确的钩子上注册能力
add_action('wp_abilities_api_init', function() {
    wp_register_ability('my-plugin/generate-summary', [
        'label' => __('Generate Post Summary', 'my-plugin'),
        'description' => __('Creates an AI-powered summary of a post', 'my-plugin'),
        'category' => 'content-creation',
        'input_schema' => [
            'type' => 'object',
            'properties' => [
                'post_id' => ['type' => 'integer', 'description' => 'The post ID to summarize']
            ],
            'required' => ['post_id']
        ],
        'output_schema' => [
            'type' => 'object',
            'properties' => [
                'summary' => ['type' => 'string', 'description' => 'The generated summary']
            ]
        ],
        'execute_callback' => 'my_plugin_generate_summary_handler',
        'permission_callback' => function() {
            return current_user_can('edit_posts');
        }
    ]);
});

// 能力的处理函数
function my_plugin_generate_summary_handler($input) {
    $post_id = isset($input['post_id']) ? absint($input['post_id']) : 0;
    $post = get_post($post_id);
    
    if (!$post) {
        return new WP_Error('invalid_post', 'Post not found');
    }
    
    $content = strip_tags($post->post_content);
    if (empty($content)) {
        return ['summary' => ''];
    }
    
    if (!function_exists('wp_ai_client_prompt')) {
        return new WP_Error('ai_unavailable', 'AI client not available');
    }
    
    $result = wp_ai_client_prompt('Summarize in 2 sentences: ' . substr($content, 0, 1000))
        ->using_temperature(0.3)
        ->generate_text();
    
    if (is_wp_error($result)) {
        return $result;
    }
    
    return ['summary' => sanitize_textarea_field($result)];
}
```

### WooCommerce 自定义产品类型
```php
add_action('init', function() {
    class WC_Product_Custom extends WC_Product {
        // 自定义产品实现
    }
});
```

## 质量门控

进入下一阶段前，验证：
- [ ] 所有自定义代码已测试
- [ ] 安全扫描通过
- [ ] 性能目标达成
- [ ] 跨浏览器测试完成
- [ ] 移动响应式验证
- [ ] 无障碍检查 (WCAG 2.1)
- [ ] WordPress 7.0 兼容性验证（新项目）

## 相关工作流套件

- `development` - 通用 Web 开发
- `security-audit` - 安全测试
- `testing-qa` - 测试工作流
- `ecommerce` - 电商开发

（文件结束 - 共 440 行）

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
