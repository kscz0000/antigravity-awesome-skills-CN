# Actor 日志参考

## JavaScript 和 TypeScript

**始终使用 `apify/log` 包进行日志记录** - 此包包含关键的安全逻辑，包括审查敏感数据（Apify token、API 密钥、凭据），以防止在日志中意外暴露。

### `apify/log` 中可用的日志级别

Apify 日志包提供以下日志方法：

- `log.debug()` - 调试级别日志（详细诊断信息）
- `log.info()` - 信息级别日志（一般信息消息）
- `log.warning()` - 警告级别日志（潜在问题情况的警告消息）
- `log.warningOnce()` - 警告级别日志（相同的警告消息仅记录一次）
- `log.error()` - 错误级别日志（失败的错误消息）
- `log.exception()` - 异常级别日志（带堆栈跟踪的异常）
- `log.perf()` - 性能级别日志（性能指标和计时信息）
- `log.deprecated()` - 弃用级别日志（关于弃用代码的警告）
- `log.softFail()` - 软失败日志（不停止执行的非关键失败，例如输入验证错误、跳过的项目）
- `log.internal()` - 内部级别日志（内部/系统消息）

### 最佳实践

- 使用 `log.debug()` 记录详细的操作级诊断（函数内部）
- 使用 `log.info()` 记录一般信息消息（API 请求、成功操作）
- 使用 `log.warning()` 记录潜在问题情况（验证失败、意外状态）
- 使用 `log.error()` 记录实际错误和失败
- 使用 `log.exception()` 记录带堆栈跟踪的捕获异常

## Python

**始终使用 `Actor.log` 进行日志记录** - 此日志器包含关键的安全逻辑，包括审查敏感数据（Apify token、API 密钥、凭据），以防止在日志中意外暴露。

### 可用的日志级别

Apify Actor 日志器提供以下日志方法：

- `Actor.log.debug()` - 调试级别日志（详细诊断信息）
- `Actor.log.info()` - 信息级别日志（一般信息消息）
- `Actor.log.warning()` - 警告级别日志（潜在问题情况的警告消息）
- `Actor.log.error()` - 错误级别日志（失败的错误消息）
- `Actor.log.exception()` - 异常级别日志（带堆栈跟踪的异常）

### 最佳实践

- 使用 `Actor.log.debug()` 记录详细的操作级诊断（函数内部）
- 使用 `Actor.log.info()` 记录一般信息消息（API 请求、成功操作）
- 使用 `Actor.log.warning()` 记录潜在问题情况（验证失败、意外状态）
- 使用 `Actor.log.error()` 记录实际错误和失败
- 使用 `Actor.log.exception()` 记录带堆栈跟踪的捕获异常
