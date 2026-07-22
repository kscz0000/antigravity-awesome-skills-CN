---
name: auri-core
description: "Auri：智能语音助手（Alexa + Claude claude-opus-4-20250805）。产品愿景、Vitoria Neural 人设、AWS 技术栈、Free/Pro/Business/Enterprise 定价模式、4 阶段路线图、GTM 策略、WAC 北极星指标及竞争分析。触发词：Auri、语音助手、Alexa Skill、智能音箱、Claude 语音、巴西葡萄牙语助手、Echo 技能开发。"
risk: none
source: community
date_added: '2026-03-06'
author: renat
tags:
- voice-assistant
- product-vision
- alexa
- aws
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# Auri - 核心产品技能

## 概述

Auri：智能语音助手（Alexa + Claude claude-opus-4-20250805）。产品愿景、Vitoria Neural 人设、AWS 技术栈、Free/Pro/Business/Enterprise 定价模式、4 阶段路线图、GTM 策略、WAC 北极星指标及竞争分析。

## 何时使用此技能

- 当你需要此领域的专业协助时

## 何时不使用此技能

- 任务与 auri-core 无关时
- 更简单、更具体的工具可以处理请求时
- 用户需要无领域专业知识的通用协助时

## 工作原理

| 属性 | 定义 |
|------|------|
| 名称 | Auri |
| 语音 | Amazon Polly Vitoria Neural pt-BR |
| 语调 | 温暖、智能、直接 |
| 个性 | 好奇、共情、可靠 |
| 语言 | 自然巴西葡萄牙语 |
| 态度 | 主动但不冒犯 |

## Auri - 核心产品技能

> 与你共同思考的声音。

Auri 是构建在 Amazon Alexa + Claude claude-opus-4-20250805 之上的新一代语音助手。
传统 Alexa 执行命令，而 Auri 进行真实对话并基于上下文推理。

---

## Auri 是什么

Auri 是一款高级 Alexa Skill，用 Anthropic 的 Claude claude-opus-4-20250805 模型替代默认响应引擎。结果：一个能够：

- 进行带上下文记忆的多轮对话
- 用自然语言推理复杂问题
- 根据用户画像调整语气和深度
- 100% 使用巴西葡萄牙语，融入文化细微差别
- 集成 Amazon 生态系统（日历、购物、智能家居、音乐）

## 独特价值主张

之前：Alexa，明天天气如何？-> 明天，28 度，多云。

之后：Auri，我明天该带伞吗？
  -> 明天下午 70% 会下雨，但上午天气晴朗。14 点有会议？带上雨伞。

## 战略差异化

1. 对话连续性 - 通过 DynamoDB 在会话间记忆上下文
2. 一致的人设 - Vitoria Neural 语音 + 精心调校的 persona
3. 深度推理 - Claude claude-opus-4-20250805 作为核心引擎
4. 集成生态系统 - Alexa 硬件原生支持（Echo、Echo Dot、Echo Show）
5. 隐私优先设计 - 数据存储在 AWS，不与第三方共享

---

## 品牌价值观

- 清晰 - 直接回答，不绕圈子
- 共情 - 理解情感上下文，调整语气
- 智能 - 从不假装知道不知道的事
- 尊重 - 维护隐私，从不评判
- 连续性 - 记住对话，与用户共同成长

## 语言指南

应该做：
- 使用第一人称
- 回答前确认理解
- 承认不确定并提供替代方案

避免：
- 机器人式回答
- 过度正式
- 无替代方案的回避

## 交互示例

用户：Auri，用简单的方式给我解释加密货币。

Auri：这样想：想象你和朋友创造了自己的货币，用于彼此支付，中间没有银行。加密货币就是这样，但面向数百万人。比特币是第一个，2009 年创造。想了解更多吗？

## SSML - 优化语音

Amazon Polly Vitoria Neural 的 SSML 标记示例：
  <voice name=Vitoria><prosody rate=medium pitch=+2%>Ola! Eu sou a Auri.</prosody>
  <break time=300ms/><prosody>Como posso te ajudar hoje?</prosody></voice>

