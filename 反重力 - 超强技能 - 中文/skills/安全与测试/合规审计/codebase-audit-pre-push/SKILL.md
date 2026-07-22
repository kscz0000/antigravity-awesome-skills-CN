---
name: codebase-audit-pre-push
description: "GitHub 推送前的深度审计：清理垃圾文件、死代码、安全漏洞和优化问题。逐行检查每个文件的生产就绪状态。当用户要求'审计代码库'、'推送前审查'、'清理代码'或'优化一切'时使用。"
category: development
risk: safe
source: community
date_added: "2026-03-05"
---

# 推送前代码库审计

作为资深工程师，你正在进行代码推送到 GitHub 前的最终审查。仔细检查一切，发现问题立即修复。

## 何时使用此技能

- 用户请求"审计代码库"或"推送前审查"
- 首次推送到 GitHub 之前
- 公开仓库之前
- 生产部署前审查
- 用户要求"清理代码"或"优化一切"

## 你的职责

逐文件审查整个代码库。仔细阅读代码。立即修复问题。不要只记录问题——做出必要的修改。

## 审计流程

### 1. 清理垃圾文件

首先查找不应出现在 GitHub 上的文件：

**立即删除：**
- 系统文件：`.DS_Store`、`Thumbs.db`、`desktop.ini`
- 日志：`*.log`、`npm-debug.log*`、`yarn-error.log*`
- 临时文件：`*.tmp`、`*.temp`、`*.cache`、`*.swp`
- 构建产物：`dist/`、`build/`、`.next/`、`out/`、`.cache/`
- 依赖目录：`node_modules/`、`vendor/`、`__pycache__/`、`*.pyc`
- IDE 文件：`.idea/`、`.vscode/`（先询问用户）、`*.iml`、`.project`
- 备份文件：`*.bak`、`*_old.*`、`*_backup.*`、`*_copy.*`
- 测试产物：`coverage/`、`.nyc_output/`、`test-results/`
- 个人杂项：`TODO.txt`、`NOTES.txt`、`scratch.*`、`test123.*`

**关键——检查敏感信息：**
- `.env` 文件（绝不应提交）
- 包含以下内容的文件：`password`、`api_key`、`token`、`secret`、`private_key`
- `*.pem`、`*.key`、`*.cert`、`credentials.json`、`serviceAccountKey.json`

如果在代码中发现敏感信息，标记为严重阻塞问题。

### 2. 修复 .gitignore

检查 `.gitignore` 文件是否存在且完整。如果缺失或不完整，更新它以包含上述所有垃圾文件模式。确保 `.env.example` 存在，包含键名但不包含值。

### 3. 审计每个源文件

检查每个代码文件：

**死代码（立即删除）：**
- 注释掉的代码块
- 未使用的 import/require
- 未使用的变量（声明但从未使用）
- 未使用的函数（定义但从未调用）
- 不可达代码（`return` 之后、`if (false)` 内部）
- 重复逻辑（多处相同代码——合并）

**代码质量（边检查边修复）：**
- 模糊命名：`data`、`info`、`temp`、`thing` → 重命名为描述性名称
- 魔法数字：`if (status === 3)` → 提取为命名常量
- 调试语句：删除 `console.log`、`print()`、`debugger`
- TODO/FIXME 注释：要么解决，要么删除
- TypeScript `any`：添加正确类型或解释为何使用 `any`
- JavaScript 中使用 `===` 而非 `==`
- 超过 50 行的函数：考虑拆分
- 嵌套超过 3 层的代码：用提前返回重构

**逻辑问题（关键）：**
- 缺少 null/undefined 检查
- 对可能为空数组执行操作
- 未 await 的异步函数
- 没有 `.catch()` 或 try/catch 的 Promise
- 可能的无限循环
- switch 语句缺少 `default`

### 4. 安全检查（零容忍）

**敏感信息：** 搜索硬编码的密码、API 密钥和 token。它们必须放在环境变量中。

**注入漏洞：**
- SQL：查询中不要字符串拼接——只用参数化查询
- 命令注入：不要对用户输入使用 `exec()`
- 路径遍历：用户输入的文件路径必须验证
- XSS：用户数据不要用 `innerHTML` 或 `dangerouslySetInnerHTML`

