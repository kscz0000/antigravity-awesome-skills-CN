# 新技能模板

使用此模板创建 Sentinel 推荐的技能。

## 目录结构

```
nome-da-skill/
├── SKILL.md                    # 元数据 + 文档
├── scripts/
│   ├── requirements.txt        # Python 依赖
│   ├── config.py               # 路径、常量、阈值
│   ├── db.py                   # SQLite 持久化（WAL 模式）
│   ├── governance.py           # 速率限制、审计日志、确认机制
│   └── [feature_modules].py    # 功能模块
├── references/
│   ├── api-reference.md        # API 文档
│   ├── schema.md               # 数据库 Schema
│   └── [domain].md             # 领域专属文档
└── data/
    ├── nome-da-skill.db        # SQLite（WAL 模式）
    └── exports/                # 导出文件
```

## SKILL.md 模板

```yaml
---
name: nome-da-skill
description: >-
  Descricao completa com trigger keywords em PT-BR e EN.
  Use quando o usuario mencionar: keyword1, keyword2, keyword3.
  Triggers: trigger1, trigger2, trigger3.
version: 1.0.0
---

# Skill: Nome da Skill

Descricao breve do que a skill faz.

## Resumo Rapido

| Area | Script | O que faz |
|------|--------|-----------|
| Core | config.py | Configuracao central |
| Core | db.py | Persistencia SQLite |
| Core | governance.py | Governanca |
| Feature | feature.py | Funcionalidade principal |

## Localizacao

[arvore de diretorios]

## Instalacao

[comando pip install]

## Comandos Principais

[exemplos de uso CLI]

## Governanca

[descricao de rate limits, audit log, confirmacoes]

## Referencias

[links para docs em references/]
```

## config.py 模板

```python
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
DATA_DIR = ROOT_DIR / "data"
DB_PATH = DATA_DIR / "nome-da-skill.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)
```

## db.py 模板

```python
import sqlite3
from config import DB_PATH

class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def init(self):
        with self._connect() as conn:
            conn.executescript(DDL)
```

## 质量清单

- [ ] SKILL.md 包含 frontmatter（name、description、version）
- [ ] description 包含双语触发词（PT-BR + EN）
- [ ] requirements.txt 包含固定版本
- [ ] config.py 包含标准路径
- [ ] db.py 使用 WAL 模式和 row_factory
- [ ] governance.py 包含操作日志
- [ ] 至少有 1 份 reference 文档
- [ ] 无硬编码密钥
- [ ] SQL 查询已参数化
- [ ] 错误处理具体明确（无 bare except）
