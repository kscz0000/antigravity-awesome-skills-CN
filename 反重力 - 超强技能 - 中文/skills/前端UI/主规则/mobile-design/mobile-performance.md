# 移动端性能参考

> 深入React Native和Flutter性能优化、60fps动画、内存管理和电池考量。
> **本文件覆盖AI生成代码失败率最高的领域。**

---

## 1. 移动端性能思维

### 为什么移动端性能不同

```
桌面端：                          移动端：
├── 电力无限                      ├── 电池有限
├── 内存充裕                      ├── 内存共享、受限
├── 网络稳定                      ├── 网络不稳定
├── CPU始终可用                   ├── CPU过热降频
└── 用户本来就期望快              └── 用户期望即时响应
```

### 性能预算概念

```
每帧必须在以下时间内完成：
├── 60fps → 每帧16.67ms
├── 120fps（ProMotion）→ 每帧8.33ms

代码超时则：
├── 掉帧 → 滚动/动画卡顿
├── 用户感觉"慢"或"坏了"
└── 他们会卸载你的应用
```

---

## 2. React Native性能

### 🚫 AI头号错误：列表用ScrollView

```javascript
// ❌ 绝不这样做 - AI最爱犯的错误
<ScrollView>
  {items.map(item => (
    <ItemComponent key={item.id} item={item} />
  ))}
</ScrollView>

// 为什么是灾难性的：
// ├── 立即渲染所有条目（1000条 = 1000次渲染）
// ├── 内存爆炸
// ├── 首次渲染耗时数秒
// └── 滚动变得卡顿

// ✅ 始终用FlatList
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={item => item.id}
/>
```

### FlatList优化检查清单

```javascript
// ✅ 正确：所有优化已应用

// 1. Memo化条目组件
const ListItem = React.memo(({ item }: { item: Item }) => {
  return (
    <Pressable style={styles.item}>
      <Text>{item.title}</Text>
    </Pressable>
  );
});

// 2. 用useCallback memo化renderItem
const renderItem = useCallback(
  ({ item }: { item: Item }) => <ListItem item={item} />,
  [] // 空依赖 = 永不重建
);

// 3. 稳定的keyExtractor（绝不用index！）
const keyExtractor = useCallback((item: Item) => item.id, []);

// 4. 固定高度条目提供getItemLayout
const getItemLayout = useCallback(
  (data: Item[] | null, index: number) => ({
    length: ITEM_HEIGHT, // 固定高度
    offset: ITEM_HEIGHT * index,
    index,
  }),
  []
);

// 5. 应用到FlatList
<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={keyExtractor}
  getItemLayout={getItemLayout}
  // 性能属性
  removeClippedSubviews={true} // Android：卸载屏外视图
  maxToRenderPerBatch={10} // 每批渲染条目数
  windowSize={5} // 渲染窗口（5 = 两侧各2屏）
  initialNumToRender={10} // 初始渲染条目数
  updateCellsBatchingPeriod={50} // 批处理延迟
/>
```

### 每项优化的意义

| 优化 | 防止什么 | 影响 |
|------|----------|------|
| `React.memo` | 父组件变更导致重渲染 | 🔴 关键 |
| `useCallback renderItem` | 每次渲染创建新函数 | 🔴 关键 |
| 稳定`keyExtractor` | 条目回收错误 | 🔴 关键 |
| `getItemLayout` | 异步布局计算 | 🟡 高 |
| `removeClippedSubviews` | 屏外视图内存 | 🟡 高 |
| `maxToRenderPerBatch` | 阻塞主线程 | 🟢 中 |
| `windowSize` | 内存使用 | 🟢 中 |

### FlashList：更好的选择

```javascript
// 考虑FlashList获得更好性能
import { FlashList } from "@shopify/flash-list";

<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={ITEM_HEIGHT}
  keyExtractor={keyExtractor}
/>

// 相比FlatList的优势：
// ├── 更快的回收
// ├── 更好的内存管理
// ├── 更简单的API
// └── 需要更少的优化属性
```

### 动画性能

```javascript
// ❌ JS驱动动画（阻塞JS线程）
Animated.timing(value, {
  toValue: 1,
  duration: 300,
  useNativeDriver: false, // 不好！
}).start();

// ✅ Native驱动动画（在UI线程运行）
Animated.timing(value, {
  toValue: 1,
  duration: 300,
  useNativeDriver: true, // 好！
}).start();

// Native驱动仅支持：
// ├── transform（translate、scale、rotate）
// └── opacity
// 
// 不支持：
// ├── width、height
// ├── backgroundColor
// ├── borderRadius变化
// └── margin、padding
```

### Reanimated处理复杂动画

