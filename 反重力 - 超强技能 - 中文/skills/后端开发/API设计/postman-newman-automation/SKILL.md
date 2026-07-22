---
name: postman-newman-automation
description: 生成 Newman CLI 命令、配置文件、Jenkins 流水线脚本和 Shell 自动化脚本，用于在 CI/CD 或本地环境中运行 Postman 集合。当用户想要从命令行运行 Postman 集合、自动化 API 测试、集成 Postman 测试到 CI/CD 流水线、生成 Newman 运行脚本或配置 Jenkins 报告时使用此技能。触发词：Newman、Postman CLI、API 测试自动化、CI/CD 集成、Jenkins 流水线、集合运行器、命令行测试、Newman 报告、htmlextra、Postman 自动化。
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/api-skill/postman/postman-to-newman
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# Postman Newman 自动化

## 何时使用

当你需要生成 Newman CLI 命令、配置文件、Jenkins 流水线脚本和 Shell 自动化脚本，用于在 CI/CD 或本地环境中运行 Postman 集合时使用此技能。当用户想要从命令行运行 Postman 集合、自动化 API 测试、集成 Postman 测试到 CI/CD 流水线时使用。

生成 **Newman CLI** 命令、**Shell 脚本**和 **Jenkins 流水线**配置，
用于在自动化环境中运行 Postman 集合。

---

## Newman 基础

Newman 是 Postman 的 CLI 运行器。安装方式：
```bash
npm install -g newman
# Optional HTML reporter:
npm install -g newman-reporter-htmlextra
```

### 核心命令结构
```bash
newman run <collection> \
  --environment <env-file> \
  --globals <globals-file> \
  --iteration-count <n> \
  --iteration-data <csv-or-json> \
  --reporters <reporter-list> \
  --reporter-htmlextra-export <output.html> \
  --reporter-junit-export <results.xml> \
  --timeout-request <ms> \
  --delay-request <ms> \
  --bail \
  --color on
```

---

## 步骤 1 — 收集需求

询问或从上下文推断：

| 参数 | 问题 |
|---|---|
| 集合来源 | 文件路径、URL 还是 Postman API UID？ |
| 环境 | 文件路径还是内联变量？ |
| 报告器 | 仅 CLI、HTML 报告还是 JUnit XML？ |
| 失败行为 | 首次失败即停止（`--bail`）还是运行全部？ |
| 迭代次数 | 单次运行还是数据驱动（CSV/JSON）？ |
| 目标环境 | 本地 Shell、Jenkins 还是两者？ |

---

## 步骤 2 — 生成 Newman 命令

### 基本运行（本地）
```bash
newman run collection.json \
  --environment environment.json \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export reports/report.html \
  --bail
```

### 从 Postman API 运行（按 UID）
```bash
newman run "https://api.getpostman.com/collections/<UID>?apikey={{POSTMAN_API_KEY}}" \
  --environment environment.json \
  --reporters cli,junit \
  --reporter-junit-export results/junit.xml
```

### 数据驱动运行（CSV）
```bash
newman run collection.json \
  --iteration-data test-data.csv \
  --iteration-count 5 \
  --reporters cli,htmlextra \
  --reporter-htmlextra-export reports/data-driven-report.html
```

### 使用环境变量覆盖（无需文件）
```bash
newman run collection.json \
  --env-var "base_url=https://staging.api.example.com" \
  --env-var "token=abc123" \
  --reporters cli
```

---

## 步骤 3 — Shell 脚本

生成可复用的 Shell 脚本：

```bash
#!/bin/bash
set -e

# Configuration
COLLECTION="./collection.json"
ENVIRONMENT="./environment.json"
REPORT_DIR="./reports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Ensure report directory exists
mkdir -p "$REPORT_DIR"

echo "Running Newman collection: $COLLECTION"

newman run "$COLLECTION" \
  --environment "$ENVIRONMENT" \
  --reporters cli,htmlextra,junit \
  --reporter-htmlextra-export "$REPORT_DIR/report_$TIMESTAMP.html" \
  --reporter-junit-export "$REPORT_DIR/junit_$TIMESTAMP.xml" \
  --timeout-request 10000 \
  --bail

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "✅ All tests passed."
else
  echo "❌ Tests failed. Check report: $REPORT_DIR/report_$TIMESTAMP.html"
  exit $EXIT_CODE
fi
```

---

## 步骤 4 — Jenkins 流水线

### 声明式 Jenkinsfile（推荐）

