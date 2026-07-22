# 重构与整洁代码实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

## 指令

### 1. 代码分析
首先分析当前代码：

- **代码异味**
  - 长方法/函数（>20行）
  - 大类（>200行）
  - 重复代码块
  - 死代码和未使用变量
  - 复杂条件语句和嵌套循环
  - 魔法数字和硬编码值
  - 命名规范差
  - 组件间紧耦合
  - 缺失抽象

- **SOLID违规**
  - 单一职责原则违规
  - 开闭原则问题
  - 里氏替换问题
  - 接口隔离问题
  - 依赖倒置违规

- **性能问题**
  - 低效算法（O(n²)或更差）
  - 不必要的对象创建
  - 潜在内存泄漏
  - 阻塞操作
  - 缺失缓存机会

### 2. 重构策略

制定优先级重构计划：

**立即修复（高影响、低投入）**
- 将魔法数字提取为常量
- 改善变量和函数命名
- 删除死代码
- 简化布尔表达式
- 将重复代码提取为函数

**方法提取**
```
# Before
def process_order(order):
    # 50 lines of validation
    # 30 lines of calculation
    # 40 lines of notification

# After
def process_order(order):
    validate_order(order)
    total = calculate_order_total(order)
    send_order_notifications(order, total)
```

**类分解**
- 将职责提取到独立类
- 为依赖创建接口
- 实现依赖注入
- 组合优于继承

**模式应用**
- 工厂模式用于对象创建
- 策略模式用于算法变体
- 观察者模式用于事件处理
- 仓储模式用于数据访问
- 装饰器模式用于扩展行为

### 3. SOLID原则实战

提供每个SOLID原则的具体示例：

**单一职责原则（SRP）**
```python
# BEFORE: Multiple responsibilities in one class
class UserManager:
    def create_user(self, data):
        # Validate data
        # Save to database
        # Send welcome email
        # Log activity
        # Update cache
        pass

# AFTER: Each class has one responsibility
class UserValidator:
    def validate(self, data): pass

class UserRepository:
    def save(self, user): pass

class EmailService:
    def send_welcome_email(self, user): pass

class UserActivityLogger:
    def log_creation(self, user): pass

class UserService:
    def __init__(self, validator, repository, email_service, logger):
        self.validator = validator
        self.repository = repository
        self.email_service = email_service
        self.logger = logger

    def create_user(self, data):
        self.validator.validate(data)
        user = self.repository.save(data)
        self.email_service.send_welcome_email(user)
        self.logger.log_creation(user)
        return user
```

**开闭原则（OCP）**
```python
# BEFORE: Modification required for new discount types
class DiscountCalculator:
    def calculate(self, order, discount_type):
        if discount_type == "percentage":
            return order.total * 0.1
        elif discount_type == "fixed":
            return 10
        elif discount_type == "tiered":
            # More logic
            pass

# AFTER: Open for extension, closed for modification
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, order): pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def calculate(self, order):
        return order.total * self.percentage

class FixedDiscount(DiscountStrategy):
    def __init__(self, amount):
        self.amount = amount

    def calculate(self, order):
        return self.amount

class TieredDiscount(DiscountStrategy):
    def calculate(self, order):
        if order.total > 1000: return order.total * 0.15
        if order.total > 500: return order.total * 0.10
        return order.total * 0.05

class DiscountCalculator:
    def calculate(self, order, strategy: DiscountStrategy):
        return strategy.calculate(order)
```

**里氏替换原则（LSP）**
```typescript
// BEFORE: Violates LSP - Square changes Rectangle behavior
class Rectangle {
    constructor(protected width: number, protected height: number) {}

    setWidth(width: number) { this.width = width; }
    setHeight(height: number) { this.height = height; }
    area(): number { return this.width * this.height; }
}

class Square extends Rectangle {
    setWidth(width: number) {
        this.width = width;
        this.height = width; // Breaks LSP
    }
    setHeight(height: number) {
        this.width = height;
        this.height = height; // Breaks LSP
    }
}

// AFTER: Proper abstraction respects LSP
interface Shape {
    area(): number;
}

class Rectangle implements Shape {
    constructor(private width: number, private height: number) {}
    area(): number { return this.width * this.height; }
}

class Square implements Shape {
    constructor(private side: number) {}
    area(): number { return this.side * this.side; }
}
```

