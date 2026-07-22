# 调试策略实施手册

本文件包含本技能所引用的详细模式、检查清单和代码示例。

## 核心原则

### 1. 科学方法

**1. 观察**：实际行为是什么？
**2. 假设**：可能的原因是什么？
**3. 实验**：验证你的假设
**4. 分析**：它证实还是证伪了你的理论？
**5. 重复**：直到找到根本原因

### 2. 调试心态

**不要假设：**
- "不可能是 X"——其实是
- "我没有改 Y"——还是要检查
- "在我机器上能跑"——找出原因

**应该做：**
- 稳定地复现
- 隔离问题
- 保留详细笔记
- 质疑一切
- 卡住时休息一下

### 3. 小黄鸭调试法

大声向小黄鸭、同事或自己解释你的代码和问题。常常能揭示问题所在。

## 系统化调试流程

### 阶段 1：复现

```markdown
## 复现检查清单

1. **能否复现？**
   - 总是？偶尔？随机？
   - 需要特定条件？
   - 其他人能否复现？

2. **创建最小复现**
   - 简化为最小示例
   - 移除无关代码
   - 隔离问题

3. **记录步骤**
   - 写下准确步骤
   - 注明环境详情
   - 捕获错误消息
```

### 阶段 2：收集信息

```markdown
## 信息收集

1. **错误消息**
   - 完整 stack trace
   - 错误码
   - 控制台/日志输出

2. **环境**
   - 操作系统版本
   - 语言/运行时版本
   - 依赖版本
   - 环境变量

3. **最近的变更**
   - Git 历史
   - 部署时间线
   - 配置变更

4. **影响范围**
   - 影响所有用户还是特定用户？
   - 所有浏览器还是特定浏览器？
   - 仅生产环境还是开发环境也有？
```

### 阶段 3：形成假设

```markdown
## 假设形成

基于收集到的信息，问：

1. **什么变了？**
   - 最近的代码变更
   - 依赖更新
   - 基础设施变更

2. **有什么不同？**
   - 正常 vs 出错环境
   - 正常 vs 出错用户
   - 之前 vs 之后

3. **哪里可能失败？**
   - 输入验证
   - 业务逻辑
   - 数据层
   - 外部服务
```

### 阶段 4：测试与验证

```markdown
## 测试策略

1. **二分查找**
   - 注释掉一半代码
   - 缩小问题范围
   - 重复直到找到

2. **添加日志**
   - 策略性地使用 console.log/print
   - 跟踪变量值
   - 追踪执行流程

3. **隔离组件**
   - 单独测试每个部分
   - Mock 依赖
   - 移除复杂性

4. **对比正常 vs 异常**
   - 对比配置
   - 对比环境
   - 对比数据
```

## 调试工具

### JavaScript/TypeScript 调试

```typescript
// Chrome DevTools Debugger
function processOrder(order: Order) {
    debugger;  // 执行在此暂停

    const total = calculateTotal(order);
    console.log('Total:', total);

    // 条件断点
    if (order.items.length > 10) {
        debugger;  // 仅在条件为真时中断
    }

    return total;
}

// Console 调试技巧
console.log('Value:', value);                    // 基础
console.table(arrayOfObjects);                   // 表格格式
console.time('operation'); /* code */ console.timeEnd('operation');  // 计时
console.trace();                                 // 堆栈跟踪
console.assert(value > 0, 'Value must be positive');  // 断言

// 性能分析
performance.mark('start-operation');
// ... 操作代码
performance.mark('end-operation');
performance.measure('operation', 'start-operation', 'end-operation');
console.log(performance.getEntriesByType('measure'));
```