```javascript
// Native驱动处理不了的动画，用Reanimated 3

import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';

const Component = () => {
  const offset = useSharedValue(0);

  const animatedStyles = useAnimatedStyle(() => ({
    transform: [{ translateX: withSpring(offset.value) }],
  }));

  return <Animated.View style={animatedStyles} />;
};

// 优势：
// ├── 在UI线程运行（保证60fps）
// ├── 可动画任何属性
// ├── 手势驱动动画
// └── Worklet处理复杂逻辑
```

### 内存泄漏预防

```javascript
// ❌ 内存泄漏：未清理的interval
useEffect(() => {
  const interval = setInterval(() => {
    fetchData();
  }, 5000);
  // 缺少清理！
}, []);

// ✅ 正确清理
useEffect(() => {
  const interval = setInterval(() => {
    fetchData();
  }, 5000);
  
  return () => clearInterval(interval); // 清理！
}, []);

// 常见内存泄漏来源：
// ├── 定时器（setInterval、setTimeout）
// ├── 事件监听器
// ├── 订阅（WebSocket、PubSub）
// ├── 卸载后仍更新state的异步操作
// └── 无限制的图片缓存
```

### React Native性能检查清单

```markdown
## 每个列表前
- [ ] 使用FlatList或FlashList（不是ScrollView）
- [ ] renderItem已用useCallback memo化
- [ ] 列表条目已用React.memo包裹
- [ ] keyExtractor使用稳定ID（不是index）
- [ ] 已提供getItemLayout（固定高度时）

## 每个动画前
- [ ] useNativeDriver: true（如果可能）
- [ ] 复杂动画使用Reanimated
- [ ] 仅动画transform/opacity
- [ ] 在低端Android设备上测试

## 每次发布前
- [ ] console.log语句已移除
- [ ] 所有useEffect有清理函数
- [ ] 无内存泄漏（用profiler测试）
- [ ] 在release构建中测试（非dev）
```

---

## 3. Flutter性能

### 🚫 AI头号错误：setState滥用

```dart
// ❌ 错误：setState重建整个widget树
class BadCounter extends StatefulWidget {
  @override
  State<BadCounter> createState() => _BadCounterState();
}

class _BadCounterState extends State<BadCounter> {
  int _counter = 0;
  
  void _increment() {
    setState(() {
      _counter++; // 这会重建下面所有内容！
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Counter: $_counter'),
        ExpensiveWidget(), // 不必要地重建！
        AnotherExpensiveWidget(), // 不必要地重建！
      ],
    );
  }
}
```

### `const`构造函数革命

```dart
// ✅ 正确：const阻止重建

class GoodCounter extends StatefulWidget {
  const GoodCounter({super.key}); // CONST构造函数！
  
  @override
  State<GoodCounter> createState() => _GoodCounterState();
}

class _GoodCounterState extends State<GoodCounter> {
  int _counter = 0;
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Counter: $_counter'),
        const ExpensiveWidget(), // 不会重建！
        const AnotherExpensiveWidget(), // 不会重建！
      ],
    );
  }
}

// 规则：给每个不依赖state的widget加`const`
```

### 精准状态管理

```dart
// ❌ setState重建整棵树
setState(() => _value = newValue);

// ✅ ValueListenableBuilder：精准重建
class TargetedState extends StatelessWidget {
  final ValueNotifier<int> counter = ValueNotifier(0);
  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // 仅这部分在counter变化时重建
        ValueListenableBuilder<int>(
          valueListenable: counter,
          builder: (context, value, child) => Text('$value'),
          child: const Icon(Icons.star), // 不会重建！
        ),
        const ExpensiveWidget(), // 永不重建
      ],
    );
  }
}
```

### Riverpod/Provider最佳实践

```dart
// ❌ 错误：在build中读取整个provider
Widget build(BuildContext context) {
  final state = ref.watch(myProvider); // 任何变化都重建
  return Text(state.name);
}

// ✅ 正确：只选择需要的
Widget build(BuildContext context) {
  final name = ref.watch(myProvider.select((s) => s.name));
  return Text(name); // 仅name变化时重建
}
```

### ListView优化

```dart
// ❌ 错误：不用builder的ListView（渲染全部）
ListView(
  children: items.map((item) => ItemWidget(item)).toList(),
)

// ✅ 正确：ListView.builder（懒渲染）
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
  // 额外优化：
  itemExtent: 56, // 固定高度 = 更快布局
  cacheExtent: 100, // 预渲染距离
)

// ✅ 更好：ListView.separated用于分隔线
ListView.separated(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(items[index]),
  separatorBuilder: (context, index) => const Divider(),
)
```

### 图片优化

