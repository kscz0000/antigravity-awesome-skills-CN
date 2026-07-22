---
name: whatsapp-cloud-api
description: 集成 WhatsApp Business Cloud API（Meta）。支持消息、模板、HMAC-SHA256 webhook、客服自动化。提供 Node.js 和 Python 样板代码。触发词：whatsapp、whatsapp business、api whatsapp、chatbot whatsapp、mensagem whatsapp、template whatsapp。
risk: critical
source: community
date_added: '2026-03-06'
author: renat
tags:
- messaging
- whatsapp
- meta
- webhooks
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# WhatsApp Cloud API - 专业集成方案

## 概述

集成 WhatsApp Business Cloud API（Meta）。支持消息、模板、HMAC-SHA256 webhook、客服自动化。提供 Node.js 和 Python 样板代码。

## 何时使用此技能

- 当用户提及 "whatsapp" 或相关主题时
- 当用户提及 "whatsapp business" 或相关主题时
- 当用户提及 "api whatsapp" 或相关主题时
- 当用户提及 "chatbot whatsapp" 或相关主题时
- 当用户提及 "mensagem whatsapp" 或相关主题时
- 当用户提及 "template whatsapp" 或相关主题时

## 何时不使用此技能

- 任务与 WhatsApp Cloud API 无关
- 更简单、更具体的工具可以处理该请求
- 用户需要不具备领域专业知识的通用帮助

## 工作原理

使用 Meta 官方的 Cloud API 实现与 WhatsApp Business 的专业集成。支持 Node.js/TypeScript 和 Python。

## 概览

WhatsApp Cloud API 是 Meta 官方提供的 API，用于通过 WhatsApp Business 发送和接收消息。自 2025 年 10 月起，它是唯一受支持的选项（On-Premises API 已被弃用）。

**API 版本：** Graph API v21.0（2026）
**基础 URL：** `https://graph.facebook.com/v21.0/{phone-number-id}/messages`
**认证方式：** Bearer Token（生产环境使用 System User Token）

**2026 年价格（每条消息）：**

| 类别            | 费用                | 计费场景                            |
|----------------|---------------------|-------------------------------------|
| Marketing      | $0.025-$0.1365      | 营销活动、促销                       |
| Utility        | $0.004-$0.0456      | 订单确认、状态更新                   |
| Authentication | $0.004-$0.0456      | 一次性密码、密码重置                 |
| Service        | 免费                | 24 小时会话窗口内的回复              |

**前置条件：**
- Meta Business Suite 账号（免费）
- 在 Meta for Developers 上创建包含 WhatsApp 产品的应用
- 已验证的电话号码
- System User Token（永久有效）

如果用户没有 Meta Business 账号，请阅读 `references/setup-guide.md` 获取从零开始的完整设置指南。

---

## 决策树

使用此决策树确定下一步操作：

```
用户是否需要初始设置？
├── 是 → 阅读 references/setup-guide.md
└── 否 → 使用哪种语言？
    ├── Node.js/TypeScript
    └── Python
    → 要做什么？
       ├── 发送消息 → 下方"消息类型"章节
       ├── 接收消息 → 下方"Webhooks"章节
       ├── 自动化客服 → 下方"自动化"章节
       ├── WhatsApp Flows / Commerce → 下方"高级功能"章节
       ├── 管理模板 → references/template-management.md
       └── 合规 / 限额 → 下方"合规与质量"章节
```

要使用现成的样板代码从零启动项目，请运行此脚本：
```bash
python scripts/setup_project.py --language nodejs --path ./meu-projeto

## 或

python scripts/setup_project.py --language python --path ./meu-projeto
```

---

## 1. 配置环境变量

```env
WHATSAPP_TOKEN=seu_access_token_aqui
PHONE_NUMBER_ID=seu_phone_number_id
WABA_ID=seu_whatsapp_business_account_id
APP_SECRET=seu_app_secret
VERIFY_TOKEN=token_customizado_para_webhook
```

## 2. 发送简单文本消息

**Node.js/TypeScript：**
```typescript
import axios from 'axios';

const GRAPH_API = 'https://graph.facebook.com/v21.0';

async function sendText(to: string, message: string) {
  const response = await axios.post(
    `${GRAPH_API}/${process.env.PHONE_NUMBER_ID}/messages`,
    {
      messaging_product: 'whatsapp',
      to,
      type: 'text',
      text: { body: message }
    },
    { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } }
  );
  return response.data; // { messaging_product, contacts, messages: [{ id }] }
}
```

