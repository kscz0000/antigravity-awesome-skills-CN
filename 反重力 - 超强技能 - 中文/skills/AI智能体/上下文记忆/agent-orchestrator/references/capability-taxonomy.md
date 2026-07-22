# 能力分类法（Capability Tags）

生态系统中技能分类的标准类别。
每个技能可以有多个类别。

---

## 类别

### data-extraction
**描述：** 从网页或API收集和提取数据。
**关键词 PT：** raspar, extrair, coletar, dados, tabela
**关键词 EN：** scrape, extract, crawl, parse, harvest, collect, data, table, csv
**当前技能：** web-scraper, junta-leiloeiros

### messaging
**描述：** 通过通信平台发送和接收消息。
**关键词 PT：** mensagem, enviar, notificacao, atendimento, comunicar, avisar
**关键词 EN：** whatsapp, message, send, chat, notify, notification, sms
**当前技能：** whatsapp-cloud-api

### social-media
**描述：** 与社交媒体平台交互（帖子、快拍、分析）。
**关键词 PT：** publicar, rede social, engajamento, post, stories
**关键词 EN：** instagram, facebook, twitter, post, stories, reels, social, feed, follower
**当前技能：** instagram

### government-data
**描述：** 收集政府数据、公共记录、官方机构信息。
**关键词 PT：** junta, leiloeiro, cadastro, governo, comercial, tribunal, certidao, registro
**关键词 EN：** government, registry, official, court, public records
**当前技能：** junta-leiloeiros

### web-automation
**描述：** 浏览器自动化、表单填写、页面交互。
**关键词 PT：** navegador, automatizar, automacao, preencher
**关键词 EN：** browser, selenium, playwright, automate, click, fill form
**当前技能：** web-scraper

### api-integration
**描述：** 与外部API集成、webhooks、OAuth认证。
**关键词 PT：** integracao, integrar, conectar, api, webhook
**关键词 EN：** api, endpoint, webhook, rest, graph, oauth, token
**当前技能：** whatsapp-cloud-api, instagram

### analytics
**描述：** 数据分析、指标、仪表盘、报告。
**关键词 PT：** relatorio, metricas, analise, estatistica
**关键词 EN：** insight, analytics, metrics, dashboard, report, stats
**当前技能：** （暂无专用技能）

### content-management
**描述：** 在平台上发布、调度和管理内容。
**关键词 PT：** publicar, agendar, conteudo, midia, template
**关键词 EN：** publish, schedule, template, content, media, upload
**当前技能：** instagram

---

## 角色（Roles）

类别按角色分组用于编排：

| 角色      | 类别                                      | 描述                        |
|:-----------|:------------------------------------------------|:---------------------------------|
| Producer   | data-extraction, government-data, analytics     | 生成/收集数据                |
| Consumer   | messaging, social-media, content-management     | 对数据进行操作（发送、发布）|
| Hybrid     | api-integration, web-automation                 | 可以生产和消费数据   |

---

## 如何在 SKILL.md 中声明

在 YAML frontmatter 中添加 `capabilities` 字段：

```yaml
---
name: minha-skill
description: "..."
capabilities: [data-extraction, web-automation]
---
```

如果省略，扫描器会通过关键词自动从 `description` 中提取。
显式标签优先，不会与自动提取的重复。
