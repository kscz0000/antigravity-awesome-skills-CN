---
name: mcp-builder-ms
description: "构建 MCP 服务器以集成外部 API 或服务时使用，支持 Python（FastMCP）和 Node/TypeScript（MCP SDK）。当用户要求'构建MCP服务器'、'集成外部API'、'创建MCP工具'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# MCP 服务器开发指南

## 适用场景
构建 MCP 服务器以集成外部 API 或服务时使用，支持 Python（FastMCP）和 Node/TypeScript（MCP SDK）。

## 概述

创建 MCP（Model Context Protocol）服务器，使 LLM 能通过精心设计的工具与外部服务交互。MCP 服务器的质量取决于它帮助 LLM 完成实际任务的能力。

---

## Microsoft MCP 生态

Microsoft 为 Azure 和 Foundry 服务提供了丰富的 MCP 基础设施。了解这个生态有助于决定是构建自定义服务器还是利用现有服务器。

### 服务器类型

| 类型 | 传输方式 | 适用场景 | 示例 |
|------|----------|----------|------|
| **本地** | stdio | 桌面应用、单用户、本地开发 | Azure MCP Server（NPM/Docker） |
| **远程** | Streamable HTTP | 云服务、多租户、Agent Service | `https://mcp.ai.azure.com`（Foundry） |

### Microsoft MCP 服务器

构建自定义服务器前，先确认 Microsoft 是否已提供：

| 服务器 | 类型 | 说明 |
|--------|------|------|
| **Azure MCP** | 本地 | 48+ Azure 服务（Storage、KeyVault、Cosmos、SQL 等） |
| **Foundry MCP** | 远程 | `https://mcp.ai.azure.com` — 模型、部署、评估、代理 |
| **Fabric MCP** | 本地 | Microsoft Fabric API、OneLake、项定义 |
| **Playwright MCP** | 本地 | 浏览器自动化与测试 |
| **GitHub MCP** | 远程 | `https://api.githubcopilot.com/mcp` |

**完整生态：** 参见 🔷 Microsoft MCP Patterns，获取完整的服务器目录和模式。

### 何时用 Microsoft 方案 vs 自定义

| 场景 | 建议 |
|------|------|
| Azure 服务集成 | 使用 **Azure MCP Server**（覆盖 48 个服务） |
| AI Foundry 代理/评估 | 使用 **Foundry MCP** 远程服务器 |
| 自定义内部 API | 构建**自定义服务器**（本指南） |
| 第三方 SaaS 集成 | 构建**自定义服务器**（本指南） |
| 扩展 Azure MCP | 遵循 Microsoft MCP Patterns |

---

# 流程

## 🚀 整体工作流

创建高质量 MCP 服务器包含四个阶段：

### 阶段 1：深入调研与规划

#### 1.1 理解现代 MCP 设计

**API 覆盖 vs 工作流工具：**
平衡全面的 API 端点覆盖与专用工作流工具。工作流工具对特定任务更便捷，而全面覆盖让代理能灵活组合操作。性能因客户端而异——有些客户端受益于组合基础工具的代码执行，有些则更适合高层工作流。不确定时，优先保证 API 覆盖的全面性。

**工具命名与可发现性：**
清晰、描述性的工具名称帮助代理快速找到合适的工具。使用一致的前缀（如 `github_create_issue`、`github_list_repos`）和面向动作的命名。

**上下文管理：**
代理受益于简洁的工具描述和过滤/分页结果的能力。设计返回聚焦、相关数据的工具。部分客户端支持代码执行，可帮助代理高效过滤和处理数据。

**可操作的错误消息：**
错误消息应通过具体建议和后续步骤引导代理找到解决方案。

#### 1.2 学习 MCP 协议文档

**浏览 MCP 规范：**

从站点地图开始查找相关页面：`https://modelcontextprotocol.io/sitemap.xml`

然后用 `.md` 后缀获取 Markdown 格式的具体页面（如 `https://modelcontextprotocol.io/specification/draft.md`）。

重点页面：
- 规范概览与架构
- 传输机制（Streamable HTTP、stdio）
- 工具、资源和提示词定义

#### 1.3 学习框架文档

**语言选择：**

| 语言 | 最适合 | SDK |
|------|--------|-----|
| **TypeScript**（推荐） | 通用 MCP 服务器，兼容性广 | `@modelcontextprotocol/sdk` |
| **Python** | 数据/ML 管道，FastAPI 集成 | `mcp`（FastMCP） |
| **C#/.NET** | Azure/Microsoft 生态，企业级 | `Microsoft.Mcp.Core` |

**传输方式选择：**

| 传输方式 | 适用场景 | 特点 |
|----------|----------|------|
| **Streamable HTTP** | 远程服务器、多租户、Agent Service | 无状态、可扩展、需认证 |
| **stdio** | 本地服务器、桌面应用 | 简单、单用户、无网络 |

**加载框架文档：**

- **MCP 最佳实践**：📋 查看最佳实践 — 核心指南

**TypeScript（推荐）：**
- **TypeScript SDK**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- ⚡ TypeScript 指南 — TypeScript 模式与示例

**Python：**
- **Python SDK**：使用 WebFetch 加载 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- 🐍 Python 指南 — Python 模式与示例

**C#/.NET（Microsoft 生态）：**
- 🔷 Microsoft MCP Patterns — C# 模式、Azure MCP 架构、命令层级

#### 1.4 规划实现

**理解 API：**
审阅服务的 API 文档，识别关键端点、认证要求和数据模型。按需使用网络搜索和 WebFetch。

**工具选择：**
优先保证 API 覆盖的全面性。列出要实现的端点，从最常用的操作开始。

