---
name: mobile-design
description: "移动端设计系统（移动优先·触控优先·尊重平台）。涉及移动应用设计、移动端UI、触控交互、平台适配时使用。"
risk: unknown
source: community
date_added: "2026-02-27"
---
# 移动端设计系统

**(移动优先 · 触控优先 · 尊重平台)**

> **理念：** 触控优先。省电意识。尊重平台。离线可用。
> **核心法则：** 移动端不是缩小版的桌面端。
> **操作准则：** 先想约束，再想美观。

本技能存在的意义是**防止桌面思维、AI默认行为和不安全假设**在移动应用设计与构建中蔓延。

---

## 1. 移动端可行性与风险指数 (MFRI)

在设计或实现**任何移动功能或页面**之前，先评估可行性。

### MFRI 维度 (1–5)

| 维度 | 问题 |
|------|------|
| **平台明确度** | 目标平台（iOS / Android / 双端）是否已明确定义？ |
| **交互复杂度** | 手势、流程或导航有多复杂？ |
| **性能风险** | 是否涉及列表、动画、重状态或媒体？ |
| **离线依赖度** | 无网络时功能是否中断或降级？ |
| **无障碍风险** | 是否影响运动、视觉或认知无障碍？ |

### 评分公式

```
MFRI = (平台明确度 + 无障碍就绪度)
       − (交互复杂度 + 性能风险 + 离线依赖度)
```

**范围：** `-10 → +10`

### 解读

| MFRI | 含义 | 必要措施 |
| ---- | ---- | -------- |
| **6–10** | 安全 | 正常推进 |
| **3–5** | 中等 | 增加性能与UX验证 |
| **0–2** | 有风险 | 简化交互或架构 |
| **< 0** | 危险 | 实现前必须重新设计 |

---

## 2. 动手前必须思考

### ⛔ 停下：先问再假设（强制）

以下任何一项**未明确说明**时，必须在推进前提问：

| 方面 | 问题 | 原因 |
| ---- | ---- | ---- |
| 平台 | iOS、Android 还是双端？ | 影响导航、手势、排版 |
| 框架 | React Native、Flutter 还是原生？ | 决定性能和模式 |
| 导航 | Tab、Stack 还是 Drawer？ | 核心UX架构 |
| 离线 | 是否需要离线工作？ | 数据与同步策略 |
| 设备 | 仅手机还是包含平板？ | 布局与密度规则 |
| 受众 | 消费者、企业还是有无障碍需求？ | 触控与可读性 |

🚫 **绝不默认使用你偏好的技术栈或模式。**

---

## 3. 必读参考资料（强制执行）

### 通用（始终先读）

| 文件 | 用途 | 状态 |
| ---- | ---- | ---- |
| **mobile-design-thinking.md** | 反记忆化，强制上下文思考 | 🔴 必读优先 |
| **touch-psychology.md** | Fitts定律、拇指区、手势 | 🔴 必读 |
| **mobile-performance.md** | 60fps、内存、电池 | 🔴 必读 |
| **mobile-backend.md** | 离线同步、推送、API | 🔴 必读 |
| **mobile-testing.md** | 设备与E2E测试 | 🔴 必读 |
| **mobile-debugging.md** | 原生 vs JS调试 | 🔴 必读 |

### 平台特定（条件性）

| 平台 | 文件 |
| ---- | ---- |
| iOS | platform-ios.md |
| Android | platform-android.md |
| 跨平台 | 以上两份均需阅读 |

> ❌ 没读过平台文件，就不允许设计UI。

---

## 4. AI移动端反模式（硬性禁止）

### 🚫 性能禁忌（不可协商）

| ❌ 绝不 | 原因 | ✅ 始终 |
| ------- | ---- | ------- |
| 长列表用ScrollView | 内存爆炸 | FlatList / FlashList / ListView.builder |
| 内联renderItem | 所有行重渲染 | useCallback + memo |
| 用index作key | 重排bug | 稳定ID |
| JS线程动画 | 卡顿 | Native driver / GPU |
| 生产环境console.log | 阻塞JS线程 | 移除日志 |
| 不做memoization | 耗电+性能下降 | React.memo / const widgets |

