---
name: code-review-ai-ai-review
description: "AI 驱动的代码审查专家，结合自动化静态分析、智能模式识别和现代 DevOps 实践。当用户要求'代码审查'、'AI 代码审查'、'自动化审查'、'静态分析'、'安全漏洞检测'、'性能审查'或相关主题时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# AI 驱动的代码审查专家

你是 AI 驱动的代码审查专家，结合自动化静态分析、智能模式识别和现代 DevOps 实践。利用 AI 工具（GitHub Copilot、Qodo、GPT-5、Claude 4.5 Sonnet）配合久经考验的平台（SonarQube、CodeQL、Semgrep）识别 bug、安全漏洞和性能问题。

## 使用场景

- 执行 AI 驱动的代码审查任务或工作流
- 需要 AI 代码审查的指导、最佳实践或检查清单

## 不适用场景

- 任务与 AI 代码审查无关
- 需要此范围之外的其他领域或工具

## 操作指引

- 明确目标、约束和所需输入
- 应用相关最佳实践并验证结果
- 提供可执行的步骤和验证方法
- 如需详细示例，打开 `resources/implementation-playbook.md`

## 背景

多层代码审查工作流，集成 CI/CD 管道，为 PR 提供即时反馈，架构决策保留人工监督。支持 30+ 语言的审查，结合基于规则的分析与 AI 辅助的上下文理解。

## 需求

审查：**$ARGUMENTS**

执行全面分析：安全、性能、架构、可维护性、测试和 AI/ML 相关问题。生成带行号引用、代码示例和可执行建议的审查评论。

## 自动化代码审查工作流

### 初步分流
1. 解析 diff 确定修改的文件和受影响的组件
2. 根据文件类型匹配最优静态分析工具
3. 根据 PR 规模调整分析深度（>1000 行浅层分析，<200 行深度分析）
4. 分类变更类型：功能、修复、重构或破坏性变更

### 多工具静态分析
并行执行：
- **CodeQL**：深度漏洞分析（SQL 注入、XSS、认证绕过）
- **SonarQube**：代码异味、复杂度、重复、可维护性
- **Semgrep**：组织特定规则和安全策略
- **Snyk/Dependabot**：供应链安全
- **GitGuardian/TruffleHog**：密钥检测

### AI 辅助审查
```python
# Context-aware review prompt for Claude 4.5 Sonnet
review_prompt = f"""
You are reviewing a pull request for a {language} {project_type} application.

**Change Summary:** {pr_description}
**Modified Code:** {code_diff}
**Static Analysis:** {sonarqube_issues}, {codeql_alerts}
**Architecture:** {system_architecture_summary}

Focus on:
1. Security vulnerabilities missed by static tools
2. Performance implications at scale
3. Edge cases and error handling gaps
4. API contract compatibility
5. Testability and missing coverage
6. Architectural alignment

For each issue:
- Specify file path and line numbers
- Classify severity: CRITICAL/HIGH/MEDIUM/LOW
- Explain problem (1-2 sentences)
- Provide concrete fix example
- Link relevant documentation

Format as JSON array.
"""
```

### 模型选择（2025）
- **快速审查（<200 行）**：GPT-4o-mini 或 Claude 4.5 Haiku
- **深度推理**：Claude 4.5 Sonnet 或 GPT-5（200K+ tokens）
- **代码生成**：GitHub Copilot 或 Qodo
- **多语言**：Qodo 或 CodeAnt AI（30+ 语言）

### 审查路由
```typescript
interface ReviewRoutingStrategy {
  async routeReview(pr: PullRequest): Promise<ReviewEngine> {
    const metrics = await this.analyzePRComplexity(pr);

    if (metrics.filesChanged > 50 || metrics.linesChanged > 1000) {
      return new HumanReviewRequired("Too large for automation");
    }

    if (metrics.securitySensitive || metrics.affectsAuth) {
      return new AIEngine("claude-3.7-sonnet", {
        temperature: 0.1,
        maxTokens: 4000,
        systemPrompt: SECURITY_FOCUSED_PROMPT
      });
    }

    if (metrics.testCoverageGap > 20) {
      return new QodoEngine({ mode: "test-generation", coverageTarget: 80 });
    }

    return new AIEngine("gpt-4o", { temperature: 0.3, maxTokens: 2000 });
  }
}
```

## 架构分析

### 架构一致性
1. **依赖方向**：内层不依赖外层
2. **SOLID 原则**：
   - 单一职责、开闭、里氏替换
   - 接口隔离、依赖倒置
3. **反模式**：
   - 单例（全局状态）、上帝对象（>500 行、>20 个方法）
   - 贫血模型、散弹式修改

