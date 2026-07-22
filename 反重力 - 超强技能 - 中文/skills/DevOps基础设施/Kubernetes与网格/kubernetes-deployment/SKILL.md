---
name: kubernetes-deployment
description: "Kubernetes 部署工作流，涵盖容器编排、Helm Charts、服务网格及生产级 K8s 配置。触发词：K8s部署、Kubernetes部署、Helm Chart、服务网格、容器编排、K8s配置"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Kubernetes 部署工作流

## 概述

面向 Kubernetes 应用部署的专业工作流，涵盖容器编排、Helm Charts、服务网格配置及生产级 K8s 模式。

## 适用场景

在以下场景使用本工作流：
- 部署应用到 Kubernetes
- 创建 Helm Charts
- 配置服务网格
- 搭建 K8s 网络
- 实施 K8s 安全策略

## 工作流阶段

### 阶段 1：容器准备

#### 调用技能
- `docker-expert` - Docker 容器化
- `k8s-manifest-generator` - K8s 清单

#### 操作步骤
1. 创建 Dockerfile
2. 构建容器镜像
3. 优化镜像体积
4. 推送到镜像仓库
5. 测试容器

#### 复制粘贴提示词
```
Use @docker-expert to containerize application for K8s
```

### 阶段 2：K8s 清单

#### 调用技能
- `k8s-manifest-generator` - 清单生成
- `kubernetes-architect` - K8s 架构

#### 操作步骤
1. 创建 Deployment
2. 配置 Service
3. 设置 ConfigMap
4. 创建 Secrets
5. 添加 Ingress

#### 复制粘贴提示词
```
Use @k8s-manifest-generator to create K8s manifests
```

### 阶段 3：Helm Chart

#### 调用技能
- `helm-chart-scaffolding` - Helm Charts

#### 操作步骤
1. 创建 Chart 目录结构
2. 定义 values.yaml
3. 添加模板
4. 配置依赖
5. 测试 Chart

#### 复制粘贴提示词
```
Use @helm-chart-scaffolding to create Helm chart
```

### 阶段 4：服务网格

#### 调用技能
- `istio-traffic-management` - Istio
- `linkerd-patterns` - Linkerd
- `service-mesh-expert` - 服务网格

#### 操作步骤
1. 选择服务网格方案
2. 安装服务网格
3. 配置流量管理
4. 设置 mTLS
5. 添加可观测性

#### 复制粘贴提示词
```
Use @istio-traffic-management to configure Istio
```

### 阶段 5：安全

#### 调用技能
- `k8s-security-policies` - K8s 安全
- `mtls-configuration` - mTLS

#### 操作步骤
1. 配置 RBAC
2. 设置 NetworkPolicy
3. 启用 PodSecurity
4. 配置 Secrets
5. 实施 mTLS

#### 复制粘贴提示词
```
Use @k8s-security-policies to secure Kubernetes cluster
```

### 阶段 6：可观测性

#### 调用技能
- `grafana-dashboards` - Grafana
- `prometheus-configuration` - Prometheus

#### 操作步骤
1. 安装监控组件栈
2. 配置 Prometheus
3. 创建 Grafana 仪表盘
4. 设置告警
5. 添加分布式追踪

#### 复制粘贴提示词
```
Use @prometheus-configuration to set up K8s monitoring
```

### 阶段 7：部署

#### 调用技能
- `deployment-engineer` - 部署
- `gitops-workflow` - GitOps

#### 操作步骤
1. 配置 CI/CD
2. 搭建 GitOps
3. 部署到集群
4. 验证部署
5. 监控发布

#### 复制粘贴提示词
```
Use @gitops-workflow to implement GitOps deployment
```

## 质量门控

- [ ] 容器运行正常
- [ ] 清单校验通过
- [ ] Helm Chart 可安装
- [ ] 安全配置就绪
- [ ] 监控已激活
- [ ] 部署成功

## 相关工作流

- `cloud-devops` - 云/DevOps
- `terraform-infrastructure` - 基础设施
- `docker-containerization` - 容器

## 限制
- 仅当任务明确符合上述范围时使用本技能。
- 输出内容不可替代针对具体环境的验证、测试或专家评审。
- 若缺少必要的输入、权限、安全边界或成功标准，请停止并请求澄清。
