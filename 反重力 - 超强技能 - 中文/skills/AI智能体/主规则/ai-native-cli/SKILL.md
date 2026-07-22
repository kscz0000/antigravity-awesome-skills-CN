---
name: ai-native-cli
description: "构建 AI 智能体可安全使用的 CLI 工具的设计规范，包含 98 条规则。涵盖结构化 JSON 输出、错误处理、输入契约、安全防护、退出码和智能体自描述。触发词：AI原生CLI、智能体CLI、CLI设计规范、命令行工具设计、agent-friendly CLI、AI agent CLI、CLI工具规范、命令行接口设计、智能体友好CLI"
risk: safe
source: https://github.com/ChaosRealmsAI/agent-cli-spec
date_added: "2026-03-15"
---

# Agent-Friendly CLI 规范 v0.1

构建或修改 CLI 工具时，请遵循以下规则，使其对 AI 智能体安全可靠。

## 概述

构建 AI 原生 CLI 工具的综合设计规范。定义了三个认证等级（Agent-Friendly、Agent-Ready、Agent-Native）共 98 条规则，按优先级（P0/P1/P2）划分。规范涵盖结构化 JSON 输出、错误处理、输入契约、安全防护、退出码、自描述，以及通过内置 issue 系统实现的反馈闭环。

## 何时使用此技能

- 构建 AI 智能体将调用的新 CLI 工具时
- 改造现有 CLI 使其对智能体友好时
- 为自动化流水线设计命令行接口时
- 审计 CLI 工具是否符合智能体安全标准时

## 核心哲学

1. **智能体优先** —— 默认输出为 JSON；人类友好格式通过 `--human` 开启
2. **智能体不可信** —— 像对待公共 API 一样验证所有输入
3. **故障封闭** —— 当验证逻辑本身出错时，默认拒绝
4. **可验证** —— 每条规则都可自动检测

## 分层模型

本规范使用两个正交轴：

- **层级** 回答推广范围：`core`、`recommended`、`ecosystem`
- **优先级** 回答严重程度：`P0`、`P1`、`P2`

使用层级进行迁移和认证：

- **core** —— 执行契约：JSON、错误、退出码、stdout/stderr、安全
- **recommended** —— 更好的机器体验：自描述、显式模式、更丰富的 schema
- **ecosystem** —— 智能体原生集成：`agent/`、`skills`、`issue`、内联上下文

认证映射到层级：

- **Agent-Friendly** —— 所有 `core` 规则通过
- **Agent-Ready** —— 所有 `core` + `recommended` 规则通过
- **Agent-Native** —— 所有层级规则通过

## 工作原理

### 步骤 1：输出模式

默认为智能体模式（JSON）。显式标志切换：

```bash
$ mycli list              # 默认 = JSON 输出（智能体模式）
$ mycli list --human      # 人类友好：彩色、表格、格式化
$ mycli list --agent      # 显式智能体模式（覆盖配置）
```

- **默认（无标志）** —— JSON 输出到 stdout。智能体无需添加标志。
- **--human** —— 人类友好格式（颜色、表格、进度条）
- **--agent** —— 显式 JSON 模式（当环境/配置覆盖默认值时有用）

### 步骤 2：agent/ 目录约定

每个 CLI 工具必须在项目根目录有 `agent/` 目录。这是工具对 AI 智能体的身份和行为契约。

```
agent/
  brief.md          # 一段话：我是谁，我能做什么
  rules/            # 行为约束（自动注册）
    trigger.md      # 智能体何时应使用此工具
    workflow.md     # 分步使用流程
    writeback.md    # 如何写回反馈
  skills/           # 扩展能力（自动注册）
    getting-started.md
```

### 步骤 3：四级自描述

1. **--brief**（名片，注入智能体配置）
2. **每个命令响应**（始终开启的上下文：data + rules + skills + issue）
3. **--help**（完整自描述：brief + commands + rules + skills + issue）
4. **skills \<name\>**（按需深入特定技能）

## 认证要求

每个等级包含前一等级的所有规则。
优先级标签 `[P0]`=智能体没有它会崩溃，`[P1]`=智能体能工作但体验差，`[P2]`=锦上添花。

### 等级 1：Agent-Friendly（core —— 20 条规则）

目标：CLI 是稳定、可调用的 API。智能体可以调用、解析和处理错误。

**输出** —— 默认为 JSON，schema 稳定
- `[P0]` O1：默认输出为 JSON。无需 `--json` 标志
- `[P0]` O2：JSON 必须通过 `jq .` 验证
- `[P0]` O3：同一版本内 JSON schema 不得变更

**错误** —— 结构化，输出到 stderr，永不交互
- `[P0]` E1：错误 -> `{"error":true, "code":"...", "message":"...", "suggestion":"..."}` 到 stderr
- `[P0]` E4：错误有机器可读的 `code`（如 `MISSING_REQUIRED`）
- `[P0]` E5：错误有人类可读的 `message`
- `[P0]` E7：出错时，永不进入交互模式 —— 立即退出
- `[P0]` E8：错误码是 API 契约 —— 跨版本不得重命名

