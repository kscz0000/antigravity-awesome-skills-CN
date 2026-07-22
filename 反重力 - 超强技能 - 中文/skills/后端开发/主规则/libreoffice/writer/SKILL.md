---
name: writer
description: "使用 LibreOffice Writer 进行文档创建、格式转换（ODT/DOCX/PDF）、邮件合并以及自动化处理。"
category: document-processing
risk: safe
source: personal
date_added: "2026-02-27"
---

# LibreOffice Writer

## 概述

使用 LibreOffice Writer 创建、编辑、转换文档并实现文档工作流自动化，基于原生 ODT（OpenDocument Text）格式。

## 适用场景

在以下场景中使用此技能：
- 创建 ODT 格式的新文档
- 在不同格式之间转换文档（ODT <-> DOCX、PDF、HTML、RTF、TXT）
- 自动化文档生成工作流
- 执行批量文档操作
- 创建模板与标准化文档格式

## 核心能力

### 1. 文档创建
- 从零开始创建新的 ODT 文档
- 基于模板生成文档
- 创建邮件合并文档
- 构建带可填写字段的表单

### 2. 格式转换
- ODT 转换为其他格式：DOCX、PDF、HTML、RTF、TXT、EPUB
- 其他格式转换为 ODT：DOCX、DOC、RTF、HTML、TXT
- 批量转换多个文档

### 3. 文档自动化
- 基于模板的文档生成
- 使用数据源（CSV、电子表格、数据库）进行邮件合并
- 批量文档处理
- 自动生成报告

### 4. 内容操作
- 文本提取与插入
- 样式管理与应用
- 表格创建与操作
- 页眉/页脚管理

### 5. 集成
- 通过 soffice 进行命令行自动化
- 使用 UNO 进行 Python 脚本编程
- 与工作流自动化工具集成

## 工作流

### 创建新文档

#### 方法一：命令行
```bash
soffice --writer template.odt
```

#### 方法二：使用 Python 和 UNO
```python
import uno

def create_document():
    local_ctx = uno.getComponentContext()
    resolver = local_ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_ctx
    )
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=8100;urp;StarOffice.ComponentContext"
    )
    smgr = ctx.ServiceManager
    doc = smgr.createInstanceWithContext("com.sun.star.text.TextDocument", ctx)
    text = doc.Text
    cursor = text.createTextCursor()
    text.insertString(cursor, "Hello from LibreOffice Writer!", 0)
    doc.storeToURL("file:///path/to/document.odt", ())
    doc.close(True)
```

#### 方法三：使用 odfpy
```python
from odf.opendocument import OpenDocumentText
from odf.text import P, H

doc = OpenDocumentText()
h1 = H(outlinelevel='1', text='Document Title')
doc.text.appendChild(h1)
doc.save("document.odt")
```

### 文档转换

```bash
# ODT to DOCX
soffice --headless --convert-to docx document.odt

# ODT to PDF
soffice --headless --convert-to pdf document.odt

# DOCX to ODT
soffice --headless --convert-to odt document.docx

# Batch convert
for file in *.odt; do
    soffice --headless --convert-to pdf "$file"
done
```

### 基于模板的生成
```python
import subprocess
import tempfile
from pathlib import Path

def generate_from_template(template_path, variables, output_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(['unzip', '-q', template_path, '-d', tmpdir])
        content_file = Path(tmpdir) / 'content.xml'
        content = content_file.read_text()
        for key, value in variables.items():
            content = content.replace(f'${{{key}}}', str(value))
        content_file.write_text(content)
        subprocess.run(['zip', '-rq', output_path, '.'], cwd=tmpdir)
    return output_path
```

## 格式转换参考

### 支持的输入格式
- ODT（原生）、DOCX、DOC、RTF、HTML、TXT、EPUB

### 支持的输出格式
- ODT、DOCX、PDF、PDF/A、HTML、RTF、TXT、EPUB

## 命令行参考

```bash
soffice --headless
soffice --headless --convert-to <format> <file>
soffice --writer    # Writer
soffice --calc      # Calc
soffice --impress   # Impress
soffice --draw      # Draw
```

## Python 库

```bash
pip install odfpy     # ODF manipulation
pip install ezodf     # Easier ODF handling
```

## 最佳实践

1. 使用样式保持一致性
2. 为重复性文档创建模板
3. 保证可访问性（标题层级、替代文本）
4. 填写文档元数据
5. 将 ODT 源文件纳入版本控制
6. 充分测试转换效果
7. 在 PDF 分发中嵌入字体
8. 妥善处理转换失败
9. 记录自动化操作日志
10. 清理临时文件

## 故障排查

### 无法打开套接字
```bash
killall soffice.bin
soffice --headless --accept="socket,host=localhost,port=8100;urp;"
```

### 转换质量问题
```bash
soffice --headless --convert-to pdf:writer_pdf_Export document.odt
```

## 资源

- [LibreOffice Writer 指南](https://documentation.libreoffice.org/)
- [LibreOffice SDK](https://wiki.documentfoundation.org/Documentation/DevGuide)
- [UNO API 参考](https://api.libreoffice.org/)
- [odfpy](https://pypi.org/project/odfpy/)

## 相关技能

- calc
- impress
- draw
- base
- docx-official
- pdf-official
- workflow-automation

## 局限性

- 仅当任务明确匹配上述范围时使用此技能。
- 请勿将输出视为环境特定验证、测试或专家审查的替代品。
- 如缺少必需的输入、权限、安全边界或成功标准，请停止操作并请求澄清。