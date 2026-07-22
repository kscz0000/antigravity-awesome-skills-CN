# 工作流自动化实现指南

本文件包含技能引用的详细模式、检查清单和代码示例。

## 指令

### 1. 工作流分析

分析现有流程并识别自动化机会：

**工作流发现脚本**
```python
import os
import yaml
import json
from pathlib import Path
from typing import List, Dict, Any

class WorkflowAnalyzer:
    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """
        分析项目以识别自动化机会
        """
        analysis = {
            'current_workflows': self._find_existing_workflows(project_path),
            'manual_processes': self._identify_manual_processes(project_path),
            'automation_opportunities': [],
            'tool_recommendations': [],
            'complexity_score': 0
        }
        
        # 分析不同方面
        analysis['build_process'] = self._analyze_build_process(project_path)
        analysis['test_process'] = self._analyze_test_process(project_path)
        analysis['deployment_process'] = self._analyze_deployment_process(project_path)
        analysis['code_quality'] = self._analyze_code_quality_checks(project_path)
        
        # 生成建议
        self._generate_recommendations(analysis)
        
        return analysis
    
    def _find_existing_workflows(self, project_path: str) -> List[Dict]:
        """查找现有的 CI/CD 工作流"""
        workflows = []
        
        # GitHub Actions
        gh_workflow_path = Path(project_path) / '.github' / 'workflows'
        if gh_workflow_path.exists():
            for workflow_file in gh_workflow_path.glob('*.y*ml'):
                with open(workflow_file) as f:
                    workflow = yaml.safe_load(f)
                    workflows.append({
                        'type': 'github_actions',
                        'name': workflow.get('name', workflow_file.stem),
                        'file': str(workflow_file),
                        'triggers': list(workflow.get('on', {}).keys())
                    })
        
        # GitLab CI
        gitlab_ci = Path(project_path) / '.gitlab-ci.yml'
        if gitlab_ci.exists():
            with open(gitlab_ci) as f:
                config = yaml.safe_load(f)
                workflows.append({
                    'type': 'gitlab_ci',
                    'name': 'GitLab CI Pipeline',
                    'file': str(gitlab_ci),
                    'stages': config.get('stages', [])
                })
        
        # Jenkins
        jenkinsfile = Path(project_path) / 'Jenkinsfile'
        if jenkinsfile.exists():
            workflows.append({
                'type': 'jenkins',
                'name': 'Jenkins Pipeline',
                'file': str(jenkinsfile)
            })
        
        return workflows
    
    def _identify_manual_processes(self, project_path: str) -> List[Dict]:
        """识别可以自动化的流程"""
        manual_processes = []
        
        # 检查手工构建脚本
        script_patterns = ['build.sh', 'deploy.sh', 'release.sh', 'test.sh']
        for pattern in script_patterns:
            scripts = Path(project_path).glob(f'**/{pattern}')
            for script in scripts:
                manual_processes.append({
                    'type': 'script',
                    'file': str(script),
                    'purpose': pattern.replace('.sh', ''),
                    'automation_potential': 'high'
                })
        
        # 检查 README 中的手工步骤
        readme_files = ['README.md', 'README.rst', 'README.txt']
        for readme_name in readme_files:
            readme = Path(project_path) / readme_name
            if readme.exists():
                content = readme.read_text()
                if any(keyword in content.lower() for keyword in ['manually', 'by hand', 'steps to']):
                    manual_processes.append({
                        'type': 'documented_process',
                        'file': str(readme),
                        'indicators': 'Contains manual process documentation'
                    })
        
        return manual_processes
    
    def _generate_recommendations(self, analysis: Dict) -> None:
        """生成自动化建议"""
        recommendations = []
        
        # CI/CD 建议
        if not analysis['current_workflows']:
            recommendations.append({
                'priority': 'high',
                'category': 'ci_cd',
                'recommendation': 'Implement CI/CD pipeline',
                'tools': ['GitHub Actions', 'GitLab CI', 'Jenkins'],
                'effort': 'medium'
            })
        
        # 构建自动化
        if analysis['build_process']['manual_steps']:
            recommendations.append({
                'priority': 'high',
                'category': 'build',
                'recommendation': 'Automate build process',
                'tools': ['Make', 'Gradle', 'npm scripts'],
                'effort': 'low'
            })
        
        # 测试自动化
        if not analysis['test_process']['automated_tests']:
            recommendations.append({
                'priority': 'high',
                'category': 'testing',
                'recommendation': 'Implement automated testing',
                'tools': ['Jest', 'Pytest', 'JUnit'],
                'effort': 'medium'
            })
        
        # 部署自动化
        if analysis['deployment_process']['manual_deployment']:
            recommendations.append({
                'priority': 'critical',
                'category': 'deployment',
                'recommendation': 'Automate deployment process',
                'tools': ['ArgoCD', 'Flux', 'Terraform'],
                'effort': 'high'
            })
        
        analysis['automation_opportunities'] = recommendations
```

