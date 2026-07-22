# create-expo-module

使用 `create-expo-module` 搭建新的 Expo 模块，使用 `create-expo-module add-platform-support` 扩展现有的 Expo 模块。

优先使用 `create-expo-module` 而非手动创建模块文件和目录。在大多数情况下，正确的做法是先生成脚手架，然后再在其上构建。

## 首先选择模块类型

### Local 模块

当原生代码仅属于一个 Expo app 时，使用 local 模块。

- 位于 app 内部
- 使用 app 的依赖和工具链
- 不创建示例 app
- 遵循 `package.json:expo.autolinking.nativeModulesDir`，否则回退到 `modules/`

### Standalone 模块

当模块需要在多个 app 间复用、作为 monorepo 包存在或发布到 npm 时，使用 standalone 模块。

- 拥有自己的 `package.json`
- 安装自己的依赖
- 在搭建过程中构建 TypeScript
- 通常会创建一个 `example` app，除非传入 `--no-example`
- 如果尚未处于某个 Git 仓库中，可能会初始化一个

创建 standalone 模块时，默认保留示例 app。仅当用户明确要求 `--no-example` 或明显不需要示例项目时才跳过它。

## 推荐命令

### Local 模块

使用显式的 slug 或路径。

```bash
npx create-expo-module@latest key-value-store --local --platform apple android --features Function AsyncFunction
```

如果你需要确定性的非交互输出，请显式传入 slug 或路径，然后再传入其他选项：

```bash
EXPO_NONINTERACTIVE=1 npx create-expo-module@latest key-value-store \
  --local \
  --name KeyValueStore \
  --package expo.modules.keyvaluestore \
  --platform apple android \
  --features Function AsyncFunction
```

重要注意事项：

- 在非交互的 local 脚手架中，省略位置参数 slug 会导致 CLI 回退到 `my-module`
- `--name` 更改原生模块类名，而非目录名

### Standalone 模块

```bash
npx create-expo-module@latest expo-key-value-store --platform apple android --features Function AsyncFunction
```

## 创建选项

以下是 CLI 暴露的模块创建选项：

| 选项                          | 适用范围            | 说明                                                                                                       |
| ----------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------- |
| `[path]`                      | local, standalone | 位置参数 slug 或目标路径。在非交互模式下，请显式传入以获得稳定的 local 脚手架。                                                    |
| `--local`                     | local             | 在当前 Expo 项目内创建 local 模块。                                                                                |
| `--platform <platforms...>`   | local, standalone | 有效值：`apple`、`android`、`web`。                                                                            |
| `--features <features...>`    | local, standalone | 选择生成的功能示例。使用 `all` 可包含全部。                                                                              |
| `--full-example`              | local, standalone | 等价于 `--features all`。                                                                                     |
| `--barrel`                    | local             | 生成一个 local `index.ts` barrel。Standalone 模块忽略此选项。                                                       |
| `--source <source_dir>`       | local, standalone | 使用本地 `expo-module-template` 目录，而非从 npm 下载。                                                                |
| `--name <name>`               | local, standalone | 原生模块名称，例如 `KeyValueStore`。                                                                                |
| `--description <description>` | standalone        | 包描述。                                                                                                     |
| `--package <package>`         | local, standalone | Android 包名，例如 `expo.modules.keyvaluestore`。                                                                 |
| `--author-name <name>`        | standalone        | 包作者姓名。                                                                                                   |
| `--author-email <email>`      | standalone        | 包作者邮箱。                                                                                                   |
| `--author-url <url>`          | standalone        | 包作者个人主页 URL。                                                                                              |
| `--repo <url>`                | standalone        | 包仓库 URL。                                                                                                  |
| `--license <license>`         | standalone        | 包许可证标识符。                                                                                                  |
| `--module-version <version>`  | standalone        | 初始包版本。                                                                                                   |
| `--package-manager <manager>` | standalone        | 之一：`npm`、`pnpm`、`yarn`、`bun`。                                                                            |
| `--with-readme`               | standalone        | 保留生成包中的 `README.md`。                                                                                     |
| `--with-changelog`            | standalone        | 保留生成包中的 `CHANGELOG.md`。                                                                                  |
| `--no-example`                | standalone        | 跳过创建示例 app。                                                                                              |