**退出码** —— 可预测的失败信号
- `[P0]` X3：参数/用法错误必须退出码 2
- `[P0]` X9：失败必须非零退出 —— 永不退出 0 然后在 stdout 报告错误

**可组合性** —— 干净的管道语义
- `[P0]` C1：stdout 仅用于数据
- `[P0]` C2：日志、进度、警告仅输出到 stderr

**输入** —— 对错误输入快速失败
- `[P1]` I4：缺少必需参数 -> 结构化错误，永不交互提示
- `[P1]` I5：类型不匹配 -> 退出码 2 + 结构化错误

**安全** —— 防止智能体失误
- `[P1]` S1：破坏性操作需要 `--yes` 确认
- `[P1]` S4：拒绝 `../../` 路径遍历、控制字符

**防护栏** —— 运行时输入保护
- `[P1]` G1：未知标志以退出码 2 拒绝
- `[P1]` G2：检测参数中的 API key / token 模式，拒绝执行
- `[P1]` G3：拒绝敏感文件路径（*.env、*.key、*.pem）
- `[P1]` G8：拒绝参数中的 shell 元字符（; | && $()）

### 等级 2：Agent-Ready（+ recommended —— 59 条规则）

目标：CLI 自描述、命名良好、管道友好。智能体无需试错即可发现能力并链式调用命令。

**自描述** —— 智能体发现 CLI 能做什么
- `[P1]` D1：`--help` 输出结构化 JSON，包含 `commands[]`
- `[P1]` D3：schema 有必需字段（help、commands）
- `[P1]` D4：所有参数有类型声明
- `[P1]` D7：参数标注为必需/可选
- `[P1]` D9：每个命令有描述
- `[P1]` D11：`--help` 输出包含 help、rules、skills、commands 的 JSON
- `[P1]` D15：`--brief` 输出 `agent/brief.md` 内容
- `[P1]` D16：默认 JSON（智能体模式），`--human` 为人类友好
- `[P2]` D2/D5/D6/D8/D10：每命令帮助、枚举、默认值、输出 schema、版本

**输入** —— 无歧义的调用约定
- `[P1]` I1：所有标志使用 `--long-name` 格式
- `[P1]` I2：无位置参数歧义
- `[P2]` I3/I6/I7：--json-input、布尔 --no-X、数组参数

**错误**
- `[P1]` E6：错误包含 `suggestion` 字段
- `[P2]` E2/E3：错误到 stderr、错误 JSON 有效

**安全**
- `[P1]` S8：`--sanitize` 标志用于外部输入
- `[P2]` S2/S3/S5/S6/S7：默认拒绝、--dry-run、无自动更新、破坏性标记

**退出码**
- `[P1]` X1：0 = 成功
- `[P2]` X2/X4-X8：1=通用、10=认证、11=权限、20=未找到、30=冲突

**可组合性**
- `[P1]` C6：管道模式无交互提示
- `[P2]` C3/C4/C5/C7：管道友好、--quiet、管道链、幂等性

**命名** —— 可预测的标志约定
- `[P1]` N4：保留标志（--agent、--human、--brief、--help、--version、--yes、--dry-run、--quiet、--fields）
- `[P2]` N1/N2/N3/N5/N6：一致命名、kebab-case、最多 3 层、--version semver

**防护栏**
- `[P1]` I8/I9：无隐式状态、非交互认证
- `[P1]` G6/G9：前置条件检查、故障封闭
- `[P2]` G4/G5/G7：权限级别、PII 脱敏、批量限制

#### 保留标志

| 标志 | 语义 | 说明 |
|------|------|------|
| `--agent` | JSON 输出（默认） | 显式覆盖 |
| `--human` | 人类友好输出 | 颜色、表格、格式化 |
| `--brief` | 一段话身份 | 用于同步到智能体配置 |
| `--help` | 完整自描述 JSON | brief + commands + rules + skills + issue |
| `--version` | Semver 版本字符串 | |
| `--yes` | 确认破坏性操作 | 删除/销毁操作必需 |
| `--dry-run` | 预览而不执行 | |
| `--quiet` | 抑制 stderr 输出 | |
| `--fields` | 过滤输出字段 | 节省 token |

### 等级 3：Agent-Native（+ ecosystem —— 19 条规则）

目标：CLI 有身份、行为契约、技能系统和反馈闭环。智能体可以学习工具、扩展使用并报告问题 —— 完整的闭环协作。

