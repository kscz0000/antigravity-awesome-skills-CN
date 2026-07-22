---
# agentskills.io compliant frontmatter
name: clarity-gate
risk: unknown
source: community
version: 2.1.3
description: >
  RAG 系统的认知质量预检验证。
  确保文档在进入知识库前经过适当认证。
  生成 CGD（Clarity-Gated Documents）并验证 SOT（Source of Truth）文件。
author: Francesco Marinoni Moretto
license: CC-BY-4.0
repository: https://github.com/frmoretto/clarity-gate
triggers:
  - clarity gate
  - check for hallucination risks
  - can an LLM read this safely
  - review for equivocation
  - verify document clarity
  - pre-ingestion check
  - cgd verify
  - sot verify
capabilities:
  - document-verification
  - epistemic-quality
  - rag-preparation
  - cgd-generation
  - sot-validation
outputs:
  - type: cgd
    extension: .cgd.md
    spec: docs/CLARITY_GATE_FORMAT_SPEC.md
spec_version: "2.1"
---

# Clarity Gate v2.1

**用途：** 预检验证系统，在文档进入 RAG 知识库前强制执行认知质量检查。生成符合 Clarity Gate Format Specification v2.1 的 Clarity-Gated Documents (CGD)。

**核心问题：** "如果另一个 LLM 阅读这份文档，它会把假设误认为事实吗？"

**核心原则：** *"检测是为了发现现状；强制执行是为了确保应然。在实践中：在缺失的不确定性标记变成自信的幻觉之前找到它们。"*

---

## v2.1 新特性

| 特性 | 描述 |
|---------|-------------|
| **Claim Completion Status** | PENDING/VERIFIED 由字段存在决定（无显式状态字段） |
| **Source Field Semantics** | 可执行的源 (PENDING) vs. 已发现的源 (VERIFIED) |
| **Claim ID Format Guidance** | 推荐使用基于哈希的 ID，并对规模进行冲突分析 |
| **Body Structure Requirements** | 存在 claims 时，必须包含 HITL Verification Record 部分 |
| **New Validation Codes** | E-ST10, W-ST11, W-HC01, W-HC02, E-SC06 (FORMAT_SPEC); E-TB01-07 (SOT validation) |
| **Bundled Scripts** | 用于确定性计算的 `claim_id.py` 和 `document_hash.py` |

---

## 规范

本技能实现并引用以下规范：

| 规范 | 版本 | 位置 |
|---------------|---------|----------|
| Clarity Gate Format (Unified) | v2.1 | docs/CLARITY_GATE_FORMAT_SPEC.md |

**注意：** v2.0 将 CGD 和 SOT 统一为单一的 `.cgd.md` 格式。SOT 现在是带有可选 `tier:` 块的 CGD。

---

## 验证代码

Clarity Gate 定义了基于 FORMAT_SPEC v2.1 的结构和语义检查代码：

### HITL Claim Validation (§1.3.2-1.3.3)
| 代码 | 检查项 | 严重程度 |
|------|-------|----------|
| **W-HC01** | 部分包含 `confirmed-by`/`confirmed-date` 字段 | WARNING |
| **W-HC02** | 模糊的来源（例如 "industry reports", "TBD"） | WARNING |
| **E-SC06** | `hitl-claims` 结构中的 Schema 错误 | ERROR |

### Body Structure (§1.2.1)
| 代码 | 检查项 | 严重程度 |
|------|-------|----------|
| **E-ST10** | 存在 claims 时缺少 `## HITL Verification Record` | ERROR |
| **W-ST11** | 表格行数与 `hitl-claims` 数量不匹配 | WARNING |

### SOT Table Validation (§3.1)
| 代码 | 检查项 | 严重程度 |
|------|-------|----------|
| **E-TB01** | 缺少 `## Verified Claims` 部分 | ERROR |
| **E-TB02** | 表格无数据行 | ERROR |
| **E-TB03** | 缺少必需的列 | ERROR |
| **E-TB04** | 列顺序错误 | ERROR |
| **E-TB05** | 必需列中存在空单元格 | ERROR |
| **E-TB06** | Verified 列中的日期格式无效 | ERROR |
| **E-TB07** | Verified 日期在未来（超过 24 小时宽限期） | ERROR |

