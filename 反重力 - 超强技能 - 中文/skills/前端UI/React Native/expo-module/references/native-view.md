# 原生视图参考

原生视图允许你将平台 UI 组件（iOS 上的 UIView、Android 上的 Android View）渲染为 React 组件。

## 定义一个视图

**Swift：**

```swift
public class MyViewModule: Module {
  public func definition() -> ModuleDefinition {
    Name("MyView")

    View(MyNativeView.self) {
      Prop("title") { (view: MyNativeView, title: String) in
        view.titleLabel.text = title
      }

      Events("onPress", "onLoad")

      AsyncFunction("reset") { (view: MyNativeView) in
        view.reset()
      }
    }
  }
}

class MyNativeView: ExpoView {
  let titleLabel = UILabel()

  required init(appContext: AppContext) {
    super.init(appContext: appContext)
    clipsToBounds = true
    addSubview(titleLabel)
  }

  override func layoutSubviews() {
    super.layoutSubviews()
    titleLabel.frame = bounds
  }
}
```

**Kotlin：**

```kotlin
class MyViewModule : Module() {
  override fun definition() = ModuleDefinition {
    Name("MyView")

    View(MyNativeView::class) {
      Prop("title") { view: MyNativeView, title: String ->
        view.titleView.text = title
      }

      Events("onPress", "onLoad")

      AsyncFunction("reset") { view: MyNativeView ->
        view.reset()
      }
    }
  }
}

class MyNativeView(context: Context, appContext: AppContext) : ExpoView(context, appContext) {
  val titleView = TextView(context).also {
    addView(it, LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT))
  }
}
```

**TypeScript：**

```typescript
import { requireNativeView } from "expo";

export type MyViewProps = {
  title?: string;
  onPress?: (event: { nativeEvent: { x: number; y: number } }) => void;
  onLoad?: () => void;
} & ViewProps;

const NativeView = requireNativeView<MyViewProps>("MyView");

export function MyView(props: MyViewProps) {
  return <NativeView {...props} />;
}
```

## 视图事件分发

**Swift：**

```swift
class MyNativeView: ExpoView {
  let onPress = EventDispatcher()

  func handleTap(at point: CGPoint) {
    onPress(["x": point.x, "y": point.y])
  }
}
```

**Kotlin：**

```kotlin
class MyNativeView(context: Context, appContext: AppContext) : ExpoView(context, appContext) {
  private val onPress by EventDispatcher()

  fun handleTap(x: Float, y: Float) {
    onPress(mapOf("x" to x, "y" to y))
  }
}
```

## 视图生命周期

```swift
// 在所有 props 被设置后调用
OnViewDidUpdateProps { (view: MyNativeView) in
  view.applyChanges()
}
```

```kotlin
// 仅 Android - 在视图不再使用时调用
OnViewDestroys { view: MyNativeView ->
  view.cleanup()
}
```

## 视图上的 AsyncFunction

在 `View` 内定义的函数可通过 React ref 访问：

```typescript
const ref = useRef<MyView>(null);
// 调用原生函数
await ref.current?.reset();
```

## PropGroup（Android）

使用共享的 setter 逻辑批量注册多个 prop：

```kotlin
View(MyNativeView::class) {
  PropGroup("border", "width" to Float::class, "color" to Int::class) { view, index, value ->
    when (index) {
      0 -> view.borderWidth = value as Float
      1 -> view.borderColor = value as Int
    }
  }
}
```

## GroupView（Android）

启用 view group 功能以管理子视图：

```kotlin
View(MyContainerView::class) {
  GroupView {
    AddChildView { parent, child, index -> parent.addView(child, index) }
    GetChildCount { parent -> parent.childCount }
    GetChildViewAt { parent, index -> parent.getChildAt(index) }
    RemoveChildView { parent, child -> parent.removeView(child) }
    RemoveChildViewAt { parent, index -> parent.removeViewAt(index) }
  }
}
```