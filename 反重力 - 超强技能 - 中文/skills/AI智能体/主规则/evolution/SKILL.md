---
name: evolution
description: "使 makepad-skills 在开发过程中持续自我改进。触发词：自我进化、技能进化、持续改进、自动改进、技能更新、钩子触发、自校正、自验证、版本适配"
risk: critical
source: community
---

<!-- security-allowlist: curl-pipe-bash -->

# Makepad Skills 进化系统

本技能使 makepad-skills 能够在开发过程中持续自我改进。

## 何时使用

- 你正在维护 `makepad-skills`，希望技能库在开发过程中自我改进
- 你需要确定何时将新模式转化为技能更新或钩子驱动的进化
- 你正在进行技能集的自校正、自验证或版本适配

## 快速导航

| 主题 | 描述 |
|------|------|
| 协作指南 | **贡献到 makepad-skills** |
| [钩子设置](#hooks-based-auto-triggering) | 使用钩子自动触发进化 |
| [何时进化](#when-to-evolve) | 触发条件和分类 |
| [进化流程](#evolution-process) | 分步指南 |
| [自校正](#self-correction) | 自动修复技能错误 |
| [自验证](#self-validation) | 验证技能准确性 |
| [版本适配](#version-adaptation) | 多分支支持 |

---

## 基于钩子的自动触发

为实现可靠的自动触发，请使用 Claude Code 钩子。使用 `--with-hooks` 安装：

```bash
# 安装 makepad-skills 并启用钩子
curl -fsSL https://raw.githubusercontent.com/ZhangHanDong/makepad-skills/main/install.sh | bash -s -- --with-hooks
```

这将把钩子安装到 `.claude/hooks/` 并配置 `.claude/settings.json`：

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/makepad-skill-router.sh"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/pre-tool.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/post-bash.sh"
          }
        ]
      }
    ]
  }
}
```

### 钩子功能

| 钩子 | 触发事件 | 动作 |
|------|----------|------|
| `makepad-skill-router.sh` | UserPromptSubmit | 自动路由到相关技能 |
| `pre-tool.sh` | Bash/Write/Edit 之前 | 从 Cargo.toml 检测 Makepad 版本 |
| `post-bash.sh` | Bash 命令失败后 | 检测 Makepad 错误，建议修复 |
| `session-end.sh` | 会话结束 | 提示捕获学习内容 |

---

## 技能路由与打包

`makepad-skill-router.sh` 钩子根据用户查询自动加载相关技能。

### 上下文检测

| 上下文 | 触发关键词 | 加载的技能 |
|--------|------------|------------|
| **完整应用** | "build app", "从零", "完整应用" | basics, dsl, layout, widgets, event-action, app-architecture |
| **UI 设计** | "ui design", "界面设计" | dsl, layout, widgets, animation, shaders |
| **组件创建** | "create widget", "创建组件", "自定义组件" | widgets, dsl, layout, animation, shaders, font, event-action |
| **生产环境** | "best practice", "robrix pattern", "实际项目" | app-architecture, widget-patterns, state-management, event-action |

### 技能依赖关系

加载某些技能时，相关技能会自动加载：

| 主技能 | 自动加载 |
|--------|----------|
| robius-app-architecture | makepad-basics, makepad-event-action |
| robius-widget-patterns | makepad-widgets, makepad-layout |
| makepad-widgets | makepad-layout, makepad-dsl |
| makepad-animation | makepad-shaders |
| makepad-shaders | makepad-widgets |
| makepad-font | makepad-widgets |
| robius-event-action | makepad-event-action |

### 示例

```
User: "我想从零开发一个 Makepad 应用"

[makepad-skills] 检测到 Makepad/Robius 查询
[makepad-skills] 检测到应用开发上下文 - 加载技能包
[makepad-skills] 路由到: makepad-basics makepad-dsl makepad-event-action
                            makepad-layout makepad-widgets robius-app-architecture
