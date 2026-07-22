---
name: deep-research
description: "运行自主研究任务，规划、搜索、阅读并综合信息生成全面报告。"
risk: safe
source: "https://github.com/sanjay3290/ai-skills/tree/main/skills/deep-research"
date_added: "2026-02-27"
---

# Gemini 深度研究技能

运行自主研究任务，规划、搜索、阅读并综合信息生成全面报告。

## 何时使用此技能

以下情况使用此技能：
- 进行市场分析
- 开展竞争格局调研
- 创建文献综述
- 进行技术研究
- 执行尽职调查
- 需要详细的、带引用的研究报告

## 环境要求

- Python 3.8+
- httpx: `pip install -r requirements.txt`
- GEMINI_API_KEY 环境变量

## 设置

1. 从 [Google AI Studio](https://aistudio.google.com/) 获取 Gemini API 密钥
2. 设置环境变量：
   ```bash
   export GEMINI_API_KEY=your-api-key-here
   ```
   或者在技能目录下创建 `.env` 文件。

## 使用方法

### 启动研究任务
```bash
python3 scripts/research.py --query "Research the history of Kubernetes"
```

### 使用结构化输出格式
```bash
python3 scripts/research.py --query "Compare Python web frameworks" \
  --format "1. Executive Summary\n2. Comparison Table\n3. Recommendations"
```

### 实时流式输出进度
```bash
python3 scripts/research.py --query "Analyze EV battery market" --stream
```

### 启动后不等待
```bash
python3 scripts/research.py --query "Research topic" --no-wait
```

### 检查正在运行的研究状态
```bash
python3 scripts/research.py --status <interaction_id>
```

### 等待完成
```bash
python3 scripts/research.py --wait <interaction_id>
```

### 继续之前的研究
```bash
python3 scripts/research.py --query "Elaborate on point 2" --continue <interaction_id>
```

### 列出最近的研究
```bash
python3 scripts/research.py --list
```

## 输出格式

- **默认**: 人类可读的 Markdown 报告
- **JSON** (`--json`): 用于程序化使用的结构化数据
- **原始** (`--raw`): 未经处理的 API 响应

## 成本与时间

| 指标 | 数值 |
|------|------|
| 时间 | 每个任务 2-10 分钟 |
| 成本 | 每个任务 $2-5（根据复杂度变化） |
| Token 使用量 | 输入约 250k-900k，输出约 60k-80k |

## 最佳使用场景

- 市场分析和竞争格局调研
- 技术文献综述
- 尽职调查研究
- 历史研究和时间线
- 比较分析（框架、产品、技术）

## 工作流程

1. 用户请求研究 → 运行 `--query "..."`
2. 告知用户预计时间（2-10 分钟）
3. 使用 `--stream` 监控或使用 `--status` 轮询
4. 返回格式化结果
5. 使用 `--continue` 进行后续问题

## 退出码

- **0**: 成功
- **1**: 错误（API 错误、配置问题、超时）
- **130**: 用户取消（Ctrl+C）

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