**接口隔离原则（ISP）**
```java
// BEFORE: Fat interface forces unnecessary implementations
interface Worker {
    void work();
    void eat();
    void sleep();
}

class Robot implements Worker {
    public void work() { /* work */ }
    public void eat() { /* robots don't eat! */ }
    public void sleep() { /* robots don't sleep! */ }
}

// AFTER: Segregated interfaces
interface Workable {
    void work();
}

interface Eatable {
    void eat();
}

interface Sleepable {
    void sleep();
}

class Human implements Workable, Eatable, Sleepable {
    public void work() { /* work */ }
    public void eat() { /* eat */ }
    public void sleep() { /* sleep */ }
}

class Robot implements Workable {
    public void work() { /* work */ }
}
```

**依赖倒置原则（DIP）**
```go
// BEFORE: High-level module depends on low-level module
type MySQLDatabase struct{}

func (db *MySQLDatabase) Save(data string) {}

type UserService struct {
    db *MySQLDatabase // Tight coupling
}

func (s *UserService) CreateUser(name string) {
    s.db.Save(name)
}

// AFTER: Both depend on abstraction
type Database interface {
    Save(data string)
}

type MySQLDatabase struct{}
func (db *MySQLDatabase) Save(data string) {}

type PostgresDatabase struct{}
func (db *PostgresDatabase) Save(data string) {}

type UserService struct {
    db Database // Depends on abstraction
}

func NewUserService(db Database) *UserService {
    return &UserService{db: db}
}

func (s *UserService) CreateUser(name string) {
    s.db.Save(name)
}
```

### 4. 完整重构场景

**场景1：遗留单体到整洁模块化架构**

```python
# BEFORE: 500-line monolithic file
class OrderSystem:
    def process_order(self, order_data):
        # Validation (100 lines)
        if not order_data.get('customer_id'):
            return {'error': 'No customer'}
        if not order_data.get('items'):
            return {'error': 'No items'}
        # Database operations mixed in (150 lines)
        conn = mysql.connector.connect(host='localhost', user='root')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders...")
        # Business logic (100 lines)
        total = 0
        for item in order_data['items']:
            total += item['price'] * item['quantity']
        # Email notifications (80 lines)
        smtp = smtplib.SMTP('smtp.gmail.com')
        smtp.sendmail(...)
        # Logging and analytics (70 lines)
        log_file = open('/var/log/orders.log', 'a')
        log_file.write(f"Order processed: {order_data}")

# AFTER: Clean, modular architecture
# domain/entities.py
from dataclasses import dataclass
from typing import List
from decimal import Decimal

@dataclass
class OrderItem:
    product_id: str
    quantity: int
    price: Decimal

@dataclass
class Order:
    customer_id: str
    items: List[OrderItem]

    @property
    def total(self) -> Decimal:
        return sum(item.price * item.quantity for item in self.items)

# domain/repositories.py
from abc import ABC, abstractmethod

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> str: pass

    @abstractmethod
    def find_by_id(self, order_id: str) -> Order: pass

# infrastructure/mysql_order_repository.py
class MySQLOrderRepository(OrderRepository):
    def __init__(self, connection_pool):
        self.pool = connection_pool

    def save(self, order: Order) -> str:
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO orders (customer_id, total) VALUES (%s, %s)",
                (order.customer_id, order.total)
            )
            return cursor.lastrowid

# application/validators.py
class OrderValidator:
    def validate(self, order: Order) -> None:
        if not order.customer_id:
            raise ValueError("Customer ID is required")
        if not order.items:
            raise ValueError("Order must contain items")
        if order.total <= 0:
            raise ValueError("Order total must be positive")

# application/services.py
class OrderService:
    def __init__(
        self,
        validator: OrderValidator,
        repository: OrderRepository,
        email_service: EmailService,
        logger: Logger
    ):
        self.validator = validator
        self.repository = repository
        self.email_service = email_service
        self.logger = logger

    def process_order(self, order: Order) -> str:
        self.validator.validate(order)
        order_id = self.repository.save(order)
        self.email_service.send_confirmation(order)
        self.logger.info(f"Order {order_id} processed successfully")
        return order_id
```

