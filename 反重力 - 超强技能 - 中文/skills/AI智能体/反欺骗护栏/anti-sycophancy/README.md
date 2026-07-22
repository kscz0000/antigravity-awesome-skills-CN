# 反迎合（Anti-Sycophancy）

一个面向 OpenCode 的技能，用于检测并消除 AI 回复中的迎合模式。所谓迎合，是指 AI 把附和用户已表达或隐含的信念置于认知诚实之上——这是 RLHF 的结构性产物，而非态度问题。

## 安装

```bash
mkdir -p ~/.config/opencode/skills
cp -r anti-sycophancy ~/.config/opencode/skills/
```

## 使用

当你希望智能体把"直接"放在优先位时，显式加载该技能：

```
/skill anti-sycophancy
```

加载后，智能体对每一次回复都执行程序化的反迎合流程：提取用户核心主张、独立评估、基于证据得出结论、并以"结论先行"的方式作答。

也可以在行内引用：

```
With the anti-sycophancy skill active, review this architecture:
```

## 覆盖的模式

### 认知迎合（你说什么）

| 编号 | 模式 | 捕捉的问题 |
|------|------|-----------|
| 1 | **答案迎合** | 附和用户的错误主张而不纠正 |
| 2 | **前提背书** | 在有缺陷的框架内作答，而不挑战该框架 |
| 3 | **模仿迎合** | 沿用用户的错误，跟着有缺陷的推理链条走 |
| 4 | **反馈迎合** | 被要求评审时给出可预期的偏向正面评价 |

### 软迎合（你怎么表达）

| 编号 | 模式 | 捕捉的问题 |
|------|------|-----------|
| 5 | **先安抚再纠正** | 在提出异议前加情绪铺垫（最常见形式） |
| 6 | **过度情感确认** | "好问题！"、夸张的感激、寒暄式的填充语 |
| 7 | **虚假赞同框架** | "你说得对，X 是这样，但是……"，而 X 其实并不对 |
| 8 | **软化异议** | 用"你或许还可以考虑……"取代"那样行不通" |
| 9 | **服从姿态** | 抬高用户权威以避免表态 |
| 10 | **被反驳后翻案** | 在没有新证据的情况下，因被质疑而改掉原本正确的答案 |

### 社交迎合（用户是谁）

| 编号 | 模式 | 捕捉的问题 |
|------|------|-----------|
| 11 | **身份服从** | 用户显露专业或权威信号时，附和变得更顺从 |
| 12 | **身份站队** | 立场向用户被感知到的身份倾斜 |
| 13 | **保全颜面的附和** | 即便有证据，也因顾忌社交摩擦而附和 |

## 工作原理

不靠模式匹配，而是对每一次回复施加同一套程序化纪律：

1. **提取**用户表述中的核心主张。剥离前提后陈述。
2. **独立评估**该主张——列出支持/反对的证据，不引用用户的认同或权威。
3. **得出结论**，仅依据第 2 步。
4. **回复**：先结论，后证据。

当用户提出异议时：
- 新证据 → 更新立场，说明发生了什么变化
- 重复的观点 → 附上证据重申立场

## 参考资料

- Sharma, M., Tong, M., Korbak, T., et al. (2023). Towards Understanding Sycophancy in Language Models. *ICLR 2024*. arXiv:2310.13548.
- Perez, E., et al. (2022). Discovering Language Model Behaviors with Model-Written Evaluations. *ACL 2023 Findings*.
- Dubois, M., Ududec, C., Summerfield, C., & Luettgau, L. (2026). Ask Don't Tell: Reducing Sycophancy in Large Language Models. arXiv:2602.23971.
- Gligorić, K., et al. (2026). SWAY: A Counterfactual Computational Linguistic Approach to Measuring and Mitigating Sycophancy. arXiv:2604.02423.
- Mohsin, M. A., et al. (2026). Pressure, What Pressure? Sycophancy Disentanglement via Reward Decomposition. arXiv:2604.05279.
- Feng, Z., et al. (2026). Good Arguments Against the People Pleasers: How Reasoning Mitigates (Yet Masks) LLM Sycophancy. arXiv:2603.16643.
- Cheng, M., Yu, S., Lee, C., Khadpe, P., Ibrahim, L., & Jurafsky, D. (2026). Social Sycophancy: A Broader Understanding of LLM Sycophancy. *Proc. ICLR 2026*. arXiv:2505.13995.
- Ibrahim, L., Hafner, F. S., & Rocher, L. (2026). Training Language Models to be Warm Can Reduce Accuracy and Increase Sycophancy. *Nature*, 652, 1159–1165. DOI: 10.1038/s41586-026-10410-0.
- Cheng, M., Lee, C., Khadpe, P., Yu, S., Han, D., & Jurafsky, D. (2026). Sycophantic AI Decreases Prosocial Intentions and Promotes Dependence. *Science*, 391(6792). DOI: 10.1126/science.aec8352.
- "The Silicon Mirror: Dynamic Behavioral Gating for Anti-Sycophancy" (ArXiv 2604.00478, 2026).

## 许可证

MIT