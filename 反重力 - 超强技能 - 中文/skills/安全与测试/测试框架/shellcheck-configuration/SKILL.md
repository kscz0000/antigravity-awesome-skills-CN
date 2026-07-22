---
name: shellcheck-configuration
description: "掌握 ShellCheck 静态分析工具的配置与使用，提升 Shell 脚本质量。适用于搭建代码检查基础设施、修复脚本问题或确保脚本可移植性。触发词：ShellCheck、Shell静态分析、脚本质量检查、shellcheck配置、shell脚本lint、代码检查工具、脚本可移植性"
risk: unknown
source: community
date_added: "2026-02-27"
---

# ShellCheck 配置与静态分析

配置和使用 ShellCheck 的完整指南，用于提升 Shell 脚本质量、捕获常见陷阱，并通过静态代码分析强制执行最佳实践。

## 不适用场景

- 任务与 ShellCheck 配置和静态分析无关
- 需要其他领域或超出此范围的工具

## 使用说明

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可操作的步骤和验证方法
- 如需详细示例，请打开 `resources/implementation-playbook.md`

## 适用场景

- 在 CI/CD 流水线中为 Shell 脚本搭建代码检查
- 分析现有 Shell 脚本中的问题
- 理解 ShellCheck 错误代码和警告
- 为特定项目需求配置 ShellCheck
- 将 ShellCheck 集成到开发工作流中
- 抑制误报并配置规则集
- 强制执行统一的代码质量标准
- 迁移脚本以满足质量门禁

## ShellCheck 基础

### 什么是 ShellCheck？

ShellCheck 是一个静态分析工具，用于分析 Shell 脚本并检测有问题的模式。支持：
- Bash、sh、dash、ksh 及其他 POSIX Shell
- 超过 100 种不同的警告和错误
- 针对目标 Shell 和标志的配置
- 与编辑器和 CI/CD 系统集成

### 安装

```bash
# macOS 使用 Homebrew
brew install shellcheck

# Ubuntu/Debian
apt-get install shellcheck

# 从源码安装
git clone https://github.com/koalaman/shellcheck.git
cd shellcheck
make build
make install

# 验证安装
shellcheck --version
```

## 配置文件

### .shellcheckrc（项目级别）

在项目根目录创建 `.shellcheckrc`：

```
# 指定目标 Shell
shell=bash

# 启用可选检查
enable=avoid-nullary-conditions
enable=require-variable-braces

# 禁用特定警告
disable=SC1091
disable=SC2086
```

### 环境变量

```bash
# 设置默认 Shell 目标
export SHELLCHECK_SHELL=bash

# 启用严格模式
export SHELLCHECK_STRICT=true

# 指定配置文件位置
export SHELLCHECK_CONFIG=~/.shellcheckrc
```

## 常见 ShellCheck 错误代码

### SC1000-1099：解析器错误
```bash
# SC1004: 反斜杠续行后未跟换行符
echo hello\
world  # 错误 - 需要行续接符

# SC1008: 运算符 `==' 的数据无效
if [[ $var =  "value" ]]; then  # == 前有多余空格
    true
fi
```

### SC2000-2099：Shell 问题

```bash
# SC2009: 建议使用 pgrep 或 pidof 代替 grep|grep
ps aux | grep -v grep | grep myprocess  # 应使用 pgrep

# SC2012: `ls` 仅用于查看，使用 `find` 获取可靠输出
for file in $(ls -la)  # 更好：使用 find 或通配符

# SC2015: 避免使用 && 和 || 代替 if-then-else
[[ -f "$file" ]] && echo "found" || echo "not found"  # 不够清晰

# SC2016: 单引号中的表达式不会展开
echo '$VAR' # 字面量 $VAR，非变量展开

# SC2026: 此词非标准。在其他 Shell 脚本中使用时需设置 POSIXLY_CORRECT
```

### SC2100-2199：引号问题

```bash
# SC2086: 使用双引号防止通配符和分词
for i in $list; do  # 应为：for i in $list 或 for i in "$list"
    echo "$i"
done

# SC2115: 路径中的波浪号未展开，使用 $HOME 代替
~/.bashrc  # 在字符串中应使用 "$HOME/.bashrc"

# SC2181: 直接用 `if` 检查退出码，而非间接检查
some_command
if [ $? -eq 0 ]; then  # 更好：if some_command; then

# SC2206: 引号包裹或设置 IFS 以防止分词
array=( $items )  # 应使用：array=( "$items" )
```

### SC3000-3999：POSIX 兼容性问题

```bash
# SC3010: 在 POSIX sh 中，使用 'case' 代替 'cond && foo'
[[ $var == "value" ]] && do_something  # 非 POSIX

# SC3043: 在 POSIX sh 中，'local' 未定义
function my_func() {
    local var=value  # 在某些 Shell 中非 POSIX
}
```

## 实用配置示例

### 最小配置（严格 POSIX）

```bash
#!/bin/bash
# 配置最大可移植性

shellcheck \
  --shell=sh \
  --external-sources \
  --check-sourced \
  script.sh
```

### 开发配置（Bash 宽松规则）

```bash
#!/bin/bash
# 配置 Bash 开发模式

shellcheck \
  --shell=bash \
  --exclude=SC1091,SC2119 \
  --enable=all \
  script.sh
```

### CI/CD 集成配置

```bash
#!/bin/bash
set -Eeuo pipefail

# 分析所有 Shell 脚本，发现问题即失败
find . -type f -name "*.sh" | while read -r script; do
    echo "Checking: $script"
    shellcheck \
        --shell=bash \
        --format=gcc \
        --exclude=SC1091 \
        "$script" || exit 1