**场景2：代码异味解决目录**

```typescript
// SMELL: Long Parameter List
// BEFORE
function createUser(
    firstName: string,
    lastName: string,
    email: string,
    phone: string,
    address: string,
    city: string,
    state: string,
    zipCode: string
) {}

// AFTER: Parameter Object
interface UserData {
    firstName: string;
    lastName: string;
    email: string;
    phone: string;
    address: Address;
}

interface Address {
    street: string;
    city: string;
    state: string;
    zipCode: string;
}

function createUser(userData: UserData) {}

// SMELL: Feature Envy (method uses another class's data more than its own)
// BEFORE
class Order {
    calculateShipping(customer: Customer): number {
        if (customer.isPremium) {
            return customer.address.isInternational ? 0 : 5;
        }
        return customer.address.isInternational ? 20 : 10;
    }
}

// AFTER: Move method to the class it envies
class Customer {
    calculateShippingCost(): number {
        if (this.isPremium) {
            return this.address.isInternational ? 0 : 5;
        }
        return this.address.isInternational ? 20 : 10;
    }
}

class Order {
    calculateShipping(customer: Customer): number {
        return customer.calculateShippingCost();
    }
}

// SMELL: Primitive Obsession
// BEFORE
function validateEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

let userEmail: string = "test@example.com";

// AFTER: Value Object
class Email {
    private readonly value: string;

    constructor(email: string) {
        if (!this.isValid(email)) {
            throw new Error("Invalid email format");
        }
        this.value = email;
    }

    private isValid(email: string): boolean {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    toString(): string {
        return this.value;
    }
}

let userEmail = new Email("test@example.com"); // Validation automatic
```

### 5. 决策框架

**代码质量指标解读矩阵**

| 指标 | 良好 | 警告 | 危险 | 行动 |
|------|------|------|------|------|
| 圈复杂度 | <10 | 10-15 | >15 | 拆分为更小方法 |
| 方法行数 | <20 | 20-50 | >50 | 提取方法，应用SRP |
| 类行数 | <200 | 200-500 | >500 | 分解为多个类 |
| 测试覆盖率 | >80% | 60-80% | <60% | 立即添加单元测试 |
| 代码重复 | <3% | 3-5% | >5% | 提取公共代码 |
| 注释率 | 10-30% | <10%或>50% | N/A | 改善命名或减少噪音 |
| 依赖数量 | <5 | 5-10 | >10 | 应用DIP，使用门面 |

**重构ROI分析**

```
Priority = (Business Value × Technical Debt) / (Effort × Risk)

Business Value (1-10):
- Critical path code: 10
- Frequently changed: 8
- User-facing features: 7
- Internal tools: 5
- Legacy unused: 2

Technical Debt (1-10):
- Causes production bugs: 10
- Blocks new features: 8
- Hard to test: 6
- Style issues only: 2

Effort (hours):
- Rename variables: 1-2
- Extract methods: 2-4
- Refactor class: 4-8
- Architecture change: 40+

Risk (1-10):
- No tests, high coupling: 10
- Some tests, medium coupling: 5
- Full tests, loose coupling: 2
```

**技术债务优先级决策树**

```
Is it causing production bugs?
├─ YES → Priority: CRITICAL (Fix immediately)
└─ NO → Is it blocking new features?
    ├─ YES → Priority: HIGH (Schedule this sprint)
    └─ NO → Is it frequently modified?
        ├─ YES → Priority: MEDIUM (Next quarter)
        └─ NO → Is code coverage < 60%?
            ├─ YES → Priority: MEDIUM (Add tests)
            └─ NO → Priority: LOW (Backlog)
```

