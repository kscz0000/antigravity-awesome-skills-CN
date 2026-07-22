---
name: skill-creator-ms
description: "为使用Azure SDK和Microsoft Foundry服务的AI编码代理创建有效技能的指南。适用于创建新技能或更新现有技能。触发词：Azure技能创建、Microsoft技能、SDK技能、Azure SDK技能、技能创建指南"
risk: unknown
source: community
date_added: "2026-02-27"
---

# 技能创建器

创建扩展AI代理能力的技能指南，重点关注Azure SDK和Microsoft Foundry。

> **必需上下文：** 创建SDK或API技能时，用户必须提供SDK包名、文档URL或仓库参考，技能才能基于此创建。

## 关于技能

技能是将通用代理转变为专业专家的模块化知识包：

1. **程序性知识** — 特定领域的多步骤工作流程
2. **SDK专业知识** — Azure服务的API模式、认证、错误处理
3. **领域上下文** — 模式、业务逻辑、公司特定模式
4. **捆绑资源** — 用于复杂任务的脚本、参考、模板

---

## 核心原则

### 1. 简洁是关键

上下文窗口是共享资源。质疑每一块内容："它值得花费这些token吗？"

**默认假设：代理已经具备能力。** 只添加它们不知道的内容。

### 2. 优先使用最新文档

**Azure SDK不断变化。** 技能应指导代理验证文档：

```markdown
## 实现前

搜索 `microsoft-docs` MCP 获取当前API模式：
- 查询: "[SDK名称] [操作] python"
- 验证: 参数与安装的SDK版本匹配
```

### 3. 自由度

根据任务脆弱性匹配特异性：

| 自由度 | 适用场景 | 示例 |
|--------|---------|------|
| **高** | 多种有效方法 | 文本指南 |
| **中** | 首选模式但有变化 | 伪代码 |
| **低** | 必须精确 | 具体脚本 |

### 4. 渐进式披露

技能分三个层级加载：

1. **元数据** (~100字) — 始终在上下文中
2. **SKILL.md正文** (<5k字) — 技能触发时
3. **参考资料** (无限制) — 按需加载

**保持SKILL.md在500行以内。** 接近此限制时拆分为参考文件。

---

## 技能结构

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML前置元数据 (name, description)
│   └── Markdown指令
└── 捆绑资源 (可选)
    ├── scripts/      — 可执行代码
    ├── references/   — 按需加载的文档
    └── assets/       — 输出资源 (模板, 图片)
```

### SKILL.md

- **前置元数据**: `name` 和 `description`。描述是触发机制。
- **正文**: 仅在触发后加载的指令。

### 捆绑资源

| 类型 | 用途 | 何时包含 |
|------|------|---------|
| `scripts/` | 确定性操作 | 重复编写相同代码 |
| `references/` | 详细模式 | API文档、模式、详细指南 |
| `assets/` | 输出资源 | 模板、图片、样板代码 |

**不要包含**: README.md、CHANGELOG.md、安装指南。

---

## 创建Azure SDK技能

为Azure SDK创建技能时，遵循以下一致模式。

### 技能章节顺序

遵循此结构（基于现有Azure SDK技能）：

1. **标题** — `# SDK名称`
2. **安装** — `pip install`, `npm install` 等
3. **环境变量** — 必需配置
4. **认证** — 始终使用 `DefaultAzureCredential`
5. **核心工作流程** — 最小可行示例
6. **功能表** — 客户端、方法、工具
7. **最佳实践** — 编号列表
8. **参考链接** — 链接到 `/references/*.md` 的表格

### 认证模式（所有语言）

始终使用 `DefaultAzureCredential`：

```python
# Python
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()
client = ServiceClient(endpoint, credential)
```

```csharp
// C#
var credential = new DefaultAzureCredential();
var client = new ServiceClient(new Uri(endpoint), credential);
```

```java
// Java
TokenCredential credential = new DefaultAzureCredentialBuilder().build();
ServiceClient client = new ServiceClientBuilder()
    .endpoint(endpoint)
    .credential(credential)
    .buildClient();
```

```typescript
// TypeScript
import { DefaultAzureCredential } from "@azure/identity";
const credential = new DefaultAzureCredential();
const client = new ServiceClient(endpoint, credential);
```

**永远不要硬编码凭据。使用环境变量。**

### 标准动词模式

Azure SDK在所有语言中使用一致的动词：

| 动词 | 行为 |
|------|------|
| `create` | 创建新资源；已存在则失败 |
| `upsert` | 创建或更新 |
| `get` | 检索；缺失则报错 |
| `list` | 返回集合 |
| `delete` | 即使缺失也成功 |
| `begin` | 启动长时间运行的操作 |

### 语言特定模式

