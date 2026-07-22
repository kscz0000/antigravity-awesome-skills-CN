# 示例：使用 3 个并行智能体构建完整的 Next.js 功能

## 场景
用户提示："添加用户认证流程——登录页、注册页和受保护的仪表盘路由。"

---

## 任务简报（协调器产出）

```
MISSION BRIEF
─────────────────────────────────────────
Goal: 包含登录、注册和受保护仪表盘的认证流程——全部连通并可用。
Total Agents: 3
Quota Strategy: 全部使用 FLASH，仅集成审查使用 Sonnet
Expected Token Cost: MEDIUM

AGENTS:
[1] ID: agent-001
    Role: Builder — 认证 UI
    Scope: /app/login/page.tsx, /app/signup/page.tsx
    Model: Gemini Flash
    Input: GEMINI.md 中的设计系统、表单字段规格
    Output: 两个完整的页面组件，使用 Tailwind 样式
    Depends on: none

[2] ID: agent-002
    Role: Builder — API 路由
    Scope: /app/api/auth/login/route.ts, /app/api/auth/signup/route.ts
    Model: Gemini Flash
    Input: 认证逻辑规格、.env.example 中的环境变量名
    Output: 两个带错误响应的 API 路由处理器
    Depends on: none

[3] ID: agent-003
    Role: Builder — 受保护路由
    Scope: /app/dashboard/page.tsx, /middleware.ts
    Model: Gemini Flash
    Input: agent-001 的输出（会话结构）、agent-002 的输出（令牌格式）
    Output: 仪表盘页面 + 中间件重定向逻辑
    Depends on: agent-001, agent-002
─────────────────────────────────────────
```

---

## 执行流程

```
第 1 轮（并行）：
  agent-001 → 构建登录 + 注册 UI
  agent-002 → 构建 API 路由

  [第 1 轮后抽查]
  ✓ agent-001 仅在 /app/login 和 /app/signup 内操作
  ✓ agent-002 使用了正确的环境变量名
  ✓ 两个输出中都没有遗留 TODO

第 2 轮（顺序，依赖第 1 轮）：
  agent-003 → 构建仪表盘 + 中间件
              接收 agent-001 的会话结构
              接收 agent-002 的令牌格式

  [第 2 轮后抽查]
  ✓ 中间件正确引用会话 cookie 名
  ✓ 仪表盘 import 解析到现有组件
  ✓ 没有硬编码的重定向 URL

集成检查：
  ✓ 所有 import 解析正确
  ✓ 没有重复的类型定义
  ✓ 构建心理验证通过
```

---

## 配额日志

| 事件 | 影响 |
|-------|--------|
| 3 个智能体生成 | LOW |
| 总共约 12 个文件索引 | LOW |
| 所有智能体约 18 次工具调用 | MEDIUM |
| 0 个浏览器智能体 | NONE |
| **预估总量** | **~25% 冲刺** |

> 提示：此任务花费约 25% 冲刺配额。免费层级下每天可以运行 3–4 个这样的任务。
