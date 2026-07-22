---
name: bash-scripting
description: "创建生产级 shell 脚本的工作流，包含防御性模式、错误处理和测试。当用户要求'编写bash脚本''创建shell脚本''自动化脚本开发'时使用。"
category: granular-workflow-bundle
risk: safe
source: personal
date_added: "2026-02-27"
---

# Bash 脚本工作流

## 概述

专用工作流，用于创建健壮的、生产级 bash 脚本，采用防御性编程模式、全面的错误处理和自动化测试。

## 何时使用此工作流

在以下场景使用此工作流：
- 创建自动化脚本
- 编写系统管理工具
- 构建部署脚本
- 开发备份方案
- 创建 CI/CD 脚本

## 工作流阶段

### 阶段 1：脚本设计

#### 调用技能
- `bash-pro` - 专业脚本编写
- `bash-defensive-patterns` - 防御性模式

#### 操作
1. 定义脚本用途
2. 确定输入/输出
3. 规划错误处理
4. 设计日志策略
5. 文档化需求

#### 复制粘贴提示词
```
Use @bash-pro to design production-ready bash script
```

### 阶段 2：脚本结构

#### 调用技能
- `bash-pro` - 脚本结构
- `bash-defensive-patterns` - 安全模式

#### 操作
1. 添加 shebang 和严格模式
2. 创建 usage 函数
3. 实现参数解析
4. 设置日志
5. 添加清理处理器

#### 复制粘贴提示词
```
Use @bash-defensive-patterns to implement strict mode and error handling
```

### 阶段 3：核心实现

#### 调用技能
- `bash-linux` - Linux 命令
- `linux-shell-scripting` - Shell 脚本编写

#### 操作
1. 实现主要函数
2. 添加输入验证
3. 创建辅助函数
4. 处理边界情况
5. 添加进度指示器

#### 复制粘贴提示词
```
Use @bash-linux to implement system commands
```

### 阶段 4：错误处理

#### 调用技能
- `bash-defensive-patterns` - 错误处理
- `error-handling-patterns` - 错误模式

#### 操作
1. 添加 trap 处理器
2. 实现重试逻辑
3. 创建错误消息
4. 设置退出码
5. 添加回滚能力

#### 复制粘贴提示词
```
Use @bash-defensive-patterns to add comprehensive error handling
```

### 阶段 5：日志

#### 调用技能
- `bash-pro` - 日志模式

#### 操作
1. 创建日志函数
2. 添加日志级别
3. 实现时间戳
4. 配置日志轮转
5. 添加调试模式

#### 复制粘贴提示词
```
Use @bash-pro to implement structured logging
```

### 阶段 6：测试

#### 调用技能
- `bats-testing-patterns` - Bats 测试
- `shellcheck-configuration` - ShellCheck

#### 操作
1. 编写 Bats 测试
2. 运行 ShellCheck
3. 测试边界情况
4. 验证错误处理
5. 使用不同输入测试

#### 复制粘贴提示词
```
Use @bats-testing-patterns to write script tests
```

```
Use @shellcheck-configuration to lint bash script
```

### 阶段 7：文档

#### 调用技能
- `documentation-templates` - 文档

#### 操作
1. 添加脚本头部
2. 文档化函数
3. 创建用法示例
4. 列出依赖项
5. 添加故障排除章节

#### 复制粘贴提示词
```
Use @documentation-templates to document bash script
```

## 脚本模板

```bash
#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_NAME=$(basename "$0")
readonly SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"; }
error() { log "ERROR: $*" >&2; exit 1; }

usage() { cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS]
Options:
    -h, --help      Show help
    -v, --verbose   Verbose output
EOF
}

main() {
    log "Script started"
    # Implementation
    log "Script completed"
}

main "$@"
```

## 质量门控

- [ ] ShellCheck 通过
- [ ] Bats 测试通过
- [ ] 错误处理正常工作
- [ ] 日志功能正常
- [ ] 文档完整

## 相关工作流包

- `os-scripting` - 操作系统脚本
- `linux-troubleshooting` - Linux 故障排查
- `cloud-devops` - DevOps 自动化

## 限制
- 仅当任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
