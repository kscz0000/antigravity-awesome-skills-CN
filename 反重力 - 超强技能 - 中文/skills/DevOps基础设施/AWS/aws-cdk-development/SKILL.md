---
name: aws-cdk-development
description: AWS Cloud Development Kit（CDK）专家，使用 TypeScript/Python 构建云基础设施。在创建 CDK Stack、定义 CDK Construct、实施基础设施即代码，或用户提及 CDK、CloudFormation、IaC、cdk synth、cdk deploy，或想要定义 AWS 资源时使用。
risk: unknown
source: https://github.com/zxkane/aws-skills/tree/main/plugins/aws-iac/skills/aws-cdk-development
source_repo: zxkane/aws-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/zxkane/aws-skills/blob/main/LICENSE
---

# AWS CDK 开发

本技能提供使用 Cloud Development Kit（CDK）开发 AWS 基础设施的全面指导，并集成 MCP 服务器以访问最新的 AWS 知识和 CDK 实用工具。

## AWS 文档要求

回答前务必使用 MCP 工具（`mcp__aws-mcp__*` 或 `mcp__*awsdocs*__*`）核实 AWS 事实。`aws-mcp-setup` 依赖项会自动加载——如果 MCP 工具不可用，请引导用户完成该技能的设置流程。

## CDK 专用 MCP 指南

AWS Labs 已将专用 CDK MCP 服务器（`awslabs.cdk-mcp-server`）替换为更广泛的 `awslabs.aws-iac-mcp-server`，后者涵盖 CDK 以及 CloudFormation 和其他 AWS 基础设施即代码工作流。

如需查询 CDK Construct、最佳实践建议和模式指导，请安装 `awslabs.aws-iac-mcp-server`。它随 `deploy-on-aws` 插件一起提供（来自 `awslabs/agent-plugins`），也可以通过 `claude mcp add aws-iac uvx awslabs.aws-iac-mcp-server@latest` 直接注册。

**何时使用它**：
- CDK Construct 推荐与 API 查询
- CDK 和 CloudFormation 最佳实践模式
- 合成模板的验证
- 跨资源配置指导

## 适用场景

满足以下任一情况时使用本技能：
- 创建新的 CDK Stack 或 Construct
- 重构现有 CDK 基础设施
- 在 CDK 中实施 Lambda 函数
- 遵循 AWS CDK 最佳实践
- 部署前验证 CDK Stack 配置
- 核实 AWS 服务能力和区域可用性

## CDK 核心原则

### 资源命名

**关键**：当 CDK Construct 中资源名称为可选项时，不要显式指定。

**原因**：CDK 生成的名称支持：
- **可复用模式**：可多次部署相同的 Construct/模式而不会冲突
- **并行部署**：多个 Stack 可以在同一区域同时部署
- **清晰的共享逻辑**：模式和共享代码可以多次初始化而不会命名冲突
- **Stack 隔离**：每个 Stack 自动获得唯一标识的资源

**模式**：让 CDK 使用 CloudFormation 的命名机制自动生成唯一名称。

```typescript
// ❌ 错误 - 显式命名会阻碍可复用性和并行部署
new lambda.Function(this, 'MyFunction', {
  functionName: 'my-lambda',  // 避免这样做
  // ...
});

// ✅ 正确 - 让 CDK 生成唯一名称
new lambda.Function(this, 'MyFunction', {
  // 未指定 functionName - CDK 生成：StackName-MyFunctionXXXXXX
  // ...
});
```

**安全提示**：针对不同环境（dev、staging、prod），应遵循 AWS 安全支柱最佳实践，使用独立的 AWS 账户，而不是依赖单一账户内的资源命名。账户级隔离提供更强的安全边界。

### Lambda 函数开发

根据运行时选用合适的 Lambda Construct：

**TypeScript/JavaScript**：使用 `@aws-cdk/aws-lambda-nodejs`
```typescript
import { NodejsFunction } from 'aws-cdk-lib/aws-lambda-nodejs';

new NodejsFunction(this, 'MyFunction', {
  entry: 'lambda/handler.ts',
  handler: 'handler',
  // 自动处理打包、依赖和转译
});
```

**Python**：使用 `@aws-cdk/aws-lambda-python`
```typescript
import { PythonFunction } from '@aws-cdk/aws-lambda-python-alpha';

new PythonFunction(this, 'MyFunction', {
  entry: 'lambda',
  index: 'handler.py',
  handler: 'handler',
  // 自动处理依赖和打包
});
```

**优势**：
- 自动打包和依赖管理
- 自动处理转译
- 无需手动打包
- 一致的部署模式

### 部署前验证

采用**多层验证策略**进行全面的 CDK 质量检查：

#### 第 1 层：实时 IDE 反馈（推荐）

**针对 TypeScript/JavaScript 项目**：

