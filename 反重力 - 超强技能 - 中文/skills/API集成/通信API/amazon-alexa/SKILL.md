---
name: amazon-alexa
description: "Amazon Alexa 完整集成，用于创建智能语音技能、将 Alexa 转换为以 Claude 为大脑的助手（Auri 项目），以及与 AWS 生态系统集成（Lambda、DynamoDB、Polly、Transcribe、Lex、Smart Home）。触发词：Alexa 技能、语音助手、Alexa 开发、ASK CLI、智能音箱、Echo、语音交互、Auri 项目、Alexa Smart Home、AWS Lambda 语音"
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- voice
- alexa
- aws
- smart-home
- iot
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# AMAZON ALEXA — 使用 Claude 的智能语音

## 概述

Amazon Alexa 完整集成，用于创建智能语音技能、将 Alexa 转换为以 Claude 为大脑的助手（Auri 项目），以及与 AWS 生态系统集成（Lambda、DynamoDB、Polly、Transcribe、Lex、Smart Home）。

## 何时使用此技能

- 当你需要此领域的专业协助时

## 何时不使用此技能

- 任务与 Amazon Alexa 无关时
- 更简单、更具体的工具可以处理请求时
- 用户需要无领域专业知识的通用协助时

## 工作原理

> 你是 Alexa 和 AWS Voice 专家。使命：使用 Claude 作为 LLM 后端，
> 将任何 Alexa 设备转换为超智能助手，具备神经语音、持久记忆
> 和 Smart Home 控制。关键项目：AURI。

---

## 1. 生态系统概述

```
[Alexa Device] → [Alexa Cloud] → [AWS Lambda] → [Claude API]
    语音          转录            逻辑            智能
      ↑               ↑               ↑                ↑
   用户           Intent          Handler          Anthropic
                               + DynamoDB
                               + Polly TTS
                               + APL Visual
```

## Auri 架构组件

| 组件 | AWS 服务 | 功能 |
|------|----------|------|
| 语音 → 文本 | Alexa ASR 原生 | 语音识别 |
| NLU | ASK Interaction Model + Lex V2 | 提取 intent 和 slots |
| 后端 | AWS Lambda (Python/Node.js) | 逻辑和编排 |
| LLM | Claude API (Anthropic) | 智能和响应 |
| 持久化 | Amazon DynamoDB | 历史和偏好 |
| 文本 → 语音 | Amazon Polly (neural) | Auri 自然语音 |
| 可视化界面 | APL (Alexa Presentation Language) | Echo Show 屏幕 |
| Smart Home | Alexa Smart Home API | 设备控制 |
| 自动化 | Alexa Routines API | 智能例程 |

---

## 2.1 前置要求

```bash

## Ask Cli

npm install -g ask-cli
ask configure

## Aws Cli

pip install awscli
aws configure
```

## 使用模板创建 Skill

ask new \
  --template hello-world \
  --skill-name auri \
  --language pt-BR

## └── .Ask/Ask-Resources.Json

```

## 2.3 配置 Invocation Name

在文件 `models/pt-BR.json` 中：
```json
{
  "interactionModel": {
    "languageModel": {
      "invocationName": "auri"
    }
  }
}
```

---

## 3.1 Auri 核心 Intents

```json
{
  "interactionModel": {
    "languageModel": {
      "invocationName": "auri",
      "intents": [
        {"name": "AMAZON.HelpIntent"},
        {"name": "AMAZON.StopIntent"},
        {"name": "AMAZON.CancelIntent"},
        {"name": "AMAZON.FallbackIntent"},
        {
          "name": "ChatIntent",
          "slots": [{"name": "query", "type": "AMAZON.SearchQuery"}],
          "samples": [
            "{query}",
            "me ajuda com {query}",
            "quero saber sobre {query}",
            "o que voce sabe sobre {query}",
            "explique {query}",
            "pesquise {query}"
          ]
        },
        {
          "name": "SmartHomeIntent",
          "slots": [
            {"name": "device", "type": "AMAZON.Room"},
            {"name": "action", "type": "ActionType"}
          ],
          "samples": [
            "{action} a {device}",
            "controla {device}",
            "acende {device}",
            "apaga {device}"
          ]
        },
        {
          "name": "RoutineIntent",
          "slots": [{"name": "routine", "type": "RoutineType"}],
          "samples": [
            "ativa rotina {routine}",
            "executa {routine}",
            "modo {routine}"
          ]
        }
      ],
      "types": [
        {
          "name": "ActionType",
          "values": [
            {"name": {"value": "liga", "synonyms": ["acende", "ativa", "liga"]}},
            {"name": {"value": "desliga", "synonyms": ["apaga", "desativa", "desliga"]}}
          ]
        },
        {
          "name": "RoutineType",
          "values": [
            {"name": {"value": "bom dia", "synonyms": ["acordar", "manhã"]}},
            {"name": {"value": "boa noite", "synonyms": ["dormir", "descansar"]}},
            {"name": {"value": "trabalho", "synonyms": ["trabalhar", "foco"]}},
            {"name": {"value": "sair", "synonyms": ["saindo", "goodbye"]}}
          ]
        }
      ]
    }
  }
}
```

---

## 4.1 Python 主 Handler

```python
import os
import time
import anthropic
import boto3
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_model import Response
from ask_sdk_dynamodb_persistence_adapter import DynamoDbPersistenceAdapter

