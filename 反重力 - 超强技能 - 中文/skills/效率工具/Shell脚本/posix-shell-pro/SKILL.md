---
name: posix-shell-pro
description: 精通严格 POSIX sh 脚本编写，实现跨类 Unix 系统的最大可移植性。专注于能在任何 POSIX 兼容 shell（dash、ash、sh、bash --posix）上运行的 shell 脚本。
risk: critical
source: community
date_added: '2026-02-27'
---

## 使用场景

- 处理 posix shell pro 相关任务或工作流时
- 需要 posix shell pro 的指导、最佳实践或检查清单时

## 不适用场景

- 任务与 posix shell pro 无关时
- 需要此范围之外的其他领域或工具时

## 指导原则

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可操作的步骤和验证方法
- 如需详细示例，请查阅 `resources/implementation-playbook.md`

## 核心关注点

- 严格 POSIX 合规，实现最大可移植性
- Shell 无关的脚本编写，兼容任何类 Unix 系统
- 防御性编程，使用可移植的错误处理
- 安全的参数解析，避免 bash 特有特性
- 可移植的文件操作和资源管理
- 跨平台兼容性（Linux、BSD、Solaris、AIX、macOS）
- 使用 dash、ash 和 POSIX 模式进行测试验证
- 使用 ShellCheck 进行 POSIX 模式静态分析
- 极简方法，仅使用 POSIX 规范特性
- 兼容遗留系统和嵌入式环境

## POSIX 约束

- 无数组（使用位置参数或分隔字符串）
- 无 `[[` 条件判断（仅使用 `[` 测试命令）
- 无进程替换 `<()` 或 `>()`
- 无花括号展开 `{1..10}`
- 无 `local` 关键字（谨慎使用函数作用域变量）
- 无 `declare`、`typeset` 或 `readonly` 变量属性
- 无 `+=` 字符串连接运算符
- 无 `${var//pattern/replacement}` 替换
- 无关联数组或哈希表
- 无 `source` 命令（使用 `.` 加载文件）

## 方法论

- 始终使用 `#!/bin/sh` shebang 指定 POSIX shell
- 使用 `set -eu` 进行错误处理（POSIX 中无 `pipefail`）
- 引用所有变量展开：`"$var"` 而非 `$var`
- 使用 `[ ]` 进行所有条件测试，切勿使用 `[[`
- 使用 `while` 和 `case` 实现参数解析（长选项不使用 `getopts`）
- 使用 `mktemp` 安全创建临时文件，并设置清理 trap
- 所有输出使用 `printf` 而非 `echo`（echo 行为不一致）
- 加载脚本使用 `. script.sh` 而非 `source script.sh`
- 使用显式 `|| exit 1` 检查实现错误处理
- 设计幂等脚本并支持 dry-run 模式
- 谨慎操作 `IFS` 并恢复原始值
- 使用 `[ -n "$var" ]` 和 `[ -z "$var" ]` 验证输入
- 使用 `--` 结束选项解析，使用 `rm -rf -- "$dir"` 确保安全
- 使用命令替换 `$()` 而非反引号，提高可读性
- 使用 `date` 实现带时间戳的结构化日志
- 使用 dash/ash 测试脚本以验证 POSIX 合规性

## 兼容性与可移植性

- 使用 `#!/bin/sh` 调用系统的 POSIX shell
- 在多个 shell 上测试：dash（Debian/Ubuntu 默认）、ash（Alpine/BusyBox）、bash --posix
- 避免 GNU 特有选项；仅使用 POSIX 规范标志
- 处理平台差异：使用 `uname -s` 检测操作系统
- 使用 `command -v` 而非 `which`（更可移植）
- 检查命令可用性：`command -v cmd >/dev/null 2>&1 || exit 1`
- 为缺失工具提供可移植的替代实现
- 使用 `[ -e "$file" ]` 检查文件存在性（兼容所有系统）
- 避免使用 `/dev/stdin`、`/dev/stdout`（非普遍可用）
- 使用显式重定向而非 `&>`（bash 特有）

## 可读性与可维护性

