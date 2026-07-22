# Error Handling Patterns 实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

# Error Handling Patterns

构建具有强大 error handling 策略的弹性应用程序，优雅地处理故障并提供出色的调试体验。

## 何时使用此技能

- 在新功能中实现 error handling
- 设计 error-resilient API
- 调试生产环境问题
- 提高应用程序可靠性
- 为用户和开发者创建更好的 error 消息
- 实现 retry 和 circuit breaker 模式
- 处理 async/concurrent error
- 构建容错分布式系统

## 核心概念

### 1. Error Handling 哲学

**Exception vs Result 类型：**
- **Exception**：传统 try-catch，中断控制流
- **Result 类型**：显式 success/failure，函数式方法
- **Error Code**：C 风格，需要纪律
- **Option/Maybe 类型**：用于可空值

**何时使用哪种：**
- Exception：意外错误、异常情况
- Result 类型：预期错误、验证失败
- Panic/Crash：不可恢复错误、编程 bug

### 2. Error 类别

**可恢复错误：**
- 网络超时
- 文件缺失
- 无效用户输入
- API 速率限制

**不可恢复错误：**
- 内存溢出
- 栈溢出
- 编程 bug（空指针等）

## 语言特定模式

### Python Error Handling

**自定义 Exception 层次结构：**
```python
class ApplicationError(Exception):
    """Base exception for all application errors."""
    def __init__(self, message: str, code: str = None, details: dict = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}
        self.timestamp = datetime.utcnow()

class ValidationError(ApplicationError):
    """Raised when validation fails."""
    pass

class NotFoundError(ApplicationError):
    """Raised when resource not found."""
    pass

class ExternalServiceError(ApplicationError):
    """Raised when external service fails."""
    def __init__(self, message: str, service: str, **kwargs):
        super().__init__(message, **kwargs)
        self.service = service

# Usage
def get_user(user_id: str) -> User:
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise NotFoundError(
            f"User not found",
            code="USER_NOT_FOUND",
            details={"user_id": user_id}
        )
    return user
```

**Context Manager 用于清理：**
```python
from contextlib import contextmanager

@contextmanager
def database_transaction(session):
    """Ensure transaction is committed or rolled back."""
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

# Usage
with database_transaction(db.session) as session:
    user = User(name="Alice")
    session.add(user)
    # Automatic commit or rollback
```

**指数退避 Retry：**
```python
import time
from functools import wraps
from typing import TypeVar, Callable

T = TypeVar('T')

def retry(
    max_attempts: int = 3,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,)
):
    """Retry decorator with exponential backoff."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = backoff_factor ** attempt
                        time.sleep(sleep_time)
                        continue
                    raise
            raise last_exception
        return wrapper
    return decorator

# Usage
@retry(max_attempts=3, exceptions=(NetworkError,))
def fetch_data(url: str) -> dict:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
```

### TypeScript/JavaScript Error Handling

**自定义 Error 类：**
```typescript
// Custom error classes
class ApplicationError extends Error {
    constructor(
        message: string,
        public code: string,
        public statusCode: number = 500,
        public details?: Record<string, any>
    ) {
        super(message);
        this.name = this.constructor.name;
        Error.captureStackTrace(this, this.constructor);
    }
}

class ValidationError extends ApplicationError {
    constructor(message: string, details?: Record<string, any>) {
        super(message, 'VALIDATION_ERROR', 400, details);
    }
}

class NotFoundError extends ApplicationError {
    constructor(resource: string, id: string) {
        super(
            `${resource} not found`,
            'NOT_FOUND',
            404,
            { resource, id }
        );
    }
}

// Usage
function getUser(id: string): User {
    const user = users.find(u => u.id === id);
    if (!user) {
        throw new NotFoundError('User', id);
    }
    return user;
}
```

**Result 类型模式：**
```typescript
// Result type for explicit error handling
type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

// Helper functions
function Ok<T>(value: T): Result<T, never> {
    return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
    return { ok: false, error };
}

// Usage
function parseJSON<T>(json: string): Result<T, SyntaxError> {
    try {
        const value = JSON.parse(json) as T;
        return Ok(value);
    } catch (error) {
        return Err(error as SyntaxError);
    }
}

// Consuming Result
const result = parseJSON<User>(userJson);
if (result.ok) {
    console.log(result.value.name);
} else {
    console.error('Parse failed:', result.error.message);
}

// Chaining Results
function chain<T, U, E>(
    result: Result<T, E>,
    fn: (value: T) => Result<U, E>
): Result<U, E> {
    return result.ok ? fn(result.value) : result;
}
```

