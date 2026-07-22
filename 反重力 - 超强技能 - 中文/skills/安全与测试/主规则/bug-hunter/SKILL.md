---
name: bug-hunter
description: "使用经过验证的调试技术系统性地查找和修复 Bug。从症状追溯到根本原因，实施修复，并防止回归。触发词：找bug、修bug、调试、debug、排查问题、修复错误、报错、异常排查"
category: development
risk: safe
source: community
date_added: "2026-03-05"
---

# Bug Hunter

使用经过验证的调试技术系统性地追踪并修复 Bug。不要猜测——跟随证据。

## 何时使用此技能

- 用户报告 Bug 或错误
- 某些功能未按预期工作
- 用户说"修复这个 bug"或"调试这个"
- 间歇性故障或异常行为
- 生产环境问题需要调查

## 调试流程

### 1. 复现 Bug

首先，让它稳定复现：

```
1. 获取确切的复现步骤
2. 尝试在本地复现
3. 记录触发条件
4. 记录错误信息/行为
5. 检查是每次都发生还是随机发生
```

如果无法复现，收集更多信息：
- 什么环境？（开发、测试、生产）
- 什么浏览器/设备？
- 用户之前做了什么操作？
- 有错误日志吗？

### 2. 收集证据

收集所有可用信息：

**检查日志：**
```bash
# 应用日志
tail -f logs/app.log

# 系统日志
journalctl -u myapp -f

# 浏览器控制台
# 打开开发者工具 → Console 标签页
```

**检查错误信息：**
- 完整堆栈跟踪
- 错误类型和信息
- 行号
- 时间戳

**检查状态：**
- 正在处理什么数据？
- 用户试图做什么？
- 数据库里有什么？
- 本地存储/Cookie 里有什么？

### 3. 形成假设

基于证据，猜测问题所在：

```
"登录超时是因为会话 Cookie 
在认证检查完成之前就过期了"

"表单失败是因为邮箱验证正则表达式
不支持加号"

"API 返回 500 是因为数据库查询
对特殊字符有语法错误"
```

### 4. 测试假设

证明或反驳你的猜测：

**添加日志：**
```javascript
console.log('Before API call:', userData);
const response = await api.login(userData);
console.log('After API call:', response);
```

**使用调试器：**
```javascript
debugger; // 执行在此暂停
const result = processData(input);
```

**隔离问题：**
```javascript
// 注释掉代码来缩小范围
// const result = complexFunction();
const result = { mock: 'data' }; // 使用模拟数据
```

### 5. 找到根本原因

追溯实际问题：

**常见根本原因：**
- Null/undefined 值
- 错误的数据类型
- 竞态条件
- 缺少错误处理
- 逻辑错误
- 差一错误
- Async/await 问题
- 缺少验证

**示例追溯：**
```
症状: "Cannot read property 'name' of undefined"
↓
位置: user.profile.name
↓
原因: user.profile 是 undefined
↓
原因: API 没有返回 profile
↓
原因: User ID 是 null
↓
根本原因: 登录时没有在会话中设置用户 ID
```

### 6. 实施修复

修复根本原因，而不是症状：

**错误修复（症状）：**
```javascript
// 只是隐藏错误
const name = user?.profile?.name || 'Unknown';
```

**正确修复（根本原因）：**
```javascript
// 确保登录时设置用户 ID
const login = async (credentials) => {
  const user = await authenticate(credentials);
  if (user) {
    session.userId = user.id; // 修复：设置用户 ID
    return user;
  }
  throw new Error('Invalid credentials');
};
```

### 7. 测试修复

验证确实有效：

```
1. 复现原始 Bug
2. 应用修复
3. 再次尝试复现（应该失败）
4. 测试边界情况
5. 测试相关功能
6. 运行现有测试
```

### 8. 防止回归

添加测试防止问题再次出现：

```javascript
test('login sets user ID in session', async () => {
  const user = await login({ email: 'test@example.com', password: 'pass' });
  
  expect(session.userId).toBe(user.id);
  expect(session.userId).not.toBeNull();
});
```

