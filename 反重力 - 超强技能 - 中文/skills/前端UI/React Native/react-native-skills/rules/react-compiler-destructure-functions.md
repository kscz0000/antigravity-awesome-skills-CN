---
title: 在渲染作用域顶部提前解构函数（React Compiler）
impact: HIGH
impactDescription: 稳定引用，减少重渲染
tags: rerender, hooks, performance, react-compiler
---

## 在渲染作用域顶部提前解构函数

此规则仅在使用 React Compiler 时适用。

在渲染作用域顶部从 hooks 中解构函数。绝不要通过点运算符访问对象来调用函数。解构后的函数是稳定引用；点运算访问会创建新引用，破坏记忆化。

**错误（通过点运算访问对象）：**

```tsx
import { useRouter } from 'expo-router'

function SaveButton(props) {
  const router = useRouter()

  // bad: react-compiler will key the cache on "props" and "router", which are objects that change each render
  const handlePress = () => {
    props.onSave()
    router.push('/success') // unstable reference
  }

  return <Button onPress={handlePress}>Save</Button>
}
```

**正确（提前解构）：**

```tsx
import { useRouter } from 'expo-router'

function SaveButton({ onSave }) {
  const { push } = useRouter()

  // good: react-compiler will key on push and onSave
  const handlePress = () => {
    onSave()
    push('/success') // stable reference
  }

  return <Button onPress={handlePress}>Save</Button>
}
```