**注意：** RFC-001（澄清文档）中可能定义了其他验证代码，但它们不属于规范性的 FORMAT_SPEC。

---

## 内置脚本

本技能包含用于 FORMAT_SPEC 确定性计算的 Python 脚本。

### scripts/claim_id.py

计算用于 HITL 跟踪的稳定、基于哈希的 claim ID（依据 §1.3.4）。

```bash
# Generate claim ID
python scripts/claim_id.py "Base price is $99/mo" "api-pricing/1"
# Output: claim-75fb137a

# Run test vectors
python scripts/claim_id.py --test
```

**算法：**
1. 文本规范化（去除首尾空白并合并连续空白）
2. 使用管道分隔符与位置连接
3. SHA-256 哈希，取前 8 个十六进制字符
4. 前缀为 "claim-"

**测试向量：**
- `claim_id("Base price is $99/mo", "api-pricing/1")` → `claim-75fb137a`
- `claim_id("The API supports GraphQL", "features/1")` → `claim-eb357742`

### scripts/document_hash.py

根据 FORMAT_SPEC §2.2-2.4 计算文档 SHA-256 哈希，支持完整规范化。

```bash
# Compute hash
python scripts/document_hash.py my-doc.cgd.md
# Output: 7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730

# Verify existing hash
python scripts/document_hash.py --verify my-doc.cgd.md
# Output: PASS: Hash verified: 7d865e...

# Run normalization tests
python scripts/document_hash.py --test
```

**算法（依据 §2.2-2.4）：**
1. 提取开头的 `---\n` 和 `<!-- CLARITY_GATE_END -->` 之间的内容
2. 仅从 YAML frontmatter 中移除 `document-sha256` 行（支持多行延续）
3. 规范化：
   - 去除每行尾部空白
   - 将 3 个以上连续换行符合并为 2 个
   - 规范化末尾换行符（恰好 1 个 LF）
   - UTF-8 NFC 规范化
4. 计算 SHA-256

**跨平台规范化：**
- 如存在 BOM 则移除
- CRLF 转 LF (Windows)
- CR 转 LF (旧版 Mac)
- 边界检测（防止在 CGD 结构外部计算哈希）
- 空白差异产生相同的哈希值（跨平台确定性）

---

## 核心区别

现有的 UnScientify 和 HedgeHunter (CoNLL-2010) 等工具**检测**文本中已存在的不确定性标记（"是否表达了不确定性？"）。

Clarity Gate **强制**在认知上要求的地方必须存在这些标记（"是否应该表达不确定性但没有？"）。

| 工具类型 | 问题 | 示例 |
|-----------|----------|---------|
| **检测** | "这段文本包含模糊限制语吗？" | UnScientify/HedgeHunter 发现 "may", "possibly" |
| **强制** | "这个声明应该被模糊限制但没有吗？" | Clarity Gate 标记 "Revenue will be $50M" |

---

## 关键局限性

> **Clarity Gate 验证的是形式，而非事实。**
>
> 本技能检查声明是否被正确标记为不确定——它无法验证声明是否真实。
>
> **风险：** LLM 可能将事实**幻觉**进文档，然后通过为虚假声明添加来源标记来“通过” Clarity Gate。
>
> **解决方案：** 在宣布 PASS 之前，HITL (Human-In-The-Loop) 验证是**强制性**的。

---

## 使用场景
- 将文档摄入 RAG 系统前
- 与其他 AI 系统共享文档前
- 编写规范、状态文档或方法论描述后
- 当文档包含预测、估计或假设时
- 发布未验证的声明前
- 在 LLM 会话之间交接文档时

---

## 9 个验证点

### 与规范套件的关系

9 个验证点指导**语义审查**——需要判断力（人工或 AI）的内容质量检查。它们回答诸如“这个声明应该被模糊限制吗？”和“这些数字一致吗？”等问题。

