---
name: planning-with-files
description: "像 Manus 一样工作：用持久化的 Markdown 文件作为「磁盘上的工作记忆」。当用户需要规划复杂任务、管理项目进度、使用文件系统作为外部记忆时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 文件化规划

像 Manus 一样工作：用持久化的 Markdown 文件作为「磁盘上的工作记忆」。

## 重要：文件存放位置

使用本技能时：

- **模板**存放在技能目录 `${CLAUDE_PLUGIN_ROOT}/templates/`
- **你的规划文件**（`task_plan.md`、`findings.md`、`progress.md`）应创建在**你的项目目录**——即你当前工作的文件夹

| 位置 | 存放内容 |
|------|----------|
| 技能目录 (`${CLAUDE_PLUGIN_ROOT}/`) | 模板、脚本、参考文档 |
| 你的项目目录 | `task_plan.md`、`findings.md`、`progress.md` |

这样可以确保规划文件与代码放在一起，而不是埋在技能安装目录里。

## 快速开始

执行任何复杂任务之前：

1. **创建 `task_plan.md`** — 参考 [templates/task_plan.md](templates/task_plan.md)
2. **创建 `findings.md`** — 参考 [templates/findings.md](templates/findings.md)
3. **创建 `progress.md`** — 参考 [templates/progress.md](templates/progress.md)
4. **决策前重读计划** — 将目标刷新到注意力窗口中
5. **每个阶段完成后更新** — 标记完成状态，记录错误

> **注意：** 三个规划文件都应创建在当前工作目录（项目根目录），而非技能安装目录。

## 核心模式

```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)

→ Anything important gets written to disk.
```

## 文件用途

| 文件 | 用途 | 更新时机 |
|------|------|----------|
| `task_plan.md` | 阶段、进度、决策 | 每个阶段完成后 |
| `findings.md` | 研究、发现 | 任何发现之后 |
| `progress.md` | 会话日志、测试结果 | 整个会话期间 |

## 关键规则

### 1. 先建计划
没有 `task_plan.md` 就不要开始复杂任务。没有商量余地。

### 2. 两步操作规则
> "每执行 2 次查看/浏览/搜索操作后，立即将关键发现保存到文本文件。"

这可以防止视觉/多模态信息丢失。

### 3. 先读后决
做重大决策前，先读取计划文件。这能将目标保持在注意力窗口中。

### 4. 做完就更新
完成任何阶段后：
- 标记阶段状态：`in_progress` → `complete`
- 记录遇到的错误
- 记录创建/修改的文件

### 5. 记录所有错误
每个错误都要写进计划文件。这能积累经验，防止重复犯错。

```markdown
## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| FileNotFoundError | 1 | Created default config |
| API timeout | 2 | Added retry logic |
```

### 6. 永远不要重复失败
```
if action_failed:
    next_action != same_action
```
记录尝试过的方法。改变策略。

## 三次失败协议

```
ATTEMPT 1: Diagnose & Fix
  → Read error carefully
  → Identify root cause
  → Apply targeted fix

ATTEMPT 2: Alternative Approach
  → Same error? Try different method
  → Different tool? Different library?
  → NEVER repeat exact same failing action

ATTEMPT 3: Broader Rethink
  → Question assumptions
  → Search for solutions
  → Consider updating the plan

AFTER 3 FAILURES: Escalate to User
  → Explain what you tried
  → Share the specific error
  → Ask for guidance
```

## 读写决策矩阵

| 场景 | 操作 | 原因 |
|------|------|------|
| 刚写完文件 | 不要读 | 内容还在上下文中 |
| 查看了图片/PDF | 立即写入发现 | 多模态内容会丢失 |
| 浏览器返回数据 | 写入文件 | 截图不会持久化 |
| 开始新阶段 | 读取计划/发现 | 上下文过时需要重新定位 |
| 出现错误 | 读取相关文件 | 需要当前状态才能修复 |
| 中断后恢复 | 读取所有规划文件 | 恢复状态 |

## 五问重启测试

如果你能回答以下问题，说明上下文管理是可靠的：

| 问题 | 答案来源 |
|------|----------|
| 我在哪？ | task_plan.md 中的当前阶段 |
| 我要去哪？ | 剩余阶段 |
| 目标是什么？ | 计划中的目标声明 |
| 我学到了什么？ | findings.md |
| 我做了什么？ | progress.md |

## 何时使用此模式

**适用场景：**
- 多步骤任务（3步以上）
- 研究任务
- 构建/创建项目
- 跨越多轮工具调用的任务
- 任何需要组织管理的工作

**跳过场景：**
- 简单问题
- 单文件编辑
- 快速查询

## 模板

复制以下模板开始使用：

- [templates/task_plan.md](templates/task_plan.md) — 阶段追踪
- [templates/findings.md](templates/findings.md) — 研究存储
- [templates/progress.md](templates/progress.md) — 会话日志

## 脚本

自动化辅助脚本：

- `scripts/init-session.sh` — 初始化所有规划文件
- `scripts/check-complete.sh` — 验证所有阶段完成

## 进阶主题

- **Manus 原则：** 见 [reference.md](reference.md)
- **实际案例：** 见 [examples.md](examples.md)

## 反模式

| 不要 | 应该 |
|------|------|
| 用 TodoWrite 做持久化 | 创建 task_plan.md 文件 |
| 说一次目标就忘了 | 决策前重读计划 |
| 隐藏错误默默重试 | 将错误记录到计划文件 |
| 把所有内容塞进上下文 | 大内容存文件 |
| 立即开始执行 | 先创建计划文件 |
| 重复失败操作 | 记录尝试，改变策略 |
| 在技能目录创建文件 | 在项目目录创建文件 |

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为特定环境验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
