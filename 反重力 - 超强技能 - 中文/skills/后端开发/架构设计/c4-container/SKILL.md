---
name: c4-container
description: C4 容器级文档专家。当用户要求'C4容器级文档'、'系统部署文档'、'容器图'、'Container Diagram'、'OpenAPI规范'或'容器级架构文档'时使用。
risk: unknown
source: community
date_added: '2026-02-27'
---

# C4 容器级：系统部署

## 使用此技能的场景

- 处理 C4 容器级：系统部署任务或工作流
- 需要 C4 容器级：系统部署的指导、最佳实践或检查清单

## 不使用此技能的场景

- 任务与 C4 容器级：系统部署无关
- 需要此范围之外的其他领域或工具

## 指导说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 容器

### [容器名称]

- **名称**：[容器名称]
- **描述**：[容器用途和部署的简要描述]
- **类型**：[Web 应用、API、数据库、消息队列等]
- **技术**：[主要技术：Node.js、Python、PostgreSQL、Redis 等]
- **部署**：[Docker、Kubernetes、云服务等]

## 用途

[此容器功能及其部署方式的详细描述]

## 组件

此容器部署以下组件：

- [组件名称]：[描述]
  - 文档：c4-component-name.md

## 接口

### [API/接口名称]

- **协议**：[REST/GraphQL/gRPC/Events 等]
- **描述**：[此接口提供的功能]
- **规范**：[OpenAPI/Swagger/API 规范文件链接]
- **端点**：
  - `GET /api/resource` - [描述]
  - `POST /api/resource` - [描述]

## 依赖

### 使用的容器

- [容器名称]：[使用方式、通信协议]

### 外部系统

- [外部系统]：[使用方式、集成类型]

## 基础设施

- **部署配置**：[Dockerfile、K8s 清单等链接]
- **扩缩容**：[水平/垂直扩缩容策略]
- **资源**：[CPU、内存、存储需求]

## 容器图

使用正确的 Mermaid C4Container 语法：

```mermaid
C4Container
    title Container Diagram for [System Name]

    Person(user, "User", "Uses the system")
    System_Boundary(system, "System Name") {
        Container(webApp, "Web Application", "Spring Boot, Java", "Provides web interface")
        Container(api, "API Application", "Node.js, Express", "Provides REST API")
        ContainerDb(database, "Database", "PostgreSQL", "Stores data")
        Container_Queue(messageQueue, "Message Queue", "RabbitMQ", "Handles async messaging")
    }
    System_Ext(external, "External System", "Third-party service")

    Rel(user, webApp, "Uses", "HTTPS")
    Rel(webApp, api, "Makes API calls to", "JSON/HTTPS")
    Rel(api, database, "Reads from and writes to", "SQL")
    Rel(api, messageQueue, "Publishes messages to")
    Rel(api, external, "Uses", "API")
```
````

**核心原则**（来自 [c4model.com](https://c4model.com/diagrams/container)）：

- 展示**高层技术选型**（技术细节应放在这一层）
- 展示**职责如何在容器间分配**
- 包含**容器类型**：应用程序、数据库、消息队列、文件系统等
- 展示容器之间的**通信协议**
- 包含容器交互的**外部系统**

````

## API 规范模板

为每个容器 API 创建 OpenAPI/Swagger 规范：

```yaml
openapi: 3.1.0
info:
  title: [Container Name] API
  description: [API description]
  version: 1.0.0
servers:
  - url: https://api.example.com
    description: Production server
paths:
  /api/resource:
    get:
      summary: [Operation summary]
      description: [Operation description]
      parameters:
        - name: param1
          in: query
          schema:
            type: string
      responses:
        '200':
          description: [Response description]
          content:
            application/json:
              schema:
                type: object
````

## 示例交互

- "根据部署定义将所有组件合成为容器"
- "将 API 组件映射到容器并将其 API 文档化为 OpenAPI 规范"
- "为微服务架构创建容器级文档"
- "将容器接口文档化为 Swagger/OpenAPI 规范"
- "分析 Kubernetes 清单并创建容器文档"

## 关键区别

- **与 C4-Component 智能体的区别**：将组件映射到部署单元；Component 智能体关注逻辑分组
- **与 C4-Context 智能体的区别**：提供容器级细节；Context 智能体创建高层系统图
- **与 C4-Code 智能体的区别**：关注部署架构；Code 智能体文档化单个代码元素

## 输出示例

合成容器时，应提供：

- 清晰的容器边界及部署理由
- 描述性的容器名称和部署特征
- 完整的 API 文档及 OpenAPI/Swagger 规范
- 所有包含组件的链接
- 展示部署架构的 Mermaid 容器图
- 部署配置链接（Dockerfile、K8s 清单等）
- 基础设施需求和扩缩容考量
- 所有容器间一致的文档格式

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 输出不能替代特定环境的验证、测试或专家审查。
- 如缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
