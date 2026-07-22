---
name: web-artifacts-builder
description: "要构建强大的 claude.ai 前端工件，请按照以下步骤操作："
risk: unknown
source: community
date_added: "2026-02-27"
---

# Web 工件构建器

要构建强大的 claude.ai 前端工件，请按照以下步骤操作：
1. 使用 `scripts/init-artifact.sh` 初始化前端仓库
2. 通过编辑生成的代码来开发你的工件
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包到单个 HTML 文件中
4. 向用户展示工件
5. （可选）测试工件

**技术栈**：React 18 + TypeScript + Vite + Parcel（打包）+ Tailwind CSS + shadcn/ui

## 设计与样式指南

非常重要：为了避免常见的所谓 "AI 痕迹"，请避免使用过度居中的布局、紫色渐变、统一圆角以及 Inter 字体。

## 快速开始

### 步骤 1：初始化项目

运行初始化脚本以创建一个新的 React 项目：
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

这会创建一个完整配置的项目，包含：
- ✅ React + TypeScript（通过 Vite）
- ✅ Tailwind CSS 3.4.1 以及 shadcn/ui 主题系统
- ✅ 路径别名（`@/`）已配置
- ✅ 预装 40+ 个 shadcn/ui 组件
- ✅ 包含所有 Radix UI 依赖
- ✅ 已配置 Parcel 用于打包（通过 .parcelrc）
- ✅ 兼容 Node 18+（自动检测并固定 Vite 版本）

### 步骤 2：开发你的工件

要构建工件，请编辑生成的文件。有关指导，请参阅下方的 **常见开发任务**。

### 步骤 3：打包为单个 HTML 文件

要将 React 应用打包为单个 HTML 工件：
```bash
bash scripts/bundle-artifact.sh
```

这会创建 `bundle.html` —— 一个自包含的工件，所有 JavaScript、CSS 和依赖项都已内联。该文件可以直接在 Claude 对话中作为工件分享。

**要求**：你的项目根目录下必须存在 `index.html`。

**脚本功能**：
- 安装打包依赖（parcel、@parcel/config-default、parcel-resolver-tspaths、html-inline）
- 创建 `.parcelrc` 配置，支持路径别名
- 使用 Parcel 构建（不生成 source map）
- 使用 html-inline 将所有资源内联到单个 HTML 中

### 步骤 4：与用户分享工件

最后，在对话中与用户分享打包好的 HTML 文件，以便他们可以将其作为工件查看。

### 步骤 5：测试/可视化工件（可选）

注意：这一步完全是可选的，仅在必要或被要求时才执行。

要测试/可视化工件，请使用可用工具（包括其他技能或 Playwright、Puppeteer 等内置工具）。通常应避免事先测试工件，因为这会在请求与看到完成工件之间增加延迟。如果被要求或出现问题，可在展示工件之后再进行测试。

## 参考资料

- **shadcn/ui 组件**：https://ui.shadcn.com/docs/components

## 使用时机
此技能适用于执行上述概览中描述的工作流或操作。

## 局限性
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将此输出视为特定环境验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
