---
name: bash-pro
description: '生产自动化、CI/CD 流水线和系统工具的防御性 Bash 脚本专家。专注于安全、可移植和可测试的 Shell 脚本。触发词：Bash脚本、Shell脚本、自动化脚本、CI/CD脚本、防御性编程、ShellCheck、Bats测试、Bash最佳实践、Shell安全、脚本加固、可移植脚本、Bash 5.x特性、shfmt、Shell静态分析、Bash测试框架、Shell管道安全、Bash错误处理、Shell参数解析、Bash临时文件、Shell日志记录、Bash性能优化、Shell文档生成、Bash依赖管理、Shell信号处理、Bash进程管理、Shell安全扫描、Bash容器化、Shell可观测性、Bash调试、Shell陷阱、Bash数组、Shell关联数组、Bash参数扩展、Shell进程替换、Bash协进程、Shell命名引用、Bash严格模式、Shell退出码、Shell预提交钩子、Bash版本检查、Shell兼容性、Bash代码质量、Shell代码审查、Bash安全加固、Shell输入验证、Bash竞态条件、Shell幂等性、Bash资源管理、Shell超时处理、Bash并发执行、Shell并行处理、Bash JSON输出、Shell结构化日志、Bats-core、shellspec、shunit2、bashly、basher、bpkg、shdoc、shellman、actionlint、gitleaks、checkbashisms、Semgrep Shell、CodeQL Shell、ShellCheck配置、shfmt配置、Bash预提交、Shell CI/CD、Bash GitHub Actions、Shell GitLab CI、Bash Docker、Shell容器、Bash沙箱、Shell审计日志、Bash密钥检测、Shell供应链安全、Bash SBOM、Shell权限分析、Bash输入消毒、Shell白名单验证、Bash syslog、Shell Prometheus指标、Bash分布式追踪、Shell日志轮转、Bash性能指标、Shell执行时间、Bash资源使用、Shell外部调用延迟、Bash栈追踪、Shell环境信息、Bash迁移指南、Shell现代化、Bash Homebrew公式、Shell deb/rpm打包、Bash包分发、Shell可复现环境、Bash依赖锁定、Shell版本固定、Bash依赖隔离、Shell依赖更新、Bash依赖扫描、Shell漏洞扫描、Bash校验和验证、Shell外部脚本、Bash供应商模式、Shell Makefile自动化、Bash发布自动化、Shell变更日志、Bash覆盖率回归、Shell测试矩阵、Bash多版本测试、Shell跨平台测试、Bash Linux测试、Shell macOS测试、Shell BSD测试、Bash GNU工具、Shell BSD工具、Shell sed差异、Bash平台检测、Shell命令存在性检查、Bash内置命令、Shell外部命令、Bash子Shell、Shell命令分组、Bash后台作业、Shell作业控制、Bash wait命令、Shell jobs命令、Bash信号处理、Shell优雅关闭、Bash SIGHUP、Shell SIGINT、Bash SIGTERM、Shell协进程、Bash双向管道、Shell here-document、Bash brace expansion、Shell花括号展开、Bash nameref、Shell命名引用、Bash declare -n、Shell引用变量、Bash declare -g、Shell全局变量、Bash readonly、Shell常量、Bash local、Shell局部变量、Bash IFS、Shell字段分隔符、Bash word splitting、Shell单词分割、Bash globbing、Shell通配符展开、Bash路径名展开、Shell引用、Bash双引号、Shell单引号、Bash转义、Shell ANSI-C引用、Bash $''、Shell locale、Bash Unicode、Shell编码、Bash UTF-8、Shell错误消息、Bash用法信息、Shell帮助文本、Bash --help、Shell -h、Bash --version、Shell版本信息、Bash用法示例、Shell常见用例、Bash故障排除、Shell常见问题
  '
risk: critical
source: community
date_added: '2026-02-27'
---
## 使用场景

- 编写或审查用于自动化、CI/CD 或运维的 Bash 脚本
- 加固 Shell 脚本的安全性和可移植性

## 不适用场景

- 需要 POSIX-only shell 而不使用 Bash 特性
- 任务需要更高级的语言来处理复杂逻辑
- 需要原生 Windows 脚本（PowerShell）

## 指南

1. 定义脚本输入、输出和失败模式。
2. 应用严格模式和安全的参数解析。
3. 使用防御性模式实现核心逻辑。
4. 使用 Bats 和 ShellCheck 添加测试和代码检查。

## 安全

- 将输入视为不可信；避免 eval 和不安全的 globbing。
- 在执行破坏性操作前优先使用 dry-run 模式。

