---
name: recursive-context-pruning-token-budgeting
description: "通过剪枝冗余上下文、管理 token 用量并强制执行极简洁、直击价值的响应，优化 AI 智能体性能。"
category: prompt-engineering
risk: safe
source: self
source_repo: Kench001/antigravity-awesome-skills
source_type: self
date_added: "2026-05-03"
author: Kench001
tags: [efficiency, token-optimization, brevity, context-management]
tools: [claude, cursor, gemini]
# Optional: declare the upstream license if source_repo is set
# license: "MIT"
# license_source: "https://github.com/owner/repo/blob/main/LICENSE"
---

# 递归上下文剪枝与 Token 预算管理

## 概述

本技能实现了一套"守门人"逻辑，用于防止上下文窗口膨胀和不必要的 token 消耗。它确保智能体仅处理相关的数据分片，并遵循原子精度协议——以零对话填充交付功能性答案。通过递归汇总状态并剥离"过渡短语"，它最大化了长时间运行的开发工作流的持久性和速度。

## 何时使用本技能

- 构建多步骤智能体时使用，以防止长对话中的重复和"记忆漂移"。
- 处理大型文档集或代码库时使用，避免将整个文件倾倒进提示中。
- 需要纯功能性输出（代码/逻辑）而不带"当然！这是你的……"之类开头时使用。

## 工作原理

### 步骤 1：元数据分片

扫描可用数据中的标题、摘要和关键指标。创建上下文的"地图"而非注入完整源文件。除非请求特定的窄片段，否则绝不要将整个文件拉入提示。

### 步骤 2：Token 预算分配

基于当前上下文窗口计算"安全响应限制"。将 30% 分配给当前逻辑处理，20% 分配给即时输出，50% 分配给未来上下文缓冲区。

### 步骤 3：原子输出过滤

剥离所有"过渡短语"（例如"我已更新了代码"、"根据你的请求"、"当然"）。响应直接以解决方案或代码块开始。

### 步骤 4：歧义检查

在执行步骤 3 之前，扫描是否缺少关键变量（例如特定文件名或环境类型）。如果提示过于模糊，跳过原子输出，精确生成一个简洁问题来解决阻塞。

### 步骤 5：抽象压缩

将当前轮次摘要为一个"压缩状态字符串"（例如 `[Project: Feasify | State: Auth-Fixed | Remaining-Tasks: 2]`），在下一轮提示前丢弃冗余对话数据。

## 示例

### 示例 1：过滤后的代码输出（无填充）

```text
User: "Update the Firebase config to use environment variables."
```

```javascript
const firebaseConfig = {
  apiKey: process.env.VITE_FIREBASE_API_KEY,
  authDomain: process.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.VITE_FIREBASE_PROJECT_ID
};
```

### 示例 2：必要澄清

```text
User: "Deploy the function."
```

```text
"Specify environment: production or staging?"
```

## 最佳实践

- ✅ **直接开始：** 将代码或答案放在响应的第一个字符处。
- ✅ **边走边总结：** 将 10 页讨论压缩为 5 个要点供下一轮使用。
- ✅ **省略签名：** 永远不要以"如果需要更多帮助请告诉我"结尾。
- ❌ **不要过渡短语：** 避免"这是代码"、"当然"或"我可以帮忙"。
- ❌ **不要猜测：** 如果缺少输入，立即提问，而非浪费 token 进行泛泛猜测。

## 局限性

- 本技能不替代环境特定的验证、测试或专家审查。
- 极端简洁有时可能隐藏重要细节；对关键注释使用简洁的行内注释（`// crucial step`）。

## 安全与注意事项

- 在压缩阶段，绝不要剪枝安全头、环境特定的安全约束或系统级指令。
- 将原始系统指令保持在上下文的"根"位置，以防止基于上下文丢失的越狱攻击。

## 常见陷阱

- **问题：** 响应过于简短，缺少实现所需的上下文。
  **解决方案：** 使用简洁的行内代码注释，而非单独的段落文字。

- **问题：** 智能体因过度压缩而丢失总体目标。
  **解决方案：** 始终将"主要目标"固定在每个剪枝后提示的顶部。

## 相关技能

- `@atomic-precision-response` - 专用于移除对话填充。
- `@context-sharding` - 用于管理大规模文档映射。
