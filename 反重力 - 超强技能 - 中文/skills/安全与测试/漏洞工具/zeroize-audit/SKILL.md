---
name: zeroize-audit
description: "检测源代码中敏感数据缺失的零化操作，并识别被编译器优化移除的零化操作，配合汇编级分析与控制流验证。用于审计处理密钥、口令或其他敏感数据的 C/C++/Rust 代码。触发词：零化审计、敏感数据清理、编译器优化检测、内存安全审计、密钥清除、DSE 检测、栈残留、寄存器溢出。"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
  - Task
  - AskUserQuestion
  - mcp__serena__activate_project
  - mcp__serena__find_symbol
  - mcp__serena__find_referencing_symbols
  - mcp__serena__get_symbols_overview
risk: unknown
source: community
---

# zeroize-audit — Claude 技能

## 使用场景
- 审计密码学实现（密钥、种子、随机数、机密数据）
- 审查认证系统（口令、令牌、会话数据）
- 分析处理 PII 或敏感凭证的代码
- 验证安全关键代码库中的安全清理
- 调查敏感数据处理的内存安全

## 不适用场景
- 无安全重点的通用代码审查
- 性能优化（除非与安全擦除相关）
- 与敏感数据无关的重构任务
- 不含可识别机密或敏感数值的代码

---

## 目的
检测源代码中敏感数据缺失的零化操作，并识别被编译器优化（如死存储消除）移除或削弱的零化操作，必须提供 LLVM IR/汇编证据。能力包括：
- 寄存器溢出和栈保留的汇编级分析
- 密钥副本的数据流追踪
- 堆分配器的安全告警
- 循环展开和 SSA 形式的语义 IR 分析
- 路径覆盖验证的控制流图分析
- 运行时验证测试生成

## 范围
- 对目标代码库只读（不修改被审计代码；将分析产物写入临时工作目录）。
- 生成结构化报告（JSON）。
- 需要有效的构建上下文（`compile_commands.json`）和可编译的翻译单元。
- "被优化掉"的发现必须附带编译器证据（IR/汇编差异）才有效。

---

## 输入参数

完整模式参见 `{baseDir}/schemas/input.json`。关键字段：

| 字段 | 必填 | 默认值 | 说明 |
|---|---|---|---|
| `path` | 是 | — | 仓库根目录 |
| `compile_db` | 否 | `null` | C/C++ 分析的 `compile_commands.json` 路径。未设置 `cargo_manifest` 时必填。 |
| `cargo_manifest` | 否 | `null` | Rust crate 分析的 `Cargo.toml` 路径。未设置 `compile_db` 时必填。 |
| `config` | 否 | — | 用于定义启发式规则和已批准擦除的 YAML |
| `opt_levels` | 否 | `["O0","O1","O2"]` | 用于 IR 对比的分析级别。O1 是诊断级别：若擦除在 O1 消失则为简单 DSE；O2 可捕获更激进的消除。 |
| `languages` | 否 | `["c","cpp","rust"]` | 要分析的语言 |
| `max_tus` | 否 | — | 从 compile DB 处理的翻译单元数量上限 |
| `mcp_mode` | 否 | `prefer` | `off`、`prefer` 或 `require` — 控制 Serena MCP 的使用方式 |
| `mcp_required_for_advanced` | 否 | `true` | 当 MCP 不可用时，将 `SECRET_COPY`、`MISSING_ON_ERROR_PATH` 和 `NOT_DOMINATING_EXITS` 降级为 `needs_review` |
| `mcp_timeout_ms` | 否 | — | MCP 语义查询的超时预算 |
| `poc_categories` | 否 | 全部 11 个可利用项 | 需要生成 PoC 的发现类别。C/C++ 发现：支持全部 11 个类别。Rust 发现：仅支持 `MISSING_SOURCE_ZEROIZE`、`SECRET_COPY` 和 `PARTIAL_WIPE`；其他 Rust 类别标记为 `poc_supported=false`。 |
| `poc_output_dir` | 否 | `generated_pocs/` | 生成的 PoC 输出目录 |
| `enable_asm` | 否 | `true` | 启用汇编生成与分析（步骤 8）；产生 `STACK_RETENTION`、`REGISTER_SPILL`。若 `emit_asm.sh` 缺失则自动禁用。 |
| `enable_semantic_ir` | 否 | `false` | 启用语义 LLVM IR 分析（步骤 9）；产生 `LOOP_UNROLLED_INCOMPLETE` |
| `enable_cfg` | 否 | `false` | 启用控制流图分析（步骤 10）；产生 `MISSING_ON_ERROR_PATH`、`NOT_DOMINATING_EXITS` |
| `enable_runtime_tests` | 否 | `false` | 启用运行时测试用例生成（步骤 11） |

