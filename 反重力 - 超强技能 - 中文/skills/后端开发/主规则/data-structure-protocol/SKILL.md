---
name: data-structure-protocol
description: "为智能体提供代码库的持久化结构记忆——导航依赖关系、追踪公开 API，并理解连接存在的原因，无需重新阅读整个仓库。"
risk: safe
source: "https://github.com/k-kolomeitsev/data-structure-protocol"
date_added: "2026-02-27"
---

# Data Structure Protocol (DSP)

LLM 编码智能体在任务之间会丢失上下文。在大型代码库中，它们将大部分 token 花费在"定位"上——弄清楚东西在哪里、什么依赖于什么、以及什么是安全可改的。DSP 通过将项目的结构图外部化为持久化、可查询的图来解决这个问题，该图存储在代码旁边的 `.dsp/` 目录中。

DSP 不是给人类看的文档，也不是 AST 转储。它捕获三件事：**含义**（为什么实体存在）、**边界**（它导入和暴露什么）、以及**原因**（为什么每个连接存在）。这足以让智能体在不将整个源代码树加载到上下文窗口的情况下导航、重构和生成代码。

## 何时使用

在以下情况下使用此技能：
- 项目有 `.dsp/` 目录（DSP 已设置）
- 用户要求设置 DSP、引导或映射项目结构
- 在 DSP 跟踪的项目中创建、修改或删除代码文件（以保持图的更新）
- 导航项目结构、理解依赖关系或查找特定模块
- 用户提到 DSP、dsp-cli、`.dsp` 或结构映射
- 在重构或依赖替换前进行影响分析

## 核心概念

### 代码 = 图

DSP 将代码库建模为有向图。节点是**实体**，边是**导入**和**共享/导出**。

存在两种实体类型：
- **Object**：任何不是函数的"东西"（模块/文件/类/配置/资源/外部依赖）
- **Function**：导出的函数/方法/处理器/管道

### 通过 UID 标识，而非文件路径

每个实体获得一个稳定的 UID：`obj-<8hex>` 用于对象，`func-<8hex>` 用于函数。文件路径是可以更改的属性；UID 在重命名、移动和重新格式化后仍然存活。

对于文件内的实体，UID 通过源代码中的注释标记锚定：

```js
// @dsp func-7f3a9c12
export function calculateTotal(items) { ... }
```

```python
# @dsp obj-e5f6g7h8
class UserService:
```

### 每个连接都有一个"为什么"

当记录导入时，DSP 存储一个简短的原因，解释*为什么*该依赖存在。这存储在被导入实体的 `exports/` 反向索引中。没有原因的依赖图告诉你*什么导入了什么*；原因告诉你**什么是安全可改的以及谁会崩溃**。

### 存储格式

每个实体在 `.dsp/` 下获得一个小目录：

```
.dsp/
├── TOC                        # 从根目录开始的所有实体 UID 有序列表
├── obj-a1b2c3d4/
│   ├── description            # 源路径、类型、用途（1-3 句话）
│   ├── imports                # 此实体依赖的 UID（每行一个）
│   ├── shared                 # 公开 API / 导出实体的 UID
│   └── exports/               # 反向索引：谁导入此实体以及为什么
│       ├── <importer_uid>     # 文件内容 = "为什么" 文本
│       └── <shared_uid>/
│           ├── description    # 导出了什么
│           └── <importer_uid> # 为什么导入这个特定导出
└── func-7f3a9c12/
    ├── description
    ├── imports
    └── exports/
```

一切都是纯文本。可 diff。可审查。不需要数据库。

### 完整导入覆盖

任何被导入的文件或工件都必须在 `.dsp` 中表示为一个 Object——代码、图片、样式、配置、JSON、wasm，一切。外部依赖（npm 包、stdlib 等）被记录为 `kind: external`，但其内部永远不会被分析。

## 工作原理

### 初始设置

此技能依赖于独立的 Python CLI 脚本 `dsp-cli.py`。如果项目中缺少它，请下载：

```bash
curl -O https://raw.githubusercontent.com/k-kolomeitsev/data-structure-protocol/main/skills/data-structure-protocol/scripts/dsp-cli.py
```

需要 **Python 3.10+**。所有命令使用 `python dsp-cli.py --root <project-root> <command>`。

### 引导（初始映射）

如果 `.dsp/` 为空，从根入口点通过 DFS 遍历项目的导入：

1. 识别根入口点（`package.json` main、框架入口、`main.py` 等）
2. 记录根文件：为每个导出执行 `create-object`、`create-function`、`create-shared`，为所有依赖执行 `add-import`
3. 取第一个非外部导入，完整记录它，深入其导入
4. 当没有未访问的本地导入时回溯；继续直到所有可达文件都被记录
5. 外部依赖：`create-object --kind external`，添加到 TOC，但永远不深入 `node_modules`/`site-packages`/等

### 工作流规则

