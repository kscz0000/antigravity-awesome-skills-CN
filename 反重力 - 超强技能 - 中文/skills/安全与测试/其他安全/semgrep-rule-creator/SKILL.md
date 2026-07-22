---
name: semgrep-rule-creator
description: 创建自定义 Semgrep 规则，用于检测安全漏洞、错误模式和代码模式。编写 Semgrep 规则或构建自定义静态分析检测时使用。触发词：Semgrep规则、安全漏洞检测、静态分析、代码模式、自定义规则、安全检测、代码审计、漏洞扫描
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebFetch
risk: unknown
source: community
---

# Semgrep 规则创建器

创建具有适当测试和验证的生产级 Semgrep 规则。

## 使用场景
**理想场景：**
- 为特定错误模式编写 Semgrep 规则
- 编写规则检测代码库中的安全漏洞
- 为数据流漏洞编写污点模式规则
- 编写规则强制执行编码标准

## 不适用场景

不要将此技能用于：
- 运行现有的 Semgrep 规则集
- 没有自定义规则的通用静态分析（使用 `static-analysis` 技能）

## 应拒绝的合理化借口

编写 Semgrep 规则时，拒绝这些常见捷径：

- **"模式看起来很完整"** → 仍然运行 `semgrep --test --config <rule-id>.yaml <rule-id>.<ext>` 进行验证。未测试的规则存在隐藏的误报/漏报。
- **"它匹配了漏洞案例"** → 匹配漏洞只是工作的一半。验证安全案例不匹配（误报会破坏信任）。
- **"污点模式对这个来说太过了"** → 如果数据从用户输入流到危险接收器，污点模式比模式匹配提供更好的精度。
- **"一个测试就够了"** → 包含边界情况：不同的编码风格、已清理的输入、安全替代方案和边界条件。
- **"我会先优化模式"** → 先编写正确的模式，所有测试通过后再优化。过早优化会导致回归。
- **"AST 转储太复杂了"** → AST 揭示了 Semgrep 如何看待代码。跳过它会导致模式遗漏语法变体。

## 反模式

**过于宽泛** - 匹配一切，对检测无用：
```yaml
# 差：匹配任何函数调用
pattern: $FUNC(...)

# 好：特定的危险函数
pattern: eval(...)
```

**测试中缺少安全案例** - 导致未检测到的误报：
```python
# 差：仅测试漏洞案例
# ruleid: my-rule
dangerous(user_input)

# 好：包含安全案例以验证无误报
# ruleid: my-rule
dangerous(user_input)

# ok: my-rule
dangerous(sanitize(user_input))

# ok: my-rule
dangerous("hardcoded_safe_value")
```

**过于具体的模式** - 遗漏变体：
```yaml
# 差：仅匹配精确格式
pattern: os.system("rm " + $VAR)

# 好：使用污点跟踪匹配所有 os.system 调用
mode: taint
pattern-sinks:
  - pattern: os.system(...)
```

## 严格程度

此工作流是**严格的** - 不要跳过步骤：
- **先阅读文档**：编写 Semgrep 规则前参见[文档](#文档)
- **测试优先是强制的**：永远不要在没有测试的情况下编写规则
- **100% 测试通过是必需的**："大部分测试通过"是不可接受的
- **优化放在最后**：仅在所有测试通过后简化模式
- **避免通用模式**：规则必须是具体的，不匹配宽泛模式
- **优先使用污点模式**：用于数据流漏洞
- **一个 YAML 文件 - 一个 Semgrep 规则**：每个 YAML 文件必须只包含一个 Semgrep 规则；不要在单个文件中组合多个规则
- **禁止通用规则**：当为 Semgrep 规则指定特定语言时 - 避免通用模式匹配（`languages: generic`）
- **禁止 `todook` 和 `todoruleid` 测试注释**：禁止在测试文件中使用 `todoruleid: <rule-id>` 和 `todook: <rule-id>` 注释用于未来的规则改进

## 概述

此技能指导创建检测安全漏洞和代码模式的 Semgrep 规则。规则是迭代创建的：分析问题，先写测试，分析 AST 结构，编写规则，迭代直到所有测试通过，优化规则。

**方法选择：**
- **污点模式**（优先）：不受信任的输入到达危险接收器的数据流问题
- **模式匹配**：没有数据流需求的简单语法模式

**为什么优先使用污点模式？** 模式匹配找到语法但遗漏上下文。模式 `eval($X)` 匹配 `eval(user_input)`（漏洞）和 `eval("safe_literal")`（安全）。污点模式跟踪数据流，因此仅在不受信任的数据实际到达接收器时才告警——大幅减少注入漏洞的误报。

**在方法间切换：** 实验是可以的。如果从污点模式开始但效果不好（例如污点传播不符合预期、误报/漏报太多），切换到模式匹配。反之，如果模式匹配在安全案例上产生太多误报，尝试污点模式。目标是工作规则——而不是死板地坚持一种方法。

**输出结构** - 在以规则 ID 命名的目录中恰好 2 个文件：
```
<rule-id>/
├── <rule-id>.yaml     # Semgrep 规则
└── <rule-id>.<ext>    # 带 ruleid/ok 注释的测试文件
```

## 快速开始

```yaml
rules:
  - id: insecure-eval
    languages: [python]
    severity: HIGH
    message: 传递给 eval() 的用户输入允许代码执行
    mode: taint
    pattern-sources:
      - pattern: request.args.get(...)
    pattern-sinks:
      - pattern: eval(...)
```

测试文件（`insecure-eval.py`）：
```python
# ruleid: insecure-eval
eval(request.args.get('code'))

# ok: insecure-eval
eval("print('safe')")
```

运行测试（从规则目录）：`semgrep --test --config <rule-id>.yaml <rule-id>.<ext>`

## 快速参考

- 关于命令、模式运算符和污点模式语法，参见 quick-reference.md。
- 关于详细工作流和示例，必须参见 workflow.md

## 工作流

复制此清单并跟踪进度：

```
Semgrep 规则进度：
- [ ] 步骤 1：分析问题
- [ ] 步骤 2：先写测试
- [ ] 步骤 3：分析 AST 结构
- [ ] 步骤 4：编写规则
- [ ] 步骤 5：迭代直到所有测试通过（semgrep --test）
- [ ] 步骤 6：优化规则（移除冗余，重新测试）
- [ ] 步骤 7：最终运行
```

## 文档

**必需**：编写任何规则前，使用 WebFetch 阅读以下 4 个 Semgrep 文档链接的**全部内容**：

1. [规则语法](https://semgrep.dev/docs/writing-rules/rule-syntax)
2. [模式语法](https://semgrep.dev/docs/writing-rules/pattern-syntax)
3. [ToB 测试手册 - Semgrep](https://appsec.guide/docs/static-analysis/semgrep/advanced/)
4. [常量传播](https://semgrep.dev/docs/writing-rules/data-flow/constant-propagation)
5. [编写规则索引](https://github.com/semgrep/semgrep-docs/tree/main/docs/writing-rules/)

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。