- 导出变量使用 UPPER_CASE，局部变量使用 lower_case
- 添加带注释块的章节标题以组织代码
- 保持函数在 50 行以内；提取复杂逻辑
- 使用一致的缩进（仅空格，通常 2 或 4 个）
- 在注释中记录函数用途和参数
- 使用有意义的命名：`validate_input` 而非 `check`
- 为非显而易见的 POSIX 变通方案添加注释
- 使用描述性标题分组相关函数
- 将重复代码提取为函数
- 使用空行分隔逻辑段落

## 安全模式

- 引用所有变量展开以防止单词分割
- 操作前验证文件权限：`[ -r "$file" ] || exit 1`
- 使用前清理用户输入
- 验证数字输入：`case $num in *[!0-9]*) exit 1 ;; esac`
- 切勿对不可信输入使用 `eval`
- 使用 `--` 分隔选项和参数：`rm -- "$file"`
- 验证必需变量：`[ -n "$VAR" ] || { echo "VAR required" >&2; exit 1; }`
- 显式检查退出码：`cmd || { echo "failed" >&2; exit 1; }`
- 使用 `trap` 进行清理：`trap 'rm -f "$tmpfile"' EXIT INT TERM`
- 为敏感文件设置限制性 umask：`umask 077`
- 将安全相关操作记录到 syslog 或文件
- 验证文件路径不包含意外字符
- 安全关键脚本中使用命令的完整路径：`/bin/rm` 而非 `rm`

## 性能优化

- 尽可能使用 shell 内建命令而非外部命令
- 避免在循环中生成子 shell：使用 `while read` 而非 `for i in $(cat)`
- 缓存命令结果到变量中，避免重复执行
- 使用 `case` 进行多字符串比较（比重复 `if` 更快）
- 大文件逐行处理
- 使用 `expr` 或 `$(( ))` 进行算术运算（POSIX 支持 `$(( ))`）
- 最小化紧密循环中的外部命令调用
- 仅需真/假时使用 `grep -q`（比捕获输出更快）
- 批量处理类似操作
- 使用 here-document 处理多行字符串，避免多次 echo 调用

## 文档标准

- 实现 `-h` 标志提供帮助（避免无适当解析的 `--help`）
- 包含显示概要和选项的使用说明
- 清晰区分必需参数和可选参数
- 列出退出码：0=成功，1=错误，特定失败使用特定代码
- 记录前置条件和必需命令
- 添加包含脚本用途和作者的头部注释
- 包含常见使用模式的示例
- 记录脚本使用的环境变量
- 提供常见问题的故障排除指导
- 在文档中注明 POSIX 合规性

## 无数组工作模式

由于 POSIX sh 缺乏数组，使用以下模式：

- **位置参数**：`set -- item1 item2 item3; for arg; do echo "$arg"; done`
- **分隔字符串**：`items="a:b:c"; IFS=:; set -- $items; IFS=' '`
- **换行分隔**：`items="a\nb\nc"; while IFS= read -r item; do echo "$item"; done <<EOF`
- **计数器**：`i=0; while [ $i -lt 10 ]; do i=$((i+1)); done`
- **字段分割**：使用 `cut`、`awk` 或参数展开进行字符串分割

## 可移植条件判断

使用 `[ ]` 测试命令配合 POSIX 运算符：

- **文件测试**：`[ -e file ]` 存在，`[ -f file ]` 常规文件，`[ -d dir ]` 目录
- **字符串测试**：`[ -z "$str" ]` 空，`[ -n "$str" ]` 非空，`[ "$a" = "$b" ]` 相等
- **数值测试**：`[ "$a" -eq "$b" ]` 等于，`[ "$a" -lt "$b" ]` 小于
- **逻辑运算**：`[ cond1 ] && [ cond2 ]` 与，`[ cond1 ] || [ cond2 ]` 或
- **取反**：`[ ! -f file ]` 非文件
- **模式匹配**：使用 `case` 而非 `[[ =~ ]]`

## CI/CD 集成

- **矩阵测试**：在 Linux、macOS、Alpine 上测试 dash、ash、bash --posix、yash
- **容器测试**：使用 alpine:latest（ash）、debian:stable（dash）进行可重现测试
- **Pre-commit 钩子**：配置 checkbashisms、shellcheck -s sh、shfmt -ln posix
- **GitHub Actions**：使用 shellcheck-problem-matchers 配合 POSIX 模式
- **跨平台验证**：在 Linux、macOS、FreeBSD、NetBSD 上测试
- **BusyBox 测试**：在 BusyBox 环境中验证嵌入式系统兼容性
- **自动化发布**：标记版本并生成可移植分发包
- **覆盖率跟踪**：确保所有 POSIX shell 的测试覆盖
- 示例工作流：`shellcheck -s sh *.sh && shfmt -ln posix -d *.sh && checkbashisms *.sh`

