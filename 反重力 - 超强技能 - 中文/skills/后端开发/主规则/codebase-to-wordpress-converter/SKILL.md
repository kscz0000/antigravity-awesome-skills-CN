---
name: codebase-to-wordpress-converter
description: "将任意代码库（React/HTML/Next.js）转换为像素级完美、SEO优化且动态的 WordPress 主题。当用户要求将 React 项目转为 WordPress 主题、需要像素级完美匹配、或审计 WordPress 转换质量时使用。"
risk: safe
source: community
date_added: "2026-04-12"
---

# Codebase to WordPress Converter

## 概述

本技能专为将静态或 React 前端高保真转换为功能完整、CMS 驱动的 WordPress 主题而设计。它扮演**资深 WordPress 架构师**、**React 专家**和**QA 工程师**三重角色，确保 100% 像素级完美匹配，同时深度集成 ACF、动态菜单和技术 SEO 保留等 WordPress 核心功能。

## 使用场景

- 将 React（CRA/Vite/Next.js）或 HTML 项目转换为 WordPress 主题
- 客户要求与原始源码 100% 像素级完美匹配
- 审计现有 WordPress 转换的结构或 SEO 缺陷
- 确保技术 SEO（Schema、Meta 标签、标题层级）完整保留

## 核心能力

### 分阶段转换与审计
本技能遵循严格的 4 阶段取证流程：
1. **阶段 1：取证 UI 对比**：React 组件与 WordPress 模板的并排表格审计，发现差异
2. **阶段 2：全面审计**：深入检查 UI、SEO、CMS 可编辑性、导航、功能和性能
3. **阶段 3：行动计划**：任务分类为 **安全**、**有风险** 或 **阻塞**，防止破坏 UI
4. **阶段 4：迭代修复**：每次执行一个安全任务，验证后再进行下一步

### 绝对 UI 锁定
严格执行不可协商的规则：
- 禁止修改布局、间距、字体或颜色
- 精确保留 Tailwind 或 CSS 类名
- 零改动 DOM 结构或 HTML 嵌套

## 分步指南

### 1. 发现与取证审计
首先识别源码中的所有组件。创建 UI 对比表，将原始源码输出与目标 WordPress 输出进行对比。
- *规则：此阶段禁止修复，仅做检测。*

### 2. 策略性字段映射
将静态 React/HTML 内容映射为动态 WordPress 函数：
- 用 `the_title()`、`get_field()` 或 `the_content()` 替换静态文本
- 用 `get_template_directory_uri()` 替换静态路径

### 3. 核心钩子实现
确保每个主题正确包含基础 WordPress 钩子：
- **布局文件（`header.php` / `footer.php`）**：必须在 `</head>` 前调用 `wp_head()`，在 `</body>` 前调用 `wp_footer()`
- **页面模板**：必须调用 `get_header()` 和 `get_footer()`
- 使用 `register_nav_menus()` 实现动态导航，且不破坏原始 HTML 结构

### 4. 验证与实时追踪
维护实时追踪器，记录总问题数、已修复数和剩余数。每次修复后必须确认：
- ✅ 无 UI 变化
- ✅ 无 DOM 变化
- ✅ 无类名变化

## 示例

### 示例 1：导航转换
```php
// 错误：静态替换会添加包装器
wp_nav_menu(['theme_location' => 'primary']);

// 正确：保留原始 Tailwind 类和结构
wp_nav_menu([
    'theme_location' => 'primary',
    'container' => false,
    'items_wrap' => '<ul class="flex space-x-8">%3$s</ul>',
    'walker' => new Custom_Tailwind_Walker()
]);
```

### 示例 2：资源路径处理
```php
// 源码: <img src="/images/logo.png" />
// WP 转换:
<img src="<?php echo get_template_directory_uri(); ?>/assets/images/logo.png" alt="Logo" />
```

## 最佳实践

- ✅ **推荐：** 使用 `get_page_by_path()` 实现健壮的内部链接
- ✅ **推荐：** 在 `functions.php` 中实现 ACF（Advanced Custom Fields）回退机制
- ✅ **推荐：** 将 Tailwind 配置保留在 `header.php` 中，确保全局样式生效
- ❌ **禁止：** 添加 div 包装器或重命名类名以"清理"代码
- ❌ **禁止：** 使用 WordPress 默认样式（如果与原始设计冲突）

## 附加资源

- [ACF 文档](https://www.advancedcustomfields.com/resources/)
- [Tailwind CSS in WordPress](https://tailwindcss.com/docs/installation)
- [WordPress 主题开发手册](https://developer.wordpress.org/themes/)

## 局限性
- 仅在任务明确匹配上述范围时使用本技能
- 输出不能替代环境特定的验证、测试或专家审查
- 若缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清
