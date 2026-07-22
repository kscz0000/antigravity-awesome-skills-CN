---
name: tmux
description: "tmux 会话、窗口和面板管理专家，用于终端复用、持久化远程工作流和 Shell 脚本自动化。当用户需要管理 tmux 会话、创建多面板布局、SSH 持久化会话、终端复用、远程工作流自动化时使用。"
category: development
risk: safe
source: community
date_added: "2026-03-28"
author: kostakost2
tags: [tmux, terminal, multiplexer, sessions, shell, remote, automation]
tools: [claude, cursor, gemini]
---

# tmux — 终端复用器

## 概述

`tmux` 可以在 SSH 断开后保持终端会话存活，将工作分割到多个面板，并实现完全可脚本化的终端自动化。本技能涵盖会话管理、窗口/面板布局、快捷键绑定模式，以及从 Shell 脚本非交互式地使用 `tmux` —— 这对于远程服务器、长时间运行的任务和自动化工作流至关重要。

## 何时使用本技能

- 在远程服务器上设置或管理持久化终端会话时使用
- 用户需要运行能够在 SSH 断开后继续存活的长时进程时使用
- 脚本化多面板终端布局时使用（例如：日志 + Shell + 编辑器）
- 从 Bash 脚本自动化执行 `tmux` 命令而无需用户交互时使用

## 工作原理

`tmux` 有三个层级：**会话**（顶层，断开后仍存活）、**窗口**（会话内的标签页）和**面板**（窗口内的分割）。所有内容都可以通过外部的 `tmux <command>` 或内部的前缀键（默认为 `Ctrl-b`）进行控制。

### 会话管理

```bash
# 创建新的命名会话
tmux new-session -s work

# 创建分离的（后台）会话
tmux new-session -d -s work

# 创建分离会话并启动命令
tmux new-session -d -s build -x 220 -y 50 "make all"

# 附加到会话
tmux attach -t work
tmux attach          # 附加到最近的会话

# 列出所有会话
tmux list-sessions
tmux ls

# 从 tmux 内部分离
# Prefix + d   (Ctrl-b d)

# 终止会话
tmux kill-session -t work

# 终止除当前会话外的所有会话
tmux kill-session -a

# 从外部重命名会话
tmux rename-session -t old-name new-name

# 从外部切换到另一个会话
tmux switch-client -t other-session

# 检查会话是否存在（在脚本中有用）
tmux has-session -t work 2>/dev/null && echo "exists"
```

### 窗口管理

```bash
# 在当前会话中创建新窗口
tmux new-window -t work -n "logs"

# 创建运行特定命令的窗口
tmux new-window -t work:3 -n "server" "python -m http.server 8080"

# 列出窗口
tmux list-windows -t work

# 选择（切换到）窗口
tmux select-window -t work:logs
tmux select-window -t work:2       # 按索引

# 重命名窗口
tmux rename-window -t work:2 "editor"

# 终止窗口
tmux kill-window -t work:logs

# 将窗口移动到新索引
tmux move-window -s work:3 -t work:1

# 从 tmux 内部：
# Prefix + c     — 新建窗口
# Prefix + ,     — 重命名窗口
# Prefix + &     — 终止窗口
# Prefix + n/p   — 下一个/上一个窗口
# Prefix + 0-9   — 按编号切换到窗口
```

### 面板管理

```bash
# 垂直分割面板（左/右）
tmux split-window -h -t work:1

# 水平分割面板（上/下）
tmux split-window -v -t work:1

# 分割并运行命令
tmux split-window -h -t work:1 "tail -f /var/log/syslog"

# 按索引选择面板
tmux select-pane -t work:1.0

# 调整面板大小
tmux resize-pane -t work:1.0 -R 20   # 向右扩展 20 列
tmux resize-pane -t work:1.0 -D 10   # 向下收缩 10 行
tmux resize-pane -Z                   # 切换缩放（全屏）

# 交换面板
tmux swap-pane -s work:1.0 -t work:1.1

# 终止面板
tmux kill-pane -t work:1.1

# 从 tmux 内部：
# Prefix + %     — 垂直分割
# Prefix + "     — 水平分割
# Prefix + 方向键 — 导航面板
# Prefix + z     — 缩放/取消缩放当前面板
# Prefix + x     — 终止面板
# Prefix + {/}   — 与上一个/下一个面板交换
```

