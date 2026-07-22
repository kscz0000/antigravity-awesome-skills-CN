# Monorepo 管理实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

# Monorepo 管理

构建高效、可扩展的 monorepo，实现跨包和应用的代码共享、统一工具链和原子变更。

## 使用此技能的场景

- 搭建新的 monorepo 项目
- 从多仓库迁移到 monorepo
- 优化构建和测试性能
- 管理共享依赖
- 实现代码共享策略
- 为 monorepo 配置 CI/CD
- 版本管理与包发布
- 排查 monorepo 特有问题

## 核心概念

### 1. 为什么选择 Monorepo？

**优势：**
- 共享代码和依赖
- 跨项目原子提交
- 统一的工具链和规范
- 更容易重构
- 简化依赖管理
- 更好的代码可见性

**挑战：**
- 大规模下的构建性能
- CI/CD 复杂度
- 访问控制
- Git 仓库体积过大

### 2. Monorepo 工具

**包管理器：**
- pnpm workspaces（推荐）
- npm workspaces
- Yarn workspaces

**构建系统：**
- Turborepo（大多数场景推荐）
- Nx（功能丰富，较复杂）
- Lerna（较旧，维护模式）

## Turborepo 配置

### 初始搭建

```bash
# Create new monorepo
npx create-turbo@latest my-monorepo
cd my-monorepo

# Structure:
# apps/
#   web/          - Next.js app
#   docs/         - Documentation site
# packages/
#   ui/           - Shared UI components
#   config/       - Shared configurations
#   tsconfig/     - Shared TypeScript configs
# turbo.json      - Turborepo configuration
# package.json    - Root package.json
```

### 配置

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "type-check": {
      "dependsOn": ["^build"],
      "outputs": []
    }
  }
}
```

```json
// package.json (root)
{
  "name": "my-monorepo",
  "private": true,
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "format": "prettier --write \"**/*.{ts,tsx,md}\"",
    "clean": "turbo run clean && rm -rf node_modules"
  },
  "devDependencies": {
    "turbo": "^1.10.0",
    "prettier": "^3.0.0",
    "typescript": "^5.0.0"
  },
  "packageManager": "pnpm@8.0.0"
}
```

### 包结构

```json
// packages/ui/package.json
{
  "name": "@repo/ui",
  "version": "0.0.0",
  "private": true,
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./button": {
      "import": "./dist/button.js",
      "types": "./dist/button.d.ts"
    }
  },
  "scripts": {
    "build": "tsup src/index.ts --format esm,cjs --dts",
    "dev": "tsup src/index.ts --format esm,cjs --dts --watch",
    "lint": "eslint src/",
    "type-check": "tsc --noEmit"
  },
  "devDependencies": {
    "@repo/tsconfig": "workspace:*",
    "tsup": "^7.0.0",
    "typescript": "^5.0.0"
  },
  "dependencies": {
    "react": "^18.2.0"
  }
}
```

## pnpm Workspaces

### 配置

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'tools/*'
```

```json
// .npmrc
# Hoist shared dependencies
shamefully-hoist=true

# Strict peer dependencies
auto-install-peers=true
strict-peer-dependencies=true

# Performance
store-dir=~/.pnpm-store
```

### 依赖管理

```bash
# Install dependency in specific package
pnpm add react --filter @repo/ui
pnpm add -D typescript --filter @repo/ui

# Install workspace dependency
pnpm add @repo/ui --filter web

# Install in all packages
pnpm add -D eslint -w

# Update all dependencies
pnpm update -r

# Remove dependency
pnpm remove react --filter @repo/ui
```

### 脚本

```bash
# Run script in specific package
pnpm --filter web dev
pnpm --filter @repo/ui build

# Run in all packages
pnpm -r build
pnpm -r test

# Run in parallel
pnpm -r --parallel dev

# Filter by pattern
pnpm --filter "@repo/*" build
pnpm --filter "...web" build  # Build web and dependencies
```

## Nx Monorepo

### 配置

```bash
# Create Nx monorepo
npx create-nx-workspace@latest my-org

# Generate applications
nx generate @nx/react:app my-app
nx generate @nx/next:app my-next-app

# Generate libraries
nx generate @nx/react:lib ui-components
nx generate @nx/js:lib utils
```

### 配置文件

```json
// nx.json
{
  "extends": "nx/presets/npm.json",
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["production", "^production"],
      "cache": true
    },
    "test": {
      "inputs": ["default", "^production", "{workspaceRoot}/jest.preset.js"],
      "cache": true
    },
    "lint": {
      "inputs": ["default", "{workspaceRoot}/.eslintrc.json"],
      "cache": true
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*", "sharedGlobals"],
    "production": [
      "default",
      "!{projectRoot}/**/?(*.)+(spec|test).[jt]s?(x)?(.snap)",
      "!{projectRoot}/tsconfig.spec.json"
    ],
    "sharedGlobals": []
  }
}
```

### 运行任务

```bash
# Run task for specific project
nx build my-app
nx test ui-components
nx lint utils

# Run for affected projects
nx affected:build
nx affected:test --base=main

# Visualize dependencies
nx graph

# Run in parallel
nx run-many --target=build --all --parallel=3
```

## 共享配置