详见 `references/azure-sdk-patterns.md`，包括：

- **Python**: `ItemPaged`, `LROPoller`, 上下文管理器, Sphinx文档字符串
- **.NET**: `Response<T>`, `Pageable<T>`, `Operation<T>`, 模拟支持
- **Java**: 构建器模式, `PagedIterable`/`PagedFlux`, Reactor类型
- **TypeScript**: `PagedAsyncIterableIterator`, `AbortSignal`, 浏览器注意事项

### 示例：Azure SDK技能结构

```markdown
---
name: skill-creator
description: |
  Azure AI示例SDK（Python）。用于[特定服务功能]。
  触发词: "示例服务", "创建示例", "列出示例".
---

# Azure AI示例SDK

## 安装

\`\`\`bash
pip install azure-ai-example
\`\`\`

## 环境变量

\`\`\`bash
AZURE_EXAMPLE_ENDPOINT=https://<resource>.example.azure.com
\`\`\`

## 认证

\`\`\`python
from azure.identity import DefaultAzureCredential
from azure.ai.example import ExampleClient

credential = DefaultAzureCredential()
client = ExampleClient(
    endpoint=os.environ["AZURE_EXAMPLE_ENDPOINT"],
    credential=credential
)
\`\`\`

## 核心工作流程

\`\`\`python
# 创建
item = client.create_item(name="example", data={...})

# 列出（自动处理分页）
for item in client.list_items():
    print(item.name)

# 长时间运行的操作
poller = client.begin_process(item_id)
result = poller.result()

# 清理
client.delete_item(item_id)
\`\`\`

## 参考文件

| 文件 | 内容 |
|------|------|
| references/tools.md | 工具集成 |
| references/streaming.md | 事件流模式 |
```

---

## 技能创建流程

1. **收集SDK上下文** — 用户提供SDK/API参考（必需）
2. **理解** — 从官方文档研究SDK模式
3. **规划** — 识别可重用资源和产品领域分类
4. **创建** — 在 `.github/skills/<skill-name>/` 编写SKILL.md
5. **分类** — 在 `skills/<language>/<category>/` 创建符号链接
6. **测试** — 创建验收标准和测试场景
7. **文档** — 更新README.md技能目录
8. **迭代** — 基于实际使用进行优化

### 步骤 1：收集SDK上下文（必需）

**在创建任何SDK技能之前，用户必须提供：**

| 必需 | 示例 | 用途 |
|------|------|------|
| **SDK包** | `azure-ai-agents`, `Azure.AI.OpenAI` | 标识确切的SDK |
| **文档URL** | `https://learn.microsoft.com/en-us/azure/ai-services/...` | 主要真实来源 |
| **仓库** (可选) | `Azure/azure-sdk-for-python` | 用于代码模式 |

**如未提供则提示用户：**
```
要创建此技能，我需要：
1. SDK包名（例如 azure-ai-projects）
2. Microsoft Learn文档URL或GitHub仓库
3. 目标语言 (py/dotnet/ts/java)
```

**首先搜索官方文档：**
```bash
# 使用 microsoft-docs MCP 获取当前API模式
# 查询: "[SDK名称] [操作] [语言]"
# 验证: 参数与最新SDK版本匹配
```

### 步骤 2：理解技能

收集具体示例：

- "此技能应涵盖哪些SDK操作？"
- "哪些触发器应激活此技能？"
- "开发者常遇到哪些错误？"

| 示例任务 | 可重用资源 |
|---------|-----------|
| 每次相同的认证代码 | SKILL.md中的代码示例 |
| 复杂的流模式 | `references/streaming.md` |
| 工具配置 | `references/tools.md` |
| 错误处理模式 | `references/error-handling.md` |

### 步骤 3：规划产品领域分类

技能通过符号链接按**语言**和**产品领域**组织在 `skills/` 目录中。

**产品领域分类：**

| 分类 | 描述 | 示例 |
|------|------|------|
| `foundry` | AI Foundry、代理、项目、推理 | `azure-ai-agents-py`, `azure-ai-projects-py` |
| `data` | 存储、Cosmos DB、Tables、Data Lake | `azure-cosmos-py`, `azure-storage-blob-py` |
| `messaging` | Event Hubs、Service Bus、Event Grid | `azure-eventhub-py`, `azure-servicebus-py` |
| `monitoring` | OpenTelemetry、App Insights、Query | `azure-monitor-opentelemetry-py` |
| `identity` | 认证、DefaultAzureCredential | `azure-identity-py` |
| `security` | Key Vault、密钥、证书 | `azure-keyvault-py` |
| `integration` | API管理、应用配置 | `azure-appconfiguration-py` |
| `compute` | 批处理、ML计算 | `azure-compute-batch-java` |
| `container` | 容器注册表、ACR | `azure-containerregistry-py` |

