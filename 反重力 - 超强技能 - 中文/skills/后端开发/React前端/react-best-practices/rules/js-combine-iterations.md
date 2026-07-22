---
title: 合并多次数组迭代
impact: LOW-MEDIUM
impactDescription: 减少迭代次数
tags: javascript, arrays, loops, performance
---

## 合并多次数组迭代

多次 `.filter()` 或 `.map()` 调用会多次遍历数组。应合并为单个循环。

**错误做法（3 次迭代）：**

```typescript
const admins = users.filter(u => u.isAdmin)
const testers = users.filter(u => u.isTester)
const inactive = users.filter(u => !u.isActive)
```

**正确做法（1 次迭代）：**

```typescript
const admins: User[] = []
const testers: User[] = []
const inactive: User[] = []

for (const user of users) {
  if (user.isAdmin) admins.push(user)
  if (user.isTester) testers.push(user)
  if (!user.isActive) inactive.push(user)
}
```