### TypeScript 配置

```json
// packages/tsconfig/base.json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "incremental": true,
    "declaration": true
  },
  "exclude": ["node_modules"]
}

// packages/tsconfig/react.json
{
  "extends": "./base.json",
  "compilerOptions": {
    "jsx": "react-jsx",
    "lib": ["ES2022", "DOM", "DOM.Iterable"]
  }
}

// apps/web/tsconfig.json
{
  "extends": "@repo/tsconfig/react.json",
  "compilerOptions": {
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### ESLint 配置

```javascript
// packages/config/eslint-preset.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  plugins: ['@typescript-eslint', 'react', 'react-hooks'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
  rules: {
    '@typescript-eslint/no-unused-vars': 'error',
    'react/react-in-jsx-scope': 'off',
  },
};

// apps/web/.eslintrc.js
module.exports = {
  extends: ['@repo/config/eslint-preset'],
  rules: {
    // App-specific rules
  },
};
```

## 代码共享模式

### 模式 1：共享 UI 组件

```typescript
// packages/ui/src/button.tsx
import * as React from 'react';

export interface ButtonProps {
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
  onClick?: () => void;
}

export function Button({ variant = 'primary', children, onClick }: ButtonProps) {
  return (
    <button
      className={`btn btn-${variant}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

// packages/ui/src/index.ts
export { Button, type ButtonProps } from './button';
export { Input, type InputProps } from './input';

// apps/web/src/app.tsx
import { Button } from '@repo/ui';

export function App() {
  return <Button variant="primary">Click me</Button>;
}
```

### 模式 2：共享工具函数

```typescript
// packages/utils/src/string.ts
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function truncate(str: string, length: number): string {
  return str.length > length ? str.slice(0, length) + '...' : str;
}

// packages/utils/src/index.ts
export * from './string';
export * from './array';
export * from './date';

// Usage in apps
import { capitalize, truncate } from '@repo/utils';
```

### 模式 3：共享类型

```typescript
// packages/types/src/user.ts
export interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
}

export interface CreateUserInput {
  email: string;
  name: string;
  password: string;
}

// Used in both frontend and backend
import type { User, CreateUserInput } from '@repo/types';
```

## 构建优化

### Turborepo 缓存

```json
// turbo.json
{
  "pipeline": {
    "build": {
      // Build depends on dependencies being built first
      "dependsOn": ["^build"],

      // Cache these outputs
      "outputs": ["dist/**", ".next/**"],

      // Cache based on these inputs (default: all files)
      "inputs": ["src/**/*.tsx", "src/**/*.ts", "package.json"]
    },
    "test": {
      // Run tests in parallel, don't depend on build
      "cache": true,
      "outputs": ["coverage/**"]
    }
  }
}
```

### 远程缓存

```bash
# Turborepo Remote Cache (Vercel)
npx turbo login
npx turbo link

# Custom remote cache
# turbo.json
{
  "remoteCache": {
    "signature": true,
    "enabled": true
  }
}
```

## Monorepo 的 CI/CD

### GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # For Nx affected commands

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v3
        with:
          node-version: 18
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm turbo run build

      - name: Test
        run: pnpm turbo run test

      - name: Lint
        run: pnpm turbo run lint

      - name: Type check
        run: pnpm turbo run type-check
```

### 仅部署变更的应用

```yaml
# Deploy only changed apps
- name: Deploy affected apps
  run: |
    if pnpm nx affected:apps --base=origin/main --head=HEAD | grep -q "web"; then
      echo "Deploying web app"
      pnpm --filter web deploy
    fi
```

## 最佳实践

1. **统一版本管理**：锁定工作区内依赖版本
2. **共享配置**：集中管理 ESLint、TypeScript、Prettier 配置
3. **依赖图**：保持无环，避免循环依赖
4. **有效缓存**：正确配置 inputs/outputs
5. **类型安全**：前后端共享类型
6. **测试策略**：包内单元测试，应用内 E2E 测试
7. **文档**：每个包内提供 README
8. **发布策略**：使用 changesets 进行版本管理

## 常见陷阱

- **循环依赖**：A 依赖 B，B 又依赖 A
- **幽灵依赖**：使用了未在 package.json 中声明的依赖
- **缓存输入不正确**：Turborepo inputs 中遗漏文件
- **过度共享**：共享了本应分离的代码
- **共享不足**：跨包重复代码
- **大型 Monorepo**：缺少合适工具时构建变慢

## 包发布

```bash
# Using Changesets
pnpm add -Dw @changesets/cli
pnpm changeset init

# Create changeset
pnpm changeset

# Version packages
pnpm changeset version

# Publish
pnpm changeset publish
```

```yaml
# .github/workflows/release.yml
- name: Create Release Pull Request or Publish
  uses: changesets/action@v1
  with:
    publish: pnpm release
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## 资源

- **references/turborepo-guide.md**：Turborepo 完整文档
- **references/nx-guide.md**：Nx monorepo 模式
- **references/pnpm-workspaces.md**：pnpm workspace 功能
- **assets/monorepo-checklist.md**：搭建检查清单
- **assets/migration-guide.md**：多仓库到 monorepo 迁移指南
- **scripts/dependency-graph.ts**：可视化包依赖关系
