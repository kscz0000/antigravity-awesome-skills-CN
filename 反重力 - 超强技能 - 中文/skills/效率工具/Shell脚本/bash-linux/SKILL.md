---
name: bash-linux
description: "Bash/Linux 终端模式。关键命令、管道、错误处理、脚本编写。在 macOS 或 Linux 系统上工作时使用。触发词：Bash、Linux、终端命令、Shell 脚本、命令行、管道操作、进程管理、文本处理、环境变量、Bash 脚本、Shell 编程。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Bash Linux 模式

> Linux/macOS 上 Bash 的核心模式。

---

## 1. 操作符语法

### 命令链式组合

| 操作符 | 含义 | 示例 |
|----------|---------|---------|
| `;` | 顺序执行 | `cmd1; cmd2` |
| `&&` | 前一条成功才执行 | `npm install && npm run dev` |
| `\|\|` | 前一条失败才执行 | `npm test \|\| echo "Tests failed"` |
| `\|` | 管道输出 | `ls \| grep ".js"` |

---

## 2. 文件操作

### 常用命令

| 任务 | 命令 |
|------|---------|
| 列出所有文件 | `ls -la` |
| 查找文件 | `find . -name "*.js" -type f` |
| 查看文件内容 | `cat file.txt` |
| 前 N 行 | `head -n 20 file.txt` |
| 后 N 行 | `tail -n 20 file.txt` |
| 实时跟踪日志 | `tail -f log.txt` |
| 在文件中搜索 | `grep -r "pattern" --include="*.js"` |
| 文件大小 | `du -sh *` |
| 磁盘使用情况 | `df -h` |

---

## 3. 进程管理

| 任务 | 命令 |
|------|---------|
| 列出进程 | `ps aux` |
| 按名称查找 | `ps aux \| grep node` |
| 按 PID 终止 | `kill -9 <PID>` |
| 查找端口占用 | `lsof -i :3000` |
| 终止端口进程 | `kill -9 $(lsof -t -i :3000)` |
| 后台运行 | `npm run dev &` |
| 查看后台任务 | `jobs -l` |
| 调至前台 | `fg %1` |

---

## 4. 文本处理

### 核心工具

| 工具 | 用途 | 示例 |
|------|---------|---------|
| `grep` | 搜索 | `grep -rn "TODO" src/` |
| `sed` | 替换 | `sed -i 's/old/new/g' file.txt` |
| `awk` | 提取列 | `awk '{print $1}' file.txt` |
| `cut` | 切分字段 | `cut -d',' -f1 data.csv` |
| `sort` | 排序行 | `sort -u file.txt` |
| `uniq` | 去重行 | `sort file.txt \| uniq -c` |
| `wc` | 计数 | `wc -l file.txt` |

---

## 5. 环境变量

| 任务 | 命令 |
|------|---------|
| 查看所有 | `env` 或 `printenv` |
| 查看单个 | `echo $PATH` |
| 临时设置 | `export VAR="value"` |
| 脚本内设置 | `VAR="value" command` |
| 添加到 PATH | `export PATH="$PATH:/new/path"` |

---

## 6. 网络

| 任务 | 命令 |
|------|---------|
| 下载文件 | `curl -O https://example.com/file` |
| API 请求 | `curl -X GET https://api.example.com` |
| POST JSON | `curl -X POST -H "Content-Type: application/json" -d '{"key":"value"}' URL` |
| 检查端口 | `nc -zv localhost 3000` |
| 网络信息 | `ifconfig` 或 `ip addr` |

---

## 7. 脚本模板

```bash
#!/bin/bash
set -euo pipefail  # Exit on error, undefined var, pipe fail

# Colors (optional)
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Main
main() {
    log_info "Starting..."
    # Your logic here
    log_info "Done!"
}

main "$@"
```

---

## 8. 常用模式

### 检查命令是否存在

```bash
if command -v node &> /dev/null; then
    echo "Node is installed"
fi
```

### 变量默认值

```bash
NAME=${1:-"default_value"}
```

### 逐行读取文件

```bash
while IFS= read -r line; do
    echo "$line"
done < file.txt
```

### 遍历文件

```bash
for file in *.js; do
    echo "Processing $file"
done
```

---

## 9. 与 PowerShell 的差异

| 任务 | PowerShell | Bash |
|------|------------|------|
| 列出文件 | `Get-ChildItem` | `ls -la` |
| 查找文件 | `Get-ChildItem -Recurse` | `find . -type f` |
| 环境变量 | `$env:VAR` | `$VAR` |
| 字符串拼接 | `"$a$b"` | `"$a$b"` (相同) |
| 空值检查 | `if ($x)` | `if [ -n "$x" ]` |
| 管道 | 基于对象 | 基于文本 |

---

## 10. 错误处理

### set 选项

```bash
set -e          # Exit on error
set -u          # Exit on undefined variable
set -o pipefail # Exit on pipe failure
set -x          # Debug: print commands
```

### trap 清理

```bash
cleanup() {
    echo "Cleaning up..."
    rm -f /tmp/tempfile
}
trap cleanup EXIT
```

---

> **记住：** Bash 是基于文本的。使用 `&&` 进行成功链式调用，使用 `set -e` 保证安全，记得给变量加引号！

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 输出内容不应替代特定环境的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