```dart
// ❌ 错误：无缓存，全分辨率
Image.network(url)

// ✅ 正确：缓存 + 合适尺寸
CachedNetworkImage(
  imageUrl: url,
  width: 100,
  height: 100,
  fit: BoxFit.cover,
  memCacheWidth: 200, // 2倍缓存给Retina
  memCacheHeight: 200,
  placeholder: (context, url) => const Skeleton(),
  errorWidget: (context, url, error) => const Icon(Icons.error),
)
```

### Dispose模式

```dart
class MyWidget extends StatefulWidget {
  @override
  State<MyWidget> createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  late final StreamSubscription _subscription;
  late final AnimationController _controller;
  late final TextEditingController _textController;
  
  @override
  void initState() {
    super.initState();
    _subscription = stream.listen((_) {});
    _controller = AnimationController(vsync: this);
    _textController = TextEditingController();
  }
  
  @override
  void dispose() {
    // 始终按创建的逆序dispose
    _textController.dispose();
    _controller.dispose();
    _subscription.cancel();
    super.dispose();
  }
  
  @override
  Widget build(BuildContext context) => Container();
}
```

### Flutter性能检查清单

```markdown
## 每个Widget前
- [ ] 已加const构造函数（无运行时参数时）
- [ ] 静态子widget加了const
- [ ] setState范围最小化
- [ ] Provider watch使用selector

## 每个列表前
- [ ] 使用ListView.builder（不是带children的ListView）
- [ ] 已提供itemExtent（固定高度时）
- [ ] 图片缓存有尺寸限制

## 每个动画前
- [ ] 使用Impeller（Flutter 3.16+）
- [ ] 避免Opacity widget（用FadeTransition）
- [ ] AnimationController用TickerProviderStateMixin

## 每次发布前
- [ ] 所有dispose()方法已实现
- [ ] 生产环境无print()
- [ ] 在profile/release模式测试
- [ ] DevTools性能叠加层已检查
```

---

## 4. 动画性能（双平台）

### 60fps的硬性要求

```
人眼检测：
├── < 24 fps → "幻灯片"（坏了）
├── 24-30 fps → "卡顿"（不舒服）
├── 30-45 fps → "明显不流畅"
├── 45-60 fps → "流畅"（可接受）
├── 60 fps → "丝滑"（目标）
└── 120 fps → "高端"（ProMotion设备）

绝不发布低于60fps的动画。
```

### GPU vs CPU动画

```
GPU加速（快）：                    CPU绑定（慢）：
├── transform: translate           ├── width、height
├── transform: scale               ├── top、left、right、bottom
├── transform: rotate              ├── margin、padding
├── opacity                        ├── border-radius（动画化）
└── （合成层，不占主线程）          └── box-shadow（动画化）

规则：仅动画transform和opacity。
其他一切都会触发布局重算。
```

### 动画时长指南

| 动画类型 | 时长 | 缓动 |
|----------|------|------|
| 微交互 | 100-200ms | ease-out |
| 标准转场 | 200-300ms | ease-out |
| 页面转场 | 300-400ms | ease-in-out |
| 复杂/戏剧性 | 400-600ms | ease-in-out |
| 加载骨架屏 | 1000-1500ms | linear（循环） |

### 弹簧物理

```javascript
// React Native Reanimated
withSpring(targetValue, {
  damping: 15,      // 多快稳定（越高越快停）
  stiffness: 150,   // 弹簧多"紧"（越高越快）
  mass: 1,          // 物体重量
})

// Flutter
SpringSimulation(
  SpringDescription(
    mass: 1,
    stiffness: 150,
    damping: 15,
  ),
  start,
  end,
  velocity,
)

// 自然感范围：
// Damping：10-20（弹跳到稳定）
// Stiffness：100-200（松到紧）
// Mass：0.5-2（轻到重）
```

---

## 5. 内存管理

### 常见内存泄漏

| 来源 | 平台 | 解决方案 |
|------|------|----------|
| 定时器 | 双平台 | 在cleanup/dispose中清除 |
| 事件监听器 | 双平台 | 在cleanup/dispose中移除 |
| 订阅 | 双平台 | 在cleanup/dispose中取消 |
| 大图片 | 双平台 | 限制缓存、调整尺寸 |
| 卸载后异步 | RN | isMounted检查或AbortController |
| 动画控制器 | Flutter | Dispose控制器 |

### 图片内存

```
图片内存 = 宽 × 高 × 4字节（RGBA）

1080p图片 = 1920 × 1080 × 4 = 8.3 MB
4K图片 = 3840 × 2160 × 4 = 33.2 MB

10张4K图片 = 332 MB → 应用崩溃！

规则：始终将图片调整到显示尺寸（或Retina的2-3倍）。
```

### 内存分析

```
React Native：
├── Flipper → Memory标签
├── Xcode Instruments（iOS）
└── Android Studio Profiler

Flutter：
├── DevTools → Memory标签
├── Observatory
└── flutter run --profile
```