---

## 前置条件

运行前请验证以下项。每项都有明确的失败处理方式。

**C/C++ 前置条件：**

| 前置条件 | 缺失时的失败处理 |
|---|---|
| `compile_db` 路径下的 `compile_commands.json` | 快速失败 — 不继续执行 |
| PATH 中的 `clang` | 快速失败 — 无法进行 IR/ASM 分析 |
| PATH 中的 `uvx`（用于 Serena） | 若 `mcp_mode=require`：失败。若 `mcp_mode=prefer`：在无 MCP 情况下继续；按置信度门控规则降级相关发现。 |
| `{baseDir}/tools/extract_compile_flags.py` | 快速失败 — 无法提取每个 TU 的编译参数 |
| `{baseDir}/tools/emit_ir.sh` | 快速失败 — 无法进行 IR 分析 |
| `{baseDir}/tools/emit_asm.sh` | 警告并跳过汇编发现（STACK_RETENTION、REGISTER_SPILL） |
| `{baseDir}/tools/mcp/check_mcp.sh` | 警告并视为 MCP 不可用 |
| `{baseDir}/tools/mcp/normalize_mcp_evidence.py` | 警告并使用原始 MCP 输出 |

**Rust 前置条件：**

| 前置条件 | 缺失时的失败处理 |
|---|---|
| `cargo_manifest` 路径下的 `Cargo.toml` | 快速失败 — 不继续执行 |
| `cargo check` 通过 | 快速失败 — crate 必须可构建 |
| PATH 中的 `cargo +nightly` | 快速失败 — MIR 和 LLVM IR 生成需要 nightly |
| PATH 中的 `uv` | 快速失败 — 运行 Python 分析脚本所需 |
| `{baseDir}/tools/validate_rust_toolchain.sh` | 警告 — 手动运行预检。检查所有工具、脚本、nightly，并可选检查 `cargo check`。使用 `--json` 输出机器可读结果，使用 `--manifest` 验证 crate 构建。 |
| `{baseDir}/tools/emit_rust_mir.sh` | 快速失败 — 无法进行 MIR 分析（支持 `--opt`、`--crate`、`--bin/--lib`；`--out` 可为文件或目录） |
| `{baseDir}/tools/emit_rust_ir.sh` | 快速失败 — 无法进行 LLVM IR 分析（`--opt` 必填；支持 `--crate`、`--bin/--lib`；`--out` 必须为 `.ll`） |
| `{baseDir}/tools/emit_rust_asm.sh` | 警告并跳过汇编发现（`STACK_RETENTION`、`REGISTER_SPILL`）。支持 `--opt`、`--crate`、`--bin/--lib`、`--target`、`--intel-syntax`；`--out` 可为 `.s` 文件或目录。 |
| `{baseDir}/tools/diff_rust_mir.sh` | 警告并跳过 MIR 级优化对比。接受 2 个及以上 MIR 文件，归一化后两两对比，报告 zeroize/drop-glue 模式首次消失的优化级别。 |
| `{baseDir}/tools/scripts/semantic_audit.py` | 警告并跳过语义源码分析 |
| `{baseDir}/tools/scripts/find_dangerous_apis.py` | 警告并跳过危险 API 扫描 |
| `{baseDir}/tools/scripts/check_mir_patterns.py` | 警告并跳过 MIR 分析 |
| `{baseDir}/tools/scripts/check_llvm_patterns.py` | 警告并跳过 LLVM IR 分析 |
| `{baseDir}/tools/scripts/check_rust_asm.py` | 警告并跳过 Rust 汇编分析（`STACK_RETENTION`、`REGISTER_SPILL`、drop-glue 检查）。分派到 `check_rust_asm_x86.py`（生产）或 `check_rust_asm_aarch64.py`（**实验性** — AArch64 发现需人工核验）。 |
| `{baseDir}/tools/scripts/check_rust_asm_x86.py` | x86-64 分析时 `check_rust_asm.py` 必需；缺失则警告并跳过 |
| `{baseDir}/tools/scripts/check_rust_asm_aarch64.py` | AArch64 分析时 `check_rust_asm.py` 必需（**实验性**）；缺失则警告并跳过 |

