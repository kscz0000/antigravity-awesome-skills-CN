---
name: flutter-app
description: Flutter 移动应用模板原则。Riverpod、Go Router、整洁架构。触发词：Flutter应用、Flutter项目、Dart应用
---
# Flutter 应用模板

## 技术栈

| 组件 | 技术 |
|-----------|------------|
| 框架 | Flutter 3.x |
| 语言 | Dart 3.x |
| 状态 | Riverpod 2.0 |
| 导航 | Go Router |
| HTTP | Dio |
| 存储 | Hive |

---

## 目录结构

```
project_name/
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/
│   │   ├── constants/
│   │   ├── theme/
│   │   ├── router/
│   │   └── utils/
│   ├── features/
│   │   ├── auth/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   └── home/
│   ├── shared/
│   │   ├── widgets/
│   │   └── providers/
│   └── services/
│       ├── api/
│       └── storage/
├── test/
└── pubspec.yaml
```

---

## 架构层级

| 层级 | 内容 |
|-------|----------|
| Presentation | 屏幕、组件、Providers |
| Domain | 实体、用例 |
| Data | 仓库、模型 |

---

## 关键包

| 包 | 用途 |
|---------|---------|
| flutter_riverpod | 状态管理 |
| riverpod_annotation | 代码生成 |
| go_router | 导航 |
| dio | HTTP 客户端 |
| freezed | 不可变模型 |
| hive | 本地存储 |

---

## 设置步骤

1. `flutter create {{name}} --org com.{{bundle}}`
2. 更新 `pubspec.yaml`
3. `flutter pub get`
4. 运行代码生成: `dart run build_runner build`
5. `flutter run`

---

## 最佳实践

- 功能优先的文件夹结构
- Riverpod 用于状态，React Query 模式用于服务端状态
- Freezed 用于不可变数据类
- Go Router 用于声明式导航
- Material 3 主题
