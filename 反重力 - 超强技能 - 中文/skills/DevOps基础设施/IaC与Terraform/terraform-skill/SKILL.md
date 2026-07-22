---
name: terraform-skill
description: "Terraform 基础设施即代码最佳实践。用于 Terraform/OpenTofu 配置、模块开发、测试策略、CI/CD 集成等场景"
risk: safe
source: "https://github.com/antonbabenko/terraform-skill"
date_added: "2026-02-27"
---
# Claude 的 Terraform 技能

全面的 Terraform 和 OpenTofu 指南，涵盖测试、模块、CI/CD 和生产模式。基于 terraform-best-practices.com 和企业实践经验。

## 适用场景

**以下情况使用此技能：**
- 创建新的 Terraform 或 OpenTofu 配置或模块
- 为 IaC 代码搭建测试基础设施
- 选择测试方法（validate、plan、框架测试）
- 构建多环境部署架构
- 实施基础设施即代码的 CI/CD
- 审查或重构现有 Terraform/OpenTofu 项目
- 选择模块模式或状态管理方案

**不适用场景：**
- 基础的 Terraform/OpenTofu 语法问题（Claude 已掌握）
- 特定 Provider 的 API 参考（请链接到官方文档）
- 与 Terraform/OpenTofu 无关的云平台问题

## 核心原则

### 1. 代码结构设计哲学

**模块层级：**

| 类型 | 使用场景 | 范围 |
|------|----------|------|
| **资源模块** | 单一逻辑组的关联资源 | VPC + 子网、安全组 + 规则 |
| **基础设施模块** | 为特定目的组合的资源模块集合 | 同一区域/账户内的多个资源模块 |
| **组合** | 完整基础设施 | 跨多个区域/账户 |

**层级关系：** 资源 → 资源模块 → 基础设施模块 → 组合

**目录结构：**
```
environments/        # 环境特定配置
├── prod/
├── staging/
└── dev/

modules/            # 可复用模块
├── networking/
├── compute/
└── data/

examples/           # 模块使用示例（同时作为测试）
├── complete/
└── minimal/
```

