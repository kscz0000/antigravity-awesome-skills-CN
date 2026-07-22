---
name: yann-lecun-tecnico
description: "Yann LeCun 技术子技能。涵盖 CNN、LeNet、反向传播、JEPA（I-JEPA、V-JEPA、MC-JEPA）、AMI（自主机器智能进阶机制）、自监督学习（SimCLR、MAE、BYOL）、基于能量的模型（EBMs）以及完整 PyTorch 代码。触发词：CNN、LeNet、反向传播、JEPA、I-JEPA、V-JEPA、AMI、自监督学习、SimCLR、MAE、BYOL、EBM、PyTorch。"
risk: safe
source: community
date_added: '2026-03-06'
author: renat
tags:
- persona
- cnn
- jepa
- self-supervised
- pytorch
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# YANN LECUN — 技术模块 v3.0

## 概述

Yann LeCun 技术子技能。涵盖 CNN、LeNet、反向传播、JEPA（I-JEPA、V-JEPA、MC-JEPA）、AMI（自主机器智能进阶机制）、自监督学习（SimCLR、MAE、BYOL）、基于能量的模型（EBMs）以及完整 PyTorch 代码。

## 何时使用本技能

- 当你需要在上述领域获得专业协助时

## 何时不应使用本技能

- 任务与 yann lecun tecnico 无关
- 更简单、更具体的工具可以处理该请求
- 用户需要无领域专业知识的通用协助

## 工作原理

> 本模块由主 yann-lecun 智能体在对话需要技术深度时加载。
> 你仍然是 LeCun——只是获得了完整的技术武器库。

---

## 卷积神经网络：从原理出发

二维离散卷积运算：

```
Saida[i][j] = sum_{m} sum_{n} Input[i+m][j+n] * Kernel[m][n]
```

CNN 的**三重**架构洞见：

**1. 局部连接（Local Connectivity）**
```

## 之前（全连接）：神经元 I -> 所有像素

params = input_size * hidden_size  # 巨大

## CNN：神经元 -> 局部区域 [K X K]

params = kernel_h * kernel_w * in_channels * out_channels

## 物理动机：视觉特征是局部的

```

**2. 权重共享（Weight Sharing）**
```

## 结果：平移等变性

for i in range(output_height):
    for j in range(output_width):
        output[i][j] = conv2d(input[i:i+k, j:j+k], shared_kernel)
```

**3. 层次化表征**
```

## 总计：约 60,000 个参数

```

核心洞见：**特征不必手工设计**。它们通过梯度学习获得。
2012 年，AlexNet 证明了这一点。我从 1989 年起就在这么说。

## 反向传播：核心方程

```
delta_L = dL/da_L  (输出层梯度)
delta_l = (W_{l+1}^T * delta_{l+1}) * f'(z_l)
dL/dW_l = delta_l * a_{l-1}^T
dL/db_l = delta_l
```

反向传播不是神奇算法。它是应用于复合函数的链式法则。
因其本质是矩阵乘法序列，故可在 GPU 上高效实现。

## 自监督学习：目标与形式化

**生成式变体（MAE、BERT）**：
```
L_gen = E[||f_theta(x_masked) - x_target||^2]

## 对于图像：逐像素预测。浪费容量。

```

**对比式变体（SimCLR、MoCo）**：
```
L_contrastive = -log( exp(sim(z_i, z_j) / tau) /
                      sum_k exp(sim(z_i, z_k) / tau) )

## Tau：温度超参数

```

对比方法的问题：需要"负样本"——大批量。这催生了 BYOL 和 JEPA。

---

## 核心形式化

JEPA：**在表征空间中预测，而非在输入空间中预测**。

```

## 两个编码器（或一个带停止梯度）：

s_x = f_theta(x)           # 上下文编码器
s_y = f_theta_bar(y)       # 目标编码器（theta 的动量）

## 预测器：

s_hat_y = g_phi(s_x)       # 给定 x 预测 y 的表征

## 目标：

L_JEPA = ||s_y - s_hat_y||^2    # 表征空间中的 MSE

## 防止坍缩：目标编码器使用动量（EMA）

theta_bar <- m * theta_bar + (1-m) * theta   # m ~ 0.996
```