```

---

## 何时进化

当开发过程中发生以下情况时，触发技能进化：

| 触发条件 | 目标技能 | 优先级 |
|----------|----------|--------|
| 发现新的组件模式 | robius-widget-patterns/_base | 高 |
| 学到着色器技术 | makepad-shaders | 高 |
| 解决编译错误 | makepad-reference/troubleshooting | 高 |
| 找到布局解决方案 | makepad-reference/adaptive-layout | 中 |
| 解决构建/打包问题 | makepad-deployment | 中 |
| 获得项目结构洞察 | makepad-basics | 低 |
| 澄清核心概念 | makepad-dsl/makepad-widgets | 低 |

---

## 进化流程

### 步骤 1：识别值得捕获的知识

问自己：
- 这是一个可复用的模式吗？（非项目特定）
- 是否花费了大量精力才弄清楚？
- 是否对其他 Makepad 开发者有帮助？
- 是否尚未在 makepad-skills 中记录？

### 步骤 2：知识分类

```
组件/部件模式           → robius-widget-patterns/_base/
着色器/视觉效果         → makepad-shaders/
错误/调试解决方案       → makepad-reference/troubleshooting.md
布局/响应式设计         → makepad-reference/adaptive-layout.md
构建/部署问题           → makepad-deployment/SKILL.md
项目结构                → makepad-basics/
核心概念/API            → makepad-dsl/ 或 makepad-widgets/
```

### 步骤 3：格式化贡献

**模式格式**：
```markdown
## 模式 N：[模式名称]

简要描述此模式解决的问题。

### live_design!
```rust
live_design! {
    // DSL 代码
}
```

### Rust 实现
```rust
// Rust 代码
```
```

**故障排除格式**：
```markdown
### [错误类型/消息]

**症状**：开发者看到的现象

**原因**：为什么会发生

**解决方案**：
```rust
// 修复后的代码
```
```

### 步骤 4：标记进化（非版本）

在新内容上方添加进化标记：

```markdown
<!-- Evolution: 2024-01-15 | source: my-app | author: @zhangsan -->
```

### 步骤 5：通过 Git 提交

```bash
# 为你的贡献创建分支
git checkout -b evolution/add-loading-pattern

# 提交更改
git add robius-widget-patterns/_base/my-pattern.md
git commit -m "evolution: add loading state pattern from my-app"

# 推送并创建 PR
git push origin evolution/add-loading-pattern
```

---

## 自校正

当技能内容导致错误时，自动校正。

### 触发条件

```
用户遵循技能建议 → 代码编译/运行失败 → Claude 识别技能错误
                                          ↓
                                    自动：立即校正技能
```

### 校正流程

1. **检测** - 技能建议导致错误
2. **验证** - 确认技能内容错误
3. **校正** - 用修复更新技能文件

### 校正标记格式

```markdown
<!-- Correction: YYYY-MM-DD | was: [旧建议] | reason: [错误原因] -->
```

---

## 自验证

定期验证技能内容仍然准确。

### 验证检查清单

```markdown
## 验证报告

### 代码示例
- [ ] 所有 `live_design!` 示例正确解析
- [ ] 所有 Rust 代码可编译
- [ ] 所有模式按文档说明工作