## ============================================================

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_handler(handler_input: HandlerInput) -> Response:
    attrs = handler_input.attributes_manager.persistent_attributes
    name = attrs.get("name", "")
    greeting = f"Oi{', ' + name if name else ''}! Eu sou a Auri. Como posso ajudar?"
    return (handler_input.response_builder
            .speak(greeting).ask("Em que posso ajudar?").response)


@sb.request_handler(can_handle_func=is_intent_name("ChatIntent"))
def chat_handler(handler_input: HandlerInput) -> Response:
    try:
        # Obter query
        slots = handler_input.request_envelope.request.intent.slots
        query = slots["query"].value if slots.get("query") else None
        if not query:
            return (handler_input.response_builder
                    .speak("Pode repetir? Nao entendi bem.").ask("Pode repetir?").response)

        # Carregar historico
        attrs = handler_input.attributes_manager.persistent_attributes
        history = attrs.get("history", [])

        # Montar mensagens para Claude
        messages = history[-MAX_HISTORY:]
        messages.append({"role": "user", "content": query})

        # Chamar Claude
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=512,
            system=AURI_SYSTEM_PROMPT,
            messages=messages
        )
        reply = response.content[0].text

        # Truncar para nao exceder timeout
        if len(reply) > MAX_RESPONSE_CHARS:
            reply = reply[:MAX_RESPONSE_CHARS] + "... Quer que eu continue?"

        # Salvar historico
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": reply})
        attrs["history"] = history[-50:]  # Manter ultimas 50
        handler_input.attributes_manager.persistent_attributes = attrs
        handler_input.attributes_manager.save_persist

## 4.2 Lambda 环境变量

```
ANTHROPIC_API_KEY=sk-...  (armazenar em Secrets Manager)
DYNAMODB_TABLE=auri-users
AWS_REGION=us-east-1
```

## 4.3 Requirements.Txt

```
ask-sdk-core>=1.19.0
ask-sdk-dynamodb-persistence-adapter>=1.19.0
anthropic>=0.40.0
boto3>=1.34.0
```

---

## 5.1 创建表

```bash
aws dynamodb create-table \
  --table-name auri-users \
  --attribute-definitions AttributeName=userId,AttributeType=S \
  --key-schema AttributeName=userId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

## 5.2 用户 Schema

```json
{
  "userId": "amzn1.ask.account.XXXXX",
  "name": "Joao",
  "history": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "preferences": {
    "language": "pt-BR",
    "voice": "Vitoria",
    "personality": "assistente profissional"
  },
  "smartHome": {
    "devices": {},
    "routines": {}
  },
  "updatedAt": 1740960000,
  "ttl": 1748736000
}
```

## 5.3 自动 TTL（过期旧数据）

```python
import time

## Adicionar Ttl De 180 Dias Ao Salvar

attrs["ttl"] = int(time.time()) + (180 * 24 * 3600)
```

---

## 6.1 可用语音（葡萄牙语）

| 语音 | 语言 | 类型 | 推荐 |
|------|------|------|------|
| `Vitoria` | pt-BR | Neural | ✅ Auri PT-BR |
| `Camila` | pt-BR | Neural | 备选 |
| `Ricardo` | pt-BR | Standard | 男声 |
| `Ines` | pt-PT | Neural | 葡萄牙 |

## 6.2 在响应中集成 Polly

```python
import boto3
import base64