审查完成后，输出符合 CLARITY_GATE_FORMAT_SPEC.md 的 CGD 文件。CLARITY_GATE_FORMAT_SPEC.md 中的 C/S 规则验证**文件结构**，而非语义内容。

**联系：**
1. 语义发现（9 个点）确定存在哪些问题
2. 问题记录在 CGD 状态字段中（`clarity-status`, `hitl-status`, `hitl-pending-count`）
3. 状态一致性由结构规则 (C7-C10) 强制执行

*示例：如果点 5（数据一致性）发现数字冲突，您需要将 `clarity-status` 标记为 `UNCLEAR` 直到解决。然后规则 C7 确保您不能在仍为 `UNCLEAR` 时声称 `REVIEWED`。*

---

### 认知检查（核心重点：点 1-4）

**1. 假设 vs 事实标记**
每个声明都必须清楚地标记为已验证或假设性的。

| 失败 | 通过 |
|-------|--------|
| "我们的架构优于竞争对手" | "我们的架构优于竞争对手 [基准数据见表 3]" |
| "模型实现了 40% 的提升" | "模型实现了 40% 的提升 [在数据集 X 上测量]" |

**修复：** 添加标记："PROJECTED:", "HYPOTHESIS:", "UNTESTED:", "(estimated)", "~", "?"

---

**2. 不确定性标记强制执行**
前瞻性陈述需要限定词。

| 失败 | 通过 |
|-------|--------|
| "收入将在 Q4 达到 5000 万美元" | "收入**预计**在 Q4 达到 5000 万美元" |
| "该功能将减少流失" | "该功能**预计**将减少流失" |

**修复：** 添加 "projected", "estimated", "expected", "designed to", "intended to"

---

**3. 假设可见性**
影响解释的隐含假设必须显式化。

| 失败 | 通过 |
|-------|--------|
| "系统线性扩展" | "系统线性扩展 [假设 <1000 并发用户]" |
| "响应时间为 50ms" | "响应时间为 50ms [在标准负载条件下]" |

**修复：** 添加括号内的条件："[assuming X]", "[under conditions Y]", "[when Z]"

---

**4. 看似权威的未验证数据**
带有具体百分比和复选框的表格看起来像测量数据。

**危险信号：** 带有具体数字（89%, 95%, 100%）但无来源的表格

**修复：** 为数字添加 "(guess)", "(est.)", "?"。添加显式警告："PROJECTED VALUES - NOT MEASURED"

---

### 数据质量检查（补充重点：点 5-7）

**5. 数据一致性**
扫描文档中冲突的数字、日期或事实。

**危险信号：** 一部分说 "500 users"，另一部分说 "750 users"

**修复：** 调和冲突或显式注明差异并解释原因。

---

**6. 隐含因果关系**
暗示因果关系但缺乏证据的声明。

**危险信号：** "更短的提示词能提高响应质量"（看似合理但未证实）

**修复：** 重构为假设："更短的提示词**可能**提高响应质量（假设，未验证）"

---

**7. 将未来状态作为现在时**
将计划中/希望的结果描述为已经实现。

**危险信号：** "系统每秒处理 10,000 个请求"（当它还没构建时）

**修复：** 使用将来时或条件句："系统**设计用于**处理..." 或 "TARGET: 10,000 rps"

---

### 验证路由（点 8-9）

**8. 时间连贯性**
文档日期和时间戳必须内部一致且合理。

| 失败 | 通过 |
|-------|--------|
| "最后更新：2024年12月"（当前为 2026 年） | "最后更新：2026年1月" |
| v1.0.0 日期 2024-12-23, v1.1.0 日期 2024-12-20 | 版本按时间顺序排列 |

**子检查：**
1. 文档日期 vs 当前日期
2. 内部时间顺序（版本、事件顺序）
3. 引用新鲜度（"current", "now", "today" 声明）

**修复：** 更新日期，添加 "as of [date]" 限定词，标记过时声明

---

