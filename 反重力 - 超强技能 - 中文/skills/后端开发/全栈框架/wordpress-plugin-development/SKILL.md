---
name: wordpress-plugin-development
description: "WordPress 插件开发工作流，涵盖插件架构、钩子、管理界面、REST API、安全最佳实践以及 WordPress 7.0 特性：实时协作（Real-Time Collaboration）、AI 连接器（AI Connectors）、Abilities API、DataViews 和纯 PHP 块（PHP-only blocks）。触发词：WordPress 插件、WordPress plugin、插件开发、WordPress 7.0、WordPress 钩子、WordPress 管理界面、WordPress REST API、插件安全、Abilities API、AI 连接器、实时协作、DataViews、纯 PHP 块。"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# WordPress 插件开发工作流

## 概述

用于创建 WordPress 插件的专业工作流，涵盖规范的架构、钩子系统、管理界面、REST API 端点以及安全实践。现已加入 WordPress 7.0 特性，支持现代插件开发。

## WordPress 7.0 插件开发

### 面向插件开发者的关键特性

1. **实时协作（Real-Time Collaboration, RTC）兼容性**
   - 基于 Yjs 的 CRDT，用于协同编辑
   - 通过 `sync.providers` 过滤器自定义传输
   - **要求**：注册 post meta 时设置 `show_in_rest => true`

2. **AI 连接器集成（AI Connector Integration）**
   - 通过 `wp_ai_client_prompt()` 接入不依赖特定提供商的 AI
   - 设置 > 连接器（Settings > Connectors）管理界面
   - 兼容 OpenAI、Claude、Gemini、Ollama

3. **Abilities API**
   - 为 AI 智能体声明插件能力
   - REST API：`/wp-json/abilities/v1/manifest`
   - 支持 MCP 适配器

4. **DataViews 与 DataForm**
   - 现代化的管理界面
   - 替代 WP_List_Table 模式
   - 内置验证

5. **纯 PHP 块（PHP-Only Blocks）**
   - 无需 JavaScript 即可注册块
   - 自动生成 Inspector 控件

## 何时使用本工作流

在以下场景使用本工作流：
- 创建自定义 WordPress 插件
- 扩展 WordPress 功能
- 构建管理界面
- 添加 REST API 端点
- 集成第三方服务
- 实现 WordPress 7.0 的 AI / 协作特性

## 工作流阶段

### 阶段 1：插件初始化

#### 调用的技能
- `app-builder` - 项目脚手架
- `backend-dev-guidelines` - 后端模式

#### 操作
1. 创建插件目录结构
2. 设置带头部信息的主插件文件
3. 实现激活/停用钩子
4. 配置自动加载
5. 配置 text domain

#### WordPress 7.0 插件头部
```php
/*
Plugin Name: My Plugin
Plugin URI: https://example.com/my-plugin
Description: A WordPress 7.0 compatible plugin with AI and RTC support
Version: 1.0.0
Requires at least: 6.0
Requires PHP: 7.4
Author: Developer Name
License: GPL2+
*/
```

#### 复制粘贴提示词
```
Use @app-builder to scaffold a new WordPress plugin
```

### 阶段 2：插件架构

#### 调用的技能
- `backend-dev-guidelines` - 架构模式

#### 操作
1. 设计插件类结构
2. 实现单例模式
3. 创建加载器类
4. 设置依赖注入
5. 配置插件生命周期

#### WordPress 7.0 架构注意事项
- 为 iframe 编辑器兼容性做准备
- 为支持协作的数据流做设计
- 考虑使用 Abilities API 进行 AI 集成

#### 复制粘贴提示词
```
Use @backend-dev-guidelines to design plugin architecture
```

### 阶段 3：钩子实现

#### 调用的技能
- `wordpress-penetration-testing` - WordPress 模式

#### 操作
1. 注册 action 钩子
2. 创建 filter 钩子
3. 实现回调函数
4. 设置钩子优先级
5. 添加条件钩子

#### 复制粘贴提示词
```
Use @wordpress-penetration-testing to understand WordPress hooks
```

### 阶段 4：管理界面

#### 调用的技能
- `frontend-developer` - 管理 UI

#### 操作
1. 创建管理菜单
2. 构建设置页面
3. 实现选项注册
4. 添加设置分区/字段
5. 创建管理通知

#### WordPress 7.0 管理注意事项
- 使用新的管理员配色方案进行测试
- 考虑使用 DataViews 进行数据展示
- 实现视图过渡（view transitions）
- 使用新的验证模式

