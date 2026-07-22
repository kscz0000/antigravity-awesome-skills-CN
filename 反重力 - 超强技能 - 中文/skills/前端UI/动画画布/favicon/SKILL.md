---
name: favicon
argument-hint: [源图像路径]
description: 从源图像生成完整的 favicon 图标集。触发词：favicon、网站图标、图标生成、favicon生成、apple-touch-icon、网站图标生成、favicon图标、网页图标
allowed-tools: Bash(magick *), Bash(which *), Bash(cp *), Bash(mkdir *)
context: fork
risk: unknown
source: community
metadata:
  author: Shpigford
  version: "1.0"
---

从 `$1` 路径的源图像生成完整的 favicon 图标集，并使用适当的 link 标签更新项目的 HTML。

## 使用时机

- 需要从单个源图像生成完整的 favicon 图标集。
- 任务包括将资源放置到正确的框架特定静态目录中，并更新 HTML link 标签。
- 需要一个工作流来验证源图像、检测项目类型并输出正确的 favicon 文件。

## 前置条件

首先，通过运行以下命令验证 ImageMagick v7+ 是否已安装：
```bash
which magick
```

如果未找到，停止并指导用户安装：
- **macOS**: `brew install imagemagick`
- **Linux**: `sudo apt install imagemagick`

## 步骤 1：验证源图像

1. 验证源图像是否存在于提供的路径：`$1`
2. 检查文件扩展名是否为支持的格式（PNG、JPG、JPEG、SVG、WEBP、GIF）
3. 如果文件不存在或不是有效的图像格式，报告错误并停止

注意源文件是否为 SVG 文件——如果是，它也会被复制为 `favicon.svg`。

## 步骤 2：检测项目类型和静态资源目录

检测项目类型并确定静态资源应放置的位置。按以下顺序检查：

| 框架 | 检测方式 | 静态资源目录 |
|-----------|-----------|------------------------|
| **Rails** | 存在 `config/routes.rb` | `public/` |
| **Next.js** | 存在 `next.config.*` | `public/` |
| **Gatsby** | 存在 `gatsby-config.*` | `static/` |
| **SvelteKit** | 存在 `svelte.config.*` | `static/` |
| **Astro** | 存在 `astro.config.*` | `public/` |
| **Hugo** | 存在 `hugo.toml` 或 `config.toml` 且包含 Hugo 标记 | `static/` |
| **Jekyll** | 存在 `_config.yml` 且包含 Jekyll 标记 | 根目录（与 `index.html` 同级） |
| **Vite** | 存在 `vite.config.*` | `public/` |
| **Create React App** | `package.json` 包含 `react-scripts` 依赖 | `public/` |
| **Vue CLI** | 存在 `vue.config.*` | `public/` |
| **Angular** | 存在 `angular.json` | `src/assets/` |
| **Eleventy** | 存在 `.eleventy.js` 或 `eleventy.config.*` | 检查 `_site` 输出或根目录 |
| **静态 HTML** | 根目录存在 `index.html` | 与 `index.html` 同目录 |

**重要**：如果发现现有的 favicon 文件（如 `favicon.ico`、`apple-touch-icon.png`），无论框架检测结果如何，都使用它们的位置作为目标目录。

报告检测到的项目类型和将要使用的静态资源目录。

**不确定时请询问**：如果您对静态资源应放置的位置不是 100% 确定（例如，项目结构模糊、多个潜在位置、不熟悉的框架），请在继续之前使用 `AskUserQuestionTool` 确认目标目录。与其把文件放错地方，不如先问清楚。

## 步骤 3：确定应用名称

从以下来源查找应用名称（按优先级顺序）：

1. **现有的 `site.webmanifest`** - 检查检测到的静态资源目录中是否存在现有的 manifest，提取 `name` 字段
2. **`package.json`** - 提取 `name` 字段（如果存在）
3. **Rails `config/application.rb`** - 提取模块名称（例如，`module MyApp` → "MyApp"）
4. **目录名称** - 使用当前工作目录名称作为后备

必要时将名称转换为标题大小写（例如，"my-app" → "My App"）。

## 步骤 4：确保静态资源目录存在

检查检测到的静态资源目录是否存在。如果不存在，则创建它。

## 步骤 5：生成 Favicon 文件

运行这些 ImageMagick 命令生成所有 favicon 文件。将 `[STATIC_DIR]` 替换为步骤 2 中检测到的静态资源目录。

**重要**：`-background none` 标志必须放在输入文件**之前**，以便在渲染 SVG 时正确保留透明度。放在输入文件之后会导致白色背景。

### favicon.ico（多分辨率：16x16、32x32、48x48）
```bash
magick -background none "$1" \
  \( -clone 0 -resize 16x16 \) \
  \( -clone 0 -resize 32x32 \) \
  \( -clone 0 -resize 48x48 \) \
  -delete 0 -alpha on \
  [STATIC_DIR]/favicon.ico
```