---

### 🚫 触控与UX禁忌

| ❌ 绝不 | 原因 | ✅ 始终 |
| ------- | ---- | ------- |
| 触控区域 <44–48px | 误触 | 最小触控目标 |
| 仅手势操作 | 排除用户 | 提供按钮备选 |
| 无加载状态 | 感觉坏了 | 明确反馈 |
| 无错误恢复 | 死胡同 | 重试+提示 |
| 忽视平台规范 | 打破肌肉记忆 | iOS ≠ Android |

---

### 🚫 安全禁忌

| ❌ 绝不 | 原因 | ✅ 始终 |
| ------- | ---- | ------- |
| Token存AsyncStorage | 容易被盗 | SecureStore / Keychain |
| 硬编码密钥 | 可被逆向 | Env + 安全存储 |
| 无SSL Pinning | 中间人风险 | 证书Pinning |
| 日志记录敏感数据 | PII泄露 | 绝不记录密钥 |

---

## 5. 平台统一与分化矩阵

```
统一                            分化
──────────────────────────     ─────────────────────────
业务逻辑                        导航行为
数据模型                        手势
API契约                         图标
校验                            排版
错误语义                        选择器/对话框
```

### 平台默认值

| 元素 | iOS | Android |
| ---- | --- | ------- |
| 字体 | SF Pro | Roboto |
| 最小触控 | 44pt | 48dp |
| 返回 | 边缘滑动 | 系统返回 |
| 弹出层 | Bottom sheet | Dialog / sheet |
| 图标 | SF Symbols | Material Icons |

---

## 6. 移动端UX心理学（非可选）

### Fitts定律（触控现实）

* 手指 ≠ 光标
* 精度低
* 可达性比精确度更重要

**规则：**

* 主要CTA放在**拇指区**
* 破坏性操作推远
* 不做悬停假设

---

## 7. 性能准则

### React Native（必选模式）

```ts
const Row = React.memo(({ item }) => (
  <View><Text>{item.title}</Text></View>
));

const renderItem = useCallback(
  ({ item }) => <Row item={item} />,
  []
);

<FlatList
  data={items}
  renderItem={renderItem}
  keyExtractor={(i) => i.id}
  getItemLayout={(_, i) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * i,
    index: i,
  })}
/>
```

### Flutter（必选模式）

```dart
class Item extends StatelessWidget {
  const Item({super.key});

  @override
  Widget build(BuildContext context) {
    return const Text('Static');
  }
}
```

* 尽可能处处使用 `const`
* 仅做定向重建

---

## 8. 移动端强制检查点

编写**任何代码**前，必须完成：

```
🧠 移动端检查点

平台：     ___________
框架：    ___________
已读文件：   ___________

我将应用的3条原则：
1.
2.
3.

我将避免的反模式：
1.
2.
```

❌ 无法完成 → 回去阅读。

---

## 9. 框架决策树（权威）

```
需要OTA + 有Web团队 → React Native + Expo
高性能UI → Flutter
仅iOS → SwiftUI
仅Android → Compose
```

没有理由不要争论。

---

## 10. 发布就绪清单

### 上线前

* [ ] 触控目标 ≥ 44–48px
* [ ] 离线已处理
* [ ] 使用安全存储
* [ ] 列表已优化
* [ ] 日志已移除
* [ ] 在低端设备上测试过
* [ ] 无障碍标签已添加
* [ ] MFRI ≥ 3

---

## 11. 相关技能

* **frontend-design** – 视觉系统与组件
* **frontend-dev-guidelines** – RN/TS架构
* **backend-dev-guidelines** – 移动端安全API
* **error-tracking** – 崩溃与性能遥测

---

> **终极法则：**
> 移动用户注意力分散、频繁被打断、缺乏耐心——通常单手操作、网络差、电量低。
> **为这个现实而设计，否则你的应用会悄无声息地失败。**

---

## 使用时机
本技能适用于执行概述中描述的工作流或操作。

## 限制
- 仅在任务明确匹配上述范围时使用本技能。
- 输出不能替代特定环境的验证、测试或专家审查。
- 缺少必要输入、权限、安全边界或成功标准时，停下来提问。
