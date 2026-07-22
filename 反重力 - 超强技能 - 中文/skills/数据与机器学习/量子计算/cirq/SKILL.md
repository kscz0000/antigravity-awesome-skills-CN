---
name: cirq
description: "Cirq 是 Google Quantum AI 的开源框架，用于在量子计算机和模拟器上设计、模拟和运行量子电路。触发词：Cirq、量子计算、量子电路、quantum computing、Google Quantum AI、量子模拟、量子门、量子比特、参数化电路、cirq-google、cirq-ionq、量子算法、VQE、QAOA、量子噪声、量子硬件、量子实验。"
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
    risk: unknown
    source: community
---

# Cirq - Python 量子计算

Cirq 是 Google Quantum AI 的开源框架，用于在量子计算机和模拟器上设计、模拟和运行量子电路。

## 何时使用

- 你正在使用 Cirq 生态系统设计、模拟或执行量子电路。
- 你需要 Google Quantum AI 风格的原语、参数化电路，或 `cirq-google` 和 `cirq-ionq` 等集成。
- 你正在用 Python 原型设计或教授量子工作流，并希望获得具体的电路示例。

## 安装

```bash
uv pip install cirq
```

硬件集成：

```bash
# Google Quantum Engine
uv pip install cirq-google

# IonQ
uv pip install cirq-ionq

# AQT (Alpine Quantum Technologies)
uv pip install cirq-aqt

# Pasqal
uv pip install cirq-pasqal

# Azure Quantum
uv pip install azure-quantum cirq
```

## 快速入门

### 基本电路

```python
import cirq
import numpy as np

# Create qubits
q0, q1 = cirq.LineQubit.range(2)

# Build circuit
circuit = cirq.Circuit(
    cirq.H(q0),              # Hadamard on q0
    cirq.CNOT(q0, q1),       # CNOT with q0 control, q1 target
    cirq.measure(q0, q1, key='result')
)

print(circuit)

# Simulate
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1000)

# Display results
print(result.histogram(key='result'))
```

### 参数化电路

```python
import sympy

# Define symbolic parameter
theta = sympy.Symbol('theta')

# Create parameterized circuit
circuit = cirq.Circuit(
    cirq.ry(theta)(q0),
    cirq.measure(q0, key='m')
)

# Sweep over parameter values
sweep = cirq.Linspace('theta', start=0, stop=2*np.pi, length=20)
results = simulator.run_sweep(circuit, params=sweep, repetitions=1000)

# Process results
for params, result in zip(sweep, results):
    theta_val = params['theta']
    counts = result.histogram(key='m')
    print(f"θ={theta_val:.2f}: {counts}")
```

## 核心能力

### 电路构建
关于构建量子电路的全面信息，包括量子比特、门、操作、自定义门和电路模式，请参阅：
- **references/building.md** - 电路构建完整指南

常见主题：
- 量子比特类型（GridQubit、LineQubit、NamedQubit）
- 单量子比特和双量子比特门
- 参数化门和操作
- 自定义门分解
- 使用时刻（moments）组织电路
- 标准电路模式（Bell 态、GHZ、QFT）
- 导入/导出（OpenQASM、JSON）
- 使用量子迪特（qudits）和可观测量

### 模拟
关于模拟量子电路的详细信息，包括精确模拟、噪声模拟、参数扫描和量子虚拟机，请参阅：
- **references/simulation.md** - 量子模拟完整指南

常见主题：
- 精确模拟（态矢量、密度矩阵）
- 采样和测量
- 参数扫描（单参数和多参数）
- 噪声模拟
- 状态直方图和可视化
- 量子虚拟机（QVM）
- 期望值和可观测量
- 性能优化

### 电路变换
关于优化、编译和操作量子电路的信息，请参阅：
- **references/transformation.md** - 电路变换完整指南

常见主题：
- 变换器框架
- 门分解
- 电路优化（合并门、弹出 Z 门、丢弃可忽略操作）
- 面向硬件的电路编译
- 量子比特路由和 SWAP 插入
- 自定义变换器
- 变换管道

### 硬件集成
关于在各种提供商的真实量子硬件上运行电路的信息，请参阅：
- **references/hardware.md** - 硬件集成完整指南

支持的提供商：
- **Google Quantum AI** (cirq-google) - Sycamore、Weber 处理器
- **IonQ** (cirq-ionq) - 离子阱量子计算机
- **Azure Quantum** (azure-quantum) - IonQ 和 Honeywell 后端
- **AQT** (cirq-aqt) - Alpine Quantum Technologies
- **Pasqal** (cirq-pasqal) - 中性原子量子计算机

主题包括设备表示、量子比特选择、认证、作业管理和面向硬件的电路优化。

### 噪声建模
关于建模噪声、噪声模拟、表征和错误缓解的信息，请参阅：
- **references/noise.md** - 噪声建模完整指南

常见主题：
- 噪声信道（去极化、振幅阻尼、相位阻尼）
- 噪声模型（常数、门特定、量子比特特定、热噪声）
- 向电路添加噪声
- 读出噪声
- 噪声表征（随机基准测试、XEB）
- 噪声可视化（热力图）
- 错误缓解技术

### 量子实验
关于设计实验、参数扫描、数据收集和使用 ReCirq 框架的信息，请参阅：
- **references/experiments.md** - 量子实验完整指南

