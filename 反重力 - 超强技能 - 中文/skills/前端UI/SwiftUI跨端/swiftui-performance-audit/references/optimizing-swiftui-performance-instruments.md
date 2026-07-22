# 使用 Instruments 优化 SwiftUI 性能（摘要）

背景：WWDC 演讲，介绍 Instruments 26 中的新一代 SwiftUI Instrument 以及如何诊断 SwiftUI 特定的性能瓶颈。

## 核心要点

- 使用 SwiftUI 模板（SwiftUI instrument + Time Profiler + Hangs/Hitches）分析 SwiftUI 问题。
- 长视图 body 更新是常见瓶颈；使用"Long View Body Updates"识别耗时的 body。
- 在长更新上设置检查范围，与 Time Profiler 关联以找到昂贵的帧。
- 将工作移出 `body`：将格式化、排序、图片解码等昂贵工作移入缓存或预计算路径。
- 使用因果图（Cause & Effect Graph）诊断*为什么*发生更新；SwiftUI 是声明式的，回溯调用栈通常没有帮助。
- 避免触发大量更新的广泛依赖（如 `@Observable` 数组或全局环境读取）。
- 优先使用细粒度的视图模型和限定作用域的状态，使仅受影响的视图更新。
- 环境值更新检查仍有开销；避免将快速变化的值（计时器、几何数据）放入环境。
- 在功能开发过程中尽早并频繁地进行性能分析以捕获回归。

## 建议工作流程（精简版）

1. 使用 SwiftUI 模板在 Release 模式下录制 trace。
2. 检查"Long View Body Updates"和"Other Long Updates"。
3. 缩放到长更新，然后检查 Time Profiler 中的热点帧。
4. 通过将重逻辑移入预计算/缓存路径来修复慢 body 工作。
5. 使用因果图识别意外的更新扇出。
6. 重新录制并对比更新次数和卡顿频率。

## 演讲中的示例模式

- 在位置管理器中缓存格式化后的距离字符串，而非在 `body` 中计算。
- 用逐项视图模型替代对全局收藏数组的依赖，以减少更新扇出。
