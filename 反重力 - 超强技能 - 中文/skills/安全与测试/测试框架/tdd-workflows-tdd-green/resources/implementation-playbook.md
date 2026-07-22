# 绿灯阶段：简单函数实现手册

本文件包含该技能引用的详细模式、检查清单和代码示例。

在 TDD 绿灯阶段编写最简代码以使失败测试通过：

[深度思考：本工具使用 test-automator 智能体来编写使测试通过所需的最简代码。重点关注简洁性，避免过度工程化，同时确保所有测试变绿。]

## 适用场景

- TDD 循环中从红灯转到绿灯
- 编写最简行为以满足测试
- 刻意保持实现简单

## 不适用场景

- 因设计或性能原因进行重构
- 测试已通过，需要新增需求
- 需要完整的架构重设计

## 操作步骤

1. 审查失败测试，定位最小修复方案
2. 编写最简变更以通过下一个测试
3. 每次变更后运行测试确认进展
4. 记录捷径或技术债务，留待重构阶段处理

## 安全准则

- 不要绕过测试来使其通过
- 变更范围仅限于失败的行为

## 实现流程

使用 Task 工具，subagent_type="unit-testing::test-automator" 来编写最简通过代码。

提示词："编写最简代码使这些失败测试通过：$ARGUMENTS。遵循 TDD 绿灯阶段原则：

1. **实现前分析**
   - 审查所有失败测试及其错误信息
   - 识别使测试通过的最简路径
   - 将测试需求映射到最小实现需求
   - 避免过早优化或过度工程化
   - 仅关注使测试变绿，而非完美代码

2. **实现策略**
   - **伪装法**：适当时返回硬编码值
   - **显而易见实现**：当方案简单明确时
   - **三角测量法**：仅在多个测试要求时才泛化
   - 从最简单的测试开始，逐步推进
   - 一次一个测试——不要试图一次性全部通过

3. **代码结构指南**
   - 编写可能工作的最简代码
   - 不要添加测试未要求的功能
   - 初始阶段使用简单数据结构
   - 架构决策推迟到重构阶段
   - 保持方法/函数小而聚焦
   - 除非测试要求，否则不添加错误处理

4. **语言特定模式**
   - **JavaScript/TypeScript**：简单函数，初始阶段避免类
   - **Python**：先函数后类，简单返回值
   - **Java**：最小类结构，暂不使用模式
   - **C#**：基础实现，暂不使用接口
   - **Go**：简单函数，推迟 goroutine/channel
   - **Ruby**：尽可能先过程式后面向对象

5. **渐进式实现**
   - 用最简代码使第一个测试通过
   - 每次变更后运行测试验证进展
   - 仅为下一个失败测试添加刚好够的代码
   - 抵制超越测试需求实现的冲动
   - 跟踪技术债务，留待重构阶段
   - 记录假设和所采取的捷径

6. **常用绿灯阶段技巧**
   - 初始测试使用硬编码返回值
   - 有限测试用例使用简单 if/else
   - 仅在迭代测试需要时使用基本循环
   - 最简数据结构（数组优先于复杂对象）
   - 内存存储优先于数据库集成
   - 同步实现优先于异步实现

7. **成功标准**
   ✓ 所有测试通过（绿色）
   ✓ 无超出测试需求的额外功能
   ✓ 代码可读，即使不是最优
   ✓ 未破坏现有功能
   ✓ 实现时间最小化
   ✓ 重构路径清晰可辨

8. **应避免的反模式**
   - 镀金或添加未要求的功能
   - 过早实现设计模式
   - 无测试依据的复杂抽象
   - 无指标依据的性能优化
   - 绿灯阶段添加测试
   - 实现过程中重构
   - 忽略测试失败以继续推进

9. **实现指标**
   - 变绿时间：跟踪实现时长
   - 代码行数：衡量实现规模
   - 圈复杂度：初始阶段保持低位
   - 测试通过率：必须达到 100%
   - 代码覆盖率：验证所有路径已测试

10. **验证步骤**
    - 运行所有测试并确认通过
    - 验证现有测试未出现回归
    - 检查实现确实是最简的
    - 记录所产生的技术债务
    - 为重构阶段准备笔记

