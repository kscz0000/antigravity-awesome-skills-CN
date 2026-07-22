---
name: cypress-skill
description: 用 JavaScript 或 TypeScript 生成生产级 Cypress 端到端测试和组件测试，支持本地执行和 TestMu AI 云端。用于编写 Cypress 测试、配置 Cypress、使用 cy 命令测试，或涉及 Cypress、cy.visit、cy.get、cy.intercept 等关键词时。触发词：Cypress、cy.visit、cy.get、cy.intercept、端到端测试、E2E、组件测试、TestMu、LambdaTest、云端测试。
risk: unknown
source: https://github.com/LambdaTest/agent-skills/tree/main/cypress-skill
source_repo: LambdaTest/agent-skills
source_type: community
date_added: 2026-07-01
license: MIT
license_source: https://github.com/LambdaTest/agent-skills/blob/main/LICENSE
---

# Cypress 自动化技能
## 适用场景

当你需要用 JavaScript 或 TypeScript 生成生产级 Cypress 端到端测试和组件测试、支持本地执行和 TestMu AI 云端时，使用本技能。当用户要求编写 Cypress 测试、配置 Cypress、使用 cy 命令测试，或提及 Cypress、cy.visit、cy.get、cy.intercept 等关键词时，同样适用。


你是一名资深 Cypress QA 自动化架构师。

## 步骤 1 —— 执行目标

```
用户说"test" / "automate"
│
├─ 提到"cloud"、"TestMu"、"LambdaTest"、"cross-browser"？
│  └─ 通过 cypress-cli 插件走 TestMu AI 云
│
├─ 提到"locally"、"open"、"headed"？
│  └─ 本地：npx cypress open
│
└─ 不明确？→ 默认本地，提示云端选项
```

## 步骤 2 —— 测试类型

| 信号 | 类型 | 配置 |
|--------|------|--------|
| "E2E"、"end-to-end"、页面 URL | E2E 测试 | `cypress/e2e/` |
| "component"、"React"、"Vue" | 组件测试 | `cypress/component/` |
| "API test"、"cy.request" | 通过 Cypress 做 API 测试 | `cypress/e2e/api/` |

## 核心模式

### 命令链式调用 —— 至关重要

```javascript
// ✅ Cypress 链式 —— 不用 await，不用 async
cy.visit('/login');
cy.get('#username').type('user@test.com');
cy.get('#password').type('password123');
cy.get('button[type="submit"]').click();
cy.url().should('include', '/dashboard');

// ❌ 严禁对 cy 命令使用 async/await
// ❌ 严禁把 cy.get() 赋值给变量延后使用
```

### 选择器优先级

```
1. cy.get('[data-cy="submit"]')     ← 最佳实践
2. cy.get('[data-testid="submit"]') ← 同样可用
3. cy.contains('Submit')            ← 基于文本
4. cy.get('#submit-btn')            ← ID
5. cy.get('.btn-primary')           ← 类名（脆弱）
```

### 反模式

| 不推荐 | 推荐 | 原因 |
|-----|------|-----|
| `cy.wait(5000)` | `cy.intercept()` + `cy.wait('@alias')` | 任意等待不靠谱 |
| `const el = cy.get()` | 直接链式调用 | Cypress 是异步的 |
| 对 cy 用 `async/await` | 必要时链式 `.then()` | 异步模型不同 |
| 测试第三方站点 | 改用 stub / mock | 脆弱且慢 |
| 单一 `beforeEach` 承担所有事 | 拆成多个聚焦的 spec | 隔离性更好 |

### 基础测试结构

```javascript
describe('Login', () => {
  beforeEach(() => {
    cy.visit('/login');
  });

  it('should login with valid credentials', () => {
    cy.get('[data-cy="username"]').type('user@test.com');
    cy.get('[data-cy="password"]').type('password123');
    cy.get('[data-cy="submit"]').click();
    cy.url().should('include', '/dashboard');
    cy.get('[data-cy="welcome"]').should('contain', 'Welcome');
  });

  it('should show error for invalid credentials', () => {
    cy.get('[data-cy="username"]').type('wrong@test.com');
    cy.get('[data-cy="password"]').type('wrong');
    cy.get('[data-cy="submit"]').click();
    cy.get('[data-cy="error"]').should('be.visible');
  });
});
```

### 网络拦截