## 嵌入式系统与受限环境

- **BusyBox 兼容性**：使用 BusyBox 有限的 ash 实现进行测试
- **Alpine Linux**：默认 shell 是 BusyBox ash，而非 bash
- **资源约束**：最小化内存使用，避免生成过多进程
- **缺失工具**：常用工具不可用时提供回退方案（`mktemp`、`seq`）
- **只读文件系统**：处理 `/tmp` 可能受限的场景
- **无 coreutils**：部分环境缺少 GNU coreutils 扩展
- **信号处理**：最小环境中的信号支持有限
- **启动脚本**：初始化脚本必须使用 POSIX 以实现最大兼容性
- 示例：检查 mktemp：`command -v mktemp >/dev/null 2>&1 || mktemp() { ... }`

## 从 Bash 迁移到 POSIX sh

- **评估**：运行 `checkbashisms` 识别 bash 特有构造
- **消除数组**：将数组转换为分隔字符串或位置参数
- **更新条件判断**：将 `[[` 替换为 `[`，将正则调整为 `case` 模式
- **局部变量**：移除 `local` 关键字，改用函数前缀
- **进程替换**：将 `<()` 替换为临时文件或管道
- **参数展开**：使用 `sed`/`awk` 进行复杂字符串操作
- **测试策略**：增量转换并持续验证
- **文档记录**：注明任何 POSIX 限制或变通方案
- **渐进迁移**：一次转换一个函数，彻底测试
- **回退支持**：过渡期间如需要可维护双重实现

## 质量检查清单

- 脚本通过 ShellCheck `-s sh` 标志（POSIX 模式）
- 代码使用 shfmt `-ln posix` 保持格式一致
- 在多个 shell 上测试：dash、ash、bash --posix、yash
- 所有变量展开正确引用
- 未使用 bash 特有特性（数组、`[[`、`local` 等）
- 错误处理覆盖所有失败模式
- 使用 EXIT trap 清理临时资源
- 脚本提供清晰的使用说明
- 输入验证防止注入攻击
- 脚本可在类 Unix 系统间移植（Linux、BSD、Solaris、macOS、Alpine）
- BusyBox 兼容性已针对嵌入式用例验证
- 未使用 GNU 特有扩展或标志

## 输出内容

- 最大化可移植性的 POSIX 合规 shell 脚本
- 使用 shellspec 或 bats-core 的测试套件，在 dash、ash、yash 上验证
- 多 shell 矩阵测试的 CI/CD 配置
- 带回退方案的常见模式可移植实现
- POSIX 限制和变通方案的文档及示例
- 将 bash 脚本逐步转换为 POSIX sh 的迁移指南
- 跨平台兼容性矩阵（Linux、BSD、macOS、Solaris、Alpine）
- 不同 POSIX shell 的性能基准对比
- 缺失工具的回退实现（mktemp、seq、timeout）
- 适用于嵌入式和容器环境的 BusyBox 兼容脚本
- 无 bash 依赖的各平台分发包

## 核心工具

### 静态分析与格式化
- **ShellCheck**：静态分析器，使用 `-s sh` 进行 POSIX 模式验证
- **shfmt**：Shell 格式化工具，使用 `-ln posix` 选项处理 POSIX 语法
- **checkbashisms**：检测脚本中的 bash 特有构造（来自 devscripts）
- **Semgrep**：SAST，支持 POSIX 特有安全规则
- **CodeQL**：Shell 脚本安全扫描

### 用于测试的 POSIX Shell 实现
- **dash**：Debian Almquist Shell - 轻量级，严格 POSIX 合规（主要测试目标）
- **ash**：Almquist Shell - BusyBox 默认，嵌入式系统
- **yash**：Yet Another Shell - 严格 POSIX 一致性验证
- **posh**：Policy-compliant Ordinary Shell - Debian 策略合规
- **osh**：Oil Shell - 现代 POSIX 兼容 shell，提供更好的错误信息
- **bash --posix**：GNU Bash 的 POSIX 模式，用于兼容性测试

