---
name: nx-workspace-patterns
description: "配置和优化 Nx monorepo 工作空间。当用户要求设置 Nx、配置项目边界、优化构建缓存或实现 affected 命令时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---

# Nx 工作空间模式

Nx monorepo 管理的生产级模式。

## 不要使用此技能的情况

- 任务与 nx 工作空间模式无关
- 你需要此范围之外的其他领域或工具

## 使用说明

- 明确目标、约束和所需输入。
- 应用相关最佳实践并验证结果。
- 提供可操作的步骤和验证方法。
- 如需详细示例，请打开 `resources/implementation-playbook.md`。

## 使用此技能的情况

- 设置新的 Nx 工作空间
- 配置项目边界
- 使用 affected 命令优化 CI
- 实现远程缓存
- 管理项目间的依赖关系
- 迁移到 Nx

## 核心概念

### 1. Nx 架构

```
workspace/
├── apps/              # Deployable applications
│   ├── web/
│   └── api/
├── libs/              # Shared libraries
│   ├── shared/
│   │   ├── ui/
│   │   └── utils/
│   └── feature/
│       ├── auth/
│       └── dashboard/
├── tools/             # Custom executors/generators
├── nx.json            # Nx configuration
└── workspace.json     # Project configuration
```

### 2. 库类型

| 类型 | 用途 | 示例 |
|------|------|------|
| **feature** | 智能组件、业务逻辑 | `feature-auth` |
| **ui** | 展示型组件 | `ui-buttons` |
| **data-access** | API 调用、状态管理 | `data-access-users` |
| **util** | 纯函数、工具函数 | `util-formatting` |
| **shell** | 应用引导 | `shell-web` |

## 模板

### 模板 1：nx.json 配置

```json
{
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "npmScope": "myorg",
  "affected": {
    "defaultBase": "main"
  },
  "tasksRunnerOptions": {
    "default": {
      "runner": "nx/tasks-runners/default",
      "options": {
        "cacheableOperations": [
          "build",
          "lint",
          "test",
          "e2e",
          "build-storybook"
        ],
        "parallel": 3
      }
    }
  },
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
    },
    "e2e": {
      "inputs": ["default", "^production"],
      "cache": true
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*", "sharedGlobals"],
    "production": [
      "default",
      "!{projectRoot}/**/?(*.)+(spec|test).[jt]s?(x)?(.snap)",
      "!{projectRoot}/tsconfig.spec.json",
      "!{projectRoot}/jest.config.[jt]s",
      "!{projectRoot}/.eslintrc.json"
    ],
    "sharedGlobals": [
      "{workspaceRoot}/babel.config.json",
      "{workspaceRoot}/tsconfig.base.json"
    ]
  },
  "generators": {
    "@nx/react": {
      "application": {
        "style": "css",
        "linter": "eslint",
        "bundler": "webpack"
      },
      "library": {
        "style": "css",
        "linter": "eslint"
      },
      "component": {
        "style": "css"
      }
    }
  }
}
```

### 模板 2：项目配置

```json
// apps/web/project.json
{
  "name": "web",
  "$schema": "../../node_modules/nx/schemas/project-schema.json",
  "sourceRoot": "apps/web/src",
  "projectType": "application",
  "tags": ["type:app", "scope:web"],
  "targets": {
    "build": {
      "executor": "@nx/webpack:webpack",
      "outputs": ["{options.outputPath}"],
      "defaultConfiguration": "production",
      "options": {
        "compiler": "babel",
        "outputPath": "dist/apps/web",
        "index": "apps/web/src/index.html",
        "main": "apps/web/src/main.tsx",
        "tsConfig": "apps/web/tsconfig.app.json",
        "assets": ["apps/web/src/assets"],
        "styles": ["apps/web/src/styles.css"]
      },
      "configurations": {
        "development": {
          "extractLicenses": false,
          "optimization": false,
          "sourceMap": true
        },
        "production": {
          "optimization": true,
          "outputHashing": "all",
          "sourceMap": false,
          "extractLicenses": true
        }
      }
    },
    "serve": {
      "executor": "@nx/webpack:dev-server",
      "defaultConfiguration": "development",
      "options": {
        "buildTarget": "web:build"
      },
      "configurations": {
        "development": {
          "buildTarget": "web:build:development"
        },
        "production": {
          "buildTarget": "web:build:production"
        }
      }
    },
    "test": {
      "executor": "@nx/jest:jest",
      "outputs": ["{workspaceRoot}/coverage/{projectRoot}"],
      "options": {
        "jestConfig": "apps/web/jest.config.ts",
        "passWithNoTests": true
      }
    },
    "lint": {
      "executor": "@nx/eslint:lint",
      "outputs": ["{options.outputFile}"],
      "options": {
        "lintFilePatterns": ["apps/web/**/*.{ts,tsx,js,jsx}"]
      }
    }
  }
}
```

### 模板 3：模块边界规则

