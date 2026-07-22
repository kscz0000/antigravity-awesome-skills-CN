---
name: azure-ai-contentunderstanding-py
description: Azure AI Content Understanding Python SDK。用于从文档、图像、音频和视频文件中提取多模态内容。触发词：Azure内容理解、多模态内容提取、文档分析、视频分析、音频转录、图像内容提取、Content Understanding、Azure AI、RAG内容提取
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure AI Content Understanding SDK for Python

多模态 AI 服务，从文档、视频、音频和图像文件中提取语义内容，用于 RAG 和自动化工作流。

## 安装

```bash
pip install azure-ai-contentunderstanding
```

## 环境变量

```bash
CONTENTUNDERSTANDING_ENDPOINT=https://<resource>.cognitiveservices.azure.com/
```

## 身份认证

```python
import os
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.identity import DefaultAzureCredential

endpoint = os.environ["CONTENTUNDERSTANDING_ENDPOINT"]
credential = DefaultAzureCredential()
client = ContentUnderstandingClient(endpoint=endpoint, credential=credential)
```

## 核心工作流

Content Understanding 操作是异步长时间运行的操作：

1. **开始分析** — 使用 `begin_analyze()` 启动分析操作（返回轮询器）
2. **轮询结果** — 轮询直到分析完成（SDK 通过 `.result()` 处理）
3. **处理结果** — 从 `AnalyzeResult.contents` 提取结构化结果

## 预置分析器

| 分析器 | 内容类型 | 用途 |
|----------|--------------|---------|
| `prebuilt-documentSearch` | 文档 | 为 RAG 应用提取 markdown |
| `prebuilt-imageSearch` | 图像 | 从图像中提取内容 |
| `prebuilt-audioSearch` | 音频 | 带时间戳的音频转录 |
| `prebuilt-videoSearch` | 视频 | 提取帧、转录、摘要 |
| `prebuilt-invoice` | 文档 | 提取发票字段 |

## 分析文档

```python
import os
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalyzeInput
from azure.identity import DefaultAzureCredential

endpoint = os.environ["CONTENTUNDERSTANDING_ENDPOINT"]
client = ContentUnderstandingClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential()
)

# 从 URL 分析文档
poller = client.begin_analyze(
    analyzer_id="prebuilt-documentSearch",
    inputs=[AnalyzeInput(url="https://example.com/document.pdf")]
)

result = poller.result()

# 访问 markdown 内容（contents 是列表）
content = result.contents[0]
print(content.markdown)
```

## 访问文档内容详情

```python
from azure.ai.contentunderstanding.models import MediaContentKind, DocumentContent

content = result.contents[0]
if content.kind == MediaContentKind.DOCUMENT:
    document_content: DocumentContent = content  # type: ignore
    print(document_content.start_page_number)
```

## 分析图像

```python
from azure.ai.contentunderstanding.models import AnalyzeInput

poller = client.begin_analyze(
    analyzer_id="prebuilt-imageSearch",
    inputs=[AnalyzeInput(url="https://example.com/image.jpg")]
)
result = poller.result()
content = result.contents[0]
print(content.markdown)
```

## 分析视频

```python
from azure.ai.contentunderstanding.models import AnalyzeInput

poller = client.begin_analyze(
    analyzer_id="prebuilt-videoSearch",
    inputs=[AnalyzeInput(url="https://example.com/video.mp4")]
)

result = poller.result()

# 访问视频内容（AudioVisualContent）
content = result.contents[0]

# 获取带时间戳的转录短语
for phrase in content.transcript_phrases:
    print(f"[{phrase.start_time} - {phrase.end_time}]: {phrase.text}")

# 获取关键帧（视频）
for frame in content.key_frames:
    print(f"Frame at {frame.time}: {frame.description}")
```

## 分析音频

```python
from azure.ai.contentunderstanding.models import AnalyzeInput

poller = client.begin_analyze(
    analyzer_id="prebuilt-audioSearch",
    inputs=[AnalyzeInput(url="https://example.com/audio.mp3")]
)

result = poller.result()

# 访问音频转录
content = result.contents[0]
for phrase in content.transcript_phrases:
    print(f"[{phrase.start_time}] {phrase.text}")
```

## 自定义分析器

使用字段架构创建自定义分析器进行专业提取：

```python
# 创建自定义分析器
analyzer = client.create_analyzer(
    analyzer_id="my-invoice-analyzer",
    analyzer={
        "description": "Custom invoice analyzer",
        "base_analyzer_id": "prebuilt-documentSearch",
        "field_schema": {
            "fields": {
                "vendor_name": {"type": "string"},
                "invoice_total": {"type": "number"},
                "line_items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "amount": {"type": "number"}
                        }
                    }
                }
            }
        }
    }
)

# 使用自定义分析器
from azure.ai.contentunderstanding.models import AnalyzeInput

poller = client.begin_analyze(
    analyzer_id="my-invoice-analyzer",
    inputs=[AnalyzeInput(url="https://example.com/invoice.pdf")]
)

result = poller.result()

# 访问提取的字段
print(result.fields["vendor_name"])
print(result.fields["invoice_total"])
```

## 分析器管理

```python
# 列出所有分析器
analyzers = client.list_analyzers()
for analyzer in analyzers:
    print(f"{analyzer.analyzer_id}: {analyzer.description}")

# 获取特定分析器
analyzer = client.get_analyzer("prebuilt-documentSearch")

# 删除自定义分析器
client.delete_analyzer("my-custom-analyzer")
```

## 异步客户端

```python
import asyncio
import os
from azure.ai.contentunderstanding.aio import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalyzeInput
from azure.identity.aio import DefaultAzureCredential

async def analyze_document():
    endpoint = os.environ["CONTENTUNDERSTANDING_ENDPOINT"]
    credential = DefaultAzureCredential()
    
    async with ContentUnderstandingClient(
        endpoint=endpoint,
        credential=credential
    ) as client:
        poller = await client.begin_analyze(
            analyzer_id="prebuilt-documentSearch",
            inputs=[AnalyzeInput(url="https://example.com/doc.pdf")]
        )
        result = await poller.result()
        content = result.contents[0]
        return content.markdown

asyncio.run(analyze_document())
```

## 内容类型

| 类 | 用于 | 提供 |
|-------|-----|----------|
| `DocumentContent` | PDF、图像、Office 文档 | 页面、表格、图形、段落 |
| `AudioVisualContent` | 音频、视频文件 | 转录短语、时间戳、关键帧 |

两者都继承自 `MediaContent`，提供基本信息和 markdown 表示。

## 模型导入

```python
from azure.ai.contentunderstanding.models import (
    AnalyzeInput,
    AnalyzeResult,
    MediaContentKind,
    DocumentContent,
    AudioVisualContent,
)
```

## 客户端类型

| 客户端 | 用途 |
|--------|---------|
| `ContentUnderstandingClient` | 同步客户端，用于所有操作 |
| `ContentUnderstandingClient` (aio) | 异步客户端，用于所有操作 |

## 最佳实践

1. **使用 `begin_analyze` 和 `AnalyzeInput`** — 这是正确的方法签名
2. **通过 `result.contents[0]` 访问结果** — 结果以列表形式返回
3. **使用预置分析器** 处理常见场景（文档/图像/音频/视频搜索）
4. **创建自定义分析器** 仅用于领域特定的字段提取
5. **使用异步客户端** 处理高吞吐量场景，配合 `azure.identity.aio` 凭证
6. **处理长时间运行的操作** — 视频/音频分析可能需要数分钟
7. **尽可能使用 URL 源** 以避免上传开销

## 适用场景
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
