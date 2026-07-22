# SwiftUI API 扫描清单

通过 Sosumi MCP 扫描的 API 区域分类清单。每个分类包含：要运行的搜索查询、要抓取的文档路径、以及要查看的 WWDC 会议。

随着 Apple 引入新 API，请新增分类或路径。

---

## 导航

**搜索查询：**
- `SwiftUI NavigationStack`
- `SwiftUI NavigationSplitView`
- `SwiftUI navigationTitle`
- `SwiftUI toolbar`
- `SwiftUI NavigationLink deprecated`

**文档路径：**
- `/documentation/swiftui/navigationstack`
- `/documentation/swiftui/navigationsplitview`
- `/documentation/swiftui/navigationlink`
- `/documentation/swiftui/view/navigationtitle(_:)-avgj`
- `/documentation/swiftui/view/toolbar(content:)-5w0tj`
- `/documentation/swiftui/view/toolbarvisibility(_:for:)`

---

## 外观与样式

**搜索查询：**
- `SwiftUI foregroundStyle`
- `SwiftUI foregroundColor deprecated`
- `SwiftUI tint modifier`
- `SwiftUI preferredColorScheme`
- `SwiftUI clipShape`

**文档路径：**
- `/documentation/swiftui/view/foregroundstyle(_:)`
- `/documentation/swiftui/view/foregroundcolor(_:)`
- `/documentation/swiftui/view/tint(_:)-93mfq`
- `/documentation/swiftui/view/preferredcolorscheme(_:)`
- `/documentation/swiftui/view/clipshape(_:style:)`

---

## 状态管理

**搜索查询：**
- `SwiftUI Observable macro`
- `SwiftUI ObservableObject deprecated`
- `SwiftUI Bindable`
- `SwiftUI State`
- `SwiftUI Entry macro`

**文档路径：**
- `/documentation/observation/observable()`
- `/documentation/swiftui/observableobject`
- `/documentation/swiftui/bindable`
- `/documentation/swiftui/state`
- `/documentation/swiftui/entry()`
- `/documentation/swiftui/environmentvalues`

---

## 展示与弹窗

**搜索查询：**
- `SwiftUI alert modifier`
- `SwiftUI confirmationDialog`
- `SwiftUI actionSheet deprecated`
- `SwiftUI sheet modifier`
- `SwiftUI fullScreenCover`

**文档路径：**
- `/documentation/swiftui/view/alert(_:ispresented:actions:message:)-8dvt8`
- `/documentation/swiftui/view/confirmationdialog(_:ispresented:titlevisibility:actions:message:)-43f72`
- `/documentation/swiftui/view/sheet(ispresented:ondismiss:content:)`

---

## 文本输入

**搜索查询：**
- `SwiftUI TextField onSubmit`
- `SwiftUI textInputAutocapitalization`
- `SwiftUI autocorrectionDisabled`
- `SwiftUI focused modifier`

**文档路径：**
- `/documentation/swiftui/view/onsubmit(of:_:)`
- `/documentation/swiftui/view/textinputautocapitalization(_:)`
- `/documentation/swiftui/view/autocorrectiondisabled(_:)`
- `/documentation/swiftui/focusstate`

---

## 布局

**搜索查询：**
- `SwiftUI ignoresSafeArea`
- `SwiftUI containerRelativeFrame`
- `SwiftUI visualEffect`
- `SwiftUI GeometryReader`
- `SwiftUI coordinateSpace`

**文档路径：**
- `/documentation/swiftui/view/ignoressafearea(_:edges:)`
- `/documentation/swiftui/view/containerrelativeframe(_:alignment:_:)`
- `/documentation/swiftui/view/visualeffect(_:)`
- `/documentation/swiftui/geometryreader`
- `/documentation/swiftui/view/coordinatespace(_:)`

---

## 手势

**搜索查询：**
- `SwiftUI MagnifyGesture`
- `SwiftUI RotateGesture`
- `SwiftUI MagnificationGesture deprecated`
- `SwiftUI RotationGesture deprecated`

**文档路径：**
- `/documentation/swiftui/magnifygesture`
- `/documentation/swiftui/rotategesture`
- `/documentation/swiftui/magnificationgesture`
- `/documentation/swiftui/rotationgesture`

---

## 无障碍

**搜索查询：**
- `SwiftUI accessibilityLabel`
- `SwiftUI accessibility deprecated`
- `SwiftUI accessibilityRepresentation`

**文档路径：**
- `/documentation/swiftui/view/accessibilitylabel(_:)-1d7jv`
- `/documentation/swiftui/view/accessibilityvalue(_:)-7a2ql`
- `/documentation/swiftui/view/accessibilityhint(_:)`
- `/documentation/swiftui/view/accessibilityrepresentation(representation:)`

---

## 动画

**搜索查询：**
- `SwiftUI animation value deprecated`
- `SwiftUI withAnimation`
- `SwiftUI phaseAnimator`
- `SwiftUI keyframeAnimator`

**文档路径：**
- `/documentation/swiftui/view/animation(_:value:)`
- `/documentation/swiftui/view/phaseanimator(_:content:animation:)`
- `/documentation/swiftui/view/keyframeanimator(initialvalue:repeating:content:keyframes:)`

---

## 标签页

**搜索查询：**
- `SwiftUI Tab API`
- `SwiftUI tabItem deprecated`
- `SwiftUI TabView`

**文档路径：**
- `/documentation/swiftui/tab`
- `/documentation/swiftui/tabview`
- `/documentation/swiftui/view/tabitem(_:)`

---

## 预览

**搜索查询：**
- `SwiftUI Previewable`
- `SwiftUI Preview macro`

**文档路径：**
- `/documentation/swiftui/previewable()`
- `/documentation/swiftui/preview(_:body:)`

---

## Liquid Glass（iOS 26+）

**搜索查询：**
- `SwiftUI glassEffect`
- `SwiftUI GlassEffectContainer`
- `SwiftUI glassProminent`
- `SwiftUI backgroundExtensionEffect`

**文档路径：**
- `/documentation/swiftui/view/glasseffect(_:in:isenabled:)`
- `/documentation/swiftui/glasseffectcontainer`
- `/documentation/swiftui/view/backgroundextensioneffect()`
- `/documentation/swiftui/view/scrolledgeeffectstyle(_:for:)`
- `/documentation/swiftui/view/tabbarminimizebehavior(_:)`

---

## 滚动与列表

**搜索查询：**
- `SwiftUI ScrollViewReader`
- `SwiftUI scrollPosition`
- `SwiftUI scrollTargetBehavior`
- `SwiftUI ForEach`

**文档路径：**
- `/documentation/swiftui/scrollviewreader`
- `/documentation/swiftui/view/scrollposition(id:)`
- `/documentation/swiftui/view/scrolltargetbehavior(_:)`
- `/documentation/swiftui/foreach`

---

## WWDC 会议

需关注的 "What's new in SwiftUI" 会议，用于查看 API 公告：

- `/videos/play/wwdc2024/10144` - What's new in SwiftUI (WWDC24)
- `/videos/play/wwdc2024/10145` - SwiftUI essentials (WWDC24)
- `/videos/play/wwdc2025/232` - What's new in SwiftUI (WWDC25)
- `/videos/play/wwdc2023/10148` - What's new in SwiftUI (WWDC23)
- `/videos/play/wwdc2022/10052` - What's new in SwiftUI (WWDC22)

当新一届 WWDC 召开时，请在此处添加最新的 "What's new in SwiftUI" 会议路径。