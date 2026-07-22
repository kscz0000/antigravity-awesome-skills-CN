---
name: github-workflow-automation
description: "AI 辅助的 GitHub 工作流自动化模式，灵感来自 [Gemini CLI](https://github.com/google-gemini/gemini-cli) 和现代 DevOps 实践。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 🔧 GitHub 工作流自动化

> AI 辅助的 GitHub 工作流自动化模式，灵感来自 [Gemini CLI](https://github.com/google-gemini/gemini-cli) 和现代 DevOps 实践。

## 何时使用此技能

在以下情况下使用此技能：

- 使用 AI 自动化 PR 审查
- 设置 issue 分类自动化
- 创建 GitHub Actions 工作流
- 将 AI 集成到 CI/CD 流水线
- 自动化 Git 操作（rebase、cherry-pick）

---

## 1. 自动化 PR 审查

### 1.1 PR 审查 Action

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get changed files
        id: changed
        run: |
          files=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)
          echo "files<<EOF" >> $GITHUB_OUTPUT
          echo "$files" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Get diff
        id: diff
        run: |
          diff=$(git diff origin/${{ github.base_ref }}...HEAD)
          echo "diff<<EOF" >> $GITHUB_OUTPUT
          echo "$diff" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: AI Review
        uses: actions/github-script@v7
        with:
          script: |
            const { Anthropic } = require('@anthropic-ai/sdk');
            const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

            const response = await client.messages.create({
              model: "claude-3-sonnet-20240229",
              max_tokens: 4096,
              messages: [{
                role: "user",
                content: `Review this PR diff and provide feedback:
                
                Changed files: ${{ steps.changed.outputs.files }}
                
                Diff:
                ${{ steps.diff.outputs.diff }}
                
                Provide:
                1. Summary of changes
                2. Potential issues or bugs
                3. Suggestions for improvement
                4. Security concerns if any
                
                Format as GitHub markdown.`
              }]
            });

            await github.rest.pulls.createReview({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              body: response.content[0].text,
              event: 'COMMENT'
            });
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### 1.2 审查评论模式

````markdown
# AI 审查结构

## 📋 概要

简要描述此 PR 的作用。

## ✅ 看起来不错的部分

- 代码结构良好
- 测试覆盖充分
- 命名规范清晰

## ⚠️ 潜在问题

1. **第 42 行**：可能存在空指针异常
   ```javascript
   // 当前代码
   user.profile.name;
   // 建议修改
   user?.profile?.name ?? "Unknown";
   ```
````
2. **第 78 行**：考虑错误处理
   ```javascript
   // 添加 try-catch 或 .catch()
   ```

## 💡 建议

- 考虑将验证逻辑提取到单独的函数中
- 为公共方法添加 JSDoc 注释

## 🔒 安全说明

- 未检测到敏感数据泄露
- API 密钥处理正确

````

### 1.3 聚焦审查

```yaml
# 仅审查特定文件类型
- name: Filter code files
  run: |
    files=$(git diff --name-only origin/${{ github.base_ref }}...HEAD | \
            grep -E '\.(ts|tsx|js|jsx|py|go)$' || true)
    echo "code_files=$files" >> $GITHUB_OUTPUT

# 带上下文的审查
- name: AI Review with context
  run: |
    # 包含相关的上下文文件
    context=""
    for file in ${{ steps.changed.outputs.files }}; do
      if [[ -f "$file" ]]; then
        context+="=== $file ===\n$(cat $file)\n\n"
      fi
    done

    # 发送给 AI 并附带完整文件上下文
````

---

## 2. Issue 分类自动化

### 2.1 自动标记 Issue

```yaml
# .github/workflows/issue-triage.yml
name: Issue Triage

on:
  issues:
    types: [opened]

jobs:
  triage:
    runs-on: ubuntu-latest
    permissions:
      issues: write

    steps:
      - name: Analyze issue
        uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;

            // 调用 AI 进行分析
            const analysis = await analyzeIssue(issue.title, issue.body);

            // 应用标签
            const labels = [];

            if (analysis.type === 'bug') {
              labels.push('bug');
              if (analysis.severity === 'high') labels.push('priority: high');
            } else if (analysis.type === 'feature') {
              labels.push('enhancement');
            } else if (analysis.type === 'question') {
              labels.push('question');
            }

            if (analysis.area) {
              labels.push(`area: ${analysis.area}`);
            }

            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: issue.number,
              labels: labels
            });

            // 添加初始回复
            if (analysis.type === 'bug' && !analysis.hasReproSteps) {
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                body: `感谢您报告此问题！

为了帮助我们调查，请您提供：
- 复现问题的步骤
- 预期行为
- 实际行为
- 环境信息（操作系统、版本等）

这将帮助我们更快地解决您的问题。🙏`
              });
            }
