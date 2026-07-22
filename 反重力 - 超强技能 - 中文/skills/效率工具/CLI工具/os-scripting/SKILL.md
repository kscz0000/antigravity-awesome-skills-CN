---
name: os-scripting
description: "面向 Linux、macOS 和 Windows 的操作系统与 Shell 脚本故障排查工作流。涵盖 bash 脚本、系统管理、调试和自动化。当用户要求编写 Shell 脚本、排查系统问题或自动化管理任务时使用。"
category: workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# 操作系统/Shell 脚本故障排查工作流包

## 概述

跨 Linux、macOS 和 Windows 的操作系统故障排查、Shell 脚本和系统管理综合工作流。此工作流包协调多项技能，用于调试系统问题、创建健壮的脚本和自动化管理任务。

## 适用场景

- 调试 Shell 脚本错误
- 创建生产就绪的 bash 脚本
- 排查系统问题
- 自动化系统管理任务
- 管理进程和服务
- 配置系统资源

## 工作流阶段

### 阶段 1：环境评估

#### 调用技能
- `bash-linux` — Linux bash 模式
- `bash-pro` — 专业 bash 脚本
- `bash-defensive-patterns` — 防御性脚本

#### 操作步骤
1. 识别操作系统和版本
2. 检查可用工具和命令
3. 验证权限和访问
4. 评估系统资源
5. 查看日志和错误信息

#### 诊断命令
```bash
# System information
uname -a
cat /etc/os-release
hostnamectl

# Resource usage
top
htop
df -h
free -m

# Process information
ps aux
pgrep -f pattern
lsof -i :port

# Network status
netstat -tulpn
ss -tulpn
ip addr show
```

#### 即用提示词
```
Use @bash-linux to diagnose system performance issues
```

### 阶段 2：脚本分析

#### 调用技能
- `bash-defensive-patterns` — 防御性脚本
- `shellcheck-configuration` — ShellCheck 代码检查
- `bats-testing-patterns` — Bats 测试

#### 操作步骤
1. 运行 ShellCheck 进行代码检查
2. 分析脚本结构
3. 识别潜在问题
4. 检查错误处理
5. 验证变量使用

#### ShellCheck 用法
```bash
# Install ShellCheck
sudo apt install shellcheck  # Debian/Ubuntu
brew install shellcheck      # macOS

# Run ShellCheck
shellcheck script.sh
shellcheck -f gcc script.sh

# Fix common issues
# - Use quotes around variables
# - Check exit codes
# - Handle errors properly
```

#### 即用提示词
```
Use @shellcheck-configuration to lint and fix shell scripts
```

### 阶段 3：调试

#### 调用技能
- `systematic-debugging` — 系统化调试
- `debugger` — 调试专家
- `error-detective` — 错误模式检测

#### 操作步骤
1. 启用调试模式
2. 添加日志语句
3. 追踪执行流
4. 隔离故障部分
5. 逐个测试组件

#### 调试技巧
```bash
# Enable debug mode
set -x  # Print commands
set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Pipeline failure detection

# Add logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> /var/log/script.log
}

# Trap errors
trap 'echo "Error on line $LINENO"' ERR

# Test sections
bash -n script.sh  # Syntax check
bash -x script.sh  # Trace execution
```

#### 即用提示词
```
Use @systematic-debugging to trace and fix shell script errors
```

### 阶段 4：脚本开发

#### 调用技能
- `bash-pro` — 专业脚本
- `bash-defensive-patterns` — 防御性模式
- `linux-shell-scripting` — Shell 脚本

#### 操作步骤
1. 设计脚本结构
2. 实现函数
3. 添加错误处理
4. 包含输入验证
5. 添加帮助文档

#### 脚本模板
```bash
#!/usr/bin/env bash
set -euo pipefail

# Constants
readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

# Logging
log() {
    local level="$1"
    shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" >&2
}

info() { log "INFO" "$@"; }
warn() { log "WARN" "$@"; }
error() { log "ERROR" "$@"; exit 1; }

# Usage
usage() {
    cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS]

Options:
    -h, --help      Show this help message
    -v, --verbose   Enable verbose output
    -d, --debug     Enable debug mode

Examples:
    $SCRIPT_NAME --verbose
    $SCRIPT_NAME -d
EOF
}

# Main function
main() {
    local verbose=false
    local debug=false

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage
                exit 0
                ;;
            -v|--verbose)
                verbose=true
                shift
                ;;
            -d|--debug)
                debug=true
                set -x
                shift
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    info "Script started"
    # Your code here
    info "Script completed"
}

main "$@"
```

