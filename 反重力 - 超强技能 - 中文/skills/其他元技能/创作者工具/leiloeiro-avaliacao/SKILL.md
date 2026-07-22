---
name: leiloeiro-avaliacao
description: 拍卖房产司法鉴定评估。市场价值、强制清算价值、ABNT NBR 14653、比较法/收益法/成本法、CUB和安全边际。当用户要求'拍卖房产评估'、'拍卖市场价值'、'评估报告'、'ABNT NBR 14653'、'房产课税价值'或'拍卖房产价格'时使用。
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- real-estate
- valuation
- appraisal
- brazilian
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# 房产评估技能 — 鉴定评估师

## 概述

拍卖房产司法鉴定评估。市场价值、强制清算价值、ABNT NBR 14653、比较法/收益法/成本法、CUB和安全边际。

## 何时使用此技能

- 涉及拍卖房产评估时
- 需要拍卖市场价值估算时
- 出具拍卖评估报告时
- 参考 ABNT NBR 14653 标准时
- 计算房产课税价值时
- 评估拍卖房产价格时

## 何时不使用此技能

- 任务与拍卖房产评估无关
- 有更简单、更专用的工具可以处理请求
- 用户需要的是无领域专业知识的通用辅助

## 工作原理

你是一名持证的**资深评估工程师/建筑师**，精通 ABNT NBR 14653，
拥有司法和非司法拍卖鉴定评估报告的丰富经验。

---

## 价值类型（ABNT NBR 14653-1）

| 概念 | 定义 | 在拍卖中的用途 |
|------|------|----------------|
| **市场价值** | 在知情且无胁迫的双方之间最可能的自由交易金额 | 公告底价（司法评估） |
| **强制清算价值** | 短期内强制出售的金额 | 估算实际拍卖成交价 |
| **使用价值** | 针对特定用途或用户的价值 | 最终买方分析 |
| **重置成本** | 在类似条件下重新建造该资产的成本 | 特殊/工业房产评估 |

**实际关系：**
```
Valor de Mercado (VMP)
    × (1 - fator de liquidação)
= Valor de Liquidação Forçada (VLF)

Fator de liquidação típico: 0,20 a 0,40 (20% a 40% de deságio)
```

---

## 方法1 — 直接比较法（主要方法）

适用于：有市场样本的住宅和商业房产。

## 操作步骤

**1. 样本采集**

至少收集5个可比房产（满足 ABNT II/III 级要求）：
- 同一街区或可比区域
- 同一类型（公寓、住宅、商业办公室）
- 同一面积区间（±30%）
- 近期交易（最近12个月——理想为6个月）

**数据来源：**
- ZAP Imóveis (zap.com.br) — 活跃挂牌
- Viva Real (vivareal.com.br)
- OLX Imóveis
- Quinto Andar (quintoandar.com)
- 房产登记处 — 契约（最可靠，但访问受限）
- 当地持牌经纪人评估（CRECI）

**2. 样本同质化**

调整每个样本使其与待估房产具有可比性：

**同质化因子（乘数）：**

```
Fator Área:
- Imóveis menores tendem a ter valor unitário maior (R$/m²)
- Fórmula: Fa = (Área Padrão / Área Amostra)^0,25

Fator Padrão Construtivo (NBR 12721):
Luxo/Alto:    1,30
Normal/Médio: 1,00
Simples:      0,80
Mínimo:       0,65

Fator Estado de Conservação:
Novo/Reformado:  1,00
Bom:             0,90
Regular:         0,80
Mau:             0,65
Ruim:            0,50

Fator Localização (relativo à amostra):
Superior:    > 1,00
Similar:     1,00
Inferior:    < 1,00
(Calibrar pela infraestrutura local, comércio, transporte)

Fator Andar (apartamentos):
Andar baixo (1-3):   0,95
Andar médio (4-9):   1,00
Andar alto (10+):    1,05 a 1,15
Cobertura:           1,20 a 1,50

Fator Vaga de Garagem:
Sem vaga:  0,90 a 0,95
1 vaga:    1,00
2 vagas:   1,05 a 1,10
```

**3. 统计处理**

同质化后，计算：
- 同质化单价均值（R$/m²）
- 裁量范围：±15%（I 级）/ ±10%（II 级）
- 剔除异常值（超过2个标准差的样本）

**4. 计算最终价值**

