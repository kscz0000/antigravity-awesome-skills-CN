---
name: deployment-pipeline-design
description: "多阶段 CI/CD 流水线的架构模式，包含审批门控和部署策略。当用户要求'设计部署流水线'、'CI/CD架构'、'部署策略'、'审批门控'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# 部署流水线设计

多阶段 CI/CD 流水线的架构模式，包含审批门控和部署策略。

## 不适用场景

- 任务与部署流水线设计无关
- 需要此范围之外的其他领域或工具

## 指导说明

- 明确目标、约束条件和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 目的

设计健壮、安全的部署流水线，通过合理的阶段组织和审批工作流，在速度与安全之间取得平衡。

## 适用场景

- 设计 CI/CD 架构
- 实现部署门控
- 配置多环境流水线
- 建立部署最佳实践
- 实现渐进式交付

## 流水线阶段

### 标准流水线流程

```
┌─────────┐   ┌──────┐   ┌─────────┐   ┌────────┐   ┌──────────┐
│  Build  │ → │ Test │ → │ Staging │ → │ Approve│ → │Production│
└─────────┘   └──────┘   └─────────┘   └────────┘   └──────────┘
```

### 详细阶段分解

1. **Source** - 代码检出
2. **Build** - 编译、打包、容器化
3. **Test** - 单元测试、集成测试、安全扫描
4. **Staging Deploy** - 部署到预发布环境
5. **Integration Tests** - E2E 测试、冒烟测试
6. **Approval Gate** - 需要人工审批
7. **Production Deploy** - 金丝雀、蓝绿、滚动部署
8. **Verification** - 健康检查、监控
9. **Rollback** - 失败时自动回滚

## 审批门控模式

### 模式 1：人工审批

```yaml
# GitHub Actions
production-deploy:
  needs: staging-deploy
  environment:
    name: production
    url: https://app.example.com
  runs-on: ubuntu-latest
  steps:
    - name: Deploy to production
      run: |
        # Deployment commands
```

### 模式 2：基于时间的审批

```yaml
# GitLab CI
deploy:production:
  stage: deploy
  script:
    - deploy.sh production
  environment:
    name: production
  when: delayed
  start_in: 30 minutes
  only:
    - main
```

### 模式 3：多审批人

```yaml
# Azure Pipelines
stages:
- stage: Production
  dependsOn: Staging
  jobs:
  - deployment: Deploy
    environment:
      name: production
      resourceType: Kubernetes
    strategy:
      runOnce:
        preDeploy:
          steps:
          - task: ManualValidation@0
            inputs:
              notifyUsers: 'team-leads@example.com'
              instructions: 'Review staging metrics before approving'
```

**参考：** 参见 `assets/approval-gate-template.yml`

## 部署策略

### 1. 滚动部署

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
```

**特点：**
- 渐进式发布
- 零停机
- 易于回滚
- 适用于大多数应用

### 2. 蓝绿部署

```yaml
# Blue (current)
kubectl apply -f blue-deployment.yaml
kubectl label service my-app version=blue

# Green (new)
kubectl apply -f green-deployment.yaml
# Test green environment
kubectl label service my-app version=green

# Rollback if needed
kubectl label service my-app version=blue
```

**特点：**
- 即时切换
- 易于回滚
- 临时增加一倍基础设施成本
- 适用于高风险部署

### 3. 金丝雀部署

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    canary:
      steps:
      - setWeight: 10
      - pause: {duration: 5m}
      - setWeight: 25
      - pause: {duration: 5m}
      - setWeight: 50
      - pause: {duration: 5m}
      - setWeight: 100
```

**特点：**
- 渐进式流量转移
- 风险缓解
- 真实用户测试
- 需要服务网格或类似技术

### 4. 功能开关

```python
from flagsmith import Flagsmith

flagsmith = Flagsmith(environment_key="API_KEY")

if flagsmith.has_feature("new_checkout_flow"):
    # New code path
    process_checkout_v2()
else:
    # Existing code path
    process_checkout_v1()
```

**特点：**
- 部署而不发布
- A/B 测试
- 即时回滚
- 细粒度控制

## 流水线编排

### 多阶段流水线示例

```yaml
name: Production Pipeline

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build application
        run: make build
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: docker push myapp:${{ github.sha }}

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Unit tests
        run: make test
      - name: Security scan
        run: trivy image myapp:${{ github.sha }}

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    environment:
      name: staging
    steps:
      - name: Deploy to staging
        run: kubectl apply -f k8s/staging/

  integration-test:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - name: Run E2E tests
        run: npm run test:e2e

  deploy-production:
    needs: integration-test
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - name: Canary deployment
        run: |
          kubectl apply -f k8s/production/
          kubectl argo rollouts promote my-app

  verify:
    needs: deploy-production
    runs-on: ubuntu-latest
    steps:
      - name: Health check
        run: curl -f https://app.example.com/health
      - name: Notify team
        run: |
          curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
            -d '{"text":"Production deployment successful!"}'
```

## 流水线最佳实践

1. **快速失败** - 优先运行快速测试
2. **并行执行** - 并发运行独立的作业
3. **缓存** - 在运行之间缓存依赖
4. **制品管理** - 存储构建产物
5. **环境一致性** - 保持环境一致
6. **密钥管理** - 使用密钥存储（Vault 等）
7. **部署窗口** - 合理安排部署时间
8. **监控集成** - 追踪部署指标
9. **回滚自动化** - 失败时自动回滚
10. **文档化** - 记录流水线阶段

## 回滚策略

### 自动回滚

```yaml
deploy-and-verify:
  steps:
    - name: Deploy new version
      run: kubectl apply -f k8s/

    - name: Wait for rollout
      run: kubectl rollout status deployment/my-app

    - name: Health check
      id: health
      run: |
        for i in {1..10}; do
          if curl -sf https://app.example.com/health; then
            exit 0
          fi
          sleep 10
        done
        exit 1

    - name: Rollback on failure
      if: failure()
      run: kubectl rollout undo deployment/my-app
```

### 手动回滚

```bash
# List revision history
kubectl rollout history deployment/my-app

# Rollback to previous version
kubectl rollout undo deployment/my-app

# Rollback to specific revision
kubectl rollout undo deployment/my-app --to-revision=3
```

## 监控与指标

### 关键流水线指标

- **部署频率** - 部署发生的频率
- **交付周期** - 从提交到生产的时间
- **变更失败率** - 失败部署的百分比
- **平均恢复时间 (MTTR)** - 从故障中恢复的时间
- **流水线成功率** - 成功运行的百分比
- **平均流水线时长** - 完成流水线的时间

### 与监控集成

```yaml
- name: Post-deployment verification
  run: |
    # Wait for metrics stabilization
    sleep 60

    # Check error rate
    ERROR_RATE=$(curl -s "$PROMETHEUS_URL/api/v1/query?query=rate(http_errors_total[5m])" | jq '.data.result[0].value[1]')

    if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
      echo "Error rate too high: $ERROR_RATE"
      exit 1
    fi
```

## 参考文件

- `references/pipeline-orchestration.md` - 复杂流水线模式
- `assets/approval-gate-template.yml` - 审批工作流模板

## 相关技能

- `github-actions-templates` - 用于 GitHub Actions 实现
- `gitlab-ci-patterns` - 用于 GitLab CI 实现
- `secrets-management` - 用于密钥处理

## 局限性
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
