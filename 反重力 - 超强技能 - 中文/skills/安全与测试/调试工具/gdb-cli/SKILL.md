---
name: gdb-cli
description: "GDB 调试助手，用于 AI 智能体分析核心转储、调试运行进程、调查崩溃和死锁，并关联源代码。触发词：GDB调试、核心转储分析、崩溃分析、死锁调试、C++调试、C调试、进程调试、内存问题、段错误、调试助手"
category: development
risk: critical
source: community
date_added: "2026-03-22"
author: Cerdore
tags:
- debugging
- gdb
- core-dump
- crash-analysis
- c++
- c
tools:
- claude-code
- cursor
- gemini-cli
- codex-cli
- antigravity
---

# GDB 调试助手

## 概述

为 AI 智能体设计的 GDB 调试技能。结合**源代码分析**与**运行时状态检查**，使用 gdb-cli 为 C/C++ 程序提供智能调试辅助。

## 何时使用此技能

- 分析核心转储或崩溃转储
- 使用 GDB attach 调试运行中的进程
- 调查崩溃、死锁或内存问题
- 获取带有源代码上下文的智能调试辅助
- 调试多线程应用程序

## 何时不使用此技能

- 任务与 C/C++ 调试无关
- 用户需要非调试相关的通用辅助
- 没有 GDB 可用（需要 GDB 9.0+ 且支持 Python）

## 前置条件

```bash
# 安装 gdb-cli
pip install gdb-cli

# 或从 GitHub 安装
pip install git+https://github.com/Cerdore/gdb-cli.git

# 验证 GDB 支持 Python
gdb -nx -q -batch -ex "python print('OK')"
```

**要求：**
- Python 3.6.8+
- GDB 9.0+ 且启用 Python 支持
- Linux 操作系统

## 工作原理

### 步骤 1：初始化调试会话

**用于核心转储分析：**
```bash
gdb-cli load --binary <binary_path> --core <core_path> [--gdb-path <gdb_path>]
```

**用于运行进程调试：**
```bash
gdb-cli attach --pid <pid> [--binary <binary_path>]
```

**输出：** 一个 session_id，如 `"session_id": "a1b2c3"`。保存此 ID 用于后续命令。

### 步骤 2：收集初始信息

```bash
SESSION="<session_id>"

# 列出所有线程
gdb-cli threads -s $SESSION

# 获取回溯（包含局部变量）
gdb-cli bt -s $SESSION --full

# 获取寄存器
gdb-cli registers -s $SESSION
```

### 步骤 3：关联源代码（关键）

对于回溯中的每一帧：
1. **提取帧信息**：`{文件}:{行号} 在 {函数}`
2. **读取源代码上下文**：获取崩溃点前后各 20 行
3. **获取局部变量**：`gdb-cli locals-cmd -s $SESSION --frame <N>`
4. **分析**：将代码逻辑与变量值关联

**示例关联：**
```
Frame #0: process_data() at src/worker.c:87
源代码显示：
  85: Node* node = get_node(id);
  86: if (node == NULL) return;
  87: node->data = value;  <- 崩溃位置

变量显示：
  node = 0x0 (NULL)

分析：第 86 行的 NULL 检查没有捕获到问题。
```

### 步骤 4：深入调查

```bash
# 检查变量
gdb-cli eval-cmd -s $SESSION "variable_name"
gdb-cli eval-cmd -s $SESSION "ptr->field"
gdb-cli ptype -s $SESSION "struct_name"

# 内存检查
gdb-cli memory -s $SESSION "0x7fffffffe000" --size 64

# 反汇编
gdb-cli disasm -s $SESSION --count 20

# 检查所有线程（用于死锁分析）
gdb-cli thread-apply -s $SESSION bt --all

# 查看共享库
gdb-cli sharedlibs -s $SESSION
```

### 步骤 5：会话管理

```bash
# 列出活跃会话
gdb-cli sessions

# 检查会话状态
gdb-cli status -s $SESSION

# 停止会话（清理）
gdb-cli stop -s $SESSION
```

## 常见调试模式

### 模式：空指针解引用

**特征：**
- 在内存访问指令处崩溃
- 指针变量值为 0x0

**调查：**
```bash
gdb-cli registers -s $SESSION  # 检查 RIP
gdb-cli eval-cmd -s $SESSION "ptr"  # 检查指针值
```

### 模式：死锁

**特征：**
- 多个线程卡在锁函数中
- 回溯中出现 `pthread_mutex_lock`

**调查：**
```bash
gdb-cli thread-apply -s $SESSION bt --all
# 查找循环等待模式
```

### 模式：内存损坏

**特征：**
- 在 malloc/free 中崩溃
- 变量值为垃圾数据

**调查：**
```bash
gdb-cli memory -s $SESSION "&variable" --size 128
gdb-cli registers -s $SESSION
```

## 示例

### 示例 1：核心转储分析

```bash
# 加载核心转储
gdb-cli load --binary ./myapp --core /tmp/core.1234

# 获取崩溃位置
gdb-cli bt -s a1b2c3 --full

# 检查崩溃帧
gdb-cli locals-cmd -s a1b2c3 --frame 0
```

### 示例 2：运行进程调试

```bash
# 附加到卡住的服务器
gdb-cli attach --pid 12345

# 检查所有线程
gdb-cli threads -s b2c3d4

# 获取所有回溯
gdb-cli thread-apply -s b2c3d4 bt --all
```

## 最佳实践

- 在根据变量值得出结论之前，始终先阅读源代码
- 对于大量线程或深层回溯，使用 `--range` 进行分页
- 在检查复杂的数据结构值之前，使用 `ptype` 理解其类型
- 对于多线程问题，检查所有线程
- 将类型与源代码定义交叉引用

## 安全与注意事项

- 此技能需要 GDB 访问进程和核心转储
- 附加进程可能需要适当的权限（sudo、ptrace_scope）
- 核心转储可能包含敏感数据——请谨慎处理
- 仅调试您有授权分析的进程

## 相关技能

- `@systematic-debugging` - 通用调试方法论
- `@test-driven-development` - 实现前先写测试

## 链接

- **仓库**: https://github.com/Cerdore/gdb-cli
- **PyPI**: https://pypi.org/project/gdb-cli/
- **文档**: https://github.com/Cerdore/gdb-cli#readme

## 限制
- 仅当任务明确符合上述描述范围时使用此技能。
- 不要将输出作为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
