---
name: react-native-app
description: React Native 移动应用模板原则。Expo、TypeScript、导航。触发词：React Native、移动应用、Expo应用、RN项目
---
# React Native 应用模板

## 技术栈

| 组件 | 技术 |
|-----------|------------|
| 框架 | React Native + Expo |
| 语言 | TypeScript |
| 导航 | Expo Router |
| 状态 | Zustand + React Query |
| 样式 | NativeWind |
| 测试 | Jest + RNTL |

---

## 目录结构

```
project-name/
├── app/                 # Expo Router (基于文件)
│   ├── _layout.tsx      # 根布局
│   ├── index.tsx        # 首页
│   ├── (tabs)/          # Tab 导航
│   └── [id].tsx         # 动态路由
├── components/
│   ├── ui/              # 可复用组件
│   └── features/
├── hooks/
├── lib/
│   ├── api.ts
│   └── storage.ts
├── store/
├── constants/
└── app.json
```

---

## 导航模式

| 模式 | 用途 |
|---------|-----|
| Stack | 页面层级 |
| Tabs | 底部导航 |
| Drawer | 侧边菜单 |
| Modal | 覆盖层屏幕 |

---

## 状态管理

| 类型 | 工具 |
|------|------|
| 本地 | Zustand |
| 服务端 | React Query |
| 表单 | React Hook Form |
| 存储 | Expo SecureStore |

---

## 关键包

| 包 | 用途 |
|---------|---------|
| expo-router | 基于文件的路由 |
| zustand | 本地状态 |
| @tanstack/react-query | 服务端状态 |
| nativewind | Tailwind 样式 |
| expo-secure-store | 安全存储 |

---

## 设置步骤

1. `npx create-expo-app {{name}} -t expo-template-blank-typescript`
2. `npx expo install expo-router react-native-safe-area-context`
3. 安装状态管理: `npm install zustand @tanstack/react-query`
4. `npx expo start`

---

## 最佳实践

- Expo Router 用于导航
- Zustand 用于本地状态，React Query 用于服务端状态
- NativeWind 用于一致的样式
- Expo SecureStore 用于令牌存储
- 在 iOS 和 Android 上都要测试
