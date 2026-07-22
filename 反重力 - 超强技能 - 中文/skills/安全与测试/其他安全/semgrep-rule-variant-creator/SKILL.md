---
name: semgrep-rule-variant-creator
description: 为现有 Semgrep 规则创建语言变体。当需要将 Semgrep 规则移植到指定目标语言时使用。接收现有规则和目标语言作为输入，为每种语言生成独立的规则+测试目录。触发词：Semgrep变体、规则移植、语言变体、多语言规则、Semgrep移植
allowed-tools:
 ...
risk: unknown
source: community
---

# Semgrep 规则变体创建器

将现有 Semgrep 规则移植到新的目标语言，包含适用性分析和测试驱动验证。

## 适用场景
**理想场景：**
- 将现有 Semgrep 规则移植到一种或多种目标语言
- 为通用漏洞模式创建特定语言的变体
- 在多语言代码库中扩展规则覆盖范围
- 在具有等效构造的语言之间翻译规则

## 不适用场景

请勿将此技能用于：
- 从零创建新的 Semgrep 规则（请改用 `semgrep-rule-creator`）
- 对代码运行现有规则
- 漏洞模式根本不适用于目标语言的情况
- 同一语言内的微小语法差异

## 输入规格

此技能需要：
1. **现有 Semgrep 规则** - YAML 文件路径或 YAML 规则内容
2. **目标语言** - 一种或多种要移植到的语言（例如 "Golang and Java"）

## 输出规格

对于每个适用的目标语言，生成：
```
<原始规则ID>-<语言>/
├── <原始规则ID>-<语言>.yaml     # 移植后的 Semgrep 规则
└── <原始规则ID>-<语言>.<ext>    # 带注解的测试文件
```

将 `sql-injection` 移植到 Go 和 Java 的输出示例：
```
sql-injection-golang/
├── sql-injection-golang.yaml
└── sql-injection-golang.go

sql-injection-java/
├── sql-injection-java.yaml
└── sql-injection-java.java
```

## 应拒绝的借口

移植 Semgrep 规则时，请拒绝以下常见捷径：

| 借口 | 为什么行不通 | 正确做法 |
|------|-------------|----------|
| "模式结构完全一样" | 不同语言的 AST 不同 | 始终为目标语言导出 AST |
| "同样的漏洞，同样的检测" | 数据流在语言间有差异 | 分析目标语言的习惯用法 |
| "原始规则已测试，不需要再测" | 语言边界情况不同 | 为目标语言编写全新测试用例 |
| "跳过适用性分析，显然能用" | 某些模式是特定语言的 | 先完成完整的适用性分析 |
| "先创建所有变体再测试" | 错误会累积，难以调试 | 每种语言完成完整周期 |
| "库的等效实现差不多" | 表面相似性隐藏了差异 | 验证 API 语义是否匹配 |
| "直接 1:1 翻译语法就行" | 语言有不同的惯用写法 | 研究目标语言的模式 |

## 严格程度

此工作流是**严格**的——不得跳过步骤：
- **适用性分析是强制性的**：不要假设模式可以直接翻译
- **每种语言独立处理**：完成完整周期后再处理下一种
- **每个变体测试先行**：永远先写测试用例再写规则
- **要求 100% 测试通过**："大部分测试通过"是不可接受的

## 概述

此技能指导为现有 Semgrep 规则创建特定语言的变体。每种目标语言经历独立的 4 阶段周期：

```
FOR EACH target language:
  Phase 1: Applicability Analysis → Verdict
  Phase 2: Test Creation (Test-First)
  Phase 3: Rule Creation
  Phase 4: Validation
  (Complete full cycle before moving to next language)
```

## 基础知识

**`semgrep-rule-creator` 技能是 Semgrep 规则创建基础知识的权威参考。** 此技能侧重于将现有规则移植到新语言，但编写高质量规则的核心原则是相同的。

