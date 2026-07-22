---
name: impress
description: "使用 LibreOffice Impress 进行演示文稿创建、格式转换（ODP/PPTX/PDF）以及幻灯片自动化。涉及LibreOffice Impress、ODP、PPTX、演示文稿转换、幻灯片自动化、UNO时使用。"
category: presentation-processing
risk: safe
source: personal
date_added: "2026-02-27"
---

# LibreOffice Impress

## 概述

LibreOffice Impress 技能，基于原生 ODP（OpenDocument Presentation）格式进行演示文稿的创建、编辑、转换与自动化操作。

## 适用场景

涉及以下任务时使用此技能：
- 以 ODP 格式创建新演示文稿
- 在 ODP、PPTX、PDF 之间相互转换
- 基于模板自动生成幻灯片
- 批量处理演示文稿相关操作
- 创建演示文稿模板

## 核心能力

### 1. 演示文稿创建
- 从零创建 ODP 演示文稿
- 基于模板生成演示文稿
- 创建幻灯片母版与版式
- 构建可交互的演示文稿

### 2. 格式转换
- ODP 转其他格式：PPTX、PDF、HTML、SWF
- 其他格式转 ODP：PPTX、PPT、PDF
- 批量转换多个文件

### 3. 幻灯片自动化
- 基于模板的幻灯片生成
- 根据数据批量创建幻灯片
- 自动插入内容
- 动态图表生成

### 4. 内容处理
- 文本与图片插入
- 图形与示意图创建
- 动画与切换效果控制
- 演讲者备注管理

### 5. 集成能力
- 通过 soffice 进行命令行自动化
- 使用 UNO 进行 Python 脚本编写
- 与工作流工具集成

## 工作流

### 创建新演示文稿

#### 方法一：命令行
```bash
soffice --impress template.odp
```

#### 方法二：Python + UNO
```python
import uno

def create_presentation():
    local_ctx = uno.getComponentContext()
    resolver = local_ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_ctx
    )
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=8100;urp;StarOffice.ComponentContext"
    )
    smgr = ctx.ServiceManager
    doc = smgr.createInstanceWithContext("com.sun.star.presentation.PresentationDocument", ctx)
    slides = doc.getDrawPages()
    slide = slides.getByIndex(0)
    doc.storeToURL("file:///path/to/presentation.odp", ())
    doc.close(True)
```

### 转换演示文稿

```bash
# ODP to PPTX
soffice --headless --convert-to pptx presentation.odp

# ODP to PDF
soffice --headless --convert-to pdf presentation.odp

# PPTX to ODP
soffice --headless --convert-to odp presentation.pptx

# Batch convert
for file in *.odp; do
    soffice --headless --convert-to pdf "$file"
done
```

### 基于模板的生成
```python
import subprocess
import tempfile
from pathlib import Path

def generate_from_template(template_path, content, output_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(['unzip', '-q', template_path, '-d', tmpdir])
        content_file = Path(tmpdir) / 'content.xml'
        content_xml = content_file.read_text()
        for key, value in content.items():
            content_xml = content_xml.replace(f'${{{key}}}', str(value))
        content_file.write_text(content_xml)
        subprocess.run(['zip', '-rq', output_path, '.'], cwd=tmpdir)
    return output_path
```

## 格式转换参考

### 支持的输入格式
- ODP（原生）、PPTX、PPT、PDF

### 支持的输出格式
- ODP、PPTX、PDF、HTML、SWF

## 命令行参考

```bash
soffice --headless
soffice --headless --convert-to <format> <file>
soffice --impress  # Impress
```

## Python 库

```bash
pip install ezodf     # ODF handling
pip install odfpy     # ODF manipulation
```

## 最佳实践

1. 使用幻灯片母版保证风格一致
2. 为重复使用的演示文稿创建模板
3. 嵌入字体以便 PDF 分发
4. 尽可能使用矢量图形
5. 将 ODP 源文件纳入版本控制
6. 充分测试转换结果
7. 控制文件大小在合理范围

## 故障排查

### 无法打开 socket
```bash
killall soffice.bin
soffice --headless --accept="socket,host=localhost,port=8100;urp;"
```

## 资源

- [LibreOffice Impress Guide](https://documentation.libreoffice.org/)
- [UNO API Reference](https://api.libreoffice.org/)

## 相关技能

- writer
- calc
- draw
- base
- pptx-official
- workflow-automation

## 使用限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出替代针对具体环境的验证、测试或专家审查。
- 若缺少必要输入、权限、安全边界或成功标准，请停下来向用户确认。