**VS Code 调试器配置：**
```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "node",
            "request": "launch",
            "name": "Debug Program",
            "program": "${workspaceFolder}/src/index.ts",
            "preLaunchTask": "tsc: build - tsconfig.json",
            "outFiles": ["${workspaceFolder}/dist/**/*.js"],
            "skipFiles": ["<node_internals>/**"]
        },
        {
            "type": "node",
            "request": "launch",
            "name": "Debug Tests",
            "program": "${workspaceFolder}/node_modules/jest/bin/jest",
            "args": ["--runInBand", "--no-cache"],
            "console": "integratedTerminal"
        }
    ]
}
```

### Python 调试

```python
# 内置调试器 (pdb)
import pdb

def calculate_total(items):
    total = 0
    pdb.set_trace()  # 调试器从此处启动

    for item in items:
        total += item.price * item.quantity

    return total

# 断点 (Python 3.7+)
def process_order(order):
    breakpoint()  # 比 pdb.set_trace() 更便捷
    # ... 代码

# 事后调试
try:
    risky_operation()
except Exception:
    import pdb
    pdb.post_mortem()  # 在异常点调试

# IPython 调试 (ipdb)
from ipdb import set_trace
set_trace()  # 比 pdb 更好的界面

# 调试日志
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def fetch_user(user_id):
    logger.debug(f'Fetching user: {user_id}')
    user = db.query(User).get(user_id)
    logger.debug(f'Found user: {user}')
    return user

# 性能分析
import cProfile
import pstats

cProfile.run('slow_function()', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # 前 10 个最慢的
```

### Go 调试

```go
// Delve 调试器
// 安装: go install github.com/go-delve/delve/cmd/dlv@latest
// 运行: dlv debug main.go

import (
    "fmt"
    "runtime"
    "runtime/debug"
)

// 打印堆栈跟踪
func debugStack() {
    debug.PrintStack()
}

// 带调试的 panic 恢复
func processRequest() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Panic:", r)
            debug.PrintStack()
        }
    }()

    // ... 可能 panic 的代码
}

// 内存分析
import _ "net/http/pprof"
// 访问 http://localhost:6060/debug/pprof/

// CPU 分析
import (
    "os"
    "runtime/pprof"
)

f, _ := os.Create("cpu.prof")
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile()
// ... 要分析的代码
```

## 高级调试技巧

### 技巧 1：二分查找调试

```bash
# 使用 git bisect 查找回归
git bisect start
git bisect bad                    # 当前 commit 是坏的
git bisect good v1.0.0            # v1.0.0 是好的

# Git 检出中间的 commit
# 测试它，然后：
git bisect good   # 如果它正常
git bisect bad    # 如果它坏了

# 继续直到找到 bug
git bisect reset  # 完成后
```

### 技巧 2：差异调试

对比正常与异常：

```markdown
## 有什么不同？

| 方面         | 正常             | 异常             |
|--------------|------------------|------------------|
| 环境         | 开发环境         | 生产环境         |
| Node 版本    | 18.16.0          | 18.15.0          |
| 数据         | 空数据库         | 100 万条记录     |
| 用户         | 管理员           | 普通用户         |
| 浏览器       | Chrome           | Safari           |
| 时间         | 白天             | 午夜之后         |

假设：基于时间的问题？检查时区处理。
```

### 技巧 3：追踪调试

```typescript
// 函数调用追踪
function trace(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;

    descriptor.value = function(...args: any[]) {
        console.log(`Calling ${propertyKey} with args:`, args);
        const result = originalMethod.apply(this, args);
        console.log(`${propertyKey} returned:`, result);
        return result;
    };

    return descriptor;
}

class OrderService {
    @trace
    calculateTotal(items: Item[]): number {
        return items.reduce((sum, item) => sum + item.price, 0);
    }
}
```

### 技巧 4：内存泄漏检测

