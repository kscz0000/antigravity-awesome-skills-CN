---
name: git-pr-workflows-git-workflow
description: "编排从代码审查到 PR 创建的完整 git 工作流，利用专业智能体进行质量保证、测试和部署就绪检查。当用户要求'git工作流'、'PR创建'、'代码审查流程'或'多智能体编排git操作'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 完整 Git 工作流与多智能体编排

编排从代码审查到 PR 创建的完整 git 工作流，利用专业智能体进行质量保证、测试和部署就绪检查。本工作流实现了现代 git 最佳实践，包括 Conventional Commits、自动化测试和结构化 PR 创建。

[扩展思考：本工作流协调多个专业智能体，确保代码在提交前通过质量检查。code-reviewer 智能体执行初始质量检查，test-automator 确保所有测试通过，deployment-engineer 验证生产就绪状态。通过顺序编排这些智能体并传递上下文，我们在保持高效率的同时防止有问题的代码进入仓库。工作流支持 trunk-based 和 feature-branch 两种策略，具有可配置选项以适应不同团队需求。]

## 使用本技能的时机

- 处理涉及多智能体编排的完整 git 工作流任务或工作流
- 需要完整 git 工作流与多智能体编排的指导、最佳实践或检查清单

## 不使用本技能的时机

- 任务与完整 git 工作流及多智能体编排无关
- 需要此范围之外的其他领域或工具

## 指令

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 配置

**目标分支**: $ARGUMENTS（如未指定则默认为 'main'）

**支持的标志**:
- --skip-tests: 跳过自动化测试执行（谨慎使用）
- --draft-pr: 将 PR 创建为草稿，用于进行中的工作
- --no-push: 执行所有检查但不推送到远程
- --squash: 推送前压缩提交
- --conventional: 严格强制 Conventional Commits 格式
- --trunk-based: 使用 trunk-based 开发工作流
- --feature-branch: 使用 feature branch 工作流（默认）

## 阶段 1：提交前审查与分析

### 1. 代码质量评估
- 使用 Task 工具，subagent_type="code-reviewer"
- 提示词："审查所有未提交的更改以发现代码质量问题。检查：1) 代码风格违规，2) 安全漏洞，3) 性能问题，4) 缺失的错误处理，5) 不完整的实现。生成包含严重程度级别（critical/high/medium/low）的详细报告，并提供具体的逐行反馈。输出格式：JSON，结构为 {issues: [], summary: {critical: 0, high: 0, medium: 0, low: 0}, recommendations: []}"
- 预期输出：结构化代码审查报告，供下一阶段使用

### 2. 依赖与破坏性变更分析
- 使用 Task 工具，subagent_type="code-reviewer"
- 提示词："分析更改中的：1) 新依赖或版本变更，2) 破坏性 API 变更，3) 数据库模式修改，4) 配置变更，5) 向后兼容性问题。来自上一审查的上下文：[插入问题摘要]。识别任何需要迁移脚本或文档更新的变更。"
- 来自上一阶段的上下文：可能表明破坏性变更的代码质量问题
- 预期输出：破坏性变更评估和迁移需求

## 阶段 2：测试与验证

### 1. 测试执行与覆盖率
- 使用 Task 工具，subagent_type="unit-testing::test-automator"
- 提示词："为修改的代码执行所有测试套件。运行：1) 单元测试，2) 集成测试，3) 端到端测试（如适用）。生成覆盖率报告并识别任何未测试的代码路径。基于审查问题：[插入 critical/high 问题]，确保测试覆盖问题区域。提供测试结果，格式为：{passed: [], failed: [], skipped: [], coverage: {statements: %, branches: %, functions: %, lines: %}, untested_critical_paths: []}"
- 来自上一阶段的上下文：需要测试覆盖的关键代码审查问题
- 预期输出：完整测试结果和覆盖率指标

### 2. 测试建议与缺口分析
- 使用 Task 工具，subagent_type="unit-testing::test-automator"
- 提示词："基于测试结果 [插入摘要] 和代码更改，识别：1) 缺失的测试场景，2) 未覆盖的边界情况，3) 需要验证的集成点，4) 需要的性能基准。按风险优先级生成测试实现建议。考虑已识别的破坏性变更：[插入破坏性变更]。"
- 来自上一阶段的上下文：测试结果、破坏性变更、未测试路径
- 预期输出：按优先级排序的额外测试需求列表

## 阶段 3：提交信息生成

### 1. 变更分析与分类
- 使用 Task 工具，subagent_type="code-reviewer"
- 提示词："分析所有更改并根据 Conventional Commits 规范进行分类。识别主要变更类型（feat/fix/docs/style/refactor/perf/test/build/ci/chore/revert）和范围。对于更改：[插入文件列表和摘要]，确定这应该是单个提交还是多个原子提交。考虑测试结果：[插入测试摘要]。"
- 来自上一阶段的上下文：测试结果、代码审查摘要
- 预期输出：提交结构建议