输出应包含：
- 完整实现代码
- 测试执行结果（全部绿色）
- 为后续重构所采取的捷径列表
- 实现时间指标
- 技术债务文档
- 重构阶段就绪评估"

## 实现后检查

实现完成后：
1. 运行完整测试套件确认所有测试通过
2. 验证现有测试未被破坏
3. 记录需要重构的区域
4. 检查实现确实是最简的
5. 记录实现时间以供指标统计

## 恢复流程

如果测试仍然失败：
- 仔细审查测试需求
- 检查是否有被误解的断言
- 添加最简代码以解决特定失败
- 避免从头重写的诱惑
- 考虑测试本身是否需要调整

## 集成点

- 承接 tdd-red.md 的测试创建
- 为 tdd-refactor.md 的改进做准备
- 更新测试覆盖率指标
- 触发 CI/CD 流水线验证
- 记录技术债务以供跟踪

## 最佳实践

- 拥抱本阶段的"够用就好"
- 速度优于完美（完美留到重构阶段）
- 先让它能跑，再让它跑对，最后让它跑快
- 信任重构阶段会改进代码
- 保持变更小而渐进
- 庆祝到达绿色状态！

## 完整实现示例

### 示例 1：最简 → 生产就绪（用户服务）

**测试需求：**
```typescript
describe('UserService', () => {
  it('should create a new user', async () => {
    const user = await userService.create({ email: 'test@example.com', name: 'Test' });
    expect(user.id).toBeDefined();
    expect(user.email).toBe('test@example.com');
  });

  it('should find user by email', async () => {
    await userService.create({ email: 'test@example.com', name: 'Test' });
    const user = await userService.findByEmail('test@example.com');
    expect(user).toBeDefined();
  });
});
```

**阶段 1：伪装法（最简）**
```typescript
class UserService {
  create(data: { email: string; name: string }) {
    return { id: '123', email: data.email, name: data.name };
  }

  findByEmail(email: string) {
    return { id: '123', email: email, name: 'Test' };
  }
}
```
*测试通过。实现明显是伪造的，但验证了测试结构。*

**阶段 2：简单真实实现**
```typescript
class UserService {
  private users: Map<string, User> = new Map();
  private nextId = 1;

  create(data: { email: string; name: string }) {
    const user = { id: String(this.nextId++), ...data };
    this.users.set(user.email, user);
    return user;
  }

  findByEmail(email: string) {
    return this.users.get(email) || null;
  }
}
```
*内存存储。测试通过。绿灯阶段够用。*

**阶段 3：生产就绪（重构阶段）**
```typescript
class UserService {
  constructor(private db: Database) {}

  async create(data: { email: string; name: string }) {
    const existing = await this.db.query('SELECT * FROM users WHERE email = ?', [data.email]);
    if (existing) throw new Error('User exists');

    const id = await this.db.insert('users', data);
    return { id, ...data };
  }

  async findByEmail(email: string) {
    return this.db.queryOne('SELECT * FROM users WHERE email = ?', [email]);
  }
}
```
*数据库集成、错误处理、验证——留待重构阶段。*

### 示例 2：API 优先实现（Express）

**测试需求：**
```javascript
describe('POST /api/tasks', () => {
  it('should create task and return 201', async () => {
    const res = await request(app)
      .post('/api/tasks')
      .send({ title: 'Test Task' });

    expect(res.status).toBe(201);
    expect(res.body.id).toBeDefined();
    expect(res.body.title).toBe('Test Task');
  });
});
```

**阶段 1：硬编码响应**
```javascript
app.post('/api/tasks', (req, res) => {
  res.status(201).json({ id: '1', title: req.body.title });
});
```
*测试立即通过。暂不需要逻辑。*

**阶段 2：简单逻辑**
```javascript
let tasks = [];
let nextId = 1;

app.post('/api/tasks', (req, res) => {
  const task = { id: String(nextId++), title: req.body.title };
  tasks.push(task);
  res.status(201).json(task);
});
```
*最小状态管理。准备接收更多测试。*

**阶段 3：分层架构（重构）**
```javascript
// Controller
app.post('/api/tasks', async (req, res) => {
  try {
    const task = await taskService.create(req.body);
    res.status(201).json(task);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Service layer
class TaskService {
  constructor(private repository: TaskRepository) {}

  async create(data: CreateTaskDto): Promise<Task> {
    this.validate(data);
    return this.repository.save(data);
  }
}
```
*重构阶段添加正确的关注点分离。*

