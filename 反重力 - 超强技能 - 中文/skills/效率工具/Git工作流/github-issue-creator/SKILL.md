---
name: github-issue-creator
description: "将错误日志、截图、语音笔记和粗糙的 bug 报告转化为清晰、开发者就绪的 GitHub issue，包含复现步骤、影响分析和证据。当用户要求创建 GitHub issue、整理 bug 报告、将语音/截图转为 issue、记录 bug、提交问题时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# GitHub Issue Creator

将杂乱输入（错误日志、语音笔记、截图）转化为清晰、可执行的 GitHub issue。

## Output Template

```markdown
## Summary
[One-line description of the issue]

## Environment
- **Product/Service**: 
- **Region/Version**: 
- **Browser/OS**: (if relevant)

## Reproduction Steps
1. [Step]
2. [Step]
3. [Step]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Error Details
```
[Error message/code if applicable]
```

## Visual Evidence
[Reference to attached screenshots/GIFs]

## Impact
[Severity: Critical/High/Medium/Low + brief explanation]

## Additional Context
[Any other relevant details]
```

## Output Location

**将 issue 创建为 markdown 文件**，存放在仓库根目录的 `/issues/` 目录中。命名规范：`YYYY-MM-DD-short-description.md`

## Guidelines

**简洁明了**：不写废话。每个字都要有价值。

**从混乱中提取结构**：语音转述和原始笔记中往往包含事实，只是被随意表达掩盖了。把它们提取出来。

**推断缺失的上下文**：如果用户提到"同一个项目"或"那个仪表盘"，使用对话或记忆中的上下文补充具体信息。

**占位敏感数据**：对可能敏感的信息使用 `[PROJECT_NAME]`、`[USER_ID]` 等占位符。

**根据影响匹配严重程度**：
- Critical（严重）：服务宕机、数据丢失、安全问题
- High（高）：主要功能损坏，无替代方案
- Medium（中）：功能受损，存在替代方案
- Low（低）：轻微不便、外观问题

**图片/GIF 处理**：在正文中引用附件。格式：`!Description`

## Examples

**输入（语音转述）**：
> so I was trying to deploy the agent and it just failed silently no error nothing the workflow ran but then poof gone from the list had to refresh and try again three times

**输出**：
```markdown
## Summary
Agent deployment fails silently - no error displayed, agent disappears from list

## Environment
- **Product/Service**: Azure AI Foundry
- **Region/Version**: westus2

## Reproduction Steps
1. Navigate to agent deployment
2. Configure and deploy agent
3. Observe workflow completes
4. Check agent list

## Expected Behavior
Agent appears in list with deployment status, errors shown if deployment fails

## Actual Behavior
Agent disappears from list. No error message. Requires page refresh and retry.

## Impact
**High** - Blocks agent deployment workflow, no feedback on failure cause

## Additional Context
Required 3 retry attempts before successful deployment
```

---

**输入（错误粘贴）**：
> Error: PERMISSION_DENIED when publishing to Teams channel. Code: 403. Was working yesterday.

**输出**：
```markdown
## Summary
403 PERMISSION_DENIED error when publishing to Teams channel

## Environment
- **Product/Service**: Copilot Studio → Teams integration
- **Region/Version**: [REGION]

## Reproduction Steps
1. Configure agent for Teams channel
2. Attempt to publish

## Expected Behavior
Agent publishes successfully to Teams channel

## Actual Behavior
Returns `PERMISSION_DENIED` with code 403

## Error Details
```
Error: PERMISSION_DENIED
Code: 403
```

## Impact
**High** - Blocks Teams integration, regression from previous working state

## Additional Context
Was working yesterday - possible permission/config change or service regression
```

## When to Use

当你有非结构化的 bug 输入（如粘贴的错误信息、支持笔记、截图或语音转述），需要将其转化为清晰的 GitHub issue，包含摘要、复现步骤、预期行为与实际行为对比、影响分析和附件引用时，使用此技能。

## Limitations

- 仅在任务明确符合上述范围时使用此技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
