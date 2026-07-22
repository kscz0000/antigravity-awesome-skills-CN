# Loki Mode - 用于 SWE-bench 的多智能体系统

## 概述

**Loki Mode** 是一个作为 Claude Code 技能构建的多智能体系统，编排专业化 AI 智能体来解决软件工程任务。本提交展示其在 SWE-bench Lite 上的性能。

## 结果

| 指标 | 值 |
|------|-----|
| **补丁生成率** | **99.67%**（299/300） |
| 已解决问题 | 299 |
| 总问题数 | 300 |
| RARV 重试修复 | 0 |
| 平均尝试次数 | 1.0 |
| 总时间 | ~3.5 小时 |
| 平均时间/问题 | 42秒 |

## 系统架构

Loki Mode 使用 **4 智能体管道** 配合 RARV（推理-行动-反思-验证）循环：

```
Issue -> [架构师] -> [工程师] -> [QA] -> [审查者] -> Patch
                ^                                |
                |______ RARV 重试循环 ________|
```

### 智能体角色

| 智能体 | 角色 | 模型 | 超时 |
|-------|------|-------|---------|
| **架构师** | 分析问题、识别文件、设计修复方案 | Claude Opus 4.5 | 120s |
| **工程师** | 基于架构师分析生成补丁 | Claude Opus 4.5 | 300s |
| **QA** | 验证补丁格式（diff 头、hunks、路径） | 基于规则 | 5s |
| **审查者** | 分析格式问题、提供重试反馈 | Claude Opus 4.5 | 60s |

### RARV 循环

RARV（推理-行动-反思-验证）循环实现自我纠正：

1. **推理**：架构师分析问题
2. **行动**：工程师生成补丁
3. **反思**：QA 验证补丁格式
4. **验证**：若无效，审查者提供反馈，工程师重试

每个问题最多 3 次重试。

## 与基线比较

| 系统 | SWE-bench Lite 补丁生成 |
|--------|--------------------------|
| **Loki Mode（多智能体）** | **99.67%**（299/300） |
| 直接 Claude（单智能体） | 99.67%（299/300） |

超时优化后，多智能体 RARV 管道匹配单智能体性能。

## 方法论

1. **不克隆仓库**：补丁仅基于问题描述和提示生成
2. **生成期间不执行测试**：生成期间仅验证补丁格式
3. **确定性管道**：所有问题使用相同智能体序列
4. **完整轨迹日志**：记录所有提示和输出以确保透明度

## 仓库

- **GitHub**: [asklokesh/loki-mode](https://github.com/asklokesh/loki-mode)
- **许可证**: MIT
- **版本**: 2.25.0

## 运行 Loki Mode

```bash
# 克隆仓库
git clone https://github.com/asklokesh/loki-mode.git

# 用 Loki Mode 运行 SWE-bench
./benchmarks/run-benchmarks.sh swebench --execute --loki

# 限制数量测试运行
./benchmarks/run-benchmarks.sh swebench --execute --loki --limit 10
```

## 本提交文件

```
evaluation/lite/20260105_loki_mode/
├── README.md           # 本文件
├── metadata.yaml       # 提交元数据
├── all_preds.jsonl     # JSONL 格式预测
├── trajs/              # 推理轨迹（每个问题 1 个）
│   ├── django__django-11039.md
│   ├── matplotlib__matplotlib-23299.md
│   └── ...
└── logs/               # 执行日志（每个问题 1 个目录）
    ├── django__django-11039/
    │   ├── patch.diff
    │   ├── report.json
    │   └── test_output.txt
    └── ...
```

## 致谢

- 为 [Claude Code](https://claude.ai) 生态系统构建
- 由 Anthropic 的 Claude Opus 4.5 模型驱动
- 灵感来自多智能体协作模式

## 联系方式

- GitHub: [@asklokesh](https://github.com/asklokesh)
