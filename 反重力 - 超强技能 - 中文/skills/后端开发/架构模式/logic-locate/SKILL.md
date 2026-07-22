---
name: logic-locate
description: 通过先回溯再前推的半形式化追踪，定位已确认故障的根因。触发词：find the bug、this test is failing、track down this crash、why is this wrong、故障定位、找bug、定位崩溃、追踪错误、根因分析
risk: unknown
source: https://github.com/hyhmrright/logic-lens/tree/main/skills/logic-locate
source_repo: hyhmrright/logic-lens
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/hyhmrright/logic-lens/blob/main/LICENSE
---

# Logic-Lens — 故障定位
## 何时使用

当需要通过先回溯再前推的半形式化追踪来定位已确认故障的根因时使用此技能。触发条件：用户提供了堆栈跟踪、失败的断言、错误消息或具体的错误值观察——"find the bug"、"this test is failing"、"track down this crash"、"why is this wrong"。


## 设置

按照 `../_shared/common.md` 第13节进行懒加载：
1. 仅在需要语言、铁律、故障置信度、范围路由、修复纪律、配置字段和加载预算时读取 `../_shared/common.md`。
2. 仅在执行到相关步骤时读取 `logic-locate-guide.md` 中对应的步骤。
3. 当当前步骤需要时，按需加载 `../_shared/logic-risks.md`、`../_shared/semiformal-guide.md`、`../_shared/semiformal-checklist.md` 和 `../_shared/report-template.md`。

## 流程

**步骤 0. 语言 + 范围路由。** 按照 `common.md` 第1节检测语言。确认存在具体故障（堆栈跟踪、失败断言、具体错误值）。如果仅为猜测，切换至 logic-review。

**步骤 1. 理解故障**（指南步骤 1）——观察到的行为、预期行为、复现路径。

**步骤 2. 定位入口点**（指南步骤 2）——失败的测试、最外层应用帧或请求处理器——选择最接近故障的那个。首先聚焦故障锥内部：堆栈帧、失败的测试夹具、直接调用的局部函数，以及该路径上读取的配置/环境值。除非追踪跨越到其他模块，否则不要扫描无关模块。

**步骤 3. 从故障点回溯追踪**（指南步骤 3）——逐跳地将每个值和状态回溯到其源头，在每一跳建立前提。

**步骤 4. 前推确认**（指南步骤 4）——从疑似根因出发，验证追踪路径能到达观察到的症状。

**步骤 5. 跨过程追踪（若被调用方涉案）**（指南步骤 5）——追踪进入被调用方；检查观察条件下的返回值、未处理异常、共享状态变异。应用 `semiformal-guide.md` 第"Call-Chain Context Labels"节定义的深度限制和调用链上下文标签格式；到达限制时，将剩余的被调用方路径作为前提假设陈述，并将置信度降级为**中等**（按照 `common.md` 第7节）。

**步骤 6. 识别根因分歧并分类**（指南步骤 6）——陈述确切的行/表达式、违反的前提、实际行为、到症状的传播链；选择 L-code。

**步骤 7. 输出聚焦报告**（指南步骤 7）——故障置信度（高/中/低，按照 `common.md` 第7节）；首要故障（单个五字段发现）；可选的贡献因素；按照 `common.md` 第10节的最小修复。**即使对于简单的单函数 bug，格式也是强制性的：始终输出带标签的 Premises / Trace / Divergence / Trigger / Remedy 字段以及故障置信度行。绝不以纯修复建议作答。**

**报告模式行：** `Fault Locate`（中文：`故障定位`）。

**输出格式：** Findings 节包含一个首要故障，而非完整的 Critical/Warning/Suggestion 划分。Logic Score 行替换为 **Fault Confidence:** High / Medium / Low。

## 限制

- 仅当任务明确匹配其上游源和本地项目上下文时使用此技能。
- 在应用变更之前，验证命令、生成的代码、依赖项、凭证和外部服务行为。
- 不要将示例替代环境特定测试、安全审查或用户对破坏性或高成本操作的批准。
