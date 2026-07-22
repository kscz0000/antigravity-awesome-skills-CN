# 重构与整洁代码实施手册

本文件包含技能引用的详细模式、检查清单和代码示例。

## 指令

### 1. 代码分析
首先，分析当前代码的以下问题：

- **代码异味**
  - 过长的方法/函数（>20行）
  - 过大的类（>200行）
  - 重复代码块
  - 死代码和未使用的变量
  - 复杂的条件判断和嵌套循环
  - 魔法数字和硬编码值
  - 命名不规范
  - 组件间紧耦合
  - 缺少抽象

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
  - 缺少缓存机会

### 2. 重构策略

制定优先级排序的重构计划：

**立即修复（高影响、低投入）**
- 将魔法数字提取为常量
- 改善变量和函数命名
- 删除死代码
- 简化布尔表达式
- 将重复代码提取为函数

**方法提取**
```
# 重构前
def process_order(order):
    # 50行验证逻辑
    # 30行计算逻辑
    # 40行通知逻辑

# 重构后
def process_order(order):
    validate_order(order)
    total = calculate_order_total(order)
    send_order_notifications(order, total)
```

**类拆分**
- 将职责提取到独立的类
- 为依赖创建接口
- 实现依赖注入
- 组合优于继承

**模式应用**
- 工厂模式用于对象创建
- 策略模式用于算法变体
- 观察者模式用于事件处理
- 仓库模式用于数据访问
- 装饰器模式用于扩展行为

### 3. SOLID原则实战

为每个SOLID原则提供具体示例：

**单一职责原则（SRP）**
```python
# 重构前：一个类承担多个职责
class UserManager:
    def create_user(self, data):
        # 验证数据
        # 保存到数据库
        # 发送欢迎邮件
        # 记录活动
        # 更新缓存
        pass

# 重构后：每个类只承担一个职责
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
# 重构前：新增折扣类型需要修改代码
class DiscountCalculator:
    def calculate(self, order, discount_type):
        if discount_type == "percentage":
            return order.total * 0.1
        elif discount_type == "fixed":
            return 10
        elif discount_type == "tiered":
            # 更多逻辑
            pass

# 重构后：对扩展开放，对修改关闭
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
// 重构前：违反LSP - Square改变了Rectangle的行为
class Rectangle {
    constructor(protected width: number, protected height: number) {}

    setWidth(width: number) { this.width = width; }
    setHeight(height: number) { this.height = height; }
    area(): number { return this.width * this.height; }
}

class Square extends Rectangle {
    setWidth(width: number) {
        this.width = width;
        this.height = width; // 破坏LSP
    }
    setHeight(height: number) {
        this.width = height;
        this.height = height; // 破坏LSP
    }
}

// 重构后：正确的抽象遵循LSP
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
// 重构前：臃肿接口强制实现不必要的方法
interface Worker {
    void work();
    void eat();
    void sleep();
}

class Robot implements Worker {
    public void work() { /* 工作 */ }
    public void eat() { /* 机器人不需要吃饭！ */ }
    public void sleep() { /* 机器人不需要睡觉！ */ }
}

// 重构后：分离的接口
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
    public void work() { /* 工作 */ }
    public void eat() { /* 吃饭 */ }
    public void sleep() { /* 睡觉 */ }
}

class Robot implements Workable {
    public void work() { /* 工作 */ }
}
```

