---
name: debugging-code
description: 交互式调试源代码——设置断点、逐行单步执行、查看运行期变量状态、对运行中的程序求值表达式、遍历调用栈追踪根因。涉及程序崩溃、抛出未预期异常、产生错误输出,或需要理解执行如何到达某个状态时使用。
risk: unknown
source: https://github.com/AlmogBaku/debug-skill/tree/master/skills/debugging-code
source_repo: AlmogBaku/debug-skill
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/AlmogBaku/debug-skill/blob/master/LICENSE
---

# 交互式调试器
## 适用场景

需要交互式调试源代码时使用本技能——设置断点、逐行单步执行、查看运行期变量状态、对运行中的程序求值表达式、遍历调用栈追踪根因。涉及程序崩溃、抛出未预期异常、产生错误输出时使用……


当程序崩溃、输出错误,或需要准确理解执行是如何到达某个状态的——再插入更多 print 语句无法快速给你答案时使用。

可以在任意位置暂停运行中的程序,在那一瞬间读取实时的变量值和调用栈,逐行向前推进或跳到下一个断点,并对运行中的进程求任意表达式——全程无需重启。

## 安装

本技能使用 `dap`,一个通过 DAP 协议与调试器交互的 CLI 工具,由后台守护进程维护调试器状态,因此你可以通过多次调用简单地与之交互。

如果 `dap` 未安装(检查方式:`command -v dap`),请立即安装。
在继续安装前先询问/告知用户。

从 Homebrew(macOS)安装:

```bash
brew install AlmogBaku/tap/dap
```

安装脚本:

```bash
bash scripts/install-dap.sh
```

从源码安装:

```bash
go install github.com/AlmogBaku/debug-skill/cmd/dap@latest
```