---

## 架构概览

数据流：Echo -> ASK SDK (Python v2) -> Lambda Python 3.12 -> Claude claude-opus-4-20250805
AWS 组件：DynamoDB（记忆）、Polly Vitoria Neural（语音）、CloudWatch（日志）、Secrets Manager（密钥）

## 3.1 依赖项

ask-sdk-core==1.19.0 | ask-sdk-model==1.85.0 | boto3==1.34.0 | anthropic==0.25.0 | python-dotenv==1.0.0

## 3.2 主 Lambda Handler

Python 代码 - lambda_function.py：
  sb = CustomSkillBuilder()
  sb.add_request_handler(ConversationIntentHandler())
  sb.add_global_request_interceptor(MemoryLoadInterceptor())
  sb.add_global_response_interceptor(MemorySaveInterceptor())
  lambda_handler = sb.lambda_handler()

## 3.3 Claude 对话 Handler

Python 代码 - handlers/conversation.py：
  class ConversationIntentHandler(AbstractRequestHandler):
      通过 slot query 接收 user_speech
      从 DynamoDB 会话加载对话历史
      调用 anthropic.Anthropic().messages.create(
          model=claude-opus-4-20250805, max_tokens=300,
          system=system_prompt, messages=history+[user_speech])
      保存回答到历史，返回带 Vitoria 语音的 SSML

## 3.4 DynamoDB Schema

表：auri-user-memory | PK: user_id | SK: session_date | TTL: 90 天
字段：profile（name、plan、preferences）、long_term_memory[]、usage_stats{}
BillingMode: PAY_PER_REQUEST | TimeToLive: 已启用（自动过期）

## 3.5 交互模型

invocationName: auri
ConversationIntent: slot query (AMAZON.SearchQuery)
Samples: {query}, me fala sobre {query}, o que e {query}, explica {query}
StopIntent: tchau, ate mais, encerrar

## 3.6 Lambda 配置

FunctionName: auri-core-handler | Runtime: python3.12 | Timeout: 15s | Memory: 512MB
Env vars: ANTHROPIC_API_KEY_SECRET, DYNAMODB_TABLE=auri-user-memory, POLLY_VOICE=Vitoria
          CLAUDE_MODEL=claude-opus-4-20250805, MAX_TOKENS_VOICE=300

---

## 3.7 完整代码示例

对话 Handler（handlers/conversation.py）：

DynamoDB Schema：

---

## 计划与定价

| 计划 | 价格 | 限制 | 目标用户 |
|------|------|------|----------|
| Free | R$ 0 | 10 个问题/天 | 体验尝鲜 |
| Pro | R$ 29/月 | 无限制，90 天记忆 | 个人用户 |
| Business | R$ 99/月 | 最多 5 用户，1 年记忆 | 家庭/中小企业 |
| Enterprise | 定制 | 无限制，SLA 保障 | 企业客户 |

## 详细说明

Free：10 个问题/天，会话间无记忆，Vitoria Neural 语音。
Pro：无限对话，90 天记忆，个性化档案，邮件支持。
Business：Pro 全部功能 + 最多 5 用户，共享记忆，仪表盘，报告。
Enterprise：无限制，可定制人设，CRM/ERP 集成，99.9% SLA。

## 收入预测（第 1 年）

保守目标：Pro 250 × R$ 29 = R$ 7.250/月 | Business 25 × R$ 99 = R$ 2.475/月
MRR 第 1 年：R$ 9.725/月（约 R$ 117k ARR）

乐观目标：Pro 800 = R$ 23.200/月 | Business 80 = R$ 7.920/月
MRR 第 1 年：R$ 31.120/月（约 R$ 373k ARR）

## 单位经济效益

| 指标 | Pro | Business |
|------|-----|----------|
| CAC | R$ 45 | R$ 120 |
| LTV | R$ 522（18 个月）| R$ 2.376（24 个月）|
| LTV/CAC | 11.6x | 19.8x |
| 流失率 | 5%/月 | 3%/月 |
| 毛利率 | ~86% | ~90% |

