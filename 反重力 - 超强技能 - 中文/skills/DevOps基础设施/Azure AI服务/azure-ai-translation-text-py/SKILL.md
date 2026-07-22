---
name: azure-ai-translation-text-py
description: Azure AI 文本翻译 Python SDK，用于实时文本翻译、音译、语言检测和字典查询。适用于应用程序中的文本内容翻译。触发词：Azure翻译、文本翻译、Azure Translator、多语言翻译、实时翻译、语言检测、音译、字典查询、translate、transliterate、Azure AI翻译
risk: unknown
source: community
date_added: '2026-02-27'
---

# Azure AI Text Translation SDK for Python

Azure AI Translator 文本翻译服务的客户端库，用于实时文本翻译、音译和语言操作。

## 安装

```bash
pip install azure-ai-translation-text
```

## 环境变量

```bash
AZURE_TRANSLATOR_KEY=<your-api-key>
AZURE_TRANSLATOR_REGION=<your-region>  # e.g., eastus, westus2
# Or use custom endpoint
AZURE_TRANSLATOR_ENDPOINT=https://<resource>.cognitiveservices.azure.com
```

## 身份验证

### API 密钥与区域

```python
import os
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

key = os.environ["AZURE_TRANSLATOR_KEY"]
region = os.environ["AZURE_TRANSLATOR_REGION"]

# Create credential with region
credential = AzureKeyCredential(key)
client = TextTranslationClient(credential=credential, region=region)
```

### API 密钥与自定义端点

```python
endpoint = os.environ["AZURE_TRANSLATOR_ENDPOINT"]

client = TextTranslationClient(
    credential=AzureKeyCredential(key),
    endpoint=endpoint
)
```

### Entra ID（推荐）

```python
from azure.ai.translation.text import TextTranslationClient
from azure.identity import DefaultAzureCredential

client = TextTranslationClient(
    credential=DefaultAzureCredential(),
    endpoint=os.environ["AZURE_TRANSLATOR_ENDPOINT"]
)
```

## 基础翻译

```python
# Translate to a single language
result = client.translate(
    body=["Hello, how are you?", "Welcome to Azure!"],
    to=["es"]  # Spanish
)

for item in result:
    for translation in item.translations:
        print(f"Translated: {translation.text}")
        print(f"Target language: {translation.to}")
```

## 翻译为多种语言

```python
result = client.translate(
    body=["Hello, world!"],
    to=["es", "fr", "de", "ja"]  # Spanish, French, German, Japanese
)

for item in result:
    print(f"Source: {item.detected_language.language if item.detected_language else 'unknown'}")
    for translation in item.translations:
        print(f"  {translation.to}: {translation.text}")
```

## 指定源语言

```python
result = client.translate(
    body=["Bonjour le monde"],
    from_parameter="fr",  # Source is French
    to=["en", "es"]
)
```

## 语言检测

```python
result = client.translate(
    body=["Hola, como estas?"],
    to=["en"]
)

for item in result:
    if item.detected_language:
        print(f"Detected language: {item.detected_language.language}")
        print(f"Confidence: {item.detected_language.score:.2f}")
```

## 音译

将文本从一种脚本转换为另一种脚本：

```python
result = client.transliterate(
    body=["konnichiwa"],
    language="ja",
    from_script="Latn",  # From Latin script
    to_script="Jpan"      # To Japanese script
)

for item in result:
    print(f"Transliterated: {item.text}")
    print(f"Script: {item.script}")
```

## 字典查询

查找替代翻译和定义：

```python
result = client.lookup_dictionary_entries(
    body=["fly"],
    from_parameter="en",
    to="es"
)

for item in result:
    print(f"Source: {item.normalized_source} ({item.display_source})")
    for translation in item.translations:
        print(f"  Translation: {translation.normalized_target}")
        print(f"  Part of speech: {translation.pos_tag}")
        print(f"  Confidence: {translation.confidence:.2f}")
```

## 字典示例

获取翻译的使用示例：

```python
from azure.ai.translation.text.models import DictionaryExampleTextItem

result = client.lookup_dictionary_examples(
    body=[DictionaryExampleTextItem(text="fly", translation="volar")],
    from_parameter="en",
    to="es"
)

for item in result:
    for example in item.examples:
        print(f"Source: {example.source_prefix}{example.source_term}{example.source_suffix}")
        print(f"Target: {example.target_prefix}{example.target_term}{example.target_suffix}")
```

## 获取支持的语言

```python
# Get all supported languages
languages = client.get_supported_languages()

# Translation languages
print("Translation languages:")
for code, lang in languages.translation.items():
    print(f"  {code}: {lang.name} ({lang.native_name})")

# Transliteration languages
print("\nTransliteration languages:")
for code, lang in languages.transliteration.items():
    print(f"  {code}: {lang.name}")
    for script in lang.scripts:
        print(f"    {script.code} -> {[t.code for t in script.to_scripts]}")

# Dictionary languages
print("\nDictionary languages:")
for code, lang in languages.dictionary.items():
    print(f"  {code}: {lang.name}")
```

## 断句

识别句子边界：

```python
result = client.find_sentence_boundaries(
    body=["Hello! How are you? I hope you are well."],
    language="en"
)

for item in result:
    print(f"Sentence lengths: {item.sent_len}")
```

## 翻译选项

```python
result = client.translate(
    body=["Hello, world!"],
    to=["de"],
    text_type="html",           # "plain" or "html"
    profanity_action="Marked",  # "NoAction", "Deleted", "Marked"
    profanity_marker="Asterisk", # "Asterisk", "Tag"
    include_alignment=True,      # Include word alignment
    include_sentence_length=True # Include sentence boundaries
)

for item in result:
    translation = item.translations[0]
    print(f"Translated: {translation.text}")
    if translation.alignment:
        print(f"Alignment: {translation.alignment.proj}")
    if translation.sent_len:
        print(f"Sentence lengths: {translation.sent_len.src_sent_len}")
```

## 异步客户端

```python
from azure.ai.translation.text.aio import TextTranslationClient
from azure.core.credentials import AzureKeyCredential

async def translate_text():
    async with TextTranslationClient(
        credential=AzureKeyCredential(key),
        region=region
    ) as client:
        result = await client.translate(
            body=["Hello, world!"],
            to=["es"]
        )
        print(result[0].translations[0].text)
```

## 客户端方法

| 方法 | 描述 |
|--------|-------------|
| `translate` | 将文本翻译为一种或多种语言 |
| `transliterate` | 在脚本之间转换文本 |
| `detect` | 检测文本的语言 |
| `find_sentence_boundaries` | 识别句子边界 |
| `lookup_dictionary_entries` | 字典查询翻译 |
| `lookup_dictionary_examples` | 获取使用示例 |
| `get_supported_languages` | 列出支持的语言 |

## 最佳实践

1. **批量翻译** — 在一个请求中发送多个文本（最多 100 个）
2. **指定源语言** — 已知时指定源语言以提高准确性
3. **使用异步客户端** — 适用于高吞吐量场景
4. **缓存语言列表** — 支持的语言不常变化
5. **适当处理敏感内容** — 根据应用程序需求处理
6. **翻译 HTML 内容时使用 html 文本类型**
7. **包含对齐信息** — 用于需要词汇映射的应用程序

## 适用场景
此技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
