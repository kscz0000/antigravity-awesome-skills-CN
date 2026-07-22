---
name: aegisops-ai
description: "自主 DevSecOps 与 FinOps 护栏。编排 Gemini 3 Flash 审计 Linux 内核补丁、Terraform 成本漂移和 K8s 合规性。触发词：DevSecOps、FinOps、内核补丁审计、Terraform 成本审计、K8s 合规、安全护栏、云成本审计、内核安全、IaC 审计、Kubernetes 策略加固"
risk: safe
source: community
author: Champbreed
date_added: "2026-03-24"
---

# /aegisops-ai — 自主治理编排器

AegisOps-AI 是一个专业级的"活管道"，将先进的 AI 推理能力直接集成到 SDLC 中。它充当系统级安全、云基础设施成本和 Kubernetes 合规性的智能守门人。

## 目标

通过以下方式自动化高风险的安全和财务审计：
1. 识别 Linux 内核补丁中基于逻辑的漏洞（UAF、陈旧状态）。
2. 检测 Terraform 计划中大规模的"静默灾难"成本漂移。
3. 将自然语言安全意图转化为加固的 K8s 清单。

## 何时使用
- **内核补丁审查：** 审计基于 C 的原始 Git 差异以检查内存安全。
- **预应用 IaC 审计：** 分析 `terraform plan` 输出以防止账单激增。
- **集群加固：** 为部署生成"最小权限" securityContext。
- **CI/CD 质量门控：** 通过 GitHub Actions 阻止不合规的合并。

## 何时不使用

- **Web 应用逻辑：** 不要用于标准 Web 漏洞（XSS、SQLi）；请使用专用 SAST 扫描器。
- **非 C 内存分析：** 补丁分析器针对 C 逻辑优化；避免用于 Python 或 JS 等高级语言。
- **直接资源变更：** 这是一个*审计器*，而非部署工具。它不执行 `terraform apply` 或 `kubectl apply`。
- **事后分析：** 要分析*为什么*之前的 AI 会话失败，请改用 `/analyze-project`。

---
## 🤖 生成式 AI 集成

AegisOps-AI 利用 **Google GenAI SDK** 实现自主安全和财务审计的"推理路径"：

* **神经补丁分析：** 对 Linux 内核补丁执行语义代码审查，超越简单的模式匹配，理解复杂的内存状态逻辑。
* **智能成本综合：** 通过财务推理模型处理原始 Terraform 计划差异，检测高风险的资源升级和"静默"财务漂移。
* **自然语言策略映射：** 将人类安全意图转化为语法正确、加固的 Kubernetes `securityContext` 配置。

## 🧭 核心模块

### 1. 🐧 内核补丁审查器 (`patch_analyzer.py`)

* **问题：** Linux 内核内存安全的手动审查耗时且容易出错。
* **解决方案：** Gemini 3 对原始 Git 差异执行"深度推理"审计，在几秒内检测关键的内存损坏漏洞（UAF、陈旧状态）。
* **关键输出：** `analysis_results.json`

### 2. 💰 FinOps 与云审计器 (`cost_auditor.py`)

* **问题：** 基础设施即代码（IaC）变更可能导致意外的"静默灾难"和大规模云账单激增。
* **解决方案：** 分析 `terraform plan` 输出以识别成本异常——例如从 `t3.micro` 意外升级到高性能 GPU 实例。
* **关键输出：** `infrastructure_audit_report.json`

### 3. ☸️ K8s 策略加固器 (`k8s_policy_generator.py`)

* **问题：** 在 Kubernetes 中实现"最小权限"安全上下文复杂且常被忽视。
* **解决方案：** 将自然语言安全要求转化为生产就绪的加固 YAML 清单（只读根文件系统、非 root 强制执行等）。
* **关键输出：** `hardened_deployment.yaml`

## 🛠️ 设置与环境

### 1. 克隆仓库

```bash
git clone https://github.com/Champbreed/AegisOps-AI.git
cd AegisOps-AI
```
## 2. 设置

```bash
python3 -m venv venv
source venv/bin/activate
pip install google-genai python-dotenv
```
### 3. API 配置

在根目录创建 `.env` 文件以安全存储您的凭据：

```bash
echo "GEMINI_API_KEY='your_api_key_here'" > .env
```
## 🏁 运行仪表盘

要按顺序执行完整的智能体套件并生成所有安全报告：

```bash
python3 main.py
```
### 模式：过度特权容器

* **指标：** `allowPrivilegeEscalation: true` 或 root 用户执行。
* **调查：** 将安全意图（例如"仅非 root"）传递给 K8s 加固模块。

---

## 💡 最佳实践

* **上下文为王：** 为 Git 差异提供至少 5 行上下文以获得更准确的神经推理。
* **持续门控：** 在每次基础设施变更之前运行 FinOps 审计器，而非之后。
* **人工签核：** 将 AI 发现作为高保真信号，但对内核级合并保持人工介入。

---

## 🔒 安全与注意事项

* **密钥管理：** 在生产环境中使用 CI/CD secrets 管理 `GEMINI_API_KEY`。
* **最小权限：** 先在预发环境中测试"加固"清单，确保无功能回归。

## 链接

+ - **仓库**: https://github.com/Champbreed/AegisOps-AI
+ - **文档**: https://github.com/Champbreed/AegisOps-AI#readme

## 限制
- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