---

## 阶段 1 - MVP 发布（第 1-3 个月）

目标：与巴西早期采用者验证产品市场契合度。

| 交付物 | 描述 | 状态 |
|--------|------|------|
| 核心 Handler | Lambda + ASK SDK + Claude | 开发中 |
| Vitoria 人设 | SSML 优化，Polly Neural | 开发中 |
| Free 计划 | 10 个问题/天速率限制 | 已规划 |
| DynamoDB 会话 | 会话内记忆 | 已规划 |
| Alexa Store | 发布到 Alexa Skills Store BR | 已规划 |
| 落地页 | auri.com.br 含 CTA | 已规划 |

阶段 1 KPI：500 次启用，40% 第 2 周留存，NPS > 50，延迟 < 2 秒。

## 阶段 2 - 个性化（第 4-6 个月）

| 交付物 | 描述 |
|--------|------|
| 长期记忆 | DynamoDB 持久化 90 天（Pro）|
| 用户画像 | 姓名、偏好、上下文 |
| Pro 计划发布 | 通过 Amazon In-Skill Purchasing |
| 分析仪表盘 | Pro 用户查看使用模式 |

阶段 2 KPI：200 次 Free->Pro 转化，WAC > 150，会话时长 > 4 分钟，流失率 < 7%。

## 阶段 3 - 多模态（第 7-12 个月）

| 交付物 | 描述 |
|--------|------|
| Echo Show 支持 | 显示屏视觉响应 |
| 日历集成 | 语音管理日程 |
| Auri Web App | 历史记录网页界面 |
| Business 计划发布 | 多用户，家庭仪表盘 |

阶段 3 KPI：WAC > 1.000，MRR > R$ 15.000，Business：50 客户，评分 > 4.5。

## 阶段 4 - 生态系统（第 2 年+）

| 交付物 | 描述 |
|--------|------|
| Auri SDK | 开发者构建 Auri 技能 |
| WhatsApp 桥接 | WhatsApp 上的 Auri 人设 |
| 移动应用 | iOS/Android 语音应用 |
| 应用市场 | 第三方技能 |
| Enterprise 发布 | SSO 和合规 |
| B2B 技能 | Auri 健康、教育、金融 |

---

## 目标细分市场

**主要：精通科技的巴西人（25-45 岁）**
- 已拥有 Echo（巴西约 200 万），对标准 Alexa 不满。
- 渠道：Reddit、Twitter/X 科技、YouTube 科技巴西。

**次要：有 Echo 的家庭**
- 儿童教育助手，家庭日历。
- 渠道：Facebook 群组、Instagram 育儿。

**第三：中小企业和专业人士**
- 律师、医生、顾问，需要快速研究。
- 渠道：LinkedIn、商业活动。

## 获客渠道

| 渠道 | 成本 | 潜力 | 周期 |
|------|------|------|------|
| Alexa Store 自然流量 | R$ 0 | 高 | 即时 |
| SEO + 博客 | 低 | 高 | 3-6 个月 |
| YouTube 演示 | 中 | 高 | 1-3 个月 |
| 巴西科技影响者 | 中 | 高 | 1-2 个月 |
| 付费广告 | 高 | 高 | 可测试 |

## 核心信息

标语：与你共同思考的声音。

电梯演讲：你对 Alexa 的机械回答感到沮丧过吗？
Auri 内置真正的智能。她记得你的对话，
理解上下文，像一个聪明人一样回答。免费开始。

价值主张：
- 给好奇者：真正理解葡萄牙语的语音 AI
- 给高效者：与你共同进化的个人助手
- 给家庭：家中每个人的智能存在
- 给专业人士：几秒内完成研究，双手不离键盘

## 发布日历

D-30：等待名单（auri.com.br）| D-15：50 用户内测 | D-0：Alexa Store
D+14：影响者推广 | D+60：Pro 发布 | D+90：阶段 1 评估

