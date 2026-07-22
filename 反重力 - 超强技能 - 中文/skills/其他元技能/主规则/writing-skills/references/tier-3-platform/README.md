---
description: 何时使用 Tier 3（平台）技能架构用于大型平台。触发词：Tier 3、平台技能、企业级、云服务
metadata:
  tags: [tier-3, platform, enterprise, cloudflare-pattern]
---

# Tier 3：平台技能

用于整个平台（AWS、Cloudflare、Convex 等）的企业级技能。

## 何时使用

- **整个平台**：10+ 产品/服务
- **总共 1000+ 行**：如果单体化将淹没上下文
- **复杂决策逻辑**：用户从"我需要 X"而非"我想要产品 Y"开始
- **未记录的陷阱**：部落知识至关重要

## Cloudflare 模式

基于 Dillon Mulroy 的 `cloudflare-skill`。

### 结构

```
my-platform/
├── SKILL.md                  # 仅包含决策树
└── references/
    └── <product>/
        ├── README.md         # 概览，何时使用
        ├── api.md            # 运行时 API 参考
        ├── configuration.md  # 配置选项
        ├── patterns.md       # 使用模式
        └── gotchas.md        # 陷阱和限制
```

### 5 文件模式

每个产品目录恰好有 5 个文件：

| 文件 | 用途 | 何时加载 |
|------|---------|--------------|
| `README.md` | 概览，何时使用 | 始终先加载 |
| `api.md` | 运行时 API、方法 | 实现功能时 |
| `configuration.md` | 配置、环境 | 设置时 |
| `patterns.md` | 常见工作流 | 最佳实践 |
| `gotchas.md` | 陷阱、限制 | 调试时 |

## 决策树

Tier 3 的强大之处在于帮助 AI **选择**的决策树：

```markdown
Need to store data?
├─ Simple key-value → kv/
├─ Relational queries → d1/
├─ Large files/blobs → r2/
├─ Per-user state → durable-objects/
└─ Vector embeddings → vectorize/
```

## 斜杠命令集成

创建斜杠命令进行编排：

```markdown
---
description: Load platform skill and get contextual guidance
---

## Workflow

1. Load skill: `skill({ name: 'my-platform' })`
2. Identify product from decision tree
3. Load relevant reference files based on task

| Task | Files |
|------|-------|
| New setup | README.md + configuration.md |
| Implement feature | api.md + patterns.md |
| Debug issue | gotchas.md |
```

## 渐进披露的实际应用

- **启动时**：仅名称 + 描述（约 100 个 token）
- **激活时**：带决策树的 SKILL.md（<5000 个 token）
- **导航时**：一个产品的 5 个文件（按需）

结果：60+ 产品参考而不会耗尽上下文。

## 检查清单

- [ ] SKILL.md 仅包含决策树 + 索引
- [ ] 每个产品恰好有 5 个文件
- [ ] 决策树涵盖所有"我需要 X"场景
- [ ] 交叉引用保持一层深
- [ ] 已创建斜杠命令进行编排
- [ ] 每个产品都有 `gotchas.md`