## 调试技术

### 二分查找

反复将问题空间减半：

```javascript
// Bug 发生在这行之前还是之后？
console.log('CHECKPOINT 1');
// ... 代码 ...
console.log('CHECKPOINT 2');
// ... 代码 ...
console.log('CHECKPOINT 3');
```

### 小黄鸭调试法

逐行大声解释代码。通常在解释过程中你会发现问题。

### 打印调试

策略性地使用 console.log：

```javascript
console.log('Input:', input);
console.log('After transform:', transformed);
console.log('Before save:', data);
console.log('Result:', result);
```

### 差异调试

对比正常和异常情况：
- 最近有什么变化？
- 环境之间有什么不同？
- 数据有什么不同？

### 时间旅行调试

使用 git 找出何时出问题：

```bash
git bisect start
git bisect bad  # 当前提交有问题
git bisect good abc123  # 这个旧提交正常
# Git 会检出提交让你测试
```

## 常见 Bug 模式

### Null/Undefined

```javascript
// Bug
const name = user.profile.name;

// 修复
const name = user?.profile?.name || 'Unknown';

// 更好的修复
if (!user || !user.profile) {
  throw new Error('User profile required');
}
const name = user.profile.name;
```

### 竞态条件

```javascript
// Bug
let data = null;
fetchData().then(result => data = result);
console.log(data); // null - 还没加载完

// 修复
const data = await fetchData();
console.log(data); // 正确的值
```

### 差一错误

```javascript
// Bug
for (let i = 0; i <= array.length; i++) {
  console.log(array[i]); // 最后一次迭代是 undefined
}

// 修复
for (let i = 0; i < array.length; i++) {
  console.log(array[i]);
}
```

### 类型强制转换

```javascript
// Bug
if (count == 0) { // 对 "", [], null 都为 true
  
// 修复
if (count === 0) { // 只对 0 为 true
```

### 异步没有 Await

```javascript
// Bug
const result = asyncFunction(); // 返回 Promise
console.log(result.data); // undefined

// 修复
const result = await asyncFunction();
console.log(result.data); // 正确的值
```

## 调试工具

### 浏览器开发者工具

```
Console: 查看日志和错误
Sources: 设置断点，逐步执行代码
Network: 检查 API 调用和响应
Application: 查看 Cookie、存储、缓存
Performance: 找出慢操作
```

### Node.js 调试

```javascript
// 内置调试器
node --inspect app.js

// 然后在 Chrome 中打开 chrome://inspect
```

### VS Code 调试

```json
// .vscode/launch.json
{
  "type": "node",
  "request": "launch",
  "name": "Debug App",
  "program": "${workspaceFolder}/app.js"
}
```

## 当你卡住时

1. 休息一下（认真说，离开 10 分钟）
2. 向别人解释（或者对着小黄鸭）
3. 搜索确切的错误信息
4. 检查是否是已知问题（GitHub issues、Stack Overflow）
5. 简化：创建最小复现
6. 从头开始：删除并重写有问题的代码
7. 寻求帮助（提供上下文，说明你尝试过什么）

## 文档模板

修复后，记录下来：

```markdown
## Bug: 登录 30 秒后超时

**症状：** 用户登录后立即被登出

**根本原因：** 会话 Cookie 在认证检查完成之前就过期了

**修复：** 在配置中将会话超时从 30 秒增加到 3600 秒

**修改的文件：**
- config/session.js (第 12 行)

**测试：** 验证登录可以持续 1 小时

**预防：** 添加了会话持久性测试
```

## 核心原则

- 先复现，后修复
- 跟随证据，不要猜测
- 修复根本原因，而非症状
- 彻底测试修复
- 添加测试防止回归
- 记录你学到的内容

## 相关技能

- `@systematic-debugging` - 高级调试
- `@test-driven-development` - 测试
- `@codebase-audit-pre-push` - 代码审查

## 限制
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家审查的替代品。
- 如果缺少所需的输入、权限、安全边界或成功标准，请停下来请求澄清。
