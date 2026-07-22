---
title: 缓存重复的函数调用
impact: MEDIUM
impactDescription: 避免冗余计算
tags: javascript, cache, memoization, performance
---

## 缓存重复的函数调用

使用模块级 Map 缓存函数结果，适用于在渲染期间以相同输入重复调用同一函数的场景。

**错误做法（冗余计算）：**

```typescript
function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // slugify() 对相同的项目名称调用了 100+ 次
        const slug = slugify(project.name)
        
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**正确做法（缓存结果）：**

```typescript
// 模块级缓存
const slugifyCache = new Map<string, string>()

function cachedSlugify(text: string): string {
  if (slugifyCache.has(text)) {
    return slugifyCache.get(text)!
  }
  const result = slugify(text)
  slugifyCache.set(text, result)
  return result
}

function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // 每个唯一的项目名称只计算一次
        const slug = cachedSlugify(project.name)
        
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**适用于单值函数的更简洁模式：**

```typescript
let isLoggedInCache: boolean | null = null

function isLoggedIn(): boolean {
  if (isLoggedInCache !== null) {
    return isLoggedInCache
  }
  
  isLoggedInCache = document.cookie.includes('auth=')
  return isLoggedInCache
}

// 认证状态变更时清除缓存
function onAuthChange() {
  isLoggedInCache = null
}
```

使用 Map（而非 hook），这样它可以在任何地方使用：工具函数、事件处理器，而不仅限于 React 组件。

参考：[How we made the Vercel Dashboard twice as fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)