### 2. GitHub Actions 工作流

创建全面的 GitHub Actions 工作流：

**多环境 CI/CD 流水线**
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  release:
    types: [created]

env:
  NODE_VERSION: '18'
  PYTHON_VERSION: '3.11'
  GO_VERSION: '1.21'

jobs:
  # 代码质量检查
  quality:
    name: Code Quality
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # 完整历史以便更好地分析

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: |
            ~/.npm
            ~/.cache
            node_modules
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: |
          npm run lint
          npm run lint:styles

      - name: Type checking
        run: npm run typecheck

      - name: Security audit
        run: |
          npm audit --production
          npx snyk test

      - name: License check
        run: npx license-checker --production --onlyAllow 'MIT;Apache-2.0;BSD-3-Clause;BSD-2-Clause;ISC'

  # 测试
  test:
    name: Test Suite
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node: [16, 18, 20]
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit -- --coverage

      - name: Run integration tests
        run: npm run test:integration
        env:
          TEST_DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}

      - name: Upload coverage
        if: matrix.os == 'ubuntu-latest' && matrix.node == 18
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          flags: unittests
          name: codecov-umbrella

  # 构建
  build:
    name: Build Application
    needs: [quality, test]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [development, staging, production]
    steps:
      - uses: actions/checkout@v4

      - name: Set up build environment
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build
        env:
          NODE_ENV: ${{ matrix.environment }}
          BUILD_NUMBER: ${{ github.run_number }}
          COMMIT_SHA: ${{ github.sha }}

      - name: Build Docker image
        run: |
          docker build \
            --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
            --build-arg VCS_REF=${GITHUB_SHA::8} \
            --build-arg VERSION=${GITHUB_REF#refs/tags/} \
            -t ${{ github.repository }}:${{ matrix.environment }}-${{ github.sha }} \
            -t ${{ github.repository }}:${{ matrix.environment }}-latest \
            .

      - name: Scan Docker image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ github.repository }}:${{ matrix.environment }}-${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

      - name: Push to registry
        if: github.event_name != 'pull_request'
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push ${{ github.repository }}:${{ matrix.environment }}-${{ github.sha }}
          docker push ${{ github.repository }}:${{ matrix.environment }}-latest

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-${{ matrix.environment }}
          path: |
            dist/
            build/
            .next/
          retention-days: 7

  # 部署
  deploy:
    name: Deploy to ${{ matrix.environment }}
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name != 'pull_request'
    strategy:
      matrix:
        environment: [staging, production]
        exclude:
          - environment: production
            branches: [develop]
    environment:
      name: ${{ matrix.environment }}
      url: ${{ steps.deploy.outputs.url }}
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to ECS
        id: deploy
        run: |
          # 更新任务定义
          aws ecs register-task-definition \
            --family myapp-${{ matrix.environment }} \
            --container-definitions "[{
              \"name\": \"app\",
              \"image\": \"${{ github.repository }}:${{ matrix.environment }}-${{ github.sha }}\",
              \"environment\": [{
                \"name\": \"ENVIRONMENT\",
                \"value\": \"${{ matrix.environment }}\"
              }]
            }]"
          
          # 更新服务
          aws ecs update-service \
            --cluster ${{ matrix.environment }}-cluster \
            --service myapp-service \
            --task-definition myapp-${{ matrix.environment }}
          
          # 获取服务 URL
          echo "url=https://${{ matrix.environment }}.example.com" >> $GITHUB_OUTPUT

      - name: Notify deployment
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: Deployment to ${{ matrix.environment }} ${{ job.status }}
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
        if: always()

  # 部署后验证
  verify:
    name: Verify Deployment
    needs: deploy
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment: [staging, production]
    steps:
      - uses: actions/checkout@v4

      - name: Run smoke tests
        run: |
          npm run test:smoke -- --url https://${{ matrix.environment }}.example.com

      - name: Run E2E tests
        uses: cypress-io/github-action@v5
        with:
          config: baseUrl=https://${{ matrix.environment }}.example.com
          record: true
        env:
          CYPRESS_RECORD_KEY: ${{ secrets.CYPRESS_RECORD_KEY }}

      - name: Performance test
        run: |
          npm install -g @sitespeed.io/sitespeed.io
          sitespeed.io https://${{ matrix.environment }}.example.com \
            --budget.configPath=.sitespeed.io/budget.json \
            --plugins.add=@sitespeed.io/plugin-lighthouse

      - name: Security scan
        run: |
          npm install -g @zaproxy/action-baseline
          zaproxy/action-baseline -t https://${{ matrix.environment }}.example.com