**通用前置条件：**

| 前置条件 | 缺失时的失败处理 |
|---|---|
| `{baseDir}/tools/generate_poc.py` | 快速失败 — PoC 生成是必需的 |

---

## 已批准的擦除 API

以下 API 被认定为有效的零化操作。可在 `{baseDir}/configs/` 中配置其他条目。

**C/C++**
- `explicit_bzero`
- `memset_s`
- `SecureZeroMemory`
- `OPENSSL_cleanse`
- `sodium_memzero`
- 易失性擦除循环（基于模式；参见 `{baseDir}/configs/default.yaml` 中的 `volatile_wipe_patterns`）
- 在 IR 中：`llvm.memset` 带 volatile 标记、易失性存储或不可被消除的擦除调用

**Rust**
- `zeroize::Zeroize` trait（`zeroize()` 方法）
- `Zeroizing<T>` 包装器（基于 drop）
- `ZeroizeOnDrop` derive 宏

---

## 发现能力

发现按所需证据分组。仅在所需工具可用时才尝试对应的发现。

| 发现 ID | 说明 | 所需条件 | PoC 支持 |
|---|---|---|---|
| `MISSING_SOURCE_ZEROIZE` | 源码中未发现零化操作 | 仅源码 | 是（C/C++ + Rust） |
| `PARTIAL_WIPE` | 大小错误或擦除不完整 | 仅源码 | 是（C/C++ + Rust） |
| `NOT_ON_ALL_PATHS` | 部分控制流路径上缺失零化（启发式） | 仅源码 | 是（仅 C/C++） |
| `SECRET_COPY` | 复制敏感数据时未跟踪零化 | 源码 + 推荐 MCP | 是（C/C++ + Rust） |
| `INSECURE_HEAP_ALLOC` | 密钥使用了不安全的分配器（malloc 而非 secure_malloc） | 仅源码 | 是（仅 C/C++） |
| `OPTIMIZED_AWAY_ZEROIZE` | 编译器移除了零化 | 必须 IR 差异（绝不能仅基于源码） | 是 |
| `STACK_RETENTION` | 栈帧在函数返回后可能残留密钥 | C/C++ 需汇编；Rust 需 LLVM IR `alloca`+`lifetime.end` 证据；汇编佐证可升级为 `confirmed` | 是（仅 C/C++） |
| `REGISTER_SPILL` | 密钥从寄存器溢出到栈 | C/C++ 需汇编；Rust 需 LLVM IR `load`+call-site 证据；汇编佐证可升级为 `confirmed` | 是（仅 C/C++） |
| `MISSING_ON_ERROR_PATH` | 错误处理路径缺少清理 | 必须 CFG 或 MCP | 是 |
| `NOT_DOMINATING_EXITS` | 擦除未支配所有退出点 | 必须 CFG 或 MCP | 是 |
| `LOOP_UNROLLED_INCOMPLETE` | 展开循环的擦除不完整 | 必须语义 IR | 是 |

---

## 智能体架构

分析流水线跨 8 个阶段使用 11 个智能体，由编排器（`{baseDir}/prompts/task.md`）通过 `Task` 调用。智能体将持久化的发现文件写入共享工作目录（`/tmp/zeroize-audit-{run_id}/`），支持并行执行并避免上下文压力。

