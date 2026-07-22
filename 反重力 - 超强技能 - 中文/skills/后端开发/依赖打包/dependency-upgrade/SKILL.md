---
name: dependency-upgrade
description: "掌握主要依赖版本升级、兼容性分析、分阶段升级策略和全面测试方法。当用户要求'升级依赖'、'版本升级'、'依赖更新'、'处理依赖冲突'时使用。"
risk: critical
source: community
date_added: "2026-02-27"
---

# Dependency Upgrade

掌握主要依赖版本升级、兼容性分析、分阶段升级策略和全面测试方法。

## 不适用场景

- 任务与依赖升级无关
- 需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束条件和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可执行的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 适用场景

- 升级主要框架版本
- 更新存在安全漏洞的依赖
- 现代化遗留依赖
- 解决依赖冲突
- 规划增量升级路径
- 测试兼容性矩阵
- 自动化依赖更新

## 语义版本控制回顾

```
MAJOR.MINOR.PATCH (例如: 2.3.1)

MAJOR: 破坏性变更
MINOR: 新功能，向后兼容
PATCH: Bug修复，向后兼容

^2.3.1 = >=2.3.1 <3.0.0 (次版本更新)
~2.3.1 = >=2.3.1 <2.4.0 (补丁更新)
2.3.1 = 精确版本
```

## 依赖分析

### 审计依赖
```bash
# npm
npm outdated
npm audit
npm audit fix

# yarn
yarn outdated
yarn audit

# 检查主要更新
npx npm-check-updates
npx npm-check-updates -u  # 更新 package.json
```

### 分析依赖树
```bash
# 查看包为何被安装
npm ls package-name
yarn why package-name

# 查找重复包
npm dedupe
yarn dedupe

# 可视化依赖
npx madge --image graph.png src/
```

## 兼容性矩阵

```javascript
// compatibility-matrix.js
const compatibilityMatrix = {
  'react': {
    '16.x': {
      'react-dom': '^16.0.0',
      'react-router-dom': '^5.0.0',
      '@testing-library/react': '^11.0.0'
    },
    '17.x': {
      'react-dom': '^17.0.0',
      'react-router-dom': '^5.0.0 || ^6.0.0',
      '@testing-library/react': '^12.0.0'
    },
    '18.x': {
      'react-dom': '^18.0.0',
      'react-router-dom': '^6.0.0',
      '@testing-library/react': '^13.0.0'
    }
  }
};

function checkCompatibility(packages) {
  // 根据矩阵验证包版本
}
```

## 分阶段升级策略

### 阶段1：规划
```bash
# 1. 确认当前版本
npm list --depth=0

# 2. 检查破坏性变更
# 阅读 CHANGELOG.md 和 MIGRATION.md

# 3. 创建升级计划
echo "Upgrade order:
1. TypeScript
2. React
3. React Router
4. Testing libraries
5. Build tools" > UPGRADE_PLAN.md
```

### 阶段2：增量更新
```bash
# 不要一次性升级所有内容！

# 步骤1：更新 TypeScript
npm install typescript@latest

# 测试
npm run test
npm run build

# 步骤2：更新 React（一次升级一个主版本）
npm install react@17 react-dom@17

# 再次测试
npm run test

# 步骤3：继续其他包
npm install react-router-dom@6

# 以此类推...
```

### 阶段3：验证
```javascript
// tests/compatibility.test.js
describe('Dependency Compatibility', () => {
  it('should have compatible React versions', () => {
    const reactVersion = require('react/package.json').version;
    const reactDomVersion = require('react-dom/package.json').version;

    expect(reactVersion).toBe(reactDomVersion);
  });

  it('should not have peer dependency warnings', () => {
    // 运行 npm ls 并检查警告
  });
});
```

## 破坏性变更处理

### 识别破坏性变更
```bash
# 使用 changelog 解析器
npx changelog-parser react 16.0.0 17.0.0

# 或手动检查
curl https://raw.githubusercontent.com/facebook/react/main/CHANGELOG.md
```

### 使用 Codemod 自动修复
```bash
# React 升级 codemods
npx react-codeshift <transform> <path>

# 示例：更新生命周期方法
npx react-codeshift \
  --parser tsx \
  --transform react-codeshift/transforms/rename-unsafe-lifecycles.js \
  src/
```

### 自定义迁移脚本
```javascript
// migration-script.js
const fs = require('fs');
const glob = require('glob');

glob('src/**/*.tsx', (err, files) => {
  files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');

    // 将旧 API 替换为新 API
    content = content.replace(
      /componentWillMount/g,
      'UNSAFE_componentWillMount'
    );

    // 更新导入
    content = content.replace(
      /import { Component } from 'react'/g,
      "import React, { Component } from 'react'"
    );

    fs.writeFileSync(file, content);
  });
});
```

