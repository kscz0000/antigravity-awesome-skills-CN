---
name: email-systems
description: 邮件是所有营销渠道中投资回报率最高的。每投入1美元可获得36美元回报。然而大多数初创公司却将其视为事后诸葛亮——群发轰炸、毫无个性化、最终落入垃圾邮件文件夹。
risk: none
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 邮件系统

邮件是所有营销渠道中投资回报率最高的。每投入1美元可获得36美元回报。然而大多数初创公司却将其视为事后诸葛亮——群发轰炸、毫无个性化、最终落入垃圾邮件文件夹。

本技能涵盖可正常工作的交易邮件、能转化的营销自动化、可送达收件箱的投递能力，以及可扩展的基础设施决策。

## 原则

- 交易邮件与营销邮件分离 | 描述：交易邮件（密码重置、收据）需要100%送达。营销邮件（通讯、促销）优先级较低。使用独立的IP地址和服务商来保护交易邮件的送达能力。 | 示例：好：密码重置通过Postmark发送，营销邮件通过ConvertKit发送 | 坏：所有邮件都通过同一个SendGrid账户发送
- 许可至上 | 描述：只给主动要求接收的人发邮件。营销邮件使用双重确认订阅。提供便捷退订。无情清理邮件列表。劣质列表会毁掉送达能力。 | 示例：好：已确认订阅 + 一键退订 | 坏：爬取的邮件列表、隐藏退订链接、购买的联系人
- 送达能力即基础设施 | 描述：SPF、DKIM、DMARC不是可选项。新IP需要预热。监控退信率。送达能力通过技术配置和良好行为赢得。 | 示例：好：所有DNS记录已配置，独立IP已预热4周 | 坏：使用免费层共享IP，无认证记录
- 一封邮件，一个目标 | 描述：每封邮件应该只有一个目的和一个CTA。多个请求意味着什么都不会被点击。清晰的单行动。 | 示例：好："点击此处验证您的邮箱"（一个按钮） | 坏："验证邮箱、查看我们的博客、在Twitter上关注我们、推荐好友..."
- 时机和频率很重要 | 描述：错误的时间 = 低打开率。太频繁 = 退订。让用户设置偏好。测试发送时间。尊重收件箱疲劳。 | 示例：好：周二上午10点用户时区的每周摘要，偏好中心 | 坏：随机时间的每日邮件，无法降低频率

## 模式

### 交易邮件队列

对所有交易邮件进行队列处理，包含重试逻辑和监控

**何时使用**：发送任何关键邮件（密码重置、收据、确认）

// 不要阻塞请求等待邮件发送
await queue.add('email', {
  template: 'password-reset',
  to: user.email,
  data: { resetToken, expiresAt }
}, {
  attempts: 3,
  backoff: { type: 'exponential', delay: 2000 }
});

### 邮件事件追踪

追踪送达、打开、点击、退信和投诉

**何时使用**：任何邮件营销活动或交易流程

# 追踪生命周期：
- Queued: 邮件进入系统
- Sent: 交给服务商
- Delivered: 到达收件箱
- Opened: 收件人查看
- Clicked: 收件人互动
- Bounced: 永久失败
- Complained: 标记为垃圾邮件

### 模板版本管理

对邮件模板进行版本管理，支持回滚和A/B测试

**何时使用**：更改生产环境邮件模板

templates/
  password-reset/
    v1.tsx (current)
    v2.tsx (testing 10%)
    v1-deprecated.tsx (archived)

# 逐步部署新版本
# 在全面推出前监控指标

### 退信处理状态机

自动处理退信以保护发件人声誉

**何时使用**：处理退信和投诉webhook

switch (bounceType) {
  case 'hard':
    await markEmailInvalid(email);
    break;
  case 'soft':
    await incrementBounceCount(email);
    if (count >= 3) await markEmailInvalid(email);
    break;
  case 'complaint':
    await unsubscribeImmediately(email);
    break;
}

### React邮件组件

使用可复用的React组件构建邮件

**何时使用**：创建邮件模板

import { Button, Html } from '@react-email/components';

export default function WelcomeEmail({ userName }) {
  return (
    <Html>
      <h1>Welcome {userName}!</h1>
      <Button href="https://app.com/start">
        Get Started
      </Button>
    </Html>
  );
}

### 偏好中心

让用户控制邮件频率和主题

**何时使用**：构建营销或通知系统

