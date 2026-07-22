---
name: base
description: "LibreOffice Base 数据库管理、表单、报表与数据操作技能。涉及LibreOffice Base、ODB数据库、表单设计、报表生成、UNO自动化、数据库连接、数据导入导出、SQL查询时使用。"
category: database-processing
risk: safe
source: personal
date_added: "2026-02-27"
---

# LibreOffice Base 数据库

## 概述

LibreOffice Base 技能，用于使用原生 ODB（OpenDocument Database）格式创建、管理和自动化数据库工作流。

## 适用场景

涉及以下情况时使用：

- 创建新的 ODB 格式数据库
- 连接外部数据库（MySQL、PostgreSQL 等）
- 自动化数据库操作与报表
- 创建表单与报表
- 构建数据库应用

## 核心能力

### 1. 数据库创建
- 从零创建新的 ODB 数据库
- 设计表、视图与关联关系
- 创建嵌入式 HSQLDB/Firebird 数据库
- 连接外部数据库

### 2. 数据操作
- 从 CSV、电子表格导入数据
- 导出数据为多种格式
- 查询执行与管理
- 批量数据处理

### 3. 表单与报表自动化
- 创建数据录入表单
- 设计自定义报表
- 自动化报表生成
- 构建表单模板

### 4. 查询与 SQL
- 可视化查询设计
- SQL 查询执行
- 查询优化
- 结果集操作

### 5. 集成
- 命令行自动化
- 使用 UNO 进行 Python 脚本编写
- JDBC/ODBC 连接

## 工作流

### 创建新数据库

#### 方法一：命令行
```bash
soffice --base
```

#### 方法二：Python + UNO
```python
import uno

def create_database():
    local_ctx = uno.getComponentContext()
    resolver = local_ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_ctx
    )
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=8100;urp;StarOffice.ComponentContext"
    )
    smgr = ctx.ServiceManager
    doc = smgr.createInstanceWithContext("com.sun.star.sdb.DatabaseDocument", ctx)
    doc.storeToURL("file:///path/to/database.odb", ())
    doc.close(True)
```

### 连接外部数据库

```python
import uno

def connect_to_mysql(host, port, database, user, password):
    local_ctx = uno.getComponentContext()
    resolver = local_ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_ctx
    )
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=8100;urp;StarOffice.ComponentContext"
    )
    smgr = ctx.ServiceManager
    
    doc = smgr.createInstanceWithContext("com.sun.star.sdb.DatabaseDocument", ctx)
    datasource = doc.getDataSource()
    datasource.URL = f"sdbc:mysql:jdbc:mysql://{host}:{port}/{database}"
    datasource.Properties["UserName"] = user
    datasource.Properties["Password"] = password
    
    doc.storeToURL("file:///path/to/connected.odb", ())
    return doc
```

## 数据库连接参考

### 支持的数据库类型
- HSQLDB（嵌入式）
- Firebird（嵌入式）
- MySQL/MariaDB
- PostgreSQL
- SQLite
- ODBC 数据源
- JDBC 数据源

### 连接字符串

```
# MySQL
sdbc:mysql:jdbc:mysql://localhost:3306/database

# PostgreSQL
sdbc:postgresql://localhost:5432/database

# SQLite
sdbc:sqlite:file:///path/to/database.db

# ODBC
sdbc:odbc:DSN_NAME
```

## 命令行参考

```bash
soffice --headless
soffice --base  # Base
```

## Python 库

```bash
pip install pyodbc    # ODBC connectivity
pip install sqlalchemy # SQL toolkit
```

## 最佳实践

1. 使用参数化查询
2. 为性能关键字段创建索引
3. 定期备份数据库
4. 使用事务保障数据完整性
5. 将 ODB 源文件纳入版本控制
6. 编写数据库 schema 文档
7. 选择恰当的数据类型
8. 妥善处理连接错误

## 故障排查

### 无法打开套接字
```bash
killall soffice.bin
soffice --headless --accept="socket,host=localhost,port=8100;urp;"
```

### 连接问题
- 确认数据库服务正在运行
- 检查连接字符串格式
- 确保 JDBC/ODBC 驱动已安装
- 验证网络连通性

## 参考资源

- [LibreOffice Base 指南](https://documentation.libreoffice.org/)
- [UNO API 参考](https://api.libreoffice.org/)
- [HSQLDB 文档](http://hsqldb.org/)
- [Firebird 文档](https://firebirdsql.org/)

## 相关技能

- writer
- calc
- impress
- draw
- workflow-automation

## 使用限制
- 仅当任务明确匹配上文所述范围时方可使用此技能。
- 输出内容不能替代特定环境下的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，应停止并请求澄清。