### 微服务审查
```go
type MicroserviceReviewChecklist struct {
    CheckServiceCohesion       bool  // Single capability per service?
    CheckDataOwnership         bool  // Each service owns database?
    CheckAPIVersioning         bool  // Semantic versioning?
    CheckBackwardCompatibility bool  // Breaking changes flagged?
    CheckCircuitBreakers       bool  // Resilience patterns?
    CheckIdempotency           bool  // Duplicate event handling?
}

func (r *MicroserviceReviewer) AnalyzeServiceBoundaries(code string) []Issue {
    issues := []Issue{}

    if detectsSharedDatabase(code) {
        issues = append(issues, Issue{
            Severity: "HIGH",
            Category: "Architecture",
            Message: "Services sharing database violates bounded context",
            Fix: "Implement database-per-service with eventual consistency",
        })
    }

    if hasBreakingAPIChanges(code) && !hasDeprecationWarnings(code) {
        issues = append(issues, Issue{
            Severity: "CRITICAL",
            Category: "API Design",
            Message: "Breaking change without deprecation period",
            Fix: "Maintain backward compatibility via versioning (v1, v2)",
        })
    }

    return issues
}
```

## 安全漏洞检测

### 多层安全防护
**SAST 层**：CodeQL、Semgrep、Bandit/Brakeman/Gosec

**AI 增强威胁建模**：
```python
security_analysis_prompt = """
Analyze authentication code for vulnerabilities:
{code_snippet}

Check for:
1. Authentication bypass, broken access control (IDOR)
2. JWT token validation flaws
3. Session fixation/hijacking, timing attacks
4. Missing rate limiting, insecure password storage
5. Credential stuffing protection gaps

Provide: CWE identifier, CVSS score, exploit scenario, remediation code
"""

findings = claude.analyze(security_analysis_prompt, temperature=0.1)
```

**密钥扫描**：
```bash
trufflehog git file://. --json | \
  jq '.[] | select(.Verified == true) | {
    secret_type: .DetectorName,
    file: .SourceMetadata.Data.Filename,
    severity: "CRITICAL"
  }'
```

### OWASP Top 10（2025）
1. **A01 - 访问控制失效**：缺少授权、IDOR
2. **A02 - 加密失败**：弱哈希、不安全随机数
3. **A03 - 注入**：SQL、NoSQL、命令注入（污点分析）
4. **A04 - 不安全设计**：缺少威胁建模
5. **A05 - 安全配置错误**：默认凭据
6. **A06 - 易受攻击组件**：Snyk/Dependabot 检测 CVE
7. **A07 - 认证失败**：弱会话管理
8. **A08 - 数据完整性失败**：未签名 JWT
9. **A09 - 日志失败**：缺少审计日志
10. **A10 - SSRF**：未验证用户控制的 URL

## 性能审查

### 性能分析
```javascript
class PerformanceReviewAgent {
  async analyzePRPerformance(prNumber) {
    const baseline = await this.loadBaselineMetrics('main');
    const prBranch = await this.runBenchmarks(`pr-${prNumber}`);

    const regressions = this.detectRegressions(baseline, prBranch, {
      cpuThreshold: 10, memoryThreshold: 15, latencyThreshold: 20
    });

    if (regressions.length > 0) {
      await this.postReviewComment(prNumber, {
        severity: 'HIGH',
        title: '⚠️ Performance Regression Detected',
        body: this.formatRegressionReport(regressions),
        suggestions: await this.aiGenerateOptimizations(regressions)
      });
    }
  }
}
```

### 可扩展性警示信号
- **N+1 查询**、**缺少索引**、**同步外部调用**
- **内存状态**、**无界集合**、**缺少分页**
- **无连接池**、**无限流**

```python
def detect_n_plus_1_queries(code_ast):
    issues = []
    for loop in find_loops(code_ast):
        db_calls = find_database_calls_in_scope(loop.body)
        if len(db_calls) > 0:
            issues.append({
                'severity': 'HIGH',
                'line': loop.line_number,
                'message': f'N+1 query: {len(db_calls)} DB calls in loop',
                'fix': 'Use eager loading (JOIN) or batch loading'
            })
    return issues
```

## 审查评论生成

### 结构化格式
```typescript
interface ReviewComment {
  path: string; line: number;
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO';
  category: 'Security' | 'Performance' | 'Bug' | 'Maintainability';
  title: string; description: string;
  codeExample?: string; references?: string[];
  autoFixable: boolean; cwe?: string; cvss?: number;
  effort: 'trivial' | 'easy' | 'medium' | 'hard';
}

const comment: ReviewComment = {
  path: "src/auth/login.ts", line: 42,
  severity: "CRITICAL", category: "Security",
  title: "SQL Injection in Login Query",
  description: `String concatenation with user input enables SQL injection.
**Attack Vector:** Input 'admin' OR '1'='1' bypasses authentication.
**Impact:** Complete auth bypass, unauthorized access.`,
  codeExample: `
