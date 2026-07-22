---
name: skill-rails-upgrade
description: "分析 Rails 应用并提供升级评估报告。触发词：Rails 升级、分析 Rails 应用、升级评估、upgrade rails、rails upgrade、analyze rails"
risk: safe
source: "https://github.com/robzolkos/skill-rails-upgrade"
date_added: "2026-02-27"
---

## 使用场景

分析 Rails 应用并提供升级评估报告

当处理分析 Rails 应用并提供升级评估报告的任务时使用此技能。

# Rails 升级分析器

分析当前 Rails 应用并提供全面的升级评估，支持选择性文件合并。

## 步骤 1：验证 Rails 应用

通过检查以下文件确认当前处于 Rails 应用中：
- `Gemfile`（必须存在且包含 'rails'）
- `config/application.rb`（Rails 应用配置）
- `config/environment.rb`（Rails 环境）

如果任何文件缺失或未表明是 Rails 应用，停下来告知用户这似乎不是一个 Rails 应用。

## 步骤 2：获取当前 Rails 版本

从以下位置提取当前 Rails 版本：
1. 首先检查 `Gemfile.lock` 中的精确已安装版本（查找 `rails (x.y.z)`）
2. 如果未找到，检查 `Gemfile` 中的版本约束

报告确切的当前版本（例如 `7.1.3`）。

## 步骤 3：查找最新 Rails 版本

使用 GitHub CLI 获取最新的 Rails 发布版本：

```bash
gh api repos/rails/rails/releases/latest --jq '.tag_name'
```

这将返回最新的稳定版本标签（例如 `v8.0.1`）。去掉 'v' 前缀用于比较。

同时检查近期标签以了解发布情况：

```bash
gh api repos/rails/rails/tags --jq '.[0:10] | .[].name'
```

## 步骤 4：确定升级类型

比较当前版本和最新版本以分类升级类型：

- **补丁升级**：相同主版本.次版本，不同补丁版本（例如 7.1.3 → 7.1.5）
- **次版本升级**：相同主版本，不同次版本（例如 7.1.3 → 7.2.0）
- **主版本升级**：不同主版本（例如 7.1.3 → 8.0.0）

## 步骤 5：获取升级指南

使用 WebFetch 获取官方 Rails 升级指南：

URL: `https://guides.rubyonrails.org/upgrading_ruby_on_rails.html`

查找与版本跳跃相关的章节。指南按目标版本组织，包含以下章节：
- "从 Rails X.Y 升级到 Rails X.Z"
- 破坏性变更
- 弃用警告
- 配置变更
- 必需的迁移

为用户的具体升级路径提取和总结相关章节。

## 步骤 6：获取 Rails Diff

使用 WebFetch 从 railsdiff.org 获取版本间的差异：

URL: `https://railsdiff.org/{当前版本}/{目标版本}`

例如：`https://railsdiff.org/7.1.3/8.0.0`

这将展示：
- 默认配置文件的变更
- 需要添加的新文件
- 修改的初始化器
- 更新的依赖
- bin/ 脚本的变更

总结关键文件变更。

## 步骤 7：检查 JavaScript 依赖

Rails 应用通常包含应随 Rails 一起更新的 JavaScript 包。检查并报告这些依赖。

### 7.1：识别 JS 包管理器

检查应用使用的包管理器：

```bash
# 检查 package.json（npm/yarn）
ls package.json 2>/dev/null

# 检查 importmap（Rails 7+）
ls config/importmap.rb 2>/dev/null
```

### 7.2：检查 Rails 相关的 JS 包

如果 `package.json` 存在，检查以下 Rails 相关的包：

```bash
# 提取 Rails 相关包的当前版本
cat package.json | grep -E '"@hotwired/|"@rails/|"stimulus"|"turbo-rails"' || echo "No Rails JS packages found"
```

**需要检查的关键包：**

| 包名 | 用途 | 版本对齐 |
|------|------|----------|
| `@hotwired/turbo-rails` | Turbo Drive/Frames/Streams | 应匹配 Rails 版本时代 |
| `@hotwired/stimulus` | Stimulus JS 框架 | 通常在各 Rails 版本间保持稳定 |
| `@rails/actioncable` | WebSocket 支持 | 应匹配 Rails 版本 |
| `@rails/activestorage` | 直接上传 | 应匹配 Rails 版本 |
| `@rails/actiontext` | 富文本编辑 | 应匹配 Rails 版本 |
| `@rails/request.js` | Rails UJS 替代 | 应匹配 Rails 版本时代 |