```

### 3. 发布自动化

自动化发布流程：

**语义化发布工作流**
```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches:
      - main

jobs:
  release:
    name: Create Release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          persist-credentials: false

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Run semantic release
        env:
          GITHUB_TOKEN: ${{ secrets.SEMANTIC_RELEASE_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release

      - name: Update documentation
        if: steps.semantic-release.outputs.new_release_published == 'true'
        run: |
          npm run docs:generate
          npm run docs:publish

      - name: Create release notes
        if: steps.semantic-release.outputs.new_release_published == 'true'
        uses: actions/github-script@v6
        with:
          script: |
            const { data: releases } = await github.rest.repos.listReleases({
              owner: context.repo.owner,
              repo: context.repo.repo,
              per_page: 1
            });
            
            const latestRelease = releases[0];
            const changelog = await generateChangelog(latestRelease);
            
            // 更新发布说明
            await github.rest.repos.updateRelease({
              owner: context.repo.owner,
              repo: context.repo.repo,
              release_id: latestRelease.id,
              body: changelog
            });
```

**发布配置**
```javascript
// .releaserc.js
module.exports = {
  branches: [
    'main',
    { name: 'beta', prerelease: true },
    { name: 'alpha', prerelease: true }
  ],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    ['@semantic-release/changelog', {
      changelogFile: 'CHANGELOG.md'
    }],
    '@semantic-release/npm',
    ['@semantic-release/git', {
      assets: ['CHANGELOG.md', 'package.json'],
      message: 'chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}'
    }],
    '@semantic-release/github'
  ]
};
```

### 4. 开发工作流自动化

自动化常见开发任务：

**Pre-commit Hooks**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: check-case-conflict
      - id: check-merge-conflict
      - id: detect-private-key

  - repo: https://github.com/psf/black
    rev: 23.10.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        additional_dependencies: [flake8-docstrings]

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.52.0
    hooks:
      - id: eslint
        files: \.[jt]sx?$
        types: [file]
        additional_dependencies:
          - eslint@8.52.0
          - eslint-config-prettier@9.0.0
          - eslint-plugin-react@7.33.2

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.0.3
    hooks:
      - id: prettier
        types_or: [css, javascript, jsx, typescript, tsx, json, yaml]

  - repo: local
    hooks:
      - id: unit-tests
        name: Run unit tests
        entry: npm run test:unit -- --passWithNoTests
        language: system
        pass_filenames: false
        stages: [commit]
```

**开发环境设置**
```bash
#!/bin/bash
# scripts/setup-dev-environment.sh

set -euo pipefail

echo "🚀 设置开发环境..."

# 检查前置条件
check_prerequisites() {
    echo "检查前置条件..."
    
    commands=("git" "node" "npm" "docker" "docker-compose")
    for cmd in "${commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            echo "❌ $cmd 未安装"
            exit 1
        fi
    done
    
    echo "✅ 所有前置条件已安装"
}

# 安装依赖
install_dependencies() {
    echo "安装依赖..."
    npm ci
    
    # 安装全局工具
    npm install -g @commitlint/cli @commitlint/config-conventional
    npm install -g semantic-release
    
    # 安装 pre-commit
    pip install pre-commit
    pre-commit install
    pre-commit install --hook-type commit-msg
}

# 设置本地服务
setup_services() {
    echo "设置本地服务..."
    
    # 创建 docker 网络
    docker network create dev-network 2>/dev/null || true
    
    # 启动服务
    docker-compose -f docker-compose.dev.yml up -d
    
    # 等待服务就绪
    echo "等待服务就绪..."
    ./scripts/wait-for-services.sh
}

# 初始化数据库
initialize_database() {
    echo "初始化数据库..."
    npm run db:migrate
    npm run db:seed
}

# 设置环境变量
setup_environment() {
    echo "设置环境变量..."
    
    if [ ! -f .env.local ]; then
        cp .env.example .env.local
        echo "✅ 已从 .env.example 创建 .env.local"
        echo "⚠️  请更新 .env.local 中的值"
    fi
}

# 主执行流程
main() {
    check_prerequisites
    install_dependencies
    setup_services
    setup_environment
    initialize_database
    
    echo "✅ 开发环境设置完成！"
    echo ""
    echo "下一步："
    echo "1. 更新 .env.local 中的配置"
    echo "2. 运行 'npm run dev' 启动开发服务器"
    echo "3. 访问 http://localhost:3000"
}

main
```

### 5. 基础设施自动化

自动化基础设施配置：

**Terraform 工作流**
```yaml
# .github/workflows/terraform.yml
name: Terraform

on:
  pull_request:
    paths:
      - 'terraform/**'
      - '.github/workflows/terraform.yml'
  push:
    branches:
      - main
    paths:
      - 'terraform/**'

env:
  TF_VERSION: '1.6.0'
  TF_VAR_project_name: ${{ github.event.repository.name }}

jobs:
  terraform:
    name: Terraform Plan & Apply
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: terraform
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: ${{ env.TF_VERSION }}
          terraform_wrapper: false
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Terraform Format Check
        run: terraform fmt -check -recursive
      
      - name: Terraform Init
        run: |
          terraform init \
            -backend-config="bucket=${{ secrets.TF_STATE_BUCKET }}" \
            -backend-config="key=${{ github.repository }}/terraform.tfstate" \
            -backend-config="region=us-east-1"
      
      - name: Terraform Validate
        run: terraform validate
      
      - name: Terraform Plan
        id: plan
        run: |
          terraform plan -out=tfplan -no-color | tee plan_output.txt
          
          # 提取计划摘要
          echo "PLAN_SUMMARY<<EOF" >> $GITHUB_ENV
          grep -E '(Plan:|No changes.|# )' plan_output.txt >> $GITHUB_ENV
          echo "EOF" >> $GITHUB_ENV
      
      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const output = `#### Terraform Plan 📖
            \`\`\`
            ${process.env.PLAN_SUMMARY}
            \`\`\`
            
            *Pushed by: @${{ github.actor }}, Action: \`${{ github.event_name }}\`*`;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            });
      
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply tfplan
```

### 6. 监控和告警自动化

自动化监控设置：

**监控栈部署**
```yaml
# .github/workflows/monitoring.yml
name: Deploy Monitoring