```typescript
// Chrome DevTools 内存分析器
// 1. 拍摄堆快照
// 2. 执行操作
// 3. 拍摄另一个堆快照
// 4. 对比快照

// Node.js 内存调试
if (process.memoryUsage().heapUsed > 500 * 1024 * 1024) {
    console.warn('High memory usage:', process.memoryUsage());

    // 生成堆转储
    require('v8').writeHeapSnapshot();
}

// 在测试中查找内存泄漏
let beforeMemory: number;

beforeEach(() => {
    beforeMemory = process.memoryUsage().heapUsed;
});

afterEach(() => {
    const afterMemory = process.memoryUsage().heapUsed;
    const diff = afterMemory - beforeMemory;

    if (diff > 10 * 1024 * 1024) {  // 10MB 阈值
        console.warn(`Possible memory leak: ${diff / 1024 / 1024}MB`);
    }
});
```

## 按问题类型分类的调试模式

### 模式 1：偶发 bug

```markdown
## 不稳定 bug 的策略

1. **添加大量日志**
   - 记录时间信息
   - 记录所有状态转换
   - 记录外部交互

2. **查找竞态条件**
   - 对共享状态的并发访问
   - 异步操作乱序完成
   - 缺少同步

3. **检查时间依赖**
   - setTimeout/setInterval
   - Promise 解析顺序
   - 动画帧时序

4. **压力测试**
   - 运行多次
   - 变化时序
   - 模拟负载
```

### 模式 2：性能问题

```markdown
## 性能调试

1. **先分析**
   - 不要盲目优化
   - 测量前后差异
   - 找到瓶颈

2. **常见原因**
   - N+1 查询
   - 不必要的重新渲染
   - 大数据量处理
   - 同步 I/O

3. **工具**
   - 浏览器 DevTools 性能面板
   - Lighthouse
   - Python: cProfile、line_profiler
   - Node: clinic.js、0x
```

### 模式 3：生产环境 bug

```markdown
## 生产环境调试

1. **收集证据**
   - 错误追踪 (Sentry、Bugsnag)
   - 应用日志
   - 用户报告
   - 指标/监控

2. **在本地复现**
   - 使用生产数据（脱敏后）
   - 匹配环境
   - 遵循准确步骤

3. **安全调查**
   - 不要修改生产环境
   - 使用 feature flag
   - 添加监控/日志
   - 在 staging 中测试修复
```

## 最佳实践

1. **先复现**：无法复现的问题无法修复
2. **隔离问题**：移除复杂性直到最小用例
3. **阅读错误消息**：它们通常很有帮助
4. **检查最近的变更**：大多数 bug 是最近引入的
5. **使用版本控制**：git bisect、blame、history
6. **适当休息**：新的视角看得更清楚
7. **记录发现**：帮助未来的你
8. **修复根本原因**：而不仅仅是症状

## 常见调试错误

- **同时做多项修改**：一次只改一个
- **不读错误消息**：阅读完整的 stack trace
- **假设问题很复杂**：通常很简单
- **在生产环境保留调试日志**：发布前移除
- **不使用调试器**：console.log 并不总是最佳选择
- **过早放弃**：坚持会得到回报
- **不测试修复**：验证它确实有效

## 快速调试检查清单

```markdown
## 卡住时，检查：

- [ ] 拼写错误（变量名拼错）
- [ ] 大小写敏感（fileName vs filename）
- [ ] null/undefined 值
- [ ] 数组索引越界
- [ ] 异步时序（竞态条件）
- [ ] 作用域问题（闭包、变量提升）
- [ ] 类型不匹配
- [ ] 缺少依赖
- [ ] 环境变量
- [ ] 文件路径（绝对路径 vs 相对路径）
- [ ] 缓存问题（清除缓存）
- [ ] 过期数据（刷新数据库）
```

## 资源

- **references/debugging-tools-guide.md**：全面的工具文档
- **references/performance-profiling.md**：性能调试指南
- **references/production-debugging.md**：调试线上系统
- **assets/debugging-checklist.md**：快速参考检查清单
- **assets/common-bugs.md**：常见 bug 模式
- **scripts/debug-helper.ts**：调试工具函数