### favicon-96x96.png
```bash
magick -background none "$1" -resize 96x96 -alpha on [STATIC_DIR]/favicon-96x96.png
```

### apple-touch-icon.png (180x180)
```bash
magick -background none "$1" -resize 180x180 -alpha on [STATIC_DIR]/apple-touch-icon.png
```

### web-app-manifest-192x192.png
```bash
magick -background none "$1" -resize 192x192 -alpha on [STATIC_DIR]/web-app-manifest-192x192.png
```

### web-app-manifest-512x512.png
```bash
magick -background none "$1" -resize 512x512 -alpha on [STATIC_DIR]/web-app-manifest-512x512.png
```

### favicon.svg（仅当源文件为 SVG 时）
如果源文件扩展名为 `.svg`，则复制它：
```bash
cp "$1" [STATIC_DIR]/favicon.svg
```

## 步骤 6：创建/更新 site.webmanifest

创建或更新 `[STATIC_DIR]/site.webmanifest`，内容如下（替换检测到的应用名称）：

```json
{
  "name": "[APP_NAME]",
  "short_name": "[APP_NAME]",
  "icons": [
    {
      "src": "/web-app-manifest-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/web-app-manifest-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    }
  ],
  "theme_color": "#ffffff",
  "background_color": "#ffffff",
  "display": "standalone"
}
```

如果静态目录中已存在 `site.webmanifest`，保留现有的 `theme_color`、`background_color` 和 `display` 值，同时更新 `name`、`short_name` 和 `icons` 数组。

## 步骤 7：更新 HTML/Layout 文件

根据检测到的项目类型，更新相应的文件。根据静态资源目录相对于 Web 根目录的位置调整 `href` 路径：
- 如果静态文件位于 `public/` 或 `static/` 且从根目录提供服务 → 使用 `/favicon.ico`
- 如果静态文件位于 `src/assets/` → 使用 `/assets/favicon.ico`
- 如果静态文件与 HTML 位于同一目录 → 使用 `./favicon.ico` 或直接使用 `favicon.ico`

### 对于 Rails 项目

编辑 `app/views/layouts/application.html.erb`。找到 `<head>` 部分，添加/替换 favicon 相关标签：

```html
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="shortcut icon" href="/favicon.ico" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
<meta name="apple-mobile-web-app-title" content="[APP_NAME]" />
<link rel="manifest" href="/site.webmanifest" />
```

**重要**：
- 如果源文件不是 SVG，省略 `<link rel="icon" type="image/svg+xml" href="/favicon.svg" />` 这一行
- 在添加新标签之前，删除任何现有的 `<link rel="icon"`、`<link rel="shortcut icon"`、`<link rel="apple-touch-icon"` 或 `<link rel="manifest"` 标签
- 将这些标签放在 `<head>` 部分的顶部附近，如果存在 `<meta charset>` 和 `<meta name="viewport">`，则放在它们之后

### 对于 Next.js 项目

编辑检测到的 layout 文件（`app/layout.tsx` 或 `src/app/layout.tsx`）。更新或添加 `metadata` 导出以包含 icons 配置：

```typescript
export const metadata: Metadata = {
  // ... 保留现有的 metadata 字段
  icons: {
    icon: [
      { url: '/favicon.ico' },
      { url: '/favicon-96x96.png', sizes: '96x96', type: 'image/png' },
      { url: '/favicon.svg', type: 'image/svg+xml' },
    ],
    shortcut: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
  appleWebApp: {
    title: '[APP_NAME]',
  },
};
```

**重要**：
- 如果源文件不是 SVG，从 icon 数组中省略 `{ url: '/favicon.svg', type: 'image/svg+xml' }` 条目
- 如果 metadata 导出不存在，仅使用 icons 相关字段创建它
- 如果 metadata 导出已存在，将 icons 配置与现有字段合并

### 对于静态 HTML 项目

编辑检测到的 `index.html` 文件。在 `<head>` 部分添加与 Rails 相同的 HTML。

### 如果未检测到项目

跳过 HTML 更新，并告知用户需要手动将以下内容添加到其 HTML `<head>` 中：

```html
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="shortcut icon" href="/favicon.ico" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
<meta name="apple-mobile-web-app-title" content="[APP_NAME]" />
<link rel="manifest" href="/site.webmanifest" />
```

## 步骤 8：总结

报告完成情况，包括：
- 检测到的项目类型和框架
- 使用的静态资源目录
- 生成的文件列表
- manifest 和 HTML 中使用的应用名称
- 更新的 layout 文件（或注明是否需要手动更新）
- 注明是否有任何现有文件被覆盖

## 错误处理

- 如果未安装 ImageMagick，提供安装说明并停止
- 如果源图像不存在，报告尝试的确切路径并停止
- 如果 ImageMagick 命令失败，报告具体的错误消息
- 如果找不到 layout 文件进行 HTML 更新，仍然生成文件并指导手动添加 HTML

## 限制

- 仅当任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