### 6. 现代代码质量实践（2024-2025）

**AI辅助代码审查集成**

```yaml
# .github/workflows/ai_review.yml
name: AI Code Review
on: [pull_request]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # GitHub Copilot Autofix
      - uses: github/copilot-autofix@v1
        with:
          languages: 'python,typescript,go'

      # CodeRabbit AI Review
      - uses: coderabbitai/action@v1
        with:
          review_type: 'comprehensive'
          focus: 'security,performance,maintainability'

      # Codium AI PR-Agent
      - uses: codiumai/pr-agent@v1
        with:
          commands: '/review --pr_reviewer.num_code_suggestions=5'
```

**静态分析工具链**

```python
# pyproject.toml
[tool.ruff]
line-length = 100
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "C90", # mccabe complexity
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "A",   # flake8-builtins
    "C4",  # flake8-comprehensions
    "SIM", # flake8-simplify
    "RET", # flake8-return
]

[tool.mypy]
strict = true
warn_unreachable = true
warn_unused_ignores = true

[tool.coverage]
fail_under = 80
```

```javascript
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended-type-checked",
    "plugin:sonarjs/recommended",
    "plugin:security/recommended"
  ],
  "plugins": ["sonarjs", "security", "no-loops"],
  "rules": {
    "complexity": ["error", 10],
    "max-lines-per-function": ["error", 20],
    "max-params": ["error", 3],
    "no-loops/no-loops": "warn",
    "sonarjs/cognitive-complexity": ["error", 15]
  }
}
```

**自动化重构建议**

```python
# Use Sourcery for automatic refactoring suggestions
# sourcery.yaml
rules:
  - id: convert-to-list-comprehension
  - id: merge-duplicate-blocks
  - id: use-named-expression
  - id: inline-immediately-returned-variable

# Example: Sourcery will suggest
# BEFORE
result = []
for item in items:
    if item.is_active:
        result.append(item.name)

# AFTER (auto-suggested)
result = [item.name for item in items if item.is_active]
```

**代码质量仪表盘配置**

```yaml
# sonar-project.properties
sonar.projectKey=my-project
sonar.sources=src
sonar.tests=tests
sonar.coverage.exclusions=**/*_test.py,**/test_*.py
sonar.python.coverage.reportPaths=coverage.xml

# Quality Gates
sonar.qualitygate.wait=true
sonar.qualitygate.timeout=300

# Thresholds
sonar.coverage.threshold=80
sonar.duplications.threshold=3
sonar.maintainability.rating=A
sonar.reliability.rating=A
sonar.security.rating=A
```

**安全导向重构**

```python
# Use Semgrep for security-aware refactoring
# .semgrep.yml
rules:
  - id: sql-injection-risk
    pattern: execute($QUERY)
    message: Potential SQL injection
    severity: ERROR
    fix: Use parameterized queries

  - id: hardcoded-secrets
    pattern: password = "..."
    message: Hardcoded password detected
    severity: ERROR
    fix: Use environment variables or secret manager

# CodeQL security analysis
# .github/workflows/codeql.yml
- uses: github/codeql-action/analyze@v3
  with:
    category: "/language:python"
    queries: security-extended,security-and-quality
```

### 7. 重构后实现

提供完整的重构代码：

**整洁代码原则**
- 有意义的命名（可搜索、可发音、无缩写）
- 函数只做一件事
- 无副作用
- 抽象层次一致
- DRY（不重复自己）
- YAGNI（你不会需要它）

**错误处理**
```python
# Use specific exceptions
class OrderValidationError(Exception):
    pass

class InsufficientInventoryError(Exception):
    pass

# Fail fast with clear messages
def validate_order(order):
    if not order.items:
        raise OrderValidationError("Order must contain at least one item")

    for item in order.items:
        if item.quantity <= 0:
            raise OrderValidationError(f"Invalid quantity for {item.name}")
```