```json
// .eslintrc.json
{
  "root": true,
  "ignorePatterns": ["**/*"],
  "plugins": ["@nx"],
  "overrides": [
    {
      "files": ["*.ts", "*.tsx", "*.js", "*.jsx"],
      "rules": {
        "@nx/enforce-module-boundaries": [
          "error",
          {
            "enforceBuildableLibDependency": true,
            "allow": [],
            "depConstraints": [
              {
                "sourceTag": "type:app",
                "onlyDependOnLibsWithTags": [
                  "type:feature",
                  "type:ui",
                  "type:data-access",
                  "type:util"
                ]
              },
              {
                "sourceTag": "type:feature",
                "onlyDependOnLibsWithTags": [
                  "type:ui",
                  "type:data-access",
                  "type:util"
                ]
              },
              {
                "sourceTag": "type:ui",
                "onlyDependOnLibsWithTags": ["type:ui", "type:util"]
              },
              {
                "sourceTag": "type:data-access",
                "onlyDependOnLibsWithTags": ["type:data-access", "type:util"]
              },
              {
                "sourceTag": "type:util",
                "onlyDependOnLibsWithTags": ["type:util"]
              },
              {
                "sourceTag": "scope:web",
                "onlyDependOnLibsWithTags": ["scope:web", "scope:shared"]
              },
              {
                "sourceTag": "scope:api",
                "onlyDependOnLibsWithTags": ["scope:api", "scope:shared"]
              },
              {
                "sourceTag": "scope:shared",
                "onlyDependOnLibsWithTags": ["scope:shared"]
              }
            ]
          }
        ]
      }
    }
  ]
}
```

### 模板 4：自定义 Generator

```typescript
// tools/generators/feature-lib/index.ts
import {
  Tree,
  formatFiles,
  generateFiles,
  joinPathFragments,
  names,
  readProjectConfiguration,
} from '@nx/devkit';
import { libraryGenerator } from '@nx/react';

interface FeatureLibraryGeneratorSchema {
  name: string;
  scope: string;
  directory?: string;
}

export default async function featureLibraryGenerator(
  tree: Tree,
  options: FeatureLibraryGeneratorSchema
) {
  const { name, scope, directory } = options;
  const projectDirectory = directory
    ? `${directory}/${name}`
    : `libs/${scope}/feature-${name}`;

  // Generate base library
  await libraryGenerator(tree, {
    name: `feature-${name}`,
    directory: projectDirectory,
    tags: `type:feature,scope:${scope}`,
    style: 'css',
    skipTsConfig: false,
    skipFormat: true,
    unitTestRunner: 'jest',
    linter: 'eslint',
  });

  // Add custom files
  const projectConfig = readProjectConfiguration(tree, `${scope}-feature-${name}`);
  const projectNames = names(name);

  generateFiles(
    tree,
    joinPathFragments(__dirname, 'files'),
    projectConfig.sourceRoot,
    {
      ...projectNames,
      scope,
      tmpl: '',
    }
  );

  await formatFiles(tree);
}
```

### 模板 5：使用 Affected 的 CI 配置

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  NX_CLOUD_ACCESS_TOKEN: ${{ secrets.NX_CLOUD_ACCESS_TOKEN }}

jobs:
  main:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Derive SHAs for affected commands
        uses: nrwl/nx-set-shas@v4

      - name: Run affected lint
        run: npx nx affected -t lint --parallel=3

      - name: Run affected test
        run: npx nx affected -t test --parallel=3 --configuration=ci

      - name: Run affected build
        run: npx nx affected -t build --parallel=3

      - name: Run affected e2e
        run: npx nx affected -t e2e --parallel=1
```

### 模板 6：远程缓存配置

```typescript
// nx.json with Nx Cloud
{
  "tasksRunnerOptions": {
    "default": {
      "runner": "nx-cloud",
      "options": {
        "cacheableOperations": ["build", "lint", "test", "e2e"],
        "accessToken": "your-nx-cloud-token",
        "parallel": 3,
        "cacheDirectory": ".nx/cache"
      }
    }
  },
  "nxCloudAccessToken": "your-nx-cloud-token"
}

// Self-hosted cache with S3
{
  "tasksRunnerOptions": {
    "default": {
      "runner": "@nx-aws-cache/nx-aws-cache",
      "options": {
        "cacheableOperations": ["build", "lint", "test"],
        "awsRegion": "us-east-1",
        "awsBucket": "my-nx-cache-bucket",
        "awsProfile": "default"
      }
    }
  }
}
```

## 常用命令

```bash
# Generate new library
nx g @nx/react:lib feature-auth --directory=libs/web --tags=type:feature,scope:web

# Run affected tests
nx affected -t test --base=main

# View dependency graph
nx graph

# Run specific project
nx build web --configuration=production

# Reset cache
nx reset

# Run migrations
nx migrate latest
nx migrate --run-migrations
```

## 最佳实践

### 推荐做法
- **始终使用标签** - 通过模块边界规则强制执行
- **尽早启用缓存** - 显著节省 CI 资源
- **保持库的专注性** - 单一职责原则
- **使用 generator** - 确保一致性
- **记录边界规则** - 帮助新开发者快速上手

### 避免做法
- **不要创建循环依赖** - 依赖图应为无环图
- **不要跳过 affected** - 只测试变更的部分
- **不要忽略边界规则** - 技术债务会不断累积
- **不要过度拆分** - 平衡库的数量

## 资源

- [Nx 文档](https://nx.dev/getting-started/intro)
- [模块边界](https://nx.dev/core-features/enforce-module-boundaries)
- [Nx Cloud](https://nx.app/)

## 限制
- 仅当任务明确匹配上述范围时才使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停下来请求澄清。