### 示例 3：数据库集成（Django）

**测试需求：**
```python
def test_product_creation():
    product = Product.objects.create(name="Widget", price=9.99)
    assert product.id is not None
    assert product.name == "Widget"

def test_product_price_validation():
    with pytest.raises(ValidationError):
        Product.objects.create(name="Widget", price=-1)
```

**阶段 1：仅模型**
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```
*第一个测试通过。第二个失败——验证未实现。*

**阶段 2：添加验证**
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
```
*所有测试通过。添加了最小验证逻辑。*

**阶段 3：富领域模型（重构）**
```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['category', '-created_at'])]

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price cannot be negative")
        if self.price > 10000:
            raise ValidationError("Price exceeds maximum")

    def apply_discount(self, percentage: float) -> Decimal:
        return self.price * (1 - percentage / 100)
```
*按需添加额外功能、索引和业务逻辑。*

### 示例 4：React 组件实现

**测试需求：**
```typescript
describe('UserProfile', () => {
  it('should display user name', () => {
    render(<UserProfile user={{ name: 'John', email: 'john@test.com' }} />);
    expect(screen.getByText('John')).toBeInTheDocument();
  });

  it('should display email', () => {
    render(<UserProfile user={{ name: 'John', email: 'john@test.com' }} />);
    expect(screen.getByText('john@test.com')).toBeInTheDocument();
  });
});
```

**阶段 1：最简 JSX**
```typescript
interface UserProfileProps {
  user: { name: string; email: string };
}

const UserProfile: React.FC<UserProfileProps> = ({ user }) => (
  <div>
    <div>{user.name}</div>
    <div>{user.email}</div>
  </div>
);
```
*测试通过。无样式，无结构。*

**阶段 2：基本结构**
```typescript
const UserProfile: React.FC<UserProfileProps> = ({ user }) => (
  <div className="user-profile">
    <h2>{user.name}</h2>
    <p>{user.email}</p>
  </div>
);
```
*添加语义化 HTML 和 className 样式钩子。*

**阶段 3：生产组件（重构）**
```typescript
const UserProfile: React.FC<UserProfileProps> = ({ user }) => {
  const [isEditing, setIsEditing] = useState(false);

  return (
    <div className="user-profile" role="article" aria-label="User profile">
      <header>
        <h2>{user.name}</h2>
        <button onClick={() => setIsEditing(true)} aria-label="Edit profile">
          Edit
        </button>
      </header>
      <section>
        <p>{user.email}</p>
        {user.bio && <p>{user.bio}</p>}
      </section>
    </div>
  );
};
```
*渐进添加无障碍、交互和额外功能。*

## 决策框架

### 框架 1：伪装 vs 真实实现

**何时使用伪装法：**
- 新功能的第一个测试
- 复杂外部依赖（支付网关、API）
- 实现方案仍不确定
- 需要先验证测试结构
- 时间紧迫，需要看到全绿

**何时使用真实实现：**
- 第二或第三个测试揭示了模式
- 实现方案简单明确
- 伪造比写真实代码更复杂
- 需要测试集成点
- 测试明确要求真实行为

**决策矩阵：**
```
复杂度 低        | 高
         ↓         | ↓
简单   → 真实实现  | 先伪装，后真实
复杂   → 真实实现  | 伪装，评估替代方案
```

### 框架 2：复杂度权衡分析

**简洁度评分计算：**
```
评分 = (代码行数) + (圈复杂度 × 2) + (依赖数 × 3)

< 20  → 足够简单，直接实现
20-50 → 考虑更简替代方案
> 50  → 将复杂度推迟到重构阶段
```

**示例评估：**
```typescript
// 方案 A：直接实现（评分：45）
function calculateShipping(weight: number, distance: number, express: boolean): number {
  let base = weight * 0.5 + distance * 0.1;
  if (express) base *= 2;
  if (weight > 50) base += 10;
  if (distance > 1000) base += 20;
  return base;
}

// 方案 B：绿灯阶段最简方案（评分：15）
function calculateShipping(weight: number, distance: number, express: boolean): number {
  return express ? 50 : 25; // 伪装法，直到更多测试驱动真实逻辑
}
```
*绿灯阶段选择方案 B，随测试需求逐步演进到方案 A。*