**确定分类**基于：
1. Azure服务系列（存储 → `data`, Event Hubs → `messaging`）
2. 主要用例（AI代理 → `foundry`）
3. 同一服务领域的现有技能

### 步骤 4：创建技能

**位置:** `.github/skills/<skill-name>/SKILL.md`

**命名约定：**
- `azure-<service>-<subservice>-<language>`
- 示例: `azure-ai-agents-py`, `azure-cosmos-java`, `azure-storage-blob-ts`

**对于Azure SDK技能：**

1. 搜索 `microsoft-docs` MCP 获取当前API模式
2. 对照已安装的SDK版本验证
3. 遵循上述章节顺序
4. 在示例中包含清理代码
5. 添加功能对比表

**先编写捆绑资源**，然后编写SKILL.md。

**前置元数据：**

```yaml
---
name: skill-name-py
description: |
  Azure服务SDK（Python）。用于[特定功能]。
  触发词: "服务名称", "创建资源", "特定操作".
---
```

### 步骤 5：使用符号链接分类

在 `.github/skills/` 创建技能后，在相应分类中创建符号链接：

```bash
# 模式: skills/<language>/<category>/<short-name> -> ../../../.github/skills/<full-skill-name>

# 示例: azure-ai-agents-py 在 python/foundry 中：
cd skills/python/foundry
ln -s ../../../.github/skills/azure-ai-agents-py agents

# 示例: azure-cosmos-db-py 在 python/data 中：
cd skills/python/data
ln -s ../../../.github/skills/azure-cosmos-db-py cosmos-db
```

**符号链接命名：**
- 使用简短、描述性名称（例如 `agents`, `cosmos`, `blob`）
- 移除 `azure-` 前缀和语言后缀
- 匹配分类中的现有模式

**验证符号链接：**
```bash
ls -la skills/python/foundry/agents
# 应显示: agents -> ../../../.github/skills/azure-ai-agents-py
```

### 步骤 6：创建测试

**每个技能必须有验收标准和测试场景。**

#### 6.1 创建验收标准

**位置:** `.github/skills/<skill-name>/references/acceptance-criteria.md`

**源材料**（按优先级）：
1. 官方Microsoft Learn文档（通过 `microsoft-docs` MCP）
2. 来自仓库的SDK源代码
3. 技能中的现有参考文件

**格式：**
```markdown
# 验收标准: <skill-name>

**SDK**: `package-name`
**仓库**: https://github.com/Azure/azure-sdk-for-<language>
**用途**: 技能测试验收标准

---

## 1. 正确的导入模式

### 1.1 客户端导入

#### ✅ 正确: 主客户端
\`\`\`python
from azure.ai.mymodule import MyClient
from azure.identity import DefaultAzureCredential
\`\`\`

#### ❌ 错误: 模块路径错误
\`\`\`python
from azure.ai.mymodule.models import MyClient  # 错误 - Client不在models中
\`\`\`

## 2. 认证模式

#### ✅ 正确: DefaultAzureCredential
\`\`\`python
credential = DefaultAzureCredential()
client = MyClient(endpoint, credential)
\`\`\`

#### ❌ 错误: 硬编码凭据
\`\`\`python
client = MyClient(endpoint, api_key="hardcoded")  # 安全风险
\`\`\`
```

**需要记录的关键模式：**
- 导入路径（Azure SDK之间差异显著）
- 认证模式
- 客户端初始化
- 异步变体（`.aio` 模块）
- 常见反模式

#### 6.2 创建测试场景

**位置:** `tests/scenarios/<skill-name>/scenarios.yaml`

```yaml
config:
  model: gpt-4
  max_tokens: 2000
  temperature: 0.3

scenarios:
  - name: basic_client_creation
    prompt: |
      使用Azure SDK创建一个基本示例。
      包含正确的认证和客户端初始化。
    expected_patterns:
      - "DefaultAzureCredential"
      - "MyClient"
    forbidden_patterns:
      - "api_key="
      - "hardcoded"
    tags:
      - basic
      - authentication
    mock_response: |
      import os
      from azure.identity import DefaultAzureCredential
      from azure.ai.mymodule import MyClient
      
      credential = DefaultAzureCredential()
      client = MyClient(
          endpoint=os.environ["AZURE_ENDPOINT"],
          credential=credential
      )
      # ... 其余工作示例
```

**场景设计原则：**
- 每个场景测试一个特定模式或功能
- `expected_patterns` — 必须出现的模式
- `forbidden_patterns` — 不得出现的常见错误
- `mock_response` — 通过所有检查的完整工作代码
- `tags` — 用于过滤（`basic`, `async`, `streaming`, `tools`）

#### 6.3 运行测试

