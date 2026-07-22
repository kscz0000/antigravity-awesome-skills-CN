---
name: sharp-edges
description: "识别容易出错的 API、危险配置和易引发安全失误的设计缺陷。适用于审查 API 设计、配置模式、加密库人体工学，或评估代码是否遵循'默认安全'原则。触发词：锐边分析、API安全、加密API、危险默认值、脚枪设计、安全审查、配置安全、footgun、sharp edges"
risk: unknown
source: community
---

# 锐边分析

评估 API、配置和接口是否具备对开发者误用的抵抗力。识别那些"最省力的路径"会导致不安全的设计。

## 适用场景
- 审查 API 或库的设计决策
- 审计配置模式中的危险选项
- 评估加密 API 的人体工学
- 评估认证/授权接口
- 审查任何向开发者暴露安全相关选择的代码

## 不适用场景

- 实现层面的 bug（使用标准代码审查）
- 业务逻辑缺陷（使用领域特定分析）
- 性能优化（不同的关注点）

## 核心原则

**成功之坑**：安全的使用方式应该是阻力最小的路径。如果开发者必须理解密码学、仔细阅读文档或记住特殊规则才能避免漏洞，那么这个 API 就是失败的。

## 应拒绝的借口

| 借口 | 为什么是错的 | 应采取的行动 |
|------|-------------|-------------|
| "文档里写了" | 开发者在截止日期压力下不会读文档 | 让安全选项成为默认值或唯一选项 |
| "高级用户需要灵活性" | 灵活性制造脚枪；大多数"高级"用法只是复制粘贴 | 提供安全的高层 API；隐藏底层原语 |
| "这是开发者的责任" | 推卸责任；是你设计了脚枪 | 消除脚枪或使其无法被误用 |
| "没人会那么干" | 开发者在压力下什么都做得出来 | 假设开发者最大程度的困惑 |
| "只是个配置选项" | 配置就是代码；错误的配置会被部署到生产环境 | 验证配置；拒绝危险组合 |
| "我们需要向后兼容" | 不安全的默认值不能靠"老规矩"保留 | 大声弃用；强制迁移 |

## 锐边分类

### 1. 算法/模式选择脚枪

允许开发者选择算法的 API 就是在邀请选错。

**JWT 模式**（经典案例）：
- Header 指定算法：攻击者可设置 `"alg": "none"` 绕过签名
- 算法混淆：切换 RS256→HS256 时，RSA 公钥被用作 HMAC 密钥
- 根本原因：让不可信输入控制安全关键决策

**检测模式：**
- 函数参数如 `algorithm`、`mode`、`cipher`、`hash_type`
- 选择加密原语的枚举/字符串
- 安全机制的配置选项

**示例 - PHP password_hash 允许弱算法：**
```php
// 危险：允许 crc32、md5、sha1
password_hash($password, PASSWORD_DEFAULT); // 正确 - 无需选择
hash($algorithm, $password); // 错误：接受 "crc32"
```

### 2. 危险默认值

不安全的默认值，或零/空值导致安全特性被禁用。

**OTP 生命周期模式：**
```python
# 当 lifetime=0 时会发生什么？
def verify_otp(code, lifetime=300):  # 默认 300 秒
    if lifetime == 0:
        return True  # 糟糕：0 意味着"全部接受"？
        # 还是意味着"立即过期"？
```

**检测模式：**
- 接受 0 的超时/生命周期（无限？立即过期？）
- 绕过检查的空字符串
- 跳过验证的 null 值
- 禁用安全功能的布尔默认值
- 语义未定义的负值

**应提出的问题：**
- `timeout=0` 会怎样？`max_attempts=0` 呢？`key=""` 呢？
- 默认值是否是最安全的选项？
- 是否有默认值能完全禁用安全特性？

### 3. 原语 API vs 语义 API

暴露原始字节而非有意义类型的 API 会导致类型混淆。

**Libsodium vs Halite 模式：**

```php
// Libsodium（原语）：字节就是字节
sodium_crypto_box($message, $nonce, $keypair);
// 容易出错：交换 nonce/keypair、复用 nonce、使用错误的密钥类型

// Halite（语义）：类型强制正确使用
Crypto::seal($message, new EncryptionPublicKey($key));
// 错误的密钥类型 = 类型错误，而非静默失败
```

**检测模式：**
- 函数对不同的安全概念使用 `bytes`、`string`、`[]byte`
- 参数可以在没有类型错误的情况下被交换
- 对密钥、nonce、密文、签名使用相同类型

**比较操作脚枪：**
```go
// 时间安全比较看起来和不安全的一样
if hmac == expected { }           // 错误：时序攻击
if hmac.Equal(mac, expected) { }  // 正确：常量时间
// 相同的类型，不同的安全属性
```

### 4. 配置断崖

一个错误的设置就会造成灾难性失败，且没有任何警告。

**检测模式：**
- 完全禁用安全的布尔标志
- 未被验证的字符串配置
- 危险交互的设置组合
- 覆盖安全设置的环境变量
- 有合理默认值但无验证的构造函数参数（调用方可以用不安全的值覆盖）

**示例：**
```yaml
# 一个拼写错误 = 灾难
verify_ssl: fasle  # 拼写错误被静默接受为真值？

# 魔法值
session_timeout: -1  # 这是"永不过期"的意思？

# 危险组合被静默接受
auth_required: true
bypass_auth_for_health_checks: true
health_check_path: "/"  # 完蛋
```

