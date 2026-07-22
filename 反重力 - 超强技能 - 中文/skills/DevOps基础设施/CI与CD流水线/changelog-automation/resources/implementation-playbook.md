# 变更日志自动化实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

## 核心概念

### 1. Keep a Changelog 格式

```markdown
# Changelog

本文件记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)，
本项目遵循 [语义化版本](https://semver.org/spec/v2.0.0.html)。

## [Unreleased]

### Added
- 新功能 X

## [1.2.0] - 2024-01-15

### Added
- 用户头像功能
- 深色模式支持

### Changed
- 加载性能提升 40%

### Deprecated
- 旧版认证 API（请使用 v2）

### Removed
- 旧版支付网关

### Fixed
- 登录超时问题 (#123)

### Security
- 更新依赖以修复 CVE-2024-1234

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
```

### 2. 约定式提交（Conventional Commits）

```
<类型>[可选范围]: <描述>

[可选正文]

[可选页脚]
```

| 类型 | 描述 | 变更日志章节 |
|------|-------------|-------------------|
| `feat` | 新功能 | Added |
| `fix` | Bug 修复 | Fixed |
| `docs` | 文档 | （通常排除） |
| `style` | 格式 | （通常排除） |
| `refactor` | 代码重构 | Changed |
| `perf` | 性能优化 | Changed |
| `test` | 测试 | （通常排除） |
| `chore` | 维护 | （通常排除） |
| `ci` | CI 变更 | （通常排除） |
| `build` | 构建系统 | （通常排除） |
| `revert` | 回退提交 | Removed |

### 3. 语义化版本

```
主版本号.次版本号.修订号

主版本号：破坏性变更（feat! 或 BREAKING CHANGE）
次版本号：新功能（feat）
修订号：Bug 修复（fix）
```

## 实施方法

### 方法 1：Conventional Changelog（Node.js）

```bash
# 安装工具
npm install -D @commitlint/cli @commitlint/config-conventional
npm install -D husky
npm install -D standard-version
# 或
npm install -D semantic-release

# 设置 commitlint
cat > commitlint.config.js << 'EOF'
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'chore',
        'ci',
        'build',
        'revert',
      ],
    ],
    'subject-case': [2, 'never', ['start-case', 'pascal-case', 'upper-case']],
    'subject-max-length': [2, 'always', 72],
  },
};
EOF

# 设置 husky
npx husky init
echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg
```

### 方法 2：standard-version 配置

```javascript
// .versionrc.js
module.exports = {
  types: [
    { type: 'feat', section: 'Features' },
    { type: 'fix', section: 'Bug Fixes' },
    { type: 'perf', section: 'Performance Improvements' },
    { type: 'revert', section: 'Reverts' },
    { type: 'docs', section: 'Documentation', hidden: true },
    { type: 'style', section: 'Styles', hidden: true },
    { type: 'chore', section: 'Miscellaneous', hidden: true },
    { type: 'refactor', section: 'Code Refactoring', hidden: true },
    { type: 'test', section: 'Tests', hidden: true },
    { type: 'build', section: 'Build System', hidden: true },
    { type: 'ci', section: 'CI/CD', hidden: true },
  ],
  commitUrlFormat: '{{host}}/{{owner}}/{{repository}}/commit/{{hash}}',
  compareUrlFormat: '{{host}}/{{owner}}/{{repository}}/compare/{{previousTag}}...{{currentTag}}',
  issueUrlFormat: '{{host}}/{{owner}}/{{repository}}/issues/{{id}}',
  userUrlFormat: '{{host}}/{{user}}',
  releaseCommitMessageFormat: 'chore(release): {{currentTag}}',
  scripts: {
    prebump: 'echo "Running prebump"',
    postbump: 'echo "Running postbump"',
    prechangelog: 'echo "Running prechangelog"',
    postchangelog: 'echo "Running postchangelog"',
  },
};
```

```json
// package.json scripts
{
  "scripts": {
    "release": "standard-version",
    "release:minor": "standard-version --release-as minor",
    "release:major": "standard-version --release-as major",
    "release:patch": "standard-version --release-as patch",
    "release:dry": "standard-version --dry-run"
  }
}
```