有关以下方面的指导，请查阅 `semgrep-rule-creator`：
- **何时使用污点模式 vs 模式匹配** - 为漏洞类型选择正确的方法
- **测试先行方法论** - 为什么测试先于规则，以及如何编写有效的测试用例
- **应避免的反模式** - 常见错误，如过于宽泛或过于具体的模式
- **迭代直到测试通过** - 验证循环和调试技巧
- **规则优化** - 测试通过后移除冗余模式

移植规则时，你是在新的语言上下文中应用这些相同的原则。如果对规则结构或方法不确定，请先参考 `semgrep-rule-creator`。

## 四阶段工作流

### 阶段 1：适用性分析

移植前，判断模式是否适用于目标语言。

**分析标准：**
1. 目标语言中是否存在该漏洞类别？
2. 是否存在等效构造（函数、模式、库）？
3. 语义是否足够相似以进行有意义的检测？

**判定选项：**
- `APPLICABLE` → 继续创建变体
- `APPLICABLE_WITH_ADAPTATION` → 继续但需要重大修改
- `NOT_APPLICABLE` → 跳过此语言，记录原因

详见 applicability-analysis.md 获取详细指导。

### 阶段 2：测试创建（测试先行）

**始终先写测试再写规则。**

使用目标语言习惯用法创建测试文件：
- 至少 2 个漏洞用例（`ruleid:`）
- 至少 2 个安全用例（`ok:`）
- 包含特定语言的边界情况

```go
// ruleid: sql-injection-golang
db.Query("SELECT * FROM users WHERE id = " + userInput)

// ok: sql-injection-golang
db.Query("SELECT * FROM users WHERE id = ?", userInput)
```

### 阶段 3：规则创建

1. **分析 AST**：`semgrep --dump-ast -l <lang> test-file`
2. **翻译模式**到目标语言语法
3. **更新元数据**：language 键、消息、规则 ID
4. **适配惯用写法**：处理特定语言的构造

详见 language-syntax-guide.md 获取翻译指导。

### 阶段 4：验证

```bash
# Validate YAML
semgrep --validate --config rule.yaml

# Run tests
semgrep --test --config rule.yaml test-file
```

**检查点**：输出必须显示 `All tests passed`。

污点规则调试：
```bash
semgrep --dataflow-traces -f rule.yaml test-file
```

详见 workflow.md 获取详细工作流和故障排查。

## 快速参考

| 任务 | 命令 |
|------|------|
| 运行测试 | `semgrep --test --config rule.yaml test-file` |
| 验证 YAML | `semgrep --validate --config rule.yaml` |
| 导出 AST | `semgrep --dump-ast -l <lang> <file>` |
| 调试污点流 | `semgrep --dataflow-traces -f rule.yaml file` |


## 与规则创建的主要区别

| 方面 | semgrep-rule-creator | 本技能 |
|------|---------------------|--------|
| 输入 | Bug 模式描述 | 现有规则 + 目标语言 |
| 输出 | 单个规则+测试 | 多个规则+测试目录 |
| 工作流 | 单次创建周期 | 每种语言独立周期 |
| 阶段 1 | 问题分析 | 每种语言的适用性分析 |
| 库研究 | 始终相关 | 可选（当原始规则使用库时） |

## 文档

**必需**：移植规则前，请阅读相关 Semgrep 文档：

- [Rule Syntax](https://semgrep.dev/docs/writing-rules/rule-syntax) - YAML 结构和运算符
- [Pattern Syntax](https://semgrep.dev/docs/writing-rules/pattern-syntax) - 模式匹配和元变量
- [Pattern Examples](https://semgrep.dev/docs/writing-rules/pattern-examples) - 各语言模式参考
- [Testing Rules](https://semgrep.dev/docs/writing-rules/testing-rules) - 测试注解
- [Trail of Bits Testing Handbook](https://appsec.guide/docs/static-analysis/semgrep/advanced/) - 高级模式

## 后续步骤

- 适用性分析指导，请参阅 applicability-analysis.md
- 语言翻译指导，请参阅 language-syntax-guide.md
- 详细工作流和示例，请参阅 workflow.md

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来寻求澄清。