on:
  push:
    paths:
      - 'monitoring/**'
      - '.github/workflows/monitoring.yml'
    branches:
      - main

jobs:
  deploy-monitoring:
    name: Deploy Monitoring Stack
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Helm
        uses: azure/setup-helm@v3
        with:
          version: '3.12.0'
      
      - name: Configure Kubernetes
        run: |
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig
      
      - name: Add Helm repositories
        run: |
          helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
          helm repo add grafana https://grafana.github.io/helm-charts
          helm repo update
      
      - name: Deploy Prometheus
        run: |
          helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
            --namespace monitoring \
            --create-namespace \
            --values monitoring/prometheus-values.yaml \
            --wait
      
      - name: Deploy Grafana Dashboards
        run: |
          kubectl apply -f monitoring/dashboards/
      
      - name: Deploy Alert Rules
        run: |
          kubectl apply -f monitoring/alerts/
      
      - name: Setup Alert Routing
        run: |
          helm upgrade --install alertmanager prometheus-community/alertmanager \
            --namespace monitoring \
            --values monitoring/alertmanager-values.yaml
```

### 7. 依赖更新自动化

自动化依赖更新：

**Renovate 配置**
```json
{
  "extends": [
    "config:base",
    ":dependencyDashboard",
    ":semanticCommits",
    ":automergeDigest",
    ":automergeMinor"
  ],
  "schedule": ["after 10pm every weekday", "before 5am every weekday", "every weekend"],
  "timezone": "America/New_York",
  "vulnerabilityAlerts": {
    "labels": ["security"],
    "automerge": true
  },
  "packageRules": [
    {
      "matchDepTypes": ["devDependencies"],
      "automerge": true
    },
    {
      "matchPackagePatterns": ["^@types/"],
      "automerge": true
    },
    {
      "matchPackageNames": ["node"],
      "enabled": false
    },
    {
      "matchPackagePatterns": ["^eslint"],
      "groupName": "eslint packages",
      "automerge": true
    },
    {
      "matchManagers": ["docker"],
      "pinDigests": true
    }
  ],
  "postUpdateOptions": [
    "npmDedupe",
    "yarnDedupeHighest"
  ],
  "prConcurrentLimit": 3,
  "prCreation": "not-pending",
  "rebaseWhen": "behind-base-branch",
  "semanticCommitScope": "deps"
}
```

### 8. 文档自动化

自动化文档生成：

**文档工作流**
```yaml
# .github/workflows/docs.yml
name: Documentation

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'docs/**'
      - 'README.md'

