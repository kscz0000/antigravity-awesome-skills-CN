---
name: c4-architecture-c4-architecture
description: "使用自底向上分析方法，为现有仓库/代码库生成全面的 C4 架构文档。当用户要求'C4架构文档'、'C4模型'、'架构文档生成'、'代码架构分析'时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# C4 架构文档工作流

使用自底向上分析方法，为现有仓库/代码库生成全面的 C4 架构文档。

[扩展思考：本工作流实现了完整的 C4 架构文档流程，遵循 C4 模型（Context、Container、Component、Code）。采用自底向上方法，从最深的代码目录开始向上推进，确保每个代码元素在合成为更高层抽象之前已被记录。工作流协调四个专业 C4 智能体（Code、Component、Container、Context），创建一套完整的架构文档，服务于技术和非技术利益相关者。]

## 使用此技能的场景

- 处理 C4 架构文档工作流任务或流程时
- 需要 C4 架构文档工作流的指导、最佳实践或检查清单时

## 不使用此技能的场景

- 任务与 C4 架构文档工作流无关时
- 需要本范围之外的其他领域或工具时

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 概述

本工作流按照 [C4 官方模型](https://c4model.com/diagrams) 创建全面的 C4 架构文档：

1. **代码层**：自底向上分析每个子目录，创建代码级文档
2. **组件层**：将代码文档合成为容器内的逻辑组件
3. **容器层**：将组件映射到部署容器并生成 API 文档（展示高层技术选型）
4. **上下文层**：创建包含角色和用户旅程的高层系统上下文（关注人和软件系统，而非技术）

**注意**：根据 [C4 模型](https://c4model.com/diagrams)，你不需要使用全部4层图——系统上下文图和容器图对大多数软件开发团队已经足够。本工作流为完整性生成所有层级，但团队可以选择使用哪些层级。

所有文档写入仓库根目录下新建的 `C4-Documentation/` 目录。

## 阶段 1：代码级文档（自底向上分析）

### 1.1 发现所有子目录

- 使用代码库搜索识别仓库中的所有子目录
- 按深度排序目录（最深的优先）以进行自底向上处理
- 过滤掉常见的非代码目录（node_modules、.git、build、dist 等）
- 创建待处理目录列表

### 1.2 处理每个目录（自底向上）

对于每个目录，从最深的开始：

- 使用 Task 工具，subagent_type="c4-architecture::c4-code"
- Prompt: |
  分析目录中的代码：[directory_path]

  按照以下结构创建全面的 C4 代码级文档：
  1. **概述部分**：
     - 名称：[此代码目录的描述性名称]
     - 描述：[此代码功能的简要描述]
     - 位置：[指向实际目录路径的链接（相对于仓库根目录）]
     - 语言：[使用的主要编程语言]
     - 用途：[此代码实现的目标]
  2. **代码元素部分**：
     - 记录所有函数/方法及其完整签名：
       - 函数名、参数（含类型）、返回类型
       - 每个函数的功能描述
       - 位置（文件路径和行号）
       - 依赖项（此函数依赖的内容）
     - 记录所有类/模块：
       - 类名、描述、位置
       - 方法及其签名
       - 依赖项
  3. **依赖项部分**：
     - 内部依赖（本仓库中的其他代码）
     - 外部依赖（库、框架、服务）
  4. **关系部分**：
     - 如果关系复杂，可选添加 Mermaid 图

  将输出保存为：C4-Documentation/c4-code-[directory-name].md
  文件名使用清理后的目录名（将 / 替换为 -，移除特殊字符）。

  确保文档包含：
  - 包含所有参数和类型的完整函数签名
  - 指向实际源代码位置的链接
  - 所有依赖项（内部和外部）
  - 清晰的描述性名称和描述

- 预期输出：C4-Documentation/ 中的 c4-code-<directory-name>.md 文件
- 上下文：目录及其子目录中的所有文件

**对每个子目录重复此操作**，直到所有目录都有对应的 c4-code-\*.md 文件。

## 阶段 2：组件级合成

### 2.1 分析所有代码级文档

- 收集阶段 1 中创建的所有 c4-code-\*.md 文件
- 分析代码结构、依赖关系和关系
- 基于以下标准识别逻辑组件边界：
  - 领域边界（相关的业务功能）
  - 技术边界（共享的框架、库）
  - 组织边界（团队归属，如可识别）

### 2.2 创建组件文档

对于每个识别的组件：

- 使用 Task 工具，subagent_type="c4-architecture::c4-component"
- Prompt: |
  将以下 C4 代码级文档文件合成为一个逻辑组件：

  待分析的代码文件：
  [c4-code-*.md 文件路径列表]

  按照以下结构创建全面的 C4 组件级文档：
  1. **概述部分**：
     - 名称：[组件名称 - 描述性且有意义的]
     - 描述：[组件用途的简要描述]
     - 类型：[Application、Service、Library 等]
     - 技术：[使用的主要技术]
  2. **用途部分**：
     - 此组件功能的详细描述
     - 它解决什么问题
     - 它在系统中的角色
  3. **软件功能部分**：
     - 列出此组件提供的所有软件功能
     - 每个功能附带简要描述
  4. **代码元素部分**：
     - 列出此组件包含的所有 c4-code-\*.md 文件
     - 链接到每个文件并附简要描述
  5. **接口部分**：
     - 记录所有组件接口：
       - 接口名称
       - 协议（REST、GraphQL、gRPC、Events 等）
       - 描述
       - 操作（函数签名、端点等）
  6. **依赖项部分**：
     - 使用的组件（此组件依赖的其他组件）
     - 外部系统（数据库、API、服务）
  7. **组件图**：
     - 显示此组件及其关系的 Mermaid 图

  将输出保存为：C4-Documentation/c4-component-[component-name].md
  文件名使用清理后的组件名称。

- 预期输出：每个组件一个 c4-component-<name>.md 文件
- 上下文：此组件的所有相关 c4-code-\*.md 文件

### 2.3 创建组件主索引

- 使用 Task 工具，subagent_type="c4-architecture::c4-component"
- Prompt: |
  创建列出系统中所有组件的组件主索引。

  基于已创建的所有 c4-component-\*.md 文件，生成：
  1. **系统组件部分**：
     - 列出所有组件：
       - 组件名称
       - 简要描述
       - 指向组件文档的链接
  2. **组件关系图**：
     - 显示所有组件及其关系的 Mermaid 图
     - 显示组件之间的依赖关系
     - 显示外部系统依赖

  将输出保存为：C4-Documentation/c4-component.md

- 预期输出：主 c4-component.md 文件
- 上下文：所有 c4-component-\*.md 文件

## 阶段 3：容器级合成

### 3.1 分析组件和部署定义

- 审查所有 c4-component-\*.md 文件
- 搜索部署/基础设施定义：
  - Dockerfiles
  - Kubernetes 清单（deployments、services 等）
  - Docker Compose 文件
  - Terraform/CloudFormation 配置
  - 云服务定义（AWS Lambda、Azure Functions 等）
  - CI/CD 流水线定义

### 3.2 将组件映射到容器

- 使用 Task 工具，subagent_type="c4-architecture::c4-container"
- Prompt: |
  基于部署定义将组件合成为容器。

  组件文档：
  [所有 c4-component-*.md 文件路径列表]

  发现的部署定义：
  [部署配置文件列表：Dockerfiles、K8s 清单等]

  按照以下结构创建全面的 C4 容器级文档：
  1. **容器部分**（每个容器）：
     - 名称：[容器名称]
     - 描述：[容器用途和部署的简要描述]
     - 类型：[Web Application、API、Database、Message Queue 等]
     - 技术：[主要技术：Node.js、Python、PostgreSQL 等]
     - 部署：[Docker、Kubernetes、Cloud Service 等]
  2. **用途部分**（每个容器）：
     - 此容器功能的详细描述
     - 部署方式
     - 在系统中的角色
  3. **组件部分**（每个容器）：
     - 列出部署在此容器中的所有组件
     - 链接到组件文档
  4. **接口部分**（每个容器）：
     - 记录所有容器 API 和接口：
       - API/接口名称
       - 协议（REST、GraphQL、gRPC、Events 等）
       - 描述
       - 指向 OpenAPI/Swagger/API Spec 文件的链接
       - 端点/操作列表
  5. **API 规范**：
     - 为每个容器 API 创建 OpenAPI 3.1+ 规范
     - 保存为：C4-Documentation/apis/[container-name]-api.yaml
     - 包含：
       - 所有端点及其方法（GET、POST 等）
       - 请求/响应模式
       - 认证要求
       - 错误响应
  6. **依赖项部分**（每个容器）：
     - 使用的容器（此容器依赖的其他容器）
     - 外部系统（数据库、第三方 API 等）
     - 通信协议
  7. **基础设施部分**（每个容器）：
     - 指向部署配置的链接（Dockerfile、K8s 清单等）
     - 扩展策略
     - 资源需求（CPU、内存、存储）
  8. **容器图**：
     - 显示所有容器及其关系的 Mermaid 图
     - 显示通信协议
     - 显示外部系统依赖

  将输出保存为：C4-Documentation/c4-container.md

- 预期输出：包含所有容器和 API 规范的 c4-container.md
- 上下文：所有组件文档和部署定义

## 阶段 4：上下文级文档

### 4.1 分析系统文档

- 审查容器和组件文档
- 搜索系统文档：
  - README 文件
  - 架构文档
  - 需求文档
  - 设计文档
  - 测试文件（用于理解系统行为）
  - API 文档
  - 用户文档

### 4.2 创建上下文文档

- 使用 Task 工具，subagent_type="c4-architecture::c4-context"
- Prompt: |
  为系统创建全面的 C4 上下文级文档。

  容器文档：C4-Documentation/c4-container.md
  组件文档：C4-Documentation/c4-component.md
  系统文档：[README、架构文档、需求等列表]
  测试文件：[展示系统行为的测试文件列表]

  按照以下结构创建全面的 C4 上下文级文档：
  1. **系统概述部分**：
     - 简要描述：[一句话描述系统功能]
     - 详细描述：[系统目的、能力、解决问题的详细描述]
  2. **角色部分**：
     - 对于每个角色（人类用户和程序化"用户"）：
       - 角色名称
       - 类型（Human User / Programmatic User / External System）
       - 描述（他们是谁，需要什么）
       - 目标（他们想实现什么）
       - 使用的关键功能
  3. **系统功能部分**：
     - 对于每个高层功能：
       - 功能名称
       - 描述（此功能做什么）
       - 用户（哪些角色使用此功能）
       - 指向用户旅程图的链接
  4. **用户旅程部分**：
     - 对于每个关键功能和角色：
       - 旅程名称：[功能名称] - [角色名称] 旅程
       - 逐步旅程：
         1. [步骤 1]：[描述]
         2. [步骤 2]：[描述]
            ...
       - 包含所有系统触点
     - 对于程序化用户（外部系统、API）：
       - 包含逐步流程的集成旅程
  5. **外部系统和依赖部分**：
     - 对于每个外部系统：
       - 系统名称
       - 类型（Database、API、Service、Message Queue 等）
       - 描述（它提供什么）
       - 集成类型（API、Events、File Transfer 等）
       - 用途（系统为什么依赖它）
  6. **系统上下文图**：
     - Mermaid C4Context 图显示：
       - 系统（作为中心的方框）
       - 周围的所有角色（用户）
       - 周围的所有外部系统
       - 关系和数据流
       - 使用 C4Context 表示法绘制标准 C4 图
  7. **相关文档部分**：
     - 指向容器文档的链接
     - 指向组件文档的链接

  将输出保存为：C4-Documentation/c4-context.md

  确保文档：
  - 非技术利益相关者可以理解
  - 关注系统目的、用户和外部关系
  - 包含全面的用户旅程图
  - 识别所有外部系统和依赖

- 预期输出：包含完整系统上下文的 c4-context.md
- 上下文：所有容器、组件和系统文档

## 配置选项

- `target_directory`：要分析的根目录（默认：当前仓库根目录）
- `exclude_patterns`：要排除的模式（默认：node_modules、.git、build、dist 等）
- `output_directory`：C4 文档写入位置（默认：C4-Documentation/）
- `include_tests`：是否分析测试文件以获取上下文（默认：true）
- `api_format`：API 规范格式（默认：openapi）

## 成功标准

- ✅ 每个子目录都有对应的 c4-code-\*.md 文件
- ✅ 所有代码级文档包含完整的函数签名
- ✅ 组件按逻辑分组，边界清晰
- ✅ 所有组件都有接口文档
- ✅ 已创建包含关系图的组件主索引
- ✅ 容器映射到实际部署单元
- ✅ 所有容器 API 已使用 OpenAPI/Swagger 规范记录
- ✅ 容器图展示部署架构
- ✅ 系统上下文包含所有角色（人类和程序化）
- ✅ 所有关键功能已记录用户旅程
- ✅ 所有外部系统和依赖已识别
- ✅ 上下文图展示系统、用户和外部系统
- ✅ 文档组织在 C4-Documentation/ 目录中

## 输出结构

```
C4-Documentation/
├── c4-code-*.md              # Code-level docs (one per directory)
├── c4-component-*.md          # Component-level docs (one per component)
├── c4-component.md            # Master component index
├── c4-container.md            # Container-level docs
├── c4-context.md              # Context-level docs
└── apis/                      # API specifications
    ├── [container]-api.yaml   # OpenAPI specs for each container
    └── ...
```

## 协调说明

- **自底向上处理**：从最深层到最浅层处理目录
- **增量合成**：每一层基于上一层的文档构建
- **完整覆盖**：每个目录在合成前必须有代码级文档
- **链接一致性**：所有文档文件之间正确链接
- **API 文档**：容器 API 必须有 OpenAPI/Swagger 规范
- **利益相关者友好**：上下文文档应能让非技术利益相关者理解
- **Mermaid 图**：所有图使用标准 C4 Mermaid 表示法

## 使用示例

```bash
/c4-architecture:c4-architecture
```

这将：

1. 自底向上遍历所有子目录
2. 为每个目录创建 c4-code-\*.md
3. 合成为组件
4. 映射到容器并生成 API 文档
5. 创建包含角色和旅程的系统上下文

所有文档写入：C4-Documentation/

## 局限性
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出替代特定环境的验证、测试或专家审查。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