**Python：**
```python
import httpx
import os

GRAPH_API = "https://graph.facebook.com/v21.0"

async def send_text(to: str, message: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{GRAPH_API}/{os.environ['PHONE_NUMBER_ID']}/messages",
            json={
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": message}
            },
            headers={"Authorization": f"Bearer {os.environ['WHATSAPP_TOKEN']}"}
        )
        return response.json()  # {"messaging_product", "contacts", "messages": [{"id"}]}
```

## 3. 发送模板消息（24 小时窗口外）

模板是与客户发起对话的唯一方式。使用前必须经过 WhatsApp 批准。

```json
{
  "messaging_product": "whatsapp",
  "to": "5511999999999",
  "type": "template",
  "template": {
    "name": "hello_world",
    "language": { "code": "pt_BR" },
    "components": [
      {
        "type": "body",
        "parameters": [
          { "type": "text", "text": "João" }
        ]
      }
    ]
  }
}
```

## 4. 验证发送是否成功

使用测试脚本进行验证：
```bash
python scripts/send_test_message.py --to 5511999999999 --message "Teste de integracao"
```

---

## 消息类型

| 类型                | 用途                                | 限制              |
|--------------------|-------------------------------------|-------------------|
| Text               | 简单文本消息                        | 4096 字符         |
| Template           | 发起对话 / 24 小时窗口外             | 正文 1600 字符    |
| Image              | 图片                                | 5MB               |
| Document           | PDF、电子表格、文档                  | 100MB             |
| Video              | 视频                                | 16MB              |
| Audio              | 语音消息                            | 16MB              |
| Interactive Button | 快速回复按钮                        | 最多 3 个按钮     |
| Interactive List   | 分区选项菜单                        | 最多 10 个选项    |
| Location           | 共享位置                            | 经纬度            |
| Contact            | 共享联系人                          | vCard 格式        |
| Reaction           | 对消息使用 emoji 反应               | 1 个 emoji        |

**示例 - 交互式按钮（Node.js）：**
```typescript
async function sendButtons(to: string, body: string, buttons: Array<{id: string, title: string}>) {
  return axios.post(`${GRAPH_API}/${process.env.PHONE_NUMBER_ID}/messages`, {
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'button',
      body: { text: body },
      action: {
        buttons: buttons.map(b => ({
          type: 'reply',
          reply: { id: b.id, title: b.title }
        }))
      }
    }
  }, { headers: { Authorization: `Bearer ${process.env.WHATSAPP_TOKEN}` } });
}

// 使用示例：
await sendButtons('5511999999999', 'Como posso ajudar?', [
  { id: 'suporte', title: 'Suporte' },
  { id: 'vendas', title: 'Vendas' },
  { id: 'info', title: 'Informacoes' }
]);
```

**有关所有类型的完整 Node.js 和 Python 示例**，请阅读 `references/message-types.md`。

---

## Webhooks

Webhook 允许您实时接收消息和状态更新。

## 验证（Get）- 必需

当您在 Meta Developers 上配置 webhook 时，Meta 会发送一个 GET 请求进行验证：

```typescript
// Node.js (Express)
app.get('/webhook', (req, res) => {
  const mode = req.query['hub.mode'];
  const token = req.query['hub.verify_token'];
  const challenge = req.query['hub.challenge'];

  if (mode === 'subscribe' && token === process.env.VERIFY_TOKEN) {
    res.status(200).send(challenge);
  } else {
    res.sendStatus(403);
  }
});
```

## 接收（Post）- 使用 HMAC-SHA256 安全验证

每个 webhook 通知都通过 `X-Hub-Signature-256` 请求头进行签名。处理前请务必验证：

```typescript
import crypto from 'crypto';

function validateSignature(rawBody: Buffer, signature: string): boolean {
  const expectedSig = crypto
    .createHmac('sha256', process.env.APP_SECRET!)
    .update(rawBody)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(`sha256=${expectedSig}`),
    Buffer.from(signature)
  );
}
```