**9. 可外部验证的声明**
可以进行事实核查的具体数字应标记为需要验证。

| 类型 | 示例 | 风险 |
|------|---------|------|
| 定价 | "每次调用约 $0.005" | API 定价变更 |
| 统计 | "论文平均包含 15-30 个方程" | 可能偏差很大 |
| 比率 | "40% 的研究人员使用 X" | 需要引用 |
| 竞争对手声明 | "没有竞争对手提供 Y" | 可能已过时 |

**修复选项：**
1. 添加带日期的来源
2. 添加不确定性标记
3. 路由至 HITL 或外部搜索
4. 泛化（"低成本" 而非 "$0.005"）

---

## 验证层级

```
Claim Extracted --> Does Source of Truth Exist?
                           |
           +---------------+---------------+
           YES                             NO
           |                               |
   Tier 1: Automated              Tier 2: HITL
   Consistency & Verification     Two-Round Verification
           |                               |
   PASS / BLOCK                   Round A → Round B → APPROVE / REJECT
```

### Tier 1: 自动化验证

**A. 内部一致性**
- 图表 vs 文本 矛盾
- 摘要 vs 正文 不匹配
- 表格 vs 散文 冲突
- 数值一致性

**B. 外部验证（扩展接口）**
- 用户提供的连接到结构化源的连接器
- 财务系统、Git 提交、CRM 等

### Tier 2: 两轮 HITL 验证 — 强制性

**Round A: 衍生数据确认**
- 来自会话中发现的来源的声明
- 人工确认解释，而非真相

**Round B: 真正的 HITL 验证**
- 需要实际验证的声明
- 未找到来源、人工自己的数据、外推数据

---

## CGD 输出格式

生成 Clarity-Gated Document 时，请按照 CLARITY_GATE_FORMAT_SPEC.md v2.1 使用此格式：

```yaml
---
clarity-gate-version: 2.1
processed-date: 2026-01-12
processed-by: Claude + Human Review
clarity-status: CLEAR
hitl-status: REVIEWED
hitl-pending-count: 0
points-passed: 1-9
rag-ingestable: true          # computed by validator - do not set manually
document-sha256: 7d865e959b2466918c9863afca942d0fb89d7c9ac0c99bafc3749504ded97730
hitl-claims:
  - id: claim-75fb137a
    text: "Revenue projection is $50M"
    value: "$50M"
    source: "Q3 planning doc"
    location: "revenue-projections/1"
    round: B
    confirmed-by: Francesco
    confirmed-date: 2026-01-12
---

# Document Title

[Document body with epistemic markers applied]

Claims like "Revenue will be $50M" become "Revenue is **projected** to be $50M *(unverified projection)*"

---

## HITL Verification Record

### Round A: Derived Data Confirmation
- Claim 1 (source) ✓
- Claim 2 (source) ✓

### Round B: True HITL Verification
| # | Claim | Status | Verified By | Date |
|---|-------|--------|-------------|------|
| 1 | [claim] | ✓ Confirmed | [name] | [date] |

<!-- CLARITY_GATE_END -->
Clarity Gate: CLEAR | REVIEWED
```

**必需的 CGD 元素（依据规范）：**
- 包含所有必需字段的 YAML frontmatter：
  - `clarity-gate-version` — 工具版本（无 "v" 前缀）
  - `processed-date` — YYYY-MM-DD 格式
  - `processed-by` — 处理者名称
  - `clarity-status` — CLEAR 或 UNCLEAR
  - `hitl-status` — PENDING, REVIEWED, 或 REVIEWED_WITH_EXCEPTIONS
  - `hitl-pending-count` — 整数 ≥ 0
  - `points-passed` — 例如 `1-9` 或 `1-4,7,9`
  - `hitl-claims` — 已验证声明列表（可为空 `[]`）
- 结束标记（HTML 注释 + 状态行）：
  ```
  <!-- CLARITY_GATE_END -->
  Clarity Gate: <clarity-status> | <hitl-status>
  ```
- HITL 验证记录（如果状态为 REVIEWED）