---

## 6. 电池优化

### 电池消耗来源

| 来源 | 影响 | 缓解措施 |
|------|------|----------|
| **屏幕常亮** | 🔴 最高 | OLED用暗黑模式 |
| **GPS持续定位** | 🔴 很高 | 用显著变化 |
| **网络请求** | 🟡 高 | 批量、积极缓存 |
| **动画** | 🟡 中 | 低电量时减少 |
| **后台工作** | 🟡 中 | 推迟非关键任务 |
| **CPU计算** | 🟢 较低 | 卸载到后端 |

### OLED省电

```
OLED屏幕：黑色像素 = 关闭 = 零功耗

暗黑模式节省：
├── 纯黑（#000000）→ 最大节省
├── 深灰（#1a1a1a）→ 少量节省
├── 任何颜色 → 有功耗
└── 白色（#FFFFFF）→ 最大功耗

规则：暗黑模式背景用纯黑。
```

### 后台任务指南

```
iOS：
├── 后台刷新：受限，系统调度
├── 推送通知：用于重要更新
├── 后台模式：仅限位置、音频、VoIP
└── 后台任务：最多约30秒

Android：
├── WorkManager：系统调度，电池感知
├── 前台服务：用户可见，持续运行
├── JobScheduler：批量网络操作
└── Doze模式：尊重它，批量操作
```

---

## 7. 网络性能

### 离线优先架构

```
                    ┌──────────────┐
                    │     UI       │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   缓存       │ ← 先从缓存读取
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   网络       │ ← 从网络更新缓存
                    └──────────────┘

优势：
├── 即时UI（缓存数据无加载转圈）
├── 离线可用
├── 减少数据用量
└── 慢网络下更好UX
```

### 请求优化

```
批量：合并多个请求为一个
├── 10个小请求 → 1个批量请求
├── 减少连接开销
└── 对电池更好（无线电只开一次）

缓存：不重新获取未变化的数据
├── ETag/If-None-Match头
├── Cache-Control头
└── Stale-while-revalidate模式

压缩：减少载荷大小
├── gzip/brotli压缩
├── 只请求需要的字段（GraphQL）
└── 大列表分页
```

---

## 8. 性能测试

### 测试什么

| 指标 | 目标 | 工具 |
|------|------|------|
| **帧率** | ≥ 60fps | 性能叠加层 |
| **内存** | 稳定，无增长 | Profiler |
| **冷启动** | < 2秒 | 手动计时 |
| **TTI（可交互时间）** | < 3秒 | Lighthouse |
| **列表滚动** | 无卡顿 | 手动感受 |
| **动画流畅度** | 无掉帧 | 性能监视器 |

### 在真机上测试

```
⚠️ 绝不完全依赖：
├── 模拟器/仿真器（比真机快）
├── 开发模式（比release慢）
├── 仅高端设备

✅ 始终测试：
├── 低端Android（<$200手机）
├── 旧款iOS设备（iPhone 8或SE）
├── Release/Profile构建
└── 真实数据（不是10条）
```

### 性能监控检查清单

```markdown
## 开发期间
- [ ] 性能叠加层已开启
- [ ] 关注掉帧
- [ ] 内存使用稳定
- [ ] 无性能相关console警告

## 发布前
- [ ] 在低端设备上测试
- [ ] 长时间使用的内存分析
- [ ] 冷启动时间已测量
- [ ] 列表滚动用1000+条目测试
- [ ] 动画60fps已测试
- [ ] 网络在慢速3G下测试
```

---

## 9. 速查卡

### React Native要点

```javascript
// 列表：始终使用
<FlatList
  data={data}
  renderItem={useCallback(({item}) => <MemoItem item={item} />, [])}
  keyExtractor={useCallback(item => item.id, [])}
  getItemLayout={useCallback((_, i) => ({length: H, offset: H*i, index: i}), [])}
/>

// 动画：始终native
useNativeDriver: true

// 清理：始终存在
useEffect(() => {
  return () => cleanup();
}, []);
```

### Flutter要点

```dart
// Widget：始终const
const MyWidget()

// 列表：始终builder
ListView.builder(itemBuilder: ...)

// 状态：始终精准
ValueListenableBuilder() or ref.watch(provider.select(...))

// Dispose：始终清理
@override
void dispose() {
  controller.dispose();
  super.dispose();
}
```

### 动画目标

```
仅动画transform/opacity ← 动画什么
每帧16.67ms ← 时间预算
最低60fps ← 目标
低端Android ← 测试设备
```

---

> **切记：** 性能不是优化——它是基本质量。慢应用就是坏应用。在用户最差的设备上测试，而不是你最好的设备上。