### 向面板发送命令（无需附加）

```bash
# 向特定面板发送命令并按回车
tmux send-keys -t work:1.0 "ls -la" Enter

# 在后台面板中运行命令而无需附加
tmux send-keys -t work:editor "vim src/main.py" Enter

# 发送 Ctrl+C 停止正在运行的进程
tmux send-keys -t work:1.0 C-c

# 发送文本但不按回车（用于预填充提示）
tmux send-keys -t work:1.0 "git commit -m '"

# 清空面板
tmux send-keys -t work:1.0 "clear" Enter

# 查看面板内容（捕获其输出）
tmux capture-pane -t work:1.0 -p
tmux capture-pane -t work:1.0 -p | grep "ERROR"
```

### 脚本化完整工作区布局

这是最强大的模式：从单个脚本创建完全配置的多面板工作区。

```bash
#!/usr/bin/env bash
set -euo pipefail

SESSION="dev"

# 如果会话已存在则退出
tmux has-session -t "$SESSION" 2>/dev/null && {
  echo "Session $SESSION already exists. Attaching..."
  tmux attach -t "$SESSION"
  exit 0
}

# 创建带有第一个窗口的会话
tmux new-session -d -s "$SESSION" -n "editor" -x 220 -y 50

# 窗口 1：编辑器 + 测试运行器并排
tmux send-keys -t "$SESSION:editor" "vim ." Enter
tmux split-window -h -t "$SESSION:editor"
tmux send-keys -t "$SESSION:editor.1" "npm test -- --watch" Enter
tmux select-pane -t "$SESSION:editor.0"

# 窗口 2：服务器日志
tmux new-window -t "$SESSION" -n "server"
tmux send-keys -t "$SESSION:server" "docker compose up" Enter
tmux split-window -v -t "$SESSION:server"
tmux send-keys -t "$SESSION:server.1" "tail -f logs/app.log" Enter

# 窗口 3：通用 Shell
tmux new-window -t "$SESSION" -n "shell"

# 聚焦第一个窗口
tmux select-window -t "$SESSION:editor"

# 附加
tmux attach -t "$SESSION"
```

### 配置（`~/.tmux.conf`）

```bash
# 将前缀键改为 Ctrl-a（screen 风格）
unbind C-b
set -g prefix C-a
bind C-a send-prefix

# 启用鼠标支持
set -g mouse on

# 窗口/面板编号从 1 开始
set -g base-index 1
setw -g pane-base-index 1

# 关闭窗口时重新编号
set -g renumber-windows on

# 增加滚动缓冲区
set -g history-limit 50000

# 在复制模式中使用 vi 键
setw -g mode-keys vi

# 更快的按键重复
set -s escape-time 0

# 无需重启即可重新加载配置
bind r source-file ~/.tmux.conf \; display "Config reloaded"

# 直观的分割键：| 和 -
bind | split-window -h -c "#{pane_current_path}"
bind - split-window -v -c "#{pane_current_path}"

# 新窗口在当前目录打开
bind c new-window -c "#{pane_current_path}"

# 状态栏
set -g status-right "#{session_name} | %H:%M %d-%b"
set -g status-interval 5
```

### 复制模式和滚动

```bash
# 进入复制模式（向上滚动查看输出）
# Prefix + [

# 在 vi 模式下：
# / 向前搜索，? 向后搜索
# Space 开始选择，Enter 复制
# q 退出复制模式

# 粘贴最近的缓冲区
# Prefix + ]

# 列出粘贴缓冲区
tmux list-buffers

# 显示最近的缓冲区
tmux show-buffer

# 将缓冲区保存到文件
tmux save-buffer /tmp/tmux-output.txt

# 将文件加载到缓冲区
tmux load-buffer /tmp/data.txt

# 将面板输出管道传输到命令
tmux pipe-pane -t work:1.0 "cat >> ~/session.log"
```

### 实用自动化模式