---

### 阶段 2：实现

#### 2.1 搭建项目结构

参见语言特定指南了解项目搭建：
- ⚡ TypeScript 指南 — 项目结构、package.json、tsconfig.json
- 🐍 Python 指南 — 模块组织、依赖管理
- 🔷 Microsoft MCP Patterns — C# 项目结构、命令层级

#### 2.2 实现核心基础设施

创建共享工具：
- 带认证的 API 客户端
- 错误处理辅助函数
- 响应格式化（JSON/Markdown）
- 分页支持

#### 2.3 实现工具

每个工具：

**输入 Schema：**
- 使用 Zod（TypeScript）或 Pydantic（Python）
- 包含约束和清晰描述
- 在字段描述中添加示例

**输出 Schema：**
- 尽可能定义 `outputSchema` 用于结构化数据
- 在工具响应中使用 `structuredContent`（TypeScript SDK 特性）
- 帮助客户端理解和处理工具输出

**工具描述：**
- 功能的简洁摘要
- 参数描述
- 返回类型 schema

**实现：**
- I/O 操作使用 async/await
- 带可操作消息的适当错误处理
- 适用时支持分页
- 使用现代 SDK 时同时返回文本内容和结构化数据

**注解：**
- `readOnlyHint`：true/false
- `destructiveHint`：true/false
- `idempotentHint`：true/false
- `openWorldHint`：true/false

---

### 阶段 3：审查与测试

#### 3.1 代码质量

审查要点：
- 无重复代码（DRY 原则）
- 一致的错误处理
- 完整的类型覆盖
- 清晰的工具描述

#### 3.2 构建与测试

**TypeScript：**
- 运行 `npm run build` 验证编译
- 使用 MCP Inspector 测试：`npx @modelcontextprotocol/inspector`

**Python：**
- 验证语法：`python -m py_compile your_server.py`
- 使用 MCP Inspector 测试

参见语言特定指南了解详细的测试方法和质量检查清单。

---

### 阶段 4：创建评估

实现 MCP 服务器后，创建全面的评估来测试其效果。

**加载 ✅ 评估指南获取完整评估规范。**

#### 4.1 理解评估目的

评估用于测试 LLM 能否有效使用你的 MCP 服务器回答真实、复杂的问题。

#### 4.2 创建 10 个评估问题

创建有效评估，遵循评估指南中的流程：

1. **工具检查**：列出可用工具，理解其能力
2. **内容探索**：使用只读操作探索可用数据
3. **问题生成**：创建 10 个复杂、真实的问题
4. **答案验证**：自己解答每个问题以验证答案

#### 4.3 评估要求

确保每个问题：
- **独立**：不依赖其他问题
- **只读**：仅需非破坏性操作
- **复杂**：需要多次工具调用和深入探索
- **真实**：基于用户真正关心的实际场景
- **可验证**：单一、清晰的答案，可通过字符串比较验证
- **稳定**：答案不会随时间变化

#### 4.4 输出格式

创建以下结构的 XML 文件：

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

---

# 参考文件

## 📚 文档库

开发过程中按需加载这些资源：

### 核心 MCP 文档（优先加载）
- **MCP 协议**：从站点地图 `https://modelcontextprotocol.io/sitemap.xml` 开始，然后用 `.md` 后缀获取具体页面
- 📋 MCP 最佳实践 — 通用 MCP 指南，包括：
  - 服务器和工具命名约定
  - 响应格式指南（JSON vs Markdown）
  - 分页最佳实践
  - 传输方式选择（Streamable HTTP vs stdio）
  - 安全与错误处理标准

### Microsoft MCP 文档（Azure/Foundry）
- 🔷 Microsoft MCP Patterns — Microsoft 特定模式，包括：
  - Azure MCP Server 架构（48+ Azure 服务）
  - C#/.NET 命令实现模式
  - Foundry Agent Service 远程 MCP
  - 认证（Entra ID、OBO 流、Managed Identity）
  - Bicep 模板测试基础设施

### SDK 文档（阶段 1/2 加载）
- **Python SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 获取
- **TypeScript SDK**：从 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 获取
- **Microsoft MCP SDK**：参见 Microsoft MCP Patterns 的 C#/.NET 部分

### 语言特定实现指南（阶段 2 加载）
- 🐍 Python 实现指南 — 完整的 Python/FastMCP 指南，包括：
  - 服务器初始化模式
  - Pydantic 模型示例
  - 使用 `@mcp.tool` 注册工具
  - 完整可运行示例
  - 质量检查清单

- ⚡ TypeScript 实现指南 — 完整的 TypeScript 指南，包括：
  - 项目结构
  - Zod schema 模式
  - 使用 `server.registerTool` 注册工具
  - 完整可运行示例
  - 质量检查清单

- 🔷 Microsoft MCP Patterns — 完整的 C#/.NET 指南，包括：
  - 命令层级（BaseCommand → GlobalCommand → SubscriptionCommand）
  - 命名约定（`{Resource}{Operation}Command`）
  - 选项处理（`.AsRequired()` / `.AsOptional()`）
  - Azure Functions 远程 MCP 部署
  - Bicep 实时测试模式

### 评估指南（阶段 4 加载）
- ✅ 评估指南 — 完整的评估创建指南，包括：
  - 问题创建指南
  - 答案验证策略
  - XML 格式规范
  - 示例问题和答案
  - 使用提供的脚本运行评估

## 局限性
- 仅在任务明确符合上述范围时使用本技能。
- 输出不能替代针对具体环境的验证、测试或专家审查。
- 若缺少必要的输入、权限、安全边界或成功标准，应停下来请求澄清。