done
```

### 项目 .shellcheckrc 配置

```
# 分析的 Shell 方言
shell=bash

# 启用可选检查
enable=avoid-nullary-conditions,require-variable-braces,check-unassigned-uppercase

# 禁用特定警告
# SC1091: 不跟踪被 source 的文件（大量误报）
disable=SC1091

# SC2119: 使用 function_name 代替 function_name --（参数）
disable=SC2119

# 用于上下文分析的外部文件
external-sources=true
```

## 集成模式

### Pre-commit Hook 配置

```bash
#!/bin/bash
# .git/hooks/pre-commit

#!/bin/bash
set -e

# 查找本次提交中所有修改的 Shell 脚本
git diff --cached --name-only | grep '\.sh$' | while read -r script; do
    echo "Linting: $script"

    if ! shellcheck "$script"; then
        echo "ShellCheck failed on $script"
        exit 1
    fi
done
```

### GitHub Actions 工作流

```yaml
name: ShellCheck

on: [push, pull_request]

jobs:
  shellcheck:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Run ShellCheck
        run: |
          sudo apt-get install shellcheck
          find . -type f -name "*.sh" -exec shellcheck {} \;
```

### GitLab CI 流水线

```yaml
shellcheck:
  stage: lint
  image: koalaman/shellcheck-alpine
  script:
    - find . -type f -name "*.sh" -exec shellcheck {} \;
  allow_failure: false
```

## 处理 ShellCheck 违规

### 抑制特定警告

```bash
#!/bin/bash

# 禁用整行警告
# shellcheck disable=SC2086
for file in $(ls -la); do
    echo "$file"
done

# 禁用整个脚本的警告
# shellcheck disable=SC1091,SC2119

# 禁用多个警告（格式各异）
command_that_fails() {
    # shellcheck disable=SC2015
    [ -f "$1" ] && echo "found" || echo "not found"
}

# 禁用 source 指令的特定检查
# shellcheck source=./helper.sh
source helper.sh
```

### 常见违规及修复

#### SC2086：使用双引号防止分词

```bash
# 问题
for i in $list; do done

# 解决方案
for i in $list; do done  # 如果 $list 已加引号，或
for i in "${list[@]}"; do done  # 如果 list 是数组
```

#### SC2181：直接检查退出码

```bash
# 问题
some_command
if [ $? -eq 0 ]; then
    echo "success"
fi

# 解决方案
if some_command; then
    echo "success"
fi
```

#### SC2015：使用 if-then 代替 && ||

```bash
# 问题
[ -f "$file" ] && echo "exists" || echo "not found"

# 解决方案 - 意图更清晰
if [ -f "$file" ]; then
    echo "exists"
else
    echo "not found"
fi
```

#### SC2016：单引号中的表达式不会展开

```bash
# 问题
echo 'Variable value: $VAR'

# 解决方案
echo "Variable value: $VAR"
```

#### SC2009：使用 pgrep 代替 grep

```bash
# 问题
ps aux | grep -v grep | grep myprocess

# 解决方案
pgrep -f myprocess
```

## 性能优化

### 检查多个文件

```bash
#!/bin/bash

# 顺序检查
for script in *.sh; do
    shellcheck "$script"
done

# 并行检查（更快）
find . -name "*.sh" -print0 | \
    xargs -0 -P 4 -n 1 shellcheck
```

### 缓存结果

```bash
#!/bin/bash

CACHE_DIR=".shellcheck_cache"
mkdir -p "$CACHE_DIR"

check_script() {
    local script="$1"
    local hash
    local cache_file

    hash=$(sha256sum "$script" | cut -d' ' -f1)
    cache_file="$CACHE_DIR/$hash"

    if [[ ! -f "$cache_file" ]]; then
        if shellcheck "$script" > "$cache_file" 2>&1; then
            touch "$cache_file.ok"
        else
            return 1
        fi
    fi

    [[ -f "$cache_file.ok" ]]
}

find . -name "*.sh" | while read -r script; do
    check_script "$script" || exit 1
done
```

## 输出格式

### 默认格式

```bash
shellcheck script.sh

# 输出：
# script.sh:1:3: warning: foo is referenced but not assigned. [SC2154]
```

### GCC 格式（适用于 CI/CD）

```bash
shellcheck --format=gcc script.sh

# 输出：
# script.sh:1:3: warning: foo is referenced but not assigned.
```

### JSON 格式（适用于解析）

```bash
shellcheck --format=json script.sh

# 输出：
# [{"file": "script.sh", "line": 1, "column": 3, "level": "warning", "code": 2154, "message": "..."}]
```

### 静默格式

```bash
shellcheck --format=quiet script.sh

# 发现问题时返回非零值，否则无输出
```

## 最佳实践

1. **在 CI/CD 中运行 ShellCheck** — 合并前捕获问题
2. **针对目标 Shell 配置** — 不要用分析 bash 的方式分析 sh
3. **记录排除项** — 说明抑制违规的原因
4. **处理违规** — 不要只是禁用警告
5. **启用严格模式** — 使用 `--enable=all` 配合谨慎的排除
6. **定期更新** — 保持 ShellCheck 为最新版本以获取新检查
7. **使用 pre-commit hook** — 推送前在本地捕获问题
8. **集成到编辑器** — 开发过程中获取实时反馈

## 资源

- **ShellCheck GitHub**: https://github.com/koalaman/shellcheck
- **ShellCheck Wiki**: https://www.shellcheck.net/wiki/
- **错误代码参考**: https://www.shellcheck.net/

## 限制
- 仅在任务明确匹配上述范围时使用此技能
- 不要将输出作为环境特定验证、测试或专家评审的替代品
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来寻求澄清