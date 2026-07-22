---
name: draw
description: "使用 LibreOffice Draw 进行矢量图形与图表创建，以及 ODG/SVG/PDF 格式转换。涉及矢量图形、ODG 转换、SVG、PDF、流程图、技术绘图、UNO 自动化时使用。"
category: graphics-processing
risk: safe
source: personal
date_added: "2026-02-27"
---

# LibreOffice Draw

## 概述

LibreOffice Draw 技能，基于原生 ODG（OpenDocument Drawing）格式，用于矢量图形与图表工作流的创建、编辑、转换与自动化处理。

## 适用场景

以下情况使用本技能：
- 以 ODG 格式创建矢量图形与图表
- 在 ODG、SVG、PDF、PNG 格式之间转换
- 自动化生成图表与流程图
- 创建技术图纸与示意图
- 批量处理图形操作

## 核心能力

### 1. 图形创建
- 从零开始创建新的 ODG 绘图
- 基于模板生成图表
- 创建流程图与组织结构图
- 设计技术图纸

### 2. 格式转换
- ODG 转其他格式：SVG、PDF、PNG、JPG
- 其他格式转 ODG：SVG、PDF
- 多文件批量转换

### 3. 图表自动化
- 基于模板的图表生成
- 自动化流程图创建
- 动态形状生成
- 批量图表生产

### 4. 图形操作
- 形状创建与操作
- 路径与贝塞尔曲线编辑
- 图层管理
- 文字与标签插入

### 5. 集成能力
- 通过 soffice 进行命令行自动化
- 使用 UNO 进行 Python 脚本编写
- 与工作流工具集成

## 工作流

### 创建新绘图

#### 方式一：命令行
```bash
soffice --draw template.odg
```

#### 方式二：Python + UNO
```python
import uno

def create_drawing():
    local_ctx = uno.getComponentContext()
    resolver = local_ctx.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", local_ctx
    )
    ctx = resolver.resolve(
        "uno:socket,host=localhost,port=8100;urp;StarOffice.ComponentContext"
    )
    smgr = ctx.ServiceManager
    doc = smgr.createInstanceWithContext("com.sun.star.drawing.DrawingDocument", ctx)
    page = doc.getDrawPages().getByIndex(0)
    doc.storeToURL("file:///path/to/drawing.odg", ())
    doc.close(True)
```

### 转换绘图

```bash
# ODG to SVG
soffice --headless --convert-to svg drawing.odg

# ODG to PDF
soffice --headless --convert-to pdf drawing.odg

# ODG to PNG
soffice --headless --convert-to png:PNG_drawing drawing.odg

# SVG to ODG
soffice --headless --convert-to odg drawing.svg

# Batch convert
for file in *.odg; do
    soffice --headless --convert-to pdf "$file"
done
```

## 格式转换参考

### 支持的输入格式
- ODG（原生）、SVG、PDF

### 支持的输出格式
- ODG、SVG、PDF、PNG、JPG、GIF、BMP、WMF、EMF

## 命令行参考

```bash
soffice --headless
soffice --headless --convert-to <format> <file>
soffice --draw  # Draw
```

## Python 库

```bash
pip install ezodf     # ODF handling
pip install odfpy     # ODF manipulation
pip install svgwrite  # SVG generation
```

## 最佳实践

1. 使用图层进行组织管理
2. 为重复使用的图表创建模板
3. 使用矢量格式以保证可缩放性
4. 为对象命名以便引用
5. 将 ODG 源文件纳入版本控制
6. 充分测试转换效果
7. 导出为 SVG 用于 Web 展示

## 故障排查

### 无法打开套接字
```bash
killall soffice.bin
soffice --headless --accept="socket,host=localhost,port=8100;urp;"
```

### PNG 导出的质量问题
```bash
soffice --headless --convert-to png:PNG_drawing_Export \
  --filterData='{"Width":2048,"Height":2048}' drawing.odg
```

## 参考资源

- [LibreOffice Draw Guide](https://documentation.libreoffice.org/)
- [UNO API Reference](https://api.libreoffice.org/)
- [SVG Specification](https://www.w3.org/TR/SVG/)

## 相关技能

- writer
- calc
- impress
- base
- workflow-automation

## 使用限制
- 仅当任务明确匹配上述范围时使用本技能。
- 输出结果不能替代环境相关的验证、测试或专家评审。
- 若缺少必需的输入、权限、安全边界或成功标准，请主动停下并请求澄清。