```javascript
// Stub API 响应
cy.intercept('POST', '/api/login', {
  statusCode: 200,
  body: { token: 'fake-jwt', user: { name: 'Test User' } },
}).as('loginRequest');

cy.get('[data-cy="submit"]').click();
cy.wait('@loginRequest').its('request.body').should('deep.include', {
  email: 'user@test.com',
});

// 等待真实 API
cy.intercept('GET', '/api/dashboard').as('dashboardLoad');
cy.visit('/dashboard');
cy.wait('@dashboardLoad');
```

### 自定义命令

```javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('[data-cy="username"]').type(email);
    cy.get('[data-cy="password"]').type(password);
    cy.get('[data-cy="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});

// 在测试中使用
cy.login('user@test.com', 'password123');
```

### TestMu AI 云

```javascript
// cypress.config.js
module.exports = {
  e2e: {
    setupNodeEvents(on, config) {
      // LambdaTest 插件
    },
  },
};

// lambdatest-config.json
{
  "lambdatest_auth": {
    "username": "${LT_USERNAME}",
    "access_key": "${LT_ACCESS_KEY}"
  },
  "browsers": [
    { "browser": "Chrome", "platform": "Windows 11", "versions": ["latest"] },
    { "browser": "Firefox", "platform": "macOS Sequoia", "versions": ["latest"] }
  ],
  "run_settings": {
    "build_name": "Cypress Build",
    "parallels": 5,
    "specs": "cypress/e2e/**/*.cy.js"
  }
}
```

**在云端运行：**
```bash
npx lambdatest-cypress run
```

## 验证工作流

1. **不任意等待**：零 `cy.wait(数字)` —— 改用 intercept
2. **选择器**：优先使用 `data-cy` 属性
3. **不用 async/await**：保持纯 Cypress 链式调用
4. **断言**：使用 `.should()` 链，而不是手动判断
5. **隔离**：每个测试相互独立，鉴权使用 `cy.session()`

## 速查表

| 任务 | 命令 |
|------|---------|
| 打开交互模式 | `npx cypress open` |
| 无头运行 | `npx cypress run` |
| 运行指定 spec | `npx cypress run --spec "cypress/e2e/login.cy.js"` |
| 在指定浏览器运行 | `npx cypress run --browser chrome` |
| 组件测试 | `npx cypress run --component` |
| 环境变量 | `CYPRESS_BASE_URL=http://localhost:3000 npx cypress run` |
| Fixtures | `cy.fixture('users.json').then(data => ...)` |
| 文件上传 | `cy.get('input[type="file"]').selectFile('file.pdf')` |
| 视口 | `cy.viewport('iphone-x')` 或 `cy.viewport(1280, 720)` |
| 截图 | `cy.screenshot('login-page')` |

## 参考文件

| 文件 | 何时阅读 |
|------|-------------|
| `reference/cloud-integration.md` | LambdaTest Cypress CLI、并行、配置 |
| `reference/component-testing.md` | React/Vue/Angular 组件测试 |
| `reference/custom-commands.md` | 进阶命令、覆盖、TypeScript |
| `reference/debugging-flaky.md` | 可重试性、DOM 分离、竞态条件 |

## 进阶手册

如需生产级模式，参阅 `reference/playbook.md`：

| 章节 | 内容 |
|---------|--------------|
| §1 生产配置 | 多环境配置、setupNodeEvents |
| §2 用 cy.session() 做鉴权 | UI 登录、API 登录、校验 |
| §3 页面对象模式 | 流畅的页面类、barrel 导出 |
| §4 网络拦截 | mock、修改、延时、等待 API |
| §5 组件测试 | React/Vue 挂载、stub、变体 |
| §6 自定义命令 | TypeScript 声明、拖放 |
| §7 数据库重置与种子 | API 重置、Cypress 任务、Prisma |
| §8 时间控制 | cy.clock()、cy.tick() |
| §9 文件操作 | 上传、拖放、下载校验 |
| §10 iframe 与 Shadow DOM | 内容访问模式 |
| §11 无障碍 | cypress-axe、WCAG 审计 |
| §12 视觉回归 | Percy、cypress-image-snapshot |
| §13 CI/CD | GitHub Actions 矩阵 + Cypress Cloud 并行 |
| §14 调试表 | 11 个常见问题与修复 |
| §15 最佳实践 | 15 条生产清单 |

## 使用限制

- 仅当任务与上游源及本地项目上下文明确匹配时使用本技能。
- 在应用改动前，校验命令、生成的代码、依赖、凭据以及外部服务行为。
- 不要把示例当作环境专属测试、安全审查，或破坏性 / 高成本操作的批准。
