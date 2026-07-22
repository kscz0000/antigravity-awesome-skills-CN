---
name: qiskit
description: "Qiskit 是全球最流行的开源量子计算框架，下载量超过 1300 万次。构建量子电路、针对硬件优化、在模拟器或真实量子计算机上执行并分析结果。支持 IBM Quantum（100+ 量子比特系统）、IonQ、Amazon Braket 等提供商。当用户要求量子计算、量子电路、Qiskit、IBM Quantum、量子算法、量子模拟时使用。"
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
    risk: unknown
    source: community
---

# Qiskit

## 何时使用

- 你正在使用 Qiskit 为模拟器或真实硬件构建或优化量子电路。
- 你需要 IBM Quantum 风格的工具来进行转译、执行、可视化或算法库操作。
- 你希望获得从简单电路原型到后端感知执行的指导。

## 概述

Qiskit 是全球最流行的开源量子计算框架，下载量超过 1300 万次。构建量子电路、针对硬件优化、在模拟器或真实量子计算机上执行并分析结果。支持 IBM Quantum（100+ 量子比特系统）、IonQ、Amazon Braket 等提供商。

**核心特性：**
- 转译速度比竞争对手快 83 倍
- 优化电路中的双量子比特门减少 29%
- 后端无关执行（本地模拟器或云端硬件）
- 面向优化、化学和机器学习的综合算法库

## 快速开始

### 安装

```bash
uv pip install qiskit
uv pip install "qiskit[visualization]" matplotlib
```

### 第一个电路

```python
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

# 创建 Bell 态（纠缠量子比特）
qc = QuantumCircuit(2)
qc.h(0)           # 在量子比特 0 上应用 Hadamard 门
qc.cx(0, 1)       # 从量子比特 0 到 1 的 CNOT 门
qc.measure_all()  # 测量两个量子比特

# 本地运行
sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
print(counts)  # {'00': ~512, '11': ~512}
```

### 可视化

```python
from qiskit.visualization import plot_histogram

qc.draw('mpl')           # 电路图
plot_histogram(counts)   # 结果直方图
```

## 核心能力

### 1. 设置与安装

详细的安装、认证和 IBM Quantum 账户设置：
- **参见 `references/setup.md`**

涵盖主题：
- 使用 uv 安装
- Python 环境设置
- IBM Quantum 账户和 API token 配置
- 本地与云端执行

### 2. 构建量子电路

使用门、测量和组合构建量子电路：
- **参见 `references/circuits.md`**

涵盖主题：
- 使用 QuantumCircuit 创建电路
- 单量子比特门（H、X、Y、Z、旋转门、相位门）
- 多量子比特门（CNOT、SWAP、Toffoli）
- 测量和屏障
- 电路组合与属性
- 用于变分算法的参数化电路

### 3. 原语（Sampler 和 Estimator）

执行量子电路并计算结果：
- **参见 `references/primitives.md`**

涵盖主题：
- **Sampler**：获取比特串测量值和概率分布
- **Estimator**：计算可观测量的期望值
- V2 接口（StatevectorSampler、StatevectorEstimator）
- 用于硬件的 IBM Quantum Runtime 原语
- Session 和 Batch 模式
- 参数绑定

### 4. 转译与优化

优化电路并为硬件执行做准备：
- **参见 `references/transpilation.md`**

涵盖主题：
- 为什么需要转译
- 优化级别（0-3）
- 六个转译阶段（init、layout、routing、translation、optimization、scheduling）
- 高级功能（虚拟置换消除、门消除）
- 常用参数（initial_layout、approximation_degree、seed）
- 高效电路的最佳实践

### 5. 可视化

显示电路、结果和量子态：
- **参见 `references/visualization.md`**

涵盖主题：
- 电路图（文本、matplotlib、LaTeX）
- 结果直方图
- 量子态可视化（Bloch 球、state city、QSphere）
- 后端拓扑和误差图
- 自定义和样式
- 保存出版级质量的图形

### 6. 硬件后端

在模拟器和真实量子计算机上运行：
- **参见 `references/backends.md`**

涵盖主题：
- IBM Quantum 后端和认证
- 后端属性和状态
- 使用 Runtime 原语在真实硬件上运行
- 作业管理和排队
- Session 模式（迭代算法）
- Batch 模式（并行作业）
- 本地模拟器（StatevectorSampler、Aer）
- 第三方提供商（IonQ、Amazon Braket）
- 错误缓解策略