**重要：** 使用 `crypto.timingSafeEqual`（Node.js）或 `hmac.compare_digest`（Python）来防止时序攻击。切勿使用简单的字符串比较。

## 接收到的事件

- **messages** - 客户消息（文本、媒体、按钮、位置）
- **statuses** - 状态更新（sent → delivered → read）
- **errors** - 投递错误

**要求：**
- 使用有效 SSL 证书的 HTTPS 端点
- 在 5 秒内返回 HTTP 200 响应
- 开发环境：使用 ngrok 进行本地测试

**有关 Node.js 和 Python 的完整设置与示例**，请阅读 `references/webhook-setup.md`。

---

## 交互式主菜单

使用按钮或列表在首次交互时创建选项菜单：

```python

## Python - 使用交互式列表的菜单

async def send_main_menu(to: str):
    await send_interactive_list(
        to=to,
        header="Bem-vindo!",
        body="Selecione o que precisa:",
        button_text="Ver opcoes",
        sections=[{
            "title": "Atendimento",
            "rows": [
                {"id": "suporte", "title": "Suporte Tecnico", "description": "Ajuda com problemas"},
                {"id": "vendas", "title": "Vendas", "description": "Conhecer nossos produtos"},
                {"id": "financeiro", "title": "Financeiro", "description": "Boletos e pagamentos"},
            ]
        }]
    )
```

## 流程状态机

使用状态机管理对话。每个客户都有一个当前状态，决定如何处理下一条消息：

```
INICIO → MENU_PRINCIPAL → SUPORTE → AGUARDANDO_DETALHES → ESCALACAO_HUMANO
                        → VENDAS → CATALOGO → CHECKOUT
                        → FINANCEIRO → SEGUNDA_VIA_BOLETO
```

## 24 小时会话窗口

- **窗口期内（客户最后一条消息后 24 小时内）：** 可以免费发送任何类型的消息
- **窗口期外：** 仅限模板消息（按类别计费）

## 集成 AI（Claude API）

将 WhatsApp 与 Claude 结合使用，提供智能回复：
1. 通过 webhook 接收消息
2. 将会话上下文一起发送到 Claude API
3. 通过 WhatsApp 返回回复
4. 保留转接人工客服的选项

**有关完整的自动化模式**，请阅读 `references/automation-patterns.md`。

---

## WhatsApp Flows

WhatsApp 内的多屏交互式表单。客户无需离开应用即可填写字段。使用 JSON 定义，包含 screens、components 和 actions。

使用场景：注册、预约、NPS 调查、产品选择。

## 商务与商品目录

WhatsApp 目录中最多可包含 500 个商品。可发送单品或多品商品消息，并支持应用内结账。

## 模板管理 API

以编程方式创建、列出和删除模板。每个账户最多 6000 个翻译版本。审批仅需几分钟。

## WhatsApp 频道

面向无限订阅者的单向广播。位于 WhatsApp 的"更新"标签页中。

## Click-to-WhatsApp 广告

在 Facebook/Instagram 上投放带有打开 WhatsApp 对话按钮的广告。打开率高达 99%。

## 状态跟踪

跟踪投递：pending → server → device → read。通过状态更新 webhook 接收。

**有关高级功能的完整详情**，请阅读 `references/advanced-features.md`。
**有关通过 API 管理模板**，请阅读 `references/template-management.md`。

---

## 基本检查清单

- [ ] 发送消息前已获得明确的选择加入
- [ ] 已实现选择退出机制（关键字 "SAIR" 或 "STOP"）
- [ ] 同意书记录包含时间戳、方式和用途
- [ ] 内容符合 WhatsApp 政策（无垃圾邮件、无违禁内容）
- [ ] 符合 LGPD/GDPR（法律基础已定义，尊重数据主体权利）
- [ ] 消息频率合理（不过度）
- [ ] 使用前模板已获批准
- [ ] 已完成企业验证（用于提高限额）

## 质量评级

WhatsApp 会监控您消息的质量并分配评级：

| 评级     | 含义                            | 措施                              |
|----------|--------------------------------|----------------------------------|
| 绿色     | 质量良好，被屏蔽少              | 保持现状 — 有资格升级            |
| 黄色     | 质量中等，需要关注              | 审查内容和频率                   |
| 红色     | 质量低，有被封禁风险            | 立即采取行动：减少发送量         |

