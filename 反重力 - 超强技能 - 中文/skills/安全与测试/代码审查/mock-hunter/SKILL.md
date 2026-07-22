---
name: mock-hunter
description: "在五个阶段（目录、点击、追踪、分类、报告）中审计实时网页，识别 Mock 数据、硬编码值、LLM 生成的指标和失效端点。输出 Markdown 报告，对每个可见值给出 REAL/MOCK/LLM/HARDCODED/BROKEN/UNKNOWN 判定。适用于网页审计、Mock 数据检测、AI 生成数据排查、硬编码值发现。"
category: testing
risk: critical
source: community
source_repo: CodeShuX/mockhunter
source_type: community
date_added: "2026-05-07"
author: CodeShuX
tags: [testing, qa, playwright, mock-detection, web-audit, ai-testing, vibe-coding, claude-code]
tools: [claude]
license: "MIT"
license_source: "https://github.com/CodeShuX/mockhunter/blob/main/LICENSE"
plugin:
  targets:
    codex: blocked
    claude: blocked
---

# MockHunter — 实时页面真实性核查

## 概述

MockHunter 是一个 Claude Code 技能，用于审计实时网页并告诉你：每个可见值是真实的、模拟的、LLM 生成的、硬编码的、损坏的，还是未知的。它专为 vibe 编码应用（Lovable、Bolt、v0、Replit、AI Studio、Cursor Composer）而设计——这类应用的 UI 看起来很完整，但数据层往往不是。

该技能使用 Playwright MCP 驱动真实浏览器，然后通过追踪网络层和 DOM 层来定位每个可见值的来源。

此技能改编自上游 `CodeShuX/mockhunter` 项目（社区源）。

由于此工作流会对真实浏览器驱动真实页面，请将其视为交互式审计工具，而非插件安全的只读辅助工具。在用户确认目标归属、指定安全的测试账号或环境、并明确批准任何可能改变状态的点击、提交或认证操作之前，默认仅做观察。

## 使用场景

- 审计 AI 生成的 UI，判断哪些值真正接通了后端数据
- 在验收前审查外包方或团队成员的交付物
- 在向客户或投资人展示 vibe 编码 MVP 之前先行自查
- 当仪表盘"看起来太整洁"——所有指标整齐划一、时间戳扎堆、毫无波动——怀疑存在种子数据时使用

## 工作原理

### 阶段一：准备与智能提问

1. 向用户问好，获取目标 URL
2. 从 URL 自动检测技术栈（`*.lovable.app`、`*.bolt.new`、`*.v0.app`、`*.replit.app`、`aistudio.google.com`，否则为自定义）
3. 提问 3-5 个定向问题：认证方式（公开 / 本地 / 表单 / 跳过）、数据库访问权限（可选）、可疑点、页面用途
4. 确认审计方案、所有权/权限、目标环境以及允许的操作类别后继续执行

### 阶段二：导航与目录采集

1. `browser_navigate` 到目标 URL
2. 按选定模式处理认证（表单登录：填写字段、点击提交）
3. 等待网络空闲（最多 10 秒）
4. 截取全页截图，捕获无障碍快照
5. 盘点每一个元素：标题、按钮、链接、输入框、卡片、徽章、指标、表格单元格、空状态、图片
6. 记录初始控制台错误和网络请求

### 阶段三：测试交互性

1. 对每个 Tab：仅在用户批准导航式交互后才点击，然后截图、滚动到底部、重新盘点
2. 对每个按钮：仅在用户明确允许的情况下操作——且控件需通过角色、无障碍名称、周边文本、图标、URL/动作目标和预期网络副作用等维度确认非破坏性；对破坏性或模糊控件选择跳过，而非仅依赖标签正则
3. 对每个表单：识别必填字段，优先做空提交校验；仅当用户明确批准了具体表单、目标环境和测试账号后，才提交一次性测试数据
4. 记录每个元素的行为表现

### 阶段四：追溯来源

对每个可见值，运行如下判定树：

