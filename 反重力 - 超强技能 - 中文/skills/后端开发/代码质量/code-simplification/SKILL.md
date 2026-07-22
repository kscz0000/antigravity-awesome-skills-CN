---
name: code-simplification
description: 简化代码以提升可读性。在不改变行为的前提下重构代码时使用。当代码能跑但比应有的可读性、可维护性、可扩展性都差时使用。当审查已积累不必要复杂度的代码时使用。
risk: unknown
source: https://github.com/addyosmani/agent-skills/tree/main/skills/code-simplification
source_repo: addyosmani/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/addyosmani/agent-skills/blob/main/LICENSE
---

# 代码简化

> 灵感来自 [Claude Code Simplifier 插件](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-simplifier/agents/code-simplifier.md)。此处改造为模型无关、流程驱动的技能，适用于任何 AI 编码智能体。

## 概述

通过降低复杂度来简化代码，同时保持行为完全不变。目标不是更少的行数——而是让代码更易读、更易理解、更易修改、更易调试。每次简化都必须通过一个简单测试："新团队成员会比原来更快地理解这段代码吗？"

## 何时使用

- 功能已可运行且测试通过，但实现感觉比所需更繁重时
- 代码审查期间，可读性或复杂性问题被指出时
- 遇到深度嵌套的逻辑、过长的函数、或不清晰的命名时
- 重构在时间压力下写出的代码时
- 整合分散在多个文件中的相关逻辑时
- 合并引入了重复或不一致的改动后

**何时不要使用：**

- 代码已经干净、可读——不要为了简化而简化
- 你还不理解代码做了什么——先理解再简化
- 代码是性能关键的，"更简单"的版本会显著变慢
- 你打算完全重写模块——简化一次性代码是浪费精力

## 五项原则

### 1. 完全保持行为不变

不要改变代码做什么——只改变它如何表达。所有输入、输出、副作用、错误行为和边界情况都必须保持一致。如果你不确定简化是否保持了行为，就不要做。

```
每次改动前自问：
→ 对每个输入是否产生相同的输出？
→ 是否保持相同的错误行为？
→ 是否保留了相同的副作用和顺序？
→ 所有现有测试是否在不做修改的情况下通过？
```

### 2. 遵循项目约定

简化意味着让代码与代码库更一致，而不是强加外部偏好。简化之前：

```
1. 读取 CLAUDE.md / 项目约定
2. 研究相邻代码如何处理类似模式
3. 匹配项目的风格：
   - 导入顺序与模块系统
   - 函数声明风格
   - 命名约定
   - 错误处理模式
   - 类型注解深度
```

破坏项目一致性的简化不是简化——是制造混乱。

### 3. 清晰优先于取巧

当紧凑版本需要大脑暂停一下才能解析时，显式代码优于紧凑代码。

```typescript
// UNCLEAR: Dense ternary chain
const label = isNew ? 'New' : isUpdated ? 'Updated' : isArchived ? 'Archived' : 'Active';

// CLEAR: Readable mapping
function getStatusLabel(item: Item): string {
  if (item.isNew) return 'New';
  if (item.isUpdated) return 'Updated';
  if (item.isArchived) return 'Archived';
  return 'Active';
}
```

```typescript
// UNCLEAR: Chained reduces with inline logic
const result = items.reduce((acc, item) => ({
  ...acc,
  [item.id]: { ...acc[item.id], count: (acc[item.id]?.count ?? 0) + 1 }
}), {});

// CLEAR: Named intermediate step
const countById = new Map<string, number>();
for (const item of items) {
  countById.set(item.id, (countById.get(item.id) ?? 0) + 1);
}
```

### 4. 保持平衡

简化有一个失败模式：过度简化。警惕这些陷阱：

- **过度内联** — 移除了为概念命名的辅助函数，使调用处更难读
- **合并无关逻辑** — 把两个简单函数合并成一个复杂函数并不更简单
- **移除"不必要的"抽象** — 某些抽象的存在是为了可扩展性或可测试性，而不是为了复杂
- **为行数优化** — 行数更少不是目标；更易理解才是

### 5. 范围限定在改动处

默认简化最近修改过的代码。除非明确要求扩大范围，否则避免顺手重构无关代码。无范围的简化为 diff 引入噪音并带来意外回归的风险。

## 简化流程