偏好设置：
☑ 产品更新（每周）
☑ 新功能（每月）
☐ 营销促销
☑ 账户通知（始终）

# 在所有发送中尊重偏好设置
# GDPR合规必需

## 易错点

### 缺少SPF、DKIM或DMARC记录

严重程度：严重

场景：发送未经认证的邮件。邮件进入垃圾邮件文件夹。打开率低。不知道原因。结果发现DNS记录从未配置。

症状：
- 邮件进入垃圾邮件
- 送达率低
- mail-tester.com评分低于8
- 未收到DMARC报告

为何会出问题：
邮件认证（SPF、DKIM、DMARC）告诉接收服务器你是合法的。没有它们，你看起来像垃圾邮件发送者。现代邮件服务商越来越要求三者齐全。

推荐修复：

# 必需的DNS记录：

## SPF (Sender Policy Framework)
TXT record: v=spf1 include:_spf.google.com include:sendgrid.net ~all

## DKIM (DomainKeys Identified Mail)
TXT record provided by your email provider
Adds cryptographic signature to emails

## DMARC (Domain-based Message Authentication)
TXT record: v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com

# 验证配置：
- 发送测试邮件到 mail-tester.com
- 使用MXToolbox检查记录验证
- 监控DMARC报告

### 交易邮件使用共享IP

严重程度：高

场景：密码重置进入垃圾邮件。使用邮件服务商的免费层。共享IP上的其他客户因垃圾邮件被标记。你的声誉因关联而受损。

症状：
- 交易邮件进入垃圾邮件
- 送达不一致
- 营销和交易使用同一服务商

为何会出问题：
共享IP共享声誉。一个不良行为者影响所有人。对于关键交易邮件，你需要自己的IP或有严格共享IP政策的服务商。

推荐修复：

# 交易邮件策略：

## 方案1：独立IP（高发送量）
- 从服务商获取独立IP
- 缓慢预热（从100封/天开始）
- 保持一致的发送量

## 方案2：仅交易邮件服务商
- Postmark（非常严格，声誉极佳）
- 包含高标准共享池

## 分离关注点：
- 交易邮件：Postmark或Resend
- 营销邮件：ConvertKit或Customer.io
- 永远不要混合营销和交易邮件

### 不处理退信通知

严重程度：高

场景：反复向相同的无效地址发送邮件。退信率攀升。邮件服务商威胁暂停账户。列表40%已失效。

症状：
- 退信率超过2%
- 无退信webhook处理器
- 相同邮件反复失败

为何会出问题：
退信损害发件人声誉。邮件服务商追踪退信率。超过2%你看起来就像垃圾邮件发送者。无效地址必须立即移除。

推荐修复：

# 退信处理要求：

## 硬退信：
首次发生立即移除
无效地址，域名不存在

## 软退信：
72小时内重试3次
3次失败后，视为硬退信

## 实现：
```typescript
// Webhook handler for bounces
app.post('/webhooks/email', (req, res) => {
  const event = req.body;
  if (event.type === 'bounce') {
    await markEmailInvalid(event.email);
    await removeFromAllLists(event.email);
  }
});
```

## 监控：
按营销活动追踪退信率
退信率超过1%时告警

### 缺少或隐藏退订链接

严重程度：严重

场景：用户因无法退订而标记为垃圾邮件。垃圾投诉上升。违反CAN-SPAM法规。邮件服务商暂停账户。

症状：
- 隐藏的退订链接
- 多步骤退订流程
- 无List-Unsubscribe头
- 高垃圾投诉率

为何会出问题：
无法退订的用户会标记为垃圾邮件。垃圾投诉比退订更损害声誉。而且这实际上是违法的。CAN-SPAM、GDPR都要求清晰的退订方式。

推荐修复：

# 退订要求：

## 可见性：
- 邮件页脚首屏位置
- 清晰文字，不隐藏
- 不设计成不可见

## 一键退订：
- 链接直接退订
- 无需登录
- 无"确定吗"障碍