### 方法 3：semantic-release（全自动化）

```javascript
// release.config.js
module.exports = {
  branches: [
    'main',
    { name: 'beta', prerelease: true },
    { name: 'alpha', prerelease: true },
  ],
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    [
      '@semantic-release/changelog',
      {
        changelogFile: 'CHANGELOG.md',
      },
    ],
    [
      '@semantic-release/npm',
      {
        npmPublish: true,
      },
    ],
    [
      '@semantic-release/github',
      {
        assets: ['dist/**/*.js', 'dist/**/*.css'],
      },
    ],
    [
      '@semantic-release/git',
      {
        assets: ['CHANGELOG.md', 'package.json'],
        message: 'chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}',
      },
    ],
  ],
};
```

### 方法 4：GitHub Actions 工作流

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      release_type:
        description: '发布类型'
        required: true
        default: 'patch'
        type: choice
        options:
          - patch
          - minor
          - major

permissions:
  contents: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: 配置 Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: 运行 semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
        run: npx semantic-release

  # 替代方案：使用 standard-version 手动发布
  manual-release:
    if: github.event_name == 'workflow_dispatch'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm ci

      - name: 配置 Git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

      - name: 更新版本并生成变更日志
        run: npx standard-version --release-as ${{ inputs.release_type }}

      - name: 推送变更
        run: git push --follow-tags origin main

      - name: 创建 GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          tag_name: ${{ steps.version.outputs.tag }}
          body_path: CHANGELOG.md
          generate_release_notes: true
```

### 方法 5：git-cliff（基于 Rust，快速）

```toml
# cliff.toml
[changelog]
header = """
# Changelog

本文件记录项目的所有重要变更。

"""
body = """
{% if version %}\
    ## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp | date(format="%Y-%m-%d") }}
{% else %}\
    ## [Unreleased]
{% endif %}\
{% for group, commits in commits | group_by(attribute="group") %}
    ### {{ group | upper_first }}
    {% for commit in commits %}
        - {% if commit.scope %}**{{ commit.scope }}:** {% endif %}\
            {{ commit.message | upper_first }}\
            {% if commit.github.pr_number %} ([#{{ commit.github.pr_number }}](https://github.com/owner/repo/pull/{{ commit.github.pr_number }})){% endif %}\
    {% endfor %}
{% endfor %}
"""
footer = """
{% for release in releases -%}
    {% if release.version -%}
        {% if release.previous.version -%}
            [{{ release.version | trim_start_matches(pat="v") }}]: \
                https://github.com/owner/repo/compare/{{ release.previous.version }}...{{ release.version }}
        {% endif -%}
    {% else -%}
        [unreleased]: https://github.com/owner/repo/compare/{{ release.previous.version }}...HEAD
    {% endif -%}
{% endfor %}
"""
trim = true

[git]
conventional_commits = true
filter_unconventional = true
split_commits = false
commit_parsers = [
    { message = "^feat", group = "Features" },
    { message = "^fix", group = "Bug Fixes" },
    { message = "^doc", group = "Documentation" },
    { message = "^perf", group = "Performance" },
    { message = "^refactor", group = "Refactoring" },
    { message = "^style", group = "Styling" },
    { message = "^test", group = "Testing" },
    { message = "^chore\\(release\\)", skip = true },
    { message = "^chore", group = "Miscellaneous" },
]
filter_commits = false
tag_pattern = "v[0-9]*"
skip_tags = ""
ignore_tags = ""
topo_order = false
sort_commits = "oldest"

[github]
owner = "owner"
repo = "repo"
```

```bash
# 生成变更日志
git cliff -o CHANGELOG.md

# 生成指定范围的变更日志
git cliff v1.0.0..v2.0.0 -o CHANGELOG.md

# 预览而不写入
git cliff --unreleased --dry-run
```

### 方法 6：Python（commitizen）

```toml
# pyproject.toml
[tool.commitizen]
name = "cz_conventional_commits"
version = "1.0.0"
version_files = [
    "pyproject.toml:version",
    "src/__init__.py:__version__",
]
tag_format = "v$version"
update_changelog_on_bump = true
changelog_incremental = true
changelog_start_rev = "v0.1.0"

