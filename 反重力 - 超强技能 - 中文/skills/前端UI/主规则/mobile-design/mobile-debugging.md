# 移动端调试指南

> **停止用console.log()调试！**
> 移动应用有复杂的原生层。文本日志远远不够。
> **本文件教授有效的移动端调试策略。**

---

## 🧠 移动端调试思维

```
Web调试：           移动端调试：
┌──────────────┐    ┌──────────────┐
│  浏览器       │    │  JS桥接层    │
│  DevTools    │    │  原生UI      │
│  网络面板     │    │  GPU/内存    │
└──────────────┘    │  多线程      │
                    └──────────────┘
```

**关键区别：**
1. **原生层：** JS代码没问题，但应用崩溃？大概率是原生层（Java/Obj-C）。
2. **部署：** 不能简单"刷新"。状态会丢失或卡住。
3. **网络：** SSL Pinning、代理配置更复杂。
4. **设备日志：** `adb logcat` 和 `Console.app` 才是真相。

---

## 🚫 AI调试反模式

| ❌ 默认做法 | ✅ 移动端正确做法 |
|------------|-------------------|
| "加console.log" | 用Flipper / Reactotron |
| "看网络面板" | 用Charles Proxy / Proxyman |
| "模拟器上没问题" | **在真机上测试**（硬件相关bug） |
| "重装node_modules" | **清理原生构建**（Gradle/Pod缓存） |
| 忽略原生日志 | 读 `logcat` / Xcode日志 |

---

## 1. 工具集

### ⚡ React Native & Expo

| 工具 | 用途 | 最适合 |
|------|------|--------|
| **Reactotron** | 状态/API/Redux | JS侧调试 |
| **Flipper** | 布局/网络/数据库 | 原生 + JS桥接 |
| **Expo Tools** | 元素检查器 | 快速UI检查 |

### 🛠️ 原生层（深入调试）

| 工具 | 平台 | 命令 | 用途 |
|------|------|------|------|
| **Logcat** | Android | `adb logcat` | 原生崩溃、ANR |
| **Console** | iOS | 通过Xcode | 原生异常、内存 |
| **布局检查器** | Android | Android Studio | UI层级bug |
| **视图检查器** | iOS | Xcode | UI层级bug |

---

## 2. 常见调试工作流

### 🕵️ "应用刚崩了"（红屏 vs 退回桌面）

**场景A：红屏（JS错误）**
- **原因：** Undefined is not an object、import错误。
- **修复：** 读屏幕上的堆栈跟踪，通常很清晰。

**场景B：退回桌面（原生崩溃）**
- **原因：** 原生模块故障、内存OOM、使用了未声明的权限。
- **工具：**
    - **Android：** `adb logcat *:E`（过滤错误）
    - **iOS：** 打开Xcode → Window → Devices → View Device Logs

> **💡 专业提示：** 如果应用启动就崩，几乎100%是原生配置问题（Info.plist、AndroidManifest.xml）。

### 🌐 "API请求失败"（网络）

**Web：** 打开Chrome DevTools → 网络。
**移动端：** *通常不容易看到。*

**方案1：Reactotron/Flipper**
- 在监控应用中查看网络请求。

**方案2：代理（Charles/Proxyman）**
- **门槛高但强大。** 能看到所有流量，包括原生SDK的。
- 需要在设备上安装SSL证书。

### 🐢 "UI卡顿"（性能）

**不要猜。要测量。**
- **React Native：** 性能监视器（摇一摇菜单）。
- **Android：** 开发者选项中的"GPU渲染分析"。
- **问题：**
    - **JS帧率下降：** JS线程计算过重。
    - **UI帧率下降：** 视图太多、层级过深、图片过大。

---

## 3. 平台专属噩梦

### Android
- **Gradle同步失败：** 通常是Java版本不匹配或重复类。
- **模拟器网络：** 模拟器的 `localhost` 是 `10.0.2.2`，不是 `127.0.0.1`。
- **缓存构建：** `./gradlew clean` 是你最好的朋友。

### iOS
- **Pod问题：** `pod deintegrate && pod install`。
- **签名错误：** 检查Team ID和Bundle Identifier。
- **缓存：** Xcode → Product → Clean Build Folder。

---

## 📝 调试检查清单

- [ ] **是JS崩溃还是原生崩溃？**（红屏还是退回桌面？）
- [ ] **清理构建了吗？**（原生缓存很顽固）
- [ ] **在真机上测试了吗？**（模拟器隐藏并发bug）
- [ ] **检查了原生日志吗？**（不只是终端输出）

> **切记：** 如果JavaScript看起来完美但应用还是崩，仔细看看原生层。