```bash
# 幂等会话：创建或附加
ensure_session() {
  local name="$1"
  tmux has-session -t "$name" 2>/dev/null \
    || tmux new-session -d -s "$name"
  tmux attach -t "$name"
}

# 在新的后台窗口中运行命令并跟踪其输出
run_bg() {
  local session="${1:-main}" cmd="${*:2}"
  tmux new-window -t "$session" -n "bg-$$"
  tmux send-keys -t "$session:bg-$$" "$cmd" Enter
}

# 等待面板产生特定输出（轮询）
wait_for_output() {
  local target="$1" pattern="$2" timeout="${3:-30}"
  local elapsed=0
  while (( elapsed < timeout )); do
    tmux capture-pane -t "$target" -p | grep -q "$pattern" && return 0
    sleep 1
    (( elapsed++ ))
  done
  return 1
}

# 终止所有匹配名称前缀的后台窗口
kill_bg_windows() {
  local session="$1" prefix="${2:-bg-}"
  tmux list-windows -t "$session" -F "#W" \
    | grep "^${prefix}" \
    | while read -r win; do
        tmux kill-window -t "${session}:${win}"
      done
}
```

### 远程和 SSH 工作流

```bash
# SSH 并立即附加到现有会话
ssh user@host -t "tmux attach -t work || tmux new-session -s work"

# 在远程主机的 tmux 会话内运行命令（即发即忘）
ssh user@host "tmux new-session -d -s deploy 'bash /opt/deploy.sh'"

# 从另一个终端监视远程会话输出
ssh user@host -t "tmux attach -t deploy -r"  # 只读附加

# 结对编程：共享会话（两个用户附加到同一会话）
# 用户 1：
tmux new-session -s shared
# 用户 2（同一服务器）：
tmux attach -t shared
```

## 最佳实践

- 在脚本中始终命名会话（`-s name`）—— 未命名的会话难以可靠定位
- 创建前使用 `tmux has-session -t name 2>/dev/null` 使脚本幂等
- 创建分离会话时设置 `-x` 和 `-y`，为检查终端尺寸的命令提供正确的面板大小
- 自动化时使用 `send-keys ... Enter` 而非管道 stdin —— 即使目标面板正在运行交互式程序也能工作
- 将 `~/.tmux.conf` 纳入版本控制，以便跨机器复现
- 对于不需要前缀的绑定，优先使用 `bind -n`，但仅用于不与应用快捷键冲突的按键

## 安全与安全注意事项

- `send-keys` 在面板中执行命令无需确认 —— 在脚本中使用前验证目标（`-t session:window.pane`）以避免向错误的面板发送按键
- 与他人共享会话时，只读附加（`-r`）可防止意外输入
- 避免在 tmux 窗口/面板标题或导出到共享机器上会话的环境变量中存储机密

## 常见陷阱

- **问题：** 脚本中的 `tmux` 命令失败，提示 "no server running"
  **解决方案：** 先用 `tmux start-server` 启动服务器，或在运行其他命令前创建一个分离会话。

- **问题：** 创建分离会话时面板大小为 0x0
  **解决方案：** 传递显式尺寸：`tmux new-session -d -s name -x 200 -y 50`。

- **问题：** `send-keys` 输入了文本但没有运行命令
  **解决方案：** 确保将 `Enter`（大写 E）作为第二个参数传递：`tmux send-keys -t target "cmd" Enter`。

- **问题：** 脚本每次运行都创建重复会话
  **解决方案：** 使用 `tmux has-session -t name 2>/dev/null || tmux new-session -d -s name` 进行保护。

- **问题：** 复制模式选择不如预期工作
  **解决方案：** 在 `~/.tmux.conf` 中确认设置了 `mode-keys vi` 或 `mode-keys emacs` 以匹配你的偏好。

## 相关技能

- `@bash-pro` — 编写编排 tmux 会话的 Shell 脚本
- `@bash-linux` — tmux 面板内使用的通用 Linux 终端模式
- `@ssh` — 结合 tmux 与 SSH 实现持久化远程工作流

## 限制
- 仅当任务明确符合上述描述的范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
