---
name: azd-deployment
description: "将容器化前端+后端应用部署到 Azure Container Apps，支持远程构建、托管身份和幂等基础设施。触发词：azd部署、Azure部署、容器应用部署、Azure Container Apps、azd up、Bicep部署、云部署、Azure Developer CLI"
risk: critical
source: community
date_added: "2026-02-27"
---

# Azure Developer CLI (azd) Container Apps 部署

将容器化前端+后端应用部署到 Azure Container Apps，支持远程构建、托管身份和幂等基础设施。

## 快速开始

```bash
# 初始化并部署
azd auth login
azd init                    # 创建 azure.yaml 和 .azure/ 文件夹
azd env new <env-name>      # 创建环境 (dev, staging, prod)
azd up                      # 预配基础设施 + 构建 + 部署
```

## 核心文件结构

```
project/
├── azure.yaml              # azd 服务定义 + 钩子
├── infra/
│   ├── main.bicep          # 根基础设施模块
│   ├── main.parameters.json # 从环境变量注入参数
│   └── modules/
│       ├── container-apps-environment.bicep
│       └── container-app.bicep
├── .azure/
│   ├── config.json         # 默认环境指针
│   └── <env-name>/
│       ├── .env            # 环境特定值（azd 管理）
│       └── config.json     # 环境元数据
└── src/
    ├── frontend/Dockerfile
    └── backend/Dockerfile
```

## azure.yaml 配置

### 最简配置

```yaml
name: azd-deployment
services:
  backend:
    project: ./src/backend
    language: python
    host: containerapp
    docker:
      path: ./Dockerfile
      remoteBuild: true
```

### 完整配置（含钩子）

```yaml
name: azd-deployment
metadata:
  template: my-project@1.0.0

infra:
  provider: bicep
  path: ./infra

azure:
  location: eastus2

services:
  frontend:
    project: ./src/frontend
    language: ts
    host: containerapp
    docker:
      path: ./Dockerfile
      context: .
      remoteBuild: true

  backend:
    project: ./src/backend
    language: python
    host: containerapp
    docker:
      path: ./Dockerfile
      context: .
      remoteBuild: true

hooks:
  preprovision:
    shell: sh
    run: |
      echo "预配前..."
      
  postprovision:
    shell: sh
    run: |
      echo "预配后 - 设置 RBAC 等"
      
  postdeploy:
    shell: sh
    run: |
      echo "Frontend: ${SERVICE_FRONTEND_URI}"
      echo "Backend: ${SERVICE_BACKEND_URI}"
```

### azure.yaml 关键选项

| 选项 | 说明 |
|------|------|
| `remoteBuild: true` | 在 Azure Container Registry 中构建镜像（推荐） |
| `context: .` | 相对于项目路径的 Docker 构建上下文 |
| `host: containerapp` | 部署到 Azure Container Apps |
| `infra.provider: bicep` | 使用 Bicep 管理基础设施 |

## 环境变量流转

### 三级配置

1. **本地 `.env`** - 仅用于本地开发
2. **`.azure/<env>/.env`** - azd 管理，从 Bicep 输出自动填充
3. **`main.parameters.json`** - 将环境变量映射到 Bicep 参数

### 参数注入模式

```json
// infra/main.parameters.json
{
  "parameters": {
    "environmentName": { "value": "${AZURE_ENV_NAME}" },
    "location": { "value": "${AZURE_LOCATION=eastus2}" },
    "azureOpenAiEndpoint": { "value": "${AZURE_OPENAI_ENDPOINT}" }
  }
}
```

语法：`${VAR_NAME}` 或 `${VAR_NAME=默认值}`

### 设置环境变量

```bash
# 为当前环境设置
azd env set AZURE_OPENAI_ENDPOINT "https://my-openai.openai.azure.com"
azd env set AZURE_SEARCH_ENDPOINT "https://my-search.search.windows.net"

# 初始化时设置
azd env new prod
azd env set AZURE_OPENAI_ENDPOINT "..." 
```

### Bicep 输出 → 环境变量

```bicep
// 在 main.bicep 中 - 输出自动填充 .azure/<env>/.env
output SERVICE_FRONTEND_URI string = frontend.outputs.uri
output SERVICE_BACKEND_URI string = backend.outputs.uri
output BACKEND_PRINCIPAL_ID string = backend.outputs.principalId
```