### API 准确性
- [ ] 组件名称存在于 makepad-widgets
- [ ] 方法签名正确
- [ ] 事件类型准确
```

### 验证提示

> "请根据当前 Makepad 版本验证 makepad-skills"

---

## 版本适配

为不同的 Makepad 分支提供特定版本的指导。

### 支持的版本

| 分支 | 状态 | 说明 |
|------|------|------|
| main | 稳定 | 生产就绪 |
| dev | 活跃 | 最新功能，可能不稳定 |
| rik | 旧版 | 较旧的 API 风格 |

### 版本检测

Claude 应从以下位置检测 Makepad 版本：

1. **Cargo.toml 分支引用**：
   ```toml
   makepad-widgets = { git = "...", branch = "dev" }
   ```

2. **Cargo.lock 内容**

3. **不清楚时询问用户**

---

## 个性化

根据项目的编码风格调整技能建议。

### 风格检测

Claude 分析当前项目以检测：

| 方面 | 检测方法 | 适配方式 |
|------|----------|----------|
| 命名约定 | 扫描现有组件 | 匹配 snake_case 或 camelCase |
| 代码组织 | 检查模块结构 | 建议匹配的模式 |
| 注释风格 | 阅读现有注释 | 匹配文档风格 |
| 组件复杂度 | 统计每个组件的行数 | 建议适当的模式 |

---

## 质量指南

### 应添加
- 通用的、可复用的模式
- 常见错误及清晰的解决方案
- 经过充分测试的着色器效果
- 平台特定的注意事项
- 性能优化

### 不应添加
- 项目特定的代码
- 未验证的解决方案
- 重复内容
- 不完整的示例
- 没有理由的个人偏好

---

## 技能文件位置

```
skills/
├── # === 核心技能 (16) ===
├── makepad-basics/        ← 入门、应用结构
├── makepad-dsl/           ← DSL 语法、继承
├── makepad-layout/        ← 布局、尺寸、对齐
├── makepad-widgets/       ← 组件部件
├── makepad-event-action/  ← 事件处理
├── makepad-animation/     ← 动画、状态
├── makepad-shaders/       ← 着色器基础
├── makepad-platform/      ← 平台支持
├── makepad-font/          ← 字体、排版
├── makepad-splash/        ← 启动画面脚本
├── robius-app-architecture/   ← 应用架构模式
├── robius-widget-patterns/    ← 组件复用模式
├── robius-event-action/       ← 自定义动作
├── robius-state-management/   ← 状态持久化
├── robius-matrix-integration/ ← Matrix SDK
├── molykit/               ← AI 聊天工具包
│
├── # === 扩展技能 (3) ===
├── makepad-shaders/ ← 高级着色器、SDF
│   ├── _base/             ← 官方模式
│   └── community/         ← 社区贡献
├── makepad-deployment/    ← 构建与打包
├── makepad-reference/     ← 故障排除、代码质量
│
├── # 注意：生产模式已整合到 robius-* 技能：
├── # - 组件模式 → robius-widget-patterns/_base/
├── # - 状态模式 → robius-state-management/_base/
├── # - 异步模式 → robius-app-architecture/_base/
│
└── evolution/             ← 自进化系统
    ├── hooks/             ← 自动触发钩子
    ├── references/        ← 详细指南
    └── templates/         ← 贡献模板
```

---

## 自动进化提示词

使用这些提示词触发自我进化：

### 解决问题后
> "这个解决方案应该添加到 makepad-skills 以供将来参考。"

### 创建组件后
> "这个组件模式是可复用的。让我把它添加到 makepad-patterns。"

### 调试后
> "这个错误及其修复应该记录在 makepad-troubleshooting 中。"

### 完成功能后
> "回顾我学到的内容，如果适用则更新 makepad-skills。"

---

## 持续改进检查清单

每次 Makepad 开发会话后，请考虑：

- [ ] 我是否发现了新的组件组合模式？
- [ ] 我是否解决了棘手的着色器问题？
- [ ] 我是否遇到并修复了令人困惑的错误？
- [ ] 我是否找到了更好的布局结构方式？
- [ ] 我是否学到了关于打包/部署的知识？
- [ ] 这些内容是否对其他 Makepad 开发者有帮助？

如果以上任何一项为是，请进化相应的技能！

## 参考资料

- [makepad-skills 仓库](https://github.com/ZhangHanDong/makepad-skills)
- [Makepad 文档](https://github.com/makepad/makepad)
- [Project Robius](https://github.com/project-robius)

## 限制

- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
