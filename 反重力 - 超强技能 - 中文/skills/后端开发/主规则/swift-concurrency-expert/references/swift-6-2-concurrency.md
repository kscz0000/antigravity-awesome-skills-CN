## Swift 6.2 中的并发编程更新

并发编程很困难，因为在多个任务之间共享内存容易出错，导致不可预测的行为。

## 数据竞争安全

Swift 6 中的数据竞争安全在编译时防止这些错误，因此你可以编写并发代码而不用担心引入难以调试的运行时 bug。但在许多情况下，最自然的代码写法容易产生数据竞争，导致你必须处理编译器错误。一个具有可变状态的类，比如这个 `PhotoProcessor` 类，只要你不并发访问它就是安全的。

```swift
class PhotoProcessor {
  func extractSticker(data: Data, with id: String?) async -> Sticker? {     }
}

@MainActor
final class StickerModel {
  let photoProcessor = PhotoProcessor()

  func extractSticker(_ item: PhotosPickerItem) async throws -> Sticker? {
    guard let data = try await item.loadTransferable(type: Data.self) else {
      return nil
    }

    // 错误：发送 'self.photoProcessor' 有导致数据竞争的风险
    // 将主 actor 隔离的 'self.photoProcessor' 发送到非隔离实例方法 'extractSticker(data:with:)'
    // 有导致非隔离和主 actor 隔离使用之间数据竞争的风险
    return await photoProcessor.extractSticker(data: data, with: item.itemIdentifier)
  }
}
```

它有一个异步方法，通过计算给定图像数据的主体来提取 `Sticker`。但如果你尝试从主 actor 上的 UI 代码调用 `extractSticker`，你会得到一个调用有数据竞争风险的错误。这是因为语言中有几个地方会隐式地将工作卸载到后台，即使你从未需要代码并行运行。

Swift 6.2 改变了这一理念，默认保持单线程，直到你选择引入并发。

```swift
class PhotoProcessor {
  func extractSticker(data: Data, with id: String?) async -> Sticker? {     }
}

@MainActor
final class StickerModel {
  let photoProcessor = PhotoProcessor()

  func extractSticker(_ item: PhotosPickerItem) async throws -> Sticker? {
    guard let data = try await item.loadTransferable(type: Data.self) else {
      return nil
    }

    // 在 Swift 6.2 中不再是数据竞争错误，因为平易近人的并发和默认 actor 隔离
    return await photoProcessor.extractSticker(data: data, with: item.itemIdentifier)
  }
}
```

Swift 6.2 中的语言变更使最自然的代码默认就是数据竞争安全的。这提供了一条更平易近人的路径来在项目中引入并发。

当你选择引入并发是因为你想并行运行代码时，数据竞争安全会保护你。

首先，我们让在具有可变状态的类型上调用异步函数变得更容易。异步函数不再急切地卸载不绑定特定 actor 的工作，而是继续在调用它的 actor 上运行。这消除了数据竞争，因为传入异步函数的值永远不会被发送到 actor 之外。异步函数仍然可以在其实现中卸载工作，但调用方不必担心他们的可变状态。

接下来，我们让在主 actor 类型上实现一致性变得更容易。这里我有一个名为 `Exportable` 的协议，我正在尝试为我的主 actor `StickerModel` 类实现一致性。export 需求没有 actor 隔离，所以语言假设它可以从主 actor 之外调用，并阻止 `StickerModel` 在其实现中使用主 actor 状态。

```swift
protocol Exportable {
  func export()
}

extension StickerModel: Exportable { // 错误：'StickerModel' 对协议 'Exportable' 的一致性跨越到主 actor 隔离代码，可能导致数据竞争
  func export() {
    photoProcessor.exportAsPNG()
  }
}
```

Swift 6.2 支持这些一致性。需要主 actor 状态的一致性被称为*隔离一致性*。这是安全的，因为编译器确保主 actor 一致性只在主 actor 上使用。

```swift
// 隔离一致性

protocol Exportable {
  func export()
}

extension StickerModel: @MainActor Exportable {
  func export() {
    photoProcessor.exportAsPNG()
  }
}
```

我可以创建一个 `ImageExporter` 类型，将 `StickerModel` 添加到任何 `Exportable` 项的数组中，只要它留在主 actor 上。

```swift
 // 隔离一致性

@MainActor
struct ImageExporter {
  var items: [any Exportable]

  mutating func add(_ item: StickerModel) {
    items.append(item)
  }

  func exportAll() {
    for item in items {
      item.export()
    }
  }
}
```

但如果我允许 `ImageExporter` 从任何地方使用，编译器会阻止将 `StickerModel` 添加到数组中，因为从主 actor 之外对 `StickerModel` 调用 export 是不安全的。

```swift
// 隔离一致性

nonisolated
struct ImageExporter {
  var items: [any Exportable]

  mutating func add(_ item: StickerModel) {
    items.append(item) // 错误：'StickerModel' 对 'Exportable' 的主 actor 隔离一致性不能在非隔离上下文中使用
  }

  func exportAll() {
    for item in items {
      item.export()
    }
  }
}
```

