---
name: wjttc-builder
description: 为任意项目规划（PLAN）并生成（GENERATE）WJTTC（锦标赛级别）测试套件。分析代码库、按 WJTTC 五大层级（Brake · Engine · Aero · Tyre · Pit）归类组件，编写分层测试计划，并生成可执行测试文件脚手架。此为构建器（BUILDER）—— 负责规划与...
risk: unknown
source: https://github.com/Wolfe-Jam/faf-skills/tree/main/skills/wjttc-builder
source_repo: Wolfe-Jam/faf-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/Wolfe-Jam/faf-skills/blob/main/LICENSE
---

# WJTTC 构建器 — 锦标赛级测试套件生成器

**理念：** "我们把东西搞坏，这样别人就永远不必知道它们曾经坏过。"

本技能遵循 WJTTC（Wolfe James Tests The Code，Wolfe James 测代码）方法论，生成 F1 灵感的测试套件。

## 目标

| 目标 | 方式 |
|------|------|
| **预先定义** | 编码前先有测试计划 → 提升代码质量 |
| **内联测试** | 边写边测 / 边写边批准 → 在萌芽阶段捕获缺陷 |
| **第一层 → 第二层** | 行业标准 + 专家级 = 金标代码 |
| **AI 优化** | 与 project.faf 100% 双向同步 |
| **写出最好的代码** | ✪ 锦标赛标准 |

## 金标代码 ✨

**代码获得金标状态的条件：**

```
┌────────────────────────────────────────┐
│         ✪ GOLD CODE ✨                │
│  ════════════════════════════════════  │
│  ✓ Pre-test plan defined               │
│  ✓ Inline testing at write time        │
│  ✓ Layer 1: 100% industry coverage     │
│  ✓ Layer 2: WJTTC expert edge cases    │
│  ✓ Bi-sync with project.faf            │
│  ✓ All tests passing                   │
│  ════════════════════════════════════  │
│  This code has earned its name.        │
└────────────────────────────────────────┘
```

## 在开发流程中的位置

**WJTTC 位于 project.faf 之后、编码之前：**

```
1. project.faf      → Define WHAT we're building (context)
2. WJTTC-TESTS.md   → Define SUCCESS CRITERIA (tests first)
3. Code             → Build to pass the tests
4. Test             → Pass/Fail
5. Repeat           → Until Championship grade
```

## 测试驱动编码（TDC）

**WJTTC 循环：**

```
Think → Cross-check → Confirm → Code → Test → [Repeat]
  │         │           │        │       │
  │         │           │        │       └── Pass/Fail verdict
  │         │           │        └── Write implementation
  │         │           └── Green light to proceed
  │         └── STOP if missing info - get it first
  └── Understand what we're building
```

**交叉验证关卡：** 如有信息缺失，先停下补齐，再继续。
- 需求不明确？提问。
- 验收标准含糊？澄清。
- 边界条件未知？先定义。

**红 → 绿 → 重构：**
1. 写一个必失败的测试（红）
2. 写代码让它通过（绿）
3. 清理代码（重构）

**绝不在没有"完成"定义的情况下动手写代码。**

## 双层测试架构

### 第一层：行业标准（100% 覆盖率）
使用框架自带的测试能力 —— Jest、pytest、Vitest 等。
- 单元测试
- 集成测试
- 标准断言
- 覆盖率要求

**这是基线，不可妥协。**

### 第二层：WJTTC 专家级（压力 + 边界用例）
捕获行业级测试漏掉的锦标赛级场景：

| 类别 | 测试内容 |
|----------|--------------|
| **语法** | 特殊字符、转义、引号、括号 |
| **Emoji** | 字符串、文件名、变量中的 🏎️ |
| **命名风格** | camelCase、snake_case、SCREAMING_CASE、混用 |
| **变量取值** | 空、null、undefined、MAX_INT、负数 |
| **Unicode** | RTL 文本、组合字符、零宽字符 |
| **注入** | SQL、XSS、命令注入尝试 |
| **边界** | 0、1、-1、MAX、MAX+1、空数组 |

**测试目标：**
- MCP 服务器与工具
- CLI 命令与标志
- API 端点与负载
- 引擎内部
- 基础设施配置

## 我们也测试测试本身

**元测试清单：**
- [ ] 这些测试真的能跑起来吗？
- [ ] 代码坏了，它们会失败吗？
- [ ] 代码正确时，它们会通过吗？
- [ ] 边界用例是否覆盖？
- [ ] 测试能否独立运行？
- [ ] 测试是否会自我清理？

## 信号完整性审计（"红即真实"信条）

**在衡量覆盖率之前，先衡量信号的可信度。**

