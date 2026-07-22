---
name: protect-mcp-governance
description: "MCP 工具调用的智能体治理技能——Cedar 策略编写、影子模式到强制模式的渐进部署、Ed25519 签名回执验证。触发词：MCP治理、Cedar策略、工具调用控制、影子模式、回执验证、智能体权限、审计追踪、Ed25519签名"
risk: safe
source: community
source_repo: scopeblind/scopeblind-gateway
source_type: official
date_added: "2026-04-05"
---

# 使用 protect-mcp 进行 MCP 智能体治理

## 概述

本技能指导如何使用 Cedar 策略和 Ed25519 签名回执来治理 AI 智能体的工具调用。你将学会为 MCP 服务器编写访问控制策略、在影子模式下运行观察、以及验证加密审计追踪。

## 何时使用本技能

- 需要控制智能体可以调用哪些 MCP 工具以及在什么条件下调用时
- 需要为智能体工具执行建立防篡改审计追踪时
- 需要渐进式部署治理策略（先影子模式，再强制模式）时
- 需要为 MCP 工具访问控制编写 Cedar 策略时
- 需要验证回执或审计包是否被篡改时

## 不适用场景

- 需要通用应用安全审计时（使用 `@security-auditor`）
- 需要扫描代码漏洞时（使用 `@security-audit`）
- 需要合规框架指导但不需要智能体专属治理时

## 工作原理

protect-mcp 拦截 MCP 工具调用，根据 Cedar 策略（与 AWS Verified Permissions 使用同一策略引擎）进行评估，并将每个决策签名生成 Ed25519 回执。回执是密码学证明，表明在特定时间对特定工具调用评估了特定策略。

```
Agent → protect-mcp → Cedar policy evaluation → MCP Server
                ↓
        Ed25519 signed receipt
```

三种运行模式：

1. **影子模式**（默认）——记录决策但不阻断。在强制执行前用此模式观察策略效果。
2. **强制模式**——阻断违反策略的工具调用。在影子模式验证后使用。
3. **Hooks 模式**——与 Claude Code hooks 集成，实现工具调用前后的治理。

## 核心概念

### Cedar 策略

Cedar 是专为授权设计的策略语言。策略通过 WASM 在本地评估——无需网络调用。

```cedar
// Allow read-only file operations
permit(
  principal,
  action == Action::"call_tool",
  resource
) when {
  resource.tool_name in ["read_file", "list_directory", "search_files"]
};

// Deny destructive operations
forbid(
  principal,
  action == Action::"call_tool",
  resource
) when {
  resource.tool_name in ["execute_command", "delete_file", "write_file"]
  && resource has args
  && resource.args.contains("rm -rf")
};
```

### 签名回执

每个策略决策都会生成签名回执：

```json
{
  "payload": {
    "type": "protectmcp:decision",
    "tool_name": "read_file",
    "decision": "allow",
    "policy_digest": "sha256:9d0fd4c9e72c1d5d",
    "issued_at": "2026-04-05T14:32:04.102Z",
    "issuer_id": "sb:issuer:de073ae64e43"
  },
  "signature": {
    "alg": "EdDSA",
    "kid": "sb:issuer:de073ae64e43",
    "sig": "2a3b5022..."
  }
}
```

回执格式遵循 [IETF Internet-Draft draft-farley-acta-signed-receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/)。

## 分步指南

### 1. 为项目初始化治理

```bash
# Install and initialize hooks (Claude Code integration)
npx protect-mcp init-hooks

# Or run as a standalone MCP gateway
npx protect-mcp serve
```

这会在项目根目录创建 `protect-mcp.config.json` 和一个入门 Cedar 策略。

### 2. 编写第一个策略

在项目中创建 `policy.cedar`：

```cedar
// Start permissive — allow everything in shadow mode
permit(
  principal,
  action == Action::"call_tool",
  resource
);
```

### 3. 以影子模式运行（先观察）

```bash
# Shadow mode is the default — logs decisions without blocking
npx protect-mcp --policy policy.cedar -- node your-mcp-server.js
```

先查看影子日志，了解智能体的行为模式，再编写限制性策略。

### 4. 收紧并强制执行

了解工具调用模式后，编写具体策略：

```cedar
// Allow file reads, deny writes outside src/
permit(
  principal,
  action == Action::"call_tool",
  resource
) when {
  resource.tool_name == "read_file"
};

permit(
  principal,
  action == Action::"call_tool",
  resource
) when {
  resource.tool_name == "write_file"
  && resource has args
  && resource.args.path like "src/*"
};

// Deny everything else
forbid(
  principal,
  action == Action::"call_tool",
  resource
);
```

