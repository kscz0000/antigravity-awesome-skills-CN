# Vibe Kanban 集成

Loki Mode 可选集成 [Vibe Kanban](https://github.com/BloopAI/vibe-kanban)，为自主执行监控提供可视化仪表板。

## 为什么在 Loki Mode 中使用 Vibe Kanban？

| 功能 | 仅 Loki Mode | + Vibe Kanban |
|------|-------------|---------------|
| 任务可视化 | 基于文件的队列 | 可视化看板 |
| 进度监控 | 日志文件 | 实时仪表板 |
| 人工干预 | 编辑队列文件 | 拖放任务 |
| 代码审查 | 自动化 3 审查者 | + 可视化差异审查 |
| 并行智能体 | 后台子智能体 | 隔离的 git worktrees |

## 设置

### 1. 安装 Vibe Kanban

```bash
npx vibe-kanban
```

### 2. 在 Loki Mode 中启用集成

运行前设置环境变量：

```bash
export LOKI_VIBE_KANBAN=true
./scripts/loki-wrapper.sh ./docs/requirements.md
```

或创建 `.loki/config/integrations.yaml`：

```yaml
vibe-kanban:
  enabled: true
  sync_interval: 30  # 秒
  export_path: ~/.vibe-kanban/loki-tasks/
```

## 工作原理

### 任务同步流程

```
Loki Mode                          Vibe Kanban
    │                                   │
    ├─ 创建任务 ──────────────────────► 任务出现在看板上
    │                                   │
    ├─ 智能体领取任务 ─────────────────► 状态："进行中"
    │                                   │
    │ ◄─────────────────── 用户暂停 ───┤ (可选干预)
    │                                   │
    ├─ 任务完成 ──────────────────────► 状态："完成"
    │                                   │
    └─ 审查结果 ◄───────────────────── 用户审查差异
```

### 任务导出格式

Loki Mode 以 Vibe Kanban 兼容格式导出任务：

```json
{
  "id": "loki-task-eng-frontend-001",
  "title": "实现用户认证界面",
  "description": "创建带验证的登录/注册表单",
  "status": "todo",
  "agent": "claude-code",
  "tags": ["eng-frontend", "phase-4", "priority-high"],
  "metadata": {
    "lokiPhase": "DEVELOPMENT",
    "lokiSwarm": "engineering",
    "lokiAgent": "eng-frontend",
    "createdAt": "2025-01-15T10:00:00Z"
  }
}
```

### Loki 阶段到看板列的映射

| Loki 阶段 | 看板列 |
|-----------|--------|
| BOOTSTRAP | 待办 |
| DISCOVERY | 规划中 |
| ARCHITECTURE | 规划中 |
| INFRASTRUCTURE | 进行中 |
| DEVELOPMENT | 进行中 |
| QA | 审查中 |
| DEPLOYMENT | 部署中 |
| BUSINESS_OPS | 完成 |
| GROWTH | 完成 |

## 导出脚本

将此脚本添加到导出 Loki Mode 任务到 Vibe Kanban：

```bash
#!/bin/bash
# scripts/export-to-vibe-kanban.sh

LOKI_DIR=".loki"
EXPORT_DIR="${VIBE_KANBAN_DIR:-~/.vibe-kanban/loki-tasks}"

mkdir -p "$EXPORT_DIR"

# 导出待处理任务
if [ -f "$LOKI_DIR/queue/pending.json" ]; then
    python3 << EOF
import json
import os

with open("$LOKI_DIR/queue/pending.json") as f:
    tasks = json.load(f)

export_dir = os.path.expanduser("$EXPORT_DIR")

for task in tasks:
    vibe_task = {
        "id": f"loki-{task['id']}",
        "title": task.get('payload', {}).get('description', task['type']),
        "description": json.dumps(task.get('payload', {}), indent=2),
        "status": "todo",
        "agent": "claude-code",
        "tags": [task['type'], f"priority-{task.get('priority', 5)}"],
        "metadata": {
            "lokiTaskId": task['id'],
            "lokiType": task['type'],
            "createdAt": task.get('createdAt', '')
        }
    }

    with open(f"{export_dir}/{task['id']}.json", 'w') as out:
        json.dump(vibe_task, out, indent=2)

print(f"已导出 {len(tasks)} 个任务到 {export_dir}")
EOF
fi
```

## 实时同步（高级）

要实现实时同步，在 Loki Mode 旁边运行监视器：

```bash
#!/bin/bash
# scripts/vibe-sync-watcher.sh

LOKI_DIR=".loki"

# 监视队列变更并同步
while true; do
    # macOS 用 fswatch，Linux 用 inotifywait
    if command -v fswatch &> /dev/null; then
        fswatch -1 "$LOKI_DIR/queue/"
    else
        inotifywait -e modify,create "$LOKI_DIR/queue/" 2>/dev/null
    fi

    ./scripts/export-to-vibe-kanban.sh
    sleep 2
done
```

## 组合使用的好处

### 1. 可视化进度跟踪
在看板上看到所有活跃的 Loki 智能体作为任务移动。

### 2. 安全隔离
Vibe Kanban 在隔离的 git worktrees 中运行每个智能体，完美适配 Loki 的并行开发。

### 3. 人机回路选项
暂停自主执行，可视化审查变更，然后恢复。

### 4. 多项目仪表板
如果在多个项目上运行 Loki Mode，在一个 Vibe Kanban 实例中查看所有项目。

## 比较：何时使用什么

| 场景 | 推荐 |
|------|------|
| 完全自主，无监控 | 仅 Loki Mode + Wrapper |
| 需要可视化进度仪表板 | 添加 Vibe Kanban |
| 想要手动任务优先级排序 | 使用 Vibe Kanban 重新排序 |
| 合并前代码审查 | 使用 Vibe Kanban 的差异查看器 |
| 多个并发 PRD | Vibe Kanban 用于项目切换 |

## 未来集成想法

- [ ] 双向同步（Vibe → Loki）
- [ ] Vibe Kanban MCP 服务器用于智能体通信
- [ ] 工具间共享智能体配置
- [ ] 统一日志仪表板
