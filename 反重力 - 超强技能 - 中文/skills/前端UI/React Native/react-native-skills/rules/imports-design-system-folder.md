---
title: Import from Design System Folder
impact: LOW
impactDescription: 支持全局变更和轻松重构
tags: imports, architecture, design-system
---

## 从设计系统文件夹导入

从设计系统文件夹重新导出依赖。应用代码从该处导入，而非直接从包导入。这支持全局变更和轻松重构。

**错误示例（直接从包导入）：**

```tsx
import { View, Text } from 'react-native'
import { Button } from '@ui/button'

function Profile() {
  return (
    <View>
      <Text>Hello</Text>
      <Button>Save</Button>
    </View>
  )
}
```

**正确示例（从设计系统导入）：**

```tsx
// components/view.tsx
import { View as RNView } from 'react-native'

// ideal: pick the props you will actually use to control implementation
export function View(
  props: Pick<React.ComponentProps<typeof RNView>, 'style' | 'children'>
) {
  return <RNView {...props} />
}
```

```tsx
// components/text.tsx
export { Text } from 'react-native'
```

```tsx
// components/button.tsx
export { Button } from '@ui/button'
```

```tsx
import { View } from '@/components/view'
import { Text } from '@/components/text'
import { Button } from '@/components/button'

function Profile() {
  return (
    <View>
      <Text>Hello</Text>
      <Button>Save</Button>
    </View>
  )
}
```

开始时简单重新导出即可。后续自定义时无需修改应用代码。