有了隔离一致性，你只需在代码表明它并发使用一致性时才需要解决数据竞争安全问题。

## 全局状态

全局和静态变量容易产生数据竞争，因为它们允许从任何地方访问可变状态。

```swift
final class StickerLibrary {
  static let shared: StickerLibrary = .init() // 错误：静态属性 'shared' 不是并发安全的，因为非 'Sendable' 类型 'StickerLibrary' 可能有共享可变状态
}
```

保护全局状态最常见的方式是使用主 actor。

```swift
final class StickerLibrary {
  @MainActor
  static let shared: StickerLibrary = .init()
}
```

而且通常用主 actor 标注整个类来保护其所有可变状态，特别是在没有大量并发任务的项目中。

```swift
@MainActor
final class StickerLibrary {
  static let shared: StickerLibrary = .init()
}
```

你可以通过在项目中的所有内容上写 `@MainActor` 来建模一个完全单线程的程序。

```swift
@MainActor
final class StickerLibrary {
  static let shared: StickerLibrary = .init()
}

@MainActor
final class StickerModel {
  let photoProcessor: PhotoProcessor

  var selection: [PhotosPickerItem]
}

extension StickerModel: @MainActor Exportable {
  func export() {
    photoProcessor.exportAsPNG()
  }
}
```

为了更容易建模单线程代码，我们引入了一种默认推断主 actor 的模式。

```swift
// Swift 6.2 中默认推断主 actor 的模式

final class StickerLibrary {
  static let shared: StickerLibrary = .init()
}

final class StickerModel {
  let photoProcessor: PhotoProcessor

  var selection: [PhotosPickerItem]
}

extension StickerModel: Exportable {
  func export() {
    photoProcessor.exportAsPNG()
  }
}
```

这消除了关于不安全全局和静态变量、调用其他主 actor 函数（如 SDK 中的函数）等的数据竞争安全错误，因为主 actor 默认保护所有可变状态。它还减少了大部分单线程代码中的并发标注。这种模式适合大部分工作在主 actor 上、并发代码封装在特定类型或文件中的项目。它是可选启用的，推荐用于应用、脚本和其他可执行目标。

## 将工作卸载到后台

将工作卸载到后台对性能仍然很重要，比如在执行 CPU 密集型任务时保持应用响应。

让我们看看 `PhotoProcessor` 上 `extractSticker` 方法的实现。

```swift
// 显式卸载异步工作

class PhotoProcessor {
  var cachedStickers: [String: Sticker]

  func extractSticker(data: Data, with id: String) async -> Sticker {
      if let sticker = cachedStickers[id] {
        return sticker
      }

      let sticker = await Self.extractSubject(from: data)
      cachedStickers[id] = sticker
      return sticker
  }

  // 使用 @concurrent 属性卸载耗时的图像处理
  @concurrent
  static func extractSubject(from data: Data) async -> Sticker { }
}
```

它首先检查是否已经为图像提取了贴纸，以便可以立即返回缓存的贴纸。如果贴纸尚未缓存，它从图像数据中提取主体并创建新贴纸。`extractSubject` 方法执行耗时的图像处理，我不想让它阻塞主 actor 或任何其他 actor。

我可以使用 `@concurrent` 属性来卸载这项工作。`@concurrent` 确保函数始终在并发线程池上运行，释放 actor 以同时运行其他任务。

### 一个示例

假设你有一个名为 `process` 的函数，你想在后台线程上运行。要在后台线程上调用该函数，你需要：

- 确保结构体或类是 `nonisolated`
- 在你想在后台运行的函数上添加 `@concurrent` 属性
- 如果函数还不是异步的，添加关键字 `async`
- 然后在任何调用方添加关键字 `await`

像这样：

```swift
nonisolated struct PhotoProcessor {

    @concurrent
    func process(data: Data) async -> ProcessedPhoto? { ... }
}

// 调用方添加了 await
processedPhotos[item.id] = await PhotoProcessor().process(data: data)
```


## 总结

这些语言变更共同使并发更加平易近人。

你首先编写默认在主 actor 上运行的代码，这里没有数据竞争风险。当你开始使用异步函数时，这些函数在调用它们的地方运行。仍然没有数据竞争风险，因为你的所有代码仍然在主 actor 上运行。当你准备好拥抱并发以提高性能时，很容易将特定代码卸载到后台并行运行。

其中一些语言变更是可选启用的，因为它们需要项目进行变更才能采用。你可以在 Xcode 构建设置的 Swift Compiler - Concurrency 部分下找到并启用所有平易近人的并发语言变更。你也可以使用 SwiftSettings API 在 Swift 包清单文件中启用这些功能。

Swift 6.2 包含迁移工具来帮助你自动进行必要的代码变更。你可以在 swift.org/migration 了解更多关于迁移工具的信息。
