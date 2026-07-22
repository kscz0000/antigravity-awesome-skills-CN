---
name: claude-monitor
description: Claude Code 和本地系统性能监控器。诊断卡顿，测量 CPU/RAM/磁盘，检查 API 延迟并生成系统健康报告。当用户要求'监控性能'、'诊断卡顿'、'系统健康检查'、'Claude 慢'、'lag'时使用。
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- monitoring
- performance
- diagnostics
- system-health
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# Claude Monitor — 性能诊断

## 概述

Claude Code 和本地系统性能监控器。诊断卡顿，测量 CPU/RAM/磁盘，检查 API 延迟并生成系统健康报告。

## 何时使用此技能

- 当用户提到"慢"或相关话题时
- 当用户提到"卡顿"或相关话题时
- 当用户提到"lag"或相关话题时
- 当用户提到"卡死了"或相关话题时
- 当用户提到"卡住"或相关话题时
- 当用户提到"claude 慢"或相关话题时

## 不应使用此技能的情况

- 任务与 claude monitor 无关
- 更简单、更具体的工具可以处理请求
- 用户需要通用帮助而非领域专业知识

## 工作原理

用于诊断和解决 Claude Code 及系统中卡顿问题的技能。
确定瓶颈是在本地（PC）还是远程（Claude API），并建议纠正措施。

## 使用场景

- 用户抱怨 Claude Code 慢或卡住
- 切换对话会话加载缓慢
- Claude 响应时间过长
- 使用 Claude Code 时 PC 感觉缓慢
- 任何关于性能、lag、卡顿的提及

## 1. 快速诊断 (health_check.py)

始终作为第一步运行：

```bash
python C:\Users\renat\skills\claude-monitor\scripts\health_check.py
```

脚本在约 3 秒内分析：
- **CPU**: 当前使用率和各核心使用率。>80% = 可能存在瓶颈
- **RAM**: 总量、已用、可用。>85% = 内存压力
- **浏览器**: 各浏览器进程数和 RAM 占用。总计 >5GB = 标签页过多
- **Claude Code**: 进程数和消耗的 RAM
- **磁盘**: 可用空间。<10% = 影响 swap/性能
- **网络**: 到 Claude API 端点的延迟
- **诊断**: 自动分类问题并提供建议

## 2. 解读结果

脚本返回一个 JSON，其中 `diagnosis` 包含：

- `bottleneck`: "cpu" | "ram" | "browsers" | "disk" | "network" | "claude_api" | "ok"
- `severity`: "critical" | "warning" | "ok"
- `suggestions`: 推荐操作列表
- `summary`: 中文摘要，用于展示给用户

**向用户展示 `summary`** 并提议执行建议。

## 3. 自动纠正措施

根据诊断，向用户提供：

#### 如果 CPU 高（>80%）:
- 列出消耗最多 CPU 的进程
- 建议关闭不必要的重型进程
- 检查 Windows Update 是否在后台运行

#### 如果浏览器过重（>5GB RAM 或 >40 个进程）:
```bash
python C:\Users\renat\skills\claude-monitor\scripts\health_check.py --browsers-detail
```
显示各浏览器的 RAM 占用并建议关闭哪些。**未经用户明确许可，切勿关闭进程。**

#### 如果磁盘已满（>85%）:
- 显示大文件夹
- 建议清理 Temp、浏览器缓存、回收站

#### 如果网络缓慢（延迟 >500ms）:
- 测试与 api.anthropic.com 的连接
- 建议检查 VPN、代理或 WiFi 连接

## 4. 持续监控（可选）

如果用户想要后台监控：

```bash
python C:\Users\renat\skills\claude-monitor\scripts\monitor.py --interval 30 --duration 300
```

参数：
- `--interval`: 每次采样的间隔秒数（默认：30）
- `--duration`: 总持续时间秒数（默认：300 = 5 分钟）
- `--output`: 日志文件路径（默认：monitor_log.json）
- `--alert-cpu`: CPU 告警阈值（默认：80）
- `--alert-ram`: RAM 百分比告警阈值（默认：85）

监控器保存周期性快照并在结束时生成报告，包含：
- CPU 和 RAM 峰值
- 趋势（改善/恶化/稳定）
- 检测到的告警事件
- 最终建议

## 5. Claude API 基准测试（可选）

用于测试卡顿是否来自 API：

```bash
python C:\Users\renat\skills\claude-monitor\scripts\api_bench.py
```

测量本地 Claude Code 进程的响应时间（不调用 API）。
与典型时间比较并指示是否在预期范围内。

## 参考阈值

| 指标 | 正常 | 警告 | 严重 |
|------|------|------|------|
| CPU % | <60% | 60-85% | >85% |
| RAM 已用 % | <70% | 70-85% | >85% |
| 浏览器 RAM | <3 GB | 3-6 GB | >6 GB |
| 浏览器进程数 | <30 | 30-60 | >60 |
| 磁盘可用 | >15% | 10-15% | <10% |
| 网络延迟 | <200ms | 200-500ms | >500ms |

## 用户提示

展示诊断时，包含这些上下文提示：

- **太多标签页 = 太多 CPU/RAM**: 每个浏览器标签页都是独立进程。
  50 个标签页 = 50 个进程竞争资源。
- **Claude Code 较重**: 它运行多个 Electron 进程。正常消耗 3-5 GB。
  但如果使用 >6 GB 且有多个会话，考虑关闭旧会话。
- **会话切换慢**: 通常由 CPU 高或太多进程竞争引起。
  会话需要加载对话历史，如果 CPU 繁忙，就会变慢。
- **磁盘接近满**: 影响 swap（虚拟内存）速度，可能导致
  全面卡顿。

## 依赖

- Python 3.10+
- psutil（如不可用，脚本会自动安装）
- 无需 API key

## 最佳实践

- 提供清晰、具体的项目上下文和需求
- 在应用到生产代码前审查所有建议
- 结合其他互补技能进行全面分析

## 常见陷阱

- 将此技能用于其专业领域之外的任务
- 在不了解具体上下文的情况下应用建议
- 未提供足够的项目上下文以进行准确分析

## 局限性
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