**认证/授权：**
- 密码用 bcrypt/argon2 哈希（绝不用 MD5 或明文）
- 受保护路由检查认证状态
- 授权检查在服务端进行，而非仅在前端
- 无 IDOR：验证用户拥有其访问的资源

**数据泄露：**
- API 响应不泄露不必要信息
- 错误消息不暴露堆栈跟踪或数据库详情
- 列表端点有分页

**依赖：**
- 运行 `npm audit` 或等效工具
- 标记严重过时或有漏洞的包

### 5. 可扩展性检查

**数据库：**
- N+1 查询：循环内有数据库调用 → 使用 JOIN 或批量查询
- WHERE/ORDER BY 列缺少索引
- 无界查询：添加 LIMIT 或分页
- 避免 `SELECT *`：指定列名

**API 设计：**
- 重操作（如邮件、报告、文件处理）→ 移到后台队列
- 公开端点限流
- 频繁读取的数据缓存
- 外部调用设置超时

**代码：**
- 无全局可变状态
- 清理事件监听器（避免内存泄漏）
- 大文件用流处理，而非加载到内存

### 6. 架构检查

**组织结构：**
- 清晰的文件夹结构
- 文件位于合理位置
- 无 "misc" 或 "stuff" 文件夹

**关注点分离：**
- UI 层：只负责渲染
- 业务逻辑：纯函数
- 数据层：隔离数据库查询
- 无 500+ 行的"上帝文件"

**可复用性：**
- 重复代码 → 提取到共享工具
- 常量定义一次并导入
- 类型/接口复用，而非重复定义

### 7. 性能

**后端：**
- 耗时操作不阻塞请求
- 尽可能批量数据库调用
- 正确设置缓存头

**前端（如适用）：**
- 实现代码分割
- 优化图片
- 小工具避免大型依赖
- 重组件懒加载

### 8. 文档

**README.md 必须包含：**
- 项目功能描述
- 安装和运行说明
- 必需的环境变量
- 测试运行指南

**代码注释：**
- 解释为什么，而非是什么
- 复杂逻辑提供说明
- 避免仅重复代码的注释

### 9. 测试

- 关键路径应有测试（认证、支付、核心功能）
- 代码中不应保留 `test.only` 或 `fdescribe`
- 避免无解释的 `test.skip`
- 测试应验证行为，而非实现细节

### 10. 最终验证

完成所有修改后，运行应用。确保没有破坏任何东西。检查：
- 应用启动无错误
- 主要功能正常
- 测试通过（如存在）
- 未引入回归

## 输出格式

审计完成后，提供报告：

```
CODEBASE AUDIT COMPLETE

FILES REMOVED:
- node_modules/ (build artifact)
- .env (contained secrets)
- old_backup.js (unused duplicate)

CODE CHANGES:
[src/api/users.js]
  ✂ Removed unused import: lodash
  ✂ Removed dead function: formatOldWay()
  🔧 Renamed 'data' → 'userData' for clarity
  🛡 Added try/catch around API call (line 47)

[src/db/queries.js]
  ⚡ Fixed N+1 query: now uses JOIN instead of loop

SECURITY ISSUES:
🚨 CRITICAL: Hardcoded API key in config.js (line 12) → moved to .env
⚠️ HIGH: SQL injection risk in search.js (line 34) → fixed with parameterized query

SCALABILITY:
⚡ Added pagination to /api/users endpoint
⚡ Added index on users.email column

FINAL STATUS:
✅ CLEAN - Ready to push to GitHub

Scores:
Security: 9/10 (one minor header missing)
Code Quality: 10/10
Scalability: 9/10
Overall: 9/10
```

## 核心原则

- 仔细阅读代码，不要略读
- 立即修复问题，不要只记录
- 不确定是否删除时，询问用户
- 修改后测试
- 全面但务实——聚焦真正的问题
- 安全问题是阻塞项——有严重漏洞就不能发布

## 相关技能

- `@security-auditor` - 更深入的安全审查
- `@systematic-debugging` - 调查具体问题
- `@git-pushing` - 审计后推送代码

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 输出不能替代环境特定的验证、测试或专家审查。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停下来请求澄清。