### 框架 3：性能考量时机

**绿灯阶段：聚焦正确性**
```
❌ 避免：
- 缓存策略
- 数据库查询优化
- 算法复杂度改进
- 过早的内存优化

✓ 接受：
- O(n²) 如果让代码更简单
- 多次数据库查询
- 同步操作
- 低效但清晰的算法
```

**绿灯阶段何时需要关注性能：**
1. 性能是明确的测试需求
2. 实现会导致测试套件超时
3. 内存泄漏会导致测试崩溃
4. 资源耗尽阻碍测试执行

**性能测试集成：**
```typescript
// 在功能测试通过后添加性能测试
describe('Performance', () => {
  it('should handle 1000 users within 100ms', () => {
    const start = Date.now();
    for (let i = 0; i < 1000; i++) {
      userService.create({ email: `user${i}@test.com`, name: `User ${i}` });
    }
    expect(Date.now() - start).toBeLessThan(100);
  });
});
```

## 框架特定模式

### React 模式

**简单组件 → Hooks → Context：**
```typescript
// 绿灯阶段：仅 Props
const Counter = ({ count, onIncrement }) => (
  <button onClick={onIncrement}>{count}</button>
);

// 重构：添加 hooks
const Counter = () => {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
};

// 重构：提取到 context
const Counter = () => {
  const { count, increment } = useCounter();
  return <button onClick={increment}>{count}</button>;
};
```

### Django 模式

**函数视图 → 类视图 → 通用视图：**
```python
# 绿灯阶段：简单函数
def product_list(request):
    products = Product.objects.all()
    return JsonResponse({'products': list(products.values())})

# 重构：基于类的视图
class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        return JsonResponse({'products': list(products.values())})

# 重构：通用视图
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
```

### Express 模式

**内联 → 中间件 → 服务层：**
```javascript
// 绿灯阶段：内联逻辑
app.post('/api/users', (req, res) => {
  const user = { id: Date.now(), ...req.body };
  users.push(user);
  res.json(user);
});

// 重构：提取中间件
app.post('/api/users', validateUser, (req, res) => {
  const user = userService.create(req.body);
  res.json(user);
});

// 重构：完整分层
app.post('/api/users',
  validateUser,
  asyncHandler(userController.create)
);
```

## 重构阻力模式

### 模式 1：测试锚点

通过维护接口契约，在重构过程中保持测试绿色：

```typescript
// 原始实现（测试绿色）
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// 重构：添加税费计算（保持接口）
function calculateTotal(items: Item[]): number {
  const subtotal = items.reduce((sum, item) => sum + item.price, 0);
  const tax = subtotal * 0.1;
  return subtotal + tax;
}

// 测试仍然绿色，因为返回类型/行为未变
```

### 模式 2：并行实现

新旧实现并行运行：

```python
def process_order(order):
    # 旧实现（测试依赖此）
    result_old = legacy_process(order)

    # 新实现（并行测试）
    result_new = new_process(order)

    # 验证结果一致
    assert result_old == result_new, "Implementation mismatch"

    return result_old  # 保持测试绿色
```

### 模式 3：重构特性标志

```javascript
class PaymentService {
  processPayment(amount) {
    if (config.USE_NEW_PAYMENT_PROCESSOR) {
      return this.newPaymentProcessor(amount);
    }
    return this.legacyPaymentProcessor(amount);
  }
}
```

## 性能优先绿灯策略

### 策略 1：类型驱动开发

用类型引导最小实现：

```typescript
// 类型定义契约
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

// 绿灯阶段：内存实现
class InMemoryUserRepository implements UserRepository {
  private users = new Map<string, User>();

  async findById(id: string) {
    return this.users.get(id) || null;
  }

  async save(user: User) {
    this.users.set(user.id, user);
  }
}

// 重构：数据库实现（相同接口）
class DatabaseUserRepository implements UserRepository {
  constructor(private db: Database) {}

  async findById(id: string) {
    return this.db.query('SELECT * FROM users WHERE id = ?', [id]);
  }

  async save(user: User) {
    await this.db.insert('users', user);
  }
}
```