| 智能体 | 阶段 | 用途 | 输出目录 |
|---|---|---|---|
| `0-preflight` | 阶段 0 | 预检（工具、工具链、compile DB、crate 构建）、配置合并、工作目录创建、TU 枚举 | `{workdir}/` |
| `1-mcp-resolver` | 阶段 1，第 1 波（仅 C/C++） | 通过 Serena MCP 解析符号、类型和跨文件引用 | `mcp-evidence/` |
| `2-source-analyzer` | 阶段 1，第 2a 波（仅 C/C++） | 识别敏感对象、检测擦除、验证正确性、数据流/堆 | `source-analysis/` |
| `2b-rust-source-analyzer` | 阶段 1，第 2b 波（仅 Rust，与 2a 并行） | 基于 Rustdoc JSON 的 trait 感知分析 + 危险 API 扫描 | `source-analysis/` |
| `3-tu-compiler-analyzer` | 阶段 2，第 3 波（仅 C/C++，N 个并行） | 每个 TU 的 IR 差异、汇编、语义 IR、CFG 分析 | `compiler-analysis/{tu_hash}/` |
| `3b-rust-compiler-analyzer` | 阶段 2，第 3R 波（仅 Rust，单个智能体） | crate 级 MIR、LLVM IR 和汇编分析 | `rust-compiler-analysis/` |
| `4-report-assembler` | 阶段 3（中间）+ 阶段 6（最终） | 收集所有智能体的发现，应用置信度门控；合并 PoC 结果并生成最终报告 | `report/` |
| `5-poc-generator` | 阶段 4 | 编写定制化的概念验证程序（C/C++：全部类别；Rust：MISSING_SOURCE_ZEROIZE、SECRET_COPY、PARTIAL_WIPE） | `poc/` |
| `5b-poc-validator` | 阶段 5 | 编译并运行所有 PoC | `poc/` |
| `5c-poc-verifier` | 阶段 5 | 验证每个 PoC 确实证明了其声明的发现 | `poc/` |
| `6-test-generator` | 阶段 7（可选） | 生成运行时验证测试用例 | `tests/` |

编排器每次从 `{baseDir}/workflows/` 读取一个阶段的工作流文件，并维护 `orchestrator-state.json` 用于上下文压缩后恢复。智能体通过文件路径（`config_path`）接收配置，而非配置值。

### 执行流程

```
阶段 0: 0-preflight 智能体 — 预检 + 配置 + 创建工作目录 + 枚举 TU
           → 写入 orchestrator-state.json、merged-config.yaml、preflight.json
阶段 1: 第 1 波： 1-mcp-resolver              （若 mcp_mode=off 或 language_mode=rust 则跳过）
         第 2a 波：2-source-analyzer          （仅 C/C++；若无 compile_db 则跳过）  ─┐ 并行
         第 2b 波：2b-rust-source-analyzer    （仅 Rust；若无 cargo_manifest 则跳过） ─┘
阶段 2: 第 3 波： 3-tu-compiler-analyzer x N  （仅 C/C++；每个 TU 并行）
         第 3R 波：3b-rust-compiler-analyzer  （仅 Rust；crate 级单个智能体）
阶段 3: 第 4 波： 4-report-assembler          （mode=interim → findings.json；读取所有智能体输出）
阶段 4: 第 5 波： 5-poc-generator             （C/C++：全部类别；Rust：MISSING_SOURCE_ZEROIZE、SECRET_COPY、PARTIAL_WIPE；其他 Rust 发现：poc_supported=false）
阶段 5: PoC 验证与核查
           步骤 1：5b-poc-validator 智能体      （编译并运行所有 PoC）
           步骤 2：5c-poc-verifier 智能体       （验证每个 PoC 确实证明了其声明的发现）
           步骤 3：编排器通过 AskUserQuestion 向用户展示验证失败项
           步骤 4：编排器将所有结果合并到 poc_final_results.json
阶段 6: 第 6 波： 4-report-assembler           （mode=final → 合并 PoC 结果、final-report.md）
阶段 7: 第 7 波： 6-test-generator             （可选）
阶段 8: 编排器 — 返回 final-report.md
```

## 交叉引用约定

ID 按智能体命名空间分配，以避免并行执行时的冲突：