jobs:
  generate-docs:
    name: Generate Documentation
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18
      
      - name: Install dependencies
        run: npm ci
      
      - name: Generate API docs
        run: |
          npm run docs:api
          npm run docs:typescript
      
      - name: Generate architecture diagrams
        run: |
          npm install -g @mermaid-js/mermaid-cli
          mmdc -i docs/architecture.mmd -o docs/architecture.png
      
      - name: Build documentation site
        run: |
          npm run docs:build
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/dist
          cname: docs.example.com
```

**文档生成脚本**
```typescript
// scripts/generate-docs.ts
import { Application, TSConfigReader, TypeDocReader } from 'typedoc';
import { generateMarkdown } from './markdown-generator';
import { createApiReference } from './api-reference';

async function generateDocumentation() {
  // 使用 TypeDoc 生成 TypeScript 文档
  const app = new Application();
  app.options.addReader(new TSConfigReader());
  app.options.addReader(new TypeDocReader());
  
  app.bootstrap({
    entryPoints: ['src/index.ts'],
    out: 'docs/api',
    theme: 'default',
    includeVersion: true,
    excludePrivate: true,
    readme: 'README.md',
    plugin: ['typedoc-plugin-markdown']
  });
  
  const project = app.convert();
  if (project) {
    await app.generateDocs(project, 'docs/api');
    
    // 生成自定义 markdown 文档
    await generateMarkdown(project, {
      output: 'docs/guides',
      includeExamples: true,
      generateTOC: true
    });
    
    // 创建 API 参考
    await createApiReference(project, {
      format: 'openapi',
      output: 'docs/openapi.json',
      includeSchemas: true
    });
  }
  
  // 生成架构文档
  await generateArchitectureDocs();
  
  // 生成部署指南
  await generateDeploymentGuides();
}

