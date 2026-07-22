---
name: performance-optimizer
description: "识别并修复代码、数据库和 API 中的性能瓶颈。优化前后进行测量，用数据证明改进效果。当用户要求'优化性能'、'加速'、'性能调优'时使用。"
category: development
risk: safe
source: community
date_added: "2026-03-05"
---

# 性能优化器

找到并修复性能瓶颈。测量、优化、验证。让代码飞起来。

## 何时使用此技能

- 应用运行缓慢或卡顿
- 用户抱怨性能问题
- 页面加载时间过长
- API 响应缓慢
- 数据库查询耗时过长
- 用户提到"慢"、"卡"、"性能"或"优化"

## 优化流程

### 1. 先测量

不测量就不要优化：

```javascript
// 测量执行时间
console.time('operation');
await slowOperation();
console.timeEnd('operation'); // operation: 2341ms
```

**需要测量的指标：**
- 页面加载时间
- API 响应时间
- 数据库查询时间
- 函数执行时间
- 内存使用量
- 网络请求数

### 2. 找到瓶颈

使用分析工具定位慢的部分：

**浏览器：**
```
DevTools → Performance 标签 → Record → Stop
查找长时间任务（红色条）
```

**Node.js：**
```bash
node --prof app.js
node --prof-process isolate-*.log > profile.txt
```

**数据库：**
```sql
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

### 3. 优化

优先修复最慢的部分（影响最大）。

## 常见优化方案

### 数据库查询

**问题：N+1 查询**
```javascript
// 错误：N+1 查询
const users = await db.users.find();
for (const user of users) {
  user.posts = await db.posts.find({ userId: user.id }); // N 次查询
}

// 正确：单次查询使用 JOIN
const users = await db.users.find()
  .populate('posts'); // 1 次查询
```

**问题：缺少索引**
```sql
-- 检查慢查询
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- 显示：Seq Scan（不好）

-- 添加索引
CREATE INDEX idx_users_email ON users(email);

-- 再次检查
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
-- 显示：Index Scan（好）
```

**问题：SELECT ***
```javascript
// 错误：获取所有列
const users = await db.query('SELECT * FROM users');

// 正确：只获取需要的列
const users = await db.query('SELECT id, name, email FROM users');
```

**问题：无分页**
```javascript
// 错误：返回所有记录
const users = await db.users.find();

// 正确：分页查询
const users = await db.users.find()
  .limit(20)
  .skip((page - 1) * 20);
```

### API 性能

**问题：无缓存**
```javascript
// 错误：每次都查询数据库
app.get('/api/stats', async (req, res) => {
  const stats = await db.stats.calculate(); // 慢
  res.json(stats);
});

// 正确：缓存 5 分钟
const cache = new Map();
app.get('/api/stats', async (req, res) => {
  const cached = cache.get('stats');
  if (cached && Date.now() - cached.time < 300000) {
    return res.json(cached.data);
  }
  
  const stats = await db.stats.calculate();
  cache.set('stats', { data: stats, time: Date.now() });
  res.json(stats);
});
```

**问题：顺序执行**
```javascript
// 错误：顺序执行（慢）
const user = await getUser(id);
const posts = await getPosts(id);
const comments = await getComments(id);
// 总耗时：300ms + 200ms + 150ms = 650ms

// 正确：并行执行（快）
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id)
]);
// 总耗时：max(300ms, 200ms, 150ms) = 300ms
```

**问题：响应体过大**
```javascript
// 错误：返回所有数据
res.json(users); // 5MB 响应

// 正确：只返回需要的字段
res.json(users.map(u => ({
  id: u.id,
  name: u.name,
  email: u.email
}))); // 500KB 响应
```

### 前端性能

**问题：不必要的重渲染**
```javascript
// 错误：父组件更新时每次都重渲染
function UserList({ users }) {
  return users.map(user => <UserCard user={user} />);
}

// 正确：使用记忆化
const UserCard = React.memo(({ user }) => {
  return <div>{user.name}</div>;
});
```

**问题：包体积过大**
```javascript
// 错误：导入整个库
import _ from 'lodash'; // 70KB

// 正确：只导入需要的部分
import debounce from 'lodash/debounce'; // 2KB
```

**问题：无代码分割**
```javascript
// 错误：所有代码打包在一起
import HeavyComponent from './HeavyComponent';

