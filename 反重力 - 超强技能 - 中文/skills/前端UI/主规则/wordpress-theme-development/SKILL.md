---
name: wordpress-theme-development
description: "WordPress 主题开发工作流，涵盖主题架构、模板层级、自定义文章类型、块编辑器支持、响应式设计以及 WordPress 7.0 新特性：DataViews、Pattern 编辑、导航浮层和后台刷新。触发词：WordPress 主题、主题开发、Gutenberg、block editor、theme.json、模板层级、自定义文章类型、WP 7.0"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# WordPress 主题开发工作流

## 概述

用于从头创建自定义 WordPress 主题的专业工作流，包括现代块编辑器（Gutenberg）支持、模板层级、响应式设计以及 WordPress 7.0 增强功能。

## WordPress 7.0 主题特性

1. **后台刷新**
   - 新的默认配色方案
   - 后台页面之间的视图过渡
   - 现代化的排版和间距

2. **Pattern 编辑**
   - 未同步 Pattern 默认采用 ContentOnly 模式
   - `disableContentOnlyForUnsyncedPatterns` 设置
   - 每个块实例的自定义 CSS

3. **导航浮层**
   - 可自定义的导航浮层
   - 改进的移动端导航

4. **新增块**
   - Icon 块
   - 带过滤器的 Breadcrumbs 块
   - 响应式网格块

5. **Theme.json 增强**
   - 伪元素支持
   - 尊重块定义的功能选择器
   - 增强的自定义 CSS

6. **Iframe 编辑器**
   - Block API v3+ 支持 iframe 文章编辑器
   - 7.1 全面强制，7.0 可选启用

## 何时使用本工作流

在以下场景使用本工作流：
- 创建自定义 WordPress 主题
- 将设计稿转换为 WordPress 主题
- 添加块编辑器支持
- 实现自定义文章类型
- 构建子主题
- 实现 WordPress 7.0 设计特性

## 工作流阶段

### 阶段 1：主题初始化

#### 调用的技能
- `app-builder` - 项目脚手架
- `frontend-developer` - 前端开发

#### 操作步骤
1. 创建主题目录结构
2. 使用主题头设置 style.css
3. 创建 functions.php
4. 配置主题支持
5. 设置脚本/样式的引入

#### WordPress 7.0 主题头
```css
/*
Theme Name: My Custom Theme
Theme URI: https://example.com
Author: Developer Name
Author URI: https://example.com
Description: A WordPress 7.0 compatible theme with modern design
Version: 1.0.0
Requires at least: 6.0
Requires PHP: 7.4
License: GNU General Public License v2
License URI: https://www.gnu.org/licenses/gpl-2.0.html
Text Domain: my-custom-theme
Tags: block-patterns, block-styles, editor-style, wide-blocks
*/
```

#### 复制粘贴提示词
```
Use @app-builder to scaffold a new WordPress theme project
```

### 阶段 2：模板层级

#### 调用的技能
- `frontend-developer` - 模板开发

#### 操作步骤
1. 创建 index.php（回退模板）
2. 实现 header.php 和 footer.php
3. 为文章创建 single.php
4. 为页面创建 page.php
5. 添加 archive.php 用于归档
6. 实现 search.php 和 404.php

#### WordPress 7.0 模板注意事项
- 使用 iframe 编辑器测试
- 验证视图过渡正常工作
- 检查新后台配色方案的兼容性

#### 复制粘贴提示词
```
Use @frontend-developer to create WordPress template files
```

### 阶段 3：主题函数

#### 调用的技能
- `backend-dev-guidelines` - 后端模式

#### 操作步骤
1. 注册导航菜单
2. 添加主题支持（缩略图、RSS 等）
3. 注册小工具区域
4. 创建自定义模板标签
5. 实现辅助函数