**可选/计算字段：**
- `rag-ingestable` — **由验证器计算**，不要手动设置。仅当为 `CLEAR | REVIEWED` 且无排除块时显示 `true`。
- `document-sha256` — 必需。64 字符小写十六进制哈希，用于完整性验证。计算规则见规范 §2。
- `exclusions-coverage` — 可选。正文在排除块内的比例 (0.0–1.0)。

**转义机制：** 要编写像 `*(estimated)*` 这样的标记而不触发解析，请用反引号包裹：`` `*(estimated)*` ``

### Claim Completion Status (v2.1)

Claim 验证状态由字段**存在**决定，而非显式状态字段：

| 状态 | `confirmed-by` | `confirmed-date` | 含义 |
|-------|----------------|------------------|----------|
| **PENDING** | 缺失 | 缺失 | 等待人工验证 |
| **VERIFIED** | 存在 | 存在 | 人工已确认 |
| *(无效)* | 存在 | 缺失 | W-HC01: 字段不完整 |
| *(无效)* | 缺失 | 存在 | W-HC01: 字段不完整 |

**为什么没有显式状态字段？** 字段存在是自我强制的——您无法在不提供谁/何时的情况下意外设置状态。

### Source Field Semantics (v2.1)

`source` 字段的含义根据 claim 状态而变化：

| 状态 | `source` 包含 | 示例 |
|-------|-------------------|----------|
| **PENDING** | 验证地点（可执行） | `"Check Q3 planning doc"` |
| **VERIFIED** | 发现内容（证据） | `"Q3 planning doc, page 12"` |

**模糊来源检测 (W-HC02):** 像 `"industry reports"`, `"research"`, `"TBD"` 这样的来源会触发警告。

### Claim ID Format (v2.1)

**通用模式：** `claim-[a-z0-9._-]{1,64}`（字母数字、点、下划线、连字符）

| 方法 | 模式 | 示例 | 使用场景 |
|----------|---------|---------|----------|
| **Hash-based** (首选) | `claim-[a-f0-9]{8,}` | `claim-75fb137a` | 确定性、抗冲突 |
| **Sequential** | `claim-[0-9]+` | `claim-1`, `claim-2` | 简单文档 |
| **Semantic** | `claim-[a-z0-9-]+` | `claim-revenue-q3` | 人工友好 |

**冲突概率：** 在 1,000 个 claims 使用 8 字符十六进制 ID 时：约 0.012%。对于 >1,000 个 claims，使用 12 个以上十六进制字符。

**建议：** 使用 `scripts/claim_id.py` 生成基于哈希的 ID 以保持一致性和抗冲突性。

---

## 排除块

当内容无法解决时（无 SME 可用、遗留散文等），将其标记为排除而不是留下歧义：

```markdown
<!-- CG-EXCLUSION:BEGIN id=auth-legacy-1 -->
Legacy authentication details that require SME review...
<!-- CG-EXCLUSION:END id=auth-legacy-1 -->
```

**规则：**
- ID 必须匹配：`[A-Za-z0-9][A-Za-z0-9._-]{0,63}`
- 不得嵌套或重叠块
- 每个 ID 仅使用一次
- 需要 `hitl-status: REVIEWED_WITH_EXCEPTIONS`
- 必须在 frontmatter 中记录 `exceptions-reason` 和 `exceptions-ids`

**重要：** 带有排除块的文档**不可摄入 RAG**。它们会被完全拒绝（无部分摄入）。

完整规则见 CLARITY_GATE_FORMAT_SPEC.md §4。

---

## SOT 验证

验证 Source of Truth 文件时，技能会检查**格式合规性**（依据 CLARITY_GATE_FORMAT_SPEC.md）和**内容质量**（9 个点）。

### 格式合规性（结构规则）

SOT 文档是带有 `tier:` 块的 CGD。它们需要包含一个有效表格的 `## Verified Claims` 部分。

