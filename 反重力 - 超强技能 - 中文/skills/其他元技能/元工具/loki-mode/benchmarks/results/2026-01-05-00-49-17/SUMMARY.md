# Loki Mode 基准测试结果

**生成时间：** 2026-01-05 01:10:21

## 概述

本目录包含 Loki Mode 多智能体系统的基准测试结果。

## HumanEval 结果

| 指标 | 值 |
|------|-----|
| 问题数 | 164 |
| 通过 | 161 |
| 失败 | 3 |
| **通过率** | **98.17%** |
| 模型 | opus |
| 时间 | 1263.46s |

### 竞争对手比较

| 系统 | Pass@1 |
|------|--------|
| MetaGPT | 85.9-87.7% |
| **Loki Mode** | **98.17%** |

## 方法论

Loki Mode 使用其多智能体架构来解决每个问题：
1. **架构师智能体** 分析问题
2. **工程师智能体** 实现解决方案
3. **QA 智能体** 用测试用例验证
4. **审查智能体** 检查代码质量

这比单智能体方法更准确地模拟了现实世界的软件开发。

## 运行基准测试

```bash
# 仅设置（下载数据集）
./benchmarks/run-benchmarks.sh all

# 使用 Claude 执行
./benchmarks/run-benchmarks.sh humaneval --execute
./benchmarks/run-benchmarks.sh humaneval --execute --limit 10  # 仅前 10 个
./benchmarks/run-benchmarks.sh swebench --execute --limit 5    # 仅前 5 个

# 使用不同模型
./benchmarks/run-benchmarks.sh humaneval --execute --model opus
```