### 第一步：理解先于动手（切斯特顿的篱笆）

在更改或移除任何东西之前，理解它为什么存在。这就是切斯特顿的篱笆：如果你在路上看到一道篱笆但不明白它为什么在那儿，不要拆掉它。先理解原因，再判断原因是否仍然适用。

```
简化前，回答：
- 这段代码的职责是什么？
- 谁调用它？它调用了什么？
- 边界情况和错误路径有哪些？
- 有定义预期行为的测试吗？
- 它当初为什么会写成这样？（性能？平台约束？历史原因？）
- 查看 git blame：这段代码的原始上下文是什么？
```

如果你回答不了这些，你还没准备好简化。先读更多上下文。

### 第二步：识别简化机会

扫描以下模式——每一个都是具体信号，而非模糊的"代码味"：

**结构复杂度：**

| 模式 | 信号 | 简化方法 |
|---------|--------|----------------|
| 深度嵌套（3 层及以上） | 控制流难以跟踪 | 将条件提取为守卫子句或辅助函数 |
| 长函数（50+ 行） | 职责过多 | 拆分为有描述性名称的专注函数 |
| 嵌套三元 | 需要心理栈来解析 | 替换为 if/else 链、switch 或查找对象 |
| 布尔参数标志 | `doThing(true, false, true)` | 替换为选项对象或独立函数 |
| 重复条件 | 多处出现相同的 `if` 检查 | 提取为命名良好的谓词函数 |

**命名与可读性：**

| 模式 | 信号 | 简化方法 |
|---------|--------|----------------|
| 通用名称 | `data`、`result`、`temp`、`val`、`item` | 重命名以描述内容：`userProfile`、`validationErrors` |
| 缩写名称 | `usr`、`cfg`、`btn`、`evt` | 使用完整单词，除非缩写是通用的（`id`、`url`、`api`） |
| 误导性命名 | 名为 `get` 的函数却修改了状态 | 重命名以反映实际行为 |
| 解释"是什么"的注释 | 在 `count++` 上方有 `// increment counter` | 删除注释——代码本身已经够清楚了 |
| 解释"为什么"的注释 | `// Retry because the API is flaky under load` | 保留这些——它们承载了代码无法表达的目的 |

**冗余：**

| 模式 | 信号 | 简化方法 |
|---------|--------|----------------|
| 重复逻辑 | 多处出现相同的 5+ 行 | 提取为共享函数 |
| 死代码 | 不可达分支、未使用变量、注释掉的代码块 | 删除（在确认确实是死代码之后） |
| 不必要的抽象 | 不增加价值的包装 | 内联包装，直接调用底层函数 |
| 过度工程的模式 | 工厂之上再造工厂、只有一种策略的策略模式 | 用简单直接的方式替换 |
| 冗余的类型断言 | 强制转换为已推断出的类型 | 删除断言 |

### 第三步：增量应用更改

一次做一个简化。每次改动后运行测试。**将重构改动与功能或缺陷修复改动分开提交。** 一个 PR 同时做重构和加新功能就是两个 PR——分开。

```
每个简化：
1. 做出改动
2. 运行测试套件
3. 如果测试通过 → 提交（或继续下一个简化）
4. 如果测试失败 → 回退并重新考虑
```

避免把多个简化合并到一个未经测试的改动中。如果出了问题，你需要知道是哪个简化导致的。

**500 规则：** 如果一次重构涉及超过 500 行，投入自动化（codemods、sed 脚本、AST 转换）而不是手工修改。这种规模的手工编辑容易出错且审查令人疲倦。

### 第四步：验证结果

完成所有简化后，退一步评估整体：

```
对比前后：
- 简化版本是否真的更容易理解？
- 是否引入了与代码库不一致的新模式？
- diff 是否干净、可审查？
- 同事会批准这个改动吗？
```

如果"简化"后的版本更难理解或更难审查，就回退。不是每次简化尝试都会成功。

## 语言特定指引

### TypeScript / JavaScript