### 2. Conventional Commit 信息创建
- 使用 Task 工具，subagent_type="llm-application-dev::prompt-engineer"
- 提示词："基于分类创建 Conventional Commits 格式的信息：[插入分类]。格式：<type>(<scope>): <subject>，空行后是 <body> 解释做了什么和为什么（不是怎么做），然后是 <footer>，如有破坏性变更则包含 BREAKING CHANGE:。包括：1) 清晰的主题行（最多 50 字符），2) 详细正文解释原因，3) 问题/工单引用，4) 共同作者（如适用）。考虑影响：[插入破坏性变更（如有）]。"
- 来自上一阶段的上下文：变更分类、破坏性变更
- 预期输出：格式正确的提交信息

## 阶段 4：分支策略与推送准备

### 1. 分支管理
- 使用 Task 工具，subagent_type="cicd-automation::deployment-engineer"
- 提示词："基于工作流类型 [--trunk-based 或 --feature-branch]，准备分支策略。对于 feature branch：确保分支名称遵循模式 (feature|bugfix|hotfix)/<ticket>-<description>。对于 trunk-based：准备直接推送到 main，如需要则准备 feature flag 策略。当前分支：[插入分支]，目标：[插入目标分支]。验证与目标分支无冲突。"
- 预期输出：分支准备命令和冲突状态

### 2. 推送前验证
- 使用 Task 工具，subagent_type="cicd-automation::deployment-engineer"
- 提示词："执行最终推送前检查：1) 验证所有 CI 检查将通过，2) 确认提交中无敏感数据，3) 如需要则验证提交签名，4) 检查分支保护规则，5) 确保所有审查意见已处理。测试摘要：[插入测试结果]。审查状态：[插入审查摘要]。"
- 来自上一阶段的上下文：所有之前的验证结果
- 预期输出：推送就绪确认或阻塞问题

## 阶段 5：Pull Request 创建

### 1. PR 描述生成
- 使用 Task 工具，subagent_type="documentation-generation::docs-architect"
- 提示词："创建全面的 PR 描述，包括：1) 变更摘要（做了什么和为什么），2) 变更类型检查清单，3) 来自 [插入测试结果] 的测试执行摘要，4) 如有 UI 变更则提供截图/录制，5) 来自 [插入部署注意事项] 的部署说明，6) 相关问题/工单，7) 破坏性变更部分（如适用）：[插入破坏性变更]，8) 审查者检查清单。格式为 GitHub 风格 Markdown。"
- 来自上一阶段的上下文：所有验证结果、测试结果、破坏性变更
- 预期输出：完整的 Markdown 格式 PR 描述

### 2. PR 元数据与自动化设置
- 使用 Task 工具，subagent_type="cicd-automation::deployment-engineer"
- 提示词："配置 PR 元数据：1) 根据 CODEOWNERS 分配合适的审查者，2) 添加标签（type、priority、component），3) 关联相关问题，4) 如适用则设置里程碑，5) 配置合并策略（squash/merge/rebase），6) 如所有检查通过则设置自动合并。考虑草稿状态：[--draft-pr 标志]。包含测试状态：[插入测试摘要]。"
- 来自上一阶段的上下文：PR 描述、测试结果、审查状态
- 预期输出：PR 配置命令和自动化规则

## 成功标准

- ✅ 所有关键和高严重程度代码问题已解决
- ✅ 测试覆盖率保持或提升（目标：>80%）
- ✅ 所有测试通过（单元、集成、端到端）
- ✅ 提交信息遵循 Conventional Commits 格式
- ✅ 与目标分支无合并冲突
- ✅ PR 描述完整，包含所有必需部分
- ✅ 分支保护规则已满足
- ✅ 安全扫描完成，无关键漏洞
- ✅ 性能基准在可接受阈值内
- ✅ 文档已更新以反映任何 API 变更

## 回滚流程

合并后如出现问题：

1. **立即回退**：使用 git revert <commit-hash> 创建回退 PR
2. **Feature Flag 禁用**：如使用 feature flag，立即禁用
3. **Hotfix 分支**：对于关键问题，从 main 创建 hotfix 分支
4. **沟通**：通过指定渠道通知团队
5. **根因分析**：使用 postmortem 模板记录问题

## 最佳实践参考

- **提交频率**：尽早且频繁提交，但确保每个提交是原子的
- **分支命名**：(feature|bugfix|hotfix|docs|chore)/<ticket-id>-<brief-description>
- **PR 大小**：保持 PR 在 400 行以内以便有效审查
- **审查响应**：在 24 小时内处理审查意见
- **合并策略**：feature branch 使用 squash，release branch 使用 merge
- **签署**：main 分支变更要求至少 2 个批准

## 局限性
- 仅当任务明确符合上述描述的范围时使用本技能。
- 不要将输出替代环境特定的验证、测试或专家审查。
- 如缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