```

### 2.2 Issue 分析提示词

```typescript
const TRIAGE_PROMPT = `
Analyze this GitHub issue and classify it:

Title: {title}
Body: {body}

Return JSON with:
{
  "type": "bug" | "feature" | "question" | "docs" | "other",
  "severity": "low" | "medium" | "high" | "critical",
  "area": "frontend" | "backend" | "api" | "docs" | "ci" | "other",
  "summary": "one-line summary",
  "hasReproSteps": boolean,
  "isFirstContribution": boolean,
  "suggestedLabels": ["label1", "label2"],
  "suggestedAssignees": ["username"] // based on area expertise
}
`;
```

### 2.3 过期 Issue 管理

```yaml
# .github/workflows/stale.yml
name: Manage Stale Issues

on:
  schedule:
    - cron: "0 0 * * *" # 每日运行

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          stale-issue-message: |
            此 issue 已被自动标记为过期，因为它近期没有活动。
            如果 14 天内仍无进一步活动，它将被关闭。

            如果此 issue 仍然相关：
            - 添加评论说明更新情况
            - 移除 `stale` 标签

            感谢您的贡献！🙏

          stale-pr-message: |
            此 PR 已被自动标记为过期。请更新它，否则将在 14 天后关闭。

          days-before-stale: 60
          days-before-close: 14
          stale-issue-label: "stale"
          stale-pr-label: "stale"
          exempt-issue-labels: "pinned,security,in-progress"
          exempt-pr-labels: "pinned,security"
```

---

## 3. CI/CD 集成

### 3.1 智能测试选择

```yaml
# .github/workflows/smart-tests.yml
name: Smart Test Selection

on:
  pull_request:

jobs:
  analyze:
    runs-on: ubuntu-latest
    outputs:
      test_suites: ${{ steps.analyze.outputs.suites }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Analyze changes
        id: analyze
        run: |
          # 获取变更的文件
          changed=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)

          # 确定运行哪些测试套件
          suites="[]"

          if echo "$changed" | grep -q "^src/api/"; then
            suites=$(echo $suites | jq '. + ["api"]')
          fi

          if echo "$changed" | grep -q "^src/frontend/"; then
            suites=$(echo $suites | jq '. + ["frontend"]')
          fi

          if echo "$changed" | grep -q "^src/database/"; then
            suites=$(echo $suites | jq '. + ["database", "api"]')
          fi

          # 如果没有特定匹配，运行全部
          if [ "$suites" = "[]" ]; then
            suites='["all"]'
          fi

          echo "suites=$suites" >> $GITHUB_OUTPUT

  test:
    needs: analyze
    runs-on: ubuntu-latest
    strategy:
      matrix:
        suite: ${{ fromJson(needs.analyze.outputs.test_suites) }}

    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        run: |
          if [ "${{ matrix.suite }}" = "all" ]; then
            npm test
          else
            npm test -- --suite ${{ matrix.suite }}
          fi
```

### 3.2 带 AI 验证的部署

```yaml
# .github/workflows/deploy.yml
name: Deploy with AI Validation

on:
  push:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Get deployment changes
        id: changes
        run: |
          # 获取上次部署以来的提交
          last_deploy=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
          if [ -n "$last_deploy" ]; then
            changes=$(git log --oneline $last_deploy..HEAD)
          else
            changes=$(git log --oneline -10)
          fi
          echo "changes<<EOF" >> $GITHUB_OUTPUT
          echo "$changes" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: AI Risk Assessment
        id: assess
        uses: actions/github-script@v7
        with:
          script: |
            // 分析变更的部署风险
            const prompt = `
            Analyze these changes for deployment risk:

            ${process.env.CHANGES}

            Return JSON:
            {
              "riskLevel": "low" | "medium" | "high",
              "concerns": ["concern1", "concern2"],
              "recommendations": ["rec1", "rec2"],
              "requiresManualApproval": boolean
            }
            `;

            // 调用 AI 并解析响应
            const analysis = await callAI(prompt);

            if (analysis.riskLevel === 'high') {
              core.setFailed('High-risk deployment detected. Manual review required.');
            }

            return analysis;
        env:
          CHANGES: ${{ steps.changes.outputs.changes }}

  deploy:
    needs: validate
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy
        run: |
          echo "Deploying to production..."
          # 部署命令放在这里