---

## WAC - 周活跃对话者

**精确定义：**
上周内进行 >= 3 次会话且每次 >= 2 分钟的唯一用户数。
周期：周一至周日，00:00-23:59 BRT。

**为什么用 WAC 而非 DAU/MAU：**
- DAU 用 10 秒访问淡化参与度。
- MAU 周期太长，产品反馈慢。
- WAC 捕捉真实习惯：回来 3 次且停留 2 分钟 = 真正参与。
- 与 30 天留存和 Free->Pro 转化相关。

## 指标层级

北极星：WAC
|
+-- 获取：启用量、首次会话完成率、次日留存
+-- 激活：每周会话/用户、平均时长、问题/会话
+-- 留存：第 2 周、第 1 月、Pro 流失率
+-- 收入：转化率、MRR、ARPU、LTV/CAC
+-- 推荐：NPS、自然分享、应用商店评分

## 各阶段 WAC 目标

| 阶段 | 月份 | WAC 目标 | WAC 挑战目标 |
|------|------|----------|--------------|
| 阶段 1 | M3 | 150 | 300 |
| 阶段 2 | M6 | 500 | 1.000 |
| 阶段 3 | M12 | 2.000 | 5.000 |
| 阶段 4 | M24 | 10.000 | 25.000 |

## 如何计算 WAC

1. 在 DynamoDB 中用 user_id 和时间戳记录 session_start。
2. 会话结束时，记录持续秒数。
3. 每周查询：session_count >= 3 且 avg_duration >= 120 的用户。
4. 发布指标到 CloudWatch namespace Auri/ProductMetrics。
5. 周环比下降 > 20% 时告警。

## CloudWatch 仪表盘（示例结构）

发布自定义指标：
- SessionStart（按计划计数：free/pro/business）
- SessionDuration（None - 分钟）
- MessagesPerSession（计数）
- WAC 周数据（仪表）
- FreeToProConversions（计数）

---

## 对比表

| 功能 | Auri | 纯 Alexa | Siri | Google Assistant | ChatGPT Voice |
|------|------|----------|------|------------------|---------------|
| 原生 PT-BR | 高 | 中 | 中 | 高 | 中 |
| 深度推理 | 高 | 低 | 中 | 中 | 高 |
| 多会话记忆 | 高 | 低 | 中 | 中 | 高 |
| 智能家居集成 | 高 | 最高 | 中 | 高 | 低 |
| 一致人设 | 高 | 中 | 中 | 中 | 高 |
| 专属硬件 | 使用 Echo | Echo | HomePod | Nest | 仅应用 |
| 基础模型 | Claude Opus 4 | Alexa LLM | Apple LLM | Gemini | GPT-4o |
| 隐私 | 高 | 中 | 最高 | 低 | 中 |
| 价格 | R$ 0-99/月 | 免费 | 免费 | 免费 | R$ /月 |
| 巴西可用 | 是 | 是 | 是 | 是 | 是 |

## 竞争格局定位

X 轴：硬件集成度 | Y 轴：智能深度

Auri 的独特象限：高智能 + 高硬件集成。
无竞争对手同时占据此象限：
- 纯 Alexa：高集成，低智能。
- ChatGPT Voice：高智能，无专属硬件。
- Google/Siri：两轴均为中等定位。

## 常见异议与回答

| 异议 | Auri 回答 |
|------|-----------|
| 为什么不用 ChatGPT？| ChatGPT 是应用，非语音优先。Auri 在 Echo 上原生运行。|
| Alexa 已经够用了 | 对于命令确实如此。对于真实对话，不够。|
| R$ 29 太贵了 | 不到每天 1 杯咖啡的价格，换取 24/7 个人助手。|
| 隐私如何？| 数据在你的 AWS，可配置保留期，符合 LGPD。|
| 亚马逊会抄袭吗？| 亚马逊鼓励技能生态系统。我们是合作伙伴。|

---

## 品牌识别