[tool.commitizen.customize]
message_template = "{{change_type}}{% if scope %}({{scope}}){% endif %}: {{message}}"
schema = "<type>(<scope>): <subject>"
schema_pattern = "^(feat|fix|docs|style|refactor|perf|test|chore)(\\(\\w+\\))?:\\s.*"
bump_pattern = "^(feat|fix|perf|refactor)"
bump_map = {"feat" = "MINOR", "fix" = "PATCH", "perf" = "PATCH", "refactor" = "PATCH"}
```

```bash
# 安装
pip install commitizen

# 交互式创建提交
cz commit

# 更新版本并生成变更日志
cz bump --changelog

# 检查提交
cz check --rev-range HEAD~5..HEAD
```

## 发布说明模板

### GitHub Release 模板

```markdown
## 变更内容

### 🚀 新功能
{{ range .Features }}
- {{ .Title }} by @{{ .Author }} in #{{ .PR }}
{{ end }}

### 🐛 Bug 修复
{{ range .Fixes }}
- {{ .Title }} by @{{ .Author }} in #{{ .PR }}
{{ end }}

### 📚 文档
{{ range .Docs }}
- {{ .Title }} by @{{ .Author }} in #{{ .PR }}
{{ end }}

### 🔧 维护
{{ range .Chores }}
- {{ .Title }} by @{{ .Author }} in #{{ .PR }}
{{ end }}

## 新贡献者
{{ range .NewContributors }}
- @{{ .Username }} 在 #{{ .PR }} 完成了首次贡献
{{ end }}

**完整变更日志**: https://github.com/owner/repo/compare/v{{ .Previous }}...v{{ .Current }}
```

### 内部发布说明

```markdown
# 发布 v2.1.0 - 2024年1月15日

## 概述
本次发布引入深色模式支持，并将结账性能提升 40%。同时包含重要的安全更新。

## 亮点

### 🌙 深色模式
用户现在可以从设置中切换到深色模式。偏好设置会自动保存并在设备间同步。

### ⚡ 性能
- 结账流程提速 40%
- 包体积减少 15%

## 破坏性变更
本次发布无破坏性变更。

## 升级指南
无需特殊步骤。按标准部署流程执行即可。

## 已知问题
- 深色模式首次加载时可能出现闪烁（计划在 v2.1.1 修复）

## 依赖更新
| 包名 | 旧版本 | 新版本 | 原因 |
|---------|------|-----|--------|
| react | 18.2.0 | 18.3.0 | 性能改进 |
| lodash | 4.17.20 | 4.17.21 | 安全补丁 |
```

## 提交消息示例

```bash
# 带范围的功能
feat(auth): add OAuth2 support for Google login

# 带问题引用的 Bug 修复
fix(checkout): resolve race condition in payment processing

Closes #123

# 破坏性变更
feat(api)!: change user endpoint response format

BREAKING CHANGE: The user endpoint now returns `userId` instead of `id`.
Migration guide: Update all API consumers to use the new field name.

# 多段落提交
fix(database): handle connection timeouts gracefully

Previously, connection timeouts would cause the entire request to fail
without retry. This change implements exponential backoff with up to
3 retries before failing.

The timeout threshold has been increased from 5s to 10s based on p99
latency analysis.

Fixes #456
Reviewed-by: @alice
```

## 最佳实践

### 推荐做法
- **遵循约定式提交** - 启用自动化
- **编写清晰的消息** - 未来的你会感谢自己
- **引用问题** - 将提交与工单关联
- **一致使用范围** - 定义团队规范
- **自动化发布** - 减少人为错误

### 避免做法
- **不要混合变更** - 每个提交只做一件事
- **不要跳过验证** - 使用 commitlint
- **不要手动编辑** - 只使用生成的变更日志
- **不要遗漏破坏性变更** - 用 `!` 或页脚标记
- **不要忽略 CI** - 在流水线中验证提交

## 资源

- [Keep a Changelog](https://keepachangelog.com/)
- [约定式提交](https://www.conventionalcommits.org/)
- [语义化版本](https://semver.org/)
- [semantic-release](https://semantic-release.gitbook.io/)
- [git-cliff](https://git-cliff.org/)
