---
name: blockrun
description: "BlockRun 与 Claude Code 和 Google Antigravity 协同工作。触发词：blockrun、图像生成、DALL-E、实时X数据、Grok、GPT第二意见、DeepSeek、钱包余额、x402微支付。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# BlockRun

**BlockRun 与 Claude Code 和 Google Antigravity 协同工作。**

你无法生成图像。你没有实时 X/Twitter 访问权限。BlockRun 为你提供这些能力。

## 理念

你有一个钱包。当你需要某个你缺乏的能力时，自主付费获取。

| 你需要 | 你调用 | 定价 |
|----------|----------|---------|
| 图像生成 | DALL-E | $0.04/张 |
| 实时 X 数据 | Grok + Live Search | $0.025/来源 |
| 第二意见 | GPT-5.2 | $1.75/M 输入, $14/M 输出 |
| 更便宜的处理 | DeepSeek | $0.14/M 输入, $0.28/M 输出 |

**工作原理：** BlockRun 使用 x402 微支付将你的请求路由到 OpenAI、xAI、Google 和其他提供商。无需 API 密钥——你的钱包按 token 付费。

## 预算控制（可选）

如果用户指定了预算（例如"最多使用 $1"），跟踪支出并在达到预算时停止：

```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()
budget = 1.0  # 用户的预算

# 每次调用前，检查是否在预算内
spending = client.get_spending()
if spending['total_usd'] >= budget:
    print(f"Budget reached: ${spending['total_usd']:.4f} spent")
    # 停止调用
else:
    response = client.chat("openai/gpt-5.2", "Hello!")

# 最后，报告支出
spending = client.get_spending()
print(f"💰 Total spent: ${spending['total_usd']:.4f} across {spending['calls']} calls")
```

## 何时使用
| 触发条件 | 你的行动 |
|---------|-------------|
| 用户明确请求（"blockrun 用 GPT 给出第二意见..."、"用 grok 检查..."、"用 dall-e 生成图像"） | 通过 BlockRun 执行 |
| 用户需要你做不到的事情（图像、实时 X 数据） | 建议 BlockRun，等待确认 |
| 你自己能很好地处理任务 | 自己做，不要提及 BlockRun |

## 用户提示示例

用户会说类似这样的话：

| 用户说 | 你做什么 |
|-----------|-------------|
| "blockrun 生成一张日落图像" | 通过 ImageClient 调用 DALL-E |
| "用 grok 检查 X 上的热门话题" | 调用 Grok 并设置 `search=True` |
| "blockrun GPT 审查这段代码" | 通过 LLMClient 调用 GPT-5.2 |
| "AI agents 的最新新闻是什么？" | 建议 Grok（你缺乏实时数据） |
| "为我的创业公司生成一个 logo" | 建议 DALL-E（你无法生成图像） |
| "blockrun 检查我的余额" | 通过 `get_balance()` 显示钱包余额 |
| "blockrun deepseek 总结这个文件" | 调用 DeepSeek 以节省成本 |

## 钱包与余额

使用 `setup_agent_wallet()` 自动创建钱包并获取客户端。首次使用时会显示二维码和欢迎消息。

**初始化客户端（始终从这里开始）：**
```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()  # 自动创建钱包，如果是新的则显示 QR
```

**检查余额（当用户问"显示余额"、"检查钱包"等时）：**
```python
balance = client.get_balance()  # 链上 USDC 余额
print(f"Balance: ${balance:.2f} USDC")
print(f"Wallet: {client.get_wallet_address()}")
```

**显示用于充值的二维码：**
```python
from blockrun_llm import generate_wallet_qr_ascii, get_wallet_address

# 用于终端显示的 ASCII QR
print(generate_wallet_qr_ascii(get_wallet_address()))
```

## SDK 使用

**前置条件：** 使用 `pip install blockrun-llm` 安装 SDK

### 基础聊天
```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()  # 如需要则自动创建钱包
response = client.chat("openai/gpt-5.2", "What is 2+2?")
print(response)

# 检查支出
spending = client.get_spending()
print(f"Spent ${spending['total_usd']:.4f}")
```

### 实时 X/Twitter 搜索（xAI Live Search）

**重要：** 对于实时 X/Twitter 数据，你必须使用 `search=True` 或 `search_parameters` 启用 Live Search。

```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()

# 简单方式：使用 search=True 启用实时搜索
response = client.chat(
    "xai/grok-3",
    "What are the latest posts from @blockrunai on X?",
    search=True  # 启用实时 X/Twitter 搜索
)
print(response)
```

### 高级 X 搜索与过滤

```python
from blockrun_llm import setup_agent_wallet

client = setup_agent_wallet()

response = client.chat(
    "xai/grok-3",
    "Analyze @blockrunai's recent content and engagement",
    search_parameters={
        "mode": "on",
        "sources": [
            {
                "type": "x",
                "included_x_handles": ["blockrunai"],
                "post_favorite_count": 5
            }
        ],
        "max_search_results": 20,
        "return_citations": True
    }
)
print(response)
```

