# React 最佳实践

一个用于创建和维护针对 agent 和 LLM 优化的 React 最佳实践的结构化仓库。

## 结构

- `rules/` - 独立的规则文件（每个规则一个文件）
  - `_sections.md` - 章节元数据（标题、影响、描述）
  - `_template.md` - 创建新规则的模板
  - `area-description.md` - 独立规则文件
- `src/` - 构建脚本和工具
- `metadata.json` - 文档元数据（版本、组织、摘要）
- __`AGENTS.md`__ - 编译输出（生成）
- __`test-cases.json`__ - 用于 LLM 评估的测试用例（生成）

## 快速开始

1. 安装依赖：
   ```bash
   pnpm install
   ```

2. 从规则构建 AGENTS.md：
   ```bash
   pnpm build
   ```

3. 验证规则文件：
   ```bash
   pnpm validate
   ```

4. 提取测试用例：
   ```bash
   pnpm extract-tests
   ```

## 创建新规则

1. 将 `rules/_template.md` 复制为 `rules/area-description.md`
2. 选择合适的区域前缀：
   - `async-` 用于消除瀑布流（第1节）
   - `bundle-` 用于包体积优化（第2节）
   - `server-` 用于服务端性能（第3节）
   - `client-` 用于客户端数据获取（第4节）
   - `rerender-` 用于重渲染优化（第5节）
   - `rendering-` 用于渲染性能（第6节）
   - `js-` 用于 JavaScript 性能（第7节）
   - `advanced-` 用于高级模式（第8节）
3. 填写 frontmatter 和内容
4. 确保有清晰的示例和解释
5. 运行 `pnpm build` 重新生成 AGENTS.md 和 test-cases.json

## 规则文件结构

每个规则文件应遵循以下结构：

```markdown
---
title: Rule Title Here
impact: MEDIUM
impactDescription: Optional description
tags: tag1, tag2, tag3
---

## Rule Title Here

Brief explanation of the rule and why it matters.

**Incorrect (description of what's wrong):**

```typescript
// Bad code example
```

**Correct (description of what's right):**

```typescript
// Good code example
```

Optional explanatory text after examples.

Reference: [Link](https://example.com)

## 文件命名规范

- 以 `_` 开头的文件是特殊的（从构建中排除）
- 规则文件：`area-description.md`（例如 `async-parallel.md`）
- 章节从文件名前缀自动推断
- 规则在每个章节内按标题字母顺序排序
- ID（例如 1.1、1.2）在构建时自动生成

## 影响级别

- `CRITICAL` - 最高优先级，主要性能提升
- `HIGH` - 显著的性能改进
- `MEDIUM-HIGH` - 中等偏高的收益
- `MEDIUM` - 中等性能改进
- `LOW-MEDIUM` - 中低收益
- `LOW` - 渐进式改进

## 脚本

- `pnpm build` - 将规则编译为 AGENTS.md
- `pnpm validate` - 验证所有规则文件
- `pnpm extract-tests` - 提取用于 LLM 评估的测试用例
- `pnpm dev` - 构建并验证

## 贡献指南

添加或修改规则时：

1. 为你的章节使用正确的文件名前缀
2. 遵循 `_template.md` 结构
3. 包含清晰的错误/正确示例及解释
4. 添加适当的标签
5. 运行 `pnpm build` 重新生成 AGENTS.md 和 test-cases.json
6. 规则按标题自动排序——无需管理编号！

## 致谢

由 [@shuding](https://x.com/shuding) 在 [Vercel](https://vercel.com) 最初创建。