#### WordPress 7.0 theme.json 配置
```json
{
  "$schema": "https://schemas.wp.org/trunk/theme.json",
  "version": 3,
  "settings": {
    "appearanceTools": true,
    "layout": {
      "contentSize": "1200px",
      "wideSize": "1400px"
    },
    "background": {
      "backgroundImage": true
    },
    "typography": {
      "fontFamilies": true,
      "fontSizes": true
    },
    "spacing": {
      "margin": true,
      "padding": true
    },
    "blocks": {
      "core/heading": {
        "typography": {
          "fontSizes": ["24px", "32px", "48px"]
        }
      }
    }
  },
  "styles": {
    "color": {
      "background": "#ffffff",
      "text": "#1a1a1a"
    },
    "elements": {
      "link": {
        "color": {
          "text": "#0066cc"
        }
      }
    }
  },
  "customTemplates": [
    {
      "name": "page-home",
      "title": "Homepage",
      "postTypes": ["page"]
    }
  ],
  "templateParts": [
    {
      "name": "header",
      "title": "Header",
      "area": "header"
    }
  ]
}
```

#### 复制粘贴提示词
```
Use @backend-dev-guidelines to create theme functions
```

### 阶段 4：自定义文章类型

#### 调用的技能
- `wordpress-penetration-testing` - WordPress 模式

#### 操作步骤
1. 注册自定义文章类型
2. 创建自定义分类法
3. 添加自定义元数据框
4. 实现自定义字段
5. 创建归档模板

#### 兼容 RTC 的 CPT 注册
```php
register_post_type('portfolio', [
    'labels' => [
        'name' => __('Portfolio', 'my-theme'),
        'singular_name' => __('Portfolio Item', 'my-theme')
    ],
    'public' => true,
    'has_archive' => true,
    'show_in_rest' => true,  // Enable for RTC
    'supports' => ['title', 'editor', 'thumbnail', 'excerpt', 'custom-fields'],
    'menu_icon' => 'dashicons-portfolio',
]);

// Register meta for collaboration
register_post_meta('portfolio', 'client_name', [
    'type' => 'string',
    'single' => true,
    'show_in_rest' => true,
    'sanitize_callback' => 'sanitize_text_field',
]);
```

#### 复制粘贴提示词
```
Use @wordpress-penetration-testing to understand WordPress CPT patterns
```

### 阶段 5：块编辑器支持

#### 调用的技能
- `frontend-developer` - 块开发

#### 操作步骤
1. 启用块编辑器支持
2. 注册自定义块
3. 创建块样式
4. 添加块 Pattern
5. 配置块模板

#### WordPress 7.0 块特性
- Block API v3 是参考模型
- 仅 PHP 的块注册
- 每个块实例的自定义 CSS
- 块可见性控制（基于视口）

#### 使用 ContentOnly 的块 Pattern（WP 7.0）
```json
{
    "name": "my-theme/hero-section",
    "title": "Hero Section",
    "contentOnly": true,
    "content": [
        {
            "name": "core/cover",
            "attributes": {
                "url": "{{hero_image}}",
                "overlay": "black",
                "dimRatio": 50
            },
            "innerBlocks": [
                {
                    "name": "core/heading",
                    "attributes": {
                        "level": 1,
                        "textAlign": "center",
                        "content": "{{hero_title}}"
                    }
                },
                {
                    "name": "core/paragraph",
                    "attributes": {
                        "align": "center",
                        "content": "{{hero_description}}"
                    }
                }
            ]
        }
    ]
}
```

#### 导航浮层模板部分
```php
// template-parts/header-overlay.php
?>
<nav class="header-navigation-overlay" aria-label="<?php esc_attr_e('Overlay Menu', 'my-theme'); ?>">
    <button class="overlay-close" aria-label="<?php esc_attr_e('Close menu', 'my-theme'); ?>">
        <span class="close-icon" aria-hidden="true">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </span>
    </button>
    <?php
    wp_nav_menu([
        'theme_location' => 'primary',
        'container' => false,
        'menu_class' => 'overlay-menu',
        'fallback_cb' => false,
    ]);
    ?>
</nav>
```

#### 复制粘贴提示词
```
Use @frontend-developer to create custom Gutenberg blocks
```

### 阶段 6：样式与设计

#### 调用的技能
- `frontend-design` - UI 设计
- `tailwind-patterns` - Tailwind CSS

#### 操作步骤
1. 实现响应式设计
2. 添加 CSS 框架或自定义样式
3. 创建设计系统
4. 实现主题自定义器
5. 添加无障碍功能

