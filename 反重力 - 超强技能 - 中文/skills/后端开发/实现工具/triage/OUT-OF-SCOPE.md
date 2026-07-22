# 范围外知识库

仓库中的 `.out-of-scope/` 目录用于持久记录被拒绝的功能请求。它有两个用途：

1. **制度记忆** — 记录某项功能被拒绝的原因，避免在 Issue 关闭后遗失判断依据
2. **去重** — 当新 Issue 与此前的拒绝相吻合时，技能可呈现该历史决策，从而避免重新讨论同一议题

## 目录结构

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

每个**概念**对应一个文件，而非每个 Issue 一个文件。多个请求同一事物的 Issue 会被归入同一文件下。

## 文件格式

文件应以较为宽松、可读的风格撰写 —— 更像一篇简短的设计文档，而非数据库条目。使用段落、代码示例和示例，让推理清晰可用，便于初次接触此文档的读者理解。

```markdown
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

The rendering pipeline assumes a single color palette defined in
`ThemeConfig`. Supporting multiple themes would require:

- A theme context provider wrapping the entire component tree
- Per-component theme-aware style resolution
- A persistence layer for user theme preferences

This is a significant architectural change that doesn't align with the
project's focus on content authoring. Theming is a concern for downstream
consumers who embed or redistribute the output.

```ts
// 当前 ThemeConfig 接口并未为运行时切换而设计：
interface ThemeConfig {
  colors: ColorPalette; // 单一调色板，在构建期解析
  fonts: FontStack;
}
```

## Prior requests

- #42 — "Add dark mode support"
- #87 — "Night theme for accessibility"
- #134 — "Dark theme option"
```

### 命名约定

使用简短、具有描述性的 kebab-case 名称来表达概念：`dark-mode.md`、`plugin-system.md`、`graphql-api.md`。名称应足够清晰，使浏览目录的人无需打开文件即可理解被拒绝的内容。

### 撰写理由

理由应当具体 —— 不是“我们不想要这个”，而是“为什么不”。好的理由会涉及：

- 项目范围或理念（“本项目聚焦 X，主题化是下游关切”）
- 技术约束（“支持此能力需要 Y，与我们的 Z 架构相冲突”）
- 战略决策（“我们选择使用 A 而非 B，因为……”）

理由应具有持久性。避免引用临时性情境（“我们现在太忙了”） —— 这并非真正的拒绝，只是延期。

## 何时检查 `.out-of-scope/`

在分流过程中（第 1 步：收集上下文），阅读 `.out-of-scope/` 中的所有文件。在评估新 Issue 时：

- 检查请求是否与现有“范围外”概念匹配
- 匹配是基于概念相似性而非关键词 —— “night theme” 与 `dark-mode.md` 相符
- 若有匹配，主动呈现给维护者：“此请求与 `.out-of-scope/dark-mode.md` 类似 —— 我们先前因 [理由] 拒绝了该方向。你现在的看法是否一致？”

维护者可以：

- **确认** — 新 Issue 被添加到现有文件的“既往请求”列表，然后关闭
- **重新考虑** — 删除或更新该“范围外”文件，Issue 进入正常分流
- **不同意** — 二者相关但不同，进入正常分流

## 何时写入 `.out-of-scope/`

仅当一项 **enhancement**（而非 bug）被作为 `wontfix` *拒绝* 时。该规则对 enhancement 形式的 PR 同样适用 —— 被拒绝的 PR 也记录在此处，使相同请求不会以全新代码的形式再次出现。

不要在此记录因**已经实现**而关闭为 `wontfix` 的情况。那是一个已构建的特性，而非被拒绝的特性；将其记录会污染去重检查、产生错误的拒绝标记。相应地，关闭评论应指向该功能已存在的实际位置。

流程为：

1. 维护者决定将某项功能请求判定为范围外
2. 检查是否存在匹配的 `.out-of-scope/` 文件
3. 若存在：将新 Issue 追加到“既往请求”列表
4. 若不存在：以概念名新建文件，包含决策、理由与第一条既往请求
5. 在 Issue 上发布评论，解释决策并提及 `.out-of-scope/` 文件
6. 给 Issue 打上 `wontfix` 标签并关闭

## 更新或删除范围外文件

若维护者改变了此前被拒绝概念的看法：

- 删除该 `.out-of-scope/` 文件
- 技能无需重新打开旧 Issue —— 它们是历史记录
- 触发重新评估的新 Issue 继续按正常分流流程推进