**Async Error Handling：**
```typescript
// Async/await with proper error handling
async function fetchUserOrders(userId: string): Promise<Order[]> {
    try {
        const user = await getUser(userId);
        const orders = await getOrders(user.id);
        return orders;
    } catch (error) {
        if (error instanceof NotFoundError) {
            return [];  // Return empty array for not found
        }
        if (error instanceof NetworkError) {
            // Retry logic
            return retryFetchOrders(userId);
        }
        // Re-throw unexpected errors
        throw error;
    }
}

// Promise error handling
function fetchData(url: string): Promise<Data> {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new NetworkError(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Fetch failed:', error);
            throw error;
        });
}
```

### Rust Error Handling

**Result 和 Option 类型：**
```rust
use std::fs::File;
use std::io::{self, Read};

// Result type for operations that can fail
fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;  // ? operator propagates errors
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// Custom error types
#[derive(Debug)]
enum AppError {
    Io(io::Error),
    Parse(std::num::ParseIntError),
    NotFound(String),
    Validation(String),
}

impl From<io::Error> for AppError {
    fn from(error: io::Error) -> Self {
        AppError::Io(error)
    }
}

// Using custom error type
fn read_number_from_file(path: &str) -> Result<i32, AppError> {
    let contents = read_file(path)?;  // Auto-converts io::Error
    let number = contents.trim().parse()
        .map_err(AppError::Parse)?;   // Explicitly convert ParseIntError
    Ok(number)
}

// Option for nullable values
fn find_user(id: &str) -> Option<User> {
    users.iter().find(|u| u.id == id).cloned()
}

// Combining Option and Result
fn get_user_age(id: &str) -> Result<u32, AppError> {
    find_user(id)
        .ok_or_else(|| AppError::NotFound(id.to_string()))
        .map(|user| user.age)
}
```

### Go Error Handling

**显式 Error 返回：**
```go
// Basic error handling
func getUser(id string) (*User, error) {
    user, err := db.QueryUser(id)
    if err != nil {
        return nil, fmt.Errorf("failed to query user: %w", err)
    }
    if user == nil {
        return nil, errors.New("user not found")
    }
    return user, nil
}

// Custom error types
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed for %s: %s", e.Field, e.Message)
}

// Sentinel errors for comparison
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrInvalidInput = errors.New("invalid input")
)

// Error checking
user, err := getUser("123")
if err != nil {
    if errors.Is(err, ErrNotFound) {
        // Handle not found
    } else {
        // Handle other errors
    }
}

// Error wrapping and unwrapping
func processUser(id string) error {
    user, err := getUser(id)
    if err != nil {
        return fmt.Errorf("process user failed: %w", err)
    }
    // Process user
    return nil
}

// Unwrap errors
err := processUser("123")
if err != nil {
    var valErr *ValidationError
    if errors.As(err, &valErr) {
        fmt.Printf("Validation error: %s\n", valErr.Field)
    }
}
```

## 通用模式

### 模式 1：Circuit Breaker

防止分布式系统中的级联故障。

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, TypeVar

T = TypeVar('T')

class CircuitState(Enum):
    CLOSED = "closed"       # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: timedelta = timedelta(seconds=60),
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.success_threshold = success_threshold
        self.failure_count = 0
        self.success_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None

    def call(self, func: Callable[[], T]) -> T:
        if self.state == CircuitState.OPEN:
            if datetime.now() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

    def on_success(self):
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0

    def on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
circuit_breaker = CircuitBreaker()

def fetch_data():
    return circuit_breaker.call(lambda: external_api.get_data())
```

### 模式 2：Error 聚合

收集多个 error 而不是在第一个 error 时就失败。

```typescript
class ErrorCollector {
    private errors: Error[] = [];

    add(error: Error): void {
        this.errors.push(error);
    }

    hasErrors(): boolean {
        return this.errors.length > 0;
    }

    getErrors(): Error[] {
        return [...this.errors];
    }

    throw(): never {
        if (this.errors.length === 1) {
            throw this.errors[0];
        }
        throw new AggregateError(
            this.errors,
            `${this.errors.length} errors occurred`
        );
    }
}