### 测试框架
- **bats-core**：Bash 测试框架（兼容 POSIX sh）
- **shellspec**：BDD 风格测试，支持 POSIX sh
- **shunit2**：xUnit 风格框架，支持 POSIX sh
- **sharness**：Git 使用的测试框架（POSIX 兼容）

## 常见陷阱

- 使用 `[[` 而非 `[`（bash 特有）
- 使用数组（POSIX sh 中不存在）
- 使用 `local` 关键字（bash/ksh 扩展）
- 使用 `echo` 而非 `printf`（行为因实现而异）
- 使用 `source` 而非 `.` 加载脚本
- 使用 bash 特有的参数展开：`${var//pattern/replacement}`
- 使用进程替换 `<()` 或 `>()`
- 使用 `function` 关键字（ksh/bash 语法）
- 使用 `$RANDOM` 变量（POSIX 中不存在）
- 使用 `read -a` 读取数组（bash 特有）
- 使用 `set -o pipefail`（bash 特有）
- 使用 `&>` 进行重定向（使用 `>file 2>&1`）

## 高级技巧

- **错误捕获**：`trap 'echo "Error at line $LINENO" >&2; exit 1' EXIT; trap - EXIT` 成功时清除
- **安全临时文件**：`tmpfile=$(mktemp) || exit 1; trap 'rm -f "$tmpfile"' EXIT INT TERM`
- **模拟数组**：`set -- item1 item2 item3; for arg; do process "$arg"; done`
- **字段解析**：`IFS=:; while read -r user pass uid gid; do ...; done < /etc/passwd`
- **字符串替换**：`echo "$str" | sed 's/old/new/g'` 或使用参数展开 `${str%suffix}`
- **默认值**：`value=${var:-default}` 变量未设置或为空时赋默认值
- **可移植函数**：避免 `function` 关键字，使用 `func_name() { ... }`
- **子 shell 隔离**：`(cd dir && cmd)` 切换目录不影响父 shell
- **Here-document**：`cat <<'EOF'` 使用引号可防止变量展开
- **命令存在性**：`command -v cmd >/dev/null 2>&1 && echo "found" || echo "missing"`

## POSIX 特有最佳实践

- 始终引用变量展开：`"$var"` 而非 `$var`
- 使用 `[ ]` 并正确添加空格：`[ "$a" = "$b" ]` 而非 `["$a"="$b"]`
- 使用 `=` 进行字符串比较，而非 `==`（bash 扩展）
- 使用 `.` 加载脚本，而非 `source`
- 所有输出使用 `printf`，避免 `echo -e` 或 `echo -n`
- 使用 `$(( ))` 进行算术运算，而非 `let` 或 `declare -i`
- 使用 `case` 进行模式匹配，而非 `[[ =~ ]]`
- 使用 `sh -n script.sh` 检查脚本语法
- 使用 `command -v` 而非 `type` 或 `which` 以提高可移植性
- 使用 `|| exit 1` 显式处理所有错误条件

## 参考与延伸阅读

### POSIX 标准与规范
- [POSIX Shell Command Language](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html) - 官方 POSIX.1-2024 规范
- [POSIX Utilities](https://pubs.opengroup.org/onlinepubs/9699919799/idx/utilities.html) - POSIX 强制工具完整列表
- [Autoconf Portable Shell Programming](https://www.gnu.org/software/autoconf/manual/autoconf.html#Portable-Shell) - GNU 官方可移植性指南

### 可移植性与最佳实践
- [Rich's sh (POSIX shell) tricks](http://www.etalabs.net/sh_tricks.html) - 高级 POSIX shell 技巧
- [Suckless Shell Style Guide](https://suckless.org/coding_style/) - 极简 POSIX sh 模式
- [FreeBSD Porter's Handbook - Shell](https://docs.freebsd.org/en/books/porters-handbook/makefiles/#porting-shlibs) - BSD 可移植性注意事项

### 工具与测试
- [checkbashisms](https://manpages.debian.org/testing/devscripts/checkbashisms.1.en.html) - 检测 bash 特有构造

## 限制说明

- 仅当任务明确匹配上述范围时使用此技能
- 切勿将输出视为环境特定验证、测试或专家评审的替代品
- 如缺少必需输入、权限、安全边界或成功标准，请停下来请求澄清