### 7. Qiskit Patterns 工作流

实现四步量子计算工作流：
- **参见 `references/patterns.md`**

涵盖主题：
- **Map**：将问题转化为量子电路
- **Optimize**：为硬件进行转译
- **Execute**：使用原语运行
- **Post-process**：提取和分析结果
- 完整的 VQE 示例
- Session 与 Batch 执行
- 常用工作流模式

### 8. 量子算法与应用

实现特定的量子算法：
- **参见 `references/algorithms.md`**

涵盖主题：
- **优化**：VQE、QAOA、Grover 算法
- **化学**：分子基态、激发态、哈密顿量
- **机器学习**：量子核、VQC、QNN
- **算法库**：Qiskit Nature、Qiskit ML、Qiskit Optimization
- 物理模拟和基准测试

## 工作流决策指南

**如果你需要：**

- 安装 Qiskit 或设置 IBM Quantum 账户 → `references/setup.md`
- 构建新的量子电路 → `references/circuits.md`
- 理解门和电路操作 → `references/circuits.md`
- 运行电路并获取测量结果 → `references/primitives.md`
- 计算期望值 → `references/primitives.md`
- 为硬件优化电路 → `references/transpilation.md`
- 可视化电路或结果 → `references/visualization.md`
- 在 IBM Quantum 硬件上执行 → `references/backends.md`
- 连接第三方提供商 → `references/backends.md`
- 实现端到端量子工作流 → `references/patterns.md`
- 构建特定算法（VQE、QAOA 等）→ `references/algorithms.md`
- 解决化学或优化问题 → `references/algorithms.md`

## 最佳实践

### 开发工作流

1. **从模拟器开始**：在使用硬件之前先在本地测试
   ```python
   from qiskit.primitives import StatevectorSampler
   sampler = StatevectorSampler()
   ```

2. **始终转译**：执行前优化电路
   ```python
   from qiskit import transpile
   qc_optimized = transpile(qc, backend=backend, optimization_level=3)
   ```

3. **使用适当的原语**：
   - Sampler 用于比特串（优化算法）
   - Estimator 用于期望值（化学、物理）

4. **选择执行模式**：
   - Session：迭代算法（VQE、QAOA）
   - Batch：独立并行作业
   - Single job：一次性实验

### 性能优化

- 生产环境使用 optimization_level=3
- 最小化双量子比特门（主要误差来源）
- 在硬件上运行前先用噪声模拟器测试
- 保存并重用转译后的电路
- 在变分算法中监控收敛

### 硬件执行

- 提交前检查后端状态
- 测试时使用 least_busy()
- 保存作业 ID 以便后续检索
- 应用错误缓解（resilience_level）
- 从较少 shots 开始，最终运行时增加

## 常用模式

### 模式 1：简单电路执行

```python
from qiskit import QuantumCircuit, transpile
from qiskit.primitives import StatevectorSampler

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

sampler = StatevectorSampler()
result = sampler.run([qc], shots=1024).result()
counts = result[0].data.meas.get_counts()
```

### 模式 2：带转译的硬件执行

```python
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit import transpile

service = QiskitRuntimeService()
backend = service.backend("ibm_brisbane")

qc_optimized = transpile(qc, backend=backend, optimization_level=3)

sampler = Sampler(backend)
job = sampler.run([qc_optimized], shots=1024)
result = job.result()
```

### 模式 3：变分算法（VQE）

```python
from qiskit_ibm_runtime import Session, EstimatorV2 as Estimator
from scipy.optimize import minimize

with Session(backend=backend) as session:
    estimator = Estimator(session=session)

    def cost_function(params):
        bound_qc = ansatz.assign_parameters(params)
        qc_isa = transpile(bound_qc, backend=backend)
        result = estimator.run([(qc_isa, hamiltonian)]).result()
        return result[0].data.evs

    result = minimize(cost_function, initial_params, method='COBYLA')
```

## 更多资源

- **官方文档**：https://quantum.ibm.com/docs
- **Qiskit 教科书**：https://qiskit.org/learn
- **API 参考**：https://docs.quantum.ibm.com/api/qiskit
- **Patterns 指南**：https://quantum.cloud.ibm.com/docs/en/guides/intro-to-patterns

## 局限性

- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