常见主题：
- 实验设计模式
- 参数扫描和数据收集
- ReCirq 框架结构
- 常见算法（VQE、QAOA、QPE）
- 数据分析和可视化
- 统计分析和保真度估计
- 并行数据收集

## 常见模式

### 变分算法模板

```python
import scipy.optimize

def variational_algorithm(ansatz, cost_function, initial_params):
    """Template for variational quantum algorithms."""

    def objective(params):
        circuit = ansatz(params)
        simulator = cirq.Simulator()
        result = simulator.simulate(circuit)
        return cost_function(result)

    # Optimize
    result = scipy.optimize.minimize(
        objective,
        initial_params,
        method='COBYLA'
    )

    return result

# Define ansatz
def my_ansatz(params):
    q = cirq.LineQubit(0)
    return cirq.Circuit(
        cirq.ry(params[0])(q),
        cirq.rz(params[1])(q)
    )

# Define cost function
def my_cost(result):
    state = result.final_state_vector
    # Calculate cost based on state
    return np.real(state[0])

# Run optimization
result = variational_algorithm(my_ansatz, my_cost, [0.0, 0.0])
```

### 硬件执行模板

```python
def run_on_hardware(circuit, provider='google', device_name='weber', repetitions=1000):
    """Template for running on quantum hardware."""

    if provider == 'google':
        import cirq_google
        engine = cirq_google.get_engine()
        processor = engine.get_processor(device_name)
        job = processor.run(circuit, repetitions=repetitions)
        return job.results()[0]

    elif provider == 'ionq':
        import cirq_ionq
        service = cirq_ionq.Service()
        result = service.run(circuit, repetitions=repetitions, target='qpu')
        return result

    elif provider == 'azure':
        from azure.quantum.cirq import AzureQuantumService
        # Setup workspace...
        service = AzureQuantumService(workspace)
        result = service.run(circuit, repetitions=repetitions, target='ionq.qpu')
        return result

    else:
        raise ValueError(f"Unknown provider: {provider}")
```

### 噪声研究模板

```python
def noise_comparison_study(circuit, noise_levels):
    """Compare circuit performance at different noise levels."""

    results = {}

    for noise_level in noise_levels:
        # Create noisy circuit
        noisy_circuit = circuit.with_noise(cirq.depolarize(p=noise_level))

        # Simulate
        simulator = cirq.DensityMatrixSimulator()
        result = simulator.run(noisy_circuit, repetitions=1000)

        # Analyze
        results[noise_level] = {
            'histogram': result.histogram(key='result'),
            'dominant_state': max(
                result.histogram(key='result').items(),
                key=lambda x: x[1]
            )
        }

    return results

# Run study
noise_levels = [0.0, 0.001, 0.01, 0.05, 0.1]
results = noise_comparison_study(circuit, noise_levels)
```

## 最佳实践

1. **电路设计**
   - 为你的拓扑结构选择合适的量子比特类型
   - 保持电路模块化和可复用
   - 使用描述性键标记测量
   - 在执行前根据设备约束验证电路

2. **模拟**
   - 对纯态使用态矢量模拟（更高效）
   - 仅在需要时使用密度矩阵模拟（混合态、噪声）
   - 利用参数扫描而非单独运行
   - 监控大型系统的内存使用（2^n 增长很快）

3. **硬件执行**
   - 始终先在模拟器上测试
   - 使用校准数据选择最佳量子比特
   - 针对目标硬件门集优化电路
   - 为生产运行实施错误缓解
   - 立即存储昂贵的硬件结果

4. **电路优化**
   - 从高级内置变换器开始
   - 顺序链接多个优化
   - 跟踪深度和门数减少
   - 变换后验证正确性

5. **噪声建模**
   - 使用来自校准数据的真实噪声模型
   - 包含所有误差源（门、退相干、读出）
   - 缓解前先表征
   - 保持电路浅层以最小化噪声累积

6. **实验**
   - 用清晰分离构建实验（数据生成、收集、分析）
   - 使用 ReCirq 模式确保可复现性
   - 频繁保存中间结果
   - 并行化独立任务
   - 用元数据彻底记录

## 其他资源

- **官方文档**: https://quantumai.google/cirq
- **API 参考**: https://quantumai.google/reference/python/cirq
- **教程**: https://quantumai.google/cirq/tutorials
- **示例**: https://github.com/quantumlib/Cirq/tree/master/examples
- **ReCirq**: https://github.com/quantumlib/ReCirq

## 常见问题

**电路对硬件来说太深：**
- 使用电路优化变换器减少深度
- 参见 `transformation.md` 了解优化技术

**模拟内存问题：**
- 从密度矩阵切换到态矢量模拟器
- 减少量子比特数量或对 Clifford 电路使用稳定子模拟器

**设备验证错误：**
- 使用 device.metadata.nx_graph 检查量子比特连通性
- 将门分解为设备原生门集
- 参见 `hardware.md` 了解设备特定编译

**噪声模拟太慢：**
- 密度矩阵模拟是 O(2^2n) - 考虑减少量子比特
- 仅对关键操作选择性地使用噪声模型
- 参见 `simulation.md` 了解性能优化

## 限制

- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
