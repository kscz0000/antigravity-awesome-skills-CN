---
name: junta-leiloeiros
description: 采集和查询巴西全部27个商业委员会的官方拍卖师数据。多州Scraper、SQLite数据库、FastAPI API及CSV/JSON导出。触发词：leiloeiro junta、junta comercial leiloeiro、scraper junta、jucesp leiloeiro、jucerja、jucemg leiloeiro、拍卖师数据采集
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- scraping
- brazilian-data
- auctioneers
- api
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# 技能：巴西商业委员会拍卖师

## 概述

采集和查询巴西全部27个商业委员会的官方拍卖师数据。多州Scraper、SQLite数据库、FastAPI API及CSV/JSON导出。

## 何时使用此技能

- 当用户提到"leiloeiro junta"或相关话题时
- 当用户提到"junta comercial leiloeiro"或相关话题时
- 当用户提到"scraper junta"或相关话题时
- 当用户提到"jucesp leiloeiro"或相关话题时
- 当用户提到"jucerja"或相关话题时
- 当用户提到"jucemg leiloeiro"或相关话题时

## 何时不使用此技能

- 任务与商业委员会拍卖师无关
- 有更简单、更专用的工具可以处理请求
- 用户需要的是无领域专业知识的通用辅助

## 工作原理

采集巴西全部27个州级商业委员会的官方拍卖师公开数据，持久化到本地SQLite数据库，并提供REST API和多格式导出。

## 目录结构

```
C:\Users\renat\skills\junta-leiloeiros\
├── scripts/
│   ├── scraper/
│   │   ├── base_scraper.py      ← 抽象类
│   │   ├── states.py            ← 27个scraper注册
│   │   ├── jucesp.py / jucerja.py / jucemg.py / jucec.py / jucis_df.py
│   │   └── generic_scraper.py   ← 其余22个州使用
│   ├── db.py                    ← SQLite数据库
│   ├── run_all.py               ← 采集编排器
│   ├── serve_api.py             ← FastAPI API
│   ├── export.py                ← 导出
│   └── requirements.txt
├── references/
│   ├── juntas_urls.md           ← 全部27个委员会的URL和状态
│   ├── schema.md                ← 数据库schema
│   └── legal.md                 ← 法律依据
└── data/
    ├── leiloeiros.db            ← SQLite数据库（首次运行时创建）
    ├── scraping_log.json        ← 每次采集日志
    └── exports/                 ← 导出文件
```

## 安装（一次性）

```bash
pip install -r C:\Users\renat\skills\junta-leiloeiros\scripts\requirements.txt

## 针对使用JavaScript的网站：

playwright install chromium
```

## 采集数据

```bash

## 全部27个州

python C:\Users\renat\skills\junta-leiloeiros\scripts\run_all.py

## 指定州

python C:\Users\renat\skills\junta-leiloeiros\scripts\run_all.py --estado SP RJ MG

## 预览将采集的内容（不实际执行）

python C:\Users\renat\skills\junta-leiloeiros\scripts\run_all.py --dry-run

## 控制并发数（默认：5）

python C:\Users\renat\skills\junta-leiloeiros\scripts\run_all.py --concurrency 3
```

## 按州查看统计

python C:\Users\renat\skills\junta-leiloeiros\scripts\db.py

## 直接执行SQL

sqlite3 C:\Users\renat\skills\junta-leiloeiros\data\leiloeiros.db \
  "SELECT estado, COUNT(*) FROM leiloeiros GROUP BY estado"
```

## 启动REST API

```bash
python C:\Users\renat\skills\junta-leiloeiros\scripts\serve_api.py

## 交互式文档：http://localhost:8000/docs

```

**端点：**
- `GET /leiloeiros?estado=SP&situacao=ATIVO&nome=silva&limit=100`
- `GET /leiloeiros/{estado}` — 例：`/leiloeiros/SP`
- `GET /busca?q=texto`
- `GET /stats`
- `GET /export/json`
- `GET /export/csv`

## 导出数据

```bash
python C:\Users\renat\skills\junta-leiloeiros\scripts\export.py --format csv
python C:\Users\renat\skills\junta-leiloeiros\scripts\export.py --format json
python C:\Users\renat\skills\junta-leiloeiros\scripts\export.py --format all
python C:\Users\renat\skills\junta-leiloeiros\scripts\export.py --format csv --estado SP
```

## 在Python代码中使用

```python
import sys
sys.path.insert(0, r"C:\Users\renat\skills\junta-leiloeiros\scripts")
from db import Database

db = Database()
db.init()

## 查询SP州所有活跃拍卖师

leiloeiros = db.get_all(estado="SP", situacao="ATIVO")

## 按姓名搜索

resultados = db.search("silva")

## 统计信息

stats = db.get_stats()
```

## 添加自定义Scraper

如果某个州需要特定逻辑（例如：网站使用JavaScript）：

```python

## scripts/scraper/meu_estado.py

from .base_scraper import AbstractJuntaScraper, Leiloeiro
from typing import List

class MeuEstadoScraper(AbstractJuntaScraper):
    estado = "XX"
    junta = "JUCEX"
    url = "https://www.jucex.xx.gov.br/leiloeiros"

    async def parse_leiloeiros(self) -> List[Leiloeiro]:
        soup = await self.fetch_page()
        if not soup:
            return []
        # 在此添加特定逻辑
        return [self.make_leiloeiro(nome="...", matricula="...")]
```

在 `scripts/scraper/states.py` 中注册：
```python
from .meu_estado import MeuEstadoScraper
SCRAPERS["XX"] = MeuEstadoScraper
```

## 参考资料

- 全部委员会URL：`references/juntas_urls.md`
- 数据库Schema：`references/schema.md`
- 采集法律依据：`references/legal.md`
- 采集日志：`data/scraping_log.json`

## 最佳实践

- 提供清晰、具体的项目背景和需求
- 在将建议应用到生产代码前进行审查
- 结合其他互补技能进行综合分析

## 常见误区

- 将此技能用于超出其领域专业范围的任务
- 在不了解具体上下文的情况下套用建议
- 未提供足够的项目背景导致分析不准确

## 相关技能

- `leiloeiro-avaliacao` — 互补技能，用于增强分析
- `leiloeiro-edital` — 互补技能，用于增强分析
- `leiloeiro-ia` — 互补技能，用于增强分析
- `leiloeiro-juridico` — 互补技能，用于增强分析
- `leiloeiro-mercado` — 互补技能，用于增强分析

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