- **修改代码前**：通过 `search`、`find-by-source` 或 `read-toc` 查找受影响的实体。阅读它们的 `description` 和 `imports` 以理解上下文。
- **创建文件/模块时**：调用 `create-object`。为每个导出函数调用 `create-function`（带 `--owner`）。通过 `create-shared` 注册导出。
- **添加导入时**：调用 `add-import` 并附带简短的 `why`。对于外部依赖——如果实体不存在，先 `create-object --kind external`。
- **删除导入/导出/文件时**：调用 `remove-import`、`remove-shared`、`remove-entity`。级联清理是自动的。
- **重命名/移动文件时**：调用 `move-entity`。UID 不会改变。
- **如果只是内部实现改变**，不影响用途或依赖，则**不要触碰 DSP**。

### 关键命令

| 类别 | 命令 |
|------|------|
| **创建** | `init`, `create-object`, `create-function`, `create-shared`, `add-import` |
| **更新** | `update-description`, `update-import-why`, `move-entity` |
| **删除** | `remove-import`, `remove-shared`, `remove-entity` |
| **导航** | `get-entity`, `get-children --depth N`, `get-parents --depth N`, `get-path`, `get-recipients`, `read-toc` |
| **搜索** | `search <query>`, `find-by-source <path>` |
| **诊断** | `detect-cycles`, `get-orphans`, `get-stats` |

### 何时更新 DSP

| 代码变更 | DSP 操作 |
|---|---|
| 新文件/模块 | `create-object` + `create-function` + `create-shared` + `add-import` |
| 添加新导入 | `add-import`（+ `create-object --kind external` 如果是新依赖） |
| 移除导入 | `remove-import` |
| 添加导出 | `create-shared`（+ `create-function` 如果是新的） |
| 移除导出 | `remove-shared` |
| 文件重命名/移动 | `move-entity` |
| 文件删除 | `remove-entity` |
| 用途改变 | `update-description` |
| 仅内部变更 | **无需更新 DSP** |

## 示例

### 示例 1：设置 DSP 并记录模块

```bash
python dsp-cli.py --root . init

python dsp-cli.py --root . create-object "src/app.ts" "主应用程序入口点"
# 输出：obj-a1b2c3d4

python dsp-cli.py --root . create-function "src/app.ts#start" "启动 HTTP 服务器" --owner obj-a1b2c3d4
# 输出：func-7f3a9c12

python dsp-cli.py --root . create-shared obj-a1b2c3d4 func-7f3a9c12

python dsp-cli.py --root . add-import obj-a1b2c3d4 obj-deadbeef "HTTP 路由"
```

### 示例 2：在修改前导航图

```bash
python dsp-cli.py --root . search "authentication"
python dsp-cli.py --root . get-entity obj-a1b2c3d4
python dsp-cli.py --root . get-children obj-a1b2c3d4 --depth 2
python dsp-cli.py --root . get-recipients obj-a1b2c3d4
python dsp-cli.py --root . get-path obj-a1b2c3d4 func-7f3a9c12
```

### 示例 3：替换库前的影响分析

```bash
python dsp-cli.py --root . find-by-source "lodash"
# 输出：obj-11223344

python dsp-cli.py --root . get-recipients obj-11223344
# 显示每个导入 lodash 的模块以及原因——让你系统地替换它
```

## 最佳实践

- ✅ **应该：** 在创建新文件、添加导入或更改公开 API 时立即更新 DSP
- ✅ **应该：** 在记录导入时始终添加有意义的 `why` 原因——这是 DSP 大部分价值所在
- ✅ **应该：** 对第三方库使用 `kind: external` 而不分析其内部
- ✅ **应该：** 保持描述最小化（1-3 句话说明用途，而非实现）
- ✅ **应该：** 将 `.dsp/` 的 diff 视为代码 diff——审查它们，保持准确
- ❌ **不应该：** 对于不影响用途或依赖的仅内部变更，不要触碰 `.dsp/`
- ❌ **不应该：** 在重命名/移动时更改实体的 UID（改用 `move-entity`）
- ❌ **不应该：** 为每个局部变量或辅助函数创建 UID——只为文件级 Object 和公开/共享实体创建

## 集成

此技能自然连接到：
- **context-compression** — DSP 通过提供定向检索而非加载所有内容来减少压缩需求
- **context-optimization** — DSP 是一种结构优化：智能体拉取最小"上下文包"而非原始源码
- **architecture** — DSP 捕获架构边界（导入/导出），为系统设计决策提供依据

## 参考资料

- **完整架构规范**：[ARCHITECTURE.md](https://github.com/k-kolomeitsev/data-structure-protocol/blob/main/ARCHITECTURE.md)
- **CLI 源码 + 参考文档**：[skills/data-structure-protocol](https://github.com/k-kolomeitsev/data-structure-protocol/tree/main/skills/data-structure-protocol)
- **介绍文章**：[article.md](https://github.com/k-kolomeitsev/data-structure-protocol/blob/main/article.md)

## 限制

- 仅当任务明显符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