def synthesize_polly(text: str, voice_id: str = "Vitoria") -> str:
    """Retorna URL de audio Polly para usar em Alexa."""
    client = boto3.client("polly", region_name="us-east-1")
    response = client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_id,
        Engine="neural"
    )
    # Salvar em S3 e retornar URL
    # (necessario para usar audio customizado no Alexa)
    return upload_to_s3(response["AudioStream"].read())

def speak_with_polly(handler_input, text, voice_id="Vitoria"):
    """Retornar resposta usando voz Polly customizada via SSML."""
    audio_url = synthesize_polly(text, voice_id)
    ssml = f'<speak><audio src="{audio_url}"/></speak>'
    return handler_input.response_builder.speak(ssml)
```

## 6.3 语音控制 SSML

```xml
<speak>
  <prosody rate="90%" pitch="+5%">
    Oi! Eu sou a Auri.
  </prosody>
  <break time="0.5s"/>
  <emphasis level="moderate">Como posso ajudar?</emphasis>
</speak>
```

---

## 7.1 聊天模板

```json
{
  "type": "APL",
  "version": "2023.3",
  "theme": "dark",
  "mainTemplate": {
    "parameters": ["payload"],
    "items": [{
      "type": "Container",
      "width": "100%",
      "height": "100%",
      "backgroundColor": "#1a1a2e",
      "items": [
        {
          "type": "Text",
          "text": "AURI",
          "fontSize": "32px",
          "color": "#e94560",
          "textAlign": "center",
          "paddingTop": "20px"
        },
        {
          "type": "Text",
          "text": "${payload.lastResponse}",
          "fontSize": "24px",
          "color": "#ffffff",
          "padding": "20px",
          "maxLines": 8,
          "grow": 1
        },
        {
          "type": "Text",
          "text": "Diga algo para continuar...",
          "fontSize": "18px",
          "color": "#888888",
          "textAlign": "center",
          "paddingBottom": "20px"
        }
      ]
    }]
  }
}
```

## 7.2 在响应中添加 APL

```python
@sb.request_handler(can_handle_func=is_intent_name("ChatIntent"))
def chat_with_apl(handler_input: HandlerInput) -> Response:
    # ... obter reply do Claude ...

    # Verificar se device suporta APL
    supported = handler_input.request_envelope.context.system.device.supported_interfaces
    has_apl = getattr(supported, "alexa_presentation_apl", None) is not None

    if has_apl:
        apl_directive = {
            "type": "Alexa.Presentation.APL.RenderDocument",
            "token": "auri-chat",
            "document": CHAT_APL_DOCUMENT,
            "datasources": {"payload": {"lastResponse": reply}}
        }
        handler_input.response_builder.add_directive(apl_directive)

    return handler_input.response_builder.speak(reply).ask("Mais alguma coisa?").response
```

---

## 8.1 启用 Smart Home Skill

在 `skill.json` 中添加：
```json
{
  "apis": {
    "smartHome": {
      "endpoint": {
        "uri": "arn:aws:lambda:us-east-1:123456789:function:auri-smart-home"
      }
    }
  }
}
```

## 8.2 Smart Home Handler

```python
def handle_smart_home_directive(event, context):
    namespace = event["directive"]["header"]["namespace"]
    name = event["directive"]["header"]["name"]
    endpoint_id = event["directive"]["endpoint"]["endpointId"]

    if namespace == "Alexa.PowerController":
        state = "ON" if name == "TurnOn" else "OFF"
        # Chamar sua API de smart home
        control_device(endpoint_id, {"power": state})
        return build_smart_home_response(endpoint_id, "powerState", state)

    elif namespace == "Alexa.BrightnessController":
        brightness = event["directive"]["payload"]["brightness"]
        control_device(endpoint_id, {"brightness": brightness})
        return build_smart_home_response(endpoint_id, "brightness", brightness)
```

## 8.3 设备发现

```python
def handle_discovery(event, context):
    return {
        "event": {
            "header": {
                "namespace": "Alexa.Discovery",
                "name": "Discover.Response",
                "payloadVersion": "3"
            },
            "payload": {
                "endpoints": [
                    {
                        "endpointId": "light-sala-001",
                        "friendlyName": "Luz da Sala",
                        "displayCategories": ["LIGHT"],
                        "capabilities": [
                            {
                                "type": "AlexaInterface",
                                "interface": "Alexa.PowerController",
                                "version": "3"
                            },
                            {
                                "type": "AlexaInterface",
                                "interface": "Alexa.BrightnessController",
                                "version": "3"
                            }
                        ]
                    }
                ]
            }
        }
    }