红色 CI 是一份契约：停下、查看、修复。如果红色意味着 *"耸肩，跑机器邻居吵闹，再跑一次就行"*，那么信号已经死了 —— 而死信号比没有信号更糟。一个 100% 覆盖率但红灯飘飘的测试套件，比一个 80% 覆盖率且零误报的套件更不可信，因为团队已经不再认真读红。

**这是母信条，所有其他测试原则都为它服务。**

### 审计方法

对任何待评估的测试套件，将最近 30 天的 CI 失败归入三个桶：

| 桶 | 含义 | 处置 |
|--------|---------|--------|
| **真实缺陷** | 红色对应了实际代码缺陷，最终由代码变更修复 | ✓ 信号有效 |
| **抖动** | 红色源于计时/网络/并发噪声；未改代码重跑即通过 | ✗ 测试设计缺陷 |
| **基础设施** | 红色源于缺失密钥、runner 镜像变更、上游依赖 —— 与被测代码无关 | ✗ 工作流设计缺陷 |

### 信号完整性得分

```
SI = (Real bugs) / (Real bugs + Flakes + Infra) × 100
```

| SI % | 评级 | 必做动作 |
|------|---------|-----------------|
| 100% | TROPHY ✪ | 保持 —— 信号典范 |
| 95-99% | Championship | 任何抖动立即标注 |
| 85-94% | Acceptable | 本迭代排期修复抖动类问题 |
| 70-84% | Eroding | 暂停添加新测试，优先修复抖动 |
| <70% | DEAD SIGNAL | 阻断所有合并，直至信号恢复 |

**可信度问题先于覆盖率问题。** 一个 60% 覆盖率、信号完整性 100% 的套件，比 95% 覆盖率、信号完整性 70% 的套件更健康。

### 见到就消灭的常见抖动来源

- **共享 CI runner 上硬性绝对时间性能断言** —— `expect(time).toBeLessThan(30)`。改为非阻塞工作流，使用 `continue-on-error: true`。
- **主套件中依赖网络的测试** —— 在边界处 mock，或归入集成层。
- **无显式顺序的并发测试** —— 使用确定性调度器。
- **依赖操作系统调度器的计时** —— 替换为统计方法（P95 over N）或相对方法（与同次运行的基线对比）。
- **因密钥缺失而失败的步骤** —— 灰色跳过，不要判失败。

### 反向规则

**本该变红却绿灯通过的 CI，同样是契约违反。** 若真实缺陷在绿灯 CI 下溜出去，那就是覆盖缺口，必须在修复落地之前补一条回归测试。假阴性与假阳性同等紧迫。

### 当对话才是真正的关卡

自动化 CI 只是支撑设施。**人类 + AI 的对话式审计 —— 发现模式、追根溯源、修复系统 —— 才是真正的质量关卡。** 抖动的 CI 浪费对话的带宽。信号完整性存在的意义，就是让 CI 配得上它所服务的对话。

## 适用场景

- 已定义 project.faf 上下文之后
- 编写任何实现代码之前
- 启动新功能时（先定义测试）
- 修复缺陷时（先写必失败的测试）
- 构建回归测试套件

## 测试层级体系 —— WJTTC 五大层级

WJTTC 包含 **五个** 层级：**Brake · Engine · Aero · Tyre · Pit**。构建器把每个组件归入其中之一。（`faf wjttc` 同样按这五个层级审计套件，并标记未分层的测试 —— 给你的测试命名时带上层级词，便于审计归类。）

### 第一层：BRAKE（安全 —— 关键级）
**当失败 = 灾难性后果**

识别并测试：
- 安全漏洞（鉴权绕过、注入、XSS）
- 数据丢失或损坏风险
- 支付 / 金融处理
- API 密钥 / 凭据泄露
- 备份 / 恢复功能

### 第二层：ENGINE（核心功能）
**当失败 = 体验糟糕或结果错误**

识别并测试：
- 核心 API 端点
- 数据转换
- 业务逻辑准确性
- 集成点
- 性能基准

### 第三层：AERO（润色）
**当失败 = 轻微不便**

识别并测试：
- UI / UX 边界用例
- 错误消息排版
- 可选功能
- 文档准确性

### 第四层：TYRE（实战 —— 真实道路）
**橡胶与道路的接触：在真实条件下长期使用的耐久性**

识别并测试：
- 在真实表面上的边界与极端输入（真实数据形态、大负载）
- 磨损与耐久性 —— 长时间会话、重复调用、浸泡 / 负载行为
- 降级条件 —— 慢网、部分数据、限流、重试
- 持续使用下的资源泄漏（内存、文件句柄、连接）

### 第五层：PIT（运维 —— 按需启用）
**维修站：把它送上赛道，并保持可维护**

