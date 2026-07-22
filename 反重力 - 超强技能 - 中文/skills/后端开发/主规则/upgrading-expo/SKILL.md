---
name: upgrading-expo
description: "升级 Expo SDK 版本，处理破坏性变更、依赖和配置更新。触发词：升级Expo、Expo SDK升级、Expo版本迁移"
risk: safe
source: "https://github.com/expo/skills/tree/main/plugins/upgrading-expo"
date_added: "2026-02-27"
---

# 升级 Expo

## 概述

安全升级 Expo SDK 版本，处理破坏性变更、依赖更新和配置迁移。

## 使用场景

当需要升级 Expo SDK 版本时使用此技能。

适用场景：
- 升级到新版 Expo SDK
- 处理 SDK 版本间的破坏性变更
- 更新依赖以确保兼容性
- 将已废弃的 API 迁移到新版本
- 为新版 Expo 功能做准备

## 操作指南

本技能引导你完成 Expo SDK 版本升级：

1. **升级前规划**：查看发布说明和破坏性变更
2. **依赖更新**：更新软件包以适配 SDK
3. **配置迁移**：更新 app.json 和配置文件
4. **代码更新**：将已废弃的 API 迁移到新版本
5. **测试验证**：升级后验证应用功能

## 升级流程

### 1. 升级前检查清单

- 查看 Expo SDK 发布说明
- 识别影响应用的破坏性变更
- 检查第三方包的兼容性
- 备份当前项目状态
- 创建功能分支进行升级

### 2. 更新 Expo SDK

```bash
# Update Expo CLI
npm install -g expo-cli@latest

# Upgrade Expo SDK
npx expo install expo@latest

# Update all Expo packages
npx expo install --fix
```

### 3. 处理破坏性变更

- 查看破坏性变更的迁移指南
- 更新已废弃的 API 调用
- 按需修改配置文件
- 如有需要更新原生依赖
- 全面测试受影响的功能

### 4. 更新依赖

```bash
# Check for outdated packages
npx expo-doctor

# Update packages to compatible versions
npx expo install --fix

# Verify compatibility
npx expo-doctor
```

### 5. 测试验证

- 测试应用核心功能
- 验证原生模块正常工作
- 检查运行时错误
- 在 iOS 和 Android 上测试
- 验证应用商店构建正常

## 常见问题

### 依赖冲突

- Expo 包使用 `expo install` 代替 `npm install`
- 检查包与新版 SDK 的兼容性
- 解决 peer dependency 警告

### 配置变更

- 按新版 SDK 要求更新 `app.json`
- 迁移已废弃的配置选项
- 如有需要更新原生配置文件

### API 破坏性变更

- 查看 API 迁移指南
- 更新代码使用新 API
- 变更后测试受影响的功能

## 最佳实践

- 始终在功能分支中升级
- 合并前充分测试
- 仔细阅读发布说明
- 逐步更新依赖
- 保持 Expo CLI 为最新版
- 使用 `expo-doctor` 验证配置

## 参考资源

更多信息请参阅[源代码仓库](https://github.com/expo/skills/tree/main/plugins/upgrading-expo)。

## 限制条件

- 仅在任务明确匹配上述范围时使用此技能。
- 输出不能替代特定环境的验证、测试或专家审查。
- 如缺少必要输入、权限、安全边界或成功标准，请停下来请求澄清。