| 代码 | 检查项 | 严重程度 |
|------|-------|----------|
| E-TB01 | 缺少 `## Verified Claims` 部分 | ERROR |
| E-TB02 | 表格无数据行 | ERROR |
| E-TB03 | 缺少必需列 (Claim, Value, Source, Verified) | ERROR |
| E-TB04 | 列顺序错误 (Claim 非首列或 Verified 非末列) | ERROR |
| E-TB05 | 必需列中存在空单元格 | ERROR |
| E-TB06 | Verified 列中的日期格式无效 | ERROR |
| E-TB07 | Verified 日期在未来（超过 24 小时宽限期） | ERROR |

### 内容质量（9 个点）

9 个验证点适用于 SOT 内容：

| 点 | SOT 应用 |
|-------|-----------------|
| 1-4 | 检查 `## Verified Claims` 中的声明是否实际已验证 |
| 5 | 检查表格中数值是否冲突 |
| 6 | 检查声明是否暗示了未支持的因果关系 |
| 7 | 检查表格是否将未来时态表述为现在时 |
| 8 | 检查日期是否按时间顺序一致 |
| 9 | 标记具体数字以供外部检查 |

### SOT 特定要求

- **需要 Tier 块：** SOT 是带有 `tier:` 块的 CGD，包含 `level`, `owner`, `version`, `promoted-date`, `promoted-by`
- **结构化 claims 表格：** `## Verified Claims` 部分包含列：Claim, Value, Source, Verified
- **表格在排除块之外：** 已验证声明表格不得位于排除块内
- **陈旧性标记：** 在内容中使用 `[STABLE]`, `[CHECK]`, `[VOLATILE]`, `[SNAPSHOT]`
  - `[STABLE]` — 无需重新检查即可安全引用
  - `[CHECK]` — 引用前需验证
  - `[VOLATILE]` — 频繁变更；始终验证
  - `[SNAPSHOT]` — 时间点数据；引用时包含日期

---

## 输出格式

运行 Clarity Gate 后，报告如下：

```
## Clarity Gate Results

**Document:** [filename]
**Issues Found:** [number]

### Critical (will cause hallucination)
- [issue + location + fix]

### Warning (could cause equivocation)  
- [issue + location + fix]

### Temporal (date/time issues)
- [issue + location + fix]

### Externally Verifiable Claims
| # | Claim | Type | Suggested Verification |
|---|-------|------|------------------------|
| 1 | [claim] | Pricing | [where to verify] |

---

## Round A: Derived Data Confirmation

- [claim] ([source])

Reply "confirmed" or flag any I misread.

---

## Round B: HITL Verification Required

| # | Claim | Why HITL Needed | Human Confirms |
|---|-------|-----------------|----------------|
| 1 | [claim] | [reason] | [ ] True / [ ] False |

---

**Would you like me to produce an annotated CGD version?**

---

**Verdict:** PENDING CONFIRMATION
```

---

## 严重程度等级

| 等级 | 定义 | 措施 |
|-------|------------|--------|
| **CRITICAL** | LLM 可能将假设视为事实 | 使用前必须修复 |
| **WARNING** | LLM 可能误解 | 应当修复 |
| **TEMPORAL** | 检测到日期/时间不一致 | 验证并更新 |
| **VERIFIABLE** | 可进行事实核查的具体声明 | 路由至 HITL 或外部搜索 |
| **ROUND A** | 源自有证可查的来源 | 快速确认 |
| **ROUND B** | 需要真正的验证 | 未确认不得通过 |
| **PASS** | 标记清晰、无歧义、已验证 | 无需操作 |

---

## 快速扫描清单

| 模式 | 措施 |
|---------|--------|
| 具体百分比 (89%, 73%) | 添加来源或标记为估计 |
| 比较表格 | 添加 "PROJECTED" 标题 |
| "Achieves", "delivers", "provides" | 如未验证，使用 "designed to", "intended to" |
| 复选框 | 验证是否已确认 |
| "100%" 任何内容 | 几乎总是需要限定 |
| "Last Updated: [date]" | 对照当前日期检查 |
| 带日期的版本号 | 验证时间顺序 |
| "$X.XX" 或 "~$X" (定价) | 标记以供外部验证 |
| "averages", "typically" | 标记以供来源/引用验证 |
| 竞争对手能力声明 | 标记以供外部验证 |