## 幂等部署

### 为什么 azd up 是幂等的

1. **Bicep 是声明式的** - 资源协调到期望状态
2. **远程构建唯一标记** - 镜像标签包含部署时间戳
3. **ACR 复用层** - 仅上传变更的层

### 保留手动更改

通过 Portal 添加的自定义域名可能在重新部署时丢失。使用钩子保留：

```yaml
hooks:
  preprovision:
    shell: sh
    run: |
      # 预配前保存自定义域名
      if az containerapp show --name "$FRONTEND_NAME" -g "$RG" &>/dev/null; then
        az containerapp show --name "$FRONTEND_NAME" -g "$RG" \
          --query "properties.configuration.ingress.customDomains" \
          -o json > /tmp/domains.json
      fi

  postprovision:
    shell: sh
    run: |
      # 验证/恢复自定义域名
      if [ -f /tmp/domains.json ]; then
        echo "已保存域名: $(cat /tmp/domains.json)"
      fi
```

### 处理现有资源

```bicep
// 引用现有 ACR（不重新创建）
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' existing = {
  name: containerRegistryName
}

// 将 customDomains 设为 null 以保留 Portal 添加的域名
customDomains: empty(customDomainsParam) ? null : customDomainsParam
```

## Container App 服务发现

同一环境中 Container Apps 之间的内部 HTTP 路由：

```bicep
// 前端环境变量中的后端引用
env: [
  {
    name: 'BACKEND_URL'
    value: 'http://ca-backend-${resourceToken}'  // 内部 DNS
  }
]
```

前端 nginx 代理到内部 URL：
```nginx
location /api {
    proxy_pass $BACKEND_URL;
}
```

## 托管身份与 RBAC

### 启用系统分配身份

```bicep
resource containerApp 'Microsoft.App/containerApps@2024-03-01' = {
  identity: {
    type: 'SystemAssigned'
  }
}

output principalId string = containerApp.identity.principalId
```

### 预配后 RBAC 分配

```yaml
hooks:
  postprovision:
    shell: sh
    run: |
      PRINCIPAL_ID="${BACKEND_PRINCIPAL_ID}"
      
      # Azure OpenAI 访问权限
      az role assignment create \
        --assignee-object-id "$PRINCIPAL_ID" \
        --assignee-principal-type ServicePrincipal \
        --role "Cognitive Services OpenAI User" \
        --scope "$OPENAI_RESOURCE_ID" 2>/dev/null || true
      
      # Azure AI Search 访问权限
      az role assignment create \
        --assignee-object-id "$PRINCIPAL_ID" \
        --role "Search Index Data Reader" \
        --scope "$SEARCH_RESOURCE_ID" 2>/dev/null || true
```

## 常用命令

```bash
# 环境管理
azd env list                        # 列出环境
azd env select <name>               # 切换环境
azd env get-values                  # 显示所有环境变量
azd env set KEY value               # 设置变量

# 部署
azd up                              # 完整预配 + 部署
azd provision                       # 仅基础设施
azd deploy                          # 仅代码部署
azd deploy --service backend        # 部署单个服务

# 调试
azd show                            # 显示项目状态
az containerapp logs show -n <app> -g <rg> --follow  # 流式日志
```

## 参考文件

- **Bicep 模式**：参见 references/bicep-patterns.md 了解 Container Apps 模块
- **故障排除**：参见 references/troubleshooting.md 了解常见问题
- **azure.yaml 架构**：参见 references/azure-yaml-schema.md 了解完整选项

## 关键提醒

1. **始终使用 `remoteBuild: true`** - 本地构建在 M1/ARM Mac 部署到 AMD64 时会失败
2. **Bicep 输出自动填充 .azure/<env>/.env** - 不要手动编辑
3. **使用 `azd env set` 设置机密** - 不要在 main.parameters.json 默认值中设置
4. **服务标签（`azd-service-name`）** - azd 查找 Container Apps 所必需
5. **钩子中的 `|| true`** - 防止 RBAC "已存在" 错误导致部署失败

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅当任务明确匹配上述范围时使用本技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
