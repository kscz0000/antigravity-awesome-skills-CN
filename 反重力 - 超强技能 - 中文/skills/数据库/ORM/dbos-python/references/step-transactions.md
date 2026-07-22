---
title: 使用事务处理数据库操作
impact: HIGH
impactDescription: 事务提供原子的数据库操作
tags: transaction, database, postgres, sqlalchemy
---

## 使用事务处理数据库操作

事务是一类为数据库访问优化的特殊步骤。它们作为单个数据库事务执行。仅用于 Postgres。

**错误（在普通步骤中访问数据库）：**

```python
@DBOS.step()
def save_to_db(data):
    # 对于 Postgres，请使用事务而不是步骤
    # 这样做无法获得事务保证
    engine.execute("INSERT INTO table VALUES (?)", data)
```

**正确（使用事务）：**

```python
from sqlalchemy import text

@DBOS.transaction()
def save_to_db(name: str, value: str) -> None:
    sql = text("INSERT INTO my_table (name, value) VALUES (:name, :value)")
    DBOS.sql_session.execute(sql, {"name": name, "value": value})

@DBOS.transaction()
def get_from_db(name: str) -> str | None:
    sql = text("SELECT value FROM my_table WHERE name = :name LIMIT 1")
    row = DBOS.sql_session.execute(sql, {"name": name}).first()
    return row[0] if row else None
```

使用 SQLAlchemy ORM：

```python
from sqlalchemy import Table, Column, String, MetaData, select

greetings = Table("greetings", MetaData(),
    Column("name", String),
    Column("note", String))

@DBOS.transaction()
def insert_greeting(name: str, note: str) -> None:
    DBOS.sql_session.execute(greetings.insert().values(name=name, note=note))
```

重要提示：
- 仅在 Postgres 数据库上使用事务
- 对于其他数据库，请使用普通步骤
- 切勿在事务中使用 `async def`

参考：[DBOS 事务](https://docs.dbos.dev/python/reference/decorators#transactions)
