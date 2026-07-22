---
name: expo-cicd-workflows
description: >
  帮助理解与编写 Expo 项目的 EAS workflow YAML 文件。当用户询问 Expo 或 EAS 场景下的 CI/CD 或 workflow、提到 `.eas/workflows/`、或想要 EAS 构建流水线与部署自动化帮助时使用。触发词：EAS workflow、CI/CD、.eas/workflows、EAS 构建、Expo 部署、GitHub Actions。
allowed-tools: "Read,Write,Bash(node:*)"
risk: unknown
source: community
version: 1.0.0
license: MIT License
---

# EAS Workflows 技能

帮助开发者编写与编辑 EAS CI/CD workflow YAML 文件。

## 何时使用

- 你需要为 Expo 项目创建、编辑或验证 `.eas/workflows/*.yml` 文件。
- 任务涉及 EAS 构建流水线、部署自动化、workflow 触发器，或 Expo CI/CD 配置。
- 你需要基于 schema 的 workflow 指导，而非依赖可能过时的记忆语法。

## 参考文档

在生成或验证 workflow 文件前，先抓取以下资源。使用本技能 `scripts/` 目录下的抓取脚本（用 Node.js 实现），用 ETag 缓存响应以提高效率：

```bash
# 抓取资源
node {baseDir}/scripts/fetch.js <url>
```

1. **JSON Schema** —— https://api.expo.dev/v2/workflows/schema
   - **必须**抓取此 schema
   - 验证的真理之源
   - 所有 job 类型及其必需/可选参数
   - 触发器类型与配置
   - Runner 类型、VM 镜像、所有枚举

2. **语法文档** —— https://raw.githubusercontent.com/expo/expo/refs/heads/main/docs/pages/eas/workflows/syntax.mdx
   - workflow YAML 语法概览
   - 示例与英文解释
   - 表达式语法与上下文

3. **预打包 Job** —— https://raw.githubusercontent.com/expo/expo/refs/heads/main/docs/pages/eas/workflows/pre-packaged-jobs.mdx
   - 支持的预打包 job 类型文档
   - job 特定参数与输出

不要依赖记忆中的值；这些资源会随着新功能加入而演进。

## Workflow 文件位置

workflow 文件位于 `.eas/workflows/*.yml`（或 `.yaml`）。

## 顶层结构

workflow 文件具有以下顶层键：

- `name` —— workflow 的显示名
- `on` —— 触发 workflow 启动的触发器（至少一个必需）
- `jobs` —— job 定义（必需）
- `defaults` —— 所有 job 的共享默认值
- `concurrency` —— 控制并行 workflow 运行

各部分的完整规范请参考 schema。

## 表达式

使用 `${{ }}` 语法表示动态值。schema 定义了可用的上下文：

- `github.*` —— GitHub 仓库与事件信息
- `inputs.*` —— `workflow_dispatch` 输入的值
- `needs.*` —— 依赖 job 的输出与状态
- `jobs.*` —— job 输出（替代语法）
- `steps.*` —— 自定义 job 内的步骤输出
- `workflow.*` —— workflow 元数据

## 生成 Workflow

在生成或编辑 workflow 时：

1. 抓取 schema 获取当前的 job 类型、参数与允许值
2. 验证每个 job 类型的必需字段都存在
3. 验证 `needs` 与 `after` 中引用的 job 在 workflow 中存在
4. 检查表达式引用了有效的上下文和输出
5. 确保 `if` 条件符合 schema 的长度约束

## 验证

生成或编辑 workflow 文件后，针对 schema 进行验证：

```sh
# 缺少依赖时先安装
[ -d "{baseDir}/scripts/node_modules" ] || npm install --prefix {baseDir}/scripts

node {baseDir}/scripts/validate.js <workflow.yml> [workflow2.yml ...]
```

验证器抓取最新 schema 并检查 YAML 结构。在确认 workflow 完成前，修复所有报告的错误。

## 回答问题

当用户询问可用选项（job 类型、触发器、runner 类型等）时，抓取 schema 并从中推导答案，而非依赖可能过时的信息。

## 限制

- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并要求澄清。