### 7.3：检查更新

对于 npm/yarn 项目，检查可用更新：

```bash
# 使用 npm
npm outdated @hotwired/turbo-rails @hotwired/stimulus @rails/actioncable @rails/activestorage 2>/dev/null

# 或直接检查最新版本
npm view @hotwired/turbo-rails version 2>/dev/null
npm view @rails/actioncable version 2>/dev/null
```

### 7.4：检查 Importmap Pin（如适用）

如果应用使用 importmap-rails，检查 `config/importmap.rb` 中的 pin 版本：

```bash
cat config/importmap.rb | grep -E 'pin.*turbo|pin.*stimulus|pin.*@rails' || echo "No importmap pins found"
```

更新 importmap pin：
```bash
bin/importmap pin @hotwired/turbo-rails
bin/importmap pin @hotwired/stimulus
```

### 7.5：JS 依赖总结

在升级总结中包含：

```
### JavaScript 依赖

**包管理器**：[npm/yarn/importmap/无]

| 包名 | 当前版本 | 最新版本 | 操作 |
|------|----------|----------|------|
| @hotwired/turbo-rails | 8.0.4 | 8.0.12 | 建议更新 |
| @rails/actioncable | 7.1.0 | 8.0.0 | 随 Rails 一起更新 |
| ... | ... | ... | ... |

**建议的 JS 更新：**
- 运行 `npm update @hotwired/turbo-rails`（或 yarn 等效命令）
- 运行 `npm update @rails/actioncable @rails/activestorage` 以匹配 Rails 版本
```

---

## 步骤 8：生成升级总结

提供包含步骤 1-7 所有发现的综合总结：

### 版本信息
- 当前版本：X.Y.Z
- 最新版本：A.B.C
- 升级类型：[补丁/次版本/主版本]

### 升级复杂度评估

根据以下因素将升级评定为**小型**、**中型**或**大型**：

| 因素 | 小型 | 中型 | 大型 |
|------|------|------|------|
| 版本跳跃 | 仅补丁版本 | 次版本 | 主版本 |
| 破坏性变更 | 无 | 少量，文档完善 | 多且重大 |
| 配置变更 | 极少 | 适中 | 大量 |
| 弃用项 | 无活跃弃用 | 部分需要处理 | 多项需要重构 |
| 依赖 | 兼容 | 部分需要更新 | 需要主要依赖更新 |

### 需要处理的关键变更

列出用户需要处理的最重要变更：
1. 配置文件更新
2. 已弃用的方法/功能更新
3. 新增的必需依赖
4. 需要的数据库迁移
5. 破坏性 API 变更

### 建议的升级步骤

1. 更新测试套件并确保通过
2. 审查当前版本中的弃用警告
3. 更新 Gemfile 中的 Rails 版本
4. 运行 `bundle update rails`
5. 更新 JavaScript 依赖（参见 JS 依赖章节）
6. **不要直接运行 `rails app:update`** - 使用下方的选择性合并流程
7. 运行数据库迁移
8. 运行测试套件
9. 审查并更新已弃用的代码

### 资源

- Rails 升级指南：https://guides.rubyonrails.org/upgrading_ruby_on_rails.html
- Rails Diff：https://railsdiff.org/{当前版本}/{目标版本}
- 发布说明：https://github.com/rails/rails/releases/tag/v{目标版本}

---


## 使用场景

分析 Rails 应用并提供升级评估报告

当处理分析 Rails 应用并提供升级评估报告的任务时使用此技能。

## 步骤 9：选择性文件更新（替代 `rails app:update`）

**重要：** 不要运行 `rails app:update`，因为它会覆盖文件而不考虑本地自定义。请改用以下选择性合并流程：

### 9.1：检测本地自定义

在任何升级前，识别有本地自定义的文件：

```bash
# 检查未提交的更改
git status

# 列出与全新 Rails 应用不同的配置文件
# 这些是我们需要小心处理的文件
git diff HEAD --name-only -- config/ bin/ public/
```

将文件归类为以下几类：
- **自定义配置文件**：包含项目特定设置的文件（i18n、mailer 等）
- **修改过的 bin 脚本**：包含自定义行为的脚本（如带 foreman 的 bin/dev 等）
- **标准文件**：未被自定义的文件

### 9.2：分析 Railsdiff 中的必需变更

根据步骤 6 的 railsdiff 输出，对每个变更文件分类：