```groovy
pipeline {
  agent any

  environment {
    POSTMAN_ENV = credentials('postman-environment-file') // Jenkins credential ID
  }

  stages {
    stage('Install Newman') {
      steps {
        sh 'npm install -g newman newman-reporter-htmlextra'
      }
    }

    stage('Run API Tests') {
      steps {
        sh """
          newman run collection.json \\
            --environment ${POSTMAN_ENV} \\
            --reporters cli,htmlextra,junit \\
            --reporter-htmlextra-export reports/report.html \\
            --reporter-junit-export reports/junit.xml \\
            --timeout-request 10000 \\
            --bail
        """
      }
    }
  }

  post {
    always {
      // Archive HTML report
      publishHTML(target: [
        allowMissing: false,
        alwaysLinkToLastBuild: true,
        keepAll: true,
        reportDir: 'reports',
        reportFiles: 'report.html',
        reportName: 'Newman API Test Report'
      ])
      // Archive JUnit results
      junit 'reports/junit.xml'
    }
    failure {
      echo 'API tests failed! Check the Newman report.'
    }
  }
}
```

### 脚本式 Jenkinsfile（当声明式不可用时）

```groovy
node {
  stage('Install Newman') {
    sh 'npm install -g newman newman-reporter-htmlextra'
  }

  stage('Run API Tests') {
    try {
      sh """
        newman run collection.json \\
          --environment environment.json \\
          --reporters cli,junit \\
          --reporter-junit-export reports/junit.xml \\
          --bail
      """
    } catch (err) {
      currentBuild.result = 'FAILURE'
      throw err
    } finally {
      junit 'reports/junit.xml'
    }
  }
}
```

### Jenkins 使用环境变量（无凭据文件）
```groovy
environment {
  BASE_URL = 'https://api.example.com'
  API_TOKEN = credentials('api-token-secret')
}

steps {
  sh """
    newman run collection.json \\
      --env-var "base_url=${BASE_URL}" \\
      --env-var "token=${API_TOKEN}" \\
      --reporters cli,junit \\
      --reporter-junit-export results/junit.xml
  """
}
```

---

## 步骤 5 — 报告器参考

| 报告器 | 安装方式 | 标志 | 输出 |
|---|---|---|---|
| `cli` | 内置 | `--reporters cli` | 终端输出 |
| `junit` | 内置 | `--reporters junit` | JUnit XML（用于 Jenkins） |
| `htmlextra` | `npm i -g newman-reporter-htmlextra` | `--reporters htmlextra` | 富文本 HTML 报告 |
| `json` | 内置 | `--reporters json` | 原始 JSON 结果 |

多个报告器：`--reporters cli,htmlextra,junit`

---

## 步骤 6 — 输出

根据用户需求提供：

1. **Newman 命令** — 可直接粘贴到终端
2. **Shell 脚本**（`run-tests.sh`）— 含退出码处理
3. **Jenkinsfile** — 根据上下文选择声明式或脚本式
4. **安装说明** — Node.js 版本要求（≥14）、npm 安装命令
5. **报告位置** — 输出文件的写入路径

---

## 常用标志速查

| 标志 | 用途 |
|---|---|
| `--bail` | 首次测试失败时停止运行 |
| `--timeout-request 5000` | 单请求超时（毫秒） |
| `--delay-request 200` | 请求间延迟（毫秒） |
| `--iteration-count 3` | 运行集合 N 次 |
| `--folder "Folder Name"` | 仅运行指定文件夹 |
| `--env-var "k=v"` | 内联环境变量 |
| `--suppress-exit-code` | 始终以退出码 0 退出（不使 CI 失败） |
| `--verbose` | 显示完整请求/响应详情 |
| `--color off` | 禁用颜色（适用于日志） |

---

## 完成 Newman 命令后

交付 CLI 命令输出后，询问用户：

"是否需要我为这个设计生成 API 文档？（是/否）"

如果用户回答**是**：
- 检查已安装技能列表中是否有 API 文档技能
- 如果技能**可用**：
  - 阅读并遵循 API 文档技能中的说明
  - 使用上面的 API 设计输出作为输入
  - 以纯文本形式交付文档
- 如果技能**不可用**：
  - 告知用户："看起来 API 文档技能未安装。你可以安装后重新运行。"

如果用户回答**否**：
- 在此结束任务

---

## 限制

- 仅当任务明确匹配其上游来源和本地项目上下文时使用此技能。
- 在应用更改前，验证命令、生成的代码、依赖项、凭据和外部服务行为。
- 不要将示例替代环境特定的测试、安全审查或用户对破坏性/高成本操作的审批。