**文档**
```python
def calculate_discount(order: Order, customer: Customer) -> Decimal:
    """
    Calculate the total discount for an order based on customer tier and order value.

    Args:
        order: The order to calculate discount for
        customer: The customer making the order

    Returns:
        The discount amount as a Decimal

    Raises:
        ValueError: If order total is negative
    """
```

### 8. 测试策略

为重构代码生成全面测试：

**单元测试**
```python
class TestOrderProcessor:
    def test_validate_order_empty_items(self):
        order = Order(items=[])
        with pytest.raises(OrderValidationError):
            validate_order(order)

    def test_calculate_discount_vip_customer(self):
        order = create_test_order(total=1000)
        customer = Customer(tier="VIP")
        discount = calculate_discount(order, customer)
        assert discount == Decimal("100.00")  # 10% VIP discount
```

**测试覆盖**
- 所有公共方法已测试
- 边界情况已覆盖
- 错误条件已验证
- 性能基准已包含

### 9. 重构前后对比

提供清晰对比展示改进：

**指标**
- 圈复杂度降低
- 每个方法行数
- 测试覆盖率提升
- 性能改进

**示例**
```
Before:
- processData(): 150 lines, complexity: 25
- 0% test coverage
- 3 responsibilities mixed

After:
- validateInput(): 20 lines, complexity: 4
- transformData(): 25 lines, complexity: 5
- saveResults(): 15 lines, complexity: 3
- 95% test coverage
- Clear separation of concerns
```

### 10. 迁移指南

若引入破坏性变更：

**分步迁移**
1. 安装新依赖
2. 更新导入语句
3. 替换废弃方法
4. 运行迁移脚本
5. 执行测试套件

**向后兼容**
```python
# Temporary adapter for smooth migration
class LegacyOrderProcessor:
    def __init__(self):
        self.processor = OrderProcessor()

    def process(self, order_data):
        # Convert legacy format
        order = Order.from_legacy(order_data)
        return self.processor.process(order)
```

### 11. 性能优化

包含具体优化：

**算法改进**
```python
# Before: O(n²)
for item in items:
    for other in items:
        if item.id == other.id:
            # process

# After: O(n)
item_map = {item.id: item for item in items}
for item_id, item in item_map.items():
    # process
```

**缓存策略**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def calculate_expensive_metric(data_id: str) -> float:
    # Expensive calculation cached
    return result
```

### 12. 代码质量检查清单

确保重构代码符合以下标准：

- [ ] 所有方法 < 20行
- [ ] 所有类 < 200行
- [ ] 无方法超过3个参数
- [ ] 圈复杂度 < 10
- [ ] 嵌套循环不超过2层
- [ ] 所有命名具有描述性
- [ ] 无注释掉的代码
- [ ] 格式一致
- [ ] 已添加类型提示（Python/TypeScript）
- [ ] 错误处理完善
- [ ] 已添加调试日志
- [ ] 已包含性能指标
- [ ] 文档完整
- [ ] 测试覆盖率 > 80%
- [ ] 无安全漏洞
- [ ] AI代码审查通过
- [ ] 静态分析干净（SonarQube/CodeQL）
- [ ] 无硬编码密钥

## 严重级别

对发现的问题和改进进行评级：

**严重**：安全漏洞、数据损坏风险、内存泄漏
**高**：性能瓶颈、可维护性阻碍、缺失测试
**中**：代码异味、轻微性能问题、文档不完整
**低**：风格不一致、命名小问题、锦上添花功能

## 输出格式

1. **分析摘要**：发现的关键问题及其影响
2. **重构计划**：带工作量估算的优先级变更列表
3. **重构代码**：带内联注释解释变更的完整实现
4. **测试套件**：所有重构组件的全面测试
5. **迁移指南**：采用变更的分步说明
6. **指标报告**：代码质量指标的前后对比
7. **AI审查结果**：自动化代码审查发现摘要
8. **质量仪表盘**：SonarQube/CodeQL结果链接

专注于提供切实可行的增量改进，可立即采用，同时保持系统稳定性。
