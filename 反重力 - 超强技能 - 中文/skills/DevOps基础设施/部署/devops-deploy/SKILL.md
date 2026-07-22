---
name: devops-deploy
description: "DevOps 和应用部署 — Docker、GitHub Actions CI/CD、AWS Lambda、SAM、Terraform、基础设施即代码和监控。当用户要求'Docker化应用、配置CI/CD流水线、AWS部署、Lambda、ECS、GitHub Actions、Terraform、回滚、蓝绿部署、健康检查、告警'时使用。"
risk: critical
source: community
date_added: '2026-03-06'
author: renat
tags:
- devops
- docker
- ci-cd
- aws
- terraform
- github-actions
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
---

# DEVOPS-DEPLOY — 从想法到生产

## 概述

DevOps 和应用部署 — Docker、GitHub Actions CI/CD、AWS Lambda、SAM、Terraform、基础设施即代码和监控。适用于：Docker化应用、配置CI/CD流水线、AWS部署、Lambda、ECS、GitHub Actions配置、Terraform、回滚、蓝绿部署、健康检查、告警。

## 何时使用此技能

- 当你需要该领域的专业协助时

## 何时不使用此技能

- 任务与 devops deploy 无关
- 更简单、更具体的工具可以处理该请求
- 用户需要无领域专业知识的一般性协助

## 工作原理

> "快速行动，但不破坏事物。" — 精英工程不是慢的。
> 它是既快速又可靠的。

---

## 优化的 Dockerfile（Python）

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Docker Compose（本地开发）

```yaml
version: "3.9"
services:
  app:
    build: .
    ports: ["8000:8000"]
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - .:/app
    depends_on: [db, redis]
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: auri
      POSTGRES_USER: auri
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
  redis:
    image: redis:7-alpine
volumes:
  pgdata:
```

---

## SAM 模板（Serverless）

```yaml

## Template.Yaml

AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    Runtime: python3.11
    Environment:
      Variables:
        ANTHROPIC_API_KEY: !Ref AnthropicApiKey
        DYNAMODB_TABLE: !Ref AuriTable

Resources:
  AuriFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: lambda_function.handler
      MemorySize: 512
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref AuriTable

  AuriTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: auri-users
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: userId
          AttributeType: S
      KeySchema:
        - AttributeName: userId
          KeyType: HASH
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
```

## 部署命令

```bash

## 构建和部署

sam build
sam deploy --guided  # 首次部署
sam deploy           # 后续部署

## 快速部署（无需确认）

sam deploy --no-confirm-changeset --no-fail-on-empty-changeset

## 实时查看日志

sam logs -n AuriFunction --tail

## 删除堆栈

sam delete
```

---

## .Github/Workflows/Deploy.Yml

name: Deploy Auri

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v4

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install bandit safety
      - run: bandit -r src/ -ll
      - run: safety check -r requirements.txt

  deploy:
    needs: [test, security]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/setup-sam@v2
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - run: sam build
      - run: sam deploy --no-confirm-changeset
      - name: Notify Telegram on Success
        run: |
          curl -s -X POST "https://api.telegram.org/bot${{ secrets.TELEGRAM_BOT_TOKEN }}/sendMessage" \
            -d "chat_id=${{ secrets.TELEGRAM_CHAT_ID }}" \
            -d "text=Auri deployed successfully! Commit: ${{ github.sha }}"
```

---

## 健康检查端点

```python
from fastapi import FastAPI
import time, os

app = FastAPI()
START_TIME = time.time()

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "uptime_seconds": time.time() - START_TIME,
        "version": os.environ.get("APP_VERSION", "unknown"),
        "environment": os.environ.get("ENV", "production")
    }
```

## CloudWatch 告警

```python
import boto3

def create_error_alarm(function_name: str, sns_topic_arn: str):
    cw = boto3.client("cloudwatch")
    cw.put_metric_alarm(
        AlarmName=f"{function_name}-errors",
        MetricName="Errors",
        Namespace="AWS/Lambda",
        Dimensions=[{"Name": "FunctionName", "Value": function_name}],
        Period=300,
        EvaluationPeriods=1,
        Threshold=5,
        ComparisonOperator="GreaterThanThreshold",
        AlarmActions=[sns_topic_arn],
        TreatMissingData="notBreaching"
    )
```

---

## 5. 生产检查清单

- [ ] 通过 Secrets Manager 配置环境变量（绝不硬编码）
- [ ] 健康检查端点正常响应
- [ ] 结构化日志（JSON）包含 request_id
- [ ] 已配置速率限制
- [ ] CORS 限制为授权域名
- [ ] DynamoDB 已启用自动备份
- [ ] Lambda 超时设置合理（10-30秒）
- [ ] CloudWatch 告警监控错误和延迟
- [ ] 已记录回滚计划
- [ ] 上线前进行负载测试

---

## 6. 命令

| 命令 | 操作 |
|---------|------|
| `/docker-setup` | Docker 化应用 |
| `/sam-deploy` | 完整部署到 AWS Lambda |
| `/ci-cd-setup` | 配置 GitHub Actions 流水线 |
| `/monitoring-setup` | 配置 CloudWatch 和告警 |
| `/production-checklist` | 运行上线前检查清单 |
| `/rollback` | 回滚到上一版本的计划 |

## 最佳实践

- 提供清晰、具体的项目上下文和需求
- 在应用到生产代码前审查所有建议
- 结合其他互补技能进行全面分析

## 常见陷阱

- 将此技能用于其专业领域之外的任务
- 在不了解具体上下文的情况下应用建议
- 未提供足够的项目上下文以进行准确分析

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