```php
// 合理的默认值不能保护糟糕的调用方
public function __construct(
    public string $hashAlgo = 'sha256',  // 好的默认值...
    public int $otpLifetime = 120,       // ...但接受 md5、0 等
) {}
```

详见 config-patterns.md 获取详细模式。

### 5. 静默失败

错误不浮出水面，或成功掩盖了失败。

**检测模式：**
- 安全失败时返回布尔值而非抛出异常
- 安全操作周围的空 catch 块
- 解析错误时替换为默认值
- 对格式错误的输入"成功"的验证函数

**示例：**
```python
# 静默绕过
def verify_signature(sig, data, key):
    if not key:
        return True  # 没有密钥 = 跳过验证？！

# 返回值被忽略
signature.verify(data, sig)  # 失败时抛出异常
crypto.verify(data, sig)     # 失败时返回 False
# 开发者忘记检查返回值
```

### 6. 字符串类型的安全

安全关键值作为纯字符串会导致注入和混淆。

**检测模式：**
- 通过字符串拼接构建的 SQL/命令
- 以逗号分隔字符串表示的权限
- 以任意字符串（而非枚举）表示的角色/作用域
- 通过拼接字符串构造的 URL

**权限累积脚枪：**
```python
permissions = "read,write"
permissions += ",admin"  # 提权太容易了

# vs. 类型安全
permissions = {Permission.READ, Permission.WRITE}
permissions.add(Permission.ADMIN)  # 至少是显式的
```

## 分析工作流程

### 阶段 1：表面识别

1. **映射安全相关 API**：认证、授权、加密、会话管理、输入验证
2. **识别开发者选择点**：开发者在哪里可以选择算法、配置超时、选择模式？
3. **查找配置模式**：环境变量、配置文件、构造函数参数

### 阶段 2：边界探测

对每个选择点提问：
- **零/空/null**：`0`、`""`、`null`、`[]` 会怎样？
- **负值**：`-1` 意味着什么？无限？错误？
- **类型混淆**：不同的安全概念能否被交换？
- **默认值**：默认值安全吗？有文档说明吗？
- **错误路径**：输入无效时会怎样？静默接受？

### 阶段 3：威胁建模

考虑三种对手：

1. **恶意者**：主动恶意的开发者或攻击者控制配置
   - 能否通过配置禁用安全？
   - 能否降级算法？
   - 能否注入恶意值？

2. **懒惰开发者**：复制粘贴示例，跳过文档
   - 找到的第一个示例是否安全？
   - 最省力的路径是否安全？
   - 错误信息是否引导安全用法？

3. **困惑开发者**：误解 API
   - 能否在没有类型错误的情况下交换参数？
   - 能否意外使用错误的密钥/算法/模式？
   - 失败模式是明显的还是静默的？

### 阶段 4：验证发现

对每个识别的锐边：

1. **复现误用**：编写最小代码演示脚枪
2. **验证可利用性**：误用是否造成真实漏洞？
3. **检查文档**：危险是否有文档记录？（文档不能为糟糕的设计开脱，但会影响严重程度）
4. **测试缓解措施**：API 能否以合理的代价安全使用？

如果某个发现存疑，返回阶段 2 探测更多边界情况。

## 严重程度分类

| 严重程度 | 标准 | 示例 |
|---------|------|------|
| 严重 | 默认或显而易见的用法不安全 | `verify: false` 默认值；允许空密码 |
| 高 | 容易的误配置破坏安全 | 算法参数接受 "none" |
| 中 | 不常见但可能的误配置 | 负超时有意外语义 |
| 低 | 需要故意误用 | 晦涩的参数组合 |

## 参考资料

**按分类：**

- **加密 API**：见 references/crypto-apis.md
- **配置模式**：见 references/config-patterns.md
- **认证/会话**：见 references/auth-patterns.md
- **真实案例研究**：见 references/case-studies.md（OpenSSL、GMP 等）

**按语言**（通用脚枪，非加密专用）：

| 语言 | 指南 |
|------|------|
| C/C++ | references/lang-c.md |
| Go | references/lang-go.md |
| Rust | references/lang-rust.md |
| Swift | references/lang-swift.md |
| Java | references/lang-java.md |
| Kotlin | references/lang-kotlin.md |
| C# | references/lang-csharp.md |
| PHP | references/lang-php.md |
| JavaScript/TypeScript | references/lang-javascript.md |
| Python | references/lang-python.md |
| Ruby | references/lang-ruby.md |

另见 references/language-specific.md 获取综合快速参考。

## 质量检查清单

完成分析前：

- [ ] 探测了所有零/空/null 边界情况
- [ ] 验证了默认值是安全的
- [ ] 检查了算法/模式选择脚枪
- [ ] 测试了安全概念间的类型混淆
- [ ] 考虑了所有三种对手类型
- [ ] 验证了错误路径不会绕过安全
- [ ] 检查了配置验证
- [ ] 验证了构造函数参数（不仅是默认值） - 见 config-patterns.md

## 局限性
- 仅在任务明确匹配上述范围时使用本技能。
- 不可将输出内容替代针对特定环境的验证、测试或专家评审。
- 当所需输入、权限、安全边界或成功标准缺失时，请停下来请求澄清。
