---
name: dwarf-expert
description: 提供 DWARF 调试文件分析和 DWARF 调试格式/标准（v3-v5）理解的专业知识。在理解 DWARF 信息、与 DWARF 文件交互、回答 DWARF 相关问题或处理解析 DWARF 数据的代码时触发。
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - WebSearch
risk: unknown
source: community
---
# 概述
本技能提供关于 DWARF 标准的技术知识和专业知识，以及如何与 DWARF 文件交互。任务包括回答关于 DWARF 标准的问题、提供各种 DWARF 功能的示例、解析和/或创建 DWARF 文件，以及编写/修改/分析与 DWARF 数据交互的代码。

## 何时使用此技能
- 理解或解析编译后二进制文件中的 DWARF 调试信息
- 回答关于 DWARF 标准（v3、v4、v5）的问题
- 编写或审查与 DWARF 数据交互的代码
- 使用 `dwarfdump` 或 `readelf` 提取调试信息
- 使用 `llvm-dwarfdump --verify` 验证 DWARF 数据完整性
- 使用 DWARF 解析库（libdwarf、pyelftools、gimli 等）

## 何时不使用此技能
- **DWARF v1/v2 分析**：专业知识仅限于版本 3、4 和 5。
- **通用 ELF 解析**：如果不需要 DWARF 数据，请使用标准 ELF 工具。
- **可执行文件调试**：调试可执行代码/运行时行为时，请使用专用调试工具（gdb、lldb 等）。
- **二进制逆向工程**：除非专门分析 DWARF 节，否则请使用专用逆向工程工具（Ghidra、IDA）。
- **编译器调试**：DWARF 生成问题是编译器特定的，不在此涵盖范围内。

# 权威来源
当需要特定的 DWARF 标准信息时，请使用以下权威来源：

1. **官方 DWARF 标准（dwarfstd.org）**：使用网络搜索在 dwarfstd.org 上查找 DWARF 规范的特定章节。搜索查询如 "DWARF5 DW_TAG_subprogram attributes site:dwarfstd.org" 非常有效。

2. **LLVM DWARF 实现**：LLVM 项目位于 `llvm/lib/DebugInfo/DWARF/` 的 DWARF 处理代码可作为可靠的参考实现。关键文件包括：
   - `DWARFDie.cpp` - DIE 处理和属性访问
   - `DWARFUnit.cpp` - 编译单元解析
   - `DWARFDebugLine.cpp` - 行号信息
   - `DWARFVerifier.cpp` - 验证逻辑

3. **libdwarf**：位于 github.com/davea42/libdwarf-code 的参考 C 实现提供了 DWARF 数据结构的详细处理。

# 验证工作流
使用 `llvm-dwarfdump` 验证选项来验证 DWARF 数据完整性：

## 结构验证
```bash
# 验证 DWARF 结构（编译单元、DIE 关系、地址范围）
llvm-dwarfdump --verify <binary>

# 详细错误输出及摘要
llvm-dwarfdump --verify --error-display=full <binary>

# 机器可读的 JSON 错误摘要
llvm-dwarfdump --verify --verify-json=errors.json <binary>
```

## 质量指标
```bash
# 以 JSON 格式输出调试信息质量指标
llvm-dwarfdump --statistics <binary>
```

`--statistics` 输出有助于比较不同编译器版本和优化级别的调试信息质量。

## 常见验证模式
- **编译后**：在分发前验证二进制文件具有有效的 DWARF
- **比较构建**：使用 `--statistics` 检测调试信息质量回归
- **调试调试器**：识别导致调试器问题的格式错误的 DWARF
- **DWARF 工具开发**：针对已知良好的二进制文件验证解析器输出

# 解析 DWARF 调试信息
## readelf
ELF 文件可以通过 `readelf` 命令解析（{baseDir}/reference/readelf.md）。用于通用 ELF 信息，但对于 DWARF 特定的解析，请优先使用 `dwarfdump`。

## dwarfdump
DWARF 文件可以通过 `dwarfdump` 命令解析，它在解析和显示复杂 DWARF 信息方面比 `readelf` 更有效，应该用于大多数 DWARF 解析任务（{baseDir}/reference/dwarfdump.md）。

# 代码工作
本技能支持编写、修改和审查与 DWARF 数据交互的代码。这可能涉及从头解析 DWARF 调试数据的代码，或利用库来解析和与 DWARF 数据交互的代码（{baseDir}/reference/coding.md）。

# 选择方法
```
┌─ 需要验证 DWARF 数据完整性？
│   └─ 使用 `llvm-dwarfdump --verify`（见上方验证工作流）
├─ 需要回答关于 DWARF 标准的问题？
│   └─ 搜索 dwarfstd.org 或参考 LLVM/libdwarf 源码
├─ 需要简单的节转储或通用 ELF 信息？
│   └─ 使用 `readelf`（{baseDir}/reference/readelf.md）
├─ 需要解析、搜索和/或转储 DWARF DIE 节点？
│   └─ 使用 `dwarfdump`（{baseDir}/reference/dwarfdump.md）
└─ 需要编写、修改或审查与 DWARF 数据交互的代码？
    └─ 参考编码参考（{baseDir}/reference/coding.md）
```

## 限制
- 仅当任务明确符合上述描述的范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