| 实体 | 模式 | 分配方 |
|---|---|---|
| 敏感对象（C/C++） | `SO-0001`–`SO-4999` | `2-source-analyzer` |
| 敏感对象（Rust） | `SO-5000`–`SO-9999`（Rust 命名空间） | `2b-rust-source-analyzer` |
| 源码发现（C/C++） | `F-SRC-NNNN` | `2-source-analyzer` |
| 源码发现（Rust） | `F-RUST-SRC-NNNN` | `2b-rust-source-analyzer` |
| IR 发现（C/C++） | `F-IR-{tu_hash}-NNNN` | `3-tu-compiler-analyzer` |
| 汇编发现（C/C++） | `F-ASM-{tu_hash}-NNNN` | `3-tu-compiler-analyzer` |
| CFG 发现 | `F-CFG-{tu_hash}-NNNN` | `3-tu-compiler-analyzer` |
| 语义 IR 发现 | `F-SIR-{tu_hash}-NNNN` | `3-tu-compiler-analyzer` |
| Rust MIR 发现 | `F-RUST-MIR-NNNN` | `3b-rust-compiler-analyzer` |
| Rust LLVM IR 发现 | `F-RUST-IR-NNNN` | `3b-rust-compiler-analyzer` |
| Rust 汇编发现 | `F-RUST-ASM-NNNN` | `3b-rust-compiler-analyzer` |
| 翻译单元 | `TU-{hash}` | 编排器 |
| 最终发现 | `ZA-NNNN` | `4-report-assembler` |

每个发现 JSON 对象都包含 `related_objects`、`related_findings` 和 `evidence_files` 字段，用于智能体之间的交叉引用。

---

## 检测策略

分析分两阶段运行。完整的分步指南请参见 `{baseDir}/references/detection-strategy.md`。

| 阶段 | 步骤 | 产生的发现 | 所需工具 |
|---|---|---|---|
| 阶段 1（源码） | 1–6 | `MISSING_SOURCE_ZEROIZE`、`PARTIAL_WIPE`、`NOT_ON_ALL_PATHS`、`SECRET_COPY`、`INSECURE_HEAP_ALLOC` | 源码 + compile DB |
| 阶段 2（编译器） | 7–12 | `OPTIMIZED_AWAY_ZEROIZE`、`STACK_RETENTION`*、`REGISTER_SPILL`*、`LOOP_UNROLLED_INCOMPLETE`†、`MISSING_ON_ERROR_PATH`‡、`NOT_DOMINATING_EXITS`‡ | `clang`、IR/ASM 工具 |

\* 需要 `enable_asm=true`（默认）
† 需要 `enable_semantic_ir=true`
‡ 需要 `enable_cfg=true`

---


## 输出格式

每次运行产生两个输出：

1. **`final-report.md`** — 完整的 Markdown 报告（主要的人类可读输出）
2. **`findings.json`** — 符合 `{baseDir}/schemas/output.json` 模式（供机器消费和下游工具使用）

### Markdown 报告结构

Markdown 报告（`final-report.md`）包含以下章节：

- **Header**：运行元数据（run_id、时间戳、仓库、compile_db、配置摘要）
- **Executive Summary**：按严重性、置信度和类别统计的发现数
- **Sensitive Objects Inventory**：所有已识别对象的表格，含 ID、类型、位置
- **Findings**：按严重性、再按置信度分组。每条发现包括位置、对象、所有证据（源码/IR/ASM/CFG）、编译器证据详情和推荐修复
- **Superseded Findings**：被 CFG 支持的发现所取代的源码发现
- **Confidence Gate Summary**：应用的降级和被拒绝的覆盖
- **Analysis Coverage**：已分析的 TU、智能体成功/失败、启用的功能
- **Appendix: Evidence Files**：发现 ID 与证据文件路径的映射

### 结构化 JSON

`findings.json` 文件遵循 `{baseDir}/schemas/output.json` 中的模式。每个 `Finding` 对象：

```json
{
  "id": "ZA-0001",
  "category": "OPTIMIZED_AWAY_ZEROIZE",
  "severity": "high",
  "confidence": "confirmed",
  "language": "c",
  "file": "src/crypto.c",
  "line": 42,
  "symbol": "key_buf",
  "evidence": "store volatile i8 0 count: O0=32, O2=0 — wipe eliminated by DSE",
  "compiler_evidence": {
    "opt_levels": ["O0", "O2"],
    "o0": "32 volatile stores targeting key_buf",
    "o2": "0 volatile stores (all eliminated)",
    "diff_summary": "All volatile wipe stores removed at O2 — classic DSE pattern"
  },
  "suggested_fix": "Replace memset with explicit_bzero or add compiler_fence(SeqCst) after the wipe",
  "poc": {
    "file": "generated_pocs/ZA-0001.c",
    "makefile_target": "ZA-0001",
    "compile_opt": "-O2",
    "requires_manual_adjustment": false,
    "validated": true,
    "validation_result": "exploitable"
  }
}
```

