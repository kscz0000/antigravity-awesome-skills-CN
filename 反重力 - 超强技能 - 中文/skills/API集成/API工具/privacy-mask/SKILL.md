---
name: privacy-mask
description: 对截图和图像中的敏感信息（PII）进行遮盖、脱敏、匿名化和审查——电话号码、邮箱、身份证号、API密钥、加密钱包、信用卡、密码等。使用OCR（Tesseract + RapidOCR）配合47条正则规则及可选NER（GLiNER）检测隐私数据。触发词：隐私遮盖、脱敏处理、PII遮盖、截图打码、敏感信息屏蔽、图像匿名化、隐私保护、redact、anonymize、mask PII、隐私审查。
risk: unknown
source: https://github.com/fullstackcrew-alpha/privacy-mask/tree/main/
source_repo: fullstackcrew-alpha/privacy-mask
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/fullstackcrew-alpha/privacy-mask/blob/main/LICENSE
---

# 隐私遮盖

在图像离开你的机器之前，本地检测并遮盖其中的敏感信息。

## 前置条件

本技能要求系统已预装 `privacy-mask` CLI。
如未安装，请告知用户需先完成安装：

1. 通过 pip 安装：`pip install privacy-mask`
2. 确保 Tesseract OCR 已安装：`brew install tesseract`（macOS）或 `apt install tesseract-ocr`（Linux）
3. 验证安装：`privacy-mask --version`
4. （可选）安装 NER 支持：`pip install privacy-mask[ner]`

## 何时使用

- 用户发送了可能包含隐私数据的截图或图像文件（`.png`、`.jpg`、`.jpeg`、`.bmp`、`.tiff`）
- 用户提及隐私、遮盖、脱敏或匿名化
- 你需要分析图像但希望先遮盖敏感信息
- 如果用户分享了用于调试的截图，则先运行 `privacy-mask mask <path> --dry-run` 检查 PII
- 如果检测到结果，则在继续分析之前遮盖图像

## 用法

遮盖图像：
```bash
privacy-mask mask /path/to/screenshot.png
privacy-mask mask /path/to/screenshot.png --in-place
privacy-mask mask /path/to/screenshot.png --dry-run   # 仅检测，不遮盖
privacy-mask mask /path/to/screenshot.png --detection-engine regex  # 仅使用正则，跳过 NER
privacy-mask mask /path/to/screenshot.png --config /path/to/custom-config.json
```

输出为 JSON：
```json
{
  "status": "success",
  "detections": [{"label": "PHONE_CN", "text": "***", "bbox": [10, 20, 100, 30]}],
  "summary": "Masked 1 regions: 1 PHONE_CN"
}
```

### 示例工作流

1. 用户提供截图：`~/Desktop/error-screenshot.png`
2. 运行检测：`privacy-mask mask ~/Desktop/error-screenshot.png --dry-run`
3. 如果检测到结果，遮盖图像：`privacy-mask mask ~/Desktop/error-screenshot.png`
4. 遮盖后的输出保存为 `~/Desktop/error-screenshot_masked.png`
5. 使用遮盖后的图像进行后续分析

## 检测范围

- **身份证件**：中国身份证、护照、港澳台证件、美国SSN、英国NINO、加拿大SIN、印度Aadhaar/PAN、韩国RRN、新加坡NRIC、马来西亚IC
- **电话**：中国手机/座机、美国电话、国际号码（+前缀）
- **金融**：银行卡、Amex、IBAN、SWIFT/BIC
- **开发者密钥**：AWS、GitHub、Slack、Google、Stripe令牌、JWT、连接字符串、API密钥、SSH/PEM密钥
- **加密货币**：Bitcoin、Ethereum钱包地址
- **其他**：邮箱、生日、IP/IPv6、MAC、UUID、车牌、MRZ、URL认证令牌
- **NER**（可选）：人名、街道地址、组织、出生日期、医疗状况

## 约束

- 不得将未遮盖的图像发送到任何外部API或云服务
- 检测到结果时不得跳过遮盖——分享前必须遮盖
- 不得修改原始图像，除非明确请求使用 `--in-place`
- 处理超大图像（>10MB）时需先警告用户处理时间

## 反模式

- **不要假设图像是安全的**——即使图像"看起来干净"也要运行检测
- **不要默认使用 `--in-place`**——除非用户另有要求，否则保留原始文件
- **不要忽略试运行结果**——如果 `--dry-run` 发现了 PII，图像在使用前必须遮盖
- **不要硬编码配置路径**——使用捆绑的默认配置或让用户指定 `--config`

## 重要说明

- 所有处理均为**本地离线**——数据不会离开本机
- 通过捆绑的 `config.json` 配置规则，或使用 `--config` 传入自定义规则

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时才使用本技能。
- 在应用更改之前，请验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定的测试、安全审查，或用户对破坏性/高成本操作的批准。
