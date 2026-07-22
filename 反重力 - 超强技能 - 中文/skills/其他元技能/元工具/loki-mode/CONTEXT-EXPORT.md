# Loki Mode - 对话上下文导出

**日期：** 2025-12-28
**版本：** 2.5.0
**仓库：** https://github.com/asklokesh/loki-mode

---

## 项目概述

**Loki Mode** 是一个 Claude Code 技能，提供多智能体自主启动系统。它动态编排 6 个集群中的专业化智能体，将 PRD 从构想转化为完全部署的产品。它仅按需生成智能体——简单项目只需几个，复杂创业项目可扩展到 100+。

### 核心特性
- 37 种专业化智能体类型，覆盖 6 个集群（工程、运营、商业、数据、产品、增长）
- 基于项目复杂度的动态智能体扩展
- Task 工具用于子智能体调度，具备全新上下文
- 分布式任务队列（待处理、进行中、已完成、失败、死信）
- 断路器用于单智能体故障处理
- 超时/卡住智能体检测，配合心跳监控
- 通过 `.loki/state/` 中的检查点进行状态恢复
- 自主执行，遇速率限制时自动恢复

---

## 文件结构

```
loki-mode/
├── SKILL.md                    # 主技能文件（需要 YAML frontmatter）
├── VERSION                     # 当前版本：2.4.0
├── CHANGELOG.md                # 完整版本历史
├── README.md                   # 主文档
├── references/
│   ├── agents.md               # 37 种智能体类型定义
│   ├── deployment.md           # 云部署指南
│   └── business-ops.md         # 业务运营工作流
├── examples/
│   ├── simple-todo-app.md      # 简单 PRD 用于测试
│   ├── api-only.md             # 仅后端 PRD
│   ├── static-landing-page.md  # 前端/营销 PRD
│   └── full-stack-demo.md      # 完整书签管理器 PRD
├── tests/
│   ├── run-all-tests.sh        # 主测试运行器（53 个测试）
│   ├── test-bootstrap.sh       # 8 个测试
│   ├── test-task-queue.sh      # 8 个测试
│   ├── test-circuit-breaker.sh # 8 个测试
│   ├── test-agent-timeout.sh   # 9 个测试
│   ├── test-state-recovery.sh  # 8 个测试
│   └── test-wrapper.sh         # 12 个测试
├── scripts/
│   ├── loki-wrapper.sh         # 旧版包装器（已弃用）
│   └── export-to-vibe-kanban.sh # 可选 Vibe Kanban 导出
├── integrations/
│   └── vibe-kanban.md          # Vibe Kanban 集成指南
├── autonomy/
│   ├── run.sh                  # ⭐ 主入口点 - 处理一切
│   └── README.md               # 自主运行文档
└── .github/workflows/
    └── release.yml             # GitHub Actions 发布工作流
```

---

## 使用方法

### 快速开始（推荐）
```bash
./autonomy/run.sh ./docs/requirements.md
```

### run.sh 做了什么
1. 检查先决条件（Claude CLI、Python、Git、curl）
2. 验证技能安装
3. 初始化 `.loki/` 目录
4. 启动状态监控器（每 5 秒更新 `.loki/STATUS.txt`）
5. 使用实时输出运行 Claude Code
6. 遇速率限制时指数退避自动恢复
7. 持续运行直到完成或达到最大重试次数

### 监控进度
```bash
# 在另一个终端
watch -n 2 cat .loki/STATUS.txt
```

---

## 关键技术细节

### Claude Code 调用
自主运行器通过 stdin 管道传递提示词以实现实时输出：
```bash
echo "$prompt" | claude --dangerously-skip-permissions
```

**重要：** 使用 `-p` 标志无法正确流式输出。通过 stdin 管道可显示交互式输出。

### 状态文件
- `.loki/state/orchestrator.json` - 当前阶段、指标
- `.loki/autonomy-state.json` - 重试计数、状态、PID
- `.loki/queue/*.json` - 任务队列
- `.loki/STATUS.txt` - 人类可读状态（每 5 秒更新）
- `.loki/logs/*.log` - 执行日志

### 环境变量
| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `LOKI_MAX_RETRIES` | 50 | 最大重试次数 |
| `LOKI_BASE_WAIT` | 60 | 基础等待时间（秒） |
| `LOKI_MAX_WAIT` | 3600 | 最大等待时间（1 小时） |
| `LOKI_SKIP_PREREQS` | false | 跳过先决条件检查 |

---

## 版本历史摘要

| 版本 | 关键变更 |
|---------|-------------|
| 2.5.0 | 真正的流式输出（stream-json），带 Anthropic 设计风格的 Web 仪表盘 |
| 2.4.0 | 实时输出修复（stdin 管道），STATUS.txt 监控器 |
| 2.3.0 | 统一自主运行器（`autonomy/run.sh`） |
| 2.2.0 | Vibe Kanban 集成 |
| 2.1.0 | 自主包装器，支持自动恢复 |
| 2.0.x | 测试套件、macOS 兼容性、发布工作流 |
| 1.x.x | 初始技能，包含智能体、部署指南 |

---

## 已知问题与解决方案

### 1. "自主运行时输出为空"
**原因：** 使用 `-p` 标志无法流式输出
**解决方案：** 使用 stdin 管道：`echo "$prompt" | claude --dangerously-skip-permissions`

### 2. "Vibe Kanban 不显示任务"
**原因：** Vibe Kanban 是 UI 驱动的，不会自动读取 JSON 文件
**解决方案：** 使用 `.loki/STATUS.txt` 进行监控，或单独运行 Vibe Kanban

### 3. "macOS 上找不到 timeout 命令"
**原因：** macOS 没有 GNU coreutils
**解决方案：** 测试脚本中使用基于 Perl 的回退方案

### 4. "TTY raw mode 错误"
**原因：** 在非交互模式下运行 Claude
**解决方案：** 最新提交（008ed86）添加了 `--no-input` 标志

---

## Git 配置

**提交者：** asklokesh（永远不要使用 Claude 作为共同作者）

**提交格式：**
```
Short description (vX.X.X)

Detailed bullet points of changes
```

---

## 测试套件

运行所有测试：
```bash
./tests/run-all-tests.sh
```

6 个测试套件共 53 个测试 - 全部应通过。

---

## 待办/未来工作

1. **Vibe Kanban 正式集成** - Vibe Kanban 不读取文件，需要 API 集成
2. **更好的实时输出** - 当前 stdin 管道可用但可能存在边缘情况
3. **任务可视化** - 可以添加简单的 TUI 用于任务监控

---

## 首先需要阅读的重要文件

开始新会话时，阅读以下文件：
1. `SKILL.md` - 实际的技能指令
2. `autonomy/run.sh` - 主入口点
3. `VERSION` 和 `CHANGELOG.md` - 当前状态
4. 本文件（`CONTEXT-EXPORT.md`） - 完整上下文

---

## 用户偏好

- 始终使用 `asklokesh` 作为提交者
- 永远不要使用 Claude 作为共同作者
- 保持技能文件整洁，自主运行代码分离
- 推送前先测试
- 实时输出很重要 - 用户希望看到正在发生什么

---

## 最后已知状态

- **版本：** 2.5.0
- **最新提交：**（待推送）
- **测试：** 全部 53 个通过
- **新增功能：** 通过 stream-json 实现真正的流式输出，带 Anthropic 设计风格的 Web 仪表盘