备注：

- `--description`、作者相关选项、`--repo`、`--license` 和 `--module-version` 仅影响 standalone 模块，因为 local 模块没有独立的包清单。
- `--with-readme`、`--with-changelog`、`--no-example` 和 `--package-manager` 仅与 standalone 有关。
- `--barrel` 仅影响 local 模块。
- `--name` 更改原生模块类名，但不会重命名 local 模块目录。

## 平台

有效值如下：

- `apple`
- `android`
- `web`

需要记住的行为：

- 在非交互模式下，当省略 `--platform` 时，standalone 模块默认使用所有平台
- 在非交互模式下，local 模块同样默认使用所有平台
- 在交互式 local 脚手架中，当 `app.json:expo.platforms` 可用时，会基于该字段预选平台（将 `ios` 映射为 `apple`）
- 无效的平台值会被忽略并发出警告；如果所有提供的值都无效，CLI 将回退到所有平台

如果你不需要 web 支持，请在搭建时省略 `web`，而不是事后移除它。

## 功能示例

功能示例是生成的入门代码片段，而非能力限制。它们是常见 Expo Modules API 模式的小型可工作示例。

可用值：

- `Constant`
- `Function`
- `AsyncFunction`
- `Event`
- `View`
- `ViewEvent`
- `SharedObject`

重要行为：

- 未选择任何功能意味着一个最小化的模块
- 在交互模式下，功能示例默认未选中
- 在非交互模式下，除非传入 `--features` 或 `--full-example`，否则不会包含任何功能
- `--full-example` 等价于 `--features all`
- `ViewEvent` 自动包含 `View`

仅当模块实际渲染 UI 时才使用 `View`。对于纯原生模块，除非你计划使用视图文件，否则不要搭建它们。

## Local 模块注意事项

- local 模块默认不会生成 `index.ts` barrel
- 仅当需要根 barrel 文件时才使用 `--barrel`
- local 模块会跳过依赖安装，且不创建 `example` app
- local 模块没有自己的 `package.json`；它们依赖宿主 app

如果未使用 `--barrel`，CLI 的后续使用说明会指向从模块的 `src/` 文件直接导入。

## Standalone 模块注意事项

- `--package-manager` 仅与 standalone 模块相关
- 如果省略，CLI 会从 user agent 或可用的包管理器中检测
- 脚手架会在安装依赖后构建 TypeScript
- 仅当启用示例时才会创建 `example` app；`--no-example` 会跳过
- `--with-readme` 和 `--with-changelog` 用于选择性地启用这些文件

生成的 standalone 脚本包括 `build`、`clean`、`test`、`prepare`、`open:ios` 和 `open:android`。

## add-platform-support

当现有 Expo 模块需要新增一个支持的平台时，请使用此子命令。

从模块根目录的交互式用法：

```bash
npx create-expo-module@latest add-platform-support
```

显式用法：

```bash
npx create-expo-module@latest add-platform-support --platform android
```

也可以传入模块路径：

```bash
npx create-expo-module@latest add-platform-support ./packages/expo-key-value-store --platform web
```

重要行为：

- 支持的值为 `apple`、`android` 和 `web`
- 在非交互模式下，`--platform` 是必需的
- 该命令只会添加 `expo-module.config.json` 中尚未存在的平台
- 它会拒绝覆盖现有的 `android/` 或 `ios/` 目录
- 对于原生模块，它仅适用于使用 Expo Modules API DSL 的模块
- 不支持旧的模块格式

### 功能检测

`add-platform-support` 会尝试从原生模块定义中检测现有模块的功能示例。这是尽力而为的。

在以下情况下，使用 `--features` 覆盖检测到的功能示例：

- 模块非常规
- 模块使用生成的代码
- 定义分散在多个文件中
- 生成的文件与现有模块的形态不匹配

如果未检测到也未提供任何功能，该命令会为新平台创建一个最小化的脚手架。

## 环境变量

- `EXPO_BETA`：使用下一个模板版本
- `EXPO_DEBUG`：启用调试日志
- `EXPO_NO_TELEMETRY`：禁用遥测
- `EXPO_NONINTERACTIVE`：强制非交互模式
- `CI`：与 `EXPO_NONINTERACTIVE` 相同，用于 CI 环境