**积极信号：** 回复率高、参与度高、被屏蔽少
**消极信号：** 被屏蔽、垃圾投诉、互动率低

## Tier 体系（消息限制）

自 2025 年 10 月起，限制按 **Business Portfolio**（而非按号码）计算：

| 等级         | 每 24 小时对话数 | 如何达到                            |
|--------------|-------------------|-------------------------------------|
| 初始         | 250               | 新账号 / 未验证                     |
| Tier 1       | 1,000             | 自动升级：7 天内使用 50%+ 限额      |
| Tier 2       | 10,000            | 自动升级：7 天内使用 50%+ 限额      |
| Tier 3       | 100,000           | 自动升级：7 天内使用 50%+ 限额      |
| 无限         | 无限制            | 自动升级：7 天内使用 50%+ 限额      |

**2026 年变化：** 2K 和 10K 等级将被移除。企业验证后，立即获得 100K 限额。

**有关完整合规指南**，请阅读 `references/compliance.md`。

---

## 故障排查

| 问题                            | 可能原因                          | 解决方案                                |
|--------------------------------|----------------------------------|-----------------------------------------|
| 401 Unauthorized               | Token 过期或无效                  | 生成新的 System User Token              |
| 400 Bad Request                | 负载格式错误                      | 参照示例检查 JSON                        |
| 模板被拒绝                     | 内容违反政策                      | 修改后重新提交                          |
| Webhook 接收不到消息           | URL 无效或未启用 HTTPS            | 开发环境使用 ngrok，生产环境使用 SSL 证书 |
| 超出速率限制                   | 超过 80 msg/s                     | 实现带重试的队列                        |
| 质量评级低                     | 被屏蔽/投诉过多                   | 减少发送量，改善内容                    |
| 消息未送达                     | 号码无效或未使用 WhatsApp         | 发送前验证号码                          |
| 号码未验证                     | 未完成 OTP 验证                   | 通过短信或电话重复验证流程              |

要验证您的配置：
```bash
python scripts/validate_config.py
```

---

## 参考资料（按需阅读）

| 文件                              | 何时阅读                                            |
|----------------------------------|----------------------------------------------------|
| `references/setup-guide.md`      | 初始设置 — 创建 Meta 账号，配置 API               |
| `references/message-types.md`    | 所有消息类型的完整示例                             |
| `references/webhook-setup.md`    | 使用 HMAC 安全机制配置 webhooks                   |
| `references/automation-patterns.md` | 聊天机器人、队列、状态机、AI 集成                |
| `references/compliance.md`       | LGPD/GDPR、选择加入、质量评级、Tier 体系          |
| `references/api-reference.md`    | 端点、错误、速率限制、2026 年价格                 |
| `references/advanced-features.md` | Flows、Commerce、Channels、Ads、状态跟踪         |
| `references/template-management.md` | 通过 API 进行模板的 CRUD 操作                    |

## 脚本

| 脚本                              | 功能                                          |
|----------------------------------|-----------------------------------------------|
| `scripts/setup_project.py`       | 使用样板代码创建项目（Node.js 或 Python）     |
| `scripts/validate_config.py`     | 验证凭据和与 API 的连接                       |
| `scripts/send_test_message.py`   | 发送测试消息以验证设置                        |

## 样板代码

| 目录                              | 内容                                          |
|----------------------------------|-----------------------------------------------|
| `assets/boilerplate/nodejs/`     | 完整的 TypeScript/Express 项目                |
| `assets/boilerplate/python/`     | 完整的 Python/Flask 项目                      |
| `assets/examples/`               | JSON 负载示例（模板、webhooks、flows）        |

## 最佳实践

- 提供清晰、具体的项目和需求背景信息
- 在将建议应用到生产代码前进行审查
- 与其他互补技能结合使用以进行全面分析

## 常见陷阱

- 将此技能用于其领域专业之外的任务
- 在不了解具体上下文的情况下应用建议
- 未提供足够的项目上下文以进行准确分析

## 相关技能

- `instagram` - 用于增强分析的互补技能
- `social-orchestrator` - 用于增强分析的互补技能
- `telegram` - 用于增强分析的互补技能

## 限制

- 仅在任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
