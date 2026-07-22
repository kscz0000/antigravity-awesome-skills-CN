# 客服自动化模式 - WhatsApp Cloud API

通过 WhatsApp 实现专业客服自动化的完整指南，包括聊天机器人、客服队列、状态机和 AI 集成。

---

## 目录

1. [自动化架构](#arquitetura-de-automacao)
2. [交互式主菜单](#menu-principal-interativo)
3. [流程状态机](#state-machine-para-fluxos)
4. [会话管理](#gerenciamento-de-sessao)
5. [客服队列](#fila-de-atendimento)
6. [升级到人工客服](#escalacao-para-humano)
7. [非工作时间回复](#respostas-fora-do-horario)
8. [AI 集成（Claude API）](#integracao-com-ia-claude-api)
9. [用于表单的 WhatsApp Flows](#whatsapp-flows-para-formularios)
10. [完整的端到端流程](#fluxo-end-to-end-completo)

---

## 自动化架构

```
WhatsApp 客户端
       │
       ▼
   Webhook POST
       │
       ▼
  HMAC 验证
       │
       ▼
  会话管理器 ──► 查找/创建客户会话
       │
       ▼
  状态路由器 ──► 根据当前状态确定处理程序
       │
       ├── INICIO → 主菜单
       ├── MENU → 选项路由器
       ├── SUPORTE → 支持流程
       ├── VENDAS → 目录/结账
       ├── HUMANO → 客服队列
       └── IA → Claude API 处理程序
```

---

## 交互式主菜单

### 使用按钮（最多 3 个选项）

**Node.js：**
```typescript
async function sendMainMenuButtons(to: string): Promise<void> {
  await sendMessage({
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'button',
      header: { type: 'text', text: 'Bem-vindo!' },
      body: { text: 'Olá! Como posso ajudar você hoje?' },
      footer: { text: 'Selecione uma opção abaixo' },
      action: {
        buttons: [
          { type: 'reply', reply: { id: 'btn_suporte', title: 'Suporte' } },
          { type: 'reply', reply: { id: 'btn_vendas', title: 'Vendas' } },
          { type: 'reply', reply: { id: 'btn_info', title: 'Informações' } }
        ]
      }
    }
  });
}
```

### 使用列表（分区中最多 10 个选项）

**Python：**
```python
async def send_main_menu_list(to: str) -> None:
    await send_message({
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "header": {"type": "text", "text": "Menu Principal"},
            "body": {"text": "Selecione o departamento:"},
            "footer": {"text": "Horário: Seg-Sex 8h-18h"},
            "action": {
                "button": "Ver opções",
                "sections": [
                    {
                        "title": "Atendimento",
                        "rows": [
                            {"id": "suporte_tecnico", "title": "Suporte Técnico", "description": "Problemas com produto ou serviço"},
                            {"id": "suporte_financeiro", "title": "Financeiro", "description": "Boletos, pagamentos, reembolsos"},
                            {"id": "suporte_comercial", "title": "Comercial", "description": "Novos pedidos e orçamentos"}
                        ]
                    },
                    {
                        "title": "Informações",
                        "rows": [
                            {"id": "info_horario", "title": "Horário de Funcionamento"},
                            {"id": "info_endereco", "title": "Endereço e Contato"},
                            {"id": "info_faq", "title": "Perguntas Frequentes"}
                        ]
                    }
                ]
            }
        }
    })
```

---

## 流程状态机

### 状态模型

```typescript
enum ConversationState {
  INICIO = 'INICIO',
  MENU_PRINCIPAL = 'MENU_PRINCIPAL',
  SUPORTE_TECNICO = 'SUPORTE_TECNICO',
  SUPORTE_AGUARDANDO_DETALHES = 'SUPORTE_AGUARDANDO_DETALHES',
  SUPORTE_AGUARDANDO_ANEXO = 'SUPORTE_AGUARDANDO_ANEXO',
  VENDAS_CATALOGO = 'VENDAS_CATALOGO',
  VENDAS_CHECKOUT = 'VENDAS_CHECKOUT',
  FINANCEIRO = 'FINANCEIRO',
  FINANCEIRO_SEGUNDA_VIA = 'FINANCEIRO_SEGUNDA_VIA',
  ATENDIMENTO_HUMANO = 'ATENDIMENTO_HUMANO',
  ATENDIMENTO_IA = 'ATENDIMENTO_IA',
  PESQUISA_NPS = 'PESQUISA_NPS',
  FINALIZADO = 'FINALIZADO'
}
```

### 状态路由器

```typescript
interface Session {
  phone: string;
  state: ConversationState;
  data: Record<string, any>;
  lastActivity: Date;
  agentId?: string;
}

async function routeMessage(session: Session, message: IncomingMessage): Promise<void> {
  const handlers: Record<ConversationState, MessageHandler> = {
    [ConversationState.INICIO]: handleInicio,
    [ConversationState.MENU_PRINCIPAL]: handleMenuPrincipal,
    [ConversationState.SUPORTE_TECNICO]: handleSuporteTecnico,
    [ConversationState.SUPORTE_AGUARDANDO_DETALHES]: handleAguardandoDetalhes,
    [ConversationState.VENDAS_CATALOGO]: handleVendasCatalogo,
    [ConversationState.FINANCEIRO]: handleFinanceiro,
    [ConversationState.ATENDIMENTO_HUMANO]: handleAtendimentoHumano,
    [ConversationState.ATENDIMENTO_IA]: handleAtendimentoIA,
    [ConversationState.PESQUISA_NPS]: handlePesquisaNPS,
    // ... 其他状态
  };

  const handler = handlers[session.state] || handleInicio;
  await handler(session, message);
}
```

### 处理程序示例

```typescript
async function handleMenuPrincipal(session: Session, message: IncomingMessage): Promise<void> {
  const selectedId = message.interactive?.button_reply?.id
    || message.interactive?.list_reply?.id
    || message.text?.body?.toLowerCase();

  switch (selectedId) {
    case 'btn_suporte':
    case 'suporte_tecnico':
      session.state = ConversationState.SUPORTE_TECNICO;
      await sendText(session.phone, 'Entendido! Descreva seu problema e nossa equipe vai ajudar.');
      session.state = ConversationState.SUPORTE_AGUARDANDO_DETALHES;
      break;

    case 'btn_vendas':
    case 'suporte_comercial':
      session.state = ConversationState.VENDAS_CATALOGO;
      await sendProductCatalog(session.phone);
      break;

    case 'btn_info':
    case 'info_faq':
      await sendFAQ(session.phone);
      // FAQ 后保持在菜单中
      break;

    default:
      await sendText(session.phone, 'Desculpe, não entendi. Vou mostrar o menu novamente.');
      await sendMainMenuButtons(session.phone);
      break;
  }

  session.lastActivity = new Date();
  await saveSession(session);
}
```

---

## 会话管理

### 使用 Redis（生产环境）

```typescript
import Redis from 'ioredis';

const redis = new Redis(process.env.REDIS_URL);
const SESSION_TTL = 86400; // 24 小时（WhatsApp 窗口）

async function getSession(phone: string): Promise<Session> {
  const data = await redis.get(`wa_session:${phone}`);
  if (data) {
    return JSON.parse(data);
  }
  return createNewSession(phone);
}

async function saveSession(session: Session): Promise<void> {
  session.lastActivity = new Date();
  await redis.set(
    `wa_session:${session.phone}`,
    JSON.stringify(session),
    'EX',
    SESSION_TTL
  );
}

function createNewSession(phone: string): Session {
  return {
    phone,
    state: ConversationState.INICIO,
    data: {},
    lastActivity: new Date()
  };
}
```

### 使用内存（开发环境）

```python
from datetime import datetime, timedelta
from typing import Dict, Optional

sessions: Dict[str, dict] = {}
SESSION_TTL = timedelta(hours=24)

def get_session(phone: str) -> dict:
    session = sessions.get(phone)
    if session and datetime.now() - session["last_activity"] < SESSION_TTL:
        return session
    return create_new_session(phone)

def save_session(session: dict) -> None:
    session["last_activity"] = datetime.now()
    sessions[session["phone"]] = session

def create_new_session(phone: str) -> dict:
    session = {
        "phone": phone,
        "state": "INICIO",
        "data": {},
        "last_activity": datetime.now()
    }
    sessions[phone] = session
    return session
```

**重要：** WhatsApp 的 24 小时窗口允许在客户最后一条消息后 24 小时内免费回复。请将会话 TTL 与此窗口对齐。

---

## 客服队列

### 带优先级的队列模型

```typescript
interface QueueItem {
  phone: string;
  department: string;
  priority: 'alta' | 'media' | 'baixa';
  enteredAt: Date;
  estimatedWait: number; // 分钟
}

class AttendanceQueue {
  private queues: Map<string, QueueItem[]> = new Map();

  async addToQueue(item: QueueItem): Promise<number> {
    const dept = item.department;
    if (!this.queues.has(dept)) this.queues.set(dept, []);

    const queue = this.queues.get(dept)!;
    queue.push(item);

    // 按优先级和进入时间排序
    queue.sort((a, b) => {
      const priorityOrder = { alta: 0, media: 1, baixa: 2 };
      if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
        return priorityOrder[a.priority] - priorityOrder[b.priority];
      }
      return a.enteredAt.getTime() - b.enteredAt.getTime();
    });

    const position = queue.indexOf(item) + 1;

    // 通知客户排队位置
    await sendText(item.phone,
      `Você está na posição ${position} da fila do setor ${dept}. ` +
      `Tempo estimado: ~${position * 5} minutos. Aguarde!`
    );

    return position;
  }

  async getNext(department: string): Promise<QueueItem | undefined> {
    const queue = this.queues.get(department);
    return queue?.shift();
  }
}
```

### SLA 与监控

```typescript
const SLA_CONFIG = {
  suporte: { maxWaitMinutes: 15, alertAfterMinutes: 10 },
  vendas: { maxWaitMinutes: 5, alertAfterMinutes: 3 },
  financeiro: { maxWaitMinutes: 20, alertAfterMinutes: 15 }
};

async function checkSLABreaches(): Promise<void> {
  for (const [dept, config] of Object.entries(SLA_CONFIG)) {
    const queue = attendanceQueue.getQueue(dept);
    for (const item of queue) {
      const waitMinutes = (Date.now() - item.enteredAt.getTime()) / 60000;
      if (waitMinutes > config.maxWaitMinutes) {
        await alertSupervisor(dept, item, waitMinutes);
      }
    }
  }
}
```

---

## 升级到人工客服

### 检测升级需求

```typescript
const ESCALATION_TRIGGERS = [
  'falar com humano', 'falar com atendente', 'atendente',
  'pessoa real', 'humano', 'reclamacao', 'reclamar',
  'cancelar', 'cancelamento', 'insatisfeito', 'gerente'
];

function shouldEscalate(message: string): boolean {
  const lower = message.toLowerCase();
  return ESCALATION_TRIGGERS.some(trigger => lower.includes(trigger));
}

async function escalateToHuman(session: Session): Promise<void> {
  session.state = ConversationState.ATENDIMENTO_HUMANO;

  // 通知客户
  await sendText(session.phone,
    'Entendi! Vou transferir você para um de nossos atendentes. ' +
    'Por favor, aguarde um momento.'
  );

  // 加入队列
  await attendanceQueue.addToQueue({
    phone: session.phone,
    department: session.data.department || 'geral',
    priority: session.data.isVIP ? 'alta' : 'media',
    enteredAt: new Date(),
    estimatedWait: 5
  });

  // 通知客服面板
  await notifyAgentPanel({
    type: 'new_customer',
    phone: session.phone,
    context: session.data,
    conversationHistory: session.data.history || []
  });

  await saveSession(session);
}
```

### 上下文移交

当人工客服接管时，应能看到自动化对话的历史记录：

```typescript
async function buildHandoffContext(session: Session): string {
  return `
📋 对话上下文：
- 客户：${session.phone}
- 部门：${session.data.department}
- 上一状态：${session.state}
- 报告问题：${session.data.problemDescription || '未指定'}
- 机器人尝试次数：${session.data.botAttempts || 0}
- 对话时长：${getElapsedTime(session.data.startedAt)}

📝 摘要历史：
${session.data.history?.map(h => `[${h.from}] ${h.text}`).join('\n') || '无历史记录'}
  `.trim();
}
```

---

## 非工作时间回复

```typescript
interface BusinessHours {
  timezone: string;
  schedule: Record<string, { open: string; close: string } | null>;
}

const BUSINESS_HOURS: BusinessHours = {
  timezone: 'America/Sao_Paulo',
  schedule: {
    monday: { open: '08:00', close: '18:00' },
    tuesday: { open: '08:00', close: '18:00' },
    wednesday: { open: '08:00', close: '18:00' },
    thursday: { open: '08:00', close: '18:00' },
    friday: { open: '08:00', close: '17:00' },
    saturday: { open: '09:00', close: '13:00' },
    sunday: null // 休息
  }
};

function isWithinBusinessHours(): boolean {
  const now = new Date().toLocaleString('en-US', { timeZone: BUSINESS_HOURS.timezone });
  const date = new Date(now);
  const day = date.toLocaleDateString('en-US', { weekday: 'long' }).toLowerCase();
  const hours = BUSINESS_HOURS.schedule[day];

  if (!hours) return false;

  const currentTime = date.toTimeString().slice(0, 5);
  return currentTime >= hours.open && currentTime <= hours.close;
}

async function handleOffHours(phone: string): Promise<void> {
  // 发送模板（24 小时窗口外可能没有活跃会话）
  await sendText(phone,
    '⏰ 我们的服务时间是：\n' +
    '周一至周四：8 点至 18 点\n' +
    '周五：8 点至 17 点\n' +
    '周六：9 点至 13 点\n\n' +
    '请留言，我们会尽快回复您！'
  );
}
```

---

## AI 集成（Claude API）

### 使用 Claude 的智能聊天机器人

```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic();

const SYSTEM_PROMPT = `您是 [公司名称] 的虚拟助手。您的职责是：
- 解答产品和服务的疑问
- 协助处理简单的技术问题
- 必要时转接给人工客服
- 保持礼貌、专业和客观
- 使用巴西葡萄牙语回复

规则：
- 每条回复最多 300 字符（WhatsApp 阅读体验限制）
- 不知道答案时，告知将转接给专员
- 切勿编造价格或库存信息
- 适度使用 emoji`;

async function getAIResponse(
  session: Session,
  userMessage: string
): Promise<{ text: string; shouldEscalate: boolean }> {
  const messages = (session.data.aiHistory || []).concat([
    { role: 'user', content: userMessage }
  ]);

  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 300,
    system: SYSTEM_PROMPT,
    messages
  });

  const aiText = response.content[0].type === 'text'
    ? response.content[0].text
    : '';

  // 检测 AI 是否建议升级
  const shouldEscalate = aiText.toLowerCase().includes('transferir')
    || aiText.toLowerCase().includes('especialista')
    || aiText.toLowerCase().includes('atendente');

  // 保存历史
  session.data.aiHistory = messages.concat([
    { role: 'assistant', content: aiText }
  ]);

  return { text: aiText, shouldEscalate };
}

async function handleAtendimentoIA(session: Session, message: IncomingMessage): Promise<void> {
  const userText = message.text?.body || '[收到的媒体]';
  const { text, shouldEscalate } = await getAIResponse(session, userText);

  await sendText(session.phone, text);

  if (shouldEscalate) {
    await escalateToHuman(session);
  }
}
```

### 机器人尝试次数限制

```typescript
const MAX_BOT_ATTEMPTS = 3;

async function handleWithFallback(session: Session, message: IncomingMessage): Promise<void> {
  session.data.botAttempts = (session.data.botAttempts || 0) + 1;

  if (session.data.botAttempts >= MAX_BOT_ATTEMPTS) {
    await sendText(session.phone,
      '看起来我无法有效帮助您。我将为您转接人工客服。'
    );
    await escalateToHuman(session);
    return;
  }

  await handleAtendimentoIA(session, message);
}
```

---

## 用于表单的 WhatsApp Flows

WhatsApp Flows 允许创建多屏交互式表单。预约流程示例：

### 发送 Flow

```typescript
async function sendAppointmentFlow(to: string, flowId: string): Promise<void> {
  await sendMessage({
    messaging_product: 'whatsapp',
    to,
    type: 'interactive',
    interactive: {
      type: 'flow',
      header: { type: 'text', text: 'Agendar Consulta' },
      body: { text: 'Preencha o formulário para agendar sua consulta.' },
      footer: { text: 'Seus dados estão protegidos' },
      action: {
        name: 'flow',
        parameters: {
          flow_message_version: '3',
          flow_id: flowId,
          flow_cta: 'Agendar agora',
          flow_action: 'navigate',
          flow_action_payload: {
            screen: 'APPOINTMENT_SCREEN',
            data: {
              available_dates: ['2026-03-01', '2026-03-02', '2026-03-03']
            }
          }
        }
      }
    }
  });
}
```

### 接收 Flow 回复

Flow 回复通过 webhook 以交互式消息形式到达：

```typescript
function handleFlowResponse(message: IncomingMessage): void {
  if (message.type === 'interactive' && message.interactive?.type === 'nfm_reply') {
    const flowResponse = JSON.parse(message.interactive.nfm_reply.response_json);
    // flowResponse 包含用户填写的数据
    console.log('Flow 数据：', flowResponse);
    // 例如：{ date: '2026-03-01', time: '14:00', name: 'João Silva' }
  }
}
```

有关 WhatsApp Flows 的更多详情，请阅读 `references/advanced-features.md`。

---

## 完整的端到端流程

### 主要 Webhook 处理程序

```typescript
app.post('/webhook', validateHMAC, async (req, res) => {
  // 立即返回 200 响应（要求：< 5 秒）
  res.sendStatus(200);

  try {
    const entry = req.body.entry?.[0];
    const changes = entry?.changes?.[0];
    const value = changes?.value;

    // 处理消息
    if (value?.messages) {
      for (const message of value.messages) {
        await processIncomingMessage(message);
      }
    }

    // 处理状态更新
    if (value?.statuses) {
      for (const status of value.statuses) {
        await processStatusUpdate(status);
      }
    }
  } catch (error) {
    console.error('处理 webhook 出错：', error);
    // 不返回错误 - 已响应 200
  }
});

async function processIncomingMessage(message: IncomingMessage): Promise<void> {
  const phone = message.from;
  const session = await getSession(phone);

  // 标记为已读
  await markAsRead(message.id);

  // 检查营业时间
  if (!isWithinBusinessHours() && session.state === ConversationState.INICIO) {
    await handleOffHours(phone);
    return;
  }

  // 检查升级触发器
  if (message.text?.body && shouldEscalate(message.text.body)) {
    await escalateToHuman(session);
    await saveSession(session);
    return;
  }

  // 如果是新对话，发送菜单
  if (session.state === ConversationState.INICIO) {
    session.state = ConversationState.MENU_PRINCIPAL;
    await sendMainMenuButtons(phone);
    await saveSession(session);
    return;
  }

  // 路由到正确的处理程序
  await routeMessage(session, message);
}
```

此流程可确保：
1. 立即返回 HTTP 200 响应（WhatsApp 要求）
2. HMAC 安全验证
3. 带状态的会话管理
4. 检查营业时间
5. 升级检测
6. 按会话状态路由
7. 自动标记为已读