- 名称：Auri
- 来源：Aura（无形存在）+ IA。暗示存在、智慧、轻盈。
- 标语：与你共同思考的声音。

## 备选标语

- 超越命令。远超命令。
- 住在你 Echo 里的 AI。
- 真实对话。真实智能。
- 与真正倾听者对话。

## 品牌价值观

1. 真实智能 - 从不模拟。不知道时诚实承认。
2. 温暖存在 - 先进技术配人性化温度。
3. 尊重时间 - 直接回答，不绕圈子。
4. 持续成长 - 与用户共同进化，从交互中学习。
5. 隐私即权利 - 用户数据属于用户。

## 品牌语音指南

语调：
- 温暖但不矫情。
- 智能但不迂腐。
- 直接但不粗鲁。
- 有趣但不轻浮。

绝不：机械、企业腔、回避、居高临下、急于讨好。

正确示例：我不知道确切答案，但我可以用其他方式帮你找到。
错误示例：抱歉，我的数据库中没有此信息。

## 品牌应用

- 应用图标：绿蓝渐变中的风格化语音波形。
- 色彩：青绿主色、中性白、深灰文字。
- 字体：现代无衬线（类似 Apple/Spotify 产品）。
- 动效：说话时的柔和波浪动画（Echo Show）。

---

## 10. 技能命令

这些命令在技能使用上下文中被提及时激活特定模式。

## /Auri-Status

显示当前状态：版本、WAC vs 目标、MRR、下个交付物、组件状态。

返回字段：
- 产品当前版本（如 v1.0.0）
- 当前 WAC vs 当前阶段目标
- 当前 MRR（R$）
- 路线图下个交付物
- 状态：Lambda（OK/降级）、DynamoDB（OK）、Claude API（OK）

## /Auri-Roadmap [阶段]

显示完整路线图。可选参数：1、2、3 或 4 查看阶段详情。
输出：交付物表格含状态、KPI 和预计日期。

## /Auri-Metrics [周期]

指标仪表盘。参数：semana | mes | trimestre。默认：semana。
输出：WAC、Sessions/User、平均时长、转化率、MRR 及增长。

## /Auri-Persona [方面]

人设指南。参数：voz | tom | linguagem | valores | exemplos。
输出：详细指南、对话示例、SSML 模板。

## /Auri-Pricing [计划]

计划与定价。参数：free | pro | business | enterprise。
输出：对比表、收入预测、单位经济效益。

## /Auri-Gtm [渠道]

Go-to-market 策略。参数：organico | pago | influenciadores | parcerias。
输出：分渠道计划、核心信息、发布日历。

## /Auri-Competitive [竞争对手]

竞争分析。参数：alexa | siri | google | chatgpt。
输出：对比表、定位图、异议与回答。

---

## 通过 AWS SAM 部署

部署命令：
  sam build --use-container
  sam deploy --stack-name auri-core --region us-east-1 --capabilities CAPABILITY_IAM

验证部署：
  aws lambda invoke --function-name auri-core-handler --payload file://test.json response.json

## CloudWatch 告警监控

| 告警 | 阈值 | 动作 |
|------|------|------|
| high_latency | Duration > 6000ms | PagerDuty |
| error_rate | 5 分钟内错误 > 5 次 | Slack #auri-alerts |
| claude_api_failures | AnthropicAPIErrors > 3 | Slack + 降级 |
| wac_drop | WAC 周环比下降 > 20% | 产品团队 Slack |

## 降级策略（Claude API 不可用）

如 Anthropic API 不可用，系统返回预配置响应：
- api_down：我有些不稳定。几分钟后重试好吗？
- timeout：这个问题需要更多时间。稍后再问我？
- rate_limit：同时对话太多。几秒后重试！

## 成本管理

| 组件 | 预估成本（1000 Pro 用户）|
|------|--------------------------|
| Claude API | R$ 4.000/月（R$ 4/用户）|
| Lambda | R$ 50/月 |
| DynamoDB | R$ 80/月 |
| CloudWatch | R$ 30/月 |
| 基础设施总计 | R$ 4.160/月 |
| 1000 Pro 收入 | R$ 29.000/月 |
| 毛利率 | ~86% |

