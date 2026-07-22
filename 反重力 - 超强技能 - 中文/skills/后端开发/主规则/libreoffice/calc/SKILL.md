---
name: calc
description: "使用 LibreOffice Calc 进行电子表格创建、格式转换（ODS/XLSX/CSV）、公式编写与数据自动化。涉及电子表格、ODS、XLSX、CSV、PDF 转换、公式自动化、UNO 脚本等场景时使用。"
category: spreadsheet-processing
risk: safe
source: personal
date_added: "2026-02-27"
---

# LibreOffice Calc

## 概述

基于原生 ODS（OpenDocument 电子表格）格式，使用 LibreOffice Calc 创建、编辑、转换和自动化电子表格工作流的技能。

## 适用场景

适用场景：
- 以 ODS 格式创建新电子表格
- 在 ODS、XLSX、CSV、PDF 格式之间相互转换
- 自动化数据处理与分析
- 创建公式、图表和数据透视表
- 批量处理电子表格操作

## 核心能力

### 1. 电子表格创建
- 从零创建 ODS 电子表格
- 基于模板生成电子表格
- 创建数据录入表单
- 构建仪表盘与报表

### 2. 格式转换
- ODS 转其他格式：XLSX、CSV、PDF、HTML
- 其他格式转 ODS：XLSX、XLS、CSV、DBF
- 批量转换多个文件

### 3. 数据自动化
- 公式自动化与计算
- 从 CSV、数据库、API 导入数据
- 导出为多种格式
- 批量数据处理

### 4. 数据分析
- 数据透视表与数据汇总
- 统计函数与分析
- 数据验证与筛选
- 条件格式

### 5. 集成
- 通过 soffice 实现命令行自动化
- 使用 UNO 进行 Python 脚本开发
- 数据库连接

## 工作流

### 创建新电子表格

#### 方法一：命令行
```bash
soffice --calc template.ods
```

#### 方法二：使用 UNO 的 Python
```python
import uno

def create_spreadsheet():
    local_ctx = uno.getComponentContext()
    resolver = local_ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_ctx
    )
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=8100;urp;StarOffice.ComponentContext"
    )
    smgr = ctx.ServiceManager
    doc = smgr.createInstanceWithContext("com.sun.star.sheet.SpreadsheetDocument", ctx)
    sheets = doc.getSheets()
    sheet = sheets.getByIndex(0)
    cell = sheet.getCellByPosition(0, 0)
    cell.setString("Hello from LibreOffice Calc!")
    doc.storeToURL("file:///path/to/spreadsheet.ods", ())
    doc.close(True)
```

#### 方法三：使用 ezodf
```python
import ezodf

doc = ezodf.newdoc('ods', 'spreadsheet.ods')
sheet = doc.sheets[0]
sheet['A1'].set_value('Hello')
sheet['B1'].set_value('World')
doc.save()
```

### 转换电子表格

```bash
# ODS to XLSX
soffice --headless --convert-to xlsx spreadsheet.ods

# ODS to CSV
soffice --headless --convert-to csv spreadsheet.ods

# ODS to PDF
soffice --headless --convert-to pdf spreadsheet.ods

# XLSX to ODS
soffice --headless --convert-to ods spreadsheet.xlsx

# Batch convert
for file in *.ods; do
    soffice --headless --convert-to xlsx "$file"
done
```

### 公式自动化
```python
import uno

def create_formula_spreadsheet():
    local_ctx = uno.getComponentContext()
    resolver = local_ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_ctx
    )
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=8100;urp;StarOffice.ComponentContext"
    )
    smgr = ctx.ServiceManager
    doc = smgr.createInstanceWithContext("com.sun.star.sheet.SpreadsheetDocument", ctx)
    sheet = doc.getSheets().getByIndex(0)
    
    sheet.getCellByPosition(0, 0).setDoubleValue(100)
    sheet.getCellByPosition(0, 1).setDoubleValue(200)
    
    cell = sheet.getCellByPosition(0, 2)
    cell.setFormula("SUM(A1:A2)")
    
    doc.storeToURL("file:///path/to/formulas.ods", ())
    doc.close(True)
```

## 格式转换参考

### 支持的输入格式
- ODS（原生）、XLSX、XLS、CSV、DBF、HTML

### 支持的输出格式
- ODS、XLSX、XLS、CSV、PDF、HTML

## 命令行参考

```bash
soffice --headless
soffice --headless --convert-to <format> <file>
soffice --calc  # Calc
```

## Python 库

```bash
pip install ezodf     # ODS handling
pip install odfpy     # ODF manipulation
pip install pandas    # Data analysis
```

## 最佳实践

1. 使用命名区域以提高可读性
2. 为复杂公式添加注释说明
3. 使用数据验证控制输入
4. 为周期性报表创建模板
5. 将 ODS 源文件纳入版本控制
6. 充分测试各类转换
7. 使用 CSV 进行数据交换
8. 优雅处理转换失败的情况

## 故障排查

### 无法打开 socket
```bash
killall soffice.bin
soffice --headless --accept="socket,host=localhost,port=8100;urp;"
```

## 资源

- [LibreOffice Calc 指南](https://documentation.libreoffice.org/)
- [UNO API 参考](https://api.libreoffice.org/)
- [ezodf 文档](http://ezodf.rst2.org/)

## 相关技能

- writer
- impress
- draw
- base
- xlsx-official
- workflow-automation

## 局限性
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出结果替代针对特定环境的验证、测试或专家评审。
- 若缺少必需的输入、权限、安全边界或成功标准，请停下来询问以澄清。