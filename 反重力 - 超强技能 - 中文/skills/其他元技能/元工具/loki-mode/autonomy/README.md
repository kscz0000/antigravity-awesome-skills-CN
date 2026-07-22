# Loki Mode - 自主运行器

单一脚本处理所有事务：先决条件、设置、Vibe Kanban 监控和带自动恢复的自主执行。

## 快速开始

```bash
# 带 PRD 运行
./autonomy/run.sh ./docs/requirements.md

# 交互式运行
./autonomy/run.sh
```

就这样！脚本会：
1. 检查所有先决条件（Claude CLI、Python、Git 等）
2. 验证技能安装
3. 初始化 `.loki/` 目录
4. **启动 Vibe Kanban 后台同步**（实时监控任务）
5. 启动带**实时输出**的 Claude Code（不再盲目等待）
6. 遇到速率限制或中断时自动恢复
7. 持续运行直到完成或达到最大重试次数

## 实时输出

Claude 的输出实时显示 - 您可以确切看到正在发生什么：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CLAUDE CODE OUTPUT (实时)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Claude 的输出在此实时显示...]
```

## 状态监视器（内置）

运行器每 5 秒更新 `.loki/STATUS.txt` 显示任务进度：

```
╔════════════════════════════════════════════════════════════════╗
║                    LOKI MODE 状态                              ║
╚════════════════════════════════════════════════════════════════╝

更新时间: Sat Dec 28 15:30:00 PST 2025

阶段: DEVELOPMENT

任务:
  ├─ 待处理:     10
  ├─ 进行中:     1
  ├─ 已完成:     5
  └─ 失败:       0

监视器: watch -n 2 cat .loki/STATUS.txt
```

### 在另一个终端中监视

```bash
# 实时查看状态更新
watch -n 2 cat .loki/STATUS.txt

# 或查看一次
cat .loki/STATUS.txt
```

## 检查内容

| 先决条件 | 必需 | 说明 |
|----------|------|------|
| Claude Code CLI | 是 | 从 https://claude.ai/code 安装 |
| Python 3 | 是 | 用于状态管理 |
| Git | 是 | 用于版本控制 |
| curl | 是 | 用于网络请求 |
| Node.js | 否 | 某些构建需要 |
| jq | 否 | 有助于 JSON 解析 |

## 配置

环境变量：

```bash
# 重试设置
export LOKI_MAX_RETRIES=50      # 最大重试次数（默认：50）
export LOKI_BASE_WAIT=60        # 基础等待时间（秒）（默认：60）
export LOKI_MAX_WAIT=3600       # 最大等待时间（秒）（默认：3600）

# 跳过先决条件检查（用于 CI/CD 或重复运行）
export LOKI_SKIP_PREREQS=true

# 使用自定义设置运行
LOKI_MAX_RETRIES=100 LOKI_BASE_WAIT=120 ./autonomy/run.sh ./docs/prd.md
```

## 自动恢复如何工作

```
┌─────────────────────────────────────────────────────────────┐
│  ./autonomy/run.sh prd.md                                   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  检查先决条件          │
              └───────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │  初始化 .loki/        │
              └───────────────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │  带 prompt 运行 Claude Code   │◄────────────────┐
         └────────────────────────────────┘                 │
                          │                                 │
                          ▼                                 │
              ┌───────────────────────┐                     │
              │  Claude 退出          │                     │
              └───────────────────────┘                     │
                          │                                 │
              ┌───────────┴───────────┐                     │
              ▼                       ▼                     │
      ┌───────────────┐       ┌───────────────┐             │
      │  已完成？     │──是───│   成功！      │             │
      └───────────────┘       └───────────────┘             │
              │ 否                                          │
              ▼                                             │
      ┌───────────────┐                                     │
      │ 等待（退避）  │─────────────────────────────────────┘
      └───────────────┘
```

## 状态文件

自主运行器创建：

```
.loki/
├── autonomy-state.json    # 运行器状态（重试次数、状态）
├── logs/
│   └── autonomy-*.log     # 执行日志
├── state/
│   └── orchestrator.json  # Loki Mode 阶段跟踪
└── COMPLETED              # 完成时创建
```

## 中断后恢复

如果停止脚本（Ctrl+C）或崩溃，只需再次运行：

```bash
# 状态已保存，将从上次检查点恢复
./autonomy/run.sh ./docs/requirements.md
```

脚本检测之前的状态并从上次中断处继续。

## 与手动模式的区别

| 功能 | 手动模式 | 自主模式 |
|------|----------|----------|
| 启动 | `claude --dangerously-skip-permissions` | `./autonomy/run.sh` |
| 先决条件检查 | 手动 | 自动 |
| 速率限制处理 | 手动重启 | 自动恢复 |
| 状态持久化 | 手动检查点 | 自动 |
| 日志记录 | 仅控制台 | 控制台 + 文件 |
| 最大运行时间 | 基于会话 | 可配置重试次数 |

## 故障排除

### "Claude Code CLI not found"
```bash
npm install -g @anthropic-ai/claude-code
# 或访问 https://claude.ai/code
```

### "SKILL.md not found"
确保从 loki-mode 目录运行或已安装技能：
```bash
# 选项 1：从项目目录运行
cd /path/to/loki-mode
./autonomy/run.sh

# 选项 2：全局安装技能
cp -r . ~/.claude/skills/loki-mode/
```

### "Max retries exceeded"
任务耗时过长或反复失败。检查：
```bash
# 查看日志
cat .loki/logs/autonomy-*.log | tail -100

# 检查编排器状态
cat .loki/state/orchestrator.json

# 增加重试次数
LOKI_MAX_RETRIES=200 ./autonomy/run.sh ./docs/prd.md
```
