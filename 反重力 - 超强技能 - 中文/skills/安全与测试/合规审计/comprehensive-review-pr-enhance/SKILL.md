---
name: comprehensive-review-pr-enhance
description: >
  从 diff 生成结构化 PR 描述，并附加审查清单、风险评估与测试覆盖率摘要。用户要求“写 PR 描述”、“改进这个 PR”、“总结我的变更”、“PR 审查”、“pull request”或需要为审查者整理 diff 时使用。
risk: unknown
source: community
---

# Pull Request 增强

## 适用场景
- 需要把 git diff 转换为审查者友好的 PR 描述。
- 需要一份包含变更分类、风险说明、测试要点和检查清单的 PR 摘要。
- diff 规模较大，审查者需要结构化呈现，而不是临时简短总结。

## 工作流程

1. 运行 `git diff <base>...HEAD --stat`，识别变更文件和影响范围。
2. 梳理变更分类：源码、测试、配置、文档、构建、样式。
3. 使用下方模板生成 PR 描述。
4. 根据出现的文件类别，补充对应审查清单。
5. 显式标注破坏性变更、安全敏感文件或大型 diff（>500 行）。

## PR 描述模板

```markdown
## Summary
<!-- 一段话执行摘要：改了什么、为什么改 -->

## Changes
| Category | Files | Key change |
|----------|-------|------------|
| source   | `src/auth.ts` | added OAuth2 PKCE flow |
| test     | `tests/auth.test.ts` | covers token refresh edge case |
| config   | `.env.example` | new `OAUTH_CLIENT_ID` var |

## Why
<!-- 关联 issue/ticket + 一句话说明动机 -->

## Testing
- [ ] unit tests pass (`npm test`)
- [ ] manual smoke test on staging
- [ ] no coverage regression

## Risks & Rollback
- **Breaking?** yes / no
- **Rollback**: revert this commit; no migration needed
- **Risk level**: low / medium / high — because ___
```

## 审查清单规则

仅在 diff 中出现对应文件类别时，才补充该类别的清单内容：

| 文件类别 | 清单项 |
|----------|--------|
| source | 无调试语句残留；函数不超过 50 行；命名清晰；错误处理完善 |
| test | 断言有意义；覆盖边界情况；无不稳定测试；遵循 AAA 模式 |
| config | 无硬编码密钥；环境变量已文档化；保持向后兼容 |
| docs | 内容准确；附带示例；已更新 changelog |
| security-sensitive（路径含 `auth`/`crypto`/`token`/`password`） | 输入已校验；日志无密钥泄露；权限校验正确 |

## 拆分大型 PR

当 diff 超过 20 个文件或 1000 行时，建议按功能领域拆分：

```
git checkout -b feature/part-1
git cherry-pick <commits-for-part-1>
```

## 资源

- `resources/implementation-playbook.md` — Python 辅助脚本，用于自动化 PR 分析、覆盖率报告和风险评分。

## 局限性
- 仅在任务明确符合上述范围时使用本技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 若缺少必需输入、权限、安全边界或成功标准，应立即停止并请求澄清。