### 图像生成
```python
from blockrun_llm import ImageClient

client = ImageClient()
result = client.generate("A cute cat wearing a space helmet")
print(result.data[0].url)
```

## xAI Live Search 参考

Live Search 是 xAI 的实时数据 API。费用：**每个来源 $0.025**（默认 10 个来源 ≈ $0.26）。

要降低成本，将 `max_search_results` 设置为更低的值：
```python
# 仅使用 5 个来源（≈$0.13）
response = client.chat("xai/grok-3", "What's trending?",
    search_parameters={"mode": "on", "max_search_results": 5})
```

### 搜索参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `mode` | string | "auto" | "off"、"auto" 或 "on" |
| `sources` | array | web,news,x | 要查询的数据源 |
| `return_citations` | bool | true | 包含来源 URL |
| `from_date` | string | - | 开始日期（YYYY-MM-DD） |
| `to_date` | string | - | 结束日期（YYYY-MM-DD） |
| `max_search_results` | int | 10 | 返回的最大来源数（自定义以控制成本） |

### 来源类型

**X/Twitter 来源：**
```python
{
    "type": "x",
    "included_x_handles": ["handle1", "handle2"],  # 最多 10 个
    "excluded_x_handles": ["spam_account"],        # 最多 10 个
    "post_favorite_count": 100,  # 最小点赞数阈值
    "post_view_count": 1000      # 最小浏览数阈值
}
```

**Web 来源：**
```python
{
    "type": "web",
    "country": "US",  # ISO alpha-2 代码
    "allowed_websites": ["example.com"],  # 最多 5 个
    "safe_search": True
}
```

**新闻来源：**
```python
{
    "type": "news",
    "country": "US",
    "excluded_websites": ["tabloid.com"]  # 最多 5 个
}
```

## 可用模型

| 模型 | 最适合 | 定价 |
|-------|----------|---------|
| `openai/gpt-5.2` | 第二意见、代码审查、通用 | $1.75/M 输入, $14/M 输出 |
| `openai/gpt-5-mini` | 成本优化的推理 | $0.30/M 输入, $1.20/M 输出 |
| `openai/o4-mini` | 最新高效推理 | $1.10/M 输入, $4.40/M 输出 |
| `openai/o3` | 高级推理、复杂问题 | $10/M 输入, $40/M 输出 |
| `xai/grok-3` | 实时 X/Twitter 数据 | $3/M + $0.025/来源 |
| `deepseek/deepseek-chat` | 简单任务、批量处理 | $0.14/M 输入, $0.28/M 输出 |
| `google/gemini-2.5-flash` | 超长文档、快速 | $0.15/M 输入, $0.60/M 输出 |
| `openai/dall-e-3` | 照片级真实图像 | $0.04/张 |
| `google/nano-banana` | 快速、艺术图像 | $0.01/张 |

*M = 百万 tokens。实际成本取决于你的提示词和响应长度。*

## 成本参考

所有 LLM 成本按百万 tokens 计算（M = 1,000,000 tokens）。

| 模型 | 输入 | 输出 |
|-------|-------|--------|
| GPT-5.2 | $1.75/M | $14.00/M |
| GPT-5-mini | $0.30/M | $1.20/M |
| Grok-3（无搜索） | $3.00/M | $15.00/M |
| DeepSeek | $0.14/M | $0.28/M |

| 固定成本操作 | |
|-------|--------|
| Grok Live Search | $0.025/来源（默认 10 个 = $0.25） |
| DALL-E 图像 | $0.04/张 |
| Nano Banana 图像 | $0.01/张 |

**典型成本：** 一个 500 词的提示词（≈750 tokens）发送给 GPT-5.2 成本约 $0.001 输入。一个 1000 词的响应（≈1500 tokens）成本约 $0.02 输出。

## 设置与充值

**钱包位置：** `$HOME/.blockrun/.session`（例如 `/Users/username/.blockrun/.session`）

**首次设置：**
1. 调用 `setup_agent_wallet()` 时自动创建钱包
2. 检查钱包和余额：
```python
from blockrun_llm import setup_agent_wallet
client = setup_agent_wallet()
print(f"Wallet: {client.get_wallet_address()}")
print(f"Balance: ${client.get_balance():.2f} USDC")
```
3. 在 Base 网络上充值 $1-5 USDC

**显示用于充值的二维码（终端 ASCII）：**
```python
from blockrun_llm import generate_wallet_qr_ascii, get_wallet_address
print(generate_wallet_qr_ascii(get_wallet_address()))
```

## 故障排除

**"Grok 说它没有实时访问权限"**
→ 你忘记启用 Live Search。添加 `search=True`：
```python
response = client.chat("xai/grok-3", "What's trending?", search=True)
```

**找不到模块**
→ 安装 SDK：`pip install blockrun-llm`

## 更新

```bash
pip install --upgrade blockrun-llm
```

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