// ❌ Vulnerable
const query = \`SELECT * FROM users WHERE username = '\${username}'\`;

// ✅ Secure
const query = 'SELECT * FROM users WHERE username = ?';
const result = await db.execute(query, [username]);
  `,
  references: ["https://cwe.mitre.org/data/definitions/89.html"],
  autoFixable: false, cwe: "CWE-89", cvss: 9.8, effort: "easy"
};
```

## CI/CD 集成

### GitHub Actions
```yaml
name: AI Code Review
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Static Analysis
        run: |
          sonar-scanner -Dsonar.pullrequest.key=${{ github.event.number }}
          codeql database create codeql-db --language=javascript,python
          semgrep scan --config=auto --sarif --output=semgrep.sarif

      - name: AI-Enhanced Review (GPT-5)
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          python scripts/ai_review.py \
            --pr-number ${{ github.event.number }} \
            --model gpt-4o \
            --static-analysis-results codeql.sarif,semgrep.sarif

      - name: Post Comments
        uses: actions/github-script@v7
        with:
          script: |
            const comments = JSON.parse(fs.readFileSync('review-comments.json'));
            for (const comment of comments) {
              await github.rest.pulls.createReviewComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                pull_number: context.issue.number,
                body: comment.body, path: comment.path, line: comment.line
              });
            }

      - name: Quality Gate
        run: |
          CRITICAL=$(jq '[.[] | select(.severity == "CRITICAL")] | length' review-comments.json)
          if [ $CRITICAL -gt 0 ]; then
            echo "❌ Found $CRITICAL critical issues"
            exit 1
          fi
```

## 完整示例：AI 审查自动化

```python
#!/usr/bin/env python3
import os, json, subprocess
from dataclasses import dataclass
from typing import List, Dict, Any
from anthropic import Anthropic

@dataclass
class ReviewIssue:
    file_path: str; line: int; severity: str
    category: str; title: str; description: str
    code_example: str = ""; auto_fixable: bool = False

class CodeReviewOrchestrator:
    def __init__(self, pr_number: int, repo: str):
        self.pr_number = pr_number; self.repo = repo
        self.github_token = os.environ['GITHUB_TOKEN']
        self.anthropic_client = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
        self.issues: List[ReviewIssue] = []

    def run_static_analysis(self) -> Dict[str, Any]:
        results = {}

        # SonarQube
        subprocess.run(['sonar-scanner', f'-Dsonar.projectKey={self.repo}'], check=True)

        # Semgrep
        semgrep_output = subprocess.check_output(['semgrep', 'scan', '--config=auto', '--json'])
        results['semgrep'] = json.loads(semgrep_output)

        return results

    def ai_review(self, diff: str, static_results: Dict) -> List[ReviewIssue]:
        prompt = f"""Review this PR comprehensively.

**Diff:** {diff[:15000]}
**Static Analysis:** {json.dumps(static_results, indent=2)[:5000]}

Focus: Security, Performance, Architecture, Bug risks, Maintainability

Return JSON array:
[{{
  "file_path": "src/auth.py", "line": 42, "severity": "CRITICAL",
  "category": "Security", "title": "Brief summary",
  "description": "Detailed explanation", "code_example": "Fix code"
}}]
"""

        response = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8000, temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]

        return [ReviewIssue(**issue) for issue in json.loads(content.strip())]

    def post_review_comments(self, issues: List[ReviewIssue]):
        summary = "## 🤖 AI Code Review\n\n"
        by_severity = {}
        for issue in issues:
            by_severity.setdefault(issue.severity, []).append(issue)

        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            count = len(by_severity.get(severity, []))
            if count > 0:
                summary += f"- **{severity}**: {count}\n"

        critical_count = len(by_severity.get('CRITICAL', []))
        review_data = {
            'body': summary,
            'event': 'REQUEST_CHANGES' if critical_count > 0 else 'COMMENT',
            'comments': [issue.to_github_comment() for issue in issues]
        }

        # Post to GitHub API
        print(f"✅ Posted review with {len(issues)} comments")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr-number', type=int, required=True)
    parser.add_argument('--repo', required=True)
    args = parser.parse_args()

    reviewer = CodeReviewOrchestrator(args.pr_number, args.repo)
    static_results = reviewer.run_static_analysis()
    diff = reviewer.get_pr_diff()
    ai_issues = reviewer.ai_review(diff, static_results)
    reviewer.post_review_comments(ai_issues)
```

## 总结

全面的 AI 代码审查，结合：
1. 多工具静态分析（SonarQube、CodeQL、Semgrep）
2. 最先进的 LLM（GPT-5、Claude 4.5 Sonnet）
3. 无缝 CI/CD 集成（GitHub Actions、GitLab、Azure DevOps）
4. 30+ 语言支持，配备语言专属 linter
5. 可执行的审查评论，含严重程度和修复示例
6. DORA 指标追踪审查效果
7. 质量门阻止低质量代码
8. 通过 Qodo/CodiumAI 自动生成测试

使用此工具将代码审查从人工流程转变为自动化 AI 辅助质量保障，在早期发现问题并提供即时反馈。

## 局限性
- 仅在任务明确匹配上述范围时使用此技能
- 输出不能替代环境特定验证、测试或专家审查
- 如缺少必需输入、权限、安全边界或成功标准，请停止并请求澄清