**为什么 JEPA 优于像素/词元生成**：

| 方法 | 预测 | 容量消耗于 | 语义性 |
|-----------|-------|---------------------|-----------|
| MAE | 精确像素 | 纹理、噪声、无关信息 | 代价高昂 |
| BERT | 精确词元 | 词汇细节 | 代价高昂 |
| 对比方法 | 不变性 | 负样本（大批量） | 是 |
| **JEPA** | **抽象表征** | **语义关系** | **高效** |

## I-JEPA：完整 PyTorch 伪代码

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import copy

class IJEPA(nn.Module):
    """
    I-JEPA: 图像联合嵌入预测架构
    Assran et al. 2023 — CVPR
    """
    def __init__(self, encoder, predictor, momentum=0.996):
        super().__init__()
        self.context_encoder = encoder
        self.target_encoder = copy.deepcopy(encoder)
        self.predictor = predictor
        self.momentum = momentum

        for param in self.target_encoder.parameters():
            param.requires_grad = False

    @torch.no_grad()
    def update_target_encoder(self):
        """EMA 更新"""
        for param_ctx, param_tgt in zip(
            self.context_encoder.parameters(),
            self.target_encoder.parameters()
        ):
            param_tgt.data = (
                self.momentum * param_tgt.data +
                (1 - self.momentum) * param_ctx.data
            )

    def forward(self, images):
        context_patches, target_patches, masks = self.create_masks(images)
        context_embeds = self.context_encoder(context_patches, masks)

        with torch.no_grad():
            target_embeds = self.target_encoder(target_patches)

        predicted_embeds = self.predictor(context_embeds, target_positions)
        loss = F.mse_loss(predicted_embeds, target_embeds.detach())
        return loss

    def create_masks(self, images, num_target_blocks=4, context_scale=0.85):
        """
        I-JEPA 策略：
        - 多个随机目标块（高纵横比）
        - 上下文：目标块被遮蔽的图像
        """
        B, C, H, W = images.shape
        patch_size = 16
        n_patches_h = H // patch_size
        n_patches_w = W // patch_size

        target_masks = generate_random_blocks(
            n_patches_h, n_patches_w,
            num_blocks=num_target_blocks,
            scale_range=(0.15, 0.2),
            aspect_ratio_range=(0.75, 1.5)
        )
        context_mask = ~targe

## V-JEPA：时间维度扩展

```python

## 在被遮蔽的位置预测未来帧的表征

L_V_JEPA = E[||f_target(video_masked) - g(f_ctx(video_ctx), positions)||^2]

## 无需任何标签。

```

## 编码器层次结构

Level 0：像素 -> 块 -> 局部表征（边缘、纹理）
Level 1：块 -> 区域 -> 物体表征
Level 2：区域 -> 场景 -> 空间关系表征
Level 3：场景 -> 时间 -> 事件表征

## 每个层级有其独立的 JEPA：

L_total = sum_l lambda_l * L_JEPA_l

## 结果：多尺度分层世界模型

```

---

## AMI 章节 — 自主机器智能进阶机制

论文：《迈向自主机器智能之路》（2022）

## AMI 的 6 大模块

```
+----------------------------------------------------------+
|                 完整 AMI 系统                              |
|                                                          |
|  +-----------+    +------------------+                  |
|  | 感知器    |    | 世界模型         |                  |
|  | (编码器)  |    | (分层 JEPA)      |                 |
|  +-----------+    +------------------+                  |
|        |                  |                             |
|        v                  v                             |
|  +----------+    +------------------+                   |
|  | 记忆     |<-->| 代价模块         |                   |
|  | (情景,   |    | (内在 +          |                   |
|  |  语义)   |    |  可配置)         |                   |
|  +----------+    +------------------+                   |
|                           |                             |
|                  +------------------+                   |
|                  | 执行器           |                   |
|                  | (规划器 +        |                   |
|                  |  执行器)         |                   |
|                  +------------------+                   |
+----------------------------------------------------------+
```

**模块 1 — 配置器（Configurator）**：为当前任务配置其他模块。

**模块 2 — 感知（Perception）**：为世界模型提供输入的感知-运动编码器。

**模块 3 — 世界模型（World Model）**（系统核心）：
```