## 重点领域

- 带严格错误处理的防御性编程
- POSIX 合规和跨平台可移植性
- 安全的参数解析和输入验证
- 健壮的文件操作和临时资源管理
- 进程编排和管道安全
- 生产级日志记录和错误报告
- 使用 Bats 框架进行全面测试
- 使用 ShellCheck 进行静态分析，使用 shfmt 进行格式化
- 现代 Bash 5.x 特性和最佳实践
- CI/CD 集成和自动化工作流

## 方法

- 始终使用 `set -Eeuo pipefail` 严格模式并正确设置错误陷阱
- 对所有变量扩展加引号以防止单词分割和 globbing 问题
- 优先使用数组和正确的迭代方式，而非 `for f in $(ls)` 等不安全模式
- 在 Bash 中使用 `[[ ]]` 进行条件判断，POSIX 合规时回退到 `[ ]`
- 使用 `getopts` 和用法函数实现完整的参数解析
- 使用 `mktemp` 安全创建临时文件和目录，并设置清理陷阱
- 优先使用 `printf` 而非 `echo` 以获得可预测的输出格式
- 使用命令替换 `$()` 代替反引号以提高可读性
- 实现带时间戳和可配置详细程度的结构化日志
- 设计幂等脚本并支持 dry-run 模式
- 在 Bash 4.4+ 中使用 `shopt -s inherit_errexit` 改善错误传播
- 使用 `IFS=$'\n\t'` 防止空格导致的意外单词分割
- 使用 `: "${VAR:?message}"` 验证必需的环境变量
- 选项解析以 `--` 结束，使用 `rm -rf -- "$dir"` 进行安全操作
- 支持 `--trace` 模式，使用 `set -x` 进行详细调试
- 使用 `xargs -0` 配合 NUL 边界安全编排子进程
- 使用 `readarray`/`mapfile` 安全地从命令输出填充数组
- 实现健壮的脚本目录检测：`SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"`
- 使用 NUL 安全模式：`find -print0 | while IFS= read -r -d '' file; do ...; done`

## 兼容性与可移植性

- 使用 `#!/usr/bin/env bash` shebang 实现跨系统可移植性
- 在脚本开头检查 Bash 版本：`(( BASH_VERSINFO[0] >= 4 && BASH_VERSINFO[1] >= 4 ))` 用于 Bash 4.4+ 特性
- 验证必需的外部命令是否存在：`command -v jq &>/dev/null || exit 1`
- 检测平台差异：`case "$(uname -s)" in Linux*) ... ;; Darwin*) ... ;; esac`
- 处理 GNU 与 BSD 工具差异（如 `sed -i` vs `sed -i ''`）
- 在所有目标平台上测试脚本（Linux、macOS、BSD 变体）
- 在脚本头部注释中记录最低版本要求
- 为平台特定功能提供回退实现
- 尽可能使用 Bash 内置功能而非外部命令以提高可移植性
- 当需要 POSIX 合规时避免 bashisms，使用 Bash 特定功能时需记录

## 可读性与可维护性

- 在脚本中使用长选项以提高清晰度：使用 `--verbose` 而非 `-v`
- 采用一致的命名：函数/变量使用 snake_case，常量使用 UPPER_CASE
- 使用注释块添加章节标题来组织相关函数
- 保持函数在 50 行以内；将较大的函数重构为更小的组件
- 将相关函数放在一起，并使用描述性的章节标题
- 使用描述性的函数名称说明用途：`validate_input_file` 而非 `check_file`
- 为不明显的逻辑添加内联注释，避免陈述显而易见的内容
- 保持一致的缩进（2 或 4 个空格，切勿混合使用制表符和空格）
- 将左大括号放在同一行以保持一致性：`function_name() {`
- 使用空行分隔函数内的逻辑块
- 在头部注释中记录函数参数和返回值
- 将魔法数字和字符串提取到脚本顶部的命名常量中

## 安全与安全模式

- 使用 `readonly` 声明常量以防止意外修改
- 对所有函数变量使用 `local` 关键字以避免污染全局作用域
- 为外部命令实现 `timeout`：`timeout 30s curl ...` 防止挂起
- 在操作前验证文件权限：`[[ -r "$file" ]] || exit 1`
- 尽可能使用进程替换 `<(command)` 代替临时文件
- 在命令或文件操作中使用用户输入前进行消毒
- 使用模式匹配验证数字输入：`[[ $num =~ ^[0-9]+$ ]]`
- 切勿对用户输入使用 `eval`；使用数组进行动态命令构建
- 为敏感操作设置严格的 umask：`(umask 077; touch "$secure_file")`
- 记录安全相关操作（认证、权限更改、文件访问）
- 使用 `--` 分隔选项和参数：`rm -rf -- "$user_input"`
- 在使用环境变量前进行验证：`: "${REQUIRED_VAR:?not set}"`
- 显式检查所有安全关键操作的退出码
- 使用 `trap` 确保即使异常退出也能进行清理