---

## 本技能不做什么

- 不对文档类型进行分类（使用 Stream Coding 代替）
- 不重组文档
- 不添加深度链接或引用
- 不评估写作质量
- **不自主检查事实准确性**（需要 HITL）

---

## 相关项目

| 项目 | 用途 | URL |
|---------|---------|-----|
| Source of Truth Creator | 创建认知校准的文档 | github.com/frmoretto/source-of-truth-creator |
| Stream Coding | 文档优先的方法论 | github.com/frmoretto/stream-coding |
| ArXiParse | 科学论文验证 | arxiparse.org |

---

## 更新日志

### v2.1.3 (2026-03-02)
- **FIXED:** `document_hash.py` 现已完全符合 FORMAT_SPEC §2.1-2.4
- **FIXED:** 围栏感知的结束标记检测（依据 §2.3/§8.5 的 Quine Protection）
- **FIXED:** 所有 4 个部署副本收敛为单一规范实现
- **ADDED:** `canonicalize()` 函数：尾部空白去除、换行符合并、NFC 规范化
- **ADDED:** YAML 感知的 `document-sha256` 移除，支持多行延续 (§2.2)
- **ADDED:** 围栏跟踪测试向量（7 个新测试，共 15 个）

### v2.1.0 (2026-01-27)
- **ADDED:** Claim Completion Status 语义（PENDING/VERIFIED 由字段存在决定）
- **ADDED:** Source Field Semantics（可执行的 vs. 已发现的）
- **ADDED:** Claim ID Format 指导及冲突分析
- **ADDED:** Body Structure Requirements（存在 claims 时必须包含 HITL Verification Record）
- **ADDED:** 新验证代码：E-ST10, W-ST11, W-HC01, W-HC02, E-SC06 (FORMAT_SPEC §1.2-1.3)
- **ADDED:** 内置脚本：`claim_id.py`, `document_hash.py`
- **UPDATED:** 引用至 FORMAT_SPEC v2.1
- **UPDATED:** CGD 输出示例至版本 2.1

### v2.0.0 (2026-01-13)
- **ADDED:** agentskills.io 合规的 YAML frontmatter
- **ADDED:** Clarity Gate Format Specification v2.0 合规性（统一 CGD/SOT）
- **ADDED:** 带有 E-TB* 错误代码的 SOT 验证支持
- **ADDED:** 验证规则映射（9 个点 → 规则代码）
- **ADDED:** 带有 `<!-- CLARITY_GATE_END -->` 标记的 CGD 输出格式模板
- **ADDED:** Quine Protection 说明 (§2.3 围栏感知标记检测)
- **ADDED:** Redacted Export 功能 (§8.11)
- **UPDATED:** `hitl-claims` 格式至 v2.0 schema (id, text, value, source, location, round)
- **UPDATED:** 结束标记格式至 HTML 注释样式
- **UPDATED:** 统一格式规范 v2.0 (单一 `.cgd.md` 扩展名)
- **RESTRUCTURED:** 适应多平台技能发现

### v1.6 (2025-12-31)
- 添加两轮 HITL 验证系统
- Round A: 衍生数据确认
- Round B: 真正的 HITL 验证

### v1.5 (2025-12-28)
- 添加点 8: 时间连贯性
- 添加点 9: 可外部验证的声明

### v1.4 (2025-12-23)
- 添加 CGD 标注输出模式

### v1.3 (2025-12-21)
- 重构点为认知 (1-4) 和数据质量 (5-7)

### v1.2 (2025-12-21)
- 添加 Source of Truth 请求步骤

### v1.1 (2025-12-21)
- 添加 HITL Fact Verification（强制性）

### v1.0 (2025-11)
- 初始发布，包含 6 点验证

---

**Version:** 2.1.3
**Spec Version:** 2.1
**Author:** Francesco Marinoni Moretto
**License:** CC-BY-4.0