**依赖倒置原则（DIP）**
```go
// 重构前：高层模块依赖低层模块
type MySQLDatabase struct{}

func (db *MySQLDatabase) Save(data string) {}

type UserService struct {
    db *MySQLDatabase // 紧耦合
}

func (s *UserService) CreateUser(name string) {
    s.db.Save(name)
}

// 重构后：两者都依赖抽象
type Database interface {
    Save(data string)
}

type MySQLDatabase struct{}
func (db *MySQLDatabase) Save(data string) {}

type PostgresDatabase struct{}
func (db *PostgresDatabase) Save(data string) {}

type UserService struct {
    db Database // 依赖抽象
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
# 重构前：500行的单体文件
class OrderSystem:
    def process_order(self, order_data):
        # 验证（100行）
        if not order_data.get('customer_id'):
            return {'error': 'No customer'}
        if not order_data.get('items'):
            return {'error': 'No items'}
        # 混杂的数据库操作（150行）
        conn = mysql.connector.connect(host='localhost', user='root')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders...")
        # 业务逻辑（100行）
        total = 0
        for item in order_data['items']:
            total += item['price'] * item['quantity']
        # 邮件通知（80行）
        smtp = smtplib.SMTP('smtp.gmail.com')
        smtp.sendmail(...)
        # 日志和分析（70行）
        log_file = open('/var/log/orders.log', 'a')
        log_file.write(f"Order processed: {order_data}")

# 重构后：整洁的模块化架构
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
// 异味：过长参数列表
// 重构前
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

// 重构后：参数对象
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

// 异味：特性嫉妒（方法更多使用另一个类的数据）
// 重构前
class Order {
    calculateShipping(customer: Customer): number {
        if (customer.isPremium) {
            return customer.address.isInternational ? 0 : 5;
        }
        return customer.address.isInternational ? 20 : 10;
    }
}

// 重构后：将方法移到它嫉妒的类
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

// 异味：基本类型偏执
// 重构前
function validateEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

let userEmail: string = "test@example.com";

// 重构后：值对象
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

let userEmail = new Email("test@example.com"); // 自动验证
```

### 5. 决策框架

**代码质量指标解读矩阵**

| 指标 | 良好 | 警告 | 危险 | 行动 |
|------|------|---------|----------|--------|
| 圈复杂度 | <10 | 10-15 | >15 | 拆分为更小的方法 |
| 方法行数 | <20 | 20-50 | >50 | 提取方法，应用SRP |
| 类行数 | <200 | 200-500 | >500 | 拆分为多个类 |
| 测试覆盖率 | >80% | 60-80% | <60% | 立即添加单元测试 |
| 代码重复率 | <3% | 3-5% | >5% | 提取公共代码 |
| 注释比例 | 10-30% | <10%或>50% | N/A | 改善命名或减少噪音 |
| 依赖数量 | <5 | 5-10 | >10 | 应用DIP，使用外观模式 |

**重构ROI分析**

```
优先级 = (业务价值 × 技术债务) / (投入 × 风险)

业务价值（1-10）：
- 关键路径代码：10
- 频繁变更：8
- 用户面向功能：7
- 内部工具：5
- 遗留未使用：2

技术债务（1-10）：
- 导致生产bug：10
- 阻碍新功能：8
- 难以测试：6
- 仅样式问题：2

投入（小时）：
- 重命名变量：1-2
- 提取方法：2-4
- 重构类：4-8
- 架构变更：40+

风险（1-10）：
- 无测试、高耦合：10
- 部分测试、中等耦合：5
- 完整测试、松耦合：2
```

**技术债务优先级决策树**

```
是否导致生产bug？
├─ 是 → 优先级：紧急（立即修复）
└─ 否 → 是否阻碍新功能？
    ├─ 是 → 优先级：高（本迭代安排）
    └─ 否 → 是否频繁修改？
        ├─ 是 → 优先级：中（下季度）
        └─ 否 → 代码覆盖率是否<60%？
            ├─ 是 → 优先级：中（添加测试）
            └─ 否 → 优先级：低（放入待办）
```

### 6. 现代代码质量实践（2024-2025）

**AI辅助代码审查集成**

```yaml
# .github/workflows/ai-review.yml
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

**自动重构建议**

```python
# 使用Sourcery获取自动重构建议
# sourcery.yaml
rules:
  - id: convert-to-list-comprehension
  - id: merge-duplicate-blocks
  - id: use-named-expression
  - id: inline-immediately-returned-variable

# 示例：Sourcery会建议
# 重构前
result = []
for item in items:
    if item.is_active:
        result.append(item.name)

# 重构后（自动建议）
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

# 质量门禁
sonar.qualitygate.wait=true
sonar.qualitygate.timeout=300

# 阈值
sonar.coverage.threshold=80
sonar.duplications.threshold=3
sonar.maintainability.rating=A
sonar.reliability.rating=A
sonar.security.rating=A
```

**安全导向重构**

```python
# 使用Semgrep进行安全感知重构
# .semgrep.yml
rules:
  - id: sql-injection-risk
    pattern: execute($QUERY)
    message: 潜在SQL注入风险
    severity: ERROR
    fix: 使用参数化查询

  - id: hardcoded-secrets
    pattern: password = "..."
    message: 检测到硬编码密码
    severity: ERROR
    fix: 使用环境变量或密钥管理器

