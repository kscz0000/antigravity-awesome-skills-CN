# 索引设计原则

> 何时及如何创建高效索引。

## 何时创建索引

```
Index these:
├── Columns in WHERE clauses
├── Columns in JOIN conditions
├── Columns in ORDER BY
├── Foreign key columns
└── Unique constraints

Don't over-index:
├── Write-heavy tables (slower inserts)
├── Low-cardinality columns
├── Columns rarely queried
```

## 索引类型选择

| 类型 | 适用场景 |
|------|---------|
| **B-tree** | 通用场景、等值与范围查询 |
| **Hash** | 仅等值查询，速度更快 |
| **GIN** | JSONB、数组、全文检索 |
| **GiST** | 几何、范围类型 |
| **HNSW/IVFFlat** | 向量相似度（pgvector） |

## 复合索引原则

```
Order matters for composite indexes:
├── Equality columns first
├── Range columns last
├── Most selective first
└── Match query pattern
```
