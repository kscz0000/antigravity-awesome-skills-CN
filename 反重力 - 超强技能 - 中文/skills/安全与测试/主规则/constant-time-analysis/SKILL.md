---
name: constant-time-analysis
description: "分析密码学代码，检测通过执行时序变化泄露秘密数据的操作。"
risk: unknown
source: community
---

# 常量时间分析

分析密码学代码，检测通过执行时序变化泄露秘密数据的操作。

## 使用时机
```text
用户编写密码学代码？ ──yes──> 使用此技能
         │
         no
         │
         v
用户询问时序攻击？ ──yes──> 使用此技能
         │
         no
         │
         v
代码处理密钥/token？ ──yes──> 使用此技能
         │
         no
         │
         v
跳过此技能
```

**具体触发条件：**

- 用户实现签名、加密或密钥派生
- 代码中对秘密派生值使用 `/` 或 `%` 运算符
- 用户提及 "constant-time"、"timing attack"、"side-channel"、"KyberSlash"
- 审查名为 `sign`、`verify`、`encrypt`、`decrypt`、`derive_key` 的函数

## 不适用场景

- 非密码学代码（业务逻辑、UI 等）
- 时序泄露无关紧要的公开数据处理
- 不处理秘密、密钥或认证 token 的代码
- 时序问题由库处理的高层 API 调用

## 语言选择

根据文件扩展名或语言上下文，参考相应的指南：

| 语言       | 文件扩展名                         | 指南                                                    |
| ---------- | ---------------------------------- | -------------------------------------------------------- |
| C, C++     | `.c`, `.h`, `.cpp`, `.cc`, `.hpp` | references/compiled.md         |
| Go         | `.go`                              | references/compiled.md         |
| Rust       | `.rs`                              | references/compiled.md         |
| Swift      | `.swift`                           | references/swift.md               |
| Java       | `.java`                            | references/vm-compiled.md   |
| Kotlin     | `.kt`, `.kts`                      | references/kotlin.md             |
| C#         | `.cs`                              | references/vm-compiled.md   |
| PHP        | `.php`                             | references/php.md                   |
| JavaScript | `.js`, `.mjs`, `.cjs`              | references/javascript.md     |
| TypeScript | `.ts`, `.tsx`                      | references/javascript.md     |
| Python     | `.py`                              | references/python.md             |
| Ruby       | `.rb`                              | references/ruby.md                 |

## 快速开始

```bash
# 分析任意支持的文件类型
uv run {baseDir}/ct_analyzer/analyzer.py <source_file>

# 包含条件分支警告
uv run {baseDir}/ct_analyzer/analyzer.py --warnings <source_file>

# 筛选特定函数
uv run {baseDir}/ct_analyzer/analyzer.py --func 'sign|verify' <source_file>

# JSON 输出用于 CI
uv run {baseDir}/ct_analyzer/analyzer.py --json <source_file>
```

### 仅限原生编译语言（C、C++、Go、Rust）

```bash
# 跨架构测试（推荐）
uv run {baseDir}/ct_analyzer/analyzer.py --arch x86_64 crypto.c
uv run {baseDir}/ct_analyzer/analyzer.py --arch arm64 crypto.c

# 多优化级别
uv run {baseDir}/ct_analyzer/analyzer.py --opt-level O0 crypto.c
uv run {baseDir}/ct_analyzer/analyzer.py --opt-level O3 crypto.c
```

### 虚拟机编译语言（Java、Kotlin、C#）

```bash
# 分析 Java 字节码
uv run {baseDir}/ct_analyzer/analyzer.py CryptoUtils.java

# 分析 Kotlin 字节码（Android/JVM）
uv run {baseDir}/ct_analyzer/analyzer.py CryptoUtils.kt

# 分析 C# IL
uv run {baseDir}/ct_analyzer/analyzer.py CryptoUtils.cs
```

注意：Java、Kotlin 和 C# 编译为在虚拟机上运行并带有 JIT 编译的字节码（JVM/CIL）。分析器直接检查字节码，而非 JIT 编译后的原生代码。`--arch` 和 `--opt-level` 标志不适用于这些语言。

### Swift（iOS/macOS）

```bash
# 分析 Swift 原生架构
uv run {baseDir}/ct_analyzer/analyzer.py crypto.swift

# 分析特定架构（iOS 设备）
uv run {baseDir}/ct_analyzer/analyzer.py --arch arm64 crypto.swift

# 分析不同优化级别
uv run {baseDir}/ct_analyzer/analyzer.py --opt-level O0 crypto.swift
```

