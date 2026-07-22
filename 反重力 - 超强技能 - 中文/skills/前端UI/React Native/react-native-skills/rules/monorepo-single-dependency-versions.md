---
title: Use Single Dependency Versions Across Monorepo
impact: MEDIUM
impactDescription: 避免重复打包和版本冲突
tags: monorepo, dependencies, installation
---

## 单仓中使用单一依赖版本

在单仓的所有包中使用每个依赖的单一版本。优先使用精确版本而非范围。多个版本会导致打包中重复代码、运行时冲突和包间行为不一致。

使用 syncpack 等工具强制执行。作为最后手段，使用 yarn resolutions 或 npm overrides。

**错误示例（版本范围，多个版本）：**

```json
// packages/app/package.json
{
  "dependencies": {
    "react-native-reanimated": "^3.0.0"
  }
}

// packages/ui/package.json
{
  "dependencies": {
    "react-native-reanimated": "^3.5.0"
  }
}
```

**正确示例（精确版本，单一来源）：**

```json
// package.json (root)
{
  "pnpm": {
    "overrides": {
      "react-native-reanimated": "3.16.1"
    }
  }
}

// packages/app/package.json
{
  "dependencies": {
    "react-native-reanimated": "3.16.1"
  }
}

// packages/ui/package.json
{
  "dependencies": {
    "react-native-reanimated": "3.16.1"
  }
}
```

使用包管理器的 override/resolution 功能在根级强制版本。添加依赖时，指定不带 `^` 或 `~` 的精确版本。