该工具开源,可在 [GitHub](https://github.com/AlmogBaku/debug-skill) 获得,持续维护并遵循最佳实践。

原生支持 Python、Go、Node.js/TypeScript、Rust、C/C++,以及任何其他支持 DAP 的语言。

如果调试器后端缺失或启动失败,请参阅 `references/installing-debuggers.md`

所有命令与参数请参考:`dap --help` 或 `dap <cmd> --help`。

## 启动会话

`dap debug <file>` 在调试器下启动程序。后端会根据文件扩展名自动检测。

根据你已知的情况选择起始策略:

- **已有假设** —— 在你怀疑的位置设置断点:`dap debug script.py --break script.py:42`
- **条件断点** —— 仅在满足条件时停下:`dap debug script.py --break "script.py:42:x > 5"`(带条件的规约请始终加引号)
- **多文件应用** —— 跨模块的断点:`--break src/api/routes.py:55 --break src/models/user.py:30`
- **无假设,小型程序** —— 从入口逐步走:`dap debug script.py --stop-on-entry`(大型项目慎用——启动代码噪音多;改用断点二分定位)
- **异常,位置未知** —— `dap debug script.py --break-on-exception raised`(Python)/ `all`(Go/JS)
- **远程进程** —— `dap debug --attach host:port --backend <name>`
- **进程已在运行(卡死的服务器、线上问题)** —— 附加而不重启:
  `dap debug --pid <PID> --backend <name>`
  > **macOS + Go 注意点:** `dlv --pid` 要求关闭 SIP(`csrutil disable`)。
  > 建议直接在调试器下启动程序,或附加到远程调试器!

**会话隔离:** `--session <name>` 防止并发智能体互相干扰。
提示:如果可用,可以使用会话 id(${CLAUDE_SESSION_ID})。

运行 `dap debug --help` 查看全部参数、后端与示例。

## 调试思维

当仅靠阅读源码无法验证根因时,才需要调试器。
调试器让你**观察**实际发生的事:真实值、真实路径、真实状态。
当它与“应该发生”的偏离时,bug 就找到了。

**两次失败,重新思考。** 如果两个假设在同一位置都失败,说明你的心智模型错了。
重读代码,形成一个**截然不同**的理论,并使用不同的断点。

**逐步升级。** 先用 `dap eval` 测试快速假设。使用条件断点过滤噪音。仅当需要交互控制时,才回退到完整断点 + 单步执行。

**模拟用户路径。** 调试用户流程时,沿着你预期代码会走的路径设置断点。
如果你预期 `compute()` 会被调用,但它从未被调用,那么 bug 在调用方——而不在 `compute()`,而在本应调用它的代码中。

**用断点替代 print。** 当你想打印某个值时,改用断点。

## 了解你的状态

每次 `dap` 执行命令都会自动返回完整上下文:当前位置、源码、局部变量、调用栈和输出。每次停下时问自己:

- 局部变量的值是否符合预期?
- 调用栈显示的是否是预期的代码路径?
- 目前为止的输出是否揭示了意料之外的信息?

**沿栈向上追溯因果。** 如果 frame 0 的值有问题,用 `dap eval "<expr>" --frame 1` 查看调用方传入的值。继续向上(`--frame 2`、`--frame 3`),直到找到值首次出错的那一帧——那才是 bug 的源头,而不是表象。

某次停下时的输出示例:

```
Stopped at compute() · script.py:41
  39:   def compute(items):
  40:       result = None
> 41:       return result
Locals: items=[]  result=None
Stack:  main [script.py:10] → compute [script.py:41]
Output: (none)
```

如果程序在到达断点前已退出:

```
Program terminated · Exit code: 1
```

→ 将断点前移,或加上 `--stop-on-entry` 重启。

## 形成假设

设置断点之前:*“我认为 bug 在 X,理由是 Y。”* 一个好假设是可证伪的——下一次观察将确认或推翻它。还没有假设?用两个断点二分缩小搜索范围,或参考前面的起始策略。

## 策略性地设置断点

- 设在问题**开始**的位置,而不是它**表现**的位置
- 第 80 行抛异常?根因在上游——从更早开始
- 不确定?二分定位:`--break f:20 --break f:60`——状态在哪个半区出错就一目了然

**断点位置:**

- **边界** —— 数据穿越格式、表示或模块边界的位置;此处状态最干净
- **状态转换** —— 给被污染的值赋值或变更的那一行
- **错误分支** —— 引导走向错误路径的条件所在
- **反模式** —— 不要在库代码里打断点;改在调用方打断点。在紧凑循环中不要使用无条件断点——请用条件。

### 会话中途管理断点

随着掌握更多信息,在嫌疑代码更深的位置添加断点,并移除已达成使命的断点——渐进式收窄,无需重启:

```bash
dap continue --break app.py:50              # 在更深处添加断点,然后继续
dap continue --remove-break app.py:20       # 移除已完成使命的断点
dap break add app.py:42 app.py:60           # 一次性添加多个断点
dap break list                              # 查看当前断点
dap break clear                             # 重新开始
```

如果断点位置无效,或适配器调整了它,`dap` 会在输出中告警。

### 条件断点

仅在条件为真时停下——对循环、热路径和特定输入值至关重要。
语法:`"file:line:condition"`(始终加引号)。

```bash
dap debug app.py --break "app.py:42:i == 100"            # 跳过 99 次迭代,在关键的那次停下
dap debug app.py --break "app.py:30:user_id == 123"      # 复现特定用户的 bug
dap continue --break "app.py:50:len(items) == 0"         # 在会话中途捕获空列表情形
```

### 不变量断点

把条件断点当作运行期断言——**一旦**出错立即停下:

```bash
dap debug app.py --break "bank.py:68:balance < 0"          # 抓住透支
dap debug app.py --break "pipe.py:30:type(val) != int"     # 类型违规
```

## 推进执行

每次停下时,根据你的怀疑选择如何前进:

如果你连续单步超过 3 次,你需要的是一个断点,而不是更多单步。

```bash
dap step                         # step over —— 信任本次调用,前进到下一行
dap step in                      # step into —— 怀疑本次调用内部有问题
dap step out                     # step out —— 当前位置不对,返回调用方
dap continue                     # 跳到下一个断点
dap continue --to file:line      # 运行到指定行(临时断点,自动移除)
dap context                      # 不单步,重新检视当前状态
dap output                       # 不输出完整上下文,仅刷新缓冲的 stdout/stderr
dap inspect <var> --depth N      # 展开嵌套/复杂对象
dap pause                        # 中断正在运行/挂起的程序
dap restart                      # 用相同参数和断点重启
dap threads                      # 列出所有线程
dap thread <id>                  # 切换线程上下文
```

每次停下都会显示当前 `file:line`,你始终知道身处何处。

用 `dap eval "<expr>"` 在不单步的情况下探查实时状态:

```bash
dap eval "len(items)"
dap eval "user.profile.settings"
dap eval "expected == actual"       # 在实时状态上验证假设
dap eval "self.config" --frame 1    # frame 1 = 调用方(可能是另一个文件)
```

避免调用有副作用方法的 eval 表达式——它们会变更程序状态,可能破坏调试会话。除非你有意在测试一个修复,否则坚持只读访问。

## 快速跳过

需要快速查看某行而不打算设置永久断点时,使用 `dap continue --to file:line`。它是一次性断点——只停一次,然后消失。适用于“我只想看看第 50 行 `x` 是什么样子”,无需管理断点生命周期。

## 高级场景

涉及卡死、并发 bug、深度嵌套状态、循环二分等高级场景,请参阅 `${CLAUDE_SKILL_DIR}/references/advanced-techniques.md`。

## 演练

**Bug:`compute()` 返回 `None`**

```
Hypothesis: result not assigned before return
→ dap debug script.py --break script.py:41
  Locals: result=None, items=[]   ← 错了,而且输入也是空的

New hypothesis: caller passing empty list
→ dap eval "items" --frame 1      → []   ← 已确认
→ dap step out                    → 调用方在第 10 行,对空输入没有防护
→ dap continue --break script.py:8 --remove-break script.py:41
  ← 收窄:在数据源处加断点,移除已用过的断点
  Stopped at main():8, items loaded from config as []

Root cause: missing guard. Fix → dap stop.
```

**无假设(异常,位置未知):**

```
Exception: TypeError, location unknown
→ dap debug script.py --break-on-exception raised
  Stopped at compute():41, items=None
Root cause: None passed where list expected.
```

## 验证你的修复

在 bug 位置暂停时,用 `eval` 在实时状态上测试你提出的修复表达式。如果在 eval 中生效,在代码里也一定生效。然后修改代码,`dap restart` 端到端确认。

应用修复后,重新跑同一场景进行验证。`dap restart` 用相同参数和断点重新运行——形成快速反馈闭环。在你亲眼看到原本发现 bug 的同一断点处行为已正确之前,不要相信修复有效。

## 清理

`dap` 会话通常在程序退出或空闲超时时自动终止。
当应用未正常关闭时(例如你在调试时把它 kill 了),可以手动终止:`dap stop`。

## 局限性

- 仅当任务与上游来源和本地项目上下文明确匹配时才使用本技能。
- 在应用变更前,请验证命令、生成的代码、依赖、凭据和外部服务行为。
- 不要把示例当作环境特定测试、安全审查或用户对破坏性/高代价操作的批准的替代品。