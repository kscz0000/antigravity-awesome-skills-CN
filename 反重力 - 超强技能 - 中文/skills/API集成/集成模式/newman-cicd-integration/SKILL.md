---
name: newman-cicd-integration
description: 生成可直接使用的 CI/CD 管道配置，安装并运行 Newman 进行自动化 API 测试。当用户想要在 CI 管道中运行 Newman、将 Postman 集合集成到自动化构建中、在 GitHub Actions、GitLab CI、Jenkins 等平台设置 API 测试时使用此技能。
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/api-skill/newman/newman-cicd-helper
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# Newman CI/CD 集成生成器
## 使用场景

当需要生成可直接使用的 CI/CD 管道配置来安装 Newman 并运行自动化 API 测试时使用此技能。当用户想要在 CI 管道中运行 Newman、将 Postman 集合集成到自动化构建中、在 GitHub Actions、GitLab CI、Jenkins 等平台设置 API 测试时触发。


生成完整、可直接复制粘贴的 CI/CD 管道配置，将 Newman 安装和 Postman 集合运行作为自动化构建的一部分。

---

## 需要从用户收集的信息

生成配置前，需确认：
1. **CI 平台** — GitHub Actions、GitLab CI、Jenkins、Azure DevOps、CircleCI、Bitbucket？
2. **集合来源** — 仓库中的本地文件，还是 Postman API URL？
3. **环境配置** — 仓库中的本地环境文件，还是通过 CI 密钥注入的环境变量？
4. **所需报告器** — JUnit XML（用于 CI 测试结果面板）、HTML 报告，还是两者都要？
5. **Node.js 版本**偏好（默认：18）
6. **触发条件** — 每次推送、拉取请求、定时任务，还是部署后？
7. **测试失败时是否中断构建？** — 几乎总是需要；请确认

---

## 平台模板

### GitHub Actions

```yaml
name: API Tests

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  api-tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install Newman
        run: |
          npm install -g newman
          npm install -g newman-reporter-htmlextra

      - name: Run API tests
        run: |
          newman run ./collections/my-api.json \
            -e ./environments/staging.json \
            -r cli,junit,htmlextra \
            --reporter-junit-export ./results/junit.xml \
            --reporter-htmlextra-export ./results/report.html \
            --reporter-htmlextra-title "API Test Results"
        env:
          BASE_URL: ${{ secrets.BASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}

      - name: Publish test results
        uses: dorny/test-reporter@v1
        if: always()
        with:
          name: Newman API Tests
          path: results/junit.xml
          reporter: java-junit

      - name: Upload HTML report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: api-test-report
          path: results/report.html
```

---

### GitLab CI

```yaml
stages:
  - test

api-tests:
  stage: test
  image: node:18-alpine
  before_script:
    - npm install -g newman newman-reporter-htmlextra
  script:
    - |
      newman run ./collections/my-api.json \
        -e ./environments/staging.json \
        --env-var "BASE_URL=$BASE_URL" \
        --env-var "API_KEY=$API_KEY" \
        -r cli,junit,htmlextra \
        --reporter-junit-export results/junit.xml \
        --reporter-htmlextra-export results/report.html
  artifacts:
    when: always
    reports:
      junit: results/junit.xml
    paths:
      - results/report.html
    expire_in: 7 days
  variables:
    BASE_URL: $BASE_URL   # Set in GitLab CI/CD > Variables
    API_KEY: $API_KEY
```

---

### Jenkins（声明式管道）

```groovy
pipeline {
  agent any

  tools {
    nodejs 'NodeJS-18'   // Configure in Global Tool Configuration
  }

  stages {
    stage('Install Newman') {
      steps {
        sh 'npm install -g newman newman-reporter-htmlextra'
      }
    }

    stage('Run API Tests') {
      steps {
        sh '''
          newman run ./collections/my-api.json \
            -e ./environments/staging.json \
            -r cli,junit,htmlextra \
            --reporter-junit-export results/junit.xml \
            --reporter-htmlextra-export results/report.html \
            --reporter-htmlextra-title "API Tests - ${BUILD_NUMBER}"
        '''
      }
    }
  }

  post {
    always {
      junit 'results/junit.xml'
      publishHTML([
        allowMissing: false,
        alwaysLinkToLastBuild: true,
        keepAll: true,
        reportDir: 'results',
        reportFiles: 'report.html',
        reportName: 'Newman API Test Report'
      ])
    }
  }
}
```