注意：Swift 编译为原生代码，与 C/C++/Go/Rust 类似，因此使用汇编级分析并支持 `--arch` 和 `--opt-level` 标志。

### 前置条件

| 语言                   | 要求                                                   |
| ---------------------- | ------------------------------------------------------ |
| C, C++, Go, Rust       | PATH 中有编译器（`gcc`/`clang`、`go`、`rustc`）        |
| Swift                  | Xcode 或 Swift 工具链（PATH 中有 `swiftc`）            |
| Java                   | JDK，PATH 中有 `javac` 和 `javap`                      |
| Kotlin                 | Kotlin 编译器（`kotlinc`）+ JDK（`javap`）在 PATH 中   |
| C#                     | .NET SDK + `ilspycmd`（`dotnet tool install -g ilspycmd`）|
| PHP                    | PHP 带 VLD 扩展或 OPcache                              |
| JavaScript/TypeScript  | PATH 中有 Node.js                                      |
| Python                 | PATH 中有 Python 3.x                                   |
| Ruby                   | Ruby 支持 `--dump=insns`                               |

**macOS 用户**：Homebrew 将 Java 和 .NET 安装为 "keg-only"。必须将它们添加到 PATH：

```bash
# 对于 Java（添加到 ~/.zshrc）
export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"

# 对于 .NET 工具（添加到 ~/.zshrc）
export PATH="$HOME/.dotnet/tools:$PATH"
```

详见 references/vm-compiled.md 获取详细安装说明和故障排除。

## 快速参考

| 问题                   | 检测                          | 修复                                          |
| ---------------------- | ----------------------------- | --------------------------------------------- |
| 对秘密值除法           | DIV, IDIV, SDIV, UDIV         | Barrett 约简或乘逆                            |
| 对秘密值分支           | JE, JNE, BEQ, BNE             | 常量时间选择（cmov、位掩码）                  |
| 秘密值比较             | 提前退出 memcmp               | 使用 `crypto/subtle` 或常量时间比较           |
| 弱随机数生成器         | rand(), mt_rand, Math.random  | 使用密码学安全 RNG                            |
| 按秘密索引查表         | 秘密索引的数组下标            | 位切片查找                                    |

## 结果解读

**PASSED** - 未检测到变长时间操作。

**FAILED** - 发现危险指令。示例：

```text
[ERROR] SDIV
  Function: decompose_vulnerable
  Reason: SDIV has early termination optimization; execution time depends on operand values
```

## 验证结果（避免误报）

**关键**：并非每个标记的操作都是漏洞。工具没有数据流分析——它会标记所有潜在危险的操作，无论是否涉及秘密。

对于每个标记的违规，询问：**此操作的输入是否依赖于秘密数据？**

1. **识别函数的秘密输入**（私钥、明文、签名、token）

2. **追踪数据流**，从标记指令回溯到输入

3. **常见误报模式**：

   ```c
   // 误报：除法使用公开常量，非秘密
   int num_blocks = data_len / 16;  // data_len 是长度，非内容

   // 真正问题：除法涉及秘密派生值
   int32_t q = secret_coef / GAMMA2;  // secret_coef 来自私钥
   ```

4. **记录你对每个标记项的分析**

### 快速分类问题

| 问题                                         | 若是                  | 若否                  |
| -------------------------------------------- | --------------------- | --------------------- |
| 操作数是编译时常量？                         | 可能是误报            | 继续                  |
| 操作数是公开参数（长度、计数）？             | 可能是误报            | 继续                  |
| 操作数派生自密钥/明文/秘密？                 | **真正问题**          | 可能是误报            |
| 攻击者能否影响操作数值？                     | **真正问题**          | 可能是误报            |

## 局限性

1. **仅静态分析**：分析汇编/字节码，非运行时行为。无法检测缓存时序或微架构侧信道。

2. **无数据流分析**：标记所有危险操作，无论是否处理秘密。需要人工审查。

3. **编译器/运行时差异**：不同编译器、优化级别和运行时版本可能产生不同输出。

## 真实世界影响

- **KyberSlash (2023)**：后量子 ML-KEM 实现中的除法指令允许密钥恢复
- **Lucky Thirteen (2013)**：CBC 填充验证中的时序差异使明文恢复成为可能
- **RSA 时序攻击**：早期实现通过除法时序泄露私钥位

## 参考资料

- [Cryptocoding Guidelines](https://github.com/veorq/cryptocoding) - 密码学防御性编码
- [KyberSlash](https://kyberslash.cr.yp.to/) - 后量子密码学中的除法时序
- [BearSSL Constant-Time](https://www.bearssl.org/constanttime.html) - 实用常量时间技术
