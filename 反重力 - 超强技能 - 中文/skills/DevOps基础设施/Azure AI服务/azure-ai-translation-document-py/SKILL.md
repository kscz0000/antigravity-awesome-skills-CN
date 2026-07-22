---
name: azure-ai-translation-document-py
description: Azure AI 文档翻译 Python SDK，用于批量翻译文档并保留格式。支持 Word、PDF、Excel、PowerPoint 等文档格式的大规模翻译。触发词：Azure文档翻译、批量文档翻译、文档翻译SDK、Word翻译、PDF翻译、Excel翻译、PPT翻译、保留格式翻译、Azure Translator、document translation、批量翻译文档。
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure AI 文档翻译 Python SDK

Azure AI Translator 文档翻译服务的客户端库，用于批量文档翻译并保留格式。

## 安装

```bash
pip install azure-ai-translation-document
```

## 环境变量

```bash
AZURE_DOCUMENT_TRANSLATION_ENDPOINT=https://<resource>.cognitiveservices.azure.com
AZURE_DOCUMENT_TRANSLATION_KEY=<your-api-key>  # 如果使用 API 密钥

# 源文档和目标文档的存储容器
AZURE_SOURCE_CONTAINER_URL=https://<storage>.blob.core.windows.net/<container>?<sas>
AZURE_TARGET_CONTAINER_URL=https://<storage>.blob.core.windows.net/<container>?<sas>
```

## 身份验证

### API 密钥

```python
import os
from azure.ai.translation.document import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential

endpoint = os.environ["AZURE_DOCUMENT_TRANSLATION_ENDPOINT"]
key = os.environ["AZURE_DOCUMENT_TRANSLATION_KEY"]

client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))
```

### Entra ID（推荐）

```python
from azure.ai.translation.document import DocumentTranslationClient
from azure.identity import DefaultAzureCredential

client = DocumentTranslationClient(
    endpoint=os.environ["AZURE_DOCUMENT_TRANSLATION_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

## 基本文档翻译

```python
from azure.ai.translation.document import DocumentTranslationInput, TranslationTarget

source_url = os.environ["AZURE_SOURCE_CONTAINER_URL"]
target_url = os.environ["AZURE_TARGET_CONTAINER_URL"]

# 启动翻译任务
poller = client.begin_translation(
    inputs=[
        DocumentTranslationInput(
            source_url=source_url,
            targets=[
                TranslationTarget(
                    target_url=target_url,
                    language="es"  # 翻译为西班牙语
                )
            ]
        )
    ]
)

# 等待完成
result = poller.result()

print(f"状态: {poller.status()}")
print(f"已翻译文档: {poller.details.documents_succeeded_count}")
print(f"失败文档: {poller.details.documents_failed_count}")
```

## 多目标语言翻译

```python
poller = client.begin_translation(
    inputs=[
        DocumentTranslationInput(
            source_url=source_url,
            targets=[
                TranslationTarget(target_url=target_url_es, language="es"),
                TranslationTarget(target_url=target_url_fr, language="fr"),
                TranslationTarget(target_url=target_url_de, language="de")
            ]
        )
    ]
)
```

## 翻译单个文档

```python
from azure.ai.translation.document import SingleDocumentTranslationClient

single_client = SingleDocumentTranslationClient(endpoint, AzureKeyCredential(key))

with open("document.docx", "rb") as f:
    document_content = f.read()

result = single_client.translate(
    body=document_content,
    target_language="es",
    content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)

# 保存翻译后的文档
with open("document_es.docx", "wb") as f:
    f.write(result)
```

## 检查翻译状态

```python
# 获取所有翻译操作
operations = client.list_translation_statuses()

for op in operations:
    print(f"操作 ID: {op.id}")
    print(f"状态: {op.status}")
    print(f"创建时间: {op.created_on}")
    print(f"文档总数: {op.documents_total_count}")
    print(f"成功: {op.documents_succeeded_count}")
    print(f"失败: {op.documents_failed_count}")
```

## 列出文档状态

```python
# 获取任务中各个文档的状态
operation_id = poller.id
document_statuses = client.list_document_statuses(operation_id)

for doc in document_statuses:
    print(f"文档: {doc.source_document_url}")
    print(f"  状态: {doc.status}")
    print(f"  翻译为: {doc.translated_to}")
    if doc.error:
        print(f"  错误: {doc.error.message}")
```

## 取消翻译

```python
# 取消正在进行的翻译
client.cancel_translation(operation_id)
```

## 使用术语表

```python
from azure.ai.translation.document import TranslationGlossary

poller = client.begin_translation(
    inputs=[
        DocumentTranslationInput(
            source_url=source_url,
            targets=[
                TranslationTarget(
                    target_url=target_url,
                    language="es",
                    glossaries=[
                        TranslationGlossary(
                            glossary_url="https://<storage>.blob.core.windows.net/glossary/terms.csv?<sas>",
                            file_format="csv"
                        )
                    ]
                )
            ]
        )
    ]
)
```

## 支持的文档格式

```python
# 获取支持的格式
formats = client.get_supported_document_formats()

for fmt in formats:
    print(f"格式: {fmt.format}")
    print(f"  扩展名: {fmt.file_extensions}")
    print(f"  内容类型: {fmt.content_types}")
```

## 支持的语言

```python
# 获取支持的语言
languages = client.get_supported_languages()

for lang in languages:
    print(f"语言: {lang.name} ({lang.code})")
```

## 异步客户端

```python
from azure.ai.translation.document.aio import DocumentTranslationClient
from azure.identity.aio import DefaultAzureCredential

async def translate_documents():
    async with DocumentTranslationClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential()
    ) as client:
        poller = await client.begin_translation(inputs=[...])
        result = await poller.result()
```

## 支持的格式

| 类别 | 格式 |
|------|------|
| 文档 | DOCX, PDF, PPTX, XLSX, HTML, TXT, RTF |
| 结构化数据 | CSV, TSV, JSON, XML |
| 本地化 | XLIFF, XLF, MHTML |

## 存储要求

- 源容器和目标容器必须是 Azure Blob Storage
- 使用具有适当权限的 SAS 令牌：
  - 源容器：读取、列出
  - 目标容器：写入、列出

## 最佳实践

1. **使用 SAS 令牌**并仅授予最低必要权限
2. **监控长时间运行的操作**，使用 `poller.status()`
3. **处理文档级错误**，通过遍历文档状态
4. **使用术语表**处理领域特定术语
5. **为每种语言使用独立的目标容器**
6. **使用异步客户端**处理多个并发任务
7. **提交文档前检查支持的格式**

## 适用场景
本技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 输出内容不应替代针对特定环境的验证、测试或专家评审。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
