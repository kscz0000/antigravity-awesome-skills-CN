---
name: expo-deployment
description: "将 Expo 应用部署到生产环境。触发词：Expo部署、Expo发布、应用商店提交、OTA更新、EAS Build、发布管理、生产构建、Expo deployment、deploy Expo"
risk: safe
source: "https://github.com/expo/skills/tree/main/plugins/expo-deployment"
date_added: "2026-02-27"
---

# Expo 部署

## 概述

将 Expo 应用部署到生产环境，包括应用商店发布和空中更新（OTA）。

## 何时使用此技能

当需要将 Expo 应用部署到生产环境时使用此技能。

在以下场景使用：
- 将 Expo 应用部署到生产环境
- 发布到应用商店（iOS App Store、Google Play）
- 设置空中更新（OTA）
- 配置生产构建设置
- 管理发布渠道和版本

## 说明

此技能提供部署 Expo 应用的指导：

1. **构建配置**：设置生产构建参数
2. **应用商店提交**：准备并提交到应用商店
3. **OTA 更新**：配置空中更新渠道
4. **发布管理**：管理版本和发布渠道
5. **生产优化**：为生产环境优化应用

## 部署工作流

### 部署前

1. 确保所有测试通过
2. 更新版本号
3. 配置生产环境变量
4. 审查并优化应用包体积
5. 在本地测试生产构建

### 应用商店部署

1. 构建生产二进制文件（iOS/Android）
2. 配置应用商店元数据
3. 提交到 App Store Connect / Google Play Console
4. 管理应用商店列表和截图
5. 处理应用审核流程

### OTA 更新

1. 配置更新渠道（production、staging 等）
2. 构建并发布更新
3. 管理灰度发布策略
4. 监控更新采纳率
5. 必要时执行回滚

## 最佳实践

- 使用 EAS Build 进行可靠的生产构建
- 在提交前测试生产构建
- 实施完善的错误追踪和分析
- 使用发布渠道进行分阶段灰度发布
- 保持应用商店元数据为最新
- 监控生产环境中的应用性能

## 资源

更多信息请参阅[源代码仓库](https://github.com/expo/skills/tree/main/plugins/expo-deployment)。

## 限制
- 仅当任务明确符合上述范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代方案。
- 如果缺少必要的输入、权限、安全边界或成功标准，请停下来请求澄清。
