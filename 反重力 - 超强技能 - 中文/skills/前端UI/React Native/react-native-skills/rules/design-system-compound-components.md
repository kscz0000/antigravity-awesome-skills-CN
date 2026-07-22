---
title: Use Compound Components Over Polymorphic Children
impact: MEDIUM
impactDescription: 灵活组合，更清晰的 API
tags: design-system, components, composition
---

## 优先使用组合组件而非多态子元素

不要创建可以接受字符串的组件，除非它是文本节点。如果一个组件能接收字符串子元素，它必须是专门的 `*Text` 组件。对于按钮等同时包含 View（或 Pressable）和文本的组件，使用组合组件，如 `Button`、`ButtonText` 和 `ButtonIcon`。

**错误示例（多态子元素）：**

```tsx
import { Pressable, Text } from 'react-native'

type ButtonProps = {
  children: string | React.ReactNode
  icon?: React.ReactNode
}

function Button({ children, icon }: ButtonProps) {
  return (
    <Pressable>
      {icon}
      {typeof children === 'string' ? <Text>{children}</Text> : children}
    </Pressable>
  )
}

// Usage is ambiguous
<Button icon={<Icon />}>Save</Button>
<Button><CustomText>Save</CustomText></Button>
```

**正确示例（组合组件）：**

```tsx
import { Pressable, Text } from 'react-native'

function Button({ children }: { children: React.ReactNode }) {
  return <Pressable>{children}</Pressable>
}

function ButtonText({ children }: { children: React.ReactNode }) {
  return <Text>{children}</Text>
}

function ButtonIcon({ children }: { children: React.ReactNode }) {
  return <>{children}</>
}

// Usage is explicit and composable
<Button>
  <ButtonIcon><SaveIcon /></ButtonIcon>
  <ButtonText>Save</ButtonText>
</Button>

<Button>
  <ButtonText>Cancel</ButtonText>
</Button>
```