# CodeQL安全分析
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
- 一致的抽象层次
- DRY（不要重复自己）
- YAGNI（你不会需要它）

**错误处理**
```python
# 使用特定异常
class OrderValidationError(Exception):
    pass

class InsufficientInventoryError(Exception):
    pass

# 快速失败，消息清晰
def validate_order(order):
    if not order.items:
        raise OrderValidationError("订单必须包含至少一个商品")

    for item in order.items:
        if item.quantity <= 0:
            raise OrderValidationError(f"{item.name}的数量无效")
```

**文档**
```python
def calculate_discount(order: Order, customer: Customer) -> Decimal:
    """
    根据客户等级和订单金额计算订单总折扣。

    Args:
        order: 要计算折扣的订单
        customer: 下单的客户

    Returns:
        折扣金额，Decimal类型

    Raises:
        ValueError: 订单金额为负数时
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
        assert discount == Decimal("100.00")  # VIP 10%折扣
```

**测试覆盖**
- 所有公共方法已测试
- 边界情况已覆盖
- 错误条件已验证
- 包含性能基准

### 9. 重构前后对比

提供清晰的改进对比：

**指标**
- 圈复杂度降低
- 每个方法的代码行数
- 测试覆盖率提升
- 性能改进

**示例**
```
重构前：
- processData(): 150行，复杂度：25
- 测试覆盖率：0%
- 混杂3个职责

重构后：
- validateInput(): 20行，复杂度：4
- transformData(): 25行，复杂度：5
- saveResults(): 15行，复杂度：3
- 测试覆盖率：95%
- 清晰的关注点分离
```

### 10. 迁移指南

如果引入破坏性变更：

**分步迁移**
1. 安装新依赖
2. 更新导入语句
3. 替换废弃方法
4. 运行迁移脚本
5. 执行测试套件

**向后兼容**
```python
# 平滑迁移的临时适配器
class LegacyOrderProcessor:
    def __init__(self):
        self.processor = OrderProcessor()

    def process(self, order_data):
        # 转换遗留格式
        order = Order.from_legacy(order_data)
        return self.processor.process(order)
```

### 11. 性能优化

包含具体优化：

**算法改进**
```python
# 重构前：O(n²)
for item in items:
    for other in items:
        if item.id == other.id:
            # 处理

# 重构后：O(n)
item_map = {item.id: item for item in items}
for item_id, item in item_map.items():
    # 处理
```

**缓存策略**
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def calculate_expensive_metric(data_id: str) -> float:
    # 昂贵计算被缓存
    return result
```

### 12. 代码质量检查清单

确保重构代码满足以下标准：

- [ ] 所有方法<20行
- [ ] 所有类<200行
- [ ] 没有方法超过3个参数
- [ ] 圈复杂度<10
- [ ] 没有超过2层的嵌套循环
- [ ] 所有命名具有描述性
- [ ] 没有注释掉的代码
- [ ] 格式一致
- [ ] 已添加类型提示（Python/TypeScript）
- [ ] 错误处理完善
- [ ] 已添加调试日志
- [ ] 包含性能指标
- [ ] 文档完整
- [ ] 测试覆盖率>80%
- [ ] 无安全漏洞
- [ ] AI代码审查通过
- [ ] 静态分析清洁（SonarQube/CodeQL）
- [ ] 无硬编码密钥

## 严重程度级别

对发现的问题和改进进行评级：

**紧急**：安全漏洞、数据损坏风险、内存泄漏
**高**：性能瓶颈、可维护性障碍、缺少测试
**中**：代码异味、轻微性能问题、文档不完整
**低**：样式不一致、轻微命名问题、锦上添花的功能

## 输出格式

1. **分析摘要**：发现的关键问题及其影响
2. **重构计划**：按优先级排序的变更列表，附带工作量估算
3. **重构代码**：完整实现，内联注释说明变更
4. **测试套件**：所有重构组件的全面测试
5. **迁移指南**：采用变更的分步说明
6. **指标报告**：代码质量指标的重构前后对比
7. **AI审查结果**：自动代码审查发现摘要
8. **质量仪表盘**：SonarQube/CodeQL结果链接

专注于交付切实可行、可立即采用的增量改进，同时保持系统稳定性。