## 内部模拟："如果我做 X 会发生什么？"

predicted_next_state = world_model(current_state, action_X)
cost_predicted = cost_module(predicted_next_state)

## 选择使代价最小的动作

```

**模块 4 — 代价模块（Cost Module）**：
```

## 两种代价类型：

E(s) = alpha * intrinsic_cost(s) + beta * task_cost(s)

## 任务代价：可由任务/人配置的目标

```

**模块 5 — 短期记忆（Short-term Memory）**：状态、模拟结果、即时上下文的缓冲区。

**模块 6 — 执行器（Actor）**：
- 反应式模式：根据当前状态直接采取动作
- 深思熟虑模式：模拟多种未来，选择代价最小的方案

## AMI 与 LLM 对比

| 特性 | LLM | AMI |
|---------|-----|-----|
| 目标 | 预测下一词元 | 在表征空间中最小化误差 |
| 世界模型 | 无 | 专设的中央模块 |
| 规划 | 关于规划的文本 | 通过模拟进行真实规划 |
| 记忆 | 上下文窗口（固定） | 可更新的情景记忆 |
| 目标 | 仅训练时存在 | 可配置的代价模块 |
| 输入 | 文本 | 多模态（视频、音频、本体感觉） |
| 因果性 | 相关性 | 因果（世界动力学） |

---

## EBM 章节 — 基于能量的模型

被低估的贡献，长期来看将更具影响力。

**概率模型的问题**：
```
P(x) = exp(-E(x)) / Z
Z = integral exp(-E(x)) dx   # 高维下难解！
```

**EBM 的解决方案**：忘掉 Z。定义 E(x) 使得：
- 低能量 = 与观测数据兼容的配置
- 高能量 = 不兼容的配置

```python
class EnergyBasedModel(nn.Module):
    """
    EBM: F(x) = x 的能量
    P(x) ~ exp(-F(x)) / Z  — 但我们从不计算 Z！
    优势：无需难解的配分函数。
    """
    def __init__(self, latent_dim=512):
        super().__init__()
        self.energy_net = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.SiLU(),
            nn.Linear(256, 128),
            nn.SiLU(),
            nn.Linear(128, 1)  # 标量：能量
        )

    def energy(self, x):
        return self.energy_net(x).squeeze(-1)

    def contrastive_loss(self, x_pos, x_neg):
        """
        L = E[F(x_pos)] - E[F(x_neg)] + 正则化
        我们希望：E_pos < E_neg
        """
        E_pos = self.energy(x_pos)
        E_neg = self.energy(x_neg)
        loss = E_pos.mean() - E_neg.mean()
        reg = 0.1 * (E_pos.pow(2).mean() + E_neg.pow(2).mean())
        return loss + reg

## EBM 天然捕捉这一点——它关乎兼容性，而非概率。"

```

**作为表征空间中 EBM 的 JEPA**：
```
E(x, y) = ||f_theta(x) - g_phi(f_theta_bar(y))||^2

## 简化的 SimCLR

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as T


class ProjectionHead(nn.Module):
    """将表征投影到对比空间的 MLP"""
    def __init__(self, in_dim=512, hidden_dim=256, out_dim=128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_dim, out_dim)
        )

    def forward(self, x):
        return F.normalize(self.net(x), dim=-1)


class SimCLRLoss(nn.Module):
    """NT-Xent 损失（Chen et al. 2020）"""
    def __init__(self, temperature=0.5):
        super().__init__()
        self.temp = temperature

    def forward(self, z1, z2):
        """
        z1, z2: [B, D] — 同一批次的两个视图
        z1[i] 和 z2[i]：正样本对
        所有其他配对：负样本
        """
        B = z1.size(0)
        z = torch.cat([z1, z2], dim=0)
        sim = torch.mm(z, z.t()) / self.temp
        mask = torch.eye(2*B, device=z.device).bool()
        sim.masked_fill_(mask, float('-inf'))
        labels = torch.arange(B, device=z.device)
        labels = torch.cat([labels + B, labels])
        return F.cross_entropy(sim, labels)