#### DataViews 示例
```javascript
import { DataViews } from '@wordpress/dataviews';

const MyPluginDataView = () => {
    const data = [/* records */];
    const fields = [
        { id: 'title', label: 'Title', sortable: true },
        { id: 'status', label: 'Status', filterBy: true }
    ];
    const view = {
        type: 'table',
        perPage: 10,
        sort: { field: 'title', direction: 'asc' }
    };

    return (
        <DataViews
            data={data}
            fields={fields}
            view={view}
            onChangeView={handleViewChange}
        />
    );
};
```

#### 复制粘贴提示词
```
Use @frontend-developer to create WordPress admin interface
```

### 阶段 5：数据库操作

#### 调用的技能
- `database-design` - 数据库设计
- `postgresql` - 数据库模式

#### 操作
1. 创建自定义表
2. 实现 CRUD 操作
3. 添加数据验证
4. 设置数据清理（sanitization）
5. 创建数据升级例程

#### 兼容 RTC 的 Post Meta
```php
// Register meta for Real-Time Collaboration
register_post_meta('post', 'my_custom_field', [
    'type' => 'string',
    'single' => true,
    'show_in_rest' => true,  // Required for RTC
    'sanitize_callback' => 'sanitize_text_field',
]);

// For WP 7.0, also consider:
register_term_meta('category', 'my_term_field', [
    'type' => 'string',
    'show_in_rest' => true,
]);
```

#### 复制粘贴提示词
```
Use @database-design to design plugin database schema
```

### 阶段 6：REST API

#### 调用的技能
- `api-design-principles` - API 设计
- `api-patterns` - API 模式

#### 操作
1. 注册 REST 路由
2. 创建端点回调
3. 实现权限回调
4. 添加请求验证
5. 编写 API 端点文档

#### WordPress 7.0 REST API 增强
- Abilities API 集成
- AI 连接器端点
- 强化的验证

#### 复制粘贴提示词
```
Use @api-design-principles to create WordPress REST API endpoints
```

### 阶段 7：安全

#### 调用的技能
- `wordpress-penetration-testing` - WordPress 安全
- `security-scanning-security-sast` - 安全扫描

#### 操作
1. 实现 nonce 校验
2. 添加权限检查
3. 清理所有输入
4. 转义所有输出
5. 保护数据库查询

#### WordPress 7.0 安全注意事项
- 测试 Abilities API 权限边界
- 校验 AI 连接器的凭据处理
- 审查协作数据隔离
- 遵循 PHP 7.4+ 版本要求

#### 复制粘贴提示词
```
Use @wordpress-penetration-testing to audit plugin security
```

### 阶段 8：WordPress 7.0 特性

#### 调用的技能
- `api-design-principles` - AI 集成
- `backend-dev-guidelines` - 块开发

#### AI 连接器实现
```php
// Using WordPress 7.0 AI Connector
add_action('save_post', 'my_plugin_generate_ai_summary', 10, 2);

function my_plugin_generate_ai_summary($post_id, $post) {
    if (wp_is_post_autosave($post_id) || wp_is_post_revision($post_id)) {
        return;
    }
    
    // Check if AI client is available
    if (!function_exists('wp_ai_client_prompt')) {
        return;
    }
    
    $content = strip_tags($post->post_content);
    if (empty($content)) {
        return;
    }
    
    // Build prompt - direct string concatenation for input
    $result = wp_ai_client_prompt(
        'Create a compelling 2-sentence summary for social media: ' . substr($content, 0, 1000)
    );
    
    if (is_wp_error($result)) {
        return;
    }
    
    // Set temperature for consistent output
    $result->using_temperature(0.3);
    $summary = $result->generate_text();
    
    if ($summary && !is_wp_error($summary)) {
        update_post_meta($post_id, '_ai_summary', sanitize_textarea_field($summary));
    }
}
```