切换到强制模式：

```bash
npx protect-mcp --policy policy.cedar --enforce -- node your-mcp-server.js
```

### 5. 验证回执

```bash
# Verify a single receipt
npx @veritasacta/verify receipt.json --key <public-key-hex>

# Verify an audit bundle (multiple receipts + keys)
npx @veritasacta/verify bundle.json --bundle

# Self-test the verifier (proves it works offline)
npx @veritasacta/verify --self-test
```

退出码：`0` = 签名有效（已证实真实），`1` = 签名无效（已证实篡改），`2` = 验证器错误（输入格式异常）。

## 示例

### 示例 1：为 Claude Code 会话添加治理

```bash
# Initialize hooks
npx protect-mcp init-hooks

# Claude Code now generates a signed receipt for every tool call.
# Receipts are stored in .protect-mcp/receipts/
```

**说明：** 初始化后，Claude Code 的每次工具调用都会生成签名回执。不会阻断任何工具调用（影子模式）。

### 示例 2：限制生产环境 MCP 服务器

```cedar
// Only allow approved tools with rate limiting
permit(
  principal,
  action == Action::"call_tool",
  resource
) when {
  resource.tool_name in [
    "get_customer",
    "search_orders",
    "list_products"
  ]
};

forbid(
  principal,
  action == Action::"call_tool",
  resource
) when {
  resource.tool_name in [
    "delete_customer",
    "modify_payment",
    "execute_sql"
  ]
};
```

**说明：** 一个提供客户数据的生产环境 MCP 服务器。允许只读操作；阻断破坏性操作。

### 示例 3：事件后验证审计包

```bash
# Export the session's audit bundle
npx protect-mcp export-bundle --session sess_abc123 --out audit.json

# Verify every receipt in the bundle
npx @veritasacta/verify audit.json --bundle

# Expected output:
# ✓ Bundle: VALID
#   Total:    47
#   Passed:   47
#   Failed:   0
```

**说明：** 事件发生后，导出审计包并验证所有回执未被篡改。审计包包含会话的所有回执以及验证所需的签名密钥。

## 最佳实践

- ✅ **应该：** 从影子模式开始，先观察再强制执行
- ✅ **应该：** 使用 `policy_digest` 追踪每个决策对应的策略版本
- ✅ **应该：** 将回执与应用日志一起存储，便于关联分析
- ✅ **应该：** 集成到 CI 时固定验证器版本（`@veritasacta/verify@0.2.5`）
- ❌ **不应该：** 跳过影子模式，直接在生产环境启用强制模式
- ❌ **不应该：** 未经独立验证就信任 `claimed_issuer_tier`
- ❌ **不应该：** 将有效签名等同于签名者可信——签名只能证明回执自签名后未被篡改

## 故障排查

### 问题：回执验证失败，提示 `no_public_key`
**症状：** `npx @veritasacta/verify receipt.json` 返回退出码 2，提示 `no_public_key`
**解决方案：** 显式提供公钥：`--key <64位十六进制字符>`。回执默认不嵌入公钥。在 `protect-mcp.config.json` 中查找发行者的公钥。

### 问题：影子模式出现意外的拒绝
**症状：** 影子日志显示预期允许的工具被 `deny`
**解决方案：** 检查 Cedar 策略的顺序。Cedar 先评估 `forbid` 规则再评估 `permit` 规则——宽泛的 `forbid` 会覆盖具体的 `permit` 规则。

### 问题：强制模式阻断了合法的工具调用
**症状：** 切换到强制模式后，智能体报告工具调用被拒绝
**解决方案：** 将该工具添加到 permit 策略中，或切回影子模式（移除 `--enforce` 标志）。查看回执的 `deny_reason` 字段了解具体的策略违规原因。

## 相关技能

- `@security-auditor` — 通用安全审计与合规
- `@security-audit` — 代码漏洞扫描
- `@mcp-development` — MCP 服务器开发模式

## 扩展资源

- [protect-mcp on npm](https://www.npmjs.com/package/protect-mcp) — MIT 许可证
- [Cedar Policy Language](https://www.cedarpolicy.com/) — AWS 开源策略引擎
- [IETF Draft: Signed Receipts](https://datatracker.ietf.org/doc/draft-farley-acta-signed-receipts/) — 回执格式规范
- [@veritasacta/verify](https://www.npmjs.com/package/@veritasacta/verify) — Apache-2.0 许可验证器，支持离线使用

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 缺少必要输入、权限、安全边界或成功标准时，停下来请求澄清。
