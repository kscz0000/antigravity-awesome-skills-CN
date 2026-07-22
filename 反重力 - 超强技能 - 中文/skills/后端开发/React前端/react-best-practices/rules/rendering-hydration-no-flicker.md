---
title: 防止水合不匹配而不闪烁
impact: MEDIUM
impactDescription: 避免视觉闪烁和水合错误
tags: rendering, ssr, hydration, localStorage, flicker
---

## 防止水合不匹配而不闪烁

当渲染依赖客户端存储（localStorage、cookies）的内容时，通过注入同步脚本在 React 水合前更新 DOM，避免 SSR 失败和水合后的闪烁。

**错误写法（破坏 SSR）：**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  // localStorage 在服务器上不可用 - 会抛出错误
  const theme = localStorage.getItem('theme') || 'light'
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

服务端渲染会失败，因为 `localStorage` 未定义。

**错误写法（视觉闪烁）：**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState('light')
  
  useEffect(() => {
    // 在水合后运行 - 导致可见闪烁
    const stored = localStorage.getItem('theme')
    if (stored) {
      setTheme(stored)
    }
  }, [])
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

组件先用默认值（`light`）渲染，然后在水合后更新，导致错误内容的可见闪烁。

**正确写法（无闪烁，无水合不匹配）：**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  return (
    <>
      <div id="theme-wrapper">
        {children}
      </div>
      <script
        dangerouslySetInnerHTML={{
          __html: `
            (function() {
              try {
                var theme = localStorage.getItem('theme') || 'light';
                var el = document.getElementById('theme-wrapper');
                if (el) el.className = theme;
              } catch (e) {}
            })();
          `,
        }}
      />
    </>
  )
}
```

内联脚本在显示元素前同步执行，确保 DOM 已有正确值。无闪烁，无水合不匹配。

此模式特别适用于主题切换、用户偏好、认证状态，以及任何需要立即渲染而不闪烁默认值的客户端数据。