完整模式和枚举值请参见 `{baseDir}/schemas/output.json`。

---

## 置信度门控

### 证据阈值

一条发现至少需要 **2 个独立信号** 才能标记为 `confirmed`。仅有 1 个信号时标记为 `likely`。没有强信号（仅有名称模式匹配）时标记为 `needs_review`。

信号包括：名称模式匹配、类型提示匹配、显式注解、IR 证据、ASM 证据、MCP 交叉引用、CFG 证据、PoC 验证。

### PoC 验证作为证据信号

每条发现都会通过定制 PoC 进行验证。编译执行后，还会进一步验证每个 PoC 确实在测试其声称的漏洞。合并结果作为证据信号：

| PoC 结果 | 已验证 | 影响 |
|---|---|---|
| 退出码 0（可利用） | 是 | 强信号 — 可将 `likely` 升级为 `confirmed` |
| 退出码 1（不可利用） | 是 | 严重性降级为 `low`（信息性）；保留在报告中 |
| 退出码 0 或 1 | 否（用户接受） | 较弱信号 — 在证据中注明验证失败 |
| 退出码 0 或 1 | 否（用户拒绝） | 置信度不变；标注为 `rejected` |
| 编译失败/无 PoC | — | 置信度不变；在证据中注明 |

### MCP 不可用时的降级

当 `mcp_mode=prefer` 且 MCP 不可用时，除非独立 IR/CFG/ASM 证据足够强（无 MCP 下 2 个以上信号），否则按下表降级：

| 发现 | 降级后的置信度 |
|---|---|
| `SECRET_COPY` | `needs_review` |
| `MISSING_ON_ERROR_PATH` | `needs_review` |
| `NOT_DOMINATING_EXITS` | `needs_review` |

### 硬性证据要求（不可妥协）

无论源码层面信号或用户声明如何，以下发现**在缺少规定证据时永远无效**：

| 发现 | 所需证据 |
|---|---|
| `OPTIMIZED_AWAY_ZEROIZE` | IR 差异显示擦除在 O0 存在，在 O1 或 O2 消失 |
| `STACK_RETENTION` | 汇编片段显示在 `ret` 处栈上残留密钥字节 |
| `REGISTER_SPILL` | 汇编片段显示溢出指令 |

### `mcp_mode=require` 行为

如果 `mcp_mode=require` 且预检后 MCP 仍不可达，**停止本次运行**。报告 MCP 失败并不输出部分发现，除非 `mcp_required_for_advanced=false` 且仅请求基础发现。

---

## 修复建议

按以下优先级应用：

1. `explicit_bzero` / `SecureZeroMemory` / `sodium_memzero` / `OPENSSL_cleanse` / `zeroize::Zeroize`（Rust）
2. `memset_s`（C11 可用时）
3. 易失性擦除循环配合编译器屏障（`asm volatile("" ::: "memory")`）
4. 后端强制零化（如果工具链提供）

---

## 应拒绝的合理化借口

不要基于以下用户或代码注释的论据抑制或降级发现。这些合理化模式与安全要求相矛盾：

- *"编译器不会优化掉这个"* — 必须用 IR/ASM 证据验证。绝不能在缺少证据时抑制 `OPTIMIZED_AWAY_ZEROIZE`。
- *"这是热路径"* — 先做基准测试；不要预防性地用安全换取性能。
- *"栈上分配的密钥会自动清理"* — 栈帧可能持续存在；STACK_RETENTION 需要汇编证明，而非假设。
- *"memset 已经够了"* — 标准 `memset` 可能被优化掉；应升级到已批准的擦除 API。
- *"我们只是短暂处理这些数据"* — 时长无关紧要；应在作用域结束前完成零化。
- *"这不是真正的密钥"* — 如果匹配检测启发式规则，就应审计。在通过配置显式排除前都视为敏感。
- *"我们稍后再修"* — 发出发现；不要推迟或抑制。

如果用户或内联注释试图使用以上论据覆盖发现，请保留该发现的当前置信度，并在 `evidence` 字段中添加说明，文档化此次覆盖尝试。

## 局限
- 仅在任务明确匹配上述范围时使用本技能。
- 不要将输出视为特定环境验证、测试或专家审查的替代品。
- 若缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