```
是否有网络请求返回了该值？
├── 是 — 在响应中发现：
│   ├── 状态码 4xx/5xx → BROKEN
│   ├── 端点匹配 /ai|openai|generate|llm|chat → LLM
│   ├── 响应体形态匹配 Mock 库（faker、MSW、mockoon）→ MOCK
│   ├── 均一性标志触发 → MOCK 或 LLM（需人工复核）
│   ├── 是否提供了数据库连接？
│   │   ├── 执行只读 SELECT，值匹配数据库行 → REAL
│   │   └── 值不在数据库中 → MOCK
│   └── 无数据库 → UNKNOWN（最优猜测）
└── 否 — 该值不在任何网络响应中：
    ├── DOM 源码中的字符串字面量 → HARDCODED
    ├── 由 Math.random / Date.now / faker 计算得出 → MOCK
    └── 无法确定 → UNKNOWN
```

均一性启发式规则标记可疑数据：
- 所有行数值完全相同
- 所有百分比均为整数（50%、75%、90%）
- 所有时间戳集中在同一分钟内
- 10+ 行中唯一值少于 3 个

### 阶段五：报告生成

生成 `mockhunter-report.md`，包含：
- 汇总表（各判定数量统计）
- 按 Section/Tab 分列的发现项（元素 / 值 / 判定 / 来源 / 严重程度 / 处置建议）
- 控制台错误和网络失败记录
- 无效按钮（NO-OP buttons）
- 可疑模式
- 面向用户的智能后续问题

## 示例

### 示例一：审计 Lovable 管理后台

```
User: /mockhunter audit https://my-app.lovable.app/admin
Skill: [阶段一] 技术栈检测：Lovable。认证：跳过。数据库：无。
       [阶段二] 目录采集：6 张指标卡、4 个审核队列、8 条动态。
       [阶段三] 搜索框：无效按钮（零次网络请求）。活动链接 → 404。
       [阶段四] 打包体积 2.7 MB。零个 /api/、零个 supabase、零个 axios。
                 "$42,850" → JSX 字符串字面量 → HARDCODED。
                 "+12% vs last month" → 字符串字面量 → HARDCODED。
       [阶段五] 判定结果：23 HARDCODED、1 BROKEN、1 NO-OP、0 REAL。
                 报告已写入 ./mockhunter-report.md
```

### 示例二：公开营销站点（基本为真实数据）

```
User: /mockhunter audit https://example-saas.com
Skill: ...
       [阶段五] 判定结果：8 REAL、18 HARDCODED（有意为之的营销文案），
                 0 MOCK、0 BROKEN、2 UNKNOWN。
                 无控制台错误，无失效端点。
```

## 最佳实践

- ✅ 有条件就提供数据库访问——可将 UNKNOWN 判定提升为 REAL 或 MOCK
- ✅ 使用专用测试账号进行表单登录认证
- ✅ 执行冷启动测试（零数据态）——大量 vibe 编码应用在此场景下会暴露问题
- ✅ 明确告知技能哪些区块是有意用 AI 生成的，避免误报
- ❌ 未经许可不要对自己不拥有的应用执行主动交互——真实点击和表单提交可能改变状态
- ❌ 不要仅依赖破坏性按钮排除列表——本地化标签、图标、aria 文本和后端路由都可能隐藏状态变更操作
- ❌ 如果页面加载失败，不要相信审计结果——先检查控制台

## 局限性

- 每次仅审计单个页面——v0.1.0 不支持多页面爬取
- 仅支持表单登录认证——v0.1.0 不支持 OAuth、Magic Link 或 2FA
- 单页最多处理约 30 个最突出的按钮
- 仅输出 Markdown 报告——暂无 JSON 输出
- 数据库验证支持可通过 shell 命令访问的任意数据库（psql、mysql、mongosh、wrangler、supabase REST），但不直接支持 Firestore

## 安全与注意事项

- 该技能只执行只读数据库 SELECT 操作，绝不执行 INSERT/UPDATE/DELETE
- 跳过具有破坏性外观、模糊含义、仅有图标、本地化或外部写入特征的控件，除非用户明确将特定控件和环境列入白名单
- 绝不会提交看起来像支付、账户删除、外部写入操作、账号变更、邀请、发布、部署、消息发送或资金流转的表单
- 对任何一次性表单测试使用占位凭据（`mockhunter@example.com`），绝不使用用户的真实凭据
- 所有 Playwright 操作均在受控的 MCP 浏览器上下文中执行——不存在无头浏览器提权风险