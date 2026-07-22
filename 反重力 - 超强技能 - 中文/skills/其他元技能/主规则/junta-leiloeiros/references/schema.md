# 数据Schema — 商业委员会拍卖师

## `leiloeiros` 表（SQLite）

```sql
CREATE TABLE leiloeiros (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    estado           TEXT    NOT NULL,     -- UF: SP, RJ, MG, ...
    junta            TEXT    NOT NULL,     -- 委员会名称: JUCESP, JUCERJA, ...
    matricula        TEXT,                 -- 注册号（未公开时可为NULL）
    nome             TEXT    NOT NULL,     -- 拍卖师全名
    cpf_cnpj         TEXT,                 -- CPF或CNPJ（有则填）
    situacao         TEXT,                 -- ATIVO | CANCELADO | SUSPENSO | IRREGULAR
    endereco         TEXT,                 -- 完整地址
    municipio        TEXT,                 -- 城市
    telefone         TEXT,                 -- 联系电话
    email            TEXT,                 -- 电子邮箱
    data_registro    TEXT,                 -- 委员会注册日期（ISO 8601或文本）
    data_atualizacao TEXT,                 -- 最近注册信息更新日期
    url_fonte        TEXT,                 -- 数据来源URL
    scraped_at       TEXT    NOT NULL,     -- 采集时间戳（ISO 8601 UTC）
    UNIQUE (estado, matricula) ON CONFLICT REPLACE
);
```

## 字段说明

| 字段 | 类型 | 必填 | 取值 |
|-------|------|-------------|---------|
| `id` | int | 自动 | 自增主键 |
| `estado` | text | 是 | 2字母大写州缩写 |
| `junta` | text | 是 | 委员会名称，如 JUCESP |
| `matricula` | text | 否 | 委员会注册号 |
| `nome` | text | 是 | 全名 |
| `cpf_cnpj` | text | 否 | 证件号，优先不含格式 |
| `situacao` | text | 否 | ATIVO、CANCELADO、SUSPENSO、IRREGULAR |
| `endereco` | text | 否 | 完整街道地址 |
| `municipio` | text | 否 | 城市 |
| `telefone` | text | 否 | 自由格式 |
| `email` | text | 否 | 联系邮箱 |
| `data_registro` | text | 否 | ISO日期或委员会原始文本 |
| `data_atualizacao` | text | 否 | ISO日期或委员会原始文本 |
| `url_fonte` | text | 否 | 采集页面URL |
| `scraped_at` | text | 是 | ISO 8601 UTC，如 2024-03-15T10:30:00+00:00 |

## `situacao` 字段标准化

各委员会的原始文本标准化为统一值：

| 原始文本（示例） | 标准化值 |
|--------------------------|-------------------|
| Ativo、Regular、Habilitado、Regularizado | `ATIVO` |
| Cancelado、Baixado、Extinto | `CANCELADO` |
| Suspenso | `SUSPENSO` |
| Irregular | `IRREGULAR` |
| 其他 | 保持原样 |

## 导出格式（JSON）

```json
{
  "exported_at": "2024-03-15T10:30:00+00:00",
  "total": 1234,
  "data": [
    {
      "id": 1,
      "estado": "SP",
      "junta": "JUCESP",
      "matricula": "001234",
      "nome": "João da Silva Leiloeiro",
      "cpf_cnpj": null,
      "situacao": "ATIVO",
      "endereco": "Rua das Flores, 100",
      "municipio": "São Paulo",
      "telefone": "(11) 3456-7890",
      "email": "joao@leiloes.com.br",
      "data_registro": "2010-05-20",
      "data_atualizacao": null,
      "url_fonte": "https://www.institucional.jucesp.sp.gov.br/tradutores-leiloeiros.html",
      "scraped_at": "2024-03-15T10:30:00+00:00"
    }
  ]
}
```

## 索引

```sql
CREATE INDEX idx_estado   ON leiloeiros (estado);
CREATE INDEX idx_nome     ON leiloeiros (nome);
CREATE INDEX idx_situacao ON leiloeiros (situacao);
CREATE INDEX idx_scraped  ON leiloeiros (scraped_at);
```