```bash
cd tests
pnpm install

# 检查技能是否被发现
pnpm harness --list

# 以模拟模式运行（快速、确定性）
pnpm harness <skill-name> --mock --verbose

# 使用Ralph Loop运行（迭代改进）
pnpm harness <skill-name> --ralph --mock --max-iterations 5 --threshold 85
```

**成功标准：**
- 所有场景通过（100%通过率）
- 无误报（模拟响应始终通过）
- 模式能捕获真实错误

### 步骤 7：更新文档

创建技能后：

1. **更新README.md** — 在技能目录的相应语言部分添加技能
   - 更新总技能数（第~73行: `> N skills in...`）
   - 更新Skill Explorer链接数（第~15行: `Browse all N skills`）
   - 更新语言计数表（第~77-83行）
   - 更新语言部分计数（例如 `> N skills • suffix: -py`）
   - 更新分类计数（例如 `<summary><strong>Foundry & AI</strong> (N skills)</summary>`）
   - 在分类中按字母顺序添加技能行
   - 更新测试覆盖率摘要（第~622行: `**N skills with N test scenarios**`）
   - 更新测试覆盖率表 — 更新技能数、场景数和该语言的顶级技能

2. **重新生成GitHub Pages数据** — 运行提取脚本更新文档站点
   ```bash
   cd docs-site && npx tsx scripts/extract-skills.ts
   ```
   这会更新 `docs-site/src/data/skills.json`，它为基于Astro的文档站点提供数据。
   然后重建文档站点：
   ```bash
   cd docs-site && npm run build
   ```
   输出到 `docs/`，由GitHub Pages提供服务。

3. **验证AGENTS.md** — 确保技能计数准确

---

## 渐进式披露模式

### 模式 1：带参考的高级指南

```markdown
# SDK名称

## 快速开始
[最小示例]

## 高级功能
- **流处理**: 参见 references/streaming.md
- **工具**: 参见 references/tools.md
```

### 模式 2：语言变体

```
azure-service-skill/
├── SKILL.md (概述 + 语言选择)
└── references/
    ├── python.md
    ├── dotnet.md
    ├── java.md
    └── typescript.md
```

### 模式 3：功能组织

```
azure-ai-agents/
├── SKILL.md (核心工作流程)
└── references/
    ├── tools.md
    ├── streaming.md
    ├── async-patterns.md
    └── error-handling.md
```

---

## 设计模式参考

| 参考 | 内容 |
|------|------|
| `references/workflows.md` | 顺序和条件工作流程 |
| `references/output-patterns.md` | 模板和示例 |
| `references/azure-sdk-patterns.md` | 语言特定的Azure SDK模式 |

---

## 反模式

| 不要 | 原因 |
|------|------|
| 没有SDK上下文就创建技能 | 用户必须提供包名/文档URL |
| 在正文中放"何时使用" | 正文在触发后加载 |
| 硬编码凭据 | 安全风险 |
| 跳过认证章节 | 代理会随意发挥 |
| 使用过时的SDK模式 | API会变化；先搜索文档 |
| 包含README.md | 代理不需要元文档 |
| 深层嵌套参考资料 | 保持一层深度 |
| 跳过验收标准 | 没有测试的技能无法验证 |
| 跳过符号链接分类 | 技能将无法按分类发现 |
| 使用错误的导入路径 | Azure SDK有特定的模块结构 |

---

## 清单

完成技能前：

**前提条件：**
- [ ] 用户提供了SDK包名或文档URL
- [ ] 通过 `microsoft-docs` MCP 验证了SDK模式

**技能创建：**
- [ ] 描述包含内容和触发条件（触发短语）
- [ ] SKILL.md在500行以内
- [ ] 认证使用 `DefaultAzureCredential`
- [ ] 示例中包含清理/删除操作
- [ ] 参考资料按功能组织

**分类：**
- [ ] 技能创建在 `.github/skills/<skill-name>/`
- [ ] 符号链接创建在 `skills/<language>/<category>/<short-name>`
- [ ] 符号链接指向 `../../../.github/skills/<skill-name>`

**测试：**
- [ ] 创建了 `references/acceptance-criteria.md`，包含正确/错误模式
- [ ] 创建了 `tests/scenarios/<skill-name>/scenarios.yaml`
- [ ] 所有场景通过 (`pnpm harness <skill> --mock`)
- [ ] 导入路径精确记录

**文档：**
- [ ] 更新了README.md技能目录
- [ ] 指导搜索 `microsoft-docs` MCP 获取当前API

## 使用场景
此技能适用于执行概述中描述的工作流程或操作。

## 限制
- 仅当任务明确匹配上述范围时使用此技能
- 不要将输出视为环境特定验证、测试或专家审查的替代品
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清