```
Valor de Mercado = Valor Unitário Homogeneizado (R$/m²) × Área do Imóvel (m²)
```

---

## 方法2 — 收益法（产生收益的房产）

适用于：购物中心、酒店、写字楼、加油站、出租房产。

## 基本公式

```
Renda Líquida Anual = Renda Bruta - Despesas Operacionais
Taxa de Capitalização (Cap Rate) = Renda Líquida / Valor de Mercado
Valor de Mercado = Renda Líquida / Cap Rate
```

**巴西典型 Cap Rate（2024）：**

| 细分市场 | Cap Rate |
|----------|---------|
| 圣保罗/里约高端住宅 | 4% - 6% |
| 中端住宅 | 5% - 8% |
| 商业办公室 | 7% - 10% |
| 物流仓库 | 8% - 12% |
| 零售商业 | 8% - 12% |
| 酒店 | 10% - 15% |

**示例：**
- 商业房产月租 R$ 10.000
- 费用：IPTU R$ 500/月 + 物业费 R$ 800/月 + 空置率 5%
- 净收益：R$ (10.000 - 500 - 800) × (1 - 0,05) = R$ 8.265/月 → R$ 99.180/年
- 当地 Cap Rate：8%
- 估算价值：R$ 99.180 / 0,08 = **R$ 1.239.750**

---

## 方法3 — 重置/成本法（特殊房产）

适用于：工业房产、仓库、医院、学校、无可比样本的房产。

## 公式

```
Valor Total = Valor do Terreno + Valor das Benfeitorias (depreciadas)

Valor das Benfeitorias = Custo de Reprodução × (1 - Depreciação)
```

**重置成本（CUB — SINDUSCON，按州按月更新）：**

| 标准 | CUB 约值（R$/m²）— 圣保罗 2024 参考 |
|------|--------------------------------------|
| 低端住宅 (R1-B) | R$ 1.800 - 2.200 |
| 普通住宅 (R1-N) | R$ 2.200 - 2.800 |
| 高端住宅 (R1-A) | R$ 2.800 - 3.800 |
| 商业 (CSL-8) | R$ 2.500 - 3.500 |
| 仓库 (GI) | R$ 1.200 - 1.800 |

*查询最新 CUB：www.sindusconsp.com.br*

**折旧（Ross-Heidecke）：**

| 房龄 / 状况 | 新建 | 良好 | 一般 | 较差 |
|-------------|------|------|------|------|
| 0-10年 | 100% | 85% | 70% | 55% |
| 11-20年 | 85% | 72% | 59% | 46% |
| 21-30年 | 70% | 59% | 49% | 38% |
| 31-40年 | 55% | 47% | 38% | 30% |
| > 40年 | 45% | 38% | 31% | 24% |

---

## 司法鉴定评估报告分析

收到评估报告进行分析时，需核查：

## 报告检查清单

**形式要件：**
- [ ] 评估师持有 CREA/CAU 执照
- [ ] 勘察日期（非出具日期）
- [ ] 房产物理描述
- [ ] 声明所采用的方法
- [ ] 依据与精度（I 级、II 级或 III 级——ABNT）

**技术内容：**
- [ ] 所用样本（I 级至少3个；II 级至少5个）
- [ ] 标明样本来源
- [ ] 同质化过程展示（或说明理由）
- [ ] 适用裁量范围
- [ ] 得出的单价 R$/m²
- [ ] 最终计算清晰

**薄弱/可疑报告的信号：**
- ⚠️ 样本少于3个（I 级不足以支撑重要拍卖）
- ⚠️ 样本来自距离过远或差异过大的街区
- ⚠️ 无勘察日期（房产何时被实地查看？）
- ⚠️ 估值与市场严重偏离且无合理解释
- ⚠️ 报告从前案复制而未更新
- ⚠️ 评估师在房产所在州无有效 CREA/CAU

---

## 区位分析（区位评分）

对每个因素赋予0到5分：

```
INFRAESTRUTURA:
[ ] Transporte público (metro, BRT, ônibus): 0-5
[ ] Comércio e serviços no entorno: 0-5
[ ] Escolas e hospitais próximos: 0-5
[ ] Parques e áreas de lazer: 0-5

URBANISMO:
[ ] Zoneamento favorável (residencial, ZEU, ZEIS...): 0-5
[ ] Potencial construtivo (coeficiente aproveitamento): 0-5
[ ] Restrições (APP, faixa de marinha, tombamento): 0-5

MERCADO:
[ ] Valorização histórica da região: 0-5
[ ] Presença de empreendimentos novos: 0-5
[ ] Liquidez estimada (facilidade de revenda): 0-5

TOTAL: ___ / 50
```

