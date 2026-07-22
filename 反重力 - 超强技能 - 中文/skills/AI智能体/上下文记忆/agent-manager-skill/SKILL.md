---
name: agent-manager-skill
description: "通过 tmux 会话管理多个本地 CLI 智能体（启动/停止/监控/分配任务），支持 cron 定时调度。触发词：智能体管理、agent manager、tmux 智能体、多智能体调度、CLI 智能体管理、智能体监控、agent 调度"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 智能体管理技能

## 何时使用

在以下场景使用此技能：

- 并行运行多个本地 CLI 智能体（独立的 tmux 会话）
- 启动/停止智能体并追踪其日志
- 向智能体分配任务并监控输出
- 调度周期性智能体工作（cron）

## 前置条件

在工作空间安装 `agent-manager-skill`：

```bash
git clone https://github.com/fractalmind-ai/agent-manager-skill.git
```

## 常用命令

```bash
python3 agent-manager/scripts/main.py doctor
python3 agent-manager/scripts/main.py list
python3 agent-manager/scripts/main.py start EMP_0001
python3 agent-manager/scripts/main.py monitor EMP_0001 --follow
python3 agent-manager/scripts/main.py assign EMP_0002 <<'EOF'
Follow teams/fractalmind-ai-maintenance.md Workflow
EOF
```

## 注意事项

- 需要 `tmux` 和 `python3`。
- 智能体配置在 `agents/` 目录下（参见仓库示例）。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出内容不能替代特定环境的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