```typescript
// SIMPLIFY: Unnecessary async wrapper
// Before
async function getUser(id: string): Promise<User> {
  return await userService.findById(id);
}
// After
function getUser(id: string): Promise<User> {
  return userService.findById(id);
}

// SIMPLIFY: Verbose conditional assignment
// Before
let displayName: string;
if (user.nickname) {
  displayName = user.nickname;
} else {
  displayName = user.fullName;
}
// After
const displayName = user.nickname || user.fullName;

// SIMPLIFY: Manual array building
// Before
const activeUsers: User[] = [];
for (const user of users) {
  if (user.isActive) {
    activeUsers.push(user);
  }
}
// After
const activeUsers = users.filter((user) => user.isActive);

// SIMPLIFY: Redundant boolean return
// Before
function isValid(input: string): boolean {
  if (input.length > 0 && input.length < 100) {
    return true;
  }
  return false;
}
// After
function isValid(input: string): boolean {
  return input.length > 0 && input.length < 100;
}
```

### Python

```python
# SIMPLIFY: Verbose dictionary building
# Before
result = {}
for item in items:
    result[item.id] = item.name
# After
result = {item.id: item.name for item in items}

# SIMPLIFY: Nested conditionals with early return
# Before
def process(data):
    if data is not None:
        if data.is_valid():
            if data.has_permission():
                return do_work(data)
            else:
                raise PermissionError("No permission")
        else:
            raise ValueError("Invalid data")
    else:
        raise TypeError("Data is None")
# After
def process(data):
    if data is None:
        raise TypeError("Data is None")
    if not data.is_valid():
        raise ValueError("Invalid data")
    if not data.has_permission():
        raise PermissionError("No permission")
    return do_work(data)
```

### React / JSX

```tsx
// SIMPLIFY: Verbose conditional rendering
// Before
function UserBadge({ user }: Props) {
  if (user.isAdmin) {
    return <Badge variant="admin">Admin</Badge>;
  } else {
    return <Badge variant="default">User</Badge>;
  }
}
// After
function UserBadge({ user }: Props) {
  const variant = user.isAdmin ? 'admin' : 'default';
  const label = user.isAdmin ? 'Admin' : 'User';
  return <Badge variant={variant}>{label}</Badge>;
}

// SIMPLIFY: Prop drilling through intermediate components
// Before — consider whether context or composition solves this better.
// This is a judgment call — flag it, don't auto-refactor.
```

## 常见的自我辩解

| 自我辩解 | 现实 |
|---|---|
| "它能跑，没必要动它" | 能跑但难读的代码，出问题时很难修复。现在简化能在未来每次改动时省时间。 |
| "行数更少总是更简单" | 1 行的嵌套三元并不比 5 行的 if/else 更简单。简单是指理解速度，不是行数。 |
| "我顺手快速简化一下无关代码" | 无范围的简化会制造混乱的 diff，并可能导致本不想改的代码出现回归。保持专注。 |
| "类型本身就自文档化" | 类型描述的是结构，不是意图。命名良好的函数比类型签名更好地解释*为什么*。 |
| "这个抽象将来可能有用" | 不要保留投机性的抽象。现在没用到，就是没有价值的复杂度。删掉，将来需要时再加。 |
| "原作者一定有他的理由" | 也许。看 git blame——应用切斯特顿的篱笆。但积累的复杂度往往没有理由，只是在压力下迭代的残留。 |
| "我加功能时顺便重构一下" | 把重构和功能工作分开。混在一起的改动更难审查、回退和从历史中理解。 |

## 危险信号

- 简化需要修改测试才能通过（你很可能改了行为）
- "简化"后的代码比原来更长、更难跟随
- 为了符合你自己的偏好而非项目约定而重命名
- 因为"让代码更干净"而移除错误处理
- 简化你还没有完全理解的代码
- 把许多简化合并成一个难以审查的大提交
- 在未被要求的情况下重构当前任务范围之外的代码

## 验证

完成一轮简化后：

- [ ] 所有现有测试在不做修改的情况下通过
- [ ] 构建成功，无新警告
- [ ] Linter/格式化器通过（无风格回归）
- [ ] 每个简化都是可审查的、增量式的改动
- [ ] diff 干净——没有混入无关改动
- [ ] 简化后的代码遵循项目约定（对照 CLAUDE.md 或同等文件核查）
- [ ] 没有错误处理被移除或削弱
- [ ] 没有遗留死代码（未使用的导入、不可达的分支）
- [ ] 同事或审查智能体会认为这是一项净改善并批准

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用更改之前，验证命令、生成的代码、依赖、凭据和外部服务行为。
- 不要把示例当作特定环境测试、安全审查或用户对破坏性/高成本操作的批准的替代。