---
name: akf-trust-metadata
description: "AI 原生文件格式。AI 的 EXIF — 为每个文件标记信任分数、来源溯源和合规元数据。嵌入 20+ 种格式（DOCX、PDF、图像、代码）。支持 EU AI Act、SOX、HIPAA 审计。触发词：AKF、信任元数据、来源溯源、合规元数据、AI文件格式、provenance、trust metadata、compliance metadata"
risk: safe
source: community
date_added: "2026-03-27"
author: HMAKT99
tags:
- trust
- metadata
- provenance
- compliance
- file-format
- ai-native
---

# AKF — AI 原生文件格式

每张照片都有 EXIF。每首歌都有 ID3。AKF 是 AI 生成内容的原生元数据格式。

## 何时使用
当您需要为 AI 生成或 AI 修改的文件标记、检查或审计来源溯源和信任元数据，用于合规、审查或交接工作流时，使用此技能。

## 创建或修改文件后

```bash
akf stamp <file> --agent <agent-name> --evidence "<what you did>"
```

证据示例：
- "generated from user prompt"
- "refactored existing code"
- "tests pass"
- "docs reviewed"

## 修改现有文件前

```bash
akf read <file>          # 检查现有信任元数据
akf inspect <file>       # 查看详细信任分数
```

## 合规审计

```bash
akf audit <file> --regulation eu_ai_act    # EU AI Act Article 50
akf audit <file> --regulation hipaa         # HIPAA
akf audit <file> --regulation sox           # SOX
akf audit <file> --regulation nist_ai       # NIST AI RMF
```

## 分类

- `--label confidential` 用于财务/机密/内部路径
- `--label public` 用于 README、文档、示例
- 默认：`internal`

## 安装

```bash
pip install akf
```

## 链接

- https://akf.dev
- https://github.com/HMAKT99/AKF
- npm: `npm install akf-format`

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