### 策略 2：契约测试集成

```typescript
// 定义契约
const userServiceContract = {
  create: {
    input: { email: 'string', name: 'string' },
    output: { id: 'string', email: 'string', name: 'string' }
  }
};

// 绿灯阶段：实现匹配契约
class UserService {
  create(data: { email: string; name: string }) {
    return { id: '123', ...data }; // 最简但符合契约
  }
}

// 契约测试确保合规
describe('UserService Contract', () => {
  it('should match create contract', () => {
    const result = userService.create({ email: 'test@test.com', name: 'Test' });
    expect(typeof result.id).toBe('string');
    expect(typeof result.email).toBe('string');
    expect(typeof result.name).toBe('string');
  });
});
```

### 策略 3：持续重构工作流

**绿灯阶段的微重构：**

```python
# 测试通过于此实现
def calculate_discount(price, customer_type):
    if customer_type == 'premium':
        return price * 0.8
    return price

# 立即微重构（测试仍然绿色）
DISCOUNT_RATES = {
    'premium': 0.8,
    'standard': 1.0
}

def calculate_discount(price, customer_type):
    rate = DISCOUNT_RATES.get(customer_type, 1.0)
    return price * rate
```

**安全重构检查清单：**
- ✓ 重构前测试绿色
- ✓ 一次只改一件事
- ✓ 每次变更后运行测试
- ✓ 每次成功重构后提交
- ✓ 仅改结构，不改行为

## 现代开发实践（2024/2025）

### 类型驱动开发

**Python 类型提示：**
```python
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class User:
    id: str
    email: str
    name: str

class UserService:
    def create(self, email: str, name: str) -> User:
        return User(id="123", email=email, name=name)

    def find_by_email(self, email: str) -> Optional[User]:
        return None  # 最简实现
```

**TypeScript 严格模式：**
```typescript
// 在 tsconfig.json 中启用严格模式
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}

// 类型引导实现
interface CreateUserDto {
  email: string;
  name: string;
}

class UserService {
  create(data: CreateUserDto): User {
    // 类型系统强制契约
    return { id: '123', email: data.email, name: data.name };
  }
}
```

### AI 辅助绿灯阶段

**使用 Copilot/AI 工具：**
1. 先写测试（人工驱动）
2. 让 AI 建议最小实现
3. 验证建议是否通过测试
4. 真正最简则接受，过度工程化则拒绝
5. 与 AI 迭代进入重构阶段

**AI 提示词模板：**
```
Given these failing tests:
[paste tests]

Provide the MINIMAL implementation that makes tests pass.
Do not add error handling, validation, or features beyond test requirements.
Focus on simplicity over completeness.
```

### 云原生模式

**本地 → 容器 → 云：**
```javascript
// 绿灯阶段：本地实现
class CacheService {
  private cache = new Map();

  get(key) { return this.cache.get(key); }
  set(key, value) { this.cache.set(key, value); }
}

// 重构：Redis 兼容接口
class CacheService {
  constructor(private redis) {}

  async get(key) { return this.redis.get(key); }
  async set(key, value) { return this.redis.set(key, value); }
}

// 生产：带降级的分布式缓存
class CacheService {
  constructor(private redis, private fallback) {}

  async get(key) {
    try {
      return await this.redis.get(key);
    } catch {
      return this.fallback.get(key);
    }
  }
}
```

### 可观测性驱动开发

**绿灯阶段添加可观测性钩子：**
```typescript
class OrderService {
  async createOrder(data: CreateOrderDto): Promise<Order> {
    console.log('[OrderService] Creating order', { data }); // 简单日志

    const order = { id: '123', ...data };

    console.log('[OrderService] Order created', { orderId: order.id }); // 成功日志

    return order;
  }
}

// 重构：结构化日志
class OrderService {
  constructor(private logger: Logger) {}

  async createOrder(data: CreateOrderDto): Promise<Order> {
    this.logger.info('order.create.start', { data });

    const order = await this.repository.save(data);

    this.logger.info('order.create.success', {
      orderId: order.id,
      duration: Date.now() - start
    });

    return order;
  }
}
```

待通过的测试：$ARGUMENTS
