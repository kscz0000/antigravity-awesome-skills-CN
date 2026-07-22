---
name: apify-actorization
description: "Actorization 将现有软件转换为与 Apify 平台兼容的可复用无服务器应用。Actor 是打包为 Docker 镜像的程序，接受定义良好的 JSON 输入，执行操作，并可选地生成结构化 JSON 输出。触发词：Apify Actor化、Actorization、无服务器应用、Docker镜像打包、Apify SDK集成、CLI工具封装、Crawlee迁移"
risk: unknown
source: community
---

# Apify Actorization

Actorization 将现有软件转换为与 Apify 平台兼容的可复用无服务器应用。Actor 是打包为 Docker 镜像的程序，接受定义良好的 JSON 输入，执行操作，并可选地生成结构化 JSON 输出。

## 快速开始

1. 在项目根目录运行 `apify init`
2. 使用 SDK 生命周期包装代码（参见下方语言特定章节）
3. 配置 `.actor/input_schema.json`
4. 使用 `apify run --input '{"key": "value"}'` 测试
5. 使用 `apify push` 部署

## 何时使用此技能

- 将现有项目转换为在 Apify 平台上运行
- 为项目添加 Apify SDK 集成
- 将 CLI 工具或脚本封装为 Actor
- 将 Crawlee 项目迁移到 Apify

## 前置条件

验证 `apify` CLI 已安装：

```bash
apify --help
```

如果未安装：

```bash
brew install apify-cli

# 或：npm install -g apify-cli
# 或从操作系统包管理器验证的官方发布包安装
```

验证 CLI 已登录：

```bash
apify info  # 应返回你的用户名
```

如果未登录，检查 `APIFY_TOKEN` 环境变量是否已定义。如果未定义，请用户在 https://console.apify.com/settings/integrations 生成一个，将其添加到 shell 或密钥管理器中（不要将实际令牌放入命令历史），然后运行：

```bash
apify login
```

## Actorization 检查清单

复制此检查清单以跟踪进度：

- [ ] 步骤 1：分析项目（语言、入口点、输入、输出）
- [ ] 步骤 2：运行 `apify init` 创建 Actor 结构
- [ ] 步骤 3：应用语言特定的 SDK 集成
- [ ] 步骤 4：配置 `.actor/input_schema.json`
- [ ] 步骤 5：配置 `.actor/output_schema.json`（如适用）
- [ ] 步骤 6：更新 `.actor/actor.json` 元数据
- [ ] 步骤 7：使用 `apify run` 本地测试
- [ ] 步骤 8：使用 `apify push` 部署

## 步骤 1：分析项目

在进行更改之前，了解项目：

1. **识别语言** - JavaScript/TypeScript、Python 或其他
2. **找到入口点** - 启动执行的主文件
3. **识别输入** - 命令行参数、环境变量、配置文件
4. **识别输出** - 文件、控制台输出、API 响应
5. **检查状态** - 是否需要在运行之间持久化数据？

## 步骤 2：初始化 Actor 结构

在项目根目录运行：

```bash
apify init
```

这将创建：
- `.actor/actor.json` - Actor 配置和元数据
- `.actor/input_schema.json` - Apify Console 的输入定义
- `Dockerfile`（如果不存在）- 容器镜像定义

## 步骤 3：应用语言特定更改

根据项目语言选择：

- **JavaScript/TypeScript**：参见 [js-ts-actorization.md](references/js-ts-actorization.md)
- **Python**：参见 [python-actorization.md](references/python-actorization.md)
- **其他语言（基于 CLI）**：参见 [cli-actorization.md](references/cli-actorization.md)

### 快速参考

| 语言 | 安装 | 包装代码 |
|----------|---------|-----------|
| JS/TS | `npm install apify` | `await Actor.init()` ... `await Actor.exit()` |
| Python | `pip install apify` | `async with Actor:` |
| 其他 | 在包装脚本中使用 CLI | `apify actor:get-input` / `apify actor:push-data` |

## 步骤 4-6：配置 Schema

参见 [schemas-and-output.md](references/schemas-and-output.md) 了解以下详细配置：
- 输入 schema（`.actor/input_schema.json`）
- 输出 schema（`.actor/output_schema.json`）
- Actor 配置（`.actor/actor.json`）
- 状态管理（请求队列、键值存储）

使用 `@apify/json_schemas` npm 包验证 schema。

## 步骤 7：本地测试

使用内联输入运行 actor（适用于 JS/TS 和 Python actor）：

```bash
apify run --input '{"startUrl": "https://example.com", "maxItems": 10}'
```

或使用输入文件：

```bash
apify run --input-file ./test-input.json
```

**重要：** 始终使用 `apify run`，而不是 `npm start` 或 `python main.py`。CLI 会设置正确的环境和存储。

## 步骤 8：部署

```bash
apify push
```

这将上传并在 Apify 平台上构建你的 actor。

## 变现（可选）

部署后，你可以在 Apify Store 中变现你的 actor。推荐模式是**按事件付费（PPE）**：

- 按结果/抓取项
- 按处理页面
- 按发起的 API 调用

在 Apify Console 的 Actor > Monetization 下配置 PPE。在代码中使用 `await Actor.charge('result')` 收取事件费用。

其他选项：**租赁**（月度订阅）或**免费**（开源）。

## 部署前检查清单

- [ ] `.actor/actor.json` 存在且名称和描述正确
- [ ] `.actor/actor.json` 通过 `@apify/json_schemas` 验证（`actor.schema.json`）
- [ ] `.actor/input_schema.json` 定义了所有必需输入
- [ ] `.actor/input_schema.json` 通过 `@apify/json_schemas` 验证（`input.schema.json`）
- [ ] `.actor/output_schema.json` 定义了输出结构（如适用）
- [ ] `.actor/output_schema.json` 通过 `@apify/json_schemas` 验证（`output.schema.json`）
- [ ] `Dockerfile` 存在且构建成功
- [ ] `Actor.init()` / `Actor.exit()` 包装主代码（JS/TS）
- [ ] `async with Actor:` 包装主代码（Python）
- [ ] 输入通过 `Actor.getInput()` / `Actor.get_input()` 读取
- [ ] 输出使用 `Actor.pushData()` 或键值存储
- [ ] `apify run` 使用测试输入成功执行
- [ ] `generatedBy` 在 actor.json meta 部分中设置

## Apify MCP 工具

如果配置了 MCP 服务器，使用以下工具获取文档：

- `search-apify-docs` - 搜索文档
- `fetch-apify-docs` - 获取完整文档页面

否则，MCP 服务器 URL：`https://mcp.apify.com/?tools=docs`。

## 资源

- [Actorization Academy](https://docs.apify.com/academy/actorization) - 综合指南
- [Apify SDK for JavaScript](https://docs.apify.com/sdk/js) - 完整 SDK 参考
- [Apify SDK for Python](https://docs.apify.com/sdk/python) - 完整 SDK 参考
- [Apify CLI Reference](https://docs.apify.com/cli) - CLI 命令
- [Actor Specification](https://raw.githubusercontent.com/apify/actor-whitepaper/refs/heads/master/README.md) - 完整规范

## 限制
- 仅当任务明确匹配上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