---

## LGPD（第 13.709/2018 号法律）

- 法律依据：合同履行（第 7 条第 V 款）适用于 Pro/Business 用户。
- 同意：通过技能引导流程中的语音 + 确认收集。
- 收集数据：对话文本、偏好、匿名化使用数据。
- 保留期：Free = 0 天 | Pro = 90 天 | Business = 365 天。
- 删除权：语音命令「Auri 删除我的数据」-> DynamoDB 删除。
- DPO：公开发布前指定。

## Alexa Skills Store - 政策

- 技能必须完全遵循 Alexa Skills Kit Policies。
- 禁止收集敏感数据（健康、金融、13 岁以下儿童）。
- In-Skill Purchasing 需亚马逊预先批准。
- 提交技能时必须提供 Privacy Policy URL。
- 变现：亚马逊通过 In-Skill Purchasing 抽取 30%。

---

## 13. 术语表

| 术语 | 定义 |
|------|------|
| WAC | Weekly Active Conversationalists - Auri 北极星指标 |
| ASK | Alexa Skills Kit - 亚马逊官方技能 SDK |
| SSML | Speech Synthesis Markup Language - 语音控制标记语言 |
| Intent | 用户想执行的动作（如：给我解释 X）|
| Slot | intent 中的变量（如：给我解释 {query} 中的 query）|
| Utterance | 触发 intent 的示例短语 |
| Session | 与 Auri 的一次连续对话（开始到结束）|
| Long-term Memory | 会话间在 DynamoDB 中持久化的数据 |
| In-Skill Purchasing | Alexa Skills Store 原生计费系统 |
| Vitoria Neural | Auri 使用的高质量 Amazon Polly pt-BR 语音 |
| Claude claude-opus-4-20250805 | 用作 Auri 引擎的 Anthropic 语言模型 |
| DynamoDB | 用于用户持久记忆的 AWS NoSQL 数据库 |
| Lambda | 处理 Auri 请求的 AWS 无服务器函数 |
| Anthropic | Claude 创造者，AI API 提供商 |
| MRR | Monthly Recurring Revenue - 月经常性收入 |
| LTV | Lifetime Value - 客户生命周期价值 |
| CAC | Customer Acquisition Cost - 客户获取成本 |

---

## 14. 链接与资源

| 资源 | URL / 位置 |
|------|------------|
| Alexa Skills Kit 文档 | https://developer.amazon.com/en-US/alexa/alexa-skills-kit |
| ASK SDK Python | https://github.com/alexa/alexa-skills-kit-sdk-for-python |
| Amazon Polly Vitoria Neural | https://docs.aws.amazon.com/polly/latest/dg/voicelist.html |
| Anthropic Claude API | https://docs.anthropic.com/en/api/getting-started |
| Claude claude-opus-4-20250805 文档 | https://docs.anthropic.com/en/docs/models-overview |
| Alexa Skills Store 巴西 | https://www.amazon.com.br/alexa-skills |
| DynamoDB 最佳实践 | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html |
| In-Skill Purchasing | https://developer.amazon.com/en-US/docs/alexa/in-skill-purchase/isp-overview.html |
| Auri 源代码 | C:/Users/renat/skills/auri-core/ |
| Amazon Alexa Skill（技术技能）| C:/Users/renat/skills/amazon-alexa/SKILL.md |

---

*Auri Core Skill - v1.0.0 | 创建于 2026-03-03 | Skills 生态系统*

## 最佳实践

- 提供清晰、具体的项目和需求上下文
- 应用到生产代码前审查所有建议
- 结合其他互补技能进行全面分析

## 常见陷阱

- 将此技能用于其专业领域之外的任务
- 不了解具体上下文就应用建议
- 未提供足够项目上下文导致分析不准确

## 限制
- 仅当任务明显符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如缺少必需输入、权限、安全边界或成功标准，请停下来请求澄清。
