---
description: 何时使用 Tier 2（扩展）技能架构。触发词：Tier 2、扩展技能、多文件
metadata:
  tags: [tier-2, expanded, multi-file]
---

# Tier 2：扩展技能

用于具有多个子概念的复杂主题的多文件技能。

## 何时使用

- **多个相关概念**：需要关注点分离
- **总共 200-1000 行**：对于一个文件来说太大
- **需要参考文件**：模式、示例、故障排除
- **交叉链接**：用户需要在子主题之间导航

## 结构

```
my-skill/
├── SKILL.md              # 概览 + 导航
└── references/
    ├── core/
    │   ├── README.md     # 主要概念
    │   └── api.md        # API 参考
    ├── patterns/
    │   └── README.md     # 使用模式
    └── troubleshooting/
        └── README.md     # 常见问题
```

## 示例

`writing-skills` 技能本身就是 Tier 2：

```
writing-skills/
├── SKILL.md              # 决策树 + 导航
├── gotchas.md            # 部落知识
└── references/
    ├── anti-rationalization/
    ├── cso/
    ├── standards/
    ├── templates/
    └── testing/
```

## 渐进披露

1. **元数据**（约 100 个 token）：启动时加载的名称 + 描述
2. **SKILL.md**（<500 行）：决策树 + 索引
3. **参考**（按需）：仅在用户导航时加载

## 与 Tier 1 的关键差异

| 方面 | Tier 1 | Tier 2 |
|--------|--------|--------|
| 文件数 | 1 | 5-20 |
| 总行数 | <200 | 200-1000 |
| 决策逻辑 | 无 | 简单树 |
| Token 成本 | 最小 | 中等（渐进） |

## 检查清单

- [ ] SKILL.md 有清晰的导航链接
- [ ] 每个 `references/` 子目录都有 README.md
- [ ] 文件之间没有循环引用
- [ ] 决策树指向特定文件