async function generateArchitectureDocs() {
  const mermaidDiagrams = `
    graph TB
      A[Client] --> B[Load Balancer]
      B --> C[Web Server]
      C --> D[Application Server]
      D --> E[Database]
      D --> F[Cache]
      D --> G[Message Queue]
  `;
  
  // 保存图表并生成文档
  await fs.writeFile('docs/architecture.mmd', mermaidDiagrams);
}
```

### 9. 安全自动化

自动化安全扫描和合规：

**安全扫描工作流**
```yaml
# .github/workflows/security.yml
name: Security Scan

on:
  push:
    branches: [main, develop]
  pull_request:
  schedule:
    - cron: '0 0 * * 0'  # 每周日

jobs:
  security-scan:
    name: Security Scanning
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
      
      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
      
      - name: Run OWASP Dependency Check
        uses: dependency-check/Dependency-Check_Action@main
        with:
          project: ${{ github.repository }}
          path: '.'
          format: 'ALL'
          args: >
            --enableRetired
            --enableExperimental
      
      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
      
      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten
      
      - name: GitLeaks secret scanning
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 10. 工作流编排

创建复杂的工作流编排：

**工作流编排器**
```typescript
// workflow-orchestrator.ts
import { EventEmitter } from 'events';
import { Logger } from 'winston';

interface WorkflowStep {
  name: string;
  type: 'parallel' | 'sequential';
  steps?: WorkflowStep[];
  action?: () => Promise<any>;
  retries?: number;
  timeout?: number;
  condition?: () => boolean;
  onError?: 'fail' | 'continue' | 'retry';
}

export class WorkflowOrchestrator extends EventEmitter {
  constructor(
    private logger: Logger,
    private config: WorkflowConfig
  ) {
    super();
  }
  
  async execute(workflow: WorkflowStep): Promise<WorkflowResult> {
    const startTime = Date.now();
    const result: WorkflowResult = {
      success: true,
      steps: [],
      duration: 0
    };
    
    try {
      await this.executeStep(workflow, result);
    } catch (error) {
      result.success = false;
      result.error = error;
      this.emit('workflow:failed', result);
    }
    
    result.duration = Date.now() - startTime;
    this.emit('workflow:completed', result);
    
    return result;
  }
  
  private async executeStep(
    step: WorkflowStep,
    result: WorkflowResult,
    parentPath: string = ''
  ): Promise<void> {
    const stepPath = parentPath ? `${parentPath}.${step.name}` : step.name;
    
    this.emit('step:start', { step: stepPath });
    
    // 检查条件
    if (step.condition && !step.condition()) {
      this.logger.info(`由于条件不满足，跳过步骤 ${stepPath}`);
      this.emit('step:skipped', { step: stepPath });
      return;
    }
    
    const stepResult: StepResult = {
      name: step.name,
      path: stepPath,
      startTime: Date.now(),
      success: true
    };
    
    try {
      if (step.action) {
        // 执行单个操作
        await this.executeAction(step, stepResult);
      } else if (step.steps) {
        // 执行子步骤
        if (step.type === 'parallel') {
          await this.executeParallel(step.steps, result, stepPath);
        } else {
          await this.executeSequential(step.steps, result, stepPath);
        }
      }
      
      stepResult.endTime = Date.now();
      stepResult.duration = stepResult.endTime - stepResult.startTime;
      result.steps.push(stepResult);
      
      this.emit('step:complete', { step: stepPath, result: stepResult });
    } catch (error) {
      stepResult.success = false;
      stepResult.error = error;
      result.steps.push(stepResult);
      
      this.emit('step:failed', { step: stepPath, error });
      
      if (step.onError === 'fail') {
        throw error;
      }
    }
  }
  
  private async executeAction(
    step: WorkflowStep,
    stepResult: StepResult
  ): Promise<void> {
    const timeout = step.timeout || this.config.defaultTimeout;
    const retries = step.retries || 0;
    
    let lastError: Error;
    
    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const result = await Promise.race([
          step.action!(),
          this.createTimeout(timeout)
        ]);
        
        stepResult.output = result;
        return;
      } catch (error) {
        lastError = error as Error;
        
        if (attempt < retries) {
          this.logger.warn(`步骤 ${step.name} 失败，重试 ${attempt + 1}/${retries}`);
          await this.delay(this.calculateBackoff(attempt));
        }
      }
    }
    
    throw lastError!;
  }
  
  private async executeParallel(
    steps: WorkflowStep[],
    result: WorkflowResult,
    parentPath: string
  ): Promise<void> {
    await Promise.all(
      steps.map(step => this.executeStep(step, result, parentPath))
    );
  }
  
  private async executeSequential(
    steps: WorkflowStep[],
    result: WorkflowResult,
    parentPath: string
  ): Promise<void> {
    for (const step of steps) {
      await this.executeStep(step, result, parentPath);
    }
  }
  
  private createTimeout(ms: number): Promise<never> {
    return new Promise((_, reject) => {
      setTimeout(() => reject(new Error(`${ms}ms 后超时`)), ms);
    });
  }
  
  private calculateBackoff(attempt: number): number {
    return Math.min(1000 * Math.pow(2, attempt), 30000);
  }
  
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// 示例工作流定义
export const deploymentWorkflow: WorkflowStep = {
  name: 'deployment',
  type: 'sequential',
  steps: [
    {
      name: 'pre-deployment',
      type: 'parallel',
      steps: [
        {
          name: 'backup-database',
          action: async () => {
            // 备份数据库
          },
          timeout: 300000 // 5 分钟
        },
        {
          name: 'health-check',
          action: async () => {
            // 检查系统健康状态
          },
          retries: 3
        }
      ]
    },
    {
      name: 'deployment',
      type: 'sequential',
      steps: [
        {
          name: 'blue-green-switch',
          action: async () => {
            // 将流量切换到新版本
          },
          onError: 'retry',
          retries: 2
        },
        {
          name: 'smoke-tests',
          action: async () => {
            // 运行冒烟测试
          },
          onError: 'fail'
        }
      ]
    },
    {
      name: 'post-deployment',
      type: 'parallel',
      steps: [
        {
          name: 'notify-teams',
          action: async () => {
            // 发送通知
          },
          onError: 'continue'
        },
        {
          name: 'update-monitoring',
          action: async () => {
            // 更新监控仪表盘
          }
        }
      ]
    }
  ]
};
```

## 输出格式

1. **工作流分析**：当前流程和自动化机会
2. **CI/CD 流水线**：完整的 GitHub Actions/GitLab CI 配置
3. **发布自动化**：语义化版本和发布工作流
4. **开发自动化**：Pre-commit hooks 和设置脚本
5. **基础设施自动化**：Terraform 和 Kubernetes 工作流
6. **安全自动化**：扫描和合规工作流
7. **文档生成**：自动化文档和图表
8. **工作流编排**：复杂工作流管理
9. **监控集成**：自动化告警和仪表盘
10. **实施指南**：分步设置说明

专注于创建可靠、可维护的自动化方案，在保持质量和安全标准的同时减少手工工作。