```

### 3.3 自动回滚

```yaml
# .github/workflows/rollback.yml
name: Automated Rollback

on:
  workflow_dispatch:
    inputs:
      reason:
        description: "回滚原因"
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Find last stable version
        id: stable
        run: |
          # 查找上次成功部署的版本
          stable=$(git tag -l 'v*' --sort=-version:refname | head -1)
          echo "version=$stable" >> $GITHUB_OUTPUT

      - name: Rollback
        run: |
          git checkout ${{ steps.stable.outputs.version }}
          # 部署稳定版本
          npm run deploy

      - name: Notify team
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "🔄 生产环境已回滚至 ${{ steps.stable.outputs.version }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*回滚已执行*\n• 版本: `${{ steps.stable.outputs.version }}`\n• 原因: ${{ inputs.reason }}\n• 触发者: ${{ github.actor }}"
                  }
                }
              ]
            }
```

---

## 4. Git 操作

### 4.1 自动 Rebase

```yaml
# .github/workflows/auto-rebase.yml
name: Auto Rebase

on:
  issue_comment:
    types: [created]

jobs:
  rebase:
    if: github.event.issue.pull_request && contains(github.event.comment.body, '/rebase')
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Setup Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: Rebase PR
        run: |
          # 获取 PR 分支
          gh pr checkout ${{ github.event.issue.number }}

          # Rebase 到 main
          git fetch origin main
          git rebase origin/main

          # 强制推送
          git push --force-with-lease
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Comment result
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: '✅ 成功 rebase 到 main！'
            })
```

### 4.2 智能 Cherry-Pick

```typescript
// AI 辅助的 cherry-pick，可处理冲突
async function smartCherryPick(commitHash: string, targetBranch: string) {
  // 获取提交信息
  const commitInfo = await exec(`git show ${commitHash} --stat`);

  // 检查潜在冲突
  const targetDiff = await exec(
    `git diff ${targetBranch}...HEAD -- ${affectedFiles}`
  );

  // AI 分析
  const analysis = await ai.analyze(`
    I need to cherry-pick this commit to ${targetBranch}:
    
    ${commitInfo}
    
    Current state of affected files on ${targetBranch}:
    ${targetDiff}
    
    Will there be conflicts? If so, suggest resolution strategy.
  `);

  if (analysis.willConflict) {
    // 创建分支用于手动解决
    await exec(
      `git checkout -b cherry-pick-${commitHash.slice(0, 7)} ${targetBranch}`
    );
    const result = await exec(`git cherry-pick ${commitHash}`, {
      allowFail: true,
    });

    if (result.failed) {
      // AI 辅助冲突解决
      const conflicts = await getConflicts();
      for (const conflict of conflicts) {
        const resolution = await ai.resolveConflict(conflict);
        await applyResolution(conflict.file, resolution);
      }
    }
  } else {
    await exec(`git checkout ${targetBranch}`);
    await exec(`git cherry-pick ${commitHash}`);
  }
}
```

### 4.3 分支清理

```yaml
# .github/workflows/branch-cleanup.yml
name: Branch Cleanup

on:
  schedule:
    - cron: '0 0 * * 0'  # 每周运行
  workflow_dispatch:

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Find stale branches
        id: stale
        run: |
          # 超过 30 天未更新的分支
          stale=$(git for-each-ref --sort=-committerdate refs/remotes/origin \
            --format='%(refname:short) %(committerdate:relative)' | \
            grep -E '[3-9][0-9]+ days|[0-9]+ months|[0-9]+ years' | \
            grep -v 'origin/main\|origin/develop' | \
            cut -d' ' -f1 | sed 's|origin/||')

          echo "branches<<EOF" >> $GITHUB_OUTPUT
          echo "$stale" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create cleanup PR
        if: steps.stale.outputs.branches != ''
        uses: actions/github-script@v7
        with:
          script: |
            const branches = `${{ steps.stale.outputs.branches }}`.split('\n').filter(Boolean);

            const body = `## 🧹 过期分支清理

以下分支已超过 30 天未更新：

${branches.map(b => `- \`${b}\``).join('\n')}

