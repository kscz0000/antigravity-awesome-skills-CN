# 合规与最佳实践 - WhatsApp Cloud API

WhatsApp Business 集成的完整合规指南，涵盖 LGPD、GDPR、WhatsApp 政策、选择加入/退出、质量评级和 Tier 体系。

---

## 目录

1. [LGPD - 巴西](#lgpd---brasil)
2. [GDPR - 欧盟](#gdpr---uniao-europeia)
3. [WhatsApp 政策](#politicas-do-whatsapp)
4. [选择加入与退出](#opt-in-e-opt-out)
5. [质量评级仪表板](#quality-rating-dashboard)
6. [Tier 体系 - 消息限制](#tier-system---limites-de-mensagem)
7. [数据保留与删除](#retencao-e-exclusao-de-dados)
8. [上线前合规检查清单](#checklist-de-compliance-pre-lancamento)

---

## LGPD - 巴西

《通用数据保护法》（第 13.709/2018 号法律）适用于在巴西进行的任何个人数据处理。

### WhatsApp 消息的法律依据

| 法律依据            | 使用场景                                    | 示例                            |
|--------------------|--------------------------------------------|--------------------------------|
| 同意                | 营销、促销、新闻通讯                        | 黑色星期五营销活动             |
| 合同履行            | 订单、交付、付款通知                        | 购买确认                       |
| 合法利益            | 客户服务、支持                              | 客户问题回复                   |
| 法律义务            | 监管通知                                    | 产品召回通知                   |

### 数据主体权利（LGPD 第 18 条）

您的集成必须支持：

1. **处理确认** - 告知正在处理哪些数据
2. **数据访问** - 提供所存储数据的副本
3. **更正** - 允许更新不正确的数据
4. **匿名化/删除** - 应要求删除数据
5. **可移植性** - 以可读格式导出数据
6. **撤销同意** - 随时选择退出

### 技术实现

```typescript
// 记录包含完整详细信息的同意
interface ConsentRecord {
  phone: string;
  consentType: 'marketing' | 'transactional' | 'support';
  method: 'whatsapp_optin' | 'website_form' | 'sms' | 'verbal';
  timestamp: Date;
  ipAddress?: string;
  message?: string; // 同意的原文
  legalBasis: 'consent' | 'contract' | 'legitimate_interest';
}

async function recordConsent(record: ConsentRecord): Promise<void> {
  await db.consents.create({
    ...record,
    timestamp: new Date(),
    active: true
  });
}

// 撤销同意
async function revokeConsent(phone: string, type: string): Promise<void> {
  await db.consents.update(
    { phone, consentType: type },
    { active: false, revokedAt: new Date() }
  );
}
```

---

## GDPR - 欧盟

如果您服务欧盟客户，则适用 GDPR（2016/679 号条例）。

### 特定要求

1. **双重选择加入（Double Opt-in）**
   - 第一次选择加入：客户提供号码（网站、表单、QR 码）
   - 第二次选择加入：通过 WhatsApp 发送确认消息
   - 客户通过关键字（例如 "SIM"）回复以确认

2. **欧盟认证 BSP**
   - 仅使用位于欧盟的 Business Solution Providers
   - Meta 的 WhatsApp Cloud API 托管在美国 — 请确认是否适合您的使用场景

3. **DPA（数据处理协议）**
   - 与 Meta 签订有关数据处理的正式合同
   - 可在 Meta Business Settings 中找到

4. **向用户提供明确信息**
   - 选择加入前，告知：哪些数据、用于什么目的、保留多长时间
   - 提供隐私政策的链接

### 双重选择加入的实现

```python
async def handle_optin_flow(phone: str, stage: str) -> None:
    if stage == "initial":
        # 首次联系 - 发送确认模板
        await send_template(
            to=phone,
            template_name="optin_confirmation",
            language="pt_BR",
            components=[{
                "type": "body",
                "parameters": [{"type": "text", "text": "mensagens promocionais"}]
            }]
        )
        await save_optin_stage(phone, "awaiting_confirmation")

    elif stage == "awaiting_confirmation":
        # 客户已回复 - 验证关键字
        # (由 webhook handler 调用)
        pass

async def process_optin_response(phone: str, message: str) -> None:
    keyword = message.strip().upper()
    if keyword in ["SIM", "YES", "ACEITO", "CONFIRMO"]:
        await record_consent(ConsentRecord(
            phone=phone,
            consent_type="marketing",
            method="whatsapp_double_optin",
            timestamp=datetime.now(),
            message=f"Usuario respondeu: {message}"
        ))
        await send_text(phone, "Obrigado! Voce foi inscrito com sucesso. Envie SAIR a qualquer momento para cancelar.")
    else:
        await send_text(phone, "Opt-in nao confirmado. Voce nao recebera mensagens promocionais.")
```

---

## WhatsApp 政策

### 禁止内容

WhatsApp 禁止包含以下内容的消息：
- 非法产品（毒品、武器、伪造文件）
- 露骨成人内容
- 未受监管的赌博
- 传销或欺诈
- 煽动暴力或仇恨的内容
- 出售个人数据
- 无处方的管制药品

### 频率规则

- 同一用户每周不超过 1 条营销消息
- 尊重用户的频率偏好
- 交易消息可更频繁（根据需要）
- 切勿在无细分的情况下群发消息

### 垃圾消息信号

WhatsApp 监控以下信号以检测垃圾消息：
- 用户屏蔽率高
- 向从未互动的号码批量发送
- 向许多收件人发送相同消息
- 回复率/互动率低
- 用户举报垃圾消息

---

## 选择加入与退出

### 有效的选择加入方法

1. **网站/登录页** - 带有明确复选框的表单
2. **QR 码** - 启动对话的 wa.me 链接
3. **短信** - 向短号发送关键字
4. **面对面** - 记录口头同意
5. **WhatsApp** - 通过消息进行双重选择加入

### 选择退出实现

```typescript
const OPTOUT_KEYWORDS = ['sair', 'stop', 'cancelar', 'parar', 'descadastrar', 'unsubscribe'];

function isOptOutRequest(message: string): boolean {
  return OPTOUT_KEYWORDS.includes(message.trim().toLowerCase());
}

async function handleOptOut(phone: string): Promise<void> {
  // 1. 撤销同意
  await revokeConsent(phone, 'marketing');

  // 2. 向用户确认
  await sendText(phone,
    'Voce foi descadastrado com sucesso e nao recebera mais mensagens promocionais. ' +
    'Mensagens transacionais (pedidos, entregas) continuarao sendo enviadas conforme necessario. ' +
    'Para se inscrever novamente, envie ATIVAR.'
  );

  // 3. 记录事件
  await logEvent('optout', { phone, timestamp: new Date() });
}
```

### 证明记录

对于每次选择加入，请记录：
- 用户的**电话**
- 精确的**时间戳**（含时区）
- 使用的**方法**（网站、QR、短信、WhatsApp）
- 展示的同意**原文**
- **IP**（如果通过 Web）
- 特定的**用途**（营销、交易、支持）

---

## 质量评级仪表板

### 如何访问

WhatsApp Manager → Overview → Insights tab

### 颜色系统

| 颜色      | 含义                              | 影响                                       |
|-----------|-----------------------------------|--------------------------------------------|
| 绿色      | 高质量                            | 有资格升级 Tier                            |
| 黄色      | 质量中等，需要关注                | 不会失去 Tier，但无法升级                  |
| 红色      | 质量低                            | 有限制风险，无法升级 Tier                  |

### 监控的信号（最近 7 天）

**积极信号：**
- 客户回复率高
- 与按钮/列表的互动
- 对话较长（多条消息）
- 屏蔽率低

**消极信号：**
- 频繁被屏蔽
- 垃圾消息举报
- 互动率低
- 未读消息

### 按评级的措施

**绿色：** 保持现状。专注于保持质量。

**黄色：**
- 审查营销消息内容
- 降低发送频率
- 改进细分（仅发送给感兴趣的人）
- 验证选择退出是否正常工作

**红色：**
- 立即停止发送营销消息
- 审查所有联系人列表（删除非活跃用户）
- 检查是否存在技术问题（重复消息）
- 在恢复前仅发送交易消息

---

## Tier 体系 - 消息限制

### Tier 结构（2025 年 10 月更新）

自 2025 年 10 月起，限制按 **Business Portfolio** 计算，而非按单个号码。

| 等级         | 每 24 小时对话数 | 吞吐量          |
|--------------|-------------------|-----------------|
| 初始         | 250               | 80 msg/s        |
| Tier 1       | 1,000             | 80 msg/s        |
| Tier 2       | 10,000            | 80 msg/s        |
| Tier 3       | 100,000           | 80 msg/s        |
| 无限         | 无限制            | 1,000 msg/s     |

### 自动升级

WhatsApp 在以下情况下执行自动升级：
1. 质量评级为绿色或黄色
2. 您在连续 7 天内发送的消息达到当前限额的 50%+
3. 升级时间：6 小时（之前为 24 小时）

**示例：** 如果您的限额是 1,000，则需在 7 天内向 500+ 独立客户发送消息才能升级到 10,000。

### 2026 年变化

- **2026 年 Q1：** 部分合作伙伴将移除 2K 和 10K Tier
- **2026 年 Q2：** 完全移除 — 企业验证后，立即获得 100K 限额
- **Business Portfolio Pacing：** 用于批量营销活动的新功能，可根据反馈自动暂停

### 重要规则

一旦您达到某个 Tier，即使质量下降也**不会失去**。评级仅影响您升级到更高 Tier 的能力。

如果 Business Portfolio 中的某个号码已处于 Unlimited 状态，则**所有**新添加的号码都将以 Unlimited 状态开始。

---

## 数据保留与删除

### 推荐策略

| 数据类型            | 推荐保留期          | 理由                          |
|--------------------|---------------------|------------------------------|
| 对话消息           | 90 天               | 支持和审计                    |
| 同意数据           | 活跃期间 + 5 年     | 法律证明                      |
| 退出数据           | 5 年                | 避免重新发送 + 证明            |
| Webhook 日志       | 30 天               | 调试和监控                    |
| 聚合指标           | 2 年                | 分析和改进                    |

### 自动删除

```typescript
// 每日清理旧数据的定时任务
async function cleanupOldData(): Promise<void> {
  const now = new Date();

  // 删除超过 90 天的消息
  await db.messages.deleteMany({
    createdAt: { $lt: new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000) }
  });

  // 删除超过 30 天的日志
  await db.webhookLogs.deleteMany({
    createdAt: { $lt: new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000) }
  });

  // 删除过期的会话
  await db.sessions.deleteMany({
    lastActivity: { $lt: new Date(now.getTime() - 24 * 60 * 60 * 1000) }
  });
}
```

### 处理数据删除请求（LGPD/GDPR）

```typescript
async function handleDataDeletionRequest(phone: string): Promise<void> {
  // 1. 匿名化消息（保留用于分析，移除个人身份信息）
  await db.messages.updateMany(
    { phone },
    { $set: { phone: 'ANONIMIZADO', content: '[REMOVIDO]' } }
  );

  // 2. 删除个人数据
  await db.customers.deleteOne({ phone });
  await db.sessions.deleteOne({ phone });

  // 3. 保留退出记录（避免再次发送）
  await db.optouts.create({ phone, deletedAt: new Date() });

  // 4. 向用户确认
  await sendText(phone,
    'Seus dados pessoais foram removidos conforme solicitado. ' +
    'Seu número será mantido apenas em nossa lista de exclusão para garantir que não enviaremos mais mensagens.'
  );

  // 5. 审计日志
  await logEvent('data_deletion', { phone, timestamp: new Date() });
}
```

---

## 上线前合规检查清单

在将集成投入生产前，请使用此检查清单：

### 同意
- [ ] 选择加入机制已实现并经过测试
- [ ] 欧盟/GDPR 适用时采用双重选择加入
- [ ] 同意书记录包含时间戳、方式和用途
- [ ] 针对每种类型（营销、交易）的具体同意

### 退出
- [ ] 识别退出关键字（SAIR、STOP、CANCELAR 等）
- [ ] 退出后发送确认
- [ ] 退出实时处理（不在第二天）
- [ ] 退出后立即更新数据库

### 数据
- [ ] 已定义并实施保留策略
- [ ] 自动删除例程正常运行
- [ ] 处理数据删除请求的流程（LGPD 第 18 条）
- [ ] 数据安全存储（静态加密）

### WhatsApp
- [ ] 模板在首次发送前已获批准
- [ ] 已完成企业验证（用于提高限额）
- [ ] 每周监控质量评级
- [ ] 内容符合 WhatsApp 政策
- [ ] 营销频率适当（每周最多 1 次）

### 安全
- [ ] Webhook 上实施 HMAC-SHA256 验证（必需）
- [ ] 令牌存储在环境变量中（绝不在代码中）
- [ ] 使用有效 SSL 证书的 HTTPS
- [ ] 访问控制：仅授权人员可访问数据

### 文档
- [ ] 隐私政策已更新，提到了 WhatsApp
- [ ] 使用条款包含 WhatsApp 渠道的使用
- [ ] 已与 Meta 签订 DPA（GDPR 适用）