#### WordPress 7.0 后台刷新注意事项
```css
/* Support new admin color scheme */
@media (prefers-color-scheme: dark) {
    :root {
        --admin-color: modern;
    }
}

/* View transitions */
.wp-admin {
    view-transition-name: none;
}

body {
    view-transition-name: page;
}
```

#### CSS 自定义属性（WP 7.0）
```css
:root {
    /* New DataViews colors */
    --wp-dataviews-color-background: #ffffff;
    --wp-dataviews-color-border: #e0e0e0;

    /* Navigation overlay */
    --wp-overlay-menu-background: #1a1a1a;
    --wp-overlay-menu-text: #ffffff;
}
```

#### 复制粘贴提示词
```
Use @frontend-design to create responsive theme design
```

### 阶段 7：WordPress 7.0 特性集成

#### 面包屑块支持
```php
// Add breadcrumb filters for custom post types
add_filter('wp_breadcrumb_args', function($args) {
    $args['separator'] = '<span class="breadcrumb-separator"> / </span>';
    $args['before'] = '<nav class="breadcrumb" aria-label="Breadcrumb">';
    $args['after'] = '</nav>';
    return $args;
});

// Add custom breadcrumb trail for CPT
add_action('breadcrumb_items', function($trail, $crumbs) {
    if (is_singular('portfolio')) {
        $portfolio_page = get_page_by_path('portfolio');
        if ($portfolio_page) {
            array_splice($trail->crumbs, 1, 0, [
                [
                    'title' => get_the_title($portfolio_page),
                    'url' => get_permalink($portfolio_page)
                ]
            ]);
        }
    }
}, 10, 2);
```

#### 图标块支持
```php
// Add custom icons for Icon block via pattern category
add_action('init', function() {
    register_block_pattern_category('my-theme/icons', [
        'label' => __('Theme Icons', 'my-theme'),
        'description' => __('Custom icons for use in the Icon block', 'my-theme'),
    ]);
});

// For actual SVG icons in the Icon block, use block.json or PHP registration
add_action('init', function() {
    register_block_pattern('my-theme/custom-icons', [
        'title' => __('Custom Icon Set', 'my-theme'),
        'categories' => ['my-theme/icons'],
        'content' => '<!-- Pattern content with Icon blocks -->'
    ]);
});
```

### 阶段 8：测试

#### 调用的技能
- `playwright-skill` - 浏览器测试
- `webapp-testing` - Web 应用测试

#### 操作步骤
1. 跨浏览器测试
2. 验证响应式断点
3. 测试块编辑器
4. 检查无障碍
5. 性能测试

#### WordPress 7.0 测试清单
- [ ] 使用 iframe 编辑器测试
- [ ] 验证视图过渡
- [ ] 检查后台配色方案
- [ ] 测试导航浮层
- [ ] 验证 contentOnly Pattern
- [ ] 在 CPT 归档上测试面包屑

#### 复制粘贴提示词
```
Use @playwright-skill to test WordPress theme
```

## 主题结构

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
├── comments.php
├── template-parts/
│   ├── header/
│   ├── footer/
│   ├── navigation/
│   └── content/
├── patterns/           # Block patterns (WP 7.0)
├── templates/          # Site editor templates
├── inc/
│   ├── class-theme.php
│   └── supports.php
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── languages/
```

## WordPress 7.0 主题清单

- [ ] PHP 7.4+ 要求已记录
- [ ] 使用 theme.json v3 模式
- [ ] 块 Pattern 已测试
- [ ] 支持 ContentOnly 编辑
- [ ] 已实现导航浮层
- [ ] 为 CPT 添加了面包屑过滤器
- [ ] 视图过渡工作正常
- [ ] 后台刷新兼容
- [ ] CPT meta 已设置 show_in_rest
- [ ] iframe 编辑器已测试

## 质量门

- [ ] 所有模板正常工作
- [ ] 支持块编辑器
- [ ] 响应式设计已验证
- [ ] 无障碍已检查
- [ ] 性能已优化
- [ ] 跨浏览器已测试
- [ ] WordPress 7.0 兼容性已验证

## 相关工作流包

- `wordpress` - WordPress 开发
- `wordpress-plugin-development` - 插件开发
- `wordpress-woocommerce` - WooCommerce

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来并请求澄清。
