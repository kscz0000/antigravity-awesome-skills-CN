---
name: create-branch
description: 按照 Sentry 命名规范创建 git 分支。当被要求"create a branch"、"new branch"、"start a branch"、"make a branch"、"switch to a new branch"，或在默认分支上开始新工作时使用。
argument-hint: '[可选的工作描述]'
risk: critical
source: community
---

# 创建分支

创建一个带有正确类型前缀和描述性名称的 git 分支，遵循 Sentry 规范。

## 何时使用
- 你需要创建一个遵循仓库命名规范的新 git 分支。
- 你正在默认分支上开始一项新工作，需要帮助将其分类为 `feat`、`fix`、`docs` 或其他分支类型。
- 你希望从任务描述或当前本地差异中生成分支名称。

## 步骤 1：获取用户名前缀

运行 `gh api user --jq .login` 获取 GitHub 用户名。

如果命令失败（例如未认证），请询问用户的首选前缀。

## 步骤 2：确定分支描述

**如果提供了 `$ARGUMENTS`**，将其用作工作描述。

**如果没有参数**，检查本地更改：

```bash
git diff
git diff --cached
git status --short
```

- **存在更改**：读取差异内容以理解工作内容并生成描述。
- **无更改**：询问用户他们将要做什么工作。

## 步骤 3：分类类型

根据描述从下表中选择类型：

| 类型      | 使用场景                                                              |
| --------- | --------------------------------------------------------------------- |
| `feat`    | 新的用户面向功能                                         |
| `fix`     | 损坏的行为现在可以工作了                                             |
| `ref`     | 相同行为，不同结构                                    |
| `chore`   | 依赖、配置、版本升级、更新现有工具 — 无新逻辑 |
| `perf`    | 相同行为，更快                                                 |
| `style`   | CSS、格式化、仅视觉                                          |
| `docs`    | 仅文档                                                    |
| `test`    | 仅测试                                                            |
| `ci`      | CI/CD 配置                                                          |
| `build`   | 构建系统                                                          |
| `meta`    | 仓库元数据更改                                                 |
| `license` | 许可证更改                                                       |

不确定时：新事物用 `feat`（包括新脚本、技能或工具），重构现有事物用 `ref`，仅当更新/维护已存在的事物时用 `chore`。

## 步骤 4：生成并提议

构建分支名称为 `<username>/<type>/<short-description>`。

`<short-description>` 的规则：

- 短横线命名，小写
- 3 到 6 个词，简洁但清晰
- 描述更改，而非文件名
- 仅使用 ASCII 字母、数字和短横线 — 不使用空格、点、冒号、波浪号或其他 git 禁止的字符

向用户展示并询问是否使用、修改或更改类型。

### 示例

| 工作描述                           | 分支名称                                 |
| ------------------------------------------ | ------------------------------------------- |
| 点击外部时下拉菜单未关闭 | `priscila/fix/dropdown-not-closing-on-blur` |
| 为对话页面添加搜索        | `priscila/feat/add-search-to-conversations` |
| 重构抽屉组件            | `priscila/ref/simplify-drawer-components`   |
| 更新测试固件                     | `priscila/chore/update-test-fixtures`       |
| 将 @sentry/react 升级到最新版本    | `priscila/chore/bump-sentry-react`          |
| 添加新的智能体技能                   | `priscila/feat/add-create-branch-skill`     |

## 步骤 5：创建分支

确认后，检测当前分支和默认分支：

```bash
git branch --show-current
git remote | grep -qx origin && echo origin || git remote | head -1
git symbolic-ref refs/remotes/<remote>/HEAD 2>/dev/null | sed 's|refs/remotes/<remote>/||' | tr -d '[:space:]'
```

如果 `symbolic-ref` 失败，回退到 `git branch --list main master`：使用存在的那个；如果都存在或都不存在，询问用户。

如果 `git branch --show-current` 为空（分离 HEAD），显示当前提交（`git rev-parse --short HEAD`）并询问是从它分支还是先切换到默认分支。

否则，如果当前分支不是默认分支，警告用户并询问是从当前分支分支还是先切换到默认分支。

如果用户想切换到默认分支，适当处理任何未提交的更改（如果存在则提供暂存），然后运行 `git checkout <default-branch>`。如果失败，恢复暂存的更改（如适用）并停止。

创建分支前，检查名称是否已在本地或远程存在（`git show-ref`）。如果存在，请用户选择不同的名称。

创建分支：

```bash
git checkout -b <branch-name>
```

分支创建后恢复任何暂存的更改。

## 参考资料

- [Sentry 分支命名](https://develop.sentry.dev/sdk/getting-started/standards/code-submission/#branch-naming)

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