#### Abilities API 注册
```php
// Register ability categories on their own hook
add_action('wp_abilities_api_categories_init', function() {
    wp_register_ability_category('content-creation', [
        'label' => __('Content Creation', 'my-plugin'),
        'description' => __('Abilities for generating and managing content', 'my-plugin'),
    ]);
});

// Register abilities on their own hook
add_action('wp_abilities_api_init', function() {
    wp_register_ability('my-plugin/generate-summary', [
        'label' => __('Generate Summary', 'my-plugin'),
        'description' => __('Creates an AI-powered summary of content', 'my-plugin'),
        'category' => 'content-creation',
        'input_schema' => [
            'type' => 'object',
            'properties' => [
                'content' => ['type' => 'string'],
                'length' => ['type' => 'integer', 'default' => 2]
            ],
            'required' => ['content']
        ],
        'output_schema' => [
            'type' => 'object',
            'properties' => [
                'summary' => ['type' => 'string']
            ]
        ],
        'execute_callback' => 'my_plugin_generate_summary_cb',
        'permission_callback' => function() {
            return current_user_can('edit_posts');
        }
    ]);
});

// Handler callback
function my_plugin_generate_summary_cb($input) {
    $content = isset($input['content']) ? $input['content'] : '';
    $length = isset($input['length']) ? absint($input['length']) : 2;
    
    if (empty($content)) {
        return new WP_Error('empty_content', 'No content provided');
    }
    
    if (!function_exists('wp_ai_client_prompt')) {
        return new WP_Error('ai_unavailable', 'AI not available');
    }
    
    $prompt = sprintf('Create a %d-sentence summary of: %s', $length, substr($content, 0, 2000));
    
    $result = wp_ai_client_prompt($prompt)
        ->using_temperature(0.3)
        ->generate_text();
    
    if (is_wp_error($result)) {
        return $result;
    }
    
    return ['summary' => sanitize_textarea_field($result)];
}
```

#### 纯 PHP 块注册
```php
// Register block entirely in PHP (WordPress 7.0)
// Note: For full PHP-only blocks, use block.json with PHP render_callback

// First, create a block.json file in build/ or includes/blocks/
// Then register in PHP:

// Simple PHP-only block registration (WordPress 7.0+)
if (function_exists('register_block_type')) {
    register_block_type('my-plugin/featured-post', [
        'render_callback' => function($attributes, $content, $block) {
            $post_id = isset($attributes['postId']) ? absint($attributes['postId']) : 0;
            
            if (!$post_id) {
                $post_id = get_the_ID();
            }
            
            $post = get_post($post_id);
            
            if (!$post) {
                return '';
            }
            
            $title = esc_html($post->post_title);
            $excerpt = esc_html(get_the_excerpt($post));
            
            return sprintf(
                '<div class="featured-post"><h2>%s</h2><p>%s</p></div>',
                $title,
                $excerpt
            );
        },
        'attributes' => [
            'postId' => ['type' => 'integer', 'default' => 0],
            'showExcerpt' => ['type' => 'boolean', 'default' => true]
        ],
    ]);
}
```

#### 禁用协作（如需）
```javascript
// Disable RTC for specific post types
import { addFilter } from '@wordpress/hooks';

addFilter(
    'sync.providers',
    'my-plugin/disable-collab',
    () => []
);
```

### 阶段 9：测试

#### 调用的技能
- `test-automator` - 测试自动化
- `php-pro` - PHP 测试

#### 操作
1. 配置 PHPUnit
2. 编写单元测试
3. 编写集成测试
4. 使用 WordPress 测试套件进行测试
5. 配置 CI

#### WordPress 7.0 测试优先级
- 测试 RTC 兼容性
- 验证 AI 连接器功能
- 验证 DataViews 集成
- 使用 `watch()` 测试 Interactivity API

#### 复制粘贴提示词
```
Use @test-automator to set up plugin testing
```

## 插件结构

```
plugin-name/
├── plugin-name.php
├── includes/
│   ├── class-plugin.php
│   ├── class-loader.php
│   ├── class-activator.php
│   └── class-deactivator.php
├── admin/
│   ├── class-plugin-admin.php
│   ├── css/
│   └── js/
├── public/
│   ├── class-plugin-public.php
│   ├── css/
│   └── js/
├── blocks/           # PHP-only blocks (WP 7.0)
├── abilities/        # Abilities API
├── ai/               # AI Connector integration
├── languages/
└── vendor/
```

## WordPress 7.0 兼容性检查清单

- [ ] PHP 7.4+ 版本要求已记录
- [ ] 为 RTC 注册 post meta 时设置了 `show_in_rest => true`
- [ ] Meta boxes 已迁移到基于块的 UI
- [ ] AI 连接器集成已测试
- [ ] Abilities API 已注册（如适用）
- [ ] DataViews 集成已测试（如适用）
- [ ] Interactivity API 使用 `watch()` 而非 `effect`
- [ ] 在 iframe 编辑器中测试通过
- [ ] 协作降级方案可用（文章锁 post locking）

## 质量门控

- [ ] 插件可无错激活
- [ ] 所有钩子正常工作
- [ ] 管理界面功能完整
- [ ] 安全措施已实施
- [ ] 测试通过
- [ ] 文档完整
- [ ] WordPress 7.0 兼容性已验证

## 相关工作流包

- `wordpress` - WordPress 开发
- `wordpress-theme-development` - 主题开发
- `wordpress-woocommerce` - WooCommerce

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要把输出视为可替代环境特定验证、测试或专家审查的产物。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并要求澄清。