识别并测试：
- 跨组件的集成与端到端连线
- 部署 / 发布检查（构建、打包、冒烟测试、迁移）
- 运维健康 —— 启动 / 关闭、配置加载、密钥就位、可观测性
- 回滚与恢复路径

## 测试套件生成流程

### 第一步：分析项目

理解测试什么：

1. 读取关键文件（package.json、主入口、API 路由）
2. 识别项目类型（Web 应用、CLI、API、库）
3. 列出所有公共接口（API、函数、UI 交互）
4. 记录外部依赖（数据库、API、服务）

### 第二步：按层级归类

对每个识别出的组件，分配五大层级之一：

```
Tier 1 (Brake): Authentication, data writes, payments, security
Tier 2 (Engine): Core features, API responses, business logic
Tier 3 (Aero):  UI polish, optional features, error formatting
Tier 4 (Tyre):  Edge cases, durability, soak/load, degraded conditions
Tier 5 (Pit):   Integration, deploy/release checks, ops health, rollback
```

### 第三步：生成测试计划

创建一个 WJTTC-TEST-SUITE.md 文件，包含：

1. **页眉** —— 项目名、版本、日期、测试人员
2. **测试概述** —— 目标与通过率目标
3. **第一层（Brake）测试** —— 所有关键 / 安全类测试，含通过 / 失败表
4. **第二层（Engine）测试** —— 核心功能测试
5. **第三层（Aero）测试** —— 润色与排版测试
6. **第四层（Tyre）测试** —— 边界、耐久性、降级条件
7. **第五层（Pit）测试** —— 集成、部署 / 运维、回滚检查
8. **性能目标** —— 时间基准
9. **执行日志** —— 运行测试的清单
10. **锦标赛认证** —— 通过率到层级的映射

### 第四步：生成可执行测试（可选）

如有需求，生成测试文件：

- JavaScript：`tests/*.test.js`（Jest / Vitest）
- Python：`tests/test_*.py`（pytest）
- Bash：`tests/test_*.sh`（shell 脚本）

## 输出格式

### 测试套件位置
```
project/
└── tests/
    ├── WJTTC-TEST-SUITE.md     # Test plan document
    ├── test_tier1_brake.js     # Executable tests (optional)
    ├── test_tier2_engine.js
    ├── test_tier3_aero.js
    ├── test_tier4_tyre.js
    └── test_tier5_pit.js
```

### 锦标赛评分

通过率映射到 FAF 的标准层级体系（FAF 处处使用的同一套层级）：

| 分数 | 层级 | 符号 | 状态 |
|-------|------|--------|--------|
| 100% | Trophy | ✪ | 完美 —— 金标代码 |
| 99% | Gold | ★ | 出类拔萃 |
| 95% | Silver | ◆ | 顶尖 |
| 85% | Bronze | ◇ | 生产就绪 |
| 70% | Green | ● | 基础扎实 |
| 55% | Yellow | ● | 需要改进 |
| 1% | Red | ○ | 大工作量 |
| 0% | White | ♡ | 空白 |

## 一键生成命令

为当前项目生成测试套件：

1. 分析代码库结构
2. 识别所有可测组件
3. 为每个组件分配层级
4. 生成 WJTTC-TEST-SUITE.md
5. 可选生成可执行测试文件

## 测试表示例格式

```markdown
### T1.1 - [Test Name]
**Status:** ⏳ PENDING
**Priority:** CRITICAL

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| [Scenario 1] | [Expected result] | | |
| [Scenario 2] | [Expected result] | | |

**Test Command:**
\`\`\`bash
[How to run this test]
\`\`\`
```

## 集成 —— 构建器的交接点

本技能是 **构建器**：负责规划与生成。**它不会运行** 该套件。

- **执行 + 报告** → 使用 `wjttc-tester` 技能（运行测试、查找缺陷、撰写 WJTTC 报告）。
- **审计层级平衡** → `faf wjttc` 将现有套件按五大层级分类，并标记未分层测试（`--strict` 在任意未分层时返回非零退出码；`--json` 用于 CI）。为你生成的测试命名时带上层级词（brake/engine/aero/tyre/pit），便于审计归类。
- **接入 CI 凭据** → `faf taf setup` 安装 TAF 凭据打印机，使每次运行留下可验证的记录。

---

*锦标赛测试标准 🏎️*

## 使用限制

- 仅当任务明确匹配其上游来源与本地项目上下文时使用本技能。
- 在应用变更前，验证命令、生成代码、依赖、凭据与外部服务行为。
- 不要把示例当作环境特定测试、安全审查，或对破坏性 / 高成本操作的用户批准的替代品。