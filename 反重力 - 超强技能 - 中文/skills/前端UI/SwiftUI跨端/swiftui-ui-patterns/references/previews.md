# 预览

## 意图

使用预览来验证布局、状态连接和注入的依赖，无需依赖运行中的应用或实时服务。

## 核心规则

- 为主要状态以及重要的次要状态（加载中、空数据、错误）添加 `#Preview` 覆盖。
- 使用确定性的 fixtures、mock 和示例数据。不要让预览依赖实时网络调用、真实数据库或全局单例。
- 直接在预览中安装所需的环境依赖，使视图可以隔离渲染。
- 预览设置靠近视图放置，直到变得杂乱时再提取轻量级的预览助手或 fixtures。
- 如果预览崩溃，在扩展功能之前先修复状态初始化或依赖连接。

## 示例：简单预览状态

```swift
#Preview("Loaded") {
  ProfileView(profile: .fixture)
}

#Preview("Empty") {
  ProfileView(profile: nil)
}
```

## 示例：带注入依赖的预览

```swift
#Preview("Search results") {
  SearchView()
    .environment(SearchClient.preview(results: [.fixture, .fixture2]))
    .environment(Theme.preview)
}
```

## 预览检查清单

- 预览是否安装了所有必需的环境依赖？
- 是否覆盖了至少一个成功路径和一个非理想路径？
- fixtures 是否稳定且足够小，能快速阅读？
- 预览能否在无网络、无认证或无应用全局初始化的情况下渲染？

## 陷阱

- 如果生产视图需要某些依赖，不要通过将依赖设为可选来隐藏预览崩溃。
- 当命名示例更易读时，避免使用大量内联 fixtures。
- 除非项目没有替代方案，否则不要将预览耦合到全局共享单例。