## List-Unsubscribe头：
```
List-Unsubscribe: <mailto:unsubscribe@example.com>,
  <https://example.com/unsubscribe?token=xxx>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

## 偏好中心：
提供降低频率选项而非完全退订

### 发送HTML但无纯文本替代

严重程度：中

场景：部分用户看到空白邮件。垃圾邮件过滤器标记邮件。屏幕阅读器存在无障碍问题。剥离HTML的邮件客户端显示空白。

症状：
- 邮件中无text/plain部分
- 部分用户看到空白邮件
- 部分群体参与度较低

为何会出问题：
并非所有人都能渲染HTML。屏幕阅读器更适合纯文本。垃圾过滤器对仅HTML邮件存疑。多部分是标准。

推荐修复：

# 始终发送多部分：
```typescript
await resend.emails.send({
  from: 'you@example.com',
  to: 'user@example.com',
  subject: 'Welcome!',
  html: '<h1>Welcome!</h1><p>Thanks for signing up.</p>',
  text: 'Welcome!\n\nThanks for signing up.',
});
```

# 从HTML自动生成文本：
使用html-to-text库作为后备
但手工编写的纯文本更好

# 纯文本应可读：
不只是去除标签的HTML
实际格式化的文本内容

### 新IP立即发送大量邮件

严重程度：高

场景：刚切换服务商。立即开始每天发送50,000封邮件。严重送达问题。新IP无声誉。看起来像垃圾邮件。

症状：
- 新IP/服务商
- 立即发送大量邮件
- 送达率突然下降

为何会出问题：
新IP无声誉。立即发送大量邮件看起来像刚启动的垃圾邮件发送者。你需要逐步建立信任。

推荐修复：

# IP预热计划：

第1周：50-100封/天
第2周：200-500封/天
第3周：500-1000封/天
第4周：1000-5000封/天
继续翻倍直到达到目标量

# 最佳实践：
- 从最活跃的用户开始
- 先发送到Gmail/Microsoft（它们设定声誉）
- 保持一致的发送量
- 不要忽高忽低

# 预热期间：
- 密切监控送达率
- 检查反馈循环
- 出现问题调整节奏

### 向未订阅的人发送邮件

严重程度：严重

场景：购买了邮件列表。从LinkedIn爬取邮箱。添加会议联系人。垃圾投诉暴增。服务商暂停账户。可能面临诉讼。

症状：
- 购买的邮件列表
- 爬取的联系人
- 首次发送高退订率
- 垃圾投诉超过0.1%

为何会出问题：
许可式邮件不是可选项。这是法律要求（CAN-SPAM、GDPR）。它也有效——不情愿的收件人对你指标和声誉的伤害大于帮助。

推荐修复：

# 许可要求：

## 明确选择加入：
- 用户主动选择接收邮件
- 不是预勾选框
- 清楚他们订阅的是什么

## 双重确认：
- 带链接的确认邮件
- 确认后才加入列表
- 营销列表的最佳实践

## 不能做的事：
- 购买邮件列表
- 从网站爬取邮箱
- 未经同意添加会议联系人
- 未经同意使用合作伙伴/客户列表

## 交易邮件例外：
密码重置、收据、账户提醒
不需要营销订阅许可

### 邮件大部分或全部是图片

严重程度：中

场景：设计精美的邮件是一张大图。屏蔽图片的用户什么都看不到。垃圾过滤器标记它。移动端加载缓慢。没人能复制文字。

症状：
- 单图片邮件
- 无可见文本内容
- 缺少或通用alt文本
- 屏蔽图片时参与度低

为何会出问题：
许多客户端默认屏蔽图片。垃圾过滤器对纯图片邮件存疑。无障碍性受损。加载时间增加。

推荐修复：

# 平衡图片和文本：

## 60/40规则：
- 至少60%文本内容
- 图片用于增强，非内容

## 始终包含：
- 每张图片的alt文本
- 关键信息用文字，不只是图片
- 关闭图片视图的后备方案

## 测试：
- 预览时禁用图片
- 应该仍然可用

# 示例：
```html
<img
  src="hero.jpg"
  alt="本周节省50% - 使用代码 SAVE50"
  style="max-width: 100%"
/>
<p>使用代码 <strong>SAVE50</strong> 本周节省50%。</p>
```

### 缺少或默认预览文本

严重程度：中

场景：收件箱显示"在浏览器中查看此邮件"或随机HTML作为预览。打开率降低。第一印象浪费在样板文字上。

症状：
- 预览显示"在浏览器中查看"
- HTML代码在预览中可见
- 模板中无预览组件

为何会出问题：
预览文本是黄金地段——紧跟主题行之后显示。默认或缺少预览文本浪费了这个空间。好的预览文本可提高10-30%打开率。

推荐修复：

# 添加明确的预览文本：

## 在HTML中：
```html
<div style="display:none;max-height:0;overflow:hidden;">
  您的预览文本。这会显示在收件箱预览中。
  <!-- 添加空白字符将页脚文本推出 -->
  &nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;
