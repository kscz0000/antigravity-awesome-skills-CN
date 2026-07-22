---
title: 使用原生 Modal 替代基于 JS 的底部弹窗
impact: HIGH
impactDescription: 原生性能、手势、无障碍
tags: modals, bottom-sheet, native, react-navigation
---

## 使用原生 Modal 替代基于 JS 的底部弹窗

使用带 `presentationStyle="formSheet"` 的原生 `<Modal>` 或 React Navigation v7 的原生表单弹窗，替代基于 JS 的底部弹窗库。原生 Modal 内置手势、无障碍支持和更好的性能。底层基础组件应依赖原生 UI。

**错误（基于 JS 的底部弹窗）：**

```tsx
import BottomSheet from 'custom-js-bottom-sheet'

function MyScreen() {
  const sheetRef = useRef<BottomSheet>(null)

  return (
    <View style={{ flex: 1 }}>
      <Button onPress={() => sheetRef.current?.expand()} title='Open' />
      <BottomSheet ref={sheetRef} snapPoints={['50%', '90%']}>
        <View>
          <Text>Sheet content</Text>
        </View>
      </BottomSheet>
    </View>
  )
}
```

**正确（原生 Modal + formSheet）：**

```tsx
import { Modal, View, Text, Button } from 'react-native'

function MyScreen() {
  const [visible, setVisible] = useState(false)

  return (
    <View style={{ flex: 1 }}>
      <Button onPress={() => setVisible(true)} title='Open' />
      <Modal
        visible={visible}
        presentationStyle='formSheet'
        animationType='slide'
        onRequestClose={() => setVisible(false)}
      >
        <View>
          <Text>Sheet content</Text>
        </View>
      </Modal>
    </View>
  )
}
```

**正确（React Navigation v7 原生表单弹窗）：**

```tsx
// In your navigator
<Stack.Screen
  name='Details'
  component={DetailsScreen}
  options={{
    presentation: 'formSheet',
    sheetAllowedDetents: 'fitToContents',
  }}
/>
```

原生 Modal 开箱即用支持滑动关闭、正确的键盘避让和无障碍。
