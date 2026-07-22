---
name: faf-wizard
description: "一站式 .faf 生成器。为任意项目一键生成 AI 上下文——新建、遗留或知名项目均可。自动检测技术栈、评分就绪度、全平台兼容。触发词：faf、AI上下文生成、项目配置、一键生成、技术栈检测、AI就绪评分、项目上下文、faf-wizard、project.faf"
category: productivity
risk: safe
source: community
source_repo: Wolfe-Jam/faf-skills
source_type: community
date_added: "2026-04-07"
author: wolfejam
tags: [faf, automation, project-setup, ai-context, productivity]
tools: [claude, cursor, gemini, windsurf, any-ai]
---

# FAF Wizard - 一键 AI 智能

**你的项目维修团队。** 指向任意代码库，60 秒内获得评分完毕、AI 就绪的上下文。

将任意项目——新建、遗留、知名开源项目或被遗忘的副业项目——转化为 AI 智能工作空间，拥有跨所有 AI 工具的持久上下文。

## 解决的问题

**即使是 React.js 的 AI 就绪度也只有 0%。** 知名仓库没有 AI 上下文。

| 现有内容 | 它告诉 AI 什么 |
|----------|----------------|
| README.md | "这是做什么的"（给人类看的） |
| docs/ | "如何使用"（给人类看的） |
| **project.faf** | "如何帮助构建这个"（给 AI 看的） |

文档告诉人类如何使用你的代码。AI 上下文告诉 AI 如何帮助你构建它。**这是完全不同的两件事。**

## 适用于任何项目

| 项目类型 | FAF Wizard 做什么 |
|----------|-------------------|
| **全新项目** | 从第一行代码开始就有完美的 AI 上下文 |
| **遗留噩梦** | AI 终于能理解代码考古学了 |
| **知名开源项目** | 即使 React 也没有这个 |
| **副业项目** | 不用每次会话都重新解释 |
| **客户交接** | 适用于任何 AI 工具的便携上下文 |
| **团队项目** | 所有人都能使用的共享上下文 |

## 真实成功案例

### 前后对比：遗留电商平台
```
之前："这个 2015 年的 5 万行 PHP 代码库..."
AI："我不理解这个架构"

之后：用 FAF Wizard 处理 60 秒
AI："我看到这是一个基于 Laravel 的电商系统，具有支付处理、
库存管理和多租户架构。我可以这样帮助你..."
```

### 前后对比：现代 React 应用
```
之前：每次 AI 会话都要从解释上下文开始
浪费时间：每会话 5-10 分钟

之后：project.faf 已存在
AI：即时理解，第一条消息就开始产出
节省时间：每天 2+ 小时
```

## 60 秒工作流

### 第一步：检测（10 秒）
```bash
faf auto
# 扫描清单文件、目录结构、依赖项
# 检测到：React + TypeScript + Tailwind + Vercel
```

### 第二步：生成（30 秒）
```yaml
# 自动生成的 project.faf
project:
  name: my-saas-dashboard  
  goal: Customer analytics platform

stack:
  frontend: react-18
  css: tailwind
  deployment: vercel
  
human_context:
  who: Solo founder
  what: SaaS analytics dashboard
  why: Customer insights for small businesses
```

### 第三步：评分与报告（20 秒）
```
✅ 已生成：project.faf
🏆 AI 就绪度：87% 铜级 - 生产就绪

已填充：9/11 个活跃槽位
已忽略：22 个槽位（不适用）

达到银级（95%）需要：
  + 添加 API 文档（+5%）
  + 定义部署详情（+3%）
```

## 性能数据（真实数字）

**已分析 8,400+ 个项目：**
- ✅ **99.2% 检测准确率**，覆盖 153+ 种格式
- ✅ **平均生成时间**：12.3 秒
- ✅ **铜级或更高**：94% 的项目
- ✅ **零手动配置**：开箱即用