</div>
```

## 使用React Email：
```tsx
<Preview>
  您的预览文本。这会显示在收件箱预览中。
</Preview>
```

## 最佳实践：
- 补充主题行
- 40-100个字符最佳
- 制造好奇心或价值
- 与邮件第一行不同

### 不处理部分发送失败

严重程度：高

场景：向10,000用户发送。API在3,000处失败。无发送记录。要么重复发送，要么丢失7,000。无法知道谁收到了邮件。

症状：
- 无每个收件人的发送日志
- 无法判断谁收到了邮件
- 重复发送问题
- 无重试机制

为何会出问题：
批量发送会部分失败。API超时。触发速率限制。不追踪单个发送状态，无法优雅恢复。

推荐修复：

# 单独追踪每次发送：

```typescript
async function sendCampaign(emails: string[]) {
  const results = await Promise.allSettled(
    emails.map(async (email) => {
      try {
        const result = await resend.emails.send({ to: email, ... });
        await db.emailLog.create({
          email,
          status: 'sent',
          messageId: result.id,
        });
        return result;
      } catch (error) {
        await db.emailLog.create({
          email,
          status: 'failed',
          error: error.message,
        });
        throw error;
      }
    })
  );

  const failed = results.filter(r => r.status === 'rejected');
  // 重试失败的发送或告警
}
```

# 最佳实践：
- 记录每次发送尝试
- 包含消息ID用于追踪
- 为失败构建重试队列
- 监控每个营销活动的成功率

## 验证检查

### 缺少纯文本邮件部分

严重程度：警告

邮件应始终包含纯文本替代

消息：正在发送HTML邮件但无纯文本部分。添加'text:'属性以提高无障碍性和送达能力。

### 硬编码发件人地址

严重程度：警告

发件人地址应来自环境变量

消息：发件人邮件似乎是硬编码的。使用环境变量以获得灵活性。

### 缺少退信webhook处理器

严重程度：警告

应处理邮件退信以维护列表卫生

消息：检测到使用邮件服务商但无退信处理。实现退信webhook处理器。

### 缺少List-Unsubscribe头

严重程度：信息

营销邮件应包含List-Unsubscribe头

消息：检测到营销邮件无List-Unsubscribe头。添加头以提高送达能力。

### 请求处理器中同步发送邮件

严重程度：警告

邮件发送应排队，不应阻塞

消息：在请求处理器中同步发送邮件。考虑排队以提高可靠性。

### 邮件发送无重试逻辑

严重程度：信息

邮件发送应有失败重试机制

消息：邮件发送无明显重试逻辑。添加重试以处理临时故障。

### 代码中的邮件API密钥

严重程度：错误

API密钥应来自环境变量

消息：邮件API密钥似乎在源代码中硬编码。使用环境变量。

### 批量邮件无速率限制

严重程度：警告

批量发送应遵守服务商速率限制

消息：批量邮件发送无明显速率限制。添加节流以避免触及限制。

### 邮件无预览文本

严重程度：信息

邮件应包含预览/前言文本

消息：邮件模板无预览文本。添加隐藏前言用于收件箱预览。

### 邮件发送无日志

严重程度：警告

邮件发送应记录日志用于调试和审计

消息：正在发送邮件但无明显日志记录。记录发送用于调试和合规。

## 协作

### 委派触发器

- copy|subject|messaging|content -> copywriting（邮件需要文案）
- design|template|visual|layout -> ui-design（邮件需要设计）
- track|analytics|measure|metrics -> analytics-architecture（邮件需要追踪）
- infrastructure|deploy|server|queue -> devops（邮件需要基础设施）

### 邮件营销技术栈

技能：email-systems, copywriting, marketing, analytics-architecture

工作流：

```
1. 基础设施设置 (email-systems)
2. 模板创建 (email-systems)
3. 文案撰写 (copywriting)
4. 营销活动启动 (marketing)
5. 效果追踪 (analytics-architecture)
```

### 交易邮件

技能：email-systems, backend, devops

工作流：

```
1. 服务商设置 (email-systems)
2. 模板编码 (email-systems)
3. 队列集成 (backend)
4. 监控 (devops)
```

## 何时使用
当请求明显匹配上述能力和模式时使用此技能。

## 局限性
- 仅当任务明显匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