---

### Azure DevOps

```yaml
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: '18.x'
    displayName: 'Set up Node.js'

  - script: |
      npm install -g newman newman-reporter-htmlextra
    displayName: 'Install Newman'

  - script: |
      newman run ./collections/my-api.json \
        -e ./environments/staging.json \
        --env-var "API_KEY=$(API_KEY)" \
        -r cli,junit,htmlextra \
        --reporter-junit-export $(System.DefaultWorkingDirectory)/results/junit.xml \
        --reporter-htmlextra-export $(System.DefaultWorkingDirectory)/results/report.html
    displayName: 'Run API Tests'
    env:
      API_KEY: $(API_KEY)   # Set in Pipeline > Variables

  - task: PublishTestResults@2
    condition: always()
    inputs:
      testResultsFormat: 'JUnit'
      testResultsFiles: 'results/junit.xml'
      testRunTitle: 'Newman API Tests'

  - task: PublishBuildArtifacts@1
    condition: always()
    inputs:
      PathtoPublish: 'results/report.html'
      ArtifactName: 'api-test-report'
```

---

### CircleCI

```yaml
version: 2.1

jobs:
  api-tests:
    docker:
      - image: cimg/node:18.0
    steps:
      - checkout
      - run:
          name: Install Newman
          command: npm install -g newman newman-reporter-htmlextra
      - run:
          name: Run API Tests
          command: |
            mkdir -p results
            newman run ./collections/my-api.json \
              -e ./environments/staging.json \
              --env-var "API_KEY=$API_KEY" \
              -r cli,junit,htmlextra \
              --reporter-junit-export results/junit.xml \
              --reporter-htmlextra-export results/report.html
      - store_test_results:
          path: results
      - store_artifacts:
          path: results/report.html

workflows:
  test:
    jobs:
      - api-tests
```

---

## 最佳实践

### 密钥管理 — 禁止硬编码凭据
始终将敏感值作为 CI 环境变量/密钥注入：
- GitHub：`Settings > Secrets and Variables > Actions`
- GitLab：`Settings > CI/CD > Variables`
- Jenkins：`Manage Jenkins > Credentials`
- Azure DevOps：`Pipelines > Variables`

通过 `--env-var "KEY=$SECRET_NAME"` 在 Newman 中引用，或在环境文件中预先设置。

### 将集合和环境文件存储在仓库中
```
/
├── collections/
│   └── my-api.json
├── environments/
│   ├── staging.json
│   └── prod.json
└── results/         ← gitignored，由 Newman 创建
```

将 `results/` 添加到 `.gitignore`。

### 始终使用 `if: always()` / `when: always`
确保即使 Newman 以失败代码退出，测试结果产物也会被发布。

### 退出码
如果任何测试失败，Newman 会以代码 `1` 退出 — 这会自动使管道步骤失败。如果想遇到第一个失败就停止而非运行所有测试，可使用 `--bail`。

---

## 如何生成配置

1. 确认 CI 平台并适配准确语法
2. 使用该平台正确的密钥/变量注入语法
3. 包含产物发布步骤，使测试结果显示在 CI 界面中
4. 添加注释说明需要配置的密钥
5. 将环境文件保留在仓库中（不含密钥）；通过 CI 变量注入敏感值

---

## 完成 Newman CICD 输出后

交付 Newman CICD 输出后，询问用户：

"是否需要我为这些命令生成 Postman 测试用例？（yes/no）"

如果用户回答 **yes**：
- 检查已安装技能列表中是否有 postman-testcase-generator 技能
- 如果技能**可用**：
  - 阅读并遵循 postman-testcase-generator 技能中的说明
  - 将上述 CICD 命令输出作为输入
- 如果技能**不可用**：
  - 通知用户："postman-testcase-generator 技能未安装。您可以安装后重新运行。"

如果用户回答 **no**：
- 任务至此结束

---

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 应用变更前，验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例替代为环境特定测试、安全审查或用户对破坏性或高成本操作的批准。