| 分类 | 操作 | 示例 |
|------|------|------|
| **新文件** | 直接创建 | `config/initializers/new_framework_defaults_X_Y.rb` |
| **本地未修改** | 可安全覆盖 | `public/404.html`（如果未自定义） |
| **本地已自定义** | 需手动合并 | `config/application.rb`、`bin/dev` |
| **仅注释变更** | 通常可跳过 | 配置文件中的小幅注释更新 |

### 9.3：创建升级计划

向用户展示清晰的升级计划：

```
## 升级计划：Rails X.Y.Z → A.B.C

### 新文件（将创建）：
- config/initializers/new_framework_defaults_A_B.rb
- bin/ci（新的 CI 脚本）

### 可安全更新（无本地自定义）：
- public/400.html
- public/404.html
- public/500.html

### 需要手动合并（检测到本地自定义）：
- config/application.rb
  └─ 本地：i18n 配置
  └─ Rails：[如有新变更则描述]

- config/environments/development.rb
  └─ 本地：letter_opener mailer 配置
  └─ Rails：[描述新 Rails 变更]

- bin/dev
  └─ 本地：foreman + Procfile.dev 设置
  └─ Rails：已更改为简单 ruby 脚本

### 跳过（仅注释变更或无关变更）：
- config/puma.rb（仅注释变更）
```

### 9.4：执行升级计划

用户确认计划后：

#### 对于新文件：
使用 railsdiff 的内容或从全新 Rails 应用中提取，直接创建：

```bash
# 生成临时的全新 Rails 应用以提取新文件
cd /tmp && rails new rails_template --skip-git --skip-bundle
# 然后复制所需文件
```

或使用 Rails 生成器创建特定文件：
```bash
bin/rails app:update:configs  # 仅更新配置文件，仍需交互
```

#### 对于安全更新：
覆盖这些文件，因为它们没有本地自定义。

#### 对于手动合并：
对每个需要合并的文件，向用户展示：

1. **当前本地版本**（他们的自定义）
2. **新的 Rails 默认值**（来自 railsdiff）
3. **建议的合并版本**，其中：
   - 保留所有本地自定义
   - 仅添加必要的新 Rails 功能
   - 移除已弃用的设置

`config/application.rb` 的合并示例：
```ruby
# 保留本地自定义：
config.i18n.available_locales = [:de, :en]
config.i18n.default_locale = :de
config.i18n.fallbacks = [:en]

# 如需要，添加新的 Rails 8.1 设置：
# （通常不需要 — 新默认值通过 new_framework_defaults 文件提供）
```

### 9.5：处理 Active Storage 迁移

文件更新后，运行任何新的迁移：

```bash
bin/rails db:migrate
```

检查新增的迁移：
```bash
ls -la db/migrate/ | tail -10
```

### 9.6：验证升级

完成合并后：

1. 启动 Rails 服务器并检查错误：
   ```bash
   bin/dev  # 或 bin/rails server
   ```

2. 检查 Rails 控制台：
   ```bash
   bin/rails console
   ```

3. 运行测试套件：
   ```bash
   bin/rails test
   ```

4. 审查日志中的弃用警告

---

## 步骤 10：最终确定框架默认值

验证应用正常工作后：

1. 审查 `config/initializers/new_framework_defaults_X_Y.rb`
2. 逐个启用每个新默认值，每次启用后测试
3. 所有默认值启用并测试完成后，更新 `config/application.rb`：
   ```ruby
   config.load_defaults X.Y  # 更新为新版本
   ```
4. 删除 `new_framework_defaults_X_Y.rb` 文件

---


## 使用场景

分析 Rails 应用并提供升级评估报告

当处理分析 Rails 应用并提供升级评估报告的任务时使用此技能。

## 错误处理

- 如果 `gh` CLI 未认证，指导用户运行 `gh auth login`
- 如果 railsdiff.org 没有精确版本，尝试使用 major.minor.0 版本
- 如果应用已是最新版本，向用户表示祝贺并告知即将到来的发布
- 如果本地自定义可能丢失，务必先停下来向用户展示将被覆盖的内容，然后再继续

## 核心原则

1. **覆盖前务必检查** - 始终先检查本地自定义
2. **保留用户意图** - 本地自定义的存在是有原因的
3. **最小变更** - 仅添加新 Rails 版本必需的内容
4. **透明** - 在执行前向用户展示确切的变更内容
5. **可逆性** - 用户应能通过 `git checkout` 恢复

## 局限性
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
