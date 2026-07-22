# Loki Mode 基准测试结果

## 概述

本目录包含 Loki Mode 多智能体系统的基准测试结果。

## 可用基准测试

### HumanEval
- **问题数：** 164 个 Python 编程问题
- **指标：** Pass@1（首次尝试解决的问题百分比）
- **竞争对手基线：** MetaGPT 达到 85.9-87.7%

### SWE-bench Lite
- **问题数：** 300 个真实 GitHub issue
- **指标：** 解决率
- **竞争对手基线：** 顶级智能体达到 45-77%

## 运行基准测试

```bash
# 运行所有基准测试
./benchmarks/run-benchmarks.sh all

# 运行特定基准测试
./benchmarks/run-benchmarks.sh humaneval --execute
./benchmarks/run-benchmarks.sh swebench --execute
```

## 结果格式

结果保存为 JSON 文件，包含：
- 时间戳
- 问题数量
- 通过率
- 单个问题结果
- Token 使用量
- 执行时间

## 方法论

Loki Mode 使用其多智能体架构来解决每个问题：
1. **架构师智能体** 分析问题
2. **工程师智能体** 实现解决方案
3. **QA 智能体** 用测试用例验证
4. **审查智能体** 检查代码质量

这比单智能体方法更准确地模拟了现实世界的软件开发。
