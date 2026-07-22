---
name: office-productivity
description: "办公效率工作流，涵盖文档创建、电子表格自动化、演示文稿生成，以及与 LibreOffice 和 Microsoft Office 格式的集成。当用户要求办公自动化、文档处理、电子表格操作、演示文稿制作或格式转换时使用。"
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# 办公效率工作流包

## 概述

覆盖文档创建、电子表格自动化、演示文稿生成及格式转换的综合办公效率工作流，基于 LibreOffice 和 Microsoft Office 工具链。

## 适用场景

适用于以下任务：
- 以编程方式创建办公文档
- 自动化文档工作流
- 文档格式互转
- 生成报告
- 从数据生成演示文稿
- 处理电子表格

## 工作流阶段

### 阶段 1：文档创建

#### 可调用技能
- `libreoffice-writer` - LibreOffice Writer
- `docx-official` - Microsoft Word
- `pdf-official` - PDF 处理

#### 操作步骤
1. 设计文档模板
2. 创建文档结构
3. 以编程方式填充内容
4. 应用格式
5. 导出为目标格式

#### 即用提示词
```
Use @libreoffice-writer to create ODT documents
```

```
Use @docx-official to create Word documents
```

### 阶段 2：电子表格自动化

#### 可调用技能
- `libreoffice-calc` - LibreOffice Calc
- `xlsx-official` - Excel 电子表格
- `googlesheets-automation` - Google Sheets

#### 操作步骤
1. 设计电子表格结构
2. 创建公式
3. 导入数据
4. 生成图表
5. 导出报告

#### 即用提示词
```
Use @libreoffice-calc to create ODS spreadsheets
```

```
Use @xlsx-official to create Excel reports
```

### 阶段 3：演示文稿生成

#### 可调用技能
- `libreoffice-impress` - LibreOffice Impress
- `pptx-official` - PowerPoint
- `frontend-slides` - HTML slides
- `nanobanana-ppt-skills` - AI PPT 生成

#### 操作步骤
1. 设计幻灯片模板
2. 从数据生成幻灯片
3. 添加图表和图形
4. 应用动画
5. 导出演示文稿

#### 即用提示词
```
Use @libreoffice-impress to create ODP presentations
```

```
Use @pptx-official to create PowerPoint presentations
```

```
Use @frontend-slides to create HTML presentations
```

### 阶段 4：格式转换

#### 可调用技能
- `libreoffice-writer` - 文档转换
- `libreoffice-calc` - 电子表格转换
- `pdf-official` - PDF 转换

#### 操作步骤
1. 识别源格式
2. 选择目标格式
3. 执行转换
4. 验证质量
5. 批量处理文件

#### 即用提示词
```
Use @libreoffice-writer to convert documents
```

### 阶段 5：文档自动化

#### 可调用技能
- `libreoffice-writer` - 邮件合并
- `workflow-automation` - 工作流自动化
- `file-organizer` - 文件整理

#### 操作步骤
1. 设计自动化工作流
2. 创建模板
3. 配置数据源
4. 生成文档
5. 分发输出

#### 即用提示词
```
Use @libreoffice-writer to perform mail merge
```

```
Use @workflow-automation to automate document workflows
```

### 阶段 6：图形与图表

#### 可调用技能
- `libreoffice-draw` - 矢量图形
- `canvas-design` - Canvas 设计
- `mermaid-expert` - 图表生成

#### 操作步骤
1. 设计图形
2. 创建图表
3. 生成图形
4. 导出图片
5. 与文档集成

#### 即用提示词
```
Use @libreoffice-draw to create vector graphics
```

```
Use @mermaid-expert to create diagrams
```

### 阶段 7：数据库集成

#### 可调用技能
- `libreoffice-base` - LibreOffice Base
- `database-architect` - 数据库设计

#### 操作步骤
1. 连接数据源
2. 创建表单
3. 设计报表
4. 自动化查询
5. 生成输出

#### 即用提示词
```
Use @libreoffice-base to create database reports
```

## 办公应用工作流

### LibreOffice
```
Skills: libreoffice-writer, libreoffice-calc, libreoffice-impress, libreoffice-draw, libreoffice-base
Formats: ODT, ODS, ODP, ODG, ODB
```

### Microsoft Office
```
Skills: docx-official, xlsx-official, pptx-official
Formats: DOCX, XLSX, PPTX
```

### Google Workspace
```
Skills: googlesheets-automation, google-drive-automation, gmail-automation
Formats: Google Docs, Sheets, Slides
```

## 质量门禁

- [ ] 文档格式正确
- [ ] 公式正常运行
- [ ] 演示文稿完整
- [ ] 转换成功
- [ ] 自动化已测试
- [ ] 文件已整理

## 相关工作流包

- `development` - 应用开发
- `documentation` - 文档生成
- `database` - 数据集成

## 使用限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来要求澄清。