#### 即用提示词
```
Use @bash-pro to create a production-ready backup script
```

```
Use @linux-shell-scripting to automate system maintenance tasks
```

### 阶段 5：测试

#### 调用技能
- `bats-testing-patterns` — Bats 测试框架
- `test-automator` — 测试自动化

#### 操作步骤
1. 编写 Bats 测试
2. 测试边界情况
3. 测试错误条件
4. 验证预期输出
5. 运行测试套件

#### Bats 测试示例
```bash
#!/usr/bin/env bats

@test "script returns success" {
    run ./script.sh
    [ "$status" -eq 0 ]
}

@test "script handles missing arguments" {
    run ./script.sh
    [ "$status" -ne 0 ]
    [ "$output" == *"Usage:"* ]
}

@test "script creates expected output" {
    run ./script.sh --output test.txt
    [ -f "test.txt" ]
}
```

#### 即用提示词
```
Use @bats-testing-patterns to write tests for shell scripts
```

### 阶段 6：系统故障排查

#### 调用技能
- `devops-troubleshooter` — DevOps 故障排查
- `incident-responder` — 事件响应
- `server-management` — 服务器管理

#### 操作步骤
1. 识别症状
2. 检查系统日志
3. 分析资源使用
4. 测试连通性
5. 验证配置
6. 实施修复

#### 故障排查命令
```bash
# Check logs
journalctl -xe
tail -f /var/log/syslog
dmesg | tail

# Network troubleshooting
ping host
traceroute host
curl -v http://host
dig domain
nslookup domain

# Process troubleshooting
strace -p PID
lsof -p PID
iotop

# Disk troubleshooting
du -sh /*
find / -type f -size +100M
lsof | grep deleted
```

#### 即用提示词
```
Use @devops-troubleshooter to diagnose server connectivity issues
```

```
Use @incident-responder to investigate system outage
```

### 阶段 7：自动化

#### 调用技能
- `workflow-automation` — 工作流自动化
- `cicd-automation-workflow-automate` — CI/CD 自动化
- `linux-shell-scripting` — Shell 脚本

#### 操作步骤
1. 识别自动化机会
2. 设计自动化工作流
3. 实现脚本
4. 使用 cron/systemd 调度
5. 监控自动化健康状态

#### Cron 示例
```bash
# Edit crontab
crontab -e

# Backup every day at 2 AM
0 2 * * * /path/to/backup.sh

# Clean logs weekly
0 3 * * 0 /path/to/cleanup.sh

# Monitor disk space hourly
0 * * * * /path/to/monitor.sh
```

#### Systemd Timer 示例
```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily backup timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

#### 即用提示词
```
Use @workflow-automation to create automated system maintenance workflow
```

## 常见故障排查场景

### CPU 使用率高
```bash
top -bn1 | head -20
ps aux --sort=-%cpu | head -10
pidstat 1 5
```

### 内存问题
```bash
free -h
vmstat 1 10
cat /proc/meminfo
```

### 磁盘空间
```bash
df -h
du -sh /* 2>/dev/null | sort -h
find / -type f -size +500M 2>/dev/null
```

### 网络问题
```bash
ip addr show
ip route show
ss -tulpn
curl -v http://target
```

### 服务故障
```bash
systemctl status service-name
journalctl -u service-name -f
systemctl restart service-name
```

## 质量关卡

完成工作流前，请验证：
- [ ] 所有脚本通过 ShellCheck
- [ ] 测试通过 Bats
- [ ] 错误处理已实现
- [ ] 日志已配置
- [ ] 文档已完成
- [ ] 自动化已调度

## 相关工作流包

- `development` — 软件开发
- `cloud-devops` — 云和 DevOps
- `security-audit` — 安全测试
- `database` — 数据库运维

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 输出结果不能替代针对特定环境的验证、测试或专家评审。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
