---
name: new-rails-project
argument-hint: [project name]
description: 创建一个新的 Rails 项目。当用户要求创建新的 Rails 项目时使用。
allowed-tools: Bash(rails *), Bash(bundle *), Bash(bin/*), Bash(npm *), Bash(yarn *)
context: fork
risk: unknown
source: community
metadata:
  author: Shpigford
  version: "1.0"
---

在当前目录中生成一个名为 $1 的新 Rails 项目。你可以参考 @CLAUDE.md 获取通用指导，但本技能中的指导优先级更高。

## 何时使用
- 你需要使用本技能中定义的技术栈来引导一个新的 Rails 项目。
- 项目需要从一开始就规划好 Rails、PostgreSQL、Inertia.js、React、Vite、Tailwind、Sidekiq 和 Redis 的整体架构。
- 你需要涵盖项目创建、约定规范、测试和验证的完整设置指导。

# 技术栈
设置以下技术栈：
- **Rails ~8** with PostgreSQL - 服务端框架和数据库
- **Inertia.js ~2.3** - 连接 Rails 和 React，无需 API 即可实现类 SPA 体验
- **React ~19.2** - 前端 UI 框架
- **Vite ~5** - 支持 HMR 的 JavaScript 打包工具
- **Tailwind CSS ~4** - 工具优先的 CSS 框架
- **Sidekiq 8** - 后台任务处理，通过 sidekiq-scheduler 支持定时任务
- **Redis** - 会话管理、缓存和任务队列

# Rails 指导
- 不要使用 Kamal 或 Docker
- 不要使用 Rails 的 "solid_*" 组件/系统
- 开发环境应尽可能与生产环境配置保持一致
- 使用 Redis 作为缓存

# 数据库
- 所有表使用 UUID 主键（pgcrypto 扩展）
- 时间戳使用 `timestamptz` 以支持时区感知
- 使用 JSONB 列存储灵活的元数据
- 建立全面的索引策略以优化性能
- 敏感数据使用加密字段（OAuth tokens、API keys）

# 后台任务
- 使用 Sidekiq 8 配合 Redis

# 测试
- 始终使用 minitest
- 外部服务使用 `mocha` gem 和 VCR（仅在 providers 层）
- 优先使用 `OpenStruct` 作为 mock 实例
- 只 mock 必要的内容

# 代码维护
- 重要代码变更后运行 `bundle exec rubocop -a`
- 使用 `.rubocop.yml` 进行代码风格配置
- 使用 `bundle exec brakeman` 进行安全扫描

# 前端
- 所有 React 组件和视图应使用 TSX

# 通用指导
- 在规划阶段多提澄清性问题，越多越好。充分利用 AskUserQuestionTool 收集需求和规格说明。问题永远不会太多。

# 验证
通过运行 `bin/rails server` 并使用 playwright MCP 访问 `http://localhost:3000` 来验证项目模板是否正常工作。

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
