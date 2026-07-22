# Schema 设计原则

> 涵盖规范化、主键、时间戳与关系建模。

## 规范化决策

```
When to normalize (separate tables):
├── Data is repeated across rows
├── Updates would need multiple changes
├── Relationships are clear
└── Query patterns benefit

When to denormalize (embed/duplicate):
├── Read performance critical
├── Data rarely changes
├── Always fetched together
└── Simpler queries needed
```

## 主键选择

| 类型 | 适用场景 |
|------|----------|
| **UUID** | 分布式系统、安全性 |
| **ULID** | 兼具 UUID 与时间排序 |
| **自增 ID** | 简单应用、单一数据库 |
| **自然键** | 极少使用（业务含义） |

## 时间戳策略

```
For every table:
├── created_at → When created
├── updated_at → Last modified
└── deleted_at → Soft delete (if needed)

Use TIMESTAMPTZ (with timezone) not TIMESTAMP
```

## 关系类型

| 类型 | 适用场景 | 实现方式 |
|------|------|----------------|
| **一对一** | 扩展数据 | 独立表 + 外键 |
| **一对多** | 父子结构 | 子表加外键 |
| **多对多** | 双方均有多条记录 | 中间关联表 |

## 外键 ON DELETE 策略

```
├── CASCADE → Delete children with parent
├── SET NULL → Children become orphans
├── RESTRICT → Prevent delete if children exist
└── SET DEFAULT → Children get default value
```
