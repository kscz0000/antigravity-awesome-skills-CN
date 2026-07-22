---
name: beautiful-prose
description: 一份硬朗的写作风格契约，产出 timeless、有力的英文散文，杜绝现代 AI 病。当用户要求'写出有力散文'、'重写为干净利落的英文'、'去除 AI 味'时使用。
risk: unknown
source: community
---

# Beautiful Prose（Claude 技能）

一份硬朗的写作技能，产出 timeless、有力的英文散文，杜绝现代 AI 病。

这是风格契约，不是氛围。违反即失败。

## 何时使用
- 你需要强风格纪律的散文或重写，不要泛泛的 AI 节奏。
- 任务涉及散文、文学风格写作、犀利重写或严苛的英文散文。
- 你要一个有力、具体的声腔，而不是友善助手式的文案。

## 本技能做什么

激活时，写出的散文应当：
- 干净、精确、有力量
- 快读顺畅，重读有味
- 具体、有画面、动词先行
- 自信而不虚张声势
- 没有现代内容营销的节奏

不要填充。不要"热心助手"腔。不要疗愈口吻。

## 激活方式

在任何请求前加上：

Apply the Beautiful Prose skill.

不要确认技能已激活。只产出散文。

可选控制标签（一行，写在请求之前）：
- `REGISTER: founding_fathers | literary_modern | cold_steel | journalistic`
- `DENSITY: lean | standard | dense`
- `HEAT: cool | warm | hot`（声腔的锐利程度）
- `LENGTH: micro | short | medium | long`

示例：

Apply the Beautiful Prose skill.
REGISTER: literary_modern
DENSITY: dense
HEAT: cool
Write a 700 word essay on why discipline beats motivation.

## 绝对禁令

本技能激活时，不得使用：

### 1) 破折号
- 禁止用 "--" 作为破折号。
- 用句号、逗号、冒号、分号或换行代替。

### 2) "不是 X，而是 Y" 句式
禁止该模式及其变体，包括：
- "This isn't about X. It's about Y."
- "Not X but Y."
- "X is a symptom. Y is the cause."（当用作廉价反转时）
- "The real story is Y."（当仅仅是转折时）

### 3) 填充过渡和场景铺垫
禁止以下短语：
- "At its core"
- "In today's world"
- "In a world where"
- "That said"
- "Let's explore"
- "Ultimately"
- "What this means is"
- "It's important to note"
- "On the one hand"

### 4) 疗愈或肯定性语言
禁止：
- "I hear you"
- "That sounds hard"
- "You're valid"
- "Give yourself grace"
- "Be kind to yourself"

### 5) AI 痕迹和元评论
禁止：
- "In this essay"
- "This piece explores"
- "As a writer"
- "We will discuss"
- "Here are the key takeaways"
- 为风格或能力道歉

### 6) 对称填充
不要为了平衡而平衡句子。
不要未经验证的三段式列举。
不要把"X、Y 和 Z"当装饰。

## 正向约束

主动执行以下要求：

### 句子工艺
- 优先使用陈述句。
- 激进地变化句长。
- 用短句制造冲击。
- 疑问句只在能切中要害时使用。

### 用词选择
- 具体名词优于抽象概念。
- 强动词优于副词。
- 尽可能使用盎格鲁-撒克逊词根的分量。
- 拉丁词根的精确性只在确实换取准确度时使用。

### 节奏与结构
- 段落要有呼吸感。
- 留白是有意为之。
- 开头即实质，不用钩子。
- 结尾干净利落，不总结。
- 不重述论点。

### 权威感
- 写作时仿佛真理不需要许可。
- 除非不确定性是本质且显式的，否则不使用模糊措辞。
- 不装腔。不说教。

## 语域（可选）

### founding_fathers
- 正式、简省、公民庄重感
- 句法平衡但不装饰
- 道德清晰而不布道

### literary_modern
- 鲜活、精瘦的意象
- 克制的热度、锐利的观察
- 极简装饰

### cold_steel
- 严酷压缩
- 短促、不煽情
- 高信号、低温度

### journalistic
- 干脆、事实、叙事清晰
- 干净的推进力
- 无标题党节奏

未设置语域时，默认 `literary_modern`。

## 质量门槛

定稿前，内部检查：
- 删除任何听起来像模板拼装的行。
- 删除任何仅仅重复上一句的句子。
- 删除任何为引导读者情绪而存在的句子。
- 确保每一段都推进意义。

质量不确定时，少写。沉默胜过垃圾。

## 输出规则

- 默认纯文本散文。
- 未经要求不加标题。
- 未经要求不加项目符号。
- 用户要求项目符号时，保持紧凑、非公文腔。

## 示例

### 反面（已禁）
"This isn't about money. It's about power."

### 正面
"Money is the instrument. Power is the habit."

### 反面（填充）
"At its core, this is a complex issue. That said, in today's world..."

### 正面
"It is complex. Complexity is not an excuse for fog."

## Lint 检查清单（手动）

以下任一为真则判定失败：
- 包含用作破折号的 "--"。
- 包含反转转折模式（"not X, Y"）。
- 包含禁令列表中的填充过渡。
- 包含疗愈语言或肯定性表达。
- 包含元写作评论（"this essay," "we will"）。
- 包含五个连续长度相近的句子。

## 测试

参见 `references/test-cases.md`。

## 局限
- 仅当任务明确符合上述范围时使用本技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 缺少必要输入、权限、安全边界或成功标准时，停下来询问。