**解读：**
- 40-50：区位优秀 — 溢价
- 30-39：区位良好 — 高于平均
- 20-29：区位一般 — 正常市场
- 10-19：区位低于平均 — 流动性较低
- 0-9：区位较差 — 高流动性风险

---

## 安全边际计算

```
Valor de Mercado Estimado (VMP):        R$ _______________
(-) Custos de aquisição (ITBI + Cart.): R$ _______________  (aprox. 4-5% do valor)
(-) Comissão leiloeiro (5%):            R$ _______________
(-) Débitos IPTU + Condomínio:          R$ _______________
(-) Custo de desocupação (se necessário): R$ _____________
(-) Obras/regularização estimada:       R$ _______________
(-) Margem de segurança (10-20%):       R$ _______________
= LANCE MÁXIMO RECOMENDADO:             R$ _______________

DESÁGIO MÍNIMO ACEITÁVEL: ____% do VMP
```

---

## 按类型分析

**住宅公寓：**
- 核查：车位、楼层、朝向（上午/下午日照）、烧烤区、储物间
- 流动性：很高（圣保罗、里约、贝洛奥里藏特、库里蒂巴）——易于转售

**小区住宅：**
- 核查：休闲设施、安保、物业费、建设限制
- 流动性：高——家庭需求稳定

**城市地块：**
- 核查：区划（容积率、占地率）
- 核查：开发可能性（潜在 VGV）
- 流动性：中等——高度依赖区位

**商业办公室：**
- 核查：档次、街道、人流量、车位、违规记录
- 流动性：低至中等——市场较窄

**物流/工业仓库：**
- 核查：层高（物流最低8米）、装卸台、卡车通道、AVCB
- 流动性：中高（在物流走廊地带：Dutra公路、Castelo Branco公路、BR-381）

**农村房产：**
- 核查：ITR、CAR、法定保留区、通路、水源、电力
- 流动性：低——专业化市场

---

## 在线市场调研 — 操作步骤

需要在无评估报告的情况下估算房产市场价值时：

## 快速调研流程（15分钟）

```
1. ABRIR ZAP IMÓVEIS (zapimoveis.com.br):
   - Buscar pelo bairro e tipo do imóvel
   - Filtrar por área similar (±20%)
   - Filtrar por nº de quartos similar
   - Anotar: 5 imóveis com preço de VENDA (não aluguel)
   - Anotar: R$/m² de cada amostra

2. ABRIR VIVA REAL (vivareal.com.br):
   - Repetir a mesma busca
   - Cruzar com dados do ZAP (evitar duplicatas)
   - Anotar: 3-5 amostras adicionais

3. APLICAR FATOR DE ELASTICIDADE:
   - Anúncios têm margem de negociação média de 10-15%
   - Valor real de venda ≈ preço anunciado × 0,85 a 0,90
   - Em mercado fraco: × 0,80
   - Em mercado aquecido: × 0,92

4. CALCULAR VMP ESTIMADO:
   - Média dos R$/m² das amostras ajustadas
   - Multiplicar pela área do imóvel do leilão
   - RESULTADO = VMP estimado (±15% de margem)

5. VALIDAÇÃO COM GOOGLE STREET VIEW:
   - Abrir o endereço no Google Maps
   - Verificar: entorno, comércio, transporte
   - Estado aparente das fachadas vizinhas
   - Confirmar se bairro corresponde ao padrão das amostras
```

## CUB 参考 2025（SINDUSCON-SP — 每月更新）

| 标准 | CUB R$/m²（2025年1月参考） |
|------|---------------------------|
| R1-B（低端住宅） | R$ 2.000 - 2.400 |
| R1-N（普通住宅） | R$ 2.400 - 3.100 |
| R1-A（高端住宅） | R$ 3.100 - 4.200 |
| R8-N（普通楼宇） | R$ 2.100 - 2.700 |
| R8-A（高端楼宇） | R$ 2.800 - 3.600 |
| R16-N（16层楼宇） | R$ 2.200 - 2.900 |
| CSL-8（商业） | R$ 2.700 - 3.800 |
| GI（工业仓库） | R$ 1.400 - 2.000 |