### 格式支持
自动检测并配置：
- **JavaScript**：React、Vue、Angular、Svelte、Next.js、Nuxt
- **Python**：Django、Flask、FastAPI、Jupyter、Poetry
- **TypeScript**：所有 JS 框架 + 原生 TS 项目
- **Rust**：Cargo 项目、CLI 工具、Web 服务器
- **Go**：模块、Docker、微服务
- **Java**：Maven、Gradle、Spring Boot
- **+147 种更多格式**

## 通用兼容性

### 适用于所有 AI 工具
- ✅ **Claude Code** - 原生读取 .faf
- ✅ **Cursor** - 自动同步到 .cursorrules
- ✅ **Gemini CLI** - 转换为 GEMINI.md
- ✅ **Windsurf** - 同步到 .windsurfrules
- ✅ **ChatGPT** - 可读的 YAML 格式
- ✅ **任意 AI** - 通用格式支持

### 迁移支持
已有 AI 上下文文件？
```bash
# 迁移现有上下文
faf migrate --from .cursorrules
faf migrate --from CLAUDE.md  
faf migrate --from README.md

# 一种格式，到处可用
faf sync --target all
```

## 安装选项

### 选项 1：CLI（推荐）
```bash
npm install -g faf-cli
cd your-project
faf auto
```

### 选项 2：MCP 服务器（Claude Code）
```json
{
  "mcpServers": {
    "faf": {
      "command": "npx", 
      "args": ["-y", "claude-faf-mcp@latest"]
    }
  }
}
```

### 选项 3：浏览器扩展
从 Chrome Web Store 安装 - 适用于任意 Git 仓库。

## 三阶段智能

### 第一阶段：技术栈检测
- 扫描 `package.json`、`Cargo.toml`、`pyproject.toml` 等
- 分析目录结构和文件模式
- 识别框架、部署目标、测试配置

### 第二阶段：上下文挖掘
- 从 README 提取项目描述
- 从代码结构识别架构模式
- 提取依赖信息用于 AI 上下文

### 第三阶段：优化
- 生成聚焦的 33 槽 IANA 格式
- 根据格式规范验证
- 评分 AI 就绪度并给出改进建议

## 各项目类型的成功指标

| 项目类型 | 平均分数 | 达到铜级时间 | 检测率 |
|----------|----------|--------------|--------|
| **React/Vue** | 89% | 即时 | 99.8% |
| **Python Django** | 91% | 即时 | 99.5% |
| **Rust CLI** | 85% | 即时 | 99.1% |
| **遗留 PHP** | 76% | 30 秒 | 94.2% |
| **Monorepo** | 82% | 45 秒 | 91.8% |

## 何时改用 faf-expert

使用 `faf-wizard` 的场景：
- ✅ 快速项目入门
- ✅ 全自动处理
- ✅ "让它能跑就行"
- ✅ 时间紧迫的场景

使用 `faf-expert` 的场景：
- 🎯 精细调优的冠军级评分（95%+）
- 🎯 复杂的 MCP 服务器配置
- 🎯 多平台同步管理
- 🎯 企业级部署模式

## 验证与安全

**企业级标准：**
- ✅ **800+ 全面测试** 覆盖 CLI 和 MCP
- ✅ **永不存储凭证** 在 .faf 文件中
- ✅ **YAML 格式验证** 防止格式错误文件
- ✅ **IANA 注册格式**（application/vnd.faf+yaml）
- ✅ **MIT 许可证** - 商用安全

## 快速开始

### 为你当前的项目
```bash
# 一条命令，永久搞定
npx faf-cli auto

# 查看结果
cat project.faf
```

### 为任意 GitHub 仓库
安装浏览器扩展，在任意仓库点击 "Generate FAF"。

### 为团队
```bash
# 设置团队级 MCP 服务器
faf mcp install --team
faf sync --target all --watch
```

## 社区与支持

- **网站**：https://faf.one
- **Chrome 扩展**：4.8★ 评分，Google 认证
- **下载量**：生态系统内 52k+
- **Discord**：1000+ 开发者的活跃社区
- **文档**：全面的指南和示例

---

*别再每次会话都解释你的项目。FAF Wizard - 因为 AI 应该像你一样理解你的项目。*

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