## 测试策略

### 单元测试
```javascript
// 确保升级前后测试都通过
npm run test

// 如需要，更新测试工具
npm install @testing-library/react@latest
```

### 集成测试
```javascript
// tests/integration/app.test.js
describe('App Integration', () => {
  it('should render without crashing', () => {
    render(<App />);
  });

  it('should handle navigation', () => {
    const { getByText } = render(<App />);
    fireEvent.click(getByText('Navigate'));
    expect(screen.getByText('New Page')).toBeInTheDocument();
  });
});
```

### 视觉回归测试
```javascript
// visual-regression.test.js
describe('Visual Regression', () => {
  it('should match snapshot', () => {
    const { container } = render(<App />);
    expect(container.firstChild).toMatchSnapshot();
  });
});
```

### E2E 测试
```javascript
// cypress/e2e/app.cy.js
describe('E2E Tests', () => {
  it('should complete user flow', () => {
    cy.visit('/');
    cy.get('[data-testid="login"]').click();
    cy.get('input[name="email"]').type('user@example.com');
    cy.get('button[type="submit"]').click();
    cy.url().should('include', '/dashboard');
  });
});
```

## 自动化依赖更新

### Renovate 配置
```json
// renovate.json
{
  "extends": ["config:base"],
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "labels": ["major-update"]
    }
  ],
  "schedule": ["before 3am on Monday"],
  "timezone": "America/New_York"
}
```

### Dependabot 配置
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    reviewers:
      - "team-leads"
    commit-message:
      prefix: "chore"
      include: "scope"
```

## 回滚计划

```javascript
// rollback.sh
#!/bin/bash

# 保存当前状态
git stash
git checkout -b upgrade-branch

# 尝试升级
npm install package@latest

# 运行测试
if npm run test; then
  echo "Upgrade successful"
  git add package.json package-lock.json
  git commit -m "chore: upgrade package"
else
  echo "Upgrade failed, rolling back"
  git checkout main
  git branch -D upgrade-branch
  npm install  # 从 package-lock.json 恢复
fi
```

## 常见升级模式

### 锁文件管理
```bash
# npm
npm install --package-lock-only  # 仅更新锁文件
npm ci  # 从锁文件干净安装

# yarn
yarn install --frozen-lockfile  # CI 模式
yarn upgrade-interactive  # 交互式升级
```

### Peer Dependency 解决方案
```bash
# npm 7+: 严格的 peer dependencies
npm install --legacy-peer-deps  # 忽略 peer deps

# npm 8+: 覆盖 peer dependencies
npm install --force
```

### Workspace 升级
```bash
# 更新所有 workspace 包
npm install --workspaces

# 更新特定 workspace
npm install package@latest --workspace=packages/app
```

## 资源

- **references/semver.md**: 语义版本控制指南
- **references/compatibility-matrix.md**: 常见兼容性问题
- **references/staged-upgrades.md**: 增量升级策略
- **references/testing-strategy.md**: 全面测试方法
- **assets/upgrade-checklist.md**: 逐步检查清单
- **assets/compatibility-matrix.csv**: 版本兼容性表
- **scripts/audit-dependencies.sh**: 依赖审计脚本

## 最佳实践

1. **阅读 Changelog**：理解变更内容
2. **增量升级**：一次升级一个主版本
3. **充分测试**：单元测试、集成测试、E2E测试
4. **检查 Peer Dependencies**：尽早解决冲突
5. **使用锁文件**：确保可复现安装
6. **自动化更新**：使用 Renovate 或 Dependabot
7. **监控**：关注升级后的运行时错误
8. **文档记录**：保留升级笔记

## 升级检查清单

```markdown
升级前：
- [ ] 检查当前依赖版本
- [ ] 阅读 changelog 了解破坏性变更
- [ ] 创建功能分支
- [ ] 备份当前状态（git tag）
- [ ] 运行完整测试套件（基线）

升级中：
- [ ] 一次升级一个依赖
- [ ] 更新 peer dependencies
- [ ] 修复 TypeScript 错误
- [ ] 如需要，更新测试
- [ ] 每次升级后运行测试套件
- [ ] 检查打包体积影响

升级后：
- [ ] 完整回归测试
- [ ] 性能测试
- [ ] 更新文档
- [ ] 部署到预发布环境
- [ ] 监控错误
- [ ] 部署到生产环境
```

## 常见陷阱

- 一次性升级所有依赖
- 每次升级后不测试
- 忽略 peer dependency 警告
- 忘记更新锁文件
- 不阅读破坏性变更说明
- 跳过主版本
- 没有回滚计划

## 局限性
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