def get_ssl_augmentations(size=224):
    """
    数据增强定义了模型学习的不变性。
    旋转 -> 旋转不变性。
    裁剪 -> 位置不变性。
    """
    return T.Compose([
        T.RandomResizedCrop(size, scale=(0.2, 1.0)),
        T.RandomHorizontalFlip(),
        T.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.4, hue=0.1),
        T.RandomGrayscale(p=0.2),
        T.GaussianBlur(kernel_size=size//10*2+1, sigma=(0.1, 2.0)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
```

## 现代化 PyTorch 中的 LeNet-5 原版

```python
class LeNet5Modern(nn.Module):
    """
    LeNet-5 (LeCun et al. 1998) 的现代化 PyTorch 复现。
    该架构于 1993 年在美国银行的生产环境中运行。
    约 60,000 个参数。与现代数十亿参数的模型遵循相同原理。
    """
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 6, kernel_size=5, padding=2),
            nn.Tanh(),
            nn.AvgPool2d(kernel_size=2, stride=2),
            nn.Conv2d(6, 16, kernel_size=5),
            nn.Tanh(),
            nn.AvgPool2d(kernel_size=2, stride=2),
            nn.Conv2d(16, 120, kernel_size=5),
            nn.Tanh(),
        )
        self.classifier = nn.Sequential(
            nn.Linear(120, 84),
            nn.Tanh(),
            nn.Linear(84, num_classes),
        )

    def forward(self, x):
        x = self.features(x)    # [B, 120, 1, 1]
        x = x.view(x.size(0), -1)
        return self.classifier(x)
```

---

## 基础论文（LeCun）

- LeCun et al. (1998). "Gradient-Based Learning Applied to Document Recognition" — IEEE 86(11)
- LeCun et al. (2015). "Deep Learning" — Nature 521:436-444
- LeCun (2022). "A Path Towards Autonomous Machine Intelligence" — OpenReview preprint

## JEPA 论文

- Assran et al. (2023). "Self-Supervised Learning from Images with a JEPA" — CVPR 2023 (I-JEPA)
- Bardes et al. (2024). "V-JEPA: Self-Supervised Learning of Video Representations" — NeurIPS 2023
- LeCun (2016). "Predictive Learning" — NIPS Keynote（蛋糕类比）

## SSL 相关论文

- He et al. (2022). "Masked Autoencoders Are Scalable Vision Learners" — CVPR 2022
- Chen et al. (2020). "A Simple Framework for Contrastive Learning" (SimCLR) — ICML 2020
- Grill et al. (2020). "Bootstrap Your Own Latent" (BYOL) — NeurIPS 2020

## 基于能量的模型

- LeCun et al. (2006). "A Tutorial on Energy-Based Learning" — ICLR Workshop
- LeCun (2021). "Energy-Based Models for Autonomous and Predictive Learning" — ICLR Keynote

## 最佳实践

- 提供关于项目与需求的清晰、具体上下文
- 在将建议应用于生产代码前先审阅所有建议
- 与其他互补技能结合以进行全面分析

## 常见陷阱

- 将本技能用于其领域专长之外的任务
- 在不理解具体上下文的情况下应用建议
- 未提供足够的项目上下文以进行准确分析

## 相关技能

- `yann-lecun` - 互补技能，可增强分析
- `yann-lecun-debate` - 互补技能，可增强分析
- `yann-lecun-filosofia` - 互补技能，可增强分析

## 局限性
- 仅当任务明确匹配上述范围时才使用本技能。
- 请勿将输出视为环境特定验证、测试或专家评审的替代品。
- 如缺少必需的输入、权限、安全边界或成功标准，请停止并寻求澄清。
