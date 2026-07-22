---
name: infinity
description: "强制执行严格的输入边界协议（检测、分类、过滤、验证），确保不受信任的数据永远不会以原始形式到达业务逻辑。触发词：输入验证、边界过滤、数据校验、input validation、boundary filter、sanitize、untrusted data"
risk: safe
source: community
date_added: "2026-06-23"
---

# infinity — 输入边界与验证协议

## 核心理念

> 不受信任的数据永远不会到达核心——它在接触之前就被拦截。没有任何外部数据会以原始形态接触代码库。数据进入系统的每一个边界都必须有过滤器。

静默 Bug、崩溃和漏洞的头号来源是外部数据以意外形态到达并被直接使用而未经检查。本技能在每一个入口点强制执行过滤层，每次都不例外。

---

## 何时使用此技能

- 需要处理 API 响应时使用
- 读取用户输入或添加表单处理器时使用
- 处理环境变量或 CLI 参数时使用
- 解析 Webhook 或从文件系统读取时使用
- 任何代码调用 `.body`、`.params`、`.query`、`.env`、`fs.read` 或第三方 SDK 响应时使用

---

## 四个阶段

### 阶段 1 — 边界检测

在编写或修改任何涉及外部数据的代码之前，AI 必须识别并列出范围内的每一个入口点：

- HTTP 请求体、请求头、查询参数
- 用户表单输入和 UI 提交的数据
- 环境变量和配置文件
- 第三方 API 响应
- Webhook 载荷
- 磁盘文件读取
- CLI 参数
- 来自外部数据源的数据库查询结果
- WebSocket 消息

> **AI 在列出范围内每一个入口点之前，不得编写任何数据处理逻辑。**

---

### 阶段 2 — 分类每个输入

对于识别到的每一个入口点，AI 将其归入三个信任等级之一：

| 等级 | 定义 | 示例 |
|---|---|---|
| `TRUSTED` | 内部常量、硬编码值、自己的编译期配置 | 枚举值、硬编码默认值、内部常量 |
| `SEMI-TRUSTED` | 自己的内部服务、内部 API、受控基础设施 | 内部微服务响应、自己的数据库读取 |
| `UNTRUSTED` | 来自用户、互联网、第三方或文件系统的任何内容 | 用户输入、外部 API 响应、上传文件、环境变量、CLI 参数 |

> **规则：** `TRUSTED` 输入可以直接使用。`SEMI-TRUSTED` 和 `UNTRUSTED` 输入在使用前必须通过过滤层。

AI 在编写任何处理代码之前输出此分类：

```
INFINITY — BOUNDARY MAP
─────────────────────────────────────────
Entry Point              | Trust Level  | Filter Required
─────────────────────────────────────────
req.body.email           | UNTRUSTED    | ✓ format + sanitize
process.env.API_KEY      | UNTRUSTED    | ✓ presence + non-empty
internalService.getData()| SEMI-TRUSTED | ✓ schema validate
PAGINATION_LIMIT = 20    | TRUSTED      | ✗ none needed
─────────────────────────────────────────
```

---

### 阶段 3 — 强制过滤层

每一个 `UNTRUSTED` 和 `SEMI-TRUSTED` 输入在到达任何业务逻辑、存储或渲染之前，必须通过验证。AI 必须根据上下文应用正确的过滤类型：

**类型检查**
- 使用前验证输入是否为预期类型
- 永远不要假设字符串就是字符串、数字就是数字、数组就是数组

**Schema 验证**
- 对于对象和 API 响应，在访问嵌套字段之前验证其结构
- 如果缺少必填字段，拒绝——不要使用会掩盖问题的回退值

**净化处理**
- 渲染到 UI 之前去除或转义内容（防止 XSS）
- 存储前规范化字符串（修剪空白、在适当情况下统一大小写）

**存在性与格式检查**
- 环境变量：使用前必须存在且非空
- ID 和令牌：使用前必须匹配预期格式

**拒绝规则**
- 输入无效时：明确拒绝并返回清晰的错误
- 永远不要用回退值静默使用错误数据
- 永远不要让错误数据通过以期在"下游"自行修复

```
// WRONG — using raw input directly
const user = await db.find(req.params.id);

// RIGHT — validate before use
const id = req.params.id;
if (!id || typeof id !== 'string' || !isValidUUID(id)) {
  return res.status(400).json({ error: 'Invalid ID format' });
}
const user = await db.find(id);
```

---

### 阶段 4 — 完成前自检

AI 在声明任何数据处理代码完成之前，必须追踪每个入口点并确认：

```
INFINITY — VERIFICATION
─────────────────────────────────────────
Entry Point              | Filter Exists | Filter Type
─────────────────────────────────────────
req.body.email           | ✓ YES         | format + sanitize
process.env.API_KEY      | ✓ YES         | presence check
internalService.getData()| ✓ YES         | schema validation
─────────────────────────────────────────
Unfiltered inputs reaching logic: NONE ✓
─────────────────────────────────────────
```

如果有任何 `UNTRUSTED` 或 `SEMI-TRUSTED` 输入在未经过滤的情况下到达了逻辑、存储或渲染——AI 必须标记它。不得静默放行。

---

## 硬性规则（不可违反）

- **业务逻辑中不得出现原始外部数据。** 绝不可以。
- **输入错误时不得静默回退。** 必须明确拒绝。
- **不得假设数据结构。** 即使 API"总是"返回字符串——也要验证。
- **不得跳过环境变量检查。** 缺失的环境变量必须在启动时大声失败，而不是在运行时静默出错。
- **不得部分过滤。** 如果验证了存在性但没有验证格式，那不叫过滤。
- **不得在错误的位置过滤。** 过滤器放在入口点——而不是在数据已经被使用过一次之后的某个下游位置。

---

## 此技能防止的问题

- 通过未验证查询参数进行的 SQL 注入
- 意外 API 响应结构导致的崩溃
- 未转义用户内容渲染到 UI 引起的 XSS
- 缺失环境变量在运行时才被发现的静默失败
- 假设外部数据匹配预期结构导致的类型错误
- 不受信任数据到达敏感操作引发的安全漏洞

---

## 快速参考

| 阶段 | 操作 | 编写代码？ |
|---|---|---|
| 1 — 检测 | 列出范围内所有入口点 | ❌ 否 |
| 2 — 分类 | 为每个输入分配信任等级 | ❌ 否 |
| 3 — 过滤 | 为所有 UNTRUSTED + SEMI-TRUSTED 编写过滤层 | ✅ 是 |
| 4 — 验证 | 追踪每个输入，确认过滤器存在 | ❌ 否 |

---

## 局限性

- 不适用于不涉及外部数据的纯内部逻辑。
- 在不需要严格验证的简单脚本中可能增加冗余代码。
