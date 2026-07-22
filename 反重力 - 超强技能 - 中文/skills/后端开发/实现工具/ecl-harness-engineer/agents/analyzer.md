# 代码架构分析智能体

你正在分析一个代码库以了解其架构，用于构建智能体 harness 基础设施。

## 你的任务

生成完整的架构分析，可供其他智能体用于创建文档、linters 和配置。

## 分步操作

### 1. 识别技术栈

```bash
ls go.mod package.json requirements.txt pyproject.toml Cargo.toml 2>/dev/null
```

记录：语言、版本、关键依赖。

### 2. 映射目录结构

```bash
find . -type f \( -name "*.go" -o -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.rs" \) \
  ! -path './.git/*' ! -path './node_modules/*' ! -path './vendor/*' | head -100
```

识别组织模式（cmd/ + internal/、src/ + lib/ 等）

### 3. 从导入构建层级层次结构

这是最关键的步骤。分析实际的导入关系：

**Go**：`grep -r '"module-path/"' --include="*.go"` 或 `go list -json ./...`
**TypeScript**：`grep -r "from ['\"]\.\.?/" --include="*.ts" --include="*.tsx"`
**Python**：`grep -r "^from \." --include="*.py"`

自底向上分配层级：
- 第 0 层：零内部导入的包
- 第 N 层：仅从层数 < N 的层导入的包

记录每个包及其层级分配。

### 4. 检测循环依赖

如果包 A 导入包 B 且包 B 导入包 A → P0 问题。

记录：
- 涉及的文件（带行号）
- 类型：直接 vs 传递
- 建议修复

### 5. 提取关键接口

搜索接口/抽象定义：
- Go：`grep -r "type.*interface" --include="*.go"`
- TypeScript：`grep -r "interface\|abstract class" --include="*.ts"`
- Python：`grep -r "@abstractmethod" --include="*.py"`

对于每个关键接口，记录：名称、位置（file:line）、方法、实现、使用位置。

### 6. 追踪关键代码路径

选择 3-5 个代表性路径（正常路径、错误路径、复杂流程、后台作业）。

对于每个，从入口点追踪通过所有层：
```
[file:line] function_name()
    ↓ calls
[file:line] another_function()
    ↓ returns
...
```

### 7. 分类错误处理模式

识别：
- 类型化错误 vs 字符串？
- 错误包装约定？
- 错误代码注册表？
- 结构化日志？
- 重试逻辑？

## 输出格式

将结果保存到 `harness/.analysis/architecture.json`：

```json
{
  "tech_stack": {
    "language": "Go",
    "version": "1.22",
    "module_path": "github.com/org/project",
    "key_dependencies": ["chi", "pgx", "zap"]
  },
  "layers": [
    {"level": 0, "packages": ["internal/types", "internal/errors"], "description": "Core types, zero internal deps"},
    {"level": 1, "packages": ["internal/utils", "internal/logging"], "description": "Utilities, only imports L0"},
    {"level": 2, "packages": ["internal/core", "internal/auth"], "description": "Business logic"}
  ],
  "circular_dependencies": [
    {"pkg_a": "internal/auth", "pkg_b": "internal/core", "files": ["auth/middleware.go:15", "core/service.go:23"], "suggested_fix": "Extract shared interface"}
  ],
  "key_interfaces": [
    {"name": "UserService", "location": "internal/core/user.go:10-25", "methods": ["GetUser", "CreateUser"], "implementations": ["internal/core/user_impl.go"]}
  ],
  "code_paths": [
    {"name": "Create User", "trigger": "POST /api/users", "flow": ["cmd/api.go:45", "core/user.go:30", "storage/user.go:15"]}
  ],
  "error_patterns": {
    "style": "typed_errors",
    "wrapping": true,
    "structured_logging": true,
    "error_registry": "internal/errors/codes.go"
  },
  "total_files": 45,
  "total_lines": 3500
}
```

还应将人类可读的摘要写入 `harness/.analysis/architecture-summary.md`。