// Usage: Validate multiple fields
function validateUser(data: any): User {
    const errors = new ErrorCollector();

    if (!data.email) {
        errors.add(new ValidationError('Email is required'));
    } else if (!isValidEmail(data.email)) {
        errors.add(new ValidationError('Email is invalid'));
    }

    if (!data.name || data.name.length < 2) {
        errors.add(new ValidationError('Name must be at least 2 characters'));
    }

    if (!data.age || data.age < 18) {
        errors.add(new ValidationError('Age must be 18 or older'));
    }

    if (errors.hasErrors()) {
        errors.throw();
    }

    return data as User;
}
```

### 模式 3：优雅降级

当 error 发生时提供回退功能。

```python
from typing import Optional, Callable, TypeVar

T = TypeVar('T')

def with_fallback(
    primary: Callable[[], T],
    fallback: Callable[[], T],
    log_error: bool = True
) -> T:
    """Try primary function, fall back to fallback on error."""
    try:
        return primary()
    except Exception as e:
        if log_error:
            logger.error(f"Primary function failed: {e}")
        return fallback()

# Usage
def get_user_profile(user_id: str) -> UserProfile:
    return with_fallback(
        primary=lambda: fetch_from_cache(user_id),
        fallback=lambda: fetch_from_database(user_id)
    )

# Multiple fallbacks
def get_exchange_rate(currency: str) -> float:
    return (
        try_function(lambda: api_provider_1.get_rate(currency))
        or try_function(lambda: api_provider_2.get_rate(currency))
        or try_function(lambda: cache.get_rate(currency))
        or DEFAULT_RATE
    )

def try_function(func: Callable[[], Optional[T]]) -> Optional[T]:
    try:
        return func()
    except Exception:
        return None
```

## 最佳实践

1. **快速失败**：尽早验证输入，快速失败
2. **保留上下文**：包含堆栈跟踪、元数据、时间戳
3. **有意义的消息**：解释发生了什么以及如何修复
4. **适当记录日志**：Error = 记录，预期失败 = 不要刷屏日志
5. **在正确层级处理**：在能有意义处理的地方捕获
6. **清理资源**：使用 try-finally、context manager、defer
7. **不要吞没错误**：记录或重新抛出，不要静默忽略
8. **类型安全的错误**：尽可能使用类型化的 error

```python
# Good error handling example
def process_order(order_id: str) -> Order:
    """Process order with comprehensive error handling."""
    try:
        # Validate input
        if not order_id:
            raise ValidationError("Order ID is required")

        # Fetch order
        order = db.get_order(order_id)
        if not order:
            raise NotFoundError("Order", order_id)

        # Process payment
        try:
            payment_result = payment_service.charge(order.total)
        except PaymentServiceError as e:
            # Log and wrap external service error
            logger.error(f"Payment failed for order {order_id}: {e}")
            raise ExternalServiceError(
                f"Payment processing failed",
                service="payment_service",
                details={"order_id": order_id, "amount": order.total}
            ) from e

        # Update order
        order.status = "completed"
        order.payment_id = payment_result.id
        db.save(order)

        return order

    except ApplicationError:
        # Re-raise known application errors
        raise
    except Exception as e:
        # Log unexpected errors
        logger.exception(f"Unexpected error processing order {order_id}")
        raise ApplicationError(
            "Order processing failed",
            code="INTERNAL_ERROR"
        ) from e
```

## 常见陷阱

- **捕获范围过广**：`except Exception` 会隐藏 bug
- **空 catch 块**：静默吞没 error
- **记录后重新抛出**：创建重复日志条目
- **未清理资源**：忘记关闭文件、连接
- **糟糕的 error 消息**：「发生错误」没有帮助
- **返回 error code**：使用 exception 或 Result 类型
- **忽略 async error**：未处理的 promise rejection

## 资源

- **references/exception-hierarchy-design.md**：设计 error 类层次结构
- **references/error-recovery-strategies.md**：不同场景的恢复模式
- **references/async-error-handling.md**：并发代码中的 error handling
- **assets/error-handling-checklist.md**：Error handling 审查清单
- **assets/error-message-guide.md**：编写有用的 error 消息
- **scripts/error-analyzer.py**：分析日志中的 error 模式