*来源：SINDUSCON-SP。每月更新查询：www.sindusconsp.com.br/indices-e-custos/cub/*

---

## 大众房产（30万雷亚尔以下）

- 评估允许误差：±15%
- 流动性：高——该价位买家众多
- 清算因子：0,20（VLF = 80% VMP）
- 拍卖理想折扣：≥30%

## 中档房产（30万-80万雷亚尔）

- 允许误差：±10%
- 流动性：中高
- 清算因子：0,25
- 拍卖理想折扣：≥35%

## 高端房产（80万-200万雷亚尔）

- 允许误差：±10%
- 流动性：中等——出售周期较长
- 清算因子：0,30
- 拍卖理想折扣：≥40%

## 奢华房产（200万雷亚尔以上）

- 允许误差：±15%（样本较少）
- 流动性：低——市场狭窄
- 清算因子：0,35 至 0,45
- 拍卖理想折扣：≥45%
- 投资者需有持有12-24个月的资金能力

---

## 拍卖房产能否贷款？

| 类型 | 可否贷款 | 备注 |
|------|----------|------|
| CEF 直接出售 | 可以——本行贷款 | 最高80% VMAV，允许使用 FGTS |
| BB/Santander 直接出售 | 可以——本行贷款 | 条件各异 |
| 银行非司法拍卖 | 视情况——需查阅公告 | 部分接受贷款 |
| 司法拍卖 | 通常不可以 | 当场付款或短期分期（第895条） |

## 司法拍卖分期付款（CPC 第895条）

- 当场支付25%定金
- 余额最多分30期
- 利息：通常月息1%（单利）
- 担保：以所购房产本身设定抵押
- **风险：** 如未按时付款，将失去房产和定金

---

## 安装

本技能为纯知识型（knowledge-only），无需安装依赖。

```bash

## Verificar Se A Skill Está Registrada:

python C:\Users\renat\skills\agent-orchestrator\scripts\scan_registry.py
```

---

## 命令与使用

如何使用此技能：

```bash

## Uso Via Orchestrator (Automático):

python agent-orchestrator/scripts/match_skills.py "avaliar imovel leilao"

## "Qual O Valor De Mercado Desse Apartamento?"

```

---

## 治理

本技能实施以下治理策略：

- **action_log**：已完成的评估通过生态系统的 log_action 记录
- **rate_limit**：通过集成的 check_rate 控制——无直接外部 API 调用
- **requires_confirmation**：负边际评估触发强制 confirmation_request
- **warning_threshold**：折扣<15%或评估过期自动触发 warning_threshold

附加策略：
- **负责人：** Leiloeiro IA 生态系统
- **范围：** 拍卖房产司法鉴定评估
- **限制：** 仅为指示性估算，不替代工程师/建筑师的鉴定评估报告
- **审计：** 由 skill-sentinel 验证
- **敏感数据：** 不存储评估数据

---

## 参考文献

规范性来源和参考文献：
- **ABNT NBR 14653-1:2019** — 通用程序
- **ABNT NBR 14653-2:2011** — 城市房产
- **ABNT NBR 14653-3:2004** — 农村房产
- **ABNT NBR 12721** — 建造成本评估
- **CUB** — 基础单位成本（SINDUSCON 按州按月更新）
- **COFECI** — 联邦经纪人委员会（评估意见书）
- **IBAPE** — 巴西工程评估与鉴定协会
- **FIPEZAP** — 房产价格指数（fipe.org.br/indices/fipezap）

## 最佳实践

- 提供清晰、具体的项目背景和需求
- 在将建议应用于生产代码前进行审查
- 结合其他互补技能进行综合分析

## 常见误区

- 将此技能用于其专业领域之外的任务
- 在不了解具体背景的情况下套用建议
- 未提供足够的项目背景导致分析不准确

## 相关技能

- `junta-leiloeiros` — 互补技能，增强分析
- `leiloeiro-edital` — 互补技能，增强分析
- `leiloeiro-ia` — 互补技能，增强分析
- `leiloeiro-juridico` — 互补技能，增强分析
- `leiloeiro-mercado` — 互补技能，增强分析

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 输出不替代针对具体环境的验证、测试或专家审查。
- 若缺少必要输入、权限、安全边界或成功标准，应停下来请求澄清。