### 操作：
- [ ] 审查每个分支
- [ ] 删除不再需要的分支
- 评论 \`/keep branch-name\` 以保留特定分支
`;

            await github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '过期分支清理',
              body: body,
              labels: ['housekeeping']
            });
```

---

## 5. 按需协助

### 5.1 @提及机器人

```yaml
# .github/workflows/mention-bot.yml
name: AI Mention Bot

on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  respond:
    if: contains(github.event.comment.body, '@ai-helper')
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Extract question
        id: question
        run: |
          # 提取 @ai-helper 后的文本
          question=$(echo "${{ github.event.comment.body }}" | sed 's/.*@ai-helper//')
          echo "question=$question" >> $GITHUB_OUTPUT

      - name: Get context
        id: context
        run: |
          if [ "${{ github.event.issue.pull_request }}" != "" ]; then
            # 这是一个 PR - 获取 diff
            gh pr diff ${{ github.event.issue.number }} > context.txt
          else
            # 这是一个 issue - 获取描述
            gh issue view ${{ github.event.issue.number }} --json body -q .body > context.txt
          fi
          echo "context=$(cat context.txt)" >> $GITHUB_OUTPUT
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: AI Response
        uses: actions/github-script@v7
        with:
          script: |
            const response = await ai.chat(`
              Context: ${process.env.CONTEXT}
              
              Question: ${process.env.QUESTION}
              
              Provide a helpful, specific answer. Include code examples if relevant.
            `);

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: response
            });
        env:
          CONTEXT: ${{ steps.context.outputs.context }}
          QUESTION: ${{ steps.question.outputs.question }}
```

### 5.2 命令模式

```markdown
## 可用命令

| 命令                  | 描述                       |
| :-------------------- | :------------------------- |
| `@ai-helper explain`  | 解释此 PR 中的代码         |
| `@ai-helper review`   | 请求 AI 代码审查           |
| `@ai-helper fix`      | 建议问题的修复方案         |
| `@ai-helper test`     | 生成测试用例               |
| `@ai-helper docs`     | 生成文档                   |
| `/rebase`             | 将 PR rebase 到 main       |
| `/update`             | 从 main 更新 PR 分支       |
| `/approve`            | 标记为机器人已批准         |
| `/label bug`          | 添加 'bug' 标签            |
| `/assign @user`       | 分配给用户                 |
```

---

## 6. 仓库配置

### 6.1 CODEOWNERS

```
# .github/CODEOWNERS

# 全局所有者
* @org/core-team

# 前端
/src/frontend/ @org/frontend-team
*.tsx @org/frontend-team
*.css @org/frontend-team

# 后端
/src/api/ @org/backend-team
/src/database/ @org/backend-team

# 基础设施
/.github/ @org/devops-team
/terraform/ @org/devops-team
Dockerfile @org/devops-team

# 文档
/docs/ @org/docs-team
*.md @org/docs-team

# 安全敏感
/src/auth/ @org/security-team
/src/crypto/ @org/security-team
```

### 6.2 分支保护

```yaml
# 通过 GitHub API 设置
- name: Configure branch protection
  uses: actions/github-script@v7
  with:
    script: |
      await github.rest.repos.updateBranchProtection({
        owner: context.repo.owner,
        repo: context.repo.repo,
        branch: 'main',
        required_status_checks: {
          strict: true,
          contexts: ['test', 'lint', 'ai-review']
        },
        enforce_admins: true,
        required_pull_request_reviews: {
          required_approving_review_count: 1,
          require_code_owner_reviews: true,
          dismiss_stale_reviews: true
        },
        restrictions: null,
        required_linear_history: true,
        allow_force_pushes: false,
        allow_deletions: false
      });
```

---

## 最佳实践

### 安全

- [ ] 将 API 密钥存储在 GitHub Secrets 中
- [ ] 在工作流中使用最小权限
- [ ] 验证所有输入
- [ ] 不要在日志中暴露敏感数据

### 性能

- [ ] 缓存依赖项
- [ ] 使用矩阵构建进行并行测试
- [ ] 使用路径过滤器跳过不必要的作业
- [ ] 对繁重的工作负载使用自托管运行器

### 可靠性

- [ ] 为作业添加超时
- [ ] 优雅地处理速率限制
- [ ] 实现重试逻辑
- [ ] 准备回滚流程

---

## 资源

- [Gemini CLI GitHub Action](https://github.com/google-github-actions/run-gemini-cli)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [GitHub REST API](https://docs.github.com/en/rest)
- [CODEOWNERS 语法](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停止并请求澄清。