**Agent 目录** —— 工具身份和行为契约
- `[P1]` D12：`agent/brief.md` 存在
- `[P1]` D13：`agent/rules/` 有 trigger.md、workflow.md、writeback.md
- `[P1]` D17：agent/rules/*.md 有 YAML frontmatter（name、description）
- `[P1]` D18：agent/skills/*.md 有 YAML frontmatter（name、description）
- `[P2]` D14：`agent/skills/` 目录 + `skills` 子命令

**响应结构** —— 每次调用内联上下文
- `[P1]` R1：每个响应包含 `rules[]`（agent/rules/ 的完整内容）
- `[P1]` R2：每个响应包含 `skills[]`（name + description + command）
- `[P1]` R3：每个响应包含 `issue`（反馈指南）

**元数据** —— 项目级集成
- `[P2]` M1：项目根目录有 AGENTS.md
- `[P2]` M2：可选 MCP tool schema 导出
- `[P2]` M3：CHANGELOG.md 标记破坏性变更

**反馈** —— 内置 issue 系统
- `[P2]` F1：`issue` 子命令（create/list/show）
- `[P2]` F2：结构化提交，包含 version/context/exit_code
- `[P2]` F3：分类：bug / requirement / suggestion / bad-output
- `[P2]` F4：issue 本地存储，无外部服务依赖
- `[P2]` F5：`issue list` / `issue show <id>` 可查询
- `[P2]` F6：issue 有状态跟踪（open/in-progress/resolved/closed）
- `[P2]` F7：issue JSON 有所有必需字段（id、type、status、message、created_at、updated_at）
- `[P2]` F8：所有 issue 有 status 字段

## 示例

### 示例 1：JSON 输出（智能体模式）

```bash
$ mycli list
{"result": [{"id": 1, "title": "Buy milk", "status": "todo"}], "rules": [...], "skills": [...], "issue": "..."}
```

### 示例 2：结构化错误

```json
{
  "error": true,
  "code": "AUTH_EXPIRED",
  "message": "Access token expired 2 hours ago",
  "suggestion": "Run 'mycli auth refresh' to get a new token"
}
```

### 示例 3：退出码表

```
0   成功            10  认证失败          20  资源未找到
1   通用错误        11  权限拒绝          30  冲突/前置条件
2   参数/用法错误
```

## 快速实现清单

按层级实现 —— 每个阶段获得下一认证等级。

**阶段 1：Agent-Friendly（core）**
1. 默认输出为 JSON —— 无需 `--json` 标志
2. 错误处理器：`{ error, code, message, suggestion }` 到 stderr
3. 退出码：0 成功、2 参数错误、1 通用错误
4. stdout = 仅数据，stderr = 仅日志
5. 缺少参数 -> 结构化错误（永不交互）
6. 破坏性操作需 `--yes` 保护
7. 防护栏：拒绝密钥、路径遍历、shell 元字符

**阶段 2：Agent-Ready（+ recommended）**
8. `--help` 返回结构化 JSON（help、commands[]、rules[]、skills[]）
9. `--brief` 读取并输出 `agent/brief.md` 内容
10. `--human` 标志切换到人类友好格式
11. 保留标志：--agent、--version、--dry-run、--quiet、--fields
12. 退出码：20 未找到、30 冲突、10 认证、11 权限

**阶段 3：Agent-Native（+ ecosystem）**
13. 创建 `agent/` 目录：`brief.md`、`rules/trigger.md`、`rules/workflow.md`、`rules/writeback.md`
14. 每个命令响应追加：rules[] + skills[] + issue
15. `skills` 子命令：列出所有 / 显示一个完整内容
16. `issue` 子命令用于反馈（create/list/show/close/transition）
17. 项目根目录有 AGENTS.md

## 最佳实践

- 应该：默认 JSON 输出，智能体无需添加标志
- 应该：在每个错误响应中包含 `suggestion` 字段
- 应该：使用三级认证模型实现渐进式采用
- 应该：`agent/brief.md` 保持一段话以节省 token
- 不应该：出错时进入交互模式 —— 始终立即退出
- 不应该：同一版本内更改 JSON schema 或错误码
- 不应该：在 stdout 放日志或进度信息 —— 仅用 stderr
- 不应该：静默接受未知标志 —— 以退出码 2 拒绝

## 常见陷阱

- **问题：** CLI 默认输出人类可读文本，破坏智能体解析
  **解决方案：** 让 JSON 成为默认输出格式；添加 `--human` 标志切换人类友好模式

- **问题：** 错误在 stdout 报告，退出码为 0
  **解决方案：** 失败时始终非零退出，并将结构化错误 JSON 写入 stderr

- **问题：** CLI 交互式提示缺少的输入
  **解决方案：** 返回带 suggestion 字段的结构化错误并立即退出

## 相关技能

- `@cli-best-practices` - 通用 CLI 设计模式（本技能专注于 AI 智能体兼容性）

## 更多资源

- [Agent CLI Spec 仓库](https://github.com/ChaosRealmsAI/agent-cli-spec)

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需输入、权限、安全边界或成功标准，请停下来请求澄清。