**terraform-best-practices.com 核心原则：**
- 将 **环境**（prod、staging）与 **模块**（可复用组件）分离
- 使用 **examples/** 同时作为文档和集成测试夹具
- 保持模块小而专注（单一职责）

**详细模块架构参见：** 代码模式：模块类型与层级

### 2. 命名规范

**资源命名：**
```hcl
# 好：描述性、有上下文
resource "aws_instance" "web_server" { }
resource "aws_s3_bucket" "application_logs" { }

# 好：单例资源使用 "this"
resource "aws_vpc" "this" { }
resource "aws_security_group" "this" { }

# 避免：非单例资源使用泛化名称
resource "aws_instance" "main" { }
resource "aws_s3_bucket" "bucket" { }
```

**单例资源：**

当模块只创建一个该类型资源时使用 `"this"`：

✅ 推荐：
```hcl
resource "aws_vpc" "this" {}           # 模块创建一个 VPC
resource "aws_security_group" "this" {}  # 模块创建一个安全组
```

❌ 不推荐：多个资源使用 "this"：
```hcl
resource "aws_subnet" "this" {}  # 如果创建多个子网
```

创建多个同类型资源时使用描述性名称。

**变量命名：**
```hcl
# 需要时添加上下文前缀
var.vpc_cidr_block          # 而非 "cidr"
var.database_instance_class # 而非 "instance_class"
```

**文件命名：**
- `main.tf` - 主要资源
- `variables.tf` - 输入变量
- `outputs.tf` - 输出值
- `versions.tf` - Provider 版本
- `data.tf` - 数据源（可选）

## 测试策略框架

### 决策矩阵：选择哪种测试方法？

| 场景 | 推荐方法 | 工具 | 成本 |
|------|----------|------|------|
| **快速语法检查** | 静态分析 | `terraform validate`、`fmt` | 免费 |
| **提交前验证** | 静态分析 + lint | `validate`、`tflint`、`trivy`、`checkov` | 免费 |
| **Terraform 1.6+，简单逻辑** | 原生测试框架 | 内置 `terraform test` | 免费-低 |
| **1.6 之前版本，或 Go 专长** | 集成测试 | Terratest | 低-中 |
| **安全/合规重点** | 策略即代码 | OPA、Sentinel | 免费 |
| **成本敏感工作流** | Mock providers（1.7+） | 原生测试 + mocking | 免费 |
| **多云、复杂场景** | 完整集成 | Terratest + 真实基础设施 | 中-高 |

### 基础设施测试金字塔

```
        /\
       /  \          端到端测试（成本高）
      /____\         - 完整环境部署
     /      \        - 类生产环境配置
    /________\
   /          \      集成测试（成本中等）
  /____________\     - 隔离环境下的模块测试
 /              \    - 测试账户中的真实资源
/________________\   静态分析（成本低）
                     - validate、fmt、lint
                     - 安全扫描
```

### 原生测试最佳实践（1.6+）

**生成测试代码前：**

1. **使用 Terraform MCP 验证 schema：**
   ```
   Search provider docs → Get resource schema → Identify block types
   ```

2. **选择正确的命令模式：**
   - `command = plan` - 快速，用于输入验证
   - `command = apply` - 计算值和 set 类型块需要

3. **正确处理 set 类型块：**
   - 不能用 `[0]` 索引
   - 使用 `for` 表达式迭代
   - 或使用 `command = apply` 实例化

**常见模式：**
- S3 加密规则：**set**（使用 for 表达式）
- 生命周期转换：**set**（使用 for 表达式）
- IAM 策略语句：**set**（使用 for 表达式）

**详细测试指南参见：**
- **测试框架指南** - 深入了解静态分析、原生测试和 Terratest
- **快速参考** - 决策流程图和命令速查表

## 代码结构标准

### 资源块排序规范

**严格排序以保持一致性：**
1. `count` 或 `for_each` 放最前面（后跟空行）
2. 其他参数
3. `tags` 作为最后一个实际参数
4. `depends_on` 放在 tags 之后（如需要）
5. `lifecycle` 放在最后（如需要）

```hcl
# ✅ 正确 - 正确的排序
resource "aws_nat_gateway" "this" {
  count = var.create_nat_gateway ? 1 : 0

  allocation_id = aws_eip.this[0].id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "${var.name}-nat"
  }

  depends_on = [aws_internet_gateway.this]

  lifecycle {
    create_before_destroy = true
  }
}
```

### 变量块排序规范

1. `description`（必须填写）
2. `type`
3. `default`
4. `validation`
5. `nullable`（设为 false 时）

```hcl
variable "environment" {
  description = "Environment name for resource tagging"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }

  nullable = false
}
```

**完整结构指南参见：** 代码模式：块排序与结构

## Count vs For_Each：何时使用

### 快速决策指南

| 场景 | 使用 | 原因 |
|------|------|------|
| 布尔条件（创建或不创建） | `count = condition ? 1 : 0` | 简单的开关切换 |
| 简单数字复制 | `count = 3` | 固定数量的相同资源 |
| 项目可能重排序/移除 | `for_each = toset(list)` | 稳定的资源地址 |
| 按键引用 | `for_each = map` | 命名访问资源 |
| 多个命名资源 | `for_each` | 更好的可维护性 |

### 常见模式

**布尔条件：**
```hcl
# ✅ 正确 - 布尔条件
resource "aws_nat_gateway" "this" {
  count = var.create_nat_gateway ? 1 : 0
  # ...
}
```

**使用 for_each 实现稳定寻址：**
```hcl
# ✅ 正确 - 移除 "us-east-1b" 只影响该子网
resource "aws_subnet" "private" {
  for_each = toset(var.availability_zones)

  availability_zone = each.key
  # ...
}

# ❌ 错误 - 移除中间的 AZ 会重建所有后续子网
resource "aws_subnet" "private" {
  count = length(var.availability_zones)

  availability_zone = var.availability_zones[count.index]
  # ...
}
```

**迁移指南和详细示例参见：** 代码模式：Count vs For_Each

## 使用 Locals 管理依赖

**使用 locals 确保正确的资源删除顺序：**

```hcl
# 问题：子网可能在 CIDR 块之后被删除，导致错误
# 解决方案：在 locals 中使用 try() 提示删除顺序

locals {
  # 优先引用辅助 CIDR，回退到 VPC
  # 强制 Terraform 在 CIDR 关联之前删除子网
  vpc_id = try(
    aws_vpc_ipv4_cidr_block_association.this[0].vpc_id,
    aws_vpc.this.id,
    ""
  )
}

resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_vpc_ipv4_cidr_block_association" "this" {
  count = var.add_secondary_cidr ? 1 : 0

  vpc_id     = aws_vpc.this.id
  cidr_block = "10.1.0.0/16"
}

resource "aws_subnet" "public" {
  vpc_id     = local.vpc_id  # 使用 local，而非直接引用
  cidr_block = "10.1.0.0/24"
}
```

**为什么这很重要：**
- 防止销毁基础设施时的删除错误
- 无需显式 `depends_on` 即可确保正确的依赖顺序
- 特别适用于带有辅助 CIDR 块的 VPC 配置

**详细示例参见：** 代码模式：使用 Locals 管理依赖

## 模块开发

### 标准模块结构

```
my-module/
├── README.md           # 使用文档
├── main.tf             # 主要资源
├── variables.tf        # 带描述的输入变量
├── outputs.tf          # 输出值
├── versions.tf         # Provider 版本约束
├── examples/
│   ├── minimal/        # 最小可用示例
│   └── complete/       # 完整功能示例
└── tests/              # 测试文件
    └── module_test.tftest.hcl  # 或 .go
```

### 最佳实践总结

**变量：**
- ✅ 始终包含 `description`
- ✅ 使用显式 `type` 约束
- ✅ 在适当处提供合理的 `default` 值
- ✅ 为复杂约束添加 `validation` 块
- ✅ 敏感信息使用 `sensitive = true`

**输出：**
- ✅ 始终包含 `description`
- ✅ 敏感输出标记 `sensitive = true`
- ✅ 考虑为相关值返回对象
- ✅ 记录使用者应如何处理每个输出

**详细模块模式参见：**
- **模块模式指南** - 变量最佳实践、输出设计、✅ 推荐 vs ❌ 不推荐模式
- **快速参考** - 资源命名、变量命名、文件组织

## CI/CD 集成

### 推荐工作流阶段

1. **验证** - 格式检查 + 语法验证 + lint
2. **测试** - 运行自动化测试（原生或 Terratest）
3. **计划** - 生成并审查执行计划
4. **应用** - 执行变更（生产环境需要审批）

### 成本优化策略

1. **PR 验证使用 mocking**（免费）
2. **仅在 main 分支运行集成测试**（可控成本）
3. **实施自动清理**（防止孤立资源）
4. **为所有测试资源打标签**（跟踪支出）

**完整 CI/CD 模板参见：**
- **CI/CD 工作流指南** - GitHub Actions、GitLab CI、Atlantis 集成、成本优化
- **快速参考** - 常见 CI/CD 问题及解决方案

## 安全与合规

### 必要安全检查

```bash
# 静态安全扫描
trivy config .
checkov -d .
```

### 常见问题避免

❌ **不要：**
- 在变量中存储密钥
- 使用默认 VPC
- 跳过加密
- 安全组开放到 0.0.0.0/0

✅ **推荐：**
- 使用 AWS Secrets Manager / Parameter Store
- 创建专用 VPC
- 启用静态加密
- 使用最小权限安全组

**详细安全指南参见：**
- **安全与合规指南** - Trivy/Checkov 集成、密钥管理、状态文件安全、合规测试

## 版本管理

### 版本约束语法

```hcl
version = "5.0.0"      # 精确版本（避免 - 不够灵活）
version = "~> 5.0"     # 推荐：仅 5.0.x
version = ">= 5.0"     # 最低版本（有风险 - 可能有破坏性变更）
```

### 按组件策略

| 组件 | 策略 | 示例 |
|------|------|------|
| **Terraform** | 锁定次版本 | `required_version = "~> 1.9"` |
| **Providers** | 锁定主版本 | `version = "~> 5.0"` |
| **模块（生产）** | 锁定精确版本 | `version = "5.1.2"` |
| **模块（开发）** | 允许补丁更新 | `version = "~> 5.1"` |

### 更新工作流

```bash
# 初始锁定版本
terraform init              # 创建 .terraform.lock.hcl

# 更新到约束范围内的最新版本
terraform init -upgrade     # 更新 providers

# 审查并测试
terraform plan
```

**详细版本管理参见：** 代码模式：版本管理

## 现代 Terraform 特性（1.0+）

### 特性版本可用性

| 特性 | 版本 | 用途 |
|------|------|------|
| `try()` 函数 | 0.13+ | 安全回退，替代 `element(concat())` |
| `nullable = false` | 1.1+ | 防止变量中的 null 值 |
| `moved` 块 | 1.1+ | 重构时避免销毁/重建 |
| `optional()` 带默认值 | 1.3+ | 可选对象属性 |
| 原生测试 | 1.6+ | 内置测试框架 |
| Mock providers | 1.7+ | 零成本单元测试 |
| Provider 函数 | 1.8+ | Provider 特定的数据转换 |
| 跨变量验证 | 1.9+ | 验证变量之间的关系 |
| 仅写参数 | 1.11+ | 密钥永不存储在状态中 |

### 快速示例

```hcl
# try() - 安全回退（0.13+）
output "sg_id" {
  value = try(aws_security_group.this[0].id, "")
}

# optional() - 带默认值的可选属性（1.3+）
variable "config" {
  type = object({
    name    = string
    timeout = optional(number, 300)  # 默认值：300
  })
}

# 跨变量验证（1.9+）
variable "environment" { type = string }
variable "backup_days" {
  type = number
  validation {
    condition     = var.environment == "prod" ? var.backup_days >= 7 : true
    error_message = "Production requires backup_days >= 7"
  }
}
```

**完整模式和示例参见：** 代码模式：现代 Terraform 特性

## 版本特定指南

### Terraform 1.0-1.5
- 使用 Terratest 进行测试
- 无原生测试框架可用
- 专注于静态分析和计划验证

### Terraform 1.6+ / OpenTofu 1.6+
- **新增：** 原生 `terraform test` / `tofu test` 命令
- 考虑从外部框架迁移到原生测试（简单测试）
- 仅对复杂集成测试保留 Terratest

### Terraform 1.7+ / OpenTofu 1.7+
- **新增：** 用于单元测试的 Mock providers
- 通过 mocking 外部依赖降低成本
- 使用真实集成测试进行最终验证

### Terraform vs OpenTofu

本技能完全支持两者。关于许可、治理和功能对比，参见快速参考：Terraform vs OpenTofu。

## 详细指南

本技能采用 **渐进式披露** - 本主文件包含核心信息，详细指南按需提供：

📚 **参考文件：**
- **测试框架** - 静态分析、原生测试和 Terratest 深入指南
- **模块模式** - 模块结构、变量/输出最佳实践、✅ 推荐 vs ❌ 不推荐模式
- **CI/CD 工作流** - GitHub Actions、GitLab CI 模板、成本优化、自动清理
- **安全与合规** - Trivy/Checkov 集成、密钥管理、合规测试
- **快速参考** - 命令速查表、决策流程图、故障排除指南

**使用方法：** 需要某主题的详细信息时，参考相应指南。Claude 将按需加载以提供全面指导。

## 许可证

本技能基于 **Apache License 2.0** 许可。完整条款参见 LICENSE 文件。

**Copyright © 2026 Anton Babenko**

## 限制条件
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要输入、权限、安全边界或成功标准，停止并请求澄清。