// 正确：懒加载
const HeavyComponent = React.lazy(() => import('./HeavyComponent'));
```

**问题：图片未优化**
```html
<!-- 错误：大图片 -->
<img src="photo.jpg" /> <!-- 5MB -->

<!-- 正确：优化并响应式 -->
<img 
  src="photo-small.webp" 
  srcset="photo-small.webp 400w, photo-large.webp 800w"
  loading="lazy"
  width="400"
  height="300"
/> <!-- 50KB -->
```

### 算法优化

**问题：低效算法**
```javascript
// 错误：O(n²) - 嵌套循环
function findDuplicates(arr) {
  const duplicates = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j]) duplicates.push(arr[i]);
    }
  }
  return duplicates;
}

// 正确：O(n) - 使用 Set 单次遍历
function findDuplicates(arr) {
  const seen = new Set();
  const duplicates = new Set();
  for (const item of arr) {
    if (seen.has(item)) duplicates.add(item);
    seen.add(item);
  }
  return Array.from(duplicates);
}
```

**问题：重复计算**
```javascript
// 错误：每次都重新计算
function getTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
// 在渲染中调用 100 次

// 正确：使用记忆化
const getTotal = useMemo(() => {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}, [items]);
```

### 内存优化

**问题：内存泄漏**
```javascript
// 错误：未清理事件监听器
useEffect(() => {
  window.addEventListener('scroll', handleScroll);
  // 内存泄漏！
}, []);

// 正确：清理
useEffect(() => {
  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
```

**问题：大文件加载到内存**
```javascript
// 错误：将整个文件加载到内存
const data = fs.readFileSync('huge-file.txt'); // 1GB

// 正确：使用流
const stream = fs.createReadStream('huge-file.txt');
stream.on('data', chunk => process(chunk));
```

## 测量优化效果

始终在优化前后进行测量：

```javascript
// 优化前
console.time('query');
const users = await db.users.find();
console.timeEnd('query');
// query: 2341ms

// 优化后（添加索引）
console.time('query');
const users = await db.users.find();
console.timeEnd('query');
// query: 23ms

// 提升：快了 100 倍！
```

## 性能预算

设定目标：

```
页面加载：< 2 秒
API 响应：< 200ms
数据库查询：< 50ms
包体积：< 200KB
可交互时间：< 3 秒
```

## 工具推荐

**浏览器：**
- Chrome DevTools Performance 标签
- Lighthouse（审计）
- Network 标签（瀑布图）

**Node.js：**
- `node --prof`（性能分析）
- `clinic`（诊断）
- `autocannon`（压力测试）

**数据库：**
- `EXPLAIN ANALYZE`（查询计划）
- 慢查询日志
- 数据库分析器

**监控：**
- New Relic
- Datadog
- Sentry Performance

## 快速见效的优化

投入小、收益大的优化：

1. **添加数据库索引**到常用查询列
2. **启用 gzip 压缩**
3. **添加缓存**处理耗时操作
4. **懒加载**图片和重型组件
5. **使用 CDN** 加速静态资源
6. **压缩** JavaScript/CSS
7. **移除未使用的依赖**
8. **使用分页**替代加载全部数据
9. **优化图片**（WebP、适当尺寸）
10. **启用 HTTP/2**

## 优化清单

- [ ] 测量当前性能
- [ ] 定位瓶颈
- [ ] 应用优化
- [ ] 测量改进效果
- [ ] 验证功能正常
- [ ] 确认无新 bug
- [ ] 记录变更

## 何时不要优化

- 过早优化（等真的慢了再优化）
- 微优化（页面要 5 秒，省 1ms 没意义）
- 可读性比微小提速更重要
- 已经足够快了

## 核心原则

- 优化前先测量
- 优先修复最大瓶颈
- 优化后测量证明改进
- 不要为微小提速牺牲可读性
- 在类生产环境进行分析
- 遵循 80/20 法则（20% 的代码导致 80% 的慢）

## 相关技能

- `@database-design` - 查询优化
- `@codebase-audit-pre-push` - 代码审查
- `@bug-hunter` - 调试

## 限制
- 仅在任务明确匹配上述范围时使用此技能。
- 输出不能替代针对特定环境的验证、测试或专家审查。
- 如果缺少必要输入、权限、安全边界或成功标准，请停下来寻求澄清。