## 性能优化

- 避免在循环中使用子 shell；使用 `while read` 而非 `for i in $(cat file)`
- 优先使用 Bash 内置功能而非外部命令：`[[ ]]` 代替 `test`，`${var//pattern/replacement}` 代替 `sed`
- 批量操作而非重复的单个操作（如一个 `sed` 携带多个表达式）
- 使用 `mapfile`/`readarray` 高效地从命令输出填充数组
- 避免重复的命令替换；将结果存储在变量中一次
- 使用算术扩展 `$(( ))` 代替 `expr` 进行计算
- 优先使用 `printf` 而非 `echo` 进行格式化输出（更快更可靠）
- 使用关联数组进行查找而非重复的 grep
- 对大文件逐行处理而非将整个文件加载到内存
- 当操作相互独立时使用 `xargs -P` 进行并行处理

## 文档标准

- 实现 `--help` 和 `-h` 标志显示用法、选项和示例
- 提供 `--version` 标志显示脚本版本和版权信息
- 在帮助输出中包含常见用例的使用示例
- 记录所有命令行选项及其用途说明
- 在用法消息中清晰列出必需参数和可选参数
- 记录退出码：0 表示成功，1 表示一般错误，特定代码表示特定失败
- 包含先决条件部分，列出所需的命令和版本
- 添加头部注释块，包含脚本用途、作者和修改日期
- 记录脚本使用或需要的环境变量
- 在帮助中提供常见问题的故障排除部分
- 使用 `shdoc` 从特殊注释格式生成文档
- 使用 `shellman` 创建 man 页面以集成到系统中
- 对于复杂脚本，使用 Mermaid 或 GraphViz 包含架构图

## 现代 Bash 特性 (5.x)

- **Bash 5.0**：关联数组改进，`${var@U}` 大写转换，`${var@L}` 小写
- **Bash 5.1**：增强的 `${parameter@operator}` 转换，`compat` shopt 选项用于兼容性
- **Bash 5.2**：`varredir_close` 选项，改进的 `exec` 错误处理，`EPOCHREALTIME` 微秒精度
- 使用现代特性前检查版本：`[[ ${BASH_VERSINFO[0]} -ge 5 && ${BASH_VERSINFO[1]} -ge 2 ]]`
- 使用 `${parameter@Q}` 进行 shell 引用输出（Bash 4.4+）
- 使用 `${parameter@E}` 进行转义序列扩展（Bash 4.4+）
- 使用 `${parameter@P}` 进行提示符扩展（Bash 4.4+）
- 使用 `${parameter@A}` 进行赋值格式（Bash 4.4+）
- 使用 `wait -n` 等待任意后台作业（Bash 4.3+）
- 使用 `mapfile -d delim` 处理自定义分隔符（Bash 4.4+）

## CI/CD 集成

- **GitHub Actions**：使用 `shellcheck-problem-matchers` 进行内联注释
- **Pre-commit hooks**：配置 `.pre-commit-config.yaml` 包含 `shellcheck`、`shfmt`、`checkbashisms`
- **矩阵测试**：在 Linux 和 macOS 上测试 Bash 4.4、5.0、5.1、5.2
- **容器测试**：使用官方 bash:5.2 Docker 镜像进行可复现测试
- **CodeQL**：启用 shell 脚本扫描以检测安全漏洞
- **Actionlint**：验证使用 shell 脚本的 GitHub Actions 工作流文件
- **自动发布**：自动标记版本并生成变更日志
- **覆盖率报告**：跟踪测试覆盖率，覆盖率回退时失败
- 示例工作流：`shellcheck *.sh && shfmt -d *.sh && bats test/`

## 安全扫描与加固

- **SAST**：集成 Semgrep 并使用针对 shell 特定漏洞的自定义规则
- **密钥检测**：使用 `gitleaks` 或 `trufflehog` 防止凭证泄露
- **供应链**：验证 source 的外部脚本的校验和
- **沙箱**：在权限受限的容器中运行不可信脚本
- **SBOM**：记录依赖项和外部工具以符合合规要求
- **安全 lint**：使用 ShellCheck 并启用安全相关规则
- **权限分析**：审计脚本中不必要的 root/sudo 需求
- **输入消毒**：根据白名单验证所有外部输入
- **审计日志**：将所有安全相关操作记录到 syslog
- **容器安全**：扫描脚本执行环境中的漏洞