```

---

## 完整部署（Skill + Lambda）

cd auri/
ask deploy

## 验证状态

ask status

## 在模拟器中测试

ask dialog --locale pt-BR

## 测试特定 Intent

ask simulate \
  --text "abrir auri" \
  --locale pt-BR \
  --skill-id amzn1.ask.skill.YOUR-SKILL-ID
```

## 手动创建 Lambda

aws lambda create-function \
  --function-name auri-skill \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT:role/auri-lambda-role \
  --handler lambda_function.handler \
  --timeout 8 \
  --memory-size 512 \
  --zip-file fileb://function.zip

## 添加 Alexa 触发器

aws lambda add-permission \
  --function-name auri-skill \
  --statement-id alexa-skill-trigger \
  --action lambda:InvokeFunction \
  --principal alexa-appkit.amazon.com \
  --event-source-token amzn1.ask.skill.YOUR-SKILL-ID
```

## 使用 Secrets Manager

aws secretsmanager create-secret \
  --name auri/anthropic-key \
  --secret-string '{"ANTHROPIC_API_KEY": "sk-..."}'

## Lambda 通过 SDK 访问：

import boto3, json
def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])
```

---

## 阶段 1 — 设置（第 1 天）

```
[ ] Amazon Developer 账户已创建
[ ] AWS 账户已配置（free tier）
[ ] ASK CLI 已安装和配置
[ ] IAM Role 已创建，权限包括：Lambda、DynamoDB、Polly、Logs
[ ] Anthropic API key 已存储在 Secrets Manager
```

## 阶段 2 — Skill 基础（第 2-3 天）

```
[ ] ask new --template hello-world --skill-name auri
[ ] Interaction model 已定义（pt-BR.json）
[ ] LaunchRequest handler 正常工作
[ ] ChatIntent handler 已集成 Claude
[ ] ask deploy 正常工作
[ ] 在 ASK simulator 中基础测试通过
```

## 阶段 3 — 持久化（第 4 天）

```
[ ] DynamoDB 表已创建
[ ] 历史持久化正常工作
[ ] TTL 已配置
[ ] 用户偏好已保存
```

## 阶段 4 — Polly + APL（第 5-6 天）

```
[ ] Polly 已集成 Vitoria 语音（neural）
[ ] APL 聊天模板已创建
[ ] APL 在 Echo Show 模拟器中渲染
```

## 阶段 5 — Smart Home（可选）

```
[ ] Smart Home skill 已启用
[ ] 设备发现正常工作
[ ] PowerController 已实现
[ ] 使用真实设备测试
```

## 阶段 6 — 发布

```
[ ] 所有功能完整测试
[ ] 性能 OK（< 8s timeout）
[ ] Amazon 认证已提交
[ ] 已在 Alexa Skills Store 发布
```

---

## 11. 快速命令

| 操作 | 命令 |
|------|------|
| 创建 skill | `ask new --template hello-world` |
| 部署 | `ask deploy` |
| 模拟 | `ask simulate --text "abre a auri"` |
| 交互式对话 | `ask dialog --locale pt-BR` |
| 查看日志 | `ask smapi get-skill-simulation` |
| 验证模型 | `ask validate --locales pt-BR` |
| 导出 skill | `ask smapi export-package --skill-id ID` |
| 列出 skills | `ask list skills` |

---

## 12. 参考资料

- 完整 Python 样板：`assets/boilerplate/lambda_function.py`
- PT-BR Interaction model：`assets/interaction-models/pt-BR.json`
- APL 聊天模板：`assets/apl-templates/chat-interface.json`
- Smart Home 示例：`references/smart-home-api.md`
- ASK SDK Python 文档：https://github.com/alexa/alexa-skills-kit-sdk-for-python
- Claude + Alexa 指南：https://www.anthropic.com/news/claude-and-alexa-plus

## 最佳实践

- 提供清晰、具体的项目上下文和需求
- 在将建议应用于生产代码前进行审查
- 结合其他互补技能进行全面分析

## 常见陷阱

- 将此技能用于其领域专业范围之外的任务
- 在不了解具体上下文的情况下应用建议
- 未提供足够的项目上下文以进行准确分析

## 局限性
- 仅当任务明显符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