安装 [cdk-nag](https://github.com/cdklabs/cdk-nag) 以在合成时进行验证：
```bash
npm install --save-dev cdk-nag
```

添加到 CDK 应用：
```typescript
import { Aspects } from 'aws-cdk-lib';
import { AwsSolutionsChecks } from 'cdk-nag';

const app = new App();
Aspects.of(app).add(new AwsSolutionsChecks());
```

**可选 - VS Code 用户**：安装 [CDK NAG Validator 扩展](https://marketplace.visualstudio.com/items?itemName=alphacrack.cdk-nag-validator) 以在文件保存时获得更快反馈。

**针对 Python/Java/C#/Go 项目**：cdk-nag 在所有 CDK 语言中均可用，并提供相同的合成时验证。

#### 第 2 层：合成时验证（必需）

1. **使用 cdk-nag 合成**：通过全面的规则验证 Stack
   ```bash
   cdk synth  # cdk-nag 通过 Aspects 自动运行
   ```

2. **抑制合法例外**并附上文档化原因：
   ```typescript
   import { NagSuppressions } from 'cdk-nag';

   // 说明为何需要该例外
   NagSuppressions.addResourceSuppressions(resource, [
     {
       id: 'AwsSolutions-L1',
       reason: 'Lambda@Edge 需要特定运行时以兼容 CloudFront'
     }
   ]);
   ```

#### 第 3 层：提交前安全网

1. **构建**：确保编译成功
   ```bash
   npm run build  # 或特定语言的构建命令
   ```

2. **测试**：运行单元测试和集成测试
   ```bash
   npm test  # 或 pytest、mvn test 等
   ```

3. **验证脚本**：元级别检查
   ```bash
   ./scripts/validate-stack.sh
   ```

验证脚本当前专注于：
- 语言检测
- 模板大小和资源数量分析
- 合成成功验证
- （注意：详细的反模式检查由 cdk-nag 处理）

## 工作流指南

### 开发工作流

1. **设计**：规划基础设施资源和关系
2. **核实 AWS 服务**：使用 AWS 文档 MCP 确认服务可用性和功能
   - 检查所有必需服务的区域可用性
   - 核实服务限制和配额
   - 确认最新的 API 规范
3. **实施**：编写遵循最佳实践的 CDK Construct
   - 使用 CDK MCP 服务器获取 Construct 推荐
   - 通过 MCP 工具参考 CDK 最佳实践
4. **验证**：运行部署前检查（见上文）
5. **合成**：生成 CloudFormation 模板
6. **审查**：检查合成的模板以确保正确性
7. **部署**：部署到目标环境
8. **核实**：确认资源已正确创建

### Stack 组织

- 对复杂应用使用嵌套 Stack
- 将关注点分离到合理的 Construct 边界
- 导出其他 Stack 可能需要的值
- 使用 CDK context 处理环境特定的配置

### 测试策略

- 单元测试各个 Construct
- 集成测试 Stack 合成
- 对 CloudFormation 模板进行快照测试
- 验证资源属性和关系

## 有效使用 MCP 服务器

### 何时使用 AWS 文档 MCP

**实施前务必核实**：
- 新的 AWS 服务功能或配置
- 目标区域的服务可用性
- API 参数规范
- 服务限制和配额
- AWS 服务的安全最佳实践

**示例场景**：
- "检查 Lambda 是否支持 Python 3.13 运行时"
- "核实 DynamoDB 在 eu-south-2 可用"
- "Lambda 当前的超时限制是多少？"
- "获取最新的 S3 加密选项"

### 何时使用 CDK MCP 服务器

**利用其获取 CDK 专用指导**：
- CDK Construct 选择和使用
- CDK API 参数选项
- CDK 最佳实践模式
- Construct 属性配置
- CDK 特定优化

**示例场景**：
- "API Gateway REST API 推荐的 CDK Construct 是什么？"
- "如何配置 NodejsFunction 的打包选项？"
- "CDK Stack 组织的最佳实践"
- "支持自动扩缩的 DynamoDB 的 CDK Construct"

### MCP 使用最佳实践

1. **先核实**：实施新功能前始终查阅 AWS 文档 MCP
2. **区域验证**：检查目标部署区域的服务可用性
3. **CDK 指导**：使用 CDK MCP 获取 Construct 特定推荐
4. **保持最新**：MCP 服务器提供超出知识截止日期的最新信息
5. **组合来源**：结合技能模式和 MCP 服务器获得全面指导

## CDK 模式参考

如需详细的 CDK 模式、反模式和架构指导，请参考综合性参考资料：

**文件**：`references/cdk-patterns.md`

该参考资料包含：
- 常见 CDK 模式及其使用场景
- 应避免的反模式
- 安全最佳实践
- 成本优化策略
- 性能考量

## 其他资源

- **验证脚本**：`scripts/validate-stack.sh` - 部署前验证
- **CDK 模式**：`references/cdk-patterns.md` - 详细的模式库
- **AWS 文档 MCP**：已集成以获取最新 AWS 信息
- **CDK MCP 服务器**：已集成以获取 CDK 专用指导

## GitHub Actions 集成

当代码仓库中存在 GitHub Actions 工作流文件时，提交前确保 `.github/workflows/` 中定义的所有检查通过。这可防止 CI/CD 失败并维护代码质量标准。

## 局限性

- 仅当任务明确匹配其上游来源和本地项目上下文时使用本技能。
- 在应用更改前核实命令、生成的代码、依赖、凭据和外部服务行为。
- 不要将示例视为环境特定测试、安全审查或用户对破坏性或高成本操作的批准的替代品。