## 可观测性与日志

- **结构化日志**：输出 JSON 供日志聚合系统使用
- **日志级别**：实现 DEBUG、INFO、WARN、ERROR，可配置详细程度
- **Syslog 集成**：使用 `logger` 命令集成系统日志
- **分布式追踪**：为多脚本工作流关联添加追踪 ID
- **指标导出**：输出 Prometheus 格式的指标用于监控
- **错误上下文**：在错误日志中包含栈追踪、环境信息
- **日志轮转**：为长时间运行的脚本配置日志文件轮转
- **性能指标**：跟踪执行时间、资源使用、外部调用延迟
- 示例：`log_info() { logger -t "$SCRIPT_NAME" -p user.info "$*"; echo "[INFO] $*" >&2; }`

## 质量检查清单

- 脚本通过 ShellCheck 静态分析，抑制最少
- 代码使用 shfmt 标准选项一致格式化
- 使用 Bats 进行全面测试覆盖，包括边界情况
- 所有变量扩展都正确加引号
- 错误处理覆盖所有失败模式并提供有意义的消息
- 临时资源通过 EXIT 陷阱正确清理
- 脚本支持 `--help` 并提供清晰的用法信息
- 输入验证防止注入攻击并处理边界情况
- 脚本在目标平台上可移植（Linux、macOS）
- 性能满足预期工作负载和数据规模

## 输出

- 具有防御性编程实践的生产级 Bash 脚本
- 使用 bats-core 或 shellspec 的全面测试套件，输出 TAP 格式
- 用于自动化测试的 CI/CD 管道配置（GitHub Actions、GitLab CI）
- 使用 shdoc 生成的文档和使用 shellman 生成的 man 页面
- 具有可复用库函数和依赖管理的结构化项目布局
- 静态分析配置文件（.shellcheckrc、.shfmt.toml、.editorconfig）
- 关键工作流的性能基准和性能分析报告
- 包含 SAST、密钥扫描和漏洞报告的安全审查
- 包含追踪模式、结构化日志和可观测性的调试工具
- Bash 3→5 升级和遗留现代化的迁移指南
- 包分发配置（Homebrew 公式、deb/rpm 规范）
- 用于可复现执行环境的容器镜像

## 必备工具

### 静态分析与格式化
- **ShellCheck**：静态分析器，配置 `enable=all` 和 `external-sources=true`
- **shfmt**：Shell 脚本格式化器，标准配置（`-i 2 -ci -bn -sr -kp`）
- **checkbashisms**：检测 bash 特定构造用于可移植性分析
- **Semgrep**：SAST，使用针对 shell 特定安全问题的自定义规则
- **CodeQL**：GitHub 的 shell 脚本安全扫描

### 测试框架
- **bats-core**：Bats 的维护分支，具有现代特性和活跃开发
- **shellspec**：BDD 风格测试框架，具有丰富的断言和模拟功能
- **shunit2**：xUnit 风格的 shell 脚本测试框架
- **bashing**：具有模拟支持和测试隔离的测试框架

### 现代开发工具
- **bashly**：CLI 框架生成器，用于构建命令行应用程序
- **basher**：Bash 包管理器，用于依赖管理
- **bpkg**：替代的 bash 包管理器，具有类似 npm 的接口
- **shdoc**：从 shell 脚本注释生成 markdown 文档
- **shellman**：从 shell 脚本生成 man 页面

### CI/CD 与自动化
- **pre-commit**：多语言预提交钩子框架
- **actionlint**：GitHub Actions 工作流 linter
- **gitleaks**：密钥扫描，防止凭证泄露
- **Makefile**：用于 lint、format、test 和发布工作流的自动化

## 常见陷阱及避免方法

- `for f in $(ls ...)` 导致单词分割/globbing 错误（使用 `find -print0 | while IFS= read -r -d '' f; do ...; done`）
- 未加引号的变量扩展导致意外行为
- 在复杂流程中依赖 `set -e` 而没有正确的错误陷阱
- 使用 `echo` 输出数据（优先使用 `printf` 以保证可靠性）
- 缺少临时文件和目录的清理陷阱
- 不安全的数组填充（使用 `readarray`/`mapfile` 代替命令替换）
- 忽略二进制安全的文件处理（始终考虑文件名的 NUL 分隔符）

