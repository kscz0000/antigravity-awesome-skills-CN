# 高级调试技巧

## 程序卡死时

当程序运行但永不返回时,这本身就是信息——有东西卡住了。不要猜测;中断并观察。

```
Bug: program hangs (infinite loop or deadlock)

→ dap pause                         ← 在任意位置中断(立即返回 OK)
  [the already-blocking debug/continue/step call returns auto-context: location + locals]
  Stopped at process() · worker.py:55, locals: i=99999
→ dap threads                       ← 其他线程是否也卡住了?
→ dap eval "lock.locked()"          ← 验证死锁假设
Root cause: lock never released. Fix → dap stop.
```

检查:是单线程卡住(死循环、阻塞 I/O),还是多线程相互等待(死锁)?`pause` 停下的位置就是第一条线索。

## 深入挖掘复杂状态

当变量不透明或嵌套很深时,展开它:`dap inspect data --depth 2`。

## 并发 Bug

如果状态错了但代码路径看起来正确,想想:是否有另一个线程在并发修改状态?

**任何并发崩溃或卡死的首选动作:** 运行 `dap threads`,然后用 `dap thread <id>` 检查每个线程的栈——出问题的线程往往不是当前停下的那一个。

- **死锁模式**:两个或多个线程互相等待对方持有的资源。检查线程状态以确认。
- **竞态条件**:在两次停下之间发生变化的意外值。留意那些未加同步就访问的共享可变状态。

## 二分定位循环(狼栅栏法)

循环在未知迭代处出错。对它做二分查找:

```
dap debug app.py --break "app.py:45:i == 500"   # 1000 的中点
→ dap eval "is_valid(result)"                    # True → bug 在 500 之后
→ dap break add "app.py:45:i == 750"             # 更新条件
→ dap restart                                    # 保留新断点重启
```

~10 轮迭代就能在 1000 次循环中定位 bug,而不是 1000 次单步。