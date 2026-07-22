---
title: Install Native Dependencies in App Directory
impact: CRITICAL
impactDescription: 自动链接的必要条件
tags: monorepo, native, autolinking, installation
---

## 在应用目录中安装原生依赖

在单仓中，包含原生代码的包必须直接安装在原生应用的目录中。自动链接只扫描应用的 `node_modules`——它无法找到安装在其他包中的原生依赖。

**错误示例（原生依赖仅在共享包中）：**

```
packages/
  ui/
    package.json  # has react-native-reanimated
  app/
    package.json  # missing react-native-reanimated
```

自动链接失败——原生代码未被链接。

**正确示例（原生依赖在应用目录中）：**

```
packages/
  ui/
    package.json  # has react-native-reanimated
  app/
    package.json  # also has react-native-reanimated
```

```json
// packages/app/package.json
{
  "dependencies": {
    "react-native-reanimated": "3.16.1"
  }
}
```

即使共享包使用了原生依赖，应用也必须列出它，自动链接才能检测并链接原生代码。