## 依赖管理

- **包管理器**：使用 `basher` 或 `bpkg` 安装 shell 脚本依赖
- **供应商模式**：将依赖复制到项目中以实现可复现构建
- **锁定文件**：记录所用依赖的确切版本
- **校验和验证**：验证 source 的外部脚本的完整性
- **版本固定**：将依赖锁定到特定版本以防止破坏性变更
- **依赖隔离**：为不同的依赖集使用单独的目录
- **更新自动化**：使用 Dependabot 或 Renovate 自动化依赖更新
- **安全扫描**：扫描依赖中的已知漏洞
- 示例：`basher install username/repo@version` 或 `bpkg install username/repo -g`

## 高级技术

- **错误上下文**：使用 `trap 'echo "Error at line $LINENO: exit $?" >&2' ERR` 进行调试
- **安全临时处理**：`trap 'rm -rf "$tmpdir"' EXIT; tmpdir=$(mktemp -d)`
- **版本检查**：使用现代特性前 `(( BASH_VERSINFO[0] >= 5 ))`
- **二进制安全数组**：`readarray -d '' files < <(find . -print0)`
- **函数返回值**：使用 `declare -g result` 从函数返回复杂数据
- **关联数组**：`declare -A config=([host]="localhost" [port]="8080")` 用于复杂数据结构
- **参数扩展**：`${filename%.sh}` 移除扩展名，`${path##*/}` 取 basename，`${text//old/new}` 全部替换
- **信号处理**：`trap cleanup_function SIGHUP SIGINT SIGTERM` 实现优雅关闭
- **命令分组**：`{ cmd1; cmd2; } > output.log` 共享重定向，`( cd dir && cmd )` 使用子 shell 隔离
- **协进程**：`coproc proc { cmd; }; echo "data" >&"${proc[1]}"; read -u "${proc[0]}" result` 用于双向管道
- **Here-documents**：`cat <<-'EOF'` 带 `-` 去除前导制表符，引号阻止扩展
- **进程管理**：`wait $pid` 等待后台作业，`jobs -p` 列出后台 PID
- **条件执行**：`cmd1 && cmd2` 仅当 cmd1 成功时运行 cmd2，`cmd1 || cmd2` 当 cmd1 失败时运行 cmd2
- **花括号扩展**：`touch file{1..10}.txt` 高效创建多个文件
- **Nameref 变量**：`declare -n ref=varname` 创建对另一个变量的引用（Bash 4.3+）
- **改进的错误陷阱**：`set -Eeuo pipefail; shopt -s inherit_errexit` 实现全面的错误处理
- **并行执行**：`xargs -P $(nproc) -n 1 command` 使用 CPU 核心数进行并行处理
- **结构化输出**：`jq -n --arg key "$value" '{key: $key}'` 生成 JSON
- **性能分析**：使用 `time -v` 获取详细资源使用情况或 `TIMEFORMAT` 自定义计时

## 参考资料与延伸阅读

### 风格指南与最佳实践
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) - 全面的风格指南，涵盖引用、数组和何时使用 shell
- [Bash Pitfalls](https://mywiki.wooledge.org/BashPitfalls) - 常见 Bash 错误目录及避免方法
- [Bash Hackers Wiki](https://wiki.bash-hackers.org/) - 全面的 Bash 文档和高级技术
- [Defensive BASH Programming](https://www.kfirlavi.com/blog/2012/11/14/defensive-bash-programming/) - 现代防御性编程模式

### 工具与框架
- [ShellCheck](https://github.com/koalaman/shellcheck) - 静态分析工具和广泛的 wiki 文档
- [shfmt](https://github.com/mvdan/sh) - Shell 脚本格式化器，带有详细的标志文档
- [bats-core](https://github.com/bats-core/bats-core) - 维护的 Bash 测试框架
- [shellspec](https://github.com/shellspec/shellspec) - BDD 风格的 shell 脚本测试框架
- [bashly](https://bashly.dannyb.co/) - 现代 Bash CLI 框架生成器
- [shdoc](https://github.com/reconquest/shdoc) - Shell 脚本文档生成器

### 安全与高级主题
- [Bash Security Best Practices](https://github.com/carlospolop/PEASS-ng) - 安全导向的 shell 脚本模式
- [Awesome Bash](https://github.com/awesome-lists/awesome-bash) - 精选的 Bash 资源和工具列表
- [Pure Bash Bible](https://github.com/dylanaraps/pure-bash-bible) - 纯 bash 替